---
title: Diggy's Adventure
slug: diggys-adventure
aka: [«Пригоди Діґґі»]
family: dig-gravity
also: [build-sim]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: runtime
  goal: collect
year: 2012
platforms: [web (Facebook, портал Pixel Federation), Android, iOS]
links:
  - {kind: other, url: "https://www.touchtapplay.com/diggys-adventure-cheats-tips-strategy-guide/", best: true, note: "гайд: усе крутиться навколо енергії, маршрут без зайвих клітин, скрині й глеки з їжею, два типи будівель табору, приховані стіни з числом"}
  - {kind: official, url: "https://portal.pixelfederation.com/en/diggysadventure/about", note: "офіційно: копати шахти, логічні пазли, лабіринти, квести, табір із декором, регіони"}
  - {kind: other, url: "https://diggysguide.com/guides/tackling-energy-cost-increase-in-new-region", note: "множники ціни клітини за регіонами (Скандинавія ×6 Єгипту, Китай ×3 …), кухня, обладнання табору"}
  - {kind: other, url: "https://diggysguide.com/7th-birthday/encrypted-black-tower", note: "сторінка шахти: 186 клітин, 7 рівнів складності за енергією, важелі біля статуй, кнопки вмикають світло, ключ, ворота між частинами"}
  - {kind: other, url: "https://www.levelwinner.com/?p=7968", note: "гайд: час і енергія — основна змінна, табір: місткість і регенерація, кухня, понад 100 персонажів"}
  - {kind: other, url: "https://www.gamezebo.com/2012/10/05/diggys-adventure-review/", note: "огляд із черги; у фетчі 403, не прочитано"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pixel_Federation", note: "студія; 2012, casual adventure / exploration puzzle"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Diggy%27s+Adventure+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [cell-click, dig-terrain, destructible-blocks, impassable-cells, multi-cell-size, hidden-under-block, item-pickup, inventory, inventory-items, key-and-door, button-toggle, collect-all, round-currency, shop-catalog, shop-window, world-map, map-window, level-unlock, achievements-window, save-autosave, +stamina-energy, +tile-energy-cost, +energy-capacity-buildings, +cost-scaling, +craft-at-station, +ad-reward-energy, +reachable-dig]
proposes: ["+cond:reachable", "+effect:regen", "+ui:tile-cost-label", "+window:camp-screen", "+feature:ad-reward", "+card:tile-energy-cost", "+card:energy-capacity-buildings", "+card:ad-reward-energy", "+card:reachable-dig"]
author: opus
date: 2026-11-09
---

# Diggy's Adventure — кожна прокопана клітина коштує енергії: плануй маршрут, копи енергію на великі плити, будуй табір, щоб її ставало більше

## Суть
Соціальна F2P-гра Pixel Federation: археолог Diggy розкопує шахти-рівні на сітці, клацаючи по клітинах. Ядро — **енергетична економіка**: кожна клітина має ціну в енергії (число над нею), енергія відновлюється в реальному часі до межі, а великі плити коштують сотні — їх можна розкопати, лише накопичивши запас. Тому головне вміння — маршрут без зайвих клітин до скринь, ключів і цілей квесту. Між шахтами гравець будує табір, що збільшує місткість і регенерацію енергії, і готує їжу на кухні.

## Поле і час
- Шахта — квадратна сітка клітин: прохід, клітини породи з ціною, великі багатоклітинні плити, стіни; частини шахти зʼєднані воротами.
- Видно область довкола Diggy; приховані руйновані стіни показують число-ціну, лише коли Diggy поруч (`info: partial`).
- Час — real-time: енергія відновлюється щогодини, навіть офлайн; копання миттєве за наявної енергії.
- Мапа світу — регіони (Єгипет, Скандинавія, Китай, Атлантида, Греція, Новий Світ, Марс …), у кожному — сюжетні й повторювані шахти та події.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Diggy | player | енергія, місткість, регенерація | іде до клацнутої клітини й копає її |
| Клітина породи | terrain | ціна в енергії | розкопана → прохід |
| Велика плита | terrain | ціна сотні енергії (напр. 600) | займає кілька клітин; копається одним махом |
| Прихована стіна | terrain | ціна видна зблизька | за нею — зазвичай скриня |
| Стіна | static | — | не копається |
| Скриня / глек | container | випадковий вміст | їжа, матеріали, інгредієнти |
| Їжа | pickup | +енергія | зʼїсти будь-коли |
| Ключ | pickup | — | відмикає ворота |
| Важіль | switch | — | відкриває нові ділянки шахти |
| Кнопка | switch | — | вмикає світло / відкриває прохід; деякі — натиснути вдвох із NPC |
| Ворота | gate | — | перехід в іншу частину локації |
| NPC (напарник) | ally | — | діалоги квестів; стоїть на кнопці разом із Diggy |
| Будівля табору (місткість) | static | +максимум енергії | ставиться в таборі; ліміт розміщення |
| Будівля табору (регенерація) | static | +енергії за годину | «вітряки» тощо |
| Кухня | spawner | рецепт, час | з інгредієнтів готує їжу, ситнішу за знайдену |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, tile)` → ЯКЩО `custom: «до клітини є прохід уже розкопаним»` and `counter(energy, ≥, tile.cost)` → ТО `custom: «Diggy іде до клітини»`, `set_cell(tile, floor)`, `counter(energy, −tile.cost)`.
- КОЛИ `input(click, tile)` → ЯКЩО `counter(energy, <, tile.cost)` → ТО `block`, `window(confirm-dialog)` — пропозиція реклами за енергію, до 3 разів на день.
- КОЛИ `input(click, big_slab)` → ЯКЩО `counter(energy, ≥, slab.cost)` → ТО `custom: «уся плита зникає одним махом»`; інакше чекати, доки накопичиться.
- КОЛИ `timer(hour)` → ЯКЩО `counter(energy, <, capacity)` → ТО `counter(energy, +regen)`; працює й офлайн.
- КОЛИ `in_range(diggy, hidden_wall, 1)` → ТО `reveal(hidden_wall)` — над стіною зʼявляється ціна.
- КОЛИ `custom: «розкопано скриню або глек»` → ТО `give(diggy, food|material|ingredient)` — вміст випадковий.
- КОЛИ `input(eat, food)` → ТО `take(diggy, food)`, `counter(energy, +food.value)`.
- КОЛИ `input(click, lever)` → ТО `set_state(gate, open)` — відкрито нову ділянку.
- КОЛИ `enter(diggy, button)` → ЯКЩО `occupied(second_button, npc)` → ТО `set_state(gate, open)` (кнопка вдвох, ?).
- КОЛИ `input(click, button)` → ТО `custom: «увімкнути світло»` (?).
- КОЛИ `picked(diggy, key)` → ТО `custom: «відімкнути ворота»`.
- КОЛИ `custom: «виконано завдання квесту»` → ТО `currency(+coins)`, `counter(xp, +n)`.
- КОЛИ `all_gone(tile)` → ТО `custom: «бонус за повне очищення шахти»` (у подіях — дорівнює ціні рівня).
- КОЛИ `custom: «вхід у новий регіон»` → ТО `custom: «ціна всіх клітин × множник регіону»` (Скандинавія ×6 Єгипту, Китай ×3 Скандинавії, Атлантида ×2, Греція ×1.8, Пд. Америка ×1.4).
- КОЛИ `input(place, building)` → ТО `place(camp, building)`: `counter(capacity, +n)` або `counter(regen, +n)`.
- КОЛИ `input(cook, recipe)` → ЯКЩО `has(diggy, ingredients)` → ТО `custom: «кухня готує страву за час»`, далі `give(diggy, food)`.
- Перемога: виконати квест шахти / розкопати всі клітини · Поразка: нема, лише нестача енергії · Рахунок: досвід, рівень, монети, відсоток очищення шахти.

## Керування і ввід
- Клік / тап по клітині — Diggy сам іде й копає (`control: indirect`); клік по скрині, важелю, NPC — взаємодія.
- Їжа — з інвентаря кліком; табір — розстановка будівель перетягуванням (?).

## Вікна, меню, HUD
- `map-window`: мапа світу з регіонами й шахтами; події — окремі вкладки.
- `game-screen`: шахта; HUD — `energy-bar` (поточна / максимум), `coins`, геми, рівень і досвід, кнопка їжі; над клітинами — `tile-cost-label`.
- `camp-screen` (`custom-window`): табір із будівлями, кухня, караван, ливарня (?), декор.
- `shop-window`: обладнання табору, декор, пакети регіону, спецпропозиції.
- `inventory-window`: матеріали, їжа, інгредієнти.
- `confirm-dialog`: реклама за енергію; `dialogue-window`: діалоги NPC; `achievements-window`.
- Переходи: map-window → шахта → (вихід) map-window / табір.

## Фічі поза полем
- `level-unlock` регіонами й квестами; повторювані шахти; сезонні події з власними шахтами й магазином.
- `achievements`, `xp-level`; геми — преміум-валюта; реклама за енергію (3/день); соцфункції — друзі на Facebook (?).
- `cloud-save` — гра онлайн, прогрес на сервері.

## Варіації й родичі
- У сімʼї: [motherload.md](motherload.md), [steamworld-dig.md](steamworld-dig.md), [dome-keeper.md](dome-keeper.md) — копання з ресурсом-таймером рейсу; [mr-driller.md](mr-driller.md) — повітря як лічильник; тут ресурс — енергія з реальним часом, без гравітації.
- Поза сімʼєю: F2P-енергія як у Candy Crush / Puzzle & Dragons (`falling-match`), але витрачається поклітинно, а не за вхід.
- **Осі варіацій**: ціна дії «фіксована / за клітину / за тип клітини»; відновлення «з часом / їжею / рекламою / будівлями»; видимість цін «усіх / лише поруч (приховані стіни)».

## Цікавинки для курсу
- Ціна клітини + найдешевший маршрут до цілі (Dijkstra з вагами-енергією) — 🥉.
- Енергія з регенерацією за реальним часом і межею, нарахування офлайн за різницею часу — 📎.
- Велика плита, що коштує більше за місткість без апгрейдів, — змушує «копити» — 🌱.
- Приховані стіни: ціна відкривається лише поруч — 🌱.
- Будівлі табору як множники економіки (місткість vs регенерація) — 📎.
- Множник ціни за регіоном (геометрична прогресія) — 🌱.

## Мапа на каталог
- Є: `cell-click` ↔ клік по клітині · `dig-terrain` + `destructible-blocks` ↔ порода → прохід · `impassable-cells` ↔ стіни · `multi-cell-size` ↔ великі плити · `hidden-under-block` ↔ скрині за прихованими стінами · `item-pickup` · `inventory` + `inventory-items` ↔ їжа · `key-and-door` · `button-toggle` ↔ важелі й кнопки · `collect-all` ↔ повне очищення · `round-currency` ↔ монети · `shop-catalog` + `shop-window` · `world-map` + `map-window` · `level-unlock` · `achievements-window` · `save-autosave`.
- **Нема** → пропозиції карток:
  - `+tile-energy-cost` «Кожна клітина має ціну в енергії» · game-logic/economy · 🌱 · слот {cost_by_type}.
  - `+energy-capacity-buildings` «Будівлі збільшують місткість і регенерацію» · game-logic/economy · 📎.
  - `+ad-reward-energy` «Ресурс за перегляд реклами з денним лімітом» · game-logic/economy · 🌱 · слот {per_day: 3}.
  - `+reachable-dig` «Копати можна лише досяжну з проходу клітину» · entities/legality · 📎.
  - Повтори: `+stamina-energy` (Puzzle & Dragons — енергія з часом), `+cost-scaling` (множник за регіоном), `+craft-at-station` (кухня).

## Пропозиції до словників
- `+cond:reachable` — до клітини веде прохід розкопаними клітинами (≈ `path_exists`, але до межі розкопаного).
- `+effect:regen` — поповнення ресурсу на N за період до максимуму.
- `+ui:tile-cost-label` — число-ціна над клітиною.
- `+window:camp-screen` — база/табір між рівнями з будівлями.
- `+feature:ad-reward` — перегляд реклами за ресурс із денним лімітом.

## Джерела
- ⭐ [TouchTapPlay: гайд](https://www.touchtapplay.com/diggys-adventure-cheats-tips-strategy-guide/) — енергія як основний ресурс, маршрут без зайвих клітин, скрині й глеки, два типи будівель, приховані стіни з числом, кухня й караван.
- [Pixel Federation: About](https://portal.pixelfederation.com/en/diggysadventure/about) — шахти, логічні пазли, лабіринти, квести, табір, регіони.
- [Diggy's Guide: ріст ціни в регіонах](https://diggysguide.com/guides/tackling-energy-cost-increase-in-new-region) — множники регіонів, кухня, обладнання.
- [Diggy's Guide: Encrypted Black Tower](https://diggysguide.com/7th-birthday/encrypted-black-tower) — 186 клітин, ціни рівнів 2 000 … 230 000 енергії, бонус за очищення, важелі, кнопки-світло, ключ, ворота.
- [LevelWinner: гайд](https://www.levelwinner.com/?p=7968) — час і енергія, табір, кухня, персонажі.
- Сніпети пошуку з wiki.diggysadventure.com (сторінки Energy, How_to; у фетчі 402): старт 200 енергії, великі плити «напр. 600», реклама 3 рази на день, синє обладнання — місткість, зелене — регенерація, регенерація офлайн.
- Сніпети AppGamer (у фетчі 403): важелі відкривають нові ділянки, жовті блоки, Diggy з татом стають на червоні кнопки.

## Непевне
- (?) Чи Diggy має бути поруч із клітиною, чи копає будь-яку досяжну проходом; як саме шукається шлях.
- (?) Чи їжа може підняти енергію понад максимум.
- (?) Старт 200 енергії і плита «600» — лише зі сніпета вікі.
- (?) Розміщення будівель табору (сітка? перетягування?), ливарня, караван — деталі не перевірено.
- (?) Кнопки «вдвох» і «світло» — зі сніпетів проходжень окремих шахт, не загальне правило.
- (?) Огляд Gamezebo (⭐ черги, 2012-10-05) не відкрився — 403; рік 2012 — з Wikipedia Pixel Federation.
