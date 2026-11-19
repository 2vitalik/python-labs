---
title: Croquet Conundrum
slug: croquet-conundrum
aka: []
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: hex
  time: turn
  opponent: none
  info: full
  random: none
  goal: collect
year: 2024
platforms: [web, Windows, Android]
links:
  - {kind: itch, url: "https://lummie-thief.itch.io/croquet-conundrum", best: true, note: "грати в браузері; опис, теги Hex Based / Sokoban / Mouse only; правила від автора в коментарях: 2 постріли максимум, воротця +1, кулі +2 і «постав кулю поруч»"}
  - {kind: play, url: "https://html-classic.itch.zone/html/11688854/index.html", note: "веб-збірка (Unity WebGL); тексти Альманаху й підказок витягнуто з її файла даних"}
  - {kind: other, url: "https://lummie-thief.itch.io/croquet-conundrum/devlog/812999/the-aforementioned-larger-update", note: "девлог 09.10.2024: смужки на кулі = постріли; рівень Boot — синю кулю зсуває досить сильний удар; «place on ice»; зміни мапи"}
  - {kind: other, url: "https://lummie-thief.itch.io/croquet-conundrum/devlog/804350/small-fixes-before-larger-update", note: "девлог 24.09.2024: пісок проти небажаних розвʼязків, опція часу доби"}
  - {kind: other, url: "https://www.bontegames.com/2024/09/croquet-conundrum-browser.html", note: "Bart Bonte, 09.09.2024: «почни з Альманаху (книжка)»"}
  - {kind: other, url: "https://play.google.com/store/apps/details?id=com.joeycook.croquetconundrum", note: "Android-версія (лінк зі сторінки itch; вміст у фетчі не відкрився)"}
  - {kind: other, url: "https://gamebrain.co/game/croquet-conundrum", note: "агрегатор: реліз 06.09.2024, PC / браузер"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Croquet", note: "справжній крокет: воротця → додатковий удар, рокет → два удари, кожну кулю — раз між воротами"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Croquet+Conundrum+Lummie+Thief", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [floor-types, inertia-slide, stop-cell, move-limit, collect-all, reach-exit, world-map, map-window, codex-window, level-solver, unsolvable-states, undo-step, restart-level, save-progress, settings-window, main-menu, sound-effects, background-music, +hex-grid-render, +drag-to-hit, +shot-economy, +roquet-charge, +color-matched-pickup, +place-adjacent-after-hit, +auto-switch-on-empty, +pipe-travel, +carry-objects-between-levels, +reveal-on-traverse, +bounce-back, +solvability-hint, +progress-hint, +goal-hint, +multiple-endings, +secret-area, +time-of-day-option]
proposes: ["+effect:hit", "+effect:stop", "+ui:shots-counter", "+feature:solvability-check", "+feature:goal-hint", "+feature:codex-grows", "+axis:control", "+card:shot-economy", "+card:roquet-charge", "+card:solvability-hint"]
author: opus
date: 2026-11-19
---

# Croquet Conundrum — крокет на гекс-островах: проведи кулю крізь усі воротця й у трубу, маючи щонайбільше два удари

## Суть
Гравець бʼє свою кулю драгом мишею, проводить її крізь воротця свого кольору й виганяє в трубу, що веде на інший острів. Ядро — **економіка ударів за справжніми правилами крокету**: у кулі максимум 2 удари, воротця дають +1, удар по «зарядженій» кулі дає +2 і право поставити свою кулю поруч з нею.

Поверх цього — поверхні (пісок зупиняє, на льоду не зупинитись), мапа островів, сполучених трубами, і кілька кінцівок за прихованими маршрутами. Підказка вміє сказати, чи пазл ще розвʼязний з поточної позиції.

## Поле і час
- Гексагональна сітка: острови з гексів-плиток серед моря; стан пазла в коді — рядок із кубічними гекс-координатами куль `(x, y, z)`, їхніми пострілами й прапорцями, вмістом труб і станом воротець (`B4{(-2, 1, 1), 1, [], F, -1}, W1{T}`).
- Шари: плитка поверхні (трава / пісок / лід) → обʼєкти (кулі, воротця, труби на краях острова).
- Покроково: хід = один удар; куля котиться анімацією, далі світ стоїть. Таймера нема; цикл дня і ночі — косметика (опцією можна вибрати час доби й зупинити його).
- Рівень (острів) може містити кілька пазлів; гра визначає пазл за точкою входу й кулями, принесеними з собою. Рівні сполучені трубами в мапу світу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Червона куля | player | постріли 0–2 (смужки на кулі) | бʼється драгом; збирає червоні воротця; лише вона веде гравця трубою на наступний рівень |
| Інша куля (синя) | object | постріли; стан `charged` | заряджена — дає +2 постріли й «підкладання»; досить сильний удар її зсуває; може стати «твоєю» кулею |
| Воротця (wicket) | pickup | колір | збирає лише куля того ж кольору: +1 постріл, інші кулі заряджаються |
| Труба | gate | куди веде; видима / прихована | вхід і вихід між островами; везе всі кулі, які в неї загнали |
| Трава | terrain | — | звичайна поверхня кочення |
| Пісок | terrain | — | зупиняє кулю одразу; з піску — лише на 1 гекс |
| Лід | terrain | — | рух не може закінчитись на льоду; зіткнення — відскок назад |
| Вода / край острова | static | — | межа острова (?) |
| Молоток | — | — | лише курсор удару, не сутність поля |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, ball)` → ЯКЩО `counter(shots, >, 0)` → ТО `counter(shots, -1)`, `custom: «куля котиться гексами в обраному напрямку»`.
- КОЛИ `enter(ball, sand)` → ТО `custom: «куля одразу зупиняється»`.
- КОЛИ `input(drag, ball)` → ЯКЩО `cell(ball, sand)` → ТО `move(ball, dir)` — з піску лише на один гекс.
- КОЛИ `enter(ball, ice)` → ТО `slide(ball, dir)` — на льоду куля не зупиняється.
- КОЛИ `blocked(ball)` → ЯКЩО `cell(ball, ice)` → ТО `bounce(ball)` — відскок у протилежному напрямку.
- КОЛИ `contact(ball, wicket)` → ЯКЩО `same(ball, wicket, color)` → ТО `pickup`, `counter(shots, +1)`, `set_state(other_balls, charged)`.
- КОЛИ `contact(ball, wicket)` → ЯКЩО `not same(ball, wicket, color)` → ТО `custom: «воротця лишаються незібраними»`.
- КОЛИ `contact(ball, ball2)` → ЯКЩО `state(ball2, charged)` → ТО `clear_state(ball2, charged)`, `counter(shots, +2)`, `choose(«поставити свою кулю поруч / ні»)`.
- КОЛИ `after(choose)` → ЯКЩО `free(cell_next_to_ball2)` → ТО `place(ball, cell_next_to_ball2)`; на лід — `place` без ковзання.
- КОЛИ `contact(ball, ball2)` → ЯКЩО `not state(ball2, charged)` → ТО `push(ball2)` (?) — «якщо вдарити досить сильно» (рівень Boot).
- КОЛИ `counter(shots, >, 2)` → ТО `set_value(shots, 2)` — у кулі не буває більше двох пострілів.
- КОЛИ `counter(shots, ==, 0)` → ЯКЩО `custom: «інша куля рівня має постріли»` → ТО `custom: «вона стає твоєю кулею»`.
- КОЛИ `enter(ball, pipe)` → ТО `custom: «куля чекає в трубі»`; пізніше переїжджає разом із гравцем.
- КОЛИ `enter(red_ball, pipe)` → ЯКЩО `count(wicket, ==, 0)` → ТО `next_level`, `custom: «наступний рівень — той, куди веде труба; кулі з цієї труби їдуть теж»`.
- КОЛИ `enter(red_ball, entry_pipe)` → ЯКЩО `count(wicket, ==, 0)` → ТО `next_level` — вийти можна й тією трубою, якою прийшов.
- КОЛИ `custom: «трубу вперше пройдено з іншого боку»` → ТО `reveal(pipe)` — частина труб зʼявляється лише так.
- КОЛИ `input(hint)` → ТО `window(hints-window)`; на «Can I solve it from here?» — `message(«нерозвʼязно; востаннє було розвʼязно N ходів тому»)`.
- Перемога: усі воротця рівня зібрані, червона куля пішла в трубу → наступний острів; уся гра — 4 кінцівки. · Поразка: нема; глухий кут (жодна куля без пострілів не рушить) → undo / рестарт. · Рахунку нема.

## Керування і ввід
- Лише миша: клік і драг по кулі — удар (на екрані молоток). Альманах: «There are no hidden controls».
- Кнопки: Альманах (книжка), підказка (лампочка або H), мапа, undo, рестарт, налаштування. F — повний екран у завантажуваній версії.
- Після удару по зарядженій кулі — вибір, чи підкласти свою кулю поруч (клік по місцю (?)).
- Секрет: ~50 натискань undo на відкритій мапі стирають збереження.

## Вікна, меню, HUD
- `main-menu`: «Click to Start», титри (Joey Cook, музика Riley Woodward, звуки Zapsplat), Save and Quit.
- `game-screen`: острів у 3D; HUD — смужки на кулі (`+ui:shots-counter`), спливні «+1» / «−1» (`popup-text`), кнопки дій.
- `codex-window` — «The Almanac»: розділи Balls · Pipes · Sand · Wickets з індексом; правило додається, щойно гравець його зустрів, з позначкою-сповіщенням.
- `hints-window` (HintMenu): питання «Can I solve it from here?», «How close have I been?», «What is my goal?», «Ask a question»; показ попередньої підказки.
- `map-window`: острови-рівні, непройдені пазли — знаками питання.
- `settings-window`: час доби (і зупинка циклу), гучність музики / ефектів / оточення (?), якість графіки (?).
- `end-screen`: «Ending N of 4», фінальні тексти; `credits-window`.
- Переходи: main-menu → game-screen ↔ map-window / codex-window / hints-window; труба → game-screen іншого острова; кінцівка → end-screen.

## Фічі поза полем
- `world-map` з нелінійними маршрутами: кілька вихідних труб, приховані труби, приховані пазли для кінцівок 2–4 (`collectibles`-подібне).
- `hint` нового типу: гра зберігає множину всіх розвʼязних станів кожного пазла (граф без циклів, розвʼязки — листки) і відповідає «чи розвʼязно звідси», «наскільки близько ти був», «яка тут мета».
- `codex`, що росте з відкриттями; `undo`, `restart-level`, `autosave` (у браузері може губитись).
- Опції: час доби; Android-порт; Unity.

## Варіації й родичі
- Справжній крокет (W:Croquet): прохід воріт дає додатковий удар; рокет — два удари (крокетний після підкладання кулі впритул і продовження); кожну кулю можна крокетувати раз між воротами — у грі це стан `charged`.
- [Golf Peaks](golf-peaks.md) — гольф на сітці з картами-ударами; [Herugolf](../pencil-logic/herugolf.md) — паперовий гольф-пазл; [Ice-sliding puzzles](../push-slide/ice-sliding-puzzles.md) — ковзання до упору.
- **Осі варіацій:** бюджет ударів — фіксований пар / карти (Golf Peaks) / поповнення подіями (тут) · поверхня — трава / пісок-гальмо / лід без зупинки · інші кулі — перешкода / ресурс ударів / запасна «душа» гравця.

## Цікавинки для курсу
- Бюджет ударів зі стелею 2 і поповненням +1 / +2 — 🥉 (стан пострілів у кожної кулі + перехід керування).
- Заряд після воріт і «підкладання» кулі поруч з обраним гексом — 📎.
- Поверхні: пісок зупиняє і випускає на 1 гекс, лід не дає зупинитись і відбиває — 📎.
- Гекс-рух у кубічних координатах `(x, y, z)` — 📎.
- Підказка «чи розвʼязно звідси»: перебір усього графа станів пазла, хеш-множина розвʼязних станів, «N ходів тому» — 🥇.
- Острови-рівні, сполучені трубами, які переносять кулі; пазл визначається входом і принесеними кулями — 🥈.

## Мапа на каталог
- Є: `floor-types` ↔ трава / пісок / лід · `inertia-slide` ↔ лід · `stop-cell` ↔ пісок · `move-limit` ↔ постріли · `collect-all` ↔ усі воротця · `reach-exit` ↔ труба · `world-map` + `map-window` ↔ мапа островів · `codex-window` ↔ Альманах · `level-solver` + `unsolvable-states` ↔ підказка · `undo-step`, `restart-level`, `save-progress`, `settings-window`, `main-menu`, `sound-effects`, `background-music`.
- **Нема** → пропозиції карток:
  - `+shot-economy` «Бюджет ударів із поповненням» · entities/legality · 🥉 · слоти {max: 2, wicket: +1, ball: +2}.
  - `+roquet-charge` «Воротця заряджають кулі; удар по зарядженій — постріли й підкладання» · entities/interact · 📎.
  - `+drag-to-hit` «Удар драгом від обʼєкта» · interface/input · 🌱.
  - `+solvability-hint` «Підказка: чи розвʼязно звідси і як близько був» · levels/solvability · 🥇.
  - `+carry-objects-between-levels` «Обʼєкти переходять у наступний рівень разом із гравцем» · levels/progression · 🥉.
  - `+reveal-on-traverse` «Прохід зʼявляється після першого проходу з іншого боку» · levels/progression · 🌱.
  - `+color-matched-pickup` «Підбирає лише сутність того ж кольору» · entities/interact · 🌱.
  - `+auto-switch-on-empty` «Без ходів — керування переходить до іншої сутності» · entities/state · 📎.

## Пропозиції до словників
- `+effect:hit(a, dir)` — сутність дістає удар і починає рух у напрямку (крокет, гольф-ігри).
- `+effect:stop(a)` — рух обривається на місці (пісок); відрізняти від `block` (рух не почався).
- `+ui:shots-counter` — лічильник пострілів; тут — смужки на самій кулі.
- `+feature:solvability-check` — «чи розвʼязно з поточної позиції» і «як близько був».
- `+feature:goal-hint` — підказка «яка мета цього рівня», без розвʼязку.
- `+feature:codex-grows` — довідник правил, що поповнюється, коли гравець зустрів правило.
- `+axis:control` — `drag-shot`: драг від обʼєкта задає напрям удару.
- `+card:shot-economy`, `+card:roquet-charge`, `+card:solvability-hint` — див. вище.

## Джерела
- ⭐ [itch: Croquet Conundrum](https://lummie-thief.itch.io/croquet-conundrum) — опис, теги, відповіді автора: «2 shots max, wickets give +1 shot, balls give +2 shots and let you put your ball next to them»; підказки на множині розвʼязних станів; кілька пазлів у рівні; мапа зі знаками питання; кінцівки.
- [Веб-збірка](https://html-classic.itch.zone/html/11688854/index.html) — тексти Альманаху: «Click and drag on your ball to hit it, consuming a shot», «Your ball cannot have more than two shots», «A ball moving into sand immediately comes to a stop», «A moving ball cannot come to a stop on ice», «…while sliding on ice, it rebounds in the opposite direction», «A wicket can only be collected by a ball of the same color», «…other balls in the level become charged», «Some pipes will only appear… after they have been traveled through»; «Ending N of 4».
- [Девлог 09.10.2024](https://lummie-thief.itch.io/croquet-conundrum/devlog/812999/the-aforementioned-larger-update) і [24.09.2024](https://lummie-thief.itch.io/croquet-conundrum/devlog/804350/small-fixes-before-larger-update) — смужки = постріли, сильний удар по синій кулі, лід, пісок, опція часу доби.
- [Bart Bonte](https://www.bontegames.com/2024/09/croquet-conundrum-browser.html) і [GameBrain](https://gamebrain.co/game/croquet-conundrum) — дата, автор, «почни з Альманаху».
- [Wikipedia: Croquet](https://en.wikipedia.org/wiki/Croquet) — правила справжнього крокету.

## Непевне
- (?) Як далеко котиться куля по траві: чи довжина драгу задає дистанцію, чи куля котиться до упору; у коді є `DragDirection`, `CalculateDistance`, але самого правила не видно.
- (?) Як саме сильний удар зсуває незаряджену кулю (передає залишок руху?) — відомо лише з девлогу про рівень Boot.
- (?) Що буває з кулею за краєм острова (вода) і з червоною кулею, загнаною в трубу до збору всіх воротець.
- (?) Кольори воротець, крім червоних; білі воротця на скриншотах.
- (?) Кількість рівнів і пазлів: у ресурсах ~20 назв (Engine, Carp, Amoeba, Boot, Tape, Siege…), точної цифри нема.
- (?) Бонусна механіка після однієї з кінцівок («fun mechanic I implemented but couldn't find a good place»), затримка між підказками (`HintCooldownTimer`), повзунки звуку й якості — лише з ідентифікаторів коду.
- (?) Статус на itch — «In development»; рік 2024 — за GameBrain (06.09.2024) і девлогами.
