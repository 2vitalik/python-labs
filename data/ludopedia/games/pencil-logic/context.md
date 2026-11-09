---
title: Context
slug: context
aka: [コンテクスト]
family: pencil-logic
also: []
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2022
platforms: [paper, web]
links:
  - {kind: other, url: "https://puzz.link/rules.html?context", best: true, note: "puzz.link: сторінка правил і вхід у плеєр/редактор (рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/context.js", note: "puzz.link: правила EN/JA, «invented by RSP», коди помилок, тест-пазл 8×8"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "pzprjs: тексти помилок nmShadeDiagNe.context, nmUnshadeAdjNe.context"}
  - {kind: other, url: "https://scrapbox.io/puzzle-pedia/Context", note: "puzzle-pedia (JA): автор RSP, CTC Fan Server 10.03.2022, техніки 131/323/333"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=context+puzzle+RSP", note: "пошук; розвʼязання"}
stage: v1
coverage: 75
mechanics: [markup-validity, completion-detection, satisfy-constraints, conflict-highlight, cell-click, keyboard-controls, dot-mark, neighbor-count-clue, connectivity-check, undo-redo, in-game-editor, import-open-formats, +cell-shade-toggle, +no-adjacent-check, +state-dependent-clue]
proposes: ["+cond:diag_count", "+card:state-dependent-clue"]
author: opus
date: 2026-11-09
---

# Context — зафарбуй клітинки; число рахує ортосусідів, якщо біле, і діагональних, якщо саме зафарбоване

## Суть
На квадратній сітці стоять числа. Гравець зафарбовує частину клітинок: зафарбовані не торкаються стороною, а білі лишаються однією звʼязною областю. Незвичне: зафарбувати можна й клітинку з числом — і тоді те саме число означає інше: біле число рахує зафарбованих ортогональних сусідів, зафарбоване — діагональних. Тобто сенс підказки залежить від рішення, яке гравець ще має прийняти.

## Поле і час
- Прямокутна сітка; клітинка має два шари: незмінна підказка (число або порожньо) і стан гравця (зафарбована / біла / крапка «точно біла»).
- Сусідство — ортогональне для заборони дотику й звʼязності білих; діагональне — лише для підказки зафарбованого числа.
- Час статичний; хід = змінити стан однієї клітинки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Число | static | N | якщо клітинка біла — N = кількість зафарбованих серед 4 ортосусідів; якщо зафарбована — N = кількість зафарбованих серед 4 діагональних |
| Зафарбована клітинка | mark | — | не має зафарбованого ортосусіда; може стояти на числі |
| Біла клітинка | mark | — | усі білі утворюють одну ортогонально звʼязну область |
| Крапка | mark | — | допоміжна позначка «біла»; на перевірку не впливає |
| Біла область | zone | — | має бути одна (`cuDivideRB`) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, cell)` → ТО `mark(cell, shaded)` toggle; КОЛИ `input(right_click, cell)` → ТО `mark(cell, dot)` (?).
- КОЛИ `custom: «дві зафарбовані клітинки мають спільну сторону»` → ТО `constraint_broken(adjacent)` (`csAdjacent`; умова `no_adjacent(shaded)`).
- КОЛИ `custom: «перевірка числа»` → ЯКЩО `not state(clue, shaded)` and `custom: «зафарбованих ортосусідів ≠ N»` → ТО `constraint_broken(clue)` (`nmUnshadeAdjNe`; по суті `adjacent_count(cell, shaded, =, N)`).
- КОЛИ `custom: «перевірка числа»` → ЯКЩО `state(clue, shaded)` and `custom: «зафарбованих діагональних сусідів ≠ N»` → ТО `constraint_broken(clue)` (`nmShadeDiagNe`; `+cond:diag_count`).
- КОЛИ `custom: «білі клітинки розпались на кілька областей»` → ТО `constraint_broken(divided)` (`cuDivideRB`; умова `connected(white)`).
- КОЛИ `custom: «на полі нема жодної зафарбованої»` → ТО `constraint_broken(empty)` (`brNoShade`).
- КОЛИ `all_constraints_met` → ТО `win`.
- Перемога: усі числа виконані у своєму «режимі», дотиків нема, білі звʼязні. Поразки й рахунку нема.
- Наслідок для дедукції: зафарбоване число не має зафарбованих ортосусідів (заборона дотику), тож лише діагональні й можуть бути зафарбовані — два режими підказки не перетинаються за клітинками.
- Техніки (puzzle-pedia, Melting_Solver): «1» між двома «1», або «2»/«3» між «1» — біла; у «323» клітинки, що продовжують «3» по прямій, зафарбовані; «333» має два розклади; хрест із п'яти «3» — центр зафарбований.

## Керування і ввід
- puzz.link (play): клік по клітинці — зафарбувати/зняти; права кнопка — крапка «біла» (?) ; drag — тягнути той самий стан по кількох клітинках (?).
- puzz.link (edit): курсор стрілками, цифри з клавіатури — підказки; розмір поля задається при створенні.
- Папір: зафарбувати олівцем, крапкою позначати білі.

## Вікна, меню, HUD
- `game-screen` (puzz.link): сітка з числами, зафарбування, крапки; `check-button`, `undo-button`, `redo-button`; `conflict-highlight` після перевірки — показує перше порушення текстом коду помилки (?).
- `editor-window` (puzz.link edit mode): числа, розмір поля, експорт у URL.
- `help-window` — сторінка правил puzz.link.
- `settings-window` (puzz.link): загальні параметри відображення pzpr (?).
- Переходи: rules → URL пазла → game-screen → Check → повідомлення «правильно / помилка».

## Фічі поза полем
- `auto-check` за кнопкою з текстом першої помилки (puzz.link).
- `undo`/`redo`; `level-editor` + `share-code` — пазл як URL puzz.link.
- `puzzle-bank` — база puzz.link і Puzzle Square JP (за puzzle-pedia).

## Варіації й родичі
- Сусіди за схемою «зафарбуй + не торкаються + білі звʼязні»: [hitori](hitori.md), [heyawake](heyawake.md), [kuromasu](kuromasu.md) — там число завжди біле.
- Числові підказки сусідства: сапер (`hidden-deduction`), [tapa](tapa.md) (кільце з 8 сусідів), [light-up](light-up.md).
- **Осі варіацій**: хто визначає сенс підказки (тип клітинки / стан гравця / колір) · окіл підказки (4 орто / 4 діагональні / 8) · обмеження зафарбованих (не торкаються / звʼязні) · обмеження білих (звʼязні / без 2×2).

## Цікавинки для курсу
- Підказка, сенс якої залежить від стану клітинки: одна функція `clue_ok(cell)` з гілкою орто/діагональ — 📎.
- Заборона дотику зафарбованих + BFS звʼязності білих — 🌱 + 📎 (повтор з Hitori).
- Перевірка «з поясненням»: повернути перший код помилки і клітинки для підсвітки — 🥉.
- Розвʼязувач: для кожного числа два режими; поширення + бектрекінг з перевіркою звʼязності — 🥇.
- Генератор з єдиним розвʼязком — 👑.

## Мапа на каталог
- Є: `neighbor-count-clue` ↔ біле число · `connectivity-check` ↔ білі звʼязні · `markup-validity`, `conflict-highlight`, `completion-detection`, `satisfy-constraints` · `cell-click`, `dot-mark`, `keyboard-controls` · `in-game-editor`, `import-open-formats` ↔ URL puzz.link · `undo-redo`.
- **Нема** → пропозиції карток:
  - `+cell-shade-toggle`, `+no-adjacent-check` — уже пропоновані в корпусі (Hitori, Heyawake).
  - `+state-dependent-clue` «Підказка, сенс якої залежить від стану її клітинки» · game-logic/constraints · 📎 · слот {modes: unshaded→orth, shaded→diag}.

## Пропозиції до словників
- `+cond:diag_count` — кількість сусідів виду лише по 4 діагоналях (порівняно з N); `adjacent_count` рахує ортогональних/8.
- `+card:state-dependent-clue` — див. мапу.

## Джерела
- ⭐ [puzz.link: Context](https://puzz.link/rules.html?context) — сторінка правил і плеєр (текст рендериться JS, WebFetch не дістав).
- [puzz.link context.js](https://puzz.link/js/pzpr-samples/context.js) — 4 правила EN/JA, «invented by RSP», коди `brNoShade csAdjacent nmShadeDiagNe nmUnshadeAdjNe cuDivideRB`.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти помилок для `.context`.
- [puzzle-pedia: Context](https://scrapbox.io/puzzle-pedia/Context) — автор RSP, анонс на CTC Fan Server 10.03.2022, назва 16.03.2022, Twitter 13.04.2022; техніки.
- YouTube: пошук «context puzzle RSP».

## Непевне
- (?) Призначення правої кнопки (крапка) і drag-зафарбування — загальна поведінка pzpr для зафарбовувальних жанрів, не перевірена саме для Context.
- (?) puzzle-pedia формулює біле число як «сама клітинка + орто-сусіди» — результат той самий, бо клітинка біла.
- (?) Чи є Context у банку Janko чи комерційних збірках — не перевіряв.
