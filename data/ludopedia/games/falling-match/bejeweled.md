---
title: Bejeweled (1–3, Twist)
slug: bejeweled
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: both
  goal: score
year: 2001
platforms: [web, PC, Mac, mobile, Xbox, Nintendo DS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bejeweled_3", best: true, note: "Flame/Star/Hypercube/Supernova і всі 8 режимів B3 в одному місці"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bejeweled_(video_game)", note: "оригінал: swap → збіг, повернення невдалого обміну, timed/untimed"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bejeweled_2", note: "Power Gem, Hypercube, режими Classic/Action/Puzzle/Endless + секретні"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bejeweled_Twist", note: "обертання 2×2, бомби, вугілля, doom gems, locked"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bejeweled_(series)", note: "серія й роки"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Bejeweled", note: "пошук; Bejeweled 2/3/Twist"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=bejeweled+3+classic+gameplay", note: "пошук; геймплей B3"}
stage: v1
coverage: 70
mechanics: [cell-click, drag-drop-piece, swipe-gestures, hover-highlight, gravity-fall, spawn-random-cell, no-moves-left, event-points, combo-multiplier, time-out, time-bonus, score-records, level-select, game-pause, background-music, end-screen, particles, +match-3-swap, +chain-reaction, +cascade-refill, +special-tiles, +no-moves-detection, +hint-move, +rotate-2x2, +countdown-tile]
proposes: ["+trigger:settled", "+effect:reshuffle", "+effect:explode_area", "+effect:clear_color", "+effect:clear_row_col", "+effect:revert_swap", "+cond:adjacent", "+ui:hint-marker", "+ui:countdown-on-tile", "+window:mode-select", "+feature:mode-zen", "+feature:hint", "+axis:control"]
author: opus
date: 2026-11-02
---

# Bejeweled — міняй сусідні камені, щоб скласти 3+ в ряд; каскади, спецкамені й нескінченне поповнення

## Суть
Поле самоцвітів (8×8 у класиці); гравець обмінює два сусідні камені, і обмін легальний, лише якщо утворює лінію з 3+ однакових. Зібрані камені зникають, верхні падають, згори сиплються нові — і можуть самі скласти лінії (каскад). Довші й фігурні збіги створюють спецкамені (вибух 3×3, хрест рядок+стовпець, «гіперкуб» усього кольору). Класика закінчується, коли нема жодного можливого ходу; Twist замінює обмін обертанням квадрата 2×2.

## Поле і час
- Поле 8×8 квадратних клітин (?), 7 кольорів каменів (?); новий камінь зʼявляється над верхнім краєм і падає в стовпець.
- Час: Classic/Zen — покроково (хід = обмін), анімації каскаду не вимагають вводу; Action/Lightning/Blitz — real-time таймер поверх покрокового поля.
- Шари: камені (тип = колір + спецвластивість) + накладки (lock, бомба з лічильником, вугілля в Twist) + курсор/підсвітка вибраного.
- Twist: курсор стоїть на **перетині** чотирьох клітин; ціль ходу — блок 2×2.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Звичайний камінь | tile | колір (7) | бере участь у збігу; падає вниз при порожнечі |
| Power Gem (B2) / Flame Gem (B3) | tile | колір | створюється збігом 4 в ряд (B2: також L/T/+); у збігу вибухає 3×3 |
| Star Gem (B3) | tile | колір | створюється L/T/+ збігом; у збігу чистить свій рядок і стовпець |
| Hypercube | tile | без кольору | створюється збігом 5 в ряд; обмін з каменем → зникає весь колір; два гіперкуби → усе поле |
| Supernova Gem (B3) | tile | колір | збіг 6+ (лише каскадом); чистить рядки й стовпці в межах 3×3 смуги |
| Lightning Gem (Twist) | tile | колір | збіг 5 в ряд; блискавки (рядок/стовпець) |
| Time Gem (B3 Lightning) | pickup | +секунди | збіг додає час у бак продовження |
| Coal (Twist) | object | — | не збігається; знищений спецефектом — великий бонус |
| Bomb Gem (Twist) | hazard | лічильник ходів | знищ до 0, інакше програш |
| Locked Gem (Twist) | gate | ланцюг | блокує обертання свого блоку, знімається збігом |
| Doom Gem (Twist) | hazard | лічильник | не рухається, не збігається; лічильник падає лише на ходах без збігу |
| Курсор / виділення | — (ui) | клітина або перетин | вибір першого каменя (B1–3) або центру блоку 2×2 (Twist) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(select a)`, `input(select b)` → ЯКЩО `adjacent(a, b)` (4-сусідство) → ТО `swap(a, b)`; ЯКЩО після обміну нема `pattern(line(3+))` → ТО `custom: «revert_swap — обмін повертається, хід не зараховано»`.
- Twist: КОЛИ `input(rotate at intersection)` → ЯКЩО `not occupied(block, locked)` → ТО `rotate(block2x2, +90)`; хід зараховано навіть без збігу.
- КОЛИ `pattern(line(3+, same_color))` (горизонт./вертик.) → ТО `clear(line)`, `score(n)`, `animate(sparkle)`.
- КОЛИ `pattern(line(4))` → ТО `clear`, `spawn_at(flame_gem, swap_cell)`; `pattern(L|T|+)` → `spawn_at(star_gem)` (B3) / `power_gem` (B2) / `flame_gem` (Twist); `pattern(line(5))` → `spawn_at(hypercube)` (Twist — lightning); `pattern(line(6+))` → `spawn_at(supernova)`.
- КОЛИ `clear(flame_gem)` → ТО `custom: «explode_area 3×3»`; `clear(star_gem)` → `custom: «clear_row_col»`; `swap(hypercube, gem)` → `custom: «clear_color(gem.color)»`; `swap(hypercube, hypercube)` → `clear(all)`. Спецкамінь, зачеплений вибухом, теж спрацьовує (ланцюг детонацій).
- КОЛИ `after(clear)` → ТО `fall(gems_above)`, `spawn_at(random_gem, top)` до заповнення стовпців.
- КОЛИ `after(fall)` → ЯКЩО `pattern(line(3+))` → ТО `clear`, `combo(+1)`, `score(× cascade)` (?), повтор; інакше `custom: «settled»`.
- КОЛИ `custom: «settled»` → ЯКЩО `no_moves(player)` → ТО Classic: `lose` («No more moves»); Zen/Endless: `custom: «reshuffle — нова розкладка без готових збігів, але з ходом»`; Finity (B2): поле замінюється новим.
- КОЛИ `counter(level_bar, ==, full)` → ТО `next_level` (B2/B3 Classic: нове поле, множник очок = рівень).
- Action (B2): КОЛИ `tick` → ТО `counter(level_bar, −)`; КОЛИ `counter(level_bar, ==, 0)` → `lose`. Lightning (B3): 1 хв; КОЛИ `clear(time_gem)` → `timer(+n)` у бак; КОЛИ `timer(==0)` → ЯКЩО бак не порожній → ТО продовження до 1 хв і `multiplier(+1)`; інакше `game_over`. Blitz (Twist): ~5 хв.
- Twist: КОЛИ `turn_end` → ТО `counter(bomb, −1)`; КОЛИ `counter(bomb, ==, 0)` → ТО `lose`. Doom: `counter(−1)` лише якщо хід без збігу.
- Рахунок: базові очки за камінь у збігу × рівень (Classic) + бонус за спецкамені й каскад; швидкі послідовні збіги — speed bonus (Lightning).

## Керування і ввід
- Миша: клік по каменю (виділення) → клік по сусідньому = обмін; або drag каменя на сусіда. Тач: свайп у напрямку сусіда.
- Twist: клік по перетину чотирьох каменів — обертання блоку 2×2 за годинниковою.
- Hint-кнопка (B1–B3): підсвічує один можливий хід (у Classic — коштом очок (?)).
- Клавіатура/геймпад у консольних версіях: курсор + кнопка вибору.

## Вікна, меню, HUD
- `splash-screen` (логотип PopCap) → `main-menu` з `mode-select`: Classic · Zen · Lightning · Quest (+ секретні: Poker, Butterflies, Ice Storm, Diamond Mine — B3; Twilight, Hyper, Finity, Cognito — B2).
- `game-screen`: поле 8×8, `score`, `progress-bar` рівня (Classic) / він же таймер (Action), `level-number`, `hint-button`, кнопка Menu; `popup-text` очок на місці збігу, голосові «Good/Excellent/Incredible» за каскад (?).
- `pause-menu` (Menu): Resume, Restart, Help, Options, Main Menu.
- `settings-window`: музика, звук, вікно/повний екран; Zen — налаштування дихання, мантри, звуків природи.
- `help-window` — правила і спецкамені; `tutorial-window` при першому запуску (?).
- `end-screen`: «No More Moves» / «Time Up» → підсумок (очки, рівень, найбільший каскад) → `leaderboard` / `stats-window` (рекорди по режимах).
- B3 Quest: `custom: «quest map»` (5 реліквій × міні-ігри) — ближче до `level-select`.
- Переходи: main-menu → mode → game-screen → (нема ходів / час) end-screen → main-menu; level_bar повний → анімація переходу → нове поле.

## Фічі поза полем
- Режими: `mode-classic`, `mode-zen` (без програшу, reshuffle), `mode-time-attack` (Lightning/Action/Blitz), `mode-puzzle` (B2 Puzzle — 80 полів, треба зчистити все, є undo), `mode-endless`; секретні режими відкриваються рівнем у інших (`unlockables`).
- `hint`, `undo` (лише Puzzle B2), `autosave`/`continue` (продовжити Classic), `stats`, `leaderboard-local`, `achievements` (B3 badges).
- Twist: Disarm Spinner — рулетка з ризиком (череп підриває бомбу) (?).
- `music-toggle`, `volume-sliders`, `fullscreen`.

## Варіації й родичі
- Bejeweled (2000/2001) → 2 (2004, Power Gem, Hypercube, режими) → Twist (2008, обертання 2×2, погані камені) → Blitz (хвилинний, соцмережі) → 3 (2010, Star/Supernova, Quest, секретні режими) → Stars (2016).
- Попередники й родичі: Shariki (1994), Colors Game; Candy Crush (цілі рівня, блокери, ліміт ходів), Zoo Keeper, Hexic (обертання трійок на гекс-полі), Puzzle Quest (match-3 як бій), Puzzle & Dragons (тягнеш камінь шляхом).
- **Осі варіацій**: ввід (обмін сусідів / обертання 2×2 / обертання трійки / drag-шлях / клік по групі) · легальність (лише зі збігом / будь-який хід) · кінець (нема ходів / час / ліміт ходів / ніколи) · поповнення (згори випадково / без поповнення — Puzzle) · спецкамені (нема / 3 / 4+ типи; комбінації двох спецкаменів).

## Цікавинки для курсу
- Обмін сусідів з відкатом, якщо нема збігу — 🌱.
- Пошук усіх ліній 3+ і «зріз» колонок з поповненням згори — 📎.
- Каскад до стабілізації з лічильником кроку і множником — 🥉.
- Детектор «нема ходів» (перебір усіх обмінів) + reshuffle з гарантією ходу й без готових збігів — 🥉.
- Спецкамені з розпізнаванням форми збігу (4 / L-T / 5 / 6+) і ланцюгом детонацій — 🥈.
- Hint як побічний продукт детектора ходів — 🌱.
- Twist-обертання 2×2 + бомби з лічильником ходів — 📎.

## Мапа на каталог
- Є: `cell-click` · `drag-drop-piece` · `swipe-gestures` · `hover-highlight` · `gravity-fall` · `spawn-random-cell` (поповнення) · `no-moves-left` · `event-points` · `combo-multiplier` (каскад) · `time-out` (Lightning) · `time-bonus` (Time Gems) · `score-records` · `level-select` (Quest/Puzzle) · `game-pause` · `background-music` · `end-screen` · `particles` (іскри, вибухи).
- **Нема** → пропозиції карток:
  - `+match-3-swap` «Обмін сусідів зі збігом» · entities/legality · 📎 · слот {revert: yes|no}.
  - `+chain-reaction` «Каскад збігів» · game-logic/score · 🥉 (спільна з Puyo/Dr. Mario).
  - `+cascade-refill` «Осідання + поповнення згори» · entities/spawn · 📎.
  - `+special-tiles` «Спецплитки з форми збігу» · entities/interact · 🥈 · слоти {shapes, effects}.
  - `+no-moves-detection` «Детектор нема ходів + reshuffle» · game-logic/constraints · 🥉.
  - `+hint-move` «Підказка ходу» · interface/hud · 🌱.
  - `+rotate-2x2` «Обертання блоку 2×2» · interface/input · 📎.
  - `+countdown-tile` «Плитка з лічильником ходів» · entities/state · 📎 (бомби Twist, Candy Crush).

## Пропозиції до словників
- `+trigger:settled` — поле стабілізувалось (спільне з Puyo/Dr. Mario).
- `+effect:reshuffle` — перемішати плитки поля з гарантією ходу; `+effect:explode_area(n×n)`; `+effect:clear_color(c)`; `+effect:clear_row_col`; `+effect:revert_swap` — відкат нелегального обміну.
- `+cond:adjacent` — є тригер `adjacent`, бракує умови-двійника для ходу «лише сусіди».
- `+ui:hint-marker` — ⏳ підтверджую; `+ui:countdown-on-tile` — число ходів на плитці (бомба).
- `+window:mode-select` — ⏳ підтверджую; `+feature:mode-zen`, `+feature:hint` — ⏳ підтверджую.
- `+axis:control` — тут `swap` / `rotate-block` як значення осі (ввід, а не напрямок аватара).

## Джерела
- ⭐ [Wikipedia: Bejeweled 3](https://en.wikipedia.org/wiki/Bejeweled_3) — Flame/Star/Hypercube/Supernova, 8 режимів, Lightning з Time Gems.
- [Wikipedia: Bejeweled (video game)](https://en.wikipedia.org/wiki/Bejeweled_(video_game)) — обмін сусідів, повернення обміну без збігу, timed/untimed, історія.
- [Wikipedia: Bejeweled 2](https://en.wikipedia.org/wiki/Bejeweled_2) — Power Gem, Hypercube, Classic/Action/Puzzle/Endless, секретні режими й обробка «нема ходів».
- [Wikipedia: Bejeweled Twist](https://en.wikipedia.org/wiki/Bejeweled_Twist) — обертання 2×2, ходи без збігу, Coal/Bomb/Locked/Doom, Classic/Zen/Blitz/Challenge.
- [Wikipedia: Bejeweled (series)](https://en.wikipedia.org/wiki/Bejeweled_(series)) — роки ігор серії.

## Непевне
- (?) Поле 8×8 і 7 кольорів — загальновідомо, але в перевірених статтях не названо.
- (?) Точна формула очок, множник каскаду, вартість hint у Classic, голосові «Excellent» — з памʼяті.
- (?) Механізм «не можна застрягнути» в Zen/Endless (reshuffle чи генерація з гарантією ходу) — джерела кажуть лише «не закінчуються ходи».
- (?) Деталі Disarm Spinner у Twist і tutorial-вікно — коротко зі статті / з памʼяті.
- (?) Bejeweled bejeweled.fandom.com недоступний (402) — спецкамені звірено лише з Wikipedia.
