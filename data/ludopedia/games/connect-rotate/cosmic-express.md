---
title: Cosmic Express
slug: cosmic-express
family: connect-rotate
also: [thinky]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2017
platforms: [PC, Mac, Linux, iOS, Android, Switch]
links:
  - {kind: youtube, url: "https://www.youtube.com/watch?v=huIYCSDY8n8", best: true, note: "офіційний трейлер з прескіту: колія, посадка й висадка прибульців за 1–2 хв"}
  - {kind: official, url: "https://cosmicexpressgame.com/", note: "сайт гри, лінки на всі платформи"}
  - {kind: other, url: "https://cosmicexpressgame.com/press", note: "прескіт: факти, автори, історія прототипу Train Braining"}
  - {kind: steam, url: "https://store.steampowered.com/app/583270/Cosmic_Express/", note: "опис: один прибулець у вагоні, сотні рівнів"}
  - {kind: other, url: "https://draknek.itch.io/cosmic-express", note: "itch.io, керування мишею"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Cosmic_Express", note: "автори, дати, платформи; механік мало"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Cosmic+Express+gameplay+walkthrough", note: "пошук; проходження з пізніми механіками"}
stage: v1
coverage: 60
mechanics: [cell-click, hover-highlight, reach-exit, collect-all, satisfy-constraints, teleport-pair, impassable-cells, completion-detection, level-select, level-unlock, sequential-levels, save-progress, game-screen, main-menu, settings-window, +path-drawing, +path-cut, +undo-redo, +world-map, +adjacent-transfer, +carriage-capacity, +seat-taint, +run-simulation]
proposes: ["+role:sink", "+role:terminal", "+trigger:input(drag)", "+trigger:adjacent", "+cond:has", "+effect:extend_path", "+effect:cut_path", "+effect:board", "+effect:alight", "+ui:run-button", "+axis:time=programmed", "+card:adjacent-transfer", "+card:carriage-capacity", "+card:seat-taint", "+card:run-simulation"]
author: opus
date: 2026-11-02
---

# Cosmic Express — проклади одну колію від входу до виходу, щоб кожен прибулець доїхав до свого дому

## Суть
Гравець малює **одну неперервну колію** по клітинах космічної станції від тунелю-входу до тунелю-виходу. Потяг їде нею сам: прибулець сідає у вагон, коли вагон проїжджає **поруч** із ним, і виходить, коли вагон проїжджає поруч із вільним будинком свого кольору. Місця обмежені (спершу один вагон — одне місце), тож маршрут має чергувати «взяти → відвезти → взяти». Уся складність — у тому, що колія не може перетинати сама себе, а сусідство спрацьовує автоматично, навіть коли ти цього не хочеш.

## Поле і час
- Невелика квадратна сітка (порядку 5×5…9×9) у формі купола станції; частина клітин — стіни, прибульці, будинки, тобто непридатні для колії (?).
- Вхід і вихід — тунелі на краю поля; колія починається від входу.
- Час «програмний»: гравець без поспіху малює колію (статичний пазл), потім потяг проїжджає її покроково, клітина за клітиною; кожен крок — перевірка сусідства для кожного вагона.
- Рівні згруповано в сузірʼя/планети на зоряній мапі; «сотні рівнів» (Steam).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вхід (тунель) | source (custom) | край поля | звідси виїжджає потяг; колія мусить з нього починатись |
| Вихід (тунель) | sink (custom) | край поля | потяг заїжджає → рівень пройдено, якщо всі прибульці вдома |
| Колія | mark | шлях клітин, без самоперетину | малюється гравцем; потяг іде лише нею |
| Потяг: локомотив | object | — | рухається по колії на 1 клітину за крок |
| Вагон | container | 1 місце; кількість вагонів задана рівнем (1–3?) | порожній — приймає сусіднього прибульця; повний — висаджує біля свого будинку |
| Прибулець (зелений, фіолетовий, …) | object | колір | сідає в порожній вагон, що проїхав поруч (ортогонально) |
| Будинок (кратер/коробка) | sink (custom) | колір, вільний/зайнятий | приймає прибульця свого кольору з вагона, що проїхав поруч |
| Слизький прибулець | object | залишає слиз | після висадки його місце стає «забрудненим» — інші туди не сідають (?) |
| Забруднене місце | — | стан вагона | інший прибулець не сідає в цей вагон (?) |
| Червоточина (wormhole) | terrain | пара | колія, що зайшла в одну, продовжується з другої (як тунель-телепорт) |
| Стіна / порожнеча | static | — | колію класти не можна |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, cell)` → ЯКЩО `free(cell)` and `adjacent(cell, path_end)` → ТО `extend_path(track, cell)`; інакше `block`.
- КОЛИ `input(drag, cell)` → ЯКЩО `occupied(cell, track)` → ТО `cut_path(track, cell)` — відкат колії до цієї клітини.
- КОЛИ колія досягла виходу → ТО `custom: «потяг вирушає»` (запуск симуляції) (?).
- КОЛИ `tick` → ТО `move(train, next_track_cell)`; вагони — `body-queue` за локомотивом.
- КОЛИ `adjacent(car, alien)` → ЯКЩО `not has(car, passenger)` and `not state(car, slimed)` → ТО `board(alien, car)` (`custom: «прибулець сідає»`).
- КОЛИ `adjacent(car, house[c])` → ЯКЩО `has(car, alien[c])` and `free(house)` → ТО `alight(alien, house)`, будинок стає зайнятим.
- КОЛИ `alight(slimy_alien)` → ТО `set_state(car, slimed)` (?).
- КОЛИ `enter(track, wormhole)` → ТО `teleport(track_end, wormhole_pair)` — малювання продовжується з парної червоточини.
- КОЛИ `reach(train, exit)` → ЯКЩО `all_on(alien, house)` → ТО `win`, `unlock(next)`; інакше `custom: «потяг повертається, рівень не зараховано»` (?).
- Порядок важить: сусідство спрацьовує автоматично, тож пройти поруч із «не тим» прибульцем, маючи вільне місце, означає взяти його — і зайняти місце, потрібне іншому.
- Перемога: усі прибульці в будинках свого кольору **і** потяг у виході. Поразки й рахунку нема — лише «розвʼязано / ні».

## Керування і ввід
- Миша / тач: натиснути на кінець колії й тягнути по клітинах — колія подовжується; повести назад — колія стирається (backtrack).
- Клік по клітині колії — обрізати хвіст до неї (?).
- Undo (Z) і рестарт рівня (R) (?); кнопка запуску потяга або автозапуск після досягнення виходу (?).

## Вікна, меню, HUD
- `main-menu`: Грати → зоряна мапа; Налаштування; Вихід.
- `level-select` у вигляді `world-map`: сузірʼя/планети, у кожній — рівні-вузли зі станом «пройдено».
- `game-screen`: купол станції з прибульцями, будинками, колією; кнопки `undo-button`, `restart-button`, повернення на мапу. Лічильників нема — мета видна з поля.
- `settings-window`: звук, музика, мова (лише EN).
- Переходи: main-menu → мапа → game-screen → (перемога) анімація відʼїзду → мапа з відкритим наступним рівнем.

## Фічі поза полем
- `levels-sequential` + `level-unlock` у межах сузірʼя; кілька відкритих рівнів одночасно — можна відкласти важкий (?).
- `undo` (необмежене), `restart-level`, `autosave` прогресу (Steam Cloud).
- `achievements` (Steam).
- Нема підказок, редактора, daily.

## Варіації й родичі
- Прототип **Train Braining** (Train Jam 2015) → Cosmic Express; продовження-мешапи **Sokobond Express** (2024) і **Spooky Express** (2025) від Draknek & Friends.
- Родичі: Railbound (ставиш шматки колії, вагони зчіплюються), Trainyard (колір поїздів), Flow Free (шлях пальцем без перетину), гамільтонові шляхи в pencil-logic.
- Осі варіацій: **тригер посадки: сусідство / наїзд на клітину / кнопка** · **місткість: 1 / N місць / кілька вагонів** · **що вирішує, хто сяде: перший сусід / колір / порядок** · **колія: одна без перетинів / з мостами / з телепортами**.

## Цікавинки для курсу
- Шлях-колія drag-ом з відкатом (backtrack) і забороною самоперетину — 📎 (картка `+path-drawing`).
- Посадка/висадка за **сусідством** під час руху: перевірка 4 сусідів кожного вагона на кожному кроці — 📎.
- Обмежена місткість + кольори будинків → маршрут як задача «підбери й довези» — 🥉 (модель стану вагонів).
- Розвʼязувач рівня: DFS по шляхах із симуляцією посадок (простір шляхів величезний) — 🥇.
- Слизькі місця: стан вагона змінюється після пасажира — 🌱.
- Червоточини, що переносять малювання шляху (не гравця) — 📎.

## Мапа на каталог
- Є: `cell-click`, `hover-highlight` (ввід) · `reach-exit` (вихід) · `collect-all` (усі прибульці) · `satisfy-constraints`, `completion-detection` · `teleport-pair` (червоточини) · `impassable-cells` · `level-select`, `level-unlock`, `sequential-levels`, `save-progress` · `game-screen`, `main-menu`, `settings-window`.
- **Нема** → пропозиції карток:
  - `+path-drawing` «Малювання шляху drag-ом по клітинах» · interface/input · 📎 — уже з Flow Free; тут слот {self_cross: false}.
  - `+path-cut` «Відкат шляху до клітини» · entities/legality · 📎 — з Flow Free.
  - `+undo-redo` «Undo ходів гравця» · game-logic · 📎.
  - `+world-map` «Мапа світу з вузлами-рівнями» · levels/progression · 🥉.
  - `+adjacent-transfer` «Посадка/висадка за сусідством» · entities/interact · 📎 · слоти {neighborhood: 4|8, priority: first|color}.
  - `+carriage-capacity` «Місткість носія» · entities/state · 🌱 · слот {seats} (дитина `inventory-limit` для сутності, не гравця).
  - `+seat-taint` «Місце псується після пасажира» · entities/state · 🌱.
  - `+run-simulation` «План → запуск симуляції» · game-logic · 🥉 · слоти {auto_start, step, speed} — спільне з Railbound.

## Пропозиції до словників
- `+role:sink` — будинок і вихід як приймачі (спільне з Pipe Mania, Deflektor); `+role:terminal` — вхід/вихід як фіксовані кінці шляху (з Flow Free).
- `+trigger:input(drag)` — подія на кожній клітині під курсором; `+trigger:adjacent` ⏳ — ядро гри: вагон поруч із прибульцем/будинком.
- `+cond:has` ⏳ — вагон має пасажира кольору c.
- `+effect:extend_path` / `+effect:cut_path` — як у Flow Free; `+effect:board(a, car)` / `+effect:alight(a, house)` — пасажир у носій / з носія (окремо від `pickup`, бо предмет не зникає, а переїжджає).
- `+ui:run-button` — кнопка «поїхали» між плануванням і симуляцією.
- `+axis:time=programmed` ⏳ — підтвердження: план малюєш, потім він виконується.
- `+card:adjacent-transfer`, `+card:carriage-capacity`, `+card:seat-taint`, `+card:run-simulation` — див. вище.

## Джерела
- ⭐ [Трейлер Cosmic Express](https://www.youtube.com/watch?v=huIYCSDY8n8) — офіційний, з прескіту; видно колію, посадку й висадку.
- [cosmicexpressgame.com](https://cosmicexpressgame.com/) — сайт, лінки на App Store, Google Play, Switch, Steam, itch.io, Epic.
- [Прескіт](https://cosmicexpressgame.com/press) — автори (Alan Hazelden, Benjamin Davis, Tyu), прототип Train Braining, 16.03.2017.
- [Steam](https://store.steampowered.com/app/583270/Cosmic_Express/) — «only room for one extraterrestrial at a time in the passenger car».
- [itch.io](https://draknek.itch.io/cosmic-express) — керування мишею, сесія «кілька хвилин».
- [Wikipedia](https://en.wikipedia.org/wiki/Cosmic_Express) — дати, платформи, наступники Sokobond Express і Spooky Express.
- YouTube: пошук «Cosmic Express gameplay walkthrough».

## Непевне
- Веб-пошук сесії вичерпано, а Thinky Games, StrategyWiki і TouchArcade віддали 403: детальні механіки написано з памʼяті, з перевірених лише «один прибулець на вагон», «прокладай колію», «сотні рівнів».
- (?) Типи прибульців за кольорами і хто саме «слизький»; чи слиз блокує всіх інших чи лише окремі кольори.
- (?) Коробки/вантаж як окремий тип пасажира (у запиті куратора згадано boxes) — не підтверджено.
- (?) Пріоритет, коли вагон одночасно поруч із двома прибульцями або з будинком і прибульцем (висадка перед посадкою?).
- (?) Чи потяг вирушає автоматично, коли колія дійшла до виходу, і що стається при невдачі (повертається / стоїть).
- (?) Розмір поля і максимальна кількість вагонів.
