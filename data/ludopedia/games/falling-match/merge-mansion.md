---
title: Merge Mansion / Merge Dragons
slug: merge-mansion
aka: [Merge Dragons!, merge-жанр, merge-2, merge-3]
family: falling-match
also: [build-sim]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: runtime
  goal: collect
year: 2020
platforms: [iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Merge_Mansion", best: true, note: "Merge Mansion: злиття двох однакових → наступний предмет, реставрація, розповідь"}
  - {kind: official, url: "https://www.mergemansion.com/", note: "офіційний сайт Merge Mansion"}
  - {kind: other, url: "https://support.metacoregames.com/hc/en/merge-mansion", note: "help-центр Metacore: продюсери, кулдаун, енергія, продаж, павутиння, скрині, задачі"}
  - {kind: other, url: "https://apps.apple.com/us/app/merge-mansion/id1484442152", note: "App Store: задачі, кімнати, події, сховище"}
  - {kind: other, url: "https://www.pocketgamer.com/merge-dragons/hatch-dragons-eggs-to-heal-the-land-in-the-pretty-puzzler-merge-dragons-out-now/", note: "Merge Dragons (2017): яйця → дракони, лікування землі, рівень = 3 статуї Гаї"}
  - {kind: other, url: "https://play.google.com/store/apps/details?id=com.gramgames.mergedragons", note: "Merge Dragons! у Google Play (Gram Games)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=merge+mansion+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [tile-merge, drag-drop-piece, spawner-entity, weighted-spawn, round-currency, shop-window, shop-catalog, inventory-limit, save-autosave, map-window, world-map, objective-text, goal-counter, collect-quota, tutorial-window, undo-step, +merge-chain-tiers, +producer-cooldown, +order-fulfillment, +sell-item, +locked-item-cobweb, +board-full-block, +energy-regen, +auto-merge-toggle, +merge-arity]
proposes: ["+axis:merge-arity", "+effect:sell", "+feature:energy-regen", "+window:task-list", "+ui:order-chips", "+ui:cooldown-clock", "+card:producer-cooldown", "+card:order-fulfillment", "+card:locked-item-cobweb"]
author: opus
date: 2026-11-09
---

# Merge Mansion / Merge Dragons — тягни однаковий предмет на однаковий: вони зливаються в наступний рівень ланцюга, а продюсери дають сировину

## Суть
Гравець на «дошці злиття» тягне предмет на такий самий: два (Merge Mansion) або три (Merge Dragons) однакові предмети стають одним предметом наступного рівня свого ланцюга (два ножі → секатор). Сировину дають продюсери: тап по продюсеру (бочка з інструментами) кладе випадковий предмет у вільну клітину, а спорожнілий продюсер іде на кулдаун. Злиті предмети потрібні для **задач** (замовлень), а виконані задачі відкривають кімнати маєтку й сюжет. Відмінність від Triple Town: поле вільне — предмет можна перетягнути куди завгодно, злиття — дія гравця, а не наслідок розміщення.

## Поле і час
- Merge Mansion: одна квадратна «Merge Board» з клітинами-слотами; частина клітин на старті закрита (предмети в павутинні, скрині), відкривається злиттям (?). Події мають окрему дошку (відгук App Store).
- Merge Dragons: поле — земля з клітинами; «мертва» (сіра) земля лікується блок за блоком; великі обʼєкти займають кілька клітин (?).
- Час — real-time з паузами: ходів нема, але є кулдауни продюсерів і відновлення енергії в реальному часі (`time: realtime`). Між сесіями гра триває (кулдауни тікають офлайн) (?).
- Що дасть продюсер — випадково (`random: runtime`); наступний предмет не видно (`info: partial`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Предмет ланцюга | tile | ланцюг, рівень | зливається з однаковим (ланцюг + рівень) у предмет рівня +1 |
| Вершина ланцюга | tile | максимальний рівень | далі не зливається; часто стає продюсером або потрібна в задачі (?) |
| Продюсер (Tool Barrel, Toy Car) | spawner | заряди, кулдаун | тап → випадковий предмет свого ланцюга в найближчу вільну клітину; порожній → кулдаун |
| Продюсер на кулдауні | spawner | таймер | годинник у кутку; не виробляє; пропуск кулдауну — за самоцвіти |
| Предмет у павутинні | tile | заблокований | не рухається; звільняється злиттям з однаковим предметом |
| Скриня | container | вміст | відкрита скриня видає предмети лише у вільні клітини; нема місця — не видає |
| Порожня клітина | terrain | — | сюди кладуться предмети з продюсерів і скринь |
| Задача (замовлення) | zone | список предметів | показує потрібні предмети; виконана → прогрес кімнати/сюжету |
| Енергія | resource | запас | витрачається на тапи продюсерів (?); купується за самоцвіти або за рекламу |
| Монети | resource | — | за продаж предметів; витрачаються в магазині (?) |
| Самоцвіти (gems) | resource | — | преміум-валюта: енергія, пропуск кулдауну, сховище |
| Сховище (storage) | container | слоти | тримає предмети поза дошкою; слоти купуються за золото/самоцвіти |
| Яйце дракона (MD) | tile | рівень | злиття яєць → дракон (Merge Dragons) |
| Дракон (MD) | ally | рівень | збирає/лікує сам (?); зливається з такими ж драконами |
| Мертва земля (MD) | terrain | — | лікується злиттям поруч із нею (?) — блок за блоком |
| Статуя Гаї (MD) | tile | — | злиття 3 статуй = перемога на рівні (Merge Dragons) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag a onto b)` → ЯКЩО `same(a, b, chain_and_tier)` → ТО `merge(a, b → tier+1)` у клітині `b` (Merge Mansion: 2 → 1).
- КОЛИ `input(drag a onto b)` → ЯКЩО `not same(a, b, chain_and_tier)` → ТО `swap(a, b)` або `move(a, cell_b)` (?).
- КОЛИ `input(drop a)` → ЯКЩО `pattern(group(3))` з однакових сусідніх → ТО `merge(group → tier+1)` у клітині скидання (Merge Dragons: 3 → 1).
- КОЛИ `input(drop a)` → ЯКЩО `pattern(group(5))` → ТО `custom: «5 однакових → 2 предмети вищого рівня замість 1 (бонус за терпіння)»` (Merge Dragons).
- КОЛИ `input(tap producer)` → ЯКЩО `counter(energy, >, 0)` і `count(free_cells, >, 0)` → ТО `spawn_at(item_of_chain, nearest_free)` (`custom: «зважений випадок рівня 1–2»`), `counter(energy, -1)` (?).
- КОЛИ `input(tap producer)` → ЯКЩО `count(free_cells, ==, 0)` → ТО `block` (дошка повна — нічого не зʼявляється).
- КОЛИ `counter(producer_charges, ==, 0)` → ТО `set_state(producer, cooldown, dur)`; КОЛИ `state_off(producer, cooldown)` → ТО заряди відновлено.
- КОЛИ `input(pay gems on producer)` → ТО `clear_state(producer, cooldown)`, `currency(-n)`.
- КОЛИ `input(drag a onto cobwebbed b)` → ЯКЩО `same(a, b, chain_and_tier)` → ТО `merge(a, b → tier+1)` і павутиння зникає.
- КОЛИ `input(tap open chest)` → ЯКЩО `count(free_cells, >, 0)` → ТО `spawn_at(chest_item, free_cell)`; інакше `block`.
- КОЛИ `input(sell item)` → ЯКЩО `custom: «предмет продається (не продюсер-особливий)»` → ТО `disappear(item)`, `currency(+coins)`; кнопка undo живе обмежений час і повертає лише останній продаж.
- КОЛИ `input(deliver items to task)` → ЯКЩО `has(board, required_items)` → ТО `take(board, required_items)`, `custom: «задача виконана → відкрито ділянку маєтку / сюжетну сцену»`.
- КОЛИ `counter(energy, ==, 0)` → ТО `window(shop-window)` з пропозицією енергії за самоцвіти або за рекламу.
- КОЛИ `timer(every)` → ТО `counter(energy, +1)` до стелі (?).
- КОЛИ `custom: «злиття поруч із мертвою землею»` → ТО `set_cell(dead_land, healed)` (Merge Dragons) (?).
- КОЛИ `pattern(match(gaia_statue, 3))` → ТО `win` рівня (Merge Dragons).
- Перемога: Merge Mansion — нема (нескінченна реставрація задачами); Merge Dragons — рівень за 3 статуями Гаї. Поразка: нема; глухий кут — повна дошка без злиттів (продати/сховати). Рахунок: нема, замість нього прогрес кімнат і події з очками й лідербордом.

## Керування і ввід
- Drag-n-drop предмета на інший предмет (злиття) або в порожню клітину (перестановка).
- Тап по продюсеру — виробити; тап по предмету — панель з описом і ціною продажу; тап по скрині — видати вміст.
- Список задач (галочка внизу праворуч) або чипи задач над дошкою; карта маєтку — скрол.
- Auto-Merge — перемикач на верху списку задач (лише поки функція активна) (?) — сам зливає предмети для задачі.

## Вікна, меню, HUD
- `game-screen`: Merge Board, чипи поточних задач зверху (`+ui:order-chips`), енергія (`energy-bar`), монети й самоцвіти (`coins`), годинник кулдауну на продюсері (`+ui:cooldown-clock`), сховище (`inventory-bar`).
- `map-window`: маєток і сад з ділянками, де видно доступні задачі.
- `+window:task-list`: прокручуваний список задач усіх ділянок і подій з потрібними предметами.
- `shop-window`: енергія, самоцвіти, паки, пропуски (Season / Mystery Pass).
- `inventory-window`: сховище зі слотами, що купуються.
- `custom-window`: панель предмета — опис, ціна продажу, кнопка продати.
- `dialogue-window`: сюжетні сцени з Мадді й бабусею Урсулою.
- `tutorial-window`: перші злиття з підказками (?).
- Переходи: map-window ↔ game-screen → task-list → game-screen; енергія 0 → shop-window.

## Фічі поза полем
- `cloud-save`/`autosave` — одна довга партія.
- `meta-progression`: кімнати й сад відкриваються задачами, декорації — косметика.
- Події: окрема дошка, очки, лідерборд, нагороди (`leaderboard-online`).
- Монетизація: самоцвіти, енергія, пропуск кулдауну, реклама за енергію, Season Pass.
- Merge Dragons: десятки рівнів-карт з окремим табором (camp) як постійною базою (?).

## Варіації й родичі
- **Triple Town** (`triple-town.md`) — предок «3 → наступний рівень»; але там предмет приходить у руку, злиття — від розміщення, поле 6×6 і ведмеді; тут — вільне перетягування, продюсери, задачі й енергія.
- 2048 (`2048.md`), Threes, Suika (`suika-game.md`) — злиття однакових іншими способами (свайп поля, гравітація фізики).
- Match3-meta-renovation (`match3-meta-renovation.md`) — та сама мета «відремонтуй маєток», але ядро — match-3, а не merge.
- Інші merge-ігри: EverMerge, Merge Magic!, Gossip Harbor, Travel Town (?).
- **Осі варіацій**: арність злиття (2 → 1 / 3 → 1 / 5 → 2) · звідки сировина (продюсер-тап / рука / таймер) · обмеження (енергія / кулдаун / місце) · мета (задачі-замовлення / рівень-ціль / рахунок) · де результат (клітина цілі / клітина скидання).

## Цікавинки для курсу
- Злиття drag-on-target з ланцюгами рівнів як дані (таблиця `chain → [tiers]`) — 🌱.
- Merge-3 з бонусом 5 → 2: flood fill групи навколо скинутого предмета + арифметика `n // 5 * 2 + n % 5 // 3` (?) — 📎.
- Продюсер із зарядами й кулдауном у реальному часі (працює і офлайн через timestamp) — 📎.
- Задачі-замовлення: перевірка «чи є на дошці потрібні предмети» і списання — 📎.
- Повна дошка як головний ресурс: спавн у найближчу вільну клітину (BFS від продюсера) — 📎.
- Продаж з одноразовим undo на обмежений час — 🌱.
- Мета-шар «маєток» з відкриттям ділянок за задачами — 🥉.

## Мапа на каталог
- Є: `tile-merge` (2/3 однакових → рівень +1) · `drag-drop-piece` · `spawner-entity` (продюсер) · `weighted-spawn` · `round-currency` + `shop-window` + `shop-catalog` · `inventory-limit` (сховище) · `save-autosave` · `map-window` + `world-map` (маєток / карти MD) · `objective-text` + `goal-counter` + `collect-quota` (задачі) · `tutorial-window` · `undo-step` (лише продаж).
- **Нема** → пропозиції карток:
  - `+merge-chain-tiers` «Ланцюги предметів з рівнями як таблиця» · entities/legality · 🌱.
  - `+producer-cooldown` «Генератор із зарядами й кулдауном у реальному часі» · entities/spawn · 📎.
  - `+order-fulfillment` «Задача-замовлення: здай N предметів» · game-logic/win · 📎.
  - `+sell-item` «Продати предмет з поля за валюту» · game-logic/economy · 🌱.
  - `+locked-item-cobweb` «Заблокований предмет, що звільняється злиттям» · entities/interact · 🌱.
  - `+board-full-block` «Повне поле блокує спавн, а не програє» · entities/spawn · 🌱.
  - `+energy-regen` «Енергія на дії, відновлюється з часом» · game-logic/economy · 📎 (споріднено з `+turn-limit-energy` Triple Town).
  - `+auto-merge-toggle` «Автозлиття для задачі» · interface/input · 📎.
  - `+merge-arity` «Скільки однакових зливається і скільки виходить» · entities/legality · 🌱 слоти {in: 2|3|5, out: 1|2}.

## Пропозиції до словників
- `+axis:merge-arity` — `2to1` · `3to1` · `5to2` (Merge Mansion, Merge Dragons, Triple Town, 2048).
- `+effect:sell` — прибрати предмет з поля за валюту (Merge Mansion; також TD-ігри продають вежі).
- `+feature:energy-regen` — дії коштують енергію, що відновлюється в реальному часі.
- `+window:task-list` — список задач-замовлень з потрібними предметами.
- `+ui:order-chips` — чипи поточних замовлень над полем · `+ui:cooldown-clock` — годинник на сутності з кулдауном.
- `+card:producer-cooldown` · `+card:order-fulfillment` · `+card:locked-item-cobweb` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Merge Mansion](https://en.wikipedia.org/wiki/Merge_Mansion) — Metacore, 2020; два однакові предмети → новий (ножі → секатор, лампочки → ліхтар), реставрація маєтку й сюжет.
- [Metacore help: Merge Mansion](https://support.metacoregames.com/hc/en/merge-mansion) — статті: кулдаун продюсерів (годинник, пропуск за самоцвіти), енергія (купівля за самоцвіти / рекламу), продаж з undo, павутиння, скрині на повній дошці, список задач, Auto-Merge.
- [App Store: Merge Mansion](https://apps.apple.com/us/app/merge-mansion/id1484442152) — задачі відкривають кімнати, події з лідербордом, сховище зі слотами (відгуки).
- [Pocket Gamer: Merge Dragons! out now](https://www.pocketgamer.com/merge-dragons/hatch-dragons-eggs-to-heal-the-land-in-the-pretty-puzzler-merge-dragons-out-now/) — Gram Games, червень 2017; яйця → дракони, лікування землі блоками, рівень = злиття 3 статуй Гаї, 500+ обʼєктів, 600+ квестів.
- [Google Play: Merge Dragons!](https://play.google.com/store/apps/details?id=com.gramgames.mergedragons) — сторінка застосунку (опис не прочитався).
- YouTube: пошук «merge mansion gameplay».

## Непевне
- (?) Правило Merge Dragons «3 → 1, 5 → 2» — з рядка черги й памʼяті; відкрите джерело (fandom 402, Wikipedia-статті нема) не підтвердило.
- (?) Чи кожен тап по продюсеру коштує 1 енергію, швидкість і стеля відновлення енергії.
- (?) Що стається при скиданні неоднакового предмета на предмет (обмін місцями чи відмова).
- (?) Механіка драконів (збирання, лікування), табору й мертвої землі в Merge Dragons — з памʼяті.
- (?) Монети й магазин Merge Mansion: на що саме витрачаються монети (стаття є, тіло не прочитано).
- Fandom-вікі обох ігор віддали 402; WebSearch-бюджет сесії вичерпано до першого запиту.
