---
title: Prince of Darkness Jr.
slug: prince-of-darkness-jr
aka: [Prince of Darkness Junior]
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
platforms: [Windows, web (jam-версія 2023)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3716870/", best: true, note: "опис: не ступай у світло, блоки кидають тінь, двері, вікна, секрети; 200+ рівнів; трейлер"}
  - {kind: official, url: "https://pondarea.com/", note: "сайт Pond Area: «box-pushing, shadow-casting», «don't touch the light»"}
  - {kind: itch, url: "https://elphyl.itch.io/princeofdarknessjr", note: "jam-версія 1-Bit Game Jam 2023: керування, ящики й картонні коробки блокують світло, лише 2 кольори"}
  - {kind: other, url: "https://itch.io/jam/1-bit-jam-wow/rate/2224145", note: "сторінка джему: місця, коментарі про світло, скляні блоки й кнопки"}
  - {kind: other, url: "https://steamcommunity.com/app/3716870/reviews/?browsefilter=toprated&l=english", note: "відгуки: світло радіально, undo після смерті, варіанти рівнів, секретні рівні"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Prince+of+Darkness+Jr+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-4dir, keyboard-controls, push-object, impassable-cells, beam-tracing, environment-death, player-death, death-animation, button-toggle, undo-redo, restart-level, game-pause, sequential-levels, achievements-window, +shadow-walk, +shadow-casting, +light-source, +transparent-block, +breakable-window, +level-variants, +secret-area]
proposes: ["+cond:in_shadow", "+effect:recast_shadows", "+card:transparent-block", "+card:breakable-window", "+card:level-variants"]
author: opus
date: 2026-11-09
---

# Prince of Darkness Jr. — Sokoban для вампіра: світло вбиває, тінь від ящика — єдиний прохід

## Суть
Малий вампір-принц ходить замком, де «скватери» запалили старі газові лампи; ступити у світло — смерть. Гравець штовхає ящики й коробки, щоб вони відкидали тінь від ламп, і тінь стає безпечною стежкою; додатково — двері, вікна, які можна розбити, скляні блоки. Головна незвичність — світло рахується геометрично (радіально від лампи, з «витоками» крізь щілини), тож перешкода змінює всю мапу безпечних клітин одразу. Виросла з джему 1-Bit Game Jam 2023 (на екрані лише два кольори) у повну гру на 200+ рівнів.

## Поле і час
- Квадратна сітка кімнати, вид згори; один екран на рівень (?).
- Шари: підлога + стіни + рухомі блоки + лампи; поверх — **карта світла**: які клітини освітлені зараз (обчислюється з положень ламп і перешкод).
- Хід = крок принца (з можливим поштовхом); світ без вводу не змінюється (Steam: «Playable without Timed Input»). Після кожного зсуву перешкоди світло перераховується.
- Світло поширюється від лампи радіально й розходиться під «дикими» кутами (відгук jeromocles), просочується крізь малі щілини (коментар джему) — це променева геометрія, а не «рядок/стовпець» як у Light Up.
- Рівні згруповані у світи (номери на кшталт 4-10); палітра змінюється між світами шейдером (опис джему).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Принц (вампір) | player | 1 життя на спробу | рух 4 напрямки; штовхає блоки; гине, опинившись у світлі |
| Газова лампа | hazard | позиція джерела | освітлює клітини, до яких доходить промінь без перешкод |
| Освітлена клітина | zone | обчислюється | смертельна для принца; змінюється після кожного зсуву блока |
| Ящик (crate) | object | — | штовхається на 1; непрозорий — відкидає тінь |
| Картонна коробка | object | — | як ящик: штовхається, блокує світло (опис itch) |
| Скляний блок | object | прозорий (?) | штовхається; світло, імовірно, пропускає (?) |
| Вікно | static | ціле / розбите | «smash windows» — розбивається; що змінює для світла — (?) |
| Двері | gate | закриті / відчинені | відчиняються механізмом рівня (кнопкою під блоком?) (?) |
| Кнопка | switch | натиснута / ні | спрацьовує від гравця чи блока; у джем-версії могла «вбити» зміною світла |
| Стіна | static | — | непрохідна; блокує світло |
| Вихід | static | — | кінець рівня (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(prince, dir)`.
- КОЛИ `contact(prince, crate|box|glass)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `after(push)` → ТО `custom: «перерахувати світло від кожної лампи: промінь іде радіально до першої непрозорої перешкоди»`.
- КОЛИ `enter(prince, lit_cell)` → ТО `lose` (анімація смерті).
- КОЛИ `after(push)` → ЯКЩО `custom: «клітина з принцом після перерахунку стала освітленою»` → ТО `lose` (зсунув власну тінь).
- КОЛИ `contact(light_ray, glass)` → ТО `custom: «промінь іде далі»` (?).
- КОЛИ `contact(light_ray, crate|box|wall)` → ТО `custom: «промінь зупиняється, за перешкодою — тінь»`.
- КОЛИ `enter(prince|crate, button)` → ТО `set_state(door, open)` (?).
- КОЛИ `contact(prince, door)` → ЯКЩО `state(door, closed)` → ТО `block`.
- КОЛИ `contact(prince, window)` → ТО `set_cell(window, broken)`, `custom: «змінюється освітлення кімнати»` (?).
- КОЛИ `reach(prince, exit)` → ТО `win`, `next_level` (?).
- КОЛИ `died(prince)` → ТО `custom: «пауза ~1 с»`, далі `undo(1)` або `restart`.
- КОЛИ `input(undo)` → ТО `undo(1)`; КОЛИ `input(restart)` → ТО `restart` (за рестарт undo не сягає).
- Перемога: дійти до виходу, не ступивши у світло (?). · Поразка: принц у світлі → повтор/undo. · Рахунку нема.

## Керування і ввід
- WASD / стрілки — крок (з поштовхом); R — рестарт рівня; Esc — пауза (jam-версія на itch).
- Undo є (відгуки: «undo after dying»), клавіша — (?).
- Steam: «Keyboard Only Option»; підтримка контролера — питання у форумі (?).

## Вікна, меню, HUD
- `splash-screen` / титул (?).
- `main-menu`: Грати → `level-select` або мапа світів (?); налаштування; вихід.
- `game-screen`: кімната у двох кольорах; світло — однією з двох барв, тінь — іншою; HUD — номер рівня (?).
- `pause-menu` (Esc): продовжити, рестарт, вихід (?).
- `settings-window`: гучність (Custom Volume Controls), кольорові альтернативи (Color Alternatives).
- `achievements-window` (Steam, 15 досягнень, частина — за секретні рівні).
- Переходи: рівень пройдено → наступний; смерть → анімація → undo/рестарт.

## Фічі поза полем
- `levels-sequential` світами; 200+ рівнів; частина — **варіанти** попередніх кімнат з іншим набором деталей («less boxes, or more glass… or more walls»).
- `collectibles`-подібні **секретні рівні** (`+secret-area`), окремі досягнення за них; гравці скаржаться, що їх шукати — «guess work».
- `undo` + `restart-level`; undo не повертає стан до рестарту.
- `colorblind-palette` / Color Alternatives; `volume-sliders`; `cloud-save` (Steam Cloud).

## Варіації й родичі
- Jam-версія (2023, браузер, 4 світи (?)) → повна гра (2025, Pond Area, 200+ рівнів); у джемі — 6-те місце за геймплеєм із 542 робіт.
- Родичі: [sokoban](sokoban.md) — ядро; Felix the Reaper (thinky) — теж «ходи лише по тіні», але тінь змінює поворот сонця; Light Up (pencil-logic) — лампа світить рядком і стовпцем; лазерні ігри (Deflektor) — промінь із відбиттями.
- Осі варіацій:
  - **геометрія світла**: рядок/стовпець (Light Up) / радіальні промені з кутами (PoD Jr.) / паралельне «сонце» з напрямком (Felix);
  - **що робить світло**: вбиває гравця (PoD Jr.) / лише показує область (стелс) / заряджає механізм;
  - **прозорість перешкод**: непрозорий ящик / скло, що пропускає (?) / вікно, яке розбивається.

## Цікавинки для курсу
- Обчислення освітлення від точкового джерела на сітці (shadow casting / visibility polygon) з перерахунком після кожного поштовху — 🥈 (симетрія, кути, «щілини» між діагональними блоками).
- Перевірка «ступив у світло» і «тінь поїхала з-під ніг» як дві різні причини смерті — 📎.
- Прозорий блок: штовхається, але не відкидає тіні — 🌱 поверх освітлення.
- Undo, що переживає смерть (смерть — звичайний стан у стеку), але не рестарт — 📎.
- Розвʼязувач: BFS по станах «принц + блоки», а безпечність клітин — функція від блоків; кешувати карту світла — 🥇.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls`; `push-object` ↔ ящики/коробки/скло; `impassable-cells` ↔ стіни; `beam-tracing` ↔ промені від лампи до перешкоди; `environment-death` + `player-death` + `death-animation` ↔ смерть у світлі; `button-toggle` ↔ кнопки/двері (?); `undo-redo` + `restart-level`; `game-pause`; `sequential-levels`; `achievements-window`.
- **Нема** → пропозиції карток:
  - `+shadow-walk` (уже з Felix the Reaper) — ходити лише по тіні; тут світло вбиває.
  - `+shadow-casting` (уже з Felix) — тінь від обʼєктів; тут від точкових ламп, радіально.
  - `+light-source` (уже в корпусі) — лампа як джерело зони.
  - `+transparent-block` «Прозорий блок: штовхається, світло пропускає» · entities/legality · 🌱.
  - `+breakable-window` «Вікно, що розбивається дотиком і змінює освітлення» · entities/interact · 📎 (?).
  - `+level-variants` «Варіант рівня з іншим набором деталей» · levels/bank · 🌱.
  - `+secret-area` (уже в корпусі) — секретні рівні.

## Пропозиції до словників
- `+cond:in_shadow` (уже з Felix) — клітина не освітлена жодним джерелом; тут — умова виживання принца.
- `+effect:recast_shadows` (уже з Felix) — перерахувати карту світла після зсуву перешкоди.
- `+card:transparent-block`, `+card:breakable-window`, `+card:level-variants`.

## Джерела
- ⭐ [Steam: Prince of Darkness Jr.](https://store.steampowered.com/app/3716870/) — «can't step into the light», блоки кидають тіні й відчиняють двері, розбиті вікна, секрети, 200+ рівнів; реліз 31.10.2025, Pond Area; категорії (Keyboard Only, Color Alternatives, 15 досягнень).
- [pondarea.com](https://pondarea.com/) — «box-pushing, shadow-casting», «Vamps vs Lamps».
- [itch: jam-версія](https://elphyl.itch.io/princeofdarknessjr) — керування WASD/R/Esc, ящики й коробки блокують світло, два кольори, автори (elphyl, spatling), фікси «world 4».
- [1-Bit Jam: сторінка оцінки](https://itch.io/jam/1-bit-jam-wow/rate/2224145) — місця, коментарі: світло «тече» крізь щілини й розширюється біля стін, скляні блоки, переробка кнопок.
- [Steam-відгуки](https://steamcommunity.com/app/3716870/reviews/?browsefilter=toprated&l=english) — радіальне світло, undo після смерті й не після рестарту, варіанти рівнів, секретні рівні.
- YouTube: пошук «Prince of Darkness Jr gameplay».

## Непевне
- (?) Умова перемоги: вихід/двері кімнати — не бачив прямого опису; «open doors» може означати і вихід, і проміжні двері.
- (?) Скло: блоки є («introduction of glass blocks»), але чи пропускають світло — висновок з назви; PlayPile пише «розбите скло дає тимчасову безпечну зону» — не підтверджено.
- (?) Вікна: «smash windows» — є, але що відбувається (вікно пропускає денне світло? розбите стає тінню?) — не знайдено.
- (?) Кнопки: у джемі кнопка спрацьовувала до кінця кроку й могла вбити; чи вони відкривають двері й чи тиснуться блоком — не перевірено.
- (?) Клавіша undo, наявність мапи світів, лічильника ходів, підтримка контролера — не перевірено.
