---
title: Sim (гра олівцем на K6)
slug: sim-pencil-game
aka: [Game of Sim, SIM]
family: connect-rotate
also: [chess-abstract]
klass: cursor
axes:
  field: graph
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: survive
year: 1969
platforms: [paper, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Sim_(game)", best: true, note: "правила на K6, R(3,3)=6 — нічиєї нема, виграє другий (перебір 1974), Ramsey-варіанти на 17 і 18 вершинах"}
  - {kind: other, url: "https://arxiv.org/abs/2001.04024", note: "Wrzos-Kaminska 2020: проста людська виграшна стратегія другого гравця (абстракт)"}
  - {kind: other, url: "https://arxiv.org/abs/cs/9911004", note: "Slany 1999: graph Ramsey games — avoidance / avoidance+ / achievement, PSPACE-повнота"}
  - {kind: other, url: "https://dx.doi.org/10.2307/2688046", note: "Mead, Rosa, Huang 1974: виграш другого (лише бачив у Wikipedia)"}
  - {kind: play, url: "https://share.catrob.at/pocketcode/program/1478", note: "застосунок Pocket Code — гра проти смартфона, з кодом (лише бачив у Wikipedia)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Sim+pencil+game+K6+triangle", note: "пошук; пояснення й партії"}
stage: v1
coverage: 65
mechanics: [hot-seat, turn-enforcement, ai-opponent, ai-random, ai-minimax, cell-click, hover-highlight, last-move-highlight, conflict-highlight, remaining-counter, game-screen, end-screen, match-setup, help-window, rule-variants, +edge-claim, +monochromatic-clique-check, +avoidance-goal]
proposes: ["+cond:mono_clique(k, color)", "+role:node", "+role:edge", "+axis:goal=avoid", "+card:monochromatic-clique-check", "+card:avoidance-goal"]
author: opus
date: 2026-11-09
---

# Sim — двоє фарбують ребра K6; хто першим замкне трикутник свого кольору, той програв

## Суть
Шість точок, кожна пара зʼєднана відрізком — повний граф K6 з 15 ребрами. Гравці по черзі фарбують по одному вільному ребру своїм кольором; хто першим утворить трикутник зі своїх ребер (вершини — три з шести точок), **програє**. Нічиєї не буває: число Рамсея R(3,3)=6 гарантує, що будь-яке двоколірне фарбування K6 містить одноколірний трикутник. Гра Gustavus Simmons (1969) — найкоротший місток від «пограти олівцем» до теорії Рамсея й повного перебору: за ідеальної гри виграє другий.

## Поле і час
- Поле `graph`: 6 вершин, 15 ребер; ребро має 3 стани — вільне / колір першого / колір другого.
- Перетини відрізків на папері не рахуються: трикутник складають лише три вершини K6.
- Покроково, хід = одне ребро. Ребер 15, тож партія не довша за 15 ходів; закінчується, щойно склався перший одноколірний трикутник.
- Інформація повна, випадковості нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вершина | node (custom) | 6 шт. | нерухомі кінці ребер |
| Ребро вільне | edge (custom) | пара вершин | гравець, чий хід, може зафарбувати |
| Ребро зафарбоване | mark | колір власника | незмінне до кінця партії |
| Одноколірний трикутник | zone | колір | поява = поразка власника кольору |
| Гравець | player | колір; перший / другий | ходять по черзі; другий має виграшну стратегію |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, edge)` → ЯКЩО `turn_of(side)` and `state(edge, free)` → ТО `paint(edge, color(side))`, `end_turn`.
- КОЛИ `input(click, edge)` → ЯКЩО `not state(edge, free)` → ТО `block`.
- КОЛИ `turn_end(side)` → ЯКЩО `custom: «нове ребро (u, v) і ребра (u, w), (v, w) для якоїсь w — усі кольору side»` → ТО `lose(side)`, `window(end-screen)`.
- Перевірка після ходу локальна: досить 4 трійок (нове ребро + кожна з 4 інших вершин), а не всіх 20 трикутників K6.
- Нічия: КОЛИ `custom: «усі 15 ребер зафарбовано»` — без трикутника не настає (R(3,3)=6), тож ефекту `draw` у грі нема.
- Стратегія: за ідеальної гри виграє другий (Mead, Rosa, Huang 1974 — комп'ютерний перебір); проста людська стратегія другого — Wrzos-Kaminska 2020.
- Варіант avoidance+: за хід можна зафарбувати більше одного ребра.
- Варіант R(4,4)=18: 18 вершин, 153 ребра; програє той, хто зафарбує своїм кольором усі 6 ребер якоїсь четвірки вершин (K4).
- Варіант R(3,3,3)=17: 17 вершин, 3 кольори; троє гравців або двоє, кожен на хід обирає один із трьох кольорів.
- Achievement-варіант: КОЛИ `custom: «склалася одноколірна копія заданого графа A»` → ТО `win(side)` замість `lose(side)`.
- Перемога: суперник замкнув трикутник свого кольору · Поразка: свій трикутник · Рахунку нема.

## Керування і ввід
- Папір: два олівці різних кольорів; шість точок зазвичай ставлять шестикутником.
- Цифрова версія: клік / тап по відрізку; ребро під курсором підсвічується (`hover-highlight`); влучання — найближчий відрізок до точки кліку.
- Проти AI (застосунок Pocket Code): гравець ходить, смартфон відповідає своїм ребром.

## Вікна, меню, HUD
- (цифрова версія) `main-menu` → `match-setup` (людина / AI, хто першим, варіант K6 / K17 тріколор / K18) → `game-screen` → `end-screen`.
- `game-screen`: 6 точок і 15 відрізків; `turn-indicator` — колір того, хто ходить; `last-move-highlight` — останнє ребро суперника; `remaining-counter` — вільних ребер.
- `end-screen`: підсвічений трикутник програвшого (`conflict-highlight`), «нова партія» / «помінятися сторонами».
- `help-window` — правила одним абзацом.
- Переходи: match-setup → game-screen → (трикутник) end-screen → match-setup.

## Фічі поза полем
- `hotseat` — папір або один екран на двох.
- `ai-opponent-levels`: випадковий / жадібний («не замикай свій трикутник, не давай собі пасток») / ідеальний (таблиця перебору).
- `custom-rules`: кількість вершин, кольорів, заборонена фігура (K3, K4), avoidance ↔ achievement, кілька ребер за хід.

## Варіації й родичі
- Ramsey-ігри на графах (Slany 1999): avoidance — склав фігуру, програв; avoidance+ — кілька ребер за хід; achievement — склав фігуру, виграв. Загальні випадки PSPACE-повні.
- Корпус: [Shannon switching / Bridg-It](shannon-switching.md) — теж захоплення ребер графа, але мета — звʼязати термінали; [Hackenbush](hackenbush.md) — ребра стирають, а не фарбують; [Black Path Game](black-path-game.md) — теж misère: хто виведе шлях у край, програв.
- Осі варіацій: **мета** — уникнути фігури / скласти фігуру / звʼязати термінали · **фігура** — K3 / K4 / довільний граф A · **кольорів** — 2 / 3 · **ребер за хід** — 1 / кілька · **поле** — K6 / K17 / K18.

## Цікавинки для курсу
- Локальна перевірка трикутника після ходу (4 трійки біля нового ребра) — 🌱: найпростіша перевірка «склався шаблон» на графі.
- Клік по відрізку: відстань від точки до відрізка, вибір найближчого ребра — 📎.
- AI-евристика: оцінка ребра за кількістю «своїх» пар, яким бракує третього ребра — 📎.
- Повний розвʼязувач: minimax з мемоізацією, стан — 15 ребер × 3 стани (3^15 ≈ 14,3 млн) — 🥈; зі зведенням за симетріями шести вершин (720 перестановок) — 🥇.
- Конструктор Ramsey-ігор (n вершин, k, кольори, avoidance / achievement) на одному двіжку — 🥉.
- Наочне R(3,3)=6: на K5 є фарбування без трикутника (пʼятикутник одним кольором, зірка іншим), на K6 — нема — 📎.

## Мапа на каталог
- Є: `hot-seat` ↔ двоє за папером / екраном; `turn-enforcement`; `ai-opponent` + `ai-random` + `ai-minimax` ↔ рівні AI; `cell-click` ↔ клік по ребру; `hover-highlight`; `last-move-highlight`; `conflict-highlight` ↔ підсвічений трикутник; `remaining-counter` ↔ вільні ребра; `game-screen`, `end-screen`, `match-setup`, `help-window`; `rule-variants` ↔ K6 / K17 / K18, avoidance / achievement.
- **Нема** → пропозиції карток:
  - `+edge-claim` (вже з Shannon) — фарбування ребра графа своїм кольором; підтвердження.
  - `+monochromatic-clique-check` «Одноколірна кліка у фарбуванні ребер» · game-logic/win · 🌱 · слот {k: 3|4}.
  - `+avoidance-goal` «Мета-уникання: склав фігуру — програв» · game-logic/win · 🌱.

## Пропозиції до словників
- `+cond:mono_clique(k, color)` — серед ребер кольору є повний підграф K_k (Sim: k=3; варіант R(4,4): k=4).
- `+role:node` / `+role:edge` — вершина й ребро як сутності поля `graph` (підтвердження: Shannon, Hackenbush).
- `+axis:goal=avoid` — мета «не скласти заборонену фігуру» (misère: Sim, Black Path Game).
- `+card:monochromatic-clique-check`, `+card:avoidance-goal`.

## Джерела
- ⭐ [Wikipedia: Sim (game)](https://en.wikipedia.org/wiki/Sim_(game)) — правила, R(3,3)=6 і неможливість нічиєї, виграш другого (1974), стратегія 2020, варіанти: кілька ребер за хід, K18 / R(4,4), три кольори / R(3,3,3)=17, застосунок Catrobat.
- [arXiv 2001.04024](https://arxiv.org/abs/2001.04024) — «A simpler winning strategy for Sim»: проста людська стратегія другого (лише абстракт).
- [arXiv cs/9911004](https://arxiv.org/abs/cs/9911004) — Slany, «Graph Ramsey games»: avoidance / avoidance+ / achievement, PSPACE-повнота, Erdős–Selfridge.
- [Mead, Rosa, Huang 1974](https://dx.doi.org/10.2307/2688046) — «The Game of Sim: A Winning Strategy for the Second Player» (посилання з Wikipedia, не відкривав).
- [Pocket Code: Sim](https://share.catrob.at/pocketcode/program/1478) — цифрова версія проти смартфона (посилання з Wikipedia, не відкривав).

## Непевне
- (?) Правило avoidance+ (скільки ребер за хід і хто вирішує) — Wikipedia лише згадує «більше одного ребра за хід».
- (?) Вікна й рівні AI — «(цифрова версія)», жодної цифрової версії не відкривав.
- (?) Скільки правил і розборів у людській стратегії Wrzos-Kaminska — бачив лише абстракт.
- (?) Розміщення точок шестикутником — звичай, у джерелах не сказано.
