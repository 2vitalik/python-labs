---
title: Zenji
slug: zenji
family: connect-rotate
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: setup
  goal: state
year: 1984
platforms: [Atari 8-bit, Atari 5200, C64, ColecoVision, MSX, ZX Spectrum]
links:
  - {kind: other, url: "https://spectrumcomputing.co.uk/pub/sinclair/games-info/z/Zenji.txt", best: true, note: "оригінальна інструкція ZX: мета «Zenji», поворот, Flames of Desire, таймер, очки, 8 рівнів, 1+4 життя"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Zenji_(video_game)", note: "Matthew Hubbard, Activision, джерело з зеленим світлом, платформи, відгуки"}
  - {kind: other, url: "https://spectrumcomputing.co.uk/entry/5850/ZX-Spectrum/Zenji", note: "картка ZX: керування, 2 гравці, інструкція PDF, вкладки Activision/Firebird"}
  - {kind: other, url: "https://www.spectrumcomputing.co.uk/reviews/5850", note: "огляди: платформи-сегменти, вороги, від яких лише тікаєш, швидкий темп"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Zenji+Activision+gameplay", note: "пошук; геймплей Atari/C64"}
stage: v1
coverage: 60
mechanics: [move-4dir, keyboard-controls, time-out, time-bonus, event-points, player-death, touch-death, sequential-levels, difficulty-levels, hot-seat, game-screen, status-panel, +tile-rotate, +pipe-connectors, +connectivity-check, +lit-from-source, +path-bound-enemy, +extra-life-threshold, +rotate-under-avatar]
proposes: ["+role:source", "+role:conduit", "+trigger:input(rotate)", "+cond:connected", "+cond:ports_match", "+effect:rotate", "+effect:paint", "+ui:lit-tiles", "+ui:timer-countdown", "+axis:control", "+card:path-bound-enemy", "+card:rotate-under-avatar", "+card:extra-life-threshold"]
author: opus
date: 2026-11-02
---

# Zenji — голова-аватар бігає лабіринтом і крутить його сегменти, доки всі не зʼєднаються з Джерелом

## Суть
Лабіринт складено з квадратних сегментів-плиток, повернутих випадково. Гравець веде «безтілесну голову» по коридорах, стає в центр сегмента й повертає його; сегменти, зʼєднані з пульсуючим **Джерелом** у центрі, світяться (зелене світло / жовтий шлях). Коли все поле — одна мережа від Джерела («Zenji»), рівень пройдено. Заважають таймер і «Полумʼя бажання» (Flames of Desire), від яких можна лише тікати. Рідкісна суміш: обертання плиток (Net/Infinity Loop) + real-time аватар із ворогами.

## Поле і час
- Квадратна сітка сегментів (порядку 6×6…8×8 (?)), Джерело — в центрі; кожен сегмент — шматок коридору (кінець, пряма, кут, трійник, хрест).
- Голова ходить лише по коридорах — тобто по портах сегментів; «не пролазить у щілини», коли хочеться (огляд YOR).
- Real-time: таймер-відлік внизу екрана, темп швидкий і росте з рівнем; полумʼя зʼявляються по ходу і рухаються самі.
- 8 рівнів складності: непарні (1, 3, 5, 7) — один гравець, парні (2, 4, 6, 8) — двоє.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Голова Zenji | player | 1 + 4 «реінкарнації» | рух по коридорах 4 напрямки; у центрі сегмента повертає його |
| Сегмент лабіринту | conduit (custom) | форма (порти), кут | повертається на 90°; зʼєднаний із Джерелом — світиться |
| Джерело (Source) | source (custom) | центр поля | пульсує; від нього рахується звʼязність |
| Освітлений сегмент | — | стан сегмента | у компоненті Джерела; колір шляху змінюється |
| Полумʼя бажання (Flames of Desire) | enemy | зʼявляються з часом | рухаються лабіринтом (по коридорах (?)); дотик — втрата голови |
| Ілюзія | enemy | пізні рівні | обманне полумʼя/копія, теж смертельне (?) |
| Числова клітина | pickup | число N | дотик → 100×N очок |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `ports_match(current, next)` → ТО `move(head, dir)`; інакше `block`.
- КОЛИ `input(fire+left|right)` → ЯКЩО `custom: «голова в центрі сегмента»` → ТО `rotate(segment, ∓90)`; голова лишається в центрі й обертається разом (?).
- КОЛИ `after(rotate)` → ТО `custom: «перерахувати компоненту Джерела (flood fill по портах)»`, `paint(connected, lit)`.
- КОЛИ `all_constraints_met` (усі сегменти `connected(source)`) → ТО `score(+bonus × time_left)`, `next_level` — «Zenji».
- КОЛИ `contact(head, flame)` → ТО `lives(-1)`, `respawn(head)`; лабіринт може лишитись незʼєднаним.
- КОЛИ `timer(op, ==, 0)` → ТО `lives(-1)` (спробу втрачено).
- КОЛИ `contact(head, number_cell[n])` → ТО `score(100 × n)`.
- КОЛИ `counter(score, >=, 10000|30000|50000…)` → ТО `lives(+1)`.
- КОЛИ `timer(spawn)` → ТО `spawn_at(flame, ?)`; полумʼя `custom: «рух коридорами лабіринту»` (?).
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over`.
- Перемога рівня: уся мережа звʼязна з Джерелом до кінця таймера. Поразка: полумʼя або час, 5 голів на гру. Рахунок: за кожне повне зʼєднання (швидше — більше) + числові клітини.

## Керування і ввід
- Джойстик або клавіші: рух 4 напрямки (ZX: O/P — вліво/вправо, 2/W — вгору/вниз).
- Поворот: стати в центр сегмента, затиснути fire (ZX: Z) і хитнути вліво/вправо (O/P).
- Меню вибору контролера цифрою (Keyboard / Kempston / Sinclair / Cursor); C — гортати інструкцію, ENTER — старт; CAPS SHIFT+ENTER — скинути гру; SYMBOL SHIFT+ENTER — у меню контролерів.

## Вікна, меню, HUD
- `main-menu` / `options-controls`: вибір контролера цифрою.
- `help-window`: багатосторінкова інструкція на екрані (C — далі).
- `difficulty-select`: рівень 1–8 (непарні — 1 гравець, парні — 2).
- `game-screen`: лабіринт із Джерелом; `timer-countdown` внизу; `score`, `lives` (голови), `level-number` (?); освітлені сегменти як `lit-tiles`.
- Переходи: меню контролера → інструкція → гра → (Zenji) наступне поле → … → game over → меню.

## Фічі поза полем
- `difficulty-presets` (8 рівнів), `hotseat` (парні рівні — двоє гравців по черзі (?)).
- `restart-level`/скидання гри комбінацією клавіш.
- Нема збережень, рекордів між сесіями (?), редактора.
- Compute!'s Gazette згадує недокументований режим до 8 гравців (?).

## Варіації й родичі
- Net (Tatham), ∞ Infinity Loop — те саме обертання до звʼязної мережі, але без аватара й ворогів; Pipe Mania — потік з джерела; Deflektor — real-time + ворог, що псує поле.
- Осі варіацій: **хто крутить: курсор «рукою» / аватар, що мусить дійти** · **мета: дерево від джерела / усі замкнені / шлях A→B** · **тиск: таймер / вороги / нема** · **вороги: ходять коридорами (залежать від твоїх поворотів) / вільно**.

## Цікавинки для курсу
- Звʼязність мережі від джерела (flood fill по портах-бітмасках) з підсвіткою — 🥉.
- Аватар, що ходить **по портах** тих самих плиток, які крутить: поворот змінює і мету, і власну прохідність — 📎.
- Вороги, що рухаються лише по зʼєднаних коридорах: твій поворот відкриває/закриває їм дорогу — 🥉.
- Генерація: розвʼязне дерево → випадкові повороти (рандом лише на старті) — 📎.
- Життя за пороги очок (10k, 30k, 50k…) — 🌱.
- Числові клітини-бонуси (100×N) — 🌱.

## Мапа на каталог
- Є: `move-4dir`, `keyboard-controls` · `time-out`, `time-bonus` (швидше — більше) · `event-points` (числові клітини) · `player-death` (1+4), `touch-death` (полумʼя) · `sequential-levels`, `difficulty-levels` (8 рівнів) · `hot-seat` · `game-screen`, `status-panel`.
- **Нема** → пропозиції карток:
  - `+tile-rotate` «Обертання плитки на місці» · entities/state · 🌱 — з Infinity Loop.
  - `+pipe-connectors` «Плитка-зʼєднувач з портами» · entities/state · 🌱 — з Pipe Mania.
  - `+connectivity-check` «Звʼязність мережі» · game-logic/constraints · 🥉 · слот {goal: from_source}.
  - `+lit-from-source` «Підсвітка підключених до джерела» · interface/hud · 📎.
  - `+path-bound-enemy` «Ворог ходить лише зʼєднаними коридорами» · entities/move · 🥉.
  - `+rotate-under-avatar` «Аватар повертає плитку, на якій стоїть» · entities/interact · 📎.
  - `+extra-life-threshold` «Життя за пороги очок» · game-logic/score · 🌱 · слот {thresholds}.

## Пропозиції до словників
- `+role:source` / `+role:conduit` — Джерело і сегменти (третя гра сімʼї → ⏳).
- `+trigger:input(rotate)` — окрема дія «повернути» з утриманням fire (не рух).
- `+cond:connected(a, source)` · `+cond:ports_match(a, b)` — з Infinity Loop / Pipe Mania; тут ще й для руху аватара.
- `+effect:rotate` ⏳ · `+effect:paint` ⏳ — фарбування підключених.
- `+ui:lit-tiles` (з Infinity Loop) · `timer-countdown` ⏳.
- `+axis:control` — `direct` (рух) + дія на місці: аватар як «рука», що мусить дійти до плитки.

## Джерела
- ⭐ [Інструкція ZX Spectrum](https://spectrumcomputing.co.uk/pub/sinclair/games-info/z/Zenji.txt) — мета, поворот (fire + вліво/вправо), Flames of Desire та ілюзії, таймер, очки (100×N, бонус за швидкість), життя за 10k/30k/50k, 8 рівнів, клавіші.
- [Wikipedia](https://en.wikipedia.org/wiki/Zenji_(video_game)) — Matthew Hubbard, Activision 1984, Джерело в центрі, зелене світло на зʼєднаних, платформи, відгуки (CGW: «potential classic»).
- [Spectrum Computing: картка](https://spectrumcomputing.co.uk/entry/5850/ZX-Spectrum/Zenji) — керування, 2 гравці, PDF-інструкція.
- [Spectrum Computing: огляди](https://www.spectrumcomputing.co.uk/reviews/5850) — поворот з центру, вороги без зброї, швидкий темп.
- YouTube: пошук «Zenji Activision gameplay».

## Непевне
- Веб-пошук вичерпано; C64-Wiki (404), Lemon64 і MobyGames (403) недоступні; PDF-інструкція — скан без тексту.
- (?) Як саме рухається полумʼя — коридорами (залежно від поворотів) чи вільно; «Sparks» з запиту куратора в інструкції ZX не згадані — можливо, назва в Atari/C64-версіях.
- (?) Що таке «ілюзії» пізніх рівнів (фальшиві вороги чи фальшиві сегменти).
- (?) Розмір поля; чи голова обертається разом із сегментом; де стоять числові клітини.
- (?) Як грають двоє на парних рівнях (по черзі чи одночасно).
- (?) Колір «зʼєднаного» шляху: Wikipedia — зелене світло, інструкція ZX — жовтий шлях (різні платформи).
