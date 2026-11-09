---
title: Congo (шахи «Конго»)
slug: congo
aka: [Конго, Congo chess]
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
year: 1982
platforms: [board, web, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Congo_(chess_variant)", best: true, note: "дошка 7×7, ріка, замки левів, усі 8 фігур з ходами, утоплення, мавпа, перемога взяттям лева"}
  - {kind: official, url: "http://www.mindsports.nl/index.php/side-dishes/interesting-games?start=2", note: "MindSports (Freeling) — офіційна сторінка (лінк зі статті, не відкривав)"}
  - {kind: other, url: "http://www.chessvariants.org/ms.dir/congo.html", note: "Chess Variant Pages (лінк зі статті)"}
  - {kind: other, url: "http://www.gamerz.net/pbmserv/congo.html", note: "Help for Congo — правила для гри поштою (лінк зі статті)"}
  - {kind: bgg, url: "https://www.boardgamegeek.com/boardgame/18813", note: "BGG (лінк зі статті)"}
  - {kind: play, url: "https://alligatorventures.itch.io/congo", note: "грати (itch.io, лінк зі статті)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=congo+chess+variant", note: "пошук; огляд правил"}
stage: v1
coverage: 60
mechanics: [piece-move-patterns, piece-capture, pawn-promotion, legal-move-highlight, drag-drop-piece, cell-click, hot-seat, ai-opponent, floor-types, environment-death, move-notation, game-screen, end-screen, help-window, codex-window, +king-capture-win, +palace-zone, +facing-kings, +multi-jump, +delayed-drowning, +blockable-leap, +zone-bound-move]
proposes: ["+cond:in_zone", "+cond:reachable_by", "+effect:jump_capture", "+trigger:capture_chain_end", "+ui:drown-warning", "+card:delayed-drowning", "+card:zone-bound-move", "+card:river-board"]
author: opus
date: 2026-11-09
---

# Congo — дитячі «шахи джунглів» 7×7: ріка топить фігури, мавпа бʼє серією стрибків, перемога — взяти лева

## Суть
Варіант шахів, який 1982 року вигадав майже восьмирічний Деміан Фрілінг (батько — геймдизайнер Christian Freeling підказав формат 7×7). Сім типів тварин з власними ходами, посередині ріка, лев замкнений у своєму замку 3×3. Шаху й мату нема: виграє той, хто **візьме** лева; пат не рятує. Корпусу цікаві три речі: клітини-ріка з відкладеною смертю, мавпа з ланцюгом стрибкових взяттів (як дамка в шашках) і лев, що бʼє лева через ріку «на льоту» (як генерали в сянці).

## Поле і час
- Дошка 7×7; середній (4-й) ряд — ріка; у кожної сторони замок 3×3 біля свого краю (центр — файл d).
- Розстановка першого ряду (a→g): жирафа, мавпа, слон, лев, слон, крокодил, зебра; другий ряд — 7 пішаків.
- Білі ходять першими; черга без пасу; один хід = одна фігура (мавпа може зробити кілька стрибків у межах ходу).
- Шару «ріка» — властивість клітин: фігура, що закінчила хід у ріці, має покинути її наступним своїм ходом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Лев | piece | 1 на сторону; ціль суперника | ходить як король, але не виходить зі свого замку; бʼє ворожого лева як ферзь по відкритій вертикалі чи діагоналі через ріку |
| Зебра | piece | — | ходить і бʼє як шаховий кінь |
| Слон (Elephant) | piece | — | 1 крок ортогонально або 2 по прямій зі стрибком через середню клітину (зайняту чи ні); ходить і бʼє однаково; може переходити ріку |
| Жирафа | piece | — | 1 крок у будь-який бік **без** взяття; або хід/взяття на 2 по прямій (ортогональ/діагональ) зі стрибком |
| Мавпа | piece | — | 1 крок у будь-який бік без взяття; бʼє стрибком через сусідню ворожу фігуру на порожню клітину за нею; кілька стрибків за хід зі зміною напрямку |
| Крокодил | piece | — | 1 крок у будь-який бік (хід і взяття); вздовж вертикалі до ріки — як тура (включно з входом у ріку); у ріці — як тура вздовж ріки; не тоне |
| Пішак | piece | 7 на сторону | хід і взяття на 1 вперед або по діагоналі вперед; за рікою — ще 1 або 2 назад прямо без взяття |
| Суперпішак | piece | з перетворення | як пішак + крок убік і відступ на 1–2 назад прямо чи по діагоналі без взяття — незалежно від положення |
| Ріка | terrain | 4-й ряд, 7 клітин | хто закінчив хід тут (крім крокодила) і не вийшов наступним ходом — тоне |
| Замок | zone | 3×3, по одному на сторону | межа руху лева |

## Правила (КОЛИ → ЯКЩО → ТО)
Рух і взяття:
- КОЛИ `input(move(p, to))` → ЯКЩО `custom: «to досяжна за патерном p»` (кандидат `+cond:reachable_by`) and `free(to)` → ТО `move(p, to)`, `end_turn`.
- КОЛИ `contact(p, enemy)` → ЯКЩО `custom: «патерн p дозволяє взяття цим ходом»` → ТО `disappear_b`; інакше `block` (жирафа на 1 крок, мавпа кроком, пішак назад — без взяття).
- Слон, жирафа: стрибок на 2 — середня клітина не заважає (родич `+card:blockable-leap`, але без блоку).
- КОЛИ `input(move(lion, to))` → ЯКЩО `not custom: «to всередині свого замку»` (кандидат `+cond:in_zone`) → ТО `block`.
- КОЛИ `line_of_sight(lion, enemy_lion)` → ЯКЩО `custom: «по вертикалі чи діагоналі, усі клітини між ними порожні»` → ТО `input(capture)` дозволений: `move(lion, enemy_lion)`, `disappear_b`, `win`.
- КОЛИ `input(move(crocodile, to))` → ЯКЩО `custom: «to на тій самій вертикалі в бік ріки або в ріці, шлях вільний»` → ТО `move(crocodile, to)`; у ріці — як тура вздовж ряду ріки.
- КОЛИ `input(move(pawn, back))` → ЯКЩО `custom: «пішак уже за рікою»` and `free(path)` → ТО `move(pawn, 1|2 назад)` без взяття.
- КОЛИ `reach(pawn, last_rank)` → ТО `transform(superpawn)`.

Мавпа:
- КОЛИ `input(jump(monkey, over))` → ЯКЩО `adjacent(monkey, enemy)` and `free(cell_beyond)` and `custom: «цього ворога ще не перестрибували в цьому ході»` → ТО `move(monkey, cell_beyond)`, `custom: «позначити ворога; можна стрибати далі в будь-якому напрямку»`.
- КОЛИ `custom: «гравець закінчив серію стрибків»` → ТО `disappear(усі перестрибнуті)`, `end_turn` — фігури знімаються лише після всієї серії.
- Взяття мавпою (і загалом) необовʼязкове; серію можна обірвати будь-коли.
- Стрибнувши на ворожого лева мавпа його бере — `win` (?).

Ріка (утоплення):
- КОЛИ `turn_end(side)` → ЯКЩО `custom: «фігура p цієї сторони стояла в ріці вже на початку цього ходу і досі в ній»` and `not crocodile` → ТО `disappear(p)` — відкладена смерть, кандидат `+card:delayed-drowning`.
- КОЛИ `enter(p, river)` → ТО `set_state(p, wet)`; КОЛИ `leave(p, river)` → ТО `clear_state(p, wet)`.
- Мавпа проходить крізь ріку серією стрибків без штрафу; тоне, лише якщо закінчила в ріці два свої ходи поспіль; взяття до утоплення лишаються.

Кінець:
- КОЛИ `destroyed(enemy_lion)` → ТО `win` — гра закінчується одразу.
- Лев може ставати під удар; уникати «шаху» не обовʼязково; пат — не нічия: хто не має безпечного ходу, просто програє.
- КОЛИ `count(pieces, ==, 2)` → ЯКЩО `custom: «лишились два леви й жоден не бʼє іншого одразу»` → ТО `draw`.
- Лев + будь-яка фігура (навіть пішак) виграє проти голого лева, якщо той не бʼє лева одразу.
- Перемога: взяти лева · Нічия: два голі леви.

## Керування і ввід
- Цифрова версія: клік/drag фігури на клітину; мавпа — послідовні кліки по клітинах приземлення, потім «завершити хід» (або подвійний клік).
- Підсвітка легальних ходів важлива: у кожної тварини свій патерн, частина кроків — без взяття.

## Вікна, меню, HUD
- `game-screen` (цифрова версія): дошка 7×7, підсвічена ріка й обидва замки; `legal-move-highlight`; `drown-warning` — позначка на фігурах, що втонуть, якщо не вийдуть цього ходу; `turn-indicator`; `captured-pieces`.
- `codex-window` — сім тварин з діаграмами ходів (ключ до гри для новачка).
- `help-window` — правила; `end-screen` — «лев узятий» / нічия.
- Переходи: main-menu → match-setup (людина/AI) → game-screen → end-screen.

## Фічі поза полем
- `hotseat`, `ai-opponent-levels` (програма Ed Friedlander, itch-версія) (?).
- `export-import` — нотація ходів як у шахах (a–g, 1–7) (?).
- `rules-page` / `codex` — для дитячої аудиторії, на яку гра й розрахована.

## Варіації й родичі
- [jungle.md](jungle.md) — Доушоуці: тварини, ріка, лігво; Congo — «шахова» версія тієї ж ідеї.
- [xiangqi.md](xiangqi.md) / [janggi.md](janggi.md) — палац для правителя, ріка, генерали «бачать» один одного через відкриту лінію.
- [checkers.md](checkers.md) / [checkers-variants.md](checkers-variants.md) — серія стрибкових взяттів із зняттям у кінці (мавпа).
- [chess.md](chess.md) — база; [chess-rule-twists.md](chess-rule-twists.md) — «взяття короля замість мату» в Duck/Dark.
- **Осі варіацій**:
  - **Ріка**: просто межа (сянці) · вода, у яку не можна (Jungle) · вода з відкладеним утопленням (Congo).
  - **Правитель**: вільний король · у палаці (сянці, Congo) · бʼє правителя через відкриту лінію (сянці — заборона, Congo — взяття).
  - **Взяття**: заміщенням · стрибком через ворога (мавпа, шашки) · серією стрибків.
  - **Ціль**: мат · взяття правителя.

## Цікавинки для курсу
- Сім патернів тварин як дані (крок/стрибок, хід ≠ взяття) — 🥉.
- Замок як зона, що обмежує одну фігуру — 🌱.
- Утоплення з відкладеною смертю: стан «мокрий» з лічильником ходів, виняток для крокодила й мавпи — 📎.
- Мавпа: серія стрибків зі зміною напрямку, кожного ворога раз, зняття наприкінці — 🥉 (DFS по варіантах серії).
- Лев бʼє лева «на льоту» через ріку — 🌱 поверх перевірки лінії.
- AI для Congo: оцінка без шаху (лева можна підставити) — 🥈.

## Мапа на каталог
- Є: `piece-move-patterns` · `piece-capture` · `pawn-promotion` ↔ суперпішак · `legal-move-highlight` · `drag-drop-piece` · `cell-click` · `hot-seat` · `ai-opponent` · `floor-types` ↔ ріка · `environment-death` ↔ утоплення · `move-notation` · `game-screen` · `end-screen` · `help-window` · `codex-window` ↔ довідник тварин.
- **Нема** → пропозиції карток:
  - `+delayed-drowning` «Клітина вбиває, якщо лишився на ній довше одного ходу» · entities/death · 📎 · слоти {grace_turns: 1|2, immune: [crocodile]}.
  - `+zone-bound-move` «Фігура не може покинути свою зону» · entities/legality · 🌱 — замок лева, палац сянці.
  - `+river-board` «Ріка посеред дошки змінює ходи фігур» · entities/legality · 📎 — Congo, сянці, Jungle.
  - `+king-capture-win`, `+palace-zone`, `+facing-kings`, `+multi-jump`, `+blockable-leap` — див. [chess-rule-twists.md](chess-rule-twists.md), [xiangqi.md](xiangqi.md), [checkers.md](checkers.md).

## Пропозиції до словників
- `+cond:in_zone(cell, zone)` — клітина належить зоні (замок лева, палац, ріка).
- `+cond:reachable_by(p, to)` — підтверджую з [capablanca-chess.md](capablanca-chess.md): кожна тварина — свій патерн.
- `+effect:jump_capture(a, over)` — стрибок через ворога зі зняттям (мавпа, шашки); тут зняття відкладене до кінця серії.
- `+trigger:capture_chain_end` — гравець завершив серію стрибків (момент зняття взятих).
- `+ui:drown-warning` — позначка «втоне наприкінці цього ходу».
- `+card:delayed-drowning` · `+card:zone-bound-move` · `+card:river-board` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Congo (chess variant)](https://en.wikipedia.org/wiki/Congo_(chess_variant)) — автор і рік, дошка, розстановка, ходи всіх фігур, утоплення, мавпа, перемога, нічия двох левів, Pritchard 1994/2007.
- [MindSports](http://www.mindsports.nl/index.php/side-dishes/interesting-games?start=2) · [Chess Variant Pages](http://www.chessvariants.org/ms.dir/congo.html) · [Gamerz: Help for Congo](http://www.gamerz.net/pbmserv/congo.html) · [BGG](https://www.boardgamegeek.com/boardgame/18813) · [itch.io](https://alligatorventures.itch.io/congo) — лінки зі статті, сам не відкривав.
- YouTube: пошук «congo chess variant».

## Непевне
- (?) Чи може мавпа завершити серію стрибком на лева (і чи тоді гра закінчується до зняття інших) — у статті прямо нема.
- (?) Точний момент утоплення: «наприкінці того ходу», коли фігура мала вийти, — переказано як `turn_end` власника.
- (?) Розміщення замку (файли c–e, ряди 1–3) — з діаграми за памʼяттю, у тексті лише «3×3».
- (?) Подвійний відступ пішака за рікою — чи потрібна вільна проміжна клітина.
- (?) Рівні AI й нотація цифрових версій — не перевіряв.
