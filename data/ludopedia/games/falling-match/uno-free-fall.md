---
title: Uno Free Fall
slug: uno-free-fall
aka: [UNO Free Fall, Uno Freefall, UNO Freefall]
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: hidden
  random: runtime
  goal: score
year: 2006
platforms: [mobile, GBA, DS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Uno_Free_Fall", best: true, note: "Classic: 8 стовпців, трійки за кольором/числом/символом, Wild, закриті картки, Draw 2 / Wild Draw 4, Skip/Reverse і лічильник рядів, рівні, кінець — картка вгорі"}
  - {kind: other, url: "https://www.pocketgamer.com/uno-bundle/review/", note: "огляд Java-«Uno Bundle» (2008): дошка з Uno-блоків, групи сусідніх за кольором/числом, Wild чистить усі групи"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=uno+free+fall+gba+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [gravity-fall, line-match-clear, chain-reaction, spawn-schedule, progress-acceleration, event-points, cell-click, keyboard-controls, game-screen, end-screen, mode-select, +multi-attribute-match, +face-down-reveal, +rising-garbage-row, +meter-pause-cards]
proposes: ["+cond:match_any(color|number|symbol)", "+ui:row-meter", "+card:multi-attribute-match", "+card:face-down-reveal"]
author: opus
date: 2026-11-09
---

# Uno Free Fall — картки Uno падають у 8 стовпців; трійка зникає, якщо збігається колір, число або символ

## Суть
Падаючий матч-пазл на колоді Uno. Карти падають згори, гравець скидає їх в один із восьми стовпців; три картки, що збігаються **хоча б за однією** властивістю Uno — колір, число або символ, — зникають і дають очки. Частина карток лежить сорочкою догори: їх не можна зібрати, доки поруч не зникнуть сусіди або не зіграє Draw 2 / Wild Draw 4 — тоді вони відкриваються й можуть запустити комбо. Збоку тікає лічильник: коли він спорожніє, на поле додається ряд закритих карток; Skip і Reverse зупиняють або подовжують його.

## Поле і час
- Квадратна сітка з 8 стовпців (Classic); висота — (?).
- Гравітація вниз; картки падають згори безперервно, лічильник рядів спадає в реальному часі.
- Інформація прихована: закриті картки невідомі до відкриття.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Картка Uno (числова) | tile | колір ×4, число 0–9 | падає у стовпець; трійка за кольором/числом/символом зникає |
| Wild | tile | — | рахується будь-яким кольором |
| Skip / Reverse | tile | колір | у трійці — зупиняє або подовжує лічильник рядів |
| Draw 2 / Wild Draw 4 | tile | колір / wild | у трійці — відкриває закриті картки |
| Закрита картка | tile | прихована | не збирається; відкривається, коли поруч зникли картки або зіграв Draw |
| Поточна картка | player | тип | скидається в обраний стовпець |
| Лічильник рядів | spawner | спадає з часом | спорожнів → ряд закритих карток |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(every)` → ТО `spawn_at(card, top)`.
- КОЛИ `input(column)` → ЯКЩО `free(top_cell(column))` → ТО `place(card, column)`, `fall(card)`.
- КОЛИ `settled` → ЯКЩО `custom: «3 сусідні відкриті картки мають спільний колір, або число, або символ»` → ТО `clear(group)`, `score(n)`.
- КОЛИ `settled` → ЯКЩО `state(card, wild)` → ТО `custom: «Wild підходить під будь-який колір у трійці»`.
- КОЛИ `after(clear)` → ЯКЩО `occupied(neighbour, face_down)` → ТО `reveal(neighbour)`; відкрита картка може скласти нову трійку (`chain(n)` → комбо).
- КОЛИ `after(clear)` → ЯКЩО `custom: «у трійці Draw 2 або Wild Draw 4»` → ТО `reveal(face_down)` (які саме — (?)).
- КОЛИ `after(clear)` → ЯКЩО `custom: «у трійці Skip»` → ТО `timer(stop)` лічильника рядів на час (?); Reverse → `timer(+n)`.
- КОЛИ `counter(row_meter, ==, 0)` → ТО `spawn_at(face_down_row, field)`, `custom: «лічильник починає знову»` (куди додається ряд — (?)).
- КОЛИ `counter(goal, >=, n)` → ТО `counter(level, +1)`, `multiplier(×k)` (більше очок за збір), `speed(row_meter, +n)`.
- КОЛИ `reach(card, top)` → ТО `lose`, `window(end-screen)`.
- Перемоги нема · Поразка: картка дійшла до верху · Рахунок: очки за трійки, комбо після відкриттів, множник рівня.

## Керування і ввід
- GBA: D-pad вліво/вправо — вибір стовпця, кнопка — скинути (?).
- Телефон: клавіші/джойстик телефона (?).
- Java-бандл 2008 — виділення групи сусідніх карт курсором (див. «Варіації»).

## Вікна, меню, HUD
- `main-menu` → `mode-select` (Classic і, судячи з назви, інші режими — (?)).
- `game-screen`: 8 стовпців, падаюча картка, `+ui:row-meter` збоку, `score`, `level-number`.
- `end-screen` — рахунок (?).

## Фічі поза полем
- `mode-classic`; рівні з ціллю (`levels-sequential`-подібно: рівень росте від виконаної цілі).
- Решта (рекорди, збереження) — (?).

## Варіації й родичі
- GBA (2007, Black Lantern / Zoo Digital), мобільна (2006, Oasis / Player X), DS-збірка «Uno / Skip-Bo / Uno Freefall».
- Java «Uno Bundle» (2008, огляд PocketGamer): поле в стилі Tetris з Uno-блоків, ряди прибувають, гравець виділяє групу сусідніх блоків одного кольору чи числа — більша група дає більше очок; спецблоки перевертають або перемішують дошку, Wild чистить усі групи разом (SameGame-логіка, а не трійки; та сама гра чи порт — (?)).
- Родичі в корпусі: [columns](columns.md) і [dr-mario](dr-mario.md) (трійки при падінні), [drop7](drop7.md) (закриті диски відкриваються від сусідніх зникнень, ряд знизу), [panel-de-pon](panel-de-pon.md) (сміття, що відкривається), [samegame-flood](samegame-flood.md) (вибір групи — Java-версія).
- **Осі варіацій**: ознака збігу (одна / **будь-яка з кількох: колір ∨ число ∨ символ**) · закриті плитки (нема / відкриваються сусіднім зникненням / спецкартою) · тиск (швидкість падіння / **лічильник рядів, яким керують Skip/Reverse**).

## Цікавинки для курсу
- Збіг «за будь-якою з трьох властивостей» — 🌱; а як шукати трійки, коли карта може належати до трьох груп одночасно, — 📎.
- Закриті картки, що відкриваються від зникнення сусідів, + комбо — 🌱.
- Лічильник рядів, який гравець зупиняє/подовжує спецкартами, — 🌱.
- Ефекти спецкарт Uno, перенесені з настільної гри в пазл (Draw → відкрити, Skip → пауза), — 📎 як вправа на таблицю ефектів.

## Мапа на каталог
- Є: `gravity-fall`; `line-match-clear` ↔ трійка зникає; `chain-reaction` ↔ відкриття → нова трійка; `spawn-schedule` ↔ ряд за лічильником; `progress-acceleration` ↔ рівні пришвидшують лічильник; `event-points`; `cell-click` / `keyboard-controls` ↔ вибір стовпця; `game-screen`, `end-screen`, `mode-select`.
- **Нема** → пропозиції карток:
  - `+multi-attribute-match` «Збіг за будь-якою з кількох властивостей» · entities/interact · 🌱 · слоти {props: color|number|symbol}.
  - `+face-down-reveal` «Закрита плитка відкривається від сусіднього зникнення» · entities/state · 🌱 (родич `+crackable-blank` з Drop7).
  - `+rising-garbage-row` (уже пропонувалось Drop7) — ряд закритих карток за лічильником.
  - `+meter-pause-cards` «Спецплитки зупиняють/подовжують таймер небезпеки» · game-logic/waves · 🌱.

## Пропозиції до словників
- `+cond:match_any(color|number|symbol)` — дві плитки «однакові», якщо збігається будь-яка з перелічених властивостей (у коді `same` — одна властивість).
- `+ui:row-meter` — шкала-таймер до нового ряду сміття.
- `+card:multi-attribute-match`, `+card:face-down-reveal` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Uno Free Fall](https://en.wikipedia.org/wiki/Uno_Free_Fall) — Classic-режим, 8 стовпців, трійки, Wild, закриті картки, Draw 2 / Wild Draw 4, Skip/Reverse і лічильник, рівні, поразка, платформи й дати.
- [Pocket Gamer: Uno Bundle](https://www.pocketgamer.com/uno-bundle/review/) — Java-версія 2008: групи сусідніх блоків, спецблоки, Wild.

## Непевне
- (?) «Трійка» — рівно 3 у лінію (горизонталь/вертикаль) чи група з 3+ сусідніх — Wikipedia каже лише «groups of three»; чи більші групи дають більше очок у GBA-версії.
- (?) Куди додається ряд закритих карток (знизу з підняттям стосу чи згори) і висота поля.
- (?) Які саме закриті картки відкриває Draw 2 / Wild Draw 4 (сусідні чи всі), на скільки Skip зупиняє і Reverse подовжує лічильник.
- (?) Інші режими, крім Classic, і керування — джерела не описують; веб-архів і GameFAQs недоступні.
- (?) Чи Java «Uno Freefall» (2008) — та сама мобільна гра 2006 року чи інша реалізація.
