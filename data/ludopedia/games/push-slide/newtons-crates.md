---
title: Newton's Crates (Andrey Shevchuk)
slug: newtons-crates
aka: [Ящики Ньютона]
family: push-slide
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2016
platforms: [web]
links:
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=9cf57ca82a0181de97e4e225bc9bf4ca", best: true, note: "грати в браузері (PuzzleScript), 16 рівнів + фінальна сцена"}
  - {kind: other, url: "https://api.github.com/gists/9cf57ca82a0181de97e4e225bc9bf4ca", note: "повний код гри: правила передачі імпульсу, умова перемоги, пасхалки, 17 карт"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Newton%27s+Crates+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 85
mechanics: [move-4dir, keyboard-controls, push-object, impassable-cells, all-on-targets, sequential-levels, undo-unlimited, restart-level, level-from-txt, sound-effects, event-effects, +momentum-transfer, +decoy-crates, +secret-messages]
proposes: ["+effect:impulse", "+cond:kind_counts", "+feature:secret-messages", "+card:decoy-crates"]
author: opus
date: 2026-11-09
---

# Newton's Crates — Sokoban як колиска Ньютона: поштовх у ряд ящиків передається, рушає лише крайній

## Суть
PuzzleScript-гра Андрія Шевчука: склад, ящики і цілі, як у Sokoban, але ящики **не їдуть ланцюгом** і не блокують одне одного. Штовхнутий ящик, що впирається в інший, зупиняється й передає йому імпульс — рушає лише останній у ряду, на одну клітину, а гравець і решта ряду лишаються на місці. Тому ряд ящиків стає «передавачем»: можна зрушити далекий ящик, не торкаючись його. Рахуються лише особливі ящики на цілях; звичайні ящики — передавачі й перешкоди.

## Поле і час
- Квадратна сітка-склад, стіни довкола; рівні — ASCII-карти PuzzleScript.
- Покроково: хід = одне натискання; ящики рухаються рівно на 1 клітину, без ковзання.
- Шари: фон (підлога, цілі, яблука, клітини-секрети) + обʼєкти (гравець, ящики, стіни).
- 17 карт: 16 рівнів і фінальна сцена-рівень, після якої на героя падає яблуко.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець (Ньютон) | player | — | рух 4 напрямки; штовхає сусідній ящик; не рухається, якщо ящик попереду не зрушив |
| Ящик-ціль | object | — | має стати на ціль; рухається на 1 від поштовху чи переданого імпульсу |
| Звичайний ящик | object | — | лише передавач і перешкода; на цілі не зараховується |
| Стіна | static | — | у тому ж класі «інерційних», але поглинає імпульс і не рухається |
| Ціль | terrain | — | клітина для ящика-цілі |
| Яблуко | pickup | — | пасхалка: гравець наступив — лишається огризок |
| Секрет-клітина | terrain | текст | пасхалка: гравець наступив — повідомлення, клітина зникає |
| Фінальна ціль | terrain | — | фінальна сцена: коли всі ящики на них — з хмари падає яблуко |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`.
- КОЛИ `contact(player, crate)` → ТО `push` — ящик отримує рух у напрямку гравця.
- КОЛИ `contact(moving_crate, crate)` → ТО `custom: «рушійний ящик зупиняється, рух передається сусідньому ящику»` (ланцюгом до кінця суцільного ряду).
- КОЛИ `contact(moving_crate, wall)` → ТО `block` — стіна поглинає імпульс, жоден ящик ряду не рухається.
- КОЛИ `custom: «останній ящик ряду має вільну клітину»` → ТО `move(last_crate, dir)` на 1; решта ряду й гравець — на місці.
- Одиничний ящик з вільною клітиною за ним — звичайний поштовх Sokoban: ящик і гравець зсуваються разом.
- КОЛИ `enter(goal_crate, target)` → ТО `sound(click)`.
- КОЛИ `all_on(goal_crate, target)` → ТО `animate(win)`, `win`, `next_level`; звичайні ящики на цілях нічого не важать.
- КОЛИ `enter(player, apple)` → ТО `transform(apple, apple_core)`, `sound(crunch)`.
- КОЛИ `enter(player, secret_cell)` → ТО `message(text)`, `disappear_b`.
- Фінальна сцена: КОЛИ `all_on(crate, final_target)` → ТО `spawn_at(apple, cloud_above_player)`, `fall(apple)`.
- Фінальна сцена: КОЛИ `contact(apple, player)` → ТО `transform(player, genius)`, далі `custom: «яблука сиплються з неба без кінця»`.
- КОЛИ `input(undo)` → ТО `undo(1)`.
- КОЛИ `input(restart)` → ТО `restart`.
- Перемога: усі ящики-цілі на цілях одночасно. · Поразка: нема (глухий кут → undo/рестарт). · Рахунок: нема.

## Керування і ввід
- Стрілки / WASD — крок або поштовх; кнопки дії немає (`noaction`).
- Z — undo без ліміту, R — рестарт рівня (звуки обох прописані в коді); Esc — у титульне меню (стандарт PuzzleScript (?)).

## Вікна, меню, HUD
- `splash-screen` / `main-menu` — титул PuzzleScript: назва, автор, «start game» / «continue».
- `game-screen` — лише поле, без HUD.
- `custom-window` — текстові екрани `message`: пасхалки на секрет-клітинах і репліки героя перед останніми рівнями («I quit!», «I'm going back to my calculus!»).
- Переходи: титул → рівень 1 → … → рівень 16 → репліки → фінальна сцена (без кінця).

## Фічі поза полем
- `levels-sequential`; продовження з поточного рівня (`continue`) — штатне збереження PuzzleScript у браузері (?).
- `undo` (∞), `restart-level`.
- `collectibles` — яблука й шість прихованих повідомлень («Wait... how was I supposed to find this one!?»).
- Звуки на рух, клік ящика на цілі, перемогу, undo, рестарт.

## Варіації й родичі
- Осі варіацій «що робить ряд ящиків від поштовху»:
  - **блокує** — лише один ящик (`sokoban`);
  - **їде весь** — `push-chain` (`mazezam`, `rodents-revenge`);
  - **передає імпульс, рушає крайній** — Newton's Crates;
  - **крайній котиться до упору** — `isaac-conservation-of-momentum` (кулі), `spacekoban` (невагомість).
- Ось «що рахується»: усі ящики (`sokoban`) / лише особливі, решта — інструмент (Newton's Crates).
- Родичі: `sokoban`, `spacekoban`, `pengo` (ковзання), `isaac-conservation-of-momentum`.

## Цікавинки для курсу
- Передача імпульсу ланцюгом: скан ряду до останнього ящика, перевірка клітини за ним — 📎.
- Стіна як «інерційний» обʼєкт, що поглинає рух (один клас правил для ящиків і стін) — 🌱.
- Два види ящиків, з яких на перемогу працює лише один — 🌱.
- Розвʼязувач BFS: стан = гравець + ящики, хід міняє лише одну клітину ящика — 🥇 (класичний Sokoban-солвер з іншою функцією ходу).
- Пасхалки на клітинах із повідомленнями — 🌱.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ стрілки; `push-object` ↔ поштовх одиничного ящика; `impassable-cells` ↔ стіни; `all-on-targets` ↔ ящики-цілі на цілях; `sequential-levels` ↔ 16 рівнів; `undo-unlimited` + `restart-level` ↔ Z / R; `level-from-txt` ↔ ASCII-карти; `sound-effects` + `event-effects` ↔ звуки й анімація перемоги.
- **Нема** → пропозиції карток:
  - `+momentum-transfer` (вже пропонована Spacekoban, Isaac) · слоти {mode: stop, chain: true} — тут рушійний зупиняється, а рух іде далі.
  - `+decoy-crates` «Ящики-інструменти, що не рахуються на цілях» · game-logic/win · 🌱.
  - `+secret-messages` «Приховані клітини з текстом» · levels/progression · 🌱.

## Пропозиції до словників
- `+effect:impulse` — передати рух наступній сутності в ряду, самій зупинитись (колиска Ньютона).
- `+cond:kind_counts` — сутність цього виду зараховується в умову перемоги (ящик-ціль vs звичайний).
- `+feature:secret-messages` — приховані повідомлення як колекційні пасхалки.
- `+card:decoy-crates` — див. «Мапа на каталог».

## Джерела
- ⭐ [PuzzleScript: Newton's Crates](https://www.puzzlescript.net/play.html?p=9cf57ca82a0181de97e4e225bc9bf4ca) — гра в браузері.
- [GitHub Gist (API)](https://api.github.com/gists/9cf57ca82a0181de97e4e225bc9bf4ca) — сирці: `[ > Inertial | Inertial ] -> [ Inertial | > Inertial ]`, стіна гасить рух, перемога «усі zCrate на Target», яблука, повідомлення, фінальна сцена; гіст створено 05.05.2016.
- YouTube: пошук «Newton's Crates puzzlescript».

## Непевне
- (?) Чи гра публікувалась ще деінде (сайт автора shevchuk.net, itch, галерея PuzzleScript) — не перевірено.
- (?) Порядок застосування правил PuzzleScript при кількох ящиках у ряду зʼясовано з коду, у грі не перевірено.
