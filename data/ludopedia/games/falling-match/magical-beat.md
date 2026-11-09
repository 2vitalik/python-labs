---
title: Magical Beat
slug: magical-beat
aka: [マジカルビート, "Magical Beat: Beat de Tsunagu Ochimono Puzzle", ビートでつなぐオチモノパズル]
family: falling-match
also: []
klass: avatar
axes:
  field: square
  time: rhythm
  opponent: ai
  info: full
  random: runtime
  goal: survive
year: 2012
platforms: [arcade (NESiCAxLive), PS Vita, PS3, Steam]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/マジカルビート", best: true, note: "JA: поле 6×9, L з 3 бітонів, шкала синхронізації такту, BEST, Tsunagi Time 4 долі, jammers, режими, BPM пісень"}
  - {kind: steam, url: "https://store.steampowered.com/app/3516620/MAGICAL_BEAT/", note: "PC (2025): правила для гравця, 100+ треків, локальний PvP"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Magical+Beat+Vita+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [gravity-fall, multi-cell-size, piece-rotate-flip, next-queue, simultaneous-versus, garbage-attack, ai-opponent, difficulty-levels, sequential-levels, mode-select, tutorial-window, online-multiplayer, background-music, keyboard-controls, end-screen, +connected-group-pop, +delayed-clear-window, +rhythm-gated-drop, +rhythm-sync-tempo, +timing-judgement-bonus, +miss-scatter-penalty, +garbage-offset, +garbage-adjacent-clear, +no-lose-during-clear, +song-select]
proposes: ["+trigger:beat", "+cond:on_beat", "+window:song-select", "+card:rhythm-gated-drop", "+card:miss-scatter-penalty", "+card:no-lose-during-clear", "+card:delayed-clear-window"]
author: opus
date: 2026-11-09
---

# Magical Beat — фігура лягає лише в такт музики; зібрана трійка блимає 4 долі, і її можна доростити

## Суть
Змагальна падаюча головоломка Arc System Works: L-фігури з трьох кольорових «бітонів», збіг — 3+ однакових по сторонах. Незвичне — **ритм як умова ходу**: скинути фігуру можна лише тоді, коли бар шкали синхронізації в синій зоні такту; промах — фігура розсипається випадково. Зібрана група не зникає одразу: 4 долі вона блимає (Tsunagi Time), і до неї можна доліплювати той самий колір — велике зникнення засипає суперника сірими jammers.

## Поле і час
- Поле 6 стовпців × 9 рядів, один бітон на клітину; над полем ще один прихований ряд, що теж тримає блок.
- Час = такт обраної пісні: шкала синхронізації поруч із полем ходить угору-вниз у темпі BPM (від 70 до 247 у списку пісень); центр шкали — одна доля.
- Versus: два поля; пісню обирають перед матчем (в intrusion-боях — по черзі, перша випадкова).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фігура | player | L з 3 бітонів; 4 кольори (червоний, синій, зелений, жовтий), у Jigoku + помаранчевий | зсув, поворот ліворуч/праворуч, скидання в такт |
| Бітон | tile | колір | 3+ однакових по сторонах → група блимає 4 долі, потім зникає |
| Блимаюча група | zone | 4 долі | однокольорові бітони, що торкнулись її, приєднуються; зникає вся разом |
| Jammer (сірий бітон) | hazard | — | сам із собою не збігається; зникає, коли поруч по рядку/стовпцю зникає звичайний бітон |
| Прихований ряд | zone | 1 ряд над полем | може тримати блок |
| Верх поля | zone | — | стек дійшов → поразка (крім Tsunagi Time) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «beat — доля пісні»` → ТО `custom: «бар шкали проходить центр»`; між долями бар рухається вгору-вниз у темпі BPM.
- КОЛИ `input(shift)` → ЯКЩО `free(target_cells)` → ТО `move(piece, dir)`; КОЛИ `input(rotate_l|rotate_r)` → ТО `rotate(piece, ±90)`.
- КОЛИ `input(drop)` → ЯКЩО `custom: «on_beat — бар у синій зоні»` → ТО `fall(piece)` у вибраний стовпець.
- КОЛИ `input(drop)` → ЯКЩО `custom: «бар у центрі — BEST»` → ТО `fall(piece)`, `score(+bonus)`, більше jammers супернику.
- КОЛИ `input(drop)` → ЯКЩО `custom: «бар у чорній зоні»` → ТО `custom: «фігура розсипається — бітони падають у випадкові місця поля»`.
- КОЛИ `settled` → ЯКЩО `pattern(group(3+, same_color, adj4))` → ТО `set_state(group, blinking, 4 beats)` — Tsunagi Time.
- КОЛИ `contact(biton, blinking_group)` → ЯКЩО `same(biton, group, color)` → ТО `custom: «бітон приєднується до групи»`.
- КОЛИ `state_off(group, blinking)` → ТО `clear(group)`, `score(n)`.
- КОЛИ `after(clear)` → ТО `fall(all_unsupported)`; нові групи → ланцюг.
- КОЛИ `custom: «поле заповнене»` → ЯКЩО `state(any_group, blinking)` → ТО поразки нема — Tsunagi Time рятує.
- КОЛИ `after(clear)` → ЯКЩО `custom: «багато за раз / BEST / ланцюг / зачистка в Tsunagi Time»` → ТО `send_garbage(jammers)`; кількість визначають очки.
- КОЛИ `custom: «до гравця летять jammers»` → ТО `custom: «попередження з числом над полем»`; ЯКЩО встиг очистити своє до падіння → ТО `custom: «offset — вхідні jammers гасяться»`.
- КОЛИ `custom: «поруч по рядку або стовпцю зник звичайний бітон»` → ТО `disappear(jammer)`.
- КОЛИ `custom: «стек дійшов до верху»` → ТО `lose`; intrusion-бій — до 2 перемог.
- Перемога: суперник програв (CPU-стадії, 2 раунди в intrusion) · Поразка: стек до верху поза Tsunagi Time · Рахунок: зачистки, бонус BEST, ланцюги, Tsunagi Time.

## Керування і ввід
- Ліво/право — зсув; дві кнопки — поворот ліворуч/праворуч; окрема дія — скинути (поставити) фігуру.
- Головне — ритм: скидати точно в долю, бо BEST дає бонус, а промах у чорну зону — хаос на полі.
- Steam: клавіатура/геймпад, локальний PvP на одному екрані.

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Hiyoko · Futsuu · Jigoku · Oreno · Futari (дім) · Mugen (дім) · Net Battle (Vita).
- `custom: «song-select»` — вибір пісні (BGM) перед матчем; в intrusion — по черзі.
- `game-screen`: поле 6×9, `custom: «шкала синхронізації такту»` поруч із полем (синя зона / чорна зона / центр BEST), `next-piece-preview` до 4 фігур, `garbage-meter` — число вхідних jammers над полем, `score`, поле суперника.
- `end-screen` раунду / матчу; у CPU-режимах — наступна стадія.
- `tutorial-window` — у режимі Hiyoko.

## Фічі поза полем
- Режими: Hiyoko (5 CPU-стадій з навчанням, проходиш до кінця навіть з поразками) · Futsuu (10 стадій, CPU сильнішає) · Jigoku (10 стадій, CPU на максимумі, 5 кольорів) · Oreno (5-стадійна практика, ☆1–5 — 4 кольори, ★1–5 — 5) · Mugen (випадкові персонажі й пісні до поразки).
- `difficulty-presets` через режими; `mode-versus`: intrusion в аркаді, Futari (Vita ad hoc / PS3 два контролери), `online-multiplayer` (Vita Ver.1.02 Net Battle).
- Музика — частина правил: оригінальні треки Kikuo + BlazBlue, Guilty Gear, XBlaze; DLC-пісні в Mugen; Steam — понад 100 треків.
- Steam: `achievements`, `cloud-save`.

## Варіації й родичі
- [lumines](lumines.md) — інший спосіб привʼязати падаючі блоки до музики: лінія часу стирає квадрати в такт; тут ритм обмежує сам ввід.
- [trioncube](trioncube.md) — те саме «вікно до зникнення», яке можна продовжити (там — таймер між квадратами).
- [puyo-puyo](puyo-puyo.md) — дуель, сміття з offset; [baku-baku-animal](baku-baku-animal.md), [magical-drop](magical-drop.md) — аркадні змагальні родичі.
- Crypt of the NecroDancer — той самий принцип «дія лише в долю» в роглайку.
- **Осі варіацій**: що ритм обмежує (ввід / зачистку / нічого) · штраф за промах (нема / розсип / пропуск) · коли зникає група (одразу / після N доль / за таймер) · колір (4 / 5).

## Цікавинки для курсу
- Шкала такту від BPM і перевірка «чи ввід у вікні долі» з трьома зонами (BEST / синя / чорна) — 🥉 (синхронізація з аудіо, допуски).
- Промах = фігура розсипається випадково по полю — 📎.
- Tsunagi Time: група блимає 4 долі, до неї приєднуються однокольорові, поки блимає — нема програшу — 🥉.
- Пошук групи 3+ по сторонах — 🌱.
- Jammers: зникають лише від сусідньої зачистки, попередження з числом, offset — 📎.
- CPU, що грає в ритм із «людськими» промахами за рівнем складності — 🥈.

## Мапа на каталог
- Є: `gravity-fall` · `multi-cell-size` · `piece-rotate-flip` · `next-queue` (4 фігури) · `simultaneous-versus` + `garbage-attack` · `ai-opponent` · `difficulty-levels` · `sequential-levels` (CPU-стадії) · `mode-select` · `tutorial-window` · `online-multiplayer` · `background-music` · `keyboard-controls` (Steam) · `end-screen`.
- **Нема** → пропозиції карток:
  - `+rhythm-gated-drop` «Хід приймається лише у вікні долі» · interface/input · 🥉 · слоти {zones: best|ok|miss}.
  - `+rhythm-sync-tempo` «Темп логіки від BPM треку» · game-logic/waves · 🥉 — як у Lumines.
  - `+timing-judgement-bonus` «Точність влучання в долю → бонус і сила атаки» · game-logic/score · 📎.
  - `+miss-scatter-penalty` «Промах розсипає фігуру випадково» · entities/move · 📎.
  - `+delayed-clear-window` «Збіг блимає N доль, його можна доростити» · game-logic/score · 🥉 — спільна з Trioncube.
  - `+no-lose-during-clear` «Поки йде зачистка, поразки нема» · game-logic/lose · 🌱.
  - `+connected-group-pop` (3+, 4-сусідство) · `+garbage-offset` · `+garbage-adjacent-clear` — як у Puyo.
  - `+song-select` «Вибір пісні = вибір темпу партії» · interface/menus · 🌱.

## Пропозиції до словників
- `+trigger:beat` — доля музики як подія (період задає аудіо, не годинник); підтверджую (NecroDancer).
- `+cond:on_beat` — ввід потрапив у вікно долі (тут ще й градація BEST); підтверджую.
- `+window:song-select` — вибір пісні перед партією; пісня задає темп правил.
- `+card:rhythm-gated-drop` · `+card:miss-scatter-penalty` · `+card:no-lose-during-clear` · `+card:delayed-clear-window` — див. «Мапа на каталог».

## Джерела
- ⭐ [JA Wikipedia: マジカルビート](https://ja.wikipedia.org/wiki/マジカルビート) — поле 6×9 + прихований ряд, L з 3 бітонів, 4/5 кольорів, 4 NEXT, збіг 3+, шкала синхронізації (синя / чорна / центр BEST), Tsunagi Time 4 долі, jammers і offset, режими, BPM пісень, дати.
- [Steam: MAGICAL BEAT](https://store.steampowered.com/app/3516620/MAGICAL_BEAT/) — PC-версія 2025: опис правил («badly timed drop breaks the block into pieces»), CHAIN time, 100+ треків, локальний PvP.
- YouTube: пошук «Magical Beat Vita gameplay».

## Непевне
- (?) Чи фігура падає сама (з таймером), чи висить над полем до скидання — джерела описують лише «рух, поворот, поставити».
- (?) Чи падають бітони після зачистки (осідання й ланцюги падіння) — JA згадує ланцюги, механіку не описує.
- (?) Ширина синьої зони, як вона залежить від BPM і складності — не знайдено.
- (?) Формула кількості jammers від очок — не знайдено.
- (?) Steam перелічує й локальний co-op — що це за режим, не перевірено.
