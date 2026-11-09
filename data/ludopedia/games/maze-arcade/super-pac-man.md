---
title: Super Pac-Man
slug: super-pac-man
aka: [Супер Пекмен, Mr. Packn, Power Pac]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: collect
year: 1982
platforms: [arcade, Commodore 64, MS-DOS, Namco Museum, Arcade Archives]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Super_Pac-Man", best: true, note: "ключі й двері, суперпілюлі, Super Speed, зірка-бонус, бонус-стадії"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=super+pac-man+arcade+gameplay", note: "пошук; геймплей аркади"}
stage: v1
coverage: 65
mechanics: [move-auto, key-and-door, collect-all, item-pickup, temporary-modes, touch-death, player-death, chase-greedy, speed-per-type, mode-indicator, event-points, time-bonus, time-out, sequential-levels, progress-acceleration, game-screen, +key-opens-door-on-eat, +super-form, +break-gates-in-super, +hold-to-boost, +slot-symbol-bonus, +timed-bonus-stage, +stacking-power-duration]
proposes: ["+effect:open", "+ui:slot-reels", "+window:bonus-round", "+card:slot-symbol-bonus", "+card:super-form"]
author: opus
date: 2026-11-09
---

# Super Pac-Man — їж ключі, щоб відчинити двері до їжі; суперпілюля робить Пекмена великим і невразливим

## Суть
Сиквел Pac-Man, де точок нема: лабіринт поділено **дверима** на секції з їжею (фрукти, флагмани Galaxian), а відчиняються двері **ключами**, які Пекмен зʼїдає. Крім звичайних енерджайзерів є дві **суперпілюлі**: Супер-Пекмен великий, проходить крізь привидів без шкоди, ламає двері без ключа і може прискорюватися кнопкою Super Speed — але зʼїсти привидів може лише після звичайної пілюлі. Рівень пройдено, коли зʼїдено всю їжу. Цікаво як «Pac-Man + key-and-door + шар станів, що комбінуються».

## Поле і час
- Один лабіринт на всі рівні (Pac-Man-подібна сітка з коридорами), розбитий на «кімнати» з їжею за замкненими дверима; будиночок привидів у центрі, під ним — дві коробки з символами для зірки-бонусу.
- Ключі на ранніх рівнях відчиняють близькі двері, на пізніших — частіше далекі.
- Real-time; режим Супер має тривалість, наприкінці Пекмен блимає білим.
- Бонус-стадії час від часу: той самий лабіринт, повний їжі, без привидів, з таймером.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пекмен | player | життя | безперервний рух 4 напрямки; їсть ключі, їжу, пілюлі |
| Супер-Пекмен | player (стан) | тривалість | більший; невразливий для привидів; ламає двері; Super Speed |
| Ключ | pickup | привʼязаний до дверей | зʼїдений → відчиняє свої двері |
| Двері | gate | закриті/відчинені | непрохідні, доки не зʼїдено ключ або не проломлено Супером |
| Їжа (фрукти, флагмани) | pickup | вартість росте з рівнем | зібрати всю → наступний рівень |
| Енерджайзер (power pellet) | pickup | — | привиди синіють, їх можна їсти |
| Суперпілюля | pickup | 2 на рівень | вмикає стан Супер |
| Привид ×4 | enemy | — | переслідують; у Супер-стані — «плоскі й тонкі», не шкодять |
| Будиночок привидів | spawner | — | Пекмен може зайти туди будь-коли без ключа |
| Зірка | pickup | на обмежений час | зʼявляється між коробками; зʼїдена — зупиняє барабани символів |
| Коробки символів | static | 2 барабани | один барабан стає, другий крутиться; збіг → великий бонус |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `contact(pacman, key)` → ТО `pickup`, `score(n)`, `custom: «відчинити двері, привʼязані до ключа»` (`+effect:open`).
- КОЛИ `contact(pacman, door)` → ЯКЩО `state(pacman, super)` → ТО `disappear_b`; ЯКЩО `state(door, open)` → прохід; інакше `block`.
- КОЛИ `contact(pacman, food)` → ТО `pickup`, `score(value(level))`.
- КОЛИ `all_gone(food)` → ТО `next_level` (їжа дорожча).
- КОЛИ `contact(pacman, power_pellet)` → ТО `pickup`, `set_state(ghosts, frightened, t)`.
- КОЛИ `contact(pacman, super_pellet)` → ТО `pickup`, `set_state(pacman, super, t)`, `transform(pacman → big)`.
- КОЛИ `contact(pacman, power_pellet|super_pellet)` → ЯКЩО `state(pacman, super)` → ТО `custom: «тривалість подовжується»`.
- КОЛИ `contact(pacman, ghost)` → ЯКЩО `state(ghost, frightened)` → ТО `score(200·2^k)`, `transform(eyes)`; ЯКЩО `state(pacman, super)` → ТО `custom: «проходить крізь привида без шкоди»`; інакше `lose`.
- КОЛИ `input(speed_button)` → ЯКЩО `state(pacman, super)` → ТО `speed(pacman, ↑)` доки кнопка натиснута.
- КОЛИ `state_off(pacman, super)` → ТО `transform(pacman → normal)`; перед цим — `flash` (блимає білим).
- КОЛИ `spawned(star)` → ТО `custom: «символи в коробках крутяться; один зупиняється, другий крутиться»`.
- КОЛИ `contact(pacman, star)` → ЯКЩО `same(box1, box2, symbol)` → ТО `score(2000)`; ЯКЩО `same(box1, box2, symbol) and same(symbol, level_symbol)` → ТО `score(5000)`; інакше `score(200…1600 за рівнем)`.
- КОЛИ `timer(star)` або `died(pacman)` → ТО `custom: «зірка зникає, бонус втрачено»`.
- Бонус-стадія: КОЛИ `level_start` → ЯКЩО `level(bonus)` → ТО `set_state(pacman, super, ∞)`, `timer(start)`, без привидів; КОЛИ `all_gone(food)` → ЯКЩО `timer(>, 0)` → ТО `score(bonus)`; КОЛИ `counter(time_left, ==, 0)` → ТО `next_level` без бонусу.
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over`.
- Перемога: рекорд (рівні нескінченні). Поразка: втрачено всі життя. Рахунок: їжа (росте з рівнем), ключі, привиди 200–1600, зірка 2000/5000 або вартість привида, бонус-стадія за час.

## Керування і ввід
- 4-позиційний джойстик (як у Pac-Man: напрям наперед, Пекмен біжить сам).
- Кнопка **Super Speed** — прискорення лише в Супер-стані.
- 1P / 2P Start; двоє по черзі (?).

## Вікна, меню, HUD
- `game-screen` — лабіринт; `score` 1UP/2UP, `hi-score`, `lives`, ряд символів пройдених рівнів (?); `+ui:slot-reels` — дві коробки-барабани під будиночком.
- `+window:bonus-round` — бонус-стадія з `timer-countdown`.
- `attract-demo` і GAME OVER → атракт (як у Pac-Man) (?).

## Фічі поза полем
- `levels-sequential` з подорожчанням їжі; бонус-стадії через інтервали.
- `operator-settings` DIP (життя, поріг extra life) — (?).
- Збережень нема; один hi-score.

## Варіації й родичі
- **Pac-Man** — базова гра (див. `pac-man.md`); **Pac & Pal** (1983) — наступник з картками-предметами замість ключів (?).
- Порти: PV-2000 і Sord M5 (Японія, «Mr. Packn», «Power Pac»), C64 (1988), MS-DOS (1989); Супер-Пекмен — Final Smash Пекмена в Super Smash Bros.
- Родичі в корпусі: Chip's Challenge (ключі й двері), Lady Bug (турнікети ділять лабіринт, бонус-літери), Libble Rabble (бонусна логіка).
- **Осі варіацій:** доступ до секцій (відкритий / двері + ключ / турнікети); посилення (одне — енерджайзер / два ортогональні — пілюля і суперпілюля, комбінуються); бонус (фрукт / слот-машина / літери).

## Цікавинки для курсу
- Ключ, що відчиняє **привʼязані** двері (часто далекі), — 📎 (мапа ключ→двері як дані).
- Два ортогональні стани гравця (Супер = невразливість + ламання дверей; енерджайзер = можна їсти), що комбінуються, — 🥉 (машина станів з перетином).
- Кнопка прискорення, активна лише в стані — 🌱.
- Слот-машина «один барабан стоїть, другий крутиться» з бонусом за збіг — 📎.
- Бонус-стадія на час без ворогів у тому самому лабіринті — 🌱.
- Подовження тривалості стану повторним підбором — 🌱.

## Мапа на каталог
- Є: `move-auto` · `key-and-door` · `collect-all` (їжа) · `item-pickup` · `temporary-modes` (енерджайзер, Супер) · `touch-death` · `player-death` · `chase-greedy` · `speed-per-type` · `mode-indicator` (плоскі привиди, блимання) · `event-points` · `time-bonus` (бонус-стадія) · `time-out` (кінець бонус-стадії) · `sequential-levels` · `progress-acceleration` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+key-opens-door-on-eat` «Ключ відчиняє свої двері одразу» · entities/interact · 📎 · слот {door_map} — дитина `key-and-door` без інвентаря.
  - `+super-form` «Великий невразливий стан» · entities/state · 🥉.
  - `+break-gates-in-super` «Ламати двері в посиленні» · entities/interact · 🌱.
  - `+hold-to-boost` «Утримуй кнопку — швидше» · entities/move · 🌱.
  - `+slot-symbol-bonus` «Бонус-слот: збіг символів» · game-logic/score · 📎.
  - `+timed-bonus-stage` «Бонус-стадія на час без ворогів» · levels/progression · 🌱.
  - `+stacking-power-duration` «Повторний підбір подовжує стан» · entities/state · 🌱.

## Пропозиції до словників
- `+effect:open` — відчинити привʼязаний `gate` дистанційно (ключ → двері; кнопка → ворота) без `take`.
- `+ui:slot-reels` — HUD-барабани символів.
- `+window:bonus-round` — окрема стадія-бонус з таймером (уже пропонувалось для Amidar; тут ще один випадок).
- `+card:slot-symbol-bonus`, `+card:super-form` — див. вище.

## Джерела
- ⭐ [Wikipedia: Super Pac-Man](https://en.wikipedia.org/wiki/Super_Pac-Man) — ключі й двері, вхід у будиночок без ключа, суперпілюлі (2), Super Speed, привиди «плоскі», їсти лише після енерджайзера, подовження стану, зірка 2000/5000/200–1600, бонус-стадії, порти.
- YouTube: пошук «super pac-man arcade gameplay».

## Непевне
- (?) Кількість енерджайзерів і ключів на рівні, очки за ключ і їжу.
- (?) На яких рівнях бонус-стадії і скільки очок за встигання.
- (?) Режим на двох, DIP-налаштування, вигляд HUD.
- (?) Pac & Pal як прямий наступник з предметами-картками.
