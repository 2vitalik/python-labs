---
title: Requiem of Reuinis (列乌尼斯的挽歌)
slug: requiem-of-reuinis
aka: [列乌尼斯的挽歌]
family: roguelike
also: [thinky, build-sim]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2026
platforms: [PC (Windows)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3371260/Requiem_of_Reuinis/", best: true, note: "Zaxiquej + Otogen Studio, 15.07.2026; Magic Tower з добовим циклом «розвідка → алхімія → дослідження», 300 предметів, 80 навичок"}
  - {kind: other, url: "https://steamcommunity.com/app/3371260/reviews/?browsefilter=toprated&l=english", note: "відгуки EN: бій ATK/DEF, день як забіг, тимчасові апгрейди, вежі відновлюються, ironman"}
  - {kind: other, url: "https://steamcommunity.com/app/3371260/reviews/?browsefilter=toprated&l=schinese", note: "відгуки CN: виробничі лінії алхімії, 扫荡 (зачистка), головоломки мап, баланс"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Requiem+of+Reuinis+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [key-and-door, hp-damage, item-pickup, cell-click, save-game, difficulty-levels, achievements-window, +deterministic-combat, +damage-preview, +stat-gems, +day-tick, +run-meta-carry, +meta-progression, +production-chain, +research-tree, +crafting-recipes, +equipment-slots, +equip-loadout, +retreat-anytime, +daily-dungeon-reset, +auto-sweep-cleared, +map-side-puzzles, +no-dead-ends]
proposes: ["+trigger:day_start", "+effect:retreat", "+effect:fight(a, b)", "+effect:stat(a, name, ±n)", "+effect:craft", "+window:research-window", "+window:crafting-window", "+window:area-select", "+feature:sweep", "+feature:mode-ironman"]
author: opus
date: 2026-11-09
---

# Requiem of Reuinis — Magic Tower як щоденна експедиція: вежа не проходиться за день, сила росте в алхімічній лабораторії

## Суть
Друга гра Zaxiquej (див. [soulestination](soulestination.md)) у жанрі [magic-tower](magic-tower.md): клітинні руїни з ключами, дверима, ворогами з видимими числами й самоцвітами, бій вирішують лише ATK і DEF. Нове — **добовий цикл «Explore → Alchemize → Research»**: щодня обираєш руїну, ідеш, доки вистачає ресурсів, потім гинеш або відступаєш; здобуті матеріали йдуть у виробничі лінії алхімії, а дослідження перетворюють їх на постійні стати, слоти спорядження й рецепти. Вежі задумано **непрохідними з першого дня** — поразка є частиною прогресу, а «мертвих кінців» (софтлоків) класичної вежі нема.

## Поле і час
- Руїни/вежі — ручні сітки (не процедурні), відновлюються щодня разом з ворогами й тимчасовими апгрейдами.
- Усередині — покроково, як у Magic Tower; між виходами — день як одиниця часу. Часового штрафу нема: «плин часу не несе загибелі».
- `info: full` — числа ворогів видно на мапі червоним.
- Шари: поле руїни + база (алхімія, дослідження, спорядження) між днями.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Тасія (героїня) | player | HP, ATK, DEF, навички, слоти спорядження | ходить руїною; бій «наступанням» |
| Ворог | enemy | HP, ATK, DEF, число на мапі | стоїть; результат бою детермінований |
| Бос | boss | фази, навички | прихований бос у 3-й фазі нищить спорядження (відгук) |
| Двері / ключ | gate / pickup | — | ключ відчиняє двері; ключі — дефіцит |
| Тимчасовий апгрейд | pickup | +стат | діє до кінця дня, щодня зʼявляється знову |
| Скриня з самоцвітом | container | +ATK / +DEF | постійне посилення |
| Матеріал | resource | вид | збирається в руїні → алхімія/дослідження |
| Виробнича лінія алхімії | spawner | продукт | щодня видає ресурс; перебудовується під нові продукти |
| Дослідження | switch | ціна в матеріалах | відкриває рецепти, слоти, постійні стати |
| Спорядження | pickup | ~300 шт., деякі з випадковими ефектами | збирається в білд |
| Навичка (закляття) | pickup | ~80, PP | бойові ефекти; регенерація HP, ланцюгові лазери |
| Головоломка мапи | zone | ~3 на мапу (відгук) | Морзе, шахи, календар, слоти збереження; нагорода — спорядження |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(hero, dir)`.
- КОЛИ `contact(hero, enemy)` → ТО `custom: «бій миттєвий, результат = f(ATK, DEF)»`, `damage(hero, n)`, `disappear(enemy)`.
- КОЛИ `contact(hero, door)` → ЯКЩО `has(hero, key)` → ТО `take(hero, key)`, `disappear(door)`; інакше `block`.
- КОЛИ `picked(hero, temp_upgrade)` → ТО `custom: «+стат до кінця дня»`.
- КОЛИ `contact(hero, chest)` → ТО `custom: «постійний +ATK / +DEF»`.
- КОЛИ `picked(hero, material)` → ТО `counter(material, +n)`.
- КОЛИ `input(retreat)` → ТО `custom: «вийти з мапи будь-коли; день завершено»`.
- КОЛИ `hp_zero(hero)` → ТО `custom: «день завершено поразкою»` (що зберігається — див. «Непевне»).
- КОЛИ `custom: «новий день»` → ТО `custom: «руїни, вороги й тимчасові апгрейди відновлюються»`, `custom: «виробничі лінії видають ресурси»`.
- КОЛИ `input(alchemy)` → ТО `choose(options)` — що «вирощувати»: зілля, більший дроп матеріалів, бойові апгрейди.
- КОЛИ `input(research)` → ЯКЩО `has(player, materials)` → ТО `custom: «відкрити рецепт / слот спорядження / постійний стат»`.
- КОЛИ `input(sweep)` → ЯКЩО `custom: «мапу вже підкорено й 扫荡 відкрито»` → ТО `custom: «миттєво зібрати ресурси мапи»`.
- КОЛИ `custom: «головоломку мапи розвʼязано»` → ТО `give(hero, equipment)`; пізній патч дозволяє пропустити (підказка або нагорода одразу).
- КОЛИ `input(equip)` → ЯКЩО `custom: «є вільний слот»` → ТО `custom: «спорядження в білд»`.
- КОЛИ `custom: «день-ціль ironman настав»` → ЯКЩО `mode(ironman)` → ТО `custom: «перевірка цілі дня»` (наслідок не описано).
- Перемога: пройти руїни й сюжет. Поразка: лише на день — гра не має безвихідних станів. Рахунок: нема (досягнення Steam).

## Керування і ввід
- Клавіатура або лише миша (категорія Steam «Mouse Only Option»); «грається без таймінгу».
- Між днями — меню бази: вибір руїни, алхімія, дослідження, спорядження й навички.
- Save Anytime (Steam).

## Вікна, меню, HUD
- `game-screen` — руїна, стати героїні, числа ворогів червоним на мапі (`damage-preview`).
- `area-select` (?) — щоденний вибір руїни/вежі.
- `crafting-window` — алхімія: виробничі лінії й продукти.
- `research-window` — дерево досліджень (гравці скаржаться на незручний UI).
- `inventory-window` — ~300 предметів, слоти; вікно навичок з PP.
- `save-slots` — збереження; частина головоломок використовує слоти збереження.
- `difficulty-select`, `mode-select` (ironman), `settings-window` (гучність), `achievements-window`.
- Переходи: база → вибір руїни → `game-screen` → відступ/смерть → база (новий день).

## Фічі поза полем
- `meta-progression`: «90 % сили — поза забігом» (відгук) — дослідження, постійні стати, слоти.
- `mode-hardcore`-подібний **ironman** з явними цілями на дні (додано після релізу).
- `difficulty-presets` (Adjustable Difficulty), `cloud-save`, `achievements`, `stats` (Steam), `localization` (EN, CN, JA, RU).
- `+feature:sweep` — автозачистка підкорених мап.

## Варіації й родичі
- [magic-tower](magic-tower.md) — ядро (ключі, детермінований бій, самоцвіти); [soulestination](soulestination.md) — попередня гра студії; [tactical-nexus](tactical-nexus.md) — мета-валюта між вежами (сонячні камені), але без добового циклу.
- Відмінність від класики: вежа — не одноразовий пазл, а ресурсна шахта, що відновлюється щодня; дефіцит ключів лишається, але помилка коштує день, а не забіг.
- Осі варіацій: **одиниця спроби** (вся вежа / день) · **прогрес** (лише в забігу / постійний поза ним) · **ресурс** (лише зібране / виробництво між днями) · **софтлок** (можливий / виключено дизайном).

## Цікавинки для курсу
- День як забіг: тимчасові апгрейди скидаються, постійні лишаються — 📎 (два шари стану).
- Виробничі лінії: щодня кожна лінія дає продукт, нові продукти вимагають перебалансування — 🥉.
- Дерево досліджень з ціною в матеріалах, що накопичуються кілька днів — 📎.
- Автозачистка підкореної мапи (детермінізм → результат відомий без проходу) — 🌱.
- Головоломки на мапі з нагородою-спорядженням (Морзе, календар, слоти збереження) — 🥉.

## Мапа на каталог
- Є: `key-and-door` · `hp-damage` · `item-pickup` · `cell-click` (керування лише мишею) · `save-game` · `difficulty-levels` · `achievements-window`.
- **Нема** → пропозиції карток:
  - `+retreat-anytime` «Вийти з рівня з усім зібраним будь-коли» · game-logic/win · 🌱.
  - `+daily-dungeon-reset` «Рівень відновлюється щодня з ворогами й тимчасовими бонусами» · levels/progression · 📎.
  - `+auto-sweep-cleared` «Миттєва зачистка вже підкореного рівня» · game-logic/economy · 🌱.
  - `+map-side-puzzles` «Необовʼязкові головоломки на мапі за спорядження» · levels/progression · 🥉.
  - `+no-dead-ends` «Дизайн без софтлоку: поразка лише відкладає» · levels/solvability · 📎.
  - `+deterministic-combat`, `+damage-preview`, `+stat-gems`, `+day-tick`, `+run-meta-carry`, `+meta-progression`, `+production-chain`, `+research-tree`, `+crafting-recipes`, `+equipment-slots`, `+equip-loadout` — уже пропоновані корпусом.

## Пропозиції до словників
- `+trigger:day_start` — почався новий ігровий день (скидання й виробництво).
- `+effect:retreat` — добровільно покинути рівень зі здобиччю.
- `+effect:fight(a, b)` — атомарний детермінований бій.
- `+effect:stat(a, name, ±n)` — змінити ATK/DEF.
- `+effect:craft` — виготовити продукт з матеріалів.
- `+window:research-window`, `+window:crafting-window` — дослідження й алхімія.
- `+window:area-select` — вибір зони/руїни на день (ширше за `level-select`: зони відновлюються).
- `+feature:sweep` — автозачистка пройдених рівнів.
- `+feature:mode-ironman` — режим з обовʼязковими цілями на дні.

## Джерела
- ⭐ [Steam: Requiem of Reuinis](https://store.steampowered.com/app/3371260/Requiem_of_Reuinis/) — «ядро класичної Magic Tower», цикл Explore–Alchemize–Research, вихід будь-коли без штрафу часу, ключі й маршрути, 300 предметів і 80 навичок, «без безвихідних станів».
- [Steam: відгуки EN](https://steamcommunity.com/app/3371260/reviews/?browsefilter=toprated&l=english) — бій лише ATK/DEF, день = забіг, тимчасові апгрейди відновлюються, вежі не проходяться з першого дня, самоцвіти в скринях, ironman.
- [Steam: відгуки CN](https://steamcommunity.com/app/3371260/reviews/?browsefilter=toprated&l=schinese) — виробничі лінії, 扫荡, ~3 головоломки на мапу, числа ворогів червоним, RPG Maker.

## Непевне
- (?) Що лишається після смерті в руїні: матеріали забігу чи нічого (відгуки кажуть лише «гинеш або відступаєш»).
- (?) Компаньйони згадані в короткому описі Steam («з компаньйонами»), але відгуки їх не описують — у сутності не внесено.
- (?) Формула бою (хто бʼє першим, спецздібності) — не описано; «результат вирішують ATK і DEF».
- (?) Частина спорядження має випадкові ефекти (відгук) — тому `random: none` стосується ядра, не всього білду.
- (?) Наслідок провалу цілі дня в ironman; чи ironman забороняє перезавантаження.
- (?) Рух 4-напрямний і сходи між поверхами — за жанром, прямо в джерелах не названо.
