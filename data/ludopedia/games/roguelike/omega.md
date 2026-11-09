---
title: Omega
slug: omega
aka: [Omega RPG, omega-rpg, WinOmega, Omega Rebirth]
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 1987
platforms: [Unix, DOS, Linux, Windows, Amiga (AmiOmega), Mac (MacOmega)]
links:
  - {kind: other, url: "https://setsideb.com/?p=1306", best: true, note: "@Play FAQ: будівлі Рампарта, гільдії й ранги, країна й хаос-шторми, мировоззрення в числах, фази місяця, умови перемоги"}
  - {kind: other, url: "https://www.roguebasin.com/index.php/Omega", note: "RogueBasin: перший роглайк з великою країною й сюжетом, «up in the air»-слот, кілька умов перемоги, версії"}
  - {kind: other, url: "https://crpgaddict.blogspot.com/2011/05/game-55-omega-1988.html", note: "CRPG Addict: анкета «грай собою», будівлі міста, тактична мапа, голод, ціна 8 команд на «зʼїсти курку»"}
  - {kind: other, url: "https://sourceforge.net/projects/omega-roguelike/", note: "SourceForge: код, curses / Win32 / X11"}
  - {kind: other, url: "https://libregamewiki.org/Omega-rpg", note: "Libre Game Wiki: версії 0.80.2 / 0.90.4, вибір гільдій у Рампарті"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Roguelike", note: "Omega першою ввела оверворлд; дивний інвентар"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Omega+roguelike+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-by-input, move-8dir, dungeon-generation, stairs-levels, hp-damage, inventory, inventory-items, inventory-limit, item-pickup, item-identification, hunger-clock, status-effects, unit-xp-skills, round-currency, shop-catalog, shop-buyback, teleport, environment-death, permadeath, player-death, score-records, fog-of-war, message-log, status-panel, keyboard-controls, console-render, +overworld-travel, +town-level, +guild-ranks, +exclusive-memberships, +xp-split, +alignment-shift, +moon-phase-cycle, +day-night-hours, +hand-slot-inventory, +multiple-endings, +questionnaire-character, +dungeon-cache-one, +word-of-recall, +elevator-cell]
proposes: ["+trigger:time_of_day(h)", "+trigger:moon_phase(p)", "+trigger:surrender(monster)", "+effect:shift_alignment(dir, n)", "+effect:join(guild)", "+effect:rank_up(guild)", "+effect:retire", "+cond:alignment(op, x)", "+cond:member(guild)", "+cond:open_hours", "+role:guild-hall", "+role:oracle", "+window:overworld-map", "+window:questionnaire", "+window:guild-window", "+ui:moon-phase", "+ui:clock", "+ui:up-in-air-slot", "+feature:multiple-endings", "+card:guild-ranks", "+card:moon-phase-cycle", "+card:hand-slot-inventory"]
author: opus
date: 2026-11-09
---

# Omega — роглайк-«життя» в ASCII: місто з гільдіями, країна з хаос-штормами, мировоззрення й фази місяця, кілька способів виграти

## Суть
Omega першою дала роглайку **велику країну** (оверворлд) і сюжет: герой стартує в місті Rampart, вступає в гільдії й релігії, ходить між містом, селами, храмами й підземеллями. Ядро — не спуск, а **членства**: кожна гільдія має ранги, досвід ділиться між усіма, де ти член, і гільдії однієї категорії взаємовиключні. Мировоззрення (law/chaos) зсувається вчинками й разом з **фазами місяця** змінює силу в бою. Виграти можна кількома шляхами: вийти на пенсію в купленому кондо, пройти Adept's Challenge, стати головою гільдії.

## Поле і час
- Три масштаби: **місто Rampart** (план фіксований, але частина закладів — за випадковими дверима), **країна** (оверворлд із селами, храмом, лабіринтом-живоплотом з Оракулом, Хаос-морем) і **підземелля**; бій у країні — на окремій тактичній мапі.
- Підземелля: Goblin Caves (ціль — рівень 10), Sewers (ціль — 18) та інші; рівні генеруються при першому відвідуванні й памʼятаються, але **лише для одного підземелля**: вхід в інше перегенеровує попереднє.
- Монстри не переходять між рівнями; підземелля має один вхід згори й знизу; ліфти — підйом вище за верх виводить на поверхню, ще вище — падіння.
- Годинник доби: денні заклади відкриті 7:00–21:00, нічні — навпаки (Злодійська гільдія, бордель). Фаза місяця триває 2 ігрові дні.
- У країні — хаос-шторм щогодини на суші.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | стати з анкети, HP, мана, Power, мировоззрення, членства й ранги | рух, бій, слот «в повітрі» + рюкзак |
| Монстр | enemy | — | бʼється; розумний може здатися |
| Тріфід (кущ) | enemy | — | маскується під живопліт; 1000 досвіду, вбивається солоною водою |
| Смерть (Adept's Challenge) | boss | — | відроджується, лишає косу |
| Охоронці міста | neutral | — | при здачі — у в'язницю |
| Оракул | neutral | — | підказки; веде на Astral Plane |
| Гільдія (Gladiators, Mercenaries, Paladins) | static | категорія Fighting, ранги | бонуси, речі, вимоги |
| Гільдія магів (Collegium Magii, Sorcerors' Guild) | static | категорія Magic | закляття, мана; Sorcerors вимагає chaos |
| Храм бога (Set, Athena, Hecate, Destiny, друїди) | static | категорія Religion | Power, закляття за рангом |
| Thieves' Guild | static | поза категоріями | відмички, ідентифікація, дорожчий продаж |
| Крамниці й послуги (Armory, Pawn Shop, Alchemist, Healer, Gym, Library, Condo, Hospice, Public Works, Autoteller, Brothel, Explorer's Club) | static | години роботи | купити, ідентифікувати, лікувати, качати стати за гроші |
| Село: статуя / вівтар / камінь | static | — | статую розбити (уламки, підказка, монстр); вівтар — гнів бога; камінь може знищити рюкзак |
| Вода | terrain | — | важкий ризикує втратити рюкзак |
| Лава | hazard | — | смертельна (крім жарту з імʼям) |
| Abyss-пастка | hazard | — | телепорт у Безодню з шкодою |
| Ліфт | static | — | рух на N рівнів |
| Кінь | ally | вантаж | швидша країна; перевантажений тікає з рюкзаком |
| Їжа | pickup | вага 20 | голод вимагає часто їсти; підземна їжа буває отруйною |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(join, guild)` → ЯКЩО `custom: «нема членства тієї ж категорії (Fighting / Magic / Religion)»` and `custom: «вимоги гільдії»` → ТО `custom: «членство»`; інакше `block`.
- КОЛИ `died(monster)` → ТО `custom: «досвід ділиться порівну між усіма гільдіями героя»` (Gladiators частки не беруть).
- КОЛИ `custom: «досвід гільдії ≥ поріг»` → ТО `custom: «наступний ранг + бонус»`; передостанній ранг — 4000; верхній — спецквест і більше досвіду, ніж у попереднього лідера.
- КОЛИ `custom: «Paladins: мировоззрення ≤ 0»` → ТО `custom: «виключення»`; КОЛИ `custom: «Sorcerors: втрачено chaos»` → ТО `custom: «мана більше не продається + прокляття»`.
- КОЛИ `custom: «Gladiators: втеча з бою без перемоги»` → ТО `custom: «виключення»`.
- КОЛИ `custom: «монстр здається»` → ЯКЩО `input(release)` → ТО `custom: «+2 law»`; `input(rob)` → `custom: «+2 chaos»`; `input(execute)` → `custom: «+13 chaos»`.
- КОЛИ `input(threaten intelligent monster)` → ТО `custom: «+3 law»`; атакувати першим — chaos, дати вдарити першим — law.
- КОЛИ `input(donate, hospice)` → ТО `currency(−100)`, `custom: «мировоззрення → 0»`.
- КОЛИ `custom: «фаза місяця збігається з мировоззренням (повня — law, молодик — chaos)»` → ТО `custom: «+рівень до влучання, подвійна шкода»`; ЯКЩО протилежна → ТО `custom: «−½ рівня до влучання, половина шкоди»`; фаза також міняє ціну заклять.
- КОЛИ `timer(every game hour)` → ЯКЩО `custom: «герой у країні на суші»` → ТО `custom: «хаос-шторм: −10 Power / мана в 0 / телепорт у Хаос-море / скидання рівня, заклять і рангів»`.
- КОЛИ `custom: «Хаос-море»` → ЯКЩО `prob(fail)` → ТО `custom: «великий зсув до chaos, втрата рівня»`, `lose`.
- КОЛИ `custom: «вантаж коня > ліміт»` → ТО `custom: «кінь тікає з рюкзаком»`.
- КОЛИ `enter(hero, water)` → ЯКЩО `custom: «надто важкий»` → ТО `choose(drop items)`.
- КОЛИ `enter(hero, lava)` → ТО `lose`.
- КОЛИ `enter(hero, abyss trap)` → ТО `teleport(hero, abyss)`, `damage(n)`.
- КОЛИ `custom: «у Безодні d100 = 13 (Йог-Сотот)»` → ЯКЩО `custom: «мировоззрення > −10»` → ТО `lose`; інакше `custom: «+2000 досвіду»`.
- КОЛИ `input(enter dungeon B)` → ЯКЩО `custom: «збережено рівні підземелля A»` → ТО `custom: «рівні A забуто»`.
- КОЛИ `input(cast Return)` → ТО `custom: «через затримку — на найглибший відвіданий рівень»`.
- КОЛИ `input(pick up)` → ТО `custom: «предмет у слот "в повітрі"»`; КОЛИ `input(pack|ready)` → ТО `custom: «у рюкзак / у руку»`; дістати з рюкзака — знову через «в повітрі».
- КОЛИ `custom: «спроба зайти в заклад»` → ЯКЩО `not custom: «години роботи»` → ТО `block`.
- КОЛИ `input(retire, condo)` → ЯКЩО `custom: «кондо куплено (50000 золота)»` → ТО `win`.
- КОЛИ `custom: «Adept's Challenge на Astral Plane пройдено»` → ТО `win` («bigwin»; далі дозволені бажання, рахунок заморожено).
- КОЛИ `custom: «топ-ранг гільдії / релігії, усі квести Герцога, рекорд law або chaos»` → ТО `custom: «місце в таблиці рекордів»`.
- КОЛИ `custom: «старт»` → ТО `window(questionnaire)`; відповіді (жим, IQ, хобі, хвороби…) → `custom: «стати героя»`.
- КОЛИ `hp_zero(hero)` → ТО `lose` (смерть остаточна).
- Перемога: пенсія в кондо / Adept / лідерство як рекорд. Поразка: смерть. Рахунок: таблиця рекордів інсталяції.

## Керування і ввід
- Клавіатура, ASCII, малі й великі літери як різні команди.
- Інвентар у кілька кроків: підняти → «в повітрі» → у рюкзак або в руку; щоб зʼїсти — ≈8 команд (CRPG Addict).
- Банкомат: відкрити рахунок, пароль (Shift-O / Shift-P).

## Вікна, меню, HUD
- `game-screen`: мапа (місто / країна / підземелля), рядки статусу, `message-log`; годинник і фаза місяця (?).
- `questionnaire` — анкета «грай собою» замість вибору раси/класу; або випадковий персонаж (?).
- `overworld-map` — країна як окремий екран; тактична мапа бою в країні.
- Вікна закладів (`custom-window`): гільдії (вступ, ранг, навчання), крамниці, банкомат, кондо.
- `inventory-window` з окремим слотом «в повітрі» та слотами рук; `end-screen`; `leaderboard`.

## Фічі поза полем
- Кілька кінцівок (`multiple-endings`): пенсія, Adept, рекорди лідерства.
- Таблиця рекордів інсталяції: топ-гільдія, квести Герцога, найбільший law/chaos — змагання з іншими гравцями тієї ж машини.
- Збереження ризиковані (поради бекапити сейви) — сейв є, смерть остаточна (?).
- Варіанти: WinOmega (тайли), AmiOmega, MacOmega, Omega Rebirth; GPL з 2010.

## Варіації й родичі
- Відкрила оверворлд → [adom](adom.md); місто з будівлями — як у [larn](larn.md) і [angband](angband.md), але з годинами роботи й членствами.
- Інвентар через руку — далекий родич ручних слотів [dungeon-master](dungeon-master.md) (?).
- Осі варіацій: **ідентичність героя** (раса+клас / анкета / членства) · **світ** (одне підземелля / країна з багатьма) · **час** (лише ходи / доба й години роботи / місячний цикл) · **перемога** (одна мета / кілька кінцівок / рекорд серед гравців).

## Цікавинки для курсу
- Гільдії-категорії: одна з кожної групи, досвід ділиться між членствами — 📎 (обмеження множин + розподіл ресурсу).
- Фаза місяця × мировоззрення як модифікатор бою — 🌱.
- Мировоззрення як число, що зсувають конкретні вчинки (+2, +3, +13) — 🌱.
- Доба й години роботи закладів — 🌱.
- Кеш рівнів лише для одного підземелля — 🌱.
- Анкета «грай собою» → стати — 🌱.
- Інвентар з проміжним слотом «в повітрі» — 📎 (як не треба: ціна в кроках).

## Мапа на каталог
- Є: `move-8dir` · `stairs-levels` · `dungeon-generation` · `hp-damage` · `inventory` + `inventory-limit` (вага від сили) · `item-identification` · `hunger-clock` · `status-effects` (отрута, хвороба, повільність) · `unit-xp-skills` · `round-currency` + `shop-catalog` + `shop-buyback` · `teleport` · `environment-death` (лава, вода, Хаос-море) · `permadeath` · `score-records` · `console-render`.
- **Нема** → пропозиції карток:
  - `+guild-ranks` «Членство з рангами за досвідом і вимогами» · game-logic/progression · 📎.
  - `+exclusive-memberships` «Одне членство з кожної категорії» · game-logic/legality · 🌱.
  - `+xp-split` «Досвід ділиться між активними членствами» · entities/state · 🌱.
  - `+moon-phase-cycle` «Циклічна фаза, що модифікує бій за мировоззренням» · game-logic/time · 🌱 · слоти {period}.
  - `+day-night-hours` «Заклади відкриті за годинами доби» · game-logic/time · 🌱.
  - `+hand-slot-inventory` «Проміжний слот "в руці/в повітрі" між полем і рюкзаком» · entities/inventory · 🌱.
  - `+questionnaire-character` «Анкета замість вибору класу» · interface/menus · 🌱.
  - `+dungeon-cache-one` «Памʼятається лише останнє підземелля» · levels/generation · 🌱.
  - `+elevator-cell` «Ліфт на N рівнів із виходом за межі» · entities/interact · 🌱. Перевикористано: `+overworld-travel`, `+town-level`, `+alignment-shift`, `+multiple-endings`, `+word-of-recall`.

## Пропозиції до словників
- `+trigger:time_of_day(h)` — настала година доби; `+trigger:moon_phase(p)` — змінилась фаза місяця; `+trigger:surrender(monster)` — монстр здався.
- `+effect:shift_alignment(dir, n)`, `+effect:join(guild)`, `+effect:rank_up(guild)`, `+effect:retire` — кінцівка «пенсія».
- `+cond:alignment(op, x)`, `+cond:member(guild)`, `+cond:open_hours` — заклад зараз працює.
- `+role:guild-hall` — клітина-вхід у гільдію; `+role:oracle` — NPC-підказник.
- `+window:overworld-map`, `+window:questionnaire`, `+window:guild-window`.
- `+ui:moon-phase`, `+ui:clock`, `+ui:up-in-air-slot`.
- `+feature:multiple-endings`.
- `+card:guild-ranks`, `+card:moon-phase-cycle`, `+card:hand-slot-inventory`.

## Джерела
- ⭐ [@Play: An Early-Level FAQ For Omega](https://setsideb.com/?p=1306) — будівлі, гільдії й категорії, ранги, хаос-шторми, Хаос-море, села, підземелля й цілі, ліфти, Return, мировоззрення в числах, фази місяця, перемоги, їжа.
- [RogueBasin: Omega](https://www.roguebasin.com/index.php/Omega) — автор, рік, перша велика країна, «up in the air», кілька перемог, вплив на ADOM, версії.
- [CRPG Addict: Omega](https://crpgaddict.blogspot.com/2011/05/game-55-omega-1988.html) — анкета, заклади Рампарта, тактична мапа, хаос-шторми, голод, 8 команд на їжу, кеш одного підземелля.
- [SourceForge: omega-roguelike](https://sourceforge.net/projects/omega-roguelike/) — опис, інтерфейси, відгуки про сейви.
- [Libre Game Wiki](https://libregamewiki.org/Omega-rpg) — версії, вибір гільдій.
- [Wikipedia: Roguelike](https://en.wikipedia.org/wiki/Roguelike) — оверворлд раніше за ADOM, «дивний інвентар».

## Непевне
- (?) Окремої статті Wikipedia нема: `Omega_(video_game)` — інша гра (Origin, програмування танків); ⭐ узято FAQ.
- (?) Чи показані годинник і фаза місяця в HUD; чи є випадковий персонаж замість анкети — не перевірено.
- (?) Як збереження поєднується з остаточною смертю (сейв при виході?) — не перевірено.
- (?) Повний список підземель і квестів Герцога, умови «total winner» — у джерелах лише згадки.
- (?) Рік: RogueBasin і WP-список — 1987, CRPG Addict — 1988.
