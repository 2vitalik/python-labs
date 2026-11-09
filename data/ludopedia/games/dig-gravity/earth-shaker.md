---
title: Earth Shaker
slug: earth-shaker
aka: []
family: dig-gravity
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 1990
platforms: [ZX Spectrum]
links:
  - {kind: other, url: "https://www.worldofspectrum.org/pub/sinclair/games-info/e/EarthShaker.txt", best: true, note: "інструкція з касети Your Sinclair: усі 13 обʼєктів по рядку"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Earth_Shaker_(video_game)", note: "історія: Michael Batty, ковертейп YS, цитата про «прості правила»"}
  - {kind: other, url: "https://spectrumcomputing.co.uk/entry/1563/ZX-Spectrum/Earth_Shaker", note: "ZXDB: випуск YS #63, BASIC, керування, рецензії"}
  - {kind: other, url: "https://worldofspectrum.org/archive/software/games/earth-shaker-your-sinclair", note: "архів WoS: файли й інструкція"}
  - {kind: play, url: "https://worldofspectrum.org/play_game/7f6e964a0996a15", note: "грати в браузері (емулятор WoS)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Earth+Shaker+ZX+Spectrum+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, gravity-fall, dig-terrain, collect-all, reach-exit, environment-death, player-death, hp-damage, item-pickup, temporary-modes, teleport-one-way, button-toggle, impassable-cells, sequential-levels, keyboard-controls, controls-remap, status-panel, +fire-and-bubble, +object-on-head]
proposes: ["+trigger:smashed", "+card:fire-and-bubble", "+card:object-on-head"]
author: opus
date: 2026-11-09
---

# Earth Shaker — Boulder Dash без ворогів: обвали, вогонь, бульбашки й силові поля

## Суть
Маленький робот риє тунелі під землею, збирає всі кристали і виходить у «чорні двері». Механіка — як у [Boulder Dash](boulder-dash.md), але без ворогів-тварин: небезпеку створюють **стихії й обʼєкти** — вогонь, силові поля, що висмоктують енергію, і самі обвали. Автор, Michael Batty, захоплювався тим, як «кілька простих правил дають складну поведінку й реалістичні обвали» — гра про каскади падінь. Нове проти BD: бульбашка-опора, вогонь, що розбиває каміння, монітор, який вимикають, скинувши на нього обʼєкт, і «гравітаційна паличка», що дозволяє тримати камінь на голові.

## Поле і час
- Підземелля з «камер»; телепорт переносить до найближчої камери в лівому верхньому куті екрана — тож поле більше за екран (?).
- Один шар: у клітині один обʼєкт; земля тримає те, що над нею.
- Real-time; робот має енергію (силові поля її «смокчуть»), окремий таймер в інструкції не згаданий.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Робот | player | енергія; життя | рух 4 напрямки; копає землю; гине від каменя на голову й від вогню |
| Земля | terrain | — | тримає обʼєкти над собою; викопав — над нею починається обвал |
| Стіна | static | невразлива | «Impenetrable» |
| Камінь | object | падає | падає без опори; на голову — смерть; вогонь розбиває його |
| Кристал | pickup | — | зібрати всі на екрані → відчиняються двері |
| Чорні двері (Back Door) | gate | закриті / відчинені | вихід після всіх кристалів |
| Jumping Jellybean | pickup | — | відновлює енергію |
| Еліксир | pickup | — | «Restores life» — повертає життя |
| Силове поле | hazard | привʼязане до монітора | висмоктує енергію; зникає, коли знищено монітор |
| Монітор | switch | — | скинути на нього обʼєкт → силові поля вимикаються |
| 4D-телепорт | object | — | переносить до найближчої камери вгорі-ліворуч |
| Гравітаційна паличка | pickup | діє обмежений час | обʼєкти можуть лежати на роботі, не вбиваючи |
| Бульбашка | object | — | тримає обʼєкти на собі; гасить вогонь |
| Вогонь | hazard | — | знищує робота; камінь, що потрапив у вогонь, розсипається |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `cell(target, earth|empty)` → ТО `move(robot, dir)`; земля → `set_cell(empty)`.
- КОЛИ `tick` → ЯКЩО `not supported(rock)` → ТО `fall(rock)`; опора — земля, стіна, бульбашка, інший обʼєкт.
- КОЛИ `contact(falling rock, robot)` → ЯКЩО `not state(robot, gravity_stick)` → ТО `lose`, `lives(-1)`; інакше камінь лежить на роботі.
- КОЛИ `contact(robot, gravity_stick)` → ТО `pickup`, `set_state(robot, gravity_stick, duration)`.
- КОЛИ `contact(robot, crystal)` → ТО `pickup`, `counter(crystals, -1)`.
- КОЛИ `counter(crystals, ==, 0)` → ТО `set_state(back_door, open)`.
- КОЛИ `contact(robot, back_door)` → ЯКЩО `state(back_door, open)` → ТО `win`, `next_level`.
- КОЛИ `tick` → ЯКЩО `in_range(robot, forcefield, 0)` → ТО `custom: «енергія робота спадає»`.
- КОЛИ `custom: «smashed: обʼєкт упав на монітор»` → ТО `disappear(forcefield)` усіх полів монітора.
- КОЛИ `contact(robot, jellybean)` → ТО `pickup`, `custom: «енергія — повна»`; `contact(robot, elixir)` → `pickup`, `lives(+1)`.
- КОЛИ `contact(robot, teleport)` → ТО `teleport(robot, nearest chamber top-left)`.
- КОЛИ `contact(robot, fire)` → ТО `lose`, `lives(-1)`.
- КОЛИ `contact(rock, fire)` → ТО `disappear_a` (`custom: «камінь розсипається»`).
- КОЛИ `contact(bubble, fire)` → ТО `disappear_b` (вогонь гасне).
- Перемога: усі кристали → двері. Поразка: камінь на голову, вогонь, енергія скінчилась (?) → −1 життя.

## Керування і ввід
- Kempston-джойстик або перепризначувані клавіші (define keys): 4 напрямки.
- Окремих клавіш дій (снап, бомби) в інструкції нема.

## Вікна, меню, HUD
- `main-menu`: вибір керування (джойстик / свої клавіші) → старт.
- `game-screen`: поле; HUD — енергія (`energy-bar`), `lives`, лишилось кристалів (`remaining-counter`) (?).
- `end-screen`: game over.

## Фічі поза полем
- `levels-sequential`: 32 рівні.
- `remap-controls`: redefine keys.
- Гра написана на Sinclair BASIC (з машинними вставками (?)) і вийшла безкоштовно на ковертейпі Your Sinclair.

## Варіації й родичі
- Корінь — [Boulder Dash](boulder-dash.md) (камінь, кристал, вихід за квотою, копання); близькі за духом «без ворогів» — [Banana](banana.md).
- Видавець Zeppelin спершу відмовив через позови First Star проти клонів BD.
- **Осі варіацій**: загроза — «вороги (BD) / лише стихії (Earth Shaker)»; захист від каменя — «нема (BD) / тимчасовий стан (паличка) / камінь не вбиває (Dot Valley, Banana)»; опора — «земля і стіни / плюс плаваюча бульбашка».

## Цікавинки для курсу
- Обвал як каскад: «нема опори → падає», бульбашка теж опора — 🥉: порядок обробки, щоб стовп каміння падав разом.
- Монітор і його силові поля: подія на одній клітині вимикає групу інших — 📎.
- Гравітаційна паличка: тимчасовий стан, що міняє правило смерті — 🌱.
- Вогонь ↔ бульбашка ↔ камінь: таблиця взаємодій трьох обʼєктів — 📎.

## Мапа на каталог
- Є: `move-4dir` · `gravity-fall` · `dig-terrain` · `collect-all` ↔ всі кристали · `reach-exit` ↔ чорні двері · `environment-death` (камінь, вогонь) · `player-death` · `hp-damage` ↔ енергія і силові поля · `item-pickup` · `temporary-modes` ↔ гравітаційна паличка · `teleport-one-way` ↔ 4D-телепорт · `button-toggle` ↔ монітор вимикає поля · `impassable-cells` · `sequential-levels` · `keyboard-controls` + `controls-remap` · `status-panel`.
- **Нема** → пропозиції карток:
  - `+fire-and-bubble` «Стихія і гасник» · entities/interact · 📎 — вогонь вбиває й руйнує, бульбашка гасить і тримає.
  - `+object-on-head` «Носити камінь на голові» · entities/state · 🌱 · слот {duration} — тимчасово падіння не вбиває.

## Пропозиції до словників
- `+trigger:smashed(a)` — на A впав обʼєкт (монітор вимикає поля); уже пропонували Emerald Mine та ін.

## Джерела
- ⭐ [Інструкція Your Sinclair (WoS)](https://www.worldofspectrum.org/pub/sinclair/games-info/e/EarthShaker.txt) — опис кожного обʼєкта одним рядком, «32 fun-packed levels», керування.
- [Wikipedia](https://en.wikipedia.org/wiki/Earth_Shaker_(video_game)) — автор, ковертейп 1990, цитата про прості правила й обвали, історія з Zeppelin.
- [Spectrum Computing / ZXDB](https://spectrumcomputing.co.uk/entry/1563/ZX-Spectrum/Earth_Shaker) — Your Sinclair #63, Sinclair BASIC, рецензія YS 91 %.
- [WoS: архів](https://worldofspectrum.org/archive/software/games/earth-shaker-your-sinclair) — файли й інструкція.

## Непевне
- (?) Чи камінь скочується з інших каменів (як у BD) — «реалістичні обвали» на це натякають, джерела не кажуть.
- (?) Бульбашка — чи спливає вгору сама, чи стоїть; у інструкції лише «тримає і гасить».
- (?) Як витрачається енергія поза силовими полями (з часом?) і чи її кінець = смерть; є чи нема таймера рівня.
- (?) Поле: скрол чи камери-екрани; формулювання телепорта натякає на камери.
- (?) «Пізні рівні вимагають ловити каміння» — переказ пошукового результату, в самій інструкції не підтвердив.
- (?) Чи вогонь поширюється — не описано.
