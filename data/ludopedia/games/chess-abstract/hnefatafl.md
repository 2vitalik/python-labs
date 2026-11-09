---
title: Hnefatafl (Тафл, «королівська дошка»)
slug: hnefatafl
aka: [Tafl, Viking Chess, King's Table, Copenhagen Hnefatafl, Fetlar Hnefatafl, Tablut, Brandubh, Ard Rí, Tawlbwrdd, Alea Evangelii, Тафл, Вікінгські шахи]
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
year: 400
platforms: [board, web, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hnefatafl", best: true, note: "сімʼя тафл: варіанти з розмірами й арміями, Tablut Ліннея, затискне взяття, трон, сучасні правила, баланс, історія"}
  - {kind: official, url: "http://aagenielsen.dk/copenhagen_rules.php", note: "Copenhagen Hnefatafl 11×11: трон і кути, ворожі клітини, щитова стіна, взяття короля, exit fort, оточення, повторення"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=hnefatafl", note: "пошук BGG (не відкривав)"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=hnefatafl", note: "пошук цифрових версій"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=copenhagen+hnefatafl+rules", note: "пошук; правила"}
stage: v1
coverage: 70
mechanics: [piece-move-patterns, piece-capture, impassable-cells, legal-move-highlight, selection-highlight, cell-click, drag-drop-piece, no-moves-left, repetition-draw, hot-seat, turn-enforcement, move-timer, ai-opponent, ai-minimax, rule-variants, field-size-picker, move-notation, replay, game-screen, main-menu, end-screen, help-window, settings-window, state-as-data, unit-tests, +custodian-capture, +asymmetric-sides, +king-escape-win, +hostile-squares, +restricted-squares, +shieldwall-capture, +exit-fort, +encirclement-win, +side-swap-match]
proposes: ["+cond:sandwiched", "+cond:hostile", "+cond:surrounded", "+cond:enclosed", "+trigger:sandwich", "+ui:escape-warning", "+ui:restricted-squares", "+window:side-select", "+feature:side-swap-match", "+card:custodian-capture", "+card:asymmetric-sides", "+card:shieldwall-capture", "+card:exit-fort", "+card:encirclement-win"]
author: opus
date: 2026-11-09
---

# Hnefatafl — нерівна битва: король із дружиною тікає в кут, удвічі більша облога ловить затиском

## Суть
Скандинавська сімʼя «тафл» (тафл — «дошка») — асиметричні ігри на квадратній дошці: у центрі король із захисниками, по краях удвічі більше нападників. Усі фігури ходять як тура; бʼють **затиском** — фігуру, що опинилась між двома ворожими (або ворогом і «ворожою» клітиною) по прямій. Захисники виграють, коли король доходить до кута (у старих правилах — до краю), нападники — коли ловлять короля. Справжні правила вікінгів не збереглись; сучасний стандарт — реконструкція **Copenhagen Hnefatafl 11×11**.

## Поле і час
- Copenhagen / Fetlar: 11×11; історичні: Tablut 9×9, Brandubh і Ard Rí 7×7, Tawlbwrdd 11×11, Hnefatafl 13×13 або 11×11, Alea evangelii 19×19.
- Особливі клітини: **трон** (центр) і 4 **кути** — «обмежені»: стояти на них може лише король; у Copenhagen крізь порожній трон можна проходити будь-кому.
- Ворожість: трон завжди ворожий нападникам, захисникам — лише порожній; кути ворожі всім; край дошки — не ворожий.
- Співвідношення армій ≈2:1 (нападники : захисники).
- Покроково, перші ходять нападники (Copenhagen); турніри — з годинником (Fetlar quickplay — 10 с на хід під гонг).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Король | piece | 1; сторона захисників | хід як тура; єдиний, хто стоїть на троні й кутах; бере участь у взяттях (Copenhagen) |
| Захисник | piece | ≈ половина нападників | хід як тура; бʼє затиском |
| Нападник | piece | ≈ удвічі більше | хід як тура; бʼє затиском; перші ходять |
| Трон | zone | центр; ворожий за правилом | лише король стоїть; порожній — прохідний |
| Кут | zone | 4; ворожий усім | лише король; король у куті = перемога |
| Табори нападників | zone | стартові групи біля середини країв | у частині правил закриті для короля і ворожі захисникам (?) |
| Край дошки | zone | не ворожий | щитова стіна і exit fort працюють біля нього |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, piece, to)` → ЯКЩО `turn_of(side)` і `custom: «to на тій самій лінії, усі клітини між вільні»` → ТО `move(piece, to)`; стрибків нема, діагоналей нема.
- КОЛИ `input(move, piece, to)` → ЯКЩО `custom: «to — трон або кут»` і `not same(piece, king, kind)` → ТО `block`; через порожній трон пройти можна.
- КОЛИ `after(move)` → ЯКЩО `custom: «сусідня ворожа фігура (не король) затиснута між рухомою і моєю фігурою або ворожою клітиною по прямій»` (`+cond:sandwiched`, `+cond:hostile`) → ТО `disappear_b`; кілька затисків одним ходом — усі.
- КОЛИ `input(move, piece, to)` → ЯКЩО `custom: «to між двома ворогами»` → ТО `move` дозволено і фігура **не** гине (взяття лише активним ходом).
- КОЛИ `after(move)` → ЯКЩО `custom: «король оточений нападниками з 4 боків»` (`+cond:surrounded(king, 4)`) → ТО `win` нападникам.
- КОЛИ `after(move)` → ЯКЩО `custom: «король поруч із троном, нападники з 3 інших боків»` → ТО `win` нападникам; на краю дошки короля не взяти (Copenhagen).
- Щитова стіна: КОЛИ `after(move)` → ЯКЩО `custom: «2+ фігури в ряд уздовж краю, обидва кінці затиснуті (кут може бути кінцем), перед кожною — ворог»` → ТО `disappear(усі в ряду)`, крім короля.
- КОЛИ `enter(king, corner)` → ТО `win` захисникам.
- Exit fort: КОЛИ `after(move)` → ЯКЩО `custom: «король на краю, може рухатись, а захисники навколо утворили фортецю, яку не зламати»` → ТО `win` захисникам.
- КОЛИ `after(move)` → ЯКЩО `custom: «нападники утворили суцільне кільце навколо короля і всіх захисників»` (`+cond:enclosed`) → ТО `win` нападникам.
- КОЛИ `turn_start(side)` → ЯКЩО `no_moves(side)` → ТО `lose`.
- КОЛИ `repetition` → ЯКЩО `custom: «вічне повторення»` → ТО `lose` одній зі сторін (Copenhagen — захисникам, формулювання сторінки неоднозначне (?)).
- КОЛИ `custom: «гра не може закінчитись (замало фігур в обох)»` → ТО `draw`.
- Tablut (Лінней): король перемагає на **будь-якому** краю; бʼється затиском з 2 боків поза троном; на троні — з 4; біля трону — з 3.
- Перемога: король у куті / exit fort (захисники) · король узятий / усі оточені / суперник без ходу (нападники) · Рахунок: — (матч з двох партій зі зміною сторін).

## Керування і ввід
- Настільна: фігури на клітинах, король вищий/особливий; кожна сторона — свій колір.
- (цифрова версія) Клік по своїй фігурі → підсвітка всіх клітин по 4 лініях до першої перешкоди (без трону/кутів для не-короля) → клік → автоматичне зняття затиснутих фігур з анімацією.
- Попередження «raichi» / «tuichu» (Tablut): відкрита одна / дві дороги королю до краю — як «шах» в іграх тафл.
- Вибір сторони перед партією; матч з двох партій з обміном сторін.

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Грати (AI / локально / онлайн) · Варіанти → `mode-select` · Правила → `help-window` · Налаштування.
- `mode-select`: Copenhagen 11×11 · Fetlar 11×11 · Tablut 9×9 · Brandubh 7×7 · Ard Rí 7×7 · Alea evangelii 19×19.
- `side-select` — грати за короля чи облогу (`+window:side-select`).
- `game-screen`: дошка з позначеними троном і кутами (`restricted-squares`), `turn-indicator`, `captured-pieces` обох, `player-clock`, `move-list`, `last-move-highlight`, `escape-warning` (королю відкрито шлях у кут), `resign-button`.
- `end-screen`: переможець і причина (кут / exit fort / король узятий / оточення / нема ходу); у матчі — рахунок двох партій.
- Переходи: main-menu → mode-select → side-select → game-screen → end-screen → наступна партія зі зміною сторін.

## Фічі поза полем
- `custom-rules` — набір правил: розмір дошки, кут/край як ціль, король збройний / беззбройний, ворожі табори, щитова стіна, exit fort.
- `side-swap-match` — дві партії зі зміною сторін або «торг» за сторону (хто пообіцяє виграти за менше ходів, бере короля).
- `online-multiplayer`, `turn-timer` (Fetlar quickplay: 10 с на хід), `ai-opponent-levels`.
- `export-import` / `move-notation` (координати як у шахах (?)).

## Варіації й родичі
- **Tablut** (саамський, записаний Ліннеєм 1732) — 9×9, король + 8 vs 16, вихід на будь-який край; переклад 1811 вимагав 4 нападників для взяття короля, що ламало баланс.
- **Brandubh** (Ірландія) — 7×7, король + 4 vs 8; **Ard Rí** (Шотландія) — 7×7, король + 8 vs 16, вихід на край; **Tawlbwrdd** (Уельс) — 11×11; **Alea evangelii** — 19×19 (рукопис XII ст.).
- **Copenhagen** — турнірний стандарт World Tafl Federation (≈з 2013): кути, щитова стіна, exit fort, оточення; **Fetlar** — попередній стандарт (2008).
- Сучасні: The Viking Game (1981), Breakthru (флагман на «ярусній» дошці, подвійний хід), Thud (Pratchett, 8 vs 32 на восьмикутній дошці).
- Родичі: шахи (королівська фігура, хід тури), го (оточення), Ludus latrunculorum (затискне взяття), reversi (затиск → перевертання, не взяття).
- **Осі варіацій**: ціль короля (край / кут) · взяття короля (2 / 3 / 4 боки) · король бере участь у взятті (так / ні) · ворожі клітини (трон / кути / табори) · масові взяття (щитова стіна) · армії (2:1, розмір дошки).

## Цікавинки для курсу
- Асиметричні сторони з різними цілями на одному полі — 🌱 (одна гра — два різні `win`).
- Затискне взяття: після ходу перевірити 4 сусідів і клітину за кожним, з урахуванням ворожих клітин — 📎.
- Обмежені й ворожі клітини, ворожість залежить від сторони й від того, чи порожній трон — 📎.
- Взяття короля за кількістю сторін і позицією біля трону — 📎.
- Щитова стіна (масове взяття вздовж краю) — 🥉.
- Exit fort і «суцільне кільце» нападників — заливка/звʼязність з умовою «не зламати» — 🥇 (exit fort — неочевидно перевіряти автоматично).

## Мапа на каталог
- Є: `piece-move-patterns` ↔ хід тури · `piece-capture` · `impassable-cells` ↔ трон і кути для не-короля · `legal-move-highlight`, `selection-highlight`, `cell-click`, `drag-drop-piece` · `no-moves-left` ↔ нема ходу = поразка · `repetition-draw` ↔ тут повторення — поразка · `hot-seat`, `turn-enforcement`, `move-timer` · `ai-opponent`, `ai-minimax` · `rule-variants`, `field-size-picker` ↔ набори правил тафл · `move-notation`, `replay` · `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window` · `state-as-data`, `unit-tests`.
- **Нема** → пропозиції карток:
  - `+custodian-capture` «Взяття затиском з двох боків» · entities/combat · 📎 · слоти {hostile_cells, active_only: true}.
  - `+asymmetric-sides` «Сторони з різними арміями й цілями» · game-logic/goals · 🌱.
  - `+king-escape-win` «Перемога — вивести фігуру в кут/край» · goals · 🌱.
  - `+hostile-squares` «Клітина рахується ворогом для затиску» · field · 🌱.
  - `+restricted-squares` «Клітини лише для однієї фігури» — окремий випадок `impassable-cells` для типу.
  - `+shieldwall-capture` «Масове взяття ряду біля краю» · combat · 🥉.
  - `+exit-fort` «Неприступна фортеця на краю = перемога» · goals · 🥇.
  - `+encirclement-win` «Оточити всі фігури суперника» · goals · 🥉.
  - `+side-swap-match` «Матч з обміном сторін» · players · 🌱.

## Пропозиції до словників
- `+cond:sandwiched(a)` — A між двома ворогами (або ворогом і ворожою клітиною) по прямій.
- `+cond:hostile(cell, side)` — клітина діє як ворог для сторони.
- `+cond:surrounded(a, n)` — A оточений з N ортогональних боків.
- `+cond:enclosed(kind)` — сутності виду замкнені суцільним кільцем ворога.
- `+trigger:sandwich` — щойно склався затиск (подія для каскаду взяття).
- `+ui:escape-warning` — «raichi/tuichu»: відкритий шлях короля; `+ui:restricted-squares` — позначки трону/кутів.
- `+window:side-select` — вибір сторони в асиметричній грі; `+feature:side-swap-match`.
- `+card:custodian-capture`, `+card:asymmetric-sides`, `+card:shieldwall-capture`, `+card:exit-fort`, `+card:encirclement-win` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Hnefatafl](https://en.wikipedia.org/wiki/Hnefatafl) — (відкривається як стаття про тафл-ігри) таблиця варіантів з розмірами й арміями, Tablut Ліннея з усіма правилами трону, сучасні правила (кут, беззбройний король, ворожі табори), Copenhagen і Fetlar, баланс, історія, World Tafl Federation.
- [Copenhagen Hnefatafl rules](http://aagenielsen.dk/copenhagen_rules.php) — трон і кути, ворожість, затиск лише активним ходом, щитова стіна, взяття короля з 4 / 3 боків, недоторканність на краю, exit fort, оточення, повторення, нема ходу, нічия.
- BGG / Steam / YouTube — пошукові сторінки.

## Непевне
- (?) Точні армії Copenhagen (звично 24 нападники vs 12 захисників + король) — сторінка правил дає лише «2:1» і діаграму.
- (?) Правило повторення: сторінка Copenhagen пише «perpetual repetition — loss for White», що суперечить кольорам; хто саме програє — неясно.
- (?) Табори нападників (заборона для короля, ворожість) — з «сучасних правил» у Wikipedia; чи вони в Copenhagen — не перевірено.
- (?) `year: 400` — умовно (Wikipedia: ~4–11 ст.; правила hnefatafl не записані).
- (?) Чи кути прохідні для інших фігур (не стояти, а пройти) — сторінка не каже окремо; за геометрією кут — кінець лінії, тож питання майже не виникає.
