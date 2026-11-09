---
title: The Castle Doctrine
slug: castle-doctrine
aka: [Castle Doctrine, TCD]
family: roguelike
also: [build-sim, thinky]
klass: hybrid
axes:
  field: square
  time: turn
  opponent: online
  info: hidden
  random: none
  goal: state
year: 2014
platforms: [Windows, macOS, Linux]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/The_Castle_Doctrine", best: true, note: "ядро: дім-сейф, грабунок чужих домів зі списку, self-test, permadeath, інструменти, сімʼя, blueprints"}
  - {kind: steam, url: "https://store.steampowered.com/app/249570/The_Castle_Doctrine/", note: "turn-based, без випадковості, асинхронний MMO, 1991 рік"}
  - {kind: other, url: "https://github.com/jasonrohrer/CastleDoctrine", note: "public-domain код: houseObjects (45 обʼєктів), tools (13), transitions.txt — повна таблиця взаємодій"}
  - {kind: other, url: "https://raw.githubusercontent.com/jasonrohrer/CastleDoctrine/master/gameSource/gameElements/transitions.txt", note: "таблиця переходів станів: струм, мобілі, інструменти"}
  - {kind: other, url: "https://raw.githubusercontent.com/jasonrohrer/CastleDoctrine/master/gameSource/gameElements/houseObjects/propertiesExplained.txt", note: "словник властивостей обʼєктів: deadly, deadlyAdjacent, conductive, mobile, playerSeeking…"}
  - {kind: other, url: "https://raw.githubusercontent.com/jasonrohrer/CastleDoctrine/master/gameSource/languages/English.txt", note: "усі рядки UI: self-test, рюкзак, копи, security tapes, аукціони"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=The+Castle+Doctrine+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-4dir, impassable-cells, interaction-table, cell-transform, destructible-blocks, button-toggle, touch-death, environment-death, chase-player, inventory, inventory-items, inventory-limit, round-currency, shop-catalog, shop-buyback, in-game-editor, editor-palette, editor-undo, editor-playtest, async-multiplayer, replay, fog-of-war, reach-exit, permadeath, player-death, time-out, keyboard-controls, cell-click, +self-test-required, +power-grid, +electric-signal, +trapdoor-fake-floor, +flee-from-player, +family-exit-path, +single-use-tool, +robbery-list, +security-tape, +blueprint-preview, +chill-lockout, +idle-death, +bounty-economy, +gallery-auction]
proposes: ["+cond:powered(cell)", "+cond:path_exists_empty(a, exit)", "+effect:power(net)", "+effect:apply_tool(tool, cell)", "+effect:steal(vault)", "+role:tool", "+role:family", "+window:rob-list", "+window:house-editor", "+window:load-backpack", "+window:security-tapes", "+window:blueprint", "+window:auction-window", "+ui:backpack-slots", "+ui:balance", "+ui:change-highlights", "+ui:shroud-toggle", "+feature:self-test", "+feature:chill-timer", "+feature:idle-timeout"]
author: opus
date: 2026-11-09
---

# The Castle Doctrine — побудуй дім-пастку, сам пройди до сейфа, грабуй чужі доми; одна смерть

## Суть
Асинхронний MMO на клітинній мапі будинку: власник ставить стіни, двері, ями, електропідлогу, проводку з вимикачами й собак навколо свого сейфа, а потім **мусить сам дійти до сейфа без інструментів** (self-test) — лише тоді дім стає доступним для грабіжників. Інші гравці обирають дім зі списку, купують інструменти в рюкзак і проходять його покроково; одна помилка — смерть персонажа назавжди. Вся фізика — детермінований **автомат станів обʼєктів** (`transitions.txt`): струм, мобілі, інструменти змінюють стан клітин за таблицею. Гра Джейсона Рорера, 1991 рік у сеттингу, сімʼя (дружина й двоє дітей) живе в домі.

## Поле і час
- Квадратна сітка дому; зовнішні стіни постійні, всередині — довільне планування. Розмір дому (?).
- Покроково: кожен крок гравця — тік; після нього мобілі (собаки, коти, сімʼя) роблять хід, а струм перераховується по мережі (обмеження 32 кроки поширення).
- Під час грабунку — **туман видимості** (shroud): стіни блокують погляд (`visionBlocking`); власник у редакторі бачить усе.
- Два шари клітини: обʼєкт (стіна, підлога, двері, дріт…) і шар мобілів (`mobile` — можуть ділити клітину з нерухомим обʼєктом).
- Реальний час довкола ходів: 5 хвилин бездіяльності в чужому домі — смерть; ліміт грабунку — 10 хвилин, потім «Sirens?» і копи.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Грабіжник / власник | player | рюкзак, гроші | рух 4 напрямки; застосовує інструмент до клітини |
| Вхід (start) | static | — | звідси заходить грабіжник; сюди тікає сімʼя |
| Сейф (vault_goal) | static | гроші, інструменти, картини | ціль: дійти — забрати вміст |
| Зовнішня стіна | static | permanent | не редагується, не руйнується |
| Дерев'яна стіна | static | — | пилка, факел, бомба руйнують |
| Металева стіна | static | — | лише факел |
| Бетонна стіна | static | — | лише бомба |
| Стіна з проводкою | conduit | conductive | проводить струм; пилка/факел/бомба — різні наслідки |
| Вікно | static | blocking | лом, цегла, кийок, бомба бʼють; факел — інакше |
| Двері-штовхалки (door_push) | gate | — | відчиняються, коли гравець або тварина в них входить |
| Електродвері (power_door) | gate | струм | під струмом зачинені (blocking); мобіль у проході тримає відчиненими |
| Яма | hazard | deadly | смерть для гравця й тварин; драбина перекриває |
| Люк (trapdoor) | hazard | струм | один стан deadly, другий — безпечний; перемикається струмом |
| Електропідлога | hazard | струм | під струмом deadly для всіх, хто стає |
| Джерело струму | source | powered | живить сусідні клітини; вода закорочує |
| Дріт · дріт лише горизонтальний / вертикальний | conduit | вісь | проводить у 4 / 2 напрямки; кусачки ріжуть |
| Місток проводів | conduit | — | перетин двох ліній без замикання |
| Вимикач-перемикач · «натиснутий» · поворотний | switch | on/off | мобіль на клітині перемикає 1↔2; on = провідний |
| Вимикач, що залипає | switch | — | лише вмикається й лишається; лом виламує |
| Реле · інвертоване реле | switch | живлення з півночі | живлення з півночі вмикає провідність зліва-направо; інвертоване — навпаки (?) |
| Індикатор (провідний / непровідний) | conduit | — | світиться під струмом; бʼється ломом, цеглою, кийком |
| Тривожна кнопка (panic_button) | switch | — | член сімʼї стає — стає провідною (замикає коло) |
| Пітбуль | enemy | playerSeeking | побачив грабіжника → іде до нього; на одній клітині — смерть |
| Чихуахуа | enemy | playerSeeking | побачив → іде слідом; сам не вбиває (?) |
| Кіт | neutral | playerAvoiding | побачив → тікає від грабіжника |
| Дружина | ally | family | побачила грабіжника → тікає до виходу; на рушниці бере зброю |
| Дружина з рушницею | enemy | deadlyAdjacent | вбиває грабіжника на сусідній клітині |
| Рушниця (wife_shotgun) | pickup | — | лежить у домі; дружина на ній озброюється |
| Син / донька (до 4 варіантів) | ally | family | тікають до виходу; потребують вільного шляху |
| Інструменти (13) | pickup | разові | купуються в рюкзак, кожен застосовується до клітини |

**Інструменти:** лом (вікна, двері, реле, залиплий вимикач, індикатор, тварини, сімʼя) · кийок (вікна, індикатори, тварини, сімʼя) · цегла (вікна, двері, індикатори, **перемикає вимикач на відстані** (?), кіт і чихуахуа) · пістолет (усі тварини й люди) · пилка (дерево) · факел (дерево, метал, вікно) · бомба з аміачної селітри (бетон, дерево, вікно) · кусачки (дріт, місток, знеструмлена електропідлога) · вода (закоротити джерело струму або підлогу під струмом) · драбина (через яму чи люк) · клин (заклинити електродвері відчиненими) · отруєне мʼясо (присипляє пітбуля й чихуахуа) · вольтметр (показував, чи дріт під струмом; згодом прибраний).

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(player, dir)`; стіни, вікна, зачинені двері — `block`.
- КОЛИ `custom: «кінець кроку гравця»` → ТО `custom: «мобілі роблять хід, потім струм перераховується по мережі (до 32 кроків)»`.
- КОЛИ `custom: «перерахунок струму»` → ТО `custom: «клітина під струмом, якщо звʼязана з джерелом через conductive-клітини; дріт-горизонталь/вертикаль проводить лише вздовж осі; місток не замикає перетин»`.
- КОЛИ `state_on(wire, powered)` → ТО `set_state(wire, powered)` (видно на індикаторі).
- КОЛИ `state_on(floor_electric, powered)` → ТО `set_state(floor_electric, deadly)`; КОЛИ `enter(player|animal, floor_electric)` → ЯКЩО `state(floor_electric, powered)` → ТО `lose` / `custom: «тварина гине»`.
- КОЛИ `state_on(power_door, powered)` → ЯКЩО `not occupied(door_cell, mobile)` → ТО `set_state(power_door, closed)`; `state_off` → відчинені.
- КОЛИ `enter(mobile, power_door)` → ТО `custom: «двері заклинені відчиненими, доки мобіль у проході»`.
- КОЛИ `state_on(trapdoor, powered)` або `state_off(trapdoor, powered)` → ТО `custom: «люк перемикає безпечний / смертельний стан»` (?).
- КОЛИ `custom: «струм з півночі на реле»` → ТО `set_state(relay, conducts_left_right)`; інвертоване реле — протилежно.
- КОЛИ `enter(mobile, toggle_switch)` → ТО `set_state(switch, flip)` (on → провідний); залипаючий — лише on.
- КОЛИ `enter(family, panic_button)` → ТО `set_state(panic_button, conductive)`.
- КОЛИ `enter(player|animal, pit)` → ТО `lose` / `custom: «тварина падає»`; КОЛИ `use(player, ladder)` на ямі → ТО `set_cell(pit, bridged)`.
- КОЛИ `contact(player|animal, door_push)` → ТО `custom: «двері відчиняються»`.
- КОЛИ `line_of_sight(animal|family, player)` → ТО `set_state(a, alert)`: пітбуль/чихуахуа — `custom: «іде до гравця»`, кіт — `custom: «тікає від гравця»`, сімʼя — `custom: «тікає до виходу»`.
- КОЛИ `contact(pitbull_alert, player)` → ТО `lose` («You were killed by: Pit Bull»).
- КОЛИ `enter(wife, shotgun)` → ТО `set_state(wife, armed)`; КОЛИ `adjacent(wife_armed, player)` → ТО `lose`.
- КОЛИ `use(player, drugged_meat)` на пітбулі/чихуахуа → ЯКЩО `state(a, alert)` → ТО `set_state(a, sleeping)`; КОЛИ `contact(player, sleeping_pitbull)` → ТО `custom: «прокидається — смерть»`.
- КОЛИ `use(player, gun|club|crowbar)` на тварині чи члені сімʼї → ТО `transform(a, dead)`; цегла — лише кіт і чихуахуа.
- КОЛИ `use(player, saw|torch|bomb)` на стіні → ЯКЩО `custom: «інструмент бере цей матеріал»` → ТО `set_cell(wall, broken)`; інакше нічого.
- КОЛИ `use(player, crowbar|brick|club)` на вікні → ТО `set_cell(window, broken)`.
- КОЛИ `use(player, wire_cutters)` на дроті / містку / знеструмленій електропідлозі → ТО `set_cell(cell, cut)` — мережу розірвано.
- КОЛИ `use(player, water)` на джерелі струму або підлозі під струмом → ТО `set_state(a, shorted)`.
- КОЛИ `use(player, doorstop)` на відчинених електродверях → ТО `set_state(power_door, wedged)`; лом — зачинені → `set_state(power_door, pried)`.
- КОЛИ `use(player, crowbar)` на реле, залиплому вимикачі, індикаторі → ТО `custom: «виламано»`.
- КОЛИ `use(player, tool)` → ТО `take(player, tool)` — інструмент разовий.
- КОЛИ `reach(player, vault)` → ТО `custom: «рюкзак порожніє, вміст сейфа — у рюкзак»`, `currency(+vault)` (стає твоїм, коли вийдеш (?)).
- КОЛИ `input(leave)` → ТО `custom: «вихід із дому; рюкзак кидаєш на бігу, якщо не дійшов до сейфа»`.
- КОЛИ `timer(robbery_limit)` → ТО `custom: «Sirens?»`; ЯКЩО `input(leave)` після цього → ТО `lose` («The cops shoot you as you leave the house»).
- КОЛИ `idle(5 min)` → ТО `lose` у чужому домі («Five idle minutes are deadly»); у своєму — вихід з редактора.
- КОЛИ `died(player)` → ТО `custom: «персонаж зникає назавжди; гроші, дім, сімʼя втрачені; нове імʼя з трьох слів»` (permadeath).
- КОЛИ `custom: «власник натиснув Done у редакторі»` → ЯКЩО `custom: «зміни є»` → ТО `custom: «self-test: дійти до сейфа без інструментів»`; ЯКЩО `died(owner)` під час тесту → ТО `lose` назавжди.
- КОЛИ `custom: «перевірка редактора»` → ЯКЩО `not path_exists(family, exit)` → ТО `message("Family needs empty path to exit.")`, зберегти не можна.
- КОЛИ `died(player)` у чужому домі або `use(tool)` у ньому → ТО `custom: «дім «дає мороз» — не ввійти певний час (до 24 год)»`.
- Перемога: грабунку — дійти до сейфа й вийти живим; власника — грабіжник загинув у пастці. Поразка: смерть = кінець персонажа. Рахунок: гроші в сейфі; нагорода (bounty) за вбивць і крадіїв.

## Керування і ввід
- Миша — майже все: вибір обʼєкта з палітри й клік по клітині (редактор), вибір інструмента з рюкзака й клік по цільовій клітині (грабунок), кнопки сторінок.
- Рух персонажа — стрілки або WASD (перепризначення — `settings/upDownLeftRightKeys.ini`).
- Ctrl-клік — «піпетка»: скопіювати обʼєкт з дому в палітру; Ctrl-Z — undo в редакторі; Enter — підтвердити «небезпечний» хід.
- Esc — пауза й меню; Alt-Enter — повний екран; у повторі — панорама тими ж клавішами, коли пауза й туман вимкнено.

## Вікна, меню, HUD
- `main-menu` (`LoginPage` → `MenuPage`): Rob (список домів) · Edit house · Security Tapes · Auctions · Gallery.
- `house-editor` (`EditHousePage`): поле дому, палітра обʼєктів з цінами, `balance`, `undo-button`, піпетка, `change-highlights` (що змінилось від останнього разу), рюкзак/сейф (перекласти інструменти, продати все), Done → self-test.
- `rob-list` (`RobPickList`): псевдонім із трьох імен, сума в сейфі, скільки пробували, скільки загинуло; Name Search, Filter, Ignore House, Un-Ignore All.
- `blueprint` (`ViewBlueprintPage`): план дому до входу.
- `load-backpack` (`LoadBackpackPage`): купити інструменти в рюкзак — `shop-window`.
- `game-screen` (`RobHousePage`): поле з туманом, `backpack-slots`, таймер-копи, Leave, Give Up (у self-test), `message`-рядки («You were killed by:»).
- `security-tapes` (`replay-window`): повтори всіх грабунків твого дому («%s stole $%d in %d steps after %d died»), Play Tape, `shroud-toggle`.
- `auction-window` + `gallery`: аукціони картин зі спадною ціною, твоя галерея й архів.
- `end-screen`: «You died» / «You stole $N and these items:»; `confirm-dialog` «Lose everything and start over».
- `pause-menu` (Esc): у чужому домі вийти не можна — «You can't quit now (you'll die)».

## Фічі поза полем
- `async-multiplayer` / `online-multiplayer`: центральний сервер (доступ — для покупців; код сервера public domain); «perma-perma-death» сервери, де після смерті не можна створити нового персонажа.
- `replay` (security tapes, повтор self-test), `blueprint`, `level-editor` = власний дім, `undo` у редакторі, `editor-playtest` обовʼязковий (self-test).
- Економіка: старт $2000; дім і дружина заробляють погодинно, поки ти не в домі; бонус-bounty за крадіжки й вбивства; продаж інструментів із сейфа; картини на аукціоні.
- `mode-hardcore` як єдиний режим: permadeath без варіантів; ліміти 5 хв бездіяльності й 10 хв на грабунок.
- `chill-timer`: дім, де ти загинув чи вжив інструменти, тимчасово «закритий» для тебе.

## Варіації й родичі
- Ідейні родичі з корпусу: [theseus-and-the-minotaur](theseus-and-the-minotaur.md) (детермінований переслідувач, який треба обдурити) · [desktop-dungeons](desktop-dungeons.md) (детермінована головоломка-забіг).
- Будівельний шар — як «рівень-редактор = гра» (Super Mario Maker: щоб опублікувати рівень, треба пройти його самому).
- Осі варіацій: **хто будує рівень** (дизайнер / інший гравець) · **перевірка рівня** (нема / автор мусить пройти / розвʼязувач) · **ціна смерті** (рестарт / втрата забігу / втрата персонажа й дому) · **інформація** (повний план / blueprint / туман).

## Цікавинки для курсу
- `transitions.txt` як рушій: «тригер × обʼєкт:стан → новий стан» — уся гра в одній таблиці — 🥈 (картка `interaction-table`, ідеальний приклад даних замість коду).
- Поширення струму по графу провідних клітин з напрямленими дротами, реле й містками, обмеження 32 кроки — 🥈.
- Self-test: опублікувати рівень можна лише після власного проходження без інструментів (доказ розвʼязності) — 🥉.
- Тварини з простими правилами (шукати / тікати / спати) як рухомі «кнопки»: собака, що біжить за тобою, натискає вимикач — 🥉.
- Перевірка «у сімʼї є вільний шлях до виходу» в редакторі — BFS — 📎.
- Туман видимості з `visionBlocking` і перемикач туману в повторі — 📎.
- Повтор грабунку як послідовність ходів (security tape) — 📎.

## Мапа на каталог
- Є: `move-4dir` · `impassable-cells` · `interaction-table` (transitions.txt) · `cell-transform` · `destructible-blocks` (стіни, вікна) · `button-toggle` (вимикачі) · `touch-death` (пітбуль, яма) · `environment-death` (струм) · `chase-player` (пітбуль, чихуахуа) · `inventory` / `inventory-items` / `inventory-limit` (рюкзак) · `round-currency` · `shop-catalog` / `shop-buyback` (інструменти, продаж) · `in-game-editor` / `editor-palette` / `editor-undo` / `editor-playtest` · `async-multiplayer` · `replay` · `fog-of-war` · `reach-exit` (сейф) · `permadeath` · `player-death` · `time-out` (копи) · `keyboard-controls` · `cell-click`.
- **Нема** → пропозиції карток:
  - `+self-test-required` «Опублікувати рівень лише після власного проходження» · levels/editor · 🥉.
  - `+power-grid` (як у корпусі) + `+electric-signal` — струм по провідних клітинах, реле, місток · entities/state · 🥈.
  - `+trapdoor-fake-floor` (як у корпусі) — люк, що відкривається від струму.
  - `+flee-from-player` «Сутність тікає від гравця, коли бачить» · entities/move · 📎.
  - `+family-exit-path` «Перевірка шляху до виходу для NPC у редакторі» · levels/solvability · 📎.
  - `+single-use-tool` (як у корпусі) — інструмент витрачається на клітині.
  - `+robbery-list` «Список чужих рівнів з лічильниками спроб і смертей» · levels/bank · 🌱.
  - `+security-tape` «Повтор чужої спроби пройти твій рівень» · interface/results · 📎.
  - `+blueprint-preview` «План рівня перед входом без туману» · interface/menus · 🌱.
  - `+chill-lockout` «Тимчасова заборона повертатися на рівень» · game-logic/opponent · 🌱.
  - `+idle-death` «Бездіяльність N хвилин = смерть» · game-logic/lose · 🌱.
  - `+bounty-economy` «Нагорода за голову кривдника» · game-logic/economy · 📎.
  - `+gallery-auction` «Аукціон зі спадною ціною» · game-logic/economy · 📎.

## Пропозиції до словників
- `+cond:powered(cell)` — клітина під струмом (уже пропонували в корпусі); `+cond:path_exists_empty(a, exit)` — шлях без перешкод для NPC.
- `+effect:power(net)` — перерахунок мережі; `+effect:apply_tool(tool, cell)` — інструмент на клітину; `+effect:steal(vault)` — вміст сейфа в рюкзак.
- `+role:tool` (разовий інструмент), `+role:family` (NPC, якого треба вивести); дроти — 🔥 `conduit`, джерело — 🔥 `source`.
- `+window:rob-list`, `+window:house-editor`, `+window:load-backpack`, `+window:security-tapes`, `+window:blueprint`, `+window:auction-window`.
- `+ui:backpack-slots`, `+ui:balance`, `+ui:change-highlights` (що змінилось від минулого візиту), `+ui:shroud-toggle`.
- `+feature:self-test`, `+feature:chill-timer`, `+feature:idle-timeout`.

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/The_Castle_Doctrine) — ядро: сейф, список домів (псевдонім, сума, спроби, смерті), захисти й інструменти, сімʼя, self-test, permadeath, blueprints, perma-perma-death сервери, $2000 на старті.
- [Steam](https://store.steampowered.com/app/249570/The_Castle_Doctrine/) — turn-based, без випадковості, permadeath, асинхронний MMO, 29.01.2014.
- [GitHub: jasonrohrer/CastleDoctrine](https://github.com/jasonrohrer/CastleDoctrine) — повний список houseObjects і tools, сторінки UI (класи *Page), Readme з керуванням, changeLog (32 кроки струму, 5 хв, 10 хв, chills, bounty, зарплати).
- [transitions.txt](https://raw.githubusercontent.com/jasonrohrer/CastleDoctrine/master/gameSource/gameElements/transitions.txt) — таблиця «тригер → обʼєкт:стан → стан» для всіх взаємодій.
- [propertiesExplained.txt](https://raw.githubusercontent.com/jasonrohrer/CastleDoctrine/master/gameSource/gameElements/houseObjects/propertiesExplained.txt) — властивості: deadly, deadlyAdjacent, mobile, playerSeeking/Avoiding, conductive*, family, visionBlocking.
- [English.txt](https://raw.githubusercontent.com/jasonrohrer/CastleDoctrine/master/gameSource/languages/English.txt) — рядки UI (self-test, рюкзак, копи, tapes, аукціони, «Family needs empty path to exit»).
- YouTube: [пошук](https://www.youtube.com/results?search_query=The+Castle+Doctrine+gameplay).

## Непевне
- (?) Розмір дому в клітинах і ціни обʼєктів/інструментів — у відкритих джерелах не бачив.
- (?) Чи гравець (а не лише мобілі) перемикає вимикачі, стаючи на них — у transitions.txt тригер записаний як `mobile`.
- (?) Люк: за властивостями стан 1 (без струму) — deadly, стан 2 (під струмом) — безпечний; тлумачення «струм тримає люк зачиненим» — моє.
- (?) Інвертоване реле — за назвою «навпаки»; файл властивостей стану 1 не знайшов.
- (?) Цегла перемикає вимикачі (у таблиці є переходи switch 1↔2 від цегли) — чи це кидок на відстань, не перевірено.
- (?) Чихуахуа шукає гравця, але не має `deadly` — схоже, лише «водить» за собою на вимикачі.
- (?) Гроші з сейфа стають твоїми при досягненні сейфа чи при виході з дому; дружина «несе» частину грошей (`wifeHolding`) — механіку не розібрав.
- (?) Офіційний сайт thecastledoctrine.net не відкрився (ECONNREFUSED) — у шапку не клав.
