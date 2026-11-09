---
title: Teki Paki (洗脳ゲーム TEKI・PAKI)
slug: teki-paki
aka: [洗脳ゲーム TEKI・PAKI, 洗脳ゲーム テキ・パキ, Sennou Game Teki Paki, Brainwashing Game Teki Paki]
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
year: 1991
platforms: [arcade, PS4, Switch, Evercade, iOS, Android]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/洗脳ゲーム_TEKI・PAKI", best: true, note: "правила: поле 8×10, 6+2 кольори, трійки, 5+ у будь-якій формі з діагоналями, смайлик, бомба, рівні, очки"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Teki_Paki", note: "трійки випадкових кольорів, одна плитка «відчіпляється» після приземлення, рівень до 999, бонус 100 000, Toaplan/Tecmo"}
  - {kind: other, url: "https://www.4gamer.net/games/584/G058460/20211006034/", note: "4Gamer (2021): M2-версія — підказка, 3 дизайни блоків, палітра для дальтоніків, онлайн-рейтинг"}
  - {kind: other, url: "https://www.arcade-museum.com/game_detail.php?game_id=10058", note: "KLOV: 2 гравці одночасно, Toaplan 1991"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Teki+Paki+arcade+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [gravity-fall, keyboard-controls, connectivity-check, chain-reaction, progress-acceleration, event-points, score-records, leaderboard, game-over-continue, theme-select, +connected-group-pop, +cascade-gravity, +wildcard-tile, +board-wipe-special, +split-on-landing, +hint-move, +colorblind-palette, +simultaneous-clear-bonus]
proposes: ["+cond:group_size", "+effect:clear_all", "+card:board-wipe-special", "+card:simultaneous-clear-bonus"]
author: opus
date: 2026-11-09
---

# Teki Paki — трійки кольорових квадратів; 5+ одного кольору будь-якою формою, разом із діагоналями, зникають

## Суть
Аркадна «падалка» Toaplan: зверху падають групи з трьох квадратних блоків випадкових кольорів. Блоки зникають, коли **5 або більше одного кольору стикуються в будь-якій формі** — по вертикалі, горизонталі й діагоналі. Два спецблоки змінюють гру: **смайлик** зʼєднується з будь-яким кольором, а **бомба** (п'ять бомб разом) змітає все поле й дає 100 000 очок. Кінцівки нема — рівні до 999, мета суто рекорд.

## Поле і час
- Поле 8 стовпців × 10 рядів (JA-вікі); заповнилось — кінець гри.
- Real-time падіння; швидкість росте з кожним рівнем.
- Кольори: 6 базових + срібний (з рівня 70) + золотий (з рівня 100); далі до 999 — 8 кольорів.
- Після зникнення блоки вище падають у порожнечу — можливі ланцюги; окремого бонусу за ланцюг нема, але одночасні великі зачистки без ланцюга не скласти.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Падаюча трійка | player | 3 квадрати випадкових кольорів | падає; після приземлення на стек один блок «відчіпляється» й ним можна дограти в щілину (EN-вікі) |
| Кольоровий блок | tile | колір (6 + срібний + золотий) | падає до опори; 5+ однакових, що торкаються (8-сусідство), → зникають |
| Смайлик (スマイリー) | tile | wildcard | зʼєднується з блоками всіх кольорів |
| Бомба (バクダン) | tile | — | 5+ бомб разом → знищує всі блоки на екрані, +100 000 |
| Поле 8×10 | static | — | заповнене → кінець гри |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `free(cells_below)` → ТО `move(trio, down)`.
- КОЛИ `input(dir)` → ЯКЩО `free(target_cells)` → ТО `move(trio, dir)` (?) — керування в джерелах не описано.
- КОЛИ `locked(trio)` → ЯКЩО `custom: «приземлилась на блоки поля»` → ТО `custom: «один блок трійки відчіпляється — гравець ще веде його в щілину»` (EN-вікі) (?).
- КОЛИ `pattern(group(5))` → ЯКЩО `same(blocks, color)` and `custom: «звʼязність з діагоналями (8-сусідство), форма будь-яка»` → ТО `clear(group)`, `score(+n)` (?).
- КОЛИ `pattern(group(5))` → ЯКЩО `occupied(group, smiley)` → ТО `custom: «смайлик рахується блоком будь-якого кольору»`.
- КОЛИ `pattern(group(5))` → ЯКЩО `same(blocks, bomb)` → ТО `custom: «clear_all — знищити всі блоки на екрані»`, `score(+100000)`, `counter(level, +1)`.
- КОЛИ `after(clear)` → ТО `fall(all_unsupported)`; ЯКЩО новий `pattern(group(5))` → ТО `clear` (ланцюг без окремого бонусу).
- КОЛИ `counter(cleared_at_once, ≥, 10)` → ТО `score(+5000)`; одночасні зачистки одного й різних кольорів зараховуються по-різному (?).
- Смайлик і бомба поєднуються: 10-зачистка й вибух поля одним ходом — «безперервний бонус» (JA-вікі).
- КОЛИ `counter(drops_plus_clears, ≥, 5)` → ТО `counter(level, +1)`, `speed(trio, +n)`; рівень 70 → `custom: «додати срібний колір»`, рівень 100 → `custom: «додати золотий»`; ліміт рівня 999.
- КОЛИ `custom: «поле 8×10 заповнене, трійка не входить»` → ТО `game_over`; аркада — `game-over-continue` за монету.
- Перемога: нема, гра на рекорд. · Рахунок: зачистки, +5000 за 10 разом, +100 000 за вибух бомб, приховані бонуси (EN-вікі: «crucial for high scores»).

## Керування і ввід
- Аркадний джойстик + кнопки (кількість — (?)): зсув трійки, прискорене падіння, можливо — поворот або перестановка кольорів (?).
- Після приземлення — короткий контроль над одним блоком, що відчепився (?).
- 2 гравці одночасно (KLOV: «joint play», JA: 2人同時プレイ可) — окремі поля чи спільне — (?).

## Вікна, меню, HUD
- `attract-demo` / `splash-screen` — титул «洗脳ゲーム».
- `game-screen`: поле 8×10, `score`, `hi-score`, `level-number` (?), `next-piece-preview` (?).
- `game-over-continue` — продовження за кредит.
- `leaderboard` — аркадна таблиця рекордів (?); M2-версія (2021) — онлайн-рейтинг.
- M2-версія: «M2-гаджети» — додаткова інформація по боках екрана; меню налаштувань (`settings-window`): дизайн блоків (3 варіанти, `skin-select`), кольори для дальтоніків, увімкнути підказку.
- Переходи: splash → game-screen → (поле заповнене) game-over-continue → leaderboard.

## Фічі поза полем
- `theme-select` — 3 дизайни блоків (M2); `colorblind-palette` (M2).
- `hint` — підказка на полі, куди поставити блок, щоб він зник (M2).
- `leaderboard-online` (M2, 2021); `continue` за кредити (аркада).
- Гра без кінцівки й капу (до рівня 999).

## Варіації й родичі
- Toaplan (1991), видавець Tecmo; композитор Tomoaki Takanohashi; порт на Mega Drive анонсовано 1992 і скасовано; 2021 — бонус до «究極タイガーヘリ» (M2, PS4/Switch); Evercade «Toaplan Arcade 1»; 2024 — мобільна збірка Amusement Arcade TOAPLAN.
- Родичі в корпусі: [Puyo Puyo](puyo-puyo.md) (група за розміром, але 4 і без діагоналей), [Columns](columns.md) (трійки, діагональні лінії), [Tetris](tetris.md), [Puzzle Bobble](puzzle-bobble.md) і [Tidalis](tidalis.md) (джокер-плитка).
- **Осі варіацій**:
  - **сусідство групи**: 4 (Puyo) / 8 з діагоналями (Teki Paki);
  - **поріг**: 3 / 4 / 5 (Teki Paki);
  - **спецблок «очистити все»**: за умовою зʼєднати N бомб (Teki Paki) / одноразовий (Columns Magic Jewel — колір);
  - **ланцюг**: з множником (Puyo) / без бонусу, але потрібен для великих одночасних зачисток (Teki Paki).

## Цікавинки для курсу
- Група 5+ у 8-сусідстві будь-якої форми (flood fill з діагоналями) — 🌱.
- Смайлик-джокер у flood fill: належить кільком групам різних кольорів одночасно — 📎.
- Бомби: група з 5 бомб → зачистка всього поля + бонус + рівень — 🌱.
- Блок, що «відчіпляється» від трійки після приземлення й ще керується — 📎.
- Рівень за лічильником «падіння + зачистки», нові кольори на 70/100 — 🌱.
- Підказка M2: перебрати позиції трійки й знайти ту, що дає зникнення — 🥉.

## Мапа на каталог
- Є: `gravity-fall` ↔ падіння; `keyboard-controls` ↔ джойстик; `connectivity-check` ↔ пошук групи; `chain-reaction` ↔ каскад; `progress-acceleration` ↔ темп за рівнем; `event-points` ↔ +5000/+100 000; `score-records` + `leaderboard` ↔ рекорди; `game-over-continue`; `theme-select` ↔ дизайн блоків M2.
- **Нема** → пропозиції карток:
  - `+connected-group-pop` {min: 5, adjacency: 8}; `+cascade-gravity`; `+wildcard-tile` ↔ смайлик; `+split-on-landing` ↔ блок, що відчіпляється; `+hint-move` ↔ підказка M2; `+colorblind-palette` — уже в корпусі.
  - `+board-wipe-special` «Спецплитки, зібрані групою, зачищають усе поле» · entities/interact · 🌱 · слот {need: 5}.
  - `+simultaneous-clear-bonus` «Бонус за N+ плиток, знищених одночасно» · game-logic/score · 🌱 · слот {n: 10, bonus: 5000}.

## Пропозиції до словників
- `+cond:group_size` — розмір звʼязної групи ≥ N (Teki Paki 5; також SameGame, Just Get 10 — пропонувалось там).
- `+effect:clear_all` — зачистити все поле (бомби Teki Paki).
- `+card:board-wipe-special`, `+card:simultaneous-clear-bonus` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia JA: 洗脳ゲーム TEKI・PAKI](https://ja.wikipedia.org/wiki/洗脳ゲーム_TEKI・PAKI) — поле 8×10, 6+2 кольори по 3, 5+ будь-якою формою з діагоналями, ланцюги без бонусу, смайлик, бомба, рівень за «падіння+зачистки» = 5, кольори на 70/100, +5000, +100 000, версії.
- [Wikipedia EN: Teki Paki](https://en.wikipedia.org/wiki/Teki_Paki) — трійки, блок, що відчіпляється після приземлення, рівні до 999, бомба й смайлик, видавці, скасований порт Mega Drive.
- [4Gamer (2021)](https://www.4gamer.net/games/584/G058460/20211006034/) — M2-версія: гаджети, підказка, 3 дизайни блоків, кольори для дальтоніків, онлайн-рейтинг.
- [KLOV](https://www.arcade-museum.com/game_detail.php?game_id=10058) — 2 гравці одночасно, Toaplan 1991.
- YouTube: пошук «Teki Paki arcade gameplay».

## Непевне
- (?) Керування (кнопки, чи є поворот/перестановка кольорів у трійці, форма трійки — лінія чи кут) — жодне відкрите джерело не описує.
- (?) Механіка «один блок відчіпляється після приземлення» — лише EN-вікі, без деталей.
- (?) Умова рівня: JA — «сума падінь і зачисток = 5»; EN — «зʼєднати 5 блоків». Беру JA.
- (?) Бомба: JA — 5+ бомб разом стирають поле; EN — бомба стирає все, а 5 бомб дають бонус. Різниця формулювань.
- (?) Як виглядає гра на двох (окремі поля / почергово) і чи є атаки супернику — не знайдено.
- (?) Приховані бонуси й тема «промивання мізків» (картинки між рівнями?) — не описані.
