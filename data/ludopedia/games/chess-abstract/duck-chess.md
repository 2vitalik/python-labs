---
title: Duck Chess (Качині шахи)
slug: duck-chess
aka: [Шахи з качкою, Duck chess]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 2016
platforms: [board, web]
links:
  - {kind: other, url: "https://www.chess.com/terms/duck-chess", best: true, note: "Chess.com: правила одним екраном — хід + переставити качку, кінь перестрибує, шаху нема, взяття короля, пат = перемога запатованого"}
  - {kind: official, url: "https://duckchess.com/", note: "офіційні правила Тіма Полдена: качку не можна лишити на місці й не можна взяти; правило «fowling»; нотація Qxh7@g5"}
  - {kind: other, url: "https://www.houseofstaunton.com/chess-blog/what-is-duck-chess/", note: "стаття: правила, стратегія (качка як щит), історія вірусності 2022, нотація"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=duck+chess+explained", note: "пошук; пояснення й партії"}
stage: v1
coverage: 80
mechanics: [piece-move-patterns, piece-capture, impassable-cells, legal-move-highlight, drag-drop-piece, cell-click, turn-enforcement, hot-seat, move-timer, ai-opponent, online-multiplayer, castling, en-passant, pawn-promotion, move-notation, last-move-highlight, game-screen, end-screen, +king-capture-win, +stalemate-win, +neutral-blocker, +shared-piece, +two-part-turn, +mandatory-relocate, +rule-variants]
proposes: ["+trigger:move_done", "+cond:not_same_cell", "+effect:relocate", "+role:shared", "+ui:duck-ghost", "+ui:turn-phase", "+axis:win-condition", "+card:shared-blocker", "+card:two-part-turn"]
author: opus
date: 2026-11-09
---

# Duck Chess — звичайні шахи, але після кожного ходу ти мусиш переставити нейтральну качку, що блокує клітину для обох

## Суть
Шахи з однією додатковою фігурою — **качкою**, яка не належить нікому. Хід складається з двох частин: звичайний шаховий хід і обовʼязкове перенесення качки на будь-яку іншу порожню клітину. Качка блокує свою клітину: ніхто не може на неї стати чи пройти крізь, лише кінь перестрибує. Через це шах втрачає сенс — супротивник завжди може закрити загрозу качкою або поставити її так, щоб заблокувати твій захист, тож **шаху й мату нема**, мета — взяти короля, а запатований гравець виграє.

## Поле і час
- Стандартна шахова дошка 8×8, стандартна розстановка.
- Додатково — одна качка (нейтральний блокер); до першого ходу її на дошці нема (?).
- Покроково; хід = **дві фази**: шаховий хід → переставити качку. Годинник зупиняється лише після другої фази.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Король | piece | сторона | ходить як у шахах; **може** йти під удар і рокіруватись через биті поля; узяття = поразка |
| Ферзь, тура, слон | piece | сторона | ходять лініями; качка на шляху зупиняє лінію |
| Кінь | piece | сторона | ходить як у шахах; єдиний перестрибує качку |
| Пішак | piece | сторона | як у шахах; качка попереду блокує хід уперед; перетворення як у шахах (?) |
| Качка | neutral | 1 на дошці, нічия | займає клітину; не може бути взята; після кожного ходу переставляється на **іншу** порожню клітину тим, хто ходив |
| Клітина | terrain | порожня / фігура / качка | качка робить клітину непрохідною для всіх, крім стрибка коня |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move(piece, to))` → ЯКЩО `turn_of(side)` and `legal(move)` → ТО `move(piece, to)` (взяття — `disappear_b`); фаза 2.
- `legal(move)`: шаховий патерн фігури · ЯКЩО `occupied(path_or_target, duck)` and `not custom: «фігура — кінь»` → ТО `block`.
- Шаху нема: КОЛИ `input(move(king, attacked_cell))` → ТО `move` дозволено; хід, що лишає короля під ударом, легальний.
- Рокіровка: ЯКЩО `custom: «король і тура не ходили»` and `free(cells_between)` → ТО рокіровка дозволена; перевірок «через бите поле» нема; качка між ними блокує.
- КОЛИ `custom: «шаховий хід виконано»` → ТО `input(duck_to)` обовʼязково → ЯКЩО `free(duck_to)` and `custom: «duck_to ≠ поточна клітина качки»` → ТО `move(duck, duck_to)`, `end_turn`; інакше `block`.
- Перший хід партії: `place(duck)` на будь-яку порожню клітину (?).
- КОЛИ `contact(piece, enemy_king)` (взяття короля) → ТО `win`.
- КОЛИ `turn_start(side)` → ЯКЩО `no_moves(side)` (навіть король не має куди піти, бо все заблоковано фігурами й качкою) → ТО `win(side)` — правило «fowling»: запатований виграє.
- Взяття на проході й перетворення пішака — як у звичайних шахах (?).
- Нічия: повторення / правило 50 ходів / згода — як у шахах (?).
- Нотація: шаховий хід + `@` + клітина качки, напр. `Qxh7@g5`; знаків шаху й мату нема.
- Перемога: взяти короля або бути запатованим · Поразка: втратити короля або запатувати суперника.

## Керування і ввід
- Фаза 1: drag або клік фігури → клік цілі (підсвічені легальні клітини; качка виключена з ліній).
- Фаза 2: drag/клік качки → клік на будь-яку порожню клітину, крім поточної; без цього хід не завершується.
- Скасування перед підтвердженням — лише в режимі аналізу (?); premove складний, бо треба вгадати обидві фази.

## Вікна, меню, HUD
(цифрова версія — Chess.com Variants)
- `main-menu` → `mode-select`: Duck Chess серед варіантів; контроль часу.
- `lobby-window`: пошук суперника, рейтинг варіанта.
- `game-screen`: дошка з качкою, `turn-phase` («ходи фігурою» / «переставь качку»), `duck-ghost` під курсором у фазі 2, `player-clock`, `move-list` з `@`-нотацією, `last-move-highlight` (фігура + качка), `captured-pieces`.
- `end-screen`: «король узятий» / «fowled» + рейтинг.
- `help-window`: правила варіанта.
- Переходи: lobby → game-screen → end-screen → replay-window / lobby.

## Фічі поза полем
- `online-multiplayer` з окремим рейтингом варіанта, `turn-timer` (шаховий годинник), `ai-opponent-levels` (рушії Fairy-Stockfish-подібні) (?).
- `replay` і аналіз партій, `export-import` нотації з `@`.
- `custom-rules`: Duck Chess як перемикач у конструкторі варіантів.

## Варіації й родичі
- Абзац про Duck Chess є в [chess-rule-twists.md](chess-rule-twists.md) (поруч з Kung-Fu, Quantum, Kriegspiel) — цей файл розгортає його окремо; умови перемоги іншими способами — [lichess-variants.md](lichess-variants.md); базові правила — [chess.md](chess.md).
- Нейтральні фігури в інших іграх: [neutron.md](neutron.md) (нейтрон, якого рухають обидва), [amazons.md](amazons.md) (стріла-блокер після кожного ходу, але залишається назавжди), [quoridor.md](quoridor.md) (стінка замість ходу).
- Варіанти з качкою: дві качки, качка з власним патерном ходу, «гусак» з правом бити (?).
- **Осі варіацій**: нейтральний блокер (немає / один / кілька) · хто його рухає (той, хто ходив / суперник) · обовʼязковість (мусиш перемістити / можна лишити) · дальність (будь-куди / на N клітин) · блокер перманентний (Amazons) чи мандрівний (Duck) · умова перемоги (мат / взяття короля) · доля пату (нічия / поразка / перемога запатованого).

## Цікавинки для курсу
- Двофазний хід (фігура → качка) у машині станів ходу — 🌱.
- Легальність ходу з нейтральним блокером: промінь лінійних фігур зупиняється на качці, кінь ігнорує — 🌱 поверх наявних шахів.
- Прибрати шах: перемога за взяттям короля, пат = перемога запатованого — 🌱; але тоді перевірка `no_moves` має враховувати ходи під удар — 📎.
- AI: коефіцієнт розгалуження ×(кількість порожніх клітин) через фазу качки — minimax з відсіканням незначущих позицій качки — 🥇.
- Нотація `move@square` і парсер/серіалізатор — 📎.

## Мапа на каталог
- Є: `piece-move-patterns` · `piece-capture` · `impassable-cells` (клітина з качкою) · `legal-move-highlight` · `drag-drop-piece` · `cell-click` · `turn-enforcement` · `hot-seat` · `move-timer` · `ai-opponent` · `online-multiplayer` · `castling` · `en-passant` · `pawn-promotion` · `move-notation` · `last-move-highlight` · `game-screen` · `end-screen`.
- Свідомо **без** `no-move-into-check`, `check-stalemate`, `checkmate` — їх ця гра скасовує.
- **Нема** → пропозиції карток:
  - `+neutral-blocker` «Нейтральна фігура блокує клітину для всіх» · entities/legality · 🌱 — уже запропоновано в chess-rule-twists.
  - `+shared-piece` «Фігура, яку рухають обидва гравці» · entities/turn · 🌱 — Duck, Neutron.
  - `+two-part-turn` «Хід з двох обовʼязкових фаз» · game-logic/turn · 🌱 — Duck, Amazons, Neutron.
  - `+mandatory-relocate` «Сутність мусить змінити клітину щоходу» · game-logic/legality · 🌱.
  - `+king-capture-win` · `+stalemate-win` · `+rule-variants` — як у chess-rule-twists.

## Пропозиції до словників
- `+trigger:move_done` — завершено першу фазу ходу (вже вживалось у chess-rule-twists, тут — рядок пропозиції).
- `+cond:not_same_cell` — ціль ≠ поточна клітина (обовʼязкове переміщення).
- `+effect:relocate` — перенести на будь-яку вільну клітину (не `move` на 1 і не `teleport` на пару).
- `+role:shared` — фігура без сторони, яку рухають обидва (точніше за `neutral`, що «ходить сама»).
- `+ui:duck-ghost` — тінь качки в фазі 2 · `+ui:turn-phase` — індикатор фази ходу.
- `+axis:win-condition` = `king-capture` · `+card:shared-blocker` · `+card:two-part-turn`.

## Джерела
- ⭐ [Chess.com: Duck Chess](https://www.chess.com/terms/duck-chess) — правила, кінь стрибає через качку, шаху нема, взяття короля, запатований виграє; Тім Полден, 2016; вірусність 2022 (Eric Rosen, Nakamura).
- [duckchess.com](https://duckchess.com/) — офіційні правила: «качку треба перемістити», не можна взяти, рокіровка без шахових обмежень, правило fowling (без ходів — виграєш), нотація `@`.
- [House of Staunton: What is Duck Chess](https://www.houseofstaunton.com/chess-blog/what-is-duck-chess/) — стратегія (качка як щит від атаки), історія (Exeter Chess Club, Chess.com — жовтень 2022), нотація; у статті плутанина щодо пату.

## Непевне
- (?) Перша фаза партії — білі ставлять качку будь-куди після першого ходу; жодне з відкритих джерел явно не каже, де качка стоїть до старту.
- (?) Взяття на проході й перетворення пішака — «як у шахах»; джерела не уточнюють, чи качка на проміжній клітині блокує подвійний хід пішака (логічно — так).
- (?) Нічиї (повторення, 50 ходів) — не перевірено.
- (?) House of Staunton пише, що «fowled» гравець програє; офіційний сайт і Chess.com — що виграє; узято офіційне.
- (?) Наявність Duck Chess на pychess / рушії Fairy-Stockfish — з памʼяті.
