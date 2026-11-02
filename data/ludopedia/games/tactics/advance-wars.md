---
title: Advance Wars
slug: advance-wars
family: tactics
also: [build-sim]
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 2001
platforms: [GBA, Wii U VC, Switch (Re-Boot Camp, 2023)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Advance_Wars", best: true, note: "правила: перемога, прямі/непрямі атаки, пальне, ландшафт, туман, CO Power, режими"}
  - {kind: play, url: "https://awbw.amarriner.com/guide.php", note: "Advance Wars By Web — фанатська онлайн-версія, FAQ правил (1000 G за властивість, туман, CO Power)"}
  - {kind: other, url: "https://awbw.amarriner.com/damage.php", note: "AWBW: повна таблиця базової шкоди юніт × юніт"}
  - {kind: fandom, url: "https://advancewars.fandom.com/wiki/Special:Search?query=Advance+Wars", note: "пошук по вікі серії"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=advance+wars+gba+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [piece-move-patterns, legal-move-highlight, melee-vs-ranged, hp-damage, round-currency, destroy-all-enemies, ai-greedy, hot-seat, interaction-table, inventory-limit, in-game-editor, level-select, level-unlock, shop-between-levels, +capture-property, +unit-production, +fuel-ammo, +terrain-bonus, +terrain-move-cost, +damage-matrix, +commander-power, +fog-of-war, +transport-load, +unit-merge, +resupply-adjacent]
proposes: ["+trigger:phase_start", "+effect:capture", "+effect:produce", "+effect:load", "+effect:unload", "+effect:resupply", "+effect:counterattack", "+cond:fuel", "+role:property", "+ui:funds", "+ui:co-power-meter", "+ui:terrain-stars", "+window:co-select", "+window:intel", "+window:production", "+window:battle-maps-shop"]
author: opus
date: 2026-11-02
---

# Advance Wars — армія без імен на клітинах: захоплюй міста, купуй танки, стеж за пальним

## Суть
Дві-чотири армії по черзі ходять на квадратній карті: кожен юніт рухається і діє (атака, захоплення, завантаження, очікування). Економіка — у **будівлях**: піхота захоплює міста за кілька ходів, кожна власна будівля дає 1000 G на хід, а заводи/аеропорти/порти виробляють нові юніти. Бій детермінований майже повністю: шкода = таблиця «хто проти кого» × HP атакуючого × захист ландшафту, плюс невелика випадковість. Над армією — командир (CO) з пасивними бонусами і силою, що накопичується.

## Поле і час
- Квадратна сітка (карти ~15×10 … 30×20), камера з прокруткою; клітина — ландшафт з «зірками захисту» (0–4) і ціною руху для 6 типів пересування.
- Хід = «день»: кожна армія по черзі (Orange Star → Blue Moon → …) ходить усіма юнітами в довільному порядку; лічильник днів.
- Туман війни (в окремих картах): видно лише в радіусі зору юнітів і власних будівель; ліси й рифи ховають юніт, якщо поруч нема свого.
- Погода (дощ/сніг) — у Versus і на CO Power Olaf: зменшує рух/зір.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Infantry | piece | 1000 G, Mov 3, пальне 99 | захоплює; кулемет |
| Mech | piece | 3000 G, Mov 2, базука 3 набої | захоплює; бʼє техніку; ходить по горах дешевше |
| Recon | piece | 4000 G, Mov 8, зір 5 | швидка розвідка, кулемет |
| APC | piece | 5000 G, Mov 6, без зброї | везе 1 піхотинця; щоходу постачає сусідні юніти пальним і набоями |
| Tank / Md Tank | piece | 7000 / 16000 G | прямий удар: гармата (набої) + кулемет |
| Artillery / Rockets | piece | 6000 / 15000 G, дальність 2–3 / 3–5 | непрямий удар: не можна рухатись і стріляти того ж ходу; не контратакує |
| Anti-Air / Missiles | piece | 8000 / 12000 G | ППО: прямий / непрямий по повітряних |
| Fighter / Bomber | piece | 20000 / 22000 G, пальне −5/день | повітря проти повітря / проти землі; без пального — падає |
| B Copter / T Copter | piece | 9000 / 5000 G, пальне −2/день | гелікоптер-ударник / транспорт 1 піхоти |
| Battleship / Cruiser | piece | 28000 / 18000 G | непрямий морський / ППО і проти підводних |
| Lander | piece | 12000 G | транспорт 2 наземних юнітів; висаджує на пляжі |
| Submarine | piece | 20000 G | Dive: невидима, пальне −5/день; бачать лише сусіди |
| HQ (штаб) | static | 20 очок захоплення, ★4 | захоплено ворогом → поразка армії |
| City | static | ★3, +1000 G/день | ремонт +2 HP наземним своєї армії |
| Base / Airport / Port | spawner | ★3, +1000 G/день | виробництво наземних / повітряних / морських; ремонт свого типу |
| Plain / Road / Bridge | terrain | ★1 / ★0 / ★0 | ціна 1 (машини на рівнині: колеса дорожче) |
| Wood | terrain | ★2 | ховає в тумані; ціна 2 для колес/гусениць |
| Mountain | terrain | ★4 | лише піхота (2) і мехи (1); +зір у тумані |
| River | terrain | ★0 | лише піхота/мехи |
| Sea / Shoal / Reef | terrain | ★0 / ★0 / ★1 | море для кораблів; мілина — висадка; риф ховає в тумані |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(side)` → ТО `currency(+1000 × власні будівлі)`; на власних будівлях свого типу `heal(unit, 2)` за `currency(−10 % ціни × HP)`; APC → `custom: «resupply сусідам»`; повітря/флот `counter(fuel, −k)`; `counter(fuel, ==, 0)` для повітря/флоту → `disappear_a`.
- КОЛИ `input(build, base, unit)` → ЯКЩО `counter(funds, ≥, price)` і `not occupied(base)` → ТО `spawn_at(unit, base)`, `currency(−price)`; новий юніт діє лише наступного дня.
- КОЛИ `input(move, unit, cell)` → ЯКЩО `custom: «шлях за ціною ландшафту ≤ Mov і ≤ fuel»` → ТО `move`, `counter(fuel, −клітин)`; ворожий юніт на шляху в тумані → `custom: «trap: рух обривається»`.
- КОЛИ `input(fire, target)` для прямого юніта → ЯКЩО `adjacent(target)` після руху → ТО шкода; захисник, якщо вижив і дістає, **контратакує** зі своїм меншим HP.
- КОЛИ `input(fire, target)` для непрямого → ЯКЩО `not moved_this_turn` і `in_range(min..max)` → ТО шкода без контратаки.
- Шкода: `custom: «dmg% = base[att][def] × (HP_att/10) × CO-модифікатори × (100 − ★ × HP_def)/100 + rng(0..9)»`; HP показується 1–10 (з округленням угору) (?).
- Зброя: КОЛИ основна зброя → `counter(ammo, −1)`; `ammo == 0` → ТО `custom: «вторинна зброя (кулемет), якщо є»`.
- КОЛИ `input(capture, property)` → ЯКЩО unit ∈ {Infantry, Mech} → ТО `counter(capture, −HP_display)` від 20; `== 0` → `set_side(property, side)`; КОЛИ юніт пішов/загинув → ТО `counter(capture, =20)`.
- КОЛИ `set_side(HQ, enemy)` → ТО `lose` для власника штабу.
- КОЛИ `input(load, transport)` → ЯКЩО місце є і тип підходить → ТО `custom: «load»`; `input(drop, cell)` → висадка на сусідню прохідну клітину.
- КОЛИ `input(join, ally_same_type)` → ТО `merge(a, b → c)` (HP сумуються до 10, надлишок → гроші) (?).
- КОЛИ `input(dive|surface)` → ТО `set_state(sub, submerged)`; видно лише сусідам.
- КОЛИ шкода завдана/отримана → ТО `counter(co_meter, +n)` (за вартістю знищеного); повний → `input(co_power)` → `set_state(army, power, 1 turn)`.
- КОЛИ `all_gone(enemy_units)` (rout) → ТО `win`; КОЛИ захоплено ворожий HQ → `win`; на окремих картах — захопити N міст або протриматись N днів.
- Поразка: втрачено HQ / усі юніти / умова місії · Рахунок: ранг S/A/B/C за Speed (дні), Power (знищені), Technique (вцілілі свої).

## Керування і ввід
- Курсор (D-pad), A на юніті → синя зона руху → клітина → меню: Fire · Capt · Supply · Load · Drop · Join · Dive/Rise · Wait.
- A на своїй базі → вікно виробництва зі списком і цінами (сірі — не вистачає грошей).
- B на юніті ворога (утримання) — показати його зону атаки; R — інфо про юніт/ландшафт.
- A на порожній клітині → меню: Unit · Intel · CO · Options · Save · End (кінець дня). CO Power — пункт «Power», коли шкала повна.

## Вікна, меню, HUD
- `splash-screen` → `main-menu`: Field Training · Campaign · War Room · Versus · Link · Stats · Design Room · Battle Maps (магазин).
- `custom-window` «CO select» — портрети CO, опис сили; налаштування гри: туман, погода, стартові гроші, гроші за будівлю.
- `game-screen`: карта; `turn-indicator` (колір армії) і `turn-counter` (день); панель CO: портрет, `coins` (гроші), шкала CO Power; панель під курсором: ландшафт з `★`, захоплення; юніт: HP-цифра на спрайті, пальне, набої; `fog-overlay`; `threat-range`.
- `custom-window` «Production» — список юнітів з цінами.
- `custom-window` «Battle animation» — коротка сцена обміну ударами (можна вимкнути).
- `custom-window` «Intel» — статус армій: юніти, будівлі, дохід, правила карти.
- `end-screen` — перемога/поразка з рангом (Speed/Power/Technique, S–C).
- `shop-window` «Battle Maps» — Hachi продає CO і карти за монети.
- `editor-window` «Design Room» — редактор карт.
- Переходи: main-menu → (Campaign) діалог → game-screen → end-screen → наступна місія / (War Room) level-select → game-screen.

## Фічі поза полем
- Режими: `tutorial` (Field Training) · кампанія (історія, вибір гілок) · War Room (карти на ранг/рекорд) · `hotseat` (Versus: одна консоль передається) · Link (до 4 GBA) · `level-editor` (Design Room).
- `rank-tiers`: гравець від #100 до #1; `unlockables`: монети → CO і карти в Battle Maps; `leaderboard-local` War Room.
- `ai-opponent-levels` — ШІ на картах; `custom-rules`: туман, погода, стартові/щоденні гроші, ліміт днів/міст.
- `save-slots` / `suspend` посеред карти; `animation-toggle` (бойові сцени вкл/викл).

## Варіації й родичі
- Серія: Game Boy Wars (1990–), AW2 (Super CO Power, Neotank), Dual Strike (два екрани, тег-CO), Days of Ruin (похмурий, нові юніти), Re-Boot Camp (2023, ремейк 1+2).
- Родичі: Fire Emblem (той самий розробник, але персонажі), Wargroove (командир на полі), Tiny Metal, Battle Isle, Nectaris, Polytopia (місто → юніти).
- **Осі варіацій**: економіка — нема / за будівлі / за захоплення території · бій — детермінований / ±rng / кубики · логістика — нема / пальне і набої / постачання · командир — пасивний бонус / сила за шкалою / юніт на полі (Wargroove).

## Цікавинки для курсу
- Матриця шкоди «юніт × юніт» + множник HP атакуючого + зірки ландшафту — 🥉 (таблиця як дані, формула).
- Захоплення будівлі за кілька ходів (лічильник 20 − HP) зі скиданням при відході — 📎.
- Економіка: дохід з будівель → виробництво на базах із переліком цін — 🥉.
- Пальне й набої + постачання від APC, падіння літаків без пального — 📎.
- Непряма атака: «або рух, або постріл», без контратаки — 📎.
- Туман війни з радіусом зору, укриттям у лісі й «пасткою» при русі — 🥈.
- CO Power: шкала, що наповнюється шкодою, і тимчасовий бонус армії — 📎.

## Мапа на каталог
- Є: `piece-move-patterns` (Mov + тип пересування) · `legal-move-highlight` · `melee-vs-ranged` (прямі/непрямі) · `hp-damage` · `round-currency` (G щодня) · `destroy-all-enemies` (rout) · `ai-greedy` · `hot-seat` · `turn-enforcement` · `interaction-table` (шкода як таблиця) · `inventory-limit` (місткість транспорту) · `in-game-editor` + `editor-palette` (Design Room) · `level-select` + `level-unlock` (War Room, Battle Maps) · `shop-between-levels` (Battle Maps) · `score-records` (ранги War Room) · `save-single-slot` · `game-screen` · `main-menu` · `mode-indicator` (чий день, CO Power) · `minimap-radar` (Intel-мапа) (?).
- **Нема** → пропозиції карток:
  - `+capture-property` «Захоплення будівлі за кілька ходів» · game-logic/economy · 📎 · слот {points: 20}.
  - `+unit-production` «Виробництво юнітів на базі» · game-logic/economy · 🥉.
  - `+fuel-ammo` «Пальне і набої» · entities/state · 📎.
  - `+terrain-bonus` / `+terrain-move-cost` — спільні з Fire Emblem.
  - `+damage-matrix` «Таблиця шкоди тип × тип» · entities/combat · 🥉.
  - `+commander-power` «Сила командира за шкалою» · game-logic/economy · 📎.
  - `+fog-of-war` — спільна з Fire Emblem.
  - `+transport-load` «Транспорт з місткістю» · entities/interact · 📎.
  - `+unit-merge` «Злиття поранених юнітів» · entities/state · 🌱.
  - `+resupply-adjacent` «Постачання сусідам на початку ходу» · entities/interact · 🌱.

## Пропозиції до словників
- `+trigger:phase_start` — початок дня армії (дохід, ремонт, пальне) — уточнення ⏳ `turn_start(side)`.
- `+effect:capture` — зменшити очки захоплення; `+effect:produce` — купити й поставити юніт; `+effect:load` / `+effect:unload` — посадка/висадка; `+effect:resupply` — поповнити пальне/набої; `+effect:counterattack` — відповідь захисника.
- `+cond:fuel` — достатньо пального (частковий випадок `has`).
- `+role:property` — будівля з власником, що дає дохід/ремонт/виробництво (між `static` і `spawner`).
- `+ui:funds` — гроші армії; `+ui:co-power-meter` — шкала сили командира; `+ui:terrain-stars` — захист клітини зірками.
- `+window:co-select` — вибір командира; `+window:intel` — статус армій; `+window:production` — купівля юнітів; `+window:battle-maps-shop` — магазин відкриттів.

## Джерела
- ⭐ [Wikipedia: Advance Wars](https://en.wikipedia.org/wiki/Advance_Wars) — перемога, бій, пальне, ландшафт, туман, CO Power, режими, ранги.
- [AWBW guide](https://awbw.amarriner.com/guide.php) — правила фанатської онлайн-версії: 1000 G за будівлю, туман, CO Power.
- [AWBW damage chart](https://awbw.amarriner.com/damage.php) — таблиця базової шкоди (Infantry↔Infantry 55, Md Tank→Tank 85, Anti-Air→B Copter 120).
- YouTube: пошук «advance wars gba gameplay».

## Непевне
- (?) Точна формула шкоди AW1 (множник HP, зірки × HP захисника, удача 0–9 %) — з памʼяті; AWBW дає лише базову таблицю.
- (?) Ціни юнітів і витрата пального — з памʼяті (AW1/AW2).
- (?) Join: надлишок HP → гроші — у AW1 чи лише з AW2.
- (?) Ремонт +2 HP за 20 % ціни; чи APC постачає на початку ходу чи командою Supply (обидва — з памʼяті).
- (?) Ціна руху колес/гусениць на рівнині/лісі — загально з памʼяті.
