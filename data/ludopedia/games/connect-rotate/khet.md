---
title: Khet (Deflexion, Laser Chess)
slug: khet
family: connect-rotate
also: [chess-abstract]
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 2005
platforms: [board, PC (Steam), iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Khet_(game)", best: true, note: "повні правила: фігури, дзеркала, хід, постріл, 1.0 vs 2.0, розширення, історія"}
  - {kind: steam, url: "https://store.steampowered.com/app/312720/Khet_20/", note: "цифрова Khet 2.0: AI 5 рівнів, онлайн з Elo, hot-seat"}
  - {kind: steam, url: "https://store.steampowered.com/app/327610/Khet_20_Eye_of_Horus_Beam_Splitter/", note: "DLC: дільник променя"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Laser_Chess", note: "предок 1987 (Mike Duppong): лазер як одна з дій"}
  - {kind: other, url: "https://dicetower.com/board-game/16991", note: "картка настолки (з черги, не відкривав)"}
  - {kind: other, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Khet", note: "пошук BGG; сторінка гри віддає 403"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Khet+2.0+how+to+play", note: "пошук; правила за 5 хв"}
stage: v1
coverage: 70
mechanics: [piece-move-patterns, orientation-state, legal-move-highlight, turn-enforcement, hot-seat, ai-opponent, ai-minimax, +online-multiplayer, move-timer, game-screen, main-menu, end-screen, settings-window, +beam-tracing, +mirror-reflect, +rotate-as-move, +swap-on-contact, +beam-capture, +restricted-squares, +mandatory-action, +repetition-draw, +rating-system, +beam-splitter, +setup-presets]
proposes: ["+role:piece", "+role:source", "+trigger:turn_end", "+trigger:beam_hit", "+trigger:repetition", "+cond:hit_side", "+cond:turn_of", "+effect:rotate", "+effect:reflect", "+effect:emit_beam", "+effect:swap", "+effect:split_beam", "+ui:beam-preview", "+feature:setup-presets", "+card:beam-capture", "+card:restricted-squares", "+card:mandatory-action", "+card:beam-splitter"]
author: opus
date: 2026-11-02
---

# Khet — шахи з дзеркалами: зроби хід або поверни фігуру, і твій лазер стріляє

## Суть
Двоє гравців на дошці 10×8 рухають фігури-дзеркала. Хід — **або** зсунути фігуру на клітину, **або** повернути її на 90°; потім гравець **обовʼязково** стріляє своїм лазером. Промінь відбивається від дзеркальних граней, а фігуру, яку він влучив у недзеркальну грань, знімає з дошки — **незалежно від кольору**, тож можна збити і свою. Перемагає той, чий промінь влучить у фараона суперника. Взяття не ходом, а геометрією променя — головна ідея.

## Поле і час
- Дошка 10×8 клітин. Частина клітин крайніх вертикалей (правий файл і ліві кути) мічена кольором — туди може ставати лише одна сторона; це не дає будувати неприступні фортеці.
- Покроково, по черзі; хід = дія + постріл. Час — без обмежень (на дошці), у цифровій версії — опційно.
- Розстановки: Classic (для новачків), Imhotep, Dynasty; гравці можуть домовитись про будь-яку.
- Khet 1.0: лазер вмонтовано в стінку дошки; Khet 2.0: лазер — на фігурі-сфінксі в куті.
- Розширення Tower of Kadesh (2008): другий рівень дошки — вежа з 4 дзеркалами в основі, що піднімають промінь (тоді `field` → `layers`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фараон | piece | 1 на сторону, без дзеркал | будь-яке влучання → знищений, власник програв |
| Піраміда | piece | 7; одне діагональне дзеркало | відбиває на 90° з двох боків; влучання в дві інші грані → знята |
| Скарабей (Djed у 1.0) | piece | 2; двостороннє дзеркало | відбиває з будь-якого боку — невразливий; може обмінятись місцями з сусідньою фігурою |
| Анубіс (лише 2.0) | piece | 2; щит спереду | влучання в лице поглинається; у бік чи спину → знятий |
| Обеліск (1.0/Deflexion) | piece | 4 (1.0) / 2 (Deflexion); без дзеркал | будь-яке влучання → знятий; «жертва» для захисту |
| Сфінкс (лише 2.0) | source (custom) | 1 у куті; 2 напрямки стрільби | не ходить, лише повертається між двома напрямками; невразливий до променя |
| Лазер у стінці (1.0) | source | фіксований | стріляє з кута дошки |
| Око Гора (розширення) | piece | замінює одного скарабея | як скарабей, але ділить промінь: половина відбивається на 90°, половина йде прямо |
| Мічена клітина | zone | колір сторони | заходити може лише фігура цієї сторони |
| Промінь | projectile | ортогональний | миттєво трасується від лазера до виходу за дошку, поглинання або знищення |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, piece, dir8)` → ЯКЩО `turn_of(owner)` and `free(cell)` and `not cell(cell, enemy_zone)` → ТО `move(piece, cell)`; інакше `block`.
- КОЛИ `input(move, scarab, cell)` → ЯКЩО `occupied(cell, pyramid|anubis)` (будь-якого кольору) → ТО `swap(scarab, b)` (?: обмін з фараоном/сфінксом заборонений).
- КОЛИ `input(rotate, piece, ±90)` → ЯКЩО `turn_of(owner)` → ТО `rotate(piece, ±90)`; сфінкс — лише між двома своїми напрямками.
- КОЛИ `turn_end(side)` → ТО `emit_beam(laser[side])` — **обовʼязково**.
- КОЛИ `beam_hit(piece)` → ЯКЩО `hit_side(mirror)` → ТО `reflect(beam, 90°)`, промінь іде далі.
- КОЛИ `beam_hit(anubis)` → ЯКЩО `hit_side(front)` → ТО `custom: «промінь поглинуто»`, стоп.
- КОЛИ `beam_hit(piece)` → ЯКЩО `not hit_side(mirror|shield)` → ТО `disappear_b`, промінь зупиняється — **будь-якого кольору**.
- КОЛИ `beam_hit(eye_of_horus)` → ТО `split_beam`: одна гілка `reflect(90°)`, друга — прямо.
- КОЛИ `edge(beam)` або `beam_hit(sphinx)` → ТО промінь зникає без наслідків.
- КОЛИ `destroyed(pharaoh[side])` → ТО `win` для суперника (і якщо свій промінь збив свого фараона).
- КОЛИ `repetition(position, 3)` → ТО `draw`.
- Перемога: промінь у фараона суперника. Нічия: трикратний повтор позиції. Рахунку нема.

## Керування і ввід
- Настолка: рух рукою + кнопка на лазері (Khet 2.0 — на сфінксі).
- Цифрова версія: клік по фігурі → `legal-move-highlight` (8 сусідніх клітин) і стрілки повороту ↻/↺; клік по клітині — рух; після дії постріл автоматичний (?); 3D-камера з обертанням.
- Hot-seat за одним компʼютером, AI 5 рівнів, онлайн.

## Вікна, меню, HUD
- `main-menu` (цифрова): локальна гра (hot-seat), проти AI → `difficulty-select` (5 рівнів), онлайн → `lobby-window`; налаштування.
- `character-select` / `custom-window` «Setup»: вибір розстановки Classic / Imhotep / Dynasty (?).
- `game-screen`: дошка, мічені клітини, `turn-indicator`, `selection-highlight`, `legal-move-highlight`, кнопки поворотів, анімація променя з відбиттями, `captured-pieces` (?).
- `end-screen`: хто переміг, зміна Elo для онлайн-партій.
- `leaderboard`: Steam-рейтинг Elo; `achievements-window` (Steam).
- `settings-window`: камера, графіка, контролер/Big Picture.
- Переходи: main-menu → (режим) → game-screen → end-screen → main-menu / реванш.

## Фічі поза полем
- `hotseat`, `ai-opponent-levels` (5), `online-multiplayer` з `rank-tiers`/Elo і `leaderboard-online`.
- `setup-presets`: три стандартні розстановки + домовлені.
- Розширення як `custom-rules`: Eye of Horus (дільник), Tower of Kadesh (другий рівень).
- `achievements`; без DRM для офлайну.

## Варіації й родичі
- Laser Chess (Mike Duppong, 1987) — предок: лазер як одна з кількох дій за хід.
- Deflexion (2005) → Khet 1.0 → Khet 2.0 (сфінкси, анубіси) → ThinkFun Laser Chess (2017, ті самі правила, sci-fi дизайн).
- Родичі: Deflektor і LaserTank (промінь і дзеркала соло), шахи (фігури, черга, повтор).
- Осі варіацій: **хто/коли стріляє: обовʼязково щоходу / як дія на вибір** · **дія: рух / поворот / обмін** · **захист фігури: дзеркало / щит-поглинач / невразливість** · **промінь: один / розщеплений** · **дошка: одна / з вежею**.

## Цікавинки для курсу
- Трасування променя після кожного ходу з таблицею «грань × напрям → відбити / поглинути / знищити» — 🥉.
- Хід = рух **або** поворот фігури з орієнтацією — 📎 (`orientation-state` в чистому вигляді).
- Знищення «чужими руками»: промінь не розрізняє кольорів — 🌱 як правило, але цікаве для AI.
- Дільник променя (дерево трасування замість лінії) — 📎.
- AI: minimax з оцінкою «наскільки фараон під загрозою» — 🥇 (генерація ходів + симуляція променя).
- Трикратний повтор як нічия — 🥈 (хеш позиції; є картка-пропозиція з шахів).

## Мапа на каталог
- Є: `piece-move-patterns` (король-подібний рух на 8) · `legal-move-highlight` · `turn-enforcement` · `hot-seat` · `ai-opponent`, `ai-minimax` · `move-timer` (онлайн) · `orientation-state` (фігура з гранями) · `game-screen`, `main-menu`, `end-screen`, `settings-window`.
- **Нема** → пропозиції карток:
  - `+beam-tracing` «Трасування променя» · entities/combat · 🥉 — з Deflektor/LaserTank.
  - `+mirror-reflect` «Дзеркало з кутом» · entities/interact · 📎.
  - `+rotate-as-move` «Поворот як хід» · entities/move · 📎 — з чесс-сімʼї.
  - `+swap-on-contact` «Обмін місцями при вході» · entities/interact · 📎 — скарабей.
  - `+beam-capture` «Знищення променем за гранню» · entities/combat · 📎 · слот {friendly_fire: true}.
  - `+restricted-squares` «Клітини лише для однієї сторони» · entities/legality · 🌱.
  - `+mandatory-action` «Обовʼязкова дія наприкінці ходу» · game-logic/opponent · 🌱 (постріл).
  - `+repetition-draw` «Нічия повторенням» · game-logic/constraints · 🥈 — з шахів.
  - `+rating-system` «Рейтинг гравців» · interface/results · 🥈 — Elo.
  - `+beam-splitter` «Дільник променя» · entities/interact · 📎.
  - `+setup-presets` «Набір стартових розстановок» · levels · 🌱.

## Пропозиції до словників
- `+role:piece` ⏳ підтверджується; `+role:source` — сфінкс/лазер як джерело променя.
- `+trigger:turn_end` ⏳ — постріл після дії; `+trigger:beam_hit` (з Deflektor/LaserTank); `+trigger:repetition` (з шахів).
- `+cond:hit_side(a, mirror|shield|plain)` — грань, у яку влучив промінь (з LaserTank; тут третя гра → кандидат на ⏳); `+cond:turn_of` ⏳.
- `+effect:rotate` ⏳ · `+effect:reflect` · `+effect:emit_beam` (з Deflektor) · `+effect:swap` ⏳ · `+effect:split_beam` — новий: промінь розгалужується.
- `+ui:beam-preview` — показ траєкторії променя до пострілу (?) — корисно для навчання.
- `+feature:setup-presets` — вибір стартової розстановки.

## Джерела
- ⭐ [Wikipedia: Khet (game)](https://en.wikipedia.org/wiki/Khet_(game)) — 10×8, 14 фігур (12 у Deflexion), склад фігур, хід «рух або поворот → постріл», дзеркала, Анубіс, Сфінкс, Eye of Horus, Tower of Kadesh, нічия повтором, історія (Tulane, 2005).
- [Steam: Khet 2.0](https://store.steampowered.com/app/312720/Khet_20/) — AI 5 рівнів, онлайн з Elo, hot-seat, 3D-камера (BlueLine Games, 2014).
- [Steam: Eye of Horus Beam Splitter](https://store.steampowered.com/app/327610/Khet_20_Eye_of_Horus_Beam_Splitter/) — перша цифрова реалізація дільника.
- [Wikipedia: Laser Chess](https://en.wikipedia.org/wiki/Laser_Chess) — предок 1987.
- [Dice Tower](https://dicetower.com/board-game/16991) — картка настолки (з черги пошукового агента).
- BGG: [пошук Khet](https://boardgamegeek.com/geeksearch.php?action=search&q=Khet); YouTube: пошук «Khet 2.0 how to play».

## Непевне
- (?) Склад 2.0: 1 фараон + 7 пірамід + 2 скарабеї + 2 анубіси + сфінкс = 13, а Wikipedia пише «14 pieces» (це рахунок 1.0: 1+7+2+4) — уточнити в правилах 2.0.
- (?) Обмеження обміну скарабея (не з фараоном/скарабеєм/сфінксом) — з памʼяті; Wikipedia каже лише «whatever its color».
- (?) Точна розмітка мічених клітин (які саме клітини якого кольору) і повні схеми Imhotep/Dynasty — Wikipedia не дає.
- (?) Цифрова версія: чи постріл автоматичний, чи є превʼю променя, екран вибору розстановки.
- (?) Офіційний сайт khet.com не відповів (connection refused); сторінка ThinkFun редіректить на Ravensburger і віддає 403.
