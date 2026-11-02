---
title: Draughts / Checkers (Шашки)
slug: checkers
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 1100
platforms: [board, web, mobile, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Draughts", best: true, note: "таблиця ~30 варіантів з дельтами правил: дошка, взяття назад, далекі дамки, правило більшості, турецький удар"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/English_draughts", note: "англійські/американські: правила, three-move ballot, нотація 1–32, Chinook"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Russian_draughts", note: "російські: взяття назад, перетворення посеред взяття, правила нічиєї"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/International_draughts", note: "10×10: правило більшості, нотація 1–50, нічиї"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Turkish_draughts", note: "ортогональні шашки, дамка-тура, знімання одразу"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Poddavki", note: "піддавки: перемагає той, хто лишився без ходів"}
  - {kind: play, url: "https://lidraughts.org/variant", note: "lidraughts: Standard, Frisian, Frysk!, Antidraughts, Breakthrough, Russian, Brazilian"}
  - {kind: other, url: "https://lidraughts.org/variant/russian", note: "правила російських + повний набір нічийних правил, вибір нотації"}
  - {kind: other, url: "https://en.wikipedia.org/wiki/Chinook_(draughts_player)", note: "програма, що розвʼязала 8×8 (нічия, 2007)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=checkers+draughts+rules+variants", note: "пошук; правила й варіанти"}
stage: v1
coverage: 70
mechanics: [piece-move-patterns, piece-capture, legal-move-highlight, no-moves-left, hot-seat, turn-enforcement, move-timer, ai-opponent, ai-random, ai-greedy, ai-minimax, cell-click, hover-highlight, drag-drop-piece, game-screen, main-menu, end-screen, help-window, settings-window, theme-select, field-size-picker, replay, state-as-data, unit-tests, +forced-capture, +multi-jump, +max-capture-rule, +flying-piece, +pawn-promotion, +repetition-draw, +move-count-draw, +move-notation, +rule-variants, +misere-win, +reach-row-win, +opening-ballot]
proposes: ["+effect:jump_capture", "+cond:can_capture", "+cond:max_capture", "+trigger:repetition", "+effect:choose_promotion", "+ui:capture-path", "+ui:last-move-highlight", "+window:variant-select", "+feature:custom-rules", "+axis:win-condition", "+card:multi-jump", "+card:max-capture-rule", "+card:flying-piece", "+card:misere-win", "+card:opening-ballot"]
author: opus
date: 2026-11-02
---

# Шашки — бий через сусіда ланцюгом, дійди до краю й стань дамкою

## Суть
Двоє рухають однакові шашки по темних клітинах (у турецьких — по всіх), бʼючи стрибком через сусіда на порожню клітину за ним. Взяття майже скрізь **обовʼязкове** і може йти ланцюгом в одному ході; шашка, що дійшла до останнього ряду, стає дамкою. Програє той, у кого на своєму ході нема легального ходу (фігур нема або всі заблоковані). Шашки — сімʼя з ~30 національних варіантів, що різняться кількома «перемикачами»: дошка, напрям взяття, дальність дамки, вибір серед взяттів, момент знімання збитих.

## Поле і час
- Квадратна дошка, грають лише темні клітини (діагональна сітка): 8×8 → 32 клітини (англ., рос., бразил., піддавки), 10×10 → 50 (міжнародні, фризькі), 12×12 → 72 (канадські). Турецькі: 8×8, усі 64 клітини, рух ортогональний.
- Старт: шашки на темних клітинах найближчих рядів — 3 ряди × 4 = 12 (8×8), 4 × 5 = 20 (10×10); турецькі — 16 у рядах 2–3, тилові ряди порожні.
- Перший хід: темні в англійських, білі в російських і міжнародних.
- Покроково; хід = простий хід **або** повна серія взяттів однією фігурою. Збиті в міжнародних/російських знімаються **після** серії (і їх не можна перестрибнути двічі); у турецьких — **одразу** («турецький удар»).
- Нотація: англ. — клітини 1–32 (`9-14`, `14x23`); міжнар. — 1–50; рос. — алгебраїчна `e3-d4`, `c5:e3`.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Шашка (man) | piece | сторона | 1 крок по діагоналі вперед; бʼє стрибком через сусіда (напрям — залежно від варіанта) |
| Дамка (king) | piece | сторона; коротка / далека | коротка — 1 крок у будь-який діагональний бік; далека («летюча») — будь-яку відстань, бʼє здалеку й обирає клітину приземлення |
| Темна клітина | static | — | єдина ігрова; світлі не існують для правил |
| Дамковий ряд | zone | останній ряд суперника | вхід шашки → перетворення |
| English / American checkers | — | 8×8, 12 | шашка бʼє лише вперед; дамка коротка; взяття обовʼязкове, але серію обирає гравець (не обовʼязково найдовшу); перетворення завершує хід; розвʼязано — нічия (Chinook, 2007) |
| Russian (шашки) | — | 8×8, 12 | шашка бʼє вперед і назад; дамка далека; вибір серії вільний; дійшовши до краю **посеред** взяття, шашка одразу стає дамкою і бʼє далі як дамка |
| International | — | 10×10, 20 | бʼє вперед і назад; дамка далека; **треба брати максимальну кількість** (дамка = шашка за рахунком); перетворення лише якщо хід **закінчився** на останньому ряду |
| Brazilian | — | 8×8, 12 | міжнародні правила на малій дошці |
| Canadian | — | 12×12, 30 | міжнародні правила на великій дошці |
| Frisian | — | 10×10, 20 | бʼють і по діагоналі, і по прямій; правило більшості рахує **вартість** (дамка «вовк» дорожча за шашку) |
| Spanish / Italian / Czech | — | 8×8 | шашка не бʼє назад; пріоритет: максимум фігур, далі максимум дамок / взяття дамкою (Italian: шашка не бʼє дамку) |
| Turkish (Dama) | — | 8×8, 16, усі клітини | шашка — 1 вперед або вбік **ортогонально**, бʼє так само; дамка ходить як тура й бʼє здалеку; максимум взяття; збиті знімаються одразу; дамці заборонено розворот на 180° між двома взяттями |
| Poddavki / Antidraughts | — | як база | ті самі правила, обовʼязкове взяття; **перемагає** той, хто лишився без ходу (віддав усі шашки чи заблокований) |
| Breakthrough (lidraughts) | — | 10×10 | перший, хто провів дамку, виграє |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(side)` → ЯКЩО `custom: «будь-яка фігура сторони може бити»` (`+cond:can_capture`) → ТО простий хід `block`; дозволені лише ходи-взяття.
- КОЛИ `input(move, man, to)` → ЯКЩО `not can_capture` і `free(to)` і `custom: «to — сусідня діагональ уперед»` → ТО `move(man, to)`, `end_turn`.
- КОЛИ `input(jump, piece, over)` → ЯКЩО `occupied(over, enemy)` і `free(cell_behind)` → ТО `custom: «стрибок»` (`+effect:jump_capture`): фігура переходить за `over`, `over` позначається збитим.
- КОЛИ `after(jump_capture)` → ЯКЩО та сама фігура може бити далі → ТО ще стрибок тією ж фігурою (обовʼязково, серію не можна обірвати); інакше `disappear(all_marked)`, `end_turn`.
- Перестрибнути ту саму збиту двічі не можна (вона стоїть до кінця серії); Turkish — збита знімається одразу, тож серія може повертатись тим самим шляхом, але без розвороту на 180°.
- КОЛИ `turn_start(side)` → ЯКЩО варіант International/Brazilian/Canadian/Turkish → ТО з усіх серій легальні лише ті, що беруть **максимум** (`+cond:max_capture`); English/Russian — будь-яка серія.
- КОЛИ `reach(man, last_row)` → ЯКЩО хід закінчився → ТО `transform(king)`; English — хід завершується навіть якщо можна бити далі; Russian — `transform(king)` і серія триває вже як дамка; International — проходження через ряд посеред серії не перетворює.
- Далека дамка: КОЛИ `input(jump, king, over)` → ЯКЩО `custom: «між дамкою й over порожньо, за over ≥1 порожня»` → ТО приземлення на будь-яку порожню клітину за `over` (з тих, звідки можна бити далі, якщо таке є).
- КОЛИ `turn_start(side)` → ЯКЩО `no_moves(side)` → ТО `lose` (у Poddavki/Antidraughts — `win`).
- КОЛИ `trigger:repetition(3)` (та сама позиція, той самий бік на ході) → ТО `draw`.
- Russian: 3+ дамки проти однієї дамки не виграли за 15 ходів → `draw`; 15 ходів поспіль лише дамками без взяття й руху шашок → `draw`. International: 25 ходів лише дамками без взять → `draw`; ендшпілі «3 дамки / 2 дамки + шашка / дамка + 2 шашки проти дамки» — 16 ходів → `draw`.
- Історичне «фук» (huffing): не побив → суперник знімає ту фігуру; в офіційних правилах скасоване, живе в малайзійському й мʼянманському варіантах.
- Турнірний старт English: перші 3 ходи — жереб з затверджених дебютів, дві партії з обміном кольорами (three-move restriction, з 1934).
- Перемога: суперник без ходу · Поразка: без ходу · Рахунок: партія 1 / ½ / 0; у матчах — сума партій.

## Керування і ввід
- Настільна: пересунути шашку, зняти збиті руками, дамку позначити другою шашкою зверху (англ.) або перевернути.
- (цифрова версія) Клік по фігурі → підсвічуються лише ті, що зобовʼязані бити; далі клік по клітині приземлення **по кроках** серії або одразу по фінальній клітині (якщо шлях однозначний); drag-n-drop; кнопка «Нічия» / «Здатись».
- Неоднозначні серії (той самий фініш різними шляхами — різні збиті) вимагають вибору проміжних клітин.

## Вікна, меню, HUD
- `main-menu`: Грати проти AI / проти людини / онлайн → `variant-select` (English, Russian, International, …) → `settings-window` (рівень AI, колір, годинник).
- `game-screen`: дошка, `turn-indicator`, `player-clock`, `captured-pieces` (лічильник збитих), `move-list` у нотації варіанта, `legal-move-highlight` (фігури, що мусять бити), `capture-path` (стрілки серії), `last-move-highlight`, `offer-draw-button`, `resign-button`, `undo-button` (проти AI).
- `end-screen`: перемога / поразка / нічия з причиною (нема ходів, повторення, правило 15/25 ходів), кнопки «Реванш», «Аналіз».
- `replay-window` / аналіз: перегляд ходів, експорт PDN.
- `help-window`: правила вибраного варіанта.
- Переходи: main-menu → variant-select → game-screen → end-screen → (реванш) game-screen / (аналіз) replay-window.

## Фічі поза полем
- `custom-rules` / `rule-variants` — варіант як набір перемикачів (розмір, взяття назад, далека дамка, максимум, момент знімання, misère).
- `ai-opponent-levels`, `online-multiplayer`, `turn-timer`, `rating`-система, `stats`, `history`, `export-import` партій (PDN), вибір нотації (номери полів / алгебраїчна) — lidraughts.
- `hint`/аналіз двигуном; `tutorial`; `puzzle-bank` (задачі «білі починають і виграють»).
- Доступність: blind mode на lidraughts.
- Автоматичне застосування правил нічиєї (повторення, 15/25 ходів) (?).

## Варіації й родичі
- Осі варіацій: **дошка** (8×8 / 10×10 / 12×12 / 8×8 усі клітини) · **сітка руху** (діагональна / ортогональна / обидві: Frisian, Armenian) · **взяття шашкою назад** (так / ні) · **дамка** (коротка / далека / «зупинка одразу за збитою») · **вибір серії** (вільний / максимум фігур / максимум вартості / пріоритет дамки) · **знімання збитих** (після серії / одразу) · **перетворення посеред взяття** (так / ні) · **ціль** (без ходів = поразка / перемога / перша дамка).
- Стовпові: Bashni, Lasca — збита стає під фігуру, що бʼє, утворюючи вежу.
- Родичі: Alquerque (предок), Fanorona, Kōnane, Hexdame (гекс-дошка), Halma й китайські шашки (стрибки без взяття).

## Цікавинки для курсу
- Генерація ходів з обовʼязковим взяттям: спочатку «чи може хтось бити», потім фільтр — 📎.
- Серія взяттів (DFS по стрибках із забороною перестрибнути збиту двічі) — 🥉; з далекою дамкою і вибором клітини приземлення — 🥈.
- Правило максимуму: перебрати всі серії, лишити найдовші, при рівності — вибір гравця — 🥈.
- Варіанти як конфіг (`rule-variants`): один двіжок, 5+ національних правил перемикачами — 🥇.
- Нічийні правила (повторення через хеш позиції, лічильники 15/25 ходів) — 🥈.
- AI minimax з обовʼязковим взяттям (мало гілок у тактичних позиціях) — 🥇; піддавки — той самий AI з перевернутою оцінкою — 📎.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ шашка/дамка · `piece-capture` ↔ стрибок · `legal-move-highlight` · `no-moves-left` ↔ програш без ходу · `hot-seat`, `turn-enforcement`, `move-timer` · `ai-opponent`, `ai-random`, `ai-greedy`, `ai-minimax` · `cell-click`, `hover-highlight`, `drag-drop-piece` · `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window`, `theme-select` · `field-size-picker` ↔ 8/10/12 · `replay`, `state-as-data`, `unit-tests` (позиції-фікстури серій).
- **Нема** → пропозиції карток:
  - `+forced-capture` (див. lichess-variants.md) — тут ядро гри.
  - `+multi-jump` «Серія взяттів однією фігурою» · entities/combat · 🥉 · слоти {remove: after|immediate, no_reverse: bool} — DFS по стрибках.
  - `+max-capture-rule` «Правило більшості» · entities/legality · 🥈 · слоти {by: count|value, then: kings}.
  - `+flying-piece` «Далекобійна фігура зі стрибком-взяттям» · entities/move · 🥉 — дамка: рух на будь-яку відстань, взяття здалеку, вибір приземлення.
  - `+pawn-promotion` (див. chess.md) — тут без вибору фігури, зате з режимом «посеред серії».
  - `+repetition-draw`, `+move-count-draw` (див. chess.md) — тут з лічильниками «лише дамками» і «N дамок проти однієї».
  - `+move-notation` (див. chess.md) — номери полів 1–32/1–50 або алгебраїчна.
  - `+rule-variants` (див. lichess-variants.md) — національні варіанти.
  - `+reach-row-win` (див. quoridor.md) — Breakthrough-варіант.
  - `+misere-win` «Обернена мета» · game-logic/win · 📎 — перемога, коли без ходів / без фігур (піддавки, Antichess, Anti-Reversi).
  - `+opening-ballot` «Жереб дебюту» · game-logic/opponent · 🌱 · слоти {moves: 2|3} — перші ходи з таблиці, обмін кольорами.

## Пропозиції до словників
- `+effect:jump_capture` — перестрибнути фігуру й позначити її збитою (зникнення — одразу чи після серії).
- `+cond:can_capture` — у сторони є хоча б одне взяття (умова обовʼязкового взяття).
- `+cond:max_capture` — хід належить до серій з максимальною кількістю/вартістю збитих.
- `+trigger:repetition` — позиція повторилась N разів (уже в chess/shogi).
- `+effect:choose_promotion` — тут вироджений (вибір один), але потрібен для уніфікації з шахами.
- `+ui:capture-path` — стрілки/точки всієї серії взяття; `+ui:last-move-highlight` — позначка останнього ходу.
- `+window:variant-select` — вибір національного варіанта; `+feature:custom-rules` — перемикачі правил.
- `+axis:win-condition` — тут три значення в одній сімʼї: без ходів = поразка / перемога / перша дамка.
- `+card:multi-jump`, `+card:max-capture-rule`, `+card:flying-piece`, `+card:misere-win`, `+card:opening-ballot` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Draughts](https://en.wikipedia.org/wiki/Draughts) — загальні правила, фук, таблиця ~30 варіантів з дельтами, піддавки, сучасні варіації.
- [Wikipedia: English draughts](https://en.wikipedia.org/wiki/English_draughts) — повні правила, коронування завершує хід, three-move restriction, нотація 1–32, Chinook і розвʼязок 2007.
- [Wikipedia: Russian draughts](https://en.wikipedia.org/wiki/Russian_draughts) — взяття назад, перетворення посеред серії, нічиї.
- [Wikipedia: International draughts](https://en.wikipedia.org/wiki/International_draughts) — правило більшості, перетворення лише в кінці ходу, нічиї.
- [Wikipedia: Turkish draughts](https://en.wikipedia.org/wiki/Turkish_draughts) — ортогональні ходи, знімання одразу, заборона розвороту на 180°.
- [Wikipedia: Poddavki](https://en.wikipedia.org/wiki/Poddavki) — піддавки.
- [Lidraughts: варіанти](https://lidraughts.org/variant) — 7 варіантів онлайн; [Russian](https://lidraughts.org/variant/russian) — повний набір правил нічиєї, вибір нотації, blind mode.
- [Wikipedia: Chinook](https://en.wikipedia.org/wiki/Chinook_(draughts_player)) — двигун, що розвʼязав 8×8 (сторінку не відкривав, лінк зі статті Draughts).
- YouTube: пошук «checkers draughts rules variants».

## Непевне
- (?) Рік 1100 — умовний (англ. draughts відомі з XII ст. за Wikipedia-статтею про English draughts, не перевіряв дослівно); предок Alquerque значно старший.
- (?) Чи автоматично застосовуються правила нічиєї в цифрових версіях (lidraughts, PlayOK) — не перевірено.
- (?) Правила Breakthrough-варіанта lidraughts (10×10, перша дамка) — лише однорядковий опис; Antidraughts — так само.
- (?) Порядок пріоритетів у Spanish/Italian/Czech — зі зведеної таблиці, деталі окремих статей не читав.
