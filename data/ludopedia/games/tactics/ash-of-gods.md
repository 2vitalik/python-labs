---
title: "Ash of Gods: Redemption"
slug: ash-of-gods
aka: [Ash of Gods, AoG]
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: setup
  goal: state
year: 2018
platforms: [PC, Mac, Linux, iOS, Android, Switch, PS4, Xbox One]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Ash_of_Gods:_Redemption", best: true, note: "тактика + колода карт, навички коштують енергію і здоровʼя, смерть героя ≠ кінець гри, порівняння з Banner Saga"}
  - {kind: steam, url: "https://store.steampowered.com/app/691690/", note: "без кидків кубика, ліміт карт, «витратити своє HP на останній удар», менший загін — кращі карти, PvP"}
  - {kind: other, url: "https://maroonersrock.com/ash-of-gods-redemption-pc-review", note: "квадратна сітка, до 6 героїв, хід по одному юніту почергово, карта замість ходу героя, до 5 карт у колоді"}
  - {kind: other, url: "http://www.gamebanshee.com/k4u49", note: "огляд: почергові ходи, порядок своїх юнітів обирає гравець, менші загони вигідніші"}
  - {kind: other, url: "https://www.siliconera.com/ash-gods-redemption-tactical-game-rewards-risk-takers/", note: "сильніші атаки ціною HP, адаптивний AI, коротший небезпечний маршрут"}
  - {kind: other, url: "https://www.moddb.com/tutorials/a-new-approach-to-turn-based-strategies", note: "пост розробників про бойову систему (403 при відкритті; зміст — за пошуковим сніпетом)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Ash+of+Gods+Redemption+combat+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [hp-damage, melee-vs-ranged, legal-move-highlight, reachable-highlight, hover-highlight, placement-screen, ai-opponent, destroy-all-enemies, unit-xp-skills, permadeath, difficulty-levels, world-map, save-autosave, online-multiplayer, leaderboard, +strength-is-hp, +alternating-side-turns, +dual-pool-target, +pay-with-hp, +energy-zero-double, +card-instead-of-turn, +fewer-units-more-cards, +story-choices, +no-dice-combat]
proposes: ["+cond:target_pool(pool)", "+effect:swap_stats(a, s1, s2)", "+ui:dual-bar", "+ui:card-hand", "+feature:story-mode-maxed", "+feature:ironman", "+card:dual-pool-target", "+card:pay-with-hp"]
author: opus
date: 2026-11-09
---

# Ash of Gods: Redemption — Banner Saga-подібна тактика, де кожен удар обирає ціль: здоровʼя або енергію, а за навички платять тими самими смугами

## Суть
Покрокові бої загонів на квадратній сітці в ізометрії з почерговими ходами по одному юніту — як у [banner-saga](banner-saga.md). Описано **відмінності**. Замість пари «броня / сила» в кожного юніта **здоровʼя і енергія**, і гравець сам обирає, по якій смузі бити; коли енергії нема, удари по ній стають подвійними. Навички коштують здоровʼя або енергії (ціна кратна атаці), тож сильний удар — ризик для себе. Поверх тактики — **колода до 5 карт**, яку грають замість ходу героя; менший загін отримує кращі карти. Кубиків нема: результат удару детермінований.

## Поле і час
- Квадратна сітка, ізометричний ракурс; перед боєм — розстановка в стартовій зоні.
- До 6 героїв у загоні; у ворога може бути більше або менше.
- Хід: сторони ходять **по одному юніту почергово**; порядок своїх юнітів гравець обирає сам у межах раунду; раунд закінчується, коли походили всі юніти обох сторін.
- Випадковості в ударі нема; випадковість лише в подіях подорожі й складі карт (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой (класи: воїн, лучник, маг…) | piece | Health, Energy, Attack, навички класу | рух, удар по здоровʼю або енергії цілі, навички за здоровʼя/енергію |
| Ворог (людина, Reaper, звір) | enemy | ті самі стати | адаптивний AI — відповідає на повторювану тактику |
| Енергія | resource | смуга юніта | витрачається на навички; 0 → удари по енергії подвійні |
| Здоровʼя | resource | смуга юніта | 0 → юніт падає; можна витратити на сильний удар |
| Карта (талісман) | supply | рівень сили; потужні — з пізніших раундів | грається замість ходу героя; ефект на поле/юніта |
| Перешкода | static | — | займає клітини |
| Караван/загін у подорожі | container | припаси (?) | дорога між боями: маршрути з ризиком і витратами |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_end(side)` → ТО `custom: «хід переходить до будь-якого ще не ходившого юніта іншої сторони, обраного її гравцем»`.
- КОЛИ `custom: «усі юніти обох сторін походили»` → ТО `custom: «новий раунд»`, `custom: «відкриваються сильніші карти»`.
- КОЛИ `input(move, unit, cell)` → ЯКЩО `path_exists(unit, cell)` і `custom: «в межах руху»` → ТО `move(unit, cell)`.
- КОЛИ `input(attack_health, a, t)` → ЯКЩО `adjacent(a, t)` або `in_range(a, t, range)` → ТО `damage(t, a.attack)` по здоровʼю.
- КОЛИ `input(attack_energy, a, t)` → ЯКЩО `counter(t.energy, >, 0)` → ТО `custom: «−attack з енергії цілі»`; ЯКЩО `counter(t.energy, ==, 0)` → ТО `custom: «подвійна шкода»` (?).
- КОЛИ `input(skill, a)` → ЯКЩО `counter(a.energy, >=, k × a.attack)` → ТО `counter(a.energy, −k × a.attack)`, `custom: «ефект навички»`; частина навичок платиться здоровʼям — `hp(a, −k × a.attack)`.
- КОЛИ `input(last_ditch, a, t)` → ТО `hp(a, −n)`, `custom: «посилений удар»` (Steam: «витратити своє HP на останній удар»).
- КОЛИ `input(card, c)` → ЯКЩО `custom: «раунд ≥ мінімального для карти»` → ТО `custom: «ефект карти»`, `end_turn`, `take(player, c)`.
- Приклад карти: КОЛИ `input(card_swap, t)` → ТО `custom: «обміняти здоровʼя й енергію цілі»` — юніт без енергії гине.
- КОЛИ `hp_zero(unit)` → ТО `disappear(unit)`; герой — `custom: «смерть остаточна (Ironman) або наслідки для сюжету, гра триває»`.
- Перемога: `all_gone(enemy)` → `win` · Поразка: `all_gone(hero)` → `custom: «сюжет іде далі з наслідками»` (?).
- Карти: КОЛИ `level_start` → ЯКЩО `custom: «у загоні менше героїв»` → ТО `custom: «кращі / більше карт»`.
- Подорож: КОЛИ `input(route, short_dangerous)` → ТО `custom: «менше витрат припасів, вищий ризик»`; КОЛИ `counter(supplies, ==, 0)` → ТО `custom: «загін втрачає людей»` (?).

## Керування і ввід
- Миша/тач/геймпад: обрати юніта зі ще не ходивших → підсвічені клітини руху → ціль → кнопки «бити здоровʼя» / «бити енергію» / навичка.
- Рука карт: тап по карті замість дії героя; карти з вищим порогом раунду неактивні.
- Перед боєм — розстановка героїв і вибір колоди (до 5 карт).

## Вікна, меню, HUD
- `main-menu`: кампанія, PvP (Arena), налаштування; вибір складності (Story / звичайна / Ironman).
- `game-screen`: сітка, над юнітом `dual-bar` (здоровʼя + енергія), `reachable-highlight`, `turn-order-bar` (?), `card-hand` з порогами раундів, прогноз шкоди.
- `placement-screen` — стартові позиції; `character-select` — склад загону; `custom-window` — колода карт.
- `map-window` — карта подорожі з маршрутами; `dialogue-window` — події з виборами.
- `end-screen`, `pause-menu`, `settings-window`, `leaderboard` (PvP).

## Фічі поза полем
- Три загони з різними героями, сюжет з розгалуженням; смерть головного героя не завершує гру.
- `difficulty-presets`: Story Mode (герої максимального рівня) · Ironman (смерті остаточні).
- `autosave` в один слот; `online-multiplayer` PvP з таблицею; адаптивний AI.

## Варіації й родичі
- [banner-saga](banner-saga.md) — пряме натхнення: та сама черга ходів і подорож; там броня/сила й Willpower, тут здоровʼя/енергія і карти.
- Сиквели AurumDust: Ash of Gods: Arena (PvP), The Way (карткова тактика, 2020), Tactics (?).
- **Осі варіацій** (до осей Banner Saga): чим платять за навички (окремий ресурс / власним HP або енергією) · дві смуги (броня, що ріже шкоду / енергія, що подвоює шкоду на нулі) · додатковий шар (нема / колода, що грається замість ходу).

## Цікавинки для курсу
- Дві смуги й вибір цілі удару + подвоєння на нульовій енергії — 📎.
- Ціна навички = k × атака, оплата здоровʼям або енергією — 🌱.
- Карта, що міняє місцями два стати (смерть юніта без енергії) — 🌱.
- Карта замість ходу юніта + поріг раунду для сильних карт — 📎.
- Менший загін → кращі карти (компенсація нерівності) — 🌱.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` · `legal-move-highlight` + `reachable-highlight` · `hover-highlight` · `placement-screen` · `ai-opponent` · `destroy-all-enemies` · `unit-xp-skills` · `permadeath` ↔ Ironman · `difficulty-levels` · `world-map` ↔ мапа подорожі · `save-autosave` · `online-multiplayer` + `leaderboard`.
- **Нема** → пропозиції карток:
  - `+dual-pool-target` «Удар обирає смугу: здоровʼя чи енергія» · entities/combat · 📎.
  - `+pay-with-hp` «Навичка платиться власним HP/енергією» · entities/combat · 🌱.
  - `+energy-zero-double` «Нуль ресурсу подвоює шкоду по ньому» · entities/combat · 🌱.
  - `+card-instead-of-turn` «Карта грається замість ходу юніта; поріг раунду» · game-logic/opponent · 📎.
  - `+fewer-units-more-cards` «Менший загін — більше карт» · game-logic/difficulty · 🌱.
  - `+no-dice-combat` «Детермінований бій без шансу влучання» · entities/combat · 🌱.
  - `+strength-is-hp`, `+alternating-side-turns`, `+story-choices` — повторно (Banner Saga).

## Пропозиції до словників
- `+cond:target_pool(pool)` — удар спрямовано в смугу (`health` / `energy`).
- `+effect:swap_stats(a, s1, s2)` — обміняти значення двох статів юніта.
- `+ui:dual-bar` — дві смуги над юнітом; `+ui:card-hand` — рука карт з порогами активації.
- `+feature:story-mode-maxed` — режим «історія» з героями максимального рівня; `+feature:ironman` — смерті й рішення остаточні.
- `+card:dual-pool-target`, `+card:pay-with-hp` — див. вище.

## Джерела
- ⭐ [Wikipedia: Ash of Gods: Redemption](https://en.wikipedia.org/wiki/Ash_of_Gods:_Redemption) — колода карт як заклинання, навички коштують енергію і здоровʼя, смерть героя ≠ game over, три загони, AurumDust, дати й платформи, порівняння з Banner Saga.
- [Steam](https://store.steampowered.com/app/691690/) — без кубиків, обмежені карти, «витратити HP на останній удар», менший загін — кращі карти, PvP, адаптивний AI.
- [Marooners' Rock: огляд](https://maroonersrock.com/ash-of-gods-redemption-pc-review) — квадратна сітка, до 6 героїв, почергові ходи, раунд, карта замість ходу, до 5 карт, Story/Ironman.
- [GameBanshee: огляд, с. 2](http://www.gamebanshee.com/k4u49) — порядок своїх ходів обирає гравець; менші загони.
- [Siliconera](https://www.siliconera.com/ash-gods-redemption-tactical-game-rewards-risk-takers/) — атаки ціною HP, адаптивний AI, ризиковий маршрут.
- [ModDB: A New Approach To Turn-Based Strategies](https://www.moddb.com/tutorials/a-new-approach-to-turn-based-strategies) — пост розробників (не відкрився, 403): три стати (здоровʼя, енергія, атака), ціна навичок у атаках, вибір «по здоровʼю чи по енергії», подвоєння на нулі енергії, карта обміну стати — за сніпетом пошуку.

## Непевне
- (?) Подвоєння: удар по нульовій енергії йде в здоровʼя подвійно чи просто «подвійна шкода» — сніпет не уточнює; механіка могла змінитись у балансному патчі.
- (?) Чи завжди можна обрати смугу («у більшості випадків» — каже розробник).
- (?) Strain (виснаження/хвороба в подорожі), припаси й маршрути — деталі не перевірено.
- (?) Як саме менший загін дає кращі карти; склад карт випадковий чи фіксований.
- (?) `turn-order-bar` у HUD; рівні складності, крім Story та Ironman.
