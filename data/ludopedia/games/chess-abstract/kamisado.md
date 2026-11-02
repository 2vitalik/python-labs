---
title: Kamisado
slug: kamisado
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: race
year: 2008
platforms: [board]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/kamisado/game-rules.php", best: true, note: "повні правила раунду: колір клітини → вежа суперника, блок, дедлок, матчі"}
  - {kind: other, url: "https://www.ultraboardgames.com/kamisado/standard-match-game-rules.php", note: "Sumo: хід до 5, Sumo push, заповнення зліва/справа, очки"}
  - {kind: other, url: "https://www.ultraboardgames.com/kamisado/long-match-game-rules.php", note: "Double Sumo: хід до 3, штовхає 1–2"}
  - {kind: other, url: "https://www.ultraboardgames.com/kamisado/marathon-match-game-rules.php", note: "Triple Sumo: хід на 1, штовхає до 3"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Kamisado", note: "Peter Burley, 2008; матчі 3/7/15; перемога першого за 17 ходів"}
  - {kind: official, url: "https://www.burleygames.com/", note: "Burley Games — видавець (Classic, Pocket, Max)"}
  - {kind: other, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=kamisado", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=kamisado+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 75
mechanics: [piece-move-patterns, legal-move-highlight, hot-seat, turn-enforcement, ai-opponent, ai-minimax, cell-click, hover-highlight, drag-drop-piece, push-object, game-screen, main-menu, end-screen, help-window, settings-window, state-as-data, +reach-row-win, +pass-turn, +forced-piece-by-color, +deadlock-loss, +multi-round-match, +sumo-push, +refill-setup, +piece-rank-up]
proposes: ["+cond:same_color", "+effect:select_piece", "+trigger:deadlock", "+effect:push_line", "+ui:required-piece-highlight", "+ui:match-score", "+window:match-setup", "+window:refill-choice", "+feature:match-length", "+card:forced-piece-by-color", "+card:deadlock-loss", "+card:multi-round-match", "+card:sumo-push", "+card:refill-setup", "+card:piece-rank-up"]
author: opus
date: 2026-11-02
---

# Kamisado — колір клітини, куди ти став, вирішує, якою вежею ходитиме суперник

## Суть
Абстрактна гонка на дошці 8×8 з 64 клітин восьми кольорів: у кожного гравця 8 веж-«драконів», по одній кожного кольору. Вежа ходить як тура/слон, але лише вперед; мета — першим довести будь-яку вежу до домашнього ряду суперника. Головна механіка: **ти не обираєш, чим ходити** — колір клітини, на яку суперник поставив свою вежу, визначає, яку твою вежу ти мусиш рухати; тож кожен хід — це ще й вибір наступного ходу для суперника. У матчах переможна вежа отримує кільце Sumo й уміє штовхати ворожі вежі.

## Поле і час
- Дошка 8×8, кожна клітина одного з 8 кольорів (оранжевий, синій, фіолетовий, рожевий, жовтий, червоний, зелений, коричневий); у кожному ряду й кожному стовпці всі 8 кольорів по одному разу — як латинський квадрат (?).
- Старт: вежі стоять на своєму домашньому ряду; колір вежі збігається з кольором клітини під нею на старті.
- Покроково; один раунд — коротка партія; матч — серія раундів до 3 / 7 / 15 очок.
- Перший хід у першому раунді — чорні, вежу обирають вільно; далі вежу визначає колір.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вежа (dragon tower) | piece | сторона gold/black; колір із 8 | будь-яка кількість клітин прямо вперед або по діагоналі вперед; без перестрибувань, без взяття, без руху назад/убік |
| Sumo-вежа | piece | 1 кільце, 1 очко | хід до 5 клітин; Sumo push: штовхає 1 ворожу звичайну вежу прямо перед собою на 1 клітину назад |
| Double Sumo | piece | 2 кільця, 3 очки | хід до 3 клітин; штовхає 1–2 вежі (звичайні або Sumo) |
| Triple Sumo | piece | 3 кільця, 7 очок | хід лише на 1 клітину; штовхає до 3 веж (крім Triple) |
| Кольорова клітина | terrain | колір | стати на неї = призначити супернику вежу цього кольору |
| Домашній ряд | zone | ряд старту кожного | досягти ряду суперника = виграти раунд; вежу на власному домашньому ряду штовхнути не можна |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО чорні обирають будь-яку вежу і ходять.
- КОЛИ `input(move, tower, to)` → ЯКЩО `turn_of(side)` і `same(tower, last_landing_cell, color)` (`+cond:same_color`) і `custom: «to прямо або по діагоналі вперед, шлях вільний»` → ТО `move(tower, to)`; інакше `block`.
- КОЛИ `after(move)` → ТО `custom: «супернику призначено вежу кольору клітини to»` (`+effect:select_piece`), `end_turn`.
- КОЛИ `turn_start(side)` → ЯКЩО `blocked(required_tower)` → ТО хід нульової довжини: `pass_turn`; суперник ходить вежею кольору клітини, на якій стоїть заблокована вежа.
- КОЛИ `custom: «цикл блоків, жоден не може рухатись»` (`+trigger:deadlock`) → ТО `lose` тому, хто зробив останній хід перед дедлоком (навіть вимушений).
- КОЛИ `reach(tower, enemy_home_row)` → ТО `win` раунду; вежа отримує кільце Sumo (`transform(sumo)`), +очки за ранг.
- Після дедлоку кільце отримує гравець, що не спричинив його, — на вежу кольору клітини, куди суперник став останнім.
- Sumo push: КОЛИ `turn_start(side)` → ЯКЩО обовʼязкова вежа — Sumo і `occupied(front, enemy_tower_lower_rank)` і `free(behind_enemy)` і ворожа не на своєму домашньому ряду → ТО `custom: «штовхнути на 1 назад»` (`+effect:push_line`); лише прямо вперед, не по діагоналі.
- КОЛИ `after(sumo_push)` → ТО `skip_turn(opponent)`; штовхач одразу ходить ще раз — вежею кольору клітини, куди потрапила відштовхнута вежа.
- Sumo push необовʼязковий, якщо є діагональний хід; обовʼязковий, якщо він єдиний легальний.
- Новий раунд: переможець (Defender) обирає заповнення зліва чи справа (`choose`); вежі обох сторін розставляються на домашні ряди в тому самому порядку, у якому стояли рядами на дошці; переможений (Challenger) ходить першим.
- Очки: звичайна вежа дійшла — 1; Sumo — ще 2 (разом 3); Double Sumo — ще 4 (разом 7); Triple Sumo, що дійшла, виграє марафон одразу.
- Перемога: першим набрати 1 / 3 / 7 / 15 очок (Single / Standard / Long / Marathon) · Поразка: суперник дійшов або ти спричинив дедлок · Рахунок: сума кілець-рангів.

## Керування і ввід
- Настільна: пересунути вежу; одягнути кільце-Sumo на вежу після раунду.
- (цифрова версія) Обовʼязкова вежа підсвічується автоматично, гравець обирає лише клітину призначення; легальні клітини — промені вперед/діагоналі з урахуванням ліміту Sumo; кнопка «заблоковано — пропуск» або автопропуск.
- Перед новим раундом — вибір «заповнити зліва/справа».

## Вікна, меню, HUD
- `main-menu`: Грати → `match-setup` (довжина матчу 1/3/7/15, суперник AI/друг) → `game-screen`; Правила → `help-window`.
- `game-screen`: кольорова дошка, `turn-indicator`, `required-piece-highlight` (яка вежа зобовʼязана ходити), `legal-move-highlight`, `match-score` (очки і кільця кожного), `last-move-highlight`.
- `refill-choice` (модал між раундами): зліва / справа.
- `end-screen`: раунд виграно (яка вежа, скільки очок), матч виграно.
- Переходи: main-menu → match-setup → game-screen → (раунд) refill-choice → game-screen → … → end-screen.

## Фічі поза полем
- `match-length` — Single / Standard / Long / Marathon; кожна відкриває нові ранги Sumo.
- `ai-opponent-levels`, `hotseat`, `rules-page`.
- Комерційні видання: Classic, Pocket, Max (?) — фізичні.

## Варіації й родичі
- Довжина матчу як вісь складності правил: Single (без Sumo) → Standard (Sumo) → Long (Double) → Marathon (Triple).
- Осі варіацій: **хто обирає фігуру** (гравець / колір клітини суперника / карта) · **ранг фігури** (звичайна → Sumo → Double → Triple: швидкість ↓, сила штовхання ↑) · **кінець** (досягти ряду / дедлок).
- Родичі: Onitama (наступний хід суперника визначає використана карта), Breakthrough (гонка до ряду).

## Цікавинки для курсу
- «Твій хід обирає фігуру супернику»: стан гри = позиція + обовʼязковий колір — 🌱 у реалізації, але глибока стратегія.
- Блок і перехід ходу з нульовим ходом, виявлення дедлоку (цикл станів без руху) — 🥉.
- Ранги веж з різним лімітом ходу й силою штовхання — 📎 (параметри патерну).
- Sumo push ланцюгом з пропуском ходу суперника й новим вибором кольору — 🥉.
- Матч з кількох раундів і перерозстановкою за порядком веж — 📎.
- AI minimax: дуже мале розгалуження (лише 1 вежа на хід) → глибокий перебір на 15+ ходів — 🥇 (і розвʼязок «перший виграє за 17 ходів»).

## Мапа на каталог
- Є: `piece-move-patterns` ↔ хід як тура/слон лише вперед · `legal-move-highlight` · `push-object` ↔ Sumo push (з обмеженнями) · `hot-seat`, `turn-enforcement` · `ai-opponent`, `ai-minimax` · `cell-click`, `hover-highlight`, `drag-drop-piece` · `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window` · `state-as-data`.
- **Нема** → пропозиції карток:
  - `+reach-row-win` (див. quoridor.md).
  - `+pass-turn` (див. reversi.md) — тут пропуск із передачею кольору.
  - `+forced-piece-by-color` «Колір клітини обирає фігуру супернику» · entities/legality · 📎.
  - `+deadlock-loss` «Дедлок — поразка того, хто спричинив» · game-logic/lose · 🥉 — виявлення циклу пропусків.
  - `+multi-round-match` «Матч з раундів до N очок» · game-logic/score · 📎 · слоти {target: 1|3|7|15}.
  - `+sumo-push` «Штовхання ряду фігур фігурою вищого рангу» · entities/combat · 🥉 · слоти {max_pushed, diag: bool}.
  - `+refill-setup` «Розстановка нового раунду з попереднього» · levels/generation · 📎 · слоти {from: left|right}.
  - `+piece-rank-up` «Ранги фігури за перемоги» · entities/state · 📎 · слоти {ranks: [move, push]}.

## Пропозиції до словників
- `+cond:same_color` — фігура збігається кольором з клітиною (окремий випадок ⏳ `same(a, b, prop)`).
- `+effect:select_piece` — призначити супернику фігуру, якою він мусить ходити.
- `+trigger:deadlock` — жодна сторона не може рухатись (цикл пропусків), відмінне від `no_moves(side)` для однієї сторони.
- `+effect:push_line` — штовхнути ряд із кількох фігур на 1 (Sumo, Abalone).
- `+ui:required-piece-highlight` — яка фігура зобовʼязана ходити; `+ui:match-score` — очки матчу й ранги.
- `+window:match-setup` — довжина матчу; `+window:refill-choice` — вибір заповнення між раундами.
- `+feature:match-length` — 1/3/7/15 очок.
- `+card:forced-piece-by-color`, `+card:deadlock-loss`, `+card:multi-round-match`, `+card:sumo-push`, `+card:refill-setup`, `+card:piece-rank-up` — див. «Мапа на каталог».

## Джерела
- ⭐ [UltraBoardGames: Kamisado rules](https://www.ultraboardgames.com/kamisado/game-rules.php) — хід, вибір вежі кольором, блок, дедлок, наступні раунди, довжини матчів.
- [Standard Match](https://www.ultraboardgames.com/kamisado/standard-match-game-rules.php) — Sumo (до 5 клітин, правила S1–S11), заповнення F1–F2, очки.
- [Long Match](https://www.ultraboardgames.com/kamisado/long-match-game-rules.php) — Double Sumo (до 3, штовхає 1–2).
- [Marathon Match](https://www.ultraboardgames.com/kamisado/marathon-match-game-rules.php) — Triple Sumo (хід 1, штовхає до 3).
- [Wikipedia: Kamisado](https://en.wikipedia.org/wiki/Kamisado) — автор, рік, матчі, Mind Sports Olympiad 2011, перемога першого за 17 ходів.
- [Burley Games](https://www.burleygames.com/) — видавець; видання Classic, Pocket, Korean.
- BGG і YouTube — пошукові сторінки.

## Непевне
- (?) Розкладка кольорів дошки як латинський квадрат — з памʼяті, на джерелі не перевірено.
- (?) Точна механіка заповнення «зліва/справа» (як саме розставляються вежі за порядком у рядах) — переказ правил F1–F2 поверхневий.
- (?) Цифрові версії (офіційний застосунок, онлайн) — не знайдено без пошуку; вікна описано як «(цифрова версія)».
- (?) Kamisado Max і кількість видань — не перевірено.
- (?) Чи може Sumo push бути ланцюгом, коли штовхнута вежа знову опиняється перед Sumo, — не вивчено.
