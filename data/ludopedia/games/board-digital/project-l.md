---
title: Project L
slug: project-l
aka: [Проєкт L]
family: board-digital
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: runtime
  goal: score
year: 2020
platforms: [board]
links:
  - {kind: other, url: "https://rulespal.com/project-l/rulebook", best: true, note: "повні правила: 5 дій, нагорода за пазл, кінець, штрафи, соло, Ghost Piece"}
  - {kind: bgg, url: "https://boardgamegeek.com/boardgame/260180/project-l", note: "BGG (403 для фетчу, не відкривав)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Project+L+board+game+how+to+play", note: "пошук; правила"}
stage: v1
coverage: 70
mechanics: [polyomino-placement, piece-rotate-flip, drag-drop-piece, hover-highlight, legal-move-highlight, completion-detection, hot-seat, turn-enforcement, ai-opponent, event-points, leftover-penalty, rule-variants, game-settings, game-screen, end-screen, help-window, +polyomino-engine-building, +piece-upgrade-ladder, +action-points-turn, +once-per-turn-master-action, +market-row-recycle, +last-round-trigger, +hand-limit-puzzles, +supply-tiebreak]
proposes: ["+trigger:area_complete", "+effect:return_pieces", "+effect:upgrade_piece", "+cond:actions_left", "+role:puzzle-card", "+ui:action-pips", "+ui:puzzle-slots", "+feature:solo-bot-deck"]
author: opus
date: 2026-11-09
---

# Project L — поліоміно як двигун: заповнений пазл повертає фігури і дає нову, більшу

## Суть
Кожен гравець бере картки-пазли з вирізаною формою (recess) і заповнює їх своїми поліоміно-фігурами. Розвʼязаний пазл повертає всі вкладені фігури назад у запас **і** дає фігуру-нагороду, тож запас росте — класичний «двигун» (engine building), де ресурс — самі поліоміно. Хід — 3 дії з пʼяти; одна з них, «Майстер», раз за хід кладе по фігурі в кожен свій пазл. Наприкінці: очки за розвʼязані пазли мінус вартість недороблених.

## Поле і час
- Поля нема: кожен пазл — окреме маленьке поле (картка з вирізом-поліоміно), у гравця одночасно ≤4 недороблених пазлів.
- Спільний стіл: два ряди по 4 відкритих пазли — білі (дешеві) і чорні (дорогі) — над закритими колодами; резерв фігур 9 форм × 15.
- Запас гравця — фігури поза полем; вкладена в пазл фігура лишається там до розвʼязання.
- Покроково за годинниковою стрілкою; хід = рівно 3 дії в будь-якому порядку, дії можна повторювати (крім Майстра).
- Кінець: колода чорних пазлів порожня → дограти коло + ще одне фінальне коло, щоб усі мали порівну ходів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фігура рівня 1–4 | piece | форма-поліоміно, рівень (за розміром) | береться з резерву, вкладається в пазл з поворотом/дзеркалом |
| Резерв фігур | supply | 9 форм × 15 | джерело Upgrade і нагород; бракує форми → така сама за рівнем, далі на рівень вище чи будь-яка нижча |
| Запас гравця | supply | фігури без ліміту | з нього Place і Master |
| Білий пазл | container | виріз-форма, очки, фігура-нагорода | 32 у колоді, 4 відкриті в ряду |
| Чорний пазл | container | виріз більший, очки вищі, нагорода | 20 у колоді, у грі 12–24 за кількістю гравців; порожня колода = кінець |
| Ряд пазлів | zone | 4 відкриті | після взяття поповнюється з колоди; Recycle — увесь ряд під низ колоди |
| Купка очок | zone | розвʼязані пазли лицем донизу | рахуються наприкінці |
| Ghost-фігура (розширення) | piece | рівень 5, 3 форми | дає дію Ghost: обміняти на фігури тієї ж форми |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `custom: «3 дії в будь-якому порядку»` (`+cond:actions_left`).
- Take: КОЛИ `input(take(puzzle))` → ЯКЩО `count(own_unfinished_puzzles, <, 4)` → ТО `give(player, puzzle)` і `spawn_at(puzzle, row_slot)` з колоди; можна взяти верхню закриту.
- Recycle: КОЛИ `input(recycle(row))` → ТО `custom: «усі 4 пазли ряду під низ колоди, відкрити 4 нові»`.
- Upgrade A: КОЛИ `input(upgrade_new)` → ТО `give(player, piece_level1)`.
- Upgrade B: КОЛИ `input(upgrade(piece))` → ТО `take(player, piece)` і `give(player, custom: «фігура того ж рівня, нижчого або на 1 вищого»)` (`+effect:upgrade_piece`).
- Place: КОЛИ `input(place(piece, puzzle, cells))` → ЯКЩО `fits(piece, cells)` і `custom: «усі клітини в межах вирізу, без накладання»` → ТО `place(piece, cells)`; інакше `block`.
- КОЛИ `input(rotate(piece))` → ТО `rotate(piece, 90)`; дзеркало дозволене.
- Master: КОЛИ `input(master)` → ЯКЩО `first_time` (за хід) → ТО `custom: «по одній фігурі з запасу в кожен свій недороблений пазл»`.
- КОЛИ `custom: «виріз пазла заповнено повністю»` (`+trigger:area_complete`) → ТО `custom: «усі фігури з пазла назад у запас»` (`+effect:return_pieces`), `give(player, reward_piece)`, `custom: «пазл на купку очок»`.
- Одна дія може розвʼязати кілька пазлів (Master) — нагорода за кожен.
- КОЛИ `custom: «колода чорних порожня»` → ТО `custom: «дограти коло + фінальне коло»`; чорні більше не поповнюються, ≤1 чорний за хід.
- Доведення (Finishing Touches): КОЛИ `game_over` → ТО `custom: «можна вкласти фігури із запасу за звичайними правилами»`, `score(-1)` за кожну; пазл, розвʼязаний тут, нагороди не дає.
- Рахунок: `score(+points)` за пазли на купці · `score(-points)` за кожен недороблений · `score(-1)` за фігуру доведення.
- Нічия: більше розвʼязаних пазлів → більше фігур у запасі → спільна перемога.
- Перемога: найбільше очок · Поразка: — .

## Керування і ввід
- Настільна: вибір дії, вибір фігури із запасу, поворот/дзеркало, вкладання у виріз.
- (цифрова версія) Перетягнути фігуру з `piece-tray` на пазл (`drag-drop-piece`), колесо/клавіша — поворот, ПКМ — дзеркало; фантом показує, чи вміщається.
- Лічильник дій (3 піпки); кнопка Master відкриває режим «по фігурі в кожен пазл» з підтвердженням.
- Upgrade — клік по фігурі запасу → вибір із легальних замін (той самий рівень / нижчий / +1).

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Нова гра · Соло · Правила · Налаштування.
- `match-setup`: кількість гравців (1–6), розширення Ghost Piece, варіанти Line Clear (5–6 гравців) і Endless White Deck; у соло — складність (6/3/0 стартових фігур бота).
- `game-screen`: ряди білих і чорних пазлів з очками й нагородою; свої `puzzle-slots` (≤4); `piece-tray` — запас фігур; `action-pips`; `score-preview` і `opponent-boards`; `turn-indicator`.
- `custom-window`: вибір заміни при Upgrade; розподіл фігур дією Master.
- `end-screen`: розклад очок (розвʼязані, −недороблені, −доведення) і тай-брейк.
- `help-window`: 5 дій і таблиця рівнів фігур.
- Переходи: main-menu → match-setup → game-screen ⇄ custom-window → end-screen.

## Фічі поза полем
- `custom-rules`: Ghost Piece, Line Clear, Endless White Deck; кількість чорних пазлів від кількості гравців.
- Соло: колода-бот у сітці 3×3, фігури над стовпцями як «замки», бот бере найдорожчий доступний пазл; складність 6/3/0 стартових фігур; Recycle заборонено.
- `rules-page`, `undo` у межах ходу (цифрова версія).

## Варіації й родичі
- **Ghost Piece** — фігури рівня 5 і 24 нові пазли; **Finesse** (?), Phoenix (?) — інші розширення.
- Родичі: Ubongo (`ubongo.md`, швидке заповнення форми), Patchwork (`patchwork.md`), Bärenpark (`barenpark.md`, нагорода за покриття), The Isle of Cats (`the-isle-of-cats.md`), Blokus (`blokus.md`), FITS (`fits.md`); Splendor — той самий двигун «купи → отримай знижку назавжди».
- **Осі варіацій**: куди кладуть фігури (одне велике поле / багато маленьких пазлів) · фігури після заповнення (лишаються / повертаються) · звідки нові (купівля / нагорода за пазл / апгрейд) · штраф (порожні клітини / вартість недоробленого).

## Цікавинки для курсу
- «Повернення фігур + нагорода» як цикл двигуна: стан гравця = мультимножина фігур — 📎.
- Перевірка «фігура лягає у виріз» з 8 орієнтаціями — 📎 (той самий код, що Blokus, але на маленькому полі).
- Розвʼязник «чи можна заповнити пазл моїм запасом» — точне покриття з мультимножиною фігур — 🥈 (backtracking / DLX).
- Хід як 3 дії з обмеженням «Master раз за хід» — 🌱.
- Upgrade-драбина рівнів з підміною при порожньому резерві — 🌱.
- Соло-бот з колодою і «замками» — 🥉.
- AI, що планує 3 дії й оцінює ризик недороблених пазлів наприкінці — 🥇.

## Мапа на каталог
- Є: `polyomino-placement` · `piece-rotate-flip` · `drag-drop-piece`, `hover-highlight`, `legal-move-highlight` · `completion-detection` ↔ виріз заповнено · `hot-seat`, `turn-enforcement`, `ai-opponent` · `event-points` · `leftover-penalty` ↔ −очки недороблених · `rule-variants`, `game-settings` · `game-screen`, `end-screen`, `help-window`.
- **Нема** → пропозиції карток:
  - `+polyomino-engine-building` «Поліоміно-двигун: заповнене повертає фігури й дає нову» · game-logic/economy · 📎.
  - `+piece-upgrade-ladder` «Обмін фігури на рівень вище» · game-logic/economy · 🌱 · слот {step: +1}.
  - `+action-points-turn` «Хід = N дій з меню» · game-logic/opponent · 🌱 · слот {n: 3}.
  - `+once-per-turn-master-action` «Сильна дія раз за хід» · game-logic/opponent · 🌱.
  - `+market-row-recycle` «Скинути весь відкритий ряд і відкрити новий» · game-logic/economy · 🌱.
  - `+last-round-trigger` · `+supply-tiebreak` (як у Bärenpark) · `+hand-limit-puzzles` «≤N незавершених цілей одночасно» · 🌱.

## Пропозиції до словників
- `+trigger:area_complete` — виріз/ділянка заповнена повністю (як у Bärenpark).
- `+effect:return_pieces` — фігури з розвʼязаного пазла повертаються в запас власника.
- `+effect:upgrade_piece` — обміняти фігуру на іншу за драбиною рівнів.
- `+cond:actions_left` — у ході лишились дії (хід з N дій).
- `+role:puzzle-card` — картка-ціль з власним маленьким полем.
- `+ui:action-pips` — лічильник дій ходу; `+ui:puzzle-slots` — слоти незавершених цілей гравця.
- `+feature:solo-bot-deck` — соло-суперник на колоді/правилах без AI.

## Джерела
- ⭐ [RulesPal: Project L rulebook](https://rulespal.com/project-l/rulebook) — компоненти (32 білі, 20 чорних, 9 форм × 15), підготовка, 5 дій, нагорода, кінець, Finishing Touches, рахунок, тай-брейк, соло, Line Clear, Ghost Piece, Endless White Deck.
- BGG: [Project L](https://boardgamegeek.com/boardgame/260180/project-l) (403).
- YouTube: пошук «Project L board game how to play».

## Непевне
- (?) ⭐ з черги (ultraboardgames.com/project-l/game-rules.php) веде на головну UBG — замінено на RulesPal.
- (?) Розподіл 9 форм за рівнями (1 — мономіно, 2 — доміно, 3 — 2 тріоміно, 4 — 5 тетраміно) — з памʼяті; джерело каже лише «рівні 1–4 за розміром».
- (?) Автори (Michal Mikeš, Jan Soukal, Adam Španěl) і видавець (Boardcubator) — з памʼяті.
- (?) Цифрової версії не знайдено (BGA-сторінка `projectl` віддала 500) — вікна гіпотетичні.
- (?) Розширення Finesse і Phoenix — RulesPal згадує Phoenix лише мимохідь; зміст не перевірено.
