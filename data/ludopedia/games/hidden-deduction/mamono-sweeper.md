---
title: Mamono Sweeper
slug: mamono-sweeper
aka: [マモノスイーパー, Mamono, Monster Sweeper]
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
year: null
platforms: [web (Flash), web (HTML5), Android]
links:
  - {kind: other, url: "https://www.mzrg.com/mines/mamono.shtml", best: true, note: "правила англійською: сума рівнів, формула шкоди, EXP, HP, таблиця режимів, керування"}
  - {kind: official, url: "http://hojamaka.com/games/mamono_sweeper/", note: "автор Hojamaka Games (JP): грати, правила бою, BLIND, HUD LV/HP/EX/NE/T, мітки цифрами"}
  - {kind: other, url: "https://skich.app/games/mamono-sweeper", note: "картка Android-версії: 13.02.2015, v1.07, знято зі сторів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mamono+Sweeper", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [cell-click, flood-reveal, hp-damage, destroy-all-enemies, difficulty-levels, mode-select, completion-detection, score-records, remaining-counter, status-panel, game-screen, end-screen, flag-cycle, +sum-of-levels-clue, +xp-level-up, +auto-battle-exchange, +exp-doubling-by-level, +numbered-monster-marks, +blind-mode-inverted-goal]
proposes: ["+effect:xp", "+effect:level_up", "+cond:level_cmp", "+ui:ex-ne-counter", "+feature:mode-combination", "+card:auto-battle-exchange", "+card:exp-doubling-by-level", "+card:numbered-monster-marks", "+card:blind-mode-inverted-goal"]
author: opus
date: 2026-11-09
---

# Mamono Sweeper — сапер з RPG: число — сума рівнів монстрів довкола, бий слабших, рости в рівні, лише тоді йди на сильніших

## Суть
Замість мін на полі сховані монстри рівнів 1–9, а число на відкритій клітині — сума їхніх рівнів у 8 сусідах. Клік по монстру — автоматичний бій: слабший за тебе гине без шкоди, сильніший знімає HP. За вбитих дається досвід, досвід підвищує твій рівень, тож порядок відкриття — головна стратегія: спершу вичистити дрібноту, потім братися за сильних. Мета — вбити всіх монстрів; у Blind-режимах навпаки — нікого не чіпати й відкрити все безпечне.

## Поле і час
- Квадратна сітка, 8-сусідство; розміри фіксовані режимом: Easy 16×16 (30 монстрів), Normal 30×16 (99), Huge 50×25 (260), Extreme 30×16 (125), Blind 30×16 (99), Huge×Extreme 50×25 (324), Huge×Blind 50×25 (260).
- Час не впливає на правила: хід = клік; таймер `T` лише міряє проходження (рекорди — за часом).
- Шари: приховане поле → відкриті клітини (числа / мертві монстри) → мітки гравця.
- На мобільному — скрол перетягуванням і pinch-зум (великі поля).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой (не на полі) | player | LV (старт 1; Blind — 0), HP (10; Huge 30; Blind 1), EX, NE | бʼє монстра силою LV, отримує EX за вбивство |
| Монстр рівня 1–9 | enemy | level 1–9 | прихований; при відкритті — бій; колір розрізняє рівні до 5 |
| Закрита клітина | static | прихований вміст | відкривається кліком (вказівник має лишатися на клітині до відпускання) |
| Відкрита клітина з числом | mark | n = сума рівнів монстрів у 8 сусідах | 0 → каскад відкриття сусідів |
| Мертвий монстр | mark | — | клік перемикає показ: монстр ↔ сума рівнів довкола (без нього самого) |
| Мітка гравця | mark | число (рівень) | ставиться на закриту клітину; клавішами по колу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(open, c)` → ЯКЩО `not occupied(c, monster)` → ТО `reveal(c)` з числом `custom: «сума рівнів монстрів серед 8 сусідів»`.
- КОЛИ `after(reveal(c))` → ЯКЩО `custom: «число = 0»` → ТО `reveal(neighbors8)` каскадом.
- КОЛИ `input(open, c)` → ЯКЩО `occupied(c, monster)` → ТО `reveal(c)`, `custom: «бій: герой бʼє на LV, монстр, якщо живий, відповідає; повтор до смерті одного»`.
- КОЛИ `custom: «бій»` → ЯКЩО `custom: «рівень монстра ≤ LV»` → ТО `disappear_b` без шкоди.
- КОЛИ `custom: «бій»` → ЯКЩО `custom: «рівень монстра > LV»` → ТО `damage(level × ⌈(level − LV) / LV⌉)` (приклад: LV 5 проти рівня 7 → 7 шкоди).
- КОЛИ `died(monster)` → ТО `counter(EX, +2^(level−1))` — рівень 1 дає 1 EX, кожен наступний рівень подвоює.
- КОЛИ `counter(NE, <=, 0)` → ТО `custom: «LV +1, NE — до наступного порогу»`.
- КОЛИ `input(open, dead_monster)` → ТО `custom: «перемкнути показ монстр ↔ сума рівнів довкола»`.
- КОЛИ `input(mark, c)` → ЯКЩО `not state(c, revealed)` → ТО `mark(c, n)` по колу (порожньо нижче 2 і вище 5 або 9 — залежно від режиму; 1 — лише в Blind).
- КОЛИ `hp_zero(hero)` → ТО `lose` (HP ≤ 0 — єдиний спосіб програти).
- КОЛИ `all_gone(monster)` → ЯКЩО `not mode(blind)` → ТО `win`.
- КОЛИ `custom: «відкрито всі клітини без монстрів»` → ЯКЩО `mode(blind)` → ТО `win`.
- Blind: LV 0 і HP 1 — будь-який монстр убиває, тож гра стає класичним сапером на суми рівнів.
- Перемога: усі монстри вбиті (Blind — усе безпечне відкрито). · Поразка: HP ≤ 0. · Рахунок: очок нема, рекорд — час.

## Керування і ввід
- Клік / тап — відкрити клітину; вказівник має лишатися на клітині впродовж кліку (на відміну від класики, де досить відпустити над нею).
- Мітки: A/D або ←/→ над закритою клітиною — число по колу (mzrg-версія); цифрові клавіші — мітка рівнем (сайт Hojamaka).
- Тап по індикатору рівня внизу — режим міток (ПК і мобільний).
- Клік по вбитому монстру — перемикання «монстр / сума довкола».
- Автор mzrg радить Flash-версію: мітки A/D там швидші.

## Вікна, меню, HUD
- `mode-select` / `difficulty-select`: Easy, Normal, Huge, Extreme, Blind, Huge×Extreme, Huge×Blind.
- `game-screen`: поле; HUD `LV`, `HP`, `EX` (досвід), `NE` (лишилось до рівня), `T` (час); нижня смуга — довідка по монстрах (у Blind — `remaining-counter` непомічених монстрів); кнопка звуку (2023).
- `end-screen`: перемога / поразка (?).
- Переходи: `mode-select` → `game-screen` → `end-screen` → `mode-select` (?).

## Фічі поза полем
- `difficulty-presets` — сім фіксованих режимів, зокрема комбіновані (Huge×Extreme, Huge×Blind).
- `mode-classic` і Blind як окремий режим з оберненою метою.
- Рекорди за часом (mzrg веде таблиці швидкості) — у самій грі не підтверджено (?).
- `sound-toggle` (кнопка звуку з 23.08.2023); посилання на «старий варіант» для повільних пристроїв.

## Варіації й родичі
- Нащадки «сапер + рівні монстрів»: [dragonsweeper](dragonsweeper.md) (сила монстра, золото = досвід), [demoncrawl](demoncrawl.md) (роглайк-забіг), [mamono-mower](mamono-mower.md) (реальний час, косарка, ривок +1 рівень).
- Класика, з якої виросла: [minesweeper](minesweeper.md); сапер з «іншими мінами» — [cavern-sweeper](cavern-sweeper.md), [tacticsweeper](tacticsweeper.md).
- **Осі варіацій**: число = кількість / сума рівнів; поразка = 1 вибух / HP; шкода = фіксована / формула від різниці рівнів; мета = відкрити безпечне / вбити всіх; досвід = лінійний / подвоєння за рівень.

## Цікавинки для курсу
- Число-сума рівнів замість кількості (одна зміна в генераторі підказок) — 🌱.
- Авто-бій «бʼю на LV, отримую у відповідь» з формулою ⌈різниця / LV⌉ — 🌱.
- Досвід 2^(рівень−1) і пороги рівня: баланс «спершу дрібнота» — 📎.
- Мітки-рівні по колу клавішами (не лише прапорець) — 🌱.
- Режим Blind як інверсія мети тієї ж механіки (LV 0, HP 1) — 🌱.
- Розвʼязувач для сум рівнів: дедукція стає системою рівнянь з цілими 1–9 — 🥇.

## Мапа на каталог
- Є: `cell-click` · `flood-reveal` ↔ каскад нулів · `hp-damage` ↔ HP героя · `destroy-all-enemies` ↔ мета · `difficulty-levels` + `mode-select` ↔ сім режимів · `flag-cycle` ↔ мітки по колу · `remaining-counter` ↔ Blind · `status-panel` ↔ LV/HP/EX/NE · `score-records` ↔ час.
- **Нема** → пропозиції карток:
  - `+auto-battle-exchange` «Авто-бій обміном ударів до смерті» · entities/combat · 🌱.
  - `+exp-doubling-by-level` «Досвід 2^(рівень−1)» · entities/state · 🌱.
  - `+numbered-monster-marks` «Мітка — число-рівень, а не прапорець» · interface/input · 🌱.
  - `+blind-mode-inverted-goal` «Режим з інвертованою метою» · game-logic/win · 🌱.
  - `+sum-of-levels-clue`, `+xp-level-up` — як у Dragonsweeper.

## Пропозиції до словників
- `+effect:xp` · `+effect:level_up` — як у Dragonsweeper / Mamono Mower (ще не у словнику).
- `+cond:level_cmp(a, b, op)` — рівень A порівняно з рівнем B (як у Mamono Mower).
- `+ui:ex-ne-counter` — пара «досвід / лишилось до рівня».
- `+feature:mode-combination` — режими-комбінації (Huge×Extreme).

## Джерела
- ⭐ [mzrg: Mamono Sweeper](https://www.mzrg.com/mines/mamono.shtml) — повні правила англійською, формула шкоди, EXP, таблиця режимів, керування A/D.
- [Hojamaka Games: マモノスイーパー](http://hojamaka.com/games/mamono_sweeper/) — оригінал: бій, BLIND, HUD, мітки цифрами, режим міток для тачу.
- [skich.app](https://skich.app/games/mamono-sweeper) — Android-версія 2015, v1.07.
- ⭐-лінк черги `https://www.mzrg.com/js/mamono/index.html` віддав 404 — не використано.

## Непевне
- (?) Рік першої (Flash) версії — у джерелах нема; черга пише 2008–2010; Android — 13.02.2015.
- (?) Точні пороги NE на кожен рівень — mzrg дає лише графіки у % досвіду.
- (?) HP у Huge×Extreme не вказано.
- (?) Кількість монстрів кожного рівня в режимах не бачив.
- (?) Як виглядає кінцевий екран і чи є таблиця рекордів у самій грі.
