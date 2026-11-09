---
title: Bumpy
slug: bumpy
aka: [Bumpy's Arcade Fantasy, Pop-Up, Cool Ball]
family: grid-platformer
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 1989
platforms: [ZX Spectrum, Amstrad CPC, MSX, Atari ST, DOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bumpy%27s_Arcade_Fantasy", best: true, note: "коротко: мʼяч, зібрати предмети → вихід, руйновані й вогняні платформи, крапля води; ремейки Pop-Up / Cool Ball"}
  - {kind: other, url: "https://spectrumcomputing.co.uk/entry/763/ZX-Spectrum/Bumpy", note: "автори, 2 гравці по черзі, керування, огляди в журналах, відео"}
  - {kind: other, url: "https://www.the-tipshop.co.uk/cgi-bin/info.pl?name=Bumpy", note: "поради з Your Sinclair 66: липкі білі платформи, Fire — високі відскоки, H — оглянути екран; чит 99 усього"}
  - {kind: other, url: "https://archive.org/stream/Your_Sinclair_064/Your_Sinclair_064#page/n12/mode/1up", note: "Your Sinclair 64 (1991): кут-платформи, танучі платформи, вода проти вогню, молоток проти стін, 100 екранів"}
  - {kind: other, url: "https://archive.org/stream/microhobby-magazine-196.pdf/MicroHobby_196#page/n27/mode/1up", note: "MicroHobby 196 (1990, ES): зʼїсти все → двері; ключі, молотки, краплі; 3 життя, 100 рівнів"}
  - {kind: play, url: "https://archive.org/details/msdos_Bumpy_1989", note: "DOS-версія в браузерному емуляторі archive.org"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Bumpy+Loriciels+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-by-input, keyboard-controls, gravity-fall, floor-types, destructible-blocks, key-and-door, inventory-items, item-pickup, collect-all, reach-exit, player-death, environment-death, extra-life-threshold, event-points, cheat-codes, status-panel, sequential-levels, main-menu, +bounce-move, +variable-jump-hold, +crumble-floor, +sticky-platform, +angled-bounce, +exit-appears]
proposes: ["+card:sticky-platform", "+card:angled-bounce", "+card:exit-appears", "+feature:route-preview"]
author: opus
date: 2026-11-09
---

# Bumpy — мʼяч, що безперервно скаче по сітці платформ, зʼїдає всю їжу на екрані, щоб відчинились двері

## Суть
Французька аркада-головоломка Loriciels (1989). Гравець керує мʼячем Bumpy, який **сам постійно підстрибує**: можна лише кермувати вліво-вправо й утримувати Fire для високого відскоку. Екран — сітка платформ із їжею й інструментами; коли зʼїдено всю їжу, зʼявляються двері на наступний рівень. Складність — у маршруті: ключі, молотки й краплі води треба зібрати раніше, ніж знадобляться, а похилі, липкі й танучі платформи відбирають контроль.

## Поле і час
- Один екран на рівень; платформи стоять у гніздах сітки 6 стовпців × 6 рядів (скриншот CPC), між ними — стіни.
- 100 рівнів (MicroHobby, YS); у DOS-версії файл рівнів має 100 записів по 189 байтів.
- Реальний час: мʼяч скаче без зупинки, гравітація тягне вниз; висоту відскоку задає Fire, напрям у польоті — джойстик.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Bumpy (мʼяч) | player | 3 життя | безперервно відскакує; ←/→ у польоті; Fire — високий відскок |
| Звичайна платформа | terrain | — | пружна опора для відскоку |
| Похила платформа | terrain | кут | відбиває в заданому напрямку, керування на час відскоку зникає; дві похилі поруч можуть «зациклити» мʼяч |
| Липка біла платформа | terrain | — | мʼяч прилипає; щоб відскочити, Fire треба натиснути ще до приземлення |
| Тануча платформа | terrain | — | після приземлення зникає — назад цим шляхом не пройти |
| Вогняна платформа | hazard | — | смерть, якщо нема краплі води; з краплею — гаситься |
| Цегляна стіна | static | — | руйнується, якщо є молоток |
| Стіна під ключ | gate | — | відкривається ключем |
| Їжа (вишні, груша, банан…) | pickup | очки | зʼїсти всю → зʼявляються двері |
| Ключ · молоток · крапля води | pickup | лічильник у HUD | витрачаються на стіну / двері / вогонь |
| Блискавка | pickup | лічильник у HUD | призначення не знайдено (?) |
| Двері-вихід | gate | зʼявляються | вхід → наступний рівень |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `contact(bumpy, platform)` → ТО `bounce(bumpy)`; ЯКЩО `custom: «Fire утримується»` → ТО `custom: «високий відскок»`; від верху стіни високого відскоку нема.
- КОЛИ `input(left|right)` → ЯКЩО `custom: «мʼяч у польоті після звичайного відскоку»` → ТО `move(bumpy, dir)`.
- КОЛИ `contact(bumpy, angled_platform)` → ТО `bounce(bumpy)` `custom: «напрям і висота задані кутом, ввід ігнорується»`.
- КОЛИ `contact(bumpy, sticky_platform)` → ЯКЩО `custom: «Fire натиснуто до приземлення»` → ТО `bounce(bumpy)`; інакше `set_state(bumpy, stuck)`.
- КОЛИ `contact(bumpy, melting_platform)` → ТО `disappear(melting_platform)`.
- КОЛИ `contact(bumpy, fire_platform)` → ЯКЩО `has(bumpy, water_drop)` → ТО `take(bumpy, water_drop)`, `set_cell(platform, normal)`; інакше `lose`, `lives(-1)`.
- КОЛИ `contact(bumpy, brick_wall)` → ЯКЩО `has(bumpy, hammer)` → ТО `take(bumpy, hammer)`, `disappear(brick_wall)`; інакше `bounce`.
- КОЛИ `contact(bumpy, lock_wall)` → ЯКЩО `has(bumpy, key)` → ТО `take(bumpy, key)`, `disappear(lock_wall)`.
- КОЛИ `contact(bumpy, food)` → ТО `pickup`, `score(n)`.
- КОЛИ `contact(bumpy, key|hammer|water_drop)` → ТО `pickup`, `counter(item, +1)`.
- КОЛИ `all_gone(food)` → ТО `spawn_at(exit_door, level_exit)`.
- КОЛИ `enter(bumpy, exit_door)` → ТО `next_level`, `custom: «бонус рівня»` (?).
- КОЛИ `counter(score, >=, threshold)` → ТО `lives(+1)` (додаткові життя «за очки й предмети»).
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over`.
- Перемога: пройти 100 рівнів. · Поразка: вогонь без краплі та інші пастки, вичерпані життя. · Рахунок: очки за їжу й предмети.

## Керування і ввід
- Джойстик (Kempston, Interface 2) або клавіші Q, A, O, P + Fire.
- ←/→ — напрям польоту; Fire утримувати — високі відскоки (серія, якщо тримати під час руху); Fire до приземлення — зірватися з липкої платформи.
- Утримувати H на старті екрана — оглянути рівень і спланувати маршрут.
- Два гравці грають по черзі (Spectrum).

## Вікна, меню, HUD
- `splash-screen` / завантаження («chargement en cours…» у DOS).
- `main-menu` — титул із вибором керування (джойстик / клавіші); там же чит: натиснути всі клавіші → по 99 усього.
- `game-screen` — поле зліва, права панель: `lives`, `score`, лічильники крапель, ключів, молотків і блискавок (по два числа на рядок (?)), `custom` бонус, ще один лічильник зі смайлом (?).
- `end-screen` / game over — (?).
- Переходи: титул → рівень → (двері) наступний рівень → … → (життя 0) титул.

## Фічі поза полем
- `levels-sequential` (100 рівнів), `extra-life-threshold`, `cheat-codes` (99 усього), `route-preview` (H).
- 2 гравці по черзі (`hotseat`-подібно, рахунок окремо).
- DOS-версія містить файли редактора (`EDIT.CPL`) і окрему таблицю рівнів гравця (`JOUETABL.BUM`) — ймовірно, `level-editor` (?).

## Варіації й родичі
- Pop-Up (Infogrames, 1991, 16-біт; на Game Boy у США — Cool Ball) — та сама гра з новою графікою; Bumpy's Arcade Fantasy (1992) — ремейк.
- У сімʼї: [Mappy](mappy.md) (батути й керування висотою стрибка — порівняння MobyGames), [Spherical](spherical.md) (мʼяч і чарівник), [Solomon's Key](solomons-key.md) (ключ і вихід на одному екрані).
- Осі варіацій: **керування відскоком** — нема / висота (Fire) / напрям (тут обидва в польоті); **що відкриває вихід** — ключ / зібрати все (тут) / дійти; **реакція платформи** — пружна / липка / похила / тане / горить.

## Цікавинки для курсу
- Аватар, що сам безперервно скаче, з керуванням лише напрямом і висотою — 📎.
- Типи платформ як таблиця реакцій (пружна, липка, похила, тане, горить) — 🥉.
- Інструменти-дозволи (ключ, молоток, крапля), що витрачаються на «свою» перешкоду — 📎.
- Двері зʼявляються, коли зʼїдено всю їжу — 🌱.
- Утримати H — огляд рівня перед стартом — 🌱.

## Мапа на каталог
- Є: `move-by-input` + `keyboard-controls`; `gravity-fall`; `floor-types` ↔ липкі, похилі, вогняні платформи; `destructible-blocks` ↔ цегла під молоток; `key-and-door` ↔ стіни під ключ; `inventory-items` + `item-pickup` ↔ ключі, молотки, краплі; `collect-all` ↔ уся їжа; `reach-exit` ↔ двері; `player-death` + `environment-death` ↔ вогонь; `extra-life-threshold`; `event-points`; `cheat-codes`; `status-panel` ↔ права панель; `sequential-levels`; `main-menu`.
- **Нема** → пропозиції карток:
  - `+bounce-move`, `+variable-jump-hold`, `+crumble-floor` — уже пропоновані в корпусі.
  - `+sticky-platform` «Липка платформа: зірватися можна лише вчасною дією» · entities/move · 🌱.
  - `+angled-bounce` «Похила поверхня відбиває під кутом і забирає керування» · entities/move · 📎.
  - `+exit-appears` «Вихід зʼявляється після виконання квоти» · game-logic/win · 🌱.

## Пропозиції до словників
- `+card:sticky-platform`, `+card:angled-bounce`, `+card:exit-appears` — див. вище.
- `+feature:route-preview` — огляд рівня перед стартом без руху (утримати H).

## Джерела
- ⭐ [Wikipedia: Bumpy's Arcade Fantasy](https://en.wikipedia.org/wiki/Bumpy%27s_Arcade_Fantasy) — мета й типи платформ коротко, ремейки Pop-Up / Cool Ball / 1992.
- [Spectrum Computing: Bumpy](https://spectrumcomputing.co.uk/entry/763/ZX-Spectrum/Bumpy) — автори (Luis Jorge Garcia, J250), 2 гравці по черзі, керування, список оглядів, відео.
- [The Tipshop: Bumpy](https://www.the-tipshop.co.uk/cgi-bin/info.pl?name=Bumpy) — поради YS 66 (липкі платформи, Fire, H), чит, POKE на ключі/молотки/воду.
- [Your Sinclair 64](https://archive.org/stream/Your_Sinclair_064/Your_Sinclair_064#page/n12/mode/1up) — опис cover game: похилі й танучі платформи, вода/вогонь, молоток/стіни, 100 екранів, керування QAOP.
- [MicroHobby 196](https://archive.org/stream/microhobby-magazine-196.pdf/MicroHobby_196#page/n27/mode/1up) — зʼїсти все → двері, ключі/молотки/краплі, 3 життя, 100 рівнів.
- [archive.org: DOS-версія](https://archive.org/details/msdos_Bumpy_1989) — опис MobyGames (порівняння з Mappy), файли гри; [CPC-версія](https://archive.org/details/Bumpy_1989_Loriciels_fr) — скриншот із сіткою 6×6 і HUD.
- [Відео Spectrum Computing](https://youtu.be/2G0bwcmNBPw) — геймплей (лінк зі сторінки гри, не переглядав).

## Непевне
- (?) Чи рух між платформами дискретний (по стовпцях сітки), чи вільний піксельний; сітка 6×6 — лише з одного скриншота CPC.
- (?) Призначення блискавки й лічильника зі смайлом, сенс двох чисел у рядках HUD, звідки бонус рівня.
- (?) Що стається, коли мʼяч зациклився між похилими платформами (втрата життя чи вихід через H/самогубство).
- (?) Наявність редактора рівнів у DOS-версії — лише за іменами файлів.
- (?) Ремейк 1992 «Bumpy's Arcade Fantasy» — платформи й відмінності не перевірені.
