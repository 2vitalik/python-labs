---
title: Picross-варіанти (Picross 3D, Round 2, Mega, Color, Clip)
slug: picross-variants
aka: [Picross 3D, Rittai Picross, 立体ピクロス, Picross 3D Round 2, Mega Picross, Color Picross, Clip Picross]
family: pencil-logic
also: []
klass: puzzle
axes:
  field: 3d
  time: realtime
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2009
platforms: [Nintendo DS, 3DS, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Picross_3D", best: true, note: "Picross 3D: блок кубів, молот і пензель, числа просте/в колі/у квадраті, 5 помилок, зірки, челенджі, редактор"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Picross_3D:_Round_2", note: "Round 2: сині й помаранчеві блоки, подвійні числа, прапорці, бомби, штраф очок, amiibo"}
  - {kind: other, url: "https://www.siliconera.com/rittai-picross-putting-the-pieces-together/", note: "огляд японської версії: обертання стилусом, розрізи шарів"}
  - {kind: other, url: "https://www.nintendoworldreport.com/review/23121/picross-3d-nintendo-ds", note: "рецензія: керування, слайсер"}
  - {kind: official, url: "https://www.nintendo.com/eu/media/downloads/games_8/emanuals/nintendo_3ds_2/picross3dround2/ElectronicManual_Nintendo3DS_Picross3DRound2_EN.pdf", note: "мануал Round 2 (PDF; текст не витягнув)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Picross_S", note: "Switch-серія: Mega, Clip (S2), Color (S3)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=picross+3d+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [satisfy-constraints, completion-detection, wrong-mark-lose, time-out, time-bonus, level-bank, level-select, level-unlock, in-game-editor, level-exchange, run-length-clues, cell-click, +picture-reveal, +color-runs, +mega-clue, +clip-composite, +group-count-clue, +voxel-carve, +slice-view, +orbit-camera, +protect-mark, +strike-limit, +stars-by-time-and-strikes]
proposes: ["+cond:group_count", "+effect:carve", "+ui:slice-slider", "+ui:strike-counter", "+ui:tool-toggle", "+feature:slice-view", "+feature:one-chance-mode", "+feature:construction-challenge", "+axis:field-3d-clues", "+card:group-count-clue", "+card:voxel-carve"]
author: opus
date: 2026-11-09
---

# Picross-варіанти — що Nintendo/HAL додали до нонограми: третій вимір, кількість груп замість серій, кольори, мега-підказки й мозаїки

## Суть
Базова нонограма вже описана — [nonogram.md](nonogram.md); тут лише те, що додають варіанти. Головне — **Picross 3D** (HAL Laboratory, DS, 2009): замість плоскої сітки — суцільний блок кубів, гравець молотом розбиває зайві кубики й пензлем позначає потрібні, доки не лишиться 3D-модель. Підказка на лінії кубів — одне число й **форма**: просте число — кубики однією групою, у колі — двома, у квадраті — трьома й більше; порядку груп нема. Round 2 (3DS, 2015) додає два кольори блоків; Switch-режими Mega, Color, Clip змінюють геометрію чи колір підказок у 2D.

## Поле і час
- Picross 3D: прямокутний паралелепіпед кубів X×Y×Z; кожна лінія вздовж однієї з трьох осей має не більше однієї підказки, а багато ліній — без підказки (нема правила).
- Підказки намальовані на гранях кубів, що виходять на зовнішню поверхню ряду; щоб їх прочитати, блок обертають.
- Видимість: внутрішні шари закриті зовнішніми — слайсер тимчасово ховає шари з одного боку, щоб дістатись усередину.
- Час: таймер-ліміт на пазл (realtime-тиск); у Time Challenge кожен розбитий куб додає час.
- 2D-варіанти (Switch S-серія): та сама сітка нонограми; Mega — підказка на два ряди, Color — серії кольорів, Clip — пазл як шматок більшої картини.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Куб | mark | unknown / painted / broken | розбитий зникає; пофарбований захищений від молота; лишаються кубики моделі |
| Підказка (просте n) | static | n | у лінії рівно n кубів однією групою |
| Підказка в колі (n) | static | n | рівно n кубів двома групами |
| Підказка в квадраті (n) | static | n | рівно n кубів трьома й більше групами |
| Лінія без підказки | static | — | обмежень нема — кубики в ній визначаються перпендикулярними лініями |
| Молот | — | інструмент | розбиває куб; якщо куб — частина моделі, це strike |
| Пензель | — | інструмент | позначає куб «лишити»; такий куб не можна розбити |
| Слайсер | — | вісь, глибина | ховає шари з одного боку; тимчасовий, не змінює стан |
| Синій блок (Round 2) | mark | — | прямий квадратний блок моделі |
| Помаранчевий блок (Round 2) | mark | — | після фарбування стає вигнутим/зрізаним блоком — деталь форми моделі |
| Подвійне число (Round 2) | static | синє + помаранчеве | лінія рахує блоки обох кольорів |
| Прапорець (Round 2) | mark | колір | «можливо тут блок цього кольору» — нотатка |
| Бомба (Round 2) | — | інструмент | швидко очищує ряди й стовпці без блоків |
| Мега-підказка (Mega Picross) | static | n на 2 ряди | одна підказка охоплює пару рядків/стовпців (див. nonogram) |
| Кольорова серія (Color Picross) | static | (n, колір) | серії різного кольору можуть торкатись, однакового — ні |
| Clip-фрагмент | zone | малий пазл | розвʼязані фрагменти складають велику картину |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(hammer, cube)` → ЯКЩО `state(cube, painted)` → ТО `block`; ЯКЩО `custom: «куб не з моделі»` → ТО `disappear_b`; інакше `counter(strikes, +1)`, `message(warning)`, куб лишається.
- КОЛИ `counter(strikes, ==, 5)` → ТО `restart` (Picross 3D: п'ять помилок — пазл з початку).
- КОЛИ `input(paint, cube)` → ТО `set_state(cube, painted)`; повтор → `clear_state(cube, painted)`.
- КОЛИ `input(drag, view)` → ТО `rotate(block, deg)` — обертання блоку стилусом (без натиснутої кнопки).
- КОЛИ `input(slice, axis, depth)` → ТО `hide(layers)` з одного боку; відпускання → `reveal(layers)`.
- КОЛИ `constraint_broken(line)` → ЯКЩО `custom: «у лінії не n кубів моделі або кількість груп ≠ формі підказки»` (`+cond:group_count`) → ТО `custom: «стан не розвʼязок»` — у грі це видно лише через strike молота (перевірка проти задуманої моделі).
- КОЛИ `counter(time_left, ==, 0)` → ТО `lose` / `restart` (ліміт часу) (?).
- КОЛИ `all_constraints_met` → ТО `win`, `custom: «модель розфарбовується й анімується»`, `score(stars)` — до 3 зірок за швидкість і кількість помилок.
- КОЛИ `win` → ЯКЩО `custom: «набрано достатньо зірок на рівні»` → ТО `unlock(bonus_puzzles)`.
- КОЛИ `input(hammer, cube)` → ЯКЩО `mode(time_challenge)` and `custom: «куб не з моделі»` → ТО `timer(+n)` (?).
- КОЛИ `input(hammer, cube)` → ЯКЩО `mode(one_chance)` and `custom: «куб з моделі»` → ТО `lose`.
- КОЛИ `input(paint_color, cube)` → ЯКЩО `custom: «колір не збігається з моделлю»` → ТО `score(-n)` (Round 2: штраф очок за хибний колір чи розбитий блок).
- КОЛИ `input(bomb, line)` → ЯКЩО `custom: «лінія без блоків»` → ТО `clear(line)` (Round 2) (?).
- Color Picross (2D): КОЛИ `constraint_broken(runs)` → ЯКЩО `same(run_a, run_b, color)` and `custom: «сусідні без пропуску»` → ТО конфлікт; різні кольори — дозволено.
- Перемога: лишилась рівно модель (усі лінії з підказками виконані). Поразка: 5 strikes → рестарт; One-Chance — з першої помилки. Рахунок: зірки (час + помилки) / очки (Round 2).

## Керування і ввід
- Picross 3D (DS): стилус тягне — обертання (360° по горизонталі, 180° по вертикалі); D-pad / кнопки перемикають пензель (вправо або Y) і молот (вгору або X); тап по кубу — дія поточного інструмента.
- Слайсер: повзунки по двох осях на краях екрана тимчасово знімають шари (зверху/збоку), щоб дістати внутрішні куби (?) — рецензенти скаржаться, що після зуму важко «вийти» зі зрізу.
- Round 2 (3DS): два кольори пензля, прапорці, бомби; перепризначення керування в Settings.
- Switch S-серія (2D): кнопки + тач, як у nonogram.md.

## Вікна, меню, HUD
- `game-screen`: блок кубів у 3D + `timer-countdown` + `+ui:strike-counter` + `+ui:tool-toggle` (пензель/молот) + `+ui:slice-slider`.
- `level-select`: рівні за складністю (Easy/Medium/Hard у Round 2), зірки на кожному пазлі, бонус-пазли за зірки.
- `end-screen`: анімація моделі, зірки; модель додається до тематичної колекції (`+window:picture-gallery`, пропозиція nonogram).
- `tutorial-window`: «technique»-уроки на початку.
- `mode-select`: основний режим · One-Chance · Time Challenge · Construction Challenge.
- `editor-window`: створення власних пазлів; Wi-Fi-обмін (до 2014) / локальна передача.
- Переходи: main-menu → level-select → game-screen → end-screen (модель) → колекція / наступний.

## Фічі поза полем
- `stars-rating` (до 3, за час і помилки) → `level-unlock` бонусних пазлів; бонусні анімації за проходження складностей.
- `+feature:one-chance-mode` (одна помилка — кінець), `mode-time-attack` (Time Challenge: час за розбиті куби), `+feature:construction-challenge` (кілька пазлів → одна велика модель).
- `level-editor` + `level-sharing` (Nintendo Wi-Fi Connection до 2014, далі — локально), тематичні конкурси пазлів.
- `tutorial` (technique), `puzzle-bank` — 350 пазлів основного режиму (Picross 3D), понад 370 (Round 2) + amiibo-пазли (до 9).
- Нема: undo (помилка — strike, а не крок історії) (?).

## Варіації й родичі
- Picross 3D (2009 JP, 2010 EU/NA) → Picross 3D: Round 2 (3DS: JP 10.2015, NA 09.2016 лише eShop, EU 12.2016).
- 2D-режими Nintendo/Jupiter — [nonogram.md](nonogram.md): Mega (підказка на 2 ряди), Clip (S2), Color (S3); Picross e (3DS), Picross S (Switch).
- Інші 3D-нонограми й «Voxel»-клони — не перевіряв (?).
- **Осі варіацій**: розмірність (2D / 3D) · що каже підказка (послідовність серій / сума + кількість груп / сума по 2 рядах) · кольори (1 / 2 в 3D / N у 2D) · ціна помилки (нічого / strike / програш / очки) · композиція (один пазл / Clip / Construction).

## Цікавинки для курсу
- Підказка «сума + кількість груп» (просте / коло / квадрат): RLE-рядок → (довжина, групи) — 🌱.
- Воксельне поле X×Y×Z з лініями по трьох осях і підказками лише на частині — 📎.
- Обертання камери навколо блоку + вибір куба під курсором (ray-cast у вокселі) — 🥈.
- Слайсер: показати лише шари ≥ k по осі — 📎.
- Розвʼязувач 3D: лінійний солвер нонограми, але з групами замість серій і по трьох осях — 🥇.
- Захисна мітка (пензель) робить молот безпечним — 🌱; strikes проти задуманої моделі — 🌱.
- Генератор з 3D-моделі: які лінії лишити без підказки, щоб розвʼязок лишився єдиним — 👑.

## Мапа на каталог
- Є: `satisfy-constraints`, `completion-detection` · `wrong-mark-lose` ↔ One-Chance · `time-out` ↔ ліміт часу · `time-bonus` ↔ Time Challenge · `level-bank`, `level-select`, `level-unlock` (бонус за зірки) · `in-game-editor`, `level-exchange` · `run-length-clues` ↔ база з нонограми · `cell-click` ↔ тап по кубу.
- Перевикористано з nonogram: `+picture-reveal`, `+color-runs`, `+mega-clue`, `+clip-composite`.
- **Нема** → пропозиції карток:
  - `+group-count-clue` «Підказка: сума + кількість груп (1 / 2 / 3+)» · game-logic/constraints · 🌱.
  - `+voxel-carve` «Висікання моделі з блоку кубів» · entities/state · 📎.
  - `+slice-view` «Тимчасово сховати шари поля» · interface/render · 📎.
  - `+orbit-camera` «Обертання камери навколо 3D-поля» · interface/render · 🥉.
  - `+protect-mark` «Мітка, що захищає від руйнівної дії» · interface/input · 🌱.
  - `+strike-limit` «N помилок — рестарт» · game-logic/lose · 🌱 · слот {limit: 5}.
  - `+stars-by-time-and-strikes` «Зірки за час і помилки» · levels/progression · 🌱.

## Пропозиції до словників
- `+cond:group_count` — кількість груп у лінії порівняно з n (1 / 2 / ≥3).
- `+effect:carve` — прибрати куб/клітинку з тіла моделі (руйнівна розмітка, протилежна `mark`).
- `+ui:slice-slider` — повзунок зрізу шарів; `+ui:strike-counter` — лічильник помилок з лімітом; `+ui:tool-toggle` — перемикач двох інструментів (пензель/молот).
- `+feature:slice-view`, `+feature:one-chance-mode`, `+feature:construction-challenge`.
- `+axis:field-3d-clues` — для `field: 3d`: підказки на лініях трьох осей (до осі field).
- `+card:group-count-clue`, `+card:voxel-carve` — див. мапу.

## Джерела
- ⭐ [Wikipedia: Picross 3D](https://en.wikipedia.org/wiki/Picross_3D) — правила 3D (число / коло = 2 групи / квадрат = 3+), молот і пензель, 5 strikes, ліміт часу, зірки, режими One-Chance / Time / Construction, 350 пазлів, Wi-Fi до 2014.
- [Wikipedia: Picross 3D: Round 2](https://en.wikipedia.org/wiki/Picross_3D:_Round_2) — сині/помаранчеві блоки, подвійні числа, прапорці, бомби, штраф очок, amiibo, 370+ пазлів, дати релізів.
- [Siliconera: Rittai Picross](https://www.siliconera.com/rittai-picross-putting-the-pieces-together/) і [Nintendo World Report](https://www.nintendoworldreport.com/review/23121/picross-3d-nintendo-ds) — обертання стилусом, слайсер (бачив у результатах пошуку, сторінки не відкривав).
- [Мануал Round 2 (PDF)](https://www.nintendo.com/eu/media/downloads/games_8/emanuals/nintendo_3ds_2/picross3dround2/ElectronicManual_Nintendo3DS_Picross3DRound2_EN.pdf) — завантажив, текст не витягнувся.
- [Wikipedia: Picross S](https://en.wikipedia.org/wiki/Picross_S) — 2D-режими (детально — у nonogram.md).
- YouTube: пошук «picross 3d gameplay».

## Непевне
- (?) Точне правило Mega Picross — як у nonogram.md, жодне відкрите джерело не дало формулювання.
- (?) Слайсер: дві осі чи чотири напрямки, кнопки — джерела розходяться (результати пошуку).
- (?) Що робить вичерпаний таймер у Picross 3D (поразка чи рестарт) і скільки часу додає Time Challenge — не бачив чисел.
- (?) Round 2: як саме працюють бомби й подвійні числа (окремий лічильник для кожного кольору?) — Wikipedia лише називає; мануал не прочитався.
- (?) Undo в Picross 3D — не згадано в джерелах; припускаю, що нема.
- (?) `time: realtime` — через таймер-ліміт; сам пазл статичний.
