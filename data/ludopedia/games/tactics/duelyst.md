---
title: Duelyst
slug: duelyst
aka: [Duelyst II, OpenDuelyst]
family: tactics
also: [chess-abstract]
klass: figure
axes:
  field: square
  time: turn
  opponent: online
  info: hidden
  random: runtime
  goal: state
year: 2016
platforms: [PC, Mac, iOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Duelyst", best: true, note: "огляд: поле 9×5, генерали, 6 фракцій, режими (практика, челенджі, рейтинг, драфт), історія й закриття 2020, код під CC0"}
  - {kind: other, url: "https://raw.githubusercontent.com/open-duelyst/duelyst/main/app/common/config.js", note: "константи з відкритого коду: поле, рука, добір, мана, replace, колода, таймер ходу, артефакти"}
  - {kind: other, url: "https://github.com/open-duelyst/duelyst", note: "OpenDuelyst — відкритий код гри, локальний сервер"}
  - {kind: steam, url: "https://store.steampowered.com/app/2004320/Duelyst_II/", note: "Duelyst II (2022): ключові слова фракцій, рейтинг, крос-платформа"}
  - {kind: official, url: "https://duelyst2.com/", note: "сайт Duelyst II (Dream Sloth Games)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Duelyst+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [hp-damage, melee-vs-ranged, piece-capture, legal-move-highlight, threat-range, hover-highlight, selection-highlight, drag-drop-piece, cell-click, move-timer, turn-enforcement, ai-opponent, online-multiplayer, rating-system, lobby-window, match-setup, mode-select, puzzle-select, level-bank, tutorial-window, status-effects, temporary-modes, spawn-points, item-pickup, round-currency, shop-window, game-screen, main-menu, end-screen, replay, profile-stats, +deck-draw, +mana-curve, +summon-adjacent, +card-replace, +mulligan, +leader-death-lose, +counterattack, +zone-of-control, +card-keywords, +deck-builder, +draft-mode, +mana-tiles, +artifact-durability, +signature-spell-cooldown]
proposes: ["+trigger:summoned", "+trigger:died_any", "+trigger:attacked", "+cond:adjacent_to_general", "+cond:behind", "+effect:draw_card", "+effect:replace_card", "+effect:counterattack", "+effect:summon_from_hand", "+role:general", "+role:card", "+ui:mana-crystals", "+ui:replace-slot", "+ui:card-hover-zoom", "+window:deck-builder", "+window:mulligan-screen", "+window:faction-select", "+window:pack-opening", "+window:crafting-window", "+feature:card-collection", "+feature:draft-run"]
author: opus
date: 2026-11-09
---

# Duelyst — колекційна карткова гра на шаховій дошці 9×5: карти викликають юнітів на поле, а генерал — і фігура, і життя гравця

## Суть
Двоє гравців по черзі грають карти з руки за ману: міньйони зʼявляються на клітинах поля 9×5, заклинання і артефакти змінюють бій. Генерал кожного — фігура на полі з власною атакою; вбити генерала суперника = перемога, тому генерал і бʼється, і ховається. Юніти рухаються й атакують сусідів, ціль бʼє у відповідь (контратака); ключові слова (Provoke, Zeal, Flying, Ranged, Backstab…) змінюють правила руху й атаки. Партія ~10 хвилин; натхнення — Fire Emblem і Front Mission.

## Поле і час
- Квадратне поле 5 рядів × 9 стовпців (`BOARDROW = 5`, `BOARDCOL = 9`); генерали стартують на протилежних краях середнього рядка (?).
- На полі є клітини-джерела мани (mana springs/tiles): юніт, що став, дає власнику +1 ману одноразово (?).
- Хід: на початку — мана відновлюється (зростає до 9); гравець у будь-якому порядку грає карти, рухає й атакує кожним юнітом, раз замінює карту; кінець ходу — добір 1 карти.
- Таймер ходу 90 с (зворотний відлік видно з 20 с); неактивний гравець — 15 с (`TURN_DURATION`).
- Інформація прихована: рука і колода суперника; поле відкрите.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Генерал | piece | HP, атака (?) 25 / 2 | рух + атака як у міньйона; HP 0 = поразка гравця; має фірмове заклинання (Bloodborn) |
| Міньйон | piece | вартість мани, атака, HP, ключові слова | викликається з руки на клітину поруч зі своїми юнітами; наступного ходу рухається й атакує |
| Заклинання | supply | вартість мани, ціль | одноразовий ефект: шкода, лікування, переміщення, бафф |
| Артефакт | supply | міцність 3, до 3 одночасно | спорядження генерала: пасивний бафф; −1 міцності, коли генерал отримує шкоду (?) |
| Фірмове заклинання (Bloodborn spell) | supply | перезарядка в ходах (?) | вміння генерала; заряджається само |
| Колода | supply | 40 карт з генералом, ≤3 копії; драфт — 31 | добір 1 за хід; рука ≤ 6 |
| Рука | supply | старт 5, максимум 6 | надлишок при доборі втрачається (?) |
| Джерело мани | pickup | +1 мана | на полі; зникає після використання (?) |
| Wraithling (Abyssian) | ally | 1/1 (?) | слабкий токен; сила в кількості |
| Shadow Creep (Abyssian) | hazard | — | клітини, що ранять ворогів у кінці ходу власника (?) |
| Стіна (Vanar) | static | HP | блокує рух; руйнується (?) |
| Яйце (Rebirth, Magmar) | object | — | міньйон з Rebirth після смерті лишає яйце, з якого відроджується (?) |
| Dervish / Obelysk (Vetruvian) | spawner | — | обеліск щохід викликає дервіша (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО кожен бере 5 карт, `custom: «mulligan: до 2 замін»`; мана старту 2.
- КОЛИ `turn_start(side)` → ТО `custom: «мана = min(9, максимум +1)»` (?) і повне відновлення.
- КОЛИ `input(play_card, minion, cell)` → ЯКЩО `has(player, mana, cost) and free(cell) and custom: «клітина поруч (8) з моїм юнітом»` → ТО `counter(mana, -cost)`, `place(minion, cell)`; інакше `block`.
- КОЛИ `input(play_card, minion, cell)` → ЯКЩО `custom: «Airdrop»` → ТО можна на будь-яку вільну клітину.
- КОЛИ `spawned(minion)` → ЯКЩО `custom: «Opening Gambit»` → ТО ефект карти одразу.
- КОЛИ `spawned(minion)` → ЯКЩО `not custom: «Rush»` → ТО `set_state(minion, exhausted, 1 turn)` — цього ходу не діє.
- КОЛИ `input(move, unit, cell)` → ЯКЩО `legal(path ≤ 2)` (?) `and not state(unit, provoked)` → ТО `move(unit, cell)`; ЯКЩО `custom: «Flying»` → ТО будь-яка вільна клітина.
- КОЛИ `input(attack, unit, target)` → ЯКЩО `custom: «target у 8 сусідніх»` або `custom: «Ranged»` → ТО `damage(attack)` цілі; після атаки юніт більше не рухається цього ходу (?).
- КОЛИ `after(damage(attack))` → ЯКЩО `custom: «ціль вижила і атакувальник у її досяжності»` → ТО `custom: «counterattack»`: ціль бʼє у відповідь своєю атакою.
- КОЛИ `input(attack)` → ЯКЩО `custom: «Backstab» and custom: «атака ззаду»` → ТО бонус шкоди і **без** контратаки.
- КОЛИ `adjacent(enemy, provoke_unit)` → ТО `set_state(enemy, provoked)`: не рухається і мусить атакувати Provoke-юніта першим (?).
- КОЛИ `custom: «Zeal»` → ЯКЩО `custom: «юніт поруч зі своїм генералом»` → ТО бонус карти увімкнено.
- КОЛИ `input(attack)` → ЯКЩО `custom: «Frenzy»` → ТО `damage` усім ворогам поруч; `custom: «Blast»` → увесь рядок/стовпець (?).
- КОЛИ `died(minion)` → ЯКЩО `custom: «Dying Wish»` → ТО ефект карти; ЯКЩО `custom: «Rebirth»` → ТО `transform(egg)`.
- КОЛИ `died(any_minion)` → ТО `custom: «Deathwatch»`: тригер у юнітів з цим словом.
- КОЛИ `turn_start(owner)` → ЯКЩО `custom: «Grow»` → ТО `custom: «+атака/+HP»`.
- КОЛИ `enter(unit, mana_spring)` → ТО `currency(+1)` власнику, `disappear_b`.
- КОЛИ `input(replace, card)` → ЯКЩО `count(replaces_this_turn, <, 1)` → ТО `custom: «карта в колоду, взяти іншу»`.
- КОЛИ `turn_end(side)` → ТО `custom: «добрати 1 карту»`; ЯКЩО `count(hand, ==, 6)` → ТО добір згорає (?).
- КОЛИ `custom: «таймер ходу 0»` → ТО `end_turn`.
- КОЛИ `input(equip, artifact)` → ЯКЩО `count(artifacts, <, 3)` → ТО бафф генерала; КОЛИ `custom: «генерал отримав шкоду»` → ТО `counter(durability, -1)` кожному артефакту (?); 0 → `disappear_a`.
- КОЛИ `input(bloodborn)` → ЯКЩО `custom: «перезарядка завершена»` → ТО ефект фракції генерала.
- КОЛИ `hp_zero(enemy_general)` → ТО `win`; КОЛИ `hp_zero(own_general)` → ТО `lose`; обидва одночасно — нічия (?).
- Перемога: вбити генерала суперника · Поразка: свій генерал загинув · Рахунок: рейтинг/ранг у ladder, нагороди за перемоги.

## Керування і ввід
- Миша / тач: перетягнути карту з руки на клітину (`drag-drop-piece`) або клік-клік; клік по юніту → підсвітка ходів і атак → клік по клітині чи ворогу.
- Replace — перетягнути карту на слот заміни; кнопка кінця ходу з таймером.
- Наведення на карту чи юніт — збільшена карта з ключовими словами.

## Вікна, меню, HUD
- `main-menu`: Play (рейтинг, казуал, друг) · Practice (проти ШІ) · Challenges (пазли) · Gauntlet (драфт) · Collection / Deck builder · Shop · Profile · Settings.
- `mode-select` → `match-setup` (вибір колоди / генерала) → `lobby-window` / пошук суперника.
- `custom-window` «Mulligan» — 5 стартових карт, до 2 замін.
- `game-screen`: поле 9×5; генерали з HP; `pocket` (рука до 6 карт); кристали мани; слот replace; лічильник карт у колоді; артефакти й фірмове заклинання з перезарядкою; `timer-countdown` ходу; `end-turn-button`; `legal-move-highlight`, `threat-range`; `tooltip` карти.
- `custom-window` «Deck builder» — колекція за фракціями, ліміт 40/3 копії, крафт за «Spirit».
- `shop-window` — паки карт за Gold; `custom-window` відкриття паків (?).
- `custom-window` «Gauntlet» — драфт карт по одній з трьох (?), серія перемог до 3 поразок (?).
- `puzzle-select` — Challenges: «виграй за цей хід» з фіксованим станом.
- `end-screen` — перемога/поразка, нагороди, ранг; `replay` (?); `leaderboard` сезону (?).

## Фічі поза полем
- Колекція і деки: 6 фракцій (Lyonar, Songhai, Vetruvian, Abyssian, Magmar, Vanar), кожна з генералами й ключовими словами.
- Рейтинговий сезонний ladder, казуальні матчі, практика проти ШІ, драфт-турнір (Gauntlet, колода 31), пазли-челенджі, навчання.
- Економіка free-to-play: Gold (паки), Spirit (крафт); локальний OpenDuelyst відкриває всі карти.
- Історія: Kickstarter 2014 → реліз 27.04.2016 → закриття серверів 27.02.2020 → код CC0 (2023) → Duelyst II (Dream Sloth, 16.12.2022).

## Варіації й родичі
- Родичі в корпусі: [archon](archon.md) (фігури + бій на шаховому полі), [chaos-battle-of-wizards](chaos-battle-of-wizards.md) (заклинання викликають істот на сітку), [advance-wars](advance-wars.md) (дуель двох армій).
- Поза корпусом: Hearthstone (мана-крива, міньйони, бойові вигуки), Faeria (карти на гексах), Hand of Fate, Mythgard; сиквел Duelyst II.
- **Осі варіацій**: поле — нема (Hearthstone) / лінії (Inscryption) / сітка 9×5 (Duelyst) / гекси (Faeria) · «життя» гравця — HP героя поза полем / генерал на полі · виклик — будь-де / поруч зі своїми / Airdrop · заміна карт — нема / 1 replace за хід.

## Цікавинки для курсу
- Генерал = фігура й життя гравця: ризик vs вигода позиціонування — 🌱.
- Виклик лише поруч зі своїми юнітами (8-сусідство) + Airdrop як виняток — 📎.
- Атака з контратакою, Backstab без неї, Provoke як зона контролю — 🥉.
- Мана-крива 2 → 9 і replace раз на хід, mulligan 2 — 📎.
- Ключові слова як подієві тригери (Opening Gambit, Dying Wish, Deathwatch, Grow) — 🥈 (шина подій поверх двіжка).
- Челенджі «виграй за хід» з фіксованого стану — 🥉 (рівні як дані + перевірка розвʼязку).
- Онлайн-матч із таймером ходу 90 с — 🥇.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` · `piece-capture` (юніт гине від атаки) · `legal-move-highlight` · `threat-range` · `hover-highlight` · `selection-highlight` · `drag-drop-piece` · `cell-click` · `move-timer` (90 с) · `turn-enforcement` · `ai-opponent` (практика) · `online-multiplayer` · `rating-system` · `lobby-window` · `match-setup` · `mode-select` · `puzzle-select` / `level-bank` (челенджі) · `tutorial-window` · `status-effects` · `round-currency` (мана) · `shop-window` · `profile-stats`.
- **Нема** → пропозиції карток:
  - `+deck-draw` «Колода / рука / добір» · entities/state · 🥉 · {start: 5, max: 6, per_turn: 1}.
  - `+mana-curve` «Мана росте щохід до ліміту» · game-logic/economy · 🌱 · {start: 2, max: 9}.
  - `+summon-adjacent` «Виклик карти на клітину поруч зі своїми» · entities/spawn · 📎.
  - `+card-replace` «Замінити карту раз за хід» · game-logic/economy · 🌱.
  - `+mulligan` «Заміна стартової руки» · game-logic/economy · 🌱 · {count: 2}.
  - `+leader-death-lose` «Смерть лідера = поразка» · game-logic/lose · 🌱.
  - `+counterattack` «Ціль бʼє у відповідь» · entities/combat · 📎.
  - `+zone-of-control` «Provoke: сусіди не рухаються» · entities/legality · 📎.
  - `+card-keywords` «Ключові слова як тригери» · entities/state · 🥈.
  - `+deck-builder` «Збирання колоди з колекції» · interface/menus · 🥉 · {size: 40, copies: 3}.
  - `+draft-mode` «Драфт колоди перед серією» · game-logic/opponent · 🥉.
  - `+mana-tiles` «Клітини-бонуси ресурсу на полі» · entities/interact · 🌱.
  - `+artifact-durability` «Спорядження з міцністю» · entities/state · 📎 · {max: 3, durability: 3}.
  - `+signature-spell-cooldown` «Вміння лідера з перезарядкою» · entities/state · 🌱.

## Пропозиції до словників
- `+trigger:summoned` — юніта викликали з руки (Opening Gambit; відрізняти від `spawned` будь-якої появи).
- `+trigger:died_any` — загинув будь-який міньйон на полі (Deathwatch).
- `+trigger:attacked` — юніта атакують (контратака).
- `+cond:adjacent_to_general` — юніт поруч зі своїм генералом (Zeal); `+cond:behind` — атака ззаду (Backstab).
- `+effect:draw_card` — добір карти (не `draw` = нічия); `+effect:replace_card` — повернути карту в колоду й узяти іншу.
- `+effect:counterattack` — ціль бʼє у відповідь; `+effect:summon_from_hand` — виклик карти на клітину (зараз `place`).
- `+role:general` — фігура-лідер, чия смерть = поразка; `+role:card`.
- `+ui:mana-crystals` — кристали мани (є / максимум); `+ui:replace-slot` — слот заміни карти; `+ui:card-hover-zoom` — збільшена карта при наведенні.
- `+window:deck-builder` · `+window:mulligan-screen` · `+window:faction-select` · `+window:pack-opening` · `+window:crafting-window`.
- `+feature:card-collection` — колекція карт між партіями; `+feature:draft-run` — драфт-серія до N поразок.

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Duelyst) — поле 9×5, генерали, 6 фракцій, режими, історія, закриття, код CC0.
- [OpenDuelyst config.js](https://raw.githubusercontent.com/open-duelyst/duelyst/main/app/common/config.js) — BOARDROW/COL, рука 5/6, добір 1, мана 2…9, replace 1, mulligan 2, колода 40/31, ≤3 копії, таймер 90 с, артефакти 3/3.
- [OpenDuelyst на GitHub](https://github.com/open-duelyst/duelyst) — відкритий код, локальний запуск, Gold/Spirit.
- [Steam: Duelyst II](https://store.steampowered.com/app/2004320/Duelyst_II/) — ключові слова фракцій (Provoke, Zeal, Backstab, Deathwatch, Shadow Creep, Grow, Rebirth, Infiltrate, Walls, Dervish), режими.
- [duelyst2.com](https://duelyst2.com/) — сайт сиквела.
- YouTube: пошук «Duelyst gameplay».

## Непевне
- (?) HP/атака генерала 25/2, приріст мани +1 за хід, кількість і розташування джерел мани, старт генералів — з памʼяті (у config.js не знайшов).
- (?) Дальність руху 2 клітини, «після атаки не рухається», виклик лише в 8-сусідство — з памʼяті.
- (?) Точні правила ключових слів (Provoke, Blast, Frenzy, Rebirth, Shadow Creep, Dervish) і перезарядки Bloodborn-заклинань — з памʼяті.
- (?) Втрата міцності артефакту від шкоди генералу, перевищення руки, нічия при одночасній смерті — з памʼяті.
- (?) Формат Gauntlet (вибір з 3, до 3 поразок), replay і лідерборд — не перевірено.
