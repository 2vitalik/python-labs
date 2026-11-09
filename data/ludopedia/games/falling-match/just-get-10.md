---
title: Just Get 10
slug: just-get-10
aka: [Get 10, Just Get Ten]
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: runtime
  goal: state
year: 2014
platforms: [iOS, web (клони), PC (клони)]
links:
  - {kind: other, url: "https://apps.apple.com/cz/app/just-get-10/id933122979", best: true, note: "App Store, Veewo Games: тап по сусідніх однакових, повторний тап зливає; мета 10 і вище; Time Mode, Flash Mode; історія версій"}
  - {kind: other, url: "https://www.engadget.com/2014/12/10/just-get-10-merging-madness/", note: "огляд 2014: тап, потім тап у точці злиття; три одиниці → 2; реклама й обмежені спроби"}
  - {kind: other, url: "https://github.com/TheNarcissisticArsonist/Just-Get-10", note: "JS-клон: 5×5, 4-звʼязна група, +1 у клітині другого тапу, гравітація, розподіл нових 1–4"}
  - {kind: other, url: "https://github.com/rhodu13/JustGet10", note: "Python/Pygame-клон: складність, перевірка «є сусідня пара», перемога/поразка"}
  - {kind: other, url: "https://github.com/nenslen/just-get-10", note: "C#-клон"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=just+get+10+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [cell-click, selection-highlight, tile-merge, gravity-fall, weighted-spawn, no-moves-left, keep-playing-after-win, mode-select, time-out, move-timer, score-records, leaderboard, achievements-window, music-toggle, sound-effects, game-screen, end-screen, +connected-group-pop, +merge-at-tapped-cell, +two-tap-confirm, +edge-spawn, +limited-tries]
proposes: ["+cond:group_size", "+card:merge-at-tapped-cell", "+card:two-tap-confirm", "+card:limited-tries", "+feature:limited-tries"]
author: opus
date: 2026-11-09
---

# Just Get 10 — тапни групу однакових сусідніх чисел, тапни ще раз — вона зливається в цій клітині як число+1; доведи до 10

## Суть
Поле заповнене кольоровими плитками з числами (1, 2, 3…). Перший тап виділяє звʼязну групу однакових сусідніх плиток, другий тап по будь-якій плитці групи зливає всю групу в одну плитку на цьому місці зі значенням +1 — незалежно від розміру групи. Плитки над порожнечами падають, згори зʼявляються нові дрібні числа. Мета — отримати 10, далі можна грати вище; партія закінчується, коли на полі не лишилось жодної пари однакових сусідів.

## Поле і час
- Квадратна сітка (клони — 5×5; розмір оригіналу — ?); сусідство 4 (ортогональ).
- Покроково, без таймера в основному режимі: хід = два тапи (виділення + злиття), далі падіння й досипання.
- Гравітація вниз у кожному стовпці; нові плитки — у порожні клітини згори.
- Режими з часом: Time Mode (дістати 10 за обмежений час), Flash Mode (злити нову плитку за 2 с).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Числова плитка | tile | значення n, колір за n | у групі однакових сусідів зливається; падає без опори |
| Виділена група | zone | 4-звʼязна множина плиток з однаковим n, ≥2 | підсвічена після першого тапу; другий тап по ній зливає |
| Плитка-результат | tile | n + 1 | зʼявляється в клітині другого тапу |
| Нова плитка | tile | 1–4 з вагами (клон: 40/30/20/10 %) | досипається згори після злиття |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(tap, tile)` → ЯКЩО `adjacent_count(tile, same_value, >=, 1)` and `not state(tile, selected)` → ТО `set_state(group, selected)` — вся звʼязна група однакових (flood fill, 4 сусіди).
- КОЛИ `input(tap, tile)` → ЯКЩО `adjacent_count(tile, same_value, ==, 0)` → ТО `block` — одиночна плитка не виділяється.
- КОЛИ `input(tap, tile)` → ЯКЩО `state(tile, selected)` → ТО `merge(group, tile)`, `set_value(tile, n + 1)`, `disappear` решти групи.
- КОЛИ `input(tap, other)` → ЯКЩО `not state(other, selected)` → ТО `clear_state(group, selected)` і виділення нової групи.
- КОЛИ `after(merge)` → ТО `fall(unsupported)`, `spawn_at(weighted_1_4, top)`.
- КОЛИ `after(merge)` → ТО `score(n)` — більше злитих плиток → більший рахунок (формула — ?).
- КОЛИ `counter(max_tile, >=, 10)` → ТО `message(«10!»)`, гра триває — «or even higher».
- КОЛИ `no_moves(player)` → ТО `game_over` — нема двох однакових сусідів.
- КОЛИ `counter(time_left, ==, 0)` → ЯКЩО `mode(time)` and `custom: «10 ще не отримано»` → ТО `lose`.
- КОЛИ `spawned(new_tile)` → ЯКЩО `mode(flash)` → ТО `timer(start, 2)`; КОЛИ `custom: «2 с минули, нову плитку не злито»` → ТО `lose` (?).
- КОЛИ `game_over` → ЯКЩО `custom: «версія до 1.09»` → ТО `lives(-1)`; без спроб — купити повну гру або поділитися лінком (Engadget).

## Керування і ввід
- Тач (iPhone/iPad): тап — виділити групу; тап по виділеній — злити в цій клітині. Вибір клітини злиття — головне тактичне рішення: куди стане n+1 і що впаде поруч.
- Клони: миша (клік і повторний клік).

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Classic · Time Mode · Flash Mode · «10 secret mode» (?).
- `game-screen`: поле, `score`, `hi-score`, `selection-highlight` групи; у Time — `timer-countdown` (?).
- `end-screen` — рахунок, рекорд; full-screen реклама після раунду (Engadget, 2014).
- `leaderboard` і `achievements-window` — Game Center.
- `settings-window` — вимкнути звук і музику (v1.09).

## Фічі поза полем
- `mode-endless` (Classic), `mode-time-attack` (Time Mode, v1.09), Flash Mode (v1.20), секретні режими (?).
- `leaderboard-online`, `achievements` (Game Center, v1.20).
- `sound-toggle`, `music-toggle` (v1.09).
- Обмежені життя-спроби — у першій версії; з v1.09 прибрано, IAP «Limited Lives» / «Remove Ads».

## Варіації й родичі
- Клони: десятки студентських реалізацій на GitHub (Python/Pygame, JS, Java, C#) — популярне навчальне завдання; розмір поля й ваги нових чисел часто — параметри складності.
- Родичі в корпусі: `samegame-flood` (клік по звʼязній групі), `2048` / `threes` (злиття в наступний рівень), `triple-town` (злиття в точці постановки), `2248` (злиття ланцюгом), `drop7`.
- **Осі варіацій**: де результат (у випадковій / **у клітині тапу** / в кінці шляху) · значення результату (сума / **n+1 незалежно від розміру** / степінь двійки) · виділення (одним тапом / **тап-підтвердження**) · мета (рекорд / **конкретне число**, потім нескінченно).

## Цікавинки для курсу
- Flood fill 4-звʼязної групи однакових і підсвітка — 🌱.
- Двотапове підтвердження (виділення → злиття в обраній клітині) як стан UI — 🌱.
- Злиття n+1 у клітині тапу, гравітація по стовпцях, досипання з вагами — 📎.
- Перевірка «нема ходів» (нема пари однакових сусідів) — 🌱.
- Режими з таймером (Time, Flash 2 с) поверх того самого ядра — 📎.
- Простий жадібний AI «який тап дає найбільше злиття» — 🥉.

## Мапа на каталог
- Є: `cell-click` ↔ тап · `selection-highlight` ↔ підсвічена група · `tile-merge` · `gravity-fall` · `weighted-spawn` ↔ нові 1–4 · `no-moves-left` · `keep-playing-after-win` ↔ «10 or even higher» · `mode-select` · `time-out` ↔ Time Mode · `move-timer` ↔ Flash Mode 2 с · `score-records` · `leaderboard` · `achievements-window` · `music-toggle` · `sound-effects` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+connected-group-pop` — підтверджую; слоти {min: 2, adjacency: 4, trigger: double_tap, result: n+1}.
  - `+edge-spawn` — підтверджую (досипання згори).
  - `+merge-at-tapped-cell` «Група зливається в клітині, яку обрав гравець» · entities/interact · 🌱.
  - `+two-tap-confirm` «Перший тап виділяє, другий виконує» · interface/input · 🌱.
  - `+limited-tries` «Обмежені безкоштовні спроби» · game-logic/meta · 🌱.

## Пропозиції до словників
- `+cond:group_size` — розмір звʼязної групи однакових порівняно з N (тут ≥2); уже пропонувалось з SameGame.
- `+card:merge-at-tapped-cell` — група зливається в одну плитку в обраній гравцем клітині.
- `+card:two-tap-confirm` — дія виконується лише другим тапом по виділенню.
- `+card:limited-tries` — кількість безкоштовних партій обмежена, після — покупка/поширення.
- `+feature:limited-tries` — ліміт спроб як фіча монетизації (Just Get 10 до v1.09).

## Джерела
- ⭐ [App Store: Just Get 10](https://apps.apple.com/cz/app/just-get-10/id933122979) — «Tap the adjacent tiles with same number», «Try to get 10, or even higher!», Endless, Time Mode (1.09), Flash Mode (1.20), Game Center, Veewo Games, v1.0 11.11.2014.
- [Engadget, 10.12.2014](https://www.engadget.com/2014/12/10/just-get-10-merging-madness/) — тап і повторний тап у точці злиття, три одиниці → 2, однакові числа одного кольору, реклама й обмежені спроби.
- [JS-клон](https://github.com/TheNarcissisticArsonist/Just-Get-10) — 5×5, ваги 40/30/20/10 % для 1–4, 4-звʼязний flood fill, +1 у клітині кліку, падіння.
- [Python-клон rhodu13](https://github.com/rhodu13/JustGet10) — «Click on adjacent tiles with the same number», перевірка наявності сусідньої пари, вибір складності.
- [C#-клон nenslen](https://github.com/nenslen/just-get-10) — ще одна реалізація без графічних бібліотек.

## Непевне
- (?) Розмір поля оригіналу й ваги нових чисел — лише з клонів (5×5, 1–4); у Veewo могло бути інакше.
- (?) Формула очок не знайдена.
- (?) Flash Mode: що саме треба зробити за 2 с і що буде, якщо не встиг; «10 secret mode» — не розкрито.
- (?) Чи досипання враховує поточний максимум (у JS-клоні — ні).
- (?) Чи гра справді закінчується лише без сусідніх пар (так у клонах; в описі App Store — «Endless challenge»).
