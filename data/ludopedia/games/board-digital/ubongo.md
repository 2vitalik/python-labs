---
title: Ubongo + Katamino / IQ Puzzler (Убонго)
slug: ubongo
family: board-digital
also: [thinky]
klass: puzzle
axes:
  field: square
  time: realtime
  opponent: hotseat
  info: full
  random: runtime
  goal: race
year: 2003
platforms: [board, PC, mobile]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/ubongo/game-rules.php", best: true, note: "повні правила Ubongo: 36 карток / 432 задачі, 3 або 4 фігури, кубик, пісочний годинник, друга спроба, самоцвіти, 9 раундів, тай-брейк, соло"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Ubongo", note: "Grzegorz Rejchtman, Pyramidens Portar 2003, Kosmos 2005; самоцвіти за місцем"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pentomino", note: "12 пентаміно, кількість розвʼязків прямокутників (6×10 — 2339), Knuth / Dancing Links"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dancing_Links", note: "Algorithm X / DLX для exact cover — розвʼязувач задач-укладок"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Gigamic", note: "видавець Katamino"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Ubongo", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Ubongo+board+game+how+to+play", note: "пошук; пояснення правил"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Katamino+pentomino+puzzle", note: "пошук; Katamino"}
stage: v1
coverage: 75
mechanics: [drag-drop-piece, hover-highlight, completion-detection, satisfy-constraints, time-out, time-bonus, event-points, level-bank, level-solver, difficulty-levels, unique-puzzle-generation, score-records, game-settings, hot-seat, +polyomino-placement, +piece-rotate-flip, +exact-cover-outline, +piece-subset-by-die, +speedsolve-timer, +race-to-pattern, +simultaneous-turns, +finish-order-reward, +random-gem-draw, +second-chance-timer, +shrinking-reward-track, +best-color-set-win, +width-slider-challenge]
proposes: ["+trigger:all_constraints_met", "+trigger:timer", "+trigger:input", "+effect:place", "+effect:rotate", "+effect:mirror", "+effect:give", "+cond:fits", "+cond:covers_exactly", "+role:piece", "+role:zone", "+role:supply", "+ui:piece-tray", "+ui:timer-countdown", "+ui:finish-order", "+window:puzzle-select", "+feature:mode-time-attack", "+feature:puzzle-bank", "+axis:turn-structure=simultaneous"]
author: opus
date: 2026-11-02
---

# Ubongo — на швидкість укласти задані поліоміно рівно в контур картки, поки сиплеться пісок

## Суть
Усі гравці **одночасно** розвʼязують по пазлу-укладці: на картці світлий контур, кидок кубика визначає 3 або 4 фігури-поліоміно з набору гравця, і їх треба вкласти без перекриттів і виступів, з поворотами й дзеркалами. Хто встиг до кінця пісочного годинника — бере самоцвіти; перший — більше. Katamino і IQ Puzzler — соло-родичі тієї ж задачі «exact cover» без таймера, з поступовою складністю.

## Поле і час
- Поле кожного гравця — картка-задача: контур з квадратних клітин (≈ 10–16 клітин) (?); сторона 3 фігур (легка) або 4 (важка).
- **Real-time**: раунд триває один пісочний годинник (~1 хв (?)); якщо ніхто не встиг — друга спроба з перевернутим годинником.
- Хід — одночасний для всіх; 9 раундів. Спільна зона — доріжка самоцвітів (2 ряди по 9: сапфіри й бурштини), мішок самоцвітів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фігура-поліоміно | piece | форма (3–5 клітин (?)), колір; 12 у наборі гравця | обертається, віддзеркалюється, кладеться в контур |
| Картка-задача | zone | контур; 6 рядків «символ → набір фігур»; легка/важка сторона | ціль: точне покриття контуру обраними фігурами |
| Кубик | supply | 6 символів | вибирає рядок картки (який набір фігур) |
| Пісочний годинник | static | 1 «тік» раунду | після спливу — «Стоп!» |
| Доріжка самоцвітів | supply | 9 сапфірів + 9 бурштинів | лічильник раундів і нагороди 1-го / 2-го |
| Самоцвіт | resource | червоний 4 · синій 3 · зелений 2 · бурий 1 (за правилами UBG); 58 | очки в кінці |
| Мішок самоцвітів | supply | випадковий самоцвіт | +1 кожному, хто встиг |
| Katamino: поле з повзунком | zone | 5 рядків × N стовпців, N задає повзунок (?) | укласти N обраних пентаміно рівно в прямокутник 5×N |
| IQ Puzzler: дошка з префіксом | zone | частина фігур уже покладена (задача з книжки) (?) | заповнити решту клітин |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `round_start` → ТО кожен бере нову картку; кидок кубика + перевертання годинника; `timer(start)`.
- КОЛИ `input(place(piece, cells, rot, flip))` → ЯКЩО `fits(piece, outline)` and `free(cells)` → ТО `place`; фігура не може виступати за контур.
- КОЛИ `all_constraints_met` (усі фігури набору покладені, контур покритий без дір) → ТО гравець кричить «Ubongo!» і отримує місце в черзі фінішу; інші продовжують.
- КОЛИ `timer(==, 0)` → ЯКЩО ніхто не фінішував → ТО друга спроба (годинник ще раз); ЯКЩО знову ніхто → раунд без нагород.
- КОЛИ `custom: «раунд закінчено»` → ТО нагороди за місцем: 1-й — сапфір з доріжки + випадковий з мішка; 2-й — бурштин з доріжки + випадковий; 3-й і 4-й — випадковий з мішка; хто не встиг — нічого.
- КОЛИ `round_end` → ТО з доріжки знімається пара (сапфір + бурштин); один фінішер — знімається лише бурштин (у мішок); ніхто — обидва в мішок.
- КОЛИ `counter(track_gems, ==, 0)` (після 9 раундів) → ТО `game_over`; переможець — найбільша сума очок самоцвітів (UBG) / найбільше самоцвітів одного кольору (Вікі, старіша редакція (?)).
- Тай-брейк: нова картка, кидок, без годинника — хто перший розвʼязав.
- Соло: максимум задач за 5/10/20 хв або мінімум часу на 5/10/20 задач; застряг — відклади й візьми нову.
- Katamino / IQ Puzzler: КОЛИ `all_constraints_met` → ТО `next_level` (задача з банку); часу нема.

## Керування і ввід
- Цифрова версія: drag фігури з лотка на поле; правий клік / кнопка / свайп двома пальцями — поворот на 90°; окрема кнопка або подвійний клік — дзеркало; фігура «прилипає» до сітки, недопустиме положення підсвічується червоним.
- Повернення фігури в лоток — drag назад; «Ubongo!» — автоматично при повному покритті.
- Мультиплеєр — усі одночасно, кожен на своєму пристрої/половині екрана; гарячі клавіші для повороту/дзеркала на ПК (?).

## Вікна, меню, HUD
- `main-menu` (цифрова версія): Партія (2–4) / Соло на час / Соло на кількість / Банк задач / Правила.
- `match-setup`: гравці, складність (3 чи 4 фігури), кількість раундів.
- `game-screen`: контур задачі, `piece-tray` (12 фігур, потрібні підсвічені за символом кубика), `timer-countdown` (пісок), `finish-order` (хто вже крикнув Ubongo), доріжка самоцвітів, `score`.
- `puzzle-select` (Katamino/IQ Puzzler): сітка задач за рівнями з позначками «розвʼязано».
- `end-screen`: самоцвіти й очки; соло — кількість задач / час і рекорд.
- Переходи: main-menu → match-setup → game-screen ×9 → end-screen; main-menu → puzzle-select → game-screen.

## Фічі поза полем
- `mode-time-attack` (соло на 5/10/20 хв), `mode-speedrun` (час на N задач), `puzzle-bank` (432 задачі; Katamino/IQ Puzzler — сотні з книжки), `difficulty-presets` (3 / 4 фігури; Katamino — ширина прямокутника), `hint` (показати одну фігуру на місці) (?), `show-solution`, `stats`/`leaderboard-local` найкращих часів.
- Генератор задач: вибрати набір фігур, скласти з них форму, контур = обрис; перевірити, що розвʼязок є (і бажано не тривіальний) — природна фіча цифрової версії.

## Варіації й родичі
- Ubongo Extreme (шестикутні фігури), Ubongo Trigo (трикутні), Ubongo 3D (будувати 2 поверхи), Ubongo Junior (?) — посилання на сторінках UBG, без правил.
- Katamino (Gigamic): 12 пентаміно, прямокутник 5×N з повзунком; IQ Puzzler Pro (SmartGames): 2D-дошка і 3D-піраміда з книжкою задач (?).
- Родичі: Blokus і Patchwork (поліоміно на полі), Tetris (укладка без вибору фігур), Project L (поліоміно як економіка), танграм, класичний пентаміно-прямокутник 6×10.
- **Осі варіацій**: форма клітин (квадрат / гекс / трикутник) · вимір (2D / 2 шари / 3D-піраміда) · фігури (задані кубиком / обираєш сам / усі) · час (пісок / без часу / на рекорд) · змагання (одночасна гонка / соло-банк).

## Цікавинки для курсу
- Перевірка точного покриття: множина клітин контуру = обʼєднання фігур без перетинів — 📎.
- 8 орієнтацій поліоміно (повороти × дзеркало) з нормалізацією для дедуплікації — 📎.
- Розвʼязувач exact cover (backtracking → Algorithm X / Dancing Links) — 🥇: класика, 6×10 має 2339 розвʼязків.
- Генератор задач з гарантованим розвʼязком (склади фігури → обріз контуру) — 🥈; з оцінкою складності/єдиності — 👑.
- Одночасна гонка з порядком фінішу й нагородами за місце + друга спроба таймера — 🥉.
- Drag + поворот + дзеркало з прилипанням до сітки — 🥉 (UI-завдання).

## Мапа на каталог
- Є: `drag-drop-piece` · `hover-highlight` · `completion-detection` · `satisfy-constraints` · `time-out` · `time-bonus` (порядок фінішу) · `event-points` · `level-bank` · `level-solver` · `difficulty-levels` · `unique-puzzle-generation` (генератор задач) · `score-records` · `game-settings` · `hot-seat`.
- **Нема** → пропозиції карток:
  - `+polyomino-placement` · `+piece-rotate-flip` — як у Blokus.
  - `+exact-cover-outline` «Укласти набір фігур рівно в контур» · game-logic/constraints · 📎 · слоти {pieces: 3|4, outline}.
  - `+piece-subset-by-die` «Кубик обирає, які фігури треба використати» · game-logic/difficulty · 🌱.
  - `+speedsolve-timer` · `+race-to-pattern` — як у п'ятнашках; тут пісочний годинник і гонка кількох гравців.
  - `+simultaneous-turns` — як у Take It Easy; тут real-time.
  - `+finish-order-reward` «Нагорода за місцем фінішу» · game-logic/score · 🌱 · слоти {rewards: [2, 2, 1, 1]}.
  - `+random-gem-draw` «Випадкова нагорода з мішка» · game-logic/economy · 🌱.
  - `+second-chance-timer` «Нікому не вдалось — друга спроба» · game-logic/lose · 🌱.
  - `+shrinking-reward-track` «Доріжка нагород = лічильник раундів» · game-logic/waves · 🌱.
  - `+best-color-set-win` «Переможець — найбільше одного кольору» · game-logic/win · 🌱 (старіша редакція (?)).
  - `+width-slider-challenge` «Розмір задачі задається повзунком» · game-logic/difficulty · 🌱 — Katamino.

## Пропозиції до словників
- `+trigger:all_constraints_met` (уже ⏳) — «Ubongo!»; `+trigger:timer` — кінець піску.
- `+effect:place` · `+effect:rotate` · `+effect:mirror` — дзеркало фігури окремо від повороту · `+effect:give` (самоцвіт).
- `+cond:fits` · `+cond:covers_exactly` — контур покрито повністю без виступів (сильніше за `fits`).
- `+role:piece` · `+role:zone` (контур) · `+role:supply` (доріжка, мішок).
- `+ui:piece-tray` · `+ui:timer-countdown` · `+ui:finish-order` — хто й у якому порядку фінішував.
- `+window:puzzle-select` · `+feature:mode-time-attack` · `+feature:puzzle-bank`.
- `+axis:turn-structure=simultaneous` — одночасна гонка без черги.

## Джерела
- ⭐ [UltraBoardGames: Ubongo rules](https://www.ultraboardgames.com/ubongo/game-rules.php) — склад (48 фігур, 36 карток/432 задачі, доріжка 9+9, 58 самоцвітів 4/3/2/1), раунд, друга спроба, нагороди, 9 раундів, тай-брейк, соло.
- [Wikipedia: Ubongo](https://en.wikipedia.org/wiki/Ubongo) — автор, історія видань, самоцвіти за місцем, переможець за одним кольором.
- [Wikipedia: Pentomino](https://en.wikipedia.org/wiki/Pentomino) — 12/18/63 пентаміно, кількість розвʼязків прямокутників, Knuth.
- [Wikipedia: Dancing Links](https://en.wikipedia.org/wiki/Dancing_Links) — Algorithm X для exact cover.
- [Wikipedia: Gigamic](https://en.wikipedia.org/wiki/Gigamic) — видавець Katamino.
- BGG: пошук «Ubongo»; YouTube: пошуки «Ubongo how to play», «Katamino».

## Непевне
- (?) Тривалість пісочного годинника (~1 хв) і розміри фігур/контурів — у джерелах не названо.
- (?) Умова перемоги розходиться: UBG — сума очок самоцвітів (4/3/2/1), Вікі — найбільше самоцвітів одного кольору (ймовірно, різні редакції).
- (?) Цифрові версії (ПК/консолі ~2008, мобільна від Kosmos) — з памʼяті; Steam-пошук «ubongo» — 0 результатів.
- (?) Деталі Katamino (повзунок, 5×N) та IQ Puzzler Pro (2D + 3D-піраміда, книжка задач) — з памʼяті, окремих статей Вікі нема.
