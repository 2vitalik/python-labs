---
title: Offworld Trading Company
slug: offworld-trading-company
aka: [OTC, Offworld]
family: build-sim
also: []
klass: cursor
axes:
  field: hex
  time: realtime
  opponent: ai
  info: partial
  random: both
  goal: state
year: 2016
platforms: [PC, Mac]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Offworld_Trading_Company", best: true, note: "Марс, 13 ресурсів, ланцюги будівель, ринок попиту й пропозиції, чорний ринок, перемога викупом акцій"}
  - {kind: other, url: "https://www.designer-notes.com/otc-designer-notes-3-claims/", note: "Soren Johnson: клейми з M.U.L.E., одна будівля на гекс, бонус сусідства +50/+25/+10 %, максимум +100 %"}
  - {kind: other, url: "https://www.designer-notes.com/otc-designer-notes-16-hq-types/", note: "типи штабу: Expansive, Robotic, Scavenger, Scientific"}
  - {kind: other, url: "https://www.designer-notes.com/otc-designer-notes-17-stock-market/", note: "акції: по одній до 5, останні 5 разом, 6+ у чужих — викуп, дочірня компанія"}
  - {kind: other, url: "https://www.designer-notes.com/otc-designer-notes-5-debt/", note: "автоборг, рейтинг облігацій, відсотки 2–6 % / 30 % при D"}
  - {kind: steam, url: "https://store.steampowered.com/app/271240/", note: "кампанія, мультиплеєр до 8, DLC, редактор рівнів, Workshop"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Offworld+Trading+Company+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [cursor-place, cell-click, hover-highlight, round-currency, shop-window, ai-opponent, realtime-ai, online-multiplayer, lobby-window, match-setup, mode-select, game-screen, end-screen, stats-window, achievements-window, leaderboard, in-game-editor, editor-window, field-scaling, player-camera, save-game, sequential-levels, +adjacency-buff, +supply-demand-price, +production-chain, +claim-tokens, +auto-logistics, +life-support-upkeep, +auto-debt-credit, +stock-buyout, +sabotage-market, +asset-auction, +random-demand-modules, +founding-countdown]
proposes: ["+effect:trade", "+cond:owned_by", "+ui:price-ticker", "+ui:stock-panel", "+ui:debt-rating", "+window:black-market", "+feature:reveal-map", "+card:claim-tokens", "+card:auto-logistics", "+card:stock-buyout", "+card:auto-debt-credit", "+card:sabotage-market", "+card:asset-auction", "+card:founding-countdown"]
author: opus
date: 2026-11-09
---

# Offworld Trading Company — економічна RTS на гексах Марса: став видобуток на заклеймлених гексах, грай на спільному ринку, скупи акції суперників

## Суть
Чотири (до восьми) компанії колонізують Марс у реальному часі; військових юнітів нема — уся боротьба через **спільний ринок** і **акції**. Гравець засновує штаб на гексі, витрачає обмежені **клейми** на будівлі (одна на гекс), видобуває й переробляє 13 ресурсів і продає запаси; кожна угода рухає ціну для всіх. Саботаж — через чорний ринок, оборона — Goon Squad. Перемагає той, хто викупить контрольні пакети всіх інших компаній. Дизайнер — Soren Johnson; система клеймів і бонусу сусідства запозичена з M.U.L.E.

## Поле і час
- Мапа — гексагональна (гекси обрали, бо на них простіше визначити сусідство); кожен гекс має тип рельєфу й поклади (кілька ресурсів на одному гексі можливі; рельєф впливає на поклади: залізо — частіше на вулканічному).
- Рівні покладу — High / … / Low / Trace (Trace дає чверть від Low) (?) середні рівні.
- У центрі — нейтральна Колонія з модулями попиту; навколо — штаби гравців і їхні будівлі.
- Реальний час із «днями» для споживання й відсотків; вантажі між будівлями й штабом возять фрахтовики — відстань коштує пального й часу.
- Початок (Reveal Map, стандарт мультиплеєра): мапу відкрито всім, лічильник боргу за заснування починається з $200K і щосекунди спадає; раннє заснування дорожче, пізнє — дешевше, після $0 росте бонус заснування.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Штаб (HQ) | player | тип, рівень, займає кілька гексів | склад ресурсів; споживає життєзабезпечення за розміром; апгрейд дає клейми |
| Клейм | resource | кількість | дозвіл поставити 1 будівлю на гекс; поповнюється апгрейдом штабу й аукціонами |
| Видобувна будівля (Metal Mine, Quarry, Water Pump (?), Condenser (?)) | object | рівень покладу | видобуває ресурс(и) гекса під собою |
| Електростанція (сонячна, геотермальна, вітрова…) (?) | object | тип і обмеження | дає Power; надлишок продається, нестача докуповується |
| Переробка (Steel Mill, Greenhouse Farm, Electrolysis Reactor, Glass Kiln, Electronics Factory, Chemical Refinery) | object | входи → вихід | Iron→Steel; Water→Food; Water→Oxygen+Fuel; Silicon+Oxygen→Glass; Silicon+Carbon+Aluminum→Electronics; Carbon+Fuel→Chemicals |
| Спецбудівлі (Offworld Market, Patent Lab, Hacker Array, Optimization Center) | object | ліміт | Offworld — ≤ 2 на гравця (рівні штабу 4 і 5), продаж поза Марсом за стабільно високими цінами |
| Інженер | neutral | авто | вилітає зі штабу будувати, зникає після роботи |
| Фрахтовик | neutral | авто, пальне | везе повний склад будівлі до штабу; постачає будівлю зі штабу |
| Пірати | enemy | тимчасові | ставляться з чорного ринку, грабують вантажі й відлітають |
| Колонія | neutral | модулі Habitat / Office / Laboratory | центр попиту: Habitat — вода/їжа/кисень, Office — енергія, Laboratory — хімікати; модулі додаються випадково |
| Ресурс на ринку (13 шт.) | resource | ціна | ціна росте від купівлі, падає від продажу; Power не зберігається |
| Акція компанії | resource | 10 на компанію (?) | купується по одній, доки не лишиться 5; останні 5 — лише разом |
| Компанія-суперник | enemy | AI або людина | та сама економіка; може скупити тебе |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(found_hq, hex)` → ЯКЩО `free(hex)` → ТО `place(player, hq)`, `counter(debt, +founding_price)` — ціна = поточне значення лічильника (Reveal Map).
- КОЛИ `input(build, hex)` → ЯКЩО `counter(claims, >, 0)` and `free(hex)` and `has(player, steel)` → ТО `place(player, building)`, `counter(claims, -1)`, `take(player, steel)`, `spawn(engineer)`; Scavenger будує за Carbon замість Steel, Expansive — за половину Steel.
- КОЛИ `timer(production)` → ЯКЩО `custom: «будівля має входи й енергію»` → ТО `counter(stock(output), +yield)`.
- Бонус сусідства: ЯКЩО `adjacent_count(building, same_type, >=, 1)` → ТО `multiplier(1.5)`; 2-й сусід — ще +25 %, 3-й — +10 %, разом не більше ×2 (трикутник з трьох — по +75 % кожній).
- Robotic HQ: ЯКЩО `custom: «поруч будівля, що постачає вхід (Steel Mill біля Metal Mine)»` → ТО `multiplier(1.5)` (Glass біля Quarry і Reactor — +75 %).
- КОЛИ `custom: «склад будівлі повний»` → ТО `spawn(freighter)` → `move(freighter, hq)`, `take(player, fuel)` ∝ відстань; кнопки-оверрайди — відправити раніше або постачити будівлю зі штабу.
- КОЛИ `input(sell, resource)` → ТО `currency(+price × qty)`, `set_value(price(resource), lower)` — для всіх (`+effect:trade`); КОЛИ `input(buy, resource)` → ТО `currency(-price × qty)`, `set_value(price(resource), higher)`; одна ціна для купівлі й продажу (без спреду).
- КОЛИ `timer(day)` → ТО `take(hq, water + food + oxygen)` за розміром штабу (Robotic — без цього, лише Power).
- КОЛИ `custom: «потрібні Power, Fuel чи життєзабезпечення, а запасу нема»` → ТО `custom: «автоматично купити з ринку»`, `counter(debt, +cost)` — безлімітний кредит.
- КОЛИ `timer(day)` → ЯКЩО `counter(debt, >, 0)` → ТО `counter(debt, +interest)`: рейтинг облігацій за боргом до активів — AAA/AA/A 2–6 %, D — 30 % і `set_state(player, no_black_market)`.
- КОЛИ `input(upgrade_hq)` → ЯКЩО `has(player, steel)` and `has(player, glass)` and `has(player, aluminum)` → ТО `counter(hq_level, +1)`, `counter(claims, +n)` (Expansive — +1 клейм понад норму), `unlock(offworld_market)` на рівнях 4 і 5.
- КОЛИ `input(launch, offworld_market)` → ТО `currency(+offworld_price)` — часто понад $50K за запуск.
- КОЛИ `input(buy_share, company)` → ЯКЩО `custom: «у вільному продажу більше 5 акцій»` → ТО `give(player, share)`, `currency(-share_price)`; борг знижує ціну акцій.
- КОЛИ `input(buyout, company)` → ЯКЩО `custom: «покупець має гроші на останні 5 акцій; чужі акції — +20 % до ціни»` → ТО `set_side(company, buyer)` → `custom: «компанія стає дочірньою під AI, прибуток ділиться між акціонерами»`.
- КОЛИ `custom: «у чужих руках ≥ 6 твоїх акцій»` → ТО `lose` (гравець стає спостерігачем); гравця попереджають, коли суперник уже може його викупити.
- КОЛИ `custom: «гравець контролює всі компанії»` → ТО `win`.
- Чорний ринок: КОЛИ `input(buy, item)` → ЯКЩО `not state(player, no_black_market)` → ТО `currency(-price)`, `set_value(price(item), higher)` — усі бачать подорожчання (сигнал атаки); у партії ~7 предметів з більшого пулу.
- Dynamite: ТО `disappear(building)` · Mutiny: ТО `set_side(building, buyer)` (?) тривалість · EMP / Power Surge: ТО `stun(buildings)` (Scientific стійкий) · Underground Nuke: ТО `set_cell(deposit, trace)` · Pirates: ТО `custom: «грабують вантажі»` · Goon Squad: ТО `set_state(building, guarded)`; КОЛИ `custom: «саботаж на охоронювану будівлю»` → ТО `custom: «саботаж перехоплено для власника охорони»`.
- Аукціон: КОЛИ `custom: «виставлено клейм / гекс / патент / предмет чорного ринку / спецбудівлю»` → ТО `choose(bid)`; переможець — останній, хто підняв; КОЛИ `custom: «аукціон виграно»` → ТО `counter(debt, +bid)`.
- КОЛИ `rng(p)` → ТО `spawn(colony_module)` — модуль додає попит на свій ресурс незалежно від гравців.
- Перемога: контроль над усіма компаніями · Поразка: 6+ твоїх акцій у чужих руках · Рахунок: вартість компанії / капітал (кампанія) (?).

## Керування і ввід
- Без виділення юнітів: інженери, фрахтовики й пірати автоматичні.
- Клік по гексу — заснувати штаб / поставити будівлю (вибір з панелі); продаж і купівля ресурсів — кнопки на панелі ринку; купівля акцій — панель компаній; покупка саботажу — чорний ринок і клік по цілі.
- Оверрайди логістики (надіслати до штабу раніше / постачити будівлю) і скасування/знесення будівлі (?) для перебудови під ринок.
- Ставки на аукціоні — кнопкою, доки інші не перестануть «блимати».

## Вікна, меню, HUD
- `main-menu` → `mode-select`: кампанія, одиночна партія з AI (?), мультиплеєр (до 8 гравців, кросплатформа), 1000 Map Challenge (Jupiter's Forge).
- `match-setup` / `lobby-window`: гравці й AI, мапа, опції (Reveal Map) (?).
- `game-screen`: гексова мапа з Колонією; HUD — `price-ticker` (13 ресурсів з ціною й трендом), запаси штабу, `coins` (кеш) і борг з `debt-rating`, кількість клеймів, `stock-panel` (акції всіх компаній, хто скільки тримає), попередження «тебе можуть викупити».
- `black-market` (`shop-window`): предмети, ціни, кулдаун.
- `custom-window` аукціону: лот, поточна ставка, учасники.
- `custom-window` штабу: рівень, апгрейд, вибір типу на заснуванні (Expansive / Robotic / Scavenger / Scientific).
- `end-screen` + `stats-window`: результат партії, графіки (?); `leaderboard` 1000 Map Challenge; `achievements-window` (Steam); `editor-window` (редактор рівнів, Scenario Toolkit DLC).
- Переходи: main-menu → match-setup → game-screen (заснування → гра) → end-screen.

## Фічі поза полем
- Кампанія з керівниками (CEO) з різними рисами; одиночні партії з AI; `online-multiplayer` PvP і co-op, кросплатформа.
- `level-editor` + `mod-support` (Steam Workshop), `cloud-save`, `achievements`.
- Розширення: Jupiter's Forge (Іо: поклади вичерпуються, 2 нові фракції, патенти, нові ресурси, власна кампанія, 1000 Map Challenge з рейтингом), The Europa Wager, The Ceres Initiative, Blue Chip Ventures, Market Corrections, Limited Supply, Interdimensional, Real Mars Map Pack, Scenario Toolkit, Almanac (безкоштовний).
- Опція Reveal Map — рівний старт для всіх (див. «Поле і час»).

## Варіації й родичі
- Предок: [mule](mule.md) — клейми ділянок, бонус за сусідство однакових виробництв, ринок з ціною від попиту й пропозиції; OTC перевів це в реальний час і на гекси.
- Ранні версії: до 4 будівель на гекс з бонусом усередині гекса → 1 будівля + бонус сусідства; початковий +50 % за кожного сусіда давав +300 % у «квітці» — додали спадну віддачу.
- **Осі варіацій**: бонус сусідства (лише той самий тип / постачальник входу — Robotic) · будівельний ресурс (Steel / Carbon) · життєзабезпечення (вода-їжа-кисень / лише енергія) · викуп (подвійна ціна за відкритого ринку / по одній до 5 і пакет / дочірня компанія під AI) · старт (сканування мапи / Reveal Map з таймером боргу).
- Родичі в корпусі: [civ6-districts](civ6-districts.md) (гексові бонуси сусідства), [islanders](islanders.md) і [dorfromantik](dorfromantik.md) (очки за сусідство), [factorio-belts](factorio-belts.md) (ланцюги виробництва), [big-pharma](big-pharma.md) (переробка під ринок).

## Цікавинки для курсу
- Бонус сусідства на гексах зі спадною віддачею (+50/+25/+10 %, межа +100 %) — 🌱 (осьові координати гекса й 6 сусідів).
- Спільний ринок: ціна як функція купівель/продажів усіх, одна ціна без спреду — 📎; плюс постійний попит Колонії й випадкові модулі — 🥉.
- Ланцюги переробки (13 ресурсів, входи → вихід, енергія без складу) — 🥉.
- Автоборг з рейтингом облігацій і відсотками за днями — 📎.
- Акції й викуп: по одній до 5, пакет із 5, +20 % за чужі, перетворення на дочірню AI-компанію — 🥈.
- Чорний ринок з ціною, що росте від кожної покупки (сигнал усім), і Goon Squad, що перехоплює саботаж — 🥉.
- AI-компанія, що вибирає, що будувати й продавати під поточні ціни — 🥇.

## Мапа на каталог
- Є: `cursor-place` + `cell-click` + `hover-highlight` ↔ розміщення на гексі · `round-currency` ↔ кеш · `shop-window` ↔ чорний ринок · `ai-opponent` + `realtime-ai` · `online-multiplayer` + `lobby-window` + `match-setup` · `mode-select` · `game-screen` · `end-screen` + `stats-window` · `achievements-window` · `leaderboard` ↔ 1000 Map Challenge · `in-game-editor` + `editor-window` · `field-scaling` + `player-camera` · `save-game` ↔ cloud saves · `sequential-levels` ↔ кампанія.
- **Нема** → пропозиції карток:
  - `+claim-tokens` «Обмежені дозволи на будівництво, що поповнюються прогресом» · game-logic/economy · 🌱.
  - `+auto-logistics` «Транспорт сам возить вантаж між будівлею і складом, ціна від відстані» · entities/move · 🥉.
  - `+stock-buyout` «Акції компаній як умова перемоги: купівля, пакет, викуп» · game-logic/win · 🥈.
  - `+auto-debt-credit` «Нестача покривається боргом з рейтингом і відсотками» · game-logic/economy · 📎.
  - `+sabotage-market` «Саботаж за гроші з ціною, що росте від покупок» · game-logic/opponent · 🥉.
  - `+asset-auction` «Аукціон клеймів, гексів, патентів» · game-logic/economy · 📎.
  - `+random-demand-modules` «Нейтральний споживач з модулями попиту, що зʼявляються випадково» · game-logic/economy · 📎.
  - `+founding-countdown` «Ціна заснування спадає з часом; хто перший — платить більше» · game-logic · 🌱.
  - `+life-support-upkeep` «Регулярне споживання ресурсів за розміром бази» · game-logic/economy · 🌱.
  - Перевикористано: `+adjacency-buff`, `+supply-demand-price` (M.U.L.E.), `+production-chain`.

## Пропозиції до словників
- `+effect:trade` — продати/купити ресурс за поточною ціною зі зсувом ціни для всіх (уже просив M.U.L.E.).
- `+cond:owned_by` — гекс/будівля належить стороні (клейм, мета саботажу).
- `+ui:price-ticker` — рядок цін ресурсів з трендом.
- `+ui:stock-panel` — акції компаній і їхні власники.
- `+ui:debt-rating` — борг і рейтинг облігацій (AAA…D).
- `+window:black-market` — магазин саботажу з цінами, що ростуть.
- `+feature:reveal-map` — відкрита мапа для всіх + таймер ціни заснування.
- `+card:claim-tokens`, `+card:auto-logistics`, `+card:stock-buyout`, `+card:auto-debt-credit`, `+card:sabotage-market`, `+card:asset-auction`, `+card:founding-countdown` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Offworld Trading Company](https://en.wikipedia.org/wiki/Offworld_Trading_Company) — Марс, 4 компанії, штаб і екстрактори, 13 ресурсів і ланцюги переробки, ринок, чорний ринок і Goon Squad, перемога через контрольні пакети, вибування, Mohawk/Stardock, 2016, Unity.
- [Designer Notes #3: Claims](https://www.designer-notes.com/otc-designer-notes-3-claims/) — M.U.L.E., 1 будівля на гекс, бонус сусідства й спадна віддача, перехід на гекси.
- [Designer Notes #1: Unit Selection](https://www.designer-notes.com/otc-designer-notes-1-unit-selection/) — інженери, фрахтовики, пірати автоматичні; оверрайди; пальне й час за відстань.
- [Designer Notes #2: Free Markets](https://www.designer-notes.com/otc-designer-notes-2-free-markets/) — одна ціна купівлі/продажу, угоди рухають ціну для всіх.
- [Designer Notes #4: Resources](https://www.designer-notes.com/otc-designer-notes-4-resources/) — первинні й вторинні ресурси, Metal Mine і Quarry, Power без складу, життєзабезпечення за розміром штабу, Steel/Glass/Aluminum для апгрейдів.
- [Designer Notes #5: Debt](https://www.designer-notes.com/otc-designer-notes-5-debt/) — автоборг, рейтинг, 2–6 % і 30 %, D без чорного ринку.
- [Designer Notes #6: Auctions](https://www.designer-notes.com/otc-designer-notes-6-auctions/) · [#7: Reveal Map](https://www.designer-notes.com/otc-designer-notes-7-reveal-map/) · [#8: Neutral Colony](https://www.designer-notes.com/otc-designer-notes-8-neutral-colony/) · [#12: Offworld Market](https://www.designer-notes.com/otc-designer-notes-12-offworld-market/) · [#13: Black Market I](https://www.designer-notes.com/otc-designer-notes-13-black-market-part-i/) · [#16: HQ Types](https://www.designer-notes.com/otc-designer-notes-16-hq-types/) · [#17: Stock Market](https://www.designer-notes.com/otc-designer-notes-17-stock-market/).
- [Steam](https://store.steampowered.com/app/271240/) — кампанія з CEO, мультиплеєр до 8, Jupiter's Forge, список DLC, редактор рівнів, Workshop.

## Непевне
- (?) Черга каже «екстрактори лише на гексах поруч зі штабом»; Вікіпедія справді пише про сусідні гекси на старті, але нотатки дизайнера (далекі клейми, швидші фрахтовики Expansive, ціна пального за відстань) показують, що будувати можна далеко — обмежують клейми й логістика.
- (?) Скільки клеймів дає кожен рівень штабу, скільки рівнів усього, точні ціни й темп зміни цін — у джерелах нема.
- (?) Повна назва водних і енергетичних будівель (Water Pump, Condenser, типи електростанцій), проміжні рівні покладів (Medium) — з памʼяті/уривків пошуку.
- (?) Тривалість і точна дія Mutiny, Bribe Claim, Magnetic Storm; кулдауни чорного ринку.
- (?) Наявність окремого режиму skirmish і склад головного меню; кількість акцій (10) виведено з «6 — більше половини».
