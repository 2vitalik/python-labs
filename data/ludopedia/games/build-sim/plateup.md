---
title: PlateUp!
slug: plateup
aka: [PlateUp]
family: build-sim
also: [maze-arcade]
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: coop
  info: full
  random: both
  goal: survive
year: 2022
platforms: [PC, Switch, PS4, PS5, Xbox One, Xbox Series]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1599600", best: true, note: "опис: 1–4 гравці, 15 днів, ланцюжки приладів, франшиза, роглайт"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/PlateUp!", note: "терпіння клієнтів, вибір 1 з 2 карток між днями, склад-HQ, дати релізу"}
  - {kind: fandom, url: "https://wiki.plateupgame.com/Automation", note: "офіційна вікі, сторінка автоматизації (фетчер отримав лише заголовок)"}
  - {kind: other, url: "https://www.touchtapplay.com/how-to-automate-serving-in-plateup-guide-tips/", note: "гайд: конвеєр, грабер, smart/rotating grabber, блюпринти, брудний посуд"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=PlateUp+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-8dir, cell-click, drag-drop-piece, multi-cell-size, row-conveyor, spawn-schedule, item-pickup, inventory-limit, round-currency, shop-between-levels, shop-catalog, shop-window, run-relics, rule-variants, progress-acceleration, online-multiplayer, save-progress, keep-playing-after-win, status-panel, goal-counter, +item-transfer-grabber, +filter-by-sample, +patience-timer, +cook-timer-burn, +recipe-combine, +blueprint-draft, +difficulty-card-pick, +prep-phase-layout, +franchise-meta]
proposes: ["+trigger:day_start", "+trigger:day_end", "+effect:combine", "+cond:patience", "+ui:patience-ring", "+ui:order-bubble", "+window:card-offer", "+window:blueprint-shop", "+feature:prep-phase", "+card:item-transfer-grabber", "+card:patience-timer"]
author: opus
date: 2026-11-09
---

# PlateUp! — ресторан на клітинах: вдень готуєш і подаєш, уночі переставляєш прилади, поки кухня не почне готувати сама

## Суть
Гравці (1–4, кооператив) керують кухарями в ресторані на сітці: беруть інгредієнти, готують на приладах, подають гостям, миють посуд — і все це на таймері терпіння клієнтів. Між днями ресторан закритий: прилади вільно переставляються, купуються нові за випадковими блюпринтами, а картка складності змінює правила до кінця забігу. Головне для корпусу — **предмети, що їдуть між клітинами** (конвеєр, грабер) і прилади-сусіди, які разом складаються в автоматичну кухню. `klass: hybrid` — аватар (кухар у реальному часі) + курсорне планування (розстановка між днями).

## Поле і час
- Ресторан — квадратна сітка клітин зі стінами, дверима й зоною входу; планування генерується для кожної нової локації (франшизи).
- Кожен прилад займає 1 клітину; столи складаються з кількох клітин-шматків (номер місця — на останньому поставленому).
- Два ритми: **день** (real-time сервіс, хвилі клієнтів) і **підготовка** між днями (ресторан закритий, можна переставляти все). Забіг — до 15 днів.
- Камера згори-збоку, все поле видно.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кухар | player | несе 1 предмет | ходить, бере/кладе предмет на прилад попереду, взаємодіє (рубати, мити) |
| Група клієнтів | neutral | розмір, терпіння, замовлення | заходить, сідає за стіл, замовляє, чекає, їсть, платить, лишає брудний посуд |
| Стіл (шматки) | static | місця | місце для групи; брудний посуд — на шматку з номером |
| Стійка (counter) | object | — | тримає 1 предмет |
| Ящик інгредієнта | spawner | вид | видає інгредієнт кухарю чи граберу |
| Плита (hob) | object | таймер готування | готує те, що на ній |
| Турбо-піч | object | — | швидша плита (згадана в Steam) |
| Мийка (сінк, soaking sink) | object | — | брудний посуд → чистий |
| Тарілки / стос посуду | resource | кількість | без чистих тарілок не подати |
| Конвеєр | object | напрям | штовхає предмет, покладений на нього, у сусідню клітину; сам не бере |
| Грабер | object | напрям | бере предмет з клітини позаду (ящик, прилад, стійка) і передає вперед |
| Smart Grabber | object | навчений предмет | як грабер, але бере лише предмет зразка |
| Rotating Grabber | object | вихід: одна з 3 сусідніх | як грабер, але вихід налаштовується |
| Комбайнер, авто-плейтер, нагрівальний міксер | object | — | збирають/готують частини страви автоматично (?) |
| Телепорт, кухонний ліфт (dumbwaiter) | object | пара | переносить предмет на відстань |
| Термінал замовлень | object | — | приймає замовлення без підходу до столу |
| Блюпринт | pickup | прилад, ціна | купується вдень підготовки, розгортається в прилад |
| Шафа блюпринтів | container | 1 блюпринт | зберігає блюпринт між раундами |
| Стіл-бюро (desk) | object | режим | копіює, апгрейдить або знижує ціну блюпринта |
| Сміттєвий бак | sink | — | знищує предмет |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `schedule(waves)` → ТО `spawn_at(customer_group, entrance)`.
- КОЛИ `enter(customer_group, table)` → ТО `custom: «група робить замовлення»`, `set_state(customer_group, waiting)`.
- КОЛИ `tick` → ЯКЩО `state(customer_group, waiting)` → ТО `counter(patience, -1)`.
- КОЛИ `counter(patience, ==, 0)` → ТО `custom: «група йде незадоволеною»`, `lose` (?).
- КОЛИ `input(serve, dish)` → ЯКЩО `same(dish, order, recipe)` → ТО `custom: «група їсть»`, потім `currency(+price)`, `spawn_at(dirty_plate, table_numbered_piece)`.
- КОЛИ `input(interact, box)` → ЯКЩО `not has(chef, item)` → ТО `give(chef, ingredient)`.
- КОЛИ `input(put, appliance)` → ЯКЩО `free(appliance)` → ТО `place(chef, item)`; інакше `custom: «поєднати, якщо рецепт дозволяє»`.
- КОЛИ `timer(cook_time)` → ЯКЩО `occupied(hob, food)` → ТО `transform(food, cooked)`.
- КОЛИ `timer(burn_time)` → ЯКЩО `state(food, cooked)` and `occupied(hob, food)` → ТО `transform(food, burnt)` (?).
- КОЛИ `timer(step)` → ЯКЩО `occupied(conveyor, item)` and `free(cell_ahead)` → ТО `move(item, facing)`; інакше `block`.
- КОЛИ `timer(step)` → ЯКЩО `occupied(cell_behind, item)` and `free(cell_ahead)` → ТО `custom: «грабер забирає предмет позаду й передає вперед»`.
- КОЛИ `timer(step)` → ЯКЩО `same(item, trained_sample, kind)` → ТО `custom: «smart grabber забирає лише предмет зразка»`.
- КОЛИ `input(rotate, rotating_grabber)` → ТО `custom: «вихід — у налаштовану з 3 сусідніх клітин»`.
- КОЛИ `contact(conveyor_item, table_seat)` → ТО `custom: «клієнт бере страву з конвеєра поруч зі столом»`.
- КОЛИ `timer(step)` → ЯКЩО `occupied(numbered_piece, dirty_plate)` and `facing(grabber, numbered_piece)` → ТО `custom: «грабер забирає брудний посуд»`.
- КОЛИ `input(wash, dirty_plate)` або сінк-автомат → ТО `transform(dirty_plate, clean_plate)`.
- КОЛИ `custom: «кінець дня»` → ТО `custom: «ресторан закривається»`, `window(blueprint-shop)` — випадкові блюпринти за `currency`.
- КОЛИ `custom: «день-рубіж»` → ТО `choose(card_a, card_b)` — картка підвищує складність і змінює правила до кінця забігу (складніше меню, механіка гравців, поведінка клієнтів).
- КОЛИ `input(buy, blueprint)` → ЯКЩО `counter(money, >=, price)` → ТО `currency(-price)`, `place(chef, appliance)`.
- КОЛИ `input(drag, appliance)` → ЯКЩО `custom: «фаза підготовки»` → ТО `move(appliance, to)`.
- КОЛИ `input(use, desk, blueprint)` → ТО `custom: «копія / апгрейд / знижка»`.
- КОЛИ `counter(day, ==, 15)` → ТО `win` («франшиза»: нова локація з перенесеними відкриттями) (?).
- Поразка: клієнти не дочекались (терпіння) · Перемога: дожити до 15 дня і франчайзити · Рахунок: гроші за день як ресурс, не очки.

## Керування і ввід
- Рух кухаря стрілками/стіком; одна кнопка — взяти/покласти, друга — дія з приладом (рубати, мити, крутити грабер). Мапінг «одна-дві кнопки» за задумом.
- Фаза підготовки: ті самі кнопки піднімають і переносять прилади; поворот приладу — дія (?).
- Smart Grabber навчається, коли на нього покласти зразок.
- Кооп до 4 гравців: локально й онлайн, кожен керує своїм кухарем.

## Вікна, меню, HUD
- `game-screen` день: ресторан, бульбашки замовлень над столами (`+ui:order-bubble`), кільця терпіння (`+ui:patience-ring`), лічильник днів (`goal-counter`), гроші (`coins`).
- `game-screen` підготовка: той самий ресторан, закритий; блюпринти лежать на підлозі з цінами (`+window:blueprint-shop` по суті є полем, не модалом).
- `custom-window`/HQ: склад-штаб франшизи між забігами — досягнення, кастомізація персонажа, апгрейд приладів, параметри наступного ресторану (вибір локації — `map-window` (?)).
- `card-offer`: вибір 1 з 2 карток складності.
- `end-screen`: забіг програно / франшиза.
- `main-menu` → `lobby-window` (кооп) → HQ → локація → `game-screen`; `pause-menu`, `settings-window`.

## Фічі поза полем
- `mode-coop` 1–4, онлайн; `meta-progression`: відкриття, здібності й апгрейди переносяться між забігами («roguelite progression»).
- `run-relics`-подібні картки складності: правило змінюється до кінця забігу.
- Франшиза: нова локація з процедурним кліматом, клієнтами й умовами; штаб із досягненнями.
- Пізніші оновлення додали event-режими, рецепти, прилади.

## Варіації й родичі
- Родичі: Overcooked (той самий кооп-хаос, але без перестановки кухні й автоматизації), `factorio-belts` (конвеєр + маніпулятор між клітинами — пряме джерело граберів), `shapez` (комбінування частин), `mindustry`, `prison-architect-rooms`.
- Осі «транспорт предмета»: лише руки / конвеєр (штовхає) / грабер (бере і штовхає) / фільтр-грабер / поворотний / телепорт.
- Осі «хто готує»: гравець у реальному часі / напівавтомат (кухар лише кладе) / повна автоматизація (кухня без людей).

## Цікавинки для курсу
- Конвеєр vs грабер: «штовхає те, що на ньому» проти «бере з сусіда й передає» — 📎; ланцюжок з фільтром за зразком — 🥉.
- Таймер терпіння на кожній групі + програш — 🌱.
- Плита з таймером «сире → готове → згоріле» — 🌱 (автомат станів предмета на клітині).
- Дві фази: real-time сервіс і вільна перестановка між днями — 🥉 (той самий стан поля, різні правила вводу).
- Вибір 1 з 2 карток, що змінюють правила до кінця забігу — 📎 (`rule-variants` в рантаймі).
- Випадкові блюпринти + шафа/бюро (копія, апгрейд, знижка) — 📎.
- Повна автоматизація ресторану як «програма з приладів» — 🥇 (граф граберів, маршрутизація посуду).

## Мапа на каталог
- Є: `move-8dir` (кухар) · `cell-click`/`drag-drop-piece` (перестановка приладів, лише в підготовці) · `multi-cell-size` (столи) · `row-conveyor` (лінія конвеєрів) · `spawn-schedule` (хвилі клієнтів) · `item-pickup` + `inventory-limit` (1 предмет у руках) · `round-currency` · `shop-between-levels` + `shop-catalog` + `shop-window` (блюпринти) · `run-relics` + `rule-variants` (картки) · `progress-acceleration` · `online-multiplayer` · `save-progress` · `keep-playing-after-win` (?) · `status-panel` · `goal-counter`.
- **Нема** → пропозиції карток:
  - `+item-transfer-grabber` «Маніпулятор між клітинами» · entities/move · 🥉 · слоти {filter, output_dir} — грабер/smart/rotating; родич Factorio inserter.
  - `+filter-by-sample` «Фільтр, навчений зразком» · entities/state · 📎.
  - `+patience-timer` «Таймер терпіння клієнта» · game-logic/lose · 🌱.
  - `+cook-timer-burn` «Сире → готове → згоріле на приладі» · entities/state · 🌱.
  - `+recipe-combine` «Скласти страву з частин» · entities/interact · 📎.
  - `+blueprint-draft` «Випадкові блюпринти до покупки» · game-logic/economy · 📎.
  - `+difficulty-card-pick` «Вибір 1 з 2 правил-ускладнень» · game-logic/difficulty · 📎.
  - `+prep-phase-layout` «Фаза вільної перестановки між раундами» · game-logic · 🥉.
  - `+franchise-meta` «Нова локація з перенесеними відкриттями» · levels/progression · 📎.

## Пропозиції до словників
- `+trigger:day_start` / `+trigger:day_end` — межі дня-раунду (сервіс ↔ підготовка).
- `+effect:combine` — частини стають стравою за рецептом.
- `+cond:patience` — терпіння групи вище нуля (окремо від `timer` гри).
- `+ui:patience-ring` — кільце терпіння над групою; `+ui:order-bubble` — бульбашка замовлення.
- `+window:card-offer` — вибір 1 з 2 карток; `+window:blueprint-shop` — крамниця як предмети на підлозі.
- `+feature:prep-phase` — фаза, коли поле редагується.
- `+card:item-transfer-grabber`, `+card:patience-timer` — див. вище.

## Джерела
- ⭐ [Steam: PlateUp!](https://store.steampowered.com/app/1599600) — кооп 1–4, 15 днів, ланцюжки приладів (турбо-печі, конвеєри), планування між змінами, франшиза, роглайт-прогресія.
- [Wikipedia](https://en.wikipedia.org/wiki/PlateUp!) — терпіння клієнтів і поразка, апгрейди після кожного дня, картки 1 з 2, склад між забігами, дати: Windows 4.08.2022, консолі 15.02.2024.
- [TouchTapPlay: автоматизація подачі](https://www.touchtapplay.com/how-to-automate-serving-in-plateup-guide-tips/) — конвеєр не бере з приладів, грабер бере; smart (зразок) і rotating; брудний посуд на шматку з номером; шафа блюпринтів, бюро.
- [PlateUp! Wiki: Automation](https://wiki.plateupgame.com/Automation) — офіційна вікі (вміст фетчеру не віддався).
- YouTube: пошук «PlateUp gameplay».

## Непевне
- (?) Поразка від першої ж незадоволеної групи чи після кількох — Wikipedia каже лише «if this goes on».
- (?) Згорання їжі й пожежа, бруд на підлозі — з памʼяті, у відкритих джерелах не бачив.
- (?) Роботу комбайнера, портіонера, авто-плейтера, міксера джерела лише називають.
- (?) Перемога на 15-му дні й «overtime» після неї — Steam каже «15 днів», механіку продовження не бачив.
- (?) На які дні випадає вибір картки — Wikipedia: «між днями», точний розклад не дано.
- (?) Rotating Grabber за гайдом «може повертатись»; за пошуком — вихід в одну з 3 сусідніх клітин.
