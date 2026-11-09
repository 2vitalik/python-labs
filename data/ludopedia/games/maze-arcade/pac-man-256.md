---
title: Pac-Man 256
slug: pac-man-256
aka: [PAC-MAN 256, Пекмен 256]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: partial
  random: runtime
  goal: score
year: 2015
platforms: [iOS, Android, PC (Steam), консолі]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pac-Man_256", best: true, note: "нескінченний лабіринт, глітч, 8 типів привидів, power-ups, монети, мультиплеєр"}
  - {kind: steam, url: "https://store.steampowered.com/app/455400/PACMAN_256/", note: "PC: 20+ power-ups, 10 тем, локальний коп до 4"}
  - {kind: other, url: "https://www.imore.com/pac-man-256-score-10000-or-more-these-tips-tricks-and-power-chains", note: "гайд: глітч, фрукти-множники, поведінка привидів, 21 power-up, монети"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=pac-man+256+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-4dir, move-auto, infinite-field, maze-generation, item-pickup, touch-death, environment-death, temporary-modes, chase-player, chase-greedy, pattern-automaton, enemy-patrol, speed-per-type, spawn-schedule, wrap-edges, combo-multiplier, event-points, player-death, projectile-shot, explode-area, inventory-items, inventory-duration, score-records, leaderboard, theme-select, swipe-gestures, keyboard-controls, achievements-window, end-screen, game-settings, +rising-hazard-front, +dot-streak-clear, +loadout-powerups, +meta-upgrades, +fruit-score-multiplier, +sleeping-enemy, +lane-rusher, +mission-goals]
proposes: ["+trigger:streak", "+effect:clear_screen", "+role:wall-front", "+window:loadout-select", "+window:missions-window", "+ui:streak-counter", "+ui:powerup-slots", "+feature:revive", "+card:rising-hazard-front", "+card:dot-streak-clear", "+card:loadout-powerups", "+card:meta-upgrades"]
author: opus
date: 2026-11-09
---

# Pac-Man 256 — нескінченний вертикальний лабіринт, знизу наздоганяє «глітч» рівня 256

## Суть
Пекмен біжить угору нескінченним лабіринтом, що генерується на льоту, а знизу підіймається «глітч» — знищене поле на згадку про kill screen 256-го рівня оригіналу. Зупинився чи заблукав — глітч поглинає; зачепив привида — мінус життя. Головне джерело очок — серія точок підряд: 256 поспіль вибухають і чистять екран від привидів. Між забігами гравець обирає до трьох power-up-ів і прокачує їх монетами — роглайт-обгортка над аркадою.

## Поле і час
- Квадратна сітка-лабіринт шириною в екран, нескінченна вгору; камера ізометрична, слідує за Пекменом; бачиш лише частину поля навколо (тому `info: partial`).
- Краї ширини працюють як тунелі: вийшов збоку — зʼявився з протилежного, з короткою невразливістю.
- Real-time: Пекмен рухається безперервно; глітч стартує через ~5 с після початку і повзе вгору; нові ряди лабіринту, точки, power-up-и й привиди генеруються над екраном.
- Частково покрита глітчем клітина прохідна, але трясе екран і сповільнює Пекмена; повне поглинання — смерть.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пекмен | player | 2 життя | безперервний рух 4 напрямки; їсть точки й предмети |
| Глітч | hazard | фронт знизу | підіймається; поглинає Пекмена й привидів; знищені ним привиди не дають очок |
| Точка | pickup | — | +очки, +1 до серії; загальна кількість відкриває power-up-и (консолі/PC) |
| Енерджайзер | pickup | — | frightened для привидів; зʼїдені зʼявляються знову вище по мапі |
| Power-up плитка | pickup | один із 3 обраних | активує свою дію на час (рівень апгрейда → тривалість і очки) |
| Фрукт | pickup | вишня ×2, яблуко ×3, полуниця ×4, апельсин ×5, диня ×6 | множник очок на обмежений час |
| Монета | pickup | — | валюта поза забігом; очок не дає |
| Стіна | static | — | непрохідна |
| Бічний тунель | terrain | 2 краї | `wrap` + коротка невразливість |
| Blinky (червоний) | enemy | зʼявляється з ~3000 очок | активно полює |
| Pinky (рожевий) | enemy | вартує коридор | коли Пекмен входить у її лінію — ривок ~120% швидкості |
| Inky (блакитний) | enemy | — | ходить фіксованим прямокутним маршрутом, не переслідує |
| Clyde (помаранчевий) | enemy | — | фіксований звивистий маршрут (Wikipedia: вниз, зміщуючись у бік Пекмена) |
| Sue (фіолетова) | enemy | групи по 3, ~60% швидкості | ходить горизонтальною смугою |
| Funky (зелений) | enemy | групи по 4, повна швидкість | ходить горизонтальною смугою |
| Spunky (сірий) | enemy | — | спить, доки Пекмен не ближче ~5 точок; тоді женеться ~5 с |
| Glitchy | enemy | — | нешкідливий рій глітчу → стає привидом, женеться як Blinky, може телепортуватись; лишає непрохідні калюжі глітчу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `move(pacman, dir)`; КОЛИ `input(dir)` → ТО `face(pacman, dir)` на найближчому повороті.
- КОЛИ `timer(5 s)` від старту → ТО `custom: «фронт глітчу починає підійматися знизу»`.
- КОЛИ `reach(pacman, upper_edge_of_generated)` → ТО `custom: «згенерувати нові ряди лабіринту з точками, привидами, предметами»`.
- КОЛИ `enter(pacman, glitch)` → ЯКЩО `state(cell, partial_glitch)` → ТО `speed(pacman, -k)`, `shake`; інакше `lives(-1)`.
- КОЛИ `contact(ghost, glitch)` → ТО `disappear_a` (без очок).
- КОЛИ `contact(pacman, dot)` → ТО `pickup`, `score(dot_value)`, `combo(+1)`, `counter(total_dots, +1)`.
- КОЛИ `counter(combo, ==, 256)` → ТО `custom: «вибух: усі привиди на екрані зникають, їхні очки й бонус зараховуються»`, `reset_combo`.
- КОЛИ `contact(pacman, energizer)` → ТО `set_state(ghosts, frightened, T)`.
- КОЛИ `contact(pacman, ghost)` → ЯКЩО `state(ghost, frightened)` → ТО `score(ghost_value)`, `spawn_at(ghost, further_up)`; інакше `lives(-1)`.
- КОЛИ `died(pacman)` → ЯКЩО `counter(lives, >, 0)` → ТО `custom: «привиди очищаються, глітч відкочується»`; інакше `game_over`.
- КОЛИ `contact(pacman, fruit)` → ТО `multiplier(×2…×6)`, `timer(start)`.
- КОЛИ `contact(pacman, coin)` → ТО `currency(+1)` (поза забігом).
- КОЛИ `edge(pacman)` → ТО `wrap(pacman)`, `set_state(pacman, invulnerable, short)`.
- КОЛИ `contact(pacman, powerup_tile)` → ТО `set_state(pacman, power_x, duration(level))`; приклади: Laser — `custom: «промінь знищує привидів по лінії»`; Freeze — `freeze(ghosts, n)`; Bomb/Boom — `explode(area)`; Giant — `custom: «великий Пекмен давить привидів»`; Tornado — `custom: «вихор рухається випадково й ловить привидів»`; Pac-Men — `spawn(mini_pacmen)`; Magnet / Regen — `custom: «точки притягуються / збираються в радіусі й відновлюються»`.
- Привиди: Blinky — `chase-greedy`; Pinky — КОЛИ `line_of_sight(pinky, pacman)` → ТО `speed(pinky, ×1.2)`, `move(pinky, toward)`; Inky / Clyde — `custom: «фіксований маршрут-патерн»`; Sue, Funky — `custom: «туди-сюди по горизонтальній смузі групою»`; Spunky — КОЛИ `in_range(spunky, pacman, 5)` → ТО `clear_state(spunky, sleeping)`, `timer(5 s)` погоні; Glitchy — `teleport` під час погоні.
- КОЛИ `counter(mission_progress, ==, goal)` → ТО `currency(+16…+256)`.
- КОЛИ `counter(currency, >=, cost)` → ЯКЩО `input(upgrade)` → ТО `custom: «апгрейд power-up-а; завершується через реальний час»`.
- Перемога: нема (endless) · Поразка: 2 життя, поглинання глітчем або дотик привида · Рахунок: точки, привиди, бонус за серію 256, множники фруктів.

## Керування і ввід
- Мобільні: свайпи в 4 напрямки (поворот на найближчому перехресті); PC/консолі — стрілки/стік.
- Power-up-и активуються підбором плитки в лабіринті, окремих кнопок нема (?).
- Локальний мультиплеєр до 4 гравців на одному екрані (консолі/PC).

## Вікна, меню, HUD
- `main-menu`: Грати · вибір power-up-ів (`+window:loadout-select`, до 3 слотів) · місії (`+window:missions-window`) · теми (`skin-select`) · налаштування.
- `game-screen`: ізометричний лабіринт; HUD — `score`, `hi-score`, `lives`, `+ui:streak-counter` (серія точок до 256), `multiplier` (фрукт), `+ui:powerup-slots`, `popup-text`.
- `end-screen` (Game Over): рахунок, прогрес місій, вхід у `settings-window` (звук, музика) звідси; пропозиція ожити за монети (`+feature:revive`).
- `shop-window` / апгрейди: power-up-и за монети з очікуванням у реальному часі; покупка монет / безлімітних кредитів (мобільні).
- `leaderboard` · `achievements-window` (Steam).
- Переходи: main-menu → loadout → game-screen → end-screen → (ожити) game-screen / main-menu.

## Фічі поза полем
- `meta-progression`: power-up-и відкриваються кількістю зʼїдених точок (консолі/PC) або з часом (мобільні); прокачка монетами збільшує тривалість і очки за вбивство.
- Місії з нагородами 16/32/64/128/256 монет; монети також у лабіринті й за рекламу (v2.0 замінила «кредити»).
- Кредити (до v2.0): кожен забіг з power-up-ами чи відродження коштував кредит, кредити відновлювались за години.
- `theme-select` — 10 тем (на PC/консолях відкриті одразу).
- `mode-coop` / `local-multiplayer` — до 4 гравців, спільний рахунок, підбитого можна оживити power-up-ом; кінець, коли гине останній.
- `leaderboard-online`, `achievements`.

## Варіації й родичі
- Pac-Man (див. `pac-man`) — привиди, енерджайзер, kill screen рівня 256 як сюжетна ідея глітчу.
- Pac-Man Championship Edition (див. `pac-man-championship-edition`) — те саме «не зупиняйся», але замкнений лабіринт і таймер; сплячий привид (Spunky) — спільна ідея.
- Crossy Road (той самий жанр «нескінченно вперед», картка `infinite-field`).
- **Осі варіацій:**
  - поле: закрите / оновлювані половини (CE) / нескінченне вгору (256);
  - тиск: таймер / привиди / фронт-переслідувач знизу;
  - прогресія: нема / лоадаут + прокачка між забігами;
  - типи ворогів: 4 класичні AI / вісім патернів (лінія, смуга, сон, засідка, телепорт).

## Цікавинки для курсу
- Нескінченна генерація лабіринту рядами зі звʼязністю нового ряду з попереднім — 🥇: `infinite-field` + `maze-generation` разом.
- Фронт-переслідувач знизу (глітч) зі «сірою зоною» сповільнення — 📎.
- Серія 256 точок підряд → очищення екрана — 🌱: лічильник + скидання.
- Вісім привидів = вісім простих автоматів (погоня, ривок по лінії, прямокутник, смуга групою, сон-погоня, телепорт) — 🥉 за набір.
- Лоадаут із 3 power-up-ів + прокачка між забігами — 🥈 (сейв метапрогресу, магазин).
- Фрукт-множник з таймером — 🌱.

## Мапа на каталог
- Є: `move-auto` + `move-4dir` · `infinite-field` · `maze-generation` · `item-pickup` · `touch-death` · `environment-death` (глітч) · `temporary-modes` · `chase-player`/`chase-greedy` (Blinky) · `pattern-automaton` (Inky, Clyde) · `enemy-patrol` (Sue, Funky) · `speed-per-type` · `spawn-schedule` · `wrap-edges` · `combo-multiplier` · `event-points` · `player-death` · `projectile-shot` (Laser) · `explode-area` (Bomb) · `inventory-items` + `inventory-duration` (power-up-и) · `score-records` · `leaderboard` · `theme-select` · `swipe-gestures` · `keyboard-controls` · `achievements-window` · `end-screen` · `game-settings`.
- **Нема** → пропозиції карток:
  - `+rising-hazard-front` «Фронт небезпеки наздоганяє» · game-logic/lose · 📎 · слот {speed, grey_zone}.
  - `+dot-streak-clear` «Серія підбирань очищає екран» · game-logic/score · 🌱 · слот {n: 256}.
  - `+loadout-powerups` «Набір з N power-up-ів перед забігом» · game-logic/economy · 🥉 · слот {slots: 3}.
  - `+meta-upgrades` «Прокачка між забігами за валюту» · game-logic/economy · 🥈.
  - `+fruit-score-multiplier` «Предмет-множник очок на час» · game-logic/score · 🌱.
  - `+sleeping-enemy` (запропоновано в `pac-man-championship-edition`) — Spunky.
  - `+lane-rusher` «Ворог робить ривок, коли гравець у його лінії» · entities/move · 📎 — Pinky.
  - `+mission-goals` «Місії з нагородами» · levels/progression · 🥉.

## Пропозиції до словників
- `+trigger:streak` — серія однакових подій без перерви досягла N (256 точок поспіль); `counter` не передає «підряд».
- `+effect:clear_screen` — прибрати всіх ворогів у видимій області (бомба-серія, вибух 256).
- `+role:wall-front` — рухомий фронт-небезпека, що займає ряди поля (глітч; «смерть знизу» в раннерах).
- `+window:loadout-select` — вибір набору здібностей/предметів перед забігом; `+window:missions-window` — список місій з нагородами.
- `+ui:streak-counter` — лічильник серії; `+ui:powerup-slots` — слоти обраних power-up-ів.
- `+feature:revive` — оживити після смерті за валюту/рекламу.
- `+card:rising-hazard-front`, `+card:dot-streak-clear`, `+card:loadout-powerups`, `+card:meta-upgrades`.

## Джерела
- ⭐ [Wikipedia: Pac-Man 256](https://en.wikipedia.org/wiki/Pac-Man_256) — нескінченний лабіринт, глітч, серія 256, до 3 power-up-ів, монети/кредити, 8 привидів, коп до 4.
- [Steam: PAC-MAN 256](https://store.steampowered.com/app/455400/PACMAN_256/) — «maze that never ends», 20+ power-ups (Laser, Tornado, Giant), 10 тем, локальний коп.
- [iMore: гайд Pac-Man 256](https://www.imore.com/pac-man-256-score-10000-or-more-these-tips-tricks-and-power-chains) — глітч через 5 с, 2 життя, множники фруктів, швидкості й тригери привидів, 21 power-up за групами, нагороди місій.
- YouTube: пошук «pac-man 256 gameplay».

## Непевне
- (?) Кількість power-up-ів: 21 (iMore), «20+» (Steam), 15–16 (інші сніпети) — різні версії; повний опис кожного не перевірено.
- (?) Що саме скидає серію точок (пропущена клітина без точки чи пауза в часі).
- (?) Поведінка Clyde: iMore — фіксований звивистий маршрут; Wikipedia — рух униз зі зміщенням до Пекмена.
- (?) Розробник (Hipster Whale разом із Bandai Namco) — з памʼяті, у відкритих сторінках не перевірено; конкретні консолі не уточнено.
- (?) Як саме подається генерація рядів (шаблони-чанки чи справжній генератор) — невідомо.
- (?) Активуються power-up-и підбором чи кнопкою на консолях.
