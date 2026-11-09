---
title: Hexa Sort
slug: hexa-sort
aka: [Hexa Stack, hex stack sort, гекса-сортування]
family: falling-match
also: []
klass: cursor
axes:
  field: hex
  time: turn
  opponent: none
  info: partial
  random: runtime
  goal: collect
year: 2023
platforms: [Android, iOS, web]
links:
  - {kind: play, url: "https://www.crazygames.com/game/hexa-sort", best: true, note: "грати в браузері; опис: 19 клітин, шари, верхні шари зливаються першими, каскади"}
  - {kind: other, url: "https://apps.apple.com/us/app/hexa-sort/id6463127238", note: "App Store: Lion Studios Plus, цілі збору, бустери, IAP (Hammer, Refresh, Lives)"}
  - {kind: other, url: "https://play.google.com/store/apps/details?id=com.gamebrain.hexasort", note: "Google Play: «sort the hexagon tile blocks by color to merge them»"}
  - {kind: official, url: "https://lionstudios.cc/games/", note: "Lion Studios — видавець"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=hexa+sort+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [drag-drop-piece, cursor-place, tile-merge, chain-reaction, next-queue, collect-quota, goal-counter, sequential-levels, level-unlock, world-map, round-currency, shop-window, no-moves-left, player-death, popup-text, +stack-top-merge, +stack-clear-threshold, +locked-cell-unlock, +remover-item, +offer-refresh]
proposes: ["+effect:transfer_run", "+cond:top_same", "+card:stack-top-merge", "+card:stack-clear-threshold", "+card:locked-cell-unlock", "+ui:stack-height-label", "+feature:lives-regen"]
author: opus
date: 2026-11-09
---

# Hexa Sort — став стопку гексів на поле: верхні шари одного кольору перетікають до сусідів, а висока одноколірна стопка зникає

## Суть
Гравець бере одну з кількох запропонованих стопок шестикутних плиток і ставить її на вільну клітину гекс-поля. Після розміщення верхні плитки одного кольору перетікають між сусідніми стопками з тим самим верхнім кольором: плитки «сортуються», відкриваючи кольори під ними, і з цього виникають каскади. Коли одноколірна верхівка стопки досягає порогу, вона зникає й дає прогрес до цілі рівня. Програш — поле заповнене, а місця для нової стопки нема. Незвичне: злиття не «2 → 1», а **перекладання серій** між стопками-контейнерами (гібрид Water Sort і Triple Town на гексах).

## Поле і час
- Гекс-поле; у браузерній версії — 19 клітин (гекс зі стороною 3: 1 + 6 + 12). На вищих рівнях поле інше й має закриті клітини (?).
- Кожна клітина — стопка шарів (вертикальний стек кольорових гексів); видно лише бічний профіль, тож колір нижніх шарів видно частково (`info: partial`) (?).
- Покроково: хід = поставити стопку; далі каскад перетікань до стабілізації, без часу.
- Новий набір стопок для вибору — випадковий (`random: runtime`).
- 3D-рендер, поле можна оглядати під різними кутами (App Store).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гекс-плитка | tile | колір | шар стопки; разом з однаковими зверху утворює «серію» |
| Стопка | container | список шарів (знизу вгору) | приймає й віддає верхню серію; зникає, коли спорожніла |
| Запропонована стопка | supply | 2–6 шарів (?) | лежить у лотку внизу; drag на вільну клітину |
| Лоток пропозицій | supply | 3 слоти (?) | поповнюється, коли всі стопки використано (?) |
| Клітина поля | terrain | вільна / зайнята | тримає одну стопку |
| Закрита клітина | gate | поріг очок / оплата (?) | недоступна, доки не відкрита |
| Ціль рівня | zone | колір/кількість | лічильник зібраних плиток |
| Молоток (Hammer) | pickup | бустер | прибирає вибрану стопку (?) |
| Refresh | pickup | бустер | замінює пропоновані стопки новими (?) |
| Життя | resource | запас | програний рівень забирає життя; купуються (Free Lives Bundle) |
| Монети | resource | — | купівля бустерів, продовження (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag stack onto cell)` → ЯКЩО `free(cell)` → ТО `place(player, stack)`; інакше `block`.
- КОЛИ `after(place)` → ЯКЩО `same(stack, neighbor, top_color)` → ТО `custom: «transfer_run — верхня серія одного кольору перетікає в сусідню стопку»` (напрям — до стопки, що дає далі збіг) (?).
- КОЛИ `after(transfer)` → ЯКЩО у віддавальної стопки відкрився новий верхній колір і `same(stack, other_neighbor, top_color)` → ТО знову `custom: «transfer_run»` (каскад, `chain(n)`).
- КОЛИ `after(transfer)` → ЯКЩО `custom: «верхня серія одного кольору ≥ порогу»` (10 (?)) → ТО `clear(run)`, `counter(goal_color, +n)`, `score(+n)`.
- КОЛИ `after(clear)` → ЯКЩО `custom: «стопка порожня»` → ТО `disappear(stack)` — клітина вільна.
- КОЛИ `settled` → ЯКЩО `custom: «лоток порожній»` → ТО `spawn_at(new_stacks, tray)` (?).
- КОЛИ `counter(goal, >=, n)` → ТО `win` рівня → `next_level`.
- КОЛИ `settled` → ЯКЩО `count(free_cells, ==, 0)` → ТО `lose` (`custom: «можна продовжити за монети / рекламу»` (?)), `lives(-1)`.
- КОЛИ `counter(score, >=, n)` → ЯКЩО `occupied(cell, locked)` → ТО `custom: «закрита клітина відкривається»` (?).
- КОЛИ `input(use hammer, stack)` → ТО `disappear(stack)` (?).
- КОЛИ `input(use refresh)` → ТО `custom: «нові стопки в лотку»` (?).
- Перемога: зібрати квоту плиток рівня. Поразка: повне поле без розвʼязку. Рахунок: зібрані плитки / очки, рівні послідовно.

## Керування і ввід
- Ліва кнопка миші / палець: перетягнути стопку з лотка на клітину; відпущення над вільною клітиною — хід.
- Тап по бустеру → тап по цілі (молоток) або одразу (refresh) (?).
- Огляд поля — поворот камери (3D) (?).

## Вікна, меню, HUD
- `game-screen`: гекс-поле, лоток зі стопками (`next-tile-preview`), ціль рівня (`progress-bar`/`objective-text`), висота стопки цифрою над нею (`+ui:stack-height-label`) (?), бустери (`ability-buttons`), монети (`coins`), рівень (`level-number`).
- `map-window`: сезонна мапа рівнів (koi-сезон, Special Meta Worlds з release notes).
- `end-screen`: рівень пройдено / нема місця (пропозиція продовжити).
- `shop-window`: паки монет, Piggy Bank, Spin Wheel (`custom-window` — колесо), Hammer/Refresh/Lives bundles.
- `settings-window`: звук, вібрація (?).
- Переходи: map-window → game-screen → end-screen → map-window.

## Фічі поза полем
- `levels-sequential` + `world-map` з сезонами; `meta-progression` (Meta Worlds) (?).
- Життя з відновленням у часі (`+feature:lives-regen`) (?); Spin Wheel — щоденна нагорода (?).
- Монетизація: монети, бустери, реклама.

## Варіації й родичі
- **Water Sort** (`water-sort.md`) — та сама ідея «стопка-контейнер, верхня серія одного кольору переливається»; там переливає гравець, тут — автоматично між сусідами після розміщення.
- **Triple Town** (`triple-town.md`) — розміщення предмета з руки, злиття з сусідами; тут злиття — перетікання шарів.
- **2048** (`2048.md`), **Drop7** (`drop7.md`) — злиття/очищення через поріг значення.
- Інші «hexa stack»: Hexa Stack, Hexa Puzzle (?), Bus Jam-подібні сортування.
- **Осі варіацій**: поле (гекс / квадрат) · хто переносить (гравець / автомат після ходу) · поріг очищення (фіксований / зростає) · напрям перетікання (до новоставленої / від неї / до найвищої) · лоток (1 / 3 стопки, чи можна відкласти).

## Цікавинки для курсу
- Стопка як стек кольорів + «верхня серія» (run-length верхівки) — 🌱.
- Перетікання між сусідами на гекс-сітці (осьові координати, 6 сусідів) — 📎.
- Каскад перетікань до стабілізації з вибором напряму (детермінізм порядку обходу) — 🥉.
- Поріг очищення і ціль рівня за кольорами — 🌱.
- Генератор пропозицій, що не робить рівень нерозвʼязним (зважування кольорів за полем) — 🥈.
- Закриті клітини, що відкриваються за очками — 🌱.

## Мапа на каталог
- Є: `drag-drop-piece` · `cursor-place` (вільна клітина) · `tile-merge` (злиття однакових — тут як перетікання) · `chain-reaction` · `next-queue` (лоток) · `collect-quota` + `goal-counter` · `sequential-levels` + `level-unlock` + `world-map` · `round-currency` + `shop-window` · `no-moves-left` (повне поле) · `player-death` (життя) · `popup-text`.
- **Нема** → пропозиції карток:
  - `+stack-top-merge` «Верхня серія стопки перетікає до сусіда того ж кольору» · entities/interact · 📎 (Hexa Sort, Water Sort).
  - `+stack-clear-threshold` «Серія з N однакових у стопці зникає» · entities/interact · 🌱.
  - `+locked-cell-unlock` «Закрита клітина відкривається за очками/оплатою» · levels/progression · 🌱.
  - `+remover-item` — ⏳ підтверджую (Triple Town bot): молоток.
  - `+offer-refresh` «Замінити запропоновані фігури новими» · entities/spawn · 🌱 (Block Blast, Hexa Sort).

## Пропозиції до словників
- `+effect:transfer_run` — перенести верхню одноколірну серію з однієї стопки в іншу (Hexa Sort, Water Sort, Ball Sort).
- `+cond:top_same` — верхні шари двох стопок одного кольору (поки пишу як `same(a, b, top_color)`).
- `+card:stack-top-merge` · `+card:stack-clear-threshold` · `+card:locked-cell-unlock` — див. «Мапа на каталог».
- `+ui:stack-height-label` — число шарів над стопкою.
- `+feature:lives-regen` — життя на спроби рівня, відновлюються в часі (Candy Crush-модель).

## Джерела
- ⭐ [CrazyGames: Hexa Sort](https://www.crazygames.com/game/hexa-sort) — грати; 19 клітин, кольори, шари («first stack the top layers»), каскади, керування мишею; дати: Android 07.2023, iOS 11.2023.
- [App Store: Hexa Sort](https://apps.apple.com/us/app/hexa-sort/id6463127238) — Lion Studios Plus, © 2023; цілі збору, бустери, 3D-огляд, IAP.
- [Google Play: Hexa Sort](https://play.google.com/store/apps/details?id=com.gamebrain.hexasort) — «sort the hexagon tile blocks by color to merge them».
- [Lion Studios: games](https://lionstudios.cc/games/) — видавець, лінки на магазини.
- YouTube: пошук «hexa sort gameplay».

## Непевне
- (?) Поріг очищення (10 однакових), кількість стопок у лотку (3) і правила поповнення — з памʼяті жанру.
- (?) Напрям перетікання й порядок каскаду при кількох сусідах одного кольору.
- (?) Дія молотка й Refresh (є лише назви IAP-паків), продовження після програшу.
- (?) Як відкриваються закриті клітини і чи поле на рівнях більше за 19.
- Оригінальний автор жанру (Lessmore / Gamebrain?) не встановлено; WebSearch-бюджет вичерпано.
