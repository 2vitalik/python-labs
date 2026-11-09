---
title: Panzer General
slug: panzer-general
aka: [PG, PG1, "Panzer General (1994)", "Танковий генерал"]
family: tactics
also: []
klass: figure
axes:
  field: hex
  time: turn
  opponent: ai
  info: hidden
  random: runtime
  goal: state
year: 1994
platforms: [DOS, 3DO, Mac, PlayStation, Windows, PC-98]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Panzer_General", best: true, note: "класи юнітів, досвід, престиж, 38 сценаріїв, кампанія з 5 стартами, major victory за 5 ходів раніше, гілки"}
  - {kind: other, url: "https://discmaster.textfiles.com/view/10989/FANCLUB1.ISO/losung/pgstr1.txt", note: "фан-гайд 1996 (ч. 1): 10 SP, overstrength за зірки, ініціатива 0–2, окопування, rugged defense, ZOC, пальне"}
  - {kind: play, url: "https://nicupavel.github.io/openpanzer-manual", note: "Open Panzer — браузерний клон PG: мануал (ZOC, окопування, набої, підтримка артилерії, погода, перемога)"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Panzer+General", note: "пошук; оригіналу нема, є наступник Panzer Corps"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Panzer+General+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [hp-damage, melee-vs-ranged, piece-move-patterns, legal-move-highlight, destroy-all-enemies, ai-opponent, hot-seat, difficulty-levels, save-game, sequential-levels, shop-between-levels, round-currency, fog-of-war, unit-xp-skills, game-settings, +hex-grid-render, +zone-of-control, +terrain-move-cost, +terrain-defense, +fuel-ammo, +resupply-in-place, +entrenchment, +rugged-defense, +initiative-first-strike, +support-fire, +strength-points, +overstrength, +elite-replacements, +prestige-economy, +core-army-carryover, +branching-campaign, +turn-limit-objectives, +victory-tiers, +air-ground-layers, +mount-transport, +damage-forecast, +weather-modifiers, +surprise-contact]
proposes: ["+trigger:enter_zoc", "+trigger:attacked", "+effect:counterattack", "+effect:entrench", "+effect:resupply", "+effect:support_fire", "+cond:entrenchment", "+cond:moved_this_turn", "+role:objective-city", "+ui:strength-plaque", "+ui:prestige", "+window:purchase-units", "+window:campaign-briefing", "+window:victory-tier", "+feature:core-army"]
author: opus
date: 2026-11-09
---

# Panzer General — гекс-кампанія Другої світової: тип юніта проти типу, окопи, пальне і армія, що росте з битви в битву

## Суть
Операційна воєнна гра на гексах: юніти — батальйони/полки з **силою 10**, кожен клас має атаку проти «мʼяких», «твердих» і повітряних цілей. Мета сценарію — захопити всі **міста-цілі** за ліміт ходів; що швидше, то вища перемога і більше **престижу** — валюти, за яку купують, поповнюють і модернізують юніти. Ядро кампанії — **армія, що переходить між битвами**: досвідчені юніти (зірки) сильніші, тож їх бережуть, а перемоги відкривають гілки «альтернативної історії» (висадка в Британії, Москва, США).

## Поле і час
- Поле — гекс-карта операційного масштабу (масштаб і розмір юнітів залежать від сценарію); ландшафт: рівнина, дорога, ліс, місто, гори, болото, річка, пустеля (?).
- Два шари: наземний і повітряний — літак стоїть «над» гексом, наземна ZOC не діє на повітряні і навпаки.
- Хід — уся сторона рухає і атакує юнітами в будь-якому порядку, потім хід противника; лічильник ходів до ліміту сценарію.
- Туман війни: прихованих юнітів видно лише в радіусі огляду (опція Hidden units); раптовий контакт з невидимим ворогом обриває рух.
- Погода (опція): суха / багнюка / мороз / хмарно / дощ / сніг — змінює рух, удари й авіацію.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Піхота | piece | Soft/Hard/Air attack, Ground/Air/Close defense, Initiative, Mov, Spot, сила 10 | захоплює міста; сильна в місті/лісі/горах (close combat) |
| Інженери / мостові | piece | — | ігнорують окопування; мостові — переправа через річку |
| Танк | piece | пальне, набої, високий Hard attack | сильний у полі; слабкий проти піхоти в місті |
| Протитанкова | piece | — | бʼє танки; буксирувана не атакує після руху |
| Розвідка | piece | великий Mov і Spot | виходить із ZOC, розкриває приховане |
| Артилерія | piece | дальність | непрямий удар; **підтримувальний вогонь** по тому, хто атакує сусіда |
| ППО | piece | Air attack | бʼє літаки; підтримка проти авіаудару |
| Винищувач | piece | пальне | бʼє бомбардувальники, перехоплює, розвідує |
| Тактичний / стратегічний бомбардувальник | piece | — | розбиває артилерію, ПТ, окопи; стратегічний пригнічує на весь хід |
| Транспорт (наземний) | object | — | піхота сідає → більший рух, але вразливіша |
| Місто-ціль (золотий прапор) | zone | власник | захопити всі → перемога |
| Місто / аеродром / порт | static | власник | престиж, поповнення, посадка/висадка |
| Ліс / місто / гори | terrain | захист, база окопу | укриття піхоти, ініціатива атакувальника падає |
| Дорога | terrain | дешевий рух | пришвидшує марш |
| Річка | terrain | — | зупиняє рух; переправа — мостові інженери |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, unit, hex)` → ЯКЩО `path_exists(unit, hex)` за ціною ландшафту ≤ Mov і `counter(fuel, ≥, cost)` → ТО `move`, `counter(fuel, −cost)`.
- КОЛИ `enter(unit, enemy_zoc)` → ТО `custom: «рух закінчується»` (крім розвідки); два ворожі юніти через гекс замикають прохід.
- КОЛИ `enter(unit, hidden_enemy)` → ТО `custom: «surprise: рух обірвано, ініціатива атакувальника 0/1»`.
- КОЛИ `input(attack, unit, target)` → ЯКЩО `adjacent(unit, target)` або `in_range(unit, target, range)` і `counter(ammo, >, 0)` → ТО `counter(ammo, −1)`; до бою — підтримувальний вогонь сусідньої артилерії/ППО захисника по атакувальнику.
- Хто стріляє першим: `custom: «ініціатива = Initiative юніта + досвід + rng(0..2); більша бʼє першою»`; при rugged defense або атаці не-піхоти на піхоту в лісі/місті/горах ініціатива атакувальника = 1.
- Шкода: `custom: «кожна одиниця сили бʼє окремо: атака за типом цілі (soft/hard/air) проти захисту (ground/air/close) + досвід + окопування»`; обидва бʼють одночасно, якщо ініціатива рівна (?).
- КОЛИ `custom: «атака на окопаний юніт»` → ЯКЩО `prob(rugged)` (вища в окопаних, нижча для досвідчених атакувальників) → ТО `custom: «rugged defense: захисник стріляє першим, атакувальник воює close defense»`.
- КОЛИ `custom: «атака на юніт»` → ТО `counter(entrenchment, −1)` цілі (будь-яка, вдала чи ні).
- КОЛИ `turn_end(side)` → ЯКЩО `not state(unit, moved)` → ТО `counter(entrenchment, +1)` до межі за ландшафтом (місто > ліс/гори > рівнина/дорога); КОЛИ `leave(unit, hex)` → ТО `counter(entrenchment, =0)`.
- КОЛИ `counter(fuel, ==, 0)` → ТО `custom: «бойові значення × ½»` (юніт без пального); КОЛИ `counter(ammo, ==, 0)` → ТО `custom: «не відповідає на атаку»`.
- КОЛИ `input(resupply, unit)` → ЯКЩО `not state(unit, moved)` → ТО `custom: «пальне і набої відновлюються; менше, якщо поруч ворог»`.
- КОЛИ `input(replace, unit)` → ЯКЩО `counter(prestige, ≥, cost)` → ТО `custom: «сила +n до 10»`, `currency(−cost)`; звичайні поповнення `counter(xp, −k)`, елітні — без втрати досвіду.
- КОЛИ `turn_end(side)` → ЯКЩО `counter(strength, ==, 10)` і `custom: «є золоті зірки досвіду»` → ТО `custom: «overstrength +1 за кожну зірку»`.
- КОЛИ `custom: «бій виграно»` → ТО `counter(xp, +n)` переможцю (більше — за сильнішого ворога); КОЛИ `counter(xp, ≥, 100·k)` → ТО `custom: «+1 зірка досвіду»`.
- КОЛИ `custom: «юніт отримав великі втрати»` → ТО `custom: «відступ на сусідній гекс; нема куди — капітуляція»` (?).
- КОЛИ `enter(infantry, enemy_city)` → ТО `set_side(city, side)`, `currency(+prestige)`.
- КОЛИ `input(buy, unit_type)` → ЯКЩО `counter(prestige, ≥, price)` і `custom: «вільне місто/аеродром для розгортання»` → ТО `spawn_at(unit, city)`, `currency(−price)`.
- КОЛИ `input(mount, infantry)` → ЯКЩО `not state(infantry, moved)` → ТО `set_state(infantry, mounted)` (рух транспорту, вразливість).
- КОЛИ `custom: «усі міста-цілі власні»` → ЯКЩО `counter(turns_left, ≥, 5)` → ТО `custom: «major victory»`; інакше `custom: «minor victory»`; оборонні сценарії — утримати ≥2 міст до кінця (≥5 — major).
- КОЛИ `counter(turn, >, limit)` → ЯКЩО `not custom: «цілі виконано»` → ТО `lose` сценарію; у кампанії — `custom: «генерала знімають — кінець»`.
- КОЛИ `all_gone(enemy_units)` → ТО `win`.
- Перемога: major / minor за швидкістю захоплення цілей · Поразка: ліміт ходів, втрата цілей · Рахунок: престиж і наступний сценарій кампанії.

## Керування і ввід
- Мишка: клік юніта → підсвічено досяжні гекси → клік гекса; наведення на ворога показує прицільний курсор і **оцінку втрат** обох сторін.
- Кнопки панелі: наступний юніт · перемикач повітря/земля · закупівля · поповнення · постачання · посадка в транспорт · стратегічна мапа · кінець ходу.
- ПКМ / Inspect — вікно параметрів юніта (атаки, захисти, ініціатива, пальне, набої, досвід, окопування).
- Скасування руху, якщо не було контакту (?).

## Вікна, меню, HUD
- `main-menu`: Campaign (вибір одного з 5 стартів: Poland, North Africa, Barbarossa, Italy, Kharkov) · Scenario (38) · Load · Options · Quit.
- `match-setup` для сценарію: сторона Axis/Allies, людина/AI, складність, опції (Hidden units, Weather, Supply…).
- `custom-window` «Briefing» (`+window:campaign-briefing`) — завдання і ліміт ходів.
- `game-screen`: гекс-мапа; `+ui:strength-plaque` (сила під іконкою, втрати спливають `popup-text`); `turn-counter`; `+ui:prestige`; `legal-move-highlight`; `fog-overlay`.
- `custom-window` «Unit info» — повні параметри юніта.
- `custom-window` «Purchase» (`+window:purchase-units`): клас → модель → ціна у престижі; модернізація.
- `map-window` — стратегічна мапа всього театру.
- `end-screen` сценарію (`+window:victory-tier`): major / minor / поразка, престиж, вибір наступного кроку кампанії.
- `save-slots` · `settings-window` (швидкість анімації, звук).

## Фічі поза полем
- Кампанія з **core army**: юніти з досвідом переходять у наступний сценарій; престиж — між битвами.
- Розгалуження: major victory змінює історію (Британія після Франції, Москва, США за обидві); поразка/звільнення — кінець.
- `hotseat` / мультиплеєр (два гравці, Axis проти Allies) (?) · `ai-opponent-levels` · `custom-rules` (вкл/викл туман, погоду, постачання).
- 38 окремих сценаріїв за реальними й вигаданими битвами.

## Варіації й родичі
- Серія «Five-Star»: Allied General, Fantasy General, Pacific General, Star General, Panzer General II, People's General, PG3D Assault, PG III Scorched Earth, Allied Assault (карткова), Fantasy General II.
- Наступники: Panzer Corps 1–2, Order of Battle, Open General, Open Panzer (браузер).
- Родичі в корпусі: [Advance Wars](advance-wars.md) (тип × тип, пальне), [Battle for Wesnoth](battle-for-wesnoth.md) (досвід і перенесення армії), [Polytopia](polytopia.md), Unity of Command (постачання).
- **Осі варіацій**: шкода — таблиця ([Advance Wars](advance-wars.md)) / атака × захист по типах цілі (PG) / CRT з шансами (Unity of Command) · логістика — нема / пальне і набої з поповненням на місці / лінії постачання · армія — одна битва / core army кампанії з досвідом.

## Цікавинки для курсу
- Ініціатива + випадковість 0–2 визначає, хто стріляє першим (або одночасно) — 📎.
- Окопування: росте щоходу на місці до межі ландшафту, падає від кожної атаки, нуль після руху — 🌱.
- ZOC на гексах: вхід зупиняє рух; два юніти через гекс — стіна — 📎.
- Підтримувальний вогонь сусідньої артилерії перед ударом — 📎.
- Престиж-економіка + core army з досвідом і overstrength між сценаріями — 🥈.
- Major/minor victory за кількістю зекономлених ходів + гілка кампанії — 📎.
- Два шари на одному гексі (повітря/земля) з окремою ZOC — 🥉.

## Мапа на каталог
- Є: `hp-damage` (сила 10) · `melee-vs-ranged` (артилерія) · `piece-move-patterns` · `legal-move-highlight` · `destroy-all-enemies` · `ai-opponent` · `hot-seat` (?) · `difficulty-levels` · `save-game` · `sequential-levels` (кампанія) · `shop-between-levels` + `round-currency` (престиж) · `fog-of-war` · `unit-xp-skills` · `game-settings`.
- **Нема** → пропозиції карток:
  - `+zone-of-control` / `+terrain-move-cost` / `+terrain-defense` / `+fuel-ammo` / `+branching-campaign` / `+weather-modifiers` / `+damage-forecast` — уже в корпусі.
  - `+entrenchment` «Окопування: росте на місці, падає від атак» · entities/state · 🌱.
  - `+rugged-defense` «Окопаний захисник стріляє першим» · entities/combat · 📎.
  - `+initiative-first-strike` «Хто бʼє першим: ініціатива + rng» · entities/combat · 📎.
  - `+support-fire` «Сусідня артилерія стріляє по атакувальнику» · entities/combat · 📎.
  - `+strength-points` «Сила юніта = HP і кількість атак» · entities/state · 🌱.
  - `+overstrength` / `+elite-replacements` «Поповнення понад 10 і без втрати досвіду» · entities/state · 🌱.
  - `+prestige-economy` «Престиж за перемоги й міста — валюта кампанії» · game-logic/economy · 📎.
  - `+core-army-carryover` «Армія переходить між сценаріями» · game-logic/progress · 🥉.
  - `+turn-limit-objectives` «Захопити всі цілі за N ходів» · game-logic/end · 🌱.
  - `+victory-tiers` «Major/minor victory за швидкістю» · game-logic/end · 🌱.
  - `+air-ground-layers` «Повітряний і наземний шар на гексі» · entities/state · 🥉.
  - `+mount-transport` «Сісти в транспорт: рух ↑, захист ↓» · entities/state · 📎.
  - `+resupply-in-place` «Поповнення пального/набоїв, якщо не рухався» · entities/state · 🌱.
  - `+surprise-contact` «Невидимий ворог обриває рух» · entities/ai · 📎.

## Пропозиції до словників
- `+trigger:enter_zoc` — сутність увійшла в зону контролю ворога.
- `+trigger:attacked` — юніт атаковано (підтримувальний вогонь, окопи).
- `+effect:counterattack` — відповідь захисника; `+effect:support_fire` — вогонь сусіда-підтримки перед боєм.
- `+effect:entrench` — +1 рівень окопування; `+cond:entrenchment` — рівень окопу.
- `+effect:resupply` — поповнити пальне/набої.
- `+cond:moved_this_turn` — юніт уже рухався цього ходу (артилерія, поповнення, посадка).
- `+role:objective-city` — клітина-ціль із власником.
- `+ui:strength-plaque` — табличка сили під юнітом; `+ui:prestige` — валюта кампанії.
- `+window:purchase-units` — закупівля/модернізація; `+window:campaign-briefing` — брифінг; `+window:victory-tier` — підсумок з рівнем перемоги.
- `+feature:core-army` — армія, що переходить між місіями.

## Джерела
- ⭐ [Wikipedia: Panzer General](https://en.wikipedia.org/wiki/Panzer_General) — класи і «камінь-ножиці», досвід, престиж, 38 сценаріїв, 5 стартів кампанії, major victory (≥5 ходів раніше), оборонні цілі, гілки, серія.
- [Фан-гайд 1996, ч. 1](https://discmaster.textfiles.com/view/10989/FANCLUB1.ISO/losung/pgstr1.txt) — 10 SP, overstrength за зірки, ініціатива 0–2, rugged defense і close defense, окопування −1 за атаку, ZOC, без пального × ½, підтримка артилерії, бомбардувальник пригнічує на хід.
- [Open Panzer manual](https://nicupavel.github.io/openpanzer-manual) — клон PG: ZOC, окопування за ландшафтом, набої, поповнення лише на місці, відступ, погода, рівні перемоги, core/auxiliary.
- Steam: пошук «Panzer General» (оригіналу нема).
- YouTube: пошук «Panzer General gameplay».

## Непевне
- (?) Точна формула бою PG (кількість раундів, як сила множить атаки) — гайд дає лише принципи.
- (?) Відступ при > 60 % втрат і капітуляція, базові рівні окопів (місто 3, ліс/гори 2…) і поповнення «на місці» — з Open Panzer, не з оригіналу.
- (?) Список ландшафтів і погод оригіналу — частково з Open Panzer.
- (?) Мультиплеєр/hot-seat оригіналу — Wikipedia згадує лише режим «проти людини».
- (?) Скасування руху (undo move) — є в Open Panzer, в оригіналі не перевірено.
