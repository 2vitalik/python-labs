---
title: Entropy (Ентропія)
slug: entropy
aka: [Hyle, Hyle7, Vis-A-Vis, Ентропія]
family: chess-abstract
also: [board-digital]
klass: hybrid
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: runtime
  goal: score
year: 1977
platforms: [board, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Entropy_(board_game)", best: true, note: "правила 7×7: ролі Хаос/Порядок, випадкова фішка з мішка, хід як тура або пас, очки за паліндроми з прикладами, два раунди зі зміною ролей, MSO"}
  - {kind: other, url: "https://raw.githubusercontent.com/AbstractPlay/gameslib/main/src/games/entropy.ts", note: "код Abstract Play: мішок N кольорів × N фішок, варіанти 5×5/6×6/7×7, підрахунок паліндромів, одночасна гра на двох дошках"}
  - {kind: play, url: "https://play.abstractplay.com/games/entropy", note: "Abstract Play: гра поштою (SPA, текст правил не віддає)"}
  - {kind: play, url: "https://vint.ee/en-gb/games/#entropy", note: "Vint.ee: real-time онлайн (з Wikipedia; не відкривав)"}
  - {kind: bgg, url: "https://boardgamegeek.com/boardgame/1329", note: "Hyle на BGG (з Wikipedia)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=entropy+eric+solomon+board+game", note: "пошук"}
stage: v1
coverage: 75
mechanics: [cursor-place, piece-move-patterns, cell-click, drag-drop-piece, legal-move-highlight, selection-highlight, last-move-highlight, pass-turn, next-queue, remaining-counter, hot-seat, turn-enforcement, ai-opponent, ai-greedy, ai-minimax, simultaneous-versus, async-multiplayer, field-size-picker, match-setup, game-screen, main-menu, end-screen, help-window, state-as-data, unit-tests, +tile-bag-draw, +asymmetric-roles, +side-swap-match, +palindrome-scoring, +ai-expectimax]
proposes: ["+effect:draw_tile", "+effect:swap_role", "+cond:palindrome", "+ui:bag-meter", "+ui:pass-button", "+ui:palindrome-highlight", "+window:round-summary", "+feature:role-swap", "+card:palindrome-scoring", "+card:shared-random-stream"]
author: opus
date: 2026-11-09
---

# Entropy — Хаос ставить випадкову фішку куди завгодно, Порядок зсуває одну фішку як туру; очки — за паліндроми кольорів у рядках і стовпцях

## Суть
Асиметрична гра Eric Solomon (1977) для двох: в одному раунді ти — Хаос, у другому — Порядок. Хаос тягне з мішка фішку випадкового кольору й ставить на будь-яку порожню клітину, щоб зруйнувати візерунки; Порядок пересуває будь-яку фішку по прямій (як тура) або пасує, щоб складати симетричні послідовності кольорів. Коли дошка повна, Порядок отримує очки за кожен паліндром у рядках і стовпцях; потім ролі міняються, і виграє той, хто як Порядок набрав більше. Клас `hybrid`: Хаос діє як `cursor` (виставлення), Порядок — як `figure`-тура над спільними фішками.

## Поле і час
- Дошка 7×7 (49 клітин), 49 фішок 7 кольорів по 7 (з 2000 р.); оригінал 1977 — 5×5 (Hyle, Vis-A-Vis), за кодом Abstract Play — 5 кольорів × 5 фішок; є й 6×6.
- Один шар, у клітині ≤1 фішка; фішки нічиї — Порядок рухає будь-яку.
- Покроково: хід Хаосу (поставити) → хід Порядку (зсунути або пас); раунд — доки не поставлено останню фішку й дошка не повна. Два раунди, ролі міняються.
- Інформація повна, випадковість — лише колір наступної фішки; склад мішка відомий (можна рахувати, що лишилось).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фішка | tile | колір 1 із 7 | ставиться Хаосом; Порядок зсуває ортогонально на будь-яку відстань через порожні клітини |
| Мішок | container | 49 фішок (7×7) | Хаос тягне наосліп одну на хід |
| Хаос | player | роль у раунді | обирає клітину для витягнутої фішки |
| Порядок | player | роль у раунді; рахунок | зсуває одну фішку або пасує; отримує очки |
| Рядок / стовпець | zone | 7 клітин | у ньому рахуються всі паліндроми довжини ≥ 2 |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «порожня дошка, повний мішок; гравці домовляються, хто перший Порядок»`.
- КОЛИ `turn_start(chaos)` → ТО `custom: «витягти з мішка випадкову фішку»` (`+effect:draw_tile`), фішку видно обом.
- КОЛИ `input(place, cell)` → ЯКЩО `turn_of(chaos)` і `free(cell)` → ТО `place(chaos, chip)`, `end_turn`.
- КОЛИ `input(move, chip, to)` → ЯКЩО `turn_of(order)` і `custom: «to на тій самій горизонталі або вертикалі»` і `free(path)` і `free(to)` → ТО `move(chip, to)`, `end_turn`; перестрибувати фішки не можна, рухати можна будь-яку фішку на дошці.
- КОЛИ `input(pass)` → ЯКЩО `turn_of(order)` → ТО `pass_turn`.
- КОЛИ `counter(empty_cells, ==, 0)` → ТО `custom: «раунд скінчився, підрахунок»`.
- КОЛИ `after(round_end)` → ЯКЩО `custom: «відрізок рядка чи стовпця довжини k ≥ 2 без порожніх читається однаково в обидва боки»` (`+cond:palindrome`) → ТО `score(+k)` Порядку — кожен паліндром окремо, вкладені й накладені теж.
- Приклади (Wikipedia): червоний-зелений-синій-зелений-червоний = 8 (3 + 5); червоний-червоний-червоний = 7 (2 + 2 + 3).
- КОЛИ `after(round_end)` → ЯКЩО `custom: «зіграно перший раунд»` → ТО `custom: «обмін ролями, нова порожня дошка й повний мішок»` (`+effect:swap_role`).
- КОЛИ `after(round_end)` → ЯКЩО `custom: «зіграно другий раунд»` і `custom: «очки A як Порядку > очки B як Порядку»` → ТО `win` для A; рівно → `draw`.
- Abstract Play: КОЛИ `turn_start(both)` → ТО `custom: «одна спільна випадкова фішка; кожен ставить її на дошку Порядку суперника і робить хід Порядку на своїй»` — дві партії одночасно, однаковий потік фішок (`+card:shared-random-stream`).
- Перемога: більше очок у ролі Порядку за два раунди · Поразка: менше · Рахунок: Σ довжин усіх паліндромів у 7 рядках і 7 стовпцях.

## Керування і ввід
- Настільна: Хаос тягне фішку й кладе; Порядок пересуває фішку пальцем по прямій або каже «пас».
- (цифрова версія) Хаос: показ витягнутої фішки (`next-queue`) + клік по порожній клітині (`cursor-place`). Порядок: клік/drag по будь-якій фішці → `legal-move-highlight` по 4 променях до першої перешкоди; кнопка `pass-button`.
- На Abstract Play — одночасний хід обох (поставити на чужу + зсунути на своїй) і підтвердження.

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Грати · Проти AI · Онлайн · Правила → `help-window`.
- `match-setup`: розмір 5×5 / 6×6 / 7×7 (`field-size-picker`), хто перший Порядок, AI-рівень; на Abstract Play — опція «номери на фішках» (для дальтоніків).
- `game-screen`: дошка; роль поточного гравця (`turn-indicator`: «Хаос» / «Порядок»); витягнута фішка; `bag-meter` і `remaining-counter` за кольорами; поточний рахунок Порядку (`score`), підсвітка паліндромів (`palindrome-highlight`); `last-move-highlight`; `pass-button`.
- `round-summary` після раунду: розбір паліндромів по лініях, очки; «Міняємось ролями».
- `end-screen`: очки обох як Порядку, переможець або нічия.
- Переходи: main-menu → match-setup → game-screen (раунд 1) → round-summary → game-screen (раунд 2) → end-screen.

## Фічі поза полем
- `field-size-picker` / `custom-rules`: 5×5, 6×6, 7×7.
- `async-multiplayer` (Abstract Play), real-time онлайн (Vint.ee); турнір Mind Sports Olympiad з першої олімпіади (Demis Hassabis — п'ять перемог).
- `role-swap` — обовʼязкова частина матчу (два раунди).

## Варіації й родичі
- Hyle (Німеччина, 5×5), Hyle7 (7×7), Vis-A-Vis (США, 5×5).
- Одночасна дводошкова версія Abstract Play зі спільним потоком фішок — рівні умови для обох.
- Родичі: [reversi](reversi.md), [pente](pente.md) (візерунки на дошці) · [quarto](../board-digital/quarto.md) (суперник обирає, що ти ставиш) · [qwirkle-ingenious](../board-digital/qwirkle-ingenious.md) (очки за лінії кольорів) · Tic-tac-toe «Order and Chaos» (ролі з тими самими назвами — інша гра).
- **Осі варіацій**: асиметрія ролей (одна гра — дві різні дії) · джерело хаосу (кубик / мішок / суперник) · що рахується (лінія N в ряд / паліндром / група) · симетрія матчу (обмін ролями / одночасні дошки зі спільним потоком).

## Цікавинки для курсу
- Підрахунок усіх паліндромних відрізків у рядку з урахуванням порожніх — 🌱 (класична задача на рядки; оптимізація — 📎).
- Хід «тура» по спільних фішках + пас — 🌱.
- Мішок з відомим складом і лічильник кольорів, що лишились — 🌱.
- Дві ролі з різними наборами дій і обмін ними між раундами — 📎.
- AI для Порядку (жадібний: максимум приросту очок) і для Хаосу (мінімум), повний — expectimax з вузлами кольору — 🥇.
- Одночасні дві партії зі спільним випадковим потоком (Abstract Play) — 🥈.

## Мапа на каталог
- Є: `cursor-place` ↔ Хаос ставить фішку · `piece-move-patterns` ↔ хід Порядку як тура · `cell-click`, `drag-drop-piece` · `legal-move-highlight`, `selection-highlight`, `last-move-highlight` · `pass-turn` ↔ пас Порядку · `next-queue` ↔ витягнута фішка · `remaining-counter` ↔ скільки лишилось кожного кольору · `hot-seat`, `turn-enforcement` · `ai-opponent`, `ai-greedy`, `ai-minimax` · `simultaneous-versus` ↔ дві дошки Abstract Play · `async-multiplayer` · `field-size-picker`, `match-setup` · `game-screen`, `main-menu`, `end-screen`, `help-window` · `state-as-data`, `unit-tests`.
- Наявні пропозиції корпусу: `+tile-bag-draw` · `+asymmetric-roles` (тут два гравці, ролі міняються) · `+side-swap-match` (матч з обміном сторін) · `+ai-expectimax` (див. [einstein-wurfelt-nicht](einstein-wurfelt-nicht.md)).
- **Нема** → пропозиції карток:
  - `+palindrome-scoring` «Очки за кожен паліндромний відрізок у рядках і стовпцях» · game-logic/score · 📎 · слоти {min_len: 2, overlaps: counted}.
  - `+shared-random-stream` «Обидва гравці отримують ту саму послідовність випадкових фішок» · game-logic/opponent · 📎 — Abstract Play Entropy, родич `simultaneous-versus`.

## Пропозиції до словників
- `+effect:draw_tile` — підтверджую (isle-of-skye, the-duke): витягти фішку з мішка.
- `+effect:swap_role` — підтверджую (pac-man-sequels): обмін ролями між раундами.
- `+cond:palindrome(segment)` — відрізок без порожніх читається однаково з обох кінців.
- `+ui:bag-meter` — підтверджую (dynamine); `+ui:pass-button` — кнопка паса; `+ui:palindrome-highlight` — підсвітка відрізків, що дають очки.
- `+window:round-summary` — розбір очок після раунду.
- `+feature:role-swap` — підтверджую (mastermind): обмін ролями як частина матчу.
- `+card:palindrome-scoring`, `+card:shared-random-stream` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Entropy (board game)](https://en.wikipedia.org/wiki/Entropy_(board_game)) — Eric Solomon 1977, 7×7 з 2000, 49 фішок 7 кольорів, ролі, тура-хід або пас, очки за паліндроми з прикладами (8 і 7), «30 можливих візерунків у лінії з 7», два раунди, назви Hyle / Hyle7 / Vis-A-Vis, MSO, Games & Puzzles 6/6.
- [Abstract Play: entropy.ts](https://raw.githubusercontent.com/AbstractPlay/gameslib/main/src/games/entropy.ts) — склад мішка (N кольорів × N), варіанти 5×5/6×6/7×7, пас завжди легальний, функція `scoreLine` (усі відрізки довжини ≥ 2 без порожніх), одночасна гра на двох дошках, опція номерів на фішках.
- [Abstract Play: Entropy](https://play.abstractplay.com/games/entropy) — онлайн-гра (сторінка — SPA).
- YouTube: пошук «entropy eric solomon board game».

## Непевне
- (?) Склад мішка на 5×5 (5 кольорів × 5) — з коду Abstract Play; в оригінальних правилах Hyle не перевірено.
- (?) Чи бачить Порядок фішку до того, як Хаос її поставить, і чи може Порядок рухати щойно поставлену — правила кажуть «будь-яку»; видимість фішки до виставлення в Wikipedia не сказано.
- (?) Хто визначає першу роль — у джерелах не знайшов.
- (?) Рік видання й видавець — Wikipedia дає лише рік дизайну 1977; 7×7 «з 2000».
- (?) Wikipedia суперечлива щодо рекорду MSO (David Jameson 2021 vs Paul Kolk у списку переможців) — не переносив.
- (?) Сімʼя: у межових випадках черги Entropy позначено `board-digital`; кладу в `chess-abstract` (абстрактна класика), `also: [board-digital]`.
