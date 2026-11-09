---
title: Gem Worlds
slug: gem-worlds
aka: []
family: dig-gravity
also: [roguelike]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: setup
  goal: state
year: 2023
platforms: [PC (Windows, macOS, Linux)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1858760/Gem_Worlds/", best: true, note: "опис: 50 згенерованих рівнів у 5 світах, 10+ умінь, міни/бурульки/кактуси, покроковість, режим безсмертя; є демо"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1858760&count=50&maxlength=0", note: "усі патчноути 2022–2023: одночасний хід, ключі й замок виходу, світлові кристали, стіни, що піднімаються, телепорти"}
  - {kind: other, url: "https://steamcommunity.com/stats/1858760/achievements", note: "11 досягнень: світи за назвами, молот, світло, інвентар 10+"}
  - {kind: other, url: "https://steamcommunity.com/app/1858760/reviews/?browsefilter=toprated&filterLanguage=all", note: "відгуки: удар-зіткнення, два телепорти, власний фаєрбол обпікає"}
  - {kind: other, url: "https://www.gamingonlinux.com/2023/01/inspired-by-boulder-dash-and-supaplex-gem-worlds-is-out-now/page=1/", note: "анонс релізу, список фіч"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Gem+Worlds+Deen+Games+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-4dir, gravity-fall, dig-terrain, push-object, item-pickup, key-and-door, reach-exit, explode-area, teleport, hp-damage, environment-death, projectile-shot, shoot-cooldown, inventory-items, dungeon-generation, sequential-levels, keyboard-controls, controls-remap, status-panel, +simultaneous-turns, +bump-attack, +skill-loadout, +choose-upgrade, +cooldown-ability, +light-radius, +popup-wall, +pattern-digger, +invincibility-toggle]
proposes: ["+trigger:smashed", "+effect:bump", "+effect:light", "+card:pattern-digger", "+card:invincibility-toggle"]
author: opus
date: 2026-11-09
---

# Gem Worlds — Boulder Dash як покроковий роглайк: каміння, міни й монстри ходять разом із тобою, а між рівнями — нові уміння

## Суть
Гравець риє землю, збирає самоцвіти, ухиляється від каміння й шукає вихід — правила Boulder Dash і Supaplex, але **покроково**: світ стоїть, доки ти не зробиш хід. Додано роглайк-шар: процедурні рівні, монстри з сердечками (бʼєш, врізаючись у них, або уміннями), скрині з предметами, світло й темрява. Кожні два рівні гравець обирає: прокачати одне з двох уже вивчених умінь або вивчити нове; після смерті можна пробувати з іншою комбінацією умінь.

## Поле і час
- Квадратна сітка, вигляд згори (?) щодо камери й розміру рівня — у джерелах нема.
- Хід = тік: **усі сутності, включно з гравцем, рухаються одночасно** (з v0.6.0), без quick-time; гравець може пропустити хід.
- 5 світів × 10 згенерованих рівнів; кожен світ генерує лише два типи рівнів; ключі й замок — на 5-му і 10-му рівнях світу.
- Видимість обмежена світлом: світлові кристали роблять світло яскравішим і довшим (стакаються), тож поле частково в темряві (?) щодо точної механіки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | сердечка; уміння, предмети | рух 4 напрямки; копає; штовхає камінь/міну; бʼє монстра, врізаючись |
| Земля | terrain | — | гравець проходить → порожньо; світлові зірки її «їдять» |
| Камінь | object | — | падає без опори; штовхається (навіть угору в телепорт); давить гравця |
| Самоцвіт | pickup | — | збирається, коли стаєш на клітину; «Gem Collector» — усі на рівні |
| Ключ | pickup | 1 або 3 на рівень | збирається як самоцвіт; відмикає вихід |
| Портал виходу | gate | замкнений / відкритий | зʼявляється не одразу після старту; вхід → наступний рівень |
| Міна | hazard | — | штовхається; вибухає площею, зона вибуху підсвічена |
| Скриня | container | — | дає предмет і показує, що саме |
| Світловий кристал | pickup | яскравість, тривалість у ходах | підсилює світло гравця; ефекти стакаються |
| Руйнована стіна | static | — | руйнується (фаєрбол — уже ні, з v0.3.1) |
| Стіна, що піднімається | gate | таймер скидання | після проходу гравця піднімається й блокує, за кілька ходів опускається |
| Телепорт | terrain | — | переносить; працює і для каміння |
| Світлова зірка | neutral | патерн руху | рухається за патерном і їсть землю |
| Монстри (3+ на світ) | enemy | сердечка (є «однасердечкові») | б'ють, коли поруч; кожен вид — своя тактика |
| Бджола | enemy | — | світ 4; не займає клітину з іншою бджолою чи каменем |
| Бурулька · кактус | hazard | — | пастки біомів (лід, пустеля) (?) щодо поведінки |
| Нана | neutral | крамниця | продає частину умінь за самоцвіти |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `cell(target, empty|dirt|gem|key)` → ТО `move(player, dir)`; земля → `set_cell(target, empty)`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(target, boulder|mine)` and `free(cell_behind)` → ТО `push(b)`; інакше `block`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(target, monster)` → ТО `damage(monster, 1)` (`custom: «удар-зіткнення, гравець лишається на місці»`).
- КОЛИ `input(skip)` → ТО `pass_turn`.
- КОЛИ `turn_end` → ТО `custom: «гравець, монстри й каміння роблять крок одночасно»`.
- КОЛИ `turn_end` → ЯКЩО `not supported(boulder)` → ТО `fall(boulder)`; з округлого — `roll(boulder)` (?).
- КОЛИ `custom: «smashed: камінь упав на гравця»` → ТО `damage(player, n)`.
- КОЛИ `contact(player, gem)` → ТО `pickup`, `counter(gems, +1)`.
- КОЛИ `contact(player, key)` → ТО `pickup`, `counter(keys, +1)`.
- КОЛИ `counter(keys, ==, need)` → ТО `set_state(exit, open)` — need = 1 або 3.
- КОЛИ `contact(player, exit)` → ЯКЩО `state(exit, open)` → ТО `next_level`.
- КОЛИ `contact(player, chest)` → ТО `give(player, item)`, `message(item)`.
- КОЛИ `input(item_slot)` → ЯКЩО `has(player, light_crystal)` → ТО `use`, `custom: «світло яскравіше й довше, стакається»`.
- КОЛИ `input(skill)` → ЯКЩО `custom: «cooldown минув»` → ТО ефект уміння, `set_state(skill, cooldown, n)`.
- Фаєрбол: КОЛИ `input(fireball)` → ТО `spawn(fireball)` недалеко вперед; КОЛИ `contact(fireball, a)` → ТО `damage(a, n)` — гравець теж обпікається.
- Молот: КОЛИ `input(hammer)` → ТО `damage(monster, n)` (?) щодо зони.
- Телепорт-уміння (два: «панічне» й звичайне): КОЛИ `input(teleport)` → ТО `teleport(player, where)` (?) щодо цілі.
- КОЛИ `custom: «міна в зоні вибуху»` → ТО `explode(area)`; КОЛИ `after(explode)` → ТО `damage(all_in_area, n)`.
- КОЛИ `leave(player, rising_wall)` → ТО `set_cell(wall)`; КОЛИ `timer(n)` → ТО `set_cell(floor)`.
- КОЛИ `enter(a, teleporter)` → ТО `teleport(a, pair)` — і для гравця, і для каменя.
- КОЛИ `turn_end` → ТО `custom: «світлова зірка — крок за патерном»`; ЯКЩО `cell(next, dirt)` → ТО `set_cell(next, empty)`.
- КОЛИ `adjacent(monster, player)` → ТО `damage(player, n)` (?) щодо точного моменту удару.
- КОЛИ `level_end` → ЯКЩО `custom: «парний рівень»` → ТО `choose(upgrade_A | upgrade_B | new_skill)`, `custom: «змінити екіпіровані уміння»`.
- КОЛИ `hp_zero(player)` → ЯКЩО `not mode(invincible)` → ТО `lose`; `mode(invincible)` → `custom: «безліч життів, без game over»`.
- Перемога: пройти 5-й світ. Поразка: сердечка скінчились. Рахунок: самоцвіти (валюта крамниці й досягнення).

## Керування і ввід
- Стрілки / d-pad — хід; пропуск ходу (на геймпаді — нижня кнопка A).
- Уміння — Z X C V (B), предмети — 1 2 3 4 (розкладка «під одну руку»); геймпад: тригери/бампери перемикають між предметами й уміннями.
- Будь-яка клавіша перепризначається (з v0.7.0); клавіатура й геймпад «усюди» (v1.2.0).

## Вікна, меню, HUD
- `game-screen`: поле; `hp-bar` (сердечка), лічильник самоцвітів (`coins`), ключі, `skill-bar` з сірими кнопками на cooldown, `inventory-bar` предметів (?) щодо розкладки.
- `upgrade-window` — між рівнями: два апгрейди або нове уміння + зміна екіпірованих.
- `shop-window` — крамниця Нани (уміння за самоцвіти); з паузи можна вийти в крамницю й повернутись на той самий рівень.
- `pause-menu` · `settings-window`: перепризначення клавіш, безсмертя, вимкнення градієнтного шейдера, великий шрифт.
- `end-screen` смерті → повтор з іншою комбінацією умінь.
- Переходи: game-screen → (вихід) → upgrade-window (кожен 2-й рівень) → game-screen наступного рівня.

## Фічі поза полем
- `assist-mode`: безсмертя вмикається будь-коли; кілька умінь «сильно спрощують гру».
- `levels-sequential` + `meta-progression` (уміння ростуть через забіг) (?) щодо того, чи вони лишаються після смерті.
- `achievements` (11, Steam) · `cloud-save` · `remap-controls` · `gamepad-support` · `one-hand-mode` · `font-scale`.
- Безкоштовне демо: один біом, 10 рівнів, 3 монстри, 5 умінь, міни.

## Варіації й родичі
- Корінь — [Boulder Dash](boulder-dash.md) і [Supaplex](supaplex.md) (автор називає обидва); найближчий покроковий родич — [Diamond Rush](diamond-rush.md)/[XOR](xor.md) (покрокове BD).
- Роглайк-сторона — як у [Spelunky](spelunky.md) (процедурні рівні) і класичних bump-роглайках.
- **Осі варіацій**: час — «real-time (BD) / покроково, світ чекає (Gem Worlds)»; бій — «лише уникати (BD) / удар-зіткнення + уміння»; прогресія — «квота самоцвітів / вибір апгрейдів кожні 2 рівні»; видимість — «усе видно / радіус світла».

## Цікавинки для курсу
- Одночасний хід усіх сутностей у покроковій BD: розвʼязання конфліктів, коли гравець і камінь цілять в одну клітину — 🥈.
- Вибір «прокачати одне з двох або взяти нове» між рівнями — 📎.
- Стіна, що піднімається за гравцем і скидається за N ходів — 🌱.
- Світловий радіус зі стакуванням тривалості й яскравості — 🥉.
- Сутність, що риє за патерном (світлова зірка), — 📎.
- Тумблер безсмертя як фіча доступності — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `gravity-fall` · `dig-terrain` · `push-object` (камінь, міна) · `item-pickup` · `key-and-door` (ключі → портал) · `reach-exit` · `explode-area` (міни) · `teleport` · `hp-damage` (сердечка) · `environment-death` (камінь, власний фаєрбол) · `projectile-shot` + `shoot-cooldown` (фаєрбол) · `inventory-items` · `dungeon-generation` · `sequential-levels` · `keyboard-controls` + `controls-remap` · `status-panel`.
- **Нема** → пропозиції карток:
  - Повтори з корпусу: `+simultaneous-turns`, `+bump-attack`, `+skill-loadout`, `+choose-upgrade`, `+cooldown-ability`, `+light-radius`, `+popup-wall` (тут зі скиданням за таймером).
  - `+pattern-digger` «Сутність їсть землю, рухаючись за патерном» · entities/move · 📎.
  - `+invincibility-toggle` «Безсмертя вмикається будь-коли» · interface/settings · 🌱.

## Пропозиції до словників
- `+trigger:smashed(a)` — на A впав камінь (повтор Earth Shaker, Emerald Mine).
- `+effect:bump(a, b)` — удар-зіткнення: A атакує B, лишаючись на місці (повтор корпусу).
- `+effect:light(a, +radius, dur)` — підсилити світло навколо A.
- Слова з наявних словників: `skill-bar` (cooldown), `upgrade-window`, `assist-mode` (безсмертя) — нових не треба.
- `+card:pattern-digger` · `+card:invincibility-toggle` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Gem Worlds](https://store.steampowered.com/app/1858760/Gem_Worlds/) — Deen Games, 16.01.2023; 50 рівнів у 5 світах, 10+ умінь (нове або апгрейд кожні 2 рівні), міни/бурульки/кактуси, покроковість, безсмертя.
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1858760&count=50&maxlength=0) — 17 патчноутів: одночасний хід (v0.6.0), ключі 1/3 і портал (v0.5.0), стіни, що піднімаються, світлові зірки, телепорти, нерф фаєрбола, крамниця Нани, клавіші Z X C V / 1 2 3 4.
- [Досягнення](https://steamcommunity.com/stats/1858760/achievements) — світи 1–5 (Spelunker, Bedouin, Snowman, Bee Hugger, Astronaut), Hammerhead, enlightened, Hoarder.
- [Відгуки Steam](https://steamcommunity.com/app/1858760/reviews/?browsefilter=toprated&filterLanguage=all) — удар-зіткнення, фаєрболи, два телепорти, «використати середовище на свою користь».
- [GamingOnLinux](https://www.gamingonlinux.com/2023/01/inspired-by-boulder-dash-and-supaplex-gem-worlds-is-out-now/page=1/) — анонс релізу.

## Непевне
- (?) Біоми за назвами досягнень: 1 — печера, 2 — пустеля (кактуси), 3 — лід (бурульки), 4 — бджоли, 5 — космос; відповідність пасток світам — здогад.
- (?) Поведінка бурульок (падають?) і кактусів (шкода при дотику?) — у джерелах лише назви.
- (?) Коли саме зʼявляється портал виходу і чи потрібна квота самоцвітів, крім ключів.
- (?) Чи скочується камінь з округлого (патч «камінь ковзав над щілиною» натякає на BD-скочування).
- (?) Точний момент удару монстра: патч v0.6.0 каже «бʼють, коли ти поруч, а потім відходиш».
- (?) Чи крамниця Нани лишилась у v1.0 поруч із вибором умінь кожні 2 рівні (патч v1.0 замінив «копити самоцвіти й купувати»).
- (?) Що руйнує руйновані стіни після нерфу фаєрбола (вибухи міни?); що дає молот, крім шкоди монстрам.
- (?) Смерть — рестарт рівня чи всього забігу; «повтор з іншою комбінацією умінь» — з опису Steam.
