---
title: Shogi (Сьоґі, японські шахи)
slug: shogi
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: online
  info: full
  random: none
  goal: state
year: 1500
platforms: [board, web, mobile, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Shogi", best: true, note: "фігури, перетворення, дропи, nifu/uchifuzume, сеннічіте, джішогі 24 очки, нотація"}
  - {kind: play, url: "https://lishogi.org/", note: "Lishogi — відкритий сервер (як Lichess), варіанти Minishogi/Chushogi/Annanshogi/Kyotoshogi/Checkshogi/Dobutsu"}
  - {kind: other, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=shogi", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=shogi+rules+explained", note: "пошук; правила"}
stage: v2
coverage: 70
mechanics: [piece-move-patterns, piece-capture, legal-move-highlight, no-move-into-check, checkmate, move-timer, turn-enforcement, ai-opponent, drag-drop-piece, cell-click, theme-select, replay, +pawn-promotion, +piece-drop, +promotion-zone, +repetition-draw, +impasse-points, +handicap-setup, +move-notation]
proposes: ["+trigger:check", "+trigger:repetition", "+cond:in_check", "+cond:in_zone", "+effect:place", "+effect:choose_promotion", "+role:zone", "+ui:pocket", "+ui:byoyomi-clock", "+window:handicap-select", "+feature:handicap"]
author: opus
date: 2026-11-02
---

# Шогі — шахи, де взяті фігури повертаються в гру на твій бік

## Суть
Шахи на 9×9 з вісьмома типами фігур, більшість з яких ходить лише на 1 клітину вперед-убік. Головна відмінність — **дропи**: взята фігура переходить у «руку» взявшого й будь-яким наступним ходом може бути поставлена на порожню клітину як своя. Тому матеріал ніколи не зникає, нічиїх майже нема, а гра закінчується атакою на короля. Друга вісь — перетворення в зоні з трьох останніх рядів.

## Поле і час
- Дошка 9×9 без кольору клітин; фігури — плоскі пʼятикутні фішки, «носом» до суперника: колір = напрям, а не фарба. Перетворення = перевернути фішку (червоний напис на звороті).
- Поза дошкою — **комадай** (підставки) кожної сторони: «рука» з взятими фігурами, видна обом.
- Хід = рух фігури **або** дроп з руки. Першим ходить Sente (чорні); у гандикапній партії — White (сильніший, без частини фігур).
- Годинник: основний час + **байо-йомі** (на кожен хід після основного — фіксований відлік, у профі зазвичай від 1 хв; останні 10 с відлічуються вголос); професійні — довгий основний час (Мейдзін — 9 год на сторону).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Король (王/玉) | piece | royal; ×1 | 1 клітина в 8 напрямках; не перетворюється |
| Тура (飛) | piece | slider; ×1 | будь-яка відстань по ортогоналях; ⇒ Дракон (龍): + 1 крок по діагоналі |
| Слон (角) | piece | slider; ×1 | будь-яка відстань по діагоналях; ⇒ Кінь-дракон (馬): + 1 крок по ортогоналі |
| Золотий генерал (金) | piece | ×2 | 6 клітин: ортогонально 1 і діагонально вперед 1; не перетворюється |
| Срібний генерал (銀) | piece | ×2 | 5 клітин: діагонально 1 і прямо вперед 1; ⇒ як золото (перетворення не обовʼязкове ніколи) |
| Кінь (桂) | piece | leaper; ×2 | лише 2 вперед + 1 убік (2 цілі), перестрибує; ⇒ як золото |
| Лансер (香) | piece | slider вперед; ×2 | будь-яка відстань прямо вперед; ⇒ як золото |
| Пішак (歩) | piece | ×9 | 1 вперед, бʼє так само (не по діагоналі); ⇒ токін (と) як золото |
| Рука / комадай | zone | фігури з лічильниками | взяті фігури, неперетворені, для дропу |
| Зона перетворення | zone | 3 дальні ряди | вхід/вихід/рух у межах → можна перетворитись |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move(piece, to))` → ЯКЩО `turn_of(side)` and `legal(move)` → ТО `move`, `end_turn`; `legal` включає «не лишати свого короля під шахом».
- КОЛИ `contact(piece, enemy_piece)` → ТО `disappear_b`, `give(capturer, hand, unpromoted(b))`, `set_side(b, capturer)`.
- КОЛИ `after(move)` → ЯКЩО `in_zone(start)` or `in_zone(end)` → ТО `choose_promotion(yes|no)` → `transform(promoted)`.
- КОЛИ `reach(pawn|lance, last_rank)` або `reach(knight, last_two_ranks)` → ТО `transform(promoted)` обовʼязково (інакше фігура без ходу).
- КОЛИ `input(drop(kind, cell))` → ЯКЩО `has(side, kind)` and `free(cell)` → ТО `place(kind, cell)` неперетвореною, `take(side, kind)`, `end_turn`; дроп не бʼє і не перетворює, навіть у зоні.
- ЯКЩО дроп `kind ∈ {pawn, lance}` на останній ряд або `knight` на два останні → `block` (фігура не матиме ходу).
- **Nifu** — ЯКЩО дроп пішака у файл, де вже є свій неперетворений пішак → `block`.
- **Uchifuzume** — ЯКЩО дроп пішака дає негайний мат → `block` (мат дропом інших фігур і ходом пішака — можна).
- КОЛИ `turn_start(side)` → ЯКЩО `in_check(side)` and `no_moves(side)` → ТО `lose(side)` (мат); у професіоналів гравець зазвичай здається раніше.
- **Сеннічіте** — КОЛИ `repetition(position + hands + side_to_move, 4)` → ТО `draw` (у профі — перегравання зі зміною кольорів); ЯКЩО повторення — вічний шах → ТО `lose` того, хто шахує.
- **Джішогі (impasse)** — КОЛИ обидва королі у своїх зонах перетворення і мат неможливий → ТО підрахунок: тура/слон = 5, решта (крім короля) = 1; `< 24` → `lose`; обидва ≥ 24 → `draw`. Аматорське правило 27 очок: ≥ 27 → `win`; декларація 81Dojo: король у зоні + ще 10 фігур у зоні, не під шахом, є час, 28 очок у Sente / 27 у Gote.
- КОЛИ `counter(clock, ==, 0)` (основний час і байо-йомі) → ТО `lose`.
- У живій професійній грі нелегальний хід (nifu тощо) = негайна поразка; цифровий клієнт такі ходи просто блокує.
- Перемога: мат · здача · тайм-аут · нелегальний хід суперника · джішогі за очками. Нічия: сеннічіте · джішогі (обидва ≥ 24).

## Керування і ввід
- Drag або клік-клік фігури; підсвітка легальних клітин; після ходу в/з/усередині зони — **діалог перетворення** (дві фішки: звичайна/перевернута); там, де перетворення обовʼязкове, діалог не зʼявляється.
- Дроп: клік/drag фігури з комадаю → підсвічені клітини, де дроп легальний (з урахуванням nifu, мертвих рядів).
- Premove, takeback-запит, здача, нічия (на Lishogi — як у Lichess).
- Перемикання стилю фігур: кандзі (1 або 2 знаки) / «міжнародні» символи-стрілки для новачків.

## Вікна, меню, HUD
- (цифрова версія — Lishogi / 81Dojo / Shogi Wars)
- `game-screen`: дошка 9×9 з `cell-coordinates` (файли 9→1 справа наліво, ряди 一…九 / a…i), два `pocket` (комадаї) з лічильниками ×N, два `player-clock` з `byoyomi-clock` (основний час → «30s» відлік, звук останніх секунд), `move-list` (кіфу), `last-move-highlight`, `legal-move-highlight`, шах — підсвітка короля.
- `confirm-dialog`-подібний вибір перетворення над клітиною.
- `handicap-select` у «Create a game»: рівний бій або гандикап (без слона, без тури, 2/4/6/8/10 фігур); варіант (Standard, Minishogi 5×5, Chushogi 12×12, Kyotoshogi 5×5, Annanshogi, Checkshogi, Dobutsu).
- `analysis-board` з рушієм (YaneuraOu/Fairy-Stockfish (?)), `editor-window` для позицій SFEN, `puzzle-window` (tsume — задачі на мат).
- `end-screen`: «Sente wins by checkmate / impasse / repetition», зміна рейтингу.
- `settings-window`: стиль фігур (кандзі/міжнародні), дошка, звуки, нотація (західна / японська / кіфу).
- Переходи: main-menu → handicap-select → пошук → game-screen → end-screen → аналіз.

## Фічі поза полем
- `handicap` — замість рейтингової компенсації сильніший гравець прибирає фігури й ходить першим (uwate/shitate).
- `online-multiplayer`, `rating`, `ai-opponent-levels`, `replay`/`export-import` (KIF/CSA/SFEN (?)), `puzzle-bank` (цумешогі), `custom-skins` (набори фігур), `localization` (японська нотація).
- Нотація: західна `Rx24`, `P*35` (дроп), `+`/`=` (перетворив / відмовився); японська — кандзі + цифри.

## Варіації й родичі
- Шахи (без дропів), Crazyhouse (дропи в шахах — див. `lichess-variants`), сянці (Китай), макрук (Таїланд).
- Міні-варіанти: Minishogi 5×5, Kyoto shogi (фігура міняє тип кожним ходом), Dōbutsu shogi 3×4 для дітей; великі: Chu shogi 12×12, Tenjiku 16×16, Taikyoku 36×36.
- **Осі варіацій**: доля взятої фігури (зникає / рука) · перетворення (лише пішак на останньому / будь-яка в зоні / щоходу) · обмеження дропу (нема / мертві ряди / nifu / мат пішаком) · розмір поля (3×4 … 36×36).

## Цікавинки для курсу
- Дропи з руки + підсвітка легальних клітин для дропу (мертві ряди, nifu) — 🥈.
- Uchifuzume: дроп пішака легальний, лише якщо **не** дає мату — потрібна перевірка мату всередині перевірки легальності — 🥇.
- Зона перетворення з опційним/обовʼязковим перетворенням і діалогом — 🥉.
- Сеннічіте: хеш позиції з рукою й чергою, 4 повторення, вічний шах — поразка — 🥈.
- Джішогі: підрахунок очок 5/1 і поріг 24 — 📎.
- Фігури-напрям: та сама фішка «дивиться» в бік власника; рендер поворотом — 🌱.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ 8 типів + перетворені · `piece-capture` · `legal-move-highlight` · `no-move-into-check` · `checkmate` · `move-timer` ↔ байо-йомі · `turn-enforcement` · `ai-opponent` · `drag-drop-piece` + `cell-click` · `theme-select` ↔ стиль фігур · `replay` ↔ кіфу.
- **Нема** → пропозиції карток:
  - `+piece-drop` «Дроп фігури з руки» · entities/legality · 🥈 (див. lichess-variants).
  - `+promotion-zone` «Зона перетворення» · entities/state · 🥉 · слоти {rows, mandatory} — опційне перетворення при вході/виході.
  - `+pawn-promotion` (див. chess.md) — тут ширше: перетворюються 6 типів.
  - `+repetition-draw` (див. chess.md) — тут n=4 і вічний шах.
  - `+impasse-points` «Підрахунок очок при безвиході» · game-logic/score · 📎 · слоти {threshold}.
  - `+handicap-setup` «Гандикап прибиранням фігур/каменів» · game-logic/difficulty · 🌱 · слоти {preset}.
  - `+move-notation` (див. chess.md) — тут з дропом `*` і `+`/`=`.

## Пропозиції до словників
- `+trigger:check` · `+trigger:repetition` · `+cond:in_check` — як у chess.md.
- `+cond:in_zone` — клітина/фігура в зоні (зона перетворення, центр KotH, джішогі).
- `+effect:place` — дроп з руки (спільне з Crazyhouse, го, Hive); `+effect:choose_promotion` — так/ні.
- `+role:zone` — рука і зона перетворення.
- `+ui:pocket` — комадай; `+ui:byoyomi-clock` — годинник з періодами байо-йомі (шогі, го).
- `+window:handicap-select` — вибір гандикапу перед партією (шогі, го).
- `+feature:handicap` — компенсація сили правилами, а не рейтингом.

## Джерела
- ⭐ [Wikipedia: Shogi](https://en.wikipedia.org/wiki/Shogi) — фігури й ходи, перетворення, дропи, nifu, uchifuzume, сеннічіте (4 повторення, вічний шах), джішогі 24/27 очок, байо-йомі, гандикапи, нотація.
- [Lishogi](https://lishogi.org/) — відкритий сервер; сторінка /variant: Minishogi, Chushogi, Annanshogi, Kyotoshogi, Checkshogi, Dobutsu.
- BGG: пошук «shogi».
- YouTube: пошук «shogi rules explained».

## Непевне
- (?) Рушії аналізу Lishogi, формати експорту (KIF/CSA/SFEN), стилі фігур і звук байо-йомі на Lishogi — з памʼяті.
- (?) Терміни uwate/shitate і точний перелік гандикапів (2/4/6/8/10) — Wikipedia підтверджує лише «від 1–2 до 10 фігур білих».
- (?) «Нема легальних ходів без шаху = поразка» — рідкісний випадок, у джерелі не перевірено, тому не внесено до правил.
- (?) Вміст вікон 81Dojo / Shogi Wars — з памʼяті, не відкривав.
- (?) `year: 1500` — умовно: за Wikipedia правило дропу «ймовірно, винайдене в XV ст.», сучасна форма — «вже в XV ст.».
