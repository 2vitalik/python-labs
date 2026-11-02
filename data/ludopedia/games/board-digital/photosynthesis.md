---
title: Photosynthesis (Фотосинтез)
slug: photosynthesis
family: board-digital
also: [build-sim]
klass: cursor
axes:
  field: hex
  time: turn
  opponent: online
  info: full
  random: none
  goal: score
year: 2017
platforms: [board, web]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/photosynthesis/game-rules.php", best: true, note: "повні правила: тіні за висотою, світло, дії й ціни, дальність насіння, збір, кінець, експерт-варіант"}
  - {kind: play, url: "https://en.boardgamearena.com/gamepanel?game=photosynthesis", note: "грати в браузері (BGA), 2–4"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Photosynthesis_(board_game)", note: "склад, фази, Under the Moonlight"}
  - {kind: official, url: "https://blueorangegames.com/index.php/games/photosynthesis", note: "видавець Blue Orange"}
  - {kind: bgg, url: "https://www.boardgamegeek.com/boardgame/218603", note: "BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Photosynthesis+board+game+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 65
mechanics: [cell-click, hover-highlight, legal-move-highlight, turn-enforcement, hot-seat, ai-opponent, round-currency, event-points, game-settings, +hex-grid-render, +directional-shadow, +rotating-light-source, +growth-stages, +seed-range-by-size, +once-per-cell-per-turn, +depleting-score-stacks, +currency-cap, +player-board-cost-track, +first-player-token, +revolution-timer]
proposes: ["+trigger:round_end", "+trigger:phase_start", "+effect:place", "+effect:grow", "+effect:harvest", "+cond:shaded", "+cond:afford", "+cond:in_range", "+role:supply", "+role:zone", "+ui:sun-indicator", "+ui:shadow-overlay", "+ui:light-track", "+ui:score-stacks", "+ui:opponent-boards", "+window:match-setup", "+card:directional-shadow", "+card:rotating-light-source", "+card:growth-stages"]
author: opus
date: 2026-11-02
---

# Photosynthesis — гекс-ліс під сонцем, що обертається: високі дерева кидають тінь, світло — валюта

## Суть
Гравці вирощують ліс на спільному гекс-полі: насіння → мале → середнє → велике дерево → зрубати за очки. Щораунду сонце пересувається на одну з 6 сторін, і кожне дерево кидає тінь у протилежний бік довжиною за своєю висотою; дерево в тіні рівного чи вищого не отримує світла. Світло — валюта на купівлю, посадку й ріст. Ядро — просторова гра з **напрямленою тінню, що крутиться**: дерево, що зараз тебе годує, через два раунди закриє тебе ж.

## Поле і час
- Гекс-поле 37 клітин (гексагон «4 на боці»), концентричні кільця родючості: центр — 4 листки, кільце 6 — 3 листки, кільце 12 — 2, зовнішнє 18 — 1 (?).
- Сонце — 6 позицій навколо поля; рух за годинниковою стрілкою на 1 позицію кожен раунд; оберт = 6 раундів. Гра — 3 оберти (18 раундів) або 4 в експерт-варіанті.
- Раунд: фаза фотосинтезу (сонце рухається, усі рахують світло) → фаза життєвого циклу (гравці по черзі, кожен робить усі дії за раз).
- Шари клітини: родючість (постійна) · дерево гравця одного з 4 розмірів (насіння, мале, середнє, велике) · тінь (обчислюється щораунду).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина | zone | родючість 1–4 листки | одне дерево/насіння; активується раз на хід гравця |
| Насіння | object | висота 0, дальність — | світла не дає, тіні не кидає |
| Мале дерево | object | висота 1, світло 1, тінь 1 | тінь на 1 клітину від сонця |
| Середнє дерево | object | висота 2, світло 2, тінь 2 | тінь на 2 клітини |
| Велике дерево | object | висота 3, світло 3, тінь 3 | тінь на 3; єдине, що можна зрубати |
| Сонце | object | позиція 0–5 | раз на раунд обертається; задає напрямок тіні |
| Планшет гравця | supply | 4 насіння, 4 малі, 3 середні, 2 великі на клітинках з цінами | купівля знизу колонки; зрубане/замінене повертається на верхнє вільне місце |
| Доступна зона | supply | старт: 2 насіння, 4 малі (2 з них одразу на поле), 1 середнє | звідси садять і ростять без купівлі |
| Трек світла | resource | 0–20 | понад 20 згорає |
| Стоси жетонів очок | supply | 4 стоси за родючістю, спадні значення | зрубав — бери верхній зі стосу родючості клітини |
| Жетон першого гравця | object | — | переходить за годинниковою стрілкою |
| Лічильник обертів | object | 3 (+1 експерт) | знімається після кожного повного оберту |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(photosynthesis)` → ЯКЩО `custom: «не перший раунд»` → ТО `rotate(sun, +60°)`.
- КОЛИ `phase_start(photosynthesis)` → ТО для кожного дерева: ЯКЩО `not shaded(tree)` → ТО `currency(owner, +height)`; насіння — 0.
- Тінь: `shaded(t)` ⇔ `custom: «на відстані ≤ h(s) від t у бік до сонця стоїть дерево s з h(s) ≥ h(t)»`; тінь кидають і затінені дерева; свої теж затінюють.
- КОЛИ `input(buy(piece))` → ЯКЩО `afford(cost_of_lowest_slot)` → ТО `currency(-cost)`, перенести в доступну зону (клітину поля не активує).
- КОЛИ `input(plant(seed, from_tree, cell))` → ЯКЩО `free(cell)` and `in_range(from_tree, cell, height)` and `custom: «ні дерево, ні клітина ще не активовані цього ходу»` → ТО `currency(-1)`, `place(seed, cell)`.
- КОЛИ `input(grow(cell))` → ЯКЩО `has(available, next_size)` and `afford(size_cost)` (1/2/3 світла для насіння→мале→середнє→велике) → ТО `transform(piece, next_size)`, старий шматок → на планшет (нема місця — з гри).
- КОЛИ `input(harvest(large_tree))` → ЯКЩО `afford(4)` → ТО `currency(-4)`, дерево → планшет, `take(top_token(stack[soil]))` (порожній стос → наступний нижчий), клітина звільнена.
- Кожну клітину поля гравець активує не більше раз за хід → не можна виростити й одразу садити з того ж дерева.
- Експерт: `custom: «не можна садити й ростити в затінених клітинах»`.
- КОЛИ `round_end` → ТО жетон першого гравця переходить; після 6 раундів — зняти лічильник оберту.
- КОЛИ `custom: «знято останній лічильник»` → ТО `game_over`: сума жетонів + 1 ПО за кожні 3 невитрачені світла.
- Перемога: найбільше ПО; нічия → більше насіння й дерев на полі → спільна перемога.
- 2 гравці: прибрати 3 найцінніші жетони 4-листкової клітини.

## Керування і ввід
- Цифрова версія: клік по шматку на планшеті — купити; клік по дереву → підсвічені клітини в радіусі для насіння; клік по дереву — виростити / зрубати.
- Перед дією показ прогнозу тіні наступного раунду (`shadow-overlay`) — у паперовій грі це рахують у голові.
- Хід послідовний: перший гравець робить усі дії, далі за годинниковою.

## Вікна, меню, HUD
(цифрова версія — BGA)
- `match-setup`: 2–4 гравці, кількість обертів (3/4), експерт-варіант.
- Стартова фаза: кожен по черзі ставить 2 малих дерева на зовнішнє кільце.
- `game-screen`: гекс-поле; `sun-indicator` — позиція сонця і напрямок променів; `shadow-overlay` — затінені клітини; `light-track` кожного; `score-stacks` — 4 стоси з верхнім значенням; планшет гравця з цінами; `opponent-boards`; `turn-indicator` + лічильник обертів.
- `end-screen`: жетони кожного гравця, бонус за світло, тай-брейк.
- `help-window`: правило тіні з прикладами.
- Переходи: match-setup → розстановка → game-screen (18 раундів) → end-screen.

## Фічі поза полем
- `online-multiplayer` (BGA), `turn-timer`.
- `custom-rules`: 4-й оберт, заборона садити в тіні.
- Розширення Under the Moonlight (2020): місяць обертається проти сонця, тварини з особливими діями.
- Нагорода Mensa Select 2018.

## Варіації й родичі
- Родичі «напрямлене освітлення/видимість»: лазери (Khet, Deflektor), тіні в стелс-іграх, `line-of-sight` у роглайках — тут з висотою як параметром «хто кого закриває».
- Родичі за економікою: Tiny Towns/Kingdomino (просторові очки), трек валюти з ціновою драбиною планшета (Power Grid, Terra Mystica).
- **Осі варіацій**: джерело світла (одне обертається / два протилежні — місяць / фіксоване) · хто кому кидає тінь (вищий-або-рівний / строго вищий) · довжина тіні (= висота / константа) · ціна дій (фіксована / зростає зі споживанням шматків).

## Цікавинки для курсу
- Тінь на гекс-полі за напрямком сонця і висотою — 🥈 (6 векторів у кубових координатах, порівняння висот уздовж променя).
- Обертання джерела світла кожен раунд і перерахунок світла — 📎.
- Стадії росту як ланцюг трансформацій з цінами — 🌱.
- Дальність насіння за висотою (гекс-відстань ≤ h) + «раз на клітину за хід» — 📎.
- Планшет-драбина цін: купуєш знизу, повертаєш на верх — 🥉 (стек з цінами, економіка, що дорожчає).
- Стоси жетонів, що виснажуються (перший збирає більше) — 🌱.
- AI, що планує на 6 раундів уперед з урахуванням обертів тіні — 👑.

## Мапа на каталог
- Є: `cell-click` · `hover-highlight` · `legal-move-highlight` (клітини для насіння) · `turn-enforcement` · `hot-seat` · `ai-opponent` · `round-currency` (світло) · `event-points` · `game-settings`.
- **Нема** → пропозиції карток:
  - `+hex-grid-render` (як у Hex).
  - `+directional-shadow` «Напрямлена тінь за висотою» · entities/interact · 🥈 · слоти {dirs: 6, length: height, blocks: ≥}.
  - `+rotating-light-source` «Джерело, що обертається щораунду» · game-logic/waves · 📎 · слот {positions: 6}.
  - `+growth-stages` «Стадії росту з цінами» · entities/state · 🌱 · слот {stages: 4}.
  - `+seed-range-by-size` «Дальність розмноження за розміром» · entities/spawn · 📎.
  - `+once-per-cell-per-turn` «Клітина активується раз за хід» · entities/legality · 🌱.
  - `+depleting-score-stacks` «Стоси очок, що дешевшають» · game-logic/score · 🌱.
  - `+currency-cap` «Стеля валюти» · game-logic/economy · 🌱 · слот {max: 20}.
  - `+player-board-cost-track` «Планшет-драбина цін» · game-logic/economy · 🥉.
  - `+first-player-token` (як Azul) — перехід по колу.
  - `+revolution-timer` «Тривалість гри = N обертів» · game-logic/waves · 🌱.

## Пропозиції до словників
- `+cond:shaded(t)` — клітина/дерево в тіні від джерела з урахуванням висот.
- `+effect:grow` — шматок переходить на наступну стадію (родич `transform`, але з ціною й поверненням старого шматка в запас).
- `+effect:harvest` — зняти сутність і отримати жетон очок із місця (Photosynthesis; родич `pickup` навпаки).
- `+trigger:phase_start` · `+trigger:round_end` · `+effect:place` · `+cond:afford` · `+cond:in_range` · `+role:supply` · `+role:zone`.
- `+ui:sun-indicator` — позиція джерела світла; `+ui:shadow-overlay` — затінені клітини; `+ui:light-track` — трек валюти зі стелею; `+ui:score-stacks` — стоси очок із верхнім значенням.
- `+ui:opponent-boards` · `+window:match-setup`.
- `+card:directional-shadow` · `+card:rotating-light-source` · `+card:growth-stages`.

## Джерела
- ⭐ [UltraBoardGames: Photosynthesis rules](https://www.ultraboardgames.com/photosynthesis/game-rules.php) — тіні (1/2/3, лише на рівні або нижчі), світло 1/2/3, дії і ціни, дальність насіння 1/2/3, збір за 4, кінець, експерт.
- [BGA: Photosynthesis](https://en.boardgamearena.com/gamepanel?game=photosynthesis) — Hjalmar Hach, Blue Orange 2017, 2–4.
- [Wikipedia](https://en.wikipedia.org/wiki/Photosynthesis_(board_game)) — склад, фази, Under the Moonlight, Mensa Select.
- [Blue Orange](https://blueorangegames.com/index.php/games/photosynthesis) · [BGG 218603](https://www.boardgamegeek.com/boardgame/218603).
- YouTube: пошук «Photosynthesis board game how to play».

## Непевне
- (?) 37 клітин і розподіл кілець 1/6/12/18 — з геометрії й памʼяті, джерела числа не дають.
- (?) Ціни купівлі на планшеті (насіння 1,1,2,2 · малі 2,2,3,3 · середні 3,3,4 · великі 4,5) і значення жетонів (4 листки 22/21/20 …) — з памʼяті.
- (?) Чи можна садити насіння через зайняті клітини (UBG: «будь-який напрямок, з поворотами») — ймовірно, рахується лише гекс-відстань.
- (?) Цифрові версії поза BGA (застосунок?) — у Steam нема.
