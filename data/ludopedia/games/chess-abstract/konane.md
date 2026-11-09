---
title: Kōnane (Конане)
slug: konane
aka: [Konane, Kōnane, mū, Hawaiian checkers, Гавайські шашки]
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
year: 1778
platforms: [board, web, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Konane", best: true, note: "дошки, відкриття з двох знімань, стрибки лише по прямій, хто не може бити — програв; PSPACE-повнота, теорія комбінаторних ігор"}
  - {kind: play, url: "https://ludii.games/details.php?keyword=Konane", note: "Ludii: правила 10×10 і 8×8, перелік неповних наборів правил інших розмірів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Konane+rules+gameplay", note: "пошук; правила й партії"}
stage: v1
coverage: 75
mechanics: [piece-move-patterns, piece-capture, legal-move-highlight, no-moves-left, hot-seat, turn-enforcement, ai-opponent, ai-random, ai-greedy, ai-minimax, cell-click, drag-drop-piece, selection-highlight, last-move-highlight, field-size-picker, game-screen, main-menu, end-screen, help-window, settings-window, replay, state-as-data, unit-tests, level-solver, +forced-capture, +multi-jump, +straight-chain-only, +opening-removal, +normal-play-win]
proposes: ["+effect:jump_capture", "+cond:can_capture", "+cond:same_direction", "+effect:stop_chain", "+trigger:no_capture", "+card:straight-chain-only", "+card:opening-removal", "+card:normal-play-win"]
author: opus
date: 2026-11-09
---

# Kōnane — гавайські «шашки», де кожен хід мусить бути стрибком, і хто не може стрибнути, той програв

## Суть
Дошка повністю заповнена каменями двох кольорів у шаховому порядку; перші два ходи — зняти по одному своєму, щоб зʼявилось місце. Далі **кожен хід — взяття**: камінь стрибає ортогонально через сусідній ворожий на порожню клітину за ним; можна стрибати кілька разів, але лише **в тому самому напрямку**. Простих ходів нема зовсім, нічиєї нема: перший, хто не може бити, програє. Гра — класичний приклад «normal play» з теорії комбінаторних ігор.

## Поле і час
- Прямокутна дошка без розмітки ліній (*papa*): традиційні розміри 6×7, 8×9, 9×13, 14×17, 13×20; сучасні квадратні — від 6×6 до 14×14 і більше (Ludii: спостережений 10×10, запропонований 8×8).
- Старт: **кожна** клітина зайнята, чорні й білі чергуються як шахова розфарбовка.
- Покроково, двоє, повна інформація; хід = один камінь робить 1+ стрибків по прямій.
- Розмір поля змінює гру сильно (довжина можливих ланцюгів, парність), тому в цифровій версії розмір — головне налаштування.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Камінь | piece | сторона (чорні / білі) | лише стрибок ортогонально через сусідній ворожий камінь на порожню клітину; простого кроку нема |
| Порожня клітина | static | — | місце приземлення; на старті нема жодної |
| Центральні клітини | zone | 4 центральні (2 чорні + 2 білі навскіс) | місце першого знімання |
| Кутові клітини | zone | 4 кути дошки | друге допустиме місце першого знімання |
| Ланцюг | — | напрямок першого стрибка | наступні стрибки — лише в тому самому напрямку |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «заповнити всі клітини каменями в шаховому порядку»`.
- КОЛИ `input(remove, stone)` → ЯКЩО `turn_of(black)` і `custom: «перший хід; stone чорний, у центрі або в куті»` → ТО `disappear(stone)`, `end_turn`.
- КОЛИ `input(remove, stone)` → ЯКЩО `turn_of(white)` і `custom: «другий хід; stone білий, ортогонально суміжний з порожньою клітиною»` → ТО `disappear(stone)`, `end_turn` (тепер на дошці дві суміжні порожні).
- КОЛИ `input(jump, stone, dir)` → ЯКЩО `occupied(next_in_dir, enemy)` і `free(cell_behind)` і `custom: «dir — ортогональ, не діагональ»` → ТО `custom: «стрибок через ворожий камінь»` (`+effect:jump_capture`): `move(stone, cell_behind)`, `disappear(enemy)`.
- КОЛИ `after(jump_capture)` → ЯКЩО `occupied(next_in_dir, enemy)` і `free(cell_behind)` і `custom: «той самий напрямок, що й перший стрибок»` (`+cond:same_direction`) → ТО `choose(continue | stop)` (`+effect:stop_chain`): продовжувати не обовʼязково.
- КОЛИ `input(jump, stone, dir2)` → ЯКЩО `custom: «dir2 ≠ напрямок першого стрибка цього ходу»` → ТО `block`.
- КОЛИ `input(move, stone, to)` → ЯКЩО `custom: «хід без взяття»` → ТО `block` — усі ходи мусять бути взяттями.
- КОЛИ `custom: «ланцюг зупинено або продовжити нема куди»` → ТО `end_turn`.
- Лише один камінь рухається за хід; мінімум одне взяття за хід обовʼязкове.
- КОЛИ `no_moves(side)` (жоден камінь сторони не може бити; окремо — `+trigger:no_capture`) → ТО `lose`.
- Нічиї не буває (кожен хід зменшує кількість каменів).
- Перемога: суперник не має взяття на своєму ході · Поразка: нема взяття · Рахунок: партія 1 / 0.

## Керування і ввід
- Настільна: камені/кульки на дошці з лунками, збиті знімають руками.
- (цифрова версія) Перші два ходи — клік по каменю, який знімаєш (підсвічені лише допустимі: центр/кути, потім сусіди порожньої).
- Далі клік по каменю → підсвічуються клітини приземлення **вздовж прямої** (1, 2, 3… стрибки); клік по дальній клітині виконує весь ланцюг, по ближній — зупиняє його.
- Drag-n-drop по прямій; нема кнопки «пас» — хід без взяття неможливий.

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Проти AI · Двоє за одним пристроєм · Правила · Налаштування.
- `match-setup` / `settings-window`: розмір дошки (6×6 … 14×14, прямокутні), хто чорні, рівень AI.
- `game-screen`: дошка; `turn-indicator`; `remaining-counter` (каменів у кожного); `legal-move-highlight` (клітини приземлення по прямій); `selection-highlight`; `last-move-highlight` (шлях ланцюга); `undo-button` проти AI.
- `end-screen`: «у білих нема взяття — чорні перемогли»; Реванш.
- `help-window`: відкриття з двох знімань, стрибки по прямій.
- `replay-window`: перегляд партії.
- Переходи: main-menu → match-setup → game-screen → end-screen → game-screen.

## Фічі поза полем
- `custom-difficulty` / `field-size-picker` — розмір дошки як основний параметр.
- `ai-opponent-levels`; `undo` проти AI; `replay`; `hint` (показати всі взяття).
- `mode-puzzle` — позиції з теорії комбінаторних ігор («хто виграє, якщо ходить перший?») (?).

## Варіації й родичі
- Розміри дошки (квадратна / прямокутна, парна / непарна), 1×n — окремо досліджувана вироджена версія.
- Родичі: шашки (`checkers.md`, стрибок-взяття, але є прості ходи й зміна напрямку ланцюга), Fanorona (`fanorona.md`, взяття наближенням/відходом), mū tōrere, leap frog, пег-солітер (самотня версія «лише стрибки»), main cuki.
- Halma / китайські шашки (`halma-chinese-checkers.md`) — стрибки без взяття, ланцюг будь-куди.
- **Осі варіацій**: простий хід (нема / є) · ланцюг (лише прямо / з поворотами) · ланцюг обовʼязковий до кінця / за вибором · кінець (хто не може ходити — програв / виграв).

## Цікавинки для курсу
- Генератор ходів «лише стрибки по прямій» з вибором довжини ланцюга — 🌱.
- Відкриття з двох знімань з обмеженнями місця — 🌱.
- Normal-play кінець через `no_moves` без окремої перевірки виграшу — 🌱.
- Minimax / alpha-beta на 6×6–8×8: мало ходів, глибоке дерево — 🥇.
- Розвʼязувач малих дошок і порівняння парності розмірів — 🥈.
- Розкладання позиції на незалежні частини й значення комбінаторних ігор (сума ігор, nim-значення) — 👑.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ стрибок по ортогоналі · `piece-capture` · `legal-move-highlight` · `no-moves-left` ↔ хто не може бити, програв · `hot-seat`, `turn-enforcement` · `ai-opponent`, `ai-random`, `ai-greedy`, `ai-minimax` · `cell-click`, `drag-drop-piece`, `selection-highlight`, `last-move-highlight` · `field-size-picker` · `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window` · `replay`, `state-as-data`, `unit-tests` · `level-solver` ↔ розвʼязання малих дошок.
- **Нема** → пропозиції карток:
  - `+forced-capture` (див. `checkers.md`) — тут крайній випадок: інших ходів нема взагалі.
  - `+multi-jump` (див. `checkers.md`) — тут з обмеженням напрямку.
  - `+straight-chain-only` «Ланцюг стрибків лише по прямій» · entities/legality · 🌱.
  - `+opening-removal` «Відкриття зніманням своїх фігур» · game-logic/opponent · 🌱 · слоти {where: center|corner|adjacent}.
  - `+normal-play-win` «Хто не може ходити — програв» · game-logic/win · 🌱 (протилежність `+misere-win`).

## Пропозиції до словників
- `+effect:jump_capture` — уже в `checkers.md`; тут єдиний вид ходу.
- `+cond:can_capture` — уже в `checkers.md` / `fanorona.md`; тут збігається з `no_moves`.
- `+cond:same_direction` — крок ланцюга в тому самому напрямку, що й перший.
- `+effect:stop_chain` — уже в `fanorona.md`; добровільна зупинка ланцюга.
- `+trigger:no_capture` — у сторони нема взять (тут = нема ходів).
- `+card:straight-chain-only` · `+card:opening-removal` · `+card:normal-play-win` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Kōnane](https://en.wikipedia.org/wiki/Konane) — дошки, відкриття (центр або кут, потім сусід порожньої), стрибки лише ортогонально й по прямій, можна зупинитись, хто не може бити — програв, нічиєї нема; Hearn: PSPACE-повнота; Ernst, Chan–Tsai (1×n), Santos–Silva (нескінченна nim-вимірність); перший професійний турнір Bishop Museum (лютий 2026).
- [Ludii: Konane](https://ludii.games/details.php?keyword=Konane) — набір правил 10×10 (Kaahaina Naihe), запропонований 8×8, список неповних наборів 8×11 … 15×15.
- YouTube: пошук «Konane rules gameplay».

## Непевне
- (?) Рік 1778 — умовний: перший письмовий опис зробив Джеймс Кук під час третьої подорожі (Гаваї 1778–1779); сама гра значно старша (згадка в Kumulipo).
- (?) Чи в окремих традиціях дозволено змінювати напрямок у ланцюгу — Wikipedia і Ludii кажуть «лише той самий напрямок».
- (?) Режим задач із теорії комбінаторних ігор у цифрових версіях — не бачив, лише ідея.
