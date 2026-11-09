---
title: Massive Assault
slug: massive-assault
aka: ["Massive Assault Network", "Massive Assault: Phantom Renaissance", "Domination"]
family: tactics
also: []
klass: figure
axes:
  field: hex
  time: turn
  opponent: ai
  info: hidden
  random: setup
  goal: territory
year: 2003
platforms: [Windows, macOS]
links:
  - {kind: wiki, url: "https://ru.wikipedia.org/wiki/Massive_Assault", best: true, note: "фази ходу, таємні союзники, партизани, захоплення столиці, характеристики юнітів, режими"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Massive_Assault", note: "гекс-сітка, ≥10 країн і ≥4 союзники на сторону, розкриті/нерозкриті/нейтральні, PBEM, серія"}
  - {kind: steam, url: "https://store.steampowered.com/app/34630/Massive_Assault/", note: "офіційний опис: «Secret Allies», 26 юнітів, 6 планет; реліз 28.10.2003"}
  - {kind: other, url: "https://worthplaying.com/article/2003/11/30/reviews/13967-pc-review-massive-assault/", note: "рецензія 2003: бойова фаза й фаза призову, рух потім постріл, перемотка ходів, хотсіт"}
  - {kind: other, url: "https://www.gog.com/en/game/massive_assault", note: "GOG: розкрити союзника й дати війська «в будь-який момент»"}
  - {kind: steam, url: "https://store.steampowered.com/app/34640/Massive_Assault_Phantom_Renaissance/", note: "сиквел 2005: World Wars на 6 планетах, 10 нових юнітів, режим Assault, 2D-атлас"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Massive+Assault+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [hp-damage, ai-opponent, hot-seat, async-multiplayer, online-multiplayer, rating-system, round-currency, undo-redo, in-game-editor, editor-window, tutorial-window, lobby-window, main-menu, game-screen, end-screen, +secret-allies, +disclose-reinforcements, +partisans-on-invasion, +capture-capital, +country-income, +move-then-fire, +turn-phases, +unit-purchase, +terrain-unit-classes, +reminder-unfired-units]
proposes: ["+trigger:invaded", "+effect:disclose", "+effect:capture", "+effect:recruit", "+cond:secret_ally_of", "+role:country", "+role:capital", "+ui:funds", "+ui:unfired-reminder", "+window:production", "+window:strategic-atlas", "+feature:mode-world-war", "+card:secret-allies"]
author: opus
date: 2026-11-09
---

# Massive Assault — гексова війна за країни, де половина союзників прихована і вводиться у гру тоді, коли вигідно власнику

## Суть
Два блоки — Союз Вільних Націй і Ліга Фантомів — воюють на гекс-карті планети, поділеній на країни. На старті кожен отримує однакову кількість **таємних союзників**: країн, про які суперник не знає. Будь-якого з них можна розкрити в будь-який хід — і в цій країні раптом зʼявляються свіжі війська. Тому суперник ніколи не знає, де фронт стане вдвічі сильнішим, і мусить ставити війська з урахуванням невідомого. Бій простий, як у настолках: юніт за хід раз рухається і раз стріляє, гроші — з підконтрольних країн.

## Поле і час
- Гексагональна сітка в 3D-рендері; шість типів світів (від снігових до тропічних); суходіл, море й повітря (сухопутні, морські, амфібії, авіація).
- Карта поділена на країни (на кожній карті ≥10, ≥4 союзники на кожну сторону — EN Wikipedia); кожна має столицю.
- Хід — по черзі сторін, усередині — фази (RU Wikipedia): розкриття союзників і закупівля з виставленням техніки в своїх країнах → бойова фаза (рух і стрільба) → фаза партизан (опір у щойно захоплених країнах) → мобілізація (дохід і закупівля) → фаза розкриття.
- Інформація прихована: суперник бачить лише розкритих союзників; туман війни зʼявився лише в Galactic Assault: Prisoner of Power.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Юніт (26 типів) | piece | HP; дальність руху; вогнева міць; дальність стрільби; ціна | за хід — один рух і один постріл; стріляти, потім рухатись не можна |
| Сухопутний / морський / амфібія / повітряний | piece | тип середовища | ходить лише своїм середовищем (?) |
| Партизани | ally | нечисленні | зʼявляються в будь-якій клітині країни; рухаються й стріляють першими |
| Країна | zone | власник: своя / розкритий союзник / нерозкритий союзник / нейтральна / ворожа | дає дохід власнику; у своїх країнах ставлять куплені юніти |
| Столиця | static | одна на країну | взяти столицю й вибити війська = захопити країну |
| Таємний союзник | zone | видимий лише власнику | розкривається власником → підкріплення |
| Гроші | resource | обмежені | дохід з усіх підконтрольних країн; витрачаються на юніти |
| Сторона | — | Союз Вільних Націй / Ліга Фантомів | юніти сторін здебільшого рівноцінні |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «кожній стороні — однакова кількість прихованих країн-союзників»` (`random: setup` — див. «Непевне»).
- КОЛИ `input(disclose, country)` → ЯКЩО `custom: «країна — твій нерозкритий союзник»` → ТО `reveal(country)`, `set_side(country, player)`, `spawn_at(fresh_troops, country)`.
- КОЛИ `input(move, unit, cell)` → ЯКЩО `custom: «юніт ще не рухався і не стріляв цього ходу»` і `path_exists(unit, cell)` → ТО `move(unit, cell)`.
- КОЛИ `input(fire, unit, target)` → ЯКЩО `in_range(unit, target, range)` і `custom: «ще не стріляв»` → ТО `damage(target, firepower)`, `set_state(unit, fired)` — після пострілу рух заборонено.
- КОЛИ `hp_zero(unit)` → ТО `disappear(unit)`.
- КОЛИ `custom: «кінець бойової фази»` → ЯКЩО `custom: «є юніти, що не стріляли»` → ТО `message(нагадування)`.
- КОЛИ `enter(enemy_unit, country)` → ЯКЩО `custom: «країна нейтральна або твій нерозкритий союзник»` → ТО `choose(підняти опір)` → `place(partisans, any_cell_of_country)`.
- КОЛИ `phase_start(partisans)` → ТО `custom: «партизани рухаються й стріляють першими»`.
- КОЛИ `custom: «у країні нема ворожих військ»` → ЯКЩО `occupied(capital, own_unit)` → ТО `set_side(country, player)`.
- КОЛИ `phase_start(mobilization)` → ТО `currency(+income)` з усіх підконтрольних країн.
- КОЛИ `input(buy, unit_type)` → ЯКЩО `counter(money, >=, cost)` → ТО `currency(-cost)`, `place(unit, own_country_cell)`.
- КОЛИ `input(rewind)` → ТО `undo(n)` — взяти ходи назад (рецензія Worthplaying).
- Перемога: `custom: «захистити свої країни й захопити ворожі»` (?) · Поразка: дзеркально · Рахунок: — (у мережевій версії — рейтинг).

## Керування і ввід
- Миша: клік по юніту → підсвічені клітини руху → клік; потім клік по цілі в радіусі стрільби.
- Кнопка розкриття союзника — у фазі розкриття (за RU Wikipedia — у будь-який хід).
- Панель закупівлі: вибір типу юніта → клік по клітині своєї країни.
- Кнопка перемотки ходів (Rewind).

## Вікна, меню, HUD
- `main-menu`: навчальні місії (`tutorial-window`) · окремі сценарії за кожну сторону · кампанії · хотсіт · мережа.
- `game-screen`: 3D-карта з гексами; кордони країн; `+ui:funds`; `turn-indicator`; `+ui:unfired-reminder` (хто ще не стріляв); інфо юніта (`stat-panel`: HP, рух, міць, дальність).
- `+window:production` — закупівля юнітів у фазі мобілізації.
- `custom-window` «Розкриття» — список прихованих союзників.
- `editor-window` — редактор карт (у комплекті).
- `lobby-window` — Massive Assault Network 2: підбір суперника, рейтинги, турніри, кланові війни.
- `+window:strategic-atlas` — Phantom Renaissance: 2D-карта в стилі історичного атласу (і «CNN-камера»).
- `end-screen` — перемога/поразка.

## Фічі поза полем
- Режими: одиночний (навчання, сценарії, кампанії, World War — велика карта з наперед заданими умовами), `hotseat`, PBEM (EN Wikipedia), мережа (Massive Assault Network, 2004; MAN 2, 2006 — рейтинги й автопідбір).
- Редактор карт; `undo`-перемотка; ШІ без повзунка складності (Worthplaying).
- Phantom Renaissance (2005): 6 нових планет для World Wars, 10 нових юнітів, унікальних для сторін, дві мегакампанії, 20 сценаріїв, режим Assault, кілька профілів поведінки ШІ.

## Варіації й родичі
- Серія: Massive Assault (2003) → Massive Assault Network (2004) → Phantom Renaissance / Domination (2005) → MAN 2 (2006) → Galactic Assault: Prisoner of Power (дві нові нації й туман війни; рік не перевірено).
- Родичі: [Diplomacy](diplomacy.md) (країни як одиниці контролю, але без прихованих союзників), [Advance Wars](advance-wars.md) (дохід з власності, купівля юнітів), [Panzer General](panzer-general.md) (гекс-воргейм), Risk (країни й підкріплення).
- **Осі варіацій**: хто на твоєму боці — відомо всім (Risk) / приховано до розкриття самим власником (Massive Assault) / визначається переговорами (Diplomacy) · момент підкріплень — щоходу за доходом / разовим «вкидом» при розкритті / реакцією на вторгнення (партизани).

## Цікавинки для курсу
- Таємні союзники: прихована власність країни, яку власник розкриває у вигідний момент — 🥈 (два представлення стану: для себе і для суперника).
- Партизани як реакція на вторгнення в нейтральну чи приховану країну — 🥉 (тригер «ворог увійшов у зону» + розміщення гравцем).
- Захоплення країни: «нема ворогів у зоні + твій юніт на столиці» — 📎.
- Рух → постріл, без зворотного порядку; нагадування про юнітів, що не стріляли — 🌱.
- Фази ходу як конвеєр (розкриття → бій → партизани → мобілізація) — 📎.
- PBEM/хотсіт: стан партії як файл, що передається між гравцями — 🥉.

## Мапа на каталог
- Є: `hp-damage` · `ai-opponent` · `hot-seat` · `async-multiplayer` (PBEM) · `online-multiplayer` · `rating-system` (MAN 2) · `round-currency` (дохід країн) · `undo-redo` (Rewind) · `in-game-editor` + `editor-window` · `tutorial-window` · `lobby-window` · вікна.
- **Нема** → пропозиції карток:
  - `+secret-allies` «Таємні союзники» · game-logic/opponent · 🥈 · слот {count}.
  - `+disclose-reinforcements` «Розкриття = вкид військ» · entities/spawn · 📎.
  - `+partisans-on-invasion` «Опір у країні при вторгненні» · entities/spawn · 🥉.
  - `+capture-capital` «Захоплення країни через столицю» · game-logic/win · 📎.
  - `+country-income` «Дохід з підконтрольних зон» · game-logic/economy · 🌱.
  - `+move-then-fire` «Спершу рух, потім постріл» · entities/combat · 🌱.
  - `+turn-phases` «Хід із фіксованих фаз» · game-logic/opponent · 📎.

## Пропозиції до словників
- `+trigger:invaded` — ворожий юніт увійшов у зону-країну (тригер партизан).
- `+effect:disclose` — власник розкриває приховану належність зони (≠ `reveal` клітин туману: тут розкривається власник, а не вміст).
- `+effect:capture` — зона змінює власника за умовою захоплення; `+effect:recruit` — купити юніт і поставити в свою зону.
- `+cond:secret_ally_of` — зона є прихованим союзником сторони.
- `+role:country` — зона-країна з власником і доходом; `+role:capital` — ключова клітина зони.
- `+ui:funds` — гроші сторони; `+ui:unfired-reminder` — нагадування про юнітів без пострілу.
- `+window:production` — закупівля юнітів; `+window:strategic-atlas` — 2D-атлас замість 3D-карти.
- `+feature:mode-world-war` — велика карта з наперед заданими умовами; `+card:secret-allies` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia RU: Massive Assault](https://ru.wikipedia.org/wiki/Massive_Assault) — фази ходу, таємні союзники, партизани, захоплення столиці, режими, редактор.
- [Wikipedia EN: Massive Assault](https://en.wikipedia.org/wiki/Massive_Assault) — гекс-сітка, статуси країн, ≥10 країн / ≥4 союзники, PBEM, серія.
- [Steam: Massive Assault](https://store.steampowered.com/app/34630/Massive_Assault/) — офіційний опис і дата.
- [Worthplaying: рецензія 2003](https://worthplaying.com/article/2003/11/30/reviews/13967-pc-review-massive-assault/) — бойова фаза й призов, «не можна стріляти, а потім рухатись», Rewind, хотсіт, World War.
- [GOG: Massive Assault](https://www.gog.com/en/game/massive_assault) — розкриття союзників «у будь-який момент».
- [Steam: Phantom Renaissance](https://store.steampowered.com/app/34640/Massive_Assault_Phantom_Renaissance/) — нове в сиквелі.

## Непевне
- (?) Як розподіляються таємні союзники на старті — випадково чи сценарієм (RU: «отримує однакову кількість»); `random: setup` — припущення.
- (?) Порядок фаз у RU Wikipedia суперечливий (розкриття і на початку, і в кінці); Worthplaying називає лише бойову і призовну.
- (?) Загальна умова перемоги (усі країни? усі юніти?) — джерела кажуть лише «захисти свою базу й захопи чужі».
- (?) «2 очки за хід» (Worthplaying) — схоже на режим/сценарій, а не загальне правило.
- (?) Чи бій детермінований (без кубиків) — не підтверджено.
- (?) Обмеження руху за середовищем для кожного типу юнітів — з опису (сухопутні, флот, амфібії, авіація), без деталей.
