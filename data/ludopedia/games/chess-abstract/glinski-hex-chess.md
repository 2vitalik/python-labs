---
title: Gliński's hexagonal chess (Гексагональні шахи Глінського)
slug: glinski-hex-chess
aka: [Hexagonal chess, Гексагональні шахи, Шахи Глінського, Szachy heksagonalne]
family: chess-abstract
also: []
klass: figure
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 1936
platforms: [board, web, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Gliński's_hexagonal_chess", best: true, note: "дошка 91 клітина, рух фігур на гексах, пішаки, пат = ¾ очка, три слони"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hexagonal_chess", note: "огляд гекс-варіантів: Gliński, McCooey, Shafran, Brusky, De Vasa, Starchess; історія, програми"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=glinski+hexagonal+chess", note: "пошук; правила й партії"}
stage: v1
coverage: 60
mechanics: [piece-move-patterns, piece-capture, legal-move-highlight, no-move-into-check, check-stalemate, checkmate, pawn-promotion, cell-click, drag-drop-piece, hot-seat, ai-opponent, online-multiplayer, async-multiplayer, rule-variants, move-notation, game-screen, end-screen, +hex-grid-render, +en-passant, +stalemate-partial-score, +three-color-board]
proposes: ["+cond:hex_dir", "+effect:score_split", "+ui:hex-coordinates", "+ui:cell-tint", "+axis:win-condition", "+card:stalemate-partial-score", "+card:hex-piece-moves"]
author: opus
date: 2026-11-09
---

# Гексагональні шахи Глінського — шахові фігури на шестикутнику з 91 клітини трьох кольорів

## Суть
Найпопулярніший гекс-варіант шахів: ті самі фігури й мета (мат), але поле — правильний шестикутник із 91 гексагональної клітини трьох кольорів. Перенесення на гекси змінює все: «ортогональ» іде через ребро (6 напрямків), «діагональ» — через вершину (ще 6), тож слонів по три на сторону (по одному на колір), кінь має нову геометрію, а пат — не нічия, а ¾ очка. Цінність для курсу — генератор ходів на гекс-сітці з тим самим набором фігур.

## Поле і час
- Правильний шестикутник, вершиною вгору, сторона — 6 клітин, 91 клітина; три кольори (світлий, темний, середній), центр — середній.
- 11 вертикалей a–l (без j), 11 горизонталей; горизонталі «ламаються» на 60° на вертикалі f. Горизонталі 1–6 мають по 11 клітин, 7-ма — 9, 8-ма — 7, … 11-та — одна клітина f11.
- Нотація — ICCF-цифрова (без рокіровки).
- Покроковий хід, білі першими; на клітині ≤1 фігура.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Король | piece | royal | 1 клітина в будь-якому з 12 напрямків (6 ортогональних + 6 діагональних); рокіровки нема |
| Ферзь | piece | — | тура + слон: будь-яка відстань по 12 напрямках |
| Тура | piece | — | будь-яка відстань ортогонально — через ребра клітин (6 напрямків) |
| Слон ×3 | piece | колір клітин | будь-яка відстань діагонально — через вершини (6 напрямків); кожен прив'язаний до одного з трьох кольорів, слони не захищають один одного |
| Кінь | piece | — | 2 клітини ортогонально, потім 1 під кутом 60°; перестрибує; еквівалентно: найближча клітина, що не лежить на спільній з вихідною лінії |
| Пішак ×9 | piece | напрямок вперед | 1 вперед на порожню; 2 — зі стартової клітини (будь-якого пішака свого кольору); бʼє на 1 «діагонально» вперед під 60° від вертикалі; en passant; перетворення в кінці будь-якої вертикалі |
| Клітина | static | один з 3 кольорів | визначає, якому слону доступна |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move(rook, to))` → ЯКЩО `custom: «to на одному з 6 ортогональних гекс-променів, шлях вільний»` → ТО `move(rook, to)`.
- КОЛИ `input(move(bishop, to))` → ЯКЩО `custom: «to на одному з 6 діагональних (через вершину) променів, шлях вільний»` → ТО `move(bishop, to)`.
- КОЛИ `input(move(queen, to))` → ЯКЩО `custom: «будь-який з 12 променів, шлях вільний»` → ТО `move(queen, to)`.
- КОЛИ `input(move(king, to))` → ЯКЩО `custom: «сусід по одному з 12 напрямків»` and `legal(move)` → ТО `move(king, to)`.
- КОЛИ `input(move(knight, to))` → ЯКЩО `custom: «2 ортогонально + 1 під 60°»` → ТО `move(knight, to)` (перестрибує).
- КОЛИ `input(move(pawn, to))` → ЯКЩО `free(to)` and `custom: «на 1 прямо вперед»` → ТО `move(pawn, to)`.
- КОЛИ `input(move(pawn, to))` → ЯКЩО `custom: «пішак на стартовій клітині пішака свого кольору, 2 прямо вперед, обидві вільні»` → ТО `move(pawn, to)`; пішак f, заблокований на f7, подвійного кроку не має.
- КОЛИ `input(capture(pawn, to))` → ЯКЩО `occupied(to, enemy)` and `custom: «на 1 вперед під 60° від вертикалі»` → ТО `disappear_b`, `move(pawn, to)`; en passant — за аналогією з шахами.
- КОЛИ `reach(pawn, custom: «кінець вертикалі»)` → ТО `choose(фігура)`, `transform`.
- КОЛИ `input(move)` → ЯКЩО `not legal(move)` (лишає короля під шахом) → ТО `block`.
- КОЛИ `check(side)` → ЯКЩО `no_moves(side)` → ТО `lose` (мат, 1 : 0).
- КОЛИ `no_moves(side)` → ЯКЩО `not in_check(side)` → ТО `score(¾ тому, хто запатував; ¼ запатованому)`.
- Перемога: мат · Пат: ¾ : ¼ · Інші нічиї — як у шахах (?).

## Керування і ввід
- (цифрова версія) Клік/drag фігури, підсвітка цілей на гексах; вибір фігури при перетворенні.
- Програми: Scatha (Mac, GUI + рушій), Green Chess (онлайн по ходах), Omnichess, Java-програми Ed Friedlander, pchess (Python), Mini Hexchess у Ludii.

## Вікна, меню, HUD
- (цифрова версія) `game-screen`: гекс-дошка з `cell-tint` трьох кольорів, `hex-coordinates` (a–l без j, 1–11), `legal-move-highlight`, `turn-indicator`, `captured-pieces`, `move-list` у нотації ICCF.
- `variant-select` (Green Chess: Gliński, McCooey, Shafran, Brusky, De Vasa).
- `end-screen`: мат / пат (¾ : ¼) / нічия.
- Переходи: main-menu → variant-select → game-screen → end-screen.

## Фічі поза полем
- `custom-rules` — набір гекс-варіантів на одному рушії (Green Chess).
- `online-multiplayer` по ходах (Green Chess) — ближче до кореспонденції; `ai-opponent` — рушій Scatha.
- `export-import` / нотація ICCF.

## Варіації й родичі
- **McCooey** (1978–79, Dave McCooey і Richard Honeycutt): 7 пішаків, пішак бʼє як слон на 1, f-пішаки без подвійного кроку, пат = ½.
- **Shafran** (1939, зареєстровано 1956): неправильний шестикутник із 70 клітин (9 вертикалей, 10 горизонталей); перший хід пішака 1–3 кроки залежно від вертикалі; рокіровка; пат = нічия.
- **Brusky** (1966): 84 клітини, 10 пішаків, бʼють прямо вперед лише нерухані пішаки, en passant, рокіровка, королі на протилежних флангах.
- **De Vasa** (1953): ромб із 81 клітини, рокіровка (коротка — 2 клітини, довга — 3), королі на протилежних флангах.
- **Starchess** (≈2004, László Polgár): гексаграма з 37 клітин, 5 пішаків, тура лише вертикально, слон — не вертикально; без рокіровки й en passant.
- Wellisch (1912, на трьох), Three-Way Chess (Harshman); Hexagonia (1864) — мета довести короля в центр.
- Родичі в корпусі: [hex.md](hex.md), [hive.md](hive.md), [abalone.md](abalone.md) — інші гекс-поля; [chess.md](chess.md) — квадратний оригінал; [xiangqi.md](xiangqi.md)/[shogi.md](shogi.md) — інші національні шахи.
- **Осі варіацій**: форма поля (шестикутник 91 · неправильний 70/84 · ромб 81 · гексаграма 37) · кількість пішаків (5–10) · взяття пішаком (60° · як слон · прямо вперед) · рокіровка (нема · є) · ціна пату (¾ · ½).

## Цікавинки для курсу
- Гекс-координати (осьові/кубічні) і 12 напрямків руху (6 через ребро, 6 через вершину) — 🥉.
- Генератор ходів шахових фігур на гексах, включно з конем «2 + 1 під 60°» — 🥉.
- Розфарбування в 3 кольори й прив'язка трьох слонів — 📎.
- Рендер гекс-дошки з ламаними горизонталями й нотацією a–l без j — 🥉.
- Пат з частковим рахунком ¾ : ¼ — 🌱 поверх шахового `check-stalemate`.
- Один рушій — шість гекс-варіантів (поле, пішаки, рокіровка як параметри) — 🥈.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ гекс-патерни · `piece-capture` · `legal-move-highlight` · `no-move-into-check` · `check-stalemate` · `checkmate` · `pawn-promotion` ↔ кінець будь-якої вертикалі · `cell-click` · `drag-drop-piece` · `hot-seat` · `ai-opponent` ↔ Scatha · `online-multiplayer` / `async-multiplayer` ↔ Green Chess по ходах · `rule-variants` ↔ McCooey/Shafran/Brusky/De Vasa · `move-notation` ↔ ICCF · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+hex-grid-render` — підтверджую (корпус ×8).
  - `+en-passant` — підтверджую (chess.md).
  - `+stalemate-partial-score` «Пат з частковим рахунком» · game-logic/score · 🌱 · слоти {winner: 0.75, loser: 0.25}.
  - `+three-color-board` «Розфарбування гекс-поля в 3 кольори» · interface/render · 📎.
  - `+hex-piece-moves` (через `+card:`) «Шахові патерни на гекс-сітці (12 напрямків)» · entities/legality · 🥉.

## Пропозиції до словників
- `+cond:hex_dir(a, b, kind)` — B на гекс-промені від A: `edge` (ортогональ) або `vertex` (діагональ).
- `+effect:score_split(a, b)` — нерівний розподіл очок за результат (пат ¾ : ¼).
- `+ui:hex-coordinates` — підписи вертикалей/горизонталей гекс-дошки.
- `+ui:cell-tint` — колір клітини як частина правил (три слони).
- `+axis:win-condition` — значення `stalemate-partial` (підтримую вісь з chess-rule-twists).
- `+card:stalemate-partial-score` · `+card:hex-piece-moves`.

## Джерела
- ⭐ [Wikipedia: Gliński's hexagonal chess](https://en.wikipedia.org/wiki/Gliński's_hexagonal_chess) — дошка, кольори, рух фігур, пішаки (f7-виняток), пат ¾, ICCF-нотація, мат K+2N, інші гекс-варіанти, історія, програми.
- [Wikipedia: Hexagonal chess](https://en.wikipedia.org/wiki/Hexagonal_chess) — огляд варіантів і популярність (понад 500 000 гравців, 130 000+ наборів, Британія 1949, рулбук 1973).
- YouTube — пошук «glinski hexagonal chess».

## Непевне
- (?) Повна розстановка (з діаграми, текстом не підтверджена): білі — K g1, Q e1, слони f1 f2 f3, коні d1 h1, тури c1 i1, пішаки b1 c2 d3 e4 f5 g4 h3 i2 k1; чорні — дзеркально (слони f9–f11, пішаки на 7-й горизонталі).
- (?) Кількість цілей коня з центру (12) — з памʼяті.
- (?) Інші нічиї (повторення, 50 ходів) — джерела не згадують; ймовірно, як у шахах.
- (?) Чи може пішак перетворюватись у будь-яку фігуру (у т.ч. четвертого слона) — у статті лише «в кінці будь-якої вертикалі».
- (?) Деталі en passant на гексах (яка клітина «пройдена») — стаття лише каже «may capture en passant».
