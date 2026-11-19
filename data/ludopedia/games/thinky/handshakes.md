---
title: Handshakes
slug: handshakes
aka: [Рукостискання]
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2022
platforms: [web, Windows, macOS, Linux, Android]
links:
  - {kind: itch, url: "https://petpumpkin.itch.io/handshakes", best: true, note: "грати в браузері; керування (ліва рука WASD, права — стрілки, E — undo, R — рестарт); коментарі про довжину руки, кнопки, пропуск рівнів і відрізану руку"}
  - {kind: steam, url: "https://store.steampowered.com/app/2171690/", note: "безкоштовно; 30 пазлів, кооп на одній клавіатурі чи контролері, 9 досягнень, таблиці рекордів"}
  - {kind: steam, url: "https://store.steampowered.com/app/2245130/", note: "сиквел Handshakes: Hands On — поршні, липкі поршні, портали, мікроби, редактор, 100+ пазлів (реліз заплановано на Q4 2026)"}
  - {kind: play, url: "https://html-classic.itch.zone/html/6448722/index.html", note: "веб-збірка Unity; з її файла даних — назви класів і плиток коду (armCut, pushableHand, DoorHoldOpen, DoorToggle, lengthRemaining)"}
  - {kind: other, url: "https://www.gamingonlinux.com/2023/02/handshakes-free-sokoban-puzzler-about-two-hands-meeting/page=1/", note: "огляд: 30 рівнів, руки мають зустрітися, ящики, двері, відрізання руки"}
  - {kind: other, url: "https://2023.amaze-berlin.de/submissions/handshakes", note: "A MAZE. Berlin 2023: кооп на спільній клавіатурі або двох контролерах"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Handshakes+Pet+Pumpkin+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, impassable-cells, button-toggle, undo-unlimited, restart-level, skip-level, level-select, sequential-levels, save-progress, controls-remap, volume-control, sound-effects, background-music, movement-animation, particles, main-menu, pause-menu, game-screen, end-screen, settings-window, +stretch-limb-path, +length-budget, +cut-body, +severed-hand-box, +door-hold-open, +meet-goal, +dual-keyset-control, +shared-keyboard-coop, +speedrun-timer]
proposes: ["+effect:extend_path", "+effect:retract", "+effect:cut_body", "+effect:toggle", "+ui:length-left", "+axis:actors", "+axis:control", "+card:length-budget", "+card:severed-hand-box", "+card:meet-goal"]
author: opus
date: 2026-11-19
---

# Handshakes — дві руки тягнуться одна до одної крізь кімнату: обмежена довжина, ящики, кнопки й двері, що можуть відрізати руку

## Суть
Покроковий Sokoban з видом згори, де аватари — дві долоні на руках, що виростають кожна зі своєї бази (лівої й правої). Кожна долоня ходить своїм набором клавіш і тягне за собою руку-слід від бази; довжина руки обмежена, а крок назад скорочує руку й повертає довжину. Долоні штовхають ящики, тиснуть кнопки, що відчиняють двері, а двері, які зачиняються на руці, відрізають її — відрізана долоня лишається на полі й служить ящиком. Мета кожного з 30 пазлів — щоб долоні зустрілись у рукостисканні.

## Поле і час
- Квадратна сітка, вигляд згори, рівень — один екран. Дві бази рук — ліва й права (плитки `handBase` / `handBaseR`); де саме вони стоять у рівні — (?).
- У коді три шари плиток: руки (долоні, прямі й зігнуті сегменти, бази), елементи (стіни, зачинені двері, ящики, відрізані долоні) і кнопки (утримання / перемикач, натиснуті й ні).
- Шлях кожної руки зберігається як список «клітина + напрям»; сегменти малюються прямими або згинами.
- Покроково: одне натискання = крок однієї долоні; утримання клавіші повторює кроки. Часу на рівень нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ліва долоня | player | база ліворуч; лишок довжини | WASD; крок на 1, за собою лишає сегмент руки |
| Права долоня | player | база праворуч; лишок довжини | стрілки; так само |
| База руки | static | — | звідси росте рука |
| Сегмент руки | segment | прямий / згин | лежить на шляху долоні; зникає, коли долоня відступає |
| Ящик | object | — | штовхається на 1; тисне кнопку |
| Відрізана долоня | object | — | лишається після відрізання; штовхається й тисне кнопку, як ящик |
| Стіна | static | — | непрохідна |
| Двері | gate | зачинені / відчинені | відчиняються кнопкою; зачиняючись на руці, відрізають її (?) |
| Кнопка утримання | switch | DoorHoldOpen | двері відчинені, поки на кнопці долоня чи ящик |
| Кнопка-перемикач | switch | DoorToggle | кожне натискання перемикає двері; лишається втиснутою |
| Рукостискання | — | — | плитка зустрічі долонь — кінець рівня |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(wasd_dir)` → ЯКЩО `free(next_cell)` і `counter(left_length, >, 0)` → ТО `move(left_hand, dir)`, `custom: «у залишеній клітині лягає сегмент руки»`, `counter(left_length, -1)`.
- КОЛИ `input(arrow_dir)` → ЯКЩО `free(next_cell)` і `counter(right_length, >, 0)` → ТО `move(right_hand, dir)`, `custom: «у залишеній клітині лягає сегмент руки»`, `counter(right_length, -1)`.
- КОЛИ `input(dir)` → ЯКЩО `custom: «клітина в напрямку — попередня клітина цієї руки»` → ТО `move(hand, dir)`, `shrink(arm, 1)`, `counter(length, +1)` — відступ скорочує руку й повертає довжину.
- КОЛИ `input(dir)` → ЯКЩО `counter(length, ==, 0)` і це не відступ → ТО `block`; число біля долоні фарбується кольором «довжини нема».
- КОЛИ `input(dir)` → ЯКЩО `occupied(next_cell, wall|closed_door|arm)` → ТО `block`.
- КОЛИ `contact(hand, box)` → ЯКЩО `free(cell_behind)` → ТО `push`, `move(hand, dir)`; інакше `block`.
- КОЛИ `contact(hand, cut_hand)` → ЯКЩО `free(cell_behind)` → ТО `push` — відрізана долоня їде, як ящик.
- КОЛИ `contact(hand, other_hand)` → ЯКЩО `custom: «чужа долоня може зсунутися»` → ТО `push` (?).
- КОЛИ `enter(hand|box|cut_hand, hold_button)` → ТО `set_state(door, open)`.
- КОЛИ `leave(hand|box|cut_hand, hold_button)` → ТО `clear_state(door, open)`.
- КОЛИ `enter(hand|box|cut_hand, toggle_button)` → ТО `custom: «двері перемикаються: відчинені ↔ зачинені»`; ту саму кнопку можна натиснути знову.
- КОЛИ `state_off(door, open)` → ЯКЩО `occupied(door_cell, arm)` → ТО `detach(hand, arm)`, `transform(hand, cut_hand)`, `custom: «сегменти руки зникають; керування повертається»` (?).
- КОЛИ `state_off(door, open)` → ЯКЩО `occupied(door_cell, box)` → ТО `disappear` (?) — «руйнувати ящики».
- КОЛИ `contact(left_hand, right_hand)` → ЯКЩО `custom: «долоні йдуть назустріч одна одній»` (?) → ТО `win`, `custom: «рукостискання й оплески»`, `next_level`.
- Перемога: дві долоні потиснули одна одну. · Поразка: нема; глухий кут — undo або рестарт. · Рахунку нема; у speedrun-режимі йде таймер усієї гри.

## Керування і ввід
- Клавіатура: ліва рука — W / A / S / D, права — стрілки; E — undo, R — рестарт рівня, Esc / Tab — меню.
- Контролер: ліва рука — лівий стік / D-pad, права — правий стік; B — undo, Y — рестарт, Start — меню.
- Утримання напрямку — повторні кроки; у коді є дії «наступний / попередній рівень», «огляд рівнів», «сховати керування», «вимкнути звук», «повний екран».
- Кооп: двоє гравців на одній клавіатурі (кожен бере свою руку) або на двох контролерах.

## Вікна, меню, HUD
- `main-menu` — титул Handshakes, автори; у веб-версії — «зроблено для Lost Relic Games Jam» і «повна гра скоро».
- `level-select` — огляд рівнів: превʼю-мініатюри з галочками пройдених.
- `game-screen`: поле; HUD — `level-number` і назва рівня, число лишку довжини біля кожної долоні (`+ui:length-left`), панель підказок керування (ховається), таймер speedrun-режиму.
- `pause-menu` (Paused): продовжити, гучність Master / Music / SFX, повний екран, перемикач speedrun-режиму, «Delete Save Data» (у v1.1.3 перейменовано з «Restart Game», щоб не стирали прогрес випадково), вихід.
- `options-controls` — Key Bindings: перепризначення клавіш.
- `end-screen` — екран успіху рівня «натисни, щоб продовжити»; фінал гри — оплески, джингл, феєрверк частинок.
- Переходи: main-menu → game-screen (або level-select) → (рукостискання) end-screen → наступний рівень; Esc → pause-menu.

## Фічі поза полем
- `undo` (стек знімків стану всіх шарів і шляхів рук), `restart-level`, `skip-level` — рівень можна пропустити.
- `level-select` з галочками, `autosave` прогресу.
- `mode-speedrun` — таймер усієї гри; Steam-таблиці рекордів; спідран Handshakes показали на AGDQ 2023.
- `mode-coop` / `local-multiplayer` — дві руки на двох гравців; `gamepad-support`, `remap-controls`, `volume-sliders`, `fullscreen`.
- `achievements` у Steam (9): «Spare an Arm», «Use the Box», «One For Each Finger», «Master of Handshakes», «Super Speed Handshaking», «Speedrunner in the Making!», «It's a Feature, Not a Bug!», «Wasn't That Level 9?», «🤝».
- Порт на Android (APK на itch); гра безкоштовна, саундтрек — платний набір підтримки.

## Варіації й родичі
- Сиквел Handshakes: Hands On — поршні, липкі поршні, портали, мікроби, редактор пазлів і Steam Workshop, 100+ пазлів.
- [GRAB-O](grab-o.md) — гумові кінцівки, що тягнуться клітинками; [Soliquid](soliquid.md) — тіло тягнеться до трьох клітин; [Growmi](growmi.md) — тіло росте від опори й стискається; [Would You Love Me If I Was a Snake?](would-you-love-me-if-i-was-a-snake.md) — відкушений хвіст стає блоком; [Tron Light Cycles](../maze-arcade/tron-light-cycles.md) — слід за рухом.
- **Осі варіацій:** довжина — без ліміту / бюджет на руку (тут) · відступ — крок назад скорочує (тут) / окрема кнопка / неможливо · відрізання — двері (тут) / укус / ніколи · що лишається після відрізання — обʼєкт-ящик (тут) / нічого · аватарів — одна рука / дві на двох наборах клавіш (тут) / дві на двох гравців.

## Цікавинки для курсу
- Рука як шлях від бази з бюджетом довжини: крок уперед — сегмент, крок назад — повернення (стек позицій) — 🥉.
- Дві долоні на двох наборах клавіш у спільному світі, одна — перешкода чи штовхач для іншої — 📎.
- Двері, що зачиняються на руці, відрізають її, а долоня стає ящиком — 🥈 (порядок подій: відпущено кнопку → двері → перевірка клітини → відрізання → перетворення).
- Кнопки двох типів (утримання / перемикач) з парними дверима — 📎.
- Undo через знімки трьох шарів плиток і шляхів обох рук — 🥉.
- Speedrun-таймер на всю гру з паузою в меню — 🌱.

## Мапа на каталог
- Є: `move-4dir` + `move-by-input` + `keyboard-controls` ↔ дві долоні; `push-object` ↔ ящики й відрізані долоні; `impassable-cells` ↔ стіни, зачинені двері; `button-toggle` ↔ кнопки й двері; `undo-unlimited`, `restart-level`, `skip-level`; `level-select` + `sequential-levels` + `save-progress` ↔ огляд рівнів з галочками; `controls-remap`, `volume-control`, `sound-effects`, `background-music`; `movement-animation`, `particles` ↔ анімація рук і фінальний феєрверк; `main-menu`, `pause-menu`, `game-screen`, `end-screen`, `settings-window`.
- **Нема** → пропозиції карток:
  - `+stretch-limb-path` (вже пропонована GRAB-O) — кінцівка тягнеться клітинками від бази.
  - `+length-budget` «Бюджет довжини; крок назад повертає» · entities/legality · 🥉 · слот {length: N per arm}.
  - `+cut-body` (вже пропонована Would You Love Me If I Was a Snake?) — тут ріжуть двері.
  - `+severed-hand-box` «Відрізана частина стає обʼєктом-ящиком» · entities/interact · 📎.
  - `+door-hold-open` «Кнопка утримання: двері відчинені, поки на ній щось є» · entities/interact · 🌱 (дитина `button-toggle`).
  - `+meet-goal` «Перемога — два аватари зустрілись» · game-logic/win · 🌱.
  - `+dual-keyset-control` «Два аватари на двох наборах клавіш одночасно» · interface/input · 📎.
  - `+shared-keyboard-coop` «Кооп на одній клавіатурі: кожен бере свій аватар» · game-logic/opponent · 🌱.
  - `+speedrun-timer` «Таймер усієї гри для спідрану» · interface/hud · 🌱.

## Пропозиції до словників
- `+effect:extend_path` — кінцівка подовжується на клітину слідом за долонею.
- `+effect:retract` — кінцівка скорочується на клітину, довжина повертається.
- `+effect:cut_body` — відрізати частину тіла чи кінцівки; відрізане лишається окремим обʼєктом.
- `+effect:toggle` — перемкнути стан цілі на протилежний (кнопка-перемикач і двері).
- `+ui:length-left` — число лишку довжини поруч з аватаром, з кольором «нуль».
- `+axis:actors` — `party`: дві долоні діють одночасно, кожна на своїх клавішах.
- `+axis:control` — `dual-keyset`: два набори клавіш, по одному на аватар.
- `+card:length-budget`, `+card:severed-hand-box`, `+card:meet-goal` — див. «Мапа на каталог».

## Джерела
- ⭐ [itch: Handshakes](https://petpumpkin.itch.io/handshakes) — опис, керування, Lost Relic Games Jam 2022, автори; коментарі: «Retracting the longer hand after reaching the switch made the length limits click», «when you go back you get back your points», «push another player and destroy boxes», «cut off your hand», «the button can actually be pressed more than once», «we can skip levels».
- [Steam: Handshakes](https://store.steampowered.com/app/2171690/) — 30 пазлів, кооп, досягнення, таблиці рекордів, реліз 13.01.2023.
- [Steam: Handshakes: Hands On](https://store.steampowered.com/app/2245130/) — механіки сиквела.
- [Веб-збірка](https://html-classic.itch.zone/html/6448722/index.html) — назви з коду: `HandMovement` (`lengthRemaining`, `isMovingToPreviousSpace`, `RemoveArmSegment`, `OnArmCut`, `TryMoveHand`, `PushTile`), `ButtonListener` (`DoorToggle`, `DoorHoldOpen`, `OpenDoor`, `CloseDoor`), плитки `armLine`, `armBend`, `pushable`, `pushableHand`, `doorClosed`, `buttonToggle`, `handshake`, `SpeedRunner`, `SkipLevel`, `LevelOverview`.
- [GamingOnLinux](https://www.gamingonlinux.com/2023/02/handshakes-free-sokoban-puzzler-about-two-hands-meeting/page=1/) — «push boxes out of the way, open doors and more», відрізання руки.
- [A MAZE. Berlin 2023](https://2023.amaze-berlin.de/submissions/handshakes) — кооп на спільній клавіатурі чи двох контролерах.

## Непевне
- (?) Що саме відрізає руку: висновок «двері зачиняються на клітині з рукою» — з назв коду (`CloseDoor`, `OnArmCut`, `pushableHand`) і коментарів гравців; у грі не перевірено.
- (?) Що стається після відрізання: чи нова долоня зʼявляється біля бази і чи відновлюється довжина (у коді `AnimateOutArmSegments`, `DelayedActivateControlsAfterCut`, `ResetLength`).
- (?) Як «руйнуються ящики» і як саме «штовхають іншого гравця» — лише з коментаря.
- (?) Точна умова рукостискання: сусідні клітини назустріч чи вхід у клітину іншої долоні (у коді — `isApproachingFromOppositeDirection`).
- (?) Чи може рука перетнути свою чи чужу руку (у коді — `ProjectedPositionHasBlocker`, `HandBasePushArmBlockers`).
- (?) Довжина рук по рівнях і глибина undo — числа в джерелах не названі.
