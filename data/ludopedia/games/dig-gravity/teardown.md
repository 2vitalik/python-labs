---
title: Teardown
slug: teardown
aka: []
family: dig-gravity
also: []
klass: avatar
axes:
  field: free
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 2022
platforms: [PC (Windows; ранній доступ 2020), PS5, Xbox Series X/S (2023)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Teardown_(video_game)", best: true, note: "воксельні рівні, тривога → 60 с до машини втечі, інструменти, типи місій, режими Sandbox/Creative/Mayhem/Hunted/Fetch, мультиплеєр, моди"}
  - {kind: steam, url: "https://store.steampowered.com/app/1167630", note: "Steam (перевірено через appdetails): 40 місій кампанії, sandbox, до 12 гравців, Workshop, редактор"}
  - {kind: official, url: "https://teardowngame.com/modding/api.html", note: "Lua API: розмір вокселя 0,1 м, класи матеріалів soft/medium/hard у MakeHole, вибух 0,5–4, вогонь, відʼєднані частини"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Teardown+heist+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [destructible-blocks, explode-area, gravity-fall, time-out, reach-exit, collect-quota, round-currency, shop-between-levels, inventory-items, chase-player, player-death, save-game, level-select, in-game-editor, online-multiplayer, particles, +first-person-view, +fire-spread, +voxel-destruction, +material-hardness-tiers, +structural-detach, +alarm-countdown, +place-plank, +vehicle-drive, +mod-support, +challenge-modes]
proposes: ["+effect:spread", "+cond:material", "+role:material", "+feature:quicksave", "+card:material-hardness-tiers", "+card:structural-detach", "+card:alarm-countdown"]
author: opus
date: 2026-11-09
---

# Teardown — межовий випадок: руйнівний воксельний світ, де підготовку не обмежено, а після тривоги лишається 60 с

## Суть
Пограбування від першої особи в повністю руйнівному воксельному світі (Tuxedo Labs). Гравець без ліміту часу готує маршрут: пробиває стіни, кладе дошки-рампи, переганяє машини, підриває перешкоди; коли бере першу ціль, привʼязану до сигналізації, вмикається тривога — 60 с, щоб забрати решту обовʼязкових цілей і доїхати до машини втечі. **Межовий випадок для сімʼї:** «клітини» — лише воксельний матеріал (0,1 м), що вирізається й падає, а рух гравця, тіла й транспорт — вільна фізика (`field: free`). Тут — коротко, як межа поруч із сітковим копанням ([boulder-dash.md](boulder-dash.md), [noita.md](noita.md)).

## Поле і час
- Рівень — набір воксельних форм (shape) на тілах (body); один воксель за замовчуванням 0,1 м (`GetShapeSize` → scale 0.1). Тіла рухаються вільно, з rigid-body фізикою; воксельна сітка — лише всередині кожної форми.
- Кожен воксель має матеріал: колір, шорсткість, світіння, відбиття й фізичний тип. Класи міцності (API `MakeHole`): **soft** — скло, листя, ґрунт, дерево, тиньк, пластик; **medium** — бетон, цегла, слабкий метал; **hard** — твердий метал і тверда кладка.
- Відʼєднана від статики частина стає окремим тілом і падає; стиснення не моделюється, тож будівля може стояти на кількох вокселях.
- Real-time; камера від першої особи, у транспорті — від третьої.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | інструменти з лімітом застосувань | ходить, лазить, носить предмети, керує транспортом |
| Воксель матеріалу | terrain | клас soft / medium / hard | вирізається інструментом свого класу або вибухом |
| Ціль із сигналізацією | pickup | — | взяти / знищити → вмикається тривога |
| Цінність | pickup | гроші | взяти → гроші на апгрейди |
| Машина втечі | static | — | доїхати після тривоги = виконати місію |
| Пропановий балон | object | — | вибухає |
| Дошка | object | кількість, довжина | ставиться як рампа чи міст |
| Транспорт (авто, вантажівка, кран, екскаватор, човен) | object | — | керований; таранить і тягне |
| Охоронний робот | enemy | — | переслідує гравця (окремі місії) |
| Гелікоптер | enemy | — | помічає машину після 60 с; у частині місій атакує |
| Вогонь | hazard | — | поширюється займистим; у місіях з пожежною сигналізацією його треба гасити |
| Вода | terrain | — | перешкода й шлях для човна |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(fire, sledgehammer)` → ЯКЩО `custom: «матеріал цілі не твердіший за клас інструмента»` → ТО `custom: «вирізати діру у вокселях радіусом за класом матеріалу»`.
- КОЛИ `input(fire, blowtorch|shotgun|bomb|rocket)` → ТО `custom: «сильніші інструменти ріжуть міцніші матеріали»` (обмежена кількість застосувань).
- КОЛИ `custom: «група вокселів втратила звʼязок зі статичною основою»` → ТО `fall(group)` (стає окремим фізичним тілом).
- КОЛИ `custom: «вибух розміру 0,5–4»` → ТО `explode(sphere, size)` з радіусами за класами матеріалів, `custom: «відкидає тіла»`.
- КОЛИ `custom: «вогонь поруч із займистим вокселем»` → ТО `custom: «вогонь поширюється й палить матеріал»`.
- КОЛИ `input(use, extinguisher)` → ТО `custom: «гасить вогонь»`.
- КОЛИ `input(use, spraycan)` → ТО `paint(surface, color)` (мітка маршруту).
- КОЛИ `input(place, plank)` → ЯКЩО `has(player, plank)` → ТО `place(player, plank)`.
- КОЛИ `picked(player, alarm_target)` або `destroyed(alarm_target)` → ЯКЩО `not state(alarm, on)` → ТО `set_state(alarm, on)`, `timer(start, 60)`.
- КОЛИ `counter(alarm_timer, <=, 0)` → ЯКЩО `not state(player, escaped)` → ТО `lose` (гелікоптер помічає машину).
- КОЛИ `enter(player, getaway_vehicle)` → ЯКЩО `custom: «обовʼязкові цілі виконано»` → ТО `win`.
- КОЛИ `picked(player, valuable)` → ТО `currency(+value)`; гроші — на апгрейди інструментів (більше й довші дошки, сильніші бомби).
- КОЛИ `hp_zero(player)` (вибух, вогонь, падіння, атака гелікоптера) → ТО `lose`; що саме роблять роботи — (?).
- Перемога: обовʼязкові цілі й машина до кінця відліку (інші місії: знести будівлю до висоти, перевезти важке, втекти від роботів, загасити пожежі). · Поразка: відлік вичерпано або гравець загинув. · Рахунок: гроші за цінності; у Mayhem — кількість зруйнованих вокселів за 60 с.

## Керування і ввід
- Вид від першої особи: рух, стрибок, присід, огляд мишею; вибір інструмента, застосування; узяти/кинути предмет; сісти в транспорт.
- Швидке збереження й завантаження в будь-який момент (світ стискається RLE, тож сейв швидкий).
- PC: клавіатура й миша, повна підтримка геймпада (Steam).

## Вікна, меню, HUD
- `main-menu` (?): кампанія · Sandbox · Creative · виклики · мультиплеєр · моди · налаштування.
- `map-window` — хаб із місіями; `level-select` у Sandbox і викликах.
- `custom-window` — брифінг місії з цілями (`objective-text`).
- `game-screen`: обраний інструмент і запас, `timer-countdown` тривоги, цілі.
- `shop-window` (custom) — апгрейди інструментів за гроші між місіями.
- `end-screen` — результат місії; `pause-menu` із квіксейвом.
- `editor-window` — Creative (малювання вокселів) і редактор рівнів на PC.

## Фічі поза полем
- Кампанія з 40 місій через хаб; апгрейди інструментів за гроші; `+feature:quicksave`.
- `mode-sandbox` (усі інструменти, без цілей) · Creative (моделювання з вокселів, збереження обʼєктів) · `mode-time-attack`-виклики Mayhem / Hunted / Fetch на кожному відкритому рівні.
- `online-multiplayer` до 12 гравців: кооп-кампанія, sandbox, deathmatch, team deathmatch, capture the flag.
- `mod-support`: Lua-скрипти, рівні з MagicaVoxel, Steam Workshop (понад 6000 модів до вересня 2023), паки модів на консолях.

## Варіації й родичі
- У сімʼї: сіткове копання з падінням ([boulder-dash.md](boulder-dash.md), [dig-dug.md](dig-dug.md)) і пісочниці матеріалів ([the-powder-toy.md](the-powder-toy.md), [noita.md](noita.md)) — Teardown переносить «матеріал за клітинами» у 3D з вільними тілами.
- Родич за духом — [infiniminer.md](infiniminer.md) (вокселі й вибухи, але сітка світу фіксована).
- **Осі варіацій**: міцність — один клас / ієрархія (soft–medium–hard) / HP на клітину; що падає — нічого / клітина без опори / звʼязна група як тіло; час — без ліміту / ліміт на всю місію / ліміт лише після тривоги.

## Цікавинки для курсу
- Дві фази місії: необмежена підготовка + 60-секундний відлік після першої цілі — 🌱 (стан рівня й таймер, переносимо в будь-яку клітинну гру).
- Ієрархія міцності матеріалів і інструментів (soft/medium/hard) — 📎.
- Звʼязність: після руйнування знайти групи клітин без опори й скинути їх (flood fill по 3D-сітці) — 🥈.
- Поширення вогню займистими клітинами — 📎.

## Мапа на каталог
- Є: `destructible-blocks` · `explode-area` ↔ бомби, балони · `gravity-fall` ↔ відʼєднані частини · `time-out` ↔ 60 с · `reach-exit` ↔ машина втечі · `collect-quota` ↔ обовʼязкові цілі · `round-currency` + `shop-between-levels` ↔ гроші й апгрейди · `inventory-items` ↔ інструменти з лімітом · `chase-player` ↔ роботи · `player-death` · `save-game` ↔ квіксейв · `level-select` · `in-game-editor` ↔ Creative · `online-multiplayer` · `particles` ↔ дим, уламки.
- **Нема** → пропозиції карток:
  - `+material-hardness-tiers` «Класи міцності матеріалу проти класу інструмента» · entities/interact · 📎 · слот {tiers}.
  - `+structural-detach` «Група без опори відʼєднується й падає» · entities/move · 🥈 · слот {connectivity: 6|26}.
  - `+alarm-countdown` «Перша ціль запускає відлік до втечі» · game-logic/win · 🌱 · слот {seconds: 60}.
  - `+voxel-destruction`, `+place-plank`, `+vehicle-drive`, `+challenge-modes` — межові, для повноти; `+fire-spread`, `+first-person-view`, `+mod-support` — повтори.

## Пропозиції до словників
- `+effect:spread` — вогонь переходить на сусідній займистий матеріал (повтор).
- `+cond:material` — матеріал клітини належить класу (повтор); `+role:material` — воксель/клітина як матеріал без поведінки агента (повтор).
- `+feature:quicksave` — миттєве збереження/завантаження в будь-який момент.

## Джерела
- ⭐ [Wikipedia: Teardown](https://en.wikipedia.org/wiki/Teardown_(video_game)) — геймплей: вокселі й матеріали, тривога й 60 с, інструменти, дошки, балони, транспорт, типи місій, хаб, квіксейв, апгрейди, режими, мультиплеєр, моди; розробка (RLE-сейви, обмеження перешкод).
- [Steam: Teardown](https://store.steampowered.com/app/1167630) — опис (через `api/appdetails`): кампанія 40 місій, sandbox, до 12 гравців, Workshop, редактор.
- [Teardown Lua API](https://teardowngame.com/modding/api.html) — `MakeHole` (soft/medium/hard і списки матеріалів), `Explosion` (0,5–4), `SpawnFire`, `GetShapeSize` (0,1 м), `IsShapeDisconnected` / `IsStaticShapeDetached`.
- YouTube: пошук «Teardown heist gameplay».

## Непевне
- (?) Який інструмент який клас бере (кувалда — soft і medium? паяльна лампа — метал?) — у відкритих джерелах не перевірено.
- (?) Як саме визначається «ціль, привʼязана до сигналізації», і чи вмикають тривогу інші дії (розбите вікно, шум).
- (?) Чи підтримує мультиплеєр кампанію повністю — за Wikipedia так (кооп), деталі не відкривав.
- (?) HP гравця й шкода від падіння, вогню, вибухів, а також поведінка охоронних роботів — не перевірено.
- (?) Склад головного меню й вигляд брифінгу — з загального опису режимів, екранів не бачив.
