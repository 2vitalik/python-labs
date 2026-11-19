# T354 · `check()` → сайт: фрагмент службової клітинки (лаби 3–5)

`2026-11-19` · до [plan.md](plan.md) §9

Що робить: після звірки відповіді `check()` каже сайтові, яку відповідь пораховано. Сайт сам судить число правилом рядка відповідей і показує студентові «ноутбук на звʼязку: 9 із 14 ✅», а викладачеві — хто на якому кроці.

Токен видає сайт: сторінка «Моя лаба» дописує до картки останній рядок `TOKEN = "…"`. У картках із файла токена нема — тоді фрагмент мовчить.

## Що вставити

1. До імпортів службової клітинки — `import json`, `import sys`, `import urllib.request` (якщо котрогось ще нема).
2. Перед `def check(` — цей блок; `3` у адресі — номер лаби.

```python
SITE = "https://ods.labs.in.ua"


def tell(name, value):
    """Каже сайтові курсу, що відповідь пораховано. Без TOKEN у картці й без мережі мовчить і більше не пробує."""
    if getattr(tell, "off", False):
        return
    try:
        url, body = f"{SITE}/api/variants/3/live", json.dumps({"vid": VARIANT, "token": TOKEN, "name": name, "value": value})
        if sys.platform == "emscripten":  # marimo у браузері: його urllib не знає timeout
            from js import XMLHttpRequest
            x = XMLHttpRequest.new(); x.open("POST", url, False); x.timeout = 3000; x.send(body)
            if x.status != 200: raise OSError(x.status)
        else:
            urllib.request.urlopen(urllib.request.Request(url, body.encode(), {"Content-Type": "text/plain"}), timeout=3)
    except Exception:
        tell.off = True
```

3. Останнім рядком `check()`, після `print("✅" if ok else "❌", …)`:

```python
    tell(name, value)
```

## Чому саме так

- **Ніколи не падає й не чекає довше 3 с**: будь-яка помилка — нема `TOKEN`, нема мережі, сайт лежить — вимикає надсилання до кінця сеансу; «Виконати все» з чотирнадцятьма `check()` не зависає.
- **Дві гілки**: у marimo в браузері (Pyodide) `urllib` підмінений і не зважає на `timeout`, тому там — XHR зі своїм; у Colab і локально — звичайний `urllib`.
- **`text/plain`** — браузер шле такий запит без попереднього OPTIONS.
- **Сайт упізнає лабу, що шле**, за рядком `/api/variants/` у службовій клітинці: після імпорту будови (`lab_io.py`) картка на «Моїй лабі» отримує `TOKEN`.
- Кількість клітинок, відповіді й картки не міняються; у marimo імена `json`, `sys`, `urllib`, `SITE`, `tell` мають жити лише в службовій клітинці.

## Перевірено

Основу фрагмента (обидві гілки, сценарії «сервер працює · лежить · висить 10 с · недосяжний · https») — у marimo в браузері (Pyodide 3.14) і в CPython 3.9 та 3.13: 0–3 с, винятків назовні нема. Прийом на сайті — смоук `tests/smoke_files.py` (токен, чужий токен, вердикт значення).

Не перевірено: Colab; справжня адреса `https://ods.labs.in.ua` (сайт ще не на сервері); варіант цього файла з `VARIANT` і `TOKEN` як глобальними іменами — після вставки прогнати розвʼязаний ноутбук і marimo-варіант, рядок відповідей має лишитись тим самим.
