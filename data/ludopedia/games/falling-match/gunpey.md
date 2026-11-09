---
title: Gunpey (Гунпей)
slug: gunpey
aka: [グンペイ, Gunpey EX, Gunpey-R, Gunpey DS, Gunpey Rebirth]
family: falling-match
also: [connect-rotate]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: score
year: 1999
platforms: [WonderSwan, WonderSwan Color, PlayStation, arcade, Nintendo DS, PSP, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Gunpey", best: true, note: "поле 5×10, 4 сегменти ∧ ∨ \\ /, свап вертикальних сусідів, лінія від краю до краю, добудова під час спалаху, режими Endless/Stage/Puzzle/Story/VS, сиквели"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/グンペイ", note: "S-подібні траси, «атодзуке» під час стирання, Break (DS) — падіння над стертою лінією, 10×10 у PSP, кольорові лінії EX"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=gunpey+wonderswan+gameplay", note: "пошук; геймплей WonderSwan"}
stage: v1
coverage: 60
mechanics: [line-match-clear, connectivity-check, pipe-connectors, completion-detection, chain-reaction, combo-multiplier, progress-acceleration, event-points, move-limit, level-bank, ai-opponent, hot-seat, mode-select, difficulty-levels, theme-select, background-music, gravity-fall, score-records, end-screen, +vertical-pair-swap, +edge-to-edge-path-clear, +clear-delay-extend, +rising-field, +all-clear-bonus, +same-color-path-bonus]
proposes: ["+trigger:path_complete", "+effect:extend_clear", "+effect:raise_field"]
author: opus
date: 2026-11-09
---

# Gunpey — міняй місцями вертикальних сусідів, щоб сегменти склали одну лінію від лівої стінки до правої

## Суть
Знизу підіймаються панелі з відрізками ліній чотирьох форм: ∧, ∨, \, /. Курсором гравець **міняє місцями дві вертикально сусідні клітини** (або зсуває сегмент у порожнє місце). Щойно відрізки утворюють неперервну лінію, що зʼєднує **лівий край поля з правим**, лінія спалахує і зникає; поки вона блимає, можна доєднати до неї гілки — і вони зникнуть разом (комбо). Гра названа на честь Гумпея Йокоі, творця Game Boy і WonderSwan. Це падаючий пазл без падіння: поле росте знизу, а критерій — звʼязність, як у трубопровідних іграх.

## Поле і час
- Поле 5 стовпців × 10 рядів (WonderSwan, вертикальна орієнтація консолі); Gunpey-R (PSP) — опційно 10×10.
- Кожна клітина — порожня або панель з одним відрізком, що зʼєднує два кути клітини: ∧ (лівий-низ → верх-центр → правий-низ (?)), ∨, \, /. Сусідні відрізки звʼязні, коли їхні кінці збігаються в спільному куті.
- Real-time: нові панелі підіймаються знизу рядами, швидкість росте з рівнем (Endless).
- Під час стирання лінії гра «стоїть», але курсор працює — можна доліплювати гілки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Курсор | player | 2 клітини по вертикалі | міняє місцями верхню й нижню клітини |
| Панель / | tile | кути: лівий-низ ↔ правий-верх | звʼязна з сусідами через кути |
| Панель \ | tile | кути: лівий-верх ↔ правий-низ | те саме |
| Панель ∧ | tile | обидва кінці внизу | лінія повертає вниз — дає S-траси |
| Панель ∨ | tile | обидва кінці вгорі | лінія повертає вгору |
| Порожня клітина | static | — | свап з нею = зсув сегмента |
| Лінія (траса) | zone | множина звʼязних панелей | торкається обох стінок → спалах → зникає |
| Ряд, що підіймається | spawner | випадкові панелі | вштовхує поле вгору |
| Кольорова панель (EX) | tile | колір | лінія з одного кольору → бонус |
| Затінена панель (Story) | hazard | — | ставить CPU; знімається заповненою шкалою |
| Бомба (Story) | projectile | — | CPU кидає знизу вгору (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move_cursor)` → ТО `move(cursor, dir)` у межах поля.
- КОЛИ `input(swap)` → ТО `swap(cell_upper, cell_lower)` під курсором (лише вертикальні сусіди; порожня клітина теж міняється).
- КОЛИ `timer(rise_rate)` → ТО `custom: «raise — усе поле на ряд вгору, знизу новий ряд випадкових панелей»`.
- КОЛИ `after(swap|raise)` → ЯКЩО `connected(segments, left_wall, right_wall)` → ТО `custom: «лінія спалахує — стан clearing на t»`.
- КОЛИ `state_on(line, clearing)` → ЯКЩО `custom: «до лінії доєднали нові звʼязні панелі»` → ТО `custom: «extend_clear — панелі приєднуються до лінії, що стирається»`, `combo(+1)`.
- КОЛИ `state_off(line, clearing)` → ТО `clear(line_cells)`, `score(n_panels × combo)` (?).
- КОЛИ `after(clear)` → ЯКЩО `mode(original)` → ТО клітини лишаються порожніми; ЯКЩО `mode(break)` (DS+) → ТО `fall(panels_above)` на кількість стертих — можливі нові лінії.
- КОЛИ `after(clear)` → ЯКЩО `all_gone(panels)` → ТО `score(+all_clear_bonus)`.
- КОЛИ `after(clear)` → ЯКЩО `same(line_panels, color)` → ТО `score(+bonus)` (Gunpey EX).
- КОЛИ `reach(panel, top_edge)` → ТО `lose` (Endless).
- Stage: КОЛИ `counter(lines, ≥, quota)` → ТО `win`, `next_level`; ЯКЩО `custom: «скінчились панелі запасу»` → ТО `lose`.
- Puzzle: КОЛИ `all_gone(panels)` → ЯКЩО `count(lines, ==, given)` → ТО `win`; панелі не мають лишатися.
- Story: КОЛИ `custom: «хід CPU»` → ТО `spawn_at(shadow_panel|bomb, field)`; КОЛИ `counter(gauge, ==, full)` → ТО `disappear_a(shadow_panels)`.
- VS: КОЛИ `after(clear)` → ТО `counter(sp, +k)`; що вища складність, то менше SP за лінію.
- Рахунок: панелі в лінії, комбо-добудова, all clear; поразка — панель дійшла до верху.

## Керування і ввід
- WonderSwan: X-пад (хрестовина) рухає курсор 1×2, кнопка — обмін верх/низ.
- Gunpey DS: стилусом тягнути сегменти; або класичне керування кнопками.
- Ключова техніка «атодзуке»: зібрати першу лінію й поки вона блимає — швидко доєднувати гілки.

## Вікна, меню, HUD
- `main-menu` з `mode-select`: Endless · Stage · Puzzle · Story (оригінал) · VS.
- `difficulty-select` для VS: High · Normal · Low · Poor.
- `puzzle-select` — номер пазлу (Puzzle mode) (?).
- `game-screen`: поле 5×10, курсор, `score`, `level-number`, лічильник ліній; Stage — `remaining-counter` панелей; Story — шкала зняття тіні; VS — SP.
- `skin-select` (Gunpey-R: 40 скінів, музика реагує на гру).
- `end-screen` → рекорди.

## Фічі поза полем
- Режими: `mode-endless`, Stage (квота з обмеженим запасом), `mode-puzzle`, Story (vs CPU з атаками), `mode-versus`; Gunpey DS — 9 персонажів, «Gunpey-kun» action-режим, секвенсор «Пікопіко-машина».
- Gunpey EX: онлайн-рейтинги через WonderGate.
- `theme-select` (скіни PSP), `custom-difficulty` (10×10).

## Варіації й родичі
- Professor Henoheno (1997, поле 4×6) → Gunpey (WonderSwan, 1999) → PlayStation, аркада → Gunpey EX (WSC, 2000: кольори, без Story) → Gunpey DS / Rebirth (2006: Break, стилус) → Gunpey-R (PSP, 2006: 40 скінів, 10×10) → мобільні.
- Родичі: Pipe Mania / Net (звʼязність сегментів, `connect-rotate`), Panel de Pon (курсор-свап сусідів, підйом поля, «активний ланцюг»), Lumines (скіни + музика).
- **Осі варіацій**: свап (вертикальний / горизонтальний / обертання плитки) · умова зникнення (край–край / замкнений цикл / джерело–приймач) · після зникнення (дірки / падіння зверху) · подача (підйом знизу / падіння згори).

## Цікавинки для курсу
- Звʼязність по кутах клітин: граф вершин-кутів, сегмент = ребро; перевірка «лівий край ↔ правий край» BFS-ом — 📎.
- Свап лише вертикальних сусідів курсором 1×2 — 🌱.
- Вікно добудови: лінія в стані «clearing», доліплені гілки входять у зчищення — 🥉.
- Два режими після зникнення (дірки vs Break-падіння) як прапорець правил — 🌱.
- Генерація ряду, що підіймається, без готових ліній — 📎.
- Puzzle mode: використати всі панелі рівно за N ліній — 🥈 (розвʼязувач перебором свапів).

## Мапа на каталог
- Є: `line-match-clear` (найближча: перевірка після кожного ходу) · `connectivity-check` · `pipe-connectors` (сегмент = порти на кутах) · `completion-detection` · `chain-reaction` · `combo-multiplier` · `progress-acceleration` · `event-points` · `move-limit` (Stage — обмежений запас) · `level-bank` (Puzzle) · `ai-opponent` · `hot-seat` (VS; найближча) · `mode-select` · `difficulty-levels` · `theme-select` · `background-music` · `gravity-fall` (Break) · `score-records` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+vertical-pair-swap` «Курсор міняє дві вертикальні клітини» · interface/input · 🌱 (дзеркало горизонтального свапу Panel de Pon).
  - `+edge-to-edge-path-clear` «Траса від краю до краю зникає» · entities/interact · 📎.
  - `+clear-delay-extend` «Добудова того, що зникає, під час затримки» · entities/interact · 🥉.
  - `+rising-field` «Поле підіймається знизу рядами» · entities/move · 🌱 (Panel de Pon теж).
  - `+all-clear-bonus` «Бонус за порожнє поле» · game-logic/score · 🌱.
  - `+same-color-path-bonus` «Бонус за одноколірну трасу» · game-logic/score · 🌱.

## Пропозиції до словників
- `+trigger:path_complete` — склалась траса між двома заданими межами (Gunpey; Pipe Mania — джерело→злив); альтернатива — `after(x)` + ⏳ `connected`.
- `+effect:extend_clear` — додати клітини до групи, що вже в стані зникнення.
- `+effect:raise_field` — поле піднімається на ряд, знизу новий ряд (Gunpey, Panel de Pon; ⏳ `shift(all, up)` близький, але без генерації).

## Джерела
- ⭐ [Wikipedia: Gunpey](https://en.wikipedia.org/wiki/Gunpey) — поле 5×10, чотири сегменти, вертикальний свап, лінія край–край, спалах і комбо, all clear, режими, сиквели.
- [ja.wikipedia: グンペイ](https://ja.wikipedia.org/wiki/グンペイ) — S-траси, «атодзуке», Break (DS), 10×10 (PSP), кольорові лінії EX.
- YouTube: пошук «gunpey wonderswan gameplay».

## Непевне
- (?) Точна геометрія ∧/∨: чи кінці в кутах клітини (так за ja.wikipedia «кінці на кутах»), і як ∧ стикується з /.
- (?) Розміри: англ. Wikipedia «5×10», японська «10 стовпців × 5 рядів» — орієнтація поля неясна (WonderSwan тримають вертикально?).
- (?) Формула очок, тривалість спалаху, темп підйому.
- (?) Чи свап з порожньою клітиною дозволений над «повітрям» (чи падає панель в оригіналі — ні, гравітації нема).
- (?) Бомби в Story кидає CPU чи гравець.
