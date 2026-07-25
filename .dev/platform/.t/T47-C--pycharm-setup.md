# T47 · PyCharm: покрокове налаштування запуску

`2026-07-26` · 🔆 clarification

Контекст:
- запит із чату 2026-07-26; PyCharm Pro ([T46](T46-Q--pre-code-questions.md) Q3); структура коду — [T45](T45-P--app-skeleton.md).

## Кроки

1. **Відкрити проєкт:** File → Open → тека `python-labs` (корінь репо — так поруч видно і `.dev/`, і код).
2. **Інтерпретатор:** Settings (⌘,) → Project: python-labs → Python Interpreter → Add Interpreter → Add Local Interpreter → **Select existing** → Interpreter: `app/api/.venv/bin/python` (середовище вже створене `uv sync`; у PyCharm ≥2024.2 можна вибрати тип «uv»).
3. **Run-конфіг бекенда:** Run → Edit Configurations → **+** → **FastAPI**:
   - Application file: `app/api/main.py`
   - Uvicorn options: `--reload --port 8000`
   - **Working directory: `app/api`** — критично: звідти читається `.env` і працюють плоскі імпорти.
4. **Run-конфіг фронта:** **+** → **npm**:
   - package.json: `app/vue/package.json`
   - Command: `run` · Scripts: `dev`.
5. **Compound:** **+** → **Compound** → назва `app` → додати обидві конфігурації. Тепер одна кнопка ▶ запускає бекенд і фронт разом.
6. **Браузер:** завжди **http://localhost:5173** (на `:8000` напряму ходити не треба; до того ж на `*:8000` по IPv6 сидить Docker Desktop і на `localhost:8000` можна впіймати його «404 page not found»).
7. **Бонус (Pro):** вкладка Database → **+** → Data Source → MongoDB → `mongodb://localhost:27017` — видно базу `python_labs` і колекцію `users` живцем.

## Нюанс: мої фонові сервери

- Поки в терміналі сесії агента крутяться мої `fastapi dev` і `vite` — порти 8000/5173 зайняті, і запуск із PyCharm упаде. Перед першим стартом з PyCharm зупини їх: `pkill -f "fastapi dev"; pkill -f vite`.

## Твої думки та питання

> 
