---
title: mine1k
slug: mine1k
aka: []
family: hidden-deduction
also: []
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: hidden
  random: setup
  goal: state
year: 2022
platforms: [PICO-8, web (HTML5), Windows, macOS, Linux, Raspberry Pi]
links:
  - {kind: itch, url: "https://pancelor.itch.io/mine1k", best: true, note: "грати в браузері; керування, «1024 байти стисненого коду разом зі спрайтами»"}
  - {kind: other, url: "https://gist.github.com/pancelor/a3aadc5e8cdf809cf0a4972ac9598433", note: "вихідний код з коментарями автора про стиснення"}
  - {kind: other, url: "https://itch.io/jam/pico-1k-2022", note: "PICO-1K Jam 2022 — обмеження 1 КБ стисненого коду"}
  - {kind: other, url: "https://github.com/thisismypassport/shrinko8", note: "shrinko8 — мініфікатор PICO-8, яким міряли стиснений розмір"}
stage: v1
coverage: 80
mechanics: [cell-click, chord-click, flag-cycle, flood-reveal, neighbor-count-clue, remaining-counter, face-button, completion-detection, game-screen, gui-render, +min-size-implementation, +reveal-queue-flood, +rle-string-sprites]
proposes: ["+feature:size-budget", "+card:min-size-implementation", "+card:reveal-queue-flood", "+card:rle-string-sprites"]
author: opus
date: 2026-11-09
---

# mine1k — класичний сапер у 1024 байтах стисненого коду PICO-8: що лишається від гри, коли рахуєш кожен байт

## Суть
Демейк Minesweeper від pancelor для PICO-1K Jam 2022: увесь картридж — 1024 байти стисненого коду разом зі спрайтами, закодованими в рядках. Механіка — канонічний [Minesweeper](minesweeper.md); цінність файла — як **мінімальний набір**: що автор визнав обовʼязковим (відкриття, прапорці, акорд, каскад нулів, лічильник мін, таймер, смайлик-рестарт), а чим пожертвував (безпечний перший клік, фіксована кількість мін, налаштування).

## Поле і час
- Сітка 16 × 14 = 224 клітини (індекс 0–223), клітина 8 px; поле нижче смуги HUD.
- Міни — незалежно в кожній клітині з імовірністю 1/9 (`rnd(9)>7`), тож кількість мін щоразу інша.
- Таймер — +1/30 с за кадр (30 fps). Пазл без тіків поля: стан змінюється лише кліком.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Закрита клітина | tile | — | відкривається кліком; може мати прапорець |
| Міна | hazard | ймовірність 1/9 на клітину | відкриття = поразка |
| Число | mark | 0–8 (сусіди-міни з 8) | нуль запускає каскад відкриття |
| Прапорець | mark | вкл/викл | блокує відкриття, змінює лічильник мін |
| Смайлик | switch | стан: гра / програш / перемога | клік — нове поле |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «кожна клітина — міна з імовірністю 1/9»`; числа = `adjacent_count(c, mine)`; захисту першого кліку нема.
- КОЛИ `input(open, c)` → ЯКЩО `cell(c, mine)` → ТО `lose`, `reveal(all)`.
- КОЛИ `input(open, c)` → ЯКЩО `not cell(c, mine)` → ТО `reveal(c)`.
- КОЛИ `after(reveal(c))` → ЯКЩО `adjacent_count(c, mine, ==, 0)` → ТО `custom: «додати 8 сусідів у чергу відкриття»` (каскад через чергу, без рекурсії).
- КОЛИ `input(flag, c)` → ЯКЩО `cell(c, closed)` → ТО `mark(c, flag)` / `unmark(c)`, `counter(mines_left, ∓1)`.
- КОЛИ `input(chord, n)` → ЯКЩО `adjacent_count(n, flag, ==, value(n))` → ТО `custom: «усі сусіди n — у чергу відкриття»`; поки кнопки затиснуті — підсвітка 3×3.
- КОЛИ `counter(closed_safe, ==, 0)` → ТО `win`.
- КОЛИ `input(click, smiley)` → ТО `restart`.
- Перемога: відкрити всі безпечні клітини · Поразка: відкрити міну · Рахунок: час у таймері.

## Керування і ввід
- Лівий клік — відкрити; правий — прапорець; обидві кнопки разом — акорд (затиснути → підсвітка 3×3, відпустити на числі → відкриття сусідів).
- Клік по смайлику — нове поле. Клавіатури нема.

## Вікна, меню, HUD
- `game-screen`: поле 16×14; угорі `remaining-counter` (міни мінус прапорці) і `timer-elapsed` у трицифрових «семисегментних» цифрах, по центру `face-button`.
- Окремих вікон, меню, налаштувань нема — програш і перемога показуються станом смайлика й полем.

## Фічі поза полем
- `size-budget` (джем-обмеження): 1024 байти стисненого коду; повторюваний код стискається добре, тому автор інколи свідомо писав «довше, але повторно».
- Відкритий код (gist) з коментарями «spooky» — рядки, де порядок впливає на стиснений розмір.

## Варіації й родичі
- Механіка — [Minesweeper](minesweeper.md); великі розширення сімʼї — [Minesweeper Infinite](minesweeper-infinite.md), [14 Minesweeper Variants](14-minesweeper-variants.md).
- **Осі варіацій** (мінімалізму): генерація «ймовірність на клітину / рівно N мін»; перший клік «без захисту / безпечний»; каскад «рекурсія / черга»; HUD «повний / нема».

## Цікавинки для курсу
- Сапер на один екран коду: черга відкриття замість рекурсії (каскад нулів) — 🌱.
- Сусіди як рядок зміщень + перевірка, що не перескочили край рядка (`abs(i%16 - j%16) < 2`) — 🌱.
- Стан гри одним числом (`death`: 999 — гра, `time` — програш, `time-1000` — перемога) і смайлик з нього — 🌱.
- Спрайти в рядку з RLE-кодуванням і розпакування на старті — 📎.
- Челендж «зроби гру ≤ N байт» як завдання з розміром у метриці — 📎.

## Мапа на каталог
- Є: `cell-click` · `chord-click` · `flag-cycle` (лише вкл/викл) · `flood-reveal` · `neighbor-count-clue` · `remaining-counter` · `face-button` · `completion-detection` · `game-screen` · `gui-render`.
- **Нема** → пропозиції карток:
  - `+min-size-implementation` «Гра в межах байтового бюджету» · project · 📎 · слот {bytes: 1024}.
  - `+reveal-queue-flood` «Каскад відкриття через чергу» — варіант `flood-reveal` · 🌱.
  - `+rle-string-sprites` «Спрайти рядком з RLE» · interface/render · 📎.

## Пропозиції до словників
- `+feature:size-budget` — обмеження розміру коду/картриджа як частина задуму (джеми 1K, 4K).

## Джерела
- ⭐ [itch.io: mine1k](https://pancelor.itch.io/mine1k) — опис, керування, розмір 1024 байти, PICO-1K Jam 2022.
- [Gist: код mine1k](https://gist.github.com/pancelor/a3aadc5e8cdf809cf0a4972ac9598433) — поле 16×14, генерація 1/9, черга відкриття, акорд, стан `death`, RLE-спрайти, нотатки про shrinko8.
- [PICO-1K Jam 2022](https://itch.io/jam/pico-1k-2022) · [shrinko8](https://github.com/thisismypassport/shrinko8).

## Непевне
- (?) Рік — 2022 з назви джему; точна дата релізу на сторінці не вказана.
- (?) Як саме виглядають три стани смайлика — у мініфікованому коді не розібрати.
