---
title: Bad Hotel
slug: bad-hotel
aka: [Поганий готель]
family: tower-lanes
also: [build-sim]
klass: cursor
axes:
  field: free
  time: realtime
  opponent: none
  info: partial
  random: none
  goal: survive
year: 2012
platforms: [iOS, PC, Mac, Linux]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bad_Hotel", best: true, note: "кімнати прибудовуються до готелю: гармати, мортири, лікування, кімнати за гроші; музика генерується з побудованого"}
  - {kind: steam, url: "https://store.steampowered.com/app/231720/Bad_Hotel/", note: "«Build Hotel. Make Music. Stop Tadstock.»; скриншоти: блоки-кімнати, палітра з цінами, смуга рівня"}
  - {kind: official, url: "https://luckyframe.co.uk/works/bad-hotel/", note: "сторінка Lucky Frame: TD + процедурна музична іграшка"}
  - {kind: other, url: "https://gameramble.com/bad-hotel-pc-game-review.html", note: "огляд: кімната має торкатися сусідньої, без опори все падає, медичні кімнати, 25 рівнів у 5 зонах, поразка — знищено ядро"}
  - {kind: other, url: "https://www.pocketgamer.com/bad-hotel/review/", note: "огляд: нема сітки, мінні гармати, мортири з крижаними блоками, кожна кімната — шар саундтреку"}
  - {kind: other, url: "https://www.ibtimes.co.uk/bad-hotel-ios-game-review-374850", note: "огляд: 5 типів спалень з орендою, кожна кімната грає свою музичну фразу"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Bad+Hotel+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [tower-placement, enemy-waves, hp-damage, projectile-shot, status-effects, round-currency, sequential-levels, level-unlock, leaderboard, background-music, sound-effects, game-pause, +structural-support, +economy-buildings-income, +adjacency-buff, +procedural-music-from-build, +attach-to-structure, +omnidirectional-attack]
proposes: ["+role:room", "+role:core", "+ui:level-progress-bar", "+card:procedural-music-from-build", "+card:attach-to-structure"]
author: opus
date: 2026-11-09
---

# Bad Hotel — готель росте прибудованими кімнатами-вежами, а музика складається з того, що ти збудував

## Суть
Межовий TD без сітки-мапи: гравець захищає маленький готель від армії магната Tarnation Tadstock (чайки з бомбами, змії-камікадзе, щурі, єті, хмари, прибульці). Захист — це сама будівля: до ядра готелю прибудовуються квадратні кімнати, кожна нова має торкатися наявної. Частина кімнат стріляє, частина приносить гроші, частина лікує сусідів; знищена опора валить усе, що на ній трималось. Кожна кімната додає свою музичну фразу, тож саундтрек — звукова мапа стану готелю.

## Поле і час
- Вид збоку: ядро готелю (вестибюль із дверима) стоїть на землі; кімнати-блоки розміром «клітинка» чіпляються до боків і верху вже збудованого. Сітки як такої нема (Pocket Gamer: «there's no grid»), але блоки однакові й ставляться впритул — фактично граф суміжності блоків.
- Фізика: кімнати тримаються одна на одній; без опори — падають (скриншот: перекошені блоки, що валяться).
- Real-time: рівень — смуга з атаками й паузами до фінішного прапорця; вороги нападають з усіх боків, шляхів не видно заздалегідь.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ядро готелю (вестибюль) | static | HP | зруйноване — поразка |
| Звичайна кімната / спальня | resource | ціна, оренда (5 видів) | приносить гроші, не атакує |
| Кімната-гармата (gun turret) | tower | ціна | стріляє кулями по птахах |
| Мінна гармата | tower | ціна | стріляє мінами проти наземних ворогів |
| Мортира | tower | ціна | кидає крижані блоки — заморожує ворогів на кілька секунд |
| Медична кімната | tower | ціна | відновлює цілісність сусідніх кімнат |
| Вибухова кімната | tower | дорога | на пізніх рівнях — єдина «зброя» |
| Чайка / голуб із бомбою | enemy | — | пікірує й кидає бомбу на кімнати |
| Змія-камікадзе, щур, єті, плавець | enemy | — | наземні атаки на нижні кімнати |
| Хмара, прибульці, космічні кораблі | enemy | — | повітряні атаки |
| Tadstock на машині / істоті (краб, хмара, дирижабль) | boss | HP | бос у кінці кожної зони |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, room, spot)` → ЯКЩО `counter(money, >=, cost)` and `custom: «кімната торкається вже збудованої»` → ТО `place(room)`, `currency(-cost)`, `sound(room_loop)`.
- КОЛИ `timer(every)` → ТО `currency(+income)` за кожну грошову кімнату.
- КОЛИ `in_range(turret, enemy, r)` → ТО `spawn(projectile)`, `sound(note)`; КОЛИ `contact(projectile, enemy)` → ТО `damage(n)`.
- КОЛИ `contact(ice_block, enemy)` → ТО `freeze(enemy, n)`.
- КОЛИ `timer(every)` → ТО `heal(adjacent_rooms, n)` (медична кімната).
- КОЛИ `contact(enemy|bomb, room)` → ТО `damage(room, n)`, `custom: «тривога в музиці»`.
- КОЛИ `hp_zero(room)` → ТО `disappear`; КОЛИ `after(disappear)` → ЯКЩО `not supported(room_above)` → ТО `collapse` — усе, що трималось на ній, падає.
- КОЛИ `hp_zero(core)` → ТО `lose`.
- КОЛИ `custom: «смуга рівня дійшла до фінішу»` → ТО `win`, `next_level`; у кінці зони — бій із Tadstock (`hp_zero(boss)` → `win`).
- КОЛИ `level_start` → ЯКЩО `custom: «рівень без атакуючих кімнат»` → ТО `custom: «доступні лише грошові/лікувальні/вибухові»`.
- Перемога: дожити до кінця рівня й перемогти боса зони · Поразка: зруйновано ядро готелю · Рахунок: глобальні лідерборди (?).

## Керування і ввід
- Тач (iOS) / миша (PC): вибрати кімнату на палітрі внизу → тапнути місце біля готелю; кімната ставиться в найближче допустиме місце (огляди скаржаться, що «стрибає» від пальця).
- Кнопка паузи; апгрейдів кімнат на полі нема — нові типи відкриваються з рівнями.

## Вікна, меню, HUD
- `game-screen`: готель на тлі; угорі — `pause-button` і `+ui:level-progress-bar` (сегменти атак і пауз, маркер Tadstock, фінішний прапорець); під нею — друга смуга (HP боса або ядра?) (?); праворуч — гроші; унизу — палітра 4–5 кімнат із цінами (закриті — тьмяні).
- `level-select` / мапа зон: 5 зон × 5 рівнів (?); `tutorial-window` — коротке навчання; `leaderboard`; `achievements-window` (Steam).
- `end-screen` (Game Over / рівень пройдено); `dialogue-window` — репліки Tadstock.

## Фічі поза полем
- `levels-sequential` 25 рівнів у 5 зонах із босом у кінці кожної; `level-unlock`.
- Генеративна музика: кожен тип кімнати — свій луп, висота й місце впливають на ноти, постріли додають ноти, пошкодження — тривоги й «плоский» трек; стилі від beach chillout до country banjo techno.
- `leaderboard-online`, `achievements`, `cloud-save`, Steam-картки.

## Варіації й родичі
- Сітковий родич — [plants-vs-zombies](plants-vs-zombies.md) (грошові й бойові «вежі» в одній сітці) і [thronefall](thronefall.md) (доходи від уцілілих будівель); фізична опора блоків — як у будівельних іграх сімʼї `build-sim`.
- **Осі варіацій**: місце вежі — сітка / слот / прибудова до структури · економіка — від вбивств / від будівель · звук — супровід / наслідок побудованого.

## Цікавинки для курсу
- Прибудова лише впритул до наявного + перевірка опори й каскадне падіння незакріпленого — 🥉 (звʼязність графа блоків після видалення).
- Генеративна музика: кожна сутність — луп, позиція → висота ноти — 🥈.
- Медична кімната лікує сусідів — 🌱.
- Баланс «грошова кімната vs гармата» на одних і тих самих клітинках — 🌱.

## Мапа на каталог
- Є: `tower-placement` ↔ кімнати-вежі · `enemy-waves` · `hp-damage` ↔ цілісність кімнат · `projectile-shot` · `status-effects` ↔ заморозка · `round-currency` · `sequential-levels` · `level-unlock` · `leaderboard` · `background-music` + `sound-effects` ↔ генеративний саундтрек · `game-pause`.
- **Нема** → пропозиції карток:
  - `+attach-to-structure` «Нова сутність ставиться лише впритул до наявної структури» · entities/legality · 📎.
  - `+procedural-music-from-build` «Музика з побудованого: сутність = луп, позиція = нота» · interface/sound · 🥈.
  - `+structural-support` (вже в корпусі) — падіння без опори; `+economy-buildings-income`; `+adjacency-buff` ↔ лікування сусідів; `+omnidirectional-attack` «Вороги з усіх боків без видимого шляху» · 🌱.

## Пропозиції до словників
- `+role:room` — кімната-блок готелю (і вежа, і будівля); `+role:core` — ядро, втрата якого = поразка.
- `+ui:level-progress-bar` — смуга рівня з сегментами атак і маркером ворога.
- `+card:procedural-music-from-build`, `+card:attach-to-structure`.

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Bad_Hotel) — прибудова кімнат, типи (гармати, мортири, лікування, кімнати за гроші), вороги Tadstock, музика з побудованого, Lucky Frame, дати.
- [Steam](https://store.steampowered.com/app/231720/Bad_Hotel/) — опис, лідерборди, нагороди (BAFTA Scotland 2012, фіналіст IGF 2013); скриншоти HUD і палітри.
- [GAMERamble: огляд](https://gameramble.com/bad-hotel-pc-game-review.html) — правило «кімната торкається сусідньої», обвал без опори, медичні кімнати, заморожувальні турелі, вибухові кімнати, 25 рівнів / 5 зон, бос Tadstock, поразка — ядро.
- [Pocket Gamer: огляд](https://www.pocketgamer.com/bad-hotel/review/) — «no grid», мінні гармати, мортири з льодом, голуби з бомбами, музика й пошкодження.
- [IBTimes: огляд](https://www.ibtimes.co.uk/bad-hotel-ios-game-review-374850) — 5 видів спалень з орендою, кожна кімната — своя музична фраза, 5 світів по 5 рівнів.

## Непевне
- (?) Чи блоки прилипають до прихованої сітки (на скриншотах вони майже вирівняні) чи стоять вільно.
- (?) Чи можна продати/переставити кімнату; звідки точно береться дохід (таймер чи оренда за гостей).
- (?) Що показує друга смуга під смугою рівня (HP боса чи ядра).
- (?) Лідерборди — за що саме рахуються очки.
