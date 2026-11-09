---
title: Cleopatra Fortune
slug: cleopatra-fortune
aka: [クレオパトラフォーチュン, "Cleopatra's Fortune", "Cleopatra Fortune S-Tribute", "Cleopatra Fortune Plus"]
family: falling-match
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: hotseat
  info: full
  random: runtime
  goal: survive
year: 1995
platforms: [Taito X-55, arcade (Taito F3), Saturn, PlayStation, Dreamcast, mobile, PS2 (Taito Memories), Switch, PS4, Xbox One, Steam]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/クレオパトラフォーチュン", best: true, note: "JA: типи блоків, обведення з діагоналями, мумії, лінії, порядок перевірок, ланцюг ×2, perfect, Mystery Mode, Plus з предметами"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Cleopatra_Fortune", note: "версії, дати, розробники (Taito, Natsume)"}
  - {kind: steam, url: "https://store.steampowered.com/app/1913690/Cleopatra_Fortune_STribute/", note: "S-Tribute: правила коротко, rewind, slow mode, quick save, безліміт кредитів"}
  - {kind: other, url: "https://retro-replay.com/db/arcade/cleopatras-fortune", note: "огляд: endless, versus зі сміттєвими каменями, puzzle-режим"}
  - {kind: other, url: "https://www.honestgamers.com/6947/dreamcast/cleopatra-fortune/review.html", note: "огляд DC: склад формацій, мумії, perfect, темп рівнів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Cleopatra+Fortune+arcade+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [gravity-fall, multi-cell-size, piece-rotate-flip, line-match-clear, chain-reaction, combo-multiplier, event-points, progress-acceleration, next-queue, score-records, simultaneous-versus, garbage-attack, end-screen, game-over-continue, mode-select, level-bank, rewind, save-game, game-settings, +enclosure-clear, +companion-clear, +clear-phase-order, +color-clear-special, +all-clear-bonus, +split-on-landing, +chain-bonus-threshold, +portrait-reward, +gauge-item-block]
proposes: ["+cond:enclosed", "+effect:clear_color", "+card:enclosure-clear", "+card:companion-clear", "+card:clear-phase-order", "+card:chain-bonus-threshold"]
author: opus
date: 2026-11-09
---

# Cleopatra Fortune — обклади скарби каменями: замкнена область зникає, мумії йдуть лише в парі зі скарбом

## Суть
Падаюча головоломка Taito/Natsume: у колодязь падають формації з каменів, скарбів, золотих трун і мумій. Головний спосіб очищення — не збіг кольору, а **обведення**: скарб, повністю оточений каменями (діагональний дотик теж «стіна», стінки колодязя — теж камінь), зникає разом з усім, що всередині. Другий спосіб — повний горизонтальний ряд блоків одного типу, як у Tetris; мумії зникають з обведення лише тоді, коли поруч у тій самій області є скарб.

## Поле і час
- Колодязь як у Tetris: ліва, права стінки й дно; розмір у джерелах не названо (?).
- Real-time падіння формації; після приземлення — фаза розвʼязання: падіння → обведення → лінії; будь-яке очищення повертає цикл на крок «падіння» (так утворюються ланцюги).
- Рівень росте з грою: швидше падіння, більше мумій і великих блоків; мета аркади — дожити до рівня 99 і пережити ще задану кількість блоків.
- Versus — два колодязі поруч, кожен гравець свій.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Формація | player | 2–3 блоки різних типів (камінь+скарб, скарб+труна, скарб+довгий камінь, 2 скарби+камінь) | зсув, поворот, прискорене падіння; частини відокремлюються залежно від того, як покладено |
| Камінь малий | object | 1 клітина | стіна обведення; сам зникає лише лінією каменів або пірамідним каменем |
| Камінь великий | object | 2 клітини | як малий; у лінії зникає цілком, без залишку |
| Скарб (коштовність) | tile | 1 клітина | зникає в обведенні або лінією скарбів |
| Золота труна | tile | 2 клітини — «великий скарб» | як скарб, але для ліній це окремий тип: скарб + труна лінії не дають |
| Мумія мала / велика | hazard | 1 / 2 клітини | в обведенні зникає лише разом зі скарбом/труною; інакше — лише лінією мумій |
| Пірамідний камінь | object | зʼявляється зрідка | приземлився → з усього поля зникають усі блоки того типу, на який він упав |
| Стінки колодязя | static | ліва, права, дно | рахуються каменем при обведенні |
| Верх колодязя | zone | — | стек дійшов до верху → поразка |
| Сміттєвий камінь | hazard | лише versus | падає в колодязь суперника за твої зачистки |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `free(cells_below)` → ТО `move(formation, down)`; КОЛИ `input(down)` → ТО швидше падіння.
- КОЛИ `input(shift)` → ЯКЩО `free(target_cells)` → ТО `move(formation, dir)`.
- КОЛИ `input(rotate)` → ЯКЩО `free(new_cells)` → ТО `rotate(formation, 90)`.
- КОЛИ `locked(formation)` → ТО `custom: «формація розпадається на окремі блоки»`, `fall(each_block)` — до опори.
- КОЛИ `settled` → ЯКЩО `pattern(region_closed)` навколо скарбу/труни, де стіна = камені + стінки колодязя, з діагональним дотиком каменів → ТО `clear(region_contents)`; порожні клітини всередині області дозволені.
- КОЛИ `pattern(region_closed)` → ЯКЩО `count(treasure_in_region, ==, 0)` → ТО мумії в області лишаються; ЯКЩО `count(treasure_in_region, >=, 1)` → ТО `clear(mummies_in_region)` разом зі скарбами.
- КОЛИ `custom: «перевірку обведень закінчено»` → ЯКЩО `pattern(row_full)` і `same(blocks_in_row, type)` → ТО `clear(row)`; великий блок зникає цілком, якщо хоч одна його клітина в ряду.
- КОЛИ `pattern(row_full)` → ЯКЩО `not same(treasure, coffin, type)` → ТО ряд не зникає (скарби й труни в одній лінії не змішуються).
- Камінь не зникає від обведення: лише `clear(row)` каменів або пірамідний камінь.
- КОЛИ `after(clear)` → ТО `fall(all_unsupported)`, цикл знову з «падіння»; нове очищення → `combo(+1)` (крок ланцюга).
- Рахунок ланцюга: кожен крок після першого — `multiplier(×2)` до попереднього кроку; КОЛИ `counter(chain, >=, 5)` → ТО `score(chain × 100000)`.
- КОЛИ `locked(pyramid_stone)` → ТО `custom: «clear_color — з усього поля зникають усі блоки типу під пірамідним каменем, будь-якого розміру»`.
- КОЛИ `all_gone(block)` → ТО `score(level × 5000)`, `custom: «показати повну картинку Патра-ко; з кожним perfect інша»`.
- КОЛИ `counter(blocks_dropped, >=, n)` → ТО `custom: «level +1»`, `speed(formation, +n)`; з рівнем частішають мумії й великі блоки.
- КОЛИ `custom: «стек дійшов до верху колодязя»` → ТО `lose` (аркада — `window(game-over-continue)`).
- КОЛИ `level(==, 99)` → ЯКЩО `custom: «пережито ще задану кількість блоків»` → ТО `win`; без жодного continue — альтернативна кінцівка з іншим костюмом.
- КОЛИ `after(clear)` → ЯКЩО `mode(versus)` → ТО `send_garbage(stones)` — «дощ» сміттєвих каменів супернику; матч до 2 перемог.
- Перемога: рівень 99 + запас блоків (аркада), 2 раунди (versus), умова задачі (Mystery) · Поразка: стек до верху · Рахунок: очищення × множник ланцюга, бонус ≥5 ланцюгів, perfect = рівень × 5000.

## Керування і ввід
- Джойстик / хрестовина: ←/→ — зсув, ↓ — прискорення; кнопки — поворот формації (Famitsu лаяв напрям повороту в DC-версії).
- Головна навичка — класти формації так, щоб камені замикали «кімнати» навколо скарбів і водночас не зростав стек каменів, які обведенням не прибрати.
- S-Tribute: окрема кнопка slow mode; rewind і quick save/load у будь-який момент.

## Вікна, меню, HUD
- `splash-screen` → `main-menu` (домашні версії): Arcade (1P / 2P versus) · Mystery Mode · Options.
- `game-screen`: колодязь, `next-piece-preview` (форма наступної формації), `score`, `level-number`, `multiplier` (множник ланцюга), `popup-text` кроків ланцюга (?).
- 2P: два колодязі поруч; другий гравець може приєднатись (аркадний «intrusion»).
- `custom-window` «Perfect»: повна картинка Патра-ко, що змінюється з кожним perfect; після 17-го — варіації костюмів.
- `game-over-continue` (аркадні кредити) → `end-screen`; фінальна кінцівка, альтернативна — без continue.
- `puzzle-select` (S-Tribute): 50 задач Сфінкса з позначкою «пройдено», доступні незалежно від прогресу.
- `settings-window` (S-Tribute): швидкість падіння, кількість кредитів (до безліміту), scan lines.

## Фічі поза полем
- `mode-classic` (аркада до рівня 99) · `mode-versus` (2P) · `mode-puzzle` — Mystery Mode: 50 задач із заданим полем, заданою послідовністю і ціллю (прибрати всі скарби / ланцюг певної довжини); за всі — нагорода.
- `unlockables`: картинки за perfect, костюми, альтернативна кінцівка.
- S-Tribute (2022): `rewind` на фіксований відрізок часу, `snapshots` (quick save/load), `assist-mode` (slow mode, безліміт кредитів, швидкість падіння), вибір задач Mystery.
- Лічильник очок має стелю 1 млрд (counter stop) — довгі ланцюги її досягають.

## Варіації й родичі
- **Cleopatra Fortune Plus** (2002, NAOMI, Altron): Story до рівня 100 · Time Attack (10 стадій, ранг і час) · Endless · Versus з intrusion; 2 слоти NEXT.
  - Jewel Level: ланцюги ≥3 і perfect наповнюють шкалу-множник до ×5, вона спадає з часом (крім Time Attack і Versus).
  - Скарби 5 кольорів, у кожного своя шкала; повна шкала кладе блок-предмет у NEXT, обведений предмет спрацьовує: молот (усі камені), ніж (довгі камені → найменші), вогонь (усі мумії), вода (3 нижні ряди), пісочний годинник (мінімальна швидкість).
- Родичі: [tetris](tetris.md) (лінії), [puyo-puyo](puyo-puyo.md) (цикл падіння → очищення → ланцюг), [hatris](hatris.md) (очищення за типом, а не кольором), го (захоплення обведенням — `chess-abstract`).
- **Осі варіацій**: спосіб очищення (збіг кольору / лінія / обведення) · що є стіною (лише камені / + стінки поля / + діагоналі) · умовні блоки (мумія потребує скарбу) · гравітація (формація цілком / розпад на блоки).

## Цікавинки для курсу
- Обведення: 4-звʼязна заливка від скарбу крізь не-камені; дійшла до відкритого верху колодязя → не замкнено; діагональні камені «тримають» стіну самі собою — 🥉 (flood fill + правильне визначення «зовні»).
- Мумія-супутник: зникає лише в області, де є хоч один скарб — 📎 (умова на вміст області).
- Порядок фаз «падіння → обведення → лінії → знову» з перезапуском після кожного очищення — 🥉 (стан-машина з пріоритетом перевірок).
- Пірамідний камінь: стерти з поля тип, на який упав — 🌱.
- Ланцюг ×2 за крок + бонус за ≥5 + стеля лічильника — 📎 (переповнення, counter stop).
- Mystery Mode: задане поле й послідовність, розвʼязувач порядку ходів для цілі «ланцюг N» — 🥇.

## Мапа на каталог
- Є: `gravity-fall` · `multi-cell-size` (великі камені, труни, мумії 2 клітини) · `piece-rotate-flip` · `line-match-clear` (ряд одного типу) · `chain-reaction` · `combo-multiplier` (×2 за крок) · `event-points` · `progress-acceleration` (рівні 1–99) · `next-queue` · `score-records` · `simultaneous-versus` + `garbage-attack` · `end-screen` · `game-over-continue` · `mode-select` · `level-bank` (Mystery з позначками) · `rewind` · `save-game` (quick save) · `game-settings`.
- **Нема** → пропозиції карток:
  - `+enclosure-clear` «Обведення стирає вміст області» · entities/interact · 🥉 · слоти {walls: stone+border, diagonal: yes, gaps: allowed}.
  - `+companion-clear` «Блок зникає лише разом із блоком-напарником в області» · entities/interact · 📎 — мумія й скарб.
  - `+clear-phase-order` «Кілька перевірок очищення з пріоритетом і перезапуском» · game-logic/score · 📎.
  - `+color-clear-special` «Спецблок стирає всі блоки одного типу» · entities/interact · 🌱 — пірамідний камінь.
  - `+all-clear-bonus` «Бонус за порожнє поле» · game-logic/score · 🌱 — perfect = рівень × 5000.
  - `+split-on-landing` «Фігура розпадається на блоки після приземлення» · entities/move · 📎.
  - `+chain-bonus-threshold` «Разовий бонус за ланцюг ≥ N» · game-logic/score · 🌱.
  - `+portrait-reward` «Картинка-нагорода за подію» · interface/menus · 🌱.
  - `+gauge-item-block` «Шкала за кольором кладе предмет у NEXT» · game-logic/economy · 📎 — Plus.

## Пропозиції до словників
- `+cond:enclosed` — область навколо сутності повністю обведена стінами заданого типу (тут: камені + стінки колодязя, діагоналі замикають); підтверджую 🔥 (Hnefatafl, Rampart).
- `+effect:clear_color` — прибрати з поля всі блоки одного кольору/типу (пірамідний камінь); підтверджую 🔥.
- `+card:enclosure-clear` · `+card:companion-clear` · `+card:clear-phase-order` · `+card:chain-bonus-threshold` — див. «Мапа на каталог».

## Джерела
- ⭐ [JA Wikipedia: クレオパトラフォーチュン](https://ja.wikipedia.org/wiki/クレオパトラフォーチュン) — 4 типи блоків, малі/великі, обведення (діагоналі й стінки = камінь, порожнечі дозволені), мумії зі скарбом, лінії за типом, порядок перевірок, ланцюг ×2, бонус ≥5, perfect, рівні до 99, Mystery Mode, Plus і його предмети, S-Tribute.
- [EN Wikipedia: Cleopatra Fortune](https://en.wikipedia.org/wiki/Cleopatra_Fortune) — версії й дати, розробники, Plus, S-Tribute, збірки.
- [Steam: Cleopatra Fortune S-Tribute](https://store.steampowered.com/app/1913690/Cleopatra_Fortune_STribute/) — правила для гравця (closures, mummies, lines, chains, Pyramid Stones, All Clears), фічі S-Tribute.
- [Retro Replay](https://retro-replay.com/db/arcade/cleopatras-fortune) — endless з прискоренням, versus із сміттєвими каменями, puzzle-режим з заданими полями.
- [HonestGamers: DC review](https://www.honestgamers.com/6947/dreamcast/cleopatra-fortune/review.html) — склад формацій, «формації відокремлюються», perfect і портрет, темп рівнів.
- YouTube: пошук «Cleopatra Fortune arcade gameplay».

## Непевне
- (?) Розмір колодязя, кількість блоків у формації понад 3, точний склад формацій — не знайдено.
- (?) Чи кожен блок формації падає окремо після приземлення: огляд каже «detachable depending on how you place them», JA цього явно не формулює.
- (?) Множник ланцюга: JA каже «×2 до 8-го кроку, з 9-го фіксовано 999×», але й «20-й ланцюг — ×524 288» (= 2¹⁹); схоже, 999 — лише межа показу, а подвоєння триває.
- (?) Як саме versus перетворює зачистки на сміттєві камені (кількість, форма) — є лише в огляді Retro Replay.
- (?) HonestGamers: «приблизно кожні 15 рівнів музика й фон змінюються, а швидкість скидається» — JA цього не підтверджує.
- (?) Кількість блоків, яку треба пережити на рівні 99, — у джерелі не названо.
