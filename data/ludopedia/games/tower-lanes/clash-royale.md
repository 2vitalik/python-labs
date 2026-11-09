---
title: Clash Royale
slug: clash-royale
aka: [CR, Клеш Рояль]
family: tower-lanes
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: online
  info: partial
  random: setup
  goal: state
year: 2016
platforms: [iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Clash_Royale", best: true, note: "річка й два мости, King + 2 Princess Towers, еліксир до 10, колода 8 / рука 4, 3 хв + овертайм, тайбрейк, режими"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=clash+royale+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [round-currency, cursor-place, drag-drop-piece, hp-damage, tower-range, melee-vs-ranged, explode-area, spawner-entity, timed-despawn, chase-greedy, online-multiplayer, ai-opponent, move-timer, enemy-reached-base, status-effects, mode-select, match-setup, lobby-window, leaderboard, shop-window, tutorial-window, end-screen, popup-text, +deck-draw, +card-cycle-queue, +regen-currency, +lane-grid, +two-lanes-bridges, +placement-zone-expand, +king-tower-wake, +overtime-sudden-death, +tiebreak-lowest-hp, +card-levels, +draft-pick, +clan-card-request, +loadout-select]
proposes: ["+role:card", "+role:building", "+role:base", "+trigger:card_played", "+trigger:deploy_done", "+effect:draw", "+effect:wake", "+cond:in_zone", "+cond:target_type", "+ui:elixir-bar", "+ui:next-card-preview", "+ui:crown-counter", "+window:deck-builder", "+window:chest-window", "+window:clan-window", "+feature:card-collection", "+feature:battle-pass", "+axis:field=lanes"]
author: opus
date: 2026-11-09
---

# Clash Royale — дві смуги через річку: карти з руки за еліксир, ціль — королівська вежа суперника

## Суть
Дуель 1v1 у реальному часі на вертикальній арені: річка ділить її навпіл, два мости роблять з неї **дві смуги**. Гравець не керує юнітами — лише кидає карти з руки (4 з колоди 8) у точку свого поля, платячи еліксиром, що набігає сам; далі юніти йдуть і бʼються самі. На кожній стороні три вежі (King + 2 Princess); знищив King Tower — перемога, інакше рахують знесені вежі. Це tower defense і tower offense водночас: захист своєї смуги = атака на чужу.

## Поле і час
- Поле — вертикальна прямокутна арена з сіткою клітин для розстановки; рух юнітів плавний, але точка висадки — клітина (?).
- Шари: земля (свої половина й чужа) · річка (непрохідна для наземних) · два мости — єдині переходи · вежі як статичні цілі; повітряні юніти летять над річкою.
- Зона розстановки: війська й будівлі — лише на своїй половині; заклинання — будь-де. Знесена Princess Tower частково розширює твою зону на чужу сторону (на її смузі).
- Час: realtime; матч до 3 хв основного часу, в останню хвилину еліксир удвічі; при рівному рахунку веж — овертайм до 2 хв (у фінальну хвилину — потрійний еліксир), перша знесена вежа вирішує.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| King Tower | static (`+role:base`) | HP, рівень від King Level | спить на старті; прокидається, якщо її вдарили або впала Princess Tower; падіння = поразка |
| Princess Tower | tower | HP, дальність | стріляє в ворогів на своїй половині; ліва й права — по одній на смугу |
| Tower Troop | ally | — | хто сидить на Princess Tower (Tower Princess або інші, відкриті прогресом) |
| Карта-військо (troop) | ally (`+role:card`) | вартість еліксиру, HP, шкода, швидкість, ціль (земля/повітря/лише будівлі), рідкість, рівень | висаджується → іде до найближчої цілі по своїй смузі, бʼється сама |
| Карта-будівля | static (`+role:building`) | вартість, HP, час життя (?) | стоїть на місці: стріляє або породжує юнітів; притягує ворогів, що бʼють будівлі |
| Карта-заклинання | projectile (`+role:card`) | вартість, радіус | миттєва дія в області будь-де на арені (шкода, статус) |
| Champion | ally | здібність з cooldown (?) | військо з окремою кнопкою активної здібності (з 2021) |
| Evolution | ally | лічильник циклів | карта, зіграна N разів за бій, отримує сильнішу форму (з 2023) |
| Річка | terrain | — | наземні не проходять, крім мостів |
| Міст | terrain | 2 | єдиний перехід для наземних; визначає смугу |
| Зона розстановки | zone | своя половина + розширення | де дозволено висаджувати війська/будівлі |
| Еліксир | resource | макс. 10, набігає з часом, ×2 / ×3 у кінці | валюта картки |
| Колода | zone | 8 карт | обирається між боями з колекції |
| Рука | zone | 4 карти | зіграна карта йде в кінець черги, звідти приходить наступна |
| Корона | resource | 1 за вежу (?) | рахунок матчу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `counter(elixir, <, 10)` → ТО `currency(+rate)`; КОЛИ `timer(last_minute)` → ТО `custom: «швидкість еліксиру ×2»`; КОЛИ `custom: «остання хвилина овертайму»` → ТО `custom: «швидкість еліксиру ×3»`.
- КОЛИ `input(drag, card, cell)` → ЯКЩО `has(elixir, cost)` and `custom: «клітина в зоні розстановки (для війська й будівлі)»` → ТО `currency(-cost)`, `place(card, cell)`, `custom: «карта йде в кінець черги, з черги в руку — наступна»`.
- КОЛИ `input(drag, spell, cell)` → ЯКЩО `has(elixir, cost)` → ТО `currency(-cost)`, `explode(radius, n)` (будь-де на арені).
- КОЛИ `spawned(troop)` → ТО `custom: «після короткої затримки висадки рушає до найближчої цілі своєї смуги»`.
- КОЛИ `in_range(troop, enemy, range)` → ЯКЩО `custom: «тип цілі підходить (земля/повітря/лише будівлі)»` → ТО `damage(n)` з `custom: «перезарядкою атаки»`.
- КОЛИ `custom: «наземний юніт дійшов до річки»` → ТО `custom: «іде до найближчого мосту»`; повітряний — `move(a, to)` напряму.
- КОЛИ `in_range(princess_tower, enemy, range)` → ЯКЩО `custom: «ворог на половині вежі»` → ТО `damage(n)`.
- КОЛИ `destroyed(princess_tower)` → ТО `custom: «King Tower прокидається»`, `counter(crowns, +1)`, `custom: «зона розстановки суперника розширюється на цю смугу»`.
- КОЛИ `custom: «King Tower отримала шкоду»` → ТО `custom: «King Tower прокидається»` (активація заздалегідь).
- КОЛИ `destroyed(king_tower)` → ТО `win` для суперника (усі вежі зараховано (?)).
- КОЛИ `timer(3 min)` → ЯКЩО `custom: «веж знесено не порівну»` → ТО `win` тому, хто зніс більше; інакше `custom: «овертайм: перша знесена вежа перемагає»`.
- КОЛИ `custom: «2 хв овертайму минули без знесеної вежі»` → ТО `custom: «перемагає той, у чиєї найслабшої вежі більше HP»` (тайбрейк за найменшим HP).
- КОЛИ `custom: «будівля-генератор»` → ТО `spawn_at(troop, building)` за `timer(every)` поки жива.
- КОЛИ `custom: «будівля прожила свій час»` → ТО `disappear_a` (?).
- КОЛИ `custom: «evolution: карту зіграно N разів»` → ТО `transform(card, evolved)`.
- КОЛИ `input(ability, champion)` → ЯКЩО `custom: «cooldown минув і є еліксир»` → ТО `custom: «активна здібність чемпіона»` (?).
- КОЛИ `level_end` → ТО `counter(trophies, ±n)`, `give(player, chest|reward)`.
- Перемога: знесена King Tower; або більше веж після 3 хв; або перша вежа в овертаймі; або тайбрейк за HP · Поразка — дзеркально · Рахунок: корони за вежі, трофеї за бій.

## Керування і ввід
- Тач: перетягнути карту з руки на арену (або тап по карті, тап по клітині (?)); під час перетягування видно зону дозволеної висадки і радіус заклинання.
- Нема прямого керування юнітом після висадки — лише вибір **що, де і коли**; тайминг висадки (позаду King Tower, на мосту) — основна майстерність.
- Емоції — колесо емоцій під час бою; Champion — кнопка здібності.

## Вікна, меню, HUD
- `main-menu` — нижні вкладки: магазин (`shop-window`), картки й колоди (`+window:deck-builder`), бій (кнопка Battle), клан (`+window:clan-window`), події/режими (`mode-select`).
- `+window:deck-builder` — колекція, кілька збережених колод по 8 карт, середня вартість еліксиру (?), рівні карток і апгрейд.
- `game-screen` — арена; рука з 4 карт, `+ui:next-card-preview`, `+ui:elixir-bar` з цифрою, `timer-countdown` (3:00 → овертайм), `+ui:crown-counter`, HP-смуги веж (`hp-bar`), `emote-wheel`, `threat-range` під час drag.
- `end-screen` — переможець, корони, ±трофеї, нагорода; далі `+window:chest-window` / розкриття нагород.
- `leaderboard` — ліги ranked (7 ліг до Ultimate Champion), клан; `lobby-window` — 2v2 з другом / випадковим.
- Draft: `choose` з двох карт кілька разів перед боєм; Clan Wars — 4 колоди без повторів карт.
- Переходи: `main-menu` → Battle → матчмейкінг → `game-screen` → `end-screen` → `main-menu`.

## Фічі поза полем
- `+feature:card-collection` — карти з нагород, магазину й запитів у клані; апгрейд копіями + валютою; рівень карти й King Level впливають на силу веж.
- Прогресія: трофеї ведуть по тематичних аренах, відкривають карти; ranked із сезонами; `+feature:battle-pass` (Pass Royale, з 2019); скрині з таймерами → з 2025 «lucky drop».
- Режими: 1v1 (trophy road), 2v2 кооп, Challenges (вхід за валюту, до 3 поразок), Draft, Clan Wars, Merge Tactics (автобатлер на 4, з 2025), тимчасові події.
- Клан: запити карт, клан-війни, чат (?).

## Варіації й родичі
- У сімʼї: [random-dice](random-dice.md) (PvP-ліги й колода), [legion-td](legion-td.md) (дві команди, смуги з королем), [mechabellum](mechabellum.md) (авто-бій юнітів після розстановки), [plants-vs-zombies](plants-vs-zombies.md) (смуги + валюта, що набігає), [teamfight-tactics](teamfight-tactics.md) — родич режиму Merge Tactics. Попередник — Clash of Clans (`build-sim/clash-of-clans-base.md`).
- **Осі варіацій**: смуги — 1 / 2 через мости / вільне поле · еліксир — сталий / прискорений у кінці · рука — черга-цикл / випадковий добір · зона висадки — фіксована / розширюється за знесену вежу · кінець — королівська вежа / більшість веж / тайбрейк за HP.

## Цікавинки для курсу
- Еліксир, що набігає з капом і прискоренням у кінці (×2, ×3) — 🌱.
- Рука як черга: зіграна карта йде в кінець, «наступна» видна наперед (deque з 8) — 🌱.
- Зона висадки, що розширюється від знесеної вежі (динамічна маска поля) — 📎.
- Юніт з типом цілі: земля/повітря/лише будівлі + вибір найближчої цілі по смузі — 🥉.
- Кінець матчу з трьох шарів: King Tower / більшість веж / овертайм «до першої» / тайбрейк за найменшим HP — 📎.
- Синхронний PvP у реальному часі з однаковою симуляцією на двох клієнтах — 🥇.

## Мапа на каталог
- Є: `round-currency` ↔ еліксир · `cursor-place` + `drag-drop-piece` ↔ висадка карти · `hp-damage` ↔ HP веж і юнітів · `tower-range` ↔ дальність веж · `melee-vs-ranged` · `explode-area` ↔ заклинання · `spawner-entity` ↔ будівлі-генератори · `timed-despawn` ↔ час життя будівлі · `chase-greedy` ↔ рух до найближчої цілі · `online-multiplayer` · `ai-opponent` (тренування) · `move-timer` ↔ 3 хв · `enemy-reached-base` ↔ атака веж · `status-effects` ↔ сповільнення, заморозка · `mode-select` · `match-setup` ↔ friendly battle · `lobby-window` ↔ 2v2 · `leaderboard` · `shop-window` · `tutorial-window` · `end-screen` · `popup-text`.
- **Нема** → пропозиції карток:
  - `+card-cycle-queue` «Рука з черги: зіграна — у кінець» · game-logic/economy · 🌱.
  - `+regen-currency` «Валюта набігає з часом з капом і множником фази» · game-logic/economy · 🌱.
  - `+two-lanes-bridges` «Поле з перешкодою й кількома переходами = смуги» · fields/topology · 📎.
  - `+placement-zone-expand` «Зона висадки змінюється від подій» · entities/legality · 📎.
  - `+king-tower-wake` «Ціль-ядро прокидається від шкоди або падіння сусіда» · entities/state · 🌱.
  - `+overtime-sudden-death` «Овертайм до першого очка» · game-logic/win · 🌱.
  - `+tiebreak-lowest-hp` «Тайбрейк за найслабшою вежею» · game-logic/win · 🌱.
  - `+card-levels` «Рівень карти з колекції впливає на статистику» · game-logic/progression · 📎.
  - `+draft-pick` «Драфт: 1 з 2 кілька разів перед боєм» · game-logic/setup · 🌱.
  - `+clan-card-request` «Запит ресурсу в учасників групи» · game-logic/social · 🥉.

## Пропозиції до словників
- `+role:card` · `+role:building` (стоїть, атакує або генерує, має час життя) · `+role:base` (ціль, падіння якої = кінець).
- `+trigger:card_played` · `+trigger:deploy_done` — юніт закінчив висадку й починає діяти.
- `+effect:draw` (добір наступної карти з черги) · `+effect:wake` (активувати сплячу сутність).
- `+cond:in_zone(cell, zone)` — клітина в дозволеній зоні · `+cond:target_type(a, b)` — B підходить під тип цілі A (земля/повітря/будівля).
- `+ui:elixir-bar` · `+ui:next-card-preview` · `+ui:crown-counter`.
- `+window:deck-builder` · `+window:chest-window` (розкриття нагород) · `+window:clan-window`.
- `+feature:card-collection` · `+feature:battle-pass`.
- `+axis:field=lanes` — поле з кількох смуг/переходів.

## Джерела
- ⭐ [Wikipedia: Clash Royale](https://en.wikipedia.org/wiki/Clash_Royale) — річка і два мости, King + 2 Princess Towers, активація King Tower, зона висадки й розширення, еліксир до 10 (×2 в останню хвилину, ×3 у кінці овертайму), колода 8 / рука 4, 3 хв, овертайм 2 хв, тайбрейк за HP, рідкості, Evolution, режими (2v2, Challenges, Draft, Clan Wars, Merge Tactics), Pass Royale, скрині → lucky drop.
- [YouTube: пошук](https://www.youtube.com/results?search_query=clash+royale+gameplay) — геймплей.

## Непевне
- (?) Сітка арени (18×32 клітини?), стартовий еліксир (5?) і швидкість (1 за 2,8 с?) — з памʼяті, не з відкритого джерела; fandom-вікі дала 402, офіційна підтримка — 403.
- (?) Корони: 1 за Princess Tower, 3 за King Tower — у Wikipedia не згадано.
- (?) Черга руки (зіграна карта повертається через 4 інші) — з пошукових сніпетів неофіційних гайдів, не з першоджерела; «наступна карта» видна в HUD — з памʼяті.
- (?) Час життя будівель, затримка висадки, кнопка здібності Champion і її cooldown — з памʼяті.
- (?) Клановий чат і колесо емоцій — у Wikipedia не описано.
