---
title: Feed the Scorchpot
slug: feed-the-scorchpot
aka: [Dragon Fodder]
family: board-digital
also: [build-sim]
klass: cursor
axes:
  field: hex
  time: turn
  opponent: none
  info: full
  random: both
  goal: survive
year: 2026
platforms: [PC (Steam, Epic), macOS]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3966510/Feed_the_Scorchpot/", best: true, note: "Moravian (подружжя), видавці Indieformer і WhisperGames; реліз 20.08.2026: 20 років годування дракона, гекс-острів, 50+ будівель, 80+ рецептів, 20+ типів кубиків, демо"}
  - {kind: other, url: "https://www.gameshedge.com/review-feed-the-scorchpot/", note: "огляд із покроковим описом: гекси з типом і числом, пара кубиків = марка, до 3 марок за хід, будівлі збирають із прилеглих гексів, Flavor/Essence/Fodder, сезони, 8 драконів"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3966510&count=30&maxlength=4000", note: "новини й патчі: числа Temple, Altar, Casino, Tollhouse, врожай 70, календар, підказка очікуваного врожаю, кодекс, 8 драконів, 10 складностей, 40 трофеїв, колишня назва Dragon Fodder"}
  - {kind: other, url: "https://rogueliker.com/feed-the-scorchpot-out-now/", note: "Rogueliker: множники в дусі Balatro — ресурси × смак, потім × есенція; кубики активують гекси"}
  - {kind: other, url: "https://vaporlens.app/app/3966510/feed_the_scorchpot", note: "зведення відгуків Steam: ядро — кубики й будівлі на числах «як Catan», скарги на удачу на старті"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Feed+the+Scorchpot+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [round-currency, shop-between-levels, shop-catalog, shop-buyback, in-round-upgrades, collect-quota, difficulty-levels, character-select, codex-window, stats-window, achievements-window, tutorial-window, field-scaling, save-game, game-screen, end-screen, +hex-grid-render, +random-board-setup, +dice-production, +sum-of-two-dice, +dice-roll-pool, +recipe-combine, +score-multiplier-stack, +rent-deadline, +early-finish-bonus, +adjacency-income, +season-cycle, +single-use-tool, +disasters, +shop-reroll, +custom-dice-types, +dice-face-edit, +anti-streak-rng, +run-setup-deck, +run-meta-carry, +boss-variants]
proposes: ["+effect:roll_dice", "+cond:dice_sum", "+effect:craft", "+window:deck-builder", "+ui:season-calendar", "+ui:harvest-forecast", "+card:score-multiplier-stack", "+card:early-finish-bonus"]
author: opus
date: 2026-11-19
---

# Feed the Scorchpot — кидай кубики, щоб гекси острова дали врожай, вари рецепти в котлі й годуй дракона 20 років

## Суть
Роглайт-«кубикова Catan» студії Moravian: острів із гексів, у кожного гекса — тип інгредієнта й число 2–12. За сезон гравець кидає кубики з утриманням, складає з пар кубиків «марки» (сума = число) — і всі гекси з цим числом дають урожай будівлям поруч. Потім інгредієнти (Fodder) переробляються рецептами в котлі Scorchpot, рецепти додають Flavor і Essence, а ті множаться в очки страви — як множники Balatro. Страва має перевищити голод дракона, що росте щороку; не встиг за сезони року — дракон тебе засмажить. Між роками — магазин будівель, рецептів, кубиків і інструментів; контракт — 20 років, далі нескінченний режим.

## Поле і час
- Гекс-острів, щоразу новий з випадкового seed; гекс має тип інгредієнта (зерно, фрукти, мʼясо, риба, молоко) і число 2–12.
- Будівлі стоять між гексами й беруть з прилеглих — вдала позиція торкається трьох гексів (?); поставлені ферми не переносяться.
- Хід = сезон: кидки кубиків (обмежена кількість) → до 3 марок → урожай → готування в котлі. Рік = кілька сезонів (кількість росте з прогресом); кінець року — дукати й магазин.
- Календар показує сезони й «цеглинки» — коли додадуться нові слоти будівель. Голод дракона росте щороку, події («істерики», напади) палять частину острова.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гекс острова | terrain | тип інгредієнта, число 2–12 | марка зі своїм числом активує всі такі гекси |
| Ферма (Farmstead) | static | селяни | збирає інгредієнт прилеглих активованих гексів |
| Святилище (Shrine) | static | — | додає кидки кубиків |
| Гавань / док | static | — | ефект на виплати острова (?) |
| Торговий пост | static | — | додає слоти рецептів |
| Вітряк, пасовище, ранчо, сад, фруктовий сад, плантація | static | базовий врожай 70 (патч 1.02) | дають основний інгредієнт |
| Temple · Altar · Casino · Tollhouse | static | 10 дукатів · 30 інгредієнтів · 4 дукати за невикористаний кидок · 4 дукати за сусідню ферму | бонуси наприкінці року / від сусідства |
| Workshop, Manufactory | static | — | виробляють інструменти |
| Кубик | resource | грані; 20+ типів: непарні, парні, кольорові, «шість шісток», рідкісні, Blessing | кидається; утримані лишаються до наступного кидка |
| Марка | mark | сума пари кубиків | активує всі гекси з цим числом; ≤ 3 за сезон |
| Інгредієнт (Fodder) | resource | кількість за типом | сировина страви; сам дракона не насичує |
| Рецепт | supply | рівень, Flavor / Essence / дукати, штампи | у треї в порядку активації переробляє інгредієнти |
| Інструмент | pickup | разовий | підвищує рівень рецепта, дає двічі вжити рецепт тощо |
| Дукат | resource | — | валюта магазину; нараховується наприкінці року |
| Котел Scorchpot | container | — | тут готують і порівнюють страву з голодом |
| Дракон | boss | голод на рік, особливість; 8 видів | вимагає страву; «істерики» палять острів |
| Карта колоди забігу | supply | ціна в очках колоди (Long Summer 4, Divination 2, Blessing of Plenty) | змінює старт і правила забігу; ліміт очок колоди |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `choose(дракон, режим, колода)`, `custom: «острів з гексів за seed: тип інгредієнта й число 2–12»`.
- КОЛИ `input(buy(building))` → ЯКЩО `counter(ducats, ≥, cost)` і `custom: «є вільний слот будівлі»` → ТО `currency(-cost)`, `place(player, building)`; переставити не можна; поставлена будівля відкриває свій вищий рівень у магазині.
- КОЛИ `input(roll)` → ЯКЩО `counter(rolls_left, >, 0)` → ТО `custom: «перекинути неутримані кубики»`, `counter(rolls_left, -1)`.
- КОЛИ `input(pick(die_a, die_b))` → ЯКЩО `custom: «сума пари = число хоча б одного гекса»` → ТО `mark(sum)`, `counter(marks, +1)`.
- КОЛИ `custom: «поставлено марку n»` → ТО `custom: «кожен гекс з числом n активовано»` → `give(building, ingredient)` кожній будівлі, що торкається гекса.
- КОЛИ `counter(marks, ==, 3)` або `counter(rolls_left, ==, 0)` → ТО `custom: «готування: рецепти з треї по черзі переробляють інгредієнти»`, `score(+fodder)`, `multiplier(×flavor)`, `multiplier(×essence)` і множники будівель/рецептів.
- КОЛИ `counter(meal, ≥, hunger)` → ТО `custom: «рік закрито»`; ЯКЩО `counter(seasons_left, >, 0)` → ТО `counter(prosperity, +n)` — дострокове виконання платить більше.
- КОЛИ `counter(seasons_left, ==, 0)` → ЯКЩО `counter(meal, <, hunger)` → ТО `lose` («пропустив обід — ти наступний у меню»).
- КОЛИ `custom: «кінець року»` → ТО `currency(+n)` за будівлі й пасивні бонуси, `window(shop-window)`, `custom: «голод дракона росте»`.
- Casino: `currency(+4)` за кожен невикористаний кидок · Tollhouse: `currency(+4)` за кожну сусідню Farmstead · Temple: `currency(+10)` · Altar: `counter(ingredients, +30)`.
- КОЛИ `input(use(tool))` → ТО `custom: «разовий ефект на рецепт чи готування»`, `disappear(tool)`.
- КОЛИ `input(sell(item))` → ТО `currency(+value)` (стартові будівлі — 0), `custom: «рахується в загальний дохід»`.
- КОЛИ `rng` / `schedule` → ТО `custom: «істерика дракона палить частину острова»` або `custom: «напад Hubris Hanger»`; подія Farmageddon спалює ферми.
- КОЛИ `custom: «кидок кубика»` → ТО `custom: «псевдовипадковість зменшує серії однакових значень»` (патч 1.04).
- КОЛИ `counter(year, ==, 20)` → ТО `win` (контракт виконано); у повній версії далі — нескінченний режим.
- Перемога: пережити 20 років · Поразка: страва < голоду після останнього сезону року · Рахунок: Fodder × Flavor × Essence × множники; рекорди — у статистиці.

## Керування і ввід
- Миша (є Mouse Only Option) або геймпад (повна підтримка): кидок, вибір кубиків для утримання й пар, перетягнути будівлю чи інструмент на острів (?).
- Масштаб — середня кнопка миші або бампер; авто-наближення, коли тримаєш інструмент чи будівлю (патч 1.04).
- Без вводу на час, «Save Anytime».

## Вікна, меню, HUD
- `character-select`: вибір дракона (Baron — базовий; Count — голодніший, але створює Feeding Ground з більшим врожаєм; Empress — голодніша, але +3 очки колоди).
- `difficulty-select` / `mode-select`: 10 рівнів складності, модифікатори режимів (?).
- `deck-builder` (`custom-window`): колода забігу з лімітом очок колоди; досягнення привʼязані до колод.
- `game-screen`: гекс-острів, лоток кубиків, трея рецептів (тримає порядок активації), котел, голод дракона, `season-calendar` з цеглинками нових слотів; `harvest-forecast` — тултіп гекса з очікуваним урожаєм від поточних марок; тултіпи значень у рецептів і кубиків з конкретним числом (Eintopf, Umami); дракона можна погладити.
- `shop-window`: будівлі (Tier I гарантовано оновлюються), предмети, рецепти, кубики; рерол рецептів; продаж.
- `codex-window` (усі рецепти, будівлі, кубики), `stats-window` (рекорди, прогрес), `achievements-window` («Трофеї», 40 = досягнення Steam), `tutorial-window` («по шматочку»).
- `end-screen` — можна закрити й роздивитись острів (патч 1.03); `settings-window` — гучність, старий саундтрек.
- Переходи: вибір дракона/складності/колоди → game-screen (сезони) → кінець року → shop-window → наступний рік … → end-screen.

## Фічі поза полем
- `difficulty-presets` (10), 8 драконів як модифікатори, `custom-rules` — колода забігу змінює старт і правила.
- `meta-progression` + `unlockables`: усе, що недоступне в демо — апгрейди будівель, унікальні кубики, рерол рецептів, повна колода.
- `mode-endless` після 20 років (лише повна версія); `codex`, `stats`, `achievements`, `cloud-save`, `localization` (EN + 10 мов), `gamepad-support`.
- Демо: необмежені забіги, лише перший дракон і складність, без мета-прогресу, кінець на перемозі.

## Варіації й родичі
- Ранні назва й демо — Dragon Fodder (анонс 2025, перейменовано в січні 2026); демо мало вибрані вручну seed-и, повна версія — випадкові.
- Родичі в корпусі: `board-digital/catan.md` (сума двох кубиків активує гекси з числом, поселення між гексами), `build-sim/luck-be-a-landlord.md` (квота до дедлайну, що росте), `board-digital/ganz-schon-clever.md` (вибір і сума кубиків), `build-sim/dorfromantik.md` і `build-sim/islanders.md` (будування з очками сусідства).
- **Осі варіацій**: як кубик активує клітину (сума двох = число гекса / грань = ряд / кубик кладеться на клітину) · рахунок (сума / база × кілька множників) · тиск (квота за сезони, що росте / таймер) · кубики (стандартні / зі зміненими гранями / типи).

## Цікавинки для курсу
- Генерація гекс-острова з числами 2–12 і активація всіх гексів з числом марки — 📎.
- Кидки з утриманням і вибір до трьох пар-марок: оптимальний вибір пар — пошук по комбінаціях — 🥉.
- Очікуваний урожай гекса: розподіл суми двох кубиків з нестандартними гранями — 🥉.
- Готування: рецепти-трансформації по черзі + Fodder × Flavor × Essence — 📎.
- Голод, що росте щороку, з лімітом сезонів і бонусом за дострокове виконання — 🌱.
- Бонуси сусідства будівель як таблиця правил (Tollhouse за сусідню ферму, Casino за невикористаний кидок) — 📎.
- Псевдовипадковість проти серій однакових граней (патч «Better RNG») — 🥉.

## Мапа на каталог
- Є: `round-currency` ↔ дукати; `shop-between-levels` + `shop-catalog` + `shop-buyback` ↔ магазин між роками з продажем; `in-round-upgrades` ↔ вищі рівні будівель; `collect-quota` ↔ голод дракона; `difficulty-levels` ↔ 10 складностей; `character-select` ↔ дракони; `codex-window`, `stats-window`, `achievements-window`, `tutorial-window`; `field-scaling` ↔ масштаб; `save-game`; `game-screen`, `end-screen`.
- **Нема** → пропозиції карток:
  - `+score-multiplier-stack` «Очки = база × кілька незалежних множників» · game-logic/score · 📎 (Balatro, тут Fodder × Flavor × Essence).
  - `+early-finish-bonus` «Квоту виконано раніше — бонус за невикористаний час» · game-logic/score · 🌱.
  - `+anti-streak-rng` «Кидок, що уникає серій» · levels/generation · 🥉.
  - `+run-setup-deck` «Колода забігу з лімітом очок» · game-logic/economy · 📎.
  - `+dice-production`, `+sum-of-two-dice`, `+dice-roll-pool`, `+rent-deadline`, `+adjacency-income`, `+single-use-tool`, `+disasters`, `+shop-reroll` — уже в корпусі.

## Пропозиції до словників
- `+effect:roll_dice` — кинути (перекинути) кубики пулу; наявне `roll` означає скочування.
- `+cond:dice_sum` — сума вибраних кубиків дорівнює числу (Catan, Feed the Scorchpot).
- `+effect:craft` — переробити інгредієнти за рецептом (котел, верстати).
- `+window:deck-builder` — збирання колоди забігу перед стартом.
- `+ui:season-calendar` — календар сезонів року з позначками майбутніх подій і слотів.
- `+ui:harvest-forecast` — підказка клітини з очікуваним результатом за поточних кубиків.
- `+card:score-multiplier-stack`, `+card:early-finish-bonus` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Feed the Scorchpot](https://store.steampowered.com/app/3966510/Feed_the_Scorchpot/) — опис: угода з драконом на 20 років, кубики → інгредієнти → рецепти → котел, ферми/святилища/гавані на гекс-острові, Flavor і Essence множать Fodder, 20+ кубиків, press your luck; JSON appdetails — 40 досягнень, категорії (контролер, складність, Save Anytime).
- [GamesHedge: огляд](https://www.gameshedge.com/review-feed-the-scorchpot/) — покроково: seed острова, типи й числа гексів, марки з пар кубиків, до 3 марок, будівлі на ребрах/кутах, готування, сезони, процвітання, магазин, інструменти, святилища й торгові пости, дракони Baron/Count/Empress.
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3966510&count=30&maxlength=4000) — патчі 1.01–1.04 (числа будівель, календар, тултіпи, Better RNG, зум), запуск (8 драконів, 10 складностей), демо, Dragon Fodder.
- [Rogueliker](https://rogueliker.com/feed-the-scorchpot-out-now/) — «Balatro-style multiplier system», порівняння з Catan і Carcassonne.
- [Vaporlens](https://vaporlens.app/app/3966510/feed_the_scorchpot) — зведення відгуків: кубики — ядро, будівлі на числах, складний старт.

## Непевне
- (?) Де саме стоять будівлі — на кутах чи ребрах між гексами (огляд каже обидва; зведення відгуків — «на числах»); «до трьох гексів» — за оглядом.
- (?) Скільки кубиків у пулі, скільки кидків і сезонів на старті; чи марка — це обовʼязково пара кубиків, чи бувають інші способи.
- (?) Що саме роблять гавані, Mason's Moorings, штампи рецептів, «Long Summer», «Divination», «Blessing of Plenty» — лише назви з патчів.
- (?) Як рахується процвітання (prosperity) і дукати наприкінці року; формула множників у деталях.
- (?) Пірати, кракени й загарбники з раннього блогу (2025) — чи дійшли до релізу.
