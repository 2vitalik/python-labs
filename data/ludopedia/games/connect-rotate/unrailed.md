---
title: Unrailed!
slug: unrailed
aka: [Unrailed]
family: connect-rotate
also: [build-sim, maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: coop
  info: full
  random: both
  goal: score
year: 2020
platforms: [PC, macOS, Linux, PS4, Switch, Xbox One]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Unrailed!", best: true, note: "кооп до 4, дерево й залізо, станції й болти, тварини на колії, NPC крадуть рейки, 5 режимів, процедурна генерація; Indoor Astronaut, 2020"}
  - {kind: official, url: "https://unrailed-game.com/", note: "«Mine resources, craft tracks and keep the train from derailing!», біоми з босами, режими Endless/Versus 4v4/Time Attack 20 хв/Classic/Terrain Conductor"}
  - {kind: steam, url: "https://store.steampowered.com/app/1016920/Unrailed/", note: "10+ вагонів-апгрейдів, 5+ біомів, Endless/Quick/Sandbox/Versus, 4 рівні складності, погода, день/ніч, replay"}
  - {kind: fandom, url: "https://unrailed-wiki.com/page/Wagons", note: "фан-вікі: список 16 вагонів, стартові Crafter/Storage/Tank, ціни в болтах, 3 вагони на вибір на станції"}
  - {kind: fandom, url: "https://unrailed-wiki.com/page/Water", note: "фан-вікі: бак — перегрів, пожежа поширюється на вагони, відро гасить"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Unrailed+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, move-by-input, move-auto, progress-acceleration, item-pickup, inventory-limit, dig-terrain, destructible-blocks, impassable-cells, random-walk, thief, infinite-field, round-currency, shop-between-levels, shop-catalog, in-round-upgrades, checkpoint, online-multiplayer, simultaneous-versus, mode-select, difficulty-levels, replay, end-screen, +track-before-train, +craft-from-resources, +overheat-fire, +shared-tools, +couch-plus-online-coop]
proposes: ["+effect:extend_path", "+effect:craft", "+effect:refill", "+effect:extinguish", "+effect:derail", "+role:tool", "+role:wagon", "+ui:heat-bar", "+ui:distance-counter", "+feature:mode-versus-race", "+feature:map-editor-share", "+card:track-before-train", "+card:craft-from-resources", "+card:overheat-fire", "+card:shared-tools"]
author: opus
date: 2026-11-09
---

# Unrailed! — кооп у реальному часі: рубай дерева, копай залізо, крафть рейки й клади їх перед поїздом, що не зупиняється

## Суть
Поїзд невпинно повзе вперед власною колією; команда з 1–4 гравців бігає воксельною картою, рубає дерева, розбиває камінь на залізо, несе їх у вагон-склад, а вагон-крафтер робить з них рейки. Рейки треба вкласти перед локомотивом до того, як він дійде до кінця колії, — інакше аварія і кінець забігу. Ядро — **логістика під тиском часу і спільні інструменти**: сокира, кайло й відро існують в одному екземплярі, бак перегрівається, тварини й злодії заважають. На станціях за болти купують і апгрейдять вагони.

## Поле і час
- Квадратна сітка клітин (воксельний вигляд), процедурно згенерована смуга, що тягнеться вправо (`infinite-field`); камера йде за поїздом (?).
- Клітини: трава, дерево, камінь, вода, непробивні скелі/залізні блоки (?), сніг (біом) тощо — біомів 5+.
- Real-time; поїзд прискорюється з відстанню (?), апгрейд локомотива скидає швидкість.
- Ритм: перегін між станціями → станція (поїзд стоїть, магазин) → наступний перегін; погода й день/ніч.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | несе 1 інструмент або стос ресурсів (?) | ходить 4/8 напрямками (?), бере/кладе предмети, діє інструментом |
| Локомотив | object | швидкість; рівень | їде колією сам; дійшов до кінця колії → аварія |
| Вагон-склад (Storage) | container | 3 шт. кожного ресурсу (рівень 1) | приймає дерево й залізо |
| Вагон-крафтер (Crafter) | spawner | — | з 1 дерева + 1 заліза робить рейку (?), витрачаючи склад |
| Вагон-бак (Tank) | object | рівень води | спадає з часом; порожній → поїзд горить, вогонь поширюється на вагони і вимикає їх |
| Вагони-апгрейди (Dynamite, Miner, Collector, Supercharger, Brake, Ghost, Light, Compass, Milk, Slot Machine, Transformer, Buckinator; Cannon — Versus) | object | рівень 1–3; ціна в болтах | купуються на станції; Dynamite робить динаміт раз на 35 с із заліза, Supercharger +1 рівень сусідам |
| Рейка | conduit (custom) | — | кладеться гравцем лише в продовження колії; знята — повертається в руки |
| Сокира / кайло / відро | pickup | 1 штука кожного | дерево → дрова; камінь → залізо; відро — вода з озера в бак, гасить пожежу, розтоплює сніг |
| Дерево / камінь | static | — | перешкода; розбивається інструментом на ресурс |
| Вода | terrain | — | джерело для відра; колію через неї класти не можна (?) |
| Тварини (корови, лами) | neutral | — | блукають; стають на колію і заважають поїзду |
| Злодій (NPC) | enemy | — | знімає шматки колії з маршруту |
| Станція | static | — | поїзд зупиняється; магазин вагонів за болти |
| Болт | resource | — | дається на станції; валюта апгрейдів |
| Бос біому | boss | — | охороняє розвилку до наступного біому (Endless, нові версії) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, dir)` → ЯКЩО `free(cell)` → ТО `move(player, dir)`; інакше `block`.
- КОЛИ `input(pick, cell)` → ЯКЩО `occupied(cell, tool|resource|rail)` → ТО `pickup`; ЯКЩО в руках щось інше → `swap(hand, cell)` (?).
- КОЛИ `input(use)` → ЯКЩО `has(player, axe)` and `facing(player, tree)` → ТО `custom: «рубати»`; після кількох ударів `transform(tree, wood)`.
- КОЛИ `input(use)` → ЯКЩО `has(player, pickaxe)` and `facing(player, rock)` → ТО `transform(rock, iron)`.
- КОЛИ `contact(player, storage)` → ЯКЩО `has(player, wood|iron)` and `not state(storage, full)` → ТО `custom: «покласти в склад»`.
- КОЛИ `timer(craft)` → ЯКЩО `count(storage.wood, >=, 1)` and `count(storage.iron, >=, 1)` → ТО `custom: «крафтер робить рейку»`, `take(storage, wood+iron)`.
- КОЛИ `input(place, rail)` → ЯКЩО `custom: «клітина сусідня з кінцем колії»` and `free(cell)` → ТО `place(rail)` — колія подовжується.
- КОЛИ `tick` → ТО `move(train, next_rail)`; швидкість `speed(train, +k)` з часом (?).
- КОЛИ `blocked(train)` (кінець колії) → ТО `crash`, `lose` (`game_over`).
- КОЛИ `timer(heat)` → ТО `counter(water, -1)`; КОЛИ `counter(water, ==, 0)` → ТО `set_state(train, burning)`, вогонь `custom: «поширюється на сусідні вагони, вони не працюють»`.
- КОЛИ `contact(player, tank)` → ЯКЩО `has(player, bucket_full)` → ТО `custom: «наповнити бак / погасити»`, `clear_state(train, burning)`.
- КОЛИ `contact(player, water)` → ЯКЩО `has(player, bucket)` → ТО `custom: «набрати воду»`.
- КОЛИ `rng(p)` → ТО `move(animal, random)`; ЯКЩО `occupied(rail, animal)` → `custom: «тварина заважає»` (?).
- КОЛИ `contact(thief, rail)` → ТО `custom: «знімає шматок колії»`.
- КОЛИ `reach(train, station)` → ТО `custom: «поїзд зупиняється»`, `currency(+bolts)`, `window(shop-window)` (3 вагони на вибір), `checkpoint` (?).
- КОЛИ `input(buy, wagon)` → ЯКЩО `has(team, bolts)` → ТО `custom: «вагон додається»`, `currency(-price)`; апгрейд — лише з наступної станції.
- КОЛИ `timer(35s)` → ЯКЩО `has(dynamite_wagon, iron)` → ТО `spawn(dynamite)`; КОЛИ `input(throw, dynamite)` → ТО `explode(area)`.
- Перемога: Endless — дістатись далі (кінцева станція після всіх біомів) · Поразка: аварія поїзда · Рахунок: пройдена відстань / станції.

## Керування і ввід
- Клавіатура/геймпад: рух, одна кнопка «взяти/покласти», дія інструментом — автоматично при упорі в клітину (?); кидок динаміту.
- Кооп: локальний (кілька геймпадів) + онлайн, змішано; інструменти спільні — треба передавати.
- Тач/миша не потрібні; ввід — пряме керування аватаром.

## Вікна, меню, HUD
- `main-menu`: Play → `mode-select` (Endless, Quick/Time Attack 20 хв, Classic, Sandbox, Versus) → `difficulty-select` (4 рівні) → `lobby-window` (онлайн, ?).
- `character-select` / `skin-select` — косметика персонажа (?).
- `game-screen`: карта, `heat-bar` бака, вміст складу на вагоні, `distance-counter`, болти (`coins`).
- `shop-window` на станції: 3 вагони на вибір, апгрейд наявних, ціна в болтах.
- `end-screen`: відстань, станції; `replay-window` (replay-система).
- `editor-window`: Terrain Conductor — мапи, якими діляться (?).
- Переходи: main-menu → mode-select → game-screen ⇄ shop-window (станція) → end-screen.

## Фічі поза полем
- `mode-endless` / `mode-time-attack` / `mode-classic` / `mode-sandbox` / `mode-versus` (до 4v4: дві команди будують наввипередки).
- `difficulty-presets` (4), `meta-progression` (постійні апгрейди гравця, нові локомотиви), `unlockables` (біоми, косметика).
- `local-multiplayer` + `online-multiplayer` змішано; `replay`; погода й день/ніч.
- `level-editor` + `level-sharing` (Terrain Conductor).

## Варіації й родичі
- Родичі: Train Valley (колії real-time, але курсором), Trainyard/Railbound (колії-пазл), Overcooked (кооп-логістика зі спільними станціями), Snake (не зупинишся — помреш), Factorio (крафт ланцюга ресурсів).
- **Осі варіацій:** хто кладе колію — курсор / аватар руками · ресурс колії — безкоштовний / бюджет / видобутий · тиск — поїзд-наздоганяч / таймер / переповнення · кооп — один гравець / спільні інструменти / команди-суперники.

## Цікавинки для курсу
- Колія, що може рости лише від кінця, і поїзд, який доганяє — 🌱.
- Ланцюг видобуток → склад → крафт → укладання з лімітами місткості — 📎.
- Спільні унікальні інструменти (одна сокира на всіх), бери/клади зі свопом — 🌱.
- Перегрів з поширенням пожежі по вагонах-ланцюжку — 📎.
- Процедурна смуга з біомами й гарантованою прохідністю — 🥈.
- Локальний + онлайн кооп одночасно — 🥇.

## Мапа на каталог
- Є: `move-4dir` · `move-by-input` · `move-auto` ↔ поїзд · `progress-acceleration` · `item-pickup` · `inventory-limit` ↔ склад · `dig-terrain` / `destructible-blocks` ↔ рубати/копати · `impassable-cells` · `random-walk` ↔ тварини · `thief` ↔ злодій рейок (тут краде колію, не інвентар) · `infinite-field` · `round-currency` ↔ болти · `shop-between-levels` · `shop-catalog` · `in-round-upgrades` ↔ вагони · `checkpoint` ↔ станція (?) · `online-multiplayer` · `simultaneous-versus` ↔ Versus · `mode-select` · `difficulty-levels` · `replay` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+track-before-train` «Клади шлях перед сутністю, що не зупиняється» · entities/move · 📎.
  - `+craft-from-resources` «Крафт предмета з ресурсів у контейнері за часом» · entities/state · 📎.
  - `+overheat-fire` «Перегрів → пожежа, що поширюється по ланцюгу» · entities/state · 📎.
  - `+shared-tools` «Унікальні інструменти, спільні для команди» · entities/interact · 🌱.
  - `+couch-plus-online-coop` «Змішаний локальний + онлайн кооп» · game-logic/opponent · 🥇.

## Пропозиції до словників
- `+effect:extend_path` (підтвердження: Flow Free, Trainyard, Train Valley).
- `+effect:craft(container, recipe)` — контейнер перетворює ресурси на предмет.
- `+effect:refill(a, n)` / `+effect:extinguish(a)` — наповнити ресурс / зняти горіння (зараз — `custom`).
- `+effect:derail` — варіант `crash` для поїзда в кінці колії (можна злити з `crash`).
- `+role:tool` — інструмент, що лишається в руках і змінює дію; `+role:wagon` — частина поїзда-ланцюга з функцією.
- `+ui:heat-bar` — шкала перегріву; `+ui:distance-counter` — пройдена відстань.
- `+feature:mode-versus-race` — команди будують наввипередки; `+feature:map-editor-share` — Terrain Conductor.
- `+card:*` — див. «Мапа на каталог».

## Джерела
- ⭐ [Unrailed! — Wikipedia](https://en.wikipedia.org/wiki/Unrailed!) — кооп до 4, дерево (рубати) й залізо (з каменю), болти на станціях, тварини, NPC знімають колію, 5 режимів, процедурна генерація, дати, Indoor Astronaut / Daedalic.
- [unrailed-game.com](https://unrailed-game.com/) — «Mine resources, craft tracks…», біоми з босами на розвилках, режими (Endless, Versus 4v4, Time Attack 20 хв, Classic, Terrain Conductor).
- [Steam](https://store.steampowered.com/app/1016920/Unrailed/) — 10+ вагонів, 5+ біомів, кожен інструмент в одному екземплярі, 4 рівні складності, погода, replay.
- [Unrailed Wiki: Wagons](https://unrailed-wiki.com/page/Wagons) — 16 вагонів, стартові Crafter/Storage/Tank, ціни 1–2 болти, 3 на вибір, апгрейд з наступної станції.
- [Unrailed Wiki: Water](https://unrailed-wiki.com/page/Water) і результати пошуку — бак, пожежа на сусідні вагони, відро; склад 3 шт., динаміт кожні 35 с.

## Непевне
- (?) Рецепт рейки (1 дерево + 1 залізо), чи несе гравець стос ресурсів, автоудар інструментом — з памʼяті.
- (?) Прискорення поїзда з часом, камера за поїздом, вода як непрохідна для колії, мости — не звірено.
- (?) Що саме роблять тварини (зупиняють поїзд? аварія?) — Wikipedia каже лише «can block».
- (?) Режими розходяться між джерелами (Quick/Time, Classic, Sandbox, Terrain Conductor як режим чи редактор).
- (?) Станція як checkpoint (продовження після аварії) — не звірено; офіційний сайт: «each locomotive loss is an opportunity to rebuild».
- Тека `connect-rotate` (як призначено: прокладання колії); за дієсловом «добувати й крафтити» межує з `build-sim`.
