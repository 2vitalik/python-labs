---
title: Linelith
slug: linelith
aka: []
family: thinky
also: [connect-rotate, pencil-logic]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2022
platforms: [PC, macOS, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1923790/Linelith", best: true, note: "70+ пазлів на скелях і кристалах: лінії за формою і символами, кілька «twists», будь-який пазл можна пропустити; Patrick Traynor, 19.05.2022"}
  - {kind: itch, url: "https://patricktraynor.itch.io/linelith", note: "itch.io: та сама гра, Godot, ~півгодини на сесію, ключ Steam"}
  - {kind: other, url: "https://www.wasdland.com/game/linelith-1923790", note: "відгуки Steam: «draw a line to clear the puzzle», підказка-число в куті, без туторіалу, краще мишею"}
  - {kind: other, url: "https://weloveeverygame.com/games/1923790-linelith.html", note: "опис: істота бігає астероїдом між пазлами, без сюжету"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Linelith+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 35
mechanics: [path-drawing, path-cut, satisfy-constraints, completion-detection, neighbor-count-clue, skip-level, world-map, +rule-discovery, +shape-bound-line]
proposes: ["+effect:extend_path", "+card:rule-discovery", "+card:shape-bound-line"]
author: opus
date: 2026-11-09
---

# Linelith — проведи лінію по скелі-фігурі так, щоб виконались символи; що означають символи, гравець відкриває сам

## Суть
Пазли «вросли» в скелі й кристали на маленькому астероїді: кожна скеля — фігура з клітин, гравець малює по ній лінію. Лінія мусить пасувати до форми скелі і до символів на ній; правил гра не пояснює — перші прості пазли навчають символ, далі він комбінується з іншими. Ядро — **відкриття правила через спроби**, як у The Witness; але форма поля сама є частиною умови. Гра коротка: 70+ пазлів, за відгуками 45 хв – 2 год.

## Поле і час
- Кожен пазл — окрема фігура з квадратних клітин на скелі (?); між пазлами — маленька істота ходить астероїдом (хаб-мапа).
- Статично: хід = намальована лінія; перевірка, коли лінію завершено (?).
- Пізні пазли додають «кілька хитрих поворотів» механіки (не розкрито джерелами).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Скеля / кристал | zone | форма з клітин | поле пазла; лінія лягає в її межах |
| Лінія гравця | mark | шлях клітинами/ребрами (?) | малюється мишею; повернення назад стирає хвіст (?) |
| Число в куті | mark | n | скільки клітин біля цього кута має бути використано лінією |
| Інші символи й вузли | mark | тип | правила відкриваються гравцем; описів у джерелах нема (?) |
| Істота-аватар | player | — | ходить між пазлами на астероїді |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, cell)` → ЯКЩО `custom: «клітина сусідня з кінцем лінії і в межах скелі»` → ТО `custom: «подовжити лінію»`; інакше `block`.
- КОЛИ `input(drag, back)` → ТО `custom: «вкоротити лінію»` (?).
- КОЛИ `input(release)` → ЯКЩО `all_constraints_met` → ТО `win`, `custom: «скеля світиться, пазл позначено розвʼязаним»`.
- КОЛИ `input(release)` → ЯКЩО `constraint_broken(c)` → ТО `custom: «лінія скидається / показує помилку»` (?).
- Обмеження «число в куті»: ЯКЩО `adjacent_count(corner, line_cell, ==, n)` — інакше `constraint_broken`.
- Обмеження форми: лінія `custom: «відповідає формі скелі»` (?): ймовірно проходить усю фігуру або від краю до краю.
- КОЛИ `input(skip)` → ТО `custom: «залишити пазл і повернутись пізніше»`.
- Перемога: усі пазли астероїда · Поразка: нема · Рахунок: нема.

## Керування і ввід
- Миша: drag лінії по фігурі; відгуки радять «справжню мишу» — великі пазли незручні на трекпаді й Steam Deck.
- Між пазлами — керування істотою на хаб-мапі (?).

## Вікна, меню, HUD
- `game-screen`: астероїд зі скелями-пазлами; розвʼязані підсвічені (?).
- `main-menu` / `settings-window` — мінімальні (?).
- HUD майже відсутній; туторіалу нема.

## Фічі поза полем
- `skip-level`: будь-який пазл можна покинути й повернутись.
- Без сюжету, без підказок (?); саундтрек і звук — Brendan Julian.

## Варіації й родичі
- Родичі: The Witness і Taiji (лінія/розмітка на панелях, правила відкриває гравець) — `thinky/taiji-witness-panels`; Slitherlink (числа біля клітин рахують ребра лінії) — `pencil-logic`; Flow Free, LYNE (лінія-шлях за правилами) — `connect-rotate`.
- Автор — Patrick Traynor (Patrick's Parabox).
- **Осі варіацій:** поле — сітка-панель / фігура довільної форми · правила — пояснені / відкриваються · символ — у клітині / в куті / на ребрі.

## Цікавинки для курсу
- Лінія в межах довільної фігури з клітин + відкат хвоста — 🌱.
- Перевірник «число в куті = кількість клітин лінії навколо кута» — 📎.
- Набір незалежних перевірок-символів і їх композиція в одному пазлі — 🥉.
- Дизайн «навчального» пазла, що однозначно відкриває правило — 🥈.

## Мапа на каталог
- Є: `path-drawing` · `path-cut` (?) · `satisfy-constraints` · `completion-detection` · `neighbor-count-clue` ↔ число в куті · `skip-level` (тут без ліміту) · `world-map` ↔ астероїд-хаб.
- **Нема** → пропозиції карток:
  - `+rule-discovery` «Правила символів не пояснюються, їх відкривають на простих пазлах» · design · 🥈.
  - `+shape-bound-line` «Лінія в межах фігури довільної форми» · interface/input · 📎.

## Пропозиції до словників
- `+effect:extend_path` — підтвердження (Flow Free, Trainyard).
- `+card:rule-discovery`, `+card:shape-bound-line` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam](https://store.steampowered.com/app/1923790/Linelith) — 70+ пазлів на скелях і кристалах, лінії «conforming to their shape and their symbols», twists, пропуск пазлів, дата, платформи.
- [itch.io](https://patricktraynor.itch.io/linelith) — те саме, Godot, ~30 хв сесія.
- [WASDland (відгуки)](https://www.wasdland.com/game/linelith-1923790) — «draw a line to clear the puzzle», число біля кута, без туторіалу, миша.
- [We Love Every Game](https://weloveeverygame.com/games/1923790-linelith.html) — істота на астероїді, без сюжету (з результату пошуку).

## Непевне
- (?) Точні правила: чи лінія має покрити всю фігуру, чи йде клітинами або ребрами, де старт і кінець, що означають інші символи — джерела не розкривають (спойлери), Thinky Games віддає 403.
- (?) Як гра показує помилку і чи є undo — не звірено.
- (?) Хаб-істота і її керування — лише з опису в результатах пошуку.
- Тека: `thinky` (ядро — відкриття правила, родич Taiji/Witness), а не призначена `connect-rotate` — там у `also`. coverage низький через брак джерел.
