---
title: Merge Tactics (Clash Royale)
slug: merge-tactics
aka: [Clash Royale Merge Tactics]
family: tower-lanes
also: [tactics]
klass: cursor
axes:
  field: hex
  time: realtime
  opponent: online
  info: partial
  random: runtime
  goal: survive
year: 2025
platforms: [iOS, Android]
links:
  - {kind: other, url: "https://supercell.com/en/games/clashroyale/blog/release-notes/merge-tactics-season-11-november-changes/", best: true, note: "офіційні нотатки сезону: еліксир за раунд, Quest Orbs, екіпірування, спільний пул копій, зірки 2–4, ротація модифікаторів за лігами"}
  - {kind: other, url: "https://supercell.com/en/games/clashroyale/blog/release-notes/merge-tactics-season-11-balance-changes/", note: "баланс: трейти з порогами (Boss, Undead, Clan, Rider), правителі з квестами, гекси як одиниця відстані"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Merge_Tactics", note: "Wikipedia (у статті про Clash Royale): постійний режим з липня 2025, 4 гравці, вибір і злиття юнітів, авто-бій"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=clash+royale+merge+tactics+guide", note: "пошук; гайди"}
stage: v1
coverage: 45
mechanics: [round-currency, shop-catalog, tile-merge, drag-drop-piece, hp-damage, melee-vs-ranged, status-effects, rule-variants, rating-system, online-multiplayer, +auto-battle, +bench-and-board, +star-up-merge, +trait-synergy, +shared-unit-pool, +item-combine, +ruler-quests, +league-modifiers, +special-tiles]
proposes: ["+trigger:phase_start", "+effect:place", "+effect:merge", "+window:ruler-select", "+ui:trait-tracker", "+feature:league-modifier-rotation", "+card:ruler-quests", "+card:league-modifiers"]
author: opus
date: 2026-11-09
---

# Merge Tactics — автобатлер Clash Royale на чотирьох: купуй карти за еліксир, зливай копії в зірки, збирай трейти, а бій іде сам

## Суть
Окремий режим [Clash Royale](clash-royale.md) (постійний з липня 2025), споріднений з [Teamfight Tactics](teamfight-tactics.md): четверо гравців щораунду отримують еліксир, купують юнітів зі спільного пулу, ставлять їх на свою половину гексового поля й дивляться автоматичний бій. Однакові юніти зливаються в сильнішу зірку, юніти зі спільним трейтом дають бонус команді. Тут описано лише відмінності режиму від TFT; карти Clash Royale (Knight, Valkyrie, P.E.K.K.A…) — це юніти.

## Поле і час
- Поле — гексова арена; відстані в правилах — у гексах (радіус страху Boss 1 гекс, розбиття щита 2 гекси).
- Раунд: фаза підготовки (купівля, розстановка, злиття) → авто-бій у реальному часі → еліксир за раунд.
- Спеціальні клітини-плитки в частині ліг: Damage Tile, Jump Tile, Invisible Tile, Wormhole Tile; трейт Rider бере бонус з «пробуджених» плиток.
- Суперник — один з трьох інших щораунду (?); програвший втрачає HP (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Юніт (війська) | ally | вартість 2–5 еліксиру, зірки, HP, damage, hit speed | авто-ціль і авто-атака в бою; власна здібність (Knight — Taunt, Dark Prince — стрибок) |
| Super-юніт | ally | у спільному пулі | посилена версія карти (Super Hog Rider, Super Dark Prince…) |
| Спільний пул | supply | копії за вартістю (2-ел. — 8, 3-ел. — 6) | вичерпується для всіх гравців разом |
| Трейт | zone | пороги 2/4/6 або 1/2/3/4 | Boss — +HP і страх; Undead — +HP/урон за полеглих союзників; Clan — швидкість атаки й лікування; Rider — бонуси з плиток |
| Правитель (Ruler) | player | квест з 3 цілей | Grand Warden, Tomb Queen, Dagger Duchess, Royale King, Spirit Empress — пасивка й квест |
| Quest Orb | pickup | рівень 1–3 | 1 — 3 еліксири + екіпірування або 2★ юніт; 2 — 6 еліксирів + …; 3 — +1 розмір команди і 3★ юніт |
| Екіпірування | pickup | пули Q1 / Q2 | на юніта: Prince's Lance, Valkyrie's Axe, Mage Wand (перетворює на кролика), Superstar Ring… |
| Розмір команди | — | ліміт на полі | +1 від Quest 3 |
| Будівлі (X-Bow, Inferno Tower, Goblin Cage, Elixir Collector) | tower | HP | ставляться як юніти; Goblin Cage «викрадає» ворога |
| Спецплитка | terrain | тип | шкодить / підкидає / ховає / телепортує (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(prep)` → ТО `currency(+5)` (5 еліксиру за раунд).
- КОЛИ `input(buy unit)` → ЯКЩО `has(player, cost)` → ТО `take(player, elixir)`, `place(unit, bench|board)`.
- КОЛИ `input(buy unit)` → ЯКЩО `same(new, owned, type and star)` → ТО `merge(a, b → star+1)` (?), до 4★.
- КОЛИ `counter(trait, >=, threshold)` → ТО `set_state(team, trait_bonus)`.
- КОЛИ `phase_start(battle)` → ТО `custom: «юніти автоматично ідуть до найближчої цілі й атакують»`.
- КОЛИ `died(ally)` → ЯКЩО `count(Undead, >=, tier)` → ТО `custom: «+1/3/5 % HP і урону живим Undead»`.
- КОЛИ `in_range(Boss, enemy, 1)` → ТО `custom: «страх на 0,5–3 с»`.
- КОЛИ `custom: «виконано ціль квесту правителя»` → ТО `give(player, quest_orb)`.
- КОЛИ `custom: «Superstar Ring»` → ТО `custom: «повтор здібності раз на старті бою»`.
- КОЛИ `all_gone(enemy units)` → ТО `custom: «раунд виграно»`; інакше `custom: «гравець отримує шкоду»` (?).
- КОЛИ `hp_zero(player)` → ТО `custom: «вибування, місце за порядком»` (?).
- Модифікатор ліги: КОЛИ `level_start` → ТО `custom: «правило сезону — Elixir Festival, Four Stars, First Free, Battle Royale…»`.
- Перемога: останній живий / високе місце (?) · Поразка: HP гравця 0 (?) · Рахунок: місце 1–4 → рейтинг ліги, Starsteel (?).

## Керування і ввід
- Тап по карті в магазині — купити; drag юніта на гекс поля — поставити; drag на інший гекс — переставити.
- Екіпірування — drag на юніта (?); квест і правитель — вибір на старті (?).

## Вікна, меню, HUD
- `ruler-select` (custom): вибір правителя перед партією (?).
- `game-screen`: гексова арена, лава (bench), магазин, `trait-tracker` (custom-ui: активні трейти з порогами), еліксир, портрети 4 гравців з HP.
- `end-screen`: місце, нагорода.
- `mode-select` в Clash Royale: Merge Tactics як окрема вкладка (?).

## Фічі поза полем
- Ліги Bronze I–III, Silver I–IV, Gold I–V, Diamond; кожна має 2 модифікатори, що ротуються щомісяця (`league-modifier-rotation`); `rank-tiers`.
- Сезони з балансом трейтів, правителів, юнітів і екіпірування; Starsteel-ресет (у сезоні 11 — нема).

## Варіації й родичі
- [teamfight-tactics](teamfight-tactics.md) — еталон жанру (8 гравців, XP, відсотки, карусель); [dota-auto-chess](dota-auto-chess.md); [hearthstone-battlegrounds](hearthstone-battlegrounds.md); [super-auto-pets](super-auto-pets.md).
- Rush Royale — Wikipedia порівнює з ним; [random-dice](random-dice.md).
- **Осі варіацій:** гравці (4 / 8) · економіка (фікс. еліксир / золото з відсотками) · прогресія сили (зірки злиттям / рівні) · мета-шар (правитель + квест / аугменти) · правила ліги (модифікатори).

## Цікавинки для курсу
- Спільний пул копій на 4 гравців (дефіцит) — 📎.
- Злиття однакових у зірку з каскадом (1+1 → 2★, 2★+2★ → 3★) — 📎.
- Трейти з порогами 2/4/6 як підрахунок за типами — 🌱.
- Авто-бій на гексах: пошук цілі, рух, атака з hit speed — 🥈.
- Правитель з квестом із трьох порогів → нагорода-орб — 📎.
- Модифікатори ліги як підміна правил (`rule-variants`) — 🥉.

## Мапа на каталог
- Є: `round-currency` · `shop-catalog` · `tile-merge` · `drag-drop-piece` · `hp-damage` · `melee-vs-ranged` · `status-effects` (страх) · `rule-variants` (модифікатори) · `rating-system` (ліги) · `online-multiplayer`.
- **Нема** → пропозиції карток:
  - `+auto-battle`, `+bench-and-board`, `+star-up-merge`, `+trait-synergy`, `+shared-unit-pool`, `+item-combine` — з TFT (підтвердження).
  - `+ruler-quests` «Персонаж-правитель із квестом-драбиною і нагородами» · game-logic/progression · 📎.
  - `+league-modifiers` «Кожна ліга грає з двома модифікаторами правил» · levels · 🥉.
  - `+special-tiles` «Плитки поля з ефектом у бою» · entities · 📎.

## Пропозиції до словників
- `+trigger:phase_start`, `+effect:place`, `+effect:merge` — уже в 🔥/коді, тут вжито.
- `+window:ruler-select`, `+ui:trait-tracker`, `+feature:league-modifier-rotation`.
- `+card:ruler-quests`, `+card:league-modifiers`.

## Джерела
- ⭐ [Supercell: Merge Tactics Season 11 (November Changes)](https://supercell.com/en/games/clashroyale/blog/release-notes/merge-tactics-season-11-november-changes/) — еліксир 5 за раунд, Quest Orbs, пул екіпірування, копії в пулі, Supers, модифікатори всіх ліг.
- [Supercell: Merge Tactics Season 11 Balance Changes](https://supercell.com/en/games/clashroyale/blog/release-notes/merge-tactics-season-11-balance-changes/) — трейти з порогами, правителі, юніти, екіпірування.
- [Wikipedia](https://en.wikipedia.org/wiki/Merge_Tactics) — постійний режим з липня 2025, 4 гравці, порівняння з Rush Royale.
- YouTube: пошук «clash royale merge tactics guide».

## Непевне
- (?) Механізм злиття (скільки копій на зірку), лава, HP гравця й шкода за поразку, вибування, нагороди за місце — fandom-вікі віддала 402, офіційні нотатки цього не пояснюють.
- (?) Як працюють спецплитки (Wormhole, Invisible) — відомі лише назви модифікаторів.
- (?) Вибір правителя на старті й вигляд HUD — з памʼяті/здогад.
