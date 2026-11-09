---
title: Number Match / Take Ten (Numberzilla)
slug: number-match
aka: [Take Ten, Numberzilla, Numbers, Digits, Sunflower seeds, Column, Make Ten, Match 10]
family: word-number
also: [falling-match]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: setup
  goal: state
year: 2019
platforms: [paper, iOS, Android]
links:
  - {kind: other, url: "https://apps.apple.com/us/app/numberzilla/id1482131986", best: true, note: "Numberzilla: пари рівних або з сумою 10, сусідство по рядку/стовпцю і з кінця рядка на початок наступного, порожні між — можна; PLUS, бустери, режими"}
  - {kind: other, url: "https://apps.apple.com/us/app/id1559290008?l=en-us", note: "Take Ten! Number Match: «класична паперова гра»; дописування залишку, мета — порожнє поле, undo/hint"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=number+match+take+ten+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [cell-click, selection-highlight, no-moves-left, completion-detection, remaining-counter, event-points, score-records, undo-step, mode-select, daily-puzzle, shop-window, game-screen, end-screen, help-window, save-autosave, +pair-sum-match, +linear-wrap-adjacency, +append-remaining, +empty-row-collapse, +booster-items]
proposes: ["+cond:pair_sum", "+cond:clear_path", "+effect:append_copy", "+ui:add-button", "+ui:adds-left", "+feature:boosters"]
author: opus
date: 2026-11-09
---

# Number Match / Take Ten — викреслюй пари рівних цифр або з сумою 10; застряг — допиши залишок у кінець

## Суть
Поле — цифри 1–9, записані рядками однакової ширини, як текст. Гравець викреслює пару сусідніх чисел, якщо вони рівні (4–4) або в сумі дають 10 (2–8). «Сусідні» — у рядку, у стовпці або через перенос рядка, причому порожні (викреслені) клітини між ними не заважають. Коли ходів нема, всі невикреслені числа переписуються в кінець — поле росте; мета — очистити його повністю. Паперова гра з дитинства (Numbers, Sunflower seeds, Column), з 2019 — хвиля мобільних «Number Match».

## Поле і час
- Поле — послідовність чисел, покладена рядками фіксованої ширини (9 у паперовій версії і більшості апів (?)); читається як текст: кінець рядка → початок наступного.
- Шари: цифри + стан «викреслено» (у апах — клітина порожніє).
- Хід = одна пара; часу нема (Classic). У режимах Survival/Sprint числа «падають» знизу/зверху з часом.
- Поле може рости без меж (Classic у Numberzilla — «unlimited time and board space»).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Число | tile | 1–9, стан active/crossed | викреслюється в парі; викреслене — «прозоре» для сусідства |
| Рядок | zone | ширина W | повністю порожній рядок зникає, нижні піднімаються (?) |
| Кнопка PLUS / «Add» | switch | лічильник використань (?) | дописує копії всіх невикреслених у кінець |
| Підказка | pickup (UI) | кількість | підсвічує доступну пару |
| Бомба (Numberzilla) | pickup | — | прибирає 9 чисел у червоній зоні-цілі |
| Swap (Numberzilla) | pickup | — | міняє місцями будь-які два числа |
| Падаючі числа (Survival/Sprint) | spawner | темп | додають рядки з часом; поле переповнилось — поразка |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(tap a)` → ТО `custom: «a виділено»` (повторний тап знімає виділення).
- КОЛИ `input(tap b)` → ЯКЩО `same(a, b, value)` or `custom: «a + b = 10»` → і `custom: «між a і b по рядку / стовпцю / через перенос — лише порожні клітини»` → ТО `disappear_both`, `score(n)`.
- КОЛИ `input(tap b)` → ЯКЩО пара не підходить → ТО `shake`, `custom: «виділення переходить на b»` (?).
- КОЛИ `after(disappear_both)` → ЯКЩО `custom: «рядок став повністю порожнім»` → ТО `clear(row)`, `collapse`, `score(bonus)` (?).
- КОЛИ `no_moves(player)` → ТО `custom: «підсвітити PLUS»`.
- КОЛИ `input(plus)` → ЯКЩО `custom: «лишились використання»` → ТО `custom: «дописати копії всіх активних чисел у кінець послідовності в тому ж порядку»`.
- КОЛИ `counter(active_numbers, ==, 0)` → ТО `win`, `window(end-screen)`.
- КОЛИ `no_moves(player)` → ЯКЩО `custom: «додавань не лишилось»` → ТО `lose` (апи з лімітом PLUS) (?).
- КОЛИ `input(hint)` → ЯКЩО `has(player, hint)` → ТО `custom: «підсвітити одну доступну пару»`, `take(player, hint)`.
- КОЛИ `input(bomb, target)` → ТО `clear(9 cells in zone)`.
- КОЛИ `input(swap, a, b)` → ТО `swap(a, b)`.
- Survival: КОЛИ `timer(every)` → ТО `spawn_at(number_row, edge)`; КОЛИ `custom: «поле заповнене»` → ТО `lose`.
- Sprint: КОЛИ `counter(cleared_above_marked_rows, ==, all)` → ЯКЩО `timer(<, limit)` → ТО `win`; інакше `lose`.
- Перемога: порожнє поле · Поразка: нема ходів і додавань / переповнення (Survival) / час (Sprint) · Рахунок: очки за пари й рядки, рекорд.

## Керування і ввід
- Тап по першому числу, тап по другому — пара. Паперова версія — олівцем закреслити.
- Кнопки: PLUS (дописати), підказка, undo (Take Ten), бустери (Numberzilla).
- Режим SHUFFLE у Dynamic — після рівня перемішати числа, щоб помножити очки.

## Вікна, меню, HUD
- `game-screen`: поле, `score`, `add-button` з `adds-left` (?), `hint-button`, `undo-button`, кнопки бустерів, `selection-highlight`, `hint-marker`.
- `mode-select`: Classic · Survival · Dynamic · Sprint (Numberzilla).
- `daily-window`: «Guess the Code» — щоденний код сейфа з бонусами (Numberzilla).
- `shop-window`: бустери, підписка Premium (без реклами, безлімітні підказки/бомби/swap).
- `end-screen`: очки, рекорд, «далі».
- `help-window`: правила пар і сусідства.
- Переходи: `main-menu` → `mode-select` → `game-screen` → `end-screen` → новий рівень.

## Фічі поза полем
- `undo`, `hint` (обмежені в безкоштовній версії, за відгуками).
- `mode-classic`, `mode-endless`, `mode-time-attack` (Sprint), Survival.
- `daily-puzzle` — окрема міні-гра дня (код сейфа), не сам Number Match.
- `boosters`: бомба, swap, shuffle — за валюту / підписку.
- `leaderboard-local` / рекорди, `autosave` поточного поля (?).

## Варіації й родичі
- Паперова «Take Ten / Numbers / Семечки»-класика: стартовий рядок 1…9, далі цифри чисел 10–19 підряд (1 1 1 2 1 3 …) (?).
- Мобільні: Number Match (Easybrain) (?), Numberzilla (AppsYouLove), Take Ten! (Shadowbiz) — різняться діагоналями, лімітом PLUS, бустерами.
- Родичі: пасьянси на пари (Pyramid — сума 13), Mahjong solitaire (вільна пара), Lines 98 і 2048 (`falling-match`) — поле росте, поки не очистиш.
- **Осі варіацій:** правило пари (рівні / сума 10 / сума N) · сусідство (рядок+стовпець / + діагональ / + перенос) · дописування (без ліміту / N разів) · порожні рядки (лишаються / зникають) · час (нема / падіння чисел).

## Цікавинки для курсу
- Пошук легальної пари з «прозорими» порожніми клітинами: лінійний скан по послідовності + по стовпцю — 📎.
- Перенос рядка як сусідство (поле = 1D-масив, 2D — лише відображення) — 🌱.
- Дописування залишку + стиснення порожніх рядків — 🌱.
- Розвʼязувач: чи можна очистити поле за K додавань (перебір з мемоізацією; простір вибухає) — 🥇.
- Survival-режим (рядки падають за таймером) — 📎: та сама логіка в real-time.

## Мапа на каталог
- Є: `cell-click` ↔ тап по числу · `selection-highlight` ↔ виділене перше число · `no-moves-left` ↔ «нема пар» · `completion-detection` ↔ поле порожнє · `remaining-counter` ↔ лишилось чисел (?) · `event-points` / `score-records` ↔ очки й рекорд · `undo-step` ↔ undo в Take Ten · `mode-select` ↔ 4 режими · `daily-puzzle` · `shop-window` · `save-autosave` (?).
- **Нема** → пропозиції карток:
  - `+pair-sum-match` «Пара: рівні або в сумі N» · entities/interact · 🌱 · слоти {sum: 10}.
  - `+linear-wrap-adjacency` «Сусідство в лінійній послідовності з переносом і прозорими порожніми» · entities/legality · 📎.
  - `+append-remaining` «Дописати копію залишку в кінець поля» · entities/spawn · 🌱 · слоти {limit: int}.
  - `+empty-row-collapse` «Порожній рядок зникає, нижні піднімаються» · entities/move · 🌱.
  - `+booster-items` «Бустери поза правилами (бомба, swap, shuffle)» · game-logic/economy · 📎.

## Пропозиції до словників
- `+cond:pair_sum` — сума значень двох сутностей дорівнює N (Take Ten, Pyramid solitaire).
- `+cond:clear_path` — між двома клітинами по лінії лише порожні (Number Match, Mahjong-«вільна», Onet).
- `+effect:append_copy` — дописати копії обраних сутностей у кінець поля.
- `+ui:add-button` — кнопка «дописати»; `+ui:adds-left` — лишилось дописувань.
- `+feature:boosters` — одноразові інструменти поза правилами за валюту.

## Джерела
- ⭐ [App Store: Numberzilla](https://apps.apple.com/us/app/numberzilla/id1482131986) — правила пар і сусідства, PLUS, бомба/swap, режими Classic/Survival/Dynamic/Sprint, «Guess the Code», Premium.
- [App Store: Take Ten! Number Match](https://apps.apple.com/us/app/id1559290008?l=en-us) — «класична паперова гра», дописування залишку, порожнє поле, undo/hint; інші назви (у пошуку).
- YouTube: пошук «number match take ten gameplay».

## Непевне
- (?) Ширина рядка 9 і стартова послідовність паперової гри (1…9, далі цифри 10–19) — з памʼяті; джерела не підтвердили.
- (?) Порожні рядки зникають — з опису черги й памʼяті; сторінка Numberzilla цього не каже.
- (?) Діагональне сусідство: є в деяких апах (Easybrain Number Match) — Numberzilla його не згадує.
- (?) Ліміт натискань PLUS і поразка, коли їх вичерпано, — у паперовій версії ліміту нема; в апах — різниться.
- (?) Очки: бонус за очищений рядок — з памʼяті.
- Рік: паперова гра — без дати; Numberzilla — точна дата релізу на сторінці не вказана, 2019 — з черги (?).
- `aka` Numbers / Digits / Sunflower seeds / Column / Make Ten — зі сторінки Take Ten! (через пошук); «Семечки» у «Варіаціях» — з памʼяті (?).
