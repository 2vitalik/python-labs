---
title: Національні варіанти шашок
slug: checkers-variants
aka: [Draughts variants, Варіанти шашок, Pool checkers, Makhos, Dama, Damii, Dameo, Frisian draughts]
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
year: 1900
platforms: [board, web, mobile, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Draughts", best: true, note: "таблиця варіантів: дошка, кількість, хто ходить першим, обмеження взяття"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Russian_draughts", note: "російські: взяття назад, далека дамка, перетворення посеред серії"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/International_draughts", note: "міжнародні 10×10: правило більшості"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pool_checkers", note: "американські pool: далека дамка, вільний вибір серії, 3 дамки проти 1 — 13 ходів"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Frisian_draughts", note: "фризькі: взяття у 8 напрямках, дамка = 1.5 шашки, правило трьох ходів дамкою"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dameo", note: "Dameo (Freeling, 2000): рух шеренгою, взяття лише ортогонально"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Thai_checkers", note: "Makhos: 8 шашок, дамка зупиняється одразу за збитою"}
  - {kind: play, url: "https://lidraughts.org/variant", note: "онлайн: Frisian, Frysk!, Russian, Brazilian, Antidraughts…"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=draughts+variants+rules+differences", note: "пошук; порівняння варіантів"}
stage: v1
coverage: 70
mechanics: [rule-variants, piece-move-patterns, piece-capture, pawn-promotion, no-moves-left, repetition-draw, field-size-picker, match-setup, multi-select, legal-move-highlight, hot-seat, ai-opponent, ai-minimax, help-window, game-screen, main-menu, end-screen, state-as-data, unit-tests, fixture-level-tests, +forced-capture, +multi-jump, +max-capture-rule, +flying-piece, +huffing, +capture-priority, +king-move-limit, +phalanx-move, +stop-behind-king]
proposes: ["+cond:can_capture", "+cond:max_capture", "+effect:jump_capture", "+trigger:missed_capture", "+effect:forfeit", "+cond:capture_value", "+cond:streak", "+effect:move_line", "+card:huffing", "+card:capture-priority", "+card:king-move-limit", "+card:phalanx-move", "+card:stop-behind-king"]
author: opus
date: 2026-11-09
---

# Національні варіанти шашок — один двіжок, десяток перемикачів: хто бʼє назад, куди летить дамка, яку серію брати

## Суть
Доповнення до `checkers.md`: там — база й головні варіанти (англійські, російські, міжнародні, бразильські, канадські, турецькі, піддавки). Тут — **решта національних правил** і повна матриця перемикачів, з якої збирається будь-який варіант: pool, тайські, малайзійські, філіппінські, ганські, кенійські, готичні, чеські, аргентинські, італійські, фризькі в деталях і сучасний Dameo. Ціль скрізь одна — залишити суперника без ходу; різниця — в кількох булевих і перелікових параметрах взяття.

## Поле і час
| Варіант | Дошка | Шашок | Перший хід | Шашка бʼє назад | Дамка | Вибір серії |
|---|---|---|---|---|---|---|
| Pool (США) | 8×8 | 12 | чорні | так | далека | будь-яка, але серію до кінця |
| Thai (Makhos) | 8×8 | 8 | чорні | ні | далека, стоп одразу за збитою | будь-яка |
| Malaysian / Singaporean | 12×12 | 30 | не фіксовано | ні | далека | обовʼязкове, за пропуск — фук |
| Filipino (Dama) | 8×8 | 12 | білі | так | далека | максимум фігур |
| Ghanaian (Damii) | 10×10 | 20 | білі | так | далека | будь-яка; пропустила взяття дамка — дамку знімають |
| Kenyan | 8×8 | 12 | білі | так | далека, стоп за збитою | будь-яка |
| Gothic | 8×8 | 16 | білі | ні (бʼє вперед і вбік) | коротка (є варіант з далекою) | обовʼязкове |
| Czech | 8×8 / 10×10 | 12 / 15 | білі | ні | далека | спершу взяття дамкою, далі будь-яка |
| Argentinian | 8×8 / 10×10 | 12 / 15 | білі | ні | далека, стоп після кожного взяття | при рівній кількості — взяття дамкою |
| Italian | 8×8 / 10×10 | 12 / 15 / 20 | білі | ні | коротка; шашка **не бʼє** дамку | максимум → дамкою → більше дамок |
| Spanish | 8×8 | 12 | білі | ні | далека | максимум фігур → максимум дамок |
| Frisian | 10×10 | 20 | світлі | так, у 8 напрямках | далека | максимум **вартості** (дамка = 1.5) |
| Sri Lankan | 12×12 | — | — | як міжнародні | далека | максимум |
| Dameo (2000) | 8×8, усі 64 | 18 | світлі | так, лише ортогонально | ферзь | максимум |

- Скрізь покроково; хід = простий хід або повна серія однією фігурою. Збиті в більшості знімаються **після** серії й не перестрибуються двічі.
- Dameo: старт трапецією a1–h1, b2–g2, c3–f3 (18 шашок).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Шашка (man) | piece | бʼє назад: так/ні; напрямки взяття: діагональ / +ортогональ | 1 крок уперед; стрибок через сусіда на порожню за ним |
| Коротка дамка | piece | — | 1 крок у будь-який діагональний бік (Italian, Gothic, Bashni) |
| Далека дамка | piece | — | будь-яка відстань; бʼє здалеку, обирає клітину приземлення |
| Дамка «стоп за збитою» | piece | — | бʼє здалеку, але приземляється одразу за збитою (Thai, Kenyan, Argentinian) |
| Вовк (Frisian king) | piece | вартість 1.5 | далека дамка; ≤3 ходи поспіль без взяття |
| Шеренга (Dameo) | piece | ≥2 своїх в лінію | рухається цілком на 1 вперед/по діагоналі, якщо клітина попереду вільна |
| Дамка Dameo | piece | — | як ферзь у 8 напрямках; бʼє ортогонально здалеку |
| Дамковий ряд | zone | останній ряд | шашка, що **закінчила** на ньому хід, стає дамкою (Frisian, Dameo — за правилами міжнародних) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(side)` → ЯКЩО `custom: «сторона може бити»` (`+cond:can_capture`) → ТО простий хід `block` (усі варіанти).
- КОЛИ `input(jump, man, over)` → ЯКЩО `occupied(over, enemy)` і `free(cell_behind)` і `custom: «напрям дозволений варіантом»` → ТО `custom: «стрибок»` (`+effect:jump_capture`).
- Italian: КОЛИ `input(jump, man, over)` → ЯКЩО `occupied(over, enemy_king)` → ТО `block`.
- Pool / Russian / Ghanaian / Kenyan: КОЛИ `turn_start(side)` → ТО легальна будь-яка серія; Filipino / Brazilian / Spanish / Italian / Dameo → лише серії з максимумом фігур (`+cond:max_capture`).
- Frisian: КОЛИ `turn_start(side)` → ТО легальні лише серії з максимальною **вартістю** (`+cond:capture_value`: шашка 1, дамка 1.5); при рівній вартості, якщо може бити дамка, — бʼє дамка.
- Spanish: при рівній кількості — серія з більшою кількістю збитих дамок. Italian: при рівній — бʼє дамка, далі — більше дамок.
- Czech: КОЛИ `turn_start(side)` → ЯКЩО `custom: «дамка може бити»` → ТО взяття шашкою `block`; далі вибір серії вільний.
- Argentinian: при рівній кількості — серія дамкою.
- Thai / Kenyan / Argentinian: КОЛИ `after(jump_capture)` з далекою дамкою → ТО `custom: «приземлення лише на клітину одразу за збитою»`, звідти бʼє далі.
- Malaysian: КОЛИ `custom: «гравець не взяв, хоча міг»` (`+trigger:missed_capture`) → ТО `custom: «суперник знімає ту фігуру (фук)»` (`+effect:forfeit`).
- Ghanaian: КОЛИ `trigger:missed_capture` → ЯКЩО `custom: «пропустила дамка»` → ТО `+effect:forfeit` дамки.
- Frisian: КОЛИ `input(move, king, to)` → ЯКЩО `custom: «ця дамка вже ходила 3 рази поспіль без взяття»` (`+cond:streak`) і `custom: «є не лише дамки»` → ТО `block`.
- Dameo: КОЛИ `input(move, line, dir)` → ЯКЩО `custom: «≥2 свої шашки в лінії вздовж dir»` і `free(cell_ahead)` → ТО `custom: «уся шеренга на 1 вперед»` (`+effect:move_line`).
- Dameo: КОЛИ `input(jump, piece, over)` → ЯКЩО `custom: «over — ортогональний сусід»` → ТО `jump_capture`; діагональне взяття `block`.
- КОЛИ `reach(man, last_row)` → ЯКЩО хід закінчився → ТО `transform(king)`.
- КОЛИ `turn_start(side)` → ЯКЩО `no_moves(side)` → ТО `lose`.
- Нічиї: Pool — 3 дамки проти 1 не виграли за 13 ходів → `draw`; Frisian — 2 дамки проти 1 за 7 ходів → `draw`, дамка проти дамки без взяття наступним ходом → `draw`; Dameo — триразове `repetition` → `draw`.
- Перемога: суперник без ходу · Поразка: без ходу · Рахунок: 1 / ½ / 0.

## Керування і ввід
- (цифрова версія) вибір варіанта перед партією; клік фігура → клітини серії; Dameo — виділення шеренги (`multi-select`: клік по задній шашці лінії + напрям).
- Неоднозначні серії далекої дамки — вибір клітини приземлення на кожному кроці.

## Вікна, меню, HUD
- (цифрова версія) `main-menu` → `match-setup`: варіант (список з короткими «що інакше»), колір, AI, годинник.
- `game-screen`: дошка під розмір варіанта, `turn-indicator`, `legal-move-highlight` (лише фігури, що мусять бити), `move-list`; Frisian — лічильник ходів дамки поспіль; нічийні лічильники (13 / 7 ходів).
- `help-window`: картка варіанта — рядок матриці.
- `end-screen`: результат і причина (нема ходів / ліміт ходів / повторення).

## Фічі поза полем
- `custom-rules`: варіант = конфіг перемикачів (дошка, бʼє назад, дамка, пріоритет, фук, ліміт ходів дамки).
- `ai-opponent-levels`, `online-multiplayer` (lidraughts: Frisian, Frysk!, Russian, Brazilian), `rules-page` на варіант.

## Варіації й родичі
- Матриця перемикачів (осі варіацій):
  - **дошка**: 8×8 темні / 8×8 усі (Turkish, Gothic, Dameo) / 10×10 / 12×12 / гекс (Hexdame, Freeling 1979).
  - **напрями взяття**: діагональ / ортогональ (Turkish, Dameo) / обидві (Frisian; Armenian tama — шашка ходить ще й по діагоналі).
  - **шашка бʼє назад**: так / ні.
  - **дамка**: коротка / далека / стоп за збитою / обмежена 3 ходами (Frisian).
  - **вибір серії**: вільний / максимум фігур / максимум вартості / пріоритет дамки (Czech, Argentinian, Italian).
  - **пропуск взяття**: заборонений / фук (Malaysian, Ghanaian для дамки).
  - **рух групою**: ні / шеренга (Dameo).
- У `checkers.md`: English, Russian, International, Brazilian, Canadian, Turkish, Poddavki, Breakthrough. Колонні — `lasca.md` (і Bashni в ній).
- Інші родичі в корпусі: `breakthrough-loa.md`, `line-games.md`.

## Цікавинки для курсу
- Варіант як dataclass-конфіг + один генератор ходів для 10+ правил, фікстури на кожен рядок матриці — 🥇.
- Пріоритети вибору серії (максимум / вартість 1.5 / спершу дамка) як ключ сортування серій — 🥈.
- Фук: зберегти «міг бити» з попереднього ходу й дати супернику зняти фігуру — 📎.
- Дамка «стоп за збитою» vs далека: дві функції генерації стрибків — 🥉.
- Dameo: рух шеренгою (знайти лінію ≥2 своїх, зсунути) + лише ортогональне взяття — 🥉.
- Frisian: лічильник ходів дамки поспіль + нічийні лічильники ендшпілю — 📎.

## Мапа на каталог
- Є: `rule-variants` ↔ уся ідея файла · `piece-move-patterns`, `piece-capture`, `pawn-promotion` · `no-moves-left` · `repetition-draw` · `field-size-picker` ↔ 8/10/12 · `match-setup` ↔ вибір варіанта · `multi-select` ↔ шеренга Dameo · `legal-move-highlight`, `hot-seat`, `ai-opponent`, `ai-minimax` · `help-window`, `game-screen`, `main-menu`, `end-screen` · `state-as-data`, `unit-tests`, `fixture-level-tests`.
- **Нема** → пропозиції карток:
  - `+forced-capture`, `+multi-jump`, `+max-capture-rule`, `+flying-piece` — див. checkers.md.
  - `+huffing` «Фук: штраф за пропущене взяття» · game-logic/opponent · 📎.
  - `+capture-priority` «Пріоритет серій взяття» · entities/legality · 🥈 · слоти {order: count|value|king-first|kings-taken}.
  - `+king-move-limit` «Ліміт ходів фігурою поспіль» · entities/legality · 🌱 · слоти {n: 3}.
  - `+phalanx-move` «Рух шеренгою» · entities/move · 🥉 — кілька фігур однією дією.
  - `+stop-behind-king` «Дамка зупиняється за збитою» · entities/move · 📎.

## Пропозиції до словників
- `+cond:can_capture`, `+cond:max_capture`, `+effect:jump_capture` — ще голоси за слова з checkers.md (ядро всіх варіантів).
- `+trigger:missed_capture` — гравець закінчив хід без обовʼязкового взяття.
- `+effect:forfeit` — сутність знімається як штраф (фук).
- `+cond:capture_value` — серія має максимальну вартість збитого (вага за типом фігури).
- `+cond:streak` — та сама фігура / дія повторилась N разів поспіль.
- `+effect:move_line` — зсув групи сутностей у лінії однією дією.
- `+card:huffing`, `+card:capture-priority`, `+card:king-move-limit`, `+card:phalanx-move`, `+card:stop-behind-king` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Draughts](https://en.wikipedia.org/wiki/Draughts) — таблиця варіантів з дошкою, кількістю, першим ходом і правилами взяття; фук; Bashni, Lasca, Dameo, Hexdame.
- [Wikipedia: Russian draughts](https://en.wikipedia.org/wiki/Russian_draughts), [International draughts](https://en.wikipedia.org/wiki/International_draughts) — база (детально в checkers.md).
- [Wikipedia: Pool checkers](https://en.wikipedia.org/wiki/Pool_checkers) — правила pool, 13 ходів для 3 дамок проти 1.
- [Wikipedia: Frisian draughts](https://en.wikipedia.org/wiki/Frisian_draughts) — 8 напрямків взяття, дамка = 1.5, правило трьох ходів, нічиї 7 ходів.
- [Wikipedia: Dameo](https://en.wikipedia.org/wiki/Dameo) — 18 шашок трапецією, шеренга, ортогональне взяття, максимум.
- [Wikipedia: Thai checkers](https://en.wikipedia.org/wiki/Thai_checkers) — 8 шашок, дамка продовжує з клітини одразу за збитою.
- [Lidraughts: варіанти](https://lidraughts.org/variant) — онлайн-версії (лінк зі checkers.md).

## Непевне
- (?) Рік 1900 — умовний «епоха кодифікації національних правил»; варіанти різного віку (Dameo — 2000).
- (?) Sri Lankan: лише «12×12 версія міжнародних» — кількість шашок і перший хід не бачив.
- (?) Thai: стартові ряди 8 шашок і чи шашка бʼє назад — у статті неповно; таблиця Draughts каже «ні».
- (?) Gothic: дошка «усі 64 клітини» і ортогональний рух — з памʼяті; таблиця дала лише 16 шашок і «бʼє вперед і вбік».
- (?) Pool: «чорні ходять першими» і «дамки бʼють усе доступне» — зі статті, що просить більше цитувань.
- (?) Armenian tama і Hexdame — лише однорядкові згадки, деталей не читав.
- (?) Dameo: чи шашка, що дійшла до краю посеред серії, продовжує як дамка — стаття мовчить.
