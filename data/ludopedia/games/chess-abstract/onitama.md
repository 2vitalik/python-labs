---
title: Onitama
slug: onitama
family: chess-abstract
also: [board-digital]
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: setup
  goal: state
year: 2014
platforms: [board, Android, iOS, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Onitama", best: true, note: "правила, обмін картами, дві умови перемоги, доповнення"}
  - {kind: official, url: "https://www.arcanewonders.com/game/onitama/", note: "Arcane Wonders: короткі правила, склад коробки"}
  - {kind: official, url: "https://www.arcanewonders.com/wp-content/uploads/2021/05/Onitama-Rulebook.pdf", note: "офіційна книжка правил (PDF; не вдалося прочитати — завеликий)"}
  - {kind: wiki, url: "https://de.wikipedia.org/wiki/Onitama", note: "DE: перший гравець за позначкою на карті, пас картою без ходу"}
  - {kind: play, url: "https://en.boardgamearena.com/gamepanel?game=onitama", note: "Board Game Arena — грати в браузері, 2 гравці"}
  - {kind: other, url: "https://www.androidpolice.com/2018/02/28/strategy-board-game-onitama-gets-asmodee-digital-release/", note: "цифрова версія Asmodee Digital 2018: AI, онлайн, pass-and-play"}
  - {kind: other, url: "https://boardgamegeek.com/boardgame/160477/onitama", note: "BGG (403 для фетча)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=onitama+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 80
mechanics: [piece-move-patterns, piece-capture, reach-exit, no-moves-left, hot-seat, turn-enforcement, ai-opponent, ai-minimax, legal-move-highlight, cell-click, drag-drop-piece, game-screen, main-menu, end-screen, help-window, theme-select, +move-cards, +card-rotation, +capture-leader-win, +pass-turn, +card-deck-select]
proposes: ["+role:card", "+trigger:card_played", "+cond:card_allows", "+effect:rotate_card", "+window:deck-select", "+ui:card-hand", "+ui:next-card-slot", "+feature:card-sets", "+card:move-cards", "+card:capture-leader-win"]
author: opus
date: 2026-11-02
---

# Onitama — шахи 5×5, де ходи фігур задають карти, а зіграна карта йде супернику

## Суть
Два майстри бойових мистецтв з учнями на полі 5×5. Фігури не мають власних патернів: як ходити, вирішують **карти руху** (5 із 16 на партію), по дві в руці кожного і одна «в дорозі». Зіграна карта переходить супернику — тож кожен хід дає йому твій прийом через хід. Перемога — взяти майстра суперника або завести свого майстра в його храм.

## Поле і час
- Квадратне поле 5×5 (килимок). Центральна клітина заднього ряду кожної сторони — **Храм** (Temple Arch).
- Шар поля — лише фігури; клітини без властивостей, крім двох храмів.
- Покроково, хід = одна карта + один рух однієї фігури. Повна інформація: усі 5 карт відкриті, видно і свої, і чужі, і ту, що прийде.
- Випадковість лише в підготовці: 5 карт навмання з колоди 16.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Майстер | piece | сторона, 1 на гравця | ходить за картою; взяття = поразка його сторони; у ворожому храмі — перемога |
| Учень | piece | сторона, 4 на гравця | ходить за картою, бʼє ворожі фігури |
| Храм | zone | сторона | старт майстра; ціль ворожого майстра |
| Карта руху | card ⏳ | ім'я, 1–4 вектори ходу, колір-позначка першого гравця | дозволяє ходи-вектори відносно гравця; після гри — повертається на 180° і йде супернику |
| Рука гравця | zone | 2 карти | з неї обирається карта ходу |
| Слот «наступна карта» | zone | 1 карта | карта, яку отримає гравець, що щойно сходив |

Колода (16): Tiger, Dragon, Frog, Rabbit, Crab, Elephant, Goose, Rooster, Monkey, Mantis, Horse, Ox, Crane, Boar, Eel, Cobra (?) — назви з памʼяті; на офіційній сторінці згадані Dragon, Horse, Cobra.

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО 5 випадкових карт: по 2 кожному, 5-та — у слот; `custom: «перший ходить гравець, чий колір позначено на 5-й карті»`.
- КОЛИ `input(play, card, piece, cell)` → ЯКЩО `turn_of(side)` і `has(side, card)` і `custom: «cell = piece + вектор із card (у системі координат гравця)»` і `not occupied(cell, own_piece)` і `custom: «cell у межах поля»` → ТО `move(piece, cell)`.
- Проміжні клітини не перевіряються: фігури «перестрибують» усе на шляху (вектор — телепорт у ціль).
- КОЛИ `move` → ЯКЩО `occupied(cell, enemy_piece)` → ТО `disappear_b` (взяття).
- КОЛИ `after(move)` → ТО `rotate(card, 180)`, `give(opponent_slot, card)`, `custom: «гравець забирає карту зі свого слоту в руку»` — 2 карти в руці відновлено.
- КОЛИ `turn_start(side)` → ЯКЩО `no_moves(side)` → ТО `custom: «обрати карту і віддати її без ходу»` (пас картою; ходити обовʼязково, якщо можна).
- КОЛИ `contact(piece, enemy_master)` → ТО `win` («Шлях каменю»).
- КОЛИ `enter(own_master, enemy_temple)` → ТО `win` («Шлях потоку»).
- Перемога: взяти ворожого майстра або поставити свого на ворожий храм · Поразка: навпаки · Рахунок: нема (партія — так/ні).

## Керування і ввід
- Настільна: обрати одну з 2 своїх карт, пересунути фігуру, покласти карту праворуч від суперника, забрати свою зі слоту.
- (цифрова версія) Тап на карту → підсвітка фігур, які можуть нею сходити → тап/drag фігури на підсвічену клітину; карта анімовано летить у слот суперника.
- Черга строго чергується; паса за бажанням нема.

## Вікна, меню, HUD
- `main-menu` (цифрова версія Asmodee): гра проти AI, гра вдвох на одному пристрої, онлайн, навчання, магазин колод і тем.
- `tutorial-window` — коротке навчання правил на старті.
- `game-screen`: поле 5×5, `card-hand` свого гравця (2 карти з сіткою векторів), 2 карти суперника (перевернуті), `next-card-slot`, `turn-indicator`, `legal-move-highlight` для обраної карти, `selection-highlight`.
- `lobby-window` — онлайн-суперник (потрібен акаунт Asmodee).
- `shop-window` — Harmony Bundle / колода Sensei's Path / теми фігур.
- `skin-select` — теми фігур і поля.
- `end-screen`: «Шлях каменю» / «Шлях потоку», переможець, реванш.
- (цифрова версія) `deck-select` — які набори карт у колоді (база / Sensei's Path).
- Переходи: main-menu → (режим) game-screen → end-screen → реванш / main-menu.

## Фічі поза полем
- `hotseat` (pass-and-play), `online-multiplayer` (акаунт Asmodee), гра проти AI (рівні — (?)).
- `tutorial`, `rules-page`.
- `custom-rules`: склад колоди (16 базових + 16 Sensei's Path); free-to-play з обмеженою колодою, повна — покупкою.
- `theme-select` — теми фігур.
- BGA — браузерна гра на двох з таблицею рейтингу (?).

## Варіації й родичі
- Sensei's Path — 16 нових карт; Way of the Wind — нейтральний дух вітру, яким можуть ходити обидва: блокує рух, не може бути зміщений; на учня — міняється з ним місцями замість взяття; Light and Shadow (2021) — фігура «ніндзя» (?) з прихованою позицією.
- Родичі: шахи й шогі (взяття заходом, фігури з патернами), Hive і Santorini (абстракти на малому полі); «ходи з карт» як ідея — шахові варіанти з картами (?).
- Осі варіацій: **звідки патерн ходу** (у фігури / у карті / у кубика) · **що з картою після ходу** (суперникові / у скид / назад собі) · **умови перемоги** (взяти лідера / дійти до точки / обидва) · **нейтральні фігури** (нема / вітер).

## Цікавинки для курсу
- Ходи як дані: карта = список векторів, що дзеркалиться для другого гравця — 🥉 (поворот 180° = інверсія вектора, гарне завдання на системи координат).
- Ротація карт: 5 карт ходять по колу між двома гравцями — 📎 (черга з трьох слотів).
- Дві умови перемоги одночасно (лідер / храм) — 🌱.
- Пас картою без ходу — 🌱, але легко забути при генерації ходів.
- AI minimax: розгалуження мале (≤ 2 карти × 5 фігур × 4 вектори = 40), повна інформація — 🥇 класичний «перший серйозний» minimax з альфа-бета.
- Нейтральна фігура «вітер», якою ходять обидва (Way of the Wind) — 🥉.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ вектори з карти · `piece-capture` ↔ взяття заходом · `reach-exit` ↔ майстер у ворожому храмі · `no-moves-left` ↔ пас картою · `hot-seat` + `turn-enforcement` · `ai-opponent` / `ai-minimax` · `legal-move-highlight` + `cell-click` + `drag-drop-piece` · `game-screen`, `main-menu`, `end-screen`, `help-window` · `theme-select`.
- **Нема** → пропозиції карток:
  - `+move-cards` «Карти ходів» · entities/legality · 🥉 · слот {cards_in_play: 5, deck: 16} — патерн ходу береться з карти, не з фігури.
  - `+card-rotation` «Ротація карт між гравцями» · game-logic/opponent · 📎 — зіграна карта переходить супернику через слот.
  - `+capture-leader-win` «Взяти лідера» · game-logic/win · 🌱 — перемога знищенням особливої фігури (спрощений `checkmate`).
  - `+pass-turn` «Пас без ходів» · game-logic/opponent · 🌱 — тут з побічним ефектом (віддати карту).
  - `+card-deck-select` «Вибір складу колоди» · interface/settings · 🌱.

## Пропозиції до словників
- `+role:card` — карта як сутність гри поза полем (рука, слот, колода): має патерн/ефект, переходить між гравцями.
- `+trigger:card_played` — гравець зіграв карту (окремо від `input`, бо запускає ротацію).
- `+cond:card_allows` — хід відповідає вектору з обраної карти (з урахуванням орієнтації гравця).
- `+effect:rotate_card` — повернути карту/патерн на 180° (дзеркалення векторів) — можна звести до `rotate(a, deg)`.
- `+window:deck-select` — вибір наборів карт перед партією.
- `+ui:card-hand` — рука карт із міні-схемою ходу; `+ui:next-card-slot` — карта, що прийде наступною.
- `+feature:card-sets` — підключення наборів-доповнень як налаштування правил.
- `+card:move-cards`, `+card:capture-leader-win` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Onitama](https://en.wikipedia.org/wiki/Onitama) — поле, фігури, ротація карт, дві умови перемоги, доповнення, цифрова версія 2018.
- [Arcane Wonders: Onitama](https://www.arcanewonders.com/game/onitama/) — офіційний опис правил і склад коробки (16 карт).
- [Rulebook PDF](https://www.arcanewonders.com/wp-content/uploads/2021/05/Onitama-Rulebook.pdf) — офіційні правила з діаграмами карт (лінк бачив, PDF не прочитав).
- [Wikipedia DE: Onitama](https://de.wikipedia.org/wiki/Onitama) — перший гравець за кольором на 5-й карті, поворот карти на 180°, пас картою.
- [Board Game Arena: Onitama](https://en.boardgamearena.com/gamepanel?game=onitama) — грати онлайн.
- [Android Police](https://www.androidpolice.com/2018/02/28/strategy-board-game-onitama-gets-asmodee-digital-release/) — цифрова версія: free-to-play, AI, онлайн з акаунтом Asmodee, pass-and-play, навчання, Sensei's Path і теми покупкою.
- YouTube: пошук «onitama how to play».

## Непевне
- (?) Список 16 назв карт і їхні вектори — з памʼяті (офіційно підтверджені лише Dragon, Horse, Cobra).
- (?) Рівні складності AI у цифровій версії і платформа iOS — стаття згадує лише Android і «гру проти AI».
- (?) Light and Shadow: «ніндзя» з прихованою позицією — Wikipedia каже лише «нова фігура Ninja».
- (?) Рейтингова таблиця на BGA для Onitama — не перевірено.
