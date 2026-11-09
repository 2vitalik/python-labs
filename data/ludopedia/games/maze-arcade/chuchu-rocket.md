---
title: ChuChu Rocket!
slug: chuchu-rocket
aka: [ChuChu Rocket, チューチューロケット!, Chu Chu Rocket]
family: maze-arcade
also: [program-robots]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: online
  info: full
  random: runtime
  goal: score
year: 1999
platforms: [Dreamcast, GBA (2001), iOS (2011), Android (2011), Wii U VC (2015)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/ChuChu_Rocket!", best: true, note: "правила: прямо й праворуч біля стін, 3 стрілки, найстаріша зникає, кіт ламає стрілку за 2 удари; режими, онлайн"}
  - {kind: other, url: "https://theghz.com/chu2/chu2/chu2.html", note: "фанатський гайд: поле 12×9, 8 подій рулетки, третина мишей за кота, золота миша 50, режими й ліміти редактора"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/チューチューロケット!", note: "JA: правила пазл-режиму, кількість пазлів у версіях"}
  - {kind: strategywiki, url: "https://www.strategywiki.org/wiki/ChuChu_Rocket!/Stage_Challenge", note: "Stage Challenge (бачив у пошуку; агентам закрито)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=ChuChu+Rocket+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [move-auto, turn-when-blocked, cursor-place, timed-despawn, speed-per-type, spawn-points, environment-death, all-on-targets, collect-quota, event-points, ai-opponent, realtime-ai, online-multiplayer, restart-level, level-bank, puzzle-select, in-game-editor, editor-map-check, level-exchange, mode-select, match-setup, lobby-window, game-screen, main-menu, +direction-arrow-tile, +arrow-limit-fifo, +arrow-wear, +bonus-roulette, +shared-field-versus, +rocket-steal-share, +place-then-run, +taunt-button]
proposes: ["+effect:steal_share", "+window:roulette", "+ui:rocket-counters", "+feature:taunt", "+card:direction-arrow-tile", "+card:arrow-limit-fifo", "+card:arrow-wear", "+card:rocket-steal-share", "+card:place-then-run"]
author: opus
date: 2026-11-09
---

# ChuChu Rocket! — стрілки на клітинах у реальному часі: заганяй мишей у свою ракету, котів — у чужу

## Суть
Гравець не має аватара: він курсором кладе на клітини стрілки, а миші (ChuChu) і коти (KapuKapu) самі біжать прямо й слухаються стрілок. Миша в ракеті — очко власнику ракети, кіт у ракеті зʼїдає третину її мишей. До чотирьох гравців ділять одне поле, і в кожного лише 3 стрілки одночасно: нова стирає найстарішу, а кіт ламає стрілку двома ударами в лоб. Пазл-режим — та сама фізика, але стрілки ставляться до старту, і потім лише дивишся на симуляцію.

## Поле і час
- Поле 12×9 = 108 клітин (гайд theghz): стіни, дірки, люки-спавнери, ракети гравців.
- Real-time: миші й коти рухаються безперервно, миші швидші за котів; подія рулетки може вдвічі сповільнити чи пришвидшити гру.
- Battle: таймер матчу (Team Battle — 3 хв за замовчуванням); Stage Challenge — 30 с на стадію; Puzzle — без часу: розставив, запустив, дивишся.
- Усе поле видно всім; iPad-версія показує чотири поля гравців на одному екрані.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Курсор гравця | — | колір гравця | ставить стрілки; не сутність поля |
| ChuChu (миша) | neutral | швидша за кота | біжить прямо; біля стіни повертає праворуч; слухається стрілок |
| Золота миша | neutral | = 50 мишей | як миша; у ракеті дає 50 |
| «?»-миша | neutral | — | у ракеті запускає рулетку подій |
| KapuKapu (кіт) | enemy | повільніший | рух як у миші; зʼїдає мишей; у ракеті — забирає третину |
| Стрілка | terrain | власник, ліміт 3, «HP» 2, тане з часом | розвертає того, хто на неї став |
| Ракета | sink | колір гравця | миша → +1, золота → +50, кіт → −⅓ мишей |
| Люк | spawner | — | випускає мишей, зрідка котів |
| Дірка | hazard | — | хто впав — зникає |
| Стіна | static | — | непрохідна; упор → поворот праворуч |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `move(mouse|cat, facing)`.
- КОЛИ `blocked(mouse|cat)` → ТО `face(a, right)`.
- КОЛИ `enter(mouse|cat, arrow)` → ТО `face(a, arrow_dir)`.
- КОЛИ `enter(cat, arrow)` → ЯКЩО `facing(cat, against arrow_dir)` → ТО `counter(arrow_hp, -1)` (стрілка зменшується); КОЛИ `counter(arrow_hp, ==, 0)` → ТО `disappear(arrow)` — два удари в лоб.
- КОЛИ `input(place, dir)` → ЯКЩО `free(cell)` → ТО `place(player, arrow[dir])`; ЯКЩО `count(own_arrows, ==, 3)` → ТО `disappear(oldest_arrow)` перед новою.
- КОЛИ `timer(arrow_life)` → ТО `disappear(arrow)` — стрілки згасають самі.
- КОЛИ `rng(p)` → ТО `spawn_at(mouse, hatch)`; рідше — `spawn_at(cat, hatch)`, `spawn_at(gold_mouse, hatch)`, `spawn_at(question_mouse, hatch)`.
- КОЛИ `contact(cat, mouse)` → ТО `disappear(mouse)`.
- КОЛИ `enter(mouse|cat, hole)` → ТО `disappear_a`.
- КОЛИ `enter(mouse, rocket)` → ТО `disappear_a`, `score(+1)` власнику ракети; золота — `score(+50)`.
- КОЛИ `enter(cat, rocket)` → ТО `disappear_a`, `custom: «зʼїдає третину мишей у цій ракеті»`.
- КОЛИ `enter(question_mouse, rocket)` → ТО `window(roulette)` → одна з 8 подій випадково:
  - Mouse Mania: `custom: «коти зникають»`, `spawn_at(mouse×many, hatch)` потоком.
  - Mouse Monopoly: `custom: «велика група мишей одразу в ракету одного гравця»`.
  - Cat Mania: `custom: «зникають усі миші й коти»`, `spawn_at(cat, hatch)`.
  - Cat Attack: `custom: «усім, крім одного, по коту в ракету»`.
  - Place Arrows Again (Timeout): `disappear(all arrows)`, коротка пауза.
  - Everybody Move: `swap(rockets)` — ракети міняються місцями.
  - Slow Down: `speed(all, ×0.5)` · Speed Up: `speed(all, ×2)`.
- КОЛИ `counter(match_time, ==, 0)` → ТО `custom: «перемагає гравець (команда) з найбільшою кількістю мишей у ракеті»`.
- Puzzle: КОЛИ `input(R)` → ТО `custom: «старт симуляції; нові стрілки ставити вже не можна»`; повторне `input(R)` → `speed(all, ×2)`; `input(L)` → `restart`.
- Puzzle: КОЛИ `contact(cat, mouse)` або `enter(mouse, hole)` або `enter(cat, rocket)` → ТО `restart`; КОЛИ `all_gone(mouse)` → ЯКЩО `custom: «усі в ракетах»` → ТО `win`.
- Stage Challenge: КОЛИ `counter(time_left, ==, 0)` → ЯКЩО `not custom: «завдання виконано»` → ТО `lose`; завдання: усіх мишей у ракету / те саме з котом / усіх мишей котові / 100 мишей / «котячий футбол» 2×2.
- Редактор: КОЛИ `input(save)` → ЯКЩО `custom: «кожна миша може врятуватись»` → ТО `custom: «зберегти»`; інакше відмова.
- Перемога: Battle — найбільше мишей до кінця часу (кілька матчів); Puzzle — усі миші в ракетах. Поразка в Puzzle — будь-яка втрачена миша чи кіт у ракеті. Рахунок: миша 1, золота 50, кіт −⅓.

## Керування і ввід
- Курсор ходить полем (Dreamcast — аналоговий стік, GBA — хрестовина); кнопка-напрямок кладе стрілку відповідного напрямку під курсор (?).
- Puzzle: R — старт / пришвидшення, L — скинути поле до початкового.
- Battle: L/R — «дражнилки» (коли програєш / ведеш).
- Онлайн (Dreamcast): затримка ≈ 2 с між натиском і появою стрілки; чат екранною або фізичною клавіатурою.

## Вікна, меню, HUD
- `main-menu` → `mode-select`: 4P Battle · Team Battle · Puzzle · Stage Challenge · Puzzle Edit · Network.
- `match-setup`: час матчу (3 хв за замовчуванням), кількість матчів 1–5 (2 за замовчуванням), одне з 24 полів, тип CPU-суперника (Weak · Hates Cats · Loves Mice · Tough · Random).
- `game-screen`: поле 12×9, ракети чотирьох кольорів з `rocket-counters` (миші в ракеті), курсори гравців, `timer-countdown`.
- `roulette` — оверлей рулетки подій після «?»-миші.
- `puzzle-select` — 4 набори по 25 (Normal · Hard · Special · Mania) = 100 пазлів.
- `editor-window` — Puzzle Edit: до 100 мишей, 20 котів, 30 ракет на поле; збереження 25 пазлів у VMU.
- `lobby-window` + `chat` — мережевий режим Dreamcast; обмін пазлами.
- `end-screen` — результати матчу.

## Фічі поза полем
- `online-multiplayer` (перша онлайн-гра Dreamcast; фанати підняли сервери 2016), `local-multiplayer` до 4, на GBA — лінк-кабелем з одного картриджа.
- `level-editor` з перевіркою розвʼязності, `level-sharing` (DC: аплоад/даунлоад; GBA містить 2500 з ~17000 пазлів користувачів).
- `ai-opponent-levels` — 5 типів CPU.
- `unlockables`: усі 25 стадій Challenge → миші-Чао; усі 100 пазлів → миші-Найтопіани.
- `puzzle-bank` (DC 100, iOS 145, Android 500+).

## Варіації й родичі
- GBA (2001) — усе, крім онлайну, + пазли користувачів; iOS/Android — більше пазлів, батл через Bluetooth/Wi-Fi; Wii U VC — перевидання GBA.
- У корпусі: [Mouse Trap](mouse-trap.md) — миші в лабіринті й двері, якими керує гравець; [Lightbot](../program-robots/lightbot.md) — програмування агента наперед, як Puzzle-режим.
- **Осі варіацій**: стрілка — «вічна / тане з часом / ламається ударами»; ліміт — «запас на рівень (Puzzle) / N одночасно з FIFO (Battle)»; час — «розстав і запусти / real-time»; ціль — «свої миші в свою ракету / чужі коти в чужу».

## Цікавинки для курсу
- Автономні агенти «прямо, біля стіни праворуч» + стрілки на клітинах як непряме керування — 🥉.
- Ліміт 3 стрілки з FIFO-витісненням найстарішої — 📎.
- Знос стрілки: кіт у лоб зменшує її, другий удар знищує — 📎.
- Puzzle «розстав і запусти» з детермінованою симуляцією + перевірка розвʼязності в редакторі — 🥈.
- Рулетка з 8 глобальних подій (помножити швидкість, переставити ракети, злива мишей) — 🥉.
- Розвʼязувач пазла: перебір розстановок стрілок із симуляцією до стабільного стану — 🥇.

## Мапа на каталог
- Є: `move-auto` ↔ миші й коти · `turn-when-blocked` ↔ праворуч біля стіни · `cursor-place` ↔ стрілка під курсор · `timed-despawn` ↔ стрілки тануть · `speed-per-type` ↔ миші швидші · `spawn-points` ↔ люки · `environment-death` ↔ дірки · `all-on-targets` ↔ Puzzle · `collect-quota` ↔ «100 мишей» · `event-points` · `ai-opponent` + `realtime-ai` · `online-multiplayer` · `restart-level` · `level-bank` + `puzzle-select` · `in-game-editor` + `editor-map-check` + `level-exchange` · `mode-select` · `match-setup` · `lobby-window` · `game-screen` · `main-menu`.
- **Нема** → пропозиції карток:
  - `+direction-arrow-tile` «Стрілка на клітині розвертає того, хто став» · entities/interact · 📎 · слот {owner, lifetime, hp}.
  - `+arrow-limit-fifo` «N поставлених одночасно, нова стирає найстарішу» · entities/legality · 🌱 · слот {n: 3}.
  - `+arrow-wear` «Ворог зношує поставлений обʼєкт ударами» · entities/state · 📎 · слот {hits: 2}.
  - `+bonus-roulette` (повтор) — рулетка з 8 подій.
  - `+shared-field-versus` (повтор) — 4 гравці на одному полі.
  - `+rocket-steal-share` «Ворог у базі забирає частку очок» · game-logic/score · 🌱 · слот {share: 1/3}.
  - `+place-then-run` «Розстав і запусти: ввід лише до старту симуляції» · game-logic/program · 🥉.
  - `+taunt-button` «Дражнилка суперникові» · interface/input · 🌱.

## Пропозиції до словників
- `+effect:steal_share` — забрати частку лічильника (кіт у ракеті → −⅓).
- `+window:roulette` — оверлей випадкової події.
- `+ui:rocket-counters` — лічильники мишей біля кожної ракети.
- `+feature:taunt` — дражнилки в батлі.
- `+card:direction-arrow-tile`, `+card:arrow-limit-fifo`, `+card:arrow-wear`, `+card:rocket-steal-share`, `+card:place-then-run` — див. «Мапу на каталог».

## Джерела
- ⭐ [Wikipedia: ChuChu Rocket!](https://en.wikipedia.org/wiki/ChuChu_Rocket!) — рух прямо і праворуч біля стін, стрілки 4 напрямків, 3 на полі з витісненням найстарішої, згасання, кіт ламає стрілку за 2 удари; Puzzle, Puzzle Edit, Challenge, Battle до 4, онлайн, GBA-версія.
- [Гайд theghz.com](https://theghz.com/chu2/chu2/chu2.html) — поле 12×9, миші швидші за котів, дірки, кіт у ракеті −⅓, золота миша 50, 8 подій рулетки, Team Battle 3 хв, 24 поля, CPU-типи, 25 стадій Challenge по 30 с, 100 пазлів, ліміти редактора, керування L/R.
- [Wikipedia JA](https://ja.wikipedia.org/wiki/チューチューロケット!) — стрілка відбиває кота до 2 разів, пазл-правила (усі стрілки до старту), «?»-миша, кількість пазлів у версіях, розблоковки.
- [StrategyWiki: Stage Challenge](https://www.strategywiki.org/wiki/ChuChu_Rocket!/Stage_Challenge) — бачив у пошуку, не відкривав.
- YouTube: пошук «ChuChu Rocket gameplay».

## Непевне
- (?) Повний алгоритм на упорі: праворуч, якщо й там стіна — ліворуч, потім назад — з памʼяті; джерела кажуть лише «праворуч».
- (?) Стіни — на ребрах між клітинами чи цілі клітини.
- (?) Розкладка кнопок для стрілок (по кнопці на напрямок) і чи можна класти стрілку на дірку/ракету.
- (?) Тривалість життя стрілки й частоти спавну мишей/котів/«?»-мишей.
- (?) Challenge-режим: EN-вікі — кооператив, 30 с, без ліміту стрілок; гайд — по 3 стрілки, як у Battle.
- (?) Назви подій рулетки різняться між версіями (Chu-chu Fever / Mouse Mania тощо); GBA має ще Night Time і Kitten Mania (за результатами пошуку).
- (?) «Кількість матчів 1–5» — це кількість раундів чи перемог до виграшу.
- (?) Розблоковка за 100 пазлів: гайд — миші-Найтопіани, JA-вікі — Piano з NiGHTS.
