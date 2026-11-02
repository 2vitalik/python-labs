---
title: N-in-a-row (Хрестики-нулики, Gomoku, Connect Four, Pentago…)
slug: line-games
family: chess-abstract
also: [board-digital]
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 1974
platforms: [paper, board, web, mobile, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tic-tac-toe", best: true, note: "база сімʼї: 8 ліній, розвʼязок, стратегія Newell–Simon, m,n,k-ігри й варіанти"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe", note: "9 полів, хід визначає наступне поле, варіанти, MCTS"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Gomoku", note: "freestyle vs exactly five, swap/swap2, розвʼязок Allis 1994"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Renju", note: "заборони для чорних, дебютні правила RIF"}
  - {kind: official, url: "https://www.renju.net/rules/", note: "RenjuNet: правила renju (3×3, 4×4, overline)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Connect_Four", note: "гравітаційне кидання, розвʼязок 1988, PopOut, Pop 10"}
  - {kind: play, url: "https://connect4.gamesolver.org/", note: "розвʼязувач Connect Four: оцінка кожного стовпця + туторіал"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pentago", note: "поворот квадранта, сильно розвʼязана"}
  - {kind: other, url: "https://perfect-pentago.net/", note: "Geoffrey Irving: Pentago — перемога першого"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/3D_tic-tac-toe", note: "Qubic 4×4×4, 76 ліній"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=ultimate+tic+tac+toe+rules", note: "пошук; правила ultimate"}
stage: v1
coverage: 75
mechanics: [hot-seat, turn-enforcement, move-timer, ai-opponent, ai-random, ai-greedy, ai-minimax, cell-click, hover-highlight, legal-move-highlight, gravity-fall, game-screen, main-menu, end-screen, help-window, settings-window, difficulty-levels, field-size-picker, theme-select, profile-stats, replay, state-as-data, unit-tests, +place-stone, +line-win, +nested-boards, +forced-board, +forbidden-patterns, +swap-rule, +column-drop, +pop-out, +quadrant-rotation, +rule-variants, +misere-win]
proposes: ["+trigger:placed", "+effect:place", "+cond:forbidden_shape", "+cond:board_target", "+effect:rotate_region", "+effect:remove_bottom", "+ui:win-line", "+ui:active-board-highlight", "+ui:column-hover", "+window:variant-select", "+window:swap-dialog", "+card:line-win", "+card:nested-boards", "+card:forced-board", "+card:forbidden-patterns", "+card:column-drop", "+card:pop-out", "+card:quadrant-rotation"]
author: opus
date: 2026-11-02
---

# N-in-a-row — постав свій знак так, щоб першим скласти лінію з N

## Суть
Сімʼя ігор, де двоє по черзі **ставлять** знак/камінь/диск у порожню клітину, і перемагає той, хто першим складе неперервну лінію з N своїх (горизонталь, вертикаль, діагональ). Фігури не ходять і не бʼються (крім рідкісних варіантів) — уся глибина в тому, **куди дозволено ставити** (гравітація, обране поле, заборонені форми) і **що відбувається після постановки** (поворот квадранта, вибивання знизу). Спільний двіжок — перевірка лінії від останнього ходу; відмінності — один-два модифікатори.

## Поле і час
- Квадратні сітки: 3×3 (хрестики-нулики), 3×3 полів по 3×3 (ultimate, 81 клітина), 15×15 перетинів (renju, gomoku; історично 19×19), 7 стовпців × 6 рядів вертикально (Connect Four), 6×6 з чотирьох квадрантів 3×3 (Pentago), куб 4×4×4 (Qubic, `field: 3d` для нього).
- Покроково; хід = постановка (+ подекуди обовʼязкова дія після неї: поворот у Pentago). Поле лише заповнюється; повне поле без лінії — нічия.
- Інформація повна, випадковості нема; майже всі члени сімʼї **розвʼязані**: хрестики-нулики — нічия; Connect Four — перший виграє з центрального стовпця (Allen, Allis 1988); freestyle gomoku 15×15 — перший виграє (Allis 1994); Qubic — перший виграє (Patashnik 1980); Pentago — перший виграє (Irving).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Знак / камінь / диск | piece | сторона X/O, чорні/білі, червоні/жовті | ставиться в порожню клітину, далі не рухається (крім Pentago-повороту й PopOut) |
| Порожня клітина | static | — | ціль ходу, якщо дозволена правилами варіанта |
| Лінія | zone | довжина N, 4 напрямки | N своїх поспіль = перемога |
| Квадрант (Pentago) | zone | 3×3, 4 шт | після постановки один квадрант повертається на 90° |
| Мале поле (Ultimate) | zone | 3×3, стан: open/won X/won O/draw | вигране мале поле стає «клітиною» великого |
| Tic-tac-toe | — | 3×3, N=3 | вільна постановка; 8 ліній; ідеальна гра — нічия; 138 термінальних позицій з точністю до симетрії |
| Ultimate tic-tac-toe | — | 9 полів 3×3, N=3 двічі | позиція твого ходу всередині малого поля визначає, в якому малому полі ходить суперник; виграв мале поле — воно твоє на великому; відправлений у вигране/повне поле — ходиш будь-де; велике поле — три малих у ряд |
| Gomoku | — | 15×15, N=5 | freestyle: 5 і більше виграють; standard: рівно 5 (overline не рахується); дебют swap/swap2 |
| Renju | — | 15×15, N=5 | чорні ходять першими в центр, але їм заборонені подвійна трійка, подвійна четвірка й overline (заборонений хід = поразка чорних, якщо він не дає рівно 5); білим можна все, overline теж виграє |
| Connect Four | — | 7×6, N=4 | диск кидається в стовпець і падає на найнижчу вільну клітину; хід = вибір стовпця |
| PopOut | — | 7×6 | хід = кинути диск зверху **або** витягти свій диск з нижнього ряду; диски над ним осідають |
| Pentago | — | 6×6 (4 квадранти), N=5 | поставити кульку, потім повернути будь-який квадрант на 90° в будь-який бік; лінія рахується після повороту |
| Qubic | — | 4×4×4, N=4 | вільна постановка в кубі; 76 ліній (рядки, стовпці, стовпи, діагоналі площин і 4 просторові) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, cell)` → ЯКЩО `turn_of(side)` і `free(cell)` і `custom: «cell дозволена варіантом»` → ТО `custom: «поставити знак»` (`+effect:place`); інакше `block`.
- КОЛИ `after(place)` → ЯКЩО `pattern(line(N))` через останній знак → ТО `win`.
- КОЛИ `after(place)` → ЯКЩО `custom: «порожніх клітин нема»` і лінії нема → ТО `draw`.
- Ultimate: КОЛИ `input(place, cell)` → ЯКЩО `custom: «cell лежить у малому полі, на яке вказав попередній хід»` (`+cond:board_target`) або те поле вигране/повне → ТО дозволено; інакше `block`.
- Ultimate: КОЛИ `pattern(line(3))` у малому полі → ТО `set_side(small_board, side)`; КОЛИ `pattern(line(3))` з малих полів на великому → ТО `win`; нема відкритих полів → `draw`.
- Gomoku standard: КОЛИ `pattern(line(N≥6))` → ТО не перемога (лише рівно 5); freestyle — перемога.
- Renju: КОЛИ `input(place, cell)` чорними → ЯКЩО `custom: «створює 3×3, 4×4 або 6+»` (`+cond:forbidden_shape`) і `not` рівно 5 → ТО `lose` (чорні); білим ця умова не діє.
- Renju: пас дозволено; два паси поспіль → `draw`.
- Swap (gomoku): КОЛИ `game_start` → ТО перший ставить 2 чорних + 1 білий, другий `choose(колір)`. Swap2: другий може (1) взяти білі й поставити білий, (2) взяти чорні, (3) поставити ще чорний + білий і віддати вибір кольору першому.
- Connect Four: КОЛИ `input(drop, column)` → ЯКЩО `custom: «стовпець не повний»` → ТО `fall(disc)` до найнижчої вільної клітини.
- PopOut: КОЛИ `input(pop, column)` → ЯКЩО `occupied(bottom(column), own)` → ТО `custom: «забрати нижній диск»` (`+effect:remove_bottom`), `fall` усіх над ним на 1.
- Pop 10: витягнутий диск, що був частиною четвірки, відкладається і дає `extra_move`; інакше повертається зверху; перший, хто відклав 10, виграє.
- Pentago: КОЛИ `after(place)` → ТО `rotate(quadrant, ±90)` (`+effect:rotate_region`); поворот можна пропустити, лише поки є квадрант із поворотною симетрією (напр. порожній); перевірка лінії — після повороту.
- Pentago: КОЛИ після повороту `pattern(line(5))` в обох сторін → ТО `draw` (?).
- Перемога: перша лінія з N · Поразка: лінія суперника / заборонений хід (renju) · Рахунок: партія 1 / ½ / 0; Pop 10 — лічильник відкладених.

## Керування і ввід
- Папір/дошка: поставити знак; Connect Four — кинути диск у щілину; Pentago — фізично крутити квадрант.
- (цифрова версія) Клік по клітині; у Connect Four — клік/наведення на стовпець з тінню диска над ним; у Pentago — постановка, потім стрілки ↺/↻ на кожному квадранті; у Ultimate — активне мале поле підсвічене, решта затемнені.
- Swap2-дебют — модальний вибір з 3 опцій.

## Вікна, меню, HUD
- `main-menu`: Грати → `variant-select` (класика 3×3, Ultimate, Gomoku/Renju, Connect Four, PopOut, Pentago) → `settings-window` (проти AI / друга, рівень, хто перший, розмір поля для m,n,k).
- `game-screen`: поле, `turn-indicator`, `win-line` (підсвічена лінія перемоги), `last-move-highlight`, `active-board-highlight` (Ultimate), `column-hover` (Connect Four), `undo-button`, `restart-button`, рахунок серії партій.
- `swap-dialog` (gomoku swap/swap2): вибір кольору або додаткових каменів.
- `end-screen`: «X виграв / нічия» з лінією на полі, «Ще раз».
- `help-window`: правила варіанта.
- Переходи: main-menu → variant-select → game-screen → end-screen → game-screen.

## Фічі поза полем
- `ai-opponent-levels`: від випадкового до ідеального (повний перебір 3×3; розвʼязувач Connect Four з оцінкою кожного стовпця).
- `hotseat`, `online-multiplayer`, `stats` (перемоги/нічиї серії), `custom-rules` (m,n,k: розмір поля і N), `hint-move` (найкращий стовпець).
- `replay` партії, `export-import` у нотації (renju — координати a–o, 1–15).
- `tutorial` на прикладі 3×3.

## Варіації й родичі
- m,n,k-ігри — узагальнення: поле m×n, лінія k (3,3,3 — хрестики; 15,15,5 — gomoku).
- Misère / Notakto — хто склав лінію, той програв; Wild tic-tac-toe — ставиш X або O на вибір; Quantum tic-tac-toe — суперпозиції ходів.
- Ultimate: правило «грати у вирішені поля, поки є місце» (перший має виграш); Tic-Tac-Ku — взяти 5 малих полів; багатошарова вкладеність.
- Gomoku-сімʼя: Caro (рівно 5 і не заблокована з обох кінців), Omok (19×19 + заборона 3×3), Renju (асиметричні заборони).
- Connect Four: PopOut, Pop 10, Power Up (диски з ефектами), Five-in-a-Row 6×9, Connect 4×4 (два шари, 4 гравці).
- Pentago XL — 3–4 гравці, 9 квадрантів.
- Осі варіацій: **куди можна ставити** (будь-де / знизу стовпця / в указане поле / не у заборонену форму) · **що після постановки** (нічого / поворот квадранта / вибивання знизу) · **довжина лінії** (рівно N / N і більше) · **ціль** (скласти / уникнути) · **вимір** (2D / 3D / вкладені поля).
- Родичі: Reversi (той самий хід-постановка), Hex (зʼєднання замість лінії), Go (оточення).

## Цікавинки для курсу
- Перевірка лінії від останнього ходу: 4 напрямки × «рахуй у обидва боки» — 🌱; для довільних m,n,k — 📎.
- Minimax для 3×3 з повним перебором і таблицею симетрій — 🥉; Connect Four з alpha-beta + bitboard + таблиця транспозицій — 🥇.
- Ultimate: два рівні стану (мале поле → клітина великого) + обмеження наступного поля — 🥉; MCTS-AI, бо нема простої оцінки — 🥇.
- Renju-заборони: розпізнати «відкриту трійку» і «четвірку» з урахуванням того, що форма має бути реально досяжною — 🥈.
- Pentago: поворот квадранта як перестановка 9 клітин + лінії в обох після повороту — 📎.
- Гравітація в Connect Four та осідання в PopOut — 🌱.
- 3D-поле Qubic: генерація всіх 76 ліній у кубі — 📎.

## Мапа на каталог
- Є: `hot-seat`, `turn-enforcement`, `move-timer` · `ai-opponent`/`ai-random`/`ai-greedy`/`ai-minimax` · `cell-click`, `hover-highlight`, `legal-move-highlight` (Ultimate — дозволене поле) · `gravity-fall` ↔ Connect Four · `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window` · `difficulty-levels`, `field-size-picker` (m,n,k), `theme-select` · `profile-stats`, `replay`, `state-as-data`, `unit-tests`.
- **Нема** → пропозиції карток:
  - `+place-stone` (див. reversi.md) — хід-постановка.
  - `+line-win` «Лінія з N» · game-logic/win · 🌱 · слоти {n, exact: bool, dirs: 4|13} — перевірка від останнього ходу.
  - `+nested-boards` «Поле з полів» · entities/state · 🥉 · слоти {levels} — вигране мале поле стає клітиною великого.
  - `+forced-board` «Хід визначає зону суперника» · entities/legality · 📎 — позиція всередині малого поля = індекс наступного поля.
  - `+forbidden-patterns` «Заборонені форми» · entities/legality · 🥈 · слоти {shapes: [3x3, 4x4, overline], side} — renju.
  - `+swap-rule` (див. hex.md) — тут swap/swap2.
  - `+column-drop` «Кидок у стовпець» · entities/move · 🌱 — дитина `gravity-fall`: хід — номер стовпця.
  - `+pop-out` «Вибити знизу» · entities/move · 📎 — забрати свій нижній диск, стовпець осідає.
  - `+quadrant-rotation` «Поворот частини поля» · entities/move · 📎 · слоти {region: 3x3, optional_if_symmetric}.
  - `+rule-variants` (див. lichess-variants.md) — варіанти сімʼї за перемикачем.
  - `+misere-win` (див. checkers.md) — misère/Notakto.

## Пропозиції до словників
- `+trigger:placed`, `+effect:place` — хід-постановка (як у reversi/go/hex).
- `+cond:forbidden_shape` — постановка створює заборонену форму (3×3, 4×4, overline).
- `+cond:board_target` — клітина належить зоні, яку визначив попередній хід суперника.
- `+effect:rotate_region` — повернути блок клітин разом із вмістом (є ⏳ `rotate(a, deg)`, але для сутності, не регіону поля).
- `+effect:remove_bottom` — прибрати нижню фігуру стовпця з осіданням (PopOut).
- `+ui:win-line` — підсвічена виграшна лінія; `+ui:active-board-highlight` — де дозволено ходити; `+ui:column-hover` — тінь диска над стовпцем.
- `+window:variant-select`, `+window:swap-dialog` — вибір варіанта; дебютний вибір кольору.
- `+card:line-win`, `+card:nested-boards`, `+card:forced-board`, `+card:forbidden-patterns`, `+card:column-drop`, `+card:pop-out`, `+card:quadrant-rotation` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Tic-tac-toe](https://en.wikipedia.org/wiki/Tic-tac-toe) — правила, 138 термінальних позицій, стратегія Newell–Simon, OXO (1952), m,n,k, misère, Notakto, wild, quantum, 3D.
- [Wikipedia: Ultimate tic-tac-toe](https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe) — правило наступного поля, варіанти, MCTS.
- [Wikipedia: Gomoku](https://en.wikipedia.org/wiki/Gomoku) — freestyle/standard, swap, swap2, Caro, Omok, розвʼязок 1994.
- [Wikipedia: Renju](https://en.wikipedia.org/wiki/Renju) і [RenjuNet: rules](https://www.renju.net/rules/) — заборони чорних, пас, дебютні правила (RIF, Soosõrv-8, Taraguchi-10).
- [Wikipedia: Connect Four](https://en.wikipedia.org/wiki/Connect_Four) — правила, розвʼязок, PopOut, Pop 10, Power Up, 4,5·10¹² позицій.
- [Connect 4 solver](https://connect4.gamesolver.org/) — оцінка кожного стовпця при ідеальній грі, туторіал з кодом (alpha-beta).
- [Wikipedia: Pentago](https://en.wikipedia.org/wiki/Pentago) і [perfect-pentago.net](https://perfect-pentago.net/) — правила повороту, розвʼязок.
- [Wikipedia: 3D tic-tac-toe](https://en.wikipedia.org/wiki/3D_tic-tac-toe) — Qubic, 76 ліній, розвʼязок.
- YouTube: пошук «ultimate tic tac toe rules».

## Непевне
- (?) Pentago: що буває, коли поворот дав п'ятірки обом — у статті не сказано; поширене правило «нічия» — з памʼяті.
- (?) PopOut: хто виграє, якщо вибивання склало четвірки обом — не підтверджено.
- (?) `year: 1974` — умовно (Connect Four як перша комерційна гра сімʼї); хрестики-нулики й гомоку значно старші.
- (?) Деталі сучасних дебютних правил renju (Soosõrv-8, Taraguchi-10: скільки варіантів 5-го ходу пропонується) не прочитані.
