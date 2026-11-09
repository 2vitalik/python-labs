---
title: Trioncube
slug: trioncube
aka: [気持ちよさ連鎖パズル トリオンキューブ, Kimochiyosa Rensa Puzzle Trioncube]
family: falling-match
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: race
year: 2006
platforms: [Nintendo DS]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/気持ちよさ連鎖パズル_トリオンキューブ", best: true, note: "JA: 5 видів фігур з 3 клітин, тріон 3×3, стан ланцюга і три умови його кінця"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Trioncube", note: "тріміно, кінець комбо, корабель Penko, 45 рівнів Story, Arcade, Endless, VS"}
  - {kind: other, url: "https://game.watch.impress.co.jp/docs/20060707/trion.htm", note: "Game Watch (JA): ланцюг триває, поки є нові тріони; блоки ланцюга стають монетами"}
  - {kind: other, url: "https://worthplaying.com/article/2007/4/6/reviews/41096-nds-review-trioncube/", note: "огляд: нові квадрати можуть брати вже засвічені клітини, очки ростуть експоненційно, junk-блоки"}
  - {kind: other, url: "https://gamevortex.com/gamevortex/soft_rev.php/3455", note: "огляд: поле лише на нижньому екрані, монети бронза/срібло/золото/діамант, D-pad + одна кнопка"}
  - {kind: other, url: "https://www.pocketgamer.com/trioncube/review/", note: "огляд: чорні блоки не починають ланцюг, режими"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Trioncube+DS+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [multi-cell-size, piece-rotate-flip, combo-multiplier, event-points, time-out, sequential-levels, mode-select, tutorial-window, simultaneous-versus, garbage-attack, ai-opponent, end-screen, +filled-square-detect, +delayed-clear-window, +overlapping-square-reuse, +chain-converts-to-coins, +distance-race-meter, +skin-unlock-progression, +chain-start-blocker]
proposes: ["+trigger:pattern(square)", "+card:filled-square-detect", "+card:delayed-clear-window", "+card:overlapping-square-reuse", "+card:distance-race-meter"]
author: opus
date: 2026-11-09
---

# Trioncube — тріміно складають квадрати 3×3; ланцюг квадратів росте, поки встигаєш, і зникає лише наприкінці

## Суть
Падаюча головоломка Namco Bandai для DS: зверху падають фігури з трьох клітин (5 видів), і мета — не ряди, а **заповнений квадрат 3×3** («тріон»). Перший тріон вмикає стан ланцюга: кожна наступна фігура, що утворює новий тріон (можна з уже засвічених клітин), продовжує його. Ланцюг обривається, коли минув час від останнього тріону або фігура не дала нового — тоді всі засвічені блоки зникають і стають монетами, а очки ростуть експоненційно від кількості квадратів.

## Поле і час
- Поле («bin») — лише на нижньому екрані; верхній показує корабель-пінгвіна Penko, що летить швидше від ланцюгів. Праворуч від поля — шкала пройденої відстані.
- Real-time падіння фігур; стан ланцюга — окреме вікно часу після кожного нового тріону.
- Story / Arcade: дістатись до цілі, доки не скінчився таймер рівня (часом — наввипередки з іншим кораблем).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фігура-тріміно | player | 3 клітини, 5 видів | падає, зсувається, обертається за командою |
| Блок | tile | — | клітина стеку; частина тріону, якщо квадрат 3×3 заповнено |
| Тріон | zone | 3×3, засвічений (блимає) | вмикає/продовжує ланцюг; його клітини можна брати в нові тріони |
| Чорний блок | hazard | — | не може бути частиною тріону, що *починає* ланцюг |
| Junk-блок | hazard | місія / VS | сміття, яке кидає суперник або місія |
| Монета | pickup | бронза / срібло / золото / діамант | лишається від блоків завершеного ланцюга; ранг — за кількістю тріонів, діамант — якщо весь bin заповнено одним ланцюгом |
| Корабель Penko | player | мета-шар: відстань | летить уперед на величину завершеного ланцюга |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `free(cells_below)` → ТО `move(piece, down)`.
- КОЛИ `input(shift)` → ЯКЩО `free(target_cells)` → ТО `move(piece, dir)`; КОЛИ `input(rotate)` → ЯКЩО `free(new_cells)` → ТО `rotate(piece, 90)`.
- КОЛИ `locked(piece)` → ЯКЩО `custom: «pattern(square) — квадрат 3×3 повністю заповнено блоками»` і `not state(game, chain)` → ТО `set_state(trion, glowing)`, `set_state(game, chain)`, `timer(start)`.
- КОЛИ `custom: «pattern(square)»` → ЯКЩО `not state(game, chain)` і `count(black_in_square, >, 0)` → ТО ланцюг не починається.
- КОЛИ `locked(piece)` → ЯКЩО `state(game, chain)` і `custom: «утворено новий 3×3, можна з уже засвічених клітин»` → ТО `set_state(trion, glowing)`, `combo(+1)`, `timer(start)` (вікно відлічується знову).
- КОЛИ `locked(piece)` → ЯКЩО `state(game, chain)` і нового тріону нема → ТО `clear_state(game, chain)`.
- КОЛИ `timer(chain_window)` минув після останнього тріону → ТО `clear_state(game, chain)`.
- КОЛИ `locked(piece)` → ЯКЩО `custom: «клітини фігури виходять за нижній край нижнього екрана»` → ТО `clear_state(game, chain)` (третя умова JA).
- КОЛИ `state_off(game, chain)` → ТО `clear(all_glowing)`, `score(n)` — росте експоненційно з кожним тріоном ланцюга; `spawn_at(coin, cleared_cells)`.
- КОЛИ `state_off(game, chain)` → ТО `custom: «Penko просувається на відстань, що залежить від розміру ланцюга»`.
- КОЛИ `counter(distance, >=, goal)` → ТО `win`, `next_level`; КОЛИ `timer(level, ==, 0)` → ТО `lose`.
- КОЛИ `state_off(game, chain)` → ЯКЩО `mode(versus)` → ТО `send_garbage(junk)` — обмежене кидання junk-блоків супернику.
- Місії Story: «ланцюгами набрати відстань» / «ланцюгами завдати шкоди» / скорочене вікно між тріонами / junk-блоки.
- Перемога: дійти до цілі за таймер (Story, Arcade) · Поразка: таймер рівня вичерпано · Рахунок: очки за блоки ланцюга, експоненційно від кількості тріонів (Endless).

## Керування і ввід
- Хрестовина — зсув і прискорення; одна кнопка — поворот фігури. Стилус — лише в меню.
- Гравець вирішує, коли «закрити» ланцюг: свідомо не робити нового тріону — і засвічене зникне.

## Вікна, меню, HUD
- `main-menu`: Story · Arcade · Endless · VS · Tutorial · колекція (монети → фони й звуки розбиття).
- `game-screen`: нижній екран — поле, `progress-bar` відстані праворуч від поля, `timer-countdown` рівня, `score`; верхній — Penko, `custom: «підсвітка тріонів, що блимають»`.
- `level-select` Story: 45 місій з цілями; час проходження оцінюється золотом/сріблом/бронзою.
- `end-screen` місії з часом і медаллю; `custom-window` колекції: що відкрито за монети.
- VS: `lobby-window` DS Download Play — один картридж на двох, до 4 гравців з кількома картриджами; Wi-Fi нема.
- `tutorial-window` — окремий режим навчання.

## Фічі поза полем
- `mode-classic` (Story, 45 місій із сюжетом) · Arcade (вісім планет і бос) · `mode-endless` (99 рівнів на очки) · `mode-versus` (CPU або люди, race-режим).
- `stars-rating` — медалі за час кожної місії.
- `unlockables`: монети з ланцюгів відкривають фони й звуки розбиття.
- `local-multiplayer` через Download Play; онлайн нема.

## Варіації й родичі
- [lumines](lumines.md) і [puzzle-scape](puzzle-scape.md) — квадрати 2×2 одного кольору; тут квадрат 3×3 без кольору, перекриття дозволене.
- [tetris](tetris.md) — та сама подача фігур, але ціль — квадрат, а не ряд.
- [magical-beat](magical-beat.md) — те саме «вікно до зникнення» (4 долі такту), у яке можна доростити групу.
- **Осі варіацій**: ціль (ряд / квадрат N×N / група кольору) · коли зникає (одразу / після вікна часу / коли гравець закриє ланцюг) · перекриття (клітина в одному квадраті / у кількох) · куди йде ланцюг (очки / сміття / відстань корабля).

## Цікавинки для курсу
- Пошук усіх заповнених квадратів 3×3, включно з тими, що перекривають уже засвічені — 📎 (вікно 3×3 по сітці).
- Стан ланцюга з таймером, що скидається кожним новим квадратом, і зникнення всього наприкінці — 🥉 (стан-машина «нема → ланцюг → зачистка»).
- Чорний блок, що забороняє лише *перший* квадрат — 🌱 (умова залежить від стану).
- Експоненційні очки + монети-ранги (бронза/срібло/золото/діамант за весь bin) — 📎.
- Гонка корабля: ланцюг → відстань, таймер рівня — 🌱 (мета поверх пазла).

## Мапа на каталог
- Є: `multi-cell-size` (тріміно) · `piece-rotate-flip` · `combo-multiplier` (експоненційні очки ланцюга) · `event-points` · `time-out` (таймер рівня) · `sequential-levels` (45 місій) · `mode-select` · `tutorial-window` · `simultaneous-versus` + `garbage-attack` (junk) · `ai-opponent` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+filled-square-detect` «Заповнений квадрат N×N, без кольору» · entities/interact · 🌱 · слоти {n: 3}.
  - `+delayed-clear-window` «Збіг блимає вікно часу, його можна доростити, зникає наприкінці» · game-logic/score · 🥉 · слоти {window: time|beats, reset_on_extend: yes} — спільна з Magical Beat.
  - `+overlapping-square-reuse` «Нова фігура може брати клітини вже зібраних квадратів» · entities/interact · 📎.
  - `+chain-converts-to-coins` «Зачищені клітини лишають монети з рангом» · game-logic/economy · 🌱.
  - `+distance-race-meter` «Ланцюги рухають корабель до цілі» · game-logic/win · 🌱.
  - `+skin-unlock-progression` — фони й звуки за монети · interface/settings · 🌱.
  - `+chain-start-blocker` «Блок, що не може почати ланцюг» · entities/legality · 🌱.

## Пропозиції до словників
- `+trigger:pattern(square)` — нова форма шаблону: квадрат N×N, повністю заповнений (без кольору); у словнику є `row_full`, `group(n)`, але не квадрат.
- `+card:filled-square-detect` · `+card:delayed-clear-window` · `+card:overlapping-square-reuse` · `+card:distance-race-meter` — див. «Мапа на каталог».

## Джерела
- ⭐ [JA Wikipedia: 気持ちよさ連鎖パズル トリオンキューブ](https://ja.wikipedia.org/wiki/気持ちよさ連鎖パズル_トリオンキューブ) — фігури з 3 клітин (5 видів), тріон 3×3, стан ланцюга і три умови його кінця (час, вихід за нижній край, нема нового тріону).
- [EN Wikipedia: Trioncube](https://en.wikipedia.org/wiki/Trioncube) — тріміно, перекриття квадратів, кінець комбо, Penko, 45 рівнів, режими, дати.
- [Game Watch (JA), пробна версія](https://game.watch.impress.co.jp/docs/20060707/trion.htm) — ланцюг триває, поки є нові тріони; блоки завершеного ланцюга → монети.
- [Worthplaying](https://worthplaying.com/article/2007/4/6/reviews/41096-nds-review-trioncube/) — квадрат з уже засвічених клітин, експоненційні очки, типи місій, junk-блоки, ad-hoc VS.
- [GameVortex](https://gamevortex.com/gamevortex/soft_rev.php/3455) — поле на нижньому екрані, монети й діамант, D-pad + одна кнопка, 2–4 гравці.
- [Pocket Gamer](https://www.pocketgamer.com/trioncube/review/) — чорні блоки, Arcade з вісьмома планетами, Story 45 місій.
- YouTube: пошук «Trioncube DS gameplay».

## Непевне
- (?) Тривалість вікна ланцюга — у джерелах не названо; місія «скорочене вікно» підтверджує, що воно параметр.
- (?) Умова «клітини виходять за нижній край нижнього екрана» з JA незрозуміла: можливо, під час ланцюга стек зсувається вниз — не перевірено.
- (?) Чи зникають повні ряди, як у Tetris, і чи падають блоки після зачистки ланцюга — джерела мовчать.
- (?) Умова поразки в Endless (стек до верху?) — не знайдено.
- (?) Як саме junk-блоки потрапляють до суперника у VS і що таке race-режим — лише згадки.
- (?) Чи є прев'ю наступної фігури — не знайдено.
