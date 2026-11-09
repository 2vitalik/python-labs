---
title: Schotten Totten / Battle Line
slug: schotten-totten
aka: [Battle Line, Schotten-Totten, Шоттен-Тоттен]
family: tower-lanes
also: [board-digital]
klass: cursor
axes:
  field: 1d
  time: turn
  opponent: hotseat
  info: hidden
  random: runtime
  goal: territory
year: 1999
platforms: [board]
links:
  - {kind: other, url: "https://rulespal.com/schotten-totten/rulebook", best: true, note: "повні правила: 54 карти 6×(1–9), 9 каменів, рука 6, 5 комбінацій, ранній захват з доказом, тайбрейк, тактичний і експертний варіанти, усі 10 тактик"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Schotten_Totten", note: "Knizia, 1999; «девʼять паралельних покерних рук»; Battle Line (GMT, 2000) — карти 1–10; перевидання 2004 з 10 тактиками"}
  - {kind: other, url: "https://rulespal.com/battle-line/rulebook", note: "Battle Line: 60 карт 6×(1–10), рука 7, формації Wedge/Phalanx/Battalion/Skirmish/Host, Fog/Mud, Scout/Redeploy/Deserter/Traitor, рахунок серії партій"}
  - {kind: other, url: "https://www.ultraboardgames.com/battle-line/game-rules.php", note: "Battle Line: порядок ходу (карта → захват → добір), нічия програє тому, хто клав останню карту, вичерпана колода"}
  - {kind: other, url: "https://rulespal.com/schotten-totten-2/rulebook", note: "Schotten Totten 2: асиметрична облога, 7 секцій стіни з вимогами, котли смоли, відступ"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Schotten+Totten+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 70
mechanics: [hot-seat, turn-enforcement, pocket, pass-turn, game-screen, end-screen, help-window, rule-variants, ai-opponent, +lane-grid, +deck-draw, +hand-limit, +poker-hand-eval, +wild-card, +location-control, +tiebreak-chain, +n-or-adjacent-win, +proof-claim, +location-modifiers, +card-relocate, +steal-card, +play-limit-vs-opponent, +match-series-score, +asymmetric-sides]
proposes: ["+effect:draw_card", "+effect:discard", "+trigger:claim", "+cond:formation_beats", "+cond:unbeatable", "+role:card", "+ui:stone-row", "+ui:tactic-counter", "+window:claim-proof", "+card:proof-claim", "+card:n-or-adjacent-win"]
author: opus
date: 2026-11-09
---

# Schotten Totten / Battle Line — девʼять покерних трійок у ряд: виклади карти біля каменів і забери 5 каменів або 3 поспіль

## Суть
Карткова дуель Райнера Кніції: між гравцями в ряд лежать 9 каменів кордону (у Battle Line — прапорів), біля кожного каменя кожен викладає зі свого боку до трьох карт. Трійки порівнюють як покерні руки — колір-ряд, трійка, колір, ряд, сума; сильніша трійка забирає камінь. Хто першим візьме 5 будь-яких каменів або 3 сусідні — виграв. Ядро гри — **ранній захват**: камінь можна забрати ще до того, як суперник доклав свої карти, якщо довести за відкритими картами, що його трійка вже не може перемогти.

## Поле і час
- Поле — лінія з 9 каменів (`field: 1d`); у кожного каменя дві сторони по 3 слоти — смуга з двома «окопами». Суміжність лінійна: важлива лише для умови «3 поспіль».
- Захоплений камінь переїжджає на бік власника; більше карт туди не кладуть навіть у неповну трійку, тактики на нього не діють.
- Хід почерговий: зіграти 1 карту → добрати → заявити захвати (Schotten Totten); у Battle Line — карта → захвати → добір до 7.
- Інформація: руки й колоди приховані, викладені карти відкриті; випадковість — порядок колоди (добір під час гри).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Камінь кордону ×9 (Battle Line: прапор) | zone | стан: вільний / мій / суперника; 3 слоти на бік (Mud — 4) | приймає карти, доки вільний; забраний — замикається |
| Карта клану (ST: 54 = 6 кольорів × 1–9) | tile (`+role:card`) | колір, сила | кладеться в слот свого боку, не рухається (крім тактик) |
| Карта війська (BL: 60 = 6 кольорів × 1–10) | tile | колір, сила (10 — слони … 1 — застрільники) | як карта клану |
| Рука | supply | ST 6 карт; тактичний варіант і BL — 7 | після ходу поповнюється |
| Колода кланів / військ | supply | лицем донизу | добір; порожня — добору нема, гра триває |
| Колода тактик (варіант / BL) | supply | 10 карт | можна добирати замість звичайної |
| Joker ×2 (BL: Alexander, Darius — Leaders) | tile | колір і сила — будь-які, обираються при захваті | не більше одного на боці гравця; другий застрягає в руці до кінця |
| Spy (BL: Companion Cavalry) | tile | сила 7 (BL: 8), колір обирається при захваті | елітний загін |
| Shield-Bearer (BL: Shield Bearers) | tile | сила 1–3, колір — на вибір при захваті | елітний загін |
| Blind-Man's Bluff (BL: Fog) | zone | модифікатор, кладеться на камінь | комбінації вимкнено — лише сума сил |
| Mud Fight (BL: Mud) | zone | модифікатор, кладеться на камінь | на цьому камені потрібно 4 карти з кожного боку |
| Recruiter (BL: Scout) | — (хитрість) | одноразова | добери 3 з будь-яких колод, поверни 2 з руки (ST — під низ, BL — лицем донизу зверху) |
| Strategist (BL: Redeploy) | — (хитрість) | одноразова | перенеси свою карту з вільного каменя на інший вільний або скинь |
| Banshee (BL: Deserter) | — (хитрість) | одноразова | скинь карту суперника з вільного каменя |
| Traitor | — (хитрість) | одноразова | перенеси карту клану суперника з вільного каменя на свій бік вільного каменя |
| Відбій хитрощів | supply | відкритий, переглядається будь-коли | куди йдуть зіграні хитрощі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(play_card, stone)` → ЯКЩО `count(my_cards_at_stone, <, 3)` and `not state(stone, claimed)` → ТО `place(player, card)`; інакше `block`.
- КОЛИ `after(place)` → ЯКЩО `count(deck, >, 0)` → ТО `custom: «draw_card: 1 карта клану (ST); добрати до 7 з колоди на вибір (варіант, BL)»`; інакше `custom: «добору нема, гра триває»`.
- КОЛИ `no_moves(player)` → ЯКЩО `custom: «у руці лише тактики або всі мої слоти повні»` → ТО `pass_turn` або зіграти тактику.
- КОЛИ `input(claim, stone)` → ЯКЩО `custom: «по 3 карти з обох боків і моя трійка сильніша»` → ТО `set_side(stone, me)`.
- КОЛИ `input(claim, stone)` → ЯКЩО `custom: «моя трійка повна, у суперника < 3 карт і жодне доповнення з невидимих карт (усі карти − викладені на столі) її не бʼє»` → ТО `set_side(stone, me)` (ранній захват); рука заявника як доказ не рахується, тактики в руках не заважають.
- Сила трійки: `custom: «колір-ряд > трійка однакових > колір > ряд > сума»`; порядок викладання для ряду неважливий; той самий тип → більша сума сил.
- КОЛИ `custom: «тип і сума рівні»` → ТО `custom: «ST: камінь бере той, хто першим доклав третю карту; BL: прапор програє той, хто клав (або клав би) останню карту»`.
- КОЛИ `counter(my_stones, >=, 5)` → ТО `win`.
- КОЛИ `pattern(line(3))` (три сусідні мої камені) → ТО `win`.
- Тактики: КОЛИ `input(play_tactic)` → ЯКЩО `custom: «моїх зіграних тактик > тактик суперника»` → ТО `block`; інакше `place(player, tactic)` або ефект хитрощу.
- КОЛИ `input(play_joker)` → ЯКЩО `occupied(my_side, joker)` → ТО `block`.
- КОЛИ `input(claim, stone)` → ЯКЩО `state(stone, blind_mans_bluff)` → ТО `custom: «порівняти лише суми сил»`.
- КОЛИ `input(claim, stone)` → ЯКЩО `state(stone, mud_fight)` → ТО `custom: «потрібні 4 карти з кожного боку»`.
- КОЛИ `input(claim, stone)` → ЯКЩО `custom: «на моєму боці wild-карта»` → ТО `set_value(wild, найвигідніше: колір і сила)`.
- КОЛИ `input(recruiter)` → ТО `custom: «draw_card ×3 з будь-яких колод»`, `custom: «повернути 2 карти з руки в колоди»`.
- КОЛИ `input(strategist, my_card)` → ЯКЩО `not state(stone, claimed)` → ТО `move(my_card, other_free_stone)` або `custom: «discard»`.
- КОЛИ `input(banshee, enemy_card)` → ЯКЩО `not state(stone, claimed)` → ТО `custom: «discard карти суперника»`.
- КОЛИ `input(traitor, enemy_clan_card)` → ЯКЩО `not state(stone, claimed)` and `free(my_slot_at_free_stone)` → ТО `set_side(card, me)`, `move(card, my_slot)`.
- Експертний варіант: КОЛИ `turn_start(player)` → ТО заявити захвати; пізніше за хід — `block` (суперник має хід, щоб відповісти тактикою).
- Серія партій: КОЛИ `custom: «партію виграно»` → ТО `score(+5)` переможцю, `score(+1 за кожен свій камінь)` тому, хто програв; переможець починає наступну (BL).
- Перемога: 5 каменів або 3 сусідні · Поразка: суперник зробив це першим · Рахунок: лише в серії партій.

## Керування і ввід
- Хід: вибрати карту з руки → вибрати камінь (свій бік) → добір (у BL і варіанті — з якої колоди).
- Захват — окрема заява з доказом: показати, що суперник не може побити (цифрова версія — кнопка «забрати» біля каменя, перевірка автоматична).
- Wild-карти (Joker, Spy, Shield-Bearer) — значення обирається не при викладанні, а при захваті.

## Вікна, меню, HUD
- (цифрова версія) `main-menu` → `match-setup`: варіант (базовий / тактичний / експертний), Schotten Totten чи Battle Line, кількість партій у серії.
- `game-screen`: `+ui:stone-row` — 9 каменів у ряд, біля кожного по 3 слоти з двох боків; `pocket` — рука (6–7 карт); лічильники колод (`remaining-counter`); `+ui:tactic-counter` — скільки тактик зіграв кожен; відбій хитрощів; позначка власника на забраних каменях; `turn-indicator`.
- `+window:claim-proof` (цифрова версія) — підтвердження раннього захвату: яка найкраща трійка суперника ще можлива.
- `pass-device` — гра на одному пристрої з прихованими руками.
- `end-screen`: хто виграв і як (5 каменів / 3 поспіль), очки серії; `help-window` — таблиця комбінацій.

## Фічі поза полем
- `custom-rules` / `rule-variants`: базова гра, тактичний варіант (+10 тактик, рука 7), експертний (захват лише на початку ходу); Battle Line — інша колода (1–10) і завжди з тактиками.
- `hotseat` (настілка); серія партій з рахунком 5 / 1 за камінь.
- (цифрова версія) `ai-opponent-levels`, `rules-page`.

## Варіації й родичі
- **Battle Line** (GMT, 2000) — та сама гра з античною тематикою: карти 1–10, рука 7, формації Wedge / Phalanx / Battalion Order / Skirmish Line / Host, тактики з іншими назвами (Fog, Mud, Scout, Redeploy, Deserter, Traitor).
- **Schotten Totten 2** (облога): гравці асиметричні — нападник і захисник; 7 секцій стіни, на кожній своя вимога (тип комбінації і макс. кількість карт); нападник виграє, пошкодивши 4 секції або пошкоджену двічі; захисник — якщо нападник мусить добирати з порожньої колоди; у захисника 3 котли смоли (скинути найближчу карту нападника), у нападника — відступ (скинути свої карти з секцій).
- Родичі в корпусі: [riftforce](riftforce.md) (5 локацій у ряд, але карти бʼються й мають HP), [marvel-snap](marvel-snap.md) (3 локації, сума сили), [queens-blood](queens-blood.md) (сума по рядах), [knucklebones](knucklebones.md) (комбінації однакових у стовпці), [gwent](gwent.md) (сума в рядах за раунд).
- **Осі варіацій**: як вирішується смуга — покерна трійка / сума / бій із HP · коли вирішується — коли обидва повні / доведено достроково / на кінець раунду · умова перемоги — більшість смуг / N з M або K поспіль / очки · модифікатори смуги — нема / Fog-Mud / ефекти локацій (Marvel Snap).

## Цікавинки для курсу
- Оцінка трійки: тип комбінації (5 рівнів) + сума + тайбрейк «хто першим доклав» — 🌱 (класична функція `rank(hand)`).
- Ранній захват із доказом: перебрати всі доповнення суперника з невидимих карт (повна колода − викладені на столі) і перевірити, що жодне не бʼє — 🥉 (комбінаторний перебір; з wild-картами і Mud — 🥈).
- Перемога «5 з 9 або 3 поспіль» — 🌱; разом із дилемою «де віддати камінь» — гарне поле для AI.
- Wild-карти з відкладеним вибором значення (максимізація на момент захвату) — 📎.
- Ліміт тактик «не більше, ніж у суперника + 1» — 🌱.
- Модифікатори каменя (лише сума / 4 карти) — правило, що змінює функцію порівняння локально — 📎.
- AI з прихованою рукою: Monte Carlo розкладів невидимих карт (determinization) — 🥇.

## Мапа на каталог
- Є: `hot-seat` + `turn-enforcement` ↔ почерговий хід; `pocket` ↔ рука; `pass-turn` ↔ пас без військових карт; `rule-variants` ↔ базовий/тактичний/експертний; `ai-opponent` (цифрова версія); `game-screen`, `end-screen`, `help-window`.
- Уже в корпусі як `+`: `+lane-grid`, `+deck-draw`, `+hand-limit`, `+poker-hand-eval`, `+wild-card`, `+location-control`, `+tiebreak-chain`, `+location-modifiers`, `+asymmetric-sides` (ST2).
- **Нема** → пропозиції карток:
  - `+proof-claim` «Достроковий захват з доказом неперемоги суперника» · game-logic/win · 🥉 · слот {proof: visible_cards_only}.
  - `+n-or-adjacent-win` «Перемога: N будь-яких або K сусідніх зон» · game-logic/win · 🌱 · слоти {n: 5, k: 3}.
  - `+card-relocate` «Перенести свою карту між зонами або скинути» · entities/interact · 🌱.
  - `+steal-card` «Забрати карту суперника на свій бік» · entities/interact · 📎.
  - `+play-limit-vs-opponent` «Не більше спецкарт, ніж у суперника + 1» · game-logic/opponent · 🌱.
  - `+match-series-score` «Серія партій: переможцю 5, переможеному — за кожну зону» · game-logic/score · 🌱.

## Пропозиції до словників
- `+effect:draw_card` — добрати карту з колоди (уже пропоноване Riftforce); `+effect:discard` — скинути карту зі столу у відбій.
- `+trigger:claim` — гравець заявляє захват зони (окремий крок ходу, не `input` дії на полі).
- `+cond:formation_beats` — трійка А сильніша за трійку Б за таблицею комбінацій; `+cond:unbeatable` — жодне можливе доповнення суперника з невидимих карт не бʼє.
- `+role:card` — карта як сутність на полі (сила, колір), повтор із сімʼї.
- `+ui:stone-row` — ряд зон зі слотами з двох боків; `+ui:tactic-counter` — лічильник зіграних спецкарт кожного гравця.
- `+window:claim-proof` — підтвердження/пояснення дострокового захвату.
- `+card:proof-claim`, `+card:n-or-adjacent-win`.

## Джерела
- ⭐ [RulesPal: Schotten Totten](https://rulespal.com/schotten-totten/rulebook) — склад, хід, 5 комбінацій, ранній захват лише за викладеними картами, тайбрейк, перемога 5/3 поспіль, серія партій, тактичний і експертний варіанти з описом усіх 10 тактик.
- [Wikipedia: Schotten Totten](https://en.wikipedia.org/wiki/Schotten_Totten) — Knizia 1999, видавці, Battle Line 2000 (1–10, інша рука, тактики), перевидання 2004.
- [RulesPal: Battle Line](https://rulespal.com/battle-line/rulebook) — 60 карт, назви сил, формації, захват і тайбрейк, ліміт тактик, Fog/Mud/Scout/Redeploy/Deserter/Traitor, рахунок серії, Advanced Variant.
- [UltraBoardGames: Battle Line](https://www.ultraboardgames.com/battle-line/game-rules.php) — порядок ходу, рука 7, вичерпана колода, пас, Leaders.
- [RulesPal: Schotten Totten 2](https://rulespal.com/schotten-totten-2/rulebook) — облога: ролі, 7 секцій, умови перемоги, котли, відступ.
- YouTube: пошук «Schotten Totten how to play».

## Непевне
- (?) Цифрові версії (застосунки, BGA) — не перевірено; вікна й AI описано як «цифрова версія».
- (?) Чи в Schotten Totten захват дозволено до добору чи лише після — RulesPal ставить захват після добору; для доказу це неважливо (рука не рахується).
- (?) Точний склад і ролі тактик у перевиданнях різних років можуть відрізнятися назвами (Banshee ↔ Deserter тощо).
- (?) Деталі Schotten Totten 2 (вимоги кожної секції стіни, умова «захисник не може зіграти») — лише за коротким переказом RulesPal.
