---
title: The Castles of Burgundy (Замки Бургундії)
slug: the-castles-of-burgundy
aka: [Castles of Burgundy, Die Burgen von Burgund, Замки Бургундії, CoB]
family: board-digital
also: []
klass: cursor
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: full
  random: both
  goal: score
year: 2011
platforms: [board, web, PC, mobile]
links:
  - {kind: other, url: "https://rulespal.com/the-castles-of-burgundy/rulebook", best: true, note: "повні правила: 4 дії кубика, ефекти тайлів, 8 будівель, регіони, бонуси кольору, кінець фази, рахунок"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/The_Castles_of_Burgundy", note: "Stefan Feld, alea 2011; огляд, версії (карткова, кубикова, Special Edition), цифрові видання"}
  - {kind: play, url: "https://en.boardgamearena.com/gamepanel?game=castlesofburgundy", note: "грати в браузері (BGA)"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=The+Castles+of+Burgundy", note: "пошук; DIGIDICED 2019"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=The+Castles+of+Burgundy+how+to+play", note: "пошук; правила"}
stage: v1
coverage: 65
mechanics: [cell-click, hover-highlight, legal-move-highlight, event-points, round-currency, completion-detection, hot-seat, turn-enforcement, ai-opponent, online-multiplayer, save-game, rule-variants, game-settings, game-screen, end-screen, help-window, tutorial-window, match-setup, +hex-grid-render, +dice-as-actions, +die-modifier-tokens, +tile-depot-by-die, +connected-placement, +region-complete-bonus, +phase-decaying-bonus, +first-to-achieve-bonus, +color-set-complete, +tile-action, +extra-action-chain, +turn-order-track, +storage-limit, +set-collection-scoring, +phase-rounds]
proposes: ["+trigger:area_complete", "+trigger:phase_end", "+cond:die_value", "+cond:afford", "+effect:take_tile", "+effect:modify_die", "+effect:extra_action", "+effect:sell", "+role:depot", "+role:storage", "+ui:dice-tray", "+ui:depot-board", "+ui:turn-order-track", "+axis:turn-structure"]
author: opus
date: 2026-11-09
---

# The Castles of Burgundy — гекс-маєток: два кубики = дві дії, номер на кубику каже, звідки взяти і куди покласти плитку

## Суть
Кожен розбудовує маєток (duchy) на особистому гекс-полі, де кожна клітина має колір і цифру 1–6. Кожен раунд гравець кидає 2 кубики, і кожен кубик — одна дія: взяти гекс-плитку зі складу з тим самим номером, покласти плитку з запасу на клітину її кольору з тим самим номером поруч із вже покладеними, продати товари цього номера або взяти 2 робітників. Робітники зсувають значення кубика на ±1. Кожна покладена плитка має свій ефект (додаткова дія, товари, гроші, постійні здібності), а заповнений регіон одного кольору дає очки — тим більше, чим раніше.

## Поле і час
- Особистий маєток: гекс-поле (37 клітин (?)) з регіонами за кольором — темно-зелені замки, сірі шахти, жовті монастирі, бежеві міста, сині ріки (кораблі), світло-зелені пасовища; на кожній клітині — цифра 1–6. Стартовий замок — у центрі.
- Біля маєтку: 3 клітини складу для плиток (?), 3 місця для товарів (≤3 різних види), рахунок робітників і срібла.
- Спільне поле: 6 складів-депо з номерами 1–6 (гекси й товари), центральне чорне депо (купівля за срібло), трек очок, трек черги ходу (міст), 5 клітин товарів на фазу, бонус-тайли за кольори.
- Час: 5 фаз (A–E) × 5 раундів; раунд — усі кидають кубики, потім ходять у порядку мосту (2 дії кожен); перед фазою депо поповнюються.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кубик гравця | resource | 2 на гравця, значення 1–6 | кожен — одна дія; значення можна зсунути робітниками |
| Білий кубик | switch | 1, у першого гравця | визначає депо, куди йде товар раунду; для дій не використовується |
| Депо 1–6 | supply | гекси, товари | «взяти плитку» з депо = значення кубика |
| Чорне депо | supply | гекси | купити 1 плитку за 2 срібла раз за хід |
| Склад гравця | supply | 3 клітини (?) | плитки чекають розміщення |
| Клітина маєтку | terrain | колір, цифра 1–6, регіон | приймає плитку свого кольору, якщо цифра = кубик і є сусід |
| Регіон | zone | 1–8 клітин одного кольору | заповнено → очки за розмір + бонус фази |
| Замок | tile | темно-зелений | покладено → додаткова дія з будь-яким значенням кубика |
| Шахта | tile | сіра | наприкінці кожної фази +1 срібло |
| Монастир (тайл знань) | tile | жовтий, номер, ефект | постійна здібність або кінцеві очки |
| Будівля | tile | бежева, 8 типів | разовий ефект; у місті кожен тип ≤1 раз |
| Корабель | tile | синій | взяти всі товари з одного депо + крок на мосту |
| Худоба | tile | світло-зелена, вид тварини, 2–4 тварини | очки = тварини + такі самі на тому ж пасовищі |
| Товар | resource | колір = номер 1–6 | продається дією кубика з цим номером |
| Робітник | resource | жетон | ±1 до значення кубика; 2 = 1 очко наприкінці |
| Срібло | resource | монета | купівля з чорного депо; 1 = 1 очко наприкінці |
| Бонус кольору | pickup | великий / малий | перший / другий, хто заповнив усі клітини кольору |
| Фішка на мості | piece | позиція, стопка | порядок ходу; кораблі просувають, верхній у стопці раніше |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «початок раунду»` → ТО `custom: «усі кидають 2 кубики; перший гравець — і білий»` → `custom: «товар раунду в депо = білий кубик»`.
- КОЛИ `turn_start(player)` → ТО `custom: «2 дії — по одній на кубик; порядок мосту»`.
- Модифікатор: КОЛИ `input(use(worker, die))` → ТО `custom: «значення кубика ±1 (6↔1 по колу (?))»` (`+effect:modify_die`), `take(player, worker)`.
- Взяти: КОЛИ `input(take(tile, depot))` → ЯКЩО `custom: «номер депо = значення кубика»` (`+cond:die_value`) і `custom: «є вільна клітина складу»` → ТО `give(player, tile)` (`+effect:take_tile`).
- Покласти: КОЛИ `input(place(tile, hex))` → ЯКЩО `same(tile, hex, color)` і `custom: «цифра клітини = значення кубика»` і `free(hex)` і `adjacent_count(hex, placed_tile, >=, 1)` → ТО `place(tile, hex)` і ефект плитки; інакше `block`.
- Продати: КОЛИ `input(sell(goods, die))` → ЯКЩО `custom: «номер товару = значення кубика»` → ТО `custom: «продати всі товари цього виду»` (`+effect:sell`), `currency(+1)`, `score(+2/3/4 за тайл)` (2/3/4 гравці).
- Робітники: КОЛИ `input(take_workers(die))` → ТО `give(player, worker ×2)` — будь-яке значення кубика.
- Чорне депо: КОЛИ `input(buy(tile))` → ЯКЩО `afford(player, 2 silver)` і `first_time` (за хід) → ТО `currency(-2)`, `give(player, tile)`; без кубика.
- Замок: КОЛИ `custom: «покладено замок»` → ТО `custom: «додаткова дія з уявним кубиком будь-якого значення»` (`+effect:extra_action`).
- Корабель: КОЛИ `custom: «покладено корабель»` → ТО `custom: «взяти всі товари з одного депо»`, `move(bridge_token, +1)`; ЯКЩО `custom: «зайняв місце першого гравця наступного раунду»` → `give(player, white_die)`.
- Худоба: КОЛИ `custom: «покладено худобу»` → ТО `score(+тварини)` і `score(+тварини тих самих тайлів цього виду на цьому пасовищі)`.
- Будівлі: Ринок — взяти корабель або худобу з депо 1–6 · Тесляр — бежеву будівлю · Церква — шахту, монастир або замок · Склад — продати один вид товару без кубика · Заїжджий двір — 4 робітники · Банк — 2 срібла · Ратуша — одразу покласти ще одну свою плитку будь-якого кольору · Вежа — `score(+4)`.
- КОЛИ `custom: «будівля того самого типу вже є в цьому місті»` → ТО `block` (крім монастиря №1).
- Монастирі: `set_state(player, ability)` — постійні знижки/правила або кінцеві очки (напр. №2: +робітник за шахту, №6: купити за 2 робітники з будь-якого депо, №27: фішка на мості завжди зверху).
- КОЛИ `custom: «регіон заповнено»` (`+trigger:area_complete`) → ТО `score(+за розмір 1–8)` і `score(+бонус фази 10/8/6/4/2 для A–E)`.
- КОЛИ `custom: «заповнено всі клітини одного кольору»` → ЯКЩО `first_time` → ТО `give(player, big_bonus)` (5/6/7 за 2/3/4 гравців); другому — малий; далі — нічого.
- КОЛИ `custom: «кінець фази»` (`+trigger:phase_end`) → ТО `currency(+1 за шахту)`, ефекти монастирів кінця фази, `custom: «прибрати залишки, поповнити депо й чорне депо»`.
- КОЛИ `custom: «кінець фази E»` → ТО `score(+1 за непроданий товар)`, `score(+1 за срібло)`, `score(+1 за 2 робітники)`, кінцеві монастирі → `game_over`.
- Нічия: менше незаповнених клітин маєтку → далі на мості (?).
- Перемога: найбільше очок · Поразка: — .

## Керування і ввід
- (цифрова версія) Кубики в `dice-tray`; drag кубика на депо (взяти), на плитку складу → клітину маєтку (покласти), на товар (продати) або на кнопку «робітники».
- Кнопки «+1/−1» біля кубика витрачають робітників; підсвітка показує, які депо / клітини стали легальними після зсуву.
- Чорне депо — клік по плитці і підтвердження оплати.
- Ефекти плиток з вибором (корабель — яке депо, ринок/церква — що взяти, ратуша — що покласти) — модальні вибори; ланцюги ефектів (замок → дія → ратуша → дія) обробляються чергою.

## Вікна, меню, HUD
(цифрова версія — DIGIDICED/Steam, BGA)
- `main-menu`: Онлайн · Проти AI · Локальна гра · Туторіал · Налаштування.
- `match-setup`: 2–4 гравці, номер дошки маєтку (1–10 / випадково), варіанти й розширення.
- `tutorial-window`: покрокове навчання діям кубиків.
- `game-screen`: свій маєток з цифрами й кольорами; `depot-board` — 6 депо + чорне; `dice-tray`; склад плиток і товарів; лічильники срібла й робітників; `turn-order-track` (міст); трек очок; лічильник фаза/раунд (`progress-bar`); `opponent-boards`; `tooltip` над монастирем/будівлею.
- `custom-window`: вибір у ефектах плиток (корабель, ринок, церква, ратуша).
- `end-screen`: розклад очок (регіони, худоба, продажі, бонуси, монастирі, кінцеві ресурси).
- `help-window`: 8 будівель і список монастирів.
- Переходи: main-menu → match-setup → game-screen ⇄ custom-window → end-screen.

## Фічі поза полем
- `ai-opponent-levels` (Steam), `online-multiplayer` (BGA, Yucata, Steam), `hotseat`, `tutorial`, `save-game`/`continue` асинхронних партій.
- `custom-rules`: дошки маєтку 1–10, варіанти на 2–3 гравців, командна гра, соло, щити, розширення (Border Posts, Inns, Trade Routes, White Castles тощо).
- `rules-page`, `tooltip`-довідка тайлів.

## Варіації й родичі
- Версії: The Card Game (2016), The Dice Game — roll-and-write (2017), Special Edition (2023, розширення Vineyard і Shields).
- Родичі: Five Tribes (`five-tribes.md`), Sagrada (`sagrada.md`, кубики як ресурс), Cascadia (`cascadia-calico.md`, гекс-маєток), Kingdomino (`kingdomino.md`); Stefan Feld — Bora Bora, AquaSphere (кубик = дія).
- **Осі варіацій**: роль кубика (рух / ресурс / номер дії і клітини) · модифікатор (нема / робітник ±1 / перекидання) · бонус регіону (фіксований / спадає з фазою) · черга ходу (по колу / трек мосту).

## Цікавинки для курсу
- Кубик як адреса: одне значення одночасно вибирає депо, клітину маєтку і товар — 🌱.
- Список легальних дій для пари кубиків з урахуванням N робітників (±k по колу) — 📎.
- Розміщення на гекс-полі: колір + цифра + сусідство з покладеним — 📎.
- Регіони одного кольору: заповнення і підрахунок за розміром, бонус за фазою — 📎 (flood fill на гексах).
- Ланцюги ефектів (замок → додаткова дія, ратуша → ще плитка, корабель → товари + міст) як черга подій — 🥉.
- 26 (?) монастирів як модифікатори правил — 🥈 (система «перків», що змінюють інші правила).
- Міст-трек зі стопками як порядок ходу — 📎.
- AI, що оцінює 2 кубики + робітників + чорне депо на кілька раундів уперед — 🥇.

## Мапа на каталог
- Є: `cell-click` · `hover-highlight`, `legal-move-highlight` · `event-points` · `round-currency` ↔ срібло · `completion-detection` ↔ регіон/колір заповнено · `hot-seat`, `turn-enforcement`, `ai-opponent`, `online-multiplayer` · `save-game` · `rule-variants`, `game-settings` · `game-screen`, `end-screen`, `help-window`, `tutorial-window`, `match-setup`.
- **Нема** → пропозиції карток:
  - `+hex-grid-render` · `+connected-placement` · `+first-to-achieve-bonus` · `+tile-action` · `+set-collection-scoring` — як в інших файлах сімʼї.
  - `+dice-as-actions` «Кубик = одна дія, значення — параметр» · game-logic/opponent · 📎.
  - `+die-modifier-tokens` «Жетони ±1 до кубика» · game-logic/economy · 🌱.
  - `+tile-depot-by-die` «Склади з номерами, вибір за кубиком» · game-logic/economy · 🌱.
  - `+region-complete-bonus` «Очки за заповнений регіон за розміром» · game-logic/score · 📎.
  - `+phase-decaying-bonus` «Бонус, що спадає з фазою гри» · game-logic/score · 🌱 · слот {10, 8, 6, 4, 2}.
  - `+color-set-complete` «Перший/другий заповнив усі клітини кольору» · game-logic/score · 🌱.
  - `+extra-action-chain` «Ефект плитки дає ще дію (каскад)» · game-logic/opponent · 🥉.
  - `+turn-order-track` «Порядок ходу за треком зі стопками» · game-logic/opponent · 📎.
  - `+storage-limit` «Обмежений склад (≤3 види товарів)» · game-logic/economy · 🌱.
  - `+phase-rounds` «Фази × раунди з поповненням ринку» · game-logic/opponent · 🌱 · слот {5 × 5}.

## Пропозиції до словників
- `+trigger:area_complete` — регіон заповнено (як у Bärenpark, Project L).
- `+trigger:phase_end` — кінець фази гри (дохід шахт, поповнення депо).
- `+cond:die_value(die, n)` — значення кубика (після модифікаторів) дорівнює N.
- `+cond:afford` — вистачає срібла.
- `+effect:take_tile` · `+effect:modify_die(±n)` · `+effect:extra_action` — додаткова дія з уявним кубиком · `+effect:sell(kind)` — продати всі товари виду.
- `+role:depot` — нумерований склад плиток; `+role:storage` — обмежений склад гравця.
- `+ui:dice-tray` · `+ui:depot-board` · `+ui:turn-order-track` (міст зі стопками).
- `+axis:turn-structure` = `track` (порядок мосту).

## Джерела
- ⭐ [RulesPal: The Castles of Burgundy rulebook](https://rulespal.com/the-castles-of-burgundy/rulebook) — хід, 4 дії кубика, робітники, чорне депо, ефекти всіх типів плиток, 8 будівель, худоба, регіони і бонус фази 10…2, бонуси кольору 5/6/7, кінець фази, кінцевий рахунок, тай-брейк, дошки 1–10.
- [Wikipedia: The Castles of Burgundy](https://en.wikipedia.org/wiki/The_Castles_of_Burgundy) — Stefan Feld, alea/Ravensburger 2011, 2–4 гравці, версії, Yucata 2014, DIGIDICED 2019.
- [BGA: The Castles of Burgundy](https://en.boardgamearena.com/gamepanel?game=castlesofburgundy) — короткі правила, гра в браузері.
- Steam: пошук «The Castles of Burgundy».
- YouTube: пошук «The Castles of Burgundy how to play».

## Непевне
- (?) ⭐ з черги (ultraboardgames.com/the-castles-of-burgundy/game-rules.php) веде на головну UBG — замінено на RulesPal.
- (?) Кількість клітин маєтку (37), клітин складу (3) і монастирів (26) — з памʼяті; RulesPal згадує 3 клітини лише в соло-правилах.
- (?) Очки за регіон за розміром 1…8 — RulesPal дає лише межі 1…36; ймовірно трикутні числа 1, 3, 6, 10, 15, 21, 28, 36.
- (?) Чи робітник зсуває 6 → 1 і 1 → 6 по колу — з памʼяті.
- (?) Тай-брейк: RulesPal — «менше незаповнених клітин», BGA-переказ — «більше порожніх клітин»; другий критерій (позиція на мості) теж розходиться.
- (?) Набір вікон Steam-версії — за загальним описом, не з власного запуску.
