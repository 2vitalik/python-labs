---
title: Guerrilla Checkers
slug: guerrilla-checkers
aka: [Партизанські шашки, COIN vs Guerrilla]
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
year: 2010
platforms: [board, Ludii]
links:
  - {kind: other, url: "https://ludii.games/details.php?keyword=Guerrilla%20Checkers", best: true, note: "Ludii: правила, опис «гібрид шашок і го», автор, видавець nestorgames, лінк на BGG"}
  - {kind: other, url: "https://jpneto.github.io/world_abstract_games/guerrilla.htm", note: "правила Brian Train (2010): оточення з урахуванням краю, варіант «двічі зі зміною ролей»"}
  - {kind: bgg, url: "https://boardgamegeek.com/boardgame/71035", note: "BGG (HTML агентам не відкривається)"}
  - {kind: official, url: "https://www.nestorgames.com", note: "видавець"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Guerrilla+Checkers+Brian+Train", note: "пошук; як грати"}
stage: v1
coverage: 70
mechanics: [piece-move-patterns, piece-capture, destroy-all-enemies, hot-seat, turn-enforcement, ai-opponent, cell-click, hover-highlight, selection-highlight, legal-move-highlight, last-move-highlight, remaining-counter, game-screen, main-menu, end-screen, help-window, state-as-data, unit-tests, +asymmetric-sides, +dual-grid, +place-stone, +paired-placement, +corner-surround-capture, +multi-jump, +supply-exhaustion-loss, +side-swap-match]
proposes: ["+cond:corners_blocked", "+effect:jump_capture", "+trigger:reserve_empty", "+axis:dual-grid", "+ui:point-grid", "+ui:stone-supply", "+card:dual-grid", "+card:paired-placement", "+card:corner-surround-capture", "+card:supply-exhaustion-loss"]
author: opus
date: 2026-11-09
---

# Guerrilla Checkers — 6 шашок на клітинах проти партизанських каменів на перехрестях: одні стрибають, інші оточують

## Суть
Асиметрична гра двох «армій» на одній шахівниці, але на різних шарах. Counterinsurgent (COIN) має 6 шашок, що ходять клітинами по діагоналі, як дамки, і бʼють стрибком. Guerrilla має 66 каменів го і щоходу ставить **рівно два** на внутрішні перехрестя ліній, ланцюжком до вже поставлених; камені ніколи не рухаються. Шашку знято, коли всі чотири кути її клітини зайняті каменями або є краєм дошки. Виграє той, хто наприкінці свого ходу зачистив поле від ворога; партизан, у якого скінчились камені, програє. Автор — Brian Train (2010), видавець nestorgames.

## Поле і час
- Шахівниця 8×8; два шари однієї геометрії (`+axis:dual-grid`): **клітини** (для шашок, лише чорні в старті) і **перехрестя** ліній між клітинами (для каменів).
- Камені — лише на внутрішніх перехрестях (7×7 = 49, підрахунок; крайові точки заборонені).
- Кожна клітина має 4 кутові точки; у крайової клітини частина кутів — край дошки, і вони «рахуються як камінь» для оточення.
- Хід = дія однієї сторони; без часу. Партія асиметрична за темпом: партизан щоходу додає 2 камені, COIN рухає одну шашку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Шашка COIN | piece | ×6, старт — чорні клітини в центрі | крок на 1 клітину по діагоналі в будь-який бік; стрибком бʼє камінь |
| Камінь Guerrilla | piece | ×66 у запасі | ставиться на внутрішнє перехрестя; ніколи не рухається |
| Запас каменів | zone | 66 → 0 | порожній запас — поразка партизана |
| Клітина | terrain | 64 | шар шашок |
| Перехрестя | terrain | 49 внутрішніх | шар каменів; крайові точки заборонені для постановки, але рахуються при оточенні |
| Кути клітини | zone | 4 точки | усі 4 «закриті» (камінь або край) → шашку знято |

## Правила (КОЛИ → ЯКЩО → ТО)
- Старт: COIN ставить 6 шашок на чорні клітини в центрі (схема — в оригіналі); у партизана на полі нічого.
- Перший хід партизана: КОЛИ `input(place, point1, point2)` → ЯКЩО `custom: «point1 — будь-яке внутрішнє перехрестя»` and `custom: «point2 ортогонально поруч з point1»` → ТО `place(stone, point1)`, `place(stone, point2)`.
- Далі: КОЛИ `input(place, point1, point2)` → ЯКЩО `adjacent_count(point1, stone, >=, 1)` (ортогонально) and `custom: «point2 ортогонально поруч з point1»` and `free(point1)` and `free(point2)` → ТО `place(stone, point1)`, `place(stone, point2)`, `counter(stones, -2)`; рівно два, не один.
- КОЛИ `input(place, point)` → ЯКЩО `cell(point, edge_point)` → ТО `block`.
- КОЛИ `after(place)` → ЯКЩО `custom: «кожен з 4 кутів клітини шашки — камінь або край дошки»` (`+cond:corners_blocked`) → ТО `disappear(checker)`.
- КОЛИ `input(move, checker, diag)` → ЯКЩО `turn_of(coin)` and `free(diag_cell)` and `not occupied(crossed_point, stone)` → ТО `move(checker, diag)`.
- КОЛИ `input(move, checker, diag)` → ЯКЩО `occupied(crossed_point, stone)` and `free(diag_cell)` → ТО `custom: «стрибок через точку з каменем на діагональну клітину»` (`+effect:jump_capture`), `disappear(stone)`.
- Взяття за бажанням, але КОЛИ `after(jump_capture)` → ЯКЩО `custom: «тією самою шашкою можна бити далі»` → ТО `custom: «бити далі, доки можна — усі можливі взяття»` (серія).
- КОЛИ `turn_end(side)` → ЯКЩО `count(enemy_pieces, ==, 0)` → ТО `win`.
- КОЛИ `custom: «у партизана скінчились камені»` (`+trigger:reserve_empty`) → ТО `lose` (партизан).
- Варіант: дві партії зі зміною ролей; переможець — той, хто як партизан переміг COIN меншою кількістю каменів.
- Перемога: знищити всі ворожі фігури наприкінці свого ходу · Поразка партизана: скінчились камені · Рахунок (матч): витрачені камені.

## Керування і ввід
- Настільна: COIN пересуває шашку; партизан кладе два камені на перехрестя.
- (цифрова версія) Хід партизана — два кліки по точках: після першого підсвічуються ортогональні сусіди для другого; хід COIN — клік по шашці → підсвітка діагональних кроків і стрибків → клік; серія взяттів — ланцюжком кліків.
- Хто ходить першим, правила прямо не кажуть; опис починається з постановки партизана.

## Вікна, меню, HUD
- `main-menu` (цифрова версія): нова партія → `match-setup` (хто COIN, хто партизан; людина / AI; одна партія або матч зі зміною ролей).
- `game-screen`: шахівниця з видимою `point-grid` (точки перехресть поверх клітин), `stone-supply` (лишок 66 каменів), `remaining-counter` шашок COIN, `turn-indicator`, `legal-move-highlight` (діагоналі / сусідні точки), `threat-range` (клітини, де шашці лишився 1 відкритий кут) (?), `last-move-highlight`.
- `end-screen`: хто зачистив поле / закінчились камені; у матчі — порівняння витрачених каменів.
- `help-window`: правила і схема старту.
- Переходи: main-menu → match-setup → game-screen → end-screen (→ друга партія з іншими ролями).

## Фічі поза полем
- `ai-opponent-levels` — Ludii грає будь-яку сторону (загальні AI двіжка).
- `hotseat`; серія з двох партій зі зміною ролей.
- Видання — nestorgames (набір: дошка, 6 шашок, 66 каменів).

## Варіації й родичі
- Батьки: [checkers](checkers.md) (рух і стрибок шашок), [go](go.md) (постановка каменів, оточення); гібрид — у самому описі Ludii.
- Асиметрія «мало сильних проти багатьох слабких»: [hnefatafl](hnefatafl.md), [bagh-chal](bagh-chal.md) (тигри стрибають, кози оточують — найближчий родич), Fox and Geese.
- Два шари на одній дошці (клітини + перехрестя) — рідкість; поруч [dots-and-boxes](dots-and-boxes.md) (лінії між точками) і [quoridor](quoridor.md) (стіни в пазах між клітинами).
- Осі варіацій: **розмір дошки й запас каменів** (автор: запас залежить від дошки) · **кількість каменів за хід** (2 / 1) · **оточення** (4 кути / з краєм як союзником) · **обовʼязковість взяття** (за бажанням, але серія до кінця).

## Цікавинки для курсу
- Подвійна сітка: координати клітин і перехресть, відображення «клітина ↔ 4 кути» і «точка ↔ 4 клітини» — 📎.
- Постановка парою з умовою сусідства (до будь-якого каменя, потім до першого) — 🌱.
- Оточення 4 кутами з краєм як «каменем» — 🌱; перевірка лише клітин біля нових каменів — 📎.
- Стрибок через точку + серія взяттів «усе, що можна» (DFS по ланцюжках) — 🥉.
- AI для асиметричної гри: дві різні функції оцінки (COIN — мобільність, партизан — щільність ланцюга) — 🥇.
- Матч зі зміною ролей і рахунком «скільки каменів витрачено» — 🌱.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ діагональний крок · `piece-capture` ↔ зняття шашки й каменя · `destroy-all-enemies` ↔ перемога зачисткою · `hot-seat`, `turn-enforcement`, `ai-opponent` · `cell-click`, `hover-highlight`, `selection-highlight`, `legal-move-highlight`, `last-move-highlight` · `remaining-counter` ↔ запас каменів, шашки · `game-screen`, `main-menu`, `end-screen`, `help-window` · `state-as-data`, `unit-tests`.
- **Нема** → пропозиції карток:
  - `+asymmetric-sides` (див. hnefatafl.md) — різні фігури, шари і способи взяття.
  - `+dual-grid` «Два шари однієї сітки: клітини й перехрестя» · field · 📎.
  - `+place-stone` (див. hex.md).
  - `+paired-placement` «Хід — дві постановки ланцюжком» · entities/legality · 🌱 · слоти {n: 2, adjacency: orth}.
  - `+corner-surround-capture` «Оточення фігури каменями в кутах клітини» · entities/combat · 📎 · слот {edge_counts: true}.
  - `+multi-jump` (див. checkers.md) — тут серія необовʼязкова на старті, але повна.
  - `+supply-exhaustion-loss` «Скінчився запас — поразка» · game-logic/lose · 🌱.
  - `+side-swap-match` (див. hnefatafl.md) — дві партії зі зміною ролей.

## Пропозиції до словників
- `+cond:corners_blocked` — усі кутові точки клітини зайняті або є краєм.
- `+effect:jump_capture` — стрибок через фігуру з її зняттям (уже пропонувалось у checkers).
- `+trigger:reserve_empty` — запас сторони вичерпано (уже пропонувалось у tak).
- `+axis:dual-grid` — значення `field`: клітини й перехрестя як два шари.
- `+ui:point-grid` — видимі точки перехресть поверх клітин; `+ui:stone-supply` — лишок запасу каменів.
- `+card:dual-grid`, `+card:paired-placement`, `+card:corner-surround-capture`, `+card:supply-exhaustion-loss` — див. «Мапа на каталог».

## Джерела
- ⭐ [Ludii: Guerrilla Checkers](https://ludii.games/details.php?keyword=Guerrilla%20Checkers) — опис і правила: 8×8, 6 шашок і 66 каменів, постановка парами, заборона крайових точок, рух як дамка, взяття за бажанням, але всі можливі; перемога зачисткою; Brian Train, nestorgames, 2010.
- [World of Abstract Games: Guerrilla Checkers](https://jpneto.github.io/world_abstract_games/guerrilla.htm) — правила автора: оточення «камінь або край» у всіх 4 точках, стрибок через точку, варіант зі зміною ролей.

## Непевне
- (?) Хто ходить першим — не сказано; за порядком опису — партизан.
- (?) Точні 6 стартових клітин COIN — лише на схемі (не бачив).
- (?) Чи кожен діагональний крок через точку з каменем — це взяття, чи стрибок «через сусідній камінь» означає інше — описи кажуть «стрибнути через точку між двома клітинами»; трактую як перше.
- (?) Чи знімаються кілька шашок одним ходом партизана, якщо обидва камені закрили кути, і чи враховуються обидва камені пари разом — не сказано.
- (?) Чи може партизан поставити камінь, що одразу оточує шашку, якщо точка не поруч з ланцюгом, — ні за правилом сусідства, але перший камінь пари може бути будь-де поруч з будь-яким каменем.
- (?) `threat-range` у HUD — ідея для цифрової версії, не з джерела.
