---
title: Railbound
slug: railbound
family: connect-rotate
also: [thinky, program-robots]
klass: cursor
axes:
  field: iso
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2022
platforms: [PC, Mac, iOS, Android, Switch, Xbox]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Railbound", best: true, note: "механіки по світах (тунелі, стрілки, станції, семафори, два локомотиви), ліміт шматків, дати"}
  - {kind: steam, url: "https://store.steampowered.com/app/1967510", note: "опис: барʼєри, стрілки, тунелі, 240+ пазлів, редактор, Workshop"}
  - {kind: other, url: "https://www.pocketgamer.com/railbound/september-6th/", note: "анонс: railbending — додати/прибрати зʼєднання"}
  - {kind: other, url: "https://www.pcgamer.com/uk/connect-traincars-in-order-in-puzzler-railbound-from-golf-peaks-and-inbento-makers/", note: "PC Gamer: вагони в правильному порядку"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Railbound+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [drag-drop-piece, cell-click, swipe-gestures, teleport-pair, impassable-cells, reach-exit, satisfy-constraints, completion-detection, sequential-levels, level-unlock, level-select, in-game-editor, editor-playtest, level-exchange, save-progress, game-screen, main-menu, settings-window, end-screen, movement-animation, +run-simulation, +track-budget, +ordered-arrival, +collision-fail, +junction-toggle, +button-toggle, +path-cut, +undo-redo, +world-map]
proposes: ["+role:sink", "+role:conduit", "+role:switch", "+role:gate", "+trigger:collide", "+trigger:reach", "+cond:order_next", "+effect:attach", "+effect:place_tile", "+ui:run-button", "+ui:pieces-left", "+axis:time=programmed", "+card:track-budget", "+card:ordered-arrival", "+card:collision-fail", "+card:junction-toggle"]
author: opus
date: 2026-11-02
---

# Railbound — доклади обмежену кількість рейок, щоб вагони приїхали до локомотива по порядку номерів

## Суть
На ізометричній сітці вже лежать шматки колії, стоять нумеровані вагони (1–4) і локомотив. Гравець докладає (і прибирає) обмежену кількість рейок, потім запускає симуляцію: усі вагони рушають **одночасно**, по клітині за тік, і мають причепитися до локомотива **в порядку номерів**, не зіткнувшись і не зійшовши з колії. Рейка — єдиний елемент, який ставить гравець; уся виразність — у стрілках, тунелях, барʼєрах і таймінгу.

## Поле і час
- Ізометрична квадратна сітка невеликого розміру; клітини — порожні (можна класти рейку), зайняті декорацією/перешкодою, з наперед заданою колією (не змінюється) (?).
- Дві фази: **планування** (статичне редагування колії) і **симуляція** (тік = кожен вагон зсувається на 1 клітину). Під час симуляції редагувати не можна; стоп повертає все на старт.
- 150+ (Wikipedia) / 240+ (Steam, з оновленнями) рівнів у «світах»: ~10 базових на світ + бонусні за розвилками.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Локомотив | sink (custom) | позиція, напрям прийому | нерухомий до зчеплення всіх; вагон, що заїхав ззаду, чіпляється |
| Вагон | object | номер 1–4, напрям старту | рухається по колії щотік; має приїхати в свою чергу |
| Рейка (пряма/поворот) | conduit (custom) | 2 порти | ставиться гравцем drag-ом; форма — з напрямку протягування |
| Задана рейка | static | — | частина рівня; гравець не змінює (?) |
| Стрілка (junction switch) | switch | 3 порти, поточна гілка | вагон зі стовбура їде в поточну гілку; після проїзду стрілка перемикається (?) |
| Тунель | terrain | пара входів | вагон заходить в один, виходить з іншого — коротший шлях між далекими точками |
| Барʼєр (переїзд) | gate | відкрито/закрито | затримує вагон, доки відкритий за таймінгом/подією (?) |
| Ворота + важіль | gate + switch | звʼязані | проїзд по важелю перемикає ворота (?) |
| Нумерована станція | static | номер | вагон має зупинитись/проїхати через станцію, щоб забрати пасажира, перш ніж до локомотива (?) |
| Семафор (оновлення 2.0) | gate | — | ставиться гравцем, тримає вагон, доки... (?) |
| Другий локомотив (оновлення 3.0) | sink | своя черга вагонів | два потяги збираються паралельно |
| Перешкода/декор | static | — | рейку не покласти |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, cells)` → ЯКЩО `free(cell)` and `counter(pieces_left, >, 0)` → ТО `place_tile(rail)`, `counter(pieces_left, -1)`; повернення по своїх рейках — прибрати їх (`counter(+1)`).
- КОЛИ `input(drag)` через наявну рейку в нову сторону → ТО `transform(rail, junction)` — так зʼявляється стрілка.
- КОЛИ `input(run)` → ТО `custom: «фаза симуляції»`; КОЛИ `input(stop)` → ТО `restart` до стану планування (колія зберігається).
- КОЛИ `tick` → ТО `move(car, next_rail)` для **всіх** вагонів одночасно.
- КОЛИ `enter(car, junction)` зі стовбура → ТО `move(car, current_branch)`; після проїзду `set_state(junction, flip)` (?).
- КОЛИ `enter(car, tunnel)` → ТО `teleport(car, tunnel_pair)`.
- КОЛИ `contact(car, barrier)` → ЯКЩО `state(barrier, closed)` → ТО `block` (вагон чекає).
- КОЛИ `enter(car, lever)` → ТО `set_state(gate, flip)` (?).
- КОЛИ `collide(car, car)` → ТО `lose` (симуляція зупиняється, місце аварії підсвічене).
- КОЛИ `blocked(car)` (кінець рейки) → ТО `lose` (сходження).
- КОЛИ `reach(car[n], locomotive)` → ЯКЩО `order_next(n)` → ТО `attach(car, train)`; інакше `lose`.
- КОЛИ `count(cars_attached, ==, total)` → ТО `win`, `custom: «потяг від'їжджає»`, `unlock(next)`.
- Перемога: усі вагони причеплені по порядку (і на станціях забрані пасажири, де є). Поразка — лише в симуляції, без покарання: повернення в планування. Рахунку нема.

## Керування і ввід
- Tap-and-drag по клітинах: тягнеш — кладеш рейку; форма (пряма, поворот, стрілка) визначається траєкторією.
- Перетягнути назад або клік по рейці — прибрати; кнопки «Go/Stop» (запуск симуляції), прискорення, undo, рестарт рівня (?).
- PC — миша, мобільні — тач, консолі — курсор геймпадом.

## Вікна, меню, HUD
- `main-menu`: Грати → мапа світу; Редактор (PC) → `editor-window`; Workshop; Налаштування; Вихід.
- `world-map` / `level-select`: маршрут подорожі собак світом; вузли-рівні, розвилки до бонусних.
- `game-screen`: поле, `pieces-left` (скільки рейок лишилось), `run-button`, `undo-button`, `restart-button`, `speed-slider`/`fast-forward` (?).
- `end-screen`: потяг від'їжджає, наступний рівень.
- `settings-window`: мова (11 мов), звук, музика.
- `editor-window` (PC): палітра елементів, тест рівня, публікація у Steam Workshop.
- Переходи: мапа → game-screen ⇄ симуляція → (успіх) end-screen → мапа.

## Фічі поза полем
- `levels-sequential` + `level-unlock` + `world-map` з бонусними гілками.
- `level-editor`, `level-sharing` через Steam Workshop, `user-levels-browser`.
- `undo`, `restart-level`, `autosave`/`cloud-save`, `achievements`.
- Оновлення як контент: 2.0 (лютий 2023) — семафори; 3.0 — два локомотиви.

## Варіації й родичі
- Родичі: Cosmic Express (одна колія, пасажири за сусідством), Trainyard (поїзди фарбуються, зливаються), Golf Peaks / inbento (ті самі автори, Afterburn), «shunting puzzles» (сортування вагонів).
- Осі варіацій: **хто рухається: один потяг / всі одночасно** · **ресурс: ліміт рейок / вільно** · **мета: порядок / колір / пасажири** · **стрілка: перемикається після проїзду / фіксована / важелем** · **таймінг: барʼєри / семафори / тунелі як «скорочення часу»**.

## Цікавинки для курсу
- Дві фази «план → симуляція» з поверненням у план при невдачі — 🥉 (стан як дані, reset).
- Одночасний рух N вагонів по тіках і виявлення зіткнень (лоб у лоб, обмін клітинами) — 🥉.
- Перевірка порядку прибуття (черга номерів) — 🌱.
- Стрілка, що перемикається після кожного проїзду — 📎 (класичний «toggle junction» з Trainyard).
- Форма рейки з траєкторії drag-у (пряма/поворот/стрілка) — 📎.
- Розвʼязувач з лімітом рейок: перебір розміщень + симуляція — 🥇.

## Мапа на каталог
- Є: `drag-drop-piece`/`cell-click`/`swipe-gestures` (ввід) · `teleport-pair` (тунелі) · `impassable-cells` · `reach-exit`, `satisfy-constraints`, `completion-detection` · `sequential-levels`, `level-unlock`, `level-select` · `in-game-editor`, `editor-playtest`, `level-exchange` (Workshop) · `save-progress` · `movement-animation` · `game-screen`, `main-menu`, `settings-window`, `end-screen`.
- **Нема** → пропозиції карток:
  - `+run-simulation` «План → запуск симуляції» · game-logic · 🥉 — спільне з Cosmic Express.
  - `+track-budget` «Ліміт елементів, які ставить гравець» · game-logic/constraints · 🌱 · слот {pieces}.
  - `+ordered-arrival` «Прибуття в заданому порядку» · game-logic/win · 🌱 · слот {order: by_number}.
  - `+collision-fail` «Зіткнення/сходження зупиняє симуляцію» · game-logic/lose · 📎.
  - `+junction-toggle` «Стрілка перемикається після проїзду» · entities/interact · 📎.
  - `+button-toggle` «Кнопка/важіль перемикає стан цілей» · entities/interact · 🥉 — з Chip's Challenge.
  - `+path-cut` · `+undo-redo` · `+world-map` — уже запропоновані.

## Пропозиції до словників
- `+role:sink` — локомотив як приймач; `+role:conduit` — рейка (порти, як труба); `+role:switch` ⏳ (стрілка, важіль), `+role:gate` ⏳ (барʼєр, ворота, семафор).
- `+trigger:collide(a, b)` — дві рухомі сутності в одну клітину або обмін клітинами за тік (`contact` не ловить обмін); `+trigger:reach` ⏳ — вагон дійшов до локомотива.
- `+cond:order_next(n)` — сутність має наступний очікуваний номер.
- `+effect:attach` ⏳ — вагон чіпляється до складу; `+effect:place_tile(t)` — гравець кладе тайл з бюджету.
- `+ui:run-button` (спільне з Cosmic Express), `+ui:pieces-left` — лишок бюджету.
- `+axis:time=programmed` ⏳ — підтвердження.
- `+card:track-budget`, `+card:ordered-arrival`, `+card:collision-fail`, `+card:junction-toggle`.

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Railbound) — tap-and-drag на ізометричній сітці, ліміт шматків, 1–4 нумеровані вагони, тунелі/стрілки → станції → семафори (2.0) → два локомотиви (3.0), світи по ~10 рівнів + бонусні.
- [Steam](https://store.steampowered.com/app/1967510) — барʼєри для таймінгу, стрілки, тунелі, 240+ пазлів, редактор, Workshop.
- [Pocket Gamer](https://www.pocketgamer.com/railbound/september-6th/) — «railbending»: додати чи прибрати зʼєднання.
- [PC Gamer](https://www.pcgamer.com/uk/connect-traincars-in-order-in-puzzler-railbound-from-golf-peaks-and-inbento-makers/) — анонс (сторінка віддала лише навігацію, URL з черги).
- YouTube: пошук «Railbound gameplay».

## Непевне
- Веб-пошук вичерпано, фан-вікі (fandom) і сайт Afterburn недоступні — деталі елементів написано частково з памʼяті.
- (?) Чи стрілка перемикається після кожного проїзду, чи фіксована й перемикається лише важелем/кнопкою.
- (?) Ворота з важелями як окремий елемент (згадано куратором; Steam називає лише барʼєри).
- (?) Точна механіка станцій (зупинка, пасажир, порядок) і семафорів 2.0 (ставить гравець? що звільняє?).
- (?) Чи можна прибирати наперед задані рейки; чи є прискорення симуляції й undo-кнопка.
