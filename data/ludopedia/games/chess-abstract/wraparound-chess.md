---
title: Шахи без країв — циліндричні (Cylinder) і кругові (Circular / Byzantine)
slug: wraparound-chess
aka: [Cylinder chess, Циліндричні шахи, Circular chess, Кругові шахи, Byzantine chess, Візантійські шахи, Shatranj al-Muddawara, Round chess, Toroidal chess, Torus chess]
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
year: 967
platforms: [board, web, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Circular_chess", best: true, note: "кільцева дошка 4×16, сучасні правила (Reynolds 1983), історичні (Amuli 1325), цитадельний варіант, снафлінг, чемпіонати в Лінкольні"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Cylinder_chess", note: "a- і h-вертикалі склеєні, en passant через шов, три правила рокіровки, нуль-хід, тор і горизонтальний циліндр, цінність фігур Muller"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Byzantine_chess", note: "переадресація на Circular chess"}
  - {kind: other, url: "https://greenchess.net/rules.php?v=circular", note: "Green Chess: кругові шахи — пішаки двома групами, заборона нуль-ходу, лише мат ферзем із базових"}
  - {kind: other, url: "https://www.chessvariants.com/shape.dir/circular.html", note: "Chess Variant Pages: Circular chess (лінк зі статті)"}
  - {kind: bgg, url: "https://boardgamegeek.com/boardgame/34856", note: "BGG: Circular chess (лінк зі статті)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=circular+chess", note: "пошук; партії на круглій дошці"}
stage: v1
coverage: 60
mechanics: [wrap-edges, piece-move-patterns, piece-capture, legal-move-highlight, no-move-into-check, check-stalemate, checkmate, pawn-promotion, castling, en-passant, repetition-draw, hot-seat, ai-opponent, drag-drop-piece, cell-click, rule-variants, game-screen, end-screen, help-window, +null-move-ban, +ring-board, +king-capture-win, +stalemate-win, +bare-king-loss, +citadel-draw, +polar-render]
proposes: ["+cond:returns_to_start", "+cond:crosses_seam", "+effect:remove_blocked_pawns", "+trigger:check", "+ui:seam-marker", "+ui:polar-board", "+axis:field-wrap", "+card:null-move-ban", "+card:ring-board", "+card:bare-king-loss", "+card:citadel-draw", "+card:polar-render"]
author: opus
date: 2026-11-09
---

# Шахи без країв — та сама шахова «фізика» на дошці, склеєній у циліндр або кільце

## Суть
Два старі варіанти, що змінюють лише **топологію** дошки, а фігури лишають шаховими. **Циліндричні шахи**: вертикалі a і h — сусіди, фігура, що йде за лівий край, виходить справа; верх і низ — звичайні краї. **Кругові (візантійські) шахи**: шахівниця розрізана навпіл і зігнута в кільце з 4 концентричних кругів по 16 клітин — кутів і країв «вздовж» немає зовсім. Обидва показують, як одна топологічна зміна ламає теорію: слабшають коні, сильніють тури/слони, класичні мати в кут неможливі.

## Поле і час
- **Cylinder**: 8×8, шов між a і h (ряди не склеєні); стандартна розстановка; хід = як у шахах.
- **Horizontal cylinder** (ряди 1 і 8 склеєні) і **Toroidal** (обидві пари країв): стандартна розстановка неможлива — королі стартували б уже в маті.
- **Circular**: 4 кільця × 16 клітин = 64; топологічно — бічна поверхня циліндра 4×16 (внутрішнє й зовнішнє кільця — «краї», по колу краю нема). Дві позначені лінії на протилежних боках кола — кожна армія стоїть навколо своєї.
- Розстановка Circular (сучасна): внутрішнє кільце — король і ферзь (ферзь на полі свого кольору), друге — слони, третє — коні, зовнішнє — тури; пішаки — перед фігурами з обох боків, тобто дві групи по 4 пішаки дивляться в протилежні боки кола.
- Рендер: циліндр малюють плоскою дошкою з позначеним швом; кільце — полярною сіткою.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фігури K Q R B N P | piece | як у шахах | патерни без змін; лінії продовжуються через шов |
| Шов (a|h — Cylinder; лінія між арміями — Circular) | zone | невидима межа | рух через шов триває на іншому боці; сама лінія ролі в грі не має |
| Пішаки двох груп (Circular) | piece | 4 + 4 на сторону | половина йде за годинниковою, половина — проти, обидві до бази суперника |
| Цитадель (історичний варіант) | zone | 2 клітини в центрі | король, що дійшов сюди, — примусова нічия |
| Радник / ферзь (історичний) | piece | шатрандж | ходи шатранджу (ферзь на 1 по діагоналі), не сучасний ферзь |
| Слон / альфіл (історичний) | piece | шатрандж | стрибок на 2 по діагоналі (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
Спільне — циклічна дошка:
- КОЛИ `edge(p)` → ЯКЩО `custom: «перетинає склеєний край (a|h у Cylinder; коло в Circular)»` → ТО `wrap(p)` і рух триває за патерном.
- КОЛИ `edge(p)` → ЯКЩО `custom: «незклеєний край (ряд 1/8 у Cylinder; внутрішнє/зовнішнє кільце в Circular)»` → ТО `block`.
- КОЛИ `input(move(p, to))` → ЯКЩО `custom: «хід повертає позицію без змін — тура/ферзь обійшли коло до своєї клітини»` (кандидат `+cond:returns_to_start`) → ТО `block` — нуль-хід заборонено (у Cylinder — опційне правило).
- КОЛИ `input(move(p, to))` → ЯКЩО `legal(move)` → ТО `move(p, to)`, `end_turn`; шах, мат, пат — як у шахах.

Cylinder:
- Тура з a3 доходить до h3 ліворуч навіть з фігурою на b3; слон c1 → a3 → h4 «через шов».
- En passant працює через шов: після …h7–h5 білий пішак a5 бʼє axh6.
- Рокіровка — три домовленості: (1) звичайна, але не з турою через шов; (2) заборонена — на циліндрі всі вертикалі однаково відкриті; (3) звичайна плюс через шов, король іде на 2 у бік тури.
- Нуль-хід (опційно): КОЛИ `input(null_move(R|Q))` → ЯКЩО `custom: «фігура обходить коло й повертається»` → ТО дозволено як «пропуск» — рідко в партіях, часто в задачах (цугцванг).
- Ендшпіль: K+R не матують голого короля; дві тури матують «драбиною» по рядах, але не по вертикалях.

Circular (сучасні правила, Reynolds 1983):
- Рокіровки й en passant нема.
- КОЛИ `custom: «пішак пройшов 6 клітин від старту (поле перед лінією бази суперника)»` → ТО `choose({Q, R, B, N})`, `transform(вибране)`.
- Оголошувати шах не обовʼязково; КОЛИ `custom: «суперник сходив під шах або не вийшов з-під нього»` → ТО `input(capture(king))` дозволено → `win` («snaffling», вирішувало партії чемпіонату світу).
- Мат, пат — як у шахах; K+P проти K: захисник без патового порятунку, рятує лише взяття пішака.

Circular (історичні правила, Amuli 1325, шатрандж аль-мудаввара):
- Ходи — шатранджу; перетворення нема (нема заднього ряду).
- КОЛИ `custom: «два пішаки однієї сторони, що йдуть назустріч, заблокували один одного»` → ТО суперник може `disappear(обидва)`, не витрачаючи ходу (кандидат `+effect:remove_blocked_pawns`).
- КОЛИ `no_moves(side)` → ЯКЩО `not in_check(side)` → ТО `win(opponent)` — пат виграє той, хто запатував.
- КОЛИ `count(own_pieces, ==, 1)` → ЯКЩО `custom: «наступним ходом не можу теж лишити суперника з голим королем»` → ТО `lose`; інакше `draw`.
- Цитадельний варіант: КОЛИ `enter(king, citadel)` → ТО `draw` (примусова нічия).

- Перемога: мат · взяття короля після ігнорованого шаху (Circular) · пат і голий король (історичні) · Нічия: пат (Cylinder, сучасні Circular), король у цитаделі, обопільний голий король.

## Керування і ввід
- Як у шахах: клік/drag фігури (цифрова версія). На циліндрі — підсвітка ходів, що «загортаються» через шов, обовʼязкова: людина не бачить цих ліній.
- Circular на екрані: полярна дошка, клік у сектор кільця; на фізичній дошці — фігури на кільцях.

## Вікна, меню, HUD
- `match-setup` (цифрова версія): топологія (cylinder / horizontal / torus / ring), правило рокіровки, нуль-хід вкл/вимк, сучасні чи історичні правила.
- `game-screen`: Cylinder — плоска дошка з `seam-marker` (позначений шов) або «нескінченна» дошка з повтореними вертикалями; Circular — `polar-board`; `legal-move-highlight`, `move-list`, `player-clock`.
- `end-screen` — мат / snaffle / пат / цитадель.
- `help-window` — правила і приклади ходів через шов.
- Переходи: main-menu → match-setup → game-screen → end-screen.

## Фічі поза полем
- `custom-rules` — топологія й домовленості як перемикачі.
- `online-multiplayer` (BrainKing, CylinderChess.com, Green Chess — за лінками статті) (?).
- `rules-page` для задач (цугцванг нуль-ходом на циліндрі).
- Турніри: чемпіонат світу з кругових шахів у Лінкольні з 1996 (Circular Chess Society).

## Варіації й родичі
- [chess.md](chess.md) — база; [glinski-hex-chess.md](glinski-hex-chess.md) і [5d-chess.md](5d-chess.md) — інша геометрія шахів.
- [chess-rule-twists.md](chess-rule-twists.md) — Alice (дві дошки), Dark (взяття короля): інші осі.
- Тор у корпусі: картка `wrap-edges` (Pac-Man-тунель, Life на торі) — тут вона застосована до ковзних фігур.
- Історичне коріння: «візантійські круглі шахи» в al-Masudi (967), шатрандж аль-мудаввара (Amuli, 1325).
- **Осі варіацій**:
  - **Що склеєно**: нічого · вертикалі (Cylinder) · ряди (horizontal) · обидві пари (тор) · кільце з радіальними краями (Circular).
  - **Нуль-хід**: заборонено · дозволено лише турі/ферзю (задачі).
  - **Рокіровка**: звичайна · через шов · заборонена.
  - **Пішаки**: одна група вперед · дві групи назустріч одна одній (Circular).
  - **Кінець**: мат · + snaffle · + пат/голий король перемагає (історичні) · цитадель = нічия.

## Цікавинки для курсу
- Тор для ковзних фігур: координата `x mod 8`, кінець ковзання — коли повернувся у старт — 🌱.
- Заборона нуль-ходу (позиція не змінилась) — 🌱; перевірка мату на циліндрі (K+R не матує) — 📎.
- Полярний рендер дошки 4×16 і клік у сектор — 📎.
- Порівняння цінності фігур на торі/циліндрі (мобільність з усіх клітин) — 🥉.
- Історичні правила: пат-перемога, голий король, знищення заблокованих пішаків — 📎.
- Тор-шахи: знайти стартову розстановку без мату — 🥉 (перебір/пошук).

## Мапа на каталог
- Є: `wrap-edges` ↔ шов a|h і кільце · `piece-move-patterns` · `piece-capture` · `legal-move-highlight` · `no-move-into-check` · `check-stalemate` · `checkmate` · `pawn-promotion` ↔ після 6 клітин (Circular) · `castling` ↔ три домовленості (Cylinder) · `en-passant` ↔ через шов · `repetition-draw` · `hot-seat` · `ai-opponent` · `drag-drop-piece` · `cell-click` · `rule-variants` ↔ топологія як перемикач · `game-screen` · `end-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+null-move-ban` «Хід, що лишає позицію незмінною, заборонено» · entities/legality · 🌱.
  - `+ring-board` «Кільцева дошка: кола × сектори» · entities/move · 📎 · слоти {rings: 4, sectors: 16}.
  - `+polar-render` «Полярний рендер сітки» · interface/render · 📎.
  - `+bare-king-loss` «Голий король програє» · game-logic/win · 🌱 — шатрандж, історичний Circular.
  - `+citadel-draw` «Клітина-притулок: король там = нічия» · game-logic/win · 🌱.
  - `+king-capture-win`, `+stalemate-win` — див. [chess-rule-twists.md](chess-rule-twists.md).

## Пропозиції до словників
- `+cond:returns_to_start(p)` — хід повертає фігуру у вихідну клітину (нуль-хід).
- `+cond:crosses_seam(move)` — хід перетинає склеєний край (правила рокіровки й підсвітки на циліндрі).
- `+effect:remove_blocked_pawns` — зняти пару своїх пішаків-зустрічних (історичний Circular), без витрати ходу.
- `+trigger:check` — підтверджую (snaffling: шах проігноровано → короля можна взяти).
- `+ui:seam-marker` — лінія склейки на плоскій дошці; `+ui:polar-board` — дошка-кільце.
- `+axis:field-wrap` — `none` · `cylinder-x` · `cylinder-y` · `torus` · `ring` (зараз `wrap` — лише булеве поле `Part kind=field`).
- `+card:null-move-ban` · `+card:ring-board` · `+card:bare-king-loss` · `+card:citadel-draw` · `+card:polar-render` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Circular chess](https://en.wikipedia.org/wiki/Circular_chess) — дошка 4×16, сучасна розстановка й правила, промоція після 6 клітин, snaffling, історичні правила Amuli 1325, цитадель, al-Masudi 967, Reynolds 1983, чемпіонати з 1996.
- [Wikipedia: Cylinder chess](https://en.wikipedia.org/wiki/Cylinder_chess) — шов, приклади тури й слона, en passant через шов, рокіровка ×3, нуль-хід, оцінки фігур Muller (P 1, N 3¼, B 4, R 5, Q 11), горизонтальний циліндр і тор, Pritchard 1994, Mongredien 1926.
- [Wikipedia: Byzantine chess](https://en.wikipedia.org/wiki/Byzantine_chess) — відкрилась як Circular chess.
- [Green Chess: Circular](https://greenchess.net/rules.php?v=circular) — дві групи пішаків, промоція перед лінією, заборона нуль-ходу, з базових матів лише ферзем; автор Dave Reynolds 1983.
- [Chess Variant Pages: Circular](https://www.chessvariants.com/shape.dir/circular.html) · [BGG](https://boardgamegeek.com/boardgame/34856) — лінки зі статті, не відкривав.
- YouTube: пошук «circular chess».

## Непевне
- (?) Походження циліндричних шахів: у черзі «середньовічні», стаття джерел до Mongredien 1926 не дає; рік у шапці — найраніша згадка круглих шахів (967).
- (?) Як слон рухається по кільцю: діагональ «закручується» між кільцями й упирається у внутрішнє/зовнішнє коло — деталей у джерелах не знайшов.
- (?) Хід альфіла й радника в історичному Circular — за загальними правилами шатранджу, стаття не уточнює.
- (?) Цитадель: чи будь-яку цитадель, чи лише ворожу (джерела розходяться/мовчать).
- (?) Дата заснування Circular Chess Society — у статті 1993 і 1996 одночасно.
