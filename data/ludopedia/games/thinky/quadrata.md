---
title: Quadrata
slug: quadrata
aka: []
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: collect
year: 2022
platforms: [PC, Mac, Linux, iOS, Android]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2066950/Quadrata/", best: true, note: "опис: два персонажі однією клавіатурою, діаманти за ліміт ходів, портали, трикутники, 90 рівнів, 8 механік, undo, редактор; реліз 10.10.2022"}
  - {kind: steam, url: "https://store.steampowered.com/app/2086310/Quadrata_Demo/", note: "безкоштовне демо, 25.07.2022"}
  - {kind: official, url: "https://mindlabor.dev/quadrata/", note: "сайт Mindlabor: лінки на Steam, Google Play, App Store, трейлер, прес-кіт"}
  - {kind: itch, url: "https://mindlabor.itch.io/quadrata", note: "itch-сторінка: Unity, textless, color-blind friendly"}
  - {kind: other, url: "https://steamcommunity.com/app/2066950/reviews/?browsefilter=toprated", note: "відгуки: ковзання до упору, точний ліміт ходів, автоперезапуск, червоний трикутник, реверс"}
  - {kind: other, url: "https://apps.apple.com/us/app/quadrata/id6751172223", note: "iPad-версія 2.0 (2025)"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=z8AaOkMErAQ", note: "трейлер (лінк з офіційного сайту)"}
stage: v1
coverage: 50
mechanics: [move-4dir, move-by-input, keyboard-controls, inertia-slide, impassable-cells, item-pickup, collect-all, move-limit, teleport, teleport-pair, touch-death, sequential-levels, undo-unlimited, restart-level, in-game-editor, background-music, +multi-agent-sync, +split-boards-one-input, +reversed-input-zone, +exact-move-budget, +auto-restart-on-budget, +textless-teaching]
proposes: ["+axis:control", "+ui:split-screen", "+feature:procedural-music", "+card:split-boards-one-input"]
author: opus
date: 2026-11-09
---

# Quadrata — два квадрати на двох половинах екрана ковзають від одного натиску; збери діаманти обох полів за точну кількість ходів

## Суть
Мінімалістична пазл-гра Mindlabor: екран розділено на два поля, на кожному свій квадрат. **Одна клавіша напрямку рухає обидва**, і кожен ковзає до стіни чи іншої твердої перешкоди. Треба зібрати сині діаманти на обох полях, маючи рівно стільки ходів, скільки в оптимальному розвʼязку. Нова механіка — приблизно кожні 10 рівнів (портали, червоні трикутники, «реверс» тощо); тексту й туторіалів нема.

## Поле і час
- Два квадратні поля поруч (ліве й праве), кожне зі своїми стінами, діамантами й обʼєктами; розміри — (?).
- Покроково: хід = один натиск напрямку; обидва квадрати ковзають одночасно, кожен до своєї перешкоди.
- Лічильник ходів на рівень; коли ходи скінчились без перемоги — рівень перезапускається сам.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Лівий квадрат | player | поле L | ковзає в напрямку вводу до перешкоди |
| Правий квадрат | player | поле R | той самий ввід, своє поле; при «реверсі» — дзеркальний напрям (?) |
| Стіна | static | — | зупиняє ковзання («use walls to your advantage») |
| Діамант (синій) | pickup | — | збирається квадратом; зібрати всі на обох полях |
| Портал | gate | пара | переносить квадрат («teleport using portals») |
| Трикутник (червоний) | hazard | — | «stay away from triangles!»; поведінка — (?) |
| Реверс-механіка | zone | — | відгук: «keep on mistaking left and right» — інвертує ліво/право для одного з квадратів (?) |
| Лічильник ходів | mark | рівно оптимум | 0 без перемоги → автоперезапуск |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `slide(square_L, dir)`, `slide(square_R, dir)`, `counter(moves, -1)`.
- КОЛИ `input(dir)` → ЯКЩО `state(square, reversed)` → ТО `mirror_input`, `slide(square, mirrored_dir)` (?).
- КОЛИ `blocked(square)` → ТО `custom: «квадрат стоїть, другий їде далі»` (?).
- КОЛИ `contact(square, diamond)` → ТО `pickup`, `counter(diamonds, -1)`.
- КОЛИ `enter(square, portal)` → ТО `teleport(square, pair)`.
- КОЛИ `contact(square, triangle)` → ТО `custom: «провал спроби»` (?).
- КОЛИ `counter(diamonds, =, 0)` → ТО `win`, `next_level`.
- КОЛИ `counter(moves, =, 0)` → ЯКЩО `count(diamond, >, 0)` → ТО `restart`.
- КОЛИ `input(undo)` → ТО `undo(1)`. КОЛИ `input(R)` → ТО `restart`.
- Перемога: зібрано всі діаманти обох полів. · Поразка: ходи вичерпано (автоперезапуск); трикутник (?). · Рахунку нема.

## Керування і ввід
- 4 напрямки: клавіатура, геймпад, миша або дотик (кожен — «only option» на Steam); одна команда на обидва поля.
- Undo без ліміту; R — ручний рестарт.

## Вікна, меню, HUD
- `game-screen`: два поля поруч (`+ui:split-screen`), `move-counter`.
- `level-select` (?): 90 рівнів групами по механіках.
- `editor-window` — вбудований редактор рівнів (Steam: «Includes level editor»).
- `settings-window`: гучність; HDR (за відгуком).
- Інтерфейс без тексту (textless).

## Фічі поза полем
- `levels-sequential` — 90 рівнів, нова механіка кожні ~10.
- `undo` ∞, `restart-level`, автоперезапуск на вичерпаних ходах.
- `level-editor`; `achievements` (15 за відгуком); `cloud-save`, `gamepad-support`, `touch-controls`.
- `+feature:procedural-music` — неповторна процедурна музика (Emre Akdeniz).
- Мобільна версія 2.0 (iPad / Android, 2025).

## Варіації й родичі
- [Ice-sliding puzzles](../push-slide/ice-sliding-puzzles.md) — базове ковзання до упору; тут його подвоєно одним вводом.
- [SUMOO](../push-slide/sumoo.md) — та сама студія (Duck Tile / Mindlabor): один натиск — усе ковзає.
- [RE:COPY](recopy.md) і [Order of the Sinking Star](order-of-the-sinking-star.md) — інші випадки «один ввід — кілька акторів» (`+multi-agent-sync`).
- **Осі варіацій:** скільки полів (одне з двома акторами / два поля) · спільний ввід (тотожний / дзеркальний «реверс») · ліміт ходів (нема / точний оптимум) · кінець спроби (поразка / автоперезапуск).

## Цікавинки для курсу
- Ковзання до упору для двох акторів на двох полях одним вводом — 🌱.
- Портали в ковзанні (вихід продовжує рух?) і дзеркальний ввід для одного поля — 📎.
- Точний бюджет ходів і автоперезапуск — 🌱.
- Розвʼязувач BFS по парах позицій + множинах зібраних діамантів — 🥉; перевірка, що оптимум рівно дорівнює бюджету, — для редактора рівнів 🥈.

## Мапа на каталог
- Є: `move-4dir`, `move-by-input`, `keyboard-controls`; `inertia-slide` ↔ ковзання; `impassable-cells` ↔ стіни; `item-pickup` + `collect-all` ↔ діаманти; `move-limit` ↔ бюджет; `teleport`, `teleport-pair` ↔ портали; `touch-death` ↔ трикутник (?); `sequential-levels`, `undo-unlimited`, `restart-level`, `in-game-editor`, `background-music`.
- **Нема** → пропозиції карток:
  - `+split-boards-one-input` «Два поля, один ввід» · entities/move · 📎 · слоти {mirror: bool}.
  - `+multi-agent-sync` (уже пропонувалась) — кілька акторів одним вводом.
  - `+reversed-input-zone` «Ліво/право інвертовано для одного актора» · entities/move · 🌱.
  - `+exact-move-budget` «Бюджет = оптимум» і `+auto-restart-on-budget` · game-logic · 🌱.
  - `+textless-teaching` «Механіки вчать рівні, без тексту» · подача · 🌱.

## Пропозиції до словників
- `+axis:control` — значення `broadcast`: один ввід розсилається всім акторам (повтор).
- `+ui:split-screen` — кілька полів на одному екрані (повтор).
- `+feature:procedural-music` — процедурна неповторна музика.
- `+card:split-boards-one-input` — див. вище.

## Джерела
- ⭐ [Steam: Quadrata](https://store.steampowered.com/app/2066950/Quadrata/) — «control two different characters with the same keys on either side and collect diamonds with a limited number of moves», стіни, портали, «Stay away from triangles!», 90 рівнів, 8 механік, нова кожні 10, undo ∞, процедурна музика, редактор; Mindlabor, 10.10.2022.
- [Steam-відгуки](https://steamcommunity.com/app/2066950/reviews/?browsefilter=toprated) — «won't stop until they hit a wall or another solid object», «exactly the amount of moves for a perfect solution», автоперезапуск, R, червоний трикутник «hard to predict», реверс «mistaking left and right», без тексту.
- [Steam: демо](https://store.steampowered.com/app/2086310/Quadrata_Demo/) — 25.07.2022.
- [itch](https://mindlabor.itch.io/quadrata), [App Store](https://apps.apple.com/us/app/quadrata/id6751172223) (розробник Alperen Guner, v2.0 від 21.08.2025), [офіційний сайт](https://mindlabor.dev/quadrata/).

## Непевне
- (?) Повний перелік 8 механік (RAWG пише 10) — названі лише стіни, портали, трикутники, реверс і «кольорові» механіки.
- (?) Що робить червоний трикутник: убиває / рухається / зупиняє — відгук каже лише, що його положення важко передбачити.
- (?) Як працює реверс (для якого квадрата, постійно чи на клітині) і чи вихід з порталу продовжує ковзання.
- (?) Чи може рухатись один квадрат, коли другий одразу впирається (ймовірно так), і чи діамант зупиняє ковзання.
- (?) Один відгук каже про 80 рівнів, офіційно — 90.
