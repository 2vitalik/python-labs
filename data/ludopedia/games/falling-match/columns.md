---
title: Columns (Колонки)
slug: columns
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: hotseat
  info: full
  random: runtime
  goal: survive
year: 1990
platforms: [HP-UX X11 (1989), arcade, Genesis/Mega Drive, Game Gear, Master System, PC Engine, MSX2, X68000, Super Famicom, Atari ST, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Columns_(video_game)", best: true, note: "стовпчик із 3 каменів, циклування порядку, збіг 3+ у 8 напрямках, ланцюги, Magic Jewel, режими Flash/Doubles/Time Trial, історія Geertsen → Sega"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Columns_II:_The_Voyage_Through_Time", note: "Flash Columns на аркаді, Vs Columns (атака піднімає поле суперника)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tile-matching_video_game", note: "Columns як предок swap/shift-ігор (Yoshi's Cookie, Panel de Pon)"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Columns", note: "пошук; Columns у SEGA Mega Drive & Genesis Classics"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=columns+sega+genesis+gameplay", note: "пошук; геймплей Genesis"}
stage: v1
coverage: 75
mechanics: [gravity-fall, multi-cell-size, keyboard-controls, progress-acceleration, event-points, combo-multiplier, score-records, time-out, game-pause, end-screen, difficulty-levels, hot-seat, ai-opponent, +line-match-clear, +chain-reaction, +cascade-gravity, +next-queue, +cycle-piece, +color-clear-special, +dig-to-target, +garbage-attack]
proposes: ["+trigger:locked", "+trigger:settled", "+trigger:pattern", "+effect:cycle", "+effect:clear_color", "+effect:send_garbage", "+cond:same", "+window:mode-select", "+feature:mode-coop", "+axis:gravity"]
author: opus
date: 2026-11-02
---

# Columns — падає вертикальна трійка каменів; міняй їхній порядок циклом і складай 3+ в будь-якому напрямку

## Суть
У стакан падає вертикальний стовпчик із трьох самоцвітів; гравець зсуває його ліворуч/праворуч і **циклує порядок** каменів (верхній → низ), а не обертає фігуру. Коли стовпчик лягає, будь-які 3+ однакових в ряд — по горизонталі, вертикалі чи діагоналі — зникають, решта падає і може дати ланцюг. Рідкісний **Magic Jewel** знищує всі камені кольору, на який упав. Це «Tetris від Sega»: та сама петля «падає фігура → лягає → зчищення», але критерій — колір, а не повний ряд.

## Поле і час
- Стакан 6 стовпців × 13 рядів (Genesis) (?); стовпчик спавниться по центру зверху, частково над видимим полем.
- Шари: стек каменів (кожен камінь окрема клітина) + активний стовпчик 1×3 + превʼю наступного.
- Real-time: стовпчик падає з темпом рівня; рівень росте з кількістю зчищених каменів (?), швидкість росте з рівнем.
- Після лягання — фаза розвʼязання: пошук ліній → зникнення (мигання) → **кожен камінь падає окремо** → повторний пошук; ввід у цій фазі неактивний.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Стовпчик (column) | player | 3 камені (кольори c1,c2,c3), позиція | падає; зсув ліво/право; цикл порядку; soft drop; лягає → 3 окремі камені |
| Камінь (jewel) | tile | колір (6, менше на легкій складності (?)) | падає до опори окремо; 3+ в лінію в 8 напрямках → зникає |
| Magic Jewel | tile | мерехтить усіма кольорами | спеціальний стовпчик; ліг → знищує всі камені кольору каменя під ним |
| Миготливий камінь (Flash Columns) | tile | позиція на дні | ціль режиму: знищити його, прокопавшись крізь шар над ним |
| Стартове сміття (Flash Columns) | tile | N рядів | випадкові камені на старті рівня; звичайні за правилами |
| Черга next | spawner | 1 стовпчик | джерело наступного стовпчика |
| Ряди-підйом (versus, Columns II+) | hazard | — | атака суперника піднімає «дно» твого стакана (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `spawned(column)` → ЯКЩО `not free(spawn_cells)` → ТО `lose` (стакан заповнено доверху).
- КОЛИ `tick` → ЯКЩО `free(cell_below)` → ТО `move(column, down)` з темпом рівня; інакше `custom: «lock — стовпчик стає трьома каменями стеку»`.
- КОЛИ `input(left|right)` → ЯКЩО `free(target_cells)` → ТО `move(column, dir)`.
- КОЛИ `input(cycle)` → ТО `custom: «cycle — (c1,c2,c3) → (c3,c1,c2)»` (нижній стає верхнім (?)); фігура не обертається й не змінює форму.
- КОЛИ `input(down)` → ТО `move(column, down)` прискорено, `score(+1/клітина)` (?).
- КОЛИ `locked(column)` → ТО перевірка `pattern(line(3+, same_color))` у 4 осях (горизонталь, вертикаль, дві діагоналі).
- КОЛИ `pattern(line(3+))` → ТО `clear(all_matched)` одночасно (лінії можуть перетинатися), `score(n × level × chain)` (?).
- КОЛИ `after(clear)` → ТО `fall(each_jewel)` до опори (каскадна гравітація: кожен камінь окремо, порожнин не лишається).
- КОЛИ `settled` → ЯКЩО `pattern(line(3+))` → ТО `clear`, `combo(+1)`, `multiplier(chain)`; інакше `spawn_at(next, top)`.
- КОЛИ `locked(magic_jewel)` → ТО `custom: «clear_color(color_of(cell_below))»` разом із самим Magic Jewel; на дні (нема каменя під ним) — просто зникає (?).
- КОЛИ `counter(jewels_cleared, ≥, level_quota)` → ТО `counter(level, +1)`, `speed(fall, +)`.
- Flash Columns: КОЛИ `clear(flash_jewel)` → ТО `win` рівня, `next_level`; бонус за швидкість (?).
- Time Trial: КОЛИ `timer(==0)` → ТО `game_over`, підсумок очок.
- Versus (Columns II/III): КОЛИ `combo(n)` → ТО `custom: «send_garbage — підняти поле суперника»`; суперник програє, коли стакан заповнено.
- Поразка: новий стовпчик не вміщується. Рахунок: очки за кожен зчищений камінь × рівень × крок ланцюга (?); макс. 99 999 999.

## Керування і ввід
- Genesis: ←/→ — зсув, ↓ — швидке падіння, A/B/C — циклувати порядок (одна дія, напрям фіксований (?)), Start — пауза.
- Нема обертання як такого: «поворот» Columns — це циклічний зсув кольорів у фігурі 1×3; форма завжди вертикальна.
- Doubles: два гравці по черзі (?) або разом керують фігурами в одному спільному стакані.

## Вікна, меню, HUD
- `splash-screen` → `main-menu` з `mode-select`: Arcade · Menu (Original Game, Flash Columns) · Time Trial · Doubles · 2P Versus (на Genesis — режим «2 Players» (?)) · Options.
- `custom: «menu-settings»` перед стартом: рівень (швидкість) 0–9 (?), складність Easy/Normal/Hard (кількість кольорів), класична/мерехтлива ціль; музика (три треки за мойрами — Clotho, Lachesis, Atropos).
- `game-screen`: стакан, `next-piece-preview` (стовпчик), `score`, `level-number`, лічильник зчищених каменів, `hi-score`; Time Trial — `timer-countdown`; Flash — номер стадії.
- `pause-menu`: Продовжити / Вихід (?).
- `end-screen` Game Over → `leaderboard` (ініціали, аркада й Genesis).
- Переходи: splash → main-menu → налаштування режиму → game-screen → (стакан повний / час / флеш зчищено) end-screen → leaderboard / наступна стадія.

## Фічі поза полем
- Режими: `mode-endless` (Original), `custom: «dig-to-target»` (Flash Columns, стадії), `mode-time-attack` (Time Trial), `mode-coop` (Doubles — один стакан на двох), `mode-versus` (Columns II та далі; на Genesis — 2P).
- `difficulty-presets` (кількість кольорів), `custom-difficulty` (стартовий рівень/швидкість).
- `leaderboard-local`, `pause`, вибір музики (`music-toggle`-родич).
- Нема hold, ghost, undo, hint.

## Варіації й родичі
- Columns (Jay Geertsen, HP-UX, 1989) → Sega (аркада і Genesis, 1990) → Columns II: The Voyage Through Time (1990, аркада: Flash і Vs Columns) → Columns III: Revenge of Columns (1993, versus з атаками (?)) → Columns '97 → Sakura Taisen Hanagumi Taisen Columns.
- Родичі: Tetris (повні ряди замість кольорів), Klax (той самий збіг 3+ у 8 напрямках, інша подача), Puyo Puyo (пара, звʼязна група 4+), Dr. Mario (капсула 1×2, лише 4 напрямки), Bejeweled (ті самі «самоцвіти», але обмін на статичному полі).
- **Осі варіацій**: фігура (1×3 цикл / пара з обертанням / тетроміно) · напрямки збігу (4 / 8) · гравітація після збігу (каскадна / наївна) · спецкамінь (нема / знищує колір / джокер) · ціль (виживання / прокопати до цілі / час / versus).

## Цікавинки для курсу
- Цикл трьох кольорів замість обертання — 🌱 (найпростіший «поворот» у сімʼї).
- Пошук ліній 3+ у 8 напрямках з одночасним зчищенням перетинів (множина клітин, не список ліній) — 📎.
- Каскадна гравітація + ланцюг із множником — 🥉.
- Magic Jewel: знищення кольору за клітиною під ним — 🌱.
- Flash Columns: генерація стартових рядів без готових збігів + ціль-клітина на дні — 📎.
- Versus із підйомом поля суперника — 🥉.

## Мапа на каталог
- Є: `gravity-fall` · `multi-cell-size` (стовпчик 1×3) · `keyboard-controls` · `progress-acceleration` · `event-points` · `combo-multiplier` (ланцюг) · `score-records` · `time-out` (Time Trial) · `game-pause` · `end-screen` · `difficulty-levels` (кількість кольорів, швидкість) · `hot-seat` (Doubles/2P — одночасно, найближча картка) · `ai-opponent` (Columns III (?)).
- **Нема** → пропозиції карток:
  - `+line-match-clear` · entities/legality · 📎 · слот {directions: 8} (спільна).
  - `+chain-reaction` · game-logic/score · 🥉 (спільна).
  - `+cascade-gravity` · entities/move · 📎 (спільна з Puyo).
  - `+next-queue` · interface/hud · 🌱 · слот {size: 1}.
  - `+cycle-piece` «Цикл кольорів у фігурі замість обертання» · interface/input · 🌱.
  - `+color-clear-special` «Спецплитка знищує весь колір» · entities/interact · 🌱 (спільна з Magical Drop; Candy Crush colour bomb).
  - `+dig-to-target` «Прокопати до цільової клітини» · game-logic/win · 📎 (Flash Columns; родич Dr. Mario-вірусів).
  - `+garbage-attack` · game-logic/opponent · 🥉 (тут — підйом дна).

## Пропозиції до словників
- `+trigger:locked`, `+trigger:settled` — 🔥 підтверджую (стовпчик ліг; ланцюг скінчився).
- `+trigger:pattern` — ⏳ підтверджую: `line(3, 8dir)`.
- `+effect:cycle` — циклічний зсув значень усередині сутності (кольори стовпчика); не `rotate`, бо форма не змінюється.
- `+effect:clear_color` — знищити всі плитки кольору (Magic Jewel; Bejeweled hypercube, Candy colour bomb).
- `+effect:send_garbage` — 🔥 підтверджую (versus).
- `+cond:same` — 🔥 підтверджую.
- `+window:mode-select` — ⏳ підтверджую.
- `+feature:mode-coop` — 🔥 підтверджую (Doubles — двоє в одному стакані).
- `+axis:gravity` — `cascade`.

## Джерела
- ⭐ [Wikipedia: Columns](https://en.wikipedia.org/wiki/Columns_(video_game)) — механіка стовпчика, циклування, збіг 3+ у будь-якому напрямку, ланцюги, Magic Jewel, режими Flash/Doubles/Time Trial, історія Geertsen/HP/Sega, продовження.
- [Wikipedia: Columns II](https://en.wikipedia.org/wiki/Columns_II:_The_Voyage_Through_Time) — Flash Columns (прокопати до миготливих), Vs Columns (комбо піднімають поле суперника).
- [Wikipedia: Tile-matching video game](https://en.wikipedia.org/wiki/Tile-matching_video_game) — Columns у другому поколінні, вплив на Yoshi's Cookie і Panel de Pon.
- YouTube: пошук «columns sega genesis gameplay».

## Непевне
- (?) Розмір стакана 6×13, 6 кольорів, залежність кольорів від складності — з памʼяті; Wikipedia каже лише «tall rectangular».
- (?) Напрям циклу (нижній → верх чи навпаки) і чи є дві кнопки на різні напрями.
- (?) Квота каменів на рівень, формула очок і множник ланцюга — з памʼяті.
- (?) Поведінка Magic Jewel на дні; частота появи.
- (?) Деталі versus у Columns III (атака піднімає дно, «crush»-механіка) — Wikipedia по III не перевірено; WebSearch вичерпано.
- (?) Пункти меню Genesis-версії, рівні 0–9, Doubles почергово чи одночасно.
