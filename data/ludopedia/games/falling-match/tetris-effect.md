---
title: Tetris Effect / Tetris Effect Connected
slug: tetris-effect
aka: [Tetris Effect Connected, TEC, Тетріс Ефект]
family: falling-match
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: score
year: 2018
platforms: [PS4, PS VR, PC, Quest, Xbox, Switch, PS5]
links:
  - {kind: fandom, url: "https://tetris.wiki/Tetris_Effect", best: true, note: "TetrisWiki: Zone, назви Zone-очисток, множник, Journey, 17 Effect-режимів, Connected, Zone Battle"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tetris_Effect", note: "історія, платформи, VR, Connected (2020)"}
  - {kind: steam, url: "https://store.steampowered.com/app/1003590/", note: "Tetris Effect: Connected — режими, кросплей, Friend Match до 8 людей"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=tetris+effect+zone+gameplay", note: "пошук; геймплей Zone"}
stage: v1
coverage: 60
mechanics: [gravity-fall, multi-cell-size, keyboard-controls, progress-acceleration, event-points, combo-multiplier, score-records, leaderboard, time-out, time-bonus, game-pause, end-screen, garbage-attack, simultaneous-versus, online-multiplayer, next-queue, mode-select, background-music, achievements-window, +zone-time-stop, +stack-cleared-at-bottom, +beat-synced-feedback, +relax-no-game-over, +mystery-events, +coop-vs-boss, +revive-rhythm-taps]
proposes: ["+trigger:meter_full", "+effect:time_stop", "+effect:stash_line", "+effect:reset_field", "+effect:random_event", "+ui:zone-meter", "+ui:zone-line-counter", "+feature:mode-chill", "+feature:weekend-event", "+feature:practice-no-lose", "+card:zone-time-stop", "+card:stack-cleared-at-bottom"]
author: opus
date: 2026-11-09
---

# Tetris Effect — Guideline-тетріс під музику, де Zone зупиняє час і складає зчищені ряди на дно

## Суть
База — сучасний [Tetris](tetris.md) за Guideline: колодязь 10×20, SRS, hold, hard drop, 1–4 next. Нове — **Zone**: лінії наповнюють метр, гравець у будь-який момент «зупиняє час», гравітація зникає, а кожен повний ряд не зникає, а **опускається на дно** стеку; коли Zone закінчується, усі накопичені ряди вибухають разом — можна зчистити понад 4 ряди однією дією (до 20+). Друга ідея — синестезія: гра привʼязана до біта, кожна з ~30 сцен має свою тему й музику. Connected (2020) додає кооп утрьох проти AI-бос і versus із Zone.

## Поле і час
- Поле, спавн, кольори, обертання, lock delay — як у [tetris.md](tetris.md) (SRS); Classic Score Attack — NRS (NES-обертання) без hold.
- Real-time з тіком кадру; зовнішній темп — етапи Journey з трьома секціями різної швидкості.
- Zone — окремий **режим часу**: гравітація = 0, але фігура, що торкнулась стеку, лочиться після затримки; таймер Zone тече. Зчищені в Zone ряди формують шар «стовпчик вибуху» знизу поля і зсувають решту стеку вгору.
- Connected, фаза Zone: три поля гравців **зливаються в одне** з каскадною гравітацією, гравці ставлять фігури по черзі.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Активна фігура | player | тип, стан повороту | як у Tetris; у Zone не падає сама |
| Клітина стеку | tile | колір | як у Tetris |
| Zone-ряд | tile | порядковий номер у Zone | повний ряд у Zone: замість зникнення опускається на дно, лежить як суцільний ряд до кінця Zone |
| Zone-метр | — (ui) | 4 чверті | наповнюється очистками поза Zone; повний — Zone можна активувати |
| Сміттєвий ряд | hazard | сірий, з дірками | з versus/Purify; виштовхує стек угору |
| Інфікований блок (Purify) | hazard | фіолетовий | зʼявляється з часом; мета режиму — зчистити його разом із сірим сміттям |
| Блок-самоцвіт (Target) | object | — | ціль режиму Target: зчистити стопки з ними |
| Бос (Connected) | enemy | HP-рівні, фази | атакує команду «бліцами», за кожні 10 своїх рядів ставить defense-orb |
| Defense-orb боса | object | ≈1 ряд сміття | гасить частину атаки команди |
| Mystery-подія | — (правило) | тривалість | випадковий модифікатор: гігантські фігури, бомби, без hold тощо |

## Правила (КОЛИ → ЯКЩО → ТО)
Спільні з Tetris (спавн, рух, поворот з кіками, hold, lock, top out, рахунок Guideline, B2B, комбо) — див. [tetris.md](tetris.md). Нижче — лише відмінності.
- КОЛИ `pattern(row_full)` → ЯКЩО `not state(game, zone)` → ТО `clear(rows)`, `drop_rows`, `counter(zone_meter, +¼)` (у Journey — за кожні x рядів залежно від складності; у Zone Marathon — за кожні 8 рядів).
- КОЛИ `input(zone)` → ЯКЩО `count(zone_meter, >, 0)` → ТО `custom: «time_stop — гравітація 0, таймер Zone = заряд метра (до 20 с при повному)»`, `set_state(game, zone)`.
- КОЛИ `tick` → ЯКЩО `state(game, zone)` → ТО `timer(-1)`; фігура не падає, `move(piece, down)` лише вводом.
- КОЛИ `pattern(row_full)` → ЯКЩО `state(game, zone)` → ТО `custom: «stash_line — ряд переноситься на дно поля, решта стеку зсувається вгору»`, `counter(zone_lines, +1)`, `score(+100)` бонусом.
- КОЛИ `timer(zone, ==, 0)` → ТО `clear(zone_lines)`, `clear_state(game, zone)`, `custom: «очки за ряди нараховуються лише зараз»`, `flash`, `message(Octoris…)`.
- Назви Zone-очистки: 4–7 Tetris · 8–11 Octoris · 12–15 Dodecatris · 16–17 Decahexatris · 18–19 Perfectris · 20 Ultimatris · 21 Kirbtris · 22 Impossibilitris · 23 Infinitris · 24 Electris · 25+ WTFtris.
- Множник Zone: +1× за кожну Octoris-очистку (8+ рядів); +1×, якщо Zone активовано на повному заряді; максимум 3×.
- КОЛИ `counter(zone_lines, ≥, 8)` → ТО `custom: «Zone Brilliance — інверсія кольорів»` (налаштування MIN/MID/MAX).
- Поразка в Zone: КОЛИ `spawned(piece)` → ЯКЩО `not free(spawn_cells)` → ТО `lose`; Zone закінчується і при top out.
- Journey: КОЛИ `counter(lines, ≥, goal)` → ТО `next_level`; goal 30 / 36 / 48 (Beginner / Normal / Expert), Metamorphosis — 90; рахуються лише очистки поза Zone.
- Relax-режими: КОЛИ `game_over` → ТО `custom: «reset_field — поле й рахунок обнуляються, гра триває»`.
- Focus-режими (All Clear, Combo, Target): база 1 хв; КОЛИ `custom: «успіх режиму (perfect clear / комбо / самоцвіт)»` → ТО `timer(+n)`; КОЛИ `timer(game, ==, 0)` → ТО `game_over`.
- Countdown (5 хв): КОЛИ `counter(pieces, ==, n)` (n = 2/5/8/10) → ТО `spawn_at(I_piece, top)` з падінням.
- Purify (3 хв): КОЛИ `timer(every)` → ТО `spawn_at(infected_blocks, field)`.
- Mystery: КОЛИ `timer(every)` → ТО `custom: «random_event — випадковий модифікатор на N с (велика фігура, бомба, без hold…)»`.
- Master: гравітація 20G від старту, 30 рівнів, 300 рядів; КОЛИ `counter(level, +1)` → ТО `custom: «lock delay і line-clear delay коротшають (M1 ≈ 492 мс → M30 ≈ 92 мс)»`.
- Zone Battle: КОЛИ `timer(zone, ==, 0)` → ТО `send_garbage(by lines and charge)` (напр. 20 рядів при 100% → 17+17); вхідне сміття можна погасити, увійшовши в Zone і зчистивши досить рядів; сміття падає лише після першого drop без очистки; дірки стають «випадковішими» на 20 000 і 60 000 очок.
- Connected: КОЛИ `counter(team_zone_meter, ==, full)` → ТО `custom: «поля зливаються, каскадна гравітація, хід по черзі»`; результат → `damage(boss, solid_garbage)`.
- Connected Revive: КОЛИ `custom: «top out гравця»` → ТО `custom: «Revive — тапи в ритм; потрібно N тапів (Pisces 40 … Tetrimidion 100), T-spin/Tetris додають +5…+15»`.
- Рахунок: Guideline + Zone-бонуси; оцінка за прохід від D/E до SS.

## Керування і ввід
- Як у Tetris (зсув, поворот CW/CCW, soft/hard drop, hold) + **окрема кнопка Zone** (активація будь-коли, якщо метр не порожній).
- Ввід синхронізований зі звуком: кожен рух/поворот/лок звучить у такт музики сцени (тому «гра — інструмент»).
- Revive у Connected — ритмічні натискання.
- VR: той самий ввід з геймпада, поле — в оточенні 360°.

## Вікна, меню, HUD
- `splash-screen` → `main-menu`: Journey · Effect modes · Connected/Multiplayer · Settings · профіль/аватар.
- `mode-select` (Effect modes): групи Classic (Marathon, Zone Marathon, Ultra, Sprint, Master, Classic Score Attack) · Relax (Chill Marathon, Quick Play, Playlist) · Focus (All Clear, Combo, Target) · Adventurous (Countdown, Purify, Mystery).
- `map-window` — мапа Journey: 7 областей, 27 етапів (у Connected — плюс Connected Area 1–5).
- `difficulty-select` для Journey: Beginner · Normal · Expert + Practice (без поразки, низька гравітація).
- `game-screen`: поле з динамічним фоном сцени; `next-piece-preview`, `hold-slot`, `score`, `level-number`, лічильник рядів, `custom: «zone-meter»` (4 сегменти), під час Zone — `custom: «лічильник рядів Zone»` і `timer-countdown`; `action-text` назви Zone-очистки.
- Versus/Connected: `opponent-boards`, `garbage-meter`, HP-шкала боса (`hp-bar`).
- `lobby-window` — Friend Match за Room ID, до 8 людей, глядачі з емодзі (`emote-wheel`).
- `end-screen`: оцінка D…SS, очки, ряди; `leaderboard`; `pause-menu`; `settings-window` (Zone Brilliance MIN/MID/MAX, частинки, ефекти, звук).
- Переходи: main-menu → (Journey) map-window → game-screen → end-screen → наступний етап; main-menu → mode-select → game-screen.

## Фічі поза полем
- Режими: 17 Effect-режимів у 4 групах (див. вище); `mode-marathon`, `mode-zen` (Relax: поразка лише обнуляє поле), `mode-time-attack` (Sprint), `custom: «Ultra»`, `mode-versus` (Zone Battle, Score Attack, Classic Score Attack), `mode-coop` (Connected проти бос), Mystery Battle на 4 (Party Edition).
- `online-multiplayer` з кросплеєм; `spectator` у Friend Match; рейтингові матчі (Ranked).
- `xp-level` — метарівень гравця відкриває режими й аватари (`unlockables`); `custom: «Weekend Ritual — спільнотна подія Сб 12:00 – Нд 12:00 UTC»`.
- `leaderboard-online`, `stats`, `achievements`.
- `cheat-codes`-подібний секрет: код на титулі відкриває етап «1984» (омаж Electronika 60).
- VR як режим подачі; `volume-sliders`, налаштування частинок.

## Варіації й родичі
- [tetris.md](tetris.md) — уся база Guideline; [lumines.md](lumines.md) — той самий автор-ідея (Мідзуґуті): падіння блоків + музика й «таймлайн».
- Zone — родич «заморозки часу» з бонусом; у Tetris 99 нема, у Tetris Effect Connected стає зброєю versus.
- Connected — рідкісний кооп у сімʼї: спільне поле під час Zone (порівн. [puyo-puyo.md](puyo-puyo.md) versus без коопу).
- **Осі варіацій**: що робить зчищений ряд (зникає / стає на дно до кінця Zone) · хто тримає час (гравітація / гравець вимикає її на заряд) · ціна поразки (кінець / обнулення поля в Relax) · поле (своє / злите з напарниками).

## Цікавинки для курсу
- Zone поверх готового тетрісу: стан «час стоїть», ряд іде на дно замість зникнення, відкладений підрахунок — 🥉 (зміна правила очистки + шар знизу + таймер).
- Таблиця назв за кількістю рядів (Octoris…WTFtris) + множник Zone — 🌱.
- Relax-режим: top out → обнулити поле, а не завершити гру — 🌱.
- Mystery: планувальник випадкових модифікаторів правил на N секунд — 🥈 (правила як знімні обʼєкти).
- Аудіо в такт: квантування звуків вводу до біта — 📎.
- Кооп «зливання полів» з чергою ходів і каскадною гравітацією — 🥇.

## Мапа на каталог
- Є: `gravity-fall`, `multi-cell-size`, `keyboard-controls`, `progress-acceleration` (секції Journey, Master), `event-points`, `combo-multiplier`, `score-records`, `leaderboard`, `time-out` (Ultra, Countdown, Focus), `time-bonus` (Focus), `game-pause`, `end-screen`, `garbage-attack` (Zone Battle), `simultaneous-versus`, `online-multiplayer`, `next-queue`, `mode-select`, `background-music`, `achievements-window`.
- **Нема** → пропозиції карток:
  - `+zone-time-stop` «Зупинка часу за заряд» · game-logic/score · 🥉 · слоти {charge: 4, max_duration}.
  - `+stack-cleared-at-bottom` «Зчищений ряд лягає на дно до кінця режиму» · entities/interact · 🥉.
  - `+beat-synced-feedback` «Звуки вводу в такт музики» · interface/sound · 📎.
  - `+relax-no-game-over` «Поразка обнуляє поле» · game-logic/lose · 🌱.
  - `+mystery-events` «Випадкові тимчасові модифікатори правил» · game-logic/difficulty · 🥈.
  - `+coop-vs-boss` «Кооп проти AI-боса зі спільним полем» · game-logic/opponent · 🥇.
  - `+revive-rhythm-taps` «Воскресіння ритмічними натисками» · game-logic/lose · 📎.

## Пропозиції до словників
- `+trigger:meter_full` — шкала заряду наповнилась (Zone, магія Tetrisphere).
- `+effect:time_stop` — вимкнути гравітацію/таймер світу, крім вводу гравця, на N с.
- `+effect:stash_line` — повний ряд не зникає, а переноситься на дно поля до події.
- `+effect:reset_field` — очистити поле й рахунок без завершення гри (Relax).
- `+effect:random_event` — увімкнути випадкове тимчасове правило (Mystery).
- `+ui:zone-meter` — сегментована шкала заряду; `+ui:zone-line-counter` — лічильник рядів, накопичених у Zone.
- `+feature:mode-chill` — нескінченна гра без поразки з ціллю рядів; `+feature:weekend-event` — спільнотна подія за розкладом; `+feature:practice-no-lose` — практика кампанії без game over.
- `+card:zone-time-stop`, `+card:stack-cleared-at-bottom` — див. «Мапу».
- Вжито наявні `garbage-meter`, `opponent-boards`, `action-text`, `hold-slot` — ще одна гра для правила трьох.

## Джерела
- ⭐ [TetrisWiki: Tetris Effect](https://tetris.wiki/Tetris_Effect) — Zone (метр, 20 с, ряди на дно, вибух наприкінці), назви очисток 4…25+, множник до 3×, Journey (27 етапів, цілі 30/36/48), 17 Effect-режимів, Master (lock delay M1…M30), Connected (бос, Revive), Zone Battle (таблиця атак), Weekend Ritual, код 1984.
- [Wikipedia: Tetris Effect](https://en.wikipedia.org/wiki/Tetris_Effect) — розробники, платформи й дати, VR, Connected 2020, біт-привʼязка.
- [Steam: Tetris Effect: Connected](https://store.steampowered.com/app/1003590/) — 10+ режимів, 30+ етапів, кросплей Room ID, до 8 людей з глядачами.

## Непевне
- (?) Точна кількість рядів на чверть метра в Journey за складністю («x lines») — TetrisWiki не дає.
- (?) Мінімальний заряд для активації Zone — «будь-який непорожній» з памʼяті; сторінка каже лише «коли метр наповнено».
- (?) Кількість етапів: Wikipedia — 30, TetrisWiki — 27 у Journey (+ Connected-області, «1984»).
- (?) Синхронізація звуку вводу з бітом — опис з рецензій/памʼяті, не з технічного джерела.
- (?) Таблиці атаки Zone Battle для інших кількостей рядів — у статті лише приклади (10, 20, 23 ряди).
- (?) Кнопка Zone на клавіатурі/геймпаді — розкладку не звірено.
