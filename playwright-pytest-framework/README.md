# Playwright + pytest — учебный фреймворк для Full Stack QA

Стек: **Python · pytest · Playwright · Page Object Model**.

## Быстрый старт

```bash
cd playwright-pytest-framework
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env
pytest -m smoke
```

## С чего читать код

Открой **[HOW_TO_READ.md](./HOW_TO_READ.md)** — пошаговый метод чтения любого автотест-фреймворка с нуля (под собеседование).

Короткий маршрут:

1. `requirements.txt` → стек  
2. `pytest.ini` → запуск  
3. `conftest.py` → фикстуры (самое важное)  
4. `pages/` → Page Object  
5. `tests/` → сценарии  

## Структура

| Путь | Роль |
|------|------|
| `conftest.py` | browser → context → page → page objects |
| `config/settings.py` | BASE_URL, креды из `.env` |
| `pages/` | POM: локаторы и действия UI |
| `tests/` | бизнес-проверки без селекторов |
| `utils/` | хелперы вне страниц |
