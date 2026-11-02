---
title: Golf Peaks
slug: golf-peaks
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: iso
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2018
platforms: [PC, Mac, iOS, Android, Switch, Xbox One]
links:
  - {kind: other, url: "https://gamingtrend.com/reviews/a-puzzle-thats-par-for-the-course-golf-peaks-review/", best: true, note: "найповніший опис: карти ground/jump/jump+roll, точне попадання, вода, бункер, лід, стіни, висоти, 9 світів × 12"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Golf_Peaks", note: "розробник, платформи, дати"}
  - {kind: steam, url: "https://store.steampowered.com/app/923260/Golf_Peaks/", note: "120+ лунок, 9 + 3 бонусні на локацію"}
  - {kind: official, url: "http://afterburn.games", note: "студія Afterburn"}
  - {kind: play, url: "https://afterburn.itch.io/golf-peaks", note: "itch.io: доступність, портрет/ландшафт"}
  - {kind: other, url: "https://www.tapsmart.com/games/review-golf-peaks-accomplished-golfing-puzzler/", note: "огляд: свайп-керування, бампери, рампи, перекочування повз лунку"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=EyKZ2tlGsa8", note: "трейлер (вбудований на сторінці GOG)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Golf+Peaks+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-4dir, floor-types, inertia-slide, impassable-cells, teleport-pair, reach-exit, environment-death, no-moves-left, sequential-levels, level-unlock, level-select, swipe-gestures, keyboard-controls, settings-window, save-progress, movement-animation, +undo-redo, +world-map, +card-hand-moves, +exact-landing, +height-levels, +jump-arc, +slope-roll, +bounce-back, +checkpoint-reset]
proposes: ["+trigger:input", "+trigger:settled", "+trigger:enter", "+cond:has", "+cond:cell", "+effect:move", "+effect:slide", "+effect:roll", "+effect:bounce", "+effect:respawn", "+effect:take", "+role:terrain", "+role:supply", "+ui:card-hand", "+window:map-window", "+feature:undo", "+axis:control"]
author: opus
date: 2026-11-02
---

# Golf Peaks — гольф на ізометричній сітці, де кожен удар — карта з точною відстанню

## Суть
М'яч стоїть на клітинній ізометричній мапі з висотами; лунка — ціль. На рівень гравець отримує **руку карт-ударів**: «котити N», «стрибнути на N», «стрибнути на N і докотити M». Обираєш карту, обираєш один із 4 напрямків — мʼяч рухається детерміновано, з урахуванням рельєфу: схили котять, пісок зупиняє, вода повертає назад, лід ковзає. Ядро — **рух як ресурс**: відстані й тип руху задані наперед, гравець лише вибирає порядок і напрям; лунка приймає мʼяч лише при **точній** зупинці.

## Поле і час
- Ізометрична квадратна сітка з **висотами** (тераси-сходинки); невеликі острівці (~5×5…10×10 (?)), один екран, камера статична.
- Клітина має тип поверхні (трава, пісок, вода, лід, схил, конвеєр…) і висоту; між клітинами можуть бути стіни/уступи.
- Покроково: хід = зіграна карта. Рух усередині ходу анімований покроково, але повністю детермінований; між ходами нічого не рухається.
- Довкола острова — порожнеча: мʼяч, що вилетів за край, втрачено (повернення).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мʼяч | player | позиція, висота | рухається лише за картою: перекочування клітина за клітиною або політ дугою |
| Лунка (прапорець) | static | — | перемога, якщо мʼяч **зупинився** на ній; пролетів чи прокотився повз — не рахується |
| Карта «котити N» | supply | N | мʼяч котиться N клітин по землі в обраному напрямку |
| Карта «стрибок N» | supply | N | мʼяч летить дугою на N клітин, перелітає перешкоди, може піднятися на висоту |
| Карта «стрибок N + котити M» | supply | N, M | спершу політ, потім докат |
| Фервей / трава | terrain | — | звичайний рух |
| Пісок (бункер) | terrain | — | котіння зупиняється, щойно мʼяч в'їхав; з піску виводить лише карта зі стрибком |
| Вода | terrain | — | мʼяч тоне → повертається на останню клітину суші, яку торкнувся; карта витрачена |
| Порожнеча / провал | hazard | — | мʼяч втрачено → повернення (?) |
| Лід | terrain | — | мʼяч ковзає через усі клітини льоду, не витрачаючи відстань (?) |
| Схил / рампа | terrain | напрям | дозволяє закотитися на верхню терасу; зупинка на схилі → мʼяч скочується вниз |
| Уступ (висота) | static | Δh | вгору — лише рампою або стрибком; вниз — вільно |
| Стіна / прямовисна грань | static | — | мʼяч, що котиться, відбивається назад (решта відстані у зворотному напрямку) |
| Бампер / пружина (позначка ×) | terrain | — | підкидає мʼяч у повітря / на висоту (?) |
| Конвеєр | terrain | напрям | зсуває мʼяч, що на ньому зупинився (?) |
| Портал-лунка | terrain | пара | телепортує мʼяч до парного (світ 5+) |
| «Липкі» / рухомі клітини | terrain | — | згадані в описі GOG; поведінка (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(card, dir)` → ТО `take(hand, card)`, `custom: «виконати програму карти: [fly(N)], [roll(M)]»`.
- КОЛИ `custom: «крок котіння»` → ЯКЩО `free(next)` → ТО `move(ball, dir)`, `counter(left, -1)`; ЯКЩО `cell(next, wall)` → ТО `bounce(ball)` (решта кроків назад).
- КОЛИ `custom: «політ N»` → ТО `move(ball, +N)` ігноруючи клітини між; приземлення на вищу терасу дозволене, якщо висота досяжна (?).
- КОЛИ `enter(ball, sand)` → ТО `custom: «зупинка, залишок котіння згорає»`.
- КОЛИ `input(roll_card)` → ЯКЩО `cell(ball, sand)` → ТО `custom: «мʼяч не рушить»` (карта витрачена (?)).
- КОЛИ `enter(ball, water)` → ТО `respawn(ball, last_land)`.
- КОЛИ `edge(ball)` → ТО `respawn(ball, last_land)` (?).
- КОЛИ `enter(ball, ice)` → ТО `slide(ball, dir)` до кінця льоду (?).
- КОЛИ `settled(ball)` → ЯКЩО `cell(ball, slope)` → ТО `roll(ball, downhill)`.
- КОЛИ `enter(ball, slope_up)` → ТО `custom: «підйом на терасу коштує крок котіння»` (?).
- КОЛИ `enter(ball, bumper)` → ТО `custom: «підкинути»` (?).
- КОЛИ `settled(ball)` → ЯКЩО `cell(ball, conveyor)` → ТО `move(ball, belt_dir)` (?).
- КОЛИ `enter(ball, portal)` → ТО `teleport(ball, pair)`.
- КОЛИ `settled(ball)` → ЯКЩО `cell(ball, hole)` → ТО `win`, `next_level`. Перекотився через лунку з невитраченими кроками — котиться далі.
- КОЛИ `count(hand, ==, 0)` і `not cell(ball, hole)` → ТО `custom: «рівень не пройдено — рестарт без штрафу»`. Використати всі карти не обовʼязково.
- Перемога: мʼяч зупинився в лунці · Поразка: рука порожня (м'яка, лише рестарт) · Рахунок: нема (нема par, нема зірок).

## Керування і ввід
- Тач: тап по карті → свайп/драг у напрямку удару (одна з 4 ізометричних осей); попадати по мʼячу не треба.
- Миша/клавіатура: клік по карті + стрілки/клік напрямку; перепризначення клавіш; геймпад на консолях.
- Прицілу, сили, кута — нема: увесь «скіл» — вибір карти й напрямку. Попередній показ траєкторії (?).
- Undo останнього удару, рестарт лунки.

## Вікна, меню, HUD
- `splash-screen` — лого Afterburn.
- `main-menu` — Play · Settings (мінімалістично, без тексту).
- `map-window` — гора: локації (світи) знизу вгору; у кожній 9 лунок «half-course» + 3 бонусні «short course» (позначені іконкою з 3 клітин).
- `game-screen` — ізометрична мапа, мʼяч, прапорець; HUD: `card-hand` (ряд карт унизу/збоку — вертикально в портреті, горизонтально в ландшафті), `undo-button`, `restart-button`, `level-number`.
- `settings-window` — звук/музика, мова (18), колорблайнд-режим, керування.
- `end-screen` — коротка анімація влучання, перехід до наступної лунки.
- Переходи: main-menu → map-window → (лунка) game-screen → (влучання) наступна лунка / map-window.

## Фічі поза полем
- `world-map` + `level-unlock`: для просування потрібні лише 9 основних лунок локації; 3 бонусні — для 100 %.
- `undo`, `restart-level` без штрафу; `tutorial` інтерактивний **без тексту**.
- `autosave` / `cloud-save`, `achievements` (Steam).
- Доступність: `colorblind-palette`, `remap-controls`, `touch-controls`, `gamepad-support`, `localization`.
- Нема рахунку, par, таймера — «chill».

## Варіації й родичі
- Родичі: Desert Golfing (фізика замість сітки), Golf Story, What the Golf (жарт), Card-based movement у Slay the Spire / Into the Breach — «рух як ресурс»; Kwirk/Sokoban — детермінізм ходу.
- Найближче за ідеєю — **«програмування» руху з обмеженого набору команд**: Lightbot, Railbound (обмежений ресурс плиток).
- **Осі варіацій:** звідки ходи — рука карт (фіксована) / колода з добором / вільний ввід; тип руху — котіння / політ / комбінація; рельєф — плаский / з висотами; ціль — точна зупинка / проходження через.

## Цікавинки для курсу
- Карта = мала програма руху (`fly(N)`, `roll(M)`), інтерпретована покроково по клітинах — 🥉.
- Типи поверхні з різною реакцією на «стан руху» (котиться / летить / зупинився) — 🥈: `floor-types` × фаза руху.
- Висоти й уступи: вгору лише рампою/стрибком, вниз вільно — 🥉.
- Відбиття від стіни з рештою відстані — 📎.
- Розвʼязувач: перебір перестановок карт × 4 напрямки (рука ≤ 5 карт → ≤ 5!·4⁵) — 🥈, гарне BFS/DFS-завдання.
- Повернення на останню сушу (water reset) — 📎.

## Мапа на каталог
- Є: `move-4dir` ↔ напрям удару; `floor-types` ↔ пісок/вода/лід/схил/конвеєр; `inertia-slide` ↔ лід; `impassable-cells` ↔ стіни; `teleport-pair` ↔ портали; `reach-exit` ↔ лунка; `environment-death` ↔ вода/провал (у мʼякій формі); `no-moves-left` ↔ рука порожня; `sequential-levels` + `level-unlock` + `level-select` ↔ гора; `swipe-gestures` + `keyboard-controls`; `settings-window`; `save-progress`; `movement-animation`.
- **Нема** → пропозиції карток:
  - `+undo-redo` «Undo ходів у грі» · game-logic/flow · 📎 — як у Baba Is You.
  - `+world-map` «Мапа світу з вузлами-рівнями» · levels/progression · 🥉 — як у Baba Is You.
  - `+card-hand-moves` «Ходи з руки карт» · game-logic/rules · 🥉 · слот {hand: fixed|deck} — карта = рух, витрачається.
  - `+exact-landing` «Ціль лише при точній зупинці» · game-logic/win · 🌱.
  - `+height-levels` «Висоти клітин і уступи» · entities/legality · 🥉 · слот {climb: ramp|jump}.
  - `+jump-arc` «Стрибок через N клітин» · entities/move · 📎.
  - `+slope-roll` «Схил скочує вниз» · entities/move · 📎.
  - `+bounce-back` «Відбиття від стіни з рештою руху» · entities/move · 📎.
  - `+checkpoint-reset` «Повернення на останню безпечну клітину» · entities/death · 🌱.

## Пропозиції до словників
- `+trigger:input(card, dir)` — вибір карти + напрям; `+trigger:settled(ball)` — мʼяч зупинився (🔥 ×6 уже); `+trigger:enter(ball, terrain)`.
- `+cond:has(hand, card)`, `+cond:cell(next, type)`.
- `+effect:move`, `+effect:slide` (лід), `+effect:roll` (скочування зі схилу), `+effect:bounce` (стіна), `+effect:respawn(ball, last_land)`, `+effect:take(hand, card)`.
- `+role:terrain` (поверхні), `+role:supply` (карти в руці — запас поза полем).
- `+ui:card-hand` — ряд карт-ходів з піктограмами (дуга = політ, стрілка = котіння, число = відстань).
- `+window:map-window` — гора з локаціями.
- `+feature:undo`.
- `+axis:control` — нове значення `card-hand`: ввід = вибір команди з обмеженого набору + напрям.

## Джерела
- ⭐ [Gaming Trend review](https://gamingtrend.com/reviews/a-puzzle-thats-par-for-the-course-golf-peaks-review/) — карти ground/jump/combo, точне попадання, вода/бункер/лід/провал/стіни/висоти, 9×12 рівнів.
- [Wikipedia](https://en.wikipedia.org/wiki/Golf_Peaks) — розробник Afterburn, платформи і дати.
- [Steam](https://store.steampowered.com/app/923260/Golf_Peaks/) — 120+ лунок, 9 + 3 на локацію, безтекстовий туторіал.
- [itch.io](https://afterburn.itch.io/golf-peaks) — доступність, портрет/ландшафт, портали з 5-го світу (коментарі).
- [TapSmart review](https://www.tapsmart.com/games/review-golf-peaks-accomplished-golfing-puzzler/) — свайп-керування, бампери, рампи, перекочування повз лунку.
- [Use a Potion review](https://www.useapotion.com/2019/03/golf-peaks-review/) — chip shot, портали, схили.
- [Трейлер](https://www.youtube.com/watch?v=EyKZ2tlGsa8) (вбудований на GOG) · [пошук «Golf Peaks gameplay»](https://www.youtube.com/results?search_query=Golf+Peaks+gameplay).

## Непевне
- (?) Пісок: Gaming Trend пише «бункер — пастка, рівень закінчено», інші огляди — «зупиняє, вибивати лише стрибком»; прийнято друге (є також «rough» лише для стрибків — можливо, той самий тип).
- (?) Лід: чи витрачає відстань при ковзанні, чи ковзає «безкоштовно» до кінця льоду.
- (?) Бампер/пружина, конвеєр, «липкі» клітини — згадані в оглядах/GOG без точної поведінки.
- (?) Провал за край: повернення на останню клітину (як вода) чи рестарт.
- (?) Кількість світів: 9 (Gaming Trend, 108 рівнів) vs 10 (рецензент GOG, 120) — пізніші оновлення додали світ.
- (?) Попередній показ траєкторії — не перевірено.
