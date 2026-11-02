---
title: Troddlers
slug: troddlers
family: grid-platformer
also: [build-sim]
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: coop
  info: full
  random: none
  goal: collect
year: 1992
platforms: [Amiga (1992), MS-DOS (1993), SNES (1993)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Troddlers", best: true, note: "чарівник, блоки, троддлери на стінах і стелі, зомбі, самоцвіти, цілі, 2 гравці, SNES-миша"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Troddlers+Amiga+gameplay", note: "пошук; геймплей Amiga"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Troddlers+SNES+gameplay", note: "пошук; SNES-версія з мишею"}
  - {kind: other, url: "https://www.mobygames.com/search/?q=Troddlers", note: "пошук MobyGames (точної сторінки не бачив)"}
stage: v1
coverage: 55
mechanics: [move-by-input, gravity-fall, impassable-cells, push-object, collect-quota, destroy-all-enemies, item-pickup, touch-death, time-out, sequential-levels, spawn-points, spawn-schedule, +create-destroy-block, +limited-blocks, +auto-walker-guide, +surface-crawler, +reverse-after-fall, +crush-transform, +mutual-annihilation, +mixed-objectives, +block-climb-trick, +level-password, +mode-coop]
proposes: ["+effect:toggle_block", "+effect:place", "+effect:face", "+effect:fall", "+trigger:landed", "+cond:charges", "+role:ally", "+role:spawner", "+ui:tool-charges", "+axis:control", "+axis:actors", "+axis:gravity", "+card:auto-walker-guide", "+card:surface-crawler"]
author: opus
date: 2026-11-02
---

# Troddlers — чарівник ставить і стирає блоки на шляху троддлерів, що ходять навіть по стелі

## Суть
Гравець керує чарівником Hokus (другий гравець — Pokus), який бігає, стрибає і магією ставить або стирає блоки розміром із себе. Троддлери виходять зі входу й ідуть самі в одному напрямку — по підлозі, стінах і стелі; блоками їх треба довести до виходу, а зомбі-троддлерів — знищити. Це **гібрид**: `avatar` (Hokus, як у Solomon's Key) + непряме керування натовпом (як у Lemmings). Цілі місії змішуються: врятувати N, знищити зомбі, зібрати самоцвіти — на час.

## Поле і час
- Бічний вигляд, клітинна сітка: блок = клітина = розмір чарівника. Рівень — один екран або трохи більший (?).
- Real-time: троддлери йдуть безперервно, зʼявляються зі входу з інтервалом (?); таймер місії.
- **Гравітація відносно поверхні:** троддлери тримаються поверхні, на якій ідуть, — підлоги, стіни, стелі; виходи бувають на стіні боком або на стелі догори дриґом. Hokus живе зі звичайною гравітацією вниз.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Hokus / Pokus | player | власний «тубус» на ≤15 блоків | біг, стрибок, ставить блок у сусідню вільну клітину, стирає блок у тубус |
| Троддлер | ally | напрям | іде вперед уздовж поверхні (підлога/стіна/стеля); без опори — падає; вижив після падіння — розвертається |
| Зомбі-троддлер (смертельний) | enemy | — | ходить, як троддлер; торкнувся звичайного — зникають обидва; вбиває чарівника |
| Зомбі-троддлер (нешкідливий) | enemy | — | як вище, але чарівникові не шкодить |
| Інші вороги | enemy | різні (?) | власна поведінка; камінь на них → синій самоцвіт |
| Блок | object | типів багато (?) | опора/стіна; поставлений на троддлера — вбиває його; стертий з-під — той падає |
| Камінь | object | — | стерти не можна, лише штовхнути; падає; на обʼєкт → обидва зникають, зʼявляються самоцвіти |
| Самоцвіт (червоний/зелений/синій) | pickup | колір | є з початку або народжується з каменя; збирається для цілі |
| Вхід | spawner | кількість троддлерів | випускає троддлерів |
| Вихід | static | орієнтація (підлога/стіна/стеля) | троддлер увійшов → +1 до врятованих; зомбі на виході ціллю не зараховується |
| Стіна рівня | static | — | непрохідна, не стирається |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(build, dir)` → ЯКЩО `free(cell_adjacent(dir))` and `custom: «charges(tube) > 0»` → ТО `custom: «place(block)»`, `counter(tube, -1)`.
- КОЛИ `input(erase, dir)` → ЯКЩО `cell(target, block)` and не камінь and `custom: «charges(tube) < 15»` → ТО `set_cell(target, empty)`, `counter(tube, +1)`.
- КОЛИ `input(build)` на клітині з троддлером → ТО `disappear_b` (блок розчавив троддлера).
- КОЛИ `tick` → ТО троддлер `move(a, forward)` уздовж поверхні; КОЛИ `blocked(a)` → ТО `custom: «переходить на стіну, що перед ним»` (?).
- КОЛИ `custom: «опору стерто»` → ТО `fall(troddler)`; КОЛИ `custom: «landed»` → ЯКЩО вижив → ТО `face(a, reverse)`; інакше `disappear_a` (?).
- КОЛИ `contact(troddler, exit)` → ТО `disappear_a`, `counter(saved, +1)`.
- КОЛИ `contact(zombie, troddler)` → ТО `disappear_both`.
- КОЛИ `contact(lethal_zombie|enemy, wizard)` → ТО `lose` (втрата життя / рестарт місії) (?).
- КОЛИ `contact(wizard, rock)` у бік руху → ЯКЩО `free(cell_behind)` → ТО `push`.
- КОЛИ `fall(rock)` на троддлера → ТО `disappear_both`, `spawn(red_gem)` (до 4); на камінь → `spawn(green_gem)`; на ворога → `spawn(blue_gem)`.
- КОЛИ `contact(wizard, gem)` → ТО `pickup`, `counter(gems, +1)`.
- КОЛИ `input(jump)` + стерти блок під собою в польоті + поставити новий → `custom: «драбина з двох блоків»` (підйом без великого запасу).
- КОЛИ `counter(saved, >=, quota)` and `all_gone(zombie)` (якщо ціль) and `counter(gems, >=, n)` (якщо ціль) → ТО `win`.
- КОЛИ `counter(time_left, ==, 0)` → ТО `lose`; КОЛИ `custom: «троддлерів лишилось менше за квоту»` → ТО `lose` (?).
- Перемога: комбінація з трьох цілей (врятувати N · знищити всіх зомбі · зібрати самоцвіти). Поразка: час, недостача троддлерів, смерть чарівника (?). Рахунок: (?).

## Керування і ввід
- Amiga/DOS: джойстик/клавіші — біг, стрибок; кнопка + напрям — поставити/стерти блок у сусідній клітині (будь-який напрям поруч із чарівником) (?точна схема).
- SNES: можна мишею — курсор-приціл, права кнопка будує блок; тоді керування стає наполовину курсорним.
- Двоє гравців одночасно: Hokus і Pokus, у кожного свій тубус блоків.

## Вікна, меню, HUD
- `splash-screen` — титул.
- `main-menu`: 1 гравець · 2 гравці · пароль → `level-password` (?).
- `game-screen` — рівень; HUD: `ui:tool-charges` (тубус блоків 0–15) на кожного гравця, `timer-countdown`, лічильник врятованих/потрібних (`progress-bar`), самоцвіти, зомбі лишилось (`remaining-counter`) (?).
- `custom-window` — брифінг місії: які цілі цього рівня (?).
- `end-screen` — місію виконано / провалено, далі пароль.
- Переходи: splash → main-menu → брифінг → game-screen → end-screen → наступна місія.

## Фічі поза полем
- `levels-sequential` місій зі змішаними цілями; `level-password` (?).
- `mode-coop`: двоє чарівників на одному екрані, окремі запаси блоків.
- `mouse-and-keyboard` — SNES Mouse як альтернативний ввід.

## Варіації й родичі
- Lemmings (натовп автоходців, яким не керуєш напряму), Solomon's Key (ставити/стирати блок поруч), Mario & Wario (вести сліпого ходця блоками), Toki Tori (обмежені інструменти).
- **Осі варіацій:** хто веде (аватар / курсор / обидва) · по чому ходить ходець (лише підлога / вся поверхня) · що з блоком (ставити / стерти / обидва, з запасом) · ціль (врятувати N / знищити зомбі / зібрати / комбінація).

## Цікавинки для курсу
- Троддлер, що тримається поверхні й переходить на стіну й стелю — 🥈 (локальна «гравітація» як орієнтація сутності).
- Натовп автоходців + квота врятованих — 🥉 (спавн із інтервалом, лічильник, умова перемоги).
- Ставити/стерти блок із запасом-тубусом 15 — 📎 (повтор `+create-destroy-block` з лімітом).
- Камінь як «реактор»: тип обʼєкта під каменем → колір самоцвіта — 📎 (таблиця взаємодій як дані).
- Зомбі анігілює зі звичайним — 🌱, але задає планування «кого кому підставити».
- Змішані цілі місії (AND з 1–3 умов) — 📎 (цілі як конфіг рівня).

## Мапа на каталог
- Є: `move-by-input` · `gravity-fall` · `impassable-cells` · `push-object` (камінь) · `collect-quota` (врятувати N, самоцвіти) · `destroy-all-enemies` (зомбі) · `item-pickup` · `touch-death` · `time-out` · `sequential-levels` · `spawn-points` + `spawn-schedule` (вхід).
- **Нема** → пропозиції карток:
  - `+create-destroy-block` (повтор Solomon's Key, Kickle) — тут у будь-який сусідній бік.
  - `+limited-blocks` (повтор Emberward) · слот {capacity: 15}.
  - `+auto-walker-guide` «Вести автоходців до виходу» · entities/move · 🥈 · слоти {spawn_every, quota}.
  - `+surface-crawler` «Ходить по стінах і стелі» · entities/move · 🥈 · слот {corners: convex|concave|both}.
  - `+reverse-after-fall` «Після падіння — розворот» · entities/move · 🌱.
  - `+crush-transform` «Падіння каменя: обидва зникають, зʼявляється продукт за типом» · entities/interact · 📎 · слот {table}.
  - `+mutual-annihilation` «Два типи знищують одне одного при дотику» · entities/interact · 🌱.
  - `+mixed-objectives` «Комбіновані цілі рівня» · game-logic/win · 📎.
  - `+block-climb-trick` «Підйом стрибком + перестановкою блока» · entities/move · 📎.
  - `+level-password` (повтор), `+mode-coop` — кооп двох аватарів.

## Пропозиції до словників
- `+effect:toggle_block(cell)` (повтор Solomon's Key) — ставити/стирати однією дією; `+effect:place` (🔥).
- `+effect:face(a, reverse)` і `+effect:fall` — розворот після падіння.
- `+trigger:landed(a)` — сутність приземлилась (перевірка «вижив/ні»).
- `+cond:charges(tube, op, n)` — запас блоків (повтор Boxboy/Toki Tori).
- `+role:ally` (троддлер), `+role:spawner` (вхід).
- `+ui:tool-charges` — тубус блоків.
- `+axis:control` = `direct` (чарівник) + `indirect` (троддлери); `+axis:actors` = `swarm`; `+axis:gravity` = `per-surface` (нове значення: гравітація відносно поверхні, на якій стоїть сутність).
- `+card:auto-walker-guide`, `+card:surface-crawler` — див. вище.

## Джерела
- ⭐ [Wikipedia: Troddlers](https://en.wikipedia.org/wiki/Troddlers) — чарівник і блоки (тубус 15), троддлери на стінах і стелі, зомбі двох видів, камені й самоцвіти трьох кольорів, три цілі, 2 гравці, SNES-миша.
- YouTube: пошук «Troddlers Amiga gameplay» і «Troddlers SNES gameplay».
- MobyGames: пошук «Troddlers» (точної сторінки не бачив).

## Непевне
- (?) Типи блоків: Wikipedia каже «багато типів зі спецефектами», але не перелічує; таблиця сутностей тут неповна.
- (?) Як троддлер переходить на стіну (входить на неї при упорі чи огинає край назовні) — з памʼяті про відео, не перевірено.
- (?) Смертельна висота падіння троддлера, інтервал спавну, кількість рівнів (≈100?), наявність паролів, система життів чарівника, рахунок.
- (?) Чи є режим змагання двох гравців (окремі виходи) — знайдено лише «у кожного свій тубус».
- Джерела Hall of Light / Lemon Amiga / MobyGames недоступні (403/404), WebSearch вичерпано.
