---
title: The Artisan of Glimmith
slug: the-artisan-of-glimmith
aka: [Artisan of Glimmith, Glimmith]
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
year: 2026
platforms: [Windows, Steam Deck]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/4160210/The_Artisan_of_Glimmith/", best: true, note: "Lunarch Studios (Islands of Insight), 17.03.2026; 16 скриншотів з картками правил (Rose Windows, Precision, Range, Minimum, Polyomino, Palisade, Delta, Gemini, Solitude, Mismatch, Compass, Size Separation, Area Number), два трейлери, демо, редактор і Workshop"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=4160210&count=30", note: "Steam News: режими вводу, CTRL — площа регіону, Show Errors, палітри, нотатки, Workshop-конкурс, підказки до Bricky і Loopy, DLC Lunar Lights (12+ правил)"}
  - {kind: other, url: "https://www.yekbot.com/the-artisan-of-glimmith-walkthrough-guide/", note: "сторонній гайд з розвʼязками: 28 зон (більшість названа за правилом), кількість пазлів у зоні, складність 1–7, плінти білі / коричневі / малинові"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=The+Artisan+of+Glimmith+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [satisfy-constraints, completion-detection, markup-validity, cell-click, edge-marking, conflict-highlight, undo-redo, redo, restart-level, in-game-editor, editor-window, world-map, map-window, tutorial-window, settings-window, game-screen, keyboard-controls, level-rating, background-music, +cell-coloring, +equal-size-partition, +region-size-check, +shape-identity-check, +rect-shape-check, +shape-bank, +compass-clue, +region-symbol-count, +edge-inequality-clue, +rules-panel, +free-draw-notes, +open-world-puzzles, +workshop-sharing, +secret-area, +border-pattern-clue, +region-shape-clue, +touching-regions-count, +region-area-hover, +error-display-modes, +custom-palette]
proposes: ["+cond:region_shape", "+cond:area_between", "+effect:set_edge", "+ui:rule-cards", "+ui:area-counter", "+feature:show-errors-modes", "+feature:custom-palette", "+window:letter-window", "+axis:rules", "+card:border-pattern-clue", "+card:region-shape-clue", "+card:touching-regions-count", "+card:region-area-hover", "+card:error-display-modes", "+card:custom-palette"]
author: opus
date: 2026-11-19
---

# The Artisan of Glimmith — розріж вітраж на регіони так, щоб виконались усі картки правил

## Суть
Пазл від Lunarch Studios (Islands of Insight) про майстра вітражів у летючому королівстві Glimmith. Кожен пазл — фігурна сітка-вітраж, яку гравець ділить на регіони: фарбує клітини й проводить між ними свинцеві межі. Колір довільний (опис: будь-які кольори, аби виконувались правила) — перевіряються лише регіони.

Понад 20 типів правил подано картками праворуч від поля: площа, форма, символи всередині, підказки на межах. Кожна зона світу вводить своє правило, далі правила змішуються; є фінальні «mastery»-пазли, приховані пазли, редактор і Steam Workshop.

## Поле і час
- Квадратна сітка неправильної форми — хрест, серце, з дірками; внутрішнє ребро — пунктир (клітини зʼєднані) або суцільна лінія (межа регіону).
- Клітина — незафарбована (біла) або зафарбована; регіон — звʼязна група клітин без меж між ними, зафарбована чи ні (CTRL-лічильник рахує обидві).
- Підказки стоять у клітинах (Polyomino, Palisade, Area Number, Compass, символи Rose Windows) або на межах (Gemini, Delta, Inequality, Difference); глобальні правила — лише на картці.
- Статика без часу. Поза пазлом — 3D-світ летючих островів з плінтами-пазлами, прихованими стежками й секретами.
- Складність пазла — число в куті «Difficulty N» (бачив 2–5; гайд групує 1–7).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина скла | mark | колір або незафарбована | фарбується будь-яким кольором; колір на правила не впливає |
| Ребро між клітинами | mark | межа (суцільна) / зʼєднання (пунктир) | межа розділяє регіони, пунктир зʼєднує |
| Регіон | zone | площа, форма, символи всередині | звʼязна група клітин без меж усередині |
| Символи Rose Windows | static | вид: трикутник, троянда, ромб, квадрат | кожен регіон має рівно по одному кожного виду |
| Гліф Polyomino | static | форма | задає форму свого регіону |
| Гліф Palisade | static | візерунок меж клітини | межі цієї клітини мають утворити візерунок, повороти дозволено |
| Число Area Number | static | n | площа свого регіону = n |
| Компас | static | числа з боків | скільки клітин свого регіону лежить далі на N / S / E / W |
| Gemini / Delta | static | на межі двох регіонів | ці регіони однакової / різної форми |
| Inequality | static | вістря | вказує на менший за площею регіон |
| Difference | static | n | різниця площ двох регіонів = n |
| Watchtower | static | n | скільки регіонів торкається підказки |
| Картка правила | static | назва, параметр (n, a–b, банк фігур) | глобальне правило для всіх регіонів пазла |
| Плінт | static | колір: білий / коричневий / малиновий (?) | точка світу, що відкриває пазл |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(paint, c)` → ТО `paint(c, color)` — колір будь-який, перевіряються лише регіони.
- КОЛИ `input(lead, edge)` → ТО `custom: «ребро стає межею — регіон розщеплюється»`; на наявній межі — `custom: «межа знімається, клітини зʼєднуються»` (?).
- КОЛИ `input(erase, c)` → ТО `unmark(c)` — стерта клітина може розщепити регіон (Steam News).
- КОЛИ `input(ctrl_hover, c)` → ТО `message(region_area)` — підсвічує звʼязну область під курсором, зафарбовану чи ні, і показує число клітин.
- Precision (n): ЯКЩО `region_size(every_region, n)` («All regions must have an area of exactly n»).
- Range (a–b): ЯКЩО `custom: «a ≤ площа кожного регіону ≤ b»`.
- Minimum (n): ЯКЩО `custom: «площа кожного регіону ≥ n»`.
- Area Number n у клітині: ЯКЩО `region_size(region_of_clue, n)`.
- Size Separation: ЯКЩО `not same(r1, r2, area)` для кожної пари сусідніх регіонів.
- Boxy: ЯКЩО `custom: «кожен регіон — прямокутник»`.
- Polyomino: ЯКЩО `same(region_of_glyph, glyph, shape)` («Defines the shape of the region it sits within»).
- Shape Bank: ЯКЩО `custom: «форма кожного регіону — одна з показаних на картці»`.
- Mismatch: ЯКЩО `unique(region_shapes)` («All regions must have different shapes»).
- Gemini (символ на межі): ЯКЩО `same(r1, r2, shape)` — для двох регіонів, що торкаються символу.
- Delta: ЯКЩО `not same(r1, r2, shape)`.
- Inequality: ЯКЩО `custom: «регіон, на який вказує вістря, менший за площею»`.
- Difference n: ЯКЩО `custom: «різниця площ двох регіонів біля символу = n»`.
- Solitude: ЯКЩО `count(symbol_in_region, ==, 1)` для кожного регіону.
- Rose Windows: ЯКЩО `custom: «у кожному регіоні рівно по одному символу кожного виду»`.
- Compass: ЯКЩО `custom: «клітин регіону північніше, південніше, східніше, західніше компаса — як числа з відповідних боків»`.
- Watchtower n: ЯКЩО `custom: «підказки торкається рівно n регіонів»`.
- Palisade: ЯКЩО `custom: «межі цієї клітини утворюють показаний візерунок; повороти дозволено»`.
- КОЛИ `constraint_broken(rule)` → ЯКЩО `mode(show_errors)` → ТО `custom: «підсвітка порушення на полі й на картці»`; у режимі «Side Panel Only» — лише на картці.
- КОЛИ `input(check_progress)` → ТО `custom: «показати, чи нема помилок у вже розміченому»` (?).
- КОЛИ `all_constraints_met` → ТО `win`, `custom: «зʼявляється Continue (Space), вітраж повертається у світ»`.
- КОЛИ `input(undo)` → ТО `undo(1)`.
- КОЛИ `input(restart)` → ТО `restart`.
- Перемога: виконано всі картки правил пазла. · Поразки нема. · Рахунку нема; прогрес — відновлені вітражі зон.

## Керування і ввід
- Ліва колонка — 4 режими вводу (тултипи; Shift+Tab — по колу), назви за значками: «пензель + паяльник» (фарба разом із межами (?)), «пензель» (лише фарба), «паяльник» (лише межі), «перо» (вільні нотатки поверх поля, кнопка «стерти нотатки»); під ними «?» — 5-значний ID пазла.
- Палітра 3×3: вісім кольорів і «?» — випадковий колір, що уникає кольорів сусідів; повторне фарбування клітини крутить кольори палітри.
- Клавіші: Esc — вихід, Z або Mouse4 — undo, R — рестарт, Space — Continue після розвʼязку, CTRL + наведення — площа регіону; у трейлері-анонсі ще «Hindsight (H)», на релізі на тому місці кнопка «Check Progress».
- Геймпад: повна підтримка, гліфи міняються самі, redo і «стерти нотатки» на D-pad, правий стік панорамує мапу; Steam Deck Verified.

## Вікна, меню, HUD
- `map-window` / світ: 3D-острови (міст, оглядовий майданчик, село, ліс, замок), плінти з вітражами; вітраж зони, заповнений прогресом, відкриває її назву.
- `game-screen` — пергамент на столі майстра: поле; ліворуч режими, палітра й «?»; Undo (Z), Restart (R), Exit (Esc); праворуч стовпчик карток правил з картинкою-прикладом (`+ui:rule-cards`); вгорі праворуч «Check Progress»; внизу праворуч «Difficulty N»; після розвʼязку — «Continue (Space)».
- `tutorial-window`: поради з картинками (Palisade, Bricky, Loopy, CTRL-лічильник у зоні Precision).
- `settings-window`: Show Errors (Enabled / Side Panel Only / Disabled), сховати Check Progress, палітри, розмір тексту, ліміт FPS, vsync, motion blur, звук у фоні, чутливість стіків.
- `editor-window` + Steam Workshop: розмір сітки міняється без втрати вмісту.
- `+window:letter-window`: лист наприкінці гри зі статистикою проходження; сюжетна рамка — новий патрон, що найняв майстра.
- HUD: `+ui:area-counter` (CTRL), `conflict-highlight` за Show Errors, ID пазла за кнопкою «?».
- Переходи: мапа → плінт → пазл → (розвʼязано) Continue → мапа; Exit — на мапу без розвʼязку.

## Фічі поза полем
- Прогресія зонами: за гайдом 28 зон, більшість названа за правилом, яке вводить, — Rose Windows, Gemini & Delta, Shape Bank, Precision, Polyomino, Mingle Shape, Area Number, Palisade, Match, Mismatch, Range, Solitude, Size Separation, Boxy, Non-Boxy, Bricky, Loopy, Inequality, Difference, Watchtower, Compass; решта — місця (Glimmith Bridge, Forest Trailhead, Castle Gate, Hedge Maze, Spiral Island, Secluded Garden).
- `world-map` з плінтами, «mastery»-фінали, `collectibles` — приховані пазли (острів під Glimmith Overlook), Vidimus-плінти в кінці гри.
- `level-editor` + `level-sharing` через Steam Workshop; Хелловін-конкурс пазлів (до 4 правил, сітка менша за 15×15 або 200 клітин).
- `undo`, `redo`, `restart-level`, `auto-check` (Show Errors), кнопка Check Progress.
- `achievements` (57), картки Steam, плеєр музики, `cloud-save`, `localization` (19 мов, серед них українська — з вересня 2026), `font-scale`, `colorblind-palette` і контрастна палітра, `gamepad-support`.
- DLC Lunar Lights: понад 12 нових правил (анонс листопада 2026).

## Варіації й родичі
- Студія: [Islands of Insight](../thinky/islands-of-insight.md) — сіткові пазли з правилами у відкритому світі; тут лише розбиття на регіони, зате правил більше.
- Окремі правила — класичні паперові пазли: Area Number + Size Separation ≈ [fillomino.md](fillomino.md); Boxy + Area Number ≈ [shikaku.md](shikaku.md); Precision ≈ рівні розміри з [palisade.md](palisade.md) і [pentominous.md](pentominous.md); Shape Bank ≈ [statue-park.md](statue-park.md); Gemini ≈ [double-choco.md](double-choco.md); Compass ≈ [compass.md](compass.md); Inequality / Difference ≈ [futoshiki.md](futoshiki.md), але між площами регіонів.
- Palisade тут показує візерунок меж клітини, а не їхню кількість, як у puzz.link.
- **Осі варіацій**: чим задано регіон — фарбою / межами / обома (Glimmith); де живе правило — картка (глобальне) / символ у клітині / символ на межі; що порівнюють — площу / форму / набір символів; показ помилок — нема / лише на картці / на полі.

## Цікавинки для курсу
- Виділення регіонів: BFS по клітинах через ребра без межі, площа під курсором — 📎.
- Канонічна форма поліоміно з поворотами й віддзеркаленнями; Gemini, Delta, Mismatch, Shape Bank, Polyomino — порівняння ключів — 🥈.
- Рушій правил-плагінів: 20+ валідаторів з картками й підсвіткою порушень у трьох режимах — 🥇.
- Compass і Watchtower: підрахунок клітин регіону за напрямком і кількості регіонів біля точки — 📎 кожне.
- Palisade: межі клітини як 4-бітна маска, порівняння з візерунком з урахуванням поворотів — 🥉.
- Палітра, що підбирає колір, відмінний від сусідів, і нові відтінки при розщепленні регіону — 📎.
- Редактор пазлів зі зміною розміру сітки й перевіркою єдиності розвʼязку — 👑.

## Мапа на каталог
- Є: `satisfy-constraints`, `completion-detection`, `markup-validity`; `cell-click` ↔ фарбування; `edge-marking` ↔ свинцеві межі; `conflict-highlight` ↔ Show Errors; `undo-redo` + `redo` + `restart-level`; `in-game-editor` + `editor-window` ↔ редактор; `world-map` + `map-window` ↔ острови з плінтами; `tutorial-window`, `settings-window`, `game-screen`, `keyboard-controls`; `level-rating` ↔ Difficulty N; `background-music` ↔ плеєр музики.
- Повтори з корпусу: `+cell-coloring`, `+equal-size-partition` (Precision), `+region-size-check` (Area Number, Range, Minimum, Size Separation), `+shape-identity-check` (Gemini, Delta, Mismatch), `+rect-shape-check` (Boxy), `+shape-bank` (тут фігура з банку, можливо, повторюється (?)), `+compass-clue`, `+region-symbol-count` (Solitude, Rose Windows), `+edge-inequality-clue` (Inequality, Difference — між площами), `+rules-panel`, `+free-draw-notes`, `+open-world-puzzles`, `+workshop-sharing`, `+secret-area`.
- **Нема** → пропозиції карток:
  - `+border-pattern-clue` «Клітина показує візерунок своїх меж, повороти дозволено» · game-logic/constraints · 📎.
  - `+region-shape-clue` «Гліф-поліоміно задає форму свого регіону» · game-logic/constraints · 🥉.
  - `+touching-regions-count` «Число = скільки регіонів торкається підказки» · game-logic/constraints · 📎.
  - `+region-area-hover` «Утримати клавішу й навести — підсвітити регіон і показати його площу» · interface/hud · 🌱.
  - `+error-display-modes` «Показ помилок: на полі / лише на картці правила / вимкнено» · interface/settings · 🌱.
  - `+custom-palette` «Палітра фарб: авто на пазл, свої набори, випадковий колір, що уникає сусідів» · interface/settings · 📎.

## Пропозиції до словників
- `+cond:region_shape(r, s)` — форма регіону з точністю до повороту чи віддзеркалення.
- `+cond:area_between(r, a, b)` — площа регіону в межах [a, b].
- `+effect:set_edge(edge, wall|join)` — зробити ребро межею або зʼєднати клітини.
- `+ui:rule-cards` — стовпчик карток правил біля поля з картинкою-прикладом.
- `+ui:area-counter` — лічильник площі регіону під курсором.
- `+feature:show-errors-modes`, `+feature:custom-palette` — див. мапу.
- `+window:letter-window` — лист-повідомлення між зонами й у кінці, зі статистикою.
- `+axis:rules` — `unlocked`: нові правила відкриваються зонами й далі змішуються.
- `+card:border-pattern-clue`, `+card:region-shape-clue`, `+card:touching-regions-count`, `+card:region-area-hover`, `+card:error-display-modes`, `+card:custom-palette`.

## Джерела
- ⭐ [Steam: The Artisan of Glimmith](https://store.steampowered.com/app/4160210/The_Artisan_of_Glimmith/) — опис (понад 20 правил, «color, cut, and join», mastery, редактор), 57 досягнень; 16 скриншотів з картками й полями; два трейлери (кадри щосекунди): ще картки Shape Bank, Boxy, Inequality, Difference, Watchtower, Precision (5) і (7), Minimum (4), процес малювання меж і компаси.
- [Steam News](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=4160210&count=30) — 16 новин: режими вводу з тултипами, CTRL-лічильник, межа або стерта клітина розщеплює регіон, Show Errors, Auto Palette, нотатки, Workshop-конкурс, мови, Lunar Lights.
- [Yekbot: walkthrough](https://www.yekbot.com/the-artisan-of-glimmith-walkthrough-guide/) — 28 зон, кількість пазлів у кожній, складність 1–7, кольори плінтів.
- YouTube: пошук «The Artisan of Glimmith gameplay».

## Непевне
- (?) Визначень Match, Non-Boxy, Bricky, Loopy, Mingle Shape не бачив — лише назви зон і новин. Здогад: Match — «усі регіони однакової форми» (пара до Mismatch; французькою Pareille / Pas Pareille), Non-Boxy — «жоден регіон не прямокутник».
- (?) Точна дія режимів: чи мазок пензлем сам зʼєднує клітини й ставить межі з іншими кольорами.
- (?) Watchtower — підказка в клітині чи у вершині сітки.
- (?) Чи Polyomino, Gemini й Delta враховують повороти й віддзеркалення (картка Palisade прямо каже «All rotations can be used», інші — ні).
- (?) Shape Bank — чи може фігура з банку повторюватися.
- (?) Кількість пазлів: гайд дає 11–70 на зону, разом близько 1200; офіційно число приховують.
- (?) Як обходять світ (камера-мапа чи аватар) і що означають кольори плінтів.
- (?) Що саме робить Check Progress (у ранній версії — «Hindsight (H)»).
