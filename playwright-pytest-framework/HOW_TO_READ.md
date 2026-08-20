# Как читать фреймворк автотестов с нуля
# Python · pytest · Playwright

Гайд для подготовки к собеседованию Full Stack QA.
Учись на папке `playwright-pytest-framework/` в этом репозитории.

---

## 1. Цель: не «выучить файлы», а понять поток выполнения

На собеседовании обычно дают репозиторий и спрашивают:

> «Расскажи, как устроен фреймворк. С чего начнёшь?»

Правильный ответ — **маршрут чтения**:

```
зависимости → конфиг запуска → фикстуры → page objects → тесты → отчёты/CI
```

Ты идёшь **сверху вниз по runtime**, а не «открываю всё подряд».

---

## 2. Карта этого фреймворка

```
playwright-pytest-framework/
├── requirements.txt      # что установлено (pytest, playwright, allure…)
├── pytest.ini            # как pytest находит и запускает тесты
├── .env.example          # какие переменные окружения нужны
├── conftest.py           # фикстуры = «склейка» всего рантайма  ← КЛЮЧ
├── config/
│   └── settings.py       # BASE_URL, креды, таймауты
├── pages/
│   ├── base_page.py      # общие действия (open/click/fill/expect)
│   └── login_page.py     # локаторы + действия конкретной страницы
├── tests/
│   └── test_login.py     # бизнес-сценарии (короткие!)
└── utils/
    └── helpers.py        # то, что не про конкретную страницу
```

---

## 3. Порядок чтения (делай так на любом проекте)

### Шаг 0 — 2 минуты на обзор дерева

Спроси себя:

| Вопрос | Зачем |
|--------|--------|
| Где тесты? | `tests/`, `test_*.py`, `*_test.py` |
| Где page objects? | `pages/`, `page_objects/`, `ui/` |
| Где API-клиент? | `api/`, `clients/`, `services/` (full stack) |
| Где фикстуры? | `conftest.py` (может быть несколько уровней) |
| Чем запускают? | `pytest`, `make test`, CI yaml |

### Шаг 1 — зависимости (`requirements.txt` / `pyproject.toml`)

Ищи стек:

- **раннер**: `pytest`
- **UI**: `playwright` + `pytest-playwright`
- **API** (часто рядом): `requests` / `httpx`
- **отчёты**: `allure-pytest`
- **конфиг**: `python-dotenv`, `pydantic-settings`

На собеседовании: *«Вижу pytest + Playwright, значит UI E2E; allure — отчётность.»*

### Шаг 2 — как запускают (`pytest.ini`)

Читай:

- `testpaths` — где лежат тесты
- `addopts` — дефолтные флаги (`--browser`, `-v`, markers)
- `markers` — как фильтруют (`smoke`, `regression`)

Команды, которые стоит уметь сказать вслух:

```bash
pytest                          # всё
pytest -m smoke                 # только smoke
pytest tests/test_login.py -k success
pytest --headed                 # с UI (если headless по умолчанию)
```

### Шаг 3 — сердце фреймворка: `conftest.py`

Это **самый важный файл** для интервью.

Читай фикстуры и их `scope`:

| Fixture | Scope | Смысл |
|---------|-------|--------|
| `settings` | session | конфиг один раз |
| `browser` | session | один браузер на прогон |
| `context` | function | чистая сессия на тест |
| `page` | function | вкладка |
| `login_page` | function | готовый Page Object |

**Цепочка вызовов в этом проекте:**

```
settings → browser → context → page → login_page → test_*
```

Запомни формулировку:

> Тест не создаёт браузер сам. Он получает `login_page` из фикстуры.
> Фикстура собирает Page Object на живом `page` и `base_url`.

### Шаг 4 — конфиг (`config/settings.py`, `.env`)

Правило зрелого фреймворка:

- URL/креды **не** в тестах
- берутся из env
- `.env.example` — документ для онбординга

Вопрос интервьюера: *«Как переключить стенд staging → prod?»*  
Ответ: *«Через `BASE_URL` / профиль CI, без правок тестов.»*

### Шаг 5 — Page Object Model (`pages/`)

**Зачем POM:** тест говорит на языке бизнеса, страница — на языке UI.

```
test:  login_page.login(user, password)
page:  fill(#username) → fill(#password) → click(submit)
```

Что искать в `LoginPage`:

1. **локаторы** в `__init__`
2. **навигация** (`open_login`)
3. **действия** (`login`)
4. **проверки** (`expect_success`) — часто через `expect()` Playwright

`BasePage` — общие примитивы, чтобы не копипастить `goto/click/fill`.

### Шаг 6 — тесты (`tests/`)

Хороший тест:

1. короткий
2. AAA (Arrange / Act / Assert)
3. без CSS-селекторов
4. с маркерами (`@pytest.mark.smoke`)

Плохой запах (скажи это на собесе):

- селекторы прямо в тесте
- `time.sleep`
- логин скопирован в 10 файлах
- assert без понятного ожидания

### Шаг 7 — отчёты и артефакты

В реальных проектах смотри:

- `allure-results/` / плагин allure
- скриншоты/видео/trace в `pytest-playwright`
- CI: GitHub Actions / GitLab CI → `pytest -m smoke`

---

## 4. Как «прогнать глазами» один сценарий end-to-end

Возьми `test_successful_login`:

1. pytest находит тест по `pytest.ini`
2. перед тестом поднимает фикстуры из `conftest.py`
3. `login_page.open_login()` → `BasePage.open("/login")`
4. `login_page.login(...)` → fill + click
5. `expect_success()` → `expect(#flash).to_contain_text(...)`
6. context/page закрываются → следующий тест чистый

Если умеешь рассказать этот путь — ты **читаешь** фреймворк, а не зубришь.

---

## 5. Full Stack QA: что ещё обычно лежит рядом

В зрелом репо часто две «ноги»:

```
tests/ui/          # Playwright
tests/api/         # httpx/requests + pydantic модели
clients/api/       # обёртки над REST
```

Как читать API-часть (тот же метод):

1. клиент (`ApiClient.get/post`)
2. модели ответа
3. фикстура `auth_token` / `api_client`
4. тест: статус + тело + иногда сверка с UI

Фраза для собеса:

> UI проверяет пользовательский путь, API — контракт и данные быстрее и стабильнее.

---

## 6. Чеклист «открыл чужой репозиторий — 15 минут»

1. [ ] Прочитал `README` / `requirements` / `pytest.ini`
2. [ ] Нашёл все `conftest.py` (корневой + пакетные)
3. [ ] Нарисовал цепочку фикстур на бумаге
4. [ ] Открыл 1 page object и 1 тест того же флоу
5. [ ] Нашёл, откуда `base_url` и креды
6. [ ] Нашёл, как запускают smoke в CI
7. [ ] Могу объяснить один падающий тест по стеку: тест → page → locator → ожидание

---

## 7. Типовые вопросы собеседования (короткие ответы)

**Чем pytest fixture отличается от обычной функции?**  
Управляется pytest: setup/teardown, scope, DI в аргументы теста.

**Зачем context на каждый тест?**  
Изоляция cookies/storage/localStorage — нет протекания состояния.

**Почему не Selenium?**  
Playwright: автоожидания, trace, multi-browser API, быстрее стабильнее для современного UI.

**Где хранить локаторы?**  
В Page Object, не в тесте.

**Как Parallel?**  
`pytest-xdist` + отдельный context/browser на воркер; осторожно с общими данными.

**Что такое flake?**  
Нестабильный тест: гонки, плохие ожидания, общая тестовая дата. Лечится expect/locator strategy + изоляция данных.

---

## 8. Мини-практика прямо в этом репо

```bash
cd playwright-pytest-framework
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env
pytest -m smoke --headed
```

Потом сломай специально локатор в `login_page.py` и прочитай traceback:  
тест → page method → locator — это и есть навык «читать фреймворк».

---

## 9. Одна шпаргалка на экран

```
requirements  → что умеет стек
pytest.ini    → как запускают
conftest.py   → кто создаёт browser/page/PO
config/       → откуда URL и секреты
pages/        → как говорят с UI
tests/        → что проверяем бизнесом
CI + allure   → как это живёт в пайплайне
```

Начни всегда с **conftest.py + один тест + его page object**. Остальное — детали.
