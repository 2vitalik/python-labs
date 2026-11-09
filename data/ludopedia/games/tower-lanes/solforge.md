---
title: SolForge
slug: solforge
aka: []
family: tower-lanes
also: []
klass: figure
axes:
  field: 1d
  time: turn
  opponent: online
  info: hidden
  random: runtime
  goal: state
year: 2016
platforms: [PC, macOS, Linux, iOS, Android]
links:
  - {kind: other, url: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/232450/manuals/SolForgeRulesV10.pdf", best: true, note: "офіційні правила v1.0 (PDF зі Steam): 5 карт у руці, зіграти 2, решта в скид; рівні карт; ранг аватара кожні 4 ходи з перетасуванням; 5 смуг × 2 ряди; фази ходу; кнопка Battle"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/SolForge", note: "Stone Blade, Garfield і Kibler, Kickstarter 2012, 120 HP, 2 карти за хід, 5 смуг, апгрейд зіграної карти, закриття 2019, фан-клієнт ReForged"}
  - {kind: steam, url: "https://store.steampowered.com/api/appdetails?appids=232450", note: "Steam 232450: реліз 25.07.2016, режими (турніри, драфт, рейтинг, кампанія, тижневі події), кування карт, крос-платформа"}
  - {kind: play, url: "https://grousewood-games.github.io/solforge/play/", note: "фан-реалізація Solforge — Mimicwurm: у браузері, Constructed/Draft проти бота або вдвох"}
  - {kind: other, url: "https://grousewood-games.github.io/solforge/docs/rules/creatures.html", note: "фан-доки: ключові слова й атрибути (Aggressive, Armor, Breakthrough, Defender, Mobility, Poison, Regenerate, Spawn, Consistent…)"}
  - {kind: other, url: "https://grousewood-games.github.io/solforge/docs/rules/battle.html", note: "фан-доки: сплячі/бадьорі істоти, наступ і оборона, порядок шкоди зліва направо"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=SolForge+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [drag-drop-piece, pocket, hp-damage, piece-capture, status-effects, ai-opponent, online-multiplayer, rating-system, hot-seat, mode-select, tutorial-window, message-log, +lane-grid, +deck-draw, +deck-builder, +card-collection, +card-keywords, +draft-mode, +rarity-copy-limit, +play-n-of-hand, +discard-unplayed, +card-level-up-on-play, +rank-reshuffle, +opposed-lane-combat, +retaliation, +summoning-sickness, +excess-damage-through, +lane-mobility, +spawn-random-empty-lane, +second-player-compensation]
proposes: ["+trigger:card_played", "+trigger:rank_up", "+effect:draw_card", "+effect:discard", "+effect:level_up_card", "+effect:shuffle_discard", "+cond:opposed", "+role:card", "+role:lane", "+ui:play-counter", "+ui:rank-orb", "+ui:battle-button", "+window:card-levels", "+window:deck-builder", "+window:draft-screen", "+card:card-level-up-on-play", "+card:rank-reshuffle", "+card:play-n-of-hand"]
author: opus
date: 2026-11-09
---

# SolForge — 5 смуг навпроти; з руки в 5 карт граєш дві, і кожна зіграна карта повертається в колоду сильнішою версією

## Суть
Цифрова картярка Stone Blade (Річард Гарфілд, Браян Кіблер), задумана як гра, неможлива на папері: **зіграна карта підвищує рівень** — її копія в колоді замінюється версією 2, потім 3. Щоходу гравець бере 5 карт і грає лише 2, решта йде в скид; кожні 4 ходи аватар підвищує ранг, скид перетасовується в колоду — і тепер звідти виходять прокачані карти. Поле — 5 смуг: істота бʼє істоту навпроти, а в порожній смузі — героя суперника.

## Поле і час
- Поле — 5 колонок-смуг × 2 ряди (свій і чужий) (`field: 1d`); у смузі на боці гравця — одна істота (за правилами v1.0 — ще й одна споруда).
- Хід: початок (істоти переходять у наступ, тригери «на початку ходу») → головна фаза в будь-якому порядку: зіграти 1-шу карту, 2-гу карту, натиснути Battle → кінець (ефекти «до кінця ходу» минають, скинути руку, підвищити ранг, якщо час, взяти 5 нових).
- Перший гравець у першому ході грає 1 карту.
- Ранг: кожні 4 ходи гравця; рахується лічильником ходів у ранзі.
- Приховане: рука й порядок колоди.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець (Forgeborn) | player | HP 100 (v1.0) / 120 (пізніше), ранг | ціль неперекритих атак |
| Істота | piece (`+role:card`) | рівень 1–3, атака, здоровʼя, ключові слова | «кується» в смугу; спершу спить, бʼється з наступного ходу |
| Закляття | object (`+role:card`) | рівень | ефект на ціль; потім рівень+1 у скид |
| Споруда | object (`+role:card`) | рівень | стоїть у смузі поруч з істотою (v1.0) |
| Смуга | zone (`+role:lane`) | 5 штук | одна істота на бік; бій лише навпроти |
| Колода · рука · скид | zone | колода 30, рука 5 | рука щоходу скидається; скид повертається в колоду на ранг |
| Ігри за хід | resource | 2 сині (звичайні) + зелені (безкоштовні для типу) | витрачаються на розіграш карти |
| Токен (Spawn) | piece | — | зʼявляється у випадковій порожній смузі |
| Фракції: Alloyin, Nekrium, Tempys, Uterra | — | колір | пул карт; у колоді — не більше двох |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «колода 30 перетасована, усі карти рівня 1»`, `custom: «взяти 5 карт»`.
- КОЛИ `turn_start(side)` → ТО `clear_state(creatures, asleep)` — свої істоти переходять у наступ; спрацьовують ефекти «на початку ходу».
- КОЛИ `turn_start(side)` → ЯКЩО `state(creature, poison)` → ТО `damage(creature, X)`; потім ЯКЩО `state(creature, regenerate)` → ТО `heal(creature, X)`.
- КОЛИ `input(play, creature, lane)` → ЯКЩО `counter(plays_left, >, 0)` → ТО `place(player, creature)`, `set_state(creature, asleep)`, `counter(plays_left, -1)`; якщо в смузі вже своя істота — `custom: «Replace: нова заміщує стару, стара не вважається загиблою»`.
- КОЛИ `custom: «карту зіграно»` → ТО `custom: «копія йде у скид рівнем вище (до 3)»`.
- КОЛИ `custom: «перший хід першого гравця»` → ТО `custom: «лише 1 гра»`.
- КОЛИ `input(battle)` → ЯКЩО `custom: «цього ходу Battle ще не натискали»` → ТО `custom: «бʼються всі істоти в наступі — свої й чужі»`.
- КОЛИ `custom: «бій у смузі»` → ЯКЩО `custom: «навпроти стоїть істота»` and `custom: «хоча б одна з двох у наступі»` → ТО `damage(each, other_atk)` одночасно; дві не-наступальні не бʼються.
- КОЛИ `custom: «бій у смузі»` → ЯКЩО `custom: «навпроти порожньо»` and `state(creature, offense)` → ТО `damage(enemy_player, atk)`; шкода героям — по смугах зліва направо.
- КОЛИ `custom: «Breakthrough-істота в наступі»` → ЯКЩО `custom: «шкода > здоровʼя суперника в смузі»` → ТО `damage(enemy_player, надлишок)`.
- КОЛИ `spawned(creature)` → ЯКЩО `state(creature, aggressive)` → ТО `clear_state(creature, asleep)` — бʼється й рухається вже цього ходу.
- КОЛИ `custom: «Defender-істота»` → ТО `custom: «ніколи не починає бій, лише відповідає»`.
- КОЛИ `custom: «Armor X: шкода за хід»` → ТО `custom: «перші X шкоди за хід поглинаються»`.
- КОЛИ `input(move, creature, lane)` → ЯКЩО `custom: «Mobility X, бадьора, свій хід, раз за хід»` and `free(lane)` and `custom: «≤ X смуг»` → ТО `move(creature, lane)`; ЯКЩО `custom: «має Flank»` → ТО `custom: «ефект»`.
- КОЛИ `custom: «Spawn»` → ТО `spawn_at(token, random_empty_lane)`; ЯКЩО `count(empty_lanes, ==, 0)` → ТО `custom: «нічого»`.
- КОЛИ `spawned(creature)` → ЯКЩО `custom: «зіграна з руки і має Forge»` → ТО `custom: «ефект Forge»`; Formation — ЯКЩО `custom: «стала між двома своїми»`; Assault — ЯКЩО `custom: «навпроти порожньо»`.
- КОЛИ `hp_zero(creature)` → ТО `disappear(creature)`; ЯКЩО `custom: «Vengeance»` → ТО `custom: «ефект»`.
- КОЛИ `turn_end(side)` → ТО `custom: «уся рука — у скид без підвищення рівня»`, `custom: «взяти 5 карт»`.
- КОЛИ `turn_end(side)` → ЯКЩО `counter(turns_in_rank, ==, 4)` → ТО `custom: «ранг +1, скид перетасовується в колоду, лічильник ходів рангу = 0»`.
- КОЛИ `custom: «карта Consistent»` → ТО `custom: «потрапляє в перші 20 карт колоди — вийде за 4 ходи рангу»`.
- КОЛИ `custom: «карта Overload зіграна»` → ТО `disappear(card)` — у скид не йде.
- КОЛИ `hp_zero(player)` → ТО `lose`; ЯКЩО `custom: «обидва нижче нуля одночасно»` → ТО `draw` (нічия).
- Збір колоди: рівно 30 карт, ≤ 2 фракції, ≤ 3 копії; драфт — без ліміту копій.
- Перемога: здоровʼя суперника до 0 · Поразка: своє до 0 · Нічия: обидва одночасно · Рахунок: рейтинг.

## Керування і ввід
- Миша/тач: вибрати карту в руці → вибрати смугу або ціль; перетягнути бадьору істоту з Mobility в іншу порожню смугу.
- Кнопка Battle — раз за хід, у будь-який момент (до, між чи після двох ігор): бій — частина рішень ходу.
- Правий клік / утримання — перегляд карти з усіма рівнями.
- Порожня гра (синя іконка) може піти на скидання карти (фан-клієнт) (?).

## Вікна, меню, HUD
- `main-menu` → `mode-select`: кампанія проти AI, рейтинг, драфт, турніри, тижневі події.
- `game-screen`: поле 5×2, рука з 5 карт, `+ui:play-counter` (сині/зелені іконки ігор), коло гравця з HP, `+ui:rank-orb` і лічильником ходів до рангу, стани (Armor, Poison) на колі, кнопки колоди й скиду з лічильниками, `+ui:battle-button`, `message-log`.
- `+window:card-levels` — картка на весь екран з перемиканням рівнів 1–3 і повʼязаних карт.
- `+window:deck-builder` (30 карт, 2 фракції); `+window:draft-screen` — пак з кількох карт, вибір однієї.
- `tutorial-window`, `end-screen`; фан-клієнт: налаштування бота (Metamind, Savant, Wurm) і пріоритетів AI.

## Фічі поза полем
- `card-collection`, бустери; кування карт (card forging) — лише згадка на Steam.
- `online-multiplayer` з крос-платформою, `rank-tiers`, турніри, тижневі події; `ai-opponent-levels`.
- Фан-життя: ReForged (2018), Solforge — Mimicwurm у браузері (Constructed/Draft, бот або `hotseat`), Kaelforge з онлайн-PvP.
- Офіційні сервери закрито в січні 2019; SolForge Fusion (Steam, 2024) — окрема гра з іншими правилами (?).

## Варіації й родичі
- Родичі в корпусі: [elder-scrolls-legends](elder-scrolls-legends.md) (2 смуги, руни), [mythgard](mythgard.md) (7 смуг), [inscryption](inscryption.md) (карти навпроти в колонках), [plants-vs-zombies-heroes](plants-vs-zombies-heroes.md), [riftforce](riftforce.md) (смуги-локації), [marvel-snap](marvel-snap.md).
- Поза корпусом: Dominion (рука скидається щоходу, колода цикл), Magic: the Gathering (каркас «істота проти істоти»).
- **Осі варіацій**: зростання карти — нема / за рівнем гравця (TESL) / **за кожен розіграш** · ресурс — мана / фіксована кількість ігор за хід · рука — зберігається / скидається щоходу · бій — атакуєш кожною / одна кнопка Battle для всіх, і чужих теж.

## Цікавинки для курсу
- Зіграна карта йде у скид рівнем вище, а скид повертається в колоду лише на ранг кожні 4 ходи — «темп прокачки» як модель колоди (deque + discard + reshuffle) — 🥉.
- 5 з руки → зіграти 2 → решту скинути: вибір і жертва щоходу — 🌱.
- Кнопка Battle раз за хід у будь-який момент, бʼються і свої, і чужі в наступі — 📎.
- Бій навпроти в смузі + шкода героєві з порожньої смуги, порядок зліва направо — 🌱.
- Mobility X: перестрибнути в порожню смугу до X позицій — 🌱.
- Consistent: гарантувати карту в перших 20 при перетасовці — 📎 (контрольований shuffle).

## Мапа на каталог
- Є: `drag-drop-piece` · `pocket` ↔ рука · `hp-damage` · `piece-capture` ↔ загибель істоти · `status-effects` ↔ Poison, Armor, сон · `ai-opponent`, `online-multiplayer`, `rating-system`, `hot-seat` (фан-клієнт) · `mode-select` · `tutorial-window` · `message-log` ↔ лог фан-клієнта.
- **Нема** → пропозиції карток:
  - `+lane-grid`, `+deck-draw`, `+deck-builder`, `+card-collection`, `+card-keywords`, `+draft-mode`, `+rarity-copy-limit`, `+retaliation`, `+second-player-compensation` — уже в корпусі.
  - `+card-level-up-on-play` «Зіграна карта повертається в колоду наступним рівнем» · game-logic/economy · 🥉.
  - `+rank-reshuffle` «Кожні N ходів скид перетасовується в колоду (ранг)» · game-logic/economy · 📎.
  - `+play-n-of-hand` «З руки в K карт зіграти лише N» · game-logic/legality · 🌱; `+discard-unplayed` «Незігране скидається в кінці ходу» · 🌱.
  - `+opposed-lane-combat` «Бій лише з фігурою навпроти, порожня смуга — удар по героєві» · entities/combat · 🌱.
  - `+summoning-sickness`, `+excess-damage-through` — як у TESL (ця пачка).
  - `+lane-mobility` «Перехід у порожню смугу до X позицій» · entities/move · 🌱; `+spawn-random-empty-lane` · entities/spawn · 🌱.

## Пропозиції до словників
- `+trigger:card_played` — повтор; `+trigger:rank_up(side)` — минуло N ходів рангу.
- `+effect:draw_card` · `+effect:discard` — повтори; `+effect:level_up_card(card)` — замінити копію карти наступним рівнем; `+effect:shuffle_discard` — повернути скид у колоду й перетасувати.
- `+cond:opposed(a)` — навпроти в смузі стоїть ворожа фігура.
- `+role:card` · `+role:lane` — повтори.
- `+ui:play-counter` — лічильник ігор за хід (звичайні/безкоштовні); `+ui:rank-orb` — ранг і ходи до наступного; `+ui:battle-button` — одна кнопка бою для всіх.
- `+window:card-levels` — перегляд рівнів карти; `+window:deck-builder`, `+window:draft-screen` — повтори.
- `+card:card-level-up-on-play`, `+card:rank-reshuffle`, `+card:play-n-of-hand`.

## Джерела
- ⭐ [SolForge Rules v1.0 (PDF, Steam)](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/232450/manuals/SolForgeRulesV10.pdf) — 100 HP, 5 карт / 2 гри, перший хід — 1 гра, скид руки, рівні карт і ранг аватара кожні 4 ходи, поле 5 смуг × 2 ряди, 1 істота + 1 споруда в смузі, фази ходу, кнопка Battle, нічия.
- [Wikipedia: SolForge](https://en.wikipedia.org/wiki/SolForge) — 120 HP, 2 карти за хід, 5 смуг, апгрейд, автори, Kickstarter, ранній доступ і реліз 31.05.2016, закриття 2017/2019, ReForged.
- [Steam appdetails 232450](https://store.steampowered.com/api/appdetails?appids=232450) — режими, кування карт, AI різної складності, крос-платформа.
- [Solforge — Mimicwurm: грати](https://grousewood-games.github.io/solforge/play/) і доки фан-реалізації: [огляд правил](https://grousewood-games.github.io/solforge/docs/rules/game-overview.html), [ключові слова](https://grousewood-games.github.io/solforge/docs/rules/creatures.html), [бій](https://grousewood-games.github.io/solforge/docs/rules/battle.html), [колода](https://grousewood-games.github.io/solforge/docs/rules/deck-rules.html), [фракції](https://grousewood-games.github.io/solforge/docs/rules/factions.html), [інтерфейс](https://grousewood-games.github.io/solforge/docs/rules/game-interface.html), [відмінності](https://grousewood-games.github.io/solforge/docs/faq/differences.html).
- YouTube: пошук «SolForge gameplay».

## Непевне
- (?) Стартове HP: 100 у правилах v1.0, 120 у Wikipedia й фан-доках — змінилось між версіями.
- (?) Споруди: правила v1.0 дозволяють 1 істоту + 1 споруду на смугу; фан-доки про споруди мовчать.
- (?) Максимальний рівень карти: «більшість має три рівні» — чи бували четверті, не перевірено.
- (?) Ліміт копій 3 і ≤ 2 фракції — з фан-доків (Mimicwurm), офіційний PDF їх не дає.
- (?) Кування карт (card forging) у колекції — лише згадка на Steam.
- (?) Скидання карти за «порожню гру» — з фан-клієнта, не з офіційних правил.
