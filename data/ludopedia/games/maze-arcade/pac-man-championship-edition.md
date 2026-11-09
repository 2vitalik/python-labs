---
title: "Pac-Man Championship Edition / DX (Пекмен: чемпіонське видання)"
slug: pac-man-championship-edition
aka: [Pac-Man CE, PMCE, Pac-Man CE DX, Pac-Man Championship Edition DX+, CE DX]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: none
  goal: score
year: 2007
platforms: [Xbox 360, PS3, PC (Steam, DX+)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pac-Man_Championship_Edition", best: true, note: "CE 2007: половинки лабіринту, фрукт, ліміт часу, 6 режимів"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pac-Man_Championship_Edition_DX", note: "DX 2010: сплячі привиди, потяг, бомби, slow-motion, режими, DX+"}
  - {kind: steam, url: "https://store.steampowered.com/app/236450/PACMAN_Championship_Edition_DX/", note: "DX+ на PC: режими, налаштування, лідерборди, DLC-курси"}
  - {kind: steam, url: "https://store.steampowered.com/app/441380/PACMAN_CHAMPIONSHIP_EDITION_2/", note: "наступник CE 2 (2016)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=pac-man+championship+edition+dx+gameplay", note: "пошук; геймплей DX"}
stage: v1
coverage: 70
mechanics: [move-4dir, move-auto, item-pickup, touch-death, temporary-modes, spawn-points, respawn, body-queue, chase-player, speed-per-type, event-points, combo-multiplier, extra-life-threshold, progress-acceleration, time-out, inventory-items, collect-quota, score-records, leaderboard, replay, mode-select, game-settings, theme-select, difficulty-levels, achievements-window, game-screen, end-screen, sound-effects, background-music, +half-maze-refresh, +sleeping-enemy, +ghost-train, +near-miss-slowmo, +panic-bomb, +score-driven-speed, +speed-drop-on-death, +score-attack-timer]
proposes: ["+effect:time_scale", "+effect:regen_region", "+trigger:near_miss", "+role:follower", "+ui:speed-gauge", "+ui:bomb-stock", "+card:half-maze-refresh", "+card:sleeping-enemy", "+card:ghost-train", "+card:near-miss-slowmo", "+card:panic-bomb", "+card:score-driven-speed", "+feature:course-select"]
author: opus
date: 2026-11-09
---

# Pac-Man Championship Edition / DX — Pac-Man на час: половинки лабіринту оновлюються, привиди збираються в потяг

## Суть
Класичний Pac-Man, перебудований під score attack: рівнів нема, є 5 або 10 хвилин і один рахунок. Лабіринт поділено на дві половини: зʼїв усі точки однієї — на другій зʼявляється фрукт, а зʼїв фрукт — очищена половина заповнюється новим візерунком точок. Швидкість гри росте разом із рахунком і падає після смерті, тож гра сама підлаштовує темп під гравця. DX (2010) додав сплячих привидів, які прокидаються, коли повз них проїхати, і чіпляються за Пекменом «потягом», а також бомби й уповільнення часу при майже-зіткненні.

## Поле і час
- Квадратна сітка-лабіринт у стилі оригіналу, тунелі по краях; поле розділене на ліву і праву половини, кожна з власним набором точок.
- Real-time: Пекмен рухається безперервно, ввід змінює напрям. Глобальний «рівень швидкості» (speed rank) підіймається з ростом рахунку й опускається після смерті та після бомби (DX).
- Таймер режиму (5 хв / 10 хв) — головне обмеження; життя вторинні.
- DX: кілька курсів (Wikipedia — 9, Steam DX+ — 7 у базі + DLC), кожен зі своєю геометрією й «особливостями»; візуальні стилі (Pac-Mania та ін.) міксуються незалежно від курсу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пекмен | player | життя; +1 кожні 20 000 очок (CE) | безперервний рух 4 напрямки; їсть точки, фрукти, переляканих привидів |
| Точка | pickup | належить половині | зникає при контакті; остання точка половини запускає фрукт |
| Енерджайзер | pickup | — | вмикає frightened; повторний продовжує режим і тримає максимальну ціну привида |
| Фрукт / бонус-предмет | pickup | зʼявляється на протилежній половині | контакт → очищена половина отримує новий візерунок точок |
| Половина лабіринту | zone | ліва / права, лічильник точок | порожня → чекає на фрукт; оновлюється новим набором |
| Стіна | static | — | непрохідна |
| Тунель | terrain | 2 входи | перехід на протилежний край |
| Будиночок привидів | spawner | центр поля | звідси виходять привиди; сюди повертаються зʼїдені й «відкинуті» бомбою |
| Привид (Blinky, Pinky, Inky, Clyde) | enemy | 4 шт. | ганяються за Пекменом; патерни руху успадковані з оригіналу (критика рецензентів) |
| Синій привид | enemy (стан) | час frightened | тікає; зʼїдається; повертається додому |
| Сплячий привид (DX) | enemy | стоїть на місці | нерухомий, доки Пекмен не проїде поруч; тоді прокидається й іде слідом |
| Потяг привидів (DX) | enemy | довжина | ланцюжок прокинутих привидів, що повторює шлях за Пекменом |
| Привид з енерджайзером (DX) | enemy | несе пелету | зʼїдений у frightened — продовжує режим |
| Бомба (DX) | pickup (запас) | обмежена кількість | застосування → усі привиди в центр, швидкість і множник точок падають |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `move(pacman, dir)`; КОЛИ `input(dir)` → ЯКЩО `free(cell_ahead)` → ТО `face(pacman, dir)`.
- КОЛИ `edge(pacman)` → ТО `wrap(pacman)` (тунель).
- КОЛИ `contact(pacman, dot)` → ТО `pickup`, `score(dot_value)`, `counter(half_dots, -1)`.
- КОЛИ `counter(half_dots, ==, 0)` → ТО `spawn_at(fruit, other_half)`.
- КОЛИ `contact(pacman, fruit)` → ТО `pickup`, `score(fruit_value)`, `custom: «очищена половина заповнюється новим візерунком точок»`.
- КОЛИ `contact(pacman, energizer)` → ТО `pickup`, `set_state(ghosts, frightened, T)`; ЯКЩО `state(pacman, powered)` → ТО `timer(+T)`, `custom: «ціна наступного привида не скидається»`.
- КОЛИ `contact(pacman, ghost)` → ЯКЩО `state(ghost, frightened)` → ТО `score(ghost_value)`, `combo(+1)`, `transform(eyes)`; інакше `lives(-1)`.
- КОЛИ `contact(eyes, ghost_house)` → ТО `respawn(ghost, ghost_house)` у звичайному стані.
- КОЛИ `counter(score, >=, 20000·k)` → ТО `lives(+1)` (CE).
- КОЛИ `counter(score, >=, rank_threshold)` → ТО `speed(all, +1 rank)`.
- КОЛИ `died(pacman)` → ТО `speed(all, -rank)`, `respawn(pacman, start)`.
- КОЛИ `counter(time_left, ==, 0)` → ТО `game_over`, `window(end-screen)`; КОЛИ `counter(lives, ==, 0)` → ТО `game_over` раніше.
- DX: КОЛИ `in_range(pacman, sleeping_ghost, r)` → ТО `clear_state(ghost, sleeping)`, `attach(ghost, train)`.
- DX: КОЛИ `state_on(ghost, near_pacman)` → ТО `custom: «звичайний привид забарвлюється веселкою і може стати в потяг»`.
- DX: КОЛИ `contact(pacman, train)` → ЯКЩО `state(train, frightened)` → ТО `custom: «привиди потяга зʼїдаються підряд, ціна росте з кожним»`, `combo(+1)` за кожного.
- DX: КОЛИ `contact(pacman, ghost_with_pellet)` → ЯКЩО `state(ghost, frightened)` → ТО `timer(+T)` (продовжити frightened).
- DX: КОЛИ `in_range(ghost, pacman, near)` → ЯКЩО `not state(ghost, frightened)` → ТО `custom: «короткочасне уповільнення часу, щоб ухилитись»`.
- DX: КОЛИ `input(bomb)` → ЯКЩО `has(pacman, bomb)` → ТО `take(pacman, bomb)`, `respawn(ghosts, ghost_house)`, `speed(all, -k)`, `multiplier(×dot↓)`.
- DX Time Trial: КОЛИ `counter(fruit_eaten, ==, quota)` → ТО `win`, `timer(stop)` → результат = час.
- DX Ghost Combo: `custom: «мета — якнайдовше тримати frightened і зʼїсти якнайбільше привидів»`.
- Перемога: нема (score attack) · Поразка: вичерпано час або життя · Рахунок: точки, фрукти, привиди (ланцюги в потягах — головне джерело очок у DX).

## Керування і ввід
- Чотири напрямки (стік/хрестовина/стрілки); Пекмен їде сам, ввід — лише поворот на найближчому перехресті.
- DX: окрема кнопка бомби; пауза.
- Жодних прицілів чи стрільби: усе багатство — в маршруті через дві половини.

## Вікна, меню, HUD
- `main-menu`: вибір режиму → `mode-select` (CE: Championship · Challenge ×2 · Extra ×3; DX: Score Attack · Time Trial · Ghost Combo), далі вибір курсу і стилю.
- `game-screen`: лабіринт на весь екран; HUD — `score`, `hi-score`, `timer-countdown`, `lives`, `popup-text` (очки привидів/фруктів), `+ui:bomb-stock` (DX), `+ui:speed-gauge` (рівень швидкості) (?).
- `pause-menu`: продовжити · рестарт · вихід.
- `end-screen`: рахунок, місце в рейтингу курсу.
- `leaderboard`: онлайн-лідерборди по режиму і курсу; у DX — ранг на курсі за позицією в загальному рейтингу; `replay-window` — відеоповтори топ-гравців Score Attack.
- `settings-window`: складність, музика, персонажі, візуал лабіринту (Steam DX+).
- `achievements-window` / медалі (DX+).
- Переходи: main-menu → mode-select → вибір курсу → game-screen → end-screen → leaderboard / знову.

## Фічі поза полем
- Режими: `mode-time-attack` (5/10 хв — Score Attack; Time Trial — квота фруктів на швидкість), Ghost Combo, Challenge-режими CE (більше енерджайзерів, лабіринт у темряві).
- `leaderboard-online`, ранги на курсах, `replay` найкращих, виклик друзям (DX+).
- `theme-select`: стилі лабіринту й скіни (Dig Dug, Rally-X, Classic — DLC або за всі медалі).
- `achievements` + медалі; `unlockables` (Classic-скін).
- `difficulty-presets` (налаштування складності на Steam).
- DLC-курси (Big Eater, Championship III, Highway II, Mountain) — `+feature:course-select`.
- «NG News» — стрічка новин у меню DX.

## Варіації й родичі
- Pac-Man (див. `pac-man`) — джерело правил привидів і лабіринту; CE прибрав рівні, лишив один довгий забіг.
- CE (2007) → CE DX (2010) → CE DX+ (2013) → CE 2 (2016); Pac-Man 256 (див. `pac-man-256`) — нескінченний вертикальний лабіринт від тієї ж ідеї «ніколи не зупиняйся».
- **Осі варіацій:**
  - оновлення поля: увесь рівень (оригінал) / половина після фрукта (CE) / нескінченна генерація (256);
  - привиди: 4 мисливці / + сплячі, що збираються в потяг (DX);
  - складність: за номером рівня / за рахунком із відкатом після смерті (CE);
  - рятівний засіб: нема / бомба-скидання (DX) / уповільнення часу при майже-зіткненні (DX);
  - мета: рекорд / квота фруктів на час / максимум привидів.

## Цікавинки для курсу
- Дві половини поля з окремими лічильниками: очистив одну → бонус на іншій → регенерація першої — 🥉: стан «зони» і генерація візерунка точок.
- Потяг привидів: прокинутий привид іде слідом за Пекменом по його шляху (черга позицій, як тіло змійки) — 🥉, картка `body-queue` у новому ролі.
- Динамічна складність: швидкість = f(рахунок), смерть відкочує — 📎, проста формула з великим ефектом.
- Slow-motion при майже-зіткненні: глобальний множник часу, коли ворог у радіусі — 🥉 (окремий «часовий» шар над тіком).
- Бомба як «паніка-кнопка» з ціною (швидкість, множник) — 📎.
- Ланцюг зʼїдених привидів із зростаючою ціною й продовженням режиму — 📎.
- Score attack на таймері замість рівнів — 🌱.

## Мапа на каталог
- Є: `move-auto` + `move-4dir` · `item-pickup` · `touch-death` · `temporary-modes` (frightened) · `spawn-points` + `respawn` (будиночок) · `body-queue` (потяг) · `chase-player` · `speed-per-type` · `combo-multiplier` · `event-points` · `extra-life-threshold` (20 000) · `progress-acceleration` (ранг швидкості) · `time-out` (таймер режиму) · `collect-quota` (Time Trial: квота фруктів) · `inventory-items` (бомби) · `score-records` + `leaderboard` + `replay` · `mode-select` · `game-settings` · `theme-select` · `difficulty-levels` · `achievements-window`.
- **Нема** → пропозиції карток:
  - `+half-maze-refresh` «Половина поля оновлюється після бонусу» · levels/generation · 🥉 · слот {zones: 2|n}.
  - `+sleeping-enemy` «Сплячий ворог прокидається поруч» · entities/state · 📎 · слот {radius}.
  - `+ghost-train` «Вороги вишиковуються ланцюгом за гравцем» · entities/move · 🥉 (дитина `body-queue`).
  - `+near-miss-slowmo` «Уповільнення часу при майже-зіткненні» · entities/state · 🥉 · слот {radius, factor}.
  - `+panic-bomb` «Бомба-скидання ворогів з ціною» · entities/combat · 📎 · слот {stock}.
  - `+score-driven-speed` «Швидкість гри за рахунком» · game-logic/waves · 📎 (поруч `progress-acceleration`).
  - `+speed-drop-on-death` «Відкат складності після смерті» · game-logic/difficulty · 🌱.
  - `+score-attack-timer` «Забіг на фіксований час» · game-logic/lose · 🌱 (поруч `time-out`).

## Пропозиції до словників
- `+effect:time_scale` — глобальний множник часу гри на N тіків (slow-motion DX); не `speed`, бо міняється темп усього світу, а не однієї сутності.
- `+effect:regen_region` — заповнити зону новим набором предметів/клітин (половина лабіринту CE).
- `+trigger:near_miss` — ворог пройшов у радіусі r без зіткнення (DX slow-mo; бонуси «впритул» в аркадах).
- `+role:follower` — ворог/союзник, що повторює шлях за ведучим (потяг привидів).
- `+ui:speed-gauge` — індикатор поточного рівня швидкості гри; `+ui:bomb-stock` — запас бомб.
- `+card:half-maze-refresh`, `+card:sleeping-enemy`, `+card:ghost-train`, `+card:near-miss-slowmo`, `+card:panic-bomb`, `+card:score-driven-speed`.
- `+feature:course-select` — вибір курсу (геометрії лабіринту) незалежно від режиму.

## Джерела
- ⭐ [Wikipedia: Pac-Man Championship Edition](https://en.wikipedia.org/wiki/Pac-Man_Championship_Edition) — половинки, фрукт → новий лабіринт, ліміт часу, швидкість від рахунку, 6 режимів, +1 життя за 20 000.
- [Wikipedia: Pac-Man Championship Edition DX](https://en.wikipedia.org/wiki/Pac-Man_Championship_Edition_DX) — сплячі привиди, Ghost Train, привиди з пелетами, slow-motion, бомби, 9 курсів, режими, ранги, повтори, DX+.
- [Steam: PAC-MAN Championship Edition DX+](https://store.steampowered.com/app/236450/PACMAN_Championship_Edition_DX/) — 5 режимів, 7 лабіринтів, налаштування складності/музики/персонажів/візуалу, лідерборди.
- [Steam: PAC-MAN Championship Edition 2](https://store.steampowered.com/app/441380/PACMAN_CHAMPIONSHIP_EDITION_2/) — наступник.
- YouTube: пошук «pac-man championship edition dx gameplay».

## Непевне
- (?) Точний порядок «яка половина оновлюється» — Wikipedia CE каже «новий лабіринт на іншій половині» відносно фрукта, тобто на очищеній; візерунки, ймовірно, наперед задані послідовністю курсу (тому `random: none`).
- (?) Потяг: щоб зʼїсти потяг, треба почати з ведучого, інакше Пекмен відскакує; бомба знижує швидкість «до 10 рівнів» — з пошукових сніпетів (TV Tropes, Pac-Man Wiki), сторінки не відкрились (403/402).
- (?) Чи нараховуються нові бомби за очки і скільки їх на старті; чи бомба автоматична в легкій складності.
- (?) Ціни точок, фруктів, привидів у потязі; поріг рангів швидкості — у джерелах нема.
- (?) Кількість курсів: Wikipedia — 9, Steam DX+ — 7 у базі; різниця, імовірно, через версії/DLC.
- (?) Вигляд HUD (`speed-gauge`) — з памʼяті, не перевірено.
