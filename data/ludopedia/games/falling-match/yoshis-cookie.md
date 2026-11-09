---
title: Yoshi's Cookie
slug: yoshis-cookie
aka: [ヨッシーのクッキー, Yoshi no Cookie]
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: state
year: 1992
platforms: [NES, Game Boy, SNES, GameCube (Nintendo Puzzle Collection), Wii VC]
links:
  - {kind: fandom, url: "https://www.mariowiki.com/Yoshi%27s_Cookie", best: true, note: "Super Mario Wiki: типи печива, лічильник 15 → Yoshi-печиво, Action 10×10, VS 5×5 до 25, ефекти Blind/Panic/Slave, Puzzle 100 від Пажитнова"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Yoshi%27s_Cookie", note: "огляд, версії, Puzzle-режим SNES"}
  - {kind: other, url: "https://ja.wikipedia.org/wiki/ヨッシーのクッキー", note: "JA: поле 8×8, тор-зсув, очки 10/20/×2, ланцюги, шкали типів, VS-правила"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=yoshi%27s+cookie+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [wrap-edges, selection-highlight, keyboard-controls, line-match-clear, chain-reaction, combo-multiplier, event-points, progress-acceleration, sequential-levels, level-select, cheat-codes, level-password, move-limit, simultaneous-versus, ai-opponent, character-select, game-settings, music-toggle, completion-detection, +line-shift-wrap, +growing-board, +board-overflow, +wildcard-tile, +type-gauge-reward, +blind-attack, +panic-bomb, +clear-all-goal, +move-limit-puzzle, +pushback-on-clear]
proposes: ["+effect:shuffle", "+effect:mirror_control", "+ui:type-gauges", "+ui:fuse-timer", "+card:line-shift-wrap", "+card:type-gauge-reward", "+card:pushback-on-clear"]
author: opus
date: 2026-11-09
---

# Yoshi's Cookie — зсувай цілі рядки й стовпці печива по колу, доки лінія не стане одного сорту

## Суть
Поле печива п'яти сортів; курсором обираєш печиво й зсуваєш весь його рядок або стовпець на одну клітину — те, що виходить за край, повертається з протилежного боку (як у кубику Рубіка). Рядок або стовпець, повністю заповнений одним сортом, зникає; Yoshi-печиво підходить до будь-якого сорту. Тим часом нове печиво підповзає зверху й справа і приростає до поля; переросло край — кінець гри. Етап пройдено, коли печива на полі не лишилось.

## Поле і час
- Action (1P): поле до 8×8; на старті блок печива в нижньому лівому куті, нові ряди/стовпці підходять зверху і справа й приростають при контакті (поле росте).
- Зсув — тороїдальний у межах поточного рядка/стовпця (зациклення).
- Real-time: печиво надходить за таймером, частіше з рівнем; гравець може прискорити надходження вручну. Що довше стоїш на етапі — то швидше.
- VS: поле 5×5 у кожного, завжди повне — зчищене одразу поповнюється.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Курсор | player | клітина | обирає печиво; разом із напрямком задає зсув рядка/стовпця |
| Печиво ×5 (серце, квітка, ромб, клітинка, коло) | tile | сорт | зсувається разом із лінією; повна лінія одного сорту → зникає |
| Yoshi-печиво | tile | wild | підходить до будь-якого сорту (1P); у VS — лише лінією самих Yoshi і запускає ефект |
| Печиво, що підходить | object | край (верх/праворуч) | рухається до поля, приростає рядом/стовпцем |
| Шкала сорту | zone | 15 зчищених | повна → Yoshi-печиво на полі, шкала = 0 (JA: ще й додатковий ряд) |
| Мушля Купи (раунди 11+) | tile | — | не надходить з країв; зчищується лише з Yoshi-печивом |
| Вороги Маріо (раунди 11+) | tile | сорт | замість печива: Piranha, Boo, Blooper, Goomba, гриб |
| Таймер-ґніт (VS) | zone | заповнюється без зчищень | повний → раунд програно |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(select, cookie)` + `input(dir)` → ТО `shift(row|col_of(cookie), dir)`, `wrap(edge_cookie)`.
- КОЛИ `after(shift)` → ЯКЩО `pattern(row_full | col_full, same_type)` (Yoshi — як будь-який) → ТО `clear(line)`, `score(10 × 2^(n-2))` (2 печива — 10, 3 — 20, далі подвоєння), `counter(gauge[type], +n)`.
- КОЛИ `after(clear)` → ЯКЩО `chain(n)` → ТО `multiplier(×2^(n-1))` (2 ланцюги ×2, 3 — ×4…).
- КОЛИ `after(clear)` → ТО `custom: «pushback — печиво, що підходить, відсувається назад»`; лінія зникла цілком → відповідні печива, що підходять, теж зникають.
- КОЛИ `timer(feed_rate)` → ТО `move(incoming, toward_field)`; КОЛИ `contact(incoming, field)` → ТО `attach(incoming, field)` (поле росте).
- КОЛИ `input(speed_up)` → ТО `speed(incoming, ×k)`.
- КОЛИ `counter(gauge[type], ≥, 15)` → ТО `spawn_at(yoshi_cookie, field)`, `counter(gauge[type], =0)`.
- КОЛИ `reach(field, edge)` (рядок/стовпець понад 7) → ТО `lose`.
- КОЛИ `all_gone(cookies)` → ТО `win`, `next_level` (10 етапів у раунді, 10 раундів).
- Puzzle (SNES): КОЛИ `all_gone(cookies)` → ЯКЩО `counter(moves, ≤, limit)` → ТО `win`; інакше `restart`.
- VS: КОЛИ `clear(line)` → ТО `counter(points, +n)`, `spawn_at(yoshi_cookie, refill)` (+1; ланцюг або дві лінії разом — +5).
- VS: КОЛИ `clear(yoshi_line)` → ТО ефект суперникові (як саме обирається — (?)): `counter(points, -7|-3|+3)` · BLIND — `hide(center_3x3)` · PANIC — `custom: «shuffle поля, дії заблоковано»` · SLAVE — `custom: «курсор жертви повторює курсор нападника»`.
- VS: КОЛИ `counter(points, ≥, 25)` → ТО `win` раунду; КОЛИ `timer(fuse, ==, full)` → ТО `lose` раунду; 3 раунди — матч.
- Перемога: поле порожнє (Action/Puzzle) / 25 очок (VS). Поразка: поле переросло край / ліміт ходів / ґніт.

## Керування і ввід
- D-pad веде курсор по полю; утримання A + напрямок зсуває рядок (←/→) чи стовпець (↑/↓) обраного печива на 1.
- Кнопка прискорення надходження печива (?).
- VS: двоє гравців на розділеному екрані, кожен своїм курсором.

## Вікна, меню, HUD
- `splash-screen` — титул (NES/GB: сценка з банкою печива).
- `main-menu`: 1P Action · VS (людина / CPU на GB/SNES) · Puzzle (SNES).
- `settings-window` перед Action: стартовий раунд, швидкість (Low/Med/Hi), музика (типи / Off).
- `character-select` (GB/SNES/GC): Маріо, Йоші, Піч, Боузер з різними параметрами.
- `game-screen`: поле, курсор, печиво на підході, `score`, `level-number` (раунд-етап), `custom: «type-gauges» — шкали 5 сортів`.
- VS-екран: два поля, `custom: «fuse-timer»`, шкала очок до 25, рахунок раундів.
- `level-password` — пароль Puzzle-пазла для продовження.
- `end-screen` етапу / Game Over; кінцівка після раунду 10 і довша — після 99.

## Фічі поза полем
- `levels-sequential` 10 раундів × 10 етапів; `level-select` стартового раунду; прихований раунди 11–99 (чіт: Music Off, Speed Hi, Round 10, ↑+Select — `cheat-codes`).
- `difficulty-presets` швидкості, `music-toggle`.
- Puzzle (SNES): `puzzle-bank` 100 пазлів (10×10) від Олексія Пажитнова, ліміт ходів, паролі.
- VS: `local-multiplayer` (2; GB і GC — до 4), `ai-opponent-levels` (4 CPU + 4 відкриті), гандикап стартовими очками.
- GC-ремейк: Story у VS-правилах, туторіал правил.

## Варіації й родичі
- Версії NES/GB (Tose) та SNES (BPS) відрізняються режимами й персонажами; GC — без універсального Yoshi у VS.
- Родичі: Sixteen / кубик Рубіка (зсув лінії по колу), Tetris (лінія → зникає), Puzzle League (зсувний курсор), Bejeweled (збіг після обміну), Columns.
- **Осі варіацій**: дія (обмін двох / зсув лінії з тором / поворот 2×2) · умова (3 в ряд / **уся лінія**) · загроза (стеля / поле росте з країв) · wild (нема / джокер / джокер-атака).

## Цікавинки для курсу
- Тороїдальний зсув рядка/стовпця — 🌱 (зсув списку з обгортанням).
- Зчищення повної лінії одного сорту з джокером на прямокутному полі змінного розміру — 📎.
- Поле, що росте з двох країв, і «відштовхування» печива, що підходить, після зчищення — 🥉.
- Шкали сортів: кожні 15 зчищених одного сорту — нагорода-джокер — 🌱.
- VS-ефекти Blind / Panic / Slave — атаки на інтерфейс суперника (сховати, перемішати, перехопити курсор) — 🥈.
- Пазл з лімітом ходів + розвʼязувач BFS по зсувах — 🥇.

## Мапа на каталог
- Є: `wrap-edges` (зсув по колу) · `selection-highlight` (курсор) · `keyboard-controls` · `line-match-clear` (вся лінія одного сорту) · `chain-reaction` · `combo-multiplier` · `event-points` · `progress-acceleration` · `sequential-levels` · `level-select` · `cheat-codes` · `level-password` · `move-limit` · `simultaneous-versus` · `ai-opponent` · `character-select` · `game-settings` · `music-toggle` · `completion-detection`.
- **Нема** → пропозиції карток:
  - `+line-shift-wrap` «Зсув рядка/стовпця з обгортанням» · entities/move · 🌱 · слот {axis: row|col}.
  - `+type-gauge-reward` «Шкала зчищеного за типом дає бонус» · game-logic/score · 🌱 · слот {n: 15}.
  - `+pushback-on-clear` (картка-пропозиція) «Зчищення відсуває загрозу» · game-logic/lose · 📎.
  - `+growing-board` · `+board-overflow` · `+wildcard-tile` · `+blind-attack` · `+panic-bomb` · `+clear-all-goal` · `+move-limit-puzzle` — теги вже є в корпусі.

## Пропозиції до словників
- `+effect:shuffle` — перемішати сутності поля (PANIC); пропозиція вже є — підтверджую.
- `+effect:mirror_control` — ввід жертви повторює ввід нападника (SLAVE), родич `mirror_input`, але між двома гравцями.
- `+ui:type-gauges` — набір шкал за типом плиток.
- `+ui:fuse-timer` — ґніт/шкала бездіяльності, що росте без успішних дій.
- `+card:line-shift-wrap` · `+card:type-gauge-reward` · `+card:pushback-on-clear` — див. «Мапу».

## Джерела
- ⭐ [Super Mario Wiki: Yoshi's Cookie](https://www.mariowiki.com/Yoshi%27s_Cookie) — сорти, 15 → Yoshi-печиво, край > 7, Action 10×10, налаштування, раунди 11–99 і чіт, VS 5×5 до 25 і ефекти, персонажі, Puzzle 100 від Пажитнова, відмінності версій.
- [Wikipedia: Yoshi's Cookie](https://en.wikipedia.org/wiki/Yoshi%27s_Cookie) — огляд, Puzzle з лімітом ходів, VS проти CPU на SNES.
- [JA Wikipedia: ヨッシーのクッキー](https://ja.wikipedia.org/wiki/ヨッシーのクッキー) — 8×8 / 5×5, зсув із зациклюванням, очки й множники ланцюгів, відштовхування, шкали, VS-поповнення Yoshi.
- YouTube: пошук «yoshi's cookie gameplay».

## Непевне
- (?) Mario Wiki пише «рядок або стовпець з принаймні двох однакових»; JA і EN — «уся лінія одного сорту». Узгодження: лінія поточного (змінного) розміру поля, тож у вузькому полі достатньо двох.
- (?) За JA повна шкала ще й додає ряд печива; Mario Wiki — лише Yoshi-печиво.
- (?) Кнопка ручного прискорення — JA каже «можна прискорити вручну», яка кнопка — не знайдено.
- (?) Підсумкові очки Action за етап і бонуси — не знайдено.
