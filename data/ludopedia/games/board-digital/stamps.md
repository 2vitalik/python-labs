---
title: Stamps
slug: stamps
aka: [Stamps by Hatem & Yury]
family: board-digital
also: [pencil-logic]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: both
  goal: constraints
year: 2025
platforms: [web, iOS, Android]
links:
  - {kind: itch, url: "https://hatemyury.itch.io/stamps", best: true, note: "безкоштовне демо в браузері (4 з 10 наборів марок), опис, коментарі розробників"}
  - {kind: other, url: "https://apps.apple.com/app/id6744961801", note: "App Store: повна гра за IAP, історія версій (зірка за перемогу, таймер вимикається)"}
  - {kind: other, url: "https://play.google.com/store/apps/details?id=com.hatemyury.stamps", note: "Google Play"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Stamps+puzzle+game", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [cursor-place, cell-click, interaction-table, push-object, pull-object, satisfy-constraints, completion-detection, goal-counter, no-moves-left, undo-redo, daily-puzzle, leaderboard, streak-stats, profile-stats, score-records, difficulty-levels, level-bank, sequential-levels, tutorial-window, main-menu, pause-menu, settings-window, game-screen, end-screen, language-picker, volume-control, background-music, sound-effects, save-game, +deck-draw, +hand-of-tiles, +country-rule-on-place, +choose-effect-target, +stage-goals, +limited-power-uses, +shape-pattern-match, +goal-replacement, +weekly-score]
proposes: ["+effect:return_to_bag", "+effect:draw_card", "+cond:parity", "+cond:consecutive", "+window:collection-window", "+ui:goal-cards", "+card:place-trigger-rule"]
author: opus
date: 2026-11-09
---

# Stamps — клади марки в сітку 4×3: правило країни зсуває, міняє чи прибирає сусідів, а ти збираєш цілі за країною, типом і ціною

## Суть
Гравець бере з руки марки й кладе в маленьку сітку, щоб виконати набір цілей («рядок марок однієї країни», «стовпець із сумою ціни рівно 10», «тип Animal буквою L»). Кожна країна має **одне правило, що спрацьовує в момент викладання**: французька марка мусить повернути сусідню в Колекцію, єгипетська — помінятися місцями з маркою того ж типу, індійська — з іншою індійською. Тож кожен хід — і розстановка, і маніпуляція вже покладеним; гра коротка (5 стадій, кілька хвилин) і рогалик-подібна: 4 випадкові країни й випадкові цілі на партію.

## Поле і час
- Головна сітка — прямокутник 4 стовпці × 3 рядки (розмір видно в даних сцени демо; узгоджується з цілями «4 кути», «діагональ із 3 марок», «стовпець із сумою < 7»).
- Окремо: рука — ряд із 3 клітин; панель цілей; Колекція (мішок) — усі марки 4 країн партії, 4×6 = 24.
- Хід = викласти одну марку з руки (+ її правило). Таймер лише для рекордів (вмикається/ховається в налаштуваннях); з v1.1.0 ліміт часу прибрано.
- Стадії: партія — 5 стадій; на кожній — набір випадкових цілей, на пізніх треба виконати **кілька одночасно**.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Марка | tile | країна; ціна 1–6; тип Animal / Landmark / Object | кладеться з руки на вільну клітину; спрацьовує правило її країни |
| Набір країни | zone | 6 марок: ціни 1–6, по 2 кожного типу | спільне правило для всіх 6 марок |
| Клітина сітки | static | вільна / зайнята | приймає одну марку |
| Рука | supply | 3 клітини | наповнюється добором 3 випадкових марок з Колекції |
| Колекція | supply | 24 марки 4 країн | джерело добору; сюди повертаються прибрані марки й марки виконаних цілей |
| Ціль | mark | шаблон (рядок/стовпець/2×2/кути/діагональ/L/S/T) + вимога (країна, тип, ціна) | виконана → позначка; лічильник стадії +1 |
| Здібність Remove | switch | 3 використання за партію | повертає будь-яку марку з сітки в Колекцію |
| Таймер | mark | секунди | для рекордів «найбільше зірок, потім найменший час» |

**Правила країн** (текст підказки марки; демо має 4 набори, повна гра — 10):

| Країна | Правило при викладанні |
|---|---|
| Франція | повернути **сусідню** марку в Колекцію |
| Єгипет | помінятися місцями з маркою **того ж типу** (Animal/Landmark/Object) |
| Індія | помінятися місцями з **іншою індійською** маркою |
| Бразилія | зсунути будь-яку кількість **зʼєднаних** марок у тому ж рядку чи стовпці |
| Китай | повернути сусідню **не-китайську** марку в **руку** |
| Австралія | добрати не-австралійську марку; цей ефект не скасовується |
| Англія / Японія / Мексика / Росія | одне з: штовхнути марку й усі за нею геть від цієї (не штовхається — тягнути) · помінятися з будь-якою з 8 сусідніх · повернути марку з тієї ж діагоналі · повернути марку з ціною ≤ ціни цієї (відповідність — у «Непевне») |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click(stamp_in_hand))` → ТО `set_state(stamp, selected)`; повторний клік — скасувати вибір.
- КОЛИ `input(click(cell))` → ЯКЩО `state(stamp, selected)` і `free(cell)` → ТО `place(player, stamp)`, `trigger(country_rule)`.
- Правило з ціллю: КОЛИ `after(place)` → ЯКЩО `custom: «є хоч одна допустима ціль правила»` → ТО `choose(target)` (підсвічені допустимі марки), далі ефект; інакше правило ігнорується («індійських більше нема — правило пропущено»).
- Франція: КОЛИ `after(place(french))` → ЯКЩО `adjacent_count(cell, stamp, >=, 1)` → ТО `choose(adjacent)`, `custom: «повернути ціль у Колекцію»` (+effect:return_to_bag).
- Єгипет: КОЛИ `after(place(egyptian))` → ЯКЩО `same(egyptian, other, type)` для якоїсь марки на полі → ТО `swap(egyptian, other)` — обовʼязково.
- Індія: КОЛИ `after(place(indian))` → ЯКЩО `count(indian, >=, 2)` → ТО `swap(indian, other_indian)`.
- Бразилія: КОЛИ `after(place(brazilian))` → ТО `custom: «зсунути ланцюжок зʼєднаних марок уздовж рядка/стовпця»` (близько до `shift`, але не весь ряд).
- Китай: КОЛИ `after(place(chinese))` → ЯКЩО `custom: «поруч є не-китайська марка»` → ТО `custom: «повернути її в руку»`.
- Австралія: КОЛИ `after(place(australian))` → ТО `custom: «добрати 1 не-австралійську марку»` (+effect:draw_card); undo через цей хід не проходить.
- Штовх/тяг: КОЛИ `after(place(x))` → ЯКЩО `free(cell_behind_line)` → ТО `push(line)`; інакше `pull(stamp)`.
- Обмін з оточенням: КОЛИ `after(place(x))` → ТО `choose(adjacent8)`, `swap(x, target)`.
- Діагональ / ціна: КОЛИ `after(place(x))` → ЯКЩО `custom: «ціль на тій самій діагоналі»` або `custom: «ціна цілі ≤ ціни x»` → ТО `custom: «повернути ціль у Колекцію»`.
- Добір: КОЛИ `input(draw_stamps)` → ЯКЩО `count(hand, ==, 0)` → ТО `custom: «3 випадкові марки з Колекції в руку»`; добір не скасовується.
- Remove: КОЛИ `input(remove_ability)` → ЯКЩО `counter(removes, >, 0)` → ТО `choose(stamp)`, `custom: «повернути в Колекцію»`, `counter(removes, -1)`.
- Undo: КОЛИ `input(undo)` → ЯКЩО `not mode(daily)` і `custom: «після останнього добору / переходу стадії / завантаження сейву»` → ТО `undo(1)` (скасовує викладання або ефект).
- Цілі країни: КОЛИ `pattern(row_full)` → ЯКЩО `same(row, country)` → ТО `custom: «ціль виконана»`; так само стовпець, 2×2, 4 кути, діагональ із 3 будь-якої орієнтації; варіант «різні країни» — `unique(row)`.
- Цілі типу: КОЛИ `pattern(row_full)` або `custom: «фігура L / S / T / 2×2 з марок»` (поворот і дзеркало дозволені) → ЯКЩО `same(cells, type)` → ТО ціль виконана.
- Цілі ціни: `sum(row, 14)` · `sum(column, 10)` · `custom: «сума стовпця < 7»` · `custom: «увесь рядок парний / непарний»` (+cond:parity) · `custom: «стовпець — послідовні ціни, найбільша вгорі / внизу»` і `custom: «рядок послідовно зростає чи спадає»` (+cond:consecutive) · `unique(column)` за ціною, країною й типом одночасно.
- Стадія: КОЛИ `counter(goals_met, >=, required)` → ТО `custom: «виконані цілі замінюються новими, марки, що їх утворили, повертаються в Колекцію»`, `counter(stage, +1)`, `message(«You did it!»)`.
- Перемога: КОЛИ `counter(stage, ==, 5)` пройдено → ТО `win`, зірка за перемогу, `window(end-screen)`.
- Поразка: КОЛИ `no_moves(player)` → ЯКЩО `custom: «сітка повна, Remove = 0, undo недоступне»` → ТО `lose`, сповіщення «Out of Moves».
- Рахунок: рекорд = найбільше зірок, потім найменший час; Daily: тижневий бал = Σ(цілі × зірки за день).

## Керування і ввід
- Лише миша/дотик: клік по марці в руці → клік по вільній клітині; потім клік по цілі правила (або повторний клік по марці — повернути її в руку).
- ПКМ (ПК) або довге натискання (мобільні) на марці — підказка з типом і правилом у правому верхньому куті; клік по цілі — пояснення вимоги.
- Кнопки: DRAW STAMPS, Undo, Remove Stamp (3 заряди), меню; клік по Колекції — подивитися всі марки партії.

## Вікна, меню, HUD
- `splash-screen` — лого.
- `main-menu`: Play / Continue · Play Daily / Replay Daily · Puzzles · Daily & Stats · Settings · кнопка «Hatem & Yury» (про авторів, Discord) · Get the Full Game.
- `tutorial-window` (окремий режим-сцена): інфобокси, підсвітка клітин, стрілка-клік; «Quit Tutorial», перезапуск — з Settings.
- `game-screen`: сітка 4×3; рука з 3 клітин; панель цілей (`+ui:goal-cards` з позначкою виконано); номер стадії; `remaining-counter` Removes Left; `undo-button`; кнопка добору; `timer-elapsed` (зліва/справа/сховано); `tooltip` марки.
- `+window:collection-window` — оверлей з усіма марками Колекції; клік будь-де закриває.
- `pause-menu`: Resume · Save & Quit · Abandon · Main Menu.
- `end-screen`: «Yay!», картки цілей пройдених стадій, Play Again; `confirm-dialog` «Out of Moves 😮» при поразці.
- `puzzle-select`: банк ручних пазлів (викласти лише 3 марки), Next Puzzle / Next Unsolved Puzzle / Restart Puzzle / All Solved!
- `daily-window`: Daily Results, Daily Leaderboard (ваш відсоток Top/Bottom), This Week / Last Week / Best Week.
- `stats-window`: Games Played · Win Rate · Current Streak · Max Streak; High Scores.
- `settings-window`: Language (EN/FR/RU…), гучність музики й звуків, показ таймера, Legal (Privacy Policy, Licenses), Restart Tutorial.
- `shop-window`: купівля повної гри (IAP), «Purchase Pending», «Thank You!».
- Переходи: main-menu → (перша гра) tutorial → game-screen → стадія 1…5 → end-screen → main-menu; Daily — одна спроба на день.

## Фічі поза полем
- `undo` (заборонене в Daily; не через добір, стадію чи завантаження), `save-slots`-подібне Save & Quit / Continue.
- `mode-daily` + `leaderboard-online` (лише перша спроба, складність росте від понеділка до неділі) + `streaks` + `stats`.
- `difficulty-presets`: у повній грі 1 з 5 рівнів; у даних — 9 назв (Easy, Basic, Simple, Normal, Moderate, Hard, Challenging, Expert, Extreme).
- `puzzle-bank` ручних мінізадач на 3 марки; `tutorial`; `localization`; `music-toggle`/`volume-sliders`.
- Демо (itch, браузер) — 4 з 10 наборів, грається безкінечно; повна гра — лише Android/iOS.
- Розробники свідомо **не** показують превʼю наступних марок і прибрали іконки типів з марок (переобтяжували UI; тип — у підказці).

## Варіації й родичі
- Осі варіацій: **момент правила** (при викладанні — Stamps / постійна аура — Bärenpark-подібні бонуси сусідства) · **хто обирає ціль ефекту** (гравець — Stamps / фіксовано — Sixteen-зсув) · **куди йде прибране** (у Колекцію / у руку / зникає) · **цілі** (фіксовані на рівень / випадкові стадіями з заміною).
- Родичі в корпусі: `sagrada.md` (обмеження на клітини сітки вітража), `qwirkle-ingenious.md` (лінії однакової ознаки), `tiny-towns.md` (шаблони-фігури з ресурсів на сітці), `noch-mal.md`; ефекти «при викладанні» — як у карткових іграх (`triple-triad.md` перевертає сусідів).
- Цілі-шаблони L/S/T «з поворотом і дзеркалом» — родич карток поліоміно (`blokus.md`, `patchwork.md`), але тут фігура складається з однотипних марок, а не кладеться цілою.

## Цікавинки для курсу
- Таблиця правил країн як дані: `country → effect(target_filter)`, один обробник «після викладання» — 📎 (картка `interaction-table`).
- Вибір цілі ефекту: обчислити допустимі цілі, підсвітити, чекати клік; автопропуск, якщо цілей нема — 🥉.
- Перевірка 22 цілей: рядок/стовпець/кути/діагональ + поліоміно-шаблони L/S/T у всіх орієнтаціях на сітці 4×3 — 🥉.
- Undo зі «стінами» (добір, нова стадія, сейв, Австралія) — стек команд з незворотними точками — 🥉.
- Стадії з заміною виконаних цілей і поверненням марок у мішок — 📎.
- Daily з однаковим seed для всіх, лідерборд «лише перша спроба», тижневий бал — 🥈.
- Розвʼязувач пазлу «3 марки»: перебір позицій × цілей ефектів — 🥈.

## Мапа на каталог
- Є: `cursor-place` + `cell-click` ↔ викладання з руки; `interaction-table` ↔ правила країн; `push-object`/`pull-object` ↔ правило «штовхни, інакше тягни»; `satisfy-constraints` + `completion-detection` + `goal-counter` ↔ цілі стадії; `no-moves-left` ↔ Out of Moves; `undo-redo` ↔ Undo; `daily-puzzle` + `leaderboard` + `streak-stats` + `profile-stats` + `score-records` ↔ Daily і статистика; `difficulty-levels`; `level-bank` ↔ Puzzles; `sequential-levels` ↔ 5 стадій; вікна `main-menu`, `pause-menu`, `settings-window`, `game-screen`, `end-screen`, `tutorial-window`; `language-picker`, `volume-control`, `background-music`, `sound-effects`, `save-game`.
- **Нема** → пропозиції карток:
  - `+country-rule-on-place` «Правило набору спрацьовує при викладанні плитки» · entities/interact · 📎 · слоти {effect, target_filter}.
  - `+choose-effect-target` «Гравець обирає ціль ефекту з підсвічених» · interface/input · 🥉.
  - `+stage-goals` «Стадії з набором випадкових цілей, кількість росте» · game-logic/win · 📎.
  - `+goal-replacement` «Виконані цілі замінюються, їхні плитки повертаються в мішок» · game-logic/win · 📎.
  - `+limited-power-uses` «Здібність із N зарядами на партію» · game-logic/economy · 🌱.
  - `+deck-draw`, `+hand-of-tiles`, `+shape-pattern-match`, `+weekly-score` — як теги.

## Пропозиції до словників
- `+effect:return_to_bag` — повернути плитку/карту з поля в мішок-колоду (Stamps: Колекція), не знищуючи.
- `+effect:draw_card` — добрати з колоди/мішка в руку (Австралія, кнопка DRAW).
- `+cond:parity` — усі значення в лінії парні / непарні.
- `+cond:consecutive` — значення в лінії йдуть підряд (зростання/спадання).
- `+window:collection-window` — оверлей «усі плитки/карти, що є в мішку партії».
- `+ui:goal-cards` — картки цілей стадії з позначкою «виконано».
- `+card:place-trigger-rule` — див. `+country-rule-on-place`.

## Джерела
- ⭐ [itch.io: Stamps](https://hatemyury.itch.io/stamps) — опис («4 random country stamps», «5 stages», правила рухають/прибирають/міняють), демо в браузері (Godot), коментарі розробників про іконки й превʼю; дати сторінки — червень 2025.
- Демо-збірка (Godot `index.pck` з itch) — тексти локалізації EN: усі 22 цілі, підказки правил, кроки туторіалу, меню, Daily, статистика; імена наборів (Brazil/Egypt/France/India у демо) і їхніх ефектів; розмір сітки 4×3 у сцені.
- [App Store](https://apps.apple.com/app/id6744961801) — повна гра $2.99 IAP, 10 наборів, Daily, stats, історія версій (1.0.4 — 06/03/2025; 1.1.0 — зірка за перемогу, ліміт часу прибрано, вмикання таймера).
- [Google Play](https://play.google.com/store/apps/details?id=com.hatemyury.stamps) — сторінка (опис у фетчі не віддався).
- YouTube: пошук «Stamps puzzle game».

## Непевне
- (?) Відповідність 4 правил (штовх/тяг, обмін з 8 сусідами, діагональ, ціна ≤) країнам Англія/Японія/Мексика/Росія — у демо цих наборів нема, тексти правил є лише в локалізації.
- (?) Бразилія = ShiftAdjacent за назвою ефекту; що саме «зсунути будь-яку кількість зʼєднаних» (напрям, на скільки клітин) — не перевірено грою.
- (?) «Сусідня» для Франції/Китаю — 4-сусідство (бо окремо є правило «включно з діагоналями»), але явно не сказано.
- (?) Скільки цілей на стадію й скільки треба виконати на кожній з 5 стадій — у бінарних ресурсах складності, не прочитано.
- (?) Чи можна добирати, коли в руці ще є марки, і чи обмежене undo лічильником (у даних є `UndosCounter`).
- (?) Рядок «Equal to the number shown in the lens» — до якої цілі/механіки належить, не зрозуміло.
