---
title: Rollerball (шаховий варіант)
slug: rollerball-chess
aka: [Rollerball, Роллербол, Rollerball chess]
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
year: 1998
platforms: [board, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Rollerball_(chess_variant)", best: true, note: "дошка 7×7 без центру 3×3, рух за годинниковою, ходи K/R/B/P з відскоками, перетворення, дві умови перемоги"}
  - {kind: other, url: "https://cdn.jsdelivr.net/npm/jocly@0.9.13/dist/browser/games/chessbase/rollerball-chess-model.js", note: "код Jocly: розстановка, графи ходів з відскоками, стан king-out, перемога, пат, повторення, 50 ходів, недостатній матеріал"}
  - {kind: other, url: "https://cdn.jsdelivr.net/npm/jocly@0.9.13/dist/browser/games/chessbase/rollerball-rules.html", note: "правила Jocly: 4 зони, поворот на 90° на кутових клітинах, «a2 лише через b1»"}
  - {kind: other, url: "https://gambiter.com/chess/variants/Rollerball_chess_variant.html", note: "переказ правил: кутові клітини зі скосом 45° для відскоку тури"}
  - {kind: play, url: "https://www.chessvariants.org/play/jocly/rollerball", note: "грати (Jocly на Chess Variant Pages); лінк з пошуку, агентам 403"}
  - {kind: other, url: "http://www.chessvariants.org/40.dir/rollerball/index.html", note: "оригінальні правила Cazaux на Chess Variant Pages (лінк зі статті, агентам 403)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=rollerball+chess+variant+cazaux", note: "пошук; партії"}
stage: v1
coverage: 60
mechanics: [piece-move-patterns, piece-capture, legal-move-highlight, no-move-into-check, check-stalemate, checkmate, pawn-promotion, repetition-draw, impassable-cells, hot-seat, ai-opponent, drag-drop-piece, cell-click, game-screen, end-screen, help-window, about-window, +ring-board, +directional-track, +bounce-move, +king-race-win, +move-count-draw, +insufficient-material]
proposes: ["+cond:forward_of", "+ui:direction-arrows", "+card:directional-track", "+card:king-race-win", "+card:ring-board", "+card:bounce-move"]
author: opus
date: 2026-11-09
---

# Rollerball — шахи на кільцевому треку 7×7 без центру: фігури біжать за годинниковою, відскакують від кутів, король може «прибігти» до ворожого старту

## Суть
Шаховий варіант Жана-Луї Казо (Jean-Louis Cazaux, 1998), натхненний фільмом «Rollerball» (1975): дошка 7×7 з вирізаним центром 3×3 — це трек шириною у дві клітини, і всі фігури рухаються переважно «вперед» = за годинниковою стрілкою. У кожної сторони 6 фігур: король, слон, дві тури, два пішаки. Тура й слон можуть один раз за хід відскочити від кута чи краю, назад ходять лише на 1. Перемога — мат або король, що обійшов трек за годинниковою і став на стартову клітину ворожого короля.

## Поле і час
- 7×7 = 49 клітин мінус центр c3–e5 = **40 клітин**: зовнішнє кільце (24) і внутрішнє (16). Гра була заявкою на конкурс варіантів для дошки з 40 клітин.
- Чотири зони — Південь, Захід, Північ, Схід (Jocly); «вперед» залежить від зони: на півдні — до вертикалі a, на заході — до 7-ї горизонталі, на півночі — до вертикалі g, на сході — до 1-ї горизонталі. Для кільця, на якому стоїть тура чи пішак, саме це кільце задає напрямок; хід з кільця на кільце — «вбік».
- Кутові й згинні клітини a1, b2, a7, b6, g7, f6, g1, f2: фігура, що стає туди, повертає орієнтацію на 90° за годинниковою (Jocly).
- Розстановка (код Jocly): білі — K d2, B d1, R e1 e2, P c1 c2; чорні — K d6, B d7, R c6 c7, P e6 e7. Обидва слони білопольні (чорнопольний — лише через перетворення). Перші ходять білі.
- Хід = півхід, як у шахах.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Король | piece | 1 на сторону | на 1 у будь-який бік; єдиний симетричний хід; рокіровки нема; під шах не ходить |
| Тура | piece | 2 на сторону | вперед уздовж кільця на будь-яку відстань (1 відскок від кута зовнішнього кільця) або вбік; назад — лише на 1 ортогонально |
| Слон | piece | 1, білопольний | по діагоналі вперед на будь-яку відстань з 1 відскоком від зовнішнього чи внутрішнього краю; назад — на 1 по діагоналі; a2 досягає лише через b1 |
| Пішак | piece | 2 на сторону | на 1 прямо вперед своїм кільцем або на 1 по діагоналі вперед на будь-яке кільце — і хід, і взяття; без подвійного кроку |
| Вирізаний центр 3×3 | static | c3–e5 | непрохідний; для слона — край, від якого можна відскочити |
| Зовнішнє / внутрішнє кільце | zone | 24 / 16 клітин | задає напрямок «вперед» для тури й пішака |
| Кутова / згинна клітина | terrain | 8 шт. | поворот орієнтації фігури на 90° за годинниковою; для тури — скіс 45° для відскоку |
| Стартові клітини ворожих пішаків | zone | білим e6/e7, чорним c1/c2 | клітини перетворення |
| Стартова клітина ворожого короля | zone | білим d6, чорним d2 | ціль «перегонів» короля |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move(p, to))` → ЯКЩО `turn_of(side)` and `legal(move)` → ТО `move(p, to)`, `end_turn`; інакше `block`.
- КОЛИ `contact(p, enemy)` → ТО `disappear_b` — взяття заміщенням, як у шахах.
- Тура: КОЛИ `input(move(rook, to))` → ЯКЩО `custom: «to — уперед уздовж свого кільця на будь-яку відстань, або вбік, або на 1 назад»` (кандидат +cond:forward_of) → ТО `move(rook, to)`.
- КОЛИ `blocked(rook)` → ЯКЩО `custom: «тура йде зовнішнім кільцем і вперлася в кут»` and `custom: «відскоку в цьому ході ще не було»` → ТО `bounce(rook)` — поворот на 90°, ковзання триває.
- Слон: КОЛИ `input(move(bishop, to))` → ЯКЩО `custom: «to — по діагоналі вперед на будь-яку відстань або на 1 по діагоналі назад»` → ТО `move(bishop, to)`.
- КОЛИ `blocked(bishop)` → ЯКЩО `custom: «край — зовнішній або край вирізаного центру»` and `custom: «відскоку ще не було»` → ТО `bounce(bishop)` — поворот на 90°.
- Пішак: КОЛИ `input(move(pawn, to))` → ЯКЩО `custom: «to — на 1 прямо вперед своїм кільцем або на 1 по діагоналі вперед на будь-яке кільце»` → ТО `move(pawn, to)`; взяття — тими самими кроками; назад і вбік не ходить.
- КОЛИ `enter(pawn, enemy_pawn_start)` → ТО `choose(R|B)`, `transform(piece)` — лише тура або слон.
- КОЛИ `enter(p, bend_cell)` → ТО `rotate(p, 90)` — «вперед» фігури повертається за годинниковою (так Jocly пояснює зміну напрямку між зонами).
- Король: КОЛИ `input(move(king, to))` → ЯКЩО `custom: «на 1 у будь-який бік»` and `not in_check(side)` після ходу → ТО `move(king, to)`; рокіровки нема.
- КОЛИ `leave(king, own_start_column)` → ЯКЩО `moving(king, clockwise)` → ТО `set_state(king, out)` (Jocly: король d1/d2 → c1/c2 стає «king-out»).
- КОЛИ `enter(king, own_start_column)` → ТО `clear_state(king, out)` — повернувшись, король знову звичайний.
- КОЛИ `enter(king, enemy_king_start)` → ЯКЩО `state(king, out)` → ТО `win` — король прибіг за годинниковою.
- КОЛИ `no_moves(side)` → ЯКЩО `in_check(side)` → ТО `lose` (мат).
- КОЛИ `no_moves(side)` → ЯКЩО `not in_check(side)` → ТО `draw` (пат).
- КОЛИ `repetition(position, 3)` → ТО `draw`.
- Jocly додає: КОЛИ `counter(plies_without_capture, ≥, 100)` → ТО `draw`; КОЛИ `custom: «в одного нема пішака, слона й тури, а в іншого — пішака й тури»` → ТО `draw` (недостатній матеріал).
- Перемога: мат · король на стартовій клітині ворожого короля після обходу за годинниковою · Нічия: пат · триразове повторення · (Jocly) 50 ходів без взяття, недостатній матеріал.

## Керування і ввід
- Фізична дошка 7×7 з позначеним вирізом; гравцю треба тримати в голові «вперед» для кожної зони.
- Цифрова версія (Jocly): клік або drag фігури, підсвітка легальних ходів — без неї відскоки й напрямки зон майже не читаються; вибір фігури при перетворенні (тура/слон).

## Вікна, меню, HUD
- `game-screen` (Jocly): кільцева дошка з діркою, `legal-move-highlight`, `move-list`, `turn-indicator`; кандидат `direction-arrows` — стрілки «вперед» по зонах.
- `help-window` — сторінки правил і опису Jocly; `about-window` — сторінка credits.
- `end-screen` — мат / король дійшов / пат / повторення.
- Переходи: вибір гри → game-screen → end-screen.

## Фічі поза полем
- `hotseat` і `ai-opponent-levels` (Jocly; у коді є функція оцінки позиції (?)).
- `custom-rules`: опція Jocly `preventRepeat` (повторення як нічия) (?).
- `rules-page` — правила, опис і credits як окремі сторінки Jocly.

## Варіації й родичі
- [chess.md](chess.md) — база ходів; [wraparound-chess.md](wraparound-chess.md) — кругові шахи: кільце без країв по колу, але без примусового напрямку.
- [lichess-variants.md](lichess-variants.md): Racing Kings і King of the Hill — інші перемоги «король дійшов»; тут вона поєднана з напрямком треку.
- Конкурс «40 клітин» (1998): Rollerball — одна із заявок; інших заявок не перевіряв (?).
- **Осі варіацій**:
  - **Напрямок руху**: симетричний (шахи) · примусовий потік за годинниковою, назад — на 1 (Rollerball).
  - **Межі ковзання**: стоп на краю · 1 відскок від кута/краю (Rollerball) · тор (Cylinder).
  - **Поле**: повна дошка · дошка з діркою-трек.
  - **Ціль**: мат · + король у ворожому таборі з умовою маршруту.

## Цікавинки для курсу
- Поле напрямків: «вперед» = функція зони клітини, поворот на згинах — 📎.
- Ковзна фігура з рівно одним відскоком (відбиття вектора на куті чи краї дірки) — 🥉.
- Дошка-маска 7×7 з діркою 3×3 і два кільця — 🌱.
- Стан king-out: перемога лише після обходу за годинниковою — 🌱.
- Генератор ходів як заздалегідь побудований граф променів (як `cbRbGraph` у Jocly) — 🥉.
- AI-суперник minimax на 40 клітинах із двома умовами перемоги — 🥇.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ ходи з напрямком зони · `piece-capture` · `legal-move-highlight` · `no-move-into-check` · `check-stalemate` · `checkmate` · `pawn-promotion` ↔ лише в R/B на клітинах ворожих пішаків · `repetition-draw` · `impassable-cells` ↔ центр 3×3 · `hot-seat` · `ai-opponent` (?) · `drag-drop-piece` · `cell-click` · `game-screen` · `end-screen` · `help-window` · `about-window` ↔ credits Jocly.
- **Нема** → пропозиції карток:
  - `+directional-track` «Трек: «вперед» задано зоною клітини» · entities/move · 📎 · слоти {zones: 4, backward_step: 1}.
  - `+bounce-move` — підтверджую (Chip's Challenge, Jezzball): тут ковзна фігура з 1 відскоком · слот {max_rebounds: 1}.
  - `+king-race-win` «Перемога — король на стартовій клітині ворожого короля» · game-logic/win · 🌱 · слот {route: clockwise}.
  - `+ring-board` — підтверджую (wraparound-chess): тут квадратна дошка з діркою, 24 + 16 клітин.
  - `+move-count-draw`, `+insufficient-material` — див. chess.md (у Jocly є обидва).

## Пропозиції до словників
- `+cond:forward_of(p, to)` — клітина лежить «вперед» від фігури за полем напрямків (зона/кільце); родич `facing`, але напрямок задає клітина, не фігура.
- `+ui:direction-arrows` — стрілки напрямку руху по зонах поля (Rollerball, конвеєри, односторонні клітини).
- `+card:directional-track` · `+card:king-race-win` · `+card:ring-board` · `+card:bounce-move` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Rollerball (chess variant)](https://en.wikipedia.org/wiki/Rollerball_(chess_variant)) — дошка, склад армій, ходи всіх фігур, «лише один відскок», перетворення, дві умови перемоги, пат і повторення, Cazaux 1998, фільм 1975.
- [Jocly: rollerball-chess-model.js](https://cdn.jsdelivr.net/npm/jocly@0.9.13/dist/browser/games/chessbase/rollerball-chess-model.js) — точна розстановка, промені ходів з відскоками, клітини перетворення, стан king-out і перевірка перемоги, правило 100 півходів, недостатній матеріал.
- [Jocly: правила](https://cdn.jsdelivr.net/npm/jocly@0.9.13/dist/browser/games/chessbase/rollerball-rules.html) — 4 зони, поворот на 90° на кутових і згинних клітинах, «a2 — лише через b1», «only if had turned clockwise».
- [Gambiter: Rollerball](https://gambiter.com/chess/variants/Rollerball_chess_variant.html) — переказ правил, скошені кути для відскоку тури.
- [Chess Variant Pages: Rollerball](http://www.chessvariants.org/40.dir/rollerball/index.html) · [грати в Jocly](https://www.chessvariants.org/play/jocly/rollerball) — лінки зі статті та пошуку, агентам 403.
- Офіційна сторінка автора history.chess.free.fr/rollerball.htm — не відкрилась (відмова зʼєднання), у шапку не клав.
- YouTube: пошук «rollerball chess variant cazaux».

## Непевне
- (?) Хід тури «вбік»: на скільки клітин (Вікіпедія — «будь-яка відстань вбік», але трек шириною 2; Jocly додає окремі прямі промені з b1, a6, f7, g2) — точну геометрію не перевіряв.
- (?) «Only if had turned clockwise»: Jocly реалізує це станом king-out при виході з вертикалі d на c (білі); чи так само в оригіналі Cazaux — не бачив.
- (?) Правило 50 ходів і недостатній матеріал — з коду Jocly, у статті Вікіпедії їх нема.
- (?) Чи виграв Rollerball конкурс «40 клітин» — у джерелах лише «заявка».
- (?) Наявність AI і рівнів у Jocly для цієї гри — з наявності функції оцінки, не перевірено в інтерфейсі.
