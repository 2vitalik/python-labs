---
title: Shadow Labyrinth
slug: shadow-labyrinth
aka: [Шедоу Лабіринт, Swordsman No. 8, Pac-Man metroidvania]
family: maze-arcade
also: [grid-platformer]
klass: hybrid
axes:
  field: free
  time: realtime
  opponent: ai
  info: hidden
  random: none
  goal: state
year: 2025
platforms: [PS5, Xbox Series X/S, Switch, Switch 2, PC (Steam)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Shadow_Labyrinth", best: true, note: "огляд: PUCK-злиття (стіни й стелі), GAIA-мех, замкнені лабіринти зі сплячими привидами, платформи, дата"}
  - {kind: steam, url: "https://store.steampowered.com/app/1859430/Shadow_Labyrinth/", note: "опис, теги Metroidvania / Souls-like, досягнення, Steam Cloud"}
  - {kind: other, url: "https://www.vice.com/en/article/shadow-labyrinth-is-an-incredible-metroidvania-that-cleverly-reinvents-pac-man-review", note: "огляд: рейки → PUCK, підбирання на рейках = досвід, автохід вимикається, метр GAIA від поїдання"}
  - {kind: other, url: "https://www.thesixthaxis.com/2025/07/21/shadow-labyrinth-review/", note: "огляд: лабіринти на час, ORA на точках збереження, перки, чекпоінти"}
  - {kind: other, url: "https://gamingbolt.com/shadow-labyrinth-review-a-complete-package", note: "огляд: ORA не губиться при смерті, Miku Sol, Nano ER, швидкий перехід за предмет"}
  - {kind: other, url: "https://noobfeed.com/reviews/shadow-labyrinth-review", note: "огляд: D-Line з автоходом, Devour лише на поваленому ворогові, крафт перків PUCK"}
  - {kind: official, url: "https://www.bandainamcoent.com/news/shadow-labyrinth-maze-reveal-trailer", note: "трейлер лабіринтових секцій, бос G-HOST Bug"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=shadow+labyrinth+maze+gameplay", note: "пошук; лабіринтові секції"}
stage: v1
coverage: 50
mechanics: [move-auto, move-4dir, chase-player, temporary-modes, item-pickup, collect-all, hp-damage, checkpoint, save-progress, shop-catalog, round-currency, unit-xp-skills, world-map, map-window, time-out, inventory-items, achievements-window, +rail-mode-switch, +devour-downed-enemy, +meter-transform, +maze-portal-challenge, +currency-kept-on-death, +fast-travel-item, +sleeping-enemy]
proposes: ["+trigger:enter_rail", "+effect:devour", "+card:rail-mode-switch", "+card:devour-downed-enemy", "+card:meter-transform", "+card:maze-portal-challenge", "+card:fast-travel-item", "+feature:fast-travel", "+window:rest-point"]
author: opus
date: 2026-11-09
---

# Shadow Labyrinth — Pac-Man як метроїдванія: мечник у вільному 2D, рейки D-Line перетворюють його на PUCK, а портали ведуть у класичні лабіринти

## Суть
Гібрид двох класів: основна гра — 2D-метроїдванія з вільною фізикою (мечник No. 8 бʼється, стрибає, досліджує), а всередині неї є дві «пекменові» вставки. Перша — світні рейки D-Line: торкнувся — став маленьким PUCK, що їде лінією по підлозі, стінах і стелі й збирає підбирання. Друга — замкнені лабіринти за порталами: класичний Pac-Man-раунд на час (точки, підсилення, привиди), що закінчується босом. Повалених ворогів «поїдають», і це живить перетворення на гігантського меха GAIA.

## Поле і час
- Основне поле — вільні координати 2D-платформера, великий звʼязний світ, частина проходів відкривається пізніше (класична метроїдванія).
- D-Line — граф ліній, вбудований у вільне поле: рух по лінії автоматичний (вмикається/вимикається), зі стрибками між лініями.
- Лабіринт-портал — окрема клітинна арена в дусі Pac-Man Championship Edition; поділена на етапи, наприкінці — бос; час обмежений.
- Real-time скрізь.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мечник No. 8 | player | HP, енергія, ESP-шкала | меч (3 удари), ESP-постріл, парирування, щит, перекат |
| PUCK / Mini-PUCK (на D-Line) | player | — | їде рейкою, по стінах і стелі; обертовий удар-лезо; стрибає між рейками |
| GAIA | player | метр | гігантський мех на обмежений час; проти сильних ворогів і босів |
| Рейка D-Line | terrain | — | дотик перетворює мечника на PUCK |
| Підбирання на рейці | pickup | — | дає досвід для прокачки навичок |
| Ворог-монстр | enemy | HP | має анімації атаки, які треба вчити |
| Повалений ворог | object | швидко зникає | можна поглинути (Devour) |
| Бос | boss | фази | у кімнаті боса; польові боси (?) |
| Портал лабіринту | static | — | переносить у лабіринт (статуї-надгробки (?)) |
| Точка (у лабіринті) | pickup | — | зʼїсти всі — умова етапу |
| Підсилення (у лабіринті) | pickup | — | привиди стають вразливими |
| Привид (у лабіринті) | enemy | сплячий / мисливець | треба зʼїсти потрібну кількість |
| Miku Sol (точка відпочинку) | static | — | відновлює HP і лікування, ворогів відроджує |
| Малий чекпоінт | static | — | зберігає прогрес, вузол швидкого переходу (?) |
| Торговець | neutral | — | продає перки, ключові предмети, предмет швидкого переходу |
| Nano ER | pickup | обмежено | лікування |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `contact(swordsman, d_line)` → ТО `transform(puck)`, `custom: «рух прикріплено до рейки»` (`+trigger:enter_rail`).
- КОЛИ `tick` → ЯКЩО `state(puck, auto)` → ТО `move(puck, along_rail)`; автохід можна вимкнути й обирати точку стрибка.
- КОЛИ `input(jump)` → ЯКЩО `state(puck, on_rail)` → ТО `custom: «стрибок на іншу рейку в напрямку стіка»`.
- КОЛИ `contact(puck, rail_pickup)` → ТО `pickup`, `counter(xp, +1)`.
- КОЛИ `input(attack)` → ЯКЩО `state(player, puck)` → ТО `custom: «вийти з рейки, мечник атакує»`.
- КОЛИ `input(switch)` на рейковій ділянці → ТО `timer(start)`; КОЛИ `timer(end)` → ЯКЩО `custom: «PUCK ще не біля дверей»` → ТО `custom: «двері зачиняються»`.
- КОЛИ `hp_zero(enemy)` → ТО `transform(downed_enemy)`; КОЛИ `timer(fade)` → ТО `disappear_a`.
- КОЛИ `input(devour)` → ЯКЩО `in_range(player, downed_enemy, 0) and has(player, energy)` → ТО `disappear_b`, `give(player, material)`, `counter(gaia_meter, +n)` (`+effect:devour`).
- КОЛИ `counter(gaia_meter, ==, full)` → ТО `custom: «можна викликати GAIA»`; КОЛИ `input(gaia)` → ТО `transform(gaia)`, `set_state(player, gaia, duration)`.
- КОЛИ `contact(player, maze_portal)` → ТО `teleport`, `custom: «старт лабіринту-арени»`.
- Лабіринт: КОЛИ `contact(puck, dot)` → ТО `disappear_b`; КОЛИ `contact(puck, power_pellet)` → ТО `set_state(ghosts, vulnerable)`.
- Лабіринт: КОЛИ `contact(puck, ghost)` → ЯКЩО `state(ghost, vulnerable)` → ТО `disappear_b`, `counter(eaten, +1)`; інакше `lives(-1)` (?).
- Лабіринт: КОЛИ `all_gone(dot) and counter(eaten, >=, quota)` → ТО `custom: «наступний етап лабіринту з новими механіками»`; останній етап → бос.
- Лабіринт: КОЛИ `timer(limit)` → ТО `lose` спроби лабіринту.
- КОЛИ `hp_zero(player)` → ТО `respawn(player, last_checkpoint)`; ORA лишається (`+card:currency-kept-on-death`).
- КОЛИ `contact(player, miku_sol)` → ТО `heal(player, full)`, `custom: «поповнити лікування»`, `respawn(enemies)`.
- КОЛИ `input(buy)` → ЯКЩО `has(player, ora)` → ТО `take(player, ora)`, `give(player, item)`; перки потім екіпуються на точці збереження.
- КОЛИ `input(fast_travel)` → ЯКЩО `has(player, travel_item)` → ТО `teleport(save_point)` (`+feature:fast-travel`).
- Перемога: пройти сюжет і босів · Поразка: лише відкат на чекпоінт · Рахунок: — (прогрес — навички, перки, відкрита мапа).

## Керування і ввід
- Геймпад/клавіатура: рух, стрибок, удар (серія з 3), ESP-постріл, перекат-ухилення, парирування, щит, Devour, виклик GAIA.
- На D-Line — лівий стік задає напрямок стрибка з рейки; огляди скаржаться на неточність стрибків.
- Режим автоходу на рейці перемикається.

## Вікна, меню, HUD
- `main-menu` → нова гра / продовжити → `game-screen`.
- `game-screen`: HUD — `hp-bar`, `energy-bar`, ESP-шкала, метр GAIA, лікування Nano ER (?).
- `map-window` — мапа світу (?: деталі не описано в джерелах).
- `+window:rest-point` — меню точки збереження: прокачка навичок за ORA, екіпірування перків, швидкий перехід.
- `shop-window` — торговці перками й предметами.
- `achievements-window` — Steam-досягнення.
- `pause-menu`, `settings-window`.

## Фічі поза полем
- `save-progress` на точках відпочинку; `checkpoint` (Miku Sol і малі чекпоінти); Steam Cloud.
- Прогресія: досвід із рейок → навички; ORA → сила меча, ESP-шкала, ключові предмети; матеріали Devour → перки PUCK.
- `fast-travel` — між точками збереження; з будь-якого місця — після купівлі предмета (джерела розходяться).
- Explorer Mode (пізніше оновлення, ймовірно легша складність) (?).

## Варіації й родичі
- `pac-man` — джерело лабіринту й привидів; `pac-man-championship-edition` — сплячі привиди і поетапні арени, на які схожі лабіринти-портали.
- Pac-Man 99, Pac-Man Mega Tunnel Battle — інші сучасні переосмислення (див. `pac-man-battle-royale`).
- Метроїдванії (Hollow Knight, Metroid) — родина основної гри; поза корпусом.
- **Осі варіацій:** Pac-Man як режим (вставка-рейка / окремий лабіринт / цілий жанр) · рух по рейці: авто / ручний · «поїдання» як ресурс: очки (класика) / досвід і метр перетворення.

## Цікавинки для курсу
- Перемикання режиму руху: вільний аватар ↔ аватар на графі ліній при дотику — 🥉: дві моделі руху з переходами.
- Лабіринт-портал: клітинна міні-гра всередині іншої гри зі своїм таймером і поверненням — 📎.
- Devour → метр → тимчасове перетворення на мех — 🌱: ресурс з убитих ворогів, що вмикає стан.
- Валюта не губиться при смерті, але ворогів відроджує відпочинок — 🌱: явна політика смерті.
- Етапи лабіринту з умовою «усі точки + N привидів» — 📎.

## Мапа на каталог
- Є: `move-auto` (рейка) · `move-4dir` (лабіринт) · `chase-player` · `temporary-modes` (вразливі привиди, GAIA) · `item-pickup` · `collect-all` (точки) · `hp-damage` · `checkpoint` · `save-progress` · `shop-catalog` · `round-currency` (ORA) · `unit-xp-skills` · `world-map`, `map-window` · `time-out` (лабіринт) · `inventory-items` · `achievements-window` · `+sleeping-enemy` (з `pac-man-championship-edition`).
- **Нема** → пропозиції карток:
  - `+rail-mode-switch` «Дотик до рейки перемикає модель руху» · entities/move · 🥉.
  - `+devour-downed-enemy` «Поглинути поваленого ворога за ресурс» · entities/interact · 🌱 · слот {fade_time}.
  - `+meter-transform` «Шкала → тимчасове перетворення» · entities/state · 🌱 · слот {duration}.
  - `+maze-portal-challenge` «Міні-гра-лабіринт за порталом» · levels/progression · 📎.
  - `+currency-kept-on-death` «Валюта не губиться при смерті» · game-logic/economy · 🌱.
  - `+fast-travel-item` «Швидкий перехід за куплений предмет» · levels/progression · 📎.

## Пропозиції до словників
- `+trigger:enter_rail` — сутність стала на лінію-рейку й перейшла на рух графом (Shadow Labyrinth D-Line).
- `+effect:devour` — поглинути повалену сутність, отримавши ресурс (відмінне від `pickup`: ціль — ворог у стані «повалений»).
- `+feature:fast-travel` — перехід між відкритими точками мапи.
- `+window:rest-point` — меню точки відпочинку (прокачка, перки, перехід).
- `+card:rail-mode-switch`, `+card:devour-downed-enemy`, `+card:meter-transform`, `+card:maze-portal-challenge`, `+card:fast-travel-item` — див. «Мапу на каталог».

## Джерела
- ⭐ [Wikipedia: Shadow Labyrinth](https://en.wikipedia.org/wiki/Shadow_Labyrinth) — No. 8, PUCK по стінах і стелях, GAIA, замкнені лабіринти зі сплячими привидами як у CE 2, платформи, 18.07.2025.
- [Steam](https://store.steampowered.com/app/1859430/Shadow_Labyrinth/) — опис, Bandai Namco Studios, 17.07.2025, досягнення, Cloud.
- [VICE](https://www.vice.com/en/article/shadow-labyrinth-is-an-incredible-metroidvania-that-cleverly-reinvents-pac-man-review) — рейки, досвід з підбирань, автохід, бій, метр GAIA, HP-каністри.
- [TheSixthAxis](https://www.thesixthaxis.com/2025/07/21/shadow-labyrinth-review/) — лабіринти на час, ORA, перки, чекпоінти.
- [GamingBolt](https://gamingbolt.com/shadow-labyrinth-review-a-complete-package) — ORA, Miku Sol, Nano ER, швидкий перехід, смерть.
- [NoobFeed](https://noobfeed.com/reviews/shadow-labyrinth-review) — D-Line, Devour, перки PUCK.
- [Bandai Namco: maze reveal](https://www.bandainamcoent.com/news/shadow-labyrinth-maze-reveal-trailer) — лабіринти, бос G-HOST Bug.

## Непевне
- (?) Будова лабіринту-порталу — з пошукових виписок оглядів (gamerguides, game8), сторінок не відкривав: етапи, «точки + підсилення → привиди вразливі», «усі точки + потрібна кількість привидів», бос наприкінці; чи є життя в лабіринті.
- (?) Вхід у лабіринт через статуї-надгробки — лише з пошукової виписки.
- (?) Одне джерело називає підсилення в лабіринті «GAIA» — можливо, плутанина з мехом.
- (?) Швидкий перехід: TheSixthAxis — лише між точками збереження; GamingBolt/NoobFeed — з будь-якого місця за куплений предмет.
- (?) «Польові боси відроджуються після кількох смертей гравця» (GamingBolt) — не перевірено.
- (?) Explorer Mode — бачив лише назву в новинах Bandai Namco.
- (?) Склад HUD і вигляд мапи — не описано в джерелах.
