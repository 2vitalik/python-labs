---
title: Outpacked
slug: outpacked
aka: []
family: board-digital
also: [pencil-logic]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2026
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/4012320/Outpacked/", best: true, note: "опис, 11 скриншотів з HUD, обмеженнями й календарем рівнів; є демо"}
  - {kind: other, url: "https://store.steampowered.com/api/appdetails?appids=4012320", note: "Steam JSON: повний опис, категорії (редактор, Workshop, лише миша)"}
  - {kind: other, url: "https://steamcommunity.com/app/4012320/reviews/?browsefilter=toprated", note: "відгуки: підказки, редактор з власними картинками, джигсо між тижнями"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Outpacked+gameplay", note: "пошук; геймплей і трейлер редактора"}
stage: v1
coverage: 65
mechanics: [polyomino-placement, multi-cell-size, drag-drop-piece, cursor-place, hover-highlight, satisfy-constraints, completion-detection, collect-quota, goal-counter, conflict-highlight, restart-level, level-select, sequential-levels, in-game-editor, editor-playtest, level-exchange, game-screen, puzzle-select, achievements-window, +tag-adjacency-constraints, +item-subset-quota, +multi-compartment-grid, +negative-contribution-item, +constraint-list-panel, +calendar-level-select, +jigsaw-interlude, +manual-submit-check]
proposes: ["+cond:adjacent_to", "+cond:only_adjacent", "+cond:on_edge", "+ui:constraint-list", "+ui:tag-ribbon", "+card:tag-adjacency-constraints", "+card:item-subset-quota", "+card:multi-compartment-grid"]
author: opus
date: 2026-11-09
---

# Outpacked — пакування валізи: поліоміно-предмети в сітку, квоти ресурсів і правила сусідства за тегами

## Суть
Персонаж просить зібрати багаж; гравець вибирає предмети з каталогу й розкладає їх у сітчасті відсіки валізи чи рюкзака. Кожен предмет — фігура з кількох клітин, має **теги** (hot, meltable, liquid, electronic, fragile, soft, plushie, sharp…) і **внесок у ресурси** (+воду, +їжу, іноді мінус). Треба одночасно набрати квоти ресурсів, вмістити фігури й виконати список обмежень сусідства («кожне meltable не поруч із hot») — автори кажуть «Tetris meets Sudoku», а по суті це ще й рюкзак (knapsack): не всі предмети з каталогу потрібні.

## Поле і час
- Поле — один або кілька відсіків-сіток однієї валізи (основне відділення, бічні кишені, нижнє відділення); відсіки бувають непрямокутні. Розміри різні в кожному рівні.
- Сусідство — ортогональне між клітинами предметів (у межах відсіку; чи рахується між відсіками — у «Непевне»).
- Статичний пазл: ходів і таймера нема; стан = розкладка; перевірка — кнопкою Submit.
- 61 ручний рівень, 4 персонажі (науковець на конференцію, сімʼя в похід з дитячими плюшевими іграшками, рок-музикант…), рівні — дні календаря; між «тижнями» — джигсо-пазли для перепочинку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Предмет | piece | форма-поліоміно; теги; внесок у ресурси (±N) | перетягується з каталогу у вільні клітини відсіку |
| Іменний предмет (Mr Flibble, Jeffrey…) | piece | власне імʼя як тег | має персональні обмеження («Jeffrey не поруч з бумерангом») |
| Відсік валізи | zone | маска клітин | приймає предмети; клітини під предметом підсвічуються |
| Клітина відсіку | static | вільна / зайнята | вільна — можна ставити |
| Каталог | supply | набір предметів рівня | використані предмети лишаються сірими силуетами |
| Квота ресурсу | mark | ціль N, іконка | поточна сума a/N: зелена — виконана, червона — ні |
| Обмеження | mark | тег A, відношення, тег B | ✓ виконано / ✗ порушено / сіре — нейтральне |
| Персонаж | neutral | репліка | ставить задачу, реагує на Submit |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag(item, cells))` → ЯКЩО `fits(item, cells)` → ТО `place(player, item)`; інакше `block`.
- КОЛИ `after(place)` → ТО `counter(resource_k, +v_k)` для кожного ресурсу предмета (бувають від'ємні: печиво −1 вода +2 їжа).
- КОЛИ `input(drag(item, catalogue))` → ТО `custom: «вийняти предмет у каталог»`, `counter(resource_k, −v_k)`.
- КОЛИ `input(reset)` → ТО `restart`.
- Обмеження «не поруч»: КОЛИ `adjacent(meltable, hot)` → ТО `custom: «рядок обмеження ✗»` — умова `no_adjacent(meltable, hot)`; так само electronic/liquid, plushie/sharp, phone/sharp, paper/sharp, hot/cold, food/dirty, іменні.
- Обмеження «обовʼязково поруч»: ЯКЩО `custom: «кожен earphone має сусіда phone»` (`+cond:adjacent_to`) → ✓; так само plushie/plushie, plushie/cold, meltable/cold.
- Обмеження «лише поруч»: ЯКЩО `custom: «усі сусіди fragile — soft»` (`+cond:only_adjacent`) → ✓.
- Обмеження «на краю»: ЯКЩО `custom: «кожен musical на краю відсіку»` (`+cond:on_edge`) → ✓.
- КОЛИ `constraint_broken(c)` → ТО `custom: «рядок c червоний з ✗; клітини предмета-порушника червоні»`.
- КОЛИ `input(submit)` → ЯКЩО `all_constraints_met` і `counter(resource_k, >=, quota_k)` для всіх k → ТО `win`, `message(«thanks! that's perfect!»)`, `next_level`; інакше `custom: «персонаж відмовляє»`.
- КОЛИ `input(hint)` → ТО `custom: «підказка-поштовх, не весь розвʼязок»`.
- Перемога: усі обмеження ✓ і всі квоти зелені · Поразка: нема · Рахунок: нема.

## Керування і ввід
- Лише миша (є категорія Steam «Mouse Only Option»): перетягнути предмет з каталогу у відсік, назад — у каталог.
- Наведення на предмет — стрічки з тегами й внеском у ресурси; наведення на тег у списку обмежень — підсвітка всіх предметів з цим тегом; наведення на значок відношення — підказка словами («must not be adjacent to»).
- Кнопки Submit · Reset · Hint; іконка щоденника — до календаря рівнів.

## Вікна, меню, HUD
- `game-screen`: ліворуч — валіза з відсіками; угорі ліворуч — панель квот (`progress-bar` на кожен ресурс, a/N, зелене/червоне); праворуч — планшет з двома вкладками: **Catalogue** (предмети рівня, використані — силуети) і **Constraints** (`+ui:constraint-list`: рядки з ✓/✗, компактна іконна нотація «A ⧉ B» або повні речення «every … must (not) be adjacent to …», прокрутка); `tooltip`-стрічки тегів (`+ui:tag-ribbon`); кнопки `check-button` (Submit), `restart-button` (Reset), `hint-button`.
- `dialogue-window`: репліка персонажа на старті й після Submit.
- `puzzle-select` у вигляді календаря-щоденника: місяці, дні-рівні; пройдені — зелені, поточний — синій.
- `editor-window`: редактор рівнів у реальному часі, свої картинки, публікація у Steam Workshop.
- `achievements-window` (Steam), налаштування гучності (категорія «Custom Volume Controls»).
- Переходи: календар → game-screen → (Submit ✓) репліка → календар з наступним днем; між тижнями — джигсо-рівень.

## Фічі поза полем
- `levels-sequential` + `level-unlock` через календар (61 рівень, 4 персонажі).
- `hint` — кнопка підказки, яка «підштовхує, не спойлерить» (за відгуками).
- `level-editor` + `level-sharing` (Steam Workshop) + `user-levels-browser`; редактор приймає власні зображення предметів.
- `achievements`, `volume-sliders`; джигсо-пазли як «перепочинок» між тижнями.
- Нема undo як кнопки: розкладку правлять перетягуванням, Reset — усе з нуля.

## Варіації й родичі
- Patchwork / Project L / The Isle of Cats (`patchwork.md`, `project-l.md`, `the-isle-of-cats.md`) — поліоміно в сітку без тегових обмежень; Isle of Cats має «родини» котів за кольором.
- Resident Evil 4 attaché case (`build-sim/re4-attache-case.md`), Backpack Hero (`build-sim/backpack-hero.md`) — інвентар-сітка, але без логічних умов сусідства.
- Unpacking (`build-sim/unpacking.md`) — протилежна дія (розпакувати), правила «де річ доречна» без сітки-тегів.
- Судоку й Star Battle (pencil-logic) — правила «не поруч» як обмеження; тут обмеження задані на тегах, а не на числах.
- **Осі варіацій**: відношення (поруч / не поруч / лише поруч з / на краю / у тому ж відсіку) · обʼєкт обмеження (тег / конкретний предмет за іменем) · вибір предметів (усі обовʼязкові / підмножина під квоти) · поле (один відсік / кілька відсіків з різними масками).

## Цікавинки для курсу
- Обмеження як дані: список трійок (tagA, relation, tagB) і одна функція перевірки над розкладкою з підсвіткою ✓/✗ — 📎.
- Поліоміно у відсіки з масками + перевірка накладання — 🥉 (картка `polyomino-placement`).
- Квоти ресурсів з відʼємними внесками: вибрати підмножину предметів, що дає ≥N кожного ресурсу і влазить — 🥈 (рюкзак із кількома вимірами).
- Розвʼязувач: backtracking з відсіканням за порушеними «не поруч» і залишком місця — 🥇.
- Компактна іконна нотація обмежень ↔ повні речення при наведенні — 🌱 (той самий обʼєкт обмеження, два рендери).
- Календар як вибір рівня (дні = рівні, тижні з перервами-джигсо) — 🌱.
- Редактор рівнів з власними картинками й публікацією — 🥈.

## Мапа на каталог
- Є: `polyomino-placement` · `multi-cell-size` (предмет на кілька клітин) · `drag-drop-piece` · `cursor-place` · `hover-highlight` (теги, підсвітка за тегом) · `satisfy-constraints` + `completion-detection` (Submit) · `collect-quota` + `goal-counter` (квоти ресурсів) · `conflict-highlight` (✗ і червоні клітини) · `restart-level` (Reset) · `level-select` + `sequential-levels` + `puzzle-select` (календар) · `in-game-editor` + `editor-playtest` + `level-exchange` (Workshop) · `game-screen` · `achievements-window`.
- **Нема** → пропозиції карток:
  - `+tag-adjacency-constraints` «Правила сусідства за тегами предметів (поруч / не поруч / лише поруч / на краю)» · game-logic/constraints · 📎 · слоти {relations}.
  - `+item-subset-quota` «Вибір підмножини предметів під кілька квот ресурсів, внески бувають відʼємні» · game-logic/win · 🥈.
  - `+multi-compartment-grid` «Поле з кількох сіток-відсіків з власними масками» · levels/format · 🌱.
  - `+negative-contribution-item` · `+constraint-list-panel` · `+calendar-level-select` · `+jigsaw-interlude` · `+manual-submit-check` — дрібні, лише як теги.

## Пропозиції до словників
- `+cond:adjacent_to` — кожна сутність виду A має хоча б одного сусіда виду B (Outpacked; пара до наявного `no_adjacent`).
- `+cond:only_adjacent` — усі сусіди сутності A — лише виду B («fragile поруч лише з soft»).
- `+cond:on_edge` — сутність торкається краю поля/відсіку.
- `+ui:constraint-list` — список обмежень рівня з позначками ✓/✗ і підсвіткою на полі.
- `+ui:tag-ribbon` — при наведенні на предмет показати його теги й числові внески.
- `+card:tag-adjacency-constraints` · `+card:item-subset-quota` · `+card:multi-compartment-grid` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Outpacked](https://store.steampowered.com/app/4012320/Outpacked/) — опис, приклади обмежень, 61 рівень, 4 персонажі, редактор, Workshop; 11 скриншотів (вкладки Catalogue/Constraints, квоти, Submit/Reset/Hint, календар).
- [Steam JSON appdetails](https://store.steampowered.com/api/appdetails?appids=4012320) — повний текст опису, категорії (Mouse Only, Includes level editor, Workshop), дата 1.04.2026, Antikythera Games.
- [Steam-відгуки](https://steamcommunity.com/app/4012320/reviews/?browsefilter=toprated) — підказки «поштовхом», редактор з власними картинками, джигсо між тижнями, складність росте швидко.
- YouTube: пошук «Outpacked gameplay».

## Непевне
- (?) Чи можна обертати предмети: на скриншотах ті самі предмети завжди в одній орієнтації — схоже, ні, але не бачив правила.
- (?) Квота — «не менше N»: на скриншотах 3/2 і 7/6 зелені й рівень прийнято; але в одному кадрі 4/3 червоне — можливо, бувають квоти «не більше» або точні.
- (?) Значки «⊡» (ймовірно, «на краю») і «ланцюжок» між electronic і liquid у компактній нотації — сенс другого не бачив (може, «не в одному відсіку»).
- (?) Чи рахується сусідство між різними відсіками однієї валізи.
- (?) Що саме робить Hint: на одному кадрі видно напівпрозорі силуети предметів у валізі — можливо, показ частини розвʼязку.
- (?) Чи обовʼязково заповнити всі клітини: на прийнятому рівні валіза повна, а в каталозі лишились невикористані предмети — правила про порожні клітини не бачив.
