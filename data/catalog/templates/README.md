# Еталонні описи базових ігор (Д4)

Один файл — одна гра-основа каталогу (`<slug>.yaml`, slug як у `games.yaml`). Це «меню» для студента: кнопка «Почати з еталона» у «Моїй грі» додає поле, сутності, вікна з меню, правила й заявки в його гру (`app/api/templates.py`), далі він викреслює й додає своє. Мова — словники `app/api/models/vocab.py`: ролі, тригери, умови, ефекти, властивості поля; картки — slug-и `tasks.yaml`.

## Формат

```yaml
field:                      # властивості поля за vocab.FIELD (усе необовʼязкове)
  size: "28×31"             # текст
  topology: square          # square | hex | graph | iso | layers | 1d | 3d | nested
  wrap: true                # тор
  view: top-down            # top-down | side | first-person
  gravity: none             # none | down | up | per-type | toward-center
  time: realtime            # turn | realtime | static | programmed | wego | rhythm
  control: direct           # direct | indirect | click-cell | drag-piece | swipe-all | drag-path | mark | programmed
  layers: [підлога, обʼєкти]
entities:
  - title: Пакмен           # назва — ключ: правила посилаються на неї; у грі студента збіг назви = та сама сутність
    role: player            # ключ vocab.ROLES
    description: "Жовте коло, їсть точки"
    stats: [{key: lives, value: "3"}, {key: speed, value: "1", unit: "кл/тік"}]   # key — з vocab.STATS або своє слово
    states: [звичайний, посилений]       # стани; переходи — правилами set_state / state
    claims: [move-4dir, player-death]   # картки каталогу на цій сутності; з параметрами — {slug: spawn-schedule, params: {every: 20}}
rules:
  - when: {kind: contact, a: Пакмен, b: Точка}          # сутності — за назвою; також "*" (будь-хто), а в cond/then — "@a", "@b", "@both"
    cond: [{kind: state, a: "@b", s: переляк, not: true}]   # необовʼязково; not: true — заперечення
    then: [{kind: disappear, a: "@b"}, {kind: score, n: 10}]
    note: "за бажанням"
windows:
  - title: Гра
    task: game-screen       # картка з тегом #window
    claims: [status-panel]  # елементи на вікні (картки HUD / налаштувань)
    items:                  # пункти меню цього вікна (необовʼязково)
      - {title: Грати, window: Гра}        # → вікно за назвою
      - {title: Гучність, task: volume-control}   # → картка
      - {title: Вихід}
claims: [collect-all, player-death]   # заявки рівня гри (не привʼязані до сутності чи вікна)
```

## Правила написання

- Лише слова зі словників: `kind` тригера — ключ `TRIGGERS`, умови — `CONDITIONS`, ефекти — `EFFECTS`; аргументи — за `args` відповідного слова (назви й типи). Не лягає — `{kind: custom, text: "…"}` одним реченням.
- Сутності в правилах — назвами з `entities`; підлога/стихія (лід, вода) — теж сутності з роллю `terrain`/`hazard`, бо тригер `enter(a, b)` чекає дві сутності.
- Картки — лише наявні slug-и з `tasks.yaml` (активні й чернетки); вигаданих не писати. Параметри (`params`) — за `slots` картки.
- Обсяг: 4–10 сутностей, 8–20 правил, 3–6 вікон, 5–15 заявок — те, що справді є в класичній версії гри, без фан-розширень; це стартове меню, не енциклопедія.
- Джерела: файл гри в `data/ludopedia/games/`, опис і приклади в `data/catalog/games.yaml`, нотатки `data/wiki/games/`.
- Перевірка: імпорт у смоуку (`tests/smoke_games.py`) має пройти без `skipped` — помилкове слово чи картка потраплять у список пропущеного.
