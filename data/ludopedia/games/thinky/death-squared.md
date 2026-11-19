---
title: Death Squared
slug: death-squared
aka: []
family: thinky
also: []
klass: avatar
axes:
  field: 3d
  time: realtime
  opponent: coop
  info: partial
  random: none
  goal: state
year: 2017
platforms: [Windows, macOS, PS4, Xbox One, Switch, iOS, Android]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/471810/Death_Squared/", best: true, note: "трейлер і опис: 1/2/4 гравці, 80 рівнів історії, 40 Party, 45 Vault, Extra Vault 2025"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Death_Squared", note: "SMG Studio, дати й платформи; роботи до цілей свого кольору, рух зсуває платформи, піднімає шипи, вмикає лазери"}
  - {kind: other, url: "https://www.nintendo.com/us/store/products/death-squared-switch/", note: "eShop: режими, Vault 30 + 15 (2019), New Game Plus ×3, фільтр для дальтоніків"}
  - {kind: other, url: "https://gamepressure.com/games/death-squared/zf4be4", note: "опис механік: енергопромені й колірне перекриття, силові поля, сховані шипи, сенсори, телепорти, стоси роботів"}
  - {kind: other, url: "https://www.pocketgamer.com/death-squared/death-squared-review-puzzling-and-yelling-with-friends/", note: "огляд: невидимі блоки, лазери, шипи, падаючі й рухомі платформи, кнопки; керування «як Brothers»"}
  - {kind: other, url: "https://www.theaureview.com/games/video-games-review-death-squared-ps4-2017-makes-death-a-learning-experience/", note: "огляд PS4: червоний і синій, шипи, лазери, розщеплювачі, телепорти, Девід та Iris, друга пара після 50-го рівня"}
  - {kind: other, url: "https://www.cubed3.com/games/reviews/playstation-4/death-squared-2", note: "огляд: стік на робота, смерть скидає рівень, ШІ оцінює за смертями, інверсія керування"}
  - {kind: other, url: "https://www.nintendoworldreport.com/review/44982", note: "огляд Switch: кнопки, лазери, шипи, рухомі платформи, миттєвий рестарт"}
  - {kind: other, url: "https://www.appspy.com/news/death-squared-doubles-the-tricky-challenges-in-this-color-based-ios-puzzler/", note: "iOS: турель повертається разом із блоком, рух зсуває вихід, кнопки з прихованими шипами"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Death+Squared+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [move-by-input, push-object, beam-tracing, teleport-pair, button-toggle, touch-death, environment-death, player-death, death-animation, restart-level, all-on-targets, height-levels, sequential-levels, mode-select, sound-effects, language-picker, +local-coop, +shared-field-coop, +coop-shared-loss, +coop-shared-win, +simultaneous-goal, +laser-blocking, +color-filter, +beam-splitter, +toggle-spikes, +fall-off-map-death, +stack-climb, +multi-agent-sync, +voice-narration, +colorblind-palette, +avatar-linked-objects, +split-stick-dual-avatar, +color-immunity]
proposes: ["+effect:move_group", "+axis:control=split-stick", "+axis:actors=pair", "+card:avatar-linked-objects", "+card:split-stick-dual-avatar", "+card:color-immunity"]
author: opus
date: 2026-11-19
---

# Death Squared — кубороботи мають одночасно стати на цілі свого кольору, а кожен крок одного зсуває світ іншому

## Суть
Кооперативна головоломка SMG Studio: кольорові роботи-куби ходять конструкцією з кубів над порожнечею й мають разом стати на цілі своїх кольорів. Рівні — пастки й привʼязки: рух робота може підняти шипи, зсунути платформи, повернути лазер чи пересунути чужу ціль. Промінь убиває будь-кого, крім робота свого кольору, який його перекриває; кольорові силові поля пропускають лише «свого». Будь-яка смерть — миттєвий рестарт рівня; сюжет тримають диктор Девід (технік Omnicorp) і його ШІ Iris. Соло гравець веде обох роботів — кожного своїм стіком.

## Поле і час
- Рівень — 3D-конструкція з кубів-плиток над порожнечею, ізометрична камера (з 2019 року її можна обертати); роботи — куби розміром із плитку, можуть стояти один на одному.
- Реальний час: робот рухається, доки тиснеш стік; пастки спрацьовують від руху, кнопок і сенсорів. Чи рух строго по клітинах — (?) (див. «Непевне»).
- Поле видно цілком, але частина пасток прихована до спрацювання (сховані шипи, невидимі блоки) — `info: partial`.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Робот | player | колір: червоний, синій; у Party ще жовтий і зелений | рухається своїм стіком; може стати на іншого робота; гине від пасток і падіння |
| Ціль | zone | колір | рівень пройдено, коли всі роботи на своїх цілях; деякі цілі зсуваються від руху роботів |
| Плитка | terrain | висота | опора; за краєм — падіння в порожнечу |
| Привʼязаний блок / платформа | object | привʼязка до робота чи кнопки | зсувається, коли рухається «його» робот або натиснуто кнопку; може зіштовхнути робота з краю |
| Штовхуваний блок | object | — | роботи штовхають; сходинка, щит, підставка |
| Падаюча платформа | terrain | — | обвалюється під роботом (огляд Pocket Gamer) |
| Невидимий блок | static | — | стіна чи підлога, яку видно лише після дотику (?) |
| Шипи | hazard | сховані / видимі | вистрибують з підлоги від кнопки чи руху — робот гине |
| Лазер (енергопромінь) | hazard | колір; турель може повертатись разом із роботом | промінь до першої перешкоди; робот іншого кольору гине, свого — перекриває промінь |
| Розщеплювач променя | static | — | ділить промінь (лише згадка в огляді) |
| Сенсор-розтяжка | switch | — | перетин променя-сенсора змінює мапу |
| Кнопка | switch | — | один робот тисне, щоб відкрити шлях іншому |
| Силове поле кольору | gate | колір; рухоме — везе | прохідне лише для робота свого кольору; для інших — стіна чи міст; рухоме поле перевозить через провалля |
| Телепорт | terrain | пара | переносить робота |
| Плитка-розмальовка | terrain | — | малює візерунок на «обличчі» робота (косметика) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(stick, robot)` → ЯКЩО `free(next_cell)` → ТО `move(robot, dir)`.
- КОЛИ `input(stick, robot)` → ТО `custom: «привʼязані до цього робота блоки, турелі чи цілі теж зсуваються або повертаються»`.
- КОЛИ `contact(robot, block)` → ЯКЩО `free(cell_behind)` → ТО `push(block)`.
- КОЛИ `edge(robot)` → ТО `fall(robot)`, `restart` — зійшов з краю чи зіштовхнула платформа.
- КОЛИ `enter(robot, button)` → ТО `set_state(target, toggled)` — шипи, платформи, проходи для іншого робота.
- КОЛИ `enter(robot, spikes)` → ЯКЩО `state(spikes, up)` → ТО `disappear(robot)`, `restart`.
- КОЛИ `line_of_sight(laser, robot)` → ЯКЩО `not same(robot, laser, color)` → ТО `disappear(robot)`, `animate(explosion)`, `restart`.
- КОЛИ `line_of_sight(laser, robot)` → ЯКЩО `same(robot, laser, color)` → ТО `custom: «промінь зупиняється на роботі — він щит для інших»`.
- КОЛИ `contact(robot, laser_sensor)` → ТО `set_state(map_part, triggered)` — сенсор змінює мапу.
- КОЛИ `contact(robot, force_field)` → ЯКЩО `same(robot, force_field, color)` → ТО `move(robot, dir)`; інакше `block` (поле — стіна або підлога-міст).
- КОЛИ `enter(robot, teleport)` → ТО `teleport(robot, pair)`.
- Роботи можуть стояти один на одному, щоб дістати вищої плитки; як саме робот вилазить нагору — (?).
- КОЛИ `died(robot)` → ТО `restart` — рівень з початку для всіх.
- КОЛИ `level_start` → ЯКЩО `level(in, inverted_segment)` → ТО `invert_controls(level)` — короткий відрізок кампанії з оберненим керуванням.
- КОЛИ `input(stick, robot)` → ЯКЩО `level(>, 50)` → ТО `custom: «друга пара того ж кольору рухається разом із першою»` (?).
- КОЛИ `all_on(robot, goal)` → ТО `win`, `next_level`.
- КОЛИ `idle(n)` → ТО `message(narrator_line)` — диктор бурчить, коли робот довго стоїть; підказує, коли розвʼязок близько.
- Перемога: усі роботи на цілях свого кольору. · Поразка: будь-яка смерть → миттєвий рестарт рівня, життів нема. · Рахунку нема; ШІ коментує спробу за кількістю смертей.

## Керування і ввід
- Геймпад: кожен стік — свій робот; соло ведеш обох, удвох — по роботу; порівнюють із Brothers: A Tale of Two Sons. Інші кнопки — косметика: танець, кліпання, ліхтарик.
- Клавіатура (з v1.1.0, 2017): у Party лівий / правий Shift перемикає, яку пару ботів ведеш (червоний/жовтий чи синій/зелений).
- Switch: TV / tabletop / handheld, Joy-Con на двох, drop-in/drop-out.
- iOS: кооп на одному пристрої — друг керує одним роботом.
- Онлайну нема: лише Parsec (2018) і Steam Remote Play Together (2019).

## Вікна, меню, HUD
- `mode-select`: Story (80 рівнів, 1–2 гравці) · Party (40, до 4) · Vault (30 надскладних, відкривається після кампанії; +15 у 2019) · Extra Vault (BETA, 2025: 42 рівні на двох) · New Game Plus ×3 (2019).
- `main-menu`, `level-select`, `pause-menu` — (?) не бачив.
- `game-screen`: ізометрична конструкція й роботи; субтитри реплік Девіда та Iris (`dialogue-window`-рядок).
- `settings-window`: обертання камери, фільтр для дальтоніків (обидва 2019), мова субтитрів (2017).
- `end-screen` (?): ШІ оцінює гравця за кількістю смертей.
- Кастомізація роботів (декалі, вуса, усмішки, «гоночні» смужки) — `custom-window` (?).
- Переходи: режим → рівень → (смерть) той самий рівень миттєво → (усі на цілях) наступний.

## Фічі поза полем
- `mode-coop`: Story 1–2, Party 2–4; `local-multiplayer` на одному пристрої; онлайн лише через Parsec / Remote Play Together.
- Vault — рівні, «too hard for the main game»; Extra Vault (2025) — рівні, вирізані 2017 року («too hard», «too small», «potential softlocks»), безкоштовно як тест інтересу до Death Squared 2.
- `colorblind-palette`, обертання камери, субтитри кількома мовами.
- Озвучений сюжет (Ricepirate Mick): 80 рівнів історії «Чи дотягне Дейв до кінця?»; пасхалки.
- Досягнення / трофеї, частина — за кількість смертей.

## Варіації й родичі
- Кооп у корпусі: `thinky/ilomilo.md` (двоє назустріч), `thinky/toodee-and-topdee.md` (два персонажі, кооп), `thinky/handshakes.md` (дві руки); рух кольором — `thinky/lock-and-pin.md`; копії, що ходять разом, — `grid-platformer/clony.md`; Binary Land (`maze-arcade/binary-land.md`) — двоє в цілі одночасно.
- Поза корпусом: Brothers: A Tale of Two Sons (два стіки — два герої), Portal 2 (іронічний ШІ-диктор).
- **Осі варіацій**: хто керує — 1 гравець двома стіками / 2 / 4; колір — фільтр (лазер і поле пропускають «свого») / ключ; смерть — рестарт усім (тут) / лише загиблому; звʼязок рухів — незалежні аватари / предмети, привʼязані до аватара / двійники, що повторюють хід.

## Цікавинки для курсу
- Колірні фільтри: промінь не шкодить роботу свого кольору й перекривається ним; поле пропускає «свого» — 📎 (таблиця взаємодій колір × сутність).
- Промінь до першої перешкоди з роботом-щитом і розщеплювачем — 🥉 (`beam-tracing` + колір).
- Предмети, привʼязані до руху робота (зсув платформ, поворот турелі, рух цілі), — 🥉 (подія «рух робота» → список залежних).
- Два аватари одночасно з окремим вводом і спільним рестартом — 📎.
- Роботи стоять один на одному: 3D-сітка з опорою — 🥈.
- Диктор за подіями (смерть, простій, близько до розвʼязку) — 📎 (скриптові репліки на тригери).

## Мапа на каталог
- Є: `move-by-input` ↔ стік; `push-object` ↔ блоки; `beam-tracing` ↔ лазери; `teleport-pair` ↔ телепорти; `button-toggle` ↔ кнопки; `touch-death` + `environment-death` + `death-animation` ↔ шипи, промінь, падіння, вибух; `player-death` + `restart-level` ↔ миттєвий рестарт; `all-on-targets` ↔ роботи на цілях; `height-levels` ↔ висоти й стоси; `sequential-levels` + `mode-select`; `sound-effects`; `language-picker` ↔ мова субтитрів.
- Уже пропоновані іншими: `+local-coop`, `+shared-field-coop`, `+coop-shared-loss`, `+coop-shared-win`, `+simultaneous-goal` (Binary Land), `+laser-blocking` (робот перекриває промінь), `+color-filter` (поле свого кольору), `+beam-splitter`, `+toggle-spikes`, `+fall-off-map-death`, `+stack-climb`, `+multi-agent-sync` (друга пара після 50-го), `+voice-narration`, `+colorblind-palette`.
- **Нема** → пропозиції карток:
  - `+avatar-linked-objects` «Рух аватара рухає привʼязані блоки, турелі, цілі» · entities/move · 🥉.
  - `+split-stick-dual-avatar` «Один гравець — два аватари, кожен на своєму стіку» · interface/input · 📎.
  - `+color-immunity` «Пастка свого кольору не шкодить аватару» · entities/combat · 📎.

## Пропозиції до словників
- `+effect:move_group` — зсунути групу, привʼязану до робота (є пропозиція з Elephant in a Bottle).
- `+axis:control=split-stick` — кожен стік керує своїм аватаром.
- `+axis:actors=pair` — два аватари одночасно в одного гравця.
- `+card:avatar-linked-objects`, `+card:split-stick-dual-avatar`, `+card:color-immunity` — механік нема в каталозі.

## Джерела
- ⭐ [Steam: Death Squared](https://store.steampowered.com/app/471810/Death_Squared/) — трейлер, опис, 80 + 40 рівнів, Vault 45, Extra Vault 2025 (42 рівні на двох), 1/2/4 гравці, озвучка.
- [Wikipedia](https://en.wikipedia.org/wiki/Death_Squared) — SMG Studio, дати (PC/PS4/Xbox 14.03.2017, Switch 13.07.2017, iOS 13.02.2018, Android 28.03.2018); рух роботів зсуває платформи, піднімає шипи, вмикає лазери; Story на 1–2, Party до 4.
- [Nintendo eShop](https://www.nintendo.com/us/store/products/death-squared-switch/) — режими, Vault 30 + 15 (2019), New Game Plus ×3, фільтр для дальтоніків, мови.
- [GamePressure](https://gamepressure.com/games/death-squared/zf4be4) — енергопромінь і перекриття свого кольору, силові поля (мости, перевізники), сховані шипи, рухомі блоки, сенсори, телепорти, плитки-розмальовки, стоси.
- [Pocket Gamer](https://www.pocketgamer.com/death-squared/death-squared-review-puzzling-and-yelling-with-friends/) — невидимі блоки, лазери, шипи, падаючі й рухомі платформи, кнопки; соло як Brothers.
- [The AU Review](https://www.theaureview.com/games/video-games-review-death-squared-ps4-2017-makes-death-a-learning-experience/) — червоний і синій, шипи, лазери, розщеплювачі, телепорти; Девід та Iris; друга пара після 50-го рівня.
- [Cubed3](https://www.cubed3.com/games/reviews/playstation-4/death-squared-2) — стік на робота, смерть скидає рівень, ШІ оцінює за смертями, інверсія керування посеред кампанії.
- [Nintendo World Report](https://www.nintendoworldreport.com/review/44982) — кнопки, лазери й шипи, рухомі платформи, миттєвий рестарт.
- [AppSpy](https://www.appspy.com/news/death-squared-doubles-the-tricky-challenges-in-this-color-based-ios-puzzler/) — турель повертається разом із блоком, рух блока зсуває вихід, кнопки з прихованими шипами.
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=471810&count=30&maxlength=3000) — Party на клавіатурі (Shift), обертання камери, Vault 2019, Extra Vault 2025.
- YouTube: пошук «Death Squared gameplay».

## Непевне
- (?) Чи рух строго по клітинах: кубічні рівні й тег Sokoban кажуть «так», Cubed3 пише про плавне ковзання з повним діапазоном стіка.
- (?) Як робот залазить на іншого робота (підйом платформою чи заїзд) і чи падає з нього.
- (?) Друга пара після 50-го рівня — копіює чи віддзеркалює рух першої.
- (?) Головне меню, вибір рівня, пауза, екран результату й лічильник смертей — не бачив.
- (?) Невидимі блоки й розщеплювачі — лише згадки в оглядах, правил немає.
- (?) iOS-реліз у заголовках оглядів фігурує як «RORORORO» — не перевірено.
