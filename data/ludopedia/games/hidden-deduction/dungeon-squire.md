---
title: Dungeon Squire
slug: dungeon-squire
aka: [Squire]
family: hidden-deduction
also: [roguelike]
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: hidden
  random: setup
  goal: state
year: 2025
platforms: [web (itch.io, HTML5), Android]
links:
  - {kind: itch, url: "https://mvolution.itch.io/squire", best: true, note: "грати в браузері; «Minesweeper meets Roguelike», прямий нащадок Dragonsweeper, туторіал, colorblind/high-contrast"}
  - {kind: official, url: "https://mvolution.itch.io/squire/devlog/901500/is-the-game-always-solvable", note: "девлог: розвʼязність, 4 молоти й 3 зілля в стартовій зоні, вогняні й камʼяні стіни, seed"}
  - {kind: official, url: "https://mvolution.itch.io/squire/devlog", note: "девлог 14.02–08.03.2025: бета, RC1 (магічна пастка Ancient Skeleton), 1.0, Dark Lord, easy-рівень"}
  - {kind: other, url: "https://play.google.com/store/apps/details?id=com.mvolution.squire", note: "Google Play (опис не прочитано)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Dungeon+Squire+minesweeper+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [cell-click, hp-damage, item-pickup, inventory-items, destructible-blocks, seed-share, dungeon-generation, codex-window, tutorial-window, game-screen, end-screen, +sum-of-levels-clue, +xp-level-up, +monster-bestiary, +guaranteed-start-kit, +memory-marker-trap]
proposes: ["+feature:auto-pickup", "+feature:auto-level-up", "+feature:show-monster-levels", "+card:guaranteed-start-kit", "+card:memory-marker-trap"]
author: opus
date: 2026-11-09
---

# Dungeon Squire — Dragonsweeper для смартфона: числа показують монстрів поруч, молоти й зілля пробивають шлях до Темного Лорда

## Суть
Пряме продовження формули [Dragonsweeper](dragonsweeper.md) (автор оригіналу схвалив проєкт): під клітинами — монстри, предмети й стіни, числа підказують, хто поруч, герой бʼється своїм HP і росте досвідом. Відмінності: **процедурні підземелля з seed-ом**, яким можна поділитись; **місцевість** — вогняні й камʼяні стіни, які треба обходити або розбивати молотами; гарантований стартовий набір (4 молоти, 3 зілля); фінальний бос — Темний Лорд. Гра спроєктована під тач на маленькому екрані Android і зроблена за місяць.

## Поле і час
- Квадратна сітка підземелля, генерується процедурно; розмір під екран телефона (?).
- Статичний: нічого не рухається без дії гравця.
- Шари: прихований вміст (монстр / предмет / стіна / порожньо) + числа + позначки (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Сквайр (герой) | player | HP, XP, рівень; аватар ч/ж | не ходить полем — бʼє клітину дотиком |
| Число | mark | монстри поруч (сума рівнів, як у Dragonsweeper (?)) | підказка; слабкий монстр може «ховатись у прогалині» |
| Монстр | enemy | рівень; 10+ видів з власним патерном чи вмінням | бій коштує HP; слизовий майстер, лепрекон, Ines, snek, Christian (з девлогу) |
| Темний Лорд | boss | — | фінал; після перемоги — сюжетний екран |
| Ancient Skeleton (магічна пастка) | hazard | на клітинах підлоги | варіація пастки, що допомагає запамʼятати позиції монстрів (?) |
| Вогняна стіна | hazard | — | непрохідна «стіна вогню»; суцільна — теоретично робить мапу нерозвʼязною |
| Камʼяна стіна | static | — | розриває вогняні стіни; руйнується молотом (?) |
| Молот | pickup | 4 гарантовано біля старту | руйнує стіну / відкриває клітину (?) |
| Зілля | pickup | 3 гарантовано біля старту | лікування |
| Лук, посох, броня | pickup | — | предмети з коментарів гравців (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(open, c)` → ЯКЩО `cell(c, empty)` → ТО `reveal(c)` з `custom: «число монстрів/сума рівнів поруч»` (?).
- КОЛИ `input(open, c)` → ЯКЩО `occupied(c, monster)` → ТО `hp(hero, -level)` (?), `custom: «XP за монстра»`; ЯКЩО `hp_zero(hero)` → ТО `lose`.
- КОЛИ `custom: «XP досить»` → ТО `custom: «кнопка level-up»` (або авто за налаштуванням) → `heal(hero, full)` (?).
- КОЛИ `input(use, hammer)` → ЯКЩО `cell(c, wall)` → ТО `set_cell(c, floor)` (?).
- КОЛИ `input(use, potion)` → ТО `heal(hero, n)` (?).
- КОЛИ `input(open, item)` → ЯКЩО `mode(auto_pickup)` → ТО `pickup`.
- КОЛИ `level_start` → ТО `custom: «генерація з seed; стартова зона — 4 молоти й 3 зілля; програмний запобіжник розвʼязності»`.
- КОЛИ `died(dark_lord)` → ТО `win`, `window(end-screen)` з тривалістю гри, `window(dialogue-window)` — сюжет.
- Перемога: перемогти Темного Лорда. · Поразка: HP вичерпано. · Рахунок: тривалість гри на екрані перемоги (?).
- Розвʼязність: «практично завжди» без вгадувань; якщо вгадувати, то 50/50 або 2/3, у рідких випадках 1:3 — «справедливо, бо можна зважити ймовірності».

## Керування і ввід
- Лише дотик / миша: тап — відкрити клітину, атакувати, підібрати; кнопка level-up на полі (не перекриває предмети з 1.0.x).

## Вікна, меню, HUD
- `game-screen`: поле, HP, XP, рівень, кнопка level-up, предмети (?).
- `codex-window` — бестіарій монстрів.
- `tutorial-window` — інтерактивний туторіал + вступний рівень easy.
- `settings-window`: auto-pickup, auto-level-up, показувати рівні монстрів, colorblind, high-contrast.
- `end-screen` перемоги з тривалістю; `dialogue-window` — сюжет після Темного Лорда.
- Вікно seed: ввести / поділитись (попередження про несумісність seed між версіями).

## Фічі поза полем
- `seed-display` / `seed-input` / `share-code` — «Dungeon Seed», щоб друг зіграв те саме підземелля.
- `difficulty-presets`: easy-вступ; `colorblind-palette`, `high-contrast`, `touch-controls`.
- `+feature:auto-pickup`, `+feature:auto-level-up`, `+feature:show-monster-levels` — налаштування-помічники.
- `codex` (бестіарій), `tutorial`.

## Варіації й родичі
- [dragonsweeper](dragonsweeper.md) — оригінал (механіки «дуже близькі»); тут описані лише відмінності.
- [mamono-sweeper](mamono-sweeper.md) — предок формули «числа = сила монстрів»; [demoncrawl](demoncrawl.md), [minato](minato.md) — інші сапер-роглайти.
- Осі варіацій: **поле** одне ручне-напівгенероване / процедурне з seed · **місцевість** нема / стіни й вогонь як барʼєри · **старт** порожній / гарантований набір інструментів · **платформа** десктоп / тач-перш.

## Цікавинки для курсу
- Seed підземелля як код для друга (відтворювана генерація) — 📎.
- Гарантований стартовий набір як запобіжник розвʼязності генератора — 📎.
- Вогняні й камʼяні стіни: перевірка, що мапа прохідна (flood fill через ламкі стіни) — 🥉.
- Оцінка «гірших шансів» при вимушеному вгадуванні (50/50 vs 1:3) — 🥇.
- Налаштування-помічники (auto-pickup, auto-level-up) поверх ядра — 🌱.

## Мапа на каталог
- Є: `cell-click` · `hp-damage` · `item-pickup` + `inventory-items` ↔ молоти, зілля · `destructible-blocks` ↔ камʼяні стіни (?) · `seed-share` ↔ Dungeon Seed · `dungeon-generation` ↔ процедурні мапи · `codex-window` ↔ бестіарій · `tutorial-window` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+sum-of-levels-clue`, `+xp-level-up`, `+monster-bestiary` — повтор пропозицій з [dragonsweeper](dragonsweeper.md).
  - `+guaranteed-start-kit` «Гарантовані інструменти біля старту генерованої мапи» · levels/generation · 🌱.
  - `+memory-marker-trap` «Пастка-позначка, що лишає слід монстра» · entities/interact · 🌱 (?).

## Пропозиції до словників
- `+feature:auto-pickup` — предмети підбираються самі.
- `+feature:auto-level-up` — рівень піднімається без підтвердження.
- `+feature:show-monster-levels` — показувати рівні відкритих монстрів (допомога памʼяті).

## Джерела
- ⭐ [itch.io: Dungeon Squire](https://mvolution.itch.io/squire) — «Minesweeper meets Roguelike», «direct descendant of Dragonsweeper», HTML5 + Android, тач, colorblind/high-contrast, туторіал; коментарі (бестіарій, easy, auto-pickup/level-up, молоти, лук, посох, slime master, leprechaun, XP).
- [Девлог: «Is the Game Always Solvable?»](https://mvolution.itch.io/squire/devlog/901500/is-the-game-always-solvable) — вогняні/камʼяні стіни, 4 молоти + 3 зілля в старті, шанси вгадування, seed-коди, схвалення автора Dragonsweeper.
- [Девлог](https://mvolution.itch.io/squire/devlog) — бета 14.02.2025 (10+ монстрів, процедурні мапи, seed), RC1 22.02 (Ancient Skeleton), 1.0 28.02.2025, Dark Lord, easy-вступ, аватари ч/ж, показ рівнів монстрів, тривалість на екрані перемоги.
- [Google Play](https://play.google.com/store/apps/details?id=com.mvolution.squire) — сторінка існує, опис не дістав.

## Непевне
- (?) Числа = сума рівнів, як у Dragonsweeper, — не підтверджено (лише «numbers indicate nearby monsters» і «mechanics very close»).
- (?) Що саме роблять молот (ламає стіну чи відкриває клітину), лук, посох, броня.
- (?) Вогняна стіна — монстр, пастка чи місцевість; чи камʼяна стіна ламається молотом.
- (?) Ancient Skeleton: «magic trap variation on floor tiles» — механіка неясна.
- (?) Розмір поля, крива XP, кількість HP — ніде не названо.
