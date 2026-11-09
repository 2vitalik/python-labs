---
title: Kingdom.py
slug: kingdom-py
aka: []
family: program-robots
also: [build-sim]
klass: figure
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: runtime
  goal: state
year: 2026
platforms: [PC (Windows, Linux/SteamOS)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/5430920/Kingdompy/", best: true, note: "повний опис: build(House, 3, 4), економіка на скриптах, городяни з 6 функціями-рисами, торгівля з 6 островами, git / ps / cron / numpy; 12 скриншотів UI"}
  - {kind: other, url: "https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1846651706690009", note: "пост розробника (Roman): натхнення TFWR + RimWorld + SimCity, CPython з numpy/pandas/matplotlib, 36 глав, ~8 год сюжету"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Kingdom.py+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [command-program, user-procedures, sensor-predicates, step-execution, code-editor-window, round-currency, in-round-upgrades, collect-quota, tutorial-window, game-screen, message-log, objective-text, theme-select, save-progress, +real-language-code, +tech-tree-unlock-language, +swarm-separate-programs, +worker-economy, +production-chain, +crop-growth-timer, +live-market-prices, +trading-bot, +district-adjacency-bonus, +inherited-traits, +runtime-error-stop, +external-editor-sync, +in-game-git, +process-console, +repl-console, +variable-watch]
proposes: ["+effect:collect(a)", "+effect:deliver(order)", "+effect:trade(item, n, price)", "+trigger:order_arrived", "+cond:price(item, op, x)", "+window:trade-guild", "+window:code-school", "+window:unlock-tree", "+window:repl-console", "+ui:worker-tabs", "+ui:variable-watch", "+feature:in-game-git", "+feature:external-editor"]
author: opus
date: 2026-11-09
---

# Kingdom.py — містобудування, де ти не клацаєш, а пишеш справжній Python для героїв, змін городян і торгових ботів

## Суть
Острів з ратушею й файлом `main.py`: `change_profession(Builder)`, `build(House, 3, 4)` — і герой іде на ділянку та будує, а редактор підсвічує поточний рядок. Уся економіка тримається на скриптах: податки самі не збираються, поле треба засіяти й зібрати до гниття, пекарні, шахти й кузні утворюють ланцюги, бандити грабують, якщо вартовий не встиг. Сюжет (36 глав) відкриває Python крок за кроком, як дерево відкриває будівлі: змінні, `while`, `if`, `for`, списки й словники, функції, модулі; у фіналі чотири герої ділять роботу через спільну базу даних. Далі — городяни з особистістю з шести Python-функцій, що успадковуються дітьми, і торгівля з шістьма островами за живими цінами.

## Поле і час
- Квадратна сітка острова (у дереві розблокувань — «map 21×21»); координати клітин видно при наведенні («(9, 0)»); будівлі стоять на ділянках, вулиці мають назви.
- Шари: суша з клітинами-ділянками + будівлі + люди, герої, кораблі біля пристані; навколо — море й шість сусідніх островів.
- Час `programmed` у реальному часі: годинник гри (45:12), швидкості 1× / 2× / 4× / 8×, пауза; `wait(n)` віддає час світу; цикл без дії й без `wait()` гра зупиняє сама.
- Випадковість під час гри: шторми, страйки, свята, пожежі, сарана, чутки змінюють ціни й події.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой (Worker 1–4) | player | професія (Builder, TaxCollector…), свій .py-файл | виконує свій скрипт рядок за рядком; ходить до ділянки; виклик — дія з тривалістю |
| Ратуша (town hall) | static | — | старт; `upgrade(X)` в коді веде робітника до ратуші й купує розблокування |
| Будинок (House) | container | запас податку («full») | накопичує податок; платить лише тоді, коли хтось прийде `collect(id)` |
| Поле (Farm) | resource | crop: empty → ripe → rotten | `plant(id)` / `harvest(id)`; зерно гниє, якщо не зібрати вчасно |
| Лісопилка | resource | гаї | зупиняється («stalled»), коли гаї вичерпано |
| Пекарня | container | зерно + дерево → хліб | ланка виробничого ланцюга |
| Шахта | container | їсть хліб | дає руду (?) |
| Кузня | container | залізо → інструменти | ланка ланцюга |
| Пристань і торговий корабель | neutral | замовлення (10 bread → 85 copper), таймер 150 с | чекає товар; відпливає, якщо не довезли |
| Бандити | enemy | ціль (b6), «12 s until they strike» | припливають і грабують дім, якщо не прийшов вартовий: `defend(id)` |
| Вартовий (the watch) | ally | — | захищає; деякі беруть хабарі |
| Городянин | neutral | 6 функцій-рис: love, work, hands, conscience, warmth, temper; вік, родина | працює, отримує платню, купує, платить податки; закохується, народжує дітей, старіє; дехто краде |
| Привид | neutral | — | померлі блукають, доки нема кладовища |
| Острови-сусіди (6) | — | ціни на 7 товарів | ринок Trade Guild, замовлення й pull request-и |
| Великі проєкти | object | дуже дорогі | маяк, обсерваторія, великий амбар, собор, королівський палац |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `exec(build(type, x, y))` → ЯКЩО `free(cell)` і `has(town, cost)` → ТО `custom: «герой іде до ділянки»`, `place(hero, building)`.
- КОЛИ `exec(change_profession(p))` → ТО `set_state(hero, p)` (дозволяє дії професії: збір податків, будівництво…).
- КОЛИ `timer(every)` → ТО `counter(house_stock, +n)`; КОЛИ `exec(collect(id))` → ЯКЩО `custom: «stock > 0»` → ТО `currency(+stock)`.
- КОЛИ `exec(plant(id))` → ЯКЩО `state(farm, empty)` або `state(farm, rotten)` → ТО `set_state(farm, sown)`; КОЛИ `custom: «зерно дозріло»` → ТО `set_state(farm, ripe)`.
- КОЛИ `timer(every)` → ЯКЩО `state(farm, ripe)` → ТО `set_state(farm, rotten)` (якщо довго не збирати).
- КОЛИ `exec(harvest(id))` → ЯКЩО `state(farm, ripe)` → ТО `give(town, grain)`, `message("Fresh harvest! 8 grain")`.
- КОЛИ `custom: «гай лісопилки вичерпано»` → ТО `set_state(lumberyard, stalled)`.
- КОЛИ `custom: «пекарня має зерно й дерево»` → ТО `custom: «виробляє хліб»`; шахта витрачає хліб; кузня перетворює залізо на інструменти.
- КОЛИ `custom: «домівкам бракує 4 хлібів на хвилину»` → ТО `set_state(town, hungry)`, `multiplier(0.5)` для доходу, доки не поїдять.
- КОЛИ `spawned(bandits)` → ТО `message("Bandits near b6 — 12 s until they strike. Send a guard: defend(id)")`; КОЛИ `timer(12)` → ЯКЩО `not custom: «вартовий дійшов до будинку»` → ТО `take(house, stock)`.
- КОЛИ `custom: «торговий корабель причалив»` → ТО `message(order)`; КОЛИ `exec(deliver(id))` → ЯКЩО `has(town, items)` → ТО `currency(+reward)`; КОЛИ `timer(150)` → ТО `custom: «корабель відпливає, замовлення згоряє»`.
- КОЛИ `exec(market.sell(item, n))` або `exec(market.buy(item, n, island))` → ТО `currency(±n·price)` + `custom: «великі угоди зсувають ціну; гільдія бере 2 %»`; `market.limit_buy(item, n, price, island)` — відкладений ордер.
- КОЛИ `rng(p)` → ТО `custom: «новина (шторм, страйк, свято, пожежа) зсуває ціни на острові»`.
- КОЛИ `pattern(group(3))` (три будівлі поруч) → ТО `multiplier(k)` доходу — район (District) (?).
- КОЛИ `died(citizen)` → ЯКЩО `not custom: «є кладовище»` → ТО `transform(citizen, ghost)`.
- КОЛИ `spawned(child)` → ТО `custom: «кожна з 6 функцій-рис береться від матері або батька, зрідка — мутація»`.
- КОЛИ `exec(upgrade(X))` → ЯКЩО `custom: «can_upgrade(X)»` → ТО `custom: «робітник іде до ратуші»`, `unlock(X)` (у вікні дерева покупка миттєва).
- КОЛИ `custom: «помилка в рядку»` → ТО `crash` + підсвітка рядка й пояснення простими словами.
- КОЛИ `custom: «нескінченний цикл без дії й wait()»` → ТО `crash` (гра зупиняє програму).
- КОЛИ `counter(income_per_min, >=, 300)` → ТО `next_level` (наступна глава; напр. глава «Districts»).
- Поразки як такої нема (?); мета — глави сюжету, далі великі проєкти.

## Керування і ввід
- Ввід — **справжній Python 3** (CPython у грі) у вікнах коду: підсвітка, автодоповнення, сніпети; ▶ Run, ■ Stop (Shift+F5), ⏸ пауза, крок; панель змінних під кодом («farm = b15 crop = ripe»); статус «running · line 9 · Waiting 1 s».
- API світу (зі скриншотів і опису): `build`, `change_profession`, `collect`, `building_at(x, y)`, `buildings(Farm)`, `inspect(id)["crop" | "stock"]`, `plant`, `harvest`, `orders()`, `deliver`, `num_items`, `per_minute`, `defend`, `wait`, `can_upgrade`, `upgrade`, `market.buy / sell / limit_buy`, `town.people()`, `town.match()`.
- Консоль `>>>` — виконує вираз на вільному робітникові й відповідає про місто; команди процесів `ps`, `top`, `kill`, `cron` — кожна програма є процесом.
- Файли: `shifts/farmer.py` — програма зміни для професії городян; `workers/worker_N.py` — скрипти героїв; редагувати можна у VS Code, гра підхоплює зміни.
- Мишею: панорама острова, кнопки нижньої панелі; будівництво також кнопкою Build (?).

## Вікна, меню, HUD
- `game-screen`: острів; верхня панель — `coins` (мідь) і ресурси (товари, інструменти, дерево, камінь, зерно з «+N/min», хліб, залізо, книги), поточне замовлення корабля з таймером, стан «hungry», годинник, ⏸, 1× / 2× / 4× / 8×, ☰; мітки над будівлями («full», «stalled», «ripe»); `toast` подій угорі.
- Нижня панель: Build · Unlocks · Lessons · Challenges · Files · Guild · Chapters · Help; рядок консолі; `+ui:worker-tabs` — вкладки Worker 1–4 з поточним викликом (`wait(60)`, `plant(farm)`) і кнопками ■ ⏸ ▶.
- Вікно Chapter: «Chapter 29 of 31 · Districts», ціль з прогрес-баром (0 / 300), Hint, Unlock tree →.
- `code-editor` (farm.py, main.py…): плаваючі вікна над островом або плиткою як в IDE; `instruction-highlight`.
- `+window:unlock-tree`: «35 of 44 levels · map 21×21 · workers 4»; вузли Lists & dicts, Farming, Baking, Functions, Commerce, Mining, Scholarship, Workers' Guild, Guild Exchange, Trade Routes, Smithing, Archive (database), Theme Shop, Theme Editor; праворуч — опис, сніпет `upgrade(...)`, Researched / Lesson →.
- `+window:code-school`: 30 уроків Python 3 (Start here, Variables, While loops, If statements, For loops, Lists & dicts…), приклад з Copy, «How it works», «Watch out», «Try it», Open my main.py.
- `+window:trade-guild`: матриця 7 товарів × 6 островів з цінами й трендами, news wire, графік ціни, Bid / Ask, Buy / Sell, кількість 1–100, підказка «In code: market.buy(Iron, 10, Ironhold)».
- Database — вміст спільної бази героїв (`trips = 442`); `+window:repl-console` — журнал подій + REPL.
- Темна й світла теми (Theme Shop / Theme Editor) — `theme-select`.

## Фічі поза полем
- `tech-tree`: конструкції мови й будівлі відкриваються в одному дереві (як у TFWR).
- `tutorial` / `hint` / `show-solution`: Code School з прикладами, підказка й еталонний розвʼязок для кожної глави; ~8 годин для новачка.
- `+feature:in-game-git`: коміти, гілки, мерджі, тести перед кожним комітом; острови надсилають pull request-и до твоїх скриптів.
- `+feature:external-editor`: скрипти — звичайні .py-файли, редагування у VS Code з підхопленням змін.
- Справжні numpy, pandas, matplotlib і requests («запити носять голуби»); кімната алгоритмів — 10 алгоритмів крок за кроком поруч з твоєю версією.
- Порівняння двох версій програми зміни на чергових змінах зі звітами.
- `speed-control`, `pause`, `cloud-save`, `localization` (англійська + 13 мов), демо.
- Challenges у нижній панелі — окремі задачі (?).

## Варіації й родичі
- Родичі в корпусі: `the-farmer-was-replaced` (прямий зразок: дрон на Python-подібній мові, тех-дерево мови), `screeps` (JS-колонія в реальному часі), `computercraft-turtles`, `autonauts` (програмовані робітники-боти); з `build-sim` — Kingdoms and Castles, SimCity-подібні економіки.
- Межа сімʼї: економіка міста як у `build-sim`, але кожна дія — виклик функції в скрипті героя чи городянина.
- Осі варіацій: **мова** (псевдо-Python / справжній CPython з бібліотеками); **хто виконує** (один дрон / кілька героїв / професії городян за «змінами»); **інструменти програміста** (редактор / консоль / git і тести / процеси й cron).

## Цікавинки для курсу
- Будівля накопичує податок, який платить лише при `collect` — модель «запас + збирач» — 🌱.
- Поле з таймерами стадій (порожнє → дозріле → згниле) і цикл обходу ферм — 📎.
- Бандити з відліком і реакцією `defend(id)` — подія з дедлайном — 📎.
- Ринок шести островів: ціни з трендом, новини зсувають ціну, великі угоди рухають ринок — 🥈.
- Особистість як шість функцій, що успадковуються від батьків з мутаціями — 🥇.
- Райони: три будівлі поруч дають бонус доходу — 📎.
- Консоль з процесами `ps / kill / cron` над програмами агентів — 🥈.

## Мапа на каталог
- Є: `command-program` · `user-procedures` · `sensor-predicates` (`inspect`) · `step-execution` · `code-editor-window` · `round-currency` (мідь) · `in-round-upgrades` (`upgrade`) · `collect-quota` (цілі глав) · `tutorial-window` (Code school) · `game-screen` · `message-log` · `objective-text` · `theme-select` · `save-progress`.
- **Нема** → пропозиції карток:
  - `+real-language-code` «Справжня мова (CPython) замість псевдомови» · game-logic/program · 🥈.
  - `+tech-tree-unlock-language` — конструкції мови в дереві розблокувань (як TFWR) · 👑.
  - `+swarm-separate-programs` «Кожен герой — свій файл» · game-logic/program · 🥉.
  - `+worker-economy` «Будівлі працюють, лише коли агент приходить» · game-logic/economy · 🥉.
  - `+production-chain` «Зерно → хліб → шахта → залізо → інструменти» · game-logic/economy · 🥈.
  - `+crop-growth-timer` «Стадії поля з гниттям» · entities/state · 📎.
  - `+live-market-prices` «Ціни з трендом і новинами» · game-logic/economy · 🥈; `+trading-bot` «Торговий бот у коді» · 🥈.
  - `+district-adjacency-bonus` «Бонус за кластер будівель» · game-logic/economy · 📎.
  - `+inherited-traits` «Риси-функції від батьків з мутацією» · entities/state · 🥇.
  - `+runtime-error-stop` «Помилка зупиняє програму й показує рядок» · game-logic/program · 📎.
  - `+external-editor-sync`, `+in-game-git`, `+process-console`, `+repl-console`, `+variable-watch` — інструменти програміста в грі.

## Пропозиції до словників
- `+effect:collect(a)` — забрати накопичений запас будівлі.
- `+effect:deliver(order)` — виконати замовлення товаром.
- `+effect:trade(item, n, price)` — купити / продати на ринку.
- `+trigger:order_arrived` — зʼявилося замовлення з дедлайном (корабель, комісія).
- `+cond:price(item, op, x)` — ціна товару порівняно з X (торговий бот).
- `+window:trade-guild` — біржа островів з графіками й новинами.
- `+window:code-school` — уроки мови з прикладами й «спробуй».
- `+window:unlock-tree` — дерево розблокувань мови й будівель.
- `+window:repl-console` — журнал подій + інтерактивна консоль.
- `+ui:worker-tabs` — вкладки агентів з поточним викликом.
- `+ui:variable-watch` — панель значень змінних під кодом.
- `+feature:in-game-git` — git з тестами всередині гри.
- `+feature:external-editor` — редагування у зовнішньому редакторі з підхопленням.

## Джерела
- ⭐ [Steam: Kingdom.py](https://store.steampowered.com/app/5430920/Kingdompy/) — повний опис механік (податки, поля, ланцюги, бандити, кораблі, городяни, 6 функцій-рис, 6 островів, git, `ps/top/kill/cron`, numpy/pandas), 12 скриншотів: дерево розблокувань, Trade Guild, Code school, редактор з панеллю змінних, консоль, вкладки робітників; реліз 05.11.2026, Kingdom Labs.
- [Пост розробника про демо й натхнення](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1846651706690009) — TFWR / RimWorld / SimCity, пацюки, пожежі, рейди, 36 глав.
- YouTube: пошук «Kingdom.py gameplay».

## Непевне
- (?) Кількість глав: пост — 36, скриншот — «Chapter 29 of 31» (можливо, різні версії).
- (?) Чи будинок / поле займають одну клітину чи ділянку 2×2; як працює `build` для великих проєктів.
- (?) Точна умова району («three buildings close together») і розмір бонусу.
- (?) Що видобуває шахта; хто й коли гасить пожежі; наслідки пацюків у амбарах.
- (?) Чи є поразка (банкрутство, голод) — опис не каже.
- (?) Розділ Challenges і кімната алгоритмів — лише згадки.
- (?) Рядки API зібрані зі скриншотів і опису; повного довідника не бачив.
