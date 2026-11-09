---
title: 4D (Beekie & Corey Hardt) і 4D-Sokoban-родичі
slug: 4d-sokoban
aka: [4D, 4D (Corey Hardt), 4D Sokoban, 4D Intuition, 四维直觉]
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: graph
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2021
platforms: [web (PuzzleScript, HTML5), PC (4D Intuition), macOS (4D Intuition)]
links:
  - {kind: itch, url: "https://coreyhardt.itch.io/4d", best: true, note: "грати в браузері; Beekie + Corey Hardt, PuzzleScript, 7 рівнів; коментарі: X перемикає пари осей, «кожна колонка — 4 зрізи куба», посилання на альтернативні види"}
  - {kind: play, url: "https://html-classic.itch.zone/html/7651970/index.html", note: "вбудована PuzzleScript-збірка з повним вихідним кодом (OBJECTS / RULES / LEVELS)"}
  - {kind: other, url: "https://api.github.com/gists/0c0062d17fefe9d6d4e54d354b31edc2", note: "варіант «Beekie & Tilmann (made worse by Tilmann)», гіст knexator від 2021-07-01: action транспонує все поле; 5 рівнів демо"}
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=0c0062d17fefe9d6d4e54d354b31edc2", note: "той самий варіант Tilmann у плеєрі PuzzleScript (посилання з коментаря tess)"}
  - {kind: itch, url: "https://knexator.itch.io/4d-sokoban", note: "4D Sokoban (knexator): два поля поруч — XY і ZW; модифікація оригіналу Beekie, натхнення — варіант Tilmann"}
  - {kind: steam, url: "https://store.steampowered.com/app/3635130/4D_Intuition/", note: "4D Intuition (Yu Gu, 2026): 4D через віртуальний «3D-дисплей», 5 розділів, 64 рівні, ходьба, стрибки, фото 4D-обʼєктів, стоси гіперкубів, 4D-Sokoban, редактор і Workshop"}
  - {kind: other, url: "https://steamcommunity.com/app/3635130/reviews/?browsefilter=toprated&l=schinese", note: "відгуки CN про 4D Intuition: канали в одну клітину, перекочування циліндрів, крихка підлога, без undo, один сейв у рівні"}
  - {kind: other, url: "https://steamcommunity.com/app/3635130/discussions/0/573795560006607334/", note: "розробник 4D Intuition: каркасні лінії, колір = орієнтація/висота, товщина = важливість лінії сітки; клавіші E/Z/Q — ana/kata"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=4D+Intuition+gameplay", note: "пошук; геймплей 4D Intuition"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=4D+puzzlescript+sokoban+Corey+Hardt", note: "пошук; 4D на PuzzleScript"}
stage: v1
coverage: 65
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, impassable-cells, all-on-targets, undo-unlimited, restart-level, sequential-levels, level-from-txt, mode-indicator, highlights, sound-effects, gravity-fall, orientation-state, in-game-editor, level-exchange, save-single-slot, +slice-view, +n-dimensional-neighborhood, +axis-pair-switch, +world-transpose, +projection-view, +photo-match-goal]
proposes: ["+axis:field=nd", "+card:axis-pair-switch", "+card:world-transpose", "+card:projection-view", "+card:photo-match-goal", "+ui:plane-highlight", "+window:message-screen", "+feature:view-toggle"]
author: opus
date: 2026-11-09
---

# 4D — Sokoban у сітці 4×4×4×4: клавіша X перемикає, по якій парі осей ти ходиш

## Суть
Звичайний Sokoban (штовхни ящики на цілі), але простір — чотиривимірна сітка 4⁴ = 256 клітин, намальована як дошка 4×4 з малих полів 4×4. Стрілки рухають аватара всередині малого поля (осі 1–2); клавіша X перемикає аватара на іншу пару осей (3–4) — тоді стрілка переносить його на ту саму позицію в сусідньому малому полі. Ящики штовхаються в обох режимах, тож «прохід» може йти крізь поля, яких на око ніщо не зʼєднує. Нижче — огляд родичів: варіант Tilmann (X транспонує весь світ), 4D Sokoban knexator (два поля XY і ZW) і комерційна 4D Intuition, де 4D видно через «3D-дисплей».

## Поле і час
- Логіка: клітина = (x, y, X, Y), кожна координата 0–3; (x, y) — позиція всередині малого поля, (X, Y) — номер малого поля. На екрані — 21×21 клітин PuzzleScript: клітина (5X+1+x, 5Y+1+y), між полями — рамка WallGap.
- Сусідство: 8 сусідів по 4 осях; але в кожен момент аватар ходить лише в одній площині — (x, y) або (X, Y).
- Стіни `#` — клітини самого 4D-простору (в обох режимах непрохідні); рамка лише розділяє зрізи. Поле не тор: за краєм — `block`.
- Хід = один ввід (`time: turn`); підсвітка площини оновлюється після кожного ходу (late-правила).
- Поворот камери чи інший вигляд не передбачено: гравці скаржаться, що поле «здається більшим, ніж є», і пропонують інші проєкції.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Аватар, режим Main | player | жовтий | крок на 1 у малому полі (осі 1–2); штовхає ящик |
| Аватар, режим Alt | player | рожевий | крок = перехід на ту саму (x, y) у сусідньому малому полі (осі 3–4); штовхає ящик так само |
| Ящик | object | — | зсувається на 1 по поточній осі, якщо за ним вільно; ланцюгом не штовхається |
| Ціль | terrain | — | перемога, коли на кожній цілі ящик |
| Стіна | static | — | непрохідна для аватара й ящика по всіх осях |
| Рамка (WallGap) | static | — | межа зрізу: у Main не пускає за край малого поля; у Alt її «перестрибують» |
| Підсвітка площини | mark | — | Main — усе поточне мале поле; Alt — 16 клітин з тією ж (x, y) в усіх полях |
| Контур рамок | mark | — | декоративні ребра біля WallGap |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(action)` → ЯКЩО `state(player, main)` → ТО `transform(player, player_alt)`, `sound(sfx1)`; ЯКЩО `state(player, alt)` → ТО `transform(player, player_main)`, `sound(sfx1)`.
- КОЛИ `input(dir)` → ЯКЩО `state(player, main)` and `free(next_cell)` → ТО `move(player, dir)`.
- КОЛИ `contact(player_main, crate)` → ЯКЩО `free(cell_behind)` → ТО `push(crate)`, `move(player, dir)`, `sound(crate_move)`; інакше `block` (рамка, стіна, другий ящик).
- КОЛИ `input(dir)` → ЯКЩО `state(player, alt)` and `custom: «у сусідньому малому полі на тій самій (x, y) нема ні ящика, ні стіни»` → ТО `move(player, dir)` по осі 3/4, `sound(sfx0)`.
- КОЛИ `input(dir)` → ЯКЩО `state(player, alt)` and `occupied(next_cell_axis34, crate)` and `custom: «наступна клітина за ящиком по тій самій осі без стіни і ящика»` → ТО `push(crate)`, `move(player, dir)`, `sound(sfx2)`; інакше `block`.
- КОЛИ `edge(player)` → ТО `block` (за останнім малим полем клітин нема).
- КОЛИ `after(move)` → ТО `custom: «перемалювати підсвітку: Main — мале поле, Alt — площина (X, Y) через аватара»`.
- КОЛИ `all_on(crate, target)` → ТО `win`, `next_level` (PuzzleScript: «All Target on Crate» — кожна ціль накрита).
- КОЛИ `input(undo)` → ТО `undo(1)` (без ліміту); КОЛИ `input(restart)` → ТО `restart`.
- Перемога: усі цілі накриті · Поразка: нема (глухий кут — undo / рестарт) · Рахунок: нема.

## Керування і ввід
- Стрілки (або WASD) — крок у поточній площині; X — перемкнути пару осей (у PuzzleScript action також на пробілі — коментатори називають обидві клавіші).
- Z — undo, R — рестарт, Esc — меню (стандарт PuzzleScript).
- Підказка автора до рівня 3: «стань на сусідню клітину, а потім рухайся *в* ящик» — тобто заходити до ящика з іншої осі.

## Вікна, меню, HUD
- `main-menu`: титул PuzzleScript — «4D», автори Beekie + Corey Hardt, start / continue (?).
- `+window:message-screen` перед кожним рівнем — назва: A Normal Puzzle → A Normal Puzzle? (X) → One More Time → Corners → Blockage → Passages → Microbes → «Thanks 4 playing!».
- `game-screen`: дошка 4×4 малих полів, без чисел; `mode-indicator` — колір аватара (жовтий / рожевий) і `+ui:plane-highlight` — фіолетова підсвітка площини руху.
- Переходи: main-menu → message-screen → game-screen → (усі цілі накриті) → наступне повідомлення.

## Фічі поза полем
- `levels-sequential` (7 рівнів), `undo` ∞, `restart-level`, `continue` у браузері (?).
- Звуки: ящик, перемикання режиму, крок і поштовх в Alt — окремі sfx.
- Рівні — ASCII-мапи 21×21 у коді PuzzleScript; вихідний код відкритий у збірці.

## Варіації й родичі
### Варіант Tilmann (PuzzleScript, гіст від 2021-07-01)
- Аватар завжди ходить у малому полі, а X **транспонує світ**: міняє місцями внутрішні й зовнішні координати (x ↔ X, y ↔ Y) для аватара, ящиків, стін і цілей.
- КОЛИ `input(action)` → ТО `custom: «кожен обʼєкт (x, y, X, Y) → (X, Y, x, y)»` — поворот у 4D замість зміни режиму руху.
- Підсвічується та сама (x, y) в усіх малих полях; 5 рівнів демо (без Blockage і Microbes).

### 4D Sokoban (knexator, PuzzleScript, девлог 2022-09-29)
- Два поля поруч: ліве — проєкція на осі XY, праве — на ZW; рух у лівому йде по XY, у правому — по ZW.
- Модифікація оригіналу Beekie з рівнем Corey Hardt, натхнена варіантом Tilmann; автор сам називає її «just about barely unplayable».

### 4D Intuition (Yu Gu, 2026) — межа сімʼї (`field: free` для аватара)
- Аватар рухається неперервно (координати X, Y, Z, H з дробами), ходить і стрибає під гравітацією; 4D-світ видно на віртуальному «3D-дисплеї» каркасними лініями: колір — орієнтація поверхні / висота, товщина — важливість лінії сітки.
- Сітковий шар: підлога й обʼєкти однакового розміру, канали «в одну клітину заввишки»; обʼєкти — гіперкуб, гіперсфера, сфероциліндр, дуоциліндр та інші.
- Механіки (5 розділів, 64 рівні): ходьба в 3D-підпросторі, стрибки, збір цілей; «3D-фото» 4D-обʼєкта з потрібного ракурсу; стоси гіперкубів; 4D-Sokoban — штовхнути форму на ціль за мінімум перекочувань (циліндри котяться, гіперкуб можна заштовхнути на обʼєкт тієї ж висоти).
- Поле: білі платформи-цілі, червоні зони, точка появи, синя крихка підлога (?).
- КОЛИ `contact(player, cylinder)` → ЯКЩО `free(cell_behind)` → ТО `custom: «форма перекочується, змінюючи орієнтацію в 4D»`.
- КОЛИ `custom: «знімок 3D-дисплея збігся із заданим ракурсом»` → ТО `win` (розділ 2).
- Керування: миша (камера) + клавіатура, E/Z/Q — рух по ana/kata; геймпад придатний; види — від першої / третьої особи, зверху, «hyperplane illusion», поворот погляду; бічні грані підписані 金 / 木 / 水 / 火; координати — опційно.
- Фічі: undo нема, один сейв / завантаження всередині рівня (поруч із рестартом), `in-game-editor` + Steam Workshop, демо, EN + 简体中文.

### Осі варіацій
- **Як показати 4D**: сітка 2D-зрізів 4×4 (4D) / два 2D-поля XY + ZW (knexator) / 3D-проєкція на «дисплеї» з обертанням камери (4D Intuition).
- **Як ходити 4-ю віссю**: перемикач пари осей (4D) / транспонування світу (Tilmann) / окремі клавіші ana/kata (4D Intuition).
- **Що штовхається**: ящик-клітина (PuzzleScript) / форми, що перекочуються й ставляться в стоси (4D Intuition).
- Родичі в корпусі: 4D Minesweeper — `hidden-deduction/minesweeper-dimensions` (те саме «поле як сітка зрізів»); класичний Sokoban — `push-slide`; Patrick's Parabox (поле в полі) — `thinky/patricks-parabox`.

## Цікавинки для курсу
- 4D-сітка як 2D-масив зрізів і перерахунок (x, y, X, Y) ↔ екранна клітина — 🌱.
- Перемикач пари осей + підсвітка площини руху (4 рядки правил у PuzzleScript) — 📎.
- Транспонування світу (x ↔ X, y ↔ Y) як «поворот у 4D» — 📎.
- Sokoban з 8 напрямками поштовху і розвʼязувач BFS по станах у 4⁴ — 🥇.
- Deadlock-перевірка в 4D: «кут» — ящик заблоковано по всіх осях — 🥇.
- Каркасна 3D-проєкція тесеракта з обертанням (4D Intuition) — 🥈.
- Перекочування циліндра / дуоциліндра як стан орієнтації в 4D — 👑 (геометрія орієнтацій у 4D нетривіальна).

## Мапа на каталог
- Є: `move-4dir` + `move-by-input` + `keyboard-controls` ↔ стрілки в площині; `push-object` ↔ ящики; `impassable-cells` ↔ стіни й рамки; `all-on-targets` ↔ «All Target on Crate»; `undo-unlimited` + `restart-level` ↔ Z / R; `sequential-levels` ↔ 7 рівнів; `level-from-txt` ↔ ASCII-рівні PuzzleScript; `mode-indicator` ↔ колір аватара; `highlights` ↔ підсвітка площини; `sound-effects`; для 4D Intuition — `gravity-fall`, `orientation-state` (перекочування), `in-game-editor` + `level-exchange` (Workshop), `save-single-slot`.
- **Нема** → пропозиції карток:
  - `+slice-view` (4D Minesweeper) — багатовимірне поле як сітка 2D-зрізів.
  - `+n-dimensional-neighborhood` (4D Minesweeper) — сусідство по N осях.
  - `+axis-pair-switch` «Клавіша перемикає пару осей, якими рухається аватар» · entities/move · 📎.
  - `+world-transpose` «Ввід переставляє координати всього світу» · entities/move · 📎.
  - `+projection-view` «Проєкція вищого виміру на 3D/2D з обертанням камери» · interface/render · 🥈.
  - `+photo-match-goal` «Мета — знімок обʼєкта з заданого ракурсу» · game-logic/win · 🥉.

## Пропозиції до словників
- `+axis:field=nd` — N-вимірна сітка (вже пропоновано в 4D Minesweeper); тут `field: graph` як найближче.
- `+card:axis-pair-switch`, `+card:world-transpose`, `+card:projection-view`, `+card:photo-match-goal` — див. «Мапа на каталог».
- `+ui:plane-highlight` — підсвітка площини / зрізу, в якому зараз діє аватар.
- `+window:message-screen` — екран-повідомлення PuzzleScript між рівнями (назва рівня).
- `+feature:view-toggle` (Kwirk) — 4D Intuition: перемикання видів без зміни логіки.

## Джерела
- ⭐ [itch.io: 4D](https://coreyhardt.itch.io/4d) — гра в браузері, автори, коментарі про X / пробіл, «4 зрізи куба», посилання на альтернативні види.
- [Вбудована збірка 4D](https://html-classic.itch.zone/html/7651970/index.html) — повний PuzzleScript-код: обʼєкти, правила Main / Alt, підсвітка, 7 рівнів, умова перемоги.
- [Гіст варіанта Tilmann](https://api.github.com/gists/0c0062d17fefe9d6d4e54d354b31edc2) — код транспонування світу, 5 рівнів демо, дата 2021-07-01.
- [itch.io: 4D Sokoban (knexator)](https://knexator.itch.io/4d-sokoban) — два поля XY / ZW, походження від Beekie, девлог 2022-09-29.
- [Steam: 4D Intuition](https://store.steampowered.com/app/3635130/4D_Intuition/) — опис, розділи й рівні, 3D-дисплей, редактор, Workshop.
- [Steam: відгуки 4D Intuition (CN)](https://steamcommunity.com/app/3635130/reviews/?browsefilter=toprated&l=schinese) — форми, перекочування, крихка підлога, зони, без undo, один сейв.
- [Steam: відгуки 4D Intuition (EN)](https://steamcommunity.com/app/3635130/reviews/?browsefilter=toprated&l=english) — види камери, hyperplane illusion, миша / геймпад.
- [Steam: «Crucial Game Idea»](https://steamcommunity.com/app/3635130/discussions/0/573795560006607334/) — розробник про лінії й глибину, E/Z/Q.
- [Steam: «边缘处无法起跳»](https://steamcommunity.com/app/3635130/discussions/0/586181370788725118/) — неперервні координати X/Y/Z/H, стрибок і опора.

## Непевне
- (?) Рік: на itch — квітень 2023, але гіст із варіантом Tilmann датований 2021-07-01 і вже містить рівні оригіналу Beekie, тож перша версія — не пізніше 2021; рівні Blockage і Microbes додано пізніше.
- (?) Титул і «continue» — стандарт PuzzleScript, у самій грі не перевірено; призначення пробілу як action — зі слів коментаторів.
- (?) 4D Intuition: дата релізу (Steam — 15.07.2026, одна з карток — 01.03.2026), чи рух ящиків строго по клітинах, що робить синя крихка підлога і червоні зони — лише з відгуків; англомовні відгуки згадують і 4D-кубик Рубіка (?).
- (?) 4D Intuition має власні 64 рівні й редактор — коли зʼявляться джерела на правила, її варто винести в окремий файл.
