---
title: AmaZoo
slug: amazoo
aka: []
family: grid-platformer
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2025
platforms: [PC (Windows)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3066360/AmaZoo/", best: true, note: "опис: Sokoban збоку, дії KoKo (нести, покласти, кинути, скласти стосом, стрибнути, вилізти, копнути), небезпеки (високі сходи, преси, несправні машини, шипи, лазери, вибухівка), 100+ рівнів, рекорди; трейлер і 9 знімків"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3066360", note: "новини Steam: патчі демо й релізу (колісний ящик, скасування взяття/кидка, роботи, глечики, геймпад)"}
  - {kind: official, url: "https://turbosoda.games/", note: "сайт студії Turbo Soda Games"}
  - {kind: youtube, url: "https://www.youtube.com/@TurboSodaGames", note: "канал студії"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=AmaZoo+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-by-input, gravity-fall, push-object, impassable-cells, reach-exit, sequential-levels, level-select, restart-level, move-counter, score-records, save-progress, touch-death, environment-death, beam-tracing, explode-area, destructible-blocks, button-toggle, cell-click, game-pause, game-screen, pause-menu, end-screen, tutorial-window, achievements-window, movement-animation, idle-animation, particles, +carry-object, +throw-item, +stack-climb, +step-climb-1, +kick-object, +rolling-box, +fragile-object, +crush-by-fall, +piston-extend, +pressure-plate]
proposes: ["+effect:climb", "+effect:kick", "+effect:stack", "+ui:move-budget-bar", "+feature:cancel-hold-action", "+card:kick-object", "+card:rolling-box", "+card:fragile-object"]
author: opus
date: 2026-11-19
---

# AmaZoo — Sokoban збоку на складі: носи, став стосом, кидай і копай ящики, щоб дістатися виходу

## Суть
KoKo, новенький комірник складу AmaZoo, у перший робочий день переставляє ящики, щоб пробитися до виходу. Це Sokoban у вигляді збоку з гравітацією: ящик можна не лише штовхнути, а й підняти над головою, поставити стосом, кинути чи копнути, а потім вилізти по ньому. Ядро — **типи ящиків з власною поведінкою** (колісний котиться, глечик тріскає, бомба вибухає) плюс машини складу: преси, поршні, лазери, шипи, роботи.

## Поле і час
- Клітинна кімната, вид збоку; рівень — одна кімната (?) з написом «AREA 07-04» на стіні (етап — рівень).
- Гравітація: KoKo, ящики й роботи падають до опори; на перешкоду висотою 1 KoKo вилазить.
- Хід = одна дія (крок, підйом, взяти, кинути…); лічильник у HUD росте на 1 за крок, без вводу світ стоїть (трейлер покадрово); чи рахуються взяти / кинути — (?).
- Шари: стіни й платформи (зокрема ґратчасті мости), ящики й роботи, машини (поршні, преси, лазери), кнопки на підлозі, вихід.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| KoKo | player | напрям; несе 0/1 предмет | крок ліво/право; підйом на 1; бере, кладе, кидає, копає; розворот на місці |
| Картонний ящик | object | — | штовхається, береться, кладеться стосом, кидається |
| Колісний ящик (зелений, «↔») | object | — | від поштовху котиться (?); поштовх у інший колісний запускає й того |
| Глечик (синій візерунок) | object | ціле / тріснуте / розбите | тріскає від удару (копняк, кидок (?)); повністю розбитий не береться |
| Ящик-ключ і важкий ящик (з патчів) | object | — | обидва падають і беруться в руки; на знімках — ймовірно, дерев'яний ящик із замком і електронний ящик із замковою щілиною; що є що й навіщо — (?) |
| Ящик-бомба (динаміт із будильником) | object | — | вибухає площею, руйнує тріснуті блоки (знімки); запуск — (?) |
| Ящик «⚠» з зубчастим верхом | object | — | видно на знімках; поведінка — (?) |
| Ящики з турбіною, гучномовцем, токсичною рослиною, сталеві «X» | object | — | видно на знімках; токсичний розбивається зеленою хмарою (?) |
| Тріснутий цегляний блок | static | — | руйнується вибухом |
| Робот (кіт-скелет на гусеницях із дулом) | enemy | — | падає; падіння на KoKo вбиває; прес чи обвал його розчавлює; буває оглушений (зірочки — поруч колісний ящик) (?); чи стріляє — (?) |
| Шипи (жовто-чорні) | hazard | — | KoKo на них гине |
| Лазер | hazard | напрям променя | промінь до першої перешкоди; ящик перекриває його (знімки) |
| Прес / вертикальний поршень | hazard | — | опускається й розчавлює (кадр «Watch out!») |
| Горизонтальний поршень | switch | — | висувається й штовхає блоки (знімок) (?) |
| Червона кнопка на підлозі | switch | → поршні, двері (?) | натиск перемикає звʼязані машини (?) |
| Двері-шлюз (зелено-червоні) | gate | відкрито / закрито | пропускають за станом |
| Вихід (зелений знак «EXIT») | static | — | KoKo дійшла — рівень пройдено |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(koko, dir)`, `counter(moves, +1)`.
- КОЛИ `input(dir)` → ЯКЩО `not free(next)` і `free(above_next)` → ТО `custom: «вилізти на сходинку висотою 1»` — і з ящиком у руках («climb with the boxes in hand»).
- КОЛИ `input(dir)` → ЯКЩО `not supported(koko)` → ТО `fall(koko)`; так само падають ящики й роботи.
- КОЛИ `input(click_koko)` → ТО `face(koko, reverse)` — розворот на місці.
- КОЛИ `input(take)` (затиснута ЛКМ на ящику) → ЯКЩО `not has(koko, item)` → ТО `carry(koko, box)` — ящик над головою.
- КОЛИ `input(drop)` → ЯКЩО `has(koko, box)` і `free(front)` → ТО `place(box, front)`, `fall(box)`.
- КОЛИ `input(drop)` → ЯКЩО `has(koko, box)` і `occupied(front, box)` → ТО `place(box, above_front)` — стос, по якому далі лізуть.
- КОЛИ `input(throw)` (затиснута ПКМ, відпустити) → ЯКЩО `has(koko, box)` → ТО `throw(box, dir)`, `fall(box)`; дальність — (?).
- КОЛИ `input(opposite_button)` → ЯКЩО `state(koko, taking)` або `state(koko, aiming)` → ТО `custom: «скасувати взяття / кидок»`.
- КОЛИ `input(kick)` → ЯКЩО `occupied(front, box)` → ТО `custom: «відкинути ящик геть»` (?).
- КОЛИ `input(kick)` → ЯКЩО `occupied(front, pot)` → ТО `set_state(pot, cracked)`.
- КОЛИ `state_on(pot, broken)` → ТО `custom: «більше не береться»`.
- КОЛИ `contact(koko, wheel_box)` → ЯКЩО `free(cell_behind)` → ТО `push`, `slide(wheel_box, dir)` (?).
- КОЛИ `contact(wheel_box, wheel_box)` → ТО `slide(other, dir)` — інший теж котиться.
- КОЛИ `contact(robot, koko)` → ЯКЩО `moving(robot, down)` → ТО `lose`.
- КОЛИ `contact(press, a)` → ЯКЩО `moving(press, down)` → ТО `lose` для KoKo; `custom: «робота розчавлено»` для робота.
- КОЛИ `enter(koko, spikes)` → ТО `lose`.
- КОЛИ `line_of_sight(laser, koko)` → ТО `lose` (?); ящик на лінії → `block` для променя.
- КОЛИ `custom: «бомба спрацювала»` → ТО `explode(area)`; тріснуті блоки в зоні → `disappear_b`.
- КОЛИ `enter(a, red_button)` → ТО `set_state(linked_machine, toggled)` (?).
- КОЛИ `enter(koko, exit)` → ТО `win`, `message("GOOD JOB!")`, `next_level`.
- КОЛИ `input(restart)` → ТО `restart`.
- КОЛИ `level_end` → ТО `custom: «зберегти власний рекорд рівня»`.
- Перемога: KoKo біля виходу. · Поразка: шипи, прес, робот згори, лазер (?) → рестарт рівня (?). · Рахунок: лічильник дій; рекорд рівня («optimizing your work is key»); смуга біля лічильника змінює колір синій → помаранчевий → червоний (?).

## Керування і ввід
- Миша (основне): затиснути ЛКМ на ящику — взяти; затиснути ПКМ — прицілитись і кинути; протилежна кнопка скасовує дію (патч 17.02.2025); ЛКМ на KoKo — розворот.
- Як ходити мишею (клік по клітині, тягнення) — (?).
- Геймпад — з квітня 2025 (повна підтримка, вібрація, навчання переписане під геймпад); DualSense.
- Кнопки HUD: рестарт і пауза.

## Вікна, меню, HUD
- `game-screen`: кімната збоку; угорі ліворуч `move-counter` (число) і смуга-шкала (+ui `move-budget-bar` (?)); угорі праворуч `restart-button` і `pause-button`; номер «AREA 07-04» намальований на стіні (`level-number`).
- `pause-menu`: з номером етапу й рівня (патч демо).
- `end-screen`: напис «GOOD JOB!» поверх кімнати.
- `tutorial-window`: навчальні рівні (01-06 — як тримати й кидати ящик у потрібний бік).
- `level-select` (?): «replay levels to beat your own record».
- `settings-window`: вібрація геймпада (патч) та інше — (?).
- `achievements-window`: 20 досягнень Steam; Steam Stats.
- Переходи: меню → рівень → (вихід) «GOOD JOB!» → наступний рівень; (смерть) → рестарт рівня (?).

## Фічі поза полем
- `levels-sequential`: 100+ рівнів у етапах «AREA етап-рівень» (видно до 17-04; рівнів на етап — до 6) (?).
- `restart-level`, `pause`; undo в джерелах не згадано (?).
- Рекорди: переграти рівень, щоб побити власний результат; `stats` Steam.
- `gamepad-support` (оновлення 10.04.2025), `cloud-save`, `achievements` (20).
- Безкоштовне демо (20+ рівнів) з формою відгуку в грі.

## Варіації й родичі
- [Block Dude](block-dude.md) — той самий кістяк: нести один блок, лізти на висоту 1; AmaZoo додає кидок, копняк і типи ящиків.
- [Bonfire Peaks](../thinky/bonfire-peaks.md) — ящики на голові й сходи з ящиків, але в 3D.
- [BoxBoy!](boxboy.md), [Catrap](catrap.md), [Quadrax](quadrax.md), [Hako-Oshimai](hako-oshimai.md) — клітинні платформери з блоками.
- [Sokoban](../push-slide/sokoban.md) — джерело, на яке посилається опис.
- Осі варіацій:
  - **як позбутися ящика**: поставити / поставити стосом / кинути / копнути;
  - **тип ящика**: звичайний / колісний / крихкий / вибуховий / ключ / важкий;
  - **хто ще рухається**: ніхто / роботи, яких оглушують і розчавлюють / машини за кнопками.

## Цікавинки для курсу
- Нести-покласти-кинути ящик у світі збоку з гравітацією — 📎 (стан `carrying` + падіння після дії).
- Стос ящиків як сходи: підйом на 1 з вантажем у руках — 📎.
- Колісний ящик: котиться до упору й передає рух іншому колісному — 📎.
- Лазер до першої перешкоди й ящик як щит — 📎 (картка `beam-tracing`).
- Бомба й тріснуті блоки, вибух площею — 🥉.
- Прес і поршні за кнопками, що розчавлюють — 🥉.
- Розвʼязувач BFS для Sokoban збоку з гравітацією й перенесенням — 🥇.

## Мапа на каталог
- Є: `move-by-input` ↔ крок; `gravity-fall` ↔ падіння; `push-object` ↔ поштовх; `impassable-cells` ↔ стіни; `reach-exit` ↔ вихід; `sequential-levels` + `level-select` ↔ етапи й переграш; `restart-level` ↔ кнопка рестарту; `move-counter` + `score-records` + `save-progress` ↔ лічильник дій і рекорд; `touch-death` + `environment-death` ↔ роботи, шипи, прес; `beam-tracing` ↔ лазери; `explode-area` + `destructible-blocks` ↔ бомби й тріснуті блоки; `button-toggle` ↔ червоні кнопки; `cell-click` ↔ клік мишею; `game-pause` + `pause-menu` + `game-screen` + `end-screen` + `tutorial-window` + `achievements-window`; `movement-animation`, `idle-animation` (патч), `particles` ↔ вибухи й уламки.
- **Нема** → пропозиції карток:
  - `+carry-object` · `+throw-item` · `+stack-climb` · `+step-climb-1` · `+crush-by-fall` · `+piston-extend` · `+pressure-plate` — уже в корпусі.
  - `+kick-object` «Копняк: ящик відлітає або тріскає» · entities/interact · 📎 · слот {result: fly|crack}.
  - `+rolling-box` «Колісний ящик котиться від поштовху й передає рух іншому» · entities/move · 📎.
  - `+fragile-object` «Крихкий обʼєкт: стани ціле → тріснуте → розбите, розбитий не береться» · entities/state · 🌱.

## Пропозиції до словників
- `+effect:climb` — вилізти на сходинку висотою 1 (як у Block Dude), тут ще й із вантажем.
- `+effect:kick` — копнути предмет перед собою (відлітає або тріскає).
- `+effect:stack` — покласти предмет на інший предмет (стос як сходи).
- `+ui:move-budget-bar` — смуга біля лічильника дій, що міняє колір у міру зростання числа (?).
- `+feature:cancel-hold-action` — скасувати затиснуту дію (взяти / кинути) протилежною кнопкою миші.
- `+card:kick-object`, `+card:rolling-box`, `+card:fragile-object` — див. «Мапу на каталог».

## Джерела
- ⭐ [Steam: AmaZoo](https://store.steampowered.com/app/3066360/AmaZoo/) — опис дій і небезпек, 100+ рівнів, рекорди; категорії (20 досягнень, Stats, повна підтримка контролера, Steam Cloud); трейлер і 9 знімків (переглянуто покадрово: типи ящиків, роботи, лазери, преси, HUD, «GOOD JOB!»).
- [Steam News API, app 3066360](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3066360) — патчі: колісний ящик штовхає інший, розворот кліком по KoKo, номери етапу й рівня, скасування взяття/кидка, роботи (падіння на KoKo вбиває, розчавлення), розбиті глечики, ящик-ключ і гравітація, важкий ящик, геймпад і вібрація, навчальний рівень 01-06.
- [Turbo Soda Games](https://turbosoda.games/) — сторінка студії: «Push, kick, grab and rearrange the boxes».
- YouTube: [канал студії](https://www.youtube.com/@TurboSodaGames) і пошук «AmaZoo gameplay».

## Непевне
- (?) Сімʼя: за `families.md` гра з гравітацією й підйомом — `grid-platformer` (як Block Dude), хоча в черзі стоїть у `push-slide`.
- (?) Як саме ходити мишею (клік по клітині чи інакше) і чи є клавіатура; що робить копняк із картонним ящиком.
- (?) Призначення ящика-ключа, важкого, «⚠», турбінного, гучномовця й токсичного — видно лише на знімках.
- (?) Чи котиться колісний ящик до упору чи на 1 клітину; що вмикає бомбу (таймер, удар, лазер).
- (?) Чи вбиває лазер, чи лише перекриває шлях; що саме перемикають червоні кнопки.
- (?) Як ходять роботи (патруль, розворот біля стіни) і чому на знімку вони «оглушені» зірочками.
- (?) Значення смуги біля лічильника дій (пар, рекорд чи медаль); чи є undo.
- (?) Кількість етапів і рівнів на етап (видно 17-04 і рівні до 06).
