---
title: Depth Charge
slug: depth-charge
aka: [DEPTH CHARGE, USS Computer]
family: hidden-deduction
also: []
klass: cursor
axes:
  field: 3d
  time: turn
  opponent: none
  info: hidden
  random: setup
  goal: state
year: 1978
platforms: [мінікомпʼютер BASIC, BASIC Computer Games (1978), console]
links:
  - {kind: other, url: "https://raw.githubusercontent.com/coding-horror/basic-computer-games/main/31_Depth_Charge/README.md", best: true, note: "опис з BASIC Computer Games: есмінець USS Computer, куб води обраного розміру, кількість зарядів визначає компʼютер, сонар після кожного вибуху; автор Dana Noftle"}
  - {kind: other, url: "https://raw.githubusercontent.com/coding-horror/basic-computer-games/main/31_Depth_Charge/depthcharge.bas", note: "оригінальний лістинг: N = INT(LOG(G)/LOG(2)) + 1, текст сонара NORTH/SOUTH/EAST/WEST + TOO LOW/TOO HIGH/DEPTH OK, повтор гри"}
  - {kind: other, url: "https://www.atariarchives.org/basicgames/showpage.php?page=55", note: "скан сторінки книги (лінк із README, не відкривав)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=depth+charge+basic+computer+games", note: "пошук; геймплей"}
stage: v1
coverage: 80
mechanics: [console-render, spawn-random-cell, move-limit, difficulty-levels, field-size-picker, confirm-dialog, game-screen, end-screen, help-window, +direction-hint, +coordinate-input, +budget-from-size, +belief-set-tracking, +grid-3d-search]
proposes: ["+cond:coord_cmp", "+window:text-prompt", "+card:budget-from-size", "+card:grid-3d-search", "+card:direction-hint", "+card:coordinate-input"]
author: opus
date: 2026-11-09
---

# Depth Charge — куб води G×G×G, ⌊log₂G⌋+1 глибинних бомб і сонар, що каже, з якого боку від субмарини вибухнув заряд

## Суть
Текстова гра з BASIC Computer Games (автор — школяр Dana Noftle, Acton High School). Гравець — капітан есмінця USS Computer: сам обирає розмір куба пошуку G, а компʼютер видає кількість зарядів N = ⌊log₂G⌋ + 1. Кожен заряд задається трьома числами (X, Y — на поверхні, Z — глибина); промах дає звіт сонара: «північніше/південніше», «східніше/західніше» і «занизько/зависоко/глибина ОК». Бюджет рівно дорівнює найгіршому випадку бінарного пошуку, тому гра виграшна лише за бездоганної тактики — три паралельні бінарні пошуки без права на зайвий постріл.

## Поле і час
- Поле — 3D-сітка G×G×G, координати 0…G−1 по кожній осі; G вводить гравець на старті.
- X — схід, Y — північ, Z — глибина (більше = глибше).
- Поля на екрані нема — лише текстовий діалог.
- Покроково: хід = один заряд («TRIAL #D»). Субмарина нерухома; вона «торпедує» есмінець лише після вичерпання зарядів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Субмарина | enemy | точка (A, B, C) | ховається випадково, не рухається |
| Глибинна бомба | projectile | точка (X, Y, Z) | вибухає в заданій точці; влучання лише при точному збігу |
| Звіт сонара | mark | N/S + E/W + LOW/HIGH/OK | де був вибух відносно субмарини, по кожній осі окремо |
| Запас бомб | resource | N = ⌊log₂G⌋ + 1 | 0 без влучання — поразка |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `input(G)` («DIMENSION OF SEARCH AREA»), `counter(shots, =INT(LOG(G)/LOG(2)) + 1)`, `message(«YOU HAVE N SHOTS»)` і правила.
- КОЛИ `level_start` → ТО `spawn_at(sub, (A, B, C))`, кожна координата = INT(G·RND).
- КОЛИ `input(shot, X, Y, Z)` → ЯКЩО `custom: «|X−A| + |Y−B| + |Z−C| = 0»` → ТО `win`, `message(«B O O M ! ! YOU FOUND IT IN D TRIES!»)`.
- КОЛИ `input(shot, X, Y, Z)` → ЯКЩО не влучив → ТО `feedback(guess)`: `message(«SONAR REPORTS SHOT WAS » + …)`.
- Поверхня: ЯКЩО `custom: «Y заряду > Y субмарини»` → «NORTH»; `<` → «SOUTH»; ЯКЩО `custom: «X заряду > X субмарини»` → «EAST»; `<` → «WEST».
- ЯКЩО X ≠ A або Y ≠ B → додається « AND»; якщо обидві збіглися — лише фраза про глибину.
- Глибина: ЯКЩО `custom: «Z заряду > Z субмарини»` → « TOO LOW.»; `<` → « TOO HIGH.»; рівні → « DEPTH OK.».
- Звіт каже, де був **постріл** відносно субмарини (Hurkle навпаки каже, куди **йти**): «NORTH» тут означає «бери південніше».
- КОЛИ `counter(shots_used, ==, N)` → ЯКЩО не влучив → ТО `lose`, `message(«YOU HAVE BEEN TORPEDOED! ABANDON SHIP!»)`, `reveal(sub)` («THE SUBMARINE WAS AT A,B,C»).
- КОЛИ `game_over` → ТО `window(confirm-dialog)` «ANOTHER GAME (Y OR N)»: Y → `restart` з тим самим G і N (нова схованка); інакше «OK. HOPE YOU ENJOYED YOURSELF.» і кінець.
- Вхід не перевіряється: точки поза кубом приймаються як звичайний постріл.
- Перемога: точне влучання · Поразка: N промахів · Рахунок: кількість спроб D.

## Керування і ввід
- Старт: число G (розмір куба).
- Хід: рядок «TRIAL #D ?» → три числа «X,Y,Z» через кому.
- Оптимальна тактика: незалежно по кожній осі брати середину можливого відрізка; три відповіді на вісь дають 2^k − 1 значень за k пострілів, а ⌊log₂G⌋ + 1 = ⌈log₂(G + 1)⌉ — рівно стільки, скільки треба.

## Вікна, меню, HUD
- `settings-window` = запит «DIMENSION OF SEARCH AREA» перед грою (єдине налаштування).
- `help-window` = вступний текст (USS Computer, N зарядів, формат трьох чисел), друкується завжди.
- `game-screen` = `text-prompt`: «TRIAL #D», звіт сонара.
- `end-screen` = «B O O M ! !…» або «YOU HAVE BEEN TORPEDOED!…» з координатами субмарини.
- `confirm-dialog` = «ANOTHER GAME (Y OR N)».
- Цифрова версія: три зрізи/проєкції куба з виключеними зонами (`fog-overlay`), `move-counter` «заряд D з N», `hint-marker` стрілки звіту.

## Фічі поза полем
- `custom-difficulty` — розмір куба обирає гравець; кількість зарядів рахується з нього (більший куб — більше зарядів, але без запасу).
- Повтор партії з тим самим G без повторного запиту розміру.
- Рекордів, рівнів, збережень нема.

## Варіації й родичі
- [Hurkle](hurkle.md) — 2D-предок того ж відгуку («GO NORTHEAST»), фіксовані 10×10 і 5 спроб із запасом.
- [Code Name: Sector](code-name-sector.md) — електронне полювання на субмарину з дальністю й глибиною та рухомою ціллю.
- [Captain Sonar](captain-sonar.md) — субмарини-гравці, курс оголошується вголос.
- [Battleship](battleship.md) — відгук «мимо/влучив» без напрямку, багато цілей.
- **Осі варіацій**: вимірність 1D / 2D / 3D · відгук «де постріл» / «куди йти» / відстань · бюджет фіксований / від розміру (рівно оптимум або з запасом) · ціль нерухома / рухається між пострілами.

## Цікавинки для курсу
- Консольна гра з трьома координатами й складанням фрази сонара — 🌱.
- Бюджет пострілів із розміру поля: довести, що ⌊log₂G⌋ + 1 = ⌈log₂(G + 1)⌉ — найгірший випадок тернарного бінарного пошуку — 📎.
- Автогравець: три незалежні бінарні пошуки; перевірка «виграє завжди» для всіх G до 1000 — 📎.
- Візуалізація куба (зрізи по Z або обертання) з виключеними областями — 🥉.
- Субмарина, що зсувається на 1 по одній осі після кожного промаху: чи вистачить бюджету — 🥉.

## Мапа на каталог
- Є: `console-render` · `spawn-random-cell` ↔ схованка · `move-limit` ↔ N зарядів · `difficulty-levels` + `field-size-picker` ↔ розмір куба · `confirm-dialog` ↔ ANOTHER GAME · `game-screen` / `end-screen` / `help-window`.
- **Нема** → пропозиції карток:
  - `+budget-from-size` «Ліміт ходів, обчислений із розміру поля» · game-logic/difficulty · 🌱 · слот {formula: floor(log2 G) + 1}.
  - `+grid-3d-search` «Пошук схованого в кубі G×G×G за осьовими відгуками» · game-logic/constraints · 📎.
  - `+direction-hint` (Hurkle) — тут зі слотом frame: shot-was.
  - `+coordinate-input` (Hurkle) — три числа замість двох.
  - `+belief-set-tracking` (Scotland Yard) — паралелепіпед можливих точок субмарини.

## Пропозиції до словників
- `+cond:coord_cmp(a, b, axis, op)` — порівняння координат по осі (повтор з Hurkle); у реченнях поки `custom`.
- `+window:text-prompt` — консольний екран «запит → відповідь».
- Вжито наявні без пропозицій: `feedback(guess)`, `message`, `spawn_at`, `restart`, `window(confirm-dialog)`.

## Джерела
- ⭐ [README Depth Charge (coding-horror/basic-computer-games)](https://raw.githubusercontent.com/coding-horror/basic-computer-games/main/31_Depth_Charge/README.md) — опис з книги 1978, автор Dana Noftle (Acton High School).
- [depthcharge.bas](https://raw.githubusercontent.com/coding-horror/basic-computer-games/main/31_Depth_Charge/depthcharge.bas) — повний лістинг: формула N (рядок 30), сонар (рядки 500–590), повтор (рядки 400–420).

## Непевне
- (?) Рік: 1978 — рік книги BASIC Computer Games; чи була гра в раніших збірках (DEC, Creative Computing) — не перевірено.
- (?) У старих BASIC з одинарною точністю LOG(G)/LOG(2) для G = 2^m може дати трохи менше за m, і INT зріже N на 1 — не перевіряв на справжньому інтерпретаторі (у Python для 8, 16, 1024 результат точний).
- (?) Що робить лістинг при G = 0 чи відʼємному G (LOG від нуля) — не перевірено.
