---
title: XOR
slug: xor
family: dig-gravity
also: [push-slide, thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: partial
  random: none
  goal: collect
year: 1987
platforms: [ZX Spectrum, C64, Amstrad CPC, BBC Micro, Acorn Electron, Amiga, Atari ST]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/XOR_(video_game)", best: true, note: "усі елементи з правилами: риби, кури, H/V-бомби, ляльки, силові поля, маски-перемикачі"}
  - {kind: wiki, url: "https://spectrumcomputing.co.uk/zxsr.php?id=5800", note: "рецензії 1987: ~2000 ходів, action replay, 15 лабіринтів, анаграма"}
  - {kind: wiki, url: "https://spectrumcomputing.co.uk/entry/5800/ZX-Spectrum/XOR", note: "запис ZXDB: видання, файли"}
  - {kind: fandom, url: "https://homeoftheunderdogs.net/game.php?id=4887", note: "огляд: без часу, жертва щита, анаграма"}
  - {kind: wiki, url: "https://worldofspectrum.org/archive/software/games/xor-logotron-ltd", note: "архів World of Spectrum"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=XOR+1987+logotron+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-4dir, gravity-fall, push-object, inertia-slide, collect-all, reach-exit, environment-death, player-death, impassable-cells, teleport-pair, blast-wave, minimap-radar, player-camera, goal-counter, replay, sequential-levels, in-game-editor, +directional-gravity, +directional-gate, +party-switch, +move-limit, +lights-off, +momentum-kill]
proposes: ["+axis:actors", "+axis:control", "+trigger:input", "+cond:moving", "+cond:facing", "+effect:fall", "+effect:slide", "+effect:explode", "+effect:reveal", "+effect:hide", "+effect:set_state", "+role:gate", "+role:switch", "+ui:move-counter", "+window:map-window", "+feature:replay"]
author: opus
date: 2026-11-02
---

# XOR — два щити, детермінована «гравітація» у двох напрямках і жодної випадковості

## Суть
Гравець по черзі керує двома щитами — Magus і Questor — у лабіринті, збирає всі маски й виводить щит до виходу. Обʼєкти мають **власні напрямки «падіння»**: риби й H-бомби падають униз, кури й V-бомби — тікають ліворуч; ляльки ковзають, куди штовхнули. Немає часу й випадковості — лише ліміт ходів, тож XOR — чиста покрокова логіка: як розчистити шлях, не опинившись під рибою, і коли пожертвувати другим щитом.

## Поле і час
- 15 лабіринтів; на екрані видно лише вікно навколо активного щита, решту відкривають шматки мапи на бічному моніторі.
- Один шар клітин; стіни — тло. Маска-перемикач може «вимкнути світло» — стіни стають невидимими.
- Покроково: хід щита → обʼєкти, що втратили опору, рухаються до упору у своєму напрямку. Таймера нема; ліміт ~2000 ходів на лабіринт.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Щит Magus / Questor | player | 2 шт., перемикання | 4 напрямки; штовхає; збирає маски; один можна втратити |
| Маска | pickup | лічильник | збір усіх → вихід можна пройти |
| Маска-перемикач (насуплена) | switch | on/off | одна вимикає світло (стіни невидимі), інша вмикає |
| Вихід | gate | всі маски | щит входить після збору → лабіринт пройдено |
| Стіна | static | — | непрохідна |
| Силове поле горизонтальне / вертикальне | gate | вісь проходу | увійти можна лише по своїй осі; щит, що входить, руйнує його |
| Риба | object | напрям «падіння» вниз | рухається вниз до упору; штовхається ліворуч/праворуч |
| Курка | object | напрям «падіння» ліворуч | рухається ліворуч до упору; штовхається вгору/вниз |
| H-бомба | object | падає як риба | штовхається вбік; вибух руйнує клітини ліворуч і праворуч |
| V-бомба | object | рух ліворуч як курка | штовхається вгору/вниз; вибух руйнує клітини вгорі й унизу |
| Лялька | object | — | сама не рухається; штовхнута — ковзає до перешкоди; бомб не підриває, крізь поля не проходить |
| Шматок мапи | pickup | — | відкриває частину плану лабіринту й маски на ній |
| Телепорт (BMUS) | terrain | пара | переносить щит до іншого порталу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(target)` або `cell(target, mask|map)` → ТО `move(shield, dir)`, `counter(moves, +1)`; маска → `pickup`, `counter(masks_left, -1)`.
- КОЛИ `input(switch)` → ТО `custom: «керування переходить до іншого щита»`, камера — на нього.
- КОЛИ `contact(shield, fish|h_bomb)` горизонтально → ЯКЩО `free(cell_behind)` → ТО `push`; КОЛИ `contact(shield, chicken|v_bomb)` вертикально → аналогічно; інакше `block`.
- КОЛИ `contact(shield, doll)` → ЯКЩО `free(cell_behind)` → ТО `slide(doll, dir)` до перешкоди.
- КОЛИ `after(move)` → ЯКЩО `free(below)` → ТО `fall(fish|h_bomb)` до упору; ЯКЩО `free(left)` → ТО `custom: «chicken|v_bomb рухається ліворуч до упору»`.
- КОЛИ `contact(moving fish|chicken, shield)` → ЯКЩО `custom: «пролетіла ≥1 клітину»` → ТО `disappear_b` (щит гине); інакше просто лягає на щит.
- КОЛИ `contact(moving fish|chicken|bomb, h_bomb|v_bomb)` → ЯКЩО `custom: «пролетіла ≥1 клітину»` → ТО `explode`: знищено того, хто вдарив, і клітини ліворуч+праворуч (H) або вгорі+внизу (V).
- КОЛИ `contact(shield, force_field)` → ЯКЩО `moving(shield, field_axis)` → ТО `disappear_b`, `move`; інакше `block`. Риби/кури проходять поле у своєму напрямку; ляльки — ні.
- КОЛИ `contact(shield, map_piece)` → ТО `pickup`, `reveal(map_region)`.
- КОЛИ `contact(shield, switch_mask)` → ТО `set_state(lights, off|on)`: `hide(walls)` / `reveal(walls)`.
- КОЛИ `contact(shield, teleport)` → ТО `teleport(shield, pair)`.
- КОЛИ `contact(shield, exit)` → ЯКЩО `all_gone(mask)` → ТО `win`, `give(letter)`, `next_level`; інакше `block`.
- КОЛИ `counter(moves, >=, limit)` → ТО `lose` (лабіринт спочатку).
- Перемога: усі маски + вихід (часом лише одним щитом — другий замурований або знищений). Поразка: обидва щити загинули або вичерпано ходи. Рахунок нема; мета-нагорода — 15 літер анаграми.

## Керування і ввід
- 4 напрямки для активного щита; окрема клавіша перемикає щит (Magus ↔ Questor).
- Клавіша мапи — показати зібрані шматки; рестарт лабіринту; action replay після невдачі.

## Вікна, меню, HUD
- `main-menu`: вибір лабіринту (з відкритих), replay, мапа.
- `game-screen`: вікно лабіринту + бічна панель: `minimap` зі шматків мапи й масок, `remaining-counter` масок (зібрано / лишилось), `move-counter`, активний щит.
- `map-window`: план лабіринту з відкритими шматками.
- `replay-window`: перегляд останньої спроби.
- `end-screen`: літера анаграми за лабіринт; після 15 — розвʼязати анаграму («Order of XOR»).

## Фічі поза полем
- `levels-sequential`: 15 лабіринтів + мета-пазл анаграми.
- `replay`: action replay невдалої спроби.
- `level-editor`: окремий продукт XOR Designer; освітня версія XOR for Schools (+6 лабіринтів і паперовий бланк планування).
- Нема `undo` (у класиці), нема часу, нема випадковості — `mode-zen` за природою, але з лімітом ходів.

## Варіації й родичі
- Клони на Windows/Mac/Linux/RISC OS/GBA; ідеї — у thinky-лінії (Stephen's Sausage Roll-подібна детермінованість).
- Родичі: Boulder Dash (падіння), Sokoban (штовхання з обмеженням осі), Lost Vikings / Trine (перемикання героїв).
- **Осі варіацій**: напрям гравітації — «один для всіх (BD) / свій для кожного типу (XOR)»; вісь штовхання — «будь-яка / лише перпендикулярно до власного руху»; смерть від падіння — «будь-яке падіння / лише з розгону ≥1»; актори — «один / два з перемиканням».

## Цікавинки для курсу
- Гравітація за типом: кожен обʼєкт має свій напрямок падіння й свою вісь штовхання — 🥉.
- «Вбиває лише з розгону» — стан руху як умова контакту — 📎.
- Два щити з перемиканням, спільне поле, жертва одного — 🥉 (камера, черга, «живі» актори).
- Силові поля з віссю проходу, що руйнуються при проході — 🌱.
- H/V-бомби: вибух по осі, що залежить від типу — 📎 поверх `blast-wave`.
- Невидимі стіни + мапа зі шматків — 📎 (інформаційний шар окремо від поля).

## Мапа на каталог
- Є: `move-4dir` · `gravity-fall` (риби) · `push-object` · `inertia-slide` ↔ ляльки · `collect-all` ↔ маски · `reach-exit` · `environment-death` ↔ риба/курка згори · `player-death` (два «життя»-щити) · `impassable-cells` · `teleport-pair` · `blast-wave` ↔ H/V-бомби (по одній осі) · `minimap-radar` ↔ шматки мапи · `player-camera` · `goal-counter` · `replay` · `sequential-levels` · `in-game-editor` ↔ XOR Designer.
- **Нема** → пропозиції карток:
  - `+directional-gravity` «Гравітація за типом обʼєкта» · entities/move · 🥉 · слот {dir per type}.
  - `+directional-gate` «Прохід лише по осі» · entities/legality · 🌱 · слот {axis; one_use}.
  - `+party-switch` «Кілька аватарів з перемиканням» · entities/move · 🥉 · слот {count}.
  - `+move-limit` «Ліміт ходів» · game-logic/lose · 🌱 · слот {limit}.
  - `+lights-off` «Невидимі стіни за перемикачем» · interface/render · 📎.
  - `+momentum-kill` «Смерть лише від обʼєкта в русі» · entities/death · 📎 · слот {min_distance}.

## Пропозиції до словників
- `+axis:actors` — `party`: два підконтрольні щити по черзі; `+axis:control` — `direct`.
- `+trigger:input` ⏳ (перемкнути щит), `+cond:moving` ⏳ (вбиває лише рухомий), `+cond:facing` ⏳ (вісь входу в поле).
- `+effect:fall` ⏳, `+effect:slide` ⏳ (ляльки), `+effect:explode(axis)`, `+effect:reveal`/`+effect:hide` ⏳ (мапа, світло), `+effect:set_state` ⏳.
- `+role:gate` ⏳ (силові поля, вихід), `+role:switch` ⏳ (маска-перемикач).
- `+ui:move-counter` ⏳ (лічильник проти ліміту), `+window:map-window` ⏳, `+feature:replay` ⏳.

## Джерела
- ⭐ [Wikipedia: XOR](https://en.wikipedia.org/wiki/XOR_(video_game)) — повний перелік обʼєктів і їх взаємодій, XOR Designer, XOR for Schools.
- [Spectrum Computing: рецензії](https://spectrumcomputing.co.uk/zxsr.php?id=5800) — Sinclair User/Crash/ACE: ~2000 ходів, action replay, 15 лабіринтів, 15 літер анаграми.
- [Home of the Underdogs](https://homeoftheunderdogs.net/game.php?id=4887) — без часу, жертва щита, мета-пазл.
- [Spectrum Computing: запис](https://spectrumcomputing.co.uk/entry/5800/ZX-Spectrum/XOR) · [World of Spectrum](https://worldofspectrum.org/archive/software/games/xor-logotron-ltd) — архів видання.

## Непевне
- (?) Ліміт «близько 2000 ходів» — лише Sinclair User; Crash каже «обмежено» без числа.
- (?) Crash пише, що «ляльки й риби падають, коли прибрано опору» — суперечить Wikipedia (ляльки самі не рухаються); лишаю Wikipedia.
- (?) Розмір лабіринту (32×32?) і вікна огляду — не перевірено.
- (?) Клавіші й склад меню (вибір лабіринту, replay) — з рецензій узагальнено, оригінальної інструкції не бачив.
- (?) Чи є в оригіналі undo — у рецензіях не згадано; вважаю, що нема.
