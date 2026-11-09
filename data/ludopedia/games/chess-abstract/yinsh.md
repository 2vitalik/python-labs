---
title: YINSH
slug: yinsh
aka: [Йінш, Yinsh]
family: chess-abstract
also: []
klass: figure
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 2003
platforms: [board, web, iOS]
links:
  - {kind: other, url: "https://www.gipf.com/yinsh/rules/rules.html", best: true, note: "офіційні правила: кільця, маркери, перестрибування з перевертанням, ряди з 5, blitz"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/YINSH", note: "85 точок, 5+5 кілець, 51 маркер, кілька рядів, кінець маркерів, цифрові версії"}
  - {kind: play, url: "https://www.boardspace.net/english/about_yinsh.html", note: "BoardSpace — онлайн"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=YINSH", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=YINSH+board+game+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 75
mechanics: [piece-move-patterns, line-match-clear, legal-move-highlight, selection-highlight, last-move-highlight, hot-seat, turn-enforcement, move-timer, ai-opponent, ai-minimax, cell-click, hover-highlight, drag-drop-piece, pass-turn, online-multiplayer, move-notation, replay, mode-select, game-screen, main-menu, end-screen, help-window, settings-window, state-as-data, unit-tests, +hex-grid-render, +placement-phase, +flip-on-jump, +trail-marker, +line-win, +self-handicap-on-score, +shared-pool, +reserve-empty-end]
proposes: ["+effect:leave_marker", "+effect:flip_jumped", "+effect:return_to_reserve", "+cond:jump_landing", "+trigger:pool_empty", "+ui:rings-removed-slots", "+ui:row-choice-highlight", "+window:row-choice", "+card:flip-on-jump", "+card:trail-marker", "+card:self-handicap-on-score"]
author: opus
date: 2026-11-09
---

# YINSH — кільце лишає маркер свого кольору й перевертає все, що перестрибнуло; хто тричі склав ряд з 5, виграв

## Суть
Кожен має 5 кілець. Хід: поклади в своє кільце маркер свого кольору і пересунь кільце прямою — маркер лишається на місці, а всі маркери, які кільце перестрибнуло, перевертаються на інший колір. Пʼять маркерів свого кольору в ряд — знімаєш їх і **одне своє кільце**; перший, хто зняв 3 кільця, виграв. Лідер слабшає з кожним успіхом: кілець для ходу менше. Пʼята гра GIPF Project (Kris Burm).

## Поле і час
- Поле — зрізана шестикутна зірка на трикутній сітці, 85 точок перетину, включно з краєм (`field: hex`, 6 напрямків; на краю — менше).
- Збоку в кожного 3 гнізда для знятих кілець — видимий лічильник прогресу.
- Дві фази: розстановка 10 кілець, потім рух. Покроково; ~30 хв. Маркери — спільний пул з 51 двобічного (білий/чорний); пул вичерпаний = кінець гри.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кільце | piece | white ×5 / black ×5 | ставиться у фазі 1; ходить прямою, лишаючи маркер; через кільця не стрибає |
| Маркер | tile | двобічний, колір угорі | кладеться в кільце; не рухається ніколи, лише перевертається при перестрибуванні |
| Пул маркерів | supply | 51, спільний | звідси маркер на кожен хід; зняті ряди повертаються сюди |
| Точка поля | terrain | 85 | порожня / кільце / маркер (кільце з маркером — під час ходу) |
| Гнізда знятих кілець | zone | 3 на гравця | заповнити всі 3 = перемога |
| Ряд | zone | 5 маркерів підряд одного кольору | знімається власником кольору разом з одним його кільцем |

## Правила (КОЛИ → ЯКЩО → ТО)
- Фаза 1: КОЛИ `input(place, cell)` → ЯКЩО `free(cell)` → ТО `place(ring, cell)`; починають білі, по черзі, доки всі 10 кілець не на полі.
- КОЛИ `input(select, ring)` → ЯКЩО `turn_of(side)` і `same(ring, side, color)` → ТО `custom: «покласти маркер свого кольору в це кільце»` (`+effect:leave_marker`).
- КОЛИ `input(move, ring, dir)` → ЯКЩО `custom: «прямою: спершу будь-скільки порожніх, далі суцільний відрізок маркерів, зупинка на першій порожній за ним»` (`+cond:jump_landing`) → ТО `move(ring, to)`; після стрибка далі по порожніх не можна.
- КОЛИ `input(move, ring, dir)` → ЯКЩО `occupied(path, ring)` → ТО `block` (через кільця не стрибають).
- КОЛИ `input(move, ring, dir)` → ЯКЩО `occupied(to, marker)` → ТО `block` (на маркері не зупиняються).
- КОЛИ `after(move)` → ТО `custom: «перевернути кожен перестрибнутий маркер»` (`+effect:flip_jumped`, як `set_side` для кожного); маркер у стартовій точці не перевертається.
- КОЛИ `pattern(line(5))` маркерів кольору X → ТО власник X знімає ці 5 маркерів у пул (`+effect:return_to_reserve`) і `choose(ring)` → `disappear(ring)` у гніздо.
- КОЛИ `pattern(line(n))` при n > 5 → ТО `choose(5 підряд)`.
- КОЛИ `pattern(line(5))` ×2 → ЯКЩО `custom: «ряди мають спільний маркер»` → ТО `choose(row)` — знімається один; без спільних — обидва, з двома кільцями.
- КОЛИ `pattern(line(5))` в обох → ТО першим знімає той, хто ходив; потім суперник — до свого ходу. Ряд, складений вашим ходом для суперника, знімає він.
- КОЛИ `counter(rings_removed, ==, 3)` → ТО `win`; якщо одним ходом третій ряд склався в обох — `win` того, хто ходив.
- КОЛИ `custom: «пул маркерів порожній»` (`+trigger:pool_empty`) → ТО `custom: «більше знятих кілець виграє»`, рівно — `draw`.
- КОЛИ `no_moves(side)` → ТО `pass_turn` (неофіційне розʼяснення автора: усі кільця заблоковані — пас).
- Blitz: КОЛИ `counter(rings_removed, ==, 1)` → ТО `win`.
- Перемога: 3 зняті кільця (blitz — 1) · Поразка: суперник першим зняв 3 · Рахунок: лише якщо скінчились маркери.

## Керування і ввід
- Настільна: поклав маркер у кільце, переніс кільце, перевернув маркери, через які пройшло кільце (рукою, по одному).
- (цифрова версія) Клік по своєму кільцю → підсвітка всіх легальних точок у 6 напрямках → клік по цілі; перевертання анімоване. Потім, якщо склався ряд, — клік по 5 маркерах (якщо ряд довший) і по кільцю, яке знімаєш.

## Вікна, меню, HUD
- `main-menu` (цифрова версія): Грати → `mode-select` (звичайна / blitz) → `match-setup` (людина / робот, колір, годинник).
- `game-screen`: зіркове поле, `turn-indicator` з фазою, `rings-removed-slots` (3 гнізда кожного), `remaining-counter` (маркерів у пулі), `legal-move-highlight`, `row-choice-highlight`, `last-move-highlight`, `move-list`, `player-clock`.
- `row-choice` — вибір 5 маркерів і кільця до зняття.
- `end-screen`: 3 кільця / blitz / маркери скінчились.
- `help-window`: діаграми стрибка й перевертання.
- Переходи: main-menu → mode-select → game-screen ⇄ row-choice → end-screen.

## Фічі поза полем
- `online-multiplayer`: BoardSpace, biskai.de, pureabstracts (неофіційні); Board Game Arena — з 2025, публічна бета.
- iOS: Shyring (грудень 2014) — неофіційна адаптація (?).
- `ai-opponent-levels` — роботи на BoardSpace (?).

## Варіації й родичі
- Blitz — один ряд виграє.
- У GIPF — YINSH-potential: рух прямою через порожні точки.
- Серія: [gipf](gipf.md) (ряди з 4 + рециклінг у запас — найближчий родич), [dvonn](dvonn.md), [zertz](zertz.md) (теж «бий себе, щоб виграти»: жертви), PÜNCT, TZAAR, LYNGK.
- Перевертання: [reversi](reversi.md) (флангування замість перестрибування); ряди: [line-games](line-games.md) (гомоку — 5 у ряд); стрибок через ряд фішок: [checkers](checkers.md) (там — взяття).
- Осі варіацій: **що перевертається** (перестрибнуте / затиснуте) · **ціна успіху** (знімаєш власний ресурс / ні) · **довжина ряду** (5 / 4) · **рядів до перемоги** (3 / 1).

## Цікавинки для курсу
- Генерація ходу кільця: порожні → суцільний відрізок маркерів → перша порожня, заборона через кільця — 📎.
- Перевертання перестрибнутих + «слід» маркера у стартовій точці — 🌱.
- Пошук рядів з 5 у 3 напрямках, довший ряд і перетини з вибором — 🥉.
- Самогандикап: успіх забирає твоє кільце — менше ходів у лідера (вбудований catch-up) — 🌱.
- Вікно вибору ряду й кільця після ходу (зокрема для суперника, до його ходу) — 📎.
- AI: оцінка рядів «майже 5» і загроз перевертання; ходів багато (5 кілець × довгі промені) — 🥇.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ рух кільця · `line-match-clear` ↔ ряд з 5 знімається · `pass-turn` · `legal-move-highlight`, `selection-highlight`, `last-move-highlight` · `hot-seat`, `turn-enforcement`, `move-timer`, `online-multiplayer` · `ai-opponent`, `ai-minimax` · `cell-click`, `hover-highlight`, `drag-drop-piece` · `move-notation`, `replay`, `state-as-data`, `unit-tests` · `mode-select`, `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window`.
- **Нема** → пропозиції карток:
  - `+hex-grid-render` (див. hex.md), `+placement-phase` (див. dvonn.md), `+line-win` (див. line-games.md).
  - `+flip-on-jump` «Перевертання перестрибнутих» · entities/interact · 📎 — дитина `+flank-flip` (reversi.md).
  - `+trail-marker` «Фігура лишає слід-маркер» · entities/move · 🌱.
  - `+self-handicap-on-score` «Успіх забирає власний ресурс» · game-logic/score · 🌱.
  - `+shared-pool` «Спільний пул фішок для обох» (див. zertz.md) · 🌱.
  - `+reserve-empty-end` «Скінчився пул — підсумок» · game-logic/win · 🌱.

## Пропозиції до словників
- `+effect:leave_marker` — сутність, рушаючи, лишає маркер у стартовій клітині.
- `+effect:flip_jumped` — перевернути (змінити колір) усі перестрибнуті сутності.
- `+effect:return_to_reserve` — повернути з поля в запас/пул (див. gipf.md).
- `+cond:jump_landing` — ціль — перша порожня клітина за суцільним відрізком.
- `+trigger:pool_empty` — спільний пул вичерпано (YINSH, ZÈRTZ).
- `+ui:rings-removed-slots` — гнізда-прогрес до перемоги.
- `+ui:row-choice-highlight`, `+window:row-choice` — вибір ряду (див. gipf.md).
- `+card:flip-on-jump`, `+card:trail-marker`, `+card:self-handicap-on-score` — див. «Мапа на каталог».

## Джерела
- ⭐ [gipf.com: правила YINSH](https://www.gipf.com/yinsh/rules/rules.html) — розстановка, хід (маркер у кільце, рух, стрибок, перевертання), ряди (довші, перетини, ряд для суперника), перемога, кінець маркерів, blitz.
- [Wikipedia: YINSH](https://en.wikipedia.org/wiki/YINSH) — 85 точок, 51 маркер, порядок розвʼязання рядів, розʼяснення про заблоковані кільця, неофіційні версії (BoardSpace, biskai.de, pureabstracts, Shyring iOS, BGA 2025).
- [BoardSpace: YINSH](https://www.boardspace.net/english/about_yinsh.html) — онлайн (лінк зі списку ігор BoardSpace; сторінку не відкривав).

## Непевне
- (?) Нагороди: Wikipedia — лише категорія «Mensa Select winners», рік не вказано.
- (?) Офіційне правило G.5 у переказі звучить неоднозначно: «два ряди, що перетинаються, — один ряд, одне кільце»; Wikipedia: «спільний маркер — розвʼязати можна лише один». Записав за Wikipedia.
- (?) Shyring для iOS — чи це саме YINSH, чи лише натхнена ним гра.
- (?) Порядок ходу у фазі руху — білі (за аналогією з розстановкою, джерела прямо не кажуть).
