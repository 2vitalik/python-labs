---
title: Mined-Out
slug: mined-out
aka: [Mined Out, Campo Minado, «Мінне поле»]
family: hidden-deduction
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: hidden
  random: setup
  goal: state
year: 1983
platforms: [ZX Spectrum 48K, Dragon 32, BBC Micro, Acorn Electron, Oric, Camputers Lynx]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mined-Out", best: true, note: "детектор по 4 сусідах, девʼять рівнів, Damsels, Mine Spreader, The Bug, зникання шляху з 6-го рівня, replay, звʼязок із Minesweeper"}
  - {kind: other, url: "https://worldofspectrum.org/archive/software/games/mined-out-quicksilva-ltd", note: "World of Spectrum: видання Quicksilva / Investronica («Campo Minado») / Microparadise, керування курсором, Currah Microspeech"}
  - {kind: other, url: "https://www.worldofspectrum.org//pub/sinclair/games-info/m/Mined-Out(MicroparadiseSoftware).txt", note: "текст перевидання: 9 рівнів, пауза, scoreboard, таблиця рекордів, Bugs, Mine Spreaders, «повторена дія»"}
  - {kind: other, url: "https://www.rzxarchive.co.uk/m/minedout.rzx", note: "RZX-запис проходження (потрібен емулятор)"}
  - {kind: other, url: "https://www.mobygames.com/game//14680", note: "MobyGames: версії й скриншоти"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mined-Out+ZX+Spectrum+gameplay", note: "пошук; геймплей Spectrum"}
stage: v1
coverage: 70
mechanics: [move-by-input, move-4dir, impassable-cells, neighbor-count-clue, touch-death, environment-death, player-death, reach-exit, item-pickup, event-points, time-bonus, chase-player, chase-greedy, sequential-levels, level-select, replay, score-records, leaderboard, game-pause, status-panel, game-screen, end-screen, help-window, attract-demo, keyboard-controls, sound-effects, reachability-check, no-guess-generation, +visited-trail, +trail-fade, +mine-spreader, +stalker-mine, +rescue-bonus-npc, +avatar-mine-detector]
proposes: ["+ui:mine-detector", "+feature:speech-output", "+card:visited-trail", "+card:trail-fade", "+card:mine-spreader", "+card:stalker-mine", "+card:rescue-bonus-npc", "+card:avatar-mine-detector"]
author: opus
date: 2026-11-09
---

# Mined-Out — пройди мінне поле знизу догори, бачачи лише, скільки мін поруч із тобою

## Суть
Гравець веде одну фігурку (аватар) мінним полем від входу внизу до виходу вгорі. Мін не видно; детектор щокроку показує, скільки мін у чотирьох сусідніх клітинах (вгору, вниз, ліворуч, праворуч), але не каже, де саме. Крок на міну — миттєва смерть; пройдений шлях лишається видимим і служить безпечним відступом. Це «сапер зсередини»: та сама математика сусідніх мін, що й у Minesweeper (1990), але інформацію гравець збирає власним тілом, а не кліками з висоти. Одна з девʼяти базових ігор курсу (база #6, `data/wiki/games/mined-out.md`).

## Поле і час
- Прямокутне поле-лабіринт, обнесене парканом; вхід — прохід унизу, вихід — угорі (у курсовій базі — стіна 🟪 з проходом). Рух лише ортогональний.
- Шари клітини: прихований вміст (порожньо / міна) + видимий шар (закрита / пройдений слід / видима міна після Spreader).
- Сусідство детектора — **4** (фон Неймана): діагоналі не рахуються. Тому підказка «бідніша», ніж у сапера з 8 сусідами, і вимагає більше обходів.
- Детектор — у верхній частині екрана, а не в клітині (у курсовій базі число малюється на самому аватарі 0️⃣–3️⃣).
- Час: аватар рухається на клітину за натиск; ліміту часу нема, але рахунок росте за швидкість, а з 4-го рівня гравця переслідує рухома міна The Bug — тому вісь `realtime` (світ живе й без вводу).
- Девʼять рівнів зростаючої складності; кожен вводить нову сутність або правило (див. таблицю).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Сапер (аватар) | player | 1 життя (?) | крок на 1 клітину в 4 напрямках; після кроку детектор показує кількість мін серед 4 сусідів |
| Закрита клітина | terrain | може ховати міну | прохідна; ступив — або слід, або вибух |
| Міна | hazard | невидима | контакт з аватаром → смерть; рахується детектором сусідніх клітин |
| Видима міна | hazard | після Spreader — крапка на екрані | та сама міна, але її видно; обходиться свідомо |
| Пройдений слід | mark | — | клітина, вже відвідана аватаром; гарантовано безпечна; з 6-го рівня зникає за спиною |
| Паркан / стіна | static | — | непрохідна межа поля |
| Вхід | static | прохід унизу | стартова позиція рівня |
| Вихід | static | прохід угорі | досяг — рівень пройдено |
| Damsel (дівчина-хробачок) | pickup | з 2-го рівня | дійти до неї — бонус до очок; не обовʼязково |
| Mine Spreader | spawner | з 3-го рівня, горизонтальна смуга | переносить міни вздовж горизонтального відрізка і робить їх видимими |
| The Bug | enemy | з 4-го рівня, «міна з лапками» | рухома міна, що переслідує аватара; дотик → смерть (?) |
| Bill the Worm | pickup | фінальна зона 9-го рівня | урятувати = пройти гру |
| Детектор мін | static (UI) | число 0–4 | показує `adjacent_count` по 4 сусідах поточної клітини |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `spawn_at(player, entrance)`, `custom: «розкласти приховані міни на полі»`, `timer(start)`.
- КОЛИ `input(move, dir)` → ЯКЩО `free(cell_ahead)` → ТО `move(player, dir)`; ЯКЩО `cell(cell_ahead, fence)` → ТО `block`.
- КОЛИ `leave(player, cell)` → ТО `mark(cell, trail)` — слід лишається видимим.
- КОЛИ `enter(player, cell)` → ЯКЩО `not cell(cell, mine)` → ТО `custom: «детектор := adjacent_count(cell, mine) по 4 сусідах»`.
- КОЛИ `enter(player, cell)` → ЯКЩО `cell(cell, mine)` → ТО `explode(cell)`, `lose`, `window(replay-window)`.
- КОЛИ `after(lose)` → ТО `reveal(all_mines)` (?) — показати, де були міни.
- КОЛИ `contact(player, damsel)` → ЯКЩО `level(>=, 2)` → ТО `pickup`, `score(bonus)`.
- КОЛИ `tick` → ЯКЩО `level(>=, 3)` → ТО `custom: «Spreader іде вздовж горизонтального відрізка й переносить міни»`, `reveal(moved_mines)`.
- КОЛИ `tick` → ЯКЩО `level(>=, 4)` → ТО `move(bug, toward(player))` — переслідування.
- КОЛИ `contact(bug, player)` → ТО `lose` (?).
- КОЛИ `leave(player, cell)` → ЯКЩО `level(>=, 6)` → ТО `custom: «слід за спиною зникає»` (`hide(trail)`); безпечний шлях назад треба памʼятати.
- КОЛИ `reach(player, exit)` → ТО `score(speed_bonus)`, `window(replay-window)`, `next_level`.
- КОЛИ `contact(player, bill)` → ЯКЩО `level(==, 9)` → ТО `win`.
- КОЛИ `input(pause)` → ТО `custom: «пауза»`.
- КОЛИ `game_over` → ЯКЩО `counter(score, >, hi_score_min)` → ТО `custom: «вписати в таблицю рекордів»`.
- Перемога: врятувати Bill the Worm на 9-му рівні. · Поразка: крок на міну (або дотик Bug). · Рахунок: очки за швидкість проходження рівня + бонуси за Damsels.

## Керування і ввід
- Чотири клавіші напрямку (Spectrum: курсорні клавіші, WoS — «Cursor only»); крок на одну клітину за натиск.
- Діагоналей нема — як і в детекторі.
- Пауза (за текстом перевидання Microparadise).
- Пройдені рівні можна обрати знову (переграти лабіринт).

## Вікна, меню, HUD
- `attract-demo` + `help-window`: перед сесією вантажиться демо та інструкції (рецензент Acorn User скаржився, що це обовʼязково щоразу).
- `game-screen`: поле з парканом, аватар, слід, видимі міни-крапки; вгорі `mine-detector` (число сусідніх мін), `score`, номер рівня (?).
- `replay-window`: миттєвий повтор після смерті або проходження рівня — програвання шляху аватара.
- `end-screen` / `leaderboard`: таблиця рекордів (high-score table, текст Microparadise).
- `level-select`: вибір уже пройденого лабіринту (?) — механізм вибору в джерелі не описаний.
- Переходи: демо/інструкції → `game-screen` → (міна) `replay-window` → новий захід / рекорди; (вихід) `replay-window` → наступний рівень.

## Фічі поза полем
- `levels-sequential` (9 рівнів) + переграти пройдений лабіринт (`mode-practice`-подібне).
- `replay` після кожної смерті/перемоги — рідкість для 1983 року.
- `leaderboard-local` — таблиця рекордів; `pause`.
- Мовлення через Currah Microspeech (синтез голосу на Spectrum).
- Написана на BASIC, не в машинних кодах — незвично для комерційної гри; цим вона близька до курсових реалізацій.

## Варіації й родичі
- Родичі в корпусі: [minesweeper](minesweeper.md) (той самий лічильник, але курсором і 8 сусідів), [hunt-the-wumpus](hunt-the-wumpus.md) (аватар відчуває небезпеку в сусідніх кімнатах), [dragonsweeper](dragonsweeper.md), [demoncrawl](demoncrawl.md), [kaboom](kaboom.md), [tametsi](tametsi.md), [hexcells](hexcells.md).
- Предки й сучасники за Wikipedia: Cube (1973), Minefield (Sinclair User, 1982); Mined-Out уточнила саме показ близькості мін. Розробник Microsoft Curt Johnson, за повідомленнями, казав, що основою Minesweeper був мак-клон Mined-Out.
- Курсові варіації (база #6): 4 vs 8 сусідів; життя/сканер на помилку; генерація, прохідна логікою; рухомі міни або вороги, що лишають міни; прапорці-припущення на полі.
- Осі варіацій:
  - **сусідство детектора**: 4 / 8 / радіус N / лише попереду;
  - **слід**: постійний / зникає (6-й рівень) / зникає через N кроків;
  - **міни**: статичні / переносяться (Spreader) / переслідують (Bug);
  - **мета**: дійти до виходу / зібрати Damsels / врятувати й вивести (Bill);
  - **ціна помилки**: смерть / життя / сканер-рятівник.

## Цікавинки для курсу
- Детектор по 4 сусідах для аватара (`adjacent_count` при кожному кроці) — 🌱: базова картка курсу «міношукач для гравця».
- Невидима міна + слід пройдених клітин + replay шляху — 📎: два шари клітини і список кроків як дані.
- Зникаючий слід з N-го рівня або через K кроків — 🌱: черга відвіданих клітин.
- The Bug — рухома міна, що женеться (жадібно або BFS) — 🥉: міна стає ворогом, детектор має рахувати і її.
- Mine Spreader — переносить міни вздовж ряду й робить їх видимими — 📎: сутність змінює прихований шар.
- Генерація поля з гарантованим шляхом від входу до виходу (BFS по безпечних клітинах) — 🥉; поле, прохідне **лише логікою** детектора без вгадувань — 🥇: солвер, що симулює знання аватара.
- Таблиця рекордів за швидкість + бонуси Damsels — 🌱.

## Мапа на каталог
- Є: `move-by-input` + `move-4dir` ↔ крок курсором · `impassable-cells` ↔ паркан · `neighbor-count-clue` ↔ детектор (4 сусіди) · `touch-death` / `environment-death` / `player-death` ↔ міна · `reach-exit` ↔ вихід угорі · `item-pickup` + `event-points` ↔ Damsels · `time-bonus` ↔ очки за швидкість · `chase-player` / `chase-greedy` ↔ The Bug · `sequential-levels` ↔ 9 рівнів · `level-select` ↔ переграти пройдене · `replay` ↔ instant replay · `score-records` + `leaderboard` ↔ рекорди · `game-pause` · `status-panel` ↔ детектор і очки · `attract-demo` + `help-window` ↔ демо й інструкції · `reachability-check`, `no-guess-generation` ↔ курсові ідеї генерації.
- **Нема** → пропозиції карток:
  - `+avatar-mine-detector` «Детектор сусідніх мін для аватара» · entities/state · 🌱 · слот {neighborhood: 4|8} — дитина `neighbor-count-clue`, але показ на аватарі/HUD, а не в клітині.
  - `+visited-trail` «Слід пройдених клітин» · entities/state · 🌱 — уже є в `catalog/tasks.yaml`, нема в автогені `catalog-cards.md`.
  - `+trail-fade` «Слід зникає за спиною» · entities/state · 🌱 · слот {after: 0|N кроків}.
  - `+mine-spreader` «Сутність переносить приховані обʼєкти й відкриває їх» · entities/move · 📎.
  - `+stalker-mine` «Рухома міна-переслідувач» · entities/move · 🥉 — небезпека з прихованого шару стає ворогом.
  - `+rescue-bonus-npc` «Необовʼязкова ціль-бонус на полі» · game-logic/score · 🌱.

## Пропозиції до словників
- `+ui:mine-detector` — число небезпек біля аватара в HUD (не в клітині); відрізняється від `remaining-counter`.
- `+feature:speech-output` — синтез голосу/озвучення подій (Currah Microspeech).
- Картки: `+card:avatar-mine-detector`, `+card:visited-trail`, `+card:trail-fade`, `+card:mine-spreader`, `+card:stalker-mine`, `+card:rescue-bonus-npc` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Mined-Out](https://en.wikipedia.org/wiki/Mined-Out) — геймплей: 4 сусіди без діагоналей, знизу догори, 9 рівнів, Damsels (2), Mine Spreader (3), The Bug (4), зникання шляху (6), replay, очки за швидкість; розробка на BASIC; Cube і Minefield як предки; звʼязок із Microsoft Minesweeper.
- [World of Spectrum: Mined-Out](https://worldofspectrum.org/archive/software/games/mined-out-quicksilva-ltd) — видавці й назви (Quicksilva «Mined Out», Investronica «Campo Minado», Microparadise), керування курсором, Currah Microspeech.
- [Інструкція Microparadise (txt)](https://www.worldofspectrum.org//pub/sinclair/games-info/m/Mined-Out(MicroparadiseSoftware).txt) — 9 рівнів, пауза, scoreboard, таблиця рекордів, Bugs («міни з лапками»), Mine Spreaders.
- [RZX Archive: проходження](https://www.rzxarchive.co.uk/m/minedout.rzx) — запис для емулятора.
- [MobyGames](https://www.mobygames.com/game//14680) — каталожна сторінка.
- Курсові описи: `data/wiki/games/mined-out.md`, `data/v2/notion/games/6-mined-out.md` (приклади поля емодзі, базові завдання).
- YouTube: пошук «Mined-Out ZX Spectrum gameplay».

## Непевне
- (?) Чи гравець має кілька життів — Wikipedia про життя мовчить, лише «миттєва смерть»; у таблиці стоїть 1 життя.
- (?) Розкладка мін: випадкова на кожен захід чи фіксована на рівень — не перевірено; `random: setup` — припущення.
- (?) Що саме робить The Bug при дотику (смерть як від міни — найімовірніше) і як він рухається (жадібно до гравця чи інакше).
- (?) Чи показуються всі міни після смерті; чи замість цього це робить лише replay.
- (?) Що додають рівні 5, 7, 8 — у джерелах не знайдено (зі спогадів — «вітер», що зносить аватара, але без підтвердження).
- (?) Що таке «Acción repetida» / «повторена дія» в інструкції Microparadise — можливо, автоповтор клавіші або replay.
- (?) Як саме обирається пройдений лабіринт для повторної гри і чи HUD показує номер рівня.
