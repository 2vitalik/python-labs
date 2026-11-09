---
title: Trike
slug: trike
aka: [Трайк]
family: chess-abstract
also: []
klass: figure
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: score
year: 2020
platforms: [board, web]
links:
  - {kind: other, url: "https://ludii.games/details.php?keyword=Trike", best: true, note: "Ludii: трикутне поле з гексів, нейтральна пішка, «постав камінь на лінії видимості й перенеси пішку», підрахунок довкола пішки, Alek Erickson"}
  - {kind: play, url: "https://www.boardspace.net/english/about_trike.html", note: "BoardSpace: онлайн і роботи («неможливо обіграти, коли видно ендшпіль»)"}
  - {kind: other, url: "https://www.boardspace.net/trike/english/rules.html", note: "BoardSpace: правила — поле будь-якого розміру, перший хід, pie rule, кінець і перемога"}
  - {kind: other, url: "https://rulespal.com/trike/rulebook", note: "правила роздрібного видання: 30+30 дисків, двобічне поле, host/guest вибір кольору, нічиїх нема"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Trike+abstract+game+Alek+Erickson", note: "пошук; партії"}
stage: v1
coverage: 75
mechanics: [cursor-place, cell-click, hover-highlight, legal-move-highlight, last-move-highlight, no-moves-left, hot-seat, turn-enforcement, ai-opponent, ai-minimax, online-multiplayer, field-size-picker, move-notation, replay, game-screen, main-menu, end-screen, help-window, settings-window, state-as-data, unit-tests, +hex-grid-render, +shared-neutral-piece, +swap-rule, +adjacency-score, +place-in-sight, +trap-end-scoring, +no-draw-parity]
proposes: ["+role:shared-piece", "+cond:in_line", "+window:swap-dialog", "+ui:score-preview", "+card:place-in-sight", "+card:trap-end-scoring", "+card:no-draw-parity"]
author: opus
date: 2026-11-09
---

# Trike — обидва водять одну пішку: став камінь на її прямій і переносиш її туди; хто більше має довкола затиснутої пішки — той виграв

## Суть
Поле — трикутник із шестикутних клітин; на ньому одна нічия пішка. Хід: обрати порожню клітину на будь-якій з 6 прямих від пішки (без перескоків), поставити туди камінь свого кольору і перенести пішку на нього. Позаду пішки лишається слід із каменів, простір звужується; коли пішці нікуди йти, рахують камені кожного **під пішкою і довкола неї** — більше має переможець. Гра — про те, щоб завести спільну фігуру у «свою пастку» і зруйнувати пастки суперника.

## Поле і час
- Трикутне поле з гексів (`field: hex`): кутова клітина має 2 сусіди, крайова — 4, внутрішня — 6. Розмір — будь-який (BoardSpace); у роздрібному виданні поле двобічне, два розміри (?).
- Шари: клітина (порожня / камінь білий / камінь чорний) + пішка зверху.
- Пішка рухається як ферзь на гекс-сітці: будь-яка кількість порожніх клітин по одній з 6 прямих; зайнята клітина зупиняє промінь.
- Покроково, двоє, пасу нема. Партія 15–30 хв (RulesPal).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пішка (pawn) | piece | ×1, без власника | після кожного ходу стоїть на щойно поставленому камені; її промені визначають легальні ходи |
| Камінь | piece | колір white / black (blue); ×30 у кожного в роздрібному виданні | ставиться назавжди; не рухається й не знімається; блокує промені пішки |
| Запас каменів | supply | у кожного свій | джерело каменів для `place` |
| Клітина | terrain | гекс; 2 / 4 / 6 сусідів | порожня або з каменем |
| Сусідство пішки | zone | клітина пішки + її сусіди | у фіналі — зона підрахунку |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО поле порожнє; `turn_start(first)` → `input(cell)` → ТО `place(stone, cell)` будь-де, `place(pawn, cell)` зверху.
- КОЛИ `turn_start(second)` → ЯКЩО `first_time` → ТО `choose(swap | move)`: swap — забрати позицію суперника собі (pie rule, `window(swap-dialog)`); у роздрібному виданні: host ставить білий камінь із пішкою, guest обирає колір, ходить синій.
- КОЛИ `input(cell)` → ЯКЩО `free(cell)` і `custom: «cell на одній з 6 прямих від пішки, усі клітини між ними порожні»` (`+cond:in_line`) → ТО `place(stone_own, cell)`, `move(pawn, cell)`, `end_turn`.
- КОЛИ `input(cell)` → ЯКЩО `occupied(cell, stone)` або `custom: «між пішкою і cell є камінь»` → ТО `block` — перескоків нема.
- КОЛИ `input(pass)` → ТО `block` — пасувати не можна.
- КОЛИ `turn_start(side)` → ЯКЩО `no_moves(pawn)` — усі сусідні клітини зайняті або поза полем → ТО `game_over`.
- КОЛИ `game_over` → ТО кожному `score(adjacent_count(pawn, own_stone, …) + custom: «1, якщо камінь під пішкою свій»)`.
- КОЛИ `after(score)` → ЯКЩО `custom: «мій рахунок більший»` → ТО `win`; інакше `lose`.
- Нічиєї нема: у зоні підрахунку завжди непарна кількість каменів (кут 2+1, край 4+1, середина 6+1) — `draw` неможливий.
- Перемога: більше своїх каменів під пішкою і довкола неї, коли вона затиснута · Поразка: менше · Рахунок: 3 / 5 / 7 каменів у зоні ділиться між двома.

## Керування і ввід
- Настільна: поставити диск свого кольору на клітину й переставити на нього пішку.
- (цифрова версія) Клік по клітині — одна дія: камінь + перенесення пішки. Підсвічені всі клітини на 6 променях до першого каменя (`legal-move-highlight`); наведення показує, як зміниться рахунок довкола пішки, якби вона застрягла там (`score-preview`).
- Першому ходу другого гравця — діалог «Обміняти сторони?».

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Грати → `match-setup` (розмір поля, людина / робот, хто ходить першим) · Правила → `help-window` · `settings-window`.
- `swap-dialog` — pie rule на другому ході.
- `game-screen`: трикутне гекс-поле; пішка; `legal-move-highlight` (промені); `last-move-highlight`; `turn-indicator`; `score-preview` поточного «якби кінець зараз»; `move-list`.
- `end-screen`: зона підрахунку підсвічена, рахунок кожного; реванш.
- Переходи: main-menu → match-setup → game-screen ⇄ swap-dialog → end-screen.

## Фічі поза полем
- `online-multiplayer` і `ai-opponent-levels` (BoardSpace; Ludii).
- `field-size-picker` — поле «будь-якого розміру» (BoardSpace) / двобічне поле (роздрібне видання).
- `swap-rule` (pie rule) як баланс першого ходу.
- `replay` / `move-notation` — архіви партій BoardSpace (?).

## Варіації й родичі
- Автор — Alek Erickson (квітень 2020, видання Kanare Abstract — за результатами пошуку). Спільнотний варіант TrikeHex — те саме на полі-гексагоні (згадано в пошуку, правил не бачив).
- Спільна нейтральна фігура: [neutron](neutron.md), [l-game](l-game.md), [gyges](gyges.md), [tumbleweed](tumbleweed.md) (теж «камінь на лінії видимості»), [phutball](phutball.md), [paper-soccer](paper-soccer.md).
- Хід «постав на промені і перенеси фігуру» — родич стріли в [amazons](amazons.md) (там промінь ферзя ставить блок, а фігура лишається).
- Трикутне поле з гексів і «нічиєї нема» — як у грі Y і [hex](hex.md).
- **Осі варіацій**: хто рухає фігуру (власник / обидва — Trike) · що лишається на шляху (нічого / блок / свій камінь) · кінець (нема ходів у когось / фігура затиснута) · підрахунок (уся дошка / лише довкола фігури).

## Цікавинки для курсу
- Гекс-поле у формі трикутника: координати, 6 променів, межі — 🥉.
- Легальні ходи = клітини на 6 променях до першої перешкоди; хід = `place` + перенесення пішки — 🌱.
- Кінець гри і підрахунок у сусідстві пішки; доказ «нічиєї нема» через парність (2/4/6 сусідів + 1) — 📎.
- Pie rule як діалог на другому ході — 🌱.
- AI: ендшпіль розвʼязується повним перебором (робот BoardSpace «неможливо обіграти, коли видно ендшпіль») — 🥇; MCTS для дебюту — 🥇.

## Мапа на каталог
- Є: `cursor-place` ↔ камінь на вільну клітину з перевіркою легальності · `cell-click`, `hover-highlight`, `legal-move-highlight`, `last-move-highlight` · `no-moves-left` ↔ пішка затиснута (кінець гри, не поразка) · `hot-seat`, `turn-enforcement` · `ai-opponent`, `ai-minimax` · `online-multiplayer` · `field-size-picker` · `move-notation`, `replay` · `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window` · `state-as-data`, `unit-tests`.
- **Нема** → пропозиції карток:
  - `+hex-grid-render` (див. [hex](hex.md)), `+shared-neutral-piece` (див. [neutron](neutron.md)), `+swap-rule` (див. [hex](hex.md)), `+adjacency-score` «Очки за типи сусідів» (див. [islanders](../build-sim/islanders.md)).
  - `+place-in-sight` «Хід: постав свій камінь на промені від спільної фігури й перенеси її туди» · entities/legality · 📎 · слоти {dirs: 6, jump: false}.
  - `+trap-end-scoring` «Кінець — фігура затиснута; рахунок у її сусідстві» · game-logic/score · 🌱.
  - `+no-draw-parity` «Нічиєї нема через непарну зону підрахунку» · game-logic/score · 🌱 — дизайнерський прийом, варто показати доведенням.

## Пропозиції до словників
- `+role:shared-piece` — фігура без сторони, яку рухають обидва (пішка Trike, нейтрон).
- `+cond:in_line` — клітина на прямій від сутності без перешкод між ними (як `line_of_sight`, але для порожньої клітини-цілі).
- `+window:swap-dialog` — пропозиція обміну сторонами після першого ходу.
- `+ui:score-preview` — рахунок «якби гра скінчилась тут» при наведенні.
- `+card:place-in-sight`, `+card:trap-end-scoring`, `+card:no-draw-parity` — див. «Мапа на каталог».

## Джерела
- ⭐ [Ludii: Trike](https://ludii.games/details.php?keyword=Trike) — «equilateral triangular hexagon-tessellated grid», нейтральна пішка, пас заборонено, ставиш камінь у точку призначення і переносиш пішку, підрахунок «adjacent to, or underneath», автор Alek Erickson.
- [BoardSpace: правила Trike](https://www.boardspace.net/trike/english/rules.html) — поле будь-якого розміру, перший хід (камінь + пішка будь-де), pie rule, кінець — пішка не рухається, перемога — більше каменів під і довкола.
- [BoardSpace: about Trike](https://www.boardspace.net/english/about_trike.html) — онлайн, роботи.
- [RulesPal: Trike](https://rulespal.com/trike/rulebook) — роздрібне видання: 1 пішка, 30 білих + 30 синіх дисків, двобічне поле, host/guest, «Draws cannot occur», 15–30 хв.

## Непевне
- (?) Рік 2020, видавець Kanare Abstract, художник Kanare Kato — лише зі зведення результатів пошуку, сторінок не відкривав.
- (?) Розміри полів (скільки клітин на стороні; що на двох боках роздрібного поля) — у джерелах не названо.
- (?) Пояснення «нічиєї нема» парністю (2/4/6 сусідів + клітина пішки) — мій висновок; RulesPal лише стверджує «Draws cannot occur», Erickson казав, що трикутне поле гарантує відсутність нічиїх.
- (?) Камінь під пішкою — завжди останній поставлений; за Ludii він рахується («underneath»), тобто останній хід дає +1 тому, хто ходив — наслідок механіки, у джерелах не підкреслено.
- (?) Варіант TrikeHex і метаправило підрахунку Erickson — лише згадки в результатах пошуку.
