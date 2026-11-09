---
title: Shrink Rooms
slug: shrink-rooms
aka: []
family: push-slide
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2025
platforms: [Windows]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3409430/Shrink_Rooms/", best: true, note: "опис: стіни стискаються щоходу-раунду, ящики на кнопки відкривають ворота, ями й пастки; механізми; 300+ рівнів, 5 розділів"}
  - {kind: itch, url: "https://ponegames.itch.io/shrink-rooms", note: "демо: стіни стискаються в кінці кожного раунду, слиз і портали, вибір рівня ходьбою, експонати"}
  - {kind: steam, url: "https://store.steampowered.com/app/3454020/Shrink_Rooms_Demo/", note: "демо в Steam"}
  - {kind: other, url: "https://steamcommunity.com/app/3409430/reviews/?browsefilter=toprated&l=english", note: "відгуки EN: порядок і час стискання видно, єдиний розвʼязок, слиз у світі 2, портали у світі 3, хаби"}
  - {kind: other, url: "https://steamcommunity.com/app/3409430/reviews/?browsefilter=toprated&l=schinese", note: "відгуки CN: бюджет кроків раунду, залізні ящики, «реверсні» кнопки, пропуск ходу в розділі 5"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Shrink+Rooms+puzzle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, keyboard-controls, push-object, impassable-cells, reach-exit, button-toggle, move-limit, environment-death, player-death, stick-together, teleport, undo-redo, restart-level, skip-level, level-unlock, level-select, achievements-window, +shrinking-arena, +crush-between-walls, +immovable-crate, +inverted-plate, +wait-turn, +hub-world, +secret-area, +optional-challenges]
proposes: ["+trigger:round_end", "+ui:round-steps", "+ui:shrink-direction", "+card:crush-between-walls", "+card:immovable-crate", "+card:inverted-plate"]
author: opus
date: 2026-11-09
---

# Shrink Rooms — Sokoban у кімнаті, стіни якої щораунду насуваються: план кроків до секунди, інакше розчавить

## Суть
Покроковий Sokoban-escape: треба поставити ящики на кнопки, щоб відчинити вихід, і втекти з кімнати. Поле саме є таймером: кожен раунд має бюджет кроків, після якого стіни зсуваються всередину, штовхаючи ящики й гравця; кого затиснуло — розчавлено. Порядок і час стискання видно наперед, тож кожен рівень має, за відгуком, «одну правильну комбінацію вводів». Далі додаються слиз-полімер (склеює), портали в стінах, якір-ящик, «клікер», ями й пастки.

## Поле і час
- Квадратна сітка кімнати, обнесена стінами; з кожним раундом корисна площа меншає з одного або кількох боків (напрям показано внизу праворуч екрана).
- Шари: підлога + ями/пастки + кнопки + ящики + стіни (рухомі межі) + портали на межі.
- Хід = крок гравця; раунд = кілька кроків (бюджет позначено рожевими стрілками), після раунду — стискання. Без вводу нічого не відбувається.
- Рівень-вибір (хаб) — теж кімната з механіками, де можна загинути.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | 1 життя на спробу | рух 4 напрямки; штовхає деревʼяні ящики |
| Рухома стіна (межа кімнати) | hazard | бік, графік стискань | після раунду зсувається на клітину всередину, штовхає все перед собою |
| Деревʼяний ящик | object | — | штовхається гравцем і стіною |
| Залізний ящик | object | — | гравець не штовхає; стіна штовхає |
| Сигнальна плита (кнопка) | switch | звичайна / «реверсна» | ящик на ній відкриває ворота; реверсна — навпаки |
| Ворота / вихід | gate | закриті / відчинені | відчиняються, коли натиснуті всі потрібні плити; вихід — перемога |
| Глибока яма | hazard | — | гравець падає — смерть (?); обʼєкт падає й зникає (?) |
| Пастка | hazard | — | смерть при вході (?) |
| Полімер (слиз) | object | — | склеює сусідні обʼєкти, далі рухаються разом; буває, що розклеює (світ 2) |
| Портальна стіна | terrain | пара | телепортує; знищена стисканням стає ямою (світ 3) |
| Якір-ящик | object | — | лише назва в описі Steam (?) |
| Клікер | switch | — | лише назва в описі Steam (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`, `counter(round_steps, -1)`.
- КОЛИ `contact(player, wood_crate)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `contact(player, iron_crate)` → ТО `block`.
- КОЛИ `counter(round_steps, ==, 0)` → ТО `custom: «межа кімнати з поточного боку зсувається на клітину всередину»`, `set_cell(edge_row, wall)`, `counter(round_steps, reset)`.
- КОЛИ `custom: «стіна зсувається»` → ЯКЩО `free(cell_behind_obstacle)` → ТО `push(crate|player)` (стіна штовхає і залізний ящик).
- КОЛИ `custom: «стіна зсувається»` → ЯКЩО `custom: «гравцю нікуди відступити»` → ТО `lose` (розчавлено).
- КОЛИ `enter(crate, plate)` → ТО `set_state(gate, open)`; КОЛИ `leave(crate, plate)` → ТО `clear_state(gate, open)`; реверсна плита — навпаки.
- КОЛИ `contact(player, gate)` → ЯКЩО `not state(gate, open)` → ТО `block`.
- КОЛИ `reach(player, exit)` → ЯКЩО `state(exit, open)` → ТО `win`.
- КОЛИ `enter(player, pit)` → ТО `lose` (?); КОЛИ `enter(object, pit)` → ТО `disappear_a` (?).
- КОЛИ `adjacent(slime, object)` → ТО `attach(slime, object)` — склеєні рухаються разом (?).
- КОЛИ `enter(a, portal)` → ТО `teleport(a, pair)`; КОЛИ `custom: «стіна наїхала на портал»` → ТО `set_cell(portal, pit)`.
- КОЛИ `input(wait)` → ТО `pass_turn`, `counter(round_steps, -1)` (з розділу 5).
- КОЛИ `input(undo)` → ТО `undo(1)`; КОЛИ `input(restart)` → ТО `restart` (undo не сягає за рестарт).
- Перемога: вийти з кімнати до того, як розчавить. · Поразка: затиснуло стіною, яма, пастка. · Рахунку нема; за основні рівні — «очки обчислювальної потужності» для відкриття розділів.

## Керування і ввід
- Клавіатура / геймпад / миша (itch): крок, undo, рестарт, пропуск ходу (з розділу 5).
- У хабі — та сама ходьба: вибір рівня = підійти до входу.

## Вікна, меню, HUD
- `main-menu` (?) → хаб розділу.
- `level-select` як ходильна кімната-хаб (`map-window` нема): входи в рівні, кути з найважчими пазлами, таблички з правилами нових механік, приховані рівні; «ключі регіонів» відкривають нові частини.
- `game-screen`: кімната; HUD — кроки до стискання (рожеві стрілки), напрям наступного стискання (внизу праворуч).
- `codex-window`-подібна галерея **віртуальних експонатів** з малюнками й описами (чорний гумор).
- `pause-menu`: undo/рестарт/вихід у хаб (?); `settings-window`: гучність; `achievements-window` (14).

## Фічі поза полем
- `levels-sequential` пачками по 3–5 рівнів одного розвʼязку; бонусні важчі пазли після основних (`+optional-challenges`).
- `level-unlock` за очками потужності; рівні можна пропускати (`skip-level`), не треба розвʼязувати всі.
- `+hub-world`: 5 розділів, кожен зі своїм хабом; швидкого переміщення нема.
- `collectibles`: експонати, приховані рівні (`+secret-area`), пасхалки.
- `undo` + `restart-level`; підказок нема; `autosave` (Save Anytime); 8 мов.

## Варіації й родичі
- [sokoban](sokoban.md) — ядро; [helltaker](helltaker.md) — ліміт ходів як лічильник; Bomberman — «Hurry Up» стискання арени в реальному часі (`+shrinking-arena`).
- Осі варіацій:
  - **ліміт**: лічильник ходів (Helltaker, XOR) / поле, що стискається від ходів (Shrink Rooms) / таймер реального часу (Bomberman);
  - **що робить стіна**: забирає клітини / ще й штовхає обʼєкти та гравця (Shrink Rooms);
  - **важкі обʼєкти**: усе штовхається / ящик лише для стіни, не для гравця (залізний).

## Цікавинки для курсу
- Стіна, що після N кроків зсувається всередину й штовхає ланцюг обʼєктів, з перевіркою «затиснуто» — 🥉.
- Графік стискань (який бік, коли) як дані рівня + HUD-превʼю — 📎.
- Два класи ящиків за «хто може штовхнути» (гравець / стіна) — 🌱 через таблицю сил.
- Реверсна плита та ворота «відкрито, коли всі натиснуті» — 🌱.
- Слиз, що склеює обʼєкти в групу для спільного поштовху — 🥈 (схоже на `stick-together`).
- Хаб-кімната як меню з тими самими правилами — 📎.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls`; `push-object`; `impassable-cells`; `reach-exit`; `button-toggle` ↔ плити й ворота; `move-limit` ↔ бюджет кроків раунду; `environment-death` + `player-death` ↔ розчавлення, ями; `stick-together` ↔ полімер; `teleport` ↔ портальні стіни; `undo-redo` + `restart-level`; `skip-level`; `level-unlock` + `level-select`; `achievements-window`.
- **Нема** → пропозиції карток:
  - `+shrinking-arena` (уже в корпусі) — тут від кроків, а не від таймера, і стіна штовхає.
  - `+crush-between-walls` «Затиснуто між стіною, що насувається, і перешкодою» · entities/death · 📎.
  - `+immovable-crate` «Ящик, якого не штовхає гравець, але штовхає середовище» · entities/legality · 🌱.
  - `+inverted-plate` «Плита, що відчиняє, поки НЕ натиснута» · entities/interact · 🌱.
  - `+wait-turn` (уже в корпусі) — пропуск ходу в розділі 5.
  - `+hub-world`, `+secret-area`, `+optional-challenges` (уже в корпусі).

## Пропозиції до словників
- `+trigger:round_end` — вичерпано бюджет кроків раунду (подія між ходом і тіком).
- `+ui:round-steps` — скільки кроків до наступного стискання (стрілки); `+ui:shrink-direction` — бік наступного стискання.
- `+card:crush-between-walls`, `+card:immovable-crate`, `+card:inverted-plate`.

## Джерела
- ⭐ [Steam: Shrink Rooms](https://store.steampowered.com/app/3409430/Shrink_Rooms/) — «Observe the timing of the wall contractions each turn», ящики відчиняють ворота, ями й пастки, механізми (Signal Pressure Plate, Polymers, Portal Walls, Anchor Crate, Clicker), 300+ рівнів, 5 розділів, очки потужності, експонати; реліз 28.05.2025, Mat-Rix / Pone Games.
- [itch: Shrink Rooms](https://ponegames.itch.io/shrink-rooms) — стіни стискаються в кінці кожного раунду, слиз і портали, вибір рівня ходьбою, приховані рівні.
- [Steam-відгуки EN](https://steamcommunity.com/app/3409430/reviews/?browsefilter=toprated&l=english) — показ порядку й часу стискань, єдиний розвʼязок, слиз (світ 2), портали (світ 3) → яма, undo/рестарт, хаби, ~300 рівнів пачками.
- [Steam-відгуки CN](https://steamcommunity.com/app/3409430/reviews/?browsefilter=toprated&l=schinese) — бюджет кроків раунду рожевими стрілками, напрям стискання в куті, залізні ящики, реверсні лінії, пропуск ходу, пропуск рівнів.
- YouTube: пошук «Shrink Rooms puzzle gameplay».

## Непевне
- (?) Чи стискається за раунд один бік чи кілька, і чи бюджет кроків однаковий у всіх раундах (CN-відгук: «не завжди однаковий»).
- (?) Що стається з ящиком у ямі (зникає / засипає) і чи яма вбиває гравця — є лише «avoid deep pits and traps».
- (?) Точна поведінка полімеру (склеює при дотику? розклеює?) — відгуки описують його через баги.
- (?) Якір-ящик і клікер — лише назви на Steam.
- (?) Кількість рівнів: itch — «200+», Steam — «300+», відгук — «трохи більше 300».
