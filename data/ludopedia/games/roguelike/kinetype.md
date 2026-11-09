---
title: Kinetype
slug: kinetype
aka: []
family: roguelike
also: [maze-arcade, word-number]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: both
  goal: state
year: 2026
platforms: [PC (Windows)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/4556110/Kinetype/", best: true, note: "Morlytic, ранній доступ з 05.06.2026; рух набором тексту, здібності, вороги, евакуація, Bytes, Hardcore-таймер, теми"}
  - {kind: other, url: "https://steamcommunity.com/app/4556110/discussions/0/836124330258633714/", note: "відгук на демо + відповіді розробника: left/right довші за up/down, PEW, команда zoomout"}
  - {kind: other, url: "https://steamcommunity.com/app/4556110/discussions/0/568163524345421261/", note: "відгук на демо: «змійка», смерть від входу у свій слід, рядки pickup_* на полі"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Kinetype+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, keyboard-controls, self-collision, path-cut, wrap-edges, chase-bfs, bomb-fuse, explode-area, projectile-shot, teleport, temporary-modes, undo-step, inventory-items, shop-between-levels, shop-catalog, shop-buyback, reach-exit, player-death, streak-stats, dungeon-generation, console-render, player-camera, field-scaling, theme-select, difficulty-levels, +typed-commands, +type-to-move, +command-length-cost, +typed-pickup, +retro-command-shortcut, +trail-wall, +trail-drain-enemy, +input-blinder, +tether-countdown, +extraction-run, +run-meta-carry, +meta-progression, +path-hint-ping, +slash-command-settings]
proposes: ["+effect:leave_trail", "+trigger:typed(text)", "+cond:typed_matches(text)", "+trigger:hold(key, s)", "+axis:control=typed", "+feature:slash-commands", "+feature:hardcore-input-timer", "+ui:typed-buffer", "+role:trail", "+card:type-to-move", "+card:command-length-cost"]
author: opus
date: 2026-11-09
---

# Kinetype — роглайт-«змійка» в терміналі: кожна набрана літера — крок, назва команди — її ціна в клітинах

## Суть
Мінімалістичний ASCII-роглайт: гравець не тисне стрілки, а **друкує**. Кожен набраний символ просуває аватар на клітину в поточному напрямку й лишається на полі слідом; поворот — слово `up`/`down`/`left`/`right` + Enter, здібність — її назва великими літерами + Enter. Тому довжина слова — це відстань: `left` коштує 4 кроки, `up` — 2, `SILENCE` — 7, і вирішувати треба, чи встигнеш «договорити» до зустрічі з ворогом. Мета забігу — зібрати предмети на процедурній мапі й дійти до точки евакуації; Bytes за успіх ідуть на постійні апгрейди.

## Поле і час
- Процедурне поле-термінал із символів; за гайдом спільноти — 2048×2048 клітин з порталами на протилежних краях (тор).
- Камера за гравцем, видно лише вʼюпорт; символи вищі, ніж ширші, тож вертикально видно менше (розробник). Масштаб — командами `/zoomin`, `/zoomout`, `/zoom0.9`.
- Звичайний режим — покроковий: світ рухається лише тоді, коли ти друкуєш. **Hardcore** — вороги ходять за таймером, якщо друкуєш повільно.
- Шари: поле (символи-перешкоди), слід гравця (набраний текст), рядки предметів `pickup_<name>`, точки `extract` і `unlock`, вороги.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Курсор-гравець | player | напрямок, інвентар здібностей | символ = крок уперед; вхід у свій слід = смерть |
| Слід (набраний текст) | static | довжина | лишається на полі; стіна для гравця; ціль VIRUS |
| Символ-перешкода | static | — | частина символів поля блокує рух |
| Рядок `pickup_<name>` | pickup | назва здібності | береться, якщо набрати його без помилок, проходячи по ньому |
| Точка `extract` | static | — | евакуація = успішний забіг |
| Точка `unlock` | switch | — | модифікатор «unlock»: перед евакуацією відвідати дві точки |
| CHASER | enemy | — | іде найкоротшим шляхом до гравця, убиває дотиком |
| VIRUS | enemy | — | іде до сліду й розповзається ним від точки контакту; зʼїдає зібрані Bytes |
| BLINDER | enemy | тривалість | тимчасово ховає набрані символи — друкуєш «наосліп» |
| FUSE | enemy | — | переслідує, як CHASER; вибухає біля гравця або сліду |
| «Гнида» (помаранчевий) | enemy | лічильник ходів | чіпляється до гравця й убиває за N ходів, якщо не набрати показану команду (назва з RU-гайду) |
| BOMB | object | запал | вибух нищить ворогів, оточення й гравця |
| MINE | object | — | вибухає, коли поруч ворог |
| Снаряд PEW | projectile | — | летить уперед; вибухає на перешкоді чи будь-якому сліді; убиває ворога |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(char)` → ЯКЩО `free(cell_ahead)` → ТО `move(player, facing)`, `custom: «символ лишається на клітині як слід»`.
- КОЛИ `input(char)` → ЯКЩО `occupied(cell_ahead, trail)` → ТО `lose` (врізався у власний слід).
- КОЛИ `input(char)` → ЯКЩО `occupied(cell_ahead, obstacle)` → ТО `block`.
- КОЛИ `input("up|down|left|right" + Enter)` → ТО `face(player, dir)`; кожна літера слова вже була кроком — довше слово = довший шлях до повороту.
- КОЛИ `input(Backspace)` → ТО `custom: «стерти останній символ сліду»`, `move(player, back)`.
- КОЛИ `edge(player)` → ТО `wrap(player)`.
- КОЛИ `enter(player, pickup_string)` → ЯКЩО `custom: «набрані символи збігаються з рядком»` → ТО `pickup(player, ability)`.
- КОЛИ `input("ZAP" + Enter)` → ЯКЩО `has(player, zap)` → ТО `disappear(nearest_enemy)`.
- КОЛИ `input("BOMB" + Enter)` → ЯКЩО `has(player, bomb)` → ТО `place(player, bomb)`; КОЛИ `timer(fuse)` → ТО `explode(area, n, floor)`.
- КОЛИ `input("MINE" + Enter)` → ТО `place(player, mine)`; КОЛИ `in_range(mine, enemy, n)` → ТО `explode(area, n, floor)`.
- КОЛИ `input("DASH" + Enter)` або `input(Tab)` (апгрейд TAB_DASH) → ТО `custom: «стрибок на 5 клітин уперед крізь перешкоди; у сліді розрив»`.
- КОЛИ `input("PING" + Enter)` → ТО `custom: «показати лінію до extract / unlock; лінія тане щотіку»`.
- КОЛИ `input("PATCH" + Enter)` → ЯКЩО `custom: «VIRUS прикріплений до сліду»` → ТО `disappear(virus)`, `custom: «останні 50 клітин сліду зцілено, ×2 Bytes за клітину»`.
- КОЛИ `input("PEW" + Enter)` → ТО `spawn(projectile, ahead)`; КОЛИ `contact(projectile, enemy)` → ТО `disappear(enemy)`; КОЛИ `blocked(projectile)` → ТО `explode(area, n, floor)`.
- КОЛИ `input("SWAP" + Enter)` → ТО `teleport(player, nearest_enemy)`, `disappear(enemy)`, `custom: «рух далі в напрямку ворога»`.
- КОЛИ `input("SILENCE" + Enter)` → ТО `stun(all_enemies, 20)`.
- КОЛИ `input("MOTION" + Enter)` → ТО `set_state(player, motion, 20)` — вільний рух `h/j/k/l` або стрілками без сліду, `i` — вийти.
- КОЛИ `input("SUDO" + Enter)` → ТО `set_state(all_enemies, flee, 100)` — тікають і ходять раз на 2 ходи; перетин їхніх слідів робить їх «латними».
- КОЛИ `input(ctrl+z)` → ТО `custom: «назад до початку поточної лінії (останнього повороту)»`.
- КОЛИ `input(ctrl+b)` → ЯКЩО `has(player, bomb)` → ТО `custom: «останні 4 символи сліду стають BOMB»` (апгрейд QUICKBOMB; так само `ctrl+s` → 7 символів = SILENCE).
- КОЛИ `turn_end(player)` → ТО `custom: «CHASER/FUSE роблять крок найкоротшим шляхом»`; ЯКЩО `prob(p)` (апгрейд ENEMY_SKIP) → ТО `custom: «вороги пропускають хід»`.
- КОЛИ `contact(chaser, player)` → ТО `lose`.
- КОЛИ `contact(virus, trail)` → ТО `custom: «вірус розповзається слідом»`, `currency(−n)`.
- КОЛИ `custom: «спрацював BLINDER»` → ТО `hide(cells)` (набраний текст) на час.
- КОЛИ `in_range(fuse, player, n)` → ТО `explode(area, n, floor)`.
- КОЛИ `adjacent(gnida, player)` → ТО `attach(gnida, player)`, `timer(start, n)`; КОЛИ `input(shown_command)` → ТО `disappear(gnida)`; КОЛИ `custom: «лічильник гниди вичерпано»` → ТО `lose`.
- КОЛИ `idle(n)` → ЯКЩО `mode(hardcore)` → ТО `custom: «вороги ходять без гравця»`.
- КОЛИ `reach(player, extract)` → ЯКЩО `custom: «модифікатор unlock: обидві точки відвідано»` → ТО `win`, `currency(+bytes)`, `counter(streak, +1)`.
- КОЛИ `counter(task, >=, n)` (напр. PING ×5) → ТО `custom: «бонус Bytes при успішній евакуації»`.
- КОЛИ `died(player)` → ТО `take(player, run_inventory)`, `custom: «серія обнуляється; банк Bytes і апгрейди лишаються»`.
- КОЛИ `input(hold R 3 s)` → ТО `custom: «здатися — забіг провалено»`.
- Перемога: дійти до `extract`. Поразка: дотик ворога, вибух, вхід у свій слід, «гнида». Рахунок: Bytes і серія успішних забігів.

## Керування і ввід
- Лише клавіатура: будь-які символи = кроки; слова-напрямки й назви здібностей + Enter; Backspace — назад по сліду.
- Скорочення з апгрейдів: `Tab` (DASH), `ctrl+b` (QUICKBOMB), `ctrl+s` (HUSH → SILENCE), `ctrl+z` (UNDO), `ctrl+[` (MOTION, розмітка гайду зіпсована); у MOTION — `h/j/k/l`/стрілки.
- Налаштування — теж набором у терміналі: `/fullscreen`, `/windowed`, `/zoomin`, `/zoomout`, `/zoom0.9`, сітка `.on/.off`, `/guide` (підказки поворотів), `/tutorial.on`, `/theme.<name>`, `font.set.<name>`, `/sound.on|off`, `sound.creamy|piano|thock` (звук клавіш).
- Затиснути R на 3 с — здатися.

## Вікна, меню, HUD
- `main-menu` — гравці кажуть, що заплутане; швидкий старт без пояснень.
- `game-screen` — термінальна сітка, слід-текст, рядки предметів, вороги-символи; лічильники ходів біля активних команд (SILENCE); лінія PING; `objective-text`-подібні необовʼязкові завдання рівня (?).
- `shop-window` — між забігами: здібності в інвентар, апгрейди, продаж назад (повернення 50 % і більше).
- `tutorial-window` — навчальний забіг за `/tutorial.on`; гравці просять кращий.
- `end-screen` — евакуація (Bytes, серія) або провал.
- Немає окремого `settings-window`: налаштування — команди в самому полі (`+feature:slash-commands`); інвентар зібраного на полі не показано (гравці просять панель).
- Переходи: `main-menu` → `game-screen` → евакуація/смерть → `end-screen` → `shop-window` → новий забіг.

## Фічі поза полем
- `meta-progression`: Bytes → постійні апгрейди (BYTE_BONUS +10 %, SELL_REFUND +5 % до 95 %, ENEMY_SKIP 0,5 → 10 %, PING_FADE, PATCH_BYTES, SILENCE_TURNS, MOTION_TURNS/SHIFT/SAVER, QUICKBOMB, TAB_DASH, HUSH) і предмети в крамниці.
- `streaks`: серія успішних евакуацій; смерть обнуляє серію й інвентар забігу.
- `difficulty-presets`: звичайний (без таймера) і Hardcore (таймер вводу).
- `theme-select` (монохром, зелена «Matrix», свої — `.txt`-файли кольорів), `mod-support` (теми), шрифти, звук клавіш.
- `achievements`, `cloud-save` (Steam); доступність Steam: розмір тексту, кольори, «грається без таймінгу».

## Варіації й родичі
- [snake](../maze-arcade/snake.md) і [tron-light-cycles](../maze-arcade/tron-light-cycles.md) — слід-стіна й смерть від власного хвоста; тут слід не рухається, а Backspace його стирає.
- [dungeons-of-daggorath](dungeons-of-daggorath.md), [island-of-kesmai](island-of-kesmai.md) — роглайки з текстовими командами, але там текст — лише ввід, а не рух.
- Typing-ігри (Typing of the Dead, Epistory) — набір слів як атака; тут набір — сама ходьба.
- Осі варіацій: **що рухає аватар** (клавіша-напрямок / будь-який символ / слово-команда) · **ціна команди** (миттєва / довжина слова в кроках) · **слід** (нема / стіна / ціль для ворогів) · **помилка друку** (ігнор / зупинка / Backspace назад).

## Цікавинки для курсу
- Рух від будь-якого символу + слід із набраного тексту на сітці — 🌱 (ввід = `move(facing)` + запис символу в клітину).
- Ціна команди = її довжина в кроках: `left` дорожче за `up` — 🌱, але красивий урок балансу.
- Збір предмета, лише якщо набраний текст збігся з рядком на полі — 📎 (посимвольне порівняння під час руху).
- Ретро-команда: `ctrl+b` перетворює останні 4 символи сліду на BOMB — 📎 (переписати хвіст буфера).
- VIRUS, що повзе вашим слідом від точки контакту, і PATCH, що «лікує» останні N клітин — 🥉 (граф сліду як лінійний список).
- Hardcore: світ покроковий, доки друкуєш, і реальний час, коли зволікаєш — 📎 (`idle` → тік ворогів).
- Поле 2048×2048 з тором і камерою, PING-стрілка до виходу — 🥉 (BFS на великому полі, вʼюпорт).

## Мапа на каталог
- Є: `move-4dir` · `keyboard-controls` · `self-collision` · `path-cut` (Backspace стирає хвіст) · `wrap-edges` (портали країв) · `chase-bfs` (CHASER) · `bomb-fuse` · `explode-area` · `projectile-shot` (PEW) · `teleport` (SWAP) · `temporary-modes` (SILENCE, MOTION, SUDO) · `undo-step` (ctrl+z) · `inventory-items` · `shop-between-levels` + `shop-catalog` + `shop-buyback` · `reach-exit` · `player-death` · `streak-stats` · `dungeon-generation` · `console-render` · `player-camera` · `field-scaling` (zoom) · `theme-select` · `difficulty-levels`.
- **Нема** → пропозиції карток:
  - `+type-to-move` «Кожен набраний символ — крок у поточному напрямку» · entities/move · 🌱.
  - `+command-length-cost` «Команда коштує стільки кроків, скільки в ній літер» · entities/move · 🌱.
  - `+typed-pickup` «Предмет береться, якщо набрати його назву поверх нього» · entities/interact · 📎.
  - `+retro-command-shortcut` «Хоткей перетворює останні N символів сліду на команду» · entities/interact · 📎.
  - `+trail-drain-enemy` «Ворог повзе слідом гравця й краде ресурс» · entities/move · 🥉.
  - `+input-blinder` «Ворог ховає ввід — друкуєш наосліп» · interface/hud · 🌱.
  - `+tether-countdown` «Ворог чіпляється й убиває за N ходів, якщо не набрати команду» · entities/combat · 📎.
  - `+extraction-run` «Забіг успішний лише після евакуації; провал — втрата зібраного» · game-logic/win · 🌱.
  - `+path-hint-ping` «Тимчасова лінія-підказка до виходу» · interface/hud · 📎.
  - `+slash-command-settings` «Налаштування як команди в полі вводу» · interface/settings · 🌱.
  - `+typed-commands`, `+trail-wall`, `+run-meta-carry`, `+meta-progression` — уже пропоновані корпусом.

## Пропозиції до словників
- `+effect:leave_trail` — клітина, з якої пішов аватар, стає слідом (тут — набраним символом).
- `+trigger:typed(text)` — гравець набрав слово/команду + Enter (ширше за `input(action)`: аргумент — текст).
- `+cond:typed_matches(text)` — набрані символи збігаються з рядком на полі.
- `+trigger:hold(key, s)` — клавішу тримали N секунд (здатися).
- `+axis:control=typed` — значення осі керування: рух і дії текстом.
- `+feature:slash-commands` — налаштування й службові дії командами в полі вводу.
- `+feature:hardcore-input-timer` — хардкор-режим: зволікання з вводом дає хід ворогам.
- `+ui:typed-buffer` — показ набраного рядка (і його приховування BLINDER-ом).
- `+role:trail` — слід як сутність поля (стіна для гравця, ціль для ворогів).
- `+card:type-to-move`, `+card:command-length-cost` — див. картки.

## Джерела
- ⭐ [Steam: Kinetype](https://store.steampowered.com/app/4556110/Kinetype/) — опис: набір команд + Enter, ZAP/BOMB/MINE/SILENCE/PING/DASH, CHASER/VIRUS/BLINDER/FUSE, евакуація, Bytes, Hardcore, теми, ранній доступ.
- [Steam-гайд «Kinetype BASIC INFO (RUS)»](https://steamcommunity.com/sharedfiles/filedetails/?id=3740894319) — команди налаштувань, PATCH/PEW/SWAP/UNDO/MOTION/SUDO, «гнида», апгрейди з числами, поле 2048×2048, Backspace; Steam позначив гайд прихованим — у вебі може не відкритись.
- [Steam: Demo feedback (xyx0826)](https://steamcommunity.com/app/4556110/discussions/0/836124330258633714/) — left/right довші за up/down; розробник: PEW, `zoomout`, вертикальний огляд.
- [Steam: Demo feedback (DazaKiwi)](https://steamcommunity.com/app/4556110/discussions/0/568163524345421261/) — «змійка», смерть від входу у свій слід, рядок `picrup_bomb`.
- [Steam: Surprisingly unergonomic](https://steamcommunity.com/app/4556110/discussions/0/562533105473177155/) — рух «будь-якими символами», суворе покарання помилок друку.
- [Steam: відгуки](https://steamcommunity.com/app/4556110/reviews/?browsefilter=toprated&l=english) — недокументовані команди, слабкий туторіал, Hardcore-серія 10.

## Непевне
- (?) Числа (2048×2048, DASH 5 клітин, PATCH 50 клітин, SUDO 100 ходів, MOTION 20, PING тане 8 клітин/тік, апгрейди у %) — з неофіційного гайду, прихованого Steam; офіційно підтверджено лише SILENCE = 20 кроків.
- (?) Що саме буває за помилку друку (гравець пише «карає надто суворо»); чи підбір `pickup_*` при помилці просто не зараховується.
- (?) Чи Enter теж коштує крок; чи поворот на 180° (вхід у свій слід) завжди смерть.
- (?) Як спрацьовує BLINDER (дотик, радіус чи час) і як FUSE вибухає «біля сліду».
- (?) Офіційна назва помаранчевого ворога («ГНИДА» — з RU-гайду).
- (?) Чи гине банк Bytes при провалі: Steam — «Bytes втрачаються, якщо забіг провалено», гайд — «накопичені Bytes і апгрейди лишаються»; ймовірно, втрачаються лише Bytes поточного забігу.
- (?) Ранній доступ: склад здібностей і ворогів змінюватиметься 6–12 місяців.
