---
title: SPIN Protocol
slug: spin-protocol
aka: [Spin Protocol]
family: connect-rotate
also: []
klass: cursor
axes:
  field: graph
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2025
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3342810/SPIN_Protocol/", best: true, note: "єдине перевірене джерело: обертання вузлів, кольорові сигнали без змішування й перетину, Fusion і Bridge вузли, ліміти часу й поворотів для perfect, 60+ рівнів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=SPIN+Protocol+gameplay", note: "пошук; геймплей (відео не відкривав)"}
  - {kind: itch, url: "https://itch.io/search?q=spin+protocol", note: "пошук; сторінка не відкрилась (522)"}
stage: v1
coverage: 50
mechanics: [tile-rotate, orientation-state, beam-tracing, cell-click, keyboard-controls, completion-detection, satisfy-constraints, sequential-levels, game-screen, end-screen, +beam-color-mix, +bridge-cell, +perfect-rating, +no-cross-signals, +rotation-limit, +gamepad-support]
proposes: ["+trigger:signal_arrive", "+cond:signal_color", "+effect:route_signal", "+effect:fuse_colors", "+card:no-cross-signals", "+card:rotation-limit"]
author: opus
date: 2026-11-09
---

# SPIN Protocol — обертай вузли, щоб кольорові сигнали дійшли до приймачів свого кольору, не змішавшись і не перетнувшись

## Суть
Пазл про маршрутизацію: на полі є джерела кольорових сигналів, вузли-перенаправлювачі й вузли-приймачі. Гравець лише обертає вузли (одна кнопка — один поворот), щоб кожен приймач отримав сигнал свого кольору. Сигнали різних кольорів не можна змішувати чи перетинати, тож очевидний маршрут часто хибний. Нові типи вузлів додаються з рівнями: Fusion (змішує два кольори в новий), Bridge (дає двом сигналам перетнутися без взаємодії) та інші (?).

## Поле і час
- Поле — 2D-схема вузлів; чи це строга квадратна сітка, джерело не каже (`graph` — обережно, див. «Непевне»).
- Час: пазл без тиску; таймер і лічильник поворотів важать лише для perfect-оцінки.
- Шари: вузли (тип + орієнтація) + сигнали, що трасуються від джерел після кожного повороту (?).
- Понад 60 рівнів зростаючої складності.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Джерело сигналу | source | колір | випускає сигнал свого кольору (?) |
| Звичайний вузол | conduit | орієнтація | поворот на крок змінює, куди йде сигнал |
| Fusion Node | conduit | 2 входи | два сигнали різних кольорів дають сигнал нового кольору |
| Bridge Node | conduit | — | два сигнали проходять навхрест, не взаємодіючи |
| Receiver Node | sink | потрібний колір | активується, коли отримує сигнал саме свого кольору |
| Інші вузли | conduit | — | «much, much more» — не перелічено (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(rotate node)` → ТО `rotate(node, step)`, `counter(rotations, +1)`.
- КОЛИ `after(rotate)` → ТО `custom: «перетрасувати всі сигнали від джерел через вузли»` (+effect:route_signal) (?).
- КОЛИ `custom: «сигнал входить у Fusion разом з іншим кольором»` → ТО `custom: «вихід — змішаний колір»` (+effect:fuse_colors).
- КОЛИ `custom: «два сигнали в Bridge»` → ТО `custom: «кожен іде прямо, без взаємодії»`.
- КОЛИ `custom: «сигнали різних кольорів зустрічаються поза Bridge/Fusion»` → ТО `custom: «конфлікт — рішення не зараховується»` (?).
- КОЛИ `custom: «сигнал дійшов до приймача»` (+trigger:signal_arrive) → ЯКЩО `custom: «колір сигналу = колір приймача»` (+cond:signal_color) → ТО `set_state(receiver, active)`.
- КОЛИ `all_constraints_met` (усі приймачі активні правильним кольором) → ТО `win`, `window(end-screen)`.
- КОЛИ `level_end` → ЯКЩО `timer(<=, limit)` and `counter(rotations, <=, limit)` → ТО `custom: «perfect score»`.
- Перемога: усі приймачі активні · Поразка: нема · Рахунок: perfect за час і кількість поворотів.

## Керування і ввід
- Обрати вузол і повернути його однією кнопкою.
- Миша, клавіатура або контролер.

## Вікна, меню, HUD
- `game-screen`: поле вузлів, сигнали, приймачі; лічильник поворотів і таймер (?).
- `end-screen`: результат рівня, позначка perfect (?).
- `main-menu`, `level-select`, `settings-window` (мова) — ймовірно, не перевірено (?).

## Фічі поза полем
- `levels-sequential` (60+ рівнів), нові вузли з прогресом.
- `achievements` (Steam), `cloud-save` (Steam Cloud), `localization` (EN, ES).
- `gamepad-support`, `mouse-and-keyboard`.

## Варіації й родичі
- У сімʼї: [infinity-loop](infinity-loop.md) (обертання плиток до замкнення), [chromatron](chromatron.md) і [octopticom](octopticom.md) (змішування кольорів променя), [flow-free](flow-free.md) (кольори не перетинаються, мости), [pipe-mania](pipe-mania.md).
- **Осі варіацій**: ввід (поворот вузла / перестановка / малювання шляху) · кольори (один / кілька без змішування / змішування у Fusion) · перетин (заборонено / дозволено лише в мостах) · оцінка (просто розвʼязати / perfect за час і кількість поворотів).

## Цікавинки для курсу
- Обертання вузла і перетрасування сигналів від джерел — 📎.
- Кольори з правилом «не змішувати, не перетинати» + міст як виняток — 🥉.
- Fusion: таблиця змішування кольорів і вихід нового сигналу — 📎.
- Perfect за ліміт поворотів: потрібен підрахунок мінімуму (BFS по станах орієнтацій) — 🥇.

## Мапа на каталог
- Є: `tile-rotate` · `orientation-state` · `beam-tracing` (сигнал як промінь по вузлах) · `cell-click` · `keyboard-controls` · `completion-detection` · `satisfy-constraints` · `sequential-levels` · `game-screen` · `end-screen`.
- Повтор чужих пропозицій: `+beam-color-mix` (Chromatron), `+bridge-cell` (Flow Free), `+perfect-rating` (Flow Free).
- **Нема** → пропозиції карток:
  - `+no-cross-signals` «Сигнали різних кольорів не перетинаються й не змішуються» · game-logic/constraints · 📎.
  - `+rotation-limit` «Ліміт поворотів для найкращої оцінки» · game-logic/score · 🌱.
  - `+gamepad-support` «Керування геймпадом» · interface/input · 📎.

## Пропозиції до словників
- `+trigger:signal_arrive(a, receiver)` — сигнал/потік дійшов до приймача.
- `+cond:signal_color(a, c)` — колір сигналу, що прийшов, дорівнює c.
- `+effect:route_signal` — перетрасувати сигнали від джерел після зміни поля.
- `+effect:fuse_colors(a, b → c)` — два сигнали дають сигнал нового кольору.

## Джерела
- ⭐ [Steam: SPIN Protocol](https://store.steampowered.com/app/3342810/SPIN_Protocol/) — опис: обертання вузлів, Receiver/Fusion/Bridge, без змішування й перетину, ліміти часу й поворотів, 60+ рівнів, миша/клавіатура/контролер, досягнення, Steam Cloud; розробники Diego і Sebastian Spartano, 31.01.2025.

## Непевне
- (?) Геометрія поля (квадратна сітка чи граф вузлів), крок повороту (90°?), вигляд джерел — у джерелі нема.
- (?) Що саме буває при зустрічі різних кольорів поза мостом — заборона ходу, конфлікт чи просто нерозвʼязаний стан.
- (?) Інші типи вузлів («much, much more») — не перелічені.
- (?) Вікна: меню, вибір рівня, налаштування — не бачив, за аналогією з жанром.
- (?) Undo, підказки — сторінка не згадує.
