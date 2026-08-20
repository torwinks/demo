# demo

Учебные материалы для подготовки к Full Stack QA.

## Playwright + pytest (основное)

Смотри каталог [`playwright-pytest-framework/`](./playwright-pytest-framework/):

- мини-фреймворк на **Python / pytest / Playwright**
- гайд **[как читать фреймворк автотестов с нуля](./playwright-pytest-framework/HOW_TO_READ.md)**

```bash
cd playwright-pytest-framework
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env
pytest -m smoke
```

## Java demo (legacy)

В `IJProjects/Api/` лежит небольшой пример на RestAssured + JUnit — для сравнения стеков.
