---
title: Diamond Rush
slug: diamond-rush
aka: []
family: dig-gravity
also: [push-slide]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: partial
  random: none
  goal: collect
year: 2006
platforms: [J2ME, BlackBerry, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Diamond_Rush", best: true, note: "огляд: 3 світи, 40 стадій, червоні/фіолетові діаманти, крамниця, чекпоінт-коло, предмети, боси"}
  - {kind: other, url: "https://www.pocketgamer.com/diamond-rush/review/", note: "огляд Pocket Gamer: падаючі камені, штовхання, загибель → початок кімнати, одна фіксована розвʼязка"}
  - {kind: wiki, url: "https://ru.wikipedia.org/wiki/Diamond_Rush", note: "рос. Вікі: срібні й золоті ключі в скринях, вороги (змії, павуки, росомахи, черепахи, тубільці)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Diamond+Rush+Gameloft+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, push-object, gravity-fall, dig-terrain, item-pickup, key-and-door, touch-death, environment-death, enemy-patrol, checkpoint, respawn, collect-quota, inventory-items, shop-window, hp-damage, player-camera, sequential-levels, world-map, +crush-by-falling, +two-currency-gems, +recall-to-checkpoint, +perfect-stage-life, +chest-container, +boss-stage]
proposes: ["+trigger:landed", "+effect:recall", "+ui:diamond-quota", "+feature:perfect-bonus", "+card:two-currency-gems", "+card:recall-to-checkpoint", "+card:perfect-stage-life"]
author: opus
date: 2026-11-09
---

# Diamond Rush — мобільний Boulder Dash-пригодник: каміння падає, червоні діаманти відмикають світи, фіолетові — купують здоровʼя

## Суть
Дослідник проходить кімнати-головоломки трьох світів (Ангкор-Ват, Баварія, Тибет): прокопується, штовхає камені, ухиляється від падаючих брил і ворогів, відкриває скрині. **Дві валюти**: червоні діаманти — квота, що відмикає двері в наступний світ, фіолетові — гроші крамниці, де купують збільшення смуги здоровʼя. Чекпоінт-коло можна «викликати» з будь-якого місця ціною життя. Кожна кімната має одну задуману розвʼязку — гра ближча до Boulder Dash-пазлу, ніж до аркади.

## Поле і час
- Квадратна сітка, вид збоку з гравітацією для каменів; поле більше за екран — камера за гравцем (`info: partial`), секретні кімнати.
- Світ = низка стадій (усього 40) з підкімнатами; останню стадію кожного світу закінчує бос.
- Real-time: камені падають і вороги ходять незалежно від гравця; рух гравця покроковий по клітинах (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Дослідник | player | смуга HP, життя | 4 напрямки; копає/проходить землю, штовхає камінь убік, підбирає предмети |
| Земля / зарості | terrain | — | прибирається, коли гравець проходить (?) |
| Стіна | static | — | непрохідна |
| Камінь | object | — | падає, якщо під ним порожньо; падаючий камінь розчавлює; штовхається вбік у вільну клітину |
| Червоний діамант | pickup | — | рахується до квоти дверей світу |
| Фіолетовий діамант | pickup | — | валюта крамниці |
| Скриня | container | вміст | червоний/фіолетовий діамант, життя, срібний чи золотий ключ |
| Срібний / золотий ключ | pickup | — | відмикає відповідні двері (?) |
| Двері | gate | вид ключа | відчиняються ключем |
| Двері світу | gate | квота червоних | відчиняються, коли зібрано потрібну кількість |
| Чекпоінт-коло | switch | — | ставши на нього, активуєш точку відновлення |
| Змія, павук, росомаха, черепаха, тубільці | enemy | — | ходять за передбачуваним патерном (?); шкодять при дотику |
| Вогняна пастка, гігантські списи | hazard | — | шкодять при контакті / за циклом (?) |
| Молот, компас, гак-кішка | pickup | — | інструменти, що відкривають нові дії в міру гри (функції — (?)) |
| Бос світу | boss | — | на останній стадії кожного світу |
| Крамниця | static | — | обмін фіолетових діамантів на збільшення HP |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, dir)` → ЯКЩО `free(target)` or `cell(target, dirt)` → ТО `move(player, dir)`; земля → `set_cell(empty)`.
- КОЛИ `input(move, left|right)` → ЯКЩО `occupied(target, boulder)` and `free(cell_behind)` → ТО `push(boulder)`; інакше `block`.
- КОЛИ `tick` → ЯКЩО `not supported(boulder)` → ТО `fall(boulder)`.
- КОЛИ `contact(falling_boulder, player)` → ТО `custom: «розчавлено»` → `lives(−1)`, `respawn(player, room_start)`.
- КОЛИ `contact(enemy|hazard, player)` → ТО `damage(player, n)`; КОЛИ `hp_zero(player)` → ТО `lives(−1)`, `respawn(player, checkpoint)`.
- КОЛИ `contact(player, chest)` → ТО `reveal(contents)` → `pickup(diamond | life | key)`.
- КОЛИ `picked(player, red_diamond)` → ТО `counter(red, +1)`; `picked(player, purple_diamond)` → `currency(+1)`.
- КОЛИ `contact(player, door)` → ЯКЩО `has(player, key)` → ТО `take(player, key)`, `disappear(door)`; інакше `block`.
- КОЛИ `contact(player, world_door)` → ЯКЩО `counter(red, >=, quota)` → ТО `next_level` (наступний світ); інакше `block`.
- КОЛИ `enter(player, checkpoint_circle)` → ТО `checkpoint`.
- КОЛИ `input(recall)` → ТО `lives(−1)`, `teleport(player, checkpoint)` — у будь-який час.
- КОЛИ `input(buy, health)` → ЯКЩО `has(player, purple, price)` → ТО `currency(−price)`, `custom: «смуга HP довшає»`.
- КОЛИ `level_end` → ЯКЩО `custom: «зібрано всі червоні й фіолетові, без рестарту і без ушкоджень»` → ТО `lives(+1)`.
- КОЛИ `destroyed(boss)` → ТО `next_level`; після трьох світів — `win`.
- Перемога: пройти три світи й босів. Поразка: закінчились життя (?). Рахунок: діаманти обох кольорів.

## Керування і ввід
- Телефонна клавіатура/джойстик J2ME: 4 напрямки (2/4/6/8 або D-pad), окрема клавіша — повернутись до чекпоінта (ціною життя), клавіша дії для предметів (?).
- Пізніші перевидання — тач (Android, Gameloft Classics) (?).

## Вікна, меню, HUD
- `splash-screen` → `main-menu` (Грати / Продовжити / Довідка / Налаштування звуку) (?).
- `world-map`/`map-window`: вибір стадії світу (?).
- `game-screen`: кімната; HUD — `hp-bar`, `lives`, лічильники червоних і фіолетових діамантів, інструменти (?).
- `shop-window`: покупка розширення HP за фіолетові.
- `end-screen` стадії: зібране, бонусне життя за ідеальне проходження (?).

## Фічі поза полем
- `levels-sequential` з квотою червоних на двері світу; секретні рівні й скрині з життями.
- `checkpoint` + «виклик» чекпоінта за життя; `autosave` прогресу між стадіями (?).
- Перевидання: Gameloft Classics Arcade (2017), Gameloft Classics: 20 Years (2020).

## Варіації й родичі
- Натхнення — [boulder-dash.md](boulder-dash.md) (камінь падає, розчавлює, штовхається вбік); родичі: [repton.md](repton.md), [emerald-mine.md](emerald-mine.md), [rocks-n-diamonds.md](rocks-n-diamonds.md); пригодницька обгортка — як [crystal-mines-ii.md](crystal-mines-ii.md).
- **Осі варіацій**: діаманти — «одна квота / дві валюти (квота + крамниця)»; смерть — «кінець рівня / початок кімнати / чекпоінт»; чекпоінт — «лише після смерті / виклик будь-коли за життя».

## Цікавинки для курсу
- Дві валюти з одного предмета (колір → квота дверей або гроші крамниці) — 🌱.
- Чекпоінт, до якого можна повернутись будь-коли за ціну життя (ручний «undo-рестарт» з вартістю) — 📎.
- Бонусне життя за «ідеальну» стадію: усі діаманти + без рестарту + без ушкоджень — 📎 (стан-лічильник через усю стадію).
- Скриня з випадковим/заданим вмістом як `container` → `reveal` → `pickup` — 🌱.
- Boulder Dash-фізика каменя (падіння + штовхання вбік + розчавлювання) — 🥉.

## Мапа на каталог
- Є: `move-4dir` · `push-object` · `gravity-fall` · `dig-terrain` · `item-pickup` · `key-and-door` · `touch-death` · `environment-death` · `enemy-patrol` · `checkpoint` · `respawn` · `collect-quota` ↔ червоні на двері · `inventory-items` ↔ молот/гак · `shop-window` · `hp-damage` · `player-camera` · `sequential-levels` · `world-map` (?).
- **Нема** → пропозиції карток:
  - `+two-currency-gems` «Два кольори збираного: квота і валюта» · game-logic/economy · 🌱.
  - `+recall-to-checkpoint` «Повернення до чекпоінта будь-коли за життя» · levels/progression · 📎.
  - `+perfect-stage-life` «Життя за ідеальне проходження стадії» · game-logic/score · 📎.
  - Також: `+crush-by-falling`, `+chest-container`, `+boss-stage`.

## Пропозиції до словників
- `+trigger:landed` — повтор (камінь приземлився на гравця).
- `+effect:recall` — повернути аватар на чекпоінт за ціну (можна `teleport` + `lives(−1)`, слабка).
- `+ui:diamond-quota` — «зібрано/потрібно» червоних для дверей світу (близько ⏳ `progress-bar`).
- `+feature:perfect-bonus` — нагорода за проходження без помилок.

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Diamond_Rush) — Gameloft, 1 грудня 2006 (J2ME), BlackBerry 2009; 3 світи, 40 стадій, червоні/фіолетові, крамниця HP, коло-чекпоінт і виклик за життя, бонусне життя, молот/компас/гак, боси.
- [Pocket Gamer review](https://www.pocketgamer.com/diamond-rush/review/) — падаючі камені розчавлюють, штовхання каменів, загибель → початок кімнати, одна фіксована розвʼязка кімнати.
- [ru.wikipedia](https://ru.wikipedia.org/wiki/Diamond_Rush) — вміст скринь (життя, срібні й золоті ключі), список ворогів і пасток.

## Непевне
- (?) Чи земля «копається» проходом, як у Boulder Dash, чи це зарості/лози; чи камені скочуються з округлого.
- (?) Функції молота, компаса й гака (з памʼяті: молот бʼє камені/стіни, гак — переправа, компас — показує секрети) — не взято в правила.
- (?) Чи рух покроковий по клітинах, чи плавний; поведінка ворогів (патерни) — лише з малодостовірного джерела.
- (?) Що відбувається, коли закінчились життя; точні вікна й меню J2ME-версії.
- (?) Чи фіолетові купують також чекпоінти (так у черзі; Wikipedia — лише HP).
