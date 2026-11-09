---
title: Block Blast! (і родина 1010! / Woodoku)
slug: block-blast
aka: [Block Blast, 1010!, Woodoku, block puzzle, «блок-пазл»]
family: falling-match
also: [board-digital]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: runtime
  goal: score
year: 2022
platforms: [iOS, Android, web]
links:
  - {kind: other, url: "https://blockblast-free-nocms-publish.pages.dev/wiki/how-to-play-blockblast", best: true, note: "неофіційний гайд: 8×8, рука з 3 фігур, без поворотів, рядок/стовпчик, комбо і стрік, кінець гри"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Block_Blast!", note: "Hungry Studio, релізи 2022, режими Classic і Adventure, монетизація рекламою"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Zynga", note: "Gram Games — автори 1010! (придбані Zynga 2018)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=block+blast+gameplay", note: "пошук; геймплей"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=woodoku+gameplay", note: "пошук; варіант з квадратами 3×3"}
stage: v1
coverage: 75
mechanics: [polyomino-placement, multi-cell-size, drag-drop-piece, no-moves-left, event-points, combo-multiplier, score-records, popup-text, pocket, game-screen, end-screen, main-menu, mode-select, sound-effects, background-music, save-progress, +line-clear, +hand-of-pieces, +streak-bonus, +fit-anywhere-check]
proposes: ["+trigger:hand_empty", "+effect:deal", "+card:hand-of-pieces", "+card:streak-bonus", "+card:fit-anywhere-check", "+feature:revive-offer"]
author: opus
date: 2026-11-09
---

# Block Blast! — став фігури з руки на 8×8 без падіння й поворотів; повний рядок або стовпчик зникає

## Суть
Гравцеві дають 3 поліоміно; кожне треба перетягнути на поле 8×8 так, як воно є, — повертати не можна. Повний рядок **або** стовпчик зникає (кілька одночасно — більше очок), серія ходів зі зчищенням дає стрік. Коли жодна з фігур у руці не вміщується ніде на полі — кінець гри. Це «Tetris без гравітації»: падіння немає, тиск створює лише випадкова рука, яку не можна відкласти. Корінь жанру — 1010! (Gram Games), гілка з квадратами 3×3 — Woodoku.

## Поле і час
- Квадратне поле 8×8 (Block Blast, 1010!-подібні 10×10 (?)), один шар клітин: порожня / зайнята.
- Поза полем — «рука» з 3 фігур (запас, не черга: порядок викладання вільний).
- Покрокова: хід = одна викладена фігура; таймера нема («no time limit»).
- Нема гравітації: після зчищення клітини не осідають, лишаються «дірки».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фігура в руці | piece | форма-поліоміно, колір (лише косметика) | перетягується на поле; не обертається; після викладання зникає з руки |
| Рука | supply | 3 слоти | коли всі 3 викладено — нова роздача 3 випадкових фігур |
| Зайнята клітина | tile | колір фігури | нерухома; зникає лише разом із повним рядком/стовпчиком |
| Порожня клітина | — | — | місце для викладання |
| Рядок / стовпчик | zone | 8 клітин | заповнився — зчищається повністю |
| Квадрат 3×3 (Woodoku) | zone | 9 клітин, сітка 3×3 на полі 9×9 | заповнився — зчищається, як рядок (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «deal — 3 випадкові фігури в руку»`.
- КОЛИ `input(drag piece → cells)` → ЯКЩО `fits(piece, target_cells)` → ТО `place(player, piece)`, `score(n)`; інакше `block` (фігура повертається в слот руки).
- Поворот і віддзеркалення заборонені: `fits` перевіряє фігуру лише в заданій орієнтації.
- КОЛИ `after(place)` → ЯКЩО `pattern(line(8))` у рядку або стовпчику → ТО `clear(line)`; рядки й стовпчики, що заповнились одним ходом, зчищаються разом (клітина на перетині — раз).
- КОЛИ `after(clear)` → ЯКЩО `count(cleared_lines, >=, 2)` → ТО `multiplier(k)` («Double points» за 2, більший множник за 3+).
- КОЛИ `after(place)` → ЯКЩО `count(cleared_lines, >, 0)` → ТО `combo(+1)`, `score(streak_bonus)`; інакше `reset_combo` (стрік — зчищення на послідовних ходах).
- КОЛИ `custom: «рука порожня»` → ТО `custom: «deal 3»`.
- КОЛИ `after(place)` → ЯКЩО `not fits(any_hand_piece, anywhere)` → ТО `game_over`.
- Woodoku: КОЛИ `after(place)` → ЯКЩО `pattern(region_closed)` для квадрата 3×3 → ТО `clear(region)` (?).
- Перемоги нема (Classic) · Поразка: нема місця жодній фігурі руки · Рахунок: клітини + лінії × множник + стрік; порівняння з рекордом.

## Керування і ввід
- Тач / миша: drag фігури з руки на поле; під пальцем показується тінь (куди ляже) і підсвітка рядків, що зникнуть (?).
- Фігуру тягнуть зі зміщенням угору від пальця, щоб її було видно (?).
- Undo нема; порядок викладання трьох фігур — головне рішення гравця.

## Вікна, меню, HUD
- `main-menu`: Classic · Adventure → `mode-select`; налаштування.
- `game-screen`: поле 8×8; знизу `pocket` (3 фігури руки, викладені — порожні слоти); угорі `score`, `hi-score`; `popup-text` / `action-text` при комбо («Double», «Combo», «Great» (?)); `combo-meter` стріку (?).
- `end-screen`: «немає місця» → очки, рекорд, «грати ще»; пропозиція продовжити за рекламу (`game-over-continue`) (?).
- `settings-window`: звук, музика, вібрація (?).
- Adventure: `level-select` / `world-map` з рівнями-цілями (?).
- Переходи: main-menu → game-screen → (нема місця) end-screen → main-menu / нова гра.

## Фічі поза полем
- Режими: `mode-classic` (нескінченна гра на рекорд) і Adventure («numerous levels»; цілі рівнів — див. «Непевне»).
- `leaderboard-local` (рекорд), `autosave` незавершеної партії (?), офлайн-гра.
- Монетизація: реклама між партіями; `custom: «revive»` — продовження за рекламу (?).

## Варіації й родичі
- 1010! (Gram Games, 2014 (?)) — предок жанру; Woodoku (Tripledot (?)) — поле 9×9 з судоку-квадратами 3×3; безліч клонів «Block Puzzle».
- Родичі: Tetris (повні ряди, але гравітація і поворот), Blokus / Patchwork (викладання поліоміно без зчищення, `board-digital`), Lines 98 (тиск заповнення без гравітації), Drop7.
- **Осі варіацій**: поле (8×8 / 10×10 / 9×9) · що зчищається (рядок+стовпчик / + квадрат 3×3 / лише рядок) · рука (1 / 3 / черга з превʼю) · поворот (заборонено / дозволено / за бустер) · генератор руки (чисто випадковий / «милосердний», що гарантує хоч одну фігуру, що влазить (?)) · цілі (рекорд / рівні з квотами).

## Цікавинки для курсу
- Перевірка «фігура влазить хоч кудись» (усі зсуви × усі фігури руки) як умова кінця гри — 🌱.
- Зчищення рядків і стовпчиків одночасно з правильним перетином — 🌱.
- Рука з 3 фігур і нова роздача, коли рука порожня — 📎.
- Стрік і множник за кілька ліній, `popup-text` — 📎.
- Drag-n-drop з тінню і підсвіткою ліній, що зникнуть — 🥉 (снапінг до клітини, зміщення від пальця).
- Генератор руки, що не дає «нечесних» роздач (перебір: чи існує порядок викладання всіх 3) — 🥈.
- AI-підказка: найкращий порядок і місця для 3 фігур (перебір 3! × позицій з евристикою дірок) — 🥇.

## Мапа на каталог
- Є: `polyomino-placement` (викладання з перевіркою) · `multi-cell-size` · `drag-drop-piece` · `no-moves-left` (жодна фігура не влазить) · `event-points` · `combo-multiplier` · `score-records` · `popup-text` · `pocket` (рука) · `game-screen` · `end-screen` · `main-menu` · `mode-select` · `sound-effects` · `background-music` · `save-progress`.
- **Нема** → пропозиції карток:
  - `+line-clear` «Зчищення повних рядів» (як у Tetris) · game-logic/score · 📎 · слот {lines: rows|rows+cols|+boxes, gravity: none|naive}.
  - `+hand-of-pieces` «Рука з N фігур і роздача» · entities/spawn · 📎 · слот {size: 3, refill: when_empty|each_turn}.
  - `+streak-bonus` «Стрік ходів зі зчищенням» · game-logic/score · 🌱.
  - `+fit-anywhere-check` «Чи влазить фігура хоч кудись» · game-logic/lose · 🌱.

## Пропозиції до словників
- `+trigger:hand_empty` — у руці/запасі не лишилось фігур (точка нової роздачі: Block Blast, роздача карт).
- `+effect:deal` — роздати N випадкових фігур/карт із генератора в руку (Block Blast; уже просили карткові данжени, RoboRally).
- `+feature:revive-offer` — продовжити програну партію за рекламу/валюту (мобільні аркади).
- Вжито вже наявні `fits`, `place`, `pocket`, `combo` / `reset_combo`, `pattern(line(n))`, `pattern(region_closed)`.

## Джерела
- ⭐ [How to Play Block Blast (фан-вікі)](https://blockblast-free-nocms-publish.pages.dev/wiki/how-to-play-blockblast) — 8×8, 3 фігури, «You cannot rotate the blocks!», рядок/стовпчик, комбо за 2+ лінії, стрік, кінець гри.
- [Wikipedia: Block Blast!](https://en.wikipedia.org/wiki/Block_Blast!) — Hungry Studio, iOS 03.04.2022 / Android 23.09.2022, режими Classic і Adventure, реклама, офлайн.
- [Wikipedia: Zynga](https://en.wikipedia.org/wiki/Zynga) — Gram Games, «Team Behind Hit Titles Merge Dragons! and 1010!».

## Непевне
- (?) Очки за клітину/лінію і значення множників — гайд дає лише «Double points» і «Massive multiplier».
- (?) Чи живе стрік ще кілька ходів без зчищення — джерела розходяться (один гайд: скидається одразу).
- (?) Розмір поля 1010! (10×10), рік 1010! (2014), автор Woodoku (Tripledot) і правило квадратів 3×3 — з памʼяті, статті Wikipedia про 1010! нема (404).
- (?) Adventure: цілі рівнів (збір самоцвітів / очки) і карта рівнів — Wikipedia підтверджує лише назву режиму.
- (?) Revive за рекламу, тінь фігури під пальцем, зміщення фігури від пальця, вібрація — з памʼяті.
- (?) Чи генератор руки гарантує хоч одну фігуру, що влазить, — невідомо.
