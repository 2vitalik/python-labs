---
title: Hurkle
slug: hurkle
aka: [HURKLE]
family: hidden-deduction
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: hidden
  random: setup
  goal: state
year: 1973
platforms: [мінікомпʼютер BASIC (People's Computer Company), BASIC Computer Games (1978), console]
links:
  - {kind: other, url: "https://raw.githubusercontent.com/coding-horror/basic-computer-games/main/51_Hurkle/README.md", best: true, note: "опис з BASIC Computer Games: сітка 10×10, 0,0 у південно-західному куті, 5 спроб («four guesses is actually enough»), напрям після кожної спроби; автор Bob Albrecht (PCC)"}
  - {kind: other, url: "https://raw.githubusercontent.com/coding-horror/basic-computer-games/main/51_Hurkle/hurkle.bas", note: "оригінальний лістинг: G=10, N=5, «GO» + NORTH/SOUTH + EAST/WEST, автоматичний новий раунд"}
  - {kind: other, url: "https://www.atariarchives.org/basicgames/showpage.php?page=94", note: "скан сторінки книги BASIC Computer Games (лінк із README, не відкривав)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hunt_the_Wumpus", note: "Development: на початку 1973 Yob бачив у PCC Hurkle і Mugwump — «хованки» на сітці 10×10"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mugwump_(video_game)", note: "предок: та сама сітка, підказка — відстань; «Mugwump led to similar games such as Hurkle»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=hurkle+basic+computer+game", note: "пошук; геймплей"}
stage: v1
coverage: 80
mechanics: [console-render, spawn-random-cell, move-limit, game-screen, end-screen, help-window, +direction-hint, +coordinate-input, +auto-new-round, +belief-set-tracking]
proposes: ["+cond:coord_cmp", "+window:text-prompt", "+card:direction-hint", "+card:coordinate-input", "+card:auto-new-round"]
author: opus
date: 2026-11-09
---

# Hurkle — знайди схованого Хуркла на сітці 10×10 за п'ять спроб, коли після кожного промаху чуєш лише «GO NORTHEAST»

## Суть
Текстова гра People's Computer Company (Bob Albrecht): комп'ютер ховає Хуркла в одній з 100 точок сітки 10×10. Гравець вводить координати «X,Y»; якщо не влучив — отримує лише **напрям**, куди йти (північ/південь і схід/захід, разом до 8 румбів). П'ять спроб на раунд, хоча вистачає чотирьох: підказка — порівняння по кожній осі окремо, тож гра — дві паралельні бінарні пошуки. Саме від таких «хованок на сітці 10×10» відштовхнувся Gregory Yob, створюючи [Hunt the Wumpus](hunt-the-wumpus.md).

## Поле і час
- Поле — точки сітки G×G, G = 10: координати 0…9; точка 0,0 — південно-західний кут; перше число — горизонталь (X, схід), друге — вертикаль (Y, північ).
- Поля на екрані нема: лише текстовий діалог; мапу гравець тримає в голові чи на папері.
- Покроково: хід = одна спроба. Хуркл не рухається.
- Раунди йдуть один за одним без меню: після перемоги чи поразки одразу ховається новий Хуркл.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Хуркл | neutral | точка (A, B), A, B ∈ 0…9 | ховається випадково, стоїть на місці |
| Спроба | mark | точка (X, Y) | вводиться текстом; влучання або відгук-напрям |
| Відгук «GO …» | mark | NORTH/SOUTH + EAST/WEST | знак різниці по кожній осі; порожньо по осі, що збіглася |
| Лічильник спроб | resource | N = 5 | 0 лишилось — поразка раунду |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `message(правила)`, `spawn_at(hurkle, (A, B))`, де A = INT(10·RND), B = INT(10·RND).
- КОЛИ `input(guess, X, Y)` → ЯКЩО `custom: «|X−A| + |Y−B| = 0»` → ТО `win`, `message(«YOU FOUND HIM IN K GUESSES!»)`.
- КОЛИ `input(guess, X, Y)` → ЯКЩО не влучив → ТО `feedback(guess)`: `message(«GO » + вертикаль + горизонталь)`.
- Вертикаль: ЯКЩО `custom: «Y спроби < Y Хуркла»` → «NORTH»; ЯКЩО `>` → «SOUTH»; ЯКЩО рівні → нічого.
- Горизонталь: ЯКЩО `custom: «X спроби < X Хуркла»` → «EAST»; ЯКЩО `>` → «WEST»; ЯКЩО рівні → нічого.
- Звідси 8 відповідей: NORTH, SOUTH, EAST, WEST, NORTHEAST, NORTHWEST, SOUTHEAST, SOUTHWEST.
- КОЛИ `counter(guesses, ==, 5)` → ЯКЩО не знайдено → ТО `lose`, `reveal(hurkle)` («SORRY, THAT'S 5 GUESSES. THE HURKLE IS AT A,B»).
- КОЛИ `game_over` → ТО `restart` («LET'S PLAY AGAIN, HURKLE IS HIDING.»): нова схованка без запитання; виходу з циклу в лістингу нема.
- Вхід не перевіряється: точка поза 0…9 приймається як звичайна спроба (у лістингу нема перевірки меж).
- Перемога: вгадати точку · Поразка: 5 промахів · Рахунок: кількість спроб K.

## Керування і ввід
- Рядок «GUESS #K ?» → гравець друкує «X,Y» (два цілих через кому) і Enter.
- Жодних клавіш руху чи курсора: вся інформація — числа і слова.
- Оптимальна тактика: по кожній осі брати середину ще можливого відрізка; три відповіді на вісь (менше / рівно / більше) дають 2⁴ − 1 = 15 ≥ 10 значень за 4 спроби.

## Вікна, меню, HUD
- `help-window` = вступний текст правил, друкується завжди на старті (G і N підставлені в текст).
- `game-screen` = `text-prompt`: «GUESS #K», рядок відповіді «GO …».
- `end-screen` = рядки «YOU FOUND HIM IN K GUESSES!» або «SORRY… THE HURKLE IS AT A,B».
- Цифрова версія: сітка 10×10 з позначеними спробами і стрілками-відгуками (`hint-marker`), заштрихована виключена зона (`fog-overlay`), `move-counter` «спроба K з 5».
- Переходи: старт → правила → спроби → кінець раунду → новий раунд (без меню).

## Фічі поза полем
- Налаштування — лише в коді: G (розмір) і N (спроби) — перші рядки програми (README: «you may change this number»).
- Нескінченна серія раундів без рахунку; рекордів і збережень нема.
- Порти на сучасні мови в репозиторії coding-horror (Python, C#, Java, JS, Kotlin, Lua, Perl, Ruby, Rust, VB.NET).

## Варіації й родичі
- Mugwump (PCC, 1973) — та сама сітка 10×10, але відгук — відстань, 10 ходів, мугвампів кілька (?); Wikipedia: «Mugwump led to similar games such as Hurkle and later Snark».
- [Depth Charge](depth-charge.md) — той самий відгук-напрям, але в кубі G×G×G і «де був постріл» замість «куди йти»; бюджет рахується від розміру.
- [Hunt the Wumpus](hunt-the-wumpus.md) — протест проти сіткових хованок: граф замість сітки.
- [Battleship](battleship.md) — відгук «мимо/влучив» без напрямку; [Mastermind](mastermind.md) — відгук на код.
- «Вгадай число» (вище/нижче) — одновимірний предок; Hurkle = дві такі гри одночасно.
- **Осі варіацій**: відгук — напрям / відстань (Mugwump) / тепло-холодно / так-ні · поле — 1D / 2D / 3D / граф · ціль — нерухома / тікає · бюджет — фіксований / від розміру.

## Цікавинки для курсу
- Консольна гра з циклом «ввід → перевірка → відгук», нескінченні раунди — 🌱.
- Відгук-напрям: знак різниці по кожній осі, складання назви румба — 🌱.
- Автогравець бінарним пошуком на двох осях і доказ «4 спроб досить» (2^k − 1 ≥ G) — 📎.
- Графічна версія: сітка з виключеними прямокутниками (множина можливих точок після кожного відгуку) — 📎.
- Хуркл, що тікає на 1 клітину після промаху, і перевірка, чи гра ще виграшна — 🥉.

## Мапа на каталог
- Є: `console-render` ↔ текстовий інтерфейс · `spawn-random-cell` ↔ схованка · `move-limit` ↔ 5 спроб, 0 = провал · `game-screen` / `end-screen` / `help-window` ↔ текстові блоки.
- **Нема** → пропозиції карток:
  - `+direction-hint` «Відгук-напрям до схованого (знак по кожній осі)» · game-logic/constraints · 🌱 · слот {words: compass|higher-lower, frame: go-to|shot-was}.
  - `+coordinate-input` «Ввід координат текстом замість кліку» · interface/input · 🌱.
  - `+auto-new-round` «Новий раунд одразу після кінця, без меню» · game-logic/win · 🌱.
  - `+belief-set-tracking` (Scotland Yard) — прямокутник можливих точок Хуркла.

## Пропозиції до словників
- `+cond:coord_cmp(a, b, axis, op)` — координата A по осі порівняно з B (основа відгуку-напряму; Depth Charge — та сама умова); у реченнях поки `custom`.
- `+window:text-prompt` — консольний екран «запит → відповідь» як вікно гри (повтор Hunt the Wumpus).
- Вжито наявні без пропозицій: `feedback(guess)`, `message`, `spawn_at`, `restart`.

## Джерела
- ⭐ [README Hurkle (coding-horror/basic-computer-games)](https://raw.githubusercontent.com/coding-horror/basic-computer-games/main/51_Hurkle/README.md) — опис з книги 1978: сітка, 0,0 на південному заході, 5 спроб, «approximate direction», автор Bob Albrecht.
- [hurkle.bas](https://raw.githubusercontent.com/coding-horror/basic-computer-games/main/51_Hurkle/hurkle.bas) — повний лістинг: G=10, N=5, підпрограма напряму (рядки 610–730), повтор раунду (рядки 440–470).
- [Wikipedia: Hunt the Wumpus](https://en.wikipedia.org/wiki/Hunt_the_Wumpus) — Hurkle серед ігор PCC на початку 1973.
- [Wikipedia: Mugwump](https://en.wikipedia.org/wiki/Mugwump_(video_game)) — родич із підказкою-відстанню, PCC Journal 1973.

## Непевне
- (?) Рік: черга дає 1978 — це рік книги BASIC Computer Games; за Wikipedia гра вже була серед ігор PCC на початку 1973, точна дата першої публікації не знайдена.
- Розбіжність у корпусі: [hunt-the-wumpus.md](hunt-the-wumpus.md) («Варіації й родичі») пише, що Hurkle, Mugwump і Snark дають підказку-відстань, і в осях — «відстань (Hurkle)»; лістинг і README Hurkle дають **напрям**, відстань — у Mugwump.
- (?) Snark — правила не перевіряв, лише згадка у Wikipedia (Mugwump).
- (?) Чи відрізнялась оригінальна PCC-версія від книжкової (тексти, кількість спроб) — не перевірено.
