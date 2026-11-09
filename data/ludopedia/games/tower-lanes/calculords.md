---
title: Calculords
slug: calculords
aka: []
family: tower-lanes
also: [word-number]
klass: cursor
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: runtime
  goal: state
year: 2014
platforms: [iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Calculords", best: true, note: "3 смуги між двома базами, числа + рівняння = вартість юніта, бонус за всі числа, що росте серією; Ninja Crime, 2014"}
  - {kind: other, url: "https://toucharcade.com/?p=149148", note: "TouchArcade: цифри 0–9, +/−/× без ділення, війська < 10 і техніка > 40, новий набір після використання всіх чисел, лише «clear»"}
  - {kind: other, url: "https://www.pocketgamer.com/articles/057758/calculords/", note: "Pocket Gamer: 9×7−1 = танк за 62, AP/HP, юніти штовхають ворогів, карти-бафи смуги, база з HP"}
  - {kind: other, url: "https://www.avclub.com/mobile-game-review-calculords-ios", note: "AV Club: картка юніта (вартість, AP, HP), риси flying/haste, типи, колода 30 і 3 слоти, 200+ карт"}
  - {kind: other, url: "https://www.videogamer.com/reviews/calculords-review/", note: "VideoGamer: карту можна зіграти лише з потрібним числом, бонус за всі числа"}
  - {kind: other, url: "https://www.gamezebo.com/reviews/calculords-review/", note: "Gamezebo: огляд (агентам 403)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Calculords+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [hp-damage, enemy-reached-base, ai-opponent, combo-multiplier, cursor-place, sequential-levels, +lane-grid, +number-combine, +deck-draw, +deck-builder, +card-collection, +card-keywords, +use-all-numbers-bonus, +lane-buff, +push-back-combat]
proposes: ["+role:card", "+role:unit", "+trigger:all_numbers_used", "+effect:draw_card", "+effect:combine", "+ui:equation-line", "+ui:number-hand", "+ui:card-hand", "+window:deck-builder", "+card:number-combine"]
author: opus
date: 2026-11-09
---

# Calculords — арифметика як мана: склади з чисел вартість юніта й пошли його однією з трьох смуг

## Суть
Покрокова карткова стратегія Ninja Crime (Seanbaby): дві бази на протилежних кінцях трьох смуг, юніти йдуть смугами до ворожої бази. Енергії нема — щоходу гравець отримує набір однозначних чисел і **операціями +, −, × складає з них рівно вартість** карти юніта (9 × 7 − 1 = 62 → танк). Використав усі числа набору — отримуєш бонус і новий набір у тому ж ході, а бонус росте за кожен такий хід поспіль. Ядро — числова головоломка «як витратити все» поверх лінійного TD-бою.

## Поле і час
- Три смуги, дві сторони: гравець ліворуч, AI праворуч; юніти рухаються смугою до бази суперника. Чи поділено смугу на клітини і скільки їх — не знайдено (?).
- Хід гравця: отримати числа й добрати руку → рахувати й виставляти → юніти діють; потім хід AI, який може зіграти будь-яку карту з руки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Числова карта | resource | цифра 0–9 | лежить у наборі ходу; витрачається в рівнянні |
| Операція | — | + · − · × (ділення нема) | двоє чисел → одне нове; n − n = 0 теж корисне |
| Рядок рівняння | — | поточне число | збирається з чисел і операцій; «clear» скасовує |
| Карта юніта | ally (`+role:unit`) | вартість, AP, HP, тип, риси | граєш, маючи число рівне вартості; ставиш у смугу |
| Піхота | ally | вартість здебільшого < 10 | дешево, слабко |
| Техніка | ally | вартість часто > 40 | дорога й сильна; потребує множення |
| Риса flying / haste | — | — | особливі правила руху/бою (?) |
| Тип human / machine / mutant / vehicle | — | — | синергії карт за типом |
| Карта-баф смуги | — | смуга | посилює юнітів у смузі |
| Смуга | zone | ×3 | шлях юнітів обох сторін |
| База | static | HP | 0 HP — поразка її власника |
| Ворожий юніт | enemy | AP, HP | іде до твоєї бази, бʼє юнітів і базу |
| Полководець-AI | enemy | своя колода, рука | ходить після гравця; вороги кампанії міняють правила (напр., урізають колоду до двох карт) |
| Колода | — | 30 карт, 3 слоти колод, 200+ карт у грі | з неї роздаються карти юнітів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `custom: «роздати набір чисел»`, `custom: «добрати карти юнітів до повної руки»`.
- КОЛИ `input(number, op, number)` → ЯКЩО `custom: «op ∈ {+, −, ×}»` → ТО `merge(a, b → result)`; ділення — `block`.
- КОЛИ `input(clear)` → ТО `custom: «рівняння розібрано, числа повертаються в набір»` (undo вже зіграного нема).
- КОЛИ `input(play, unit, lane)` → ЯКЩО `has(player, number == cost)` → ТО `take(player, number)`, `place(player, unit)` у початок смуги.
- КОЛИ `input(play, lane_buff, lane)` → ТО `custom: «посилити юнітів смуги»`.
- КОЛИ `counter(numbers_left, ==, 0)` → ТО `custom: «Calculords-бонус»`, `custom: «новий набір чисел у тому ж ході»`.
- КОЛИ `counter(numbers_left, ==, 0)` → ЯКЩО `chain(n)` → ТО `multiplier(×n)` — бонус більшає за кожен хід поспіль.
- КОЛИ `turn_end(player)` → ТО `custom: «юніти просуваються смугою (?)»`.
- КОЛИ `custom: «юніт зустрів ворожого в смузі»` → ТО `damage(enemy_unit, AP)`, `custom: «відкидає ворога назад»`.
- КОЛИ `hp_zero(unit)` → ТО `disappear(unit)`.
- КОЛИ `reach(unit, enemy_base)` → ТО `damage(base, AP)`.
- КОЛИ `hp_zero(enemy_base)` → ТО `win`, `give(player, card)`, `counter(xp, +n)`.
- КОЛИ `hp_zero(own_base)` → ТО `lose`.
- Перемога: знищено ворожу базу · Поразка: знищено свою базу · Рахунок: — (нагорода — нові карти й досвід).

## Керування і ввід
- Тач: тап по числу → тап по операції → тап по числу; результат стає новим числом набору. Тап по карті юніта, коли є число-вартість, → вибір смуги.
- Кнопка «clear» рівняння; скасувати вже виставленого юніта не можна.

## Вікна, меню, HUD
- `game-screen`: три смуги з юнітами, HP обох баз, `+ui:number-hand` (набір цифр), кнопки операцій, `+ui:equation-line`, `+ui:card-hand` юнітів (вартість ліворуч угорі, AP і HP знизу), лічильник бонусу.
- `+window:deck-builder` — 3 слоти колод по 30 карт; `shop-window` — паки карт за реальні гроші й вимкнення реклами.
- `end-screen` — перемога/поразка, нова карта, досвід; між боями — кампанія з ворогами-полководцями (`sequential-levels`).

## Фічі поза полем
- Кампанія: Star Nerd проти полководців, головний лиходій Hate Bit — його поплічники по одному.
- Колекція 200+ карт, нагороди за бої, повторне проходження ранніх етапів для фарму карт і досвіду.
- Free-to-play: паки по 1.99 $, карти з паків теж роздаються випадково.

## Варіації й родичі
- Родичі в сімʼї: [clash-royale](clash-royale.md) (смуги й вартість карт, але еліксир у реальному часі), [swords-and-soldiers](swords-and-soldiers.md) і [age-of-war-stick-war](age-of-war-stick-war.md) (юніти йдуть лінією до бази), [plants-vs-zombies](plants-vs-zombies.md) (смуги й валюта). Поза сімʼєю — числова «Countdown»-головоломка.
- **Осі варіацій** ресурсу на виставлення: енергія росте з часом (Clash Royale) / фіксована мана за хід / **головоломка з чисел** (Calculords) / слово (worDefense — [wordefense](wordefense.md)).

## Цікавинки для курсу
- Перебір: чи можна з набору цифр операціями +, −, × отримати ціль N, і як використати всі — 🥉 (рекурсія з мемоізацією).
- Бонус за повне використання ресурсу з серією ходів — 🌱.
- Смуговий бій двох сторін: рух, зустріч, відкидання, атака бази — 📎.
- Картка юніта (вартість, AP, HP, риси) з колоди з добором до повної руки — 📎.

## Мапа на каталог
- Є: `hp-damage` · `enemy-reached-base` · `ai-opponent` · `combo-multiplier` ↔ бонус за серію ходів · `cursor-place` ↔ виставлення юніта в смугу · `sequential-levels` ↔ кампанія.
- **Нема** → пропозиції карток:
  - `+number-combine` «Скласти ціль із чисел операціями» · game-logic/constraints · 🥉 · слот {ops: + − × ÷}.
  - `+use-all-numbers-bonus` «Бонус і новий набір за витрачений увесь ресурс» · game-logic/score · 🌱.
  - `+lane-buff` «Карта посилює одну смугу» · entities/state · 🌱.
  - `+push-back-combat` «Юніт відкидає ворога назад смугою» · entities/combat · 📎.

## Пропозиції до словників
- `+role:card` — карта в руці/колоді; `+role:unit` — бойовий юніт.
- `+trigger:all_numbers_used` — набір чисел вичерпано (бонус).
- `+effect:draw_card` — добрати карту; `+effect:combine` — два числа операцією → одне.
- `+ui:equation-line` · `+ui:number-hand` · `+ui:card-hand`; `+window:deck-builder`.
- `+card:number-combine`.

## Джерела
- ⭐ [Wikipedia: Calculords](https://en.wikipedia.org/wiki/Calculords) — 3 смуги, бази з HP, карти з числом, рівняння з набору чисел, бонус за всі числа зі зростанням серією; iOS 21.02.2014, Android 08.2014; з 2023 у сторах нема.
- [TouchArcade](https://toucharcade.com/?p=149148) — цифри 0–9, +/−/× (ділення нема), n − n = 0, війська і техніка, новий набір після використання всіх чисел, лише «clear», колода й паки, гравець ліворуч, AI праворуч.
- [Pocket Gamer](https://www.pocketgamer.com/articles/057758/calculords/) — 9 × 7 − 1 = 62, AP/HP, ролі юнітів, відкидання, бафи смуги, база з HP.
- [AV Club](https://www.avclub.com/mobile-game-review-calculords-ios) — анатомія карти, риси flying/haste, типи, колода 30, 3 слоти, 200+ карт, Hate Bit.
- [VideoGamer](https://www.videogamer.com/reviews/calculords-review/) — карта лише з потрібним числом, «Calculords bonus», free-to-play.

## Непевне
- (?) Поділ смуги на клітини, швидкість руху юнітів, коли саме вони ходять (кінець ходу?) — не знайдено.
- (?) Що дають риси flying і haste — названо в огляді, правила не описано.
- (?) Розмір набору чисел і руки юнітів, HP баз — не знайдено.
- (?) Сиквели (Calculords 2/3) — у відкритих джерелах не перевірено.
