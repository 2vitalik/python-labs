---
title: Pocket Mine
slug: pocket-mine
aka: []
family: dig-gravity
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: both
  goal: score
year: 2013
platforms: [iOS, Android]
links:
  - {kind: other, url: "https://nardio.net/?p=6362", best: true, note: "огляд 12.10.2013: блоки 1–2 удари й незламні, міцність кирки, бустер-картки, ключі за цілі, скрині до 9 ключів, заряд 5 забігів"}
  - {kind: other, url: "https://www.148apps.com/reviews/pocket-review/", note: "огляд 148Apps (03.10.2013): тап для руху, автоскрол, три картки на раунд, апгрейд кирки між забігами, додаткові цілі"}
  - {kind: other, url: "https://www.tuttoandroid.net/giochi/pocket-mine-android-152603/", note: "огляд Android (28.10.2013, IT): квадратні блоки, вкраплення золота/вугілля/самоцвітів, ящики з бомбами й відбійним молотком, аптечка"}
  - {kind: other, url: "https://apps.apple.com/us/app/pocket-mine/id585528957", note: "App Store (Roofdog Games): тап по блоках, скрині, артефакти, ланцюги вибухів, колода бустер-карток, персонажі, музей"}
  - {kind: other, url: "https://www.148apps.com/reviews/pocket-mine-2-review/", note: "огляд Pocket Mine 2 (2015): рівні замість одного забігу, злиття карток, фабрики"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Pocket+Mine+Roofdog+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [cell-click, dig-terrain, destructible-blocks, impassable-cells, explode-area, chain-detonation, item-pickup, round-currency, shop-between-levels, weighted-spawn, infinite-field, player-camera, leaderboard, save-progress, game-over-continue, +scroll-death-edge, +tool-durability, +pre-level-boosters, +card-collection, +bonus-objectives, +stamina-energy, +multi-hit-block, +run-meta-carry, +depth-goal, +artifact-set-collection, +auto-dig-powerup]
proposes: ["+feature:energy-regen", "+feature:boosters", "+ui:depth-meter", "+ui:pick-durability", "+window:deck-builder", "+card:tool-durability", "+card:multi-hit-block", "+card:artifact-set-collection"]
author: opus
date: 2026-11-09
---

# Pocket Mine — тапай блоки вниз, поки не зламалась кирка й не наздогнав екран; три картки задають бонуси забігу

## Суть
Мобільна free-to-play копанка Roofdog Games (2013): шахтар спускається у вертикальну шахту з квадратних блоків, гравець тапає блок — шахтар іде до нього й бʼє кіркою. Забіг обмежують дві речі: кирка має скінченну кількість ударів, а екран сам зсувається вниз і розчавлює того, хто відстав. Ящики дають бомби, динаміт, гранати й відбійні молотки; перед кожним забігом три бустер-картки вирішують, які бонуси трапляться. Між забігами гроші йдуть на міцність кирки й нові картки.

## Поле і час
- Вертикальна шахта з квадратних блоків, що продовжується вниз (`infinite-field`); видно вікно в кілька рядків, камера йде за спуском.
- Real-time: поле підіймається / екран прокручується вниз само, з постійною швидкістю (?); темп задає автоскрол.
- Глибина в метрах — головний результат забігу (рекорд рецензента — 274 м).
- Щонайменше пʼять випадкових мап-оточень, складність не змінюють; вміст ящиків — випадковий (`random: both`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Шахтар | player | удари кирки (міцність) | іде до тапнутої клітини, бʼє блок |
| Звичайний блок | terrain | 1 удар | руйнується |
| Сірий блок | terrain | 2 удари | руйнується з другого удару |
| Коричневий «звивистий» блок | static | — | звичайна кирка не бере |
| Блок із вкрапленням (вугілля, золото, самоцвіти, діаманти) | resource | цінність | зруйнований → гроші |
| Деревʼяний ящик | container | — | зруйнований → бонус (набір — від карток) |
| Бомба / динаміт / граната | object | — | вибух руйнує блоки навколо; ланцюг вибухів |
| Відбійний молоток / бур | pickup | — | копає автоматично (?) |
| Аптечка | pickup | — | повертає удари кирці |
| Скриня зі скарбом | container | до 9 ключів | відкривається ключами |
| Артефакт | pickup | набір | збирається в колекції музею |
| Край екрана | hazard | — | наздогнав шахтаря → кінець забігу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(tap, empty)` → ТО `move(miner, to)`.
- КОЛИ `input(tap, block)` → ТО `custom: «шахтар підходить і бʼє кіркою»`, `counter(pick, -1)`, `counter(block_hits, -1)`.
- КОЛИ `counter(block_hits, ==, 0)` → ТО `set_cell(block, empty)`; ЯКЩО `cell(block, ore)` → ТО `currency(+value)`.
- КОЛИ `input(tap, brown_block)` → ТО `block`.
- КОЛИ `destroyed(crate)` → ТО `spawn(power_up)` з набору бустер-карток.
- КОЛИ `input(tap, bomb|dynamite|grenade)` → ТО `explode(area, empty)`; КОЛИ `custom: «вибух зачепив інший вибуховий обʼєкт»` → ТО `explode(...)` і для нього.
- КОЛИ `picked(miner, medkit)` → ТО `counter(pick, +n)`.
- КОЛИ `tick` → ТО `custom: «екран зсувається вниз»`; КОЛИ `custom: «шахтар вийшов за верхній край»` → ТО `game_over`.
- КОЛИ `counter(pick, ==, 0)` → ТО `custom: «кирка зламалась»`, `window(game-over-continue)`: продовжити за рубіни або забрати нагороду.
- КОЛИ `level_start` (старт забігу) → ТО `window(custom-window)` з трьома картками; картки дають предмети (динаміт, гранати) або `custom: «підвищують шанс появи предмета»`.
- КОЛИ `counter(goal, >=, n)` (зібрати 10 золота, використати 5 гранат…) → ТО `give(player, key)`.
- КОЛИ `input(open, chest)` → ЯКЩО `counter(keys, >=, cost)` → ТО `counter(keys, -cost)`, `give(player, reward)`.
- КОЛИ `input(start_run)` → ЯКЩО `counter(charge, >, 0)` → ТО `counter(charge, -1)`; заряд відновлюється з рівнем профілю, часом, за рубіни чи рекламу.
- Між забігами: КОЛИ `input(buy, upgrade)` → ЯКЩО `counter(money, >=, price)` → ТО `currency(-price)`, `custom: «більше ударів кирки»`; гроші також купують картки.
- Перемога: нема. · Поразка забігу: кирка зламалась або наздогнав екран. · Рахунок: глибина й гроші.

## Керування і ввід
- Тап по блоку — підійти й бити; тап по порожній клітині — підійти; тап по бонусу — застосувати (?).
- У меню — тапи по картках, скринях, магазину; підтвердження покупок за рубіни нема (скарга рецензента).

## Вікна, меню, HUD
- `main-menu` / хаб профілю: рівень, заряд, гроші, рубіни, ключі.
- `custom-window` → `+window:deck-builder`: три бустер-картки забігу, перемішування.
- `game-screen`: шахта; HUD — глибина (`+ui:depth-meter`), удари кирки (`+ui:pick-durability`), гроші (`coins`), цілі забігу (`objective-text`).
- `game-over-continue` — зламана кирка: продовжити за рубіни чи забрати.
- `end-screen` — підрахунок здобичі забігу.
- `shop-window` — апгрейд кирки, картки, рубіни, ліміт заряду.
- `custom-window` — скрині з ключами; музей артефактів (у пізніх версіях).
- `leaderboard`, `achievements-window` (Game Center).

## Фічі поза полем
- `+feature:boosters`: колода бустер-карток, дублікати → рідкісніші картки (скарга: «важко зібрати дублікати на легендарну»).
- `+feature:energy-regen`: заряд 5 забігів, покупка за $1.99 піднімає до 8 (2013); оновлення 5.0.0 (2023) — максимум енергії з 8 до 10 через апгрейд.
- `meta-progression`: апгрейд кирки з «prestige»-коронами (відгук користувача), рівень профілю.
- `cloud-save`, `leaderboard-online`, `achievements`, обмін артефактами з друзями.

## Варіації й родичі
- Pocket Mine 2 (2015): окремі рівні замість одного безкінечного спуску, картки визначають бонуси мапи, злиття дублікатів, лоадаути на час, фабрики для крафту, набори артефактів за нагороди. Pocket Mine 3 — наступна частина (?).
- У сімʼї: [mr-driller.md](mr-driller.md) (спуск з ресурсом-таймером — повітря), [downwell.md](downwell.md) (вертикальний спуск), [motherload.md](motherload.md) (руда → гроші → апгрейди), [diggys-adventure.md](diggys-adventure.md) (копання за енергію).
- **Осі варіацій**: ліміт забігу — міцність інструмента / автоскрол / повітря / паливо; міцність блока — 1 удар / N ударів / незламний; бонуси — випадкові / визначені картками перед забігом.

## Цікавинки для курсу
- Два обмежувачі забігу одночасно: лічильник ударів кирки + автоскрол, що наздоганяє — 📎.
- Блоки з кількістю ударів і незламні блоки на вертикальному нескінченному полі — 🌱.
- Бустер-картки перед забігом як ваги ймовірностей появи бонусів у ящиках — 📎 (зважений спавн).
- Ланцюг вибухів: бомба підриває сусідні вибухові обʼєкти — 📎.
- Цілі забігу → ключі → скрині з ціною в ключах — 🌱.

## Мапа на каталог
- Є: `cell-click` ↔ тап · `dig-terrain` + `destructible-blocks` · `impassable-cells` ↔ коричневий блок · `explode-area` + `chain-detonation` · `item-pickup` · `round-currency` ↔ гроші · `shop-between-levels` ↔ апгрейди між забігами · `weighted-spawn` ↔ картки змінюють шанси · `infinite-field` ↔ безкінечний спуск · `player-camera` · `leaderboard` · `save-progress` · `game-over-continue` ↔ продовження за рубіни.
- **Нема** → пропозиції карток:
  - `+tool-durability` «Інструмент на N застосувань, кінець — кінець забігу» · entities/state · 🌱 · слот {uses}.
  - `+multi-hit-block` «Блок руйнується за N ударів» · entities/interact · 🌱 · слот {hits}.
  - `+artifact-set-collection` «Набори предметів між забігами за нагороду» · game-logic/economy · 📎.
  - `+auto-dig-powerup` «Бонус копає сам кілька клітин» · entities/interact · 🌱.
  - `+scroll-death-edge`, `+pre-level-boosters`, `+card-collection`, `+bonus-objectives`, `+stamina-energy`, `+run-meta-carry`, `+depth-goal` — повтори з інших файлів.

## Пропозиції до словників
- `+feature:energy-regen` — заряд забігів, що відновлюється з часом (повтор).
- `+feature:boosters` — бустери перед забігом (повтор).
- `+ui:depth-meter` — глибина забігу (повтор); `+ui:pick-durability` — лишок ударів кирки.
- `+window:deck-builder` — вибір/перегляд карток перед забігом (повтор).

## Джерела
- ⭐ [Nardio: Pocket Mine review](https://nardio.net/?p=6362) — тапи, типи блоків (1 і 2 удари, незламні), міцність кирки, продовження за рубіни, бустер-картки, цілі → ключі → скрині, заряд 5/8, гроші й рубіни, мапи.
- [148Apps: Pocket Mine Review](https://www.148apps.com/reviews/pocket-review/) — автоскрол, кінець забігу при зламаній кирці, три картки на раунд, апгрейди й картки між забігами, додаткові цілі.
- [TuttoAndroid](https://www.tuttoandroid.net/giochi/pocket-mine-android-152603/) — квадратні блоки, вкраплення, ящики з бомбами й відбійним молотком, аптечка, розчавлення екраном.
- [App Store: Pocket Mine](https://apps.apple.com/us/app/pocket-mine/id585528957) — актуальний опис: скрині, артефакти, ланцюги вибухів, бонуси (бомби, динаміт, бури), колода бустер-карток, персонажі, музей; історія версій (енергія 8 → 10 у 5.0.0).
- [148Apps: Pocket Mine 2 Review](https://www.148apps.com/reviews/pocket-mine-2-review/) — сиквел: рівні, злиття карток, фабрики, артефакти.
- YouTube: пошук «Pocket Mine Roofdog gameplay».

## Непевне
- (?) Ширина шахти в блоках і чи шахтар може ходити вбік і вгору — у джерелах нема.
- (?) Чи бонуси (бомби, молоток) спрацьовують від тапа, чи відразу при розбитті ящика.
- (?) Як саме шахтар «підходить» до тапнутої цілі (лише сусідні клітини чи шлях) і чи кожен удар знімає одиницю міцності.
- (?) Швидкість автоскролу й чи вона росте з глибиною.
- (?) Персонажі зі здібностями й музей — з сучасного опису App Store; у версії 2013 їх, можливо, ще не було.
- (?) Pocket Mine 3 — назва з результатів пошуку, сторінку не відкривав.
