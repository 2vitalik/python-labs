---
title: Flamme Rouge
slug: flamme-rouge
aka: [Фламм Руж, Червоний прапор]
family: board-digital
also: []
klass: figure
axes:
  field: 1d
  time: wego
  opponent: hotseat
  info: partial
  random: runtime
  goal: race
year: 2016
platforms: [board]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/flamme-rouge/game-rules.php", best: true, note: "базові правила: 3 фази, 2 смуги, рух від переднього, слипстрім, втома"}
  - {kind: other, url: "https://cs.uwaterloo.ca/~dtompkin/archive/dtlib/base/Flamme%20Rouge.pdf", note: "PDF правил Lautapelit.fi 2016 (дзеркало): склад, траса, фази, приклади зграй, гори, гандикап, 6 етапів"}
  - {kind: other, url: "https://www.ultraboardgames.com/flamme-rouge/additional-rules.php", note: "гори (підйом ≤5, спуск ≥5), гандикап, альтернативні етапи"}
  - {kind: other, url: "https://www.ultraboardgames.com/flamme-rouge/peloton.php", note: "доповнення Peloton: бруківка, зони постачання, відрив на 5–6, боти Peloton і Muscle, соло"}
  - {kind: other, url: "https://rulespal.com/flamme-rouge/rulebook", note: "склад: 21 тайл траси, 120 енергокарт, 60 карт втоми"}
  - {kind: other, url: "https://rules.dized.com/flamme-rouge/rule/components/energy-and-exhaustion-cards", note: "по 15 карт на вершника, 30 + 30 карт втоми"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Flamme+Rouge+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 70
mechanics: [hot-seat, rule-variants, ai-opponent, difficulty-levels, level-select, game-screen, end-screen, help-window, editor-window, movement-animation, +deck-draw, +draw-4-play-1, +card-recycle-bottom, +simultaneous-hidden-orders, +two-lane-track, +frontmost-first-resolution, +blocked-square-stop-behind, +slipstream-pack, +exhaustion-junk-card, +movement-cap-terrain, +movement-floor-terrain, +modular-track, +finish-furthest-tiebreak, +handicap-setup, +bot-team-deck, +breakaway-bid]
proposes: ["+effect:draw_cards", "+effect:recycle", "+trigger:deck_empty", "+cond:gap_ahead", "+ui:card-hand", "+ui:deck-counter", "+ui:recycled-pile", "+card:slipstream-pack", "+card:exhaustion-junk-card", "+card:movement-cap-terrain"]
author: opus
date: 2026-11-09
---

# Flamme Rouge — велогонка на дві смуги: тягни 4 карти, грай 1, ховайся в зграї, а за порожньою клітиною попереду отримуй втому

## Суть
Кожен гравець веде команду з двох вершників — руле (Rouleur) і спринтера (Sprinteur), — у кожного своя колода енергокарт. Щораунду всі одночасно тягнуть 4 карти для вершника, потай грають одну (на стільки клітин він проїде), а решту кладуть у низ колоди; зіграна карта зникає з гри. Після руху працює **слипстрім**: зграя, від якої до наступної рівно одна порожня клітина, підтягується вперед. Вершник із порожньою клітиною перед собою отримує карту втоми — «сміттєву» двійку в колоду.

## Поле і час
- Траса — лінійна послідовність клітин (`1d`), кожна з 2 смугами (ліва/права); вершник займає смугу, на порожню клітину стає в праву. Повна клітина — 2 вершники.
- Трасу збирають з 21 двобічного тайла (старт, фініш, 7 прямих, 6 мʼяких і 6 крутих поворотів) за рядком літер на карті етапу; 6 запропонованих етапів + власні.
- Типи клітин: звичайна, підйом (червоний), спуск (синій); у Peloton — бруківка (1 смуга) і зона постачання (3 смуги).
- Раунд (`wego`): фаза енергії (усі одночасно, потай) → фаза руху (розкриття, рух від переднього) → кінцева фаза (зіграні карти з гри, слипстрім, втома).
- Інформація часткова: відкриті карти в низу своєї колоди видно власнику, зіграні карти суперників — лише після розкриття.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Руле | piece | колода 15 енергокарт | рухається на значення зіграної карти |
| Спринтер | piece | колода 15 енергокарт | так само; колода з малими й великим значенням |
| Енергокарта | object | значення = клітин руху | зіграна — з гри назавжди; незіграні — відкритими в низ колоди |
| Карта втоми | object | значення 2; 30 для руле + 30 для спринтерів | дається за порожню клітину попереду; іде в низ колоди відкритою |
| Клітина траси | terrain | 2 смуги | ≤2 вершники; порожня → права смуга; зміна смуги безкоштовна |
| Підйом | terrain | червоний | рух ≤5 для того, хто стартує, заїжджає чи перетинає; на ньому ні дає, ні отримує слипстрім |
| Спуск | terrain | синій | старт ходу на спуску → рух щонайменше 5 |
| Бруківка (Peloton) | terrain | 1 смуга | без слипстріму до і від |
| Зона постачання (Peloton) | terrain | 3 смуги | старт ходу в зоні → рух щонайменше 4 |
| Старт / фініш | static | жовті тайли | за лінією фінішу — кінець |
| Зграя | zone | вершники без порожніх клітин між ними | одиниця слипстріму |
| Карта етапу | mark | 6 етапів | рядок літер — порядок і боки тайлів |
| Дошка гравця | supply | місця колод і зіграних карт | закриті / відкриті частини колоди |
| Команда Peloton (бот) | enemy | обидва вершники + колода руле + 2 «Attack!» | одна відкрита карта рухає обох; «Attack!»: передній 2, задній 9; без втоми |
| Команда Muscle (бот) | enemy | обидві колоди + карта Muscle у спринтера | верхня карта кожної колоди; без втоми |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(energy)` → ТО для обраного вершника `custom: «тягнути 4 карти з його колоди»` (`+effect:draw_cards`), `choose(1)` → `custom: «покласти закритою біля колоди»`, решту `custom: «відкритими в низ колоди»` (`+effect:recycle`); потім так само для другого вершника — не раніше.
- КОЛИ `custom: «закриті карти колоди скінчились»` (`+trigger:deck_empty`) → ТО `custom: «перетасувати відкриті й покласти закритими»`; ЯКЩО `custom: «у колоді менше 4 карт»` → ТО `custom: «тягнути всі»`.
- КОЛИ `phase_start(movement)` → ТО `reveal(played_cards)`; вершники рухаються від найпереднішого (ближчий до фінішу; на рівній клітині права смуга попереду): `move(rider, +card_value)` — рівно на значення.
- КОЛИ `custom: «кінцева клітина руху повна»` → ЯКЩО `count(rider_on_cell, ==, 2)` → ТО `custom: «стати на першу клітину позаду з вільною смугою»`; проїжджати крізь вершників можна.
- КОЛИ `enter(rider, cell)` → ЯКЩО `free(cell)` → ТО `custom: «права смуга»`.
- КОЛИ `custom: «рух починається на підйомі, заходить на нього чи перетинає»` → ТО `custom: «рух = min(значення, 5), надлишок пропадає»`; ЯКЩО `custom: «6-й і далі крок зайшов би на перший підйом»` → ТО `custom: «зупинитись на останній вільній смузі перед підйомом»`.
- КОЛИ `turn_start(rider)` → ЯКЩО `cell(rider, descent)` → ТО `custom: «рух = max(значення, 5)»`.
- КОЛИ `turn_start(rider)` → ЯКЩО `cell(rider, supply_zone)` (Peloton) → ТО `custom: «рух = max(значення, 4)»`.
- КОЛИ `phase_start(end)` → ТО `disappear(played_cards)` — кожна карта грається один раз за гонку.
- КОЛИ `phase_start(end)` → ТО від задньої зграї до передньої: ЯКЩО `custom: «між зграєю і наступною попереду рівно 1 порожня клітина»` (`+cond:gap_ahead`) і `not cell(pack, ascent)` і `not cell(pack, cobblestone)` → ТО `move(pack, +1)`; злита зграя перевіряється далі, тож вершник може отримати слипстрім кілька разів за раунд.
- КОЛИ `after(slipstream)` → ЯКЩО `free(cell_ahead)` (уся клітина; порожня смуга не рахується) → ТО `give(rider_deck, exhaustion_card)` → `custom: «відкритою в низ колоди»`.
- КОЛИ `reach(rider, finish)` → ТО `custom: «раунд доходить до кінця; з кількох фінішерів перемагає той, хто заїхав далі за лінію»`, `win`.
- Гандикап: КОЛИ `level_start` → ЯКЩО `custom: «гравець уже грав»` → ТО `give(both_decks, exhaustion_card)` (дуже досвідчений — ще одну).
- Peloton-бот: КОЛИ `phase_start(movement)` → ТО `custom: «після розкриття людей відкрити 1 карту колоди пелотону; обидва вершники рухаються на неї; "Attack!" — передній 2, задній 9»`.
- Muscle-бот: КОЛИ `phase_start(movement)` → ТО `custom: «відкрити верхню карту кожної колоди й рухати відповідного вершника»`.
- Відрив (5–6 гравців, Peloton): КОЛИ `level_start` → ТО `custom: «2 раунди ставок: кожен вершник грає 1 з 4 закритою; двоє з найбільшою сумою — у відрив, найвища ставка — права смуга, нічия — задньому»`, `give(breakaway_rider, exhaustion_card ×2)`.
- Соло (Peloton): КОЛИ `level_start` → ЯКЩО `mode(solo)` → ТО `custom: «одна команда Peloton + одна Muscle; гравець починає з 3 картами втоми»`.
- Перемога: перший вершник за фінішем (при кількох — найдальший) · Поразка: — · Рахунок: нема.

## Керування і ввід
- Настільна: одночасно — взяти 4 карти обраного вершника, покласти одну закритою, решту в низ; повторити для другого; далі всі рухи — механічно за правилами.
- Вибір смуги — під час руху (безкоштовно); порядок вибору вершника в фазі енергії (кого першим) — рішення гравця.
- (цифрова версія) Тап по вершнику → рука з 4 карт → вибір; кнопка «Готово»; у hot-seat — завіса між гравцями; рух, слипстрім і втома — анімацією з поясненням.

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Гонка · Соло · Редактор траси · Правила.
- `match-setup`: 2–4 гравці (Peloton: до 6), кольори, боти Peloton/Muscle, гандикап, вибір етапу.
- `level-select`: 6 етапів (карти етапів) + власні траси.
- `editor-window`: траса з двобічних тайлів (прямі, мʼякі й круті повороти, підйоми/спуски) у рядок літер.
- `game-screen`: траса зі скролом/зумом, вершники на смугах; `deck-counter` закритих карт кожного вершника, `recycled-pile` (видно власнику), слоти зіграних карт; `card-hand` з 4 карт у фазі енергії; маркери зграй, стрілки слипстріму й іконки втоми в кінцевій фазі; `turn-indicator` фази.
- `end-screen`: порядок фінішу, переможець.
- `help-window`: картка-памʼятка 3 фаз (у коробці — 4 памʼятки).
- Переходи: main-menu → match-setup → level-select → game-screen → end-screen.

## Фічі поза полем
- `level-editor`: власні траси з тайлів; 6 готових етапів.
- `custom-difficulty` / гандикап картами втоми; `ai-opponent-levels` — боти Peloton і Muscle; соло з ботами.
- `hotseat` / одночасна гра 2–4 (Peloton — 5–6 з відривом).
- Доповнення (лише назви): Peloton, Meteo, Grand Tour, Team Trial.

## Варіації й родичі
- Peloton: бруківка, зони постачання, бонусний тайл, відрив, боти; рекорд дизайнера в соло — 6.
- **Осі варіацій**: рух (кубик / карта з руки / карта з колоди «тягни 4, грай 1») · ресурс (одноразові карти / рецикл) · бонус групи (слипстрім при розриві рівно 1 / нема) · штраф (втома в колоду / мінус енергії) · ландшафт (стеля руху на підйомі / підлога на спуску / зміна ширини смуг).
- Родичі: Heat: Pedal to the Metal (автоперегони; за пошуком Wikipedia, стаття про Heat згадує Flamme Rouge), RoboRally (`roborally.md`, одночасні закриті ходи), Galaxy Trucker (`galaxy-trucker.md`, перегони на треку).

## Цікавинки для курсу
- Колода з рециклом: тягни 4, грай 1, решту в низ відкритими, зіграна — з гри, перетасування лише відкритих — 📎.
- Розвʼязання руху: від переднього до заднього, 2 смуги, «повна клітина → перша позаду з вільною смугою», права смуга як тай-брейк позиції — 📎.
- Слипстрім: розбити вершників на зграї (компоненти без порожніх клітин), зсунути задню при розриві рівно 1, перевіряти каскадом від хвоста — 🥉.
- Втома як «сміттєва» карта, що розбавляє колоду (зворотне до deck-thinning) — 🌱.
- Ландшафт як модифікатор значення: стеля 5 на підйомі із зупинкою перед ним, підлога 5 на спуску, 4 у зоні постачання — 📎.
- Боти Peloton/Muscle як автомати на власних колодах — 📎.
- Порадник «яку карту зіграти»: Монте-Карло по решті колоди й можливим ходам суперників — 🥈.
- Траса з двобічних тайлів за рядком літер: рендер прямих і поворотів зі збереженням нумерації клітин — 🥉.

## Мапа на каталог
- Є: `hot-seat` · `rule-variants` ↔ гори, бруківка, відрив · `ai-opponent` ↔ боти · `difficulty-levels` ↔ гандикап · `level-select` ↔ етапи · `editor-window` ↔ власні траси · `movement-animation` · `game-screen`, `end-screen`, `help-window`.
- **Нема** → пропозиції карток:
  - `+slipstream-pack` «Слипстрім: зграя підтягується через розрив 1» · entities/move · 🥉 · слоти {gap: 1, blocked_on: [ascent, cobble]}.
  - `+exhaustion-junk-card` «Штраф — сміттєва карта в колоду» · game-logic/economy · 🌱 · слоти {value: 2}.
  - `+movement-cap-terrain` / `+movement-floor-terrain` «Клітина обмежує рух зверху / знизу» · entities/legality · 📎 · слоти {cap: 5, floor: 5|4}.
  - `+draw-4-play-1` / `+card-recycle-bottom` «Тягни N, грай 1, решту в низ відкритими» · game-logic/economy · 📎.
  - `+two-lane-track` · `+frontmost-first-resolution` · `+blocked-square-stop-behind` · `+finish-furthest-tiebreak` · `+modular-track` · `+bot-team-deck` · `+breakaway-bid` — одним рядком кожна, див. «Цікавинки».
  - `+deck-draw`, `+simultaneous-hidden-orders`, `+handicap-setup` — уже пропоновані корпусом.

## Пропозиції до словників
- `+effect:draw_cards(deck, n)` — тягнути N карт з колоди (`draw` у словнику — нічия, тому інше імʼя).
- `+effect:recycle(cards)` — покласти відкритими в низ колоди.
- `+trigger:deck_empty(deck)` — закриті карти скінчились (тасування відкритих).
- `+cond:gap_ahead(a, n)` — попереду рівно N порожніх клітин (слипстрім, втома при n ≥ 1).
- `+ui:card-hand` — рука з N карт; `+ui:deck-counter` — лишок закритих карт; `+ui:recycled-pile` — відкрита частина колоди, видима власнику.
- `+card:slipstream-pack` · `+card:exhaustion-junk-card` · `+card:movement-cap-terrain` — див. «Мапа на каталог».

## Джерела
- ⭐ [UltraBoardGames: Flamme Rouge rules](https://www.ultraboardgames.com/flamme-rouge/game-rules.php) — компоненти, підготовка, 3 фази, смуги, рух від переднього, слипстрім, втома = 2.
- [Правила Lautapelit.fi 2016 (PDF, дзеркало)](https://cs.uwaterloo.ca/~dtompkin/archive/dtlib/base/Flamme%20Rouge.pdf) — оригінальний буклет: 21 тайл, 120 + 60 карт, старт-розстановка, приклад зграй, «порожня смуга не дає втоми», гори, гандикап, 6 етапів; дизайнер Asger Sams Granerud.
- [UltraBoardGames: Additional rules](https://www.ultraboardgames.com/flamme-rouge/additional-rules.php) — підйоми/спуски, гандикап, альтернативні етапи.
- [UltraBoardGames: Peloton](https://www.ultraboardgames.com/flamme-rouge/peloton.php) — бруківка, зони постачання, відрив, боти Peloton і Muscle, соло.
- [RulesPal: Flamme Rouge rulebook](https://rulespal.com/flamme-rouge/rulebook) і [Dized: energy and exhaustion cards](https://rules.dized.com/flamme-rouge/rule/components/energy-and-exhaustion-cards) — склад колод (по 15 на вершника), список доповнень.
- YouTube: пошук «Flamme Rouge how to play».

## Непевне
- (?) Значення енергокарт: руле — 3, 4, 5, 6, 7 по 3 штуки, спринтер — 2, 3, 4, 5, 9 по 3 штуки — з памʼяті; у текстах правил значення лише на картинках.
- (?) Правила доповнень Meteo, Grand Tour, Team Trial і багатоетапної гонки — не відкривав.
- (?) Чи порядок «передній — права смуга» діє й у фазі слипстріму всередині зграї — не сказано.
- (?) Цифрової версії не перевірено; вікна гіпотетичні. Звʼязок з Heat — лише за сніпетом пошуку Wikipedia, сторінку Heat не відкривав.
- (?) `goal: race` і `time: wego` — тлумачення: фази енергії одночасні й закриті, рух — розвʼязання.
