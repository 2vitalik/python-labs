---
title: ScaleBox
slug: scalebox
aka: []
family: push-slide
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2025
platforms: [Windows, web (itch, у розробці)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3528380/", best: true, note: "правило «сумарний розмір ящиків ≤ твого», крок = розмір, портали змінюють розмір; 8 розділів, 100 рівнів, підказки"}
  - {kind: itch, url: "https://eggnisi.itch.io/scalebox", note: "безкоштовна HTML5-версія (in development)"}
  - {kind: other, url: "https://steamcommunity.com/app/3528380/reviews/?browsefilter=toprated&l=english", note: "відгуки EN: портали, «вихід із порталу штовхає будь-що», точне заповнення цілей, undo"}
  - {kind: other, url: "https://steamcommunity.com/app/3528380/reviews/?browsefilter=toprated&l=schinese", note: "відгуки CN: розміри 4 і 9 клітин, чорна діра, різання/зʼєднання ящиків, підказки за часом"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=ScaleBox+sokoban+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, keyboard-controls, push-object, multi-cell-size, impassable-cells, all-on-targets, teleport, teleport-pair, undo-redo, restart-level, sequential-levels, level-select, achievements-window, +size-push-limit, +step-equals-size, +resize-portal, +portal-push-force, +portal-on-object, +exact-size-target, +timed-hint, +optional-challenges]
proposes: ["+cond:size_le", "+effect:push_group", "+axis:step-length", "+feature:timed-hint", "+card:size-push-limit", "+card:step-equals-size", "+card:resize-portal", "+card:portal-push-force"]
author: opus
date: 2026-11-09
---

# ScaleBox — Sokoban, де ти і ящики бувають 1×1, 2×2, 3×3: штовхаєш сумарно не більше за себе, а крок дорівнює твоєму розміру

## Суть
Гравець — квадрат розміру s×s, ящики — теж квадрати різних розмірів. Штовхнути можна будь-яку групу ящиків, якщо їхній **сумарний розмір не перевищує твій**; зате кожен крок переносить тебе на s клітин, тож великий гравець сильний, але неточний. **Портали** змінюють розмір гравця і ящиків (вхід малий — вихід великий і навпаки), а вихід із порталу дає поштовх, що зсуває будь-що. Мета рівня — заповнити всі цільові клітини ящиками **точно потрібного розміру**.

## Поле і час
- Квадратна сітка; і гравець, і ящики займають квадрат s×s (у відгуках — 1×1, 2×2, 3×3, 4×4; гравець — «4 або навіть 9 клітин»).
- Шари: підлога + цільові області + стіни + портали (на стінах і на ящиках) + рухомі квадрати.
- Хід = один ввід; світ без вводу стоїть. Великі рівні не вміщаються в екран — гравці просять зум/вільну камеру.
- Довжина кроку = розмір гравця; спосіб «зупинитись на клітину раніше» — впертись у перешкоду (відгуки: «block your movements 1 cell earlier»).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | size s (мін. 1×1) | крок 4 напрямки на s клітин; штовхає групу ящиків сумарного розміру ≤ s |
| Ящик | object | size k×k | зсувається від поштовху; проходить портали й змінює розмір |
| Ціль (клітини для ящика) | zone | розмір k×k | заповнюється лише ящиком того самого розміру |
| Портал (пара різних ширин) | terrain | ширина входу / виходу | вхід → вихід; розмір того, хто пройшов, стає шириною виходу |
| Портал на ящику | object | орієнтація | рухається з ящиком; ящик з порталом у інший портал — портал повертається |
| Стіна | static | — | непрохідна; упор, щоб зупинити великий крок |
| Чорна діра | static | — | важка перешкода; зрушує її лише поштовх із порталу (CN-відгук) (?) |
| «Пружна мотузка» | object | — | елемент рівня з CN-відгуку, механіка не описана (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(path_s_cells)` → ТО `move(player, dir)` на s клітин.
- КОЛИ `input(dir)` → ЯКЩО `custom: «на шляху перешкода раніше ніж за s клітин»` → ТО `custom: «гравець зупиняється впритул до неї»` (?).
- КОЛИ `contact(player, boxes)` → ЯКЩО `custom: «сумарна площа ящиків фронту ≤ площі гравця»` і `free(cells_behind)` → ТО `push` (усієї групи).
- КОЛИ `contact(player, boxes)` → ЯКЩО `custom: «сумарна площа більша»` → ТО `block`.
- КОЛИ `enter(player|box, portal_in)` → ЯКЩО `custom: «розмір сутності ≤ ширини порталу»` → ТО `teleport(a, portal_out)`, `grow(a, n)` або `shrink(a, n)` до ширини виходу.
- КОЛИ `contact(player, portal)` → ЯКЩО `custom: «гравець більший за портал»` → ТО `block`.
- КОЛИ `after(teleport)` → ТО `custom: «вихід із порталу штовхає все попереду незалежно від розміру»` (і чорну діру).
- КОЛИ `enter(box_with_portal, portal)` → ТО `rotate(portal, 90)` (?) — портал на ящику змінює орієнтацію.
- КОЛИ `all_on(box, target)` → ЯКЩО `fits(box, target)` (розмір збігається точно) → ТО `win`, `next_level`.
- КОЛИ `input(undo)` → ТО `undo(1)`; КОЛИ `input(restart)` → ТО `restart` (undo не сягає за рестарт).
- КОЛИ `counter(time_in_level, >=, n)` → ТО `custom: «відкривається підказка»` (час — (?)).
- Перемога: усі цілі заповнені ящиками точного розміру. · Поразка: нема; глухий кут → undo/рестарт. · Рахунку нема.

## Керування і ввід
- Стрілки / WASD — крок (з поштовхом); undo; рестарт (точні клавіші — (?)).
- Steam: повна підтримка контролера (DualShock, DualSense).

## Вікна, меню, HUD
- `main-menu`: Грати → `level-select` (8 розділів), налаштування, вихід; кнопка «повернутись до вибору рівня» в меню налаштувань (CN-відгук: не працювала).
- `level-select`: розділи з рівнями; основний маршрут + необовʼязкові важкі рівні.
- `game-screen`: поле з сіткою (лінії поділу на тлі), кнопка/вікно підказки після очікування.
- `hints-window` — підказка до рівня (?).
- `settings-window`, `achievements-window` (Steam, 10 досягнень).

## Фічі поза полем
- `levels-sequential` + `level-unlock`: 8 розділів, 100 рівнів; найважчі — необовʼязкові (`+optional-challenges`).
- `hint` з затримкою: підказка доступна лише після певного часу на рівні (`+feature:timed-hint`).
- `undo` + `restart-level`; `cloud-save`; `localization` (7 мов).

## Варіації й родичі
- [sokoban](sokoban.md) — ядро; [kwirk](kwirk.md) і [rush-hour](rush-hour.md) — блоки w×h, але гравець 1×1; [room-to-grow](room-to-grow.md) — аватар росте, але кроком; Parabox (thinky) — вхід у ящик змінює масштаб.
- Осі варіацій:
  - **сила поштовху**: 1 ящик (Sokoban) / ланцюг будь-якої довжини / сума розмірів ≤ власного (ScaleBox);
  - **довжина кроку**: 1 / до упору (ковзання) / рівно s клітин, упор зупиняє раніше (ScaleBox);
  - **зміна розміру**: нема / портал задає розмір виходом / рекурсивний масштаб (Parabox);
  - **ціль**: будь-який ящик на ціль / ящик точно свого розміру (ScaleBox).

## Цікавинки для курсу
- Колізія квадратів s×s на сітці й штовхання групи з підсумком площ фронту (рекурсивний збір ланцюга) — 🥉.
- Крок на s клітин зі зупинкою біля першої перешкоди — 📎.
- Портал, що масштабує сутність до ширини виходу, з перевіркою «влазить?» і перерахунком зайнятих клітин — 🥈.
- «Безмежна» сила поштовху з порталу як виняток із правила ваги — 📎.
- Перевірка перемоги «ціль заповнена ящиком точно того розміру» — 🌱.
- Розвʼязувач: стан = (позиція, розмір гравця) + множина ящиків з розмірами; простір росте від масштабу — 🥇.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls`; `push-object`; `multi-cell-size` ↔ квадрати s×s; `impassable-cells`; `all-on-targets` ↔ заповнити цілі; `teleport` + `teleport-pair` ↔ портали; `undo-redo` + `restart-level`; `sequential-levels` + `level-select`; `achievements-window`.
- **Нема** → пропозиції карток:
  - `+size-push-limit` «Штовхаєш групу, якщо сума розмірів ≤ твого» · entities/legality · 🥉 · слот {measure: area|count}.
  - `+step-equals-size` «Крок дорівнює розміру аватара» · entities/move · 📎.
  - `+resize-portal` «Портал змінює розмір того, хто пройшов» · entities/interact · 🥈 · слот {in_width, out_width}.
  - `+portal-push-force` «Вихід із порталу штовхає будь-що» · entities/interact · 📎.
  - `+portal-on-object` «Портал на рухомому ящику» · entities/interact · 🥉.
  - `+exact-size-target` «Ціль приймає лише ящик свого розміру» · game-logic/win · 🌱.
  - `+timed-hint` «Підказка відкривається після N часу на рівні» · game-logic/difficulty · 🌱.
  - `+optional-challenges` (уже в корпусі) — важкі рівні поза основним маршрутом.

## Пропозиції до словників
- `+cond:size_le` — розмір (площа) А ≤ розміру Б; правило ваги поштовху й проходу в портал.
- `+effect:push_group` — зсунути весь фронт ящиків як одне ціле (не ланцюг по одному).
- `+axis:step-length` — довжина кроку: `1` / `size` / `until-blocked`.
- `+feature:timed-hint` — підказка за таймером на рівні.
- `+card:size-push-limit`, `+card:step-equals-size`, `+card:resize-portal`, `+card:portal-push-force`.

## Джерела
- ⭐ [Steam: ScaleBox](https://store.steampowered.com/app/3528380/) — правило сумарного розміру, крок = розмір, портали, 8 розділів / 100 рівнів, підказки; реліз 19.06.2025, EGGNISI; контролер, 10 досягнень.
- [itch: ScaleBox](https://eggnisi.itch.io/scalebox) — HTML5-версія, Unity, без опису механік.
- [Steam-відгуки EN](https://steamcommunity.com/app/3528380/reviews/?browsefilter=toprated&l=english) — портали подвійної ширини, «exiting a portal… can push anything», обертання порталу ящиком, точне заповнення, undo не після рестарту.
- [Steam-відгуки CN](https://steamcommunity.com/app/3528380/reviews/?browsefilter=toprated&l=schinese) — гравець 4 і 9 клітин, чорна діра, різання/зʼєднання ящиків, підказки після очікування, пружна мотузка.
- YouTube: пошук «ScaleBox sokoban gameplay».

## Непевне
- (?) Межа поштовху: Steam — «total size does not exceed your own» (≤), відгук EN — «equal to your weight»; пишемо ≤ за сторінкою Steam.
- (?) Чи гравець при кроці на s клітин зупиняється біля перешкоди, чи крок блокується цілком — відгуки натякають на зупинку раніше.
- (?) Обертання порталу «ящик з порталом у інший портал» — з одного відгуку; кут і правило не перевірено.
- (?) Чорна діра, «різання й зʼєднання ящиків», пружна мотузка — лише згадки в CN-відгуках, механіка не описана.
- (?) Скільки часу треба чекати на підказку, вигляд вікна підказки, клавіші — не перевірено.
