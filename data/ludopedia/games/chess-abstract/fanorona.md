---
title: Fanorona (Фанорона)
slug: fanorona
aka: [Fanoron-Tsivy, Fanoron-Sivy, Фанорона]
family: chess-abstract
also: [board-digital]
klass: figure
axes:
  field: graph
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 1600
platforms: [board, web, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Fanorona", best: true, note: "дошка 9×5 з сильними/слабкими точками, паїка, взяття наближенням і відходом, серії, Telo/Dimy, розвʼязок 2007 (нічия)"}
  - {kind: play, url: "https://ludii.games/details.php?keyword=Fanorona", note: "Ludii: правила Fanorona-Tsivy, грати проти AI"}
  - {kind: other, url: "https://ludii.games/library.php", note: "бібліотека Ludii (схожі: Vela, Alquerque)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Fanorona+rules", note: "пошук; правила й партії"}
stage: v1
coverage: 70
mechanics: [piece-move-patterns, piece-capture, legal-move-highlight, cell-click, drag-drop-piece, hover-highlight, selection-highlight, last-move-highlight, hot-seat, turn-enforcement, ai-opponent, ai-minimax, destroy-all-enemies, level-solver, rule-variants, field-size-picker, game-screen, main-menu, end-screen, help-window, replay, state-as-data, unit-tests, +forced-capture, +approach-capture, +withdrawal-capture, +line-capture-run, +optional-capture-chain, +no-revisit-in-chain, +no-same-direction-twice, +strong-weak-points, +capture-type-choice]
proposes: ["+cond:can_capture", "+cond:strong_point", "+cond:visited_in_chain", "+effect:capture_line", "+effect:stop_chain", "+ui:capture-path", "+ui:capture-choice", "+card:approach-capture", "+card:line-capture-run", "+card:no-same-direction-twice"]
author: opus
date: 2026-11-09
---

# Fanorona — мадагаскарські шашки: бʼєш, підходячи до ряду ворогів або відходячи від нього, і знімаєш увесь ряд

## Суть
Двоє рухають по 22 камені по лініях дошки 9×5 — на крок до сусідньої точки. Бити можна не стрибком, а **наближенням** (зупинився впритул до ворожого каменя на лінії руху) або **відходом** (відійшов від сусіднього каменя вздовж лінії); знімається не один камінь, а весь неперервний ряд ворожих за ним. Взяття обовʼязкове, серію можна продовжувати, але не тим самим напрямком двічі і не в ту саму точку. Перемагає той, хто зняв усі камені суперника.

## Поле і час
- Дошка Fanoron-Tsivy: 9 стовпців × 5 рядів = 45 точок на перетинах ліній; камені стоять на точках, не в клітинах.
- **Сильні** точки мають діагоналі (рух у 8 напрямках), **слабкі** — лише 4 ортогональні; разом — фрагмент тетракіс-квадратної мозаїки (`field: graph`).
- Старт: 22 + 22 камені займають усі точки, крім центральної; середній ряд — по черзі чорні й білі. Білі ходять першими.
- Покроково; хід = паїка (тихий крок) або серія взяттів одним каменем.
- Складність: дерево гри ≈ 10^46, простір станів ≈ 10^21; слабко розвʼязано як нічию (Schadd et al., 2007).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Камінь | piece | сторона (білі / чорні); 22 на старті | крок на сусідню вільну точку вздовж лінії; бʼє наближенням або відходом |
| Сильна точка | static | 8 ліній | дозволяє діагональні ходи |
| Слабка точка | static | 4 лінії | лише горизонталь / вертикаль |
| Центральна точка | static | порожня на старті | єдина вільна точка → перший хід неминуче в неї |
| Ряд ворогів | zone | неперервна лінія ворожих каменів за точкою удару | знімається цілком до першої порожньої точки або свого каменя |
| Серія взяття | — | точки, які камінь уже відвідав; напрямок останнього кроку | обмежує продовження серії |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(side)` → ЯКЩО `custom: «будь-який камінь сторони може бити»` (`+cond:can_capture`) → ТО паїка `block`; дозволені лише взяття.
- КОЛИ `input(move(stone, to))` → ЯКЩО `free(to)` і `custom: «to — сусідня точка по лінії; діагональ лише з сильної точки»` (`+cond:strong_point`) → ТО `move(stone, to)`.
- Наближення: КОЛИ `after(move)` → ЯКЩО `occupied(next_in_dir, enemy)` → ТО `custom: «зняти ряд ворожих каменів, починаючи з next_in_dir, до порожньої точки або свого каменя»` (`+effect:capture_line`).
- Відхід: КОЛИ `after(move)` → ЯКЩО `occupied(prev_in_dir, enemy)` (камінь стояв поруч, і ми відійшли від нього вздовж тієї ж лінії) → ТО `custom: «зняти ряд від prev_in_dir у бік, протилежний рухові»`.
- КОЛИ `custom: «хід дає і наближення, і відхід»` → ТО `choose(approach | withdrawal)` — одне з двох, не обидва.
- КОЛИ `after(capture_line)` → ЯКЩО `custom: «той самий камінь може бити ще»` → ТО `choose(continue | stop)` — продовження необовʼязкове (`+effect:stop_chain`).
- У серії: ЯКЩО `custom: «точка вже відвідана в цій серії»` (`+cond:visited_in_chain`) → ТО `block`.
- У серії: ЯКЩО `moving(stone, dir)` і `custom: «попередній крок серії мав той самий напрямок»` → ТО `block`.
- КОЛИ `custom: «серію завершено або паїку зроблено»` → ТО `end_turn`.
- КОЛИ `all_gone(enemy_stones)` → ТО `win`.
- КОЛИ `custom: «жодна сторона не може атакувати, не послабивши себе»` → ТО `draw` за згодою.
- Перемога: зняти всі камені суперника · Поразка: втратити всі · Рахунок: партія 1 / ½ / 0.

## Керування і ввід
- Настільна: пересунути камінь по лінії, зняти ряд руками; серію грають крок за кроком.
- (цифрова версія) Клік по каменю → підсвічуються лише камені, що мусять бити, і їхні точки призначення; клік по точці виконує крок.
- Якщо крок дає і наближення, і відхід — дві стрілки / кнопки «вперед» і «назад» (`capture-choice`), бо знімаються різні ряди.
- Після взяття — підсвічені продовження серії й кнопка «завершити хід».

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Проти AI · Двоє за одним пристроєм · Правила · Налаштування.
- `settings-window` / `match-setup`: розмір (Telo 3×3, Dimy 5×5, Tsivy 9×5), рівень AI, хто ходить першим.
- `game-screen`: дошка з лініями (сильні точки з діагоналями); `turn-indicator`; `captured-pieces` / `remaining-counter` (каменів у кожного); `legal-move-highlight` (обовʼязкові взяття); `capture-path` (кроки серії); `capture-choice` (наближення / відхід); `last-move-highlight`; `end-turn-button` для обриву серії.
- `end-screen`: перемога / нічия; «Реванш».
- `replay-window`: перегляд партії по ходах.
- `help-window`: схема сильних і слабких точок, два види взяття з прикладами.
- Переходи: main-menu → match-setup → game-screen → end-screen → game-screen.

## Фічі поза полем
- `custom-rules` / `rule-variants`: Telo (3×3, як хрестики-нулики за складністю), Dimy (5×5), Tsivy (9×5).
- `ai-opponent-levels`, `undo` проти AI, `replay`, `hint`.
- `field-size-picker` — фактично вибір варіанта дошки.

## Варіації й родичі
- Розміри: Fanoron-Telo 3×3 · Fanoron-Dimy 5×5 · Fanoron-Tsivy 9×5 (основний).
- Vela — окрема гра в Ludii, повʼязана з Fanorona (?); Alquerque — родич дошки з діагоналями.
- Нащадки ідеї: Bushka К. Фрілінга (шашки з Fanorona-взяттям) → Dameo; Baroque chess (`baroque-chess.md`) має фігуру, що бʼє відходом.
- Родичі за «бʼє не так, як ходить»: шашки (`checkers.md`, стрибок), Surakarta (петлі), Ataxx (перефарбування).
- **Осі варіацій**: спосіб взяття (стрибок / наближення / відхід / оточення) · скільки знімається (одна / ряд) · серія (обовʼязкова / за вибором) · обмеження серії (без повтору точки / без того ж напрямку) · топологія (усі 8 напрямків / сильні-слабкі точки).

## Цікавинки для курсу
- Граф дошки з сильними й слабкими точками (діагоналі лише з парних точок) — 🌱.
- Генерація взяттів наближенням і відходом з рядом-«хвостом» — 📎.
- Вибір між наближенням і відходом на тому самому кроці (неоднозначний хід) — 📎.
- Серія з двома обмеженнями (не повторити точку, не той самий напрямок) і правом зупинитись — 🥉 (DFS по станах серії).
- AI minimax на 9×5 з дуже рясними взяттями на старті — 🥇.
- Розвʼязувач для Telo/Dimy повним перебором — 🥈; Tsivy — 👑 (нічия доведена лише 2007).

## Мапа на каталог
- Є: `piece-move-patterns` ↔ кроки по лініях · `piece-capture` · `legal-move-highlight` · `cell-click`, `drag-drop-piece`, `hover-highlight`, `selection-highlight`, `last-move-highlight` · `hot-seat`, `turn-enforcement` · `ai-opponent`, `ai-minimax` · `destroy-all-enemies` ↔ зняти всі камені · `level-solver` · `rule-variants`, `field-size-picker` ↔ Telo / Dimy / Tsivy · `game-screen`, `main-menu`, `end-screen`, `help-window` · `replay`, `state-as-data`, `unit-tests`.
- **Нема** → пропозиції карток:
  - `+forced-capture` (див. `checkers.md`) — взяття переважає паїку.
  - `+withdrawal-capture` (див. `baroque-chess.md`) — тут з рядом.
  - `+approach-capture` «Взяття наближенням» · entities/combat · 📎 — зупинка впритул до ворога на лінії руху.
  - `+line-capture-run` «Знімається весь ряд за першим» · entities/combat · 📎.
  - `+optional-capture-chain` «Серія взяттів за вибором» · entities/combat · 🥉 (родич `+multi-jump`, але без обовʼязку).
  - `+no-revisit-in-chain` · `+no-same-direction-twice` «Обмеження серії» · entities/legality · 📎.
  - `+strong-weak-points` «Точки з різною кількістю ліній» · entities/legality · 🌱.
  - `+capture-type-choice` «Вибір виду взяття на тому самому кроці» · interface/input · 📎.

## Пропозиції до словників
- `+cond:can_capture` — у сторони є взяття (уже в `checkers.md`; не в словнику).
- `+cond:strong_point` — точка має діагональні лінії.
- `+cond:visited_in_chain` — точку вже відвідано поточною серією.
- `+effect:capture_line` — зняти неперервний ряд ворожих сутностей від точки в напрямку.
- `+effect:stop_chain` — гравець обриває серію добровільно.
- `+ui:capture-path` (уже в `checkers.md`) · `+ui:capture-choice` — вибір між двома взяттями одного кроку.
- `+card:approach-capture` · `+card:line-capture-run` · `+card:no-same-direction-twice` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Fanorona](https://en.wikipedia.org/wiki/Fanorona) — дошка, сильні/слабкі точки, паїка, обовʼязкове взяття, наближення/відхід, ряд, обмеження серії, Telo/Dimy/Tsivy, розвʼязок, Bushka/Dameo.
- [Ludii: Fanorona](https://ludii.games/details.php?keyword=Fanorona) — правила Fanorona-Tsivy (центральний ряд чергується, серія необовʼязкова, той самий напрямок заборонено), гра проти AI.
- [Ludii: library](https://ludii.games/library.php) — каталог, схожі ігри Vela, Alquerque.
- YouTube: пошук «Fanorona rules».

## Непевне
- (?) Рік 1600 — умовний: Wikipedia наводить легенду про короля Раламбо і його синів; дата правління з памʼяті (≈ межа XVI–XVII ст.), не перевірено.
- (?) Обмеження першого ходу (за деякими джерелами перший хід обовʼязково в центр і лише одне взяття) — ні Wikipedia, ні Ludii не підтвердили.
- (?) Vela — у Ludii окрема гра; за памʼяттю, це «відкат» після поразки, де переможець спершу віддає камені, — не перевірено.
- (?) Правило нічиєї — у статті лише приклад позиції, формальних лічильників ходів нема.
- (?) Чи серія може змінити вид взяття (наближення → відхід) на наступному кроці — дозволено, якщо напрямок інший (за прикладом Wikipedia «a withdrawal followed by an approach» у тому самому напрямку заборонено).
