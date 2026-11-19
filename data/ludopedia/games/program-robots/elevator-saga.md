---
title: Elevator Saga
slug: elevator-saga
aka: []
family: program-robots
also: []
klass: figure
axes:
  field: 1d
  time: programmed
  opponent: none
  info: partial
  random: runtime
  goal: collect
year: 2015
platforms: [web]
links:
  - {kind: play, url: "https://play.elevatorsaga.com/", best: true, note: "грати в браузері: 19 челенджів, симуляція будинку над редактором коду"}
  - {kind: other, url: "https://play.elevatorsaga.com/documentation.html", note: "документація: init/update, API ліфта й поверху, події, поради"}
  - {kind: other, url: "https://github.com/magwo/elevatorsaga", note: "сирці (MIT): challenges.js, world.js, elevator.js, user.js, app.js"}
  - {kind: other, url: "https://github.com/magwo/elevatorsaga/wiki/", note: "Wiki & Solutions — розвʼязки спільноти"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=elevator+saga+solution", note: "пошук; розбори розвʼязків"}
stage: v1
coverage: 55
mechanics: [code-editor-window, sequential-levels, collect-quota, time-out, move-limit, spawn-schedule, weighted-spawn, carrier-platform, objective-text, status-panel, help-window, confirm-dialog, end-screen, game-loop, game-pause, save-single-slot, +event-driven-program, +destination-queue, +direction-indicator-boarding, +wait-time-metrics, +challenge-evaluator, +elevator-physics-1d, +carrier-capacity, +url-hash-state, +step-run-speed, +solution-metrics]
proposes: ["+trigger:event(name)", "+effect:enqueue(a, x)", "+effect:clear_queue(a)", "+ui:metric-panel", "+feature:url-state", "+axis:control", "+card:event-driven-program"]
author: opus
date: 2026-11-19
---

# Elevator Saga — напиши JavaScript-диспетчер ліфтів: події кнопок, черги поверхів і норма пасажирів за час

## Суть
Браузерна гра Magnus Wolffelt: гравець пише обʼєкт JavaScript з функціями `init(elevators, floors)` і `update(dt, elevators, floors)`, вішає обробники подій ліфтів і поверхів і керує чергами призначень. Пасажири зʼявляються самі, тиснуть ↑/↓ на поверсі й кнопку свого поверху в кабіні, а гра лише симулює фізику ліфтів і міряє результат.

Челендж — перевезти N людей за T секунд, або так, щоб ніхто не чекав довше W секунд, або не більше ніж за M переміщень; останній, 19-й, — нескінченне демо. Ядро гри — алгоритм диспетчеризації в подієвій моделі: код не «ходить», а реагує.

## Поле і час
- Поле — будинок на 3–21 поверх: 1D-лінія поверхів; ліфтів 1–8, кожен у своїй вертикальній шахті; поверх 0 — вестибюль.
- Ліфт рухається безперервно: прискорення `floorHeight × 2.1`, гальмування `× 2.6`, максимальна швидкість `floorHeight × speedFloorsPerSec`; прибуття — коли до цілі < 0.5 і швидкість < 3.
- Час — секунди симуляції: кадр ділиться на підкроки `dtMax`, `update` гравця викликається раз за кадр; масштаб часу — кнопки −/+, за замовчуванням ×2.
- «Moves» = кількість змін поверху всіма ліфтами (підказка інтерфейсу: «floors travelled by elevators»).
- Інформація часткова: документований API дає стан кнопок, натиснуті поверхи в кабіні й `loadFactor`, але не кількість людей на поверсі і не їхні цілі до входу (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ліфт | player | місткість 4 за замовчуванням або 4–10 за челенджем; індикатори ↑/↓; черга `destinationQueue` | їде до першого поверху черги; на зупинці спершу випускає, потім впускає |
| Пасажир | neutral | вага 55–100; вигляд: дитина 1/41, жінка чи чоловік порівну | зʼявляється, тисне ↑/↓, входить у придатний ліфт, тисне свій поверх, виходить на ньому |
| Потік пасажирів | spawner | `spawnRate` 0.3–3.0 людини/с | новий пасажир кожні 1/spawnRate с; перший — одразу на старті |
| Поверх | zone | номер; кнопки ↑/↓ | події «up_button_pressed» / «down_button_pressed» |
| Вестибюль (поверх 0) | zone | — | щонайменше половина пасажирів зʼявляється тут; ≈10/11 решти їдуть сюди |
| Кнопка виклику ↑/↓ | switch | натиснута / ні | тисне пасажир; подію ловить код гравця |
| Кнопка поверху в кабіні | switch | номер поверху | подія «floor_button_pressed»; гасне, коли ліфт зупинився на цьому поверсі |
| Індикатор напрямку ↑/↓ | switch | обидва увімкнені на старті | пускає лише тих, кому в цей бік |
| Черга призначень | supply | масив поверхів | `goToFloor(n)` — у кінець, `goToFloor(n, true)` — на початок; той самий поверх двічі не додається |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(1/spawnRate)` → ТО `spawn_at(user, floor)`: з імовірністю 1/2 вестибюль, інакше рівномірно будь-який поверх.
- Ціль пасажира: з вестибюля — рівномірно один з верхніх; з інших поверхів ≈10/11 — у вестибюль, ≈1/11 — випадковий інший поверх.
- КОЛИ `spawned(user)` → ТО `set_state(call_button, pressed)` — ↓, якщо ціль нижче, інакше ↑.
- КОЛИ `custom: «натиснуто кнопку виклику на поверсі»` → ТО `custom: «подія поверху → обробник гравця»`.
- КОЛИ `exec(goToFloor)` → ЯКЩО `custom: «поверху ще нема в черзі»` → ТО `custom: «додати в кінець; з directly — на початок»`.
- КОЛИ `exec(stop)` → ТО `custom: «очистити чергу й зупинитись»`.
- КОЛИ `tick` → ЯКЩО `custom: «черга не порожня»` → ТО `move(elevator, queue_head)` з розгоном і гальмуванням.
- КОЛИ `custom: «ліфт от-от мине поверх, що не є ціллю»` → ТО `custom: «подія passing_floor(поверх, напрямок)»`.
- КОЛИ `reach(elevator, floor)` → ТО `clear_state(cabin_button, pressed)`, `custom: «подія stopped_at_floor»`.
- КОЛИ `reach(elevator, floor)` → ЯКЩО `same(user, floor, destination)` → ТО `disappear(user)`, `counter(transported, +1)`.
- КОЛИ `reach(elevator, floor)` → ЯКЩО `state(elevator, indicator_matches)` and `not state(elevator, full)` → ТО `carry(elevator, user)`, `set_state(cabin_button, pressed)`.
- КОЛИ `reach(elevator, floor)` → ЯКЩО `not state(elevator, indicator_matches)` → ТО `custom: «пасажир чекає далі й кнопку не тисне»`.
- КОЛИ `reach(elevator, floor)` → ЯКЩО `state(elevator, full)` → ТО `set_state(call_button, pressed)` — пасажир тисне знову.
- КОЛИ `custom: «натиснуто ↑/↓, а на поверсі стоїть неповний ліфт з таким індикатором»` → ТО `custom: «ліфт повторно прибуває — двері відчиняються знову»`.
- КОЛИ `custom: «черга ліфта спорожніла»` → ТО `custom: «подія idle»`.
- КОЛИ `custom: «округлений поверх ліфта змінився»` → ТО `counter(moves, +1)`.
- КОЛИ `tick` → ТО `custom: «максимум очікування = max(старий, зараз − час появи) для кожного, хто ще чекає або їде»`.
- КОЛИ `custom: «пасажир вийшов»` → ТО `custom: «оновити середнє очікування й Transported/s»`.
- КОЛИ `counter(transported, >=, N)` → ЯКЩО `custom: «жодну межу челенджу (T, W чи M) ще не перейдено»` → ТО `win`.
- КОЛИ `custom: «минуло T секунд»` → ЯКЩО `counter(transported, <, N)` → ТО `lose`.
- КОЛИ `counter(max_wait, >=, W)` → ЯКЩО `counter(transported, <, N)` → ТО `lose`.
- КОЛИ `counter(moves, >=, M)` → ЯКЩО `counter(transported, <, N)` → ТО `lose`.
- КОЛИ `custom: «помилка в коді під час виконання»` → ТО `custom: «пауза + «There is a problem with your code:»»`.
- Типи норм: #1–5, 10, 16, 17 — N людей за T с (від 15 за 60 до 110 за 80); #6–7 — за M переміщень (40 за 60, 100 за 63); #8, 9, 11–15 — без очікування понад W (від 21 до 14 с); #18 — 2675 людей за 1800 с без очікування понад 45 с; #19 — демо без кінця.
- Перемога: норма виконана в момент, коли спрацювала перша з меж · Поразка: межу часу, очікування чи переміщень перейдено раніше · Рахунок: Transported, Elapsed time, Transported/s, Avg і Max waiting time, Moves.

## Керування і ввід
- Код — у редакторі CodeMirror під симуляцією; Apply перезапускає челендж з новим кодом і стартує його.
- Save — у localStorage («Code saved» з часом); Reset — після підтвердження замінює код на «робочий, але простий» шаблон з бекапом; Undo reset — повертає бекап.
- Кнопка старт / пауза в заголовку челенджу (після кінця — рестарт), масштаб часу −/+.
- URL-хеш: `#challenge=N`, `timescale=…`, `autostart=false`, `fullscreen`, `devtest`.
- Налагодження — інструменти розробника браузера.

## Вікна, меню, HUD
- `game-screen`: заголовок «Challenge #N: умова», кнопка старт / пауза, `speed-slider` (−, ×k, +).
- Будинок: поверхи з номером і кнопками ↑/↓; ліфти з індикаторами ↑/↓, номером поверху й натиснутими кнопками; пасажири — іконки людей.
- HUD-панель метрик: Transported · Elapsed time · Transported/s · Avg waiting time · Max waiting time · Moves.
- `code-editor` під будинком: рядок помилки «There is a problem with your code:», кнопки Reset · Undo reset · Apply · Save.
- `end-screen` поверх будинку: «Success!» / «Challenge completed» з посиланням «Next challenge» або «Challenge failed» / «Maybe your program needs an improvement?».
- `help-window` — окрема сторінка документації; посилання Wiki & Solutions, Source code, Run tests.
- `confirm-dialog` — перед Reset і Undo reset.
- Головного меню й списку рівнів нема: перехід — посиланням «Next challenge» або хешем URL.

## Фічі поза полем
- `levels-sequential`: 19 челенджів, де ростуть поверхи, ліфти, потік і різниться місткість; #19 — «Perpetual demo».
- Код і масштаб часу зберігаються в localStorage браузера.
- `speed-control` (масштаб часу) і `pause`.
- Стан у URL-хеші — посилання прямо на челендж з потрібною швидкістю.
- Тести рушія (`test/index.html`), відкриті сирці; розвʼязки спільнота збирає у вікі.
- Нема рекордів, акаунтів і очок: результат челенджу — лише «так / ні» плюс метрики.

## Варіації й родичі
- Родичі в корпусі: [Screeps](screeps.md) (браузерний код-диспетчер юнітів), [Human Resource Machine](human-resource-machine.md) (1D-поле й потік входу-виходу), [Bot arenas](bot-arenas.md) (код проти середовища з метриками).
- Класична задача за кадром — планування ліфтів (SCAN / LOOK, найближчий вільний, зони поверхів) (?).
- **Осі варіацій**: стиль коду (тік-цикл / події-колбеки) · що оптимізується (пропускна здатність / максимальне очікування / переміщення-енергія) · скільки знає код (кнопки / натиснуті поверхи / усі пасажири) · один ліфт / група з координацією.

## Цікавинки для курсу
- Подієва модель: `on(event, handler)` на обʼєктах ліфтів і поверхів, `init` один раз і `update(dt)` щокадру — 🥉.
- Фізика 1D-ліфта з розгоном, гальмуванням і подією «от-от мину поверх» для рішення зупинитись — 📎.
- Генератор пасажирів зі зваженим вестибюлем і цілями — 🌱 (картка `weighted-spawn`).
- Умова рівня як функція `evaluate(world) → null | true | false` (ще граємо / виграв / програв) — 📎.
- Метрики: ковзне середнє й максимум очікування, пропускна здатність, лічильник переміщень — 🌱.
- Диспетчер для кількох ліфтів, що проходить челенджі #11–18 — 🥇.
- Масштаб часу з фіксованими підкроками `dtMax` — однакова симуляція на різних швидкостях — 📎.

## Мапа на каталог
- Є: `code-editor-window` ↔ редактор під полем; `sequential-levels` ↔ 19 челенджів; `collect-quota` ↔ перевезти N людей; `time-out` ↔ межа T с; `move-limit` ↔ межа M переміщень; `spawn-schedule` ↔ потік spawnRate; `weighted-spawn` ↔ вестибюль 1/2, дитина 1/41; `carrier-platform` ↔ ліфт везе пасажирів; `objective-text` ↔ «Challenge #N: …»; `status-panel` ↔ панель метрик; `help-window` ↔ документація; `confirm-dialog` ↔ Reset; `end-screen` ↔ Success / failed; `game-loop` ↔ кадр + підкроки; `game-pause` ↔ старт / пауза; `save-single-slot` ↔ код у localStorage.
- **Нема** → пропозиції карток:
  - `+event-driven-program` «Програма — обробники подій симуляції» · game-logic/program · 🥉.
  - `+destination-queue` «Черга цілей сутності з вставкою на початок» · game-logic/program · 📎.
  - `+direction-indicator-boarding` «Індикатор напрямку вирішує, хто сідає» · entities/interact · 🌱.
  - `+wait-time-metrics` «Середнє й максимальне очікування агентів» · game-logic/score · 🌱.
  - `+challenge-evaluator` «Умова рівня — функція null / true / false» · game-logic/win · 📎.
  - `+elevator-physics-1d` «Розгін і гальмування на лінії» · entities/move · 📎.
  - `+carrier-capacity` «Місткість транспорту за кількістю й вагою» · entities/state · 🌱.
  - `+url-hash-state` «Рівень і налаштування в URL» · interface/settings · 🌱.
  - Уже пропоновані: `+step-run-speed` (масштаб часу), `+solution-metrics`.

## Пропозиції до словників
- `+trigger:event(name)` — спрацювала подія API (idle, passing_floor, stopped_at_floor, кнопки): програма-обробник замість тіку.
- `+effect:enqueue(a, x)` — додати ціль у чергу сутності (goToFloor; з directly — на початок).
- `+effect:clear_queue(a)` — очистити чергу (stop).
- `+ui:metric-panel` — панель метрик рішення.
- `+feature:url-state` — рівень і налаштування в URL-хеші.
- `+axis:control` — значення `event-driven`: гравець пише обробники подій, не послідовність команд.
- `+card:event-driven-program`.

## Джерела
- ⭐ [Elevator Saga](https://play.elevatorsaga.com/) — гра: заголовок челенджу, панель метрик, кнопки, версія 1.6.5, «Made by Magnus Wolffelt and contributors».
- [Документація](https://play.elevatorsaga.com/documentation.html) — `init` / `update`, API ліфта й поверху, події, поради (Reset, швидкість, devtools).
- [GitHub: magwo/elevatorsaga](https://github.com/magwo/elevatorsaga) — MIT, репозиторій від 2014-08-15; `challenges.js` (19 челенджів і `evaluate`), `world.js` (спавн, метрики, цикл), `elevator.js` (фізика, Moves), `user.js` (вхід і вихід), `index.html` і `app.js` (шаблони, тексти фідбеку, URL-параметри, localStorage).
- [Wiki & Solutions](https://github.com/magwo/elevatorsaga/wiki/) — розвʼязки спільноти (посилання зі сторінки гри, не відкривав).
- YouTube: пошук «elevator saga solution».

## Непевне
- (?) Рік: репозиторій створено 2014-08-15, у черзі стоїть 2015; дату публічного запуску не бачив.
- (?) Чи код бачить `buttonStates` поверхів і скільки людей чекає — документація описує лише події кнопок.
- (?) Коли гасне кнопка виклику на поверсі: у `elevator.js` гасне лише кнопка в кабіні.
- (?) Документація пише, що код зберігається автоматично, а в `app.js` збереження — кнопкою Save.
- (?) Межі масштабу часу й значення `dtMax` не бачив.
- (?) «SCAN / LOOK» як класика розвʼязків — з загальних знань, вікі не відкривав.
