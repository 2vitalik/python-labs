---
title: Dynamo chess (Динамо-шахи)
slug: dynamo-chess
aka: [Dynamoschach, Динамо-шахи]
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
year: 1968
platforms: [board]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dynamo_chess", best: true, note: "push/pull замість взяття, стаціонарні ходи, пішаки, шах як загроза виштовхування, нотація /E, варіанти"}
  - {kind: wiki, url: "https://de.wikipedia.org/wiki/Hans_Klüver", note: "автор (DE-вікі): Doppelzugschach і Dynamoschach; лише сніпет пошуку"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Dynamo+chess+variant", note: "пошук; відео не перевіряв"}
stage: v1
coverage: 60
mechanics: [piece-move-patterns, push-object, pull-object, no-move-into-check, check-stalemate, checkmate, pawn-promotion, castling, en-passant, move-notation, legal-move-highlight, selection-highlight, cell-click, drag-drop-piece, hot-seat, turn-enforcement, game-screen, end-screen, help-window, state-as-data, unit-tests, +push-off-capture, +no-capture-rule, +push-own-piece, +stationary-push, +pull-off-kamikaze, +no-immediate-undo, +edge-threat-check, +move-opponent-piece]
proposes: ["+effect:push_off(b)", "+cond:away_from(a, b)", "+cond:undoes_last(move)", "+ui:off-board-ring", "+ui:dynamo-arrows", "+card:push-off-capture", "+card:stationary-push", "+card:pull-off-kamikaze", "+card:no-immediate-undo", "+card:edge-threat-check"]
author: opus
date: 2026-11-09
---

# Dynamo chess — шахи без взяття: фігуру можна лише виштовхнути чи витягнути за край дошки

## Суть
Звичайна дошка, фігури й розстановка шахів, але **взяття нема**: замість нього фігура штовхає іншу (свою чи чужу) або тягне її за собою. Фігура зникає, лише коли її виштовхнули чи витягли **за край** дошки. Тому центр безпечний, а край — небезпечний; шах — це загроза виштовхнути короля. Придумали шахові композитори Ганс Клювер і Петер Каль (1968) за мотивами Push chess Фреда Гелвіна (1967).

## Поле і час
- Дошка 8×8, стартова позиція шахів ([chess.md](chess.md)); поза дошкою — умовна клітина **E** («за краєм»), куди фігура зникає.
- Хід = звичайний хід без взяття **або** динамо-хід (push / pull); за хід рухається щонайбільше **одна** «чужа для ходу» фігура.
- Черга, годинник — як у шахах; інформація повна, випадковості нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ферзь, тура, слон | piece | slider | ходять як у шахах; хід на зайняту клітину штовхає фігуру в тому ж напрямку **на ту саму відстань**; хід «від» фігури тягне її на свою стартову клітину |
| Король | piece | royal; leaper | динамо-ходи можна, але не можна вийти за край під час pull; шах = загроза виштовхування/витягування |
| Кінь | piece | leaper | динамо-ходи можна; приклад стаціонарного ходу Nb1/Bc3d5 — кінь лишився, слон зсунувся на «кінський» вектор |
| Пішак | piece | leaper; лише вперед | тягнути не може; хід уперед на 1/2 штовхає **свою** фігуру на ту саму відстань; бʼє-штовхає ворожу на 1 по діагоналі вперед (там, де в шахах узяв би) |
| Край дошки (E) | zone | 8×8 периметр | фігура, що пішла за край, знімається з гри — єдиний спосіб «взяття» |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move(piece, to))` → ЯКЩО `free(to)` and `legal(move)` → ТО `move(piece, to)` — звичайний хід без взяття.
- КОЛИ `contact(slider, b)` (хід на зайняту клітину, будь-якого кольору) → ЯКЩО `free(path)` and `custom: «клітини, які пройде b у тому ж напрямку на ту саму відстань, вільні або за краєм»` → ТО `push` (b на відстань ходу), `move(slider, b_start)`; інакше `block`.
- КОЛИ `edge(b)` → ТО `disappear(b)` — фігура виходить з гри.
- КОЛИ `input(move(piece, away))` → ЯКЩО `custom: «b стоїть на продовженні лінії позаду piece, між ними порожньо, клітини руху вільні або за краєм»` → ТО `move(piece)`, `pull` (b лягає на стартову клітину piece).
- КОЛИ `edge(piece)` під час pull → ТО `disappear(piece)`, `disappear(b)` — «камікадзе»: обидві фігури знято.
- КОЛИ `edge(king)` під час pull → ТО `block` — королю так не можна.
- КОЛИ `input(stationary(piece, b))` → ТО `custom: «piece лишається на місці — а b зсувається чи тягнеться так, ніби piece зробив хід»` (у Push chess таких ходів нема).
- КОЛИ `input(move(pawn, fwd 1|2))` → ЯКЩО `occupied(to, own_piece)` → ТО `push` (своя фігура на ту саму відстань уперед); пішак `pull` — `block`.
- КОЛИ `contact(pawn, enemy)` по діагоналі вперед → ТО `push` (на 1 по діагоналі).
- КОЛИ `reach(pawn, start_rank)` (його відштовхнули назад) → ТО `set_state(pawn, double_step)` — знову може піти на 2.
- КОЛИ `reach(pawn, last_rank)` (і коли його туди заштовхали) → ТО `choose(Q|R|B|N)` гравцем, що зробив хід → `transform(pawn, choice)`.
- Анти-«пінг-понг»: КОЛИ `input(dynamo)` → ЯКЩО `custom: «хід просто скасовує попередній хід»` → ТО `block`.
- Рокіровка: не динамо-хід; ЯКЩО `custom: «король і тура ніколи не ходили самі — їх лише штовхали/тягли й повернули на місце»` → ТО рокіровка дозволена.
- Шах: умова `in_check(side)` тут = `custom: «короля можна виштовхнути чи витягнути за край наступним ходом суперника»`; КОЛИ `check` → ТО `message(«шах»)`.
- КОЛИ `input(dynamo)` → ЯКЩО `in_check(side)` → ТО `block` — від шаху не можна рятуватися динамо-ходом; так само не можна динамо-ходом поставити свого короля під шах чи провести короля через шах.
- КОЛИ `no_moves(side)` → ЯКЩО `in_check(side)` → ТО `lose(side)` (мат).
- КОЛИ `no_moves(side)` → ЯКЩО not `in_check(side)` → ТО `draw` (пат).
- Варіант «en passant»: КОЛИ `custom: «пішак на крайній вертикалі щойно пішов на 2»` → ЯКЩО `custom: «ворожий пішак міг би взяти його на проході»` → ТО `push` за край.
- Варіант «owner promotion»: перетворення обирає власник пішака, а не той, хто штовхав.
- Перемога: мат. · Нічия: пат (решта — як у шахах (?)). · Рахунку нема.

## Керування і ввід
- Нотація: звичайна алгебраїчна + `/` і кінцеве поле штовхнутої/витягнутої фігури; `E` — за краєм: `Ra1a5/Ba5E` — тура з a1 виштовхує слона з a5 за дошку; стаціонарний — `Nb1/Bc3d5`.
- Цифрова версія (?): клік фігури → підсвітка трьох видів цілей (звичайний хід / push / pull) → для pull і стаціонарних — другий клік по фігурі-цілі; превʼю, куди полетить ціль (стрілка до краю).

## Вікна, меню, HUD
- (цифрова версія — офіційної не знайдено)
- `game-screen`: дошка 8×8 з підсвіченим периметром-зоною «E»; `legal-move-highlight` з різними маркерами для push/pull; `dynamo-arrows` — стрілка «куди піде штовхнута фігура»; `move-list` з нотацією `/E`; `captured-pieces` — виштовхнуті.
- `confirm-dialog`-подібний вибір фігури перетворення (може зʼявитися й у суперника, якщо його пішака заштовхали).
- `help-window`: push, pull, стаціонарний хід, шах як загроза краю.
- `end-screen`: мат / пат.

## Фічі поза полем
- `hotseat` (настільна гра); варіанти правил (en passant для крайнього пішака, owner promotion) — `custom-rules`.
- Виникли в шаховій композиції (Märchenschach): задачі «мат у N» з динамо-ходами (?).

## Варіації й родичі
- Push chess (Fred Galvin, 1967) — предок: штовхання без стаціонарних ходів.
- Сусіди корпусу: [abalone.md](abalone.md) (виштовхування за край як єдине взяття), [kamisado.md](kamisado.md) (sumo-поштовх), [chess-rule-twists.md](chess-rule-twists.md) (Avalanche — штовхнути ворожого пішака після ходу), [djambi.md](djambi.md) (переставляння чужих фігур замість взяття).
- **Осі варіацій**:
  - як знімають фігуру: взяттям (шахи) / виштовхуванням за край (Dynamo, Abalone) / трупом на дошці (Djambi);
  - push: на 1 / на ту саму відстань, що пройшов штовхач (Dynamo) / ланцюг більшістю (Abalone);
  - pull: нема / є, з «камікадзе» за край;
  - чи можна штовхати свої — так (Dynamo) / ні;
  - чи рухається штовхач — завжди (Push chess) / можна стояти (Dynamo).

## Цікавинки для курсу
- Push на ту саму відстань, з перевіркою шляху й «посадкової смуги» за ціллю (можна за край) — 🥉.
- Pull: фігура позаду лягає на стартову клітину рухомої; «камікадзе», коли рухома йде за край — 🥉.
- Шах як «чи може суперник виштовхнути короля» — генерація всіх динамо-ходів суперника — 🥇 (як `check-stalemate`, але з новою моделлю загрози).
- Заборона рятуватися від шаху динамо-ходом + заборона ходу, що скасовує попередній — 🥈 (історія ходів у легальності).
- Нотація `Ra1a5/Ba5E` — парсер і генератор — 📎.
- Перетворення пішака, якого заштовхав суперник: хто обирає фігуру — перемикач правил — 🌱.

## Мапа на каталог
- Є: `piece-move-patterns` · `push-object` ↔ push · `pull-object` ↔ pull · `no-move-into-check` + `check-stalemate` + `checkmate` · `pawn-promotion` (зокрема заштовханого) · `castling` (з умовою «не ходили самі») · `en-passant` ↔ варіант для крайнього пішака · `move-notation` ↔ `/` і `E` · `legal-move-highlight` + `selection-highlight` + `cell-click` + `drag-drop-piece` · `hot-seat` + `turn-enforcement` · `game-screen` / `end-screen` / `help-window` · `state-as-data` + `unit-tests`.
- **Нема** → пропозиції карток:
  - `+push-off-capture` (див. abalone) — тут фігура однієї штовхальної дії, а не більшість.
  - `+no-capture-rule` «Взяття нема: ворожа клітина = поштовх» · entities/combat · 🌱 · слот {replace_with: push|pull|block}.
  - `+push-own-piece` «Штовхати можна й свої» · entities/legality · 🌱.
  - `+stationary-push` «Поштовх без руху штовхача» · entities/legality · 📎.
  - `+pull-off-kamikaze` «Pull за край знімає обох» · entities/combat · 📎.
  - `+no-immediate-undo` «Не можна просто скасувати попередній хід» · game-logic/constraints · 📎 · слот {depth: 1}.
  - `+edge-threat-check` «Шах = загроза виштовхнути короля» · game-logic/constraints · 🥇.
  - `+move-opponent-piece` (див. chess-rule-twists) — динамо-хід рухає ворожу фігуру.

## Пропозиції до словників
- `+effect:push_off(b)` — поштовх, що виводить B за край (окремо від `push`, бо дає «взяття»).
- `+cond:away_from(a, b)` — A рухається строго від B по одній лінії (умова pull).
- `+cond:undoes_last(move)` — хід відтворює позицію до попереднього ходу (анти-пінг-понг).
- `+ui:off-board-ring` — підсвічений периметр «за краєм» як ціль ходу; `+ui:dynamo-arrows` — стрілка, куди полетить штовхнута/витягнута фігура.
- `+card:push-off-capture`, `+card:stationary-push`, `+card:pull-off-kamikaze`, `+card:no-immediate-undo`, `+card:edge-threat-check`.

## Джерела
- ⭐ [Wikipedia: Dynamo chess](https://en.wikipedia.org/wiki/Dynamo_chess) — автори й рік, Push chess Гелвіна, push/pull, «лише одна фігура за хід», стаціонарні ходи, пішаки, рокіровка, шах і заборони, нотація з `E`, варіанти en passant і owner promotion; стаття з позначкою «спирається на первинні джерела».
- [DE-Wikipedia: Hans Klüver](https://de.wikipedia.org/wiki/Hans_Klüver) — лише сніпет пошуку: Клювер розробив Doppelzugschach і Dynamoschach.
- YouTube: [пошук «Dynamo chess variant»](https://www.youtube.com/results?search_query=Dynamo+chess+variant).

## Непевне
- (?) Точна геометрія динамо-ходів коня й короля (на який вектор штовхають і чи можуть тягнути) — Wikipedia каже лише «можуть»; приклад `Nb1/Bc3d5` — єдиний.
- (?) Стаціонарний pull — як саме виглядає, у джерелі не описано.
- (?) Чи правила нічиєї (50 ходів, повторення) — як у шахах; у джерелі згадано лише пат.
- (?) Цифрових реалізацій (Fairy-Stockfish, pychess тощо) не знайдено; вікна вище — проєкція.
- (?) Задачі «мат у N» у Dynamo-композиції — з контексту «композитори-автори», прикладів не бачив.
- (?) Сторінка Chess Variant Pages про Dynamo не відкривається агентам (403) — не перевірено.
