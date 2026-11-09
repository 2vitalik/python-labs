---
title: Circe chess (шахи «Цирцея»)
slug: circe-chess
aka: [Circe, Circé, Échecs Circé, Цирцея, Шахи Цирцеї, Anticirce, Circe Parrain, Mirror Circe, Platzwechsel Circe, PWC, Circe Rex Inclusive, Chameleon Circe, Progressive Circe]
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
year: 1967
platforms: [board, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Circe_chess", best: true, note: "клітини відродження за типами, зайнята клітина, рокіровка й подвійний крок після відродження, en passant, нотація Rxe8(Ng8), приклад з 1…Ba1!, 17 варіантів Circe"}
  - {kind: wiki, url: "https://fr.wikipedia.org/wiki/Échecs_Circé", note: "Monréal і Boyer, журнал Problème 1968; приклад f6 → b8; варіанти Circé caméléon, koko, miroir, symétrique, maléfique martien"}
  - {kind: other, url: "https://www.janko.at/Retros/Glossary/Circe.htm", note: "глосарій Janko: взяття нелегальне, якщо відродження шахує своєму королю; казкові фігури; Rex Inclusive; Atom-, Alsatian-, Hydra-, Antipoden-Circe"}
  - {kind: other, url: "https://raw.githubusercontent.com/thomas-maeder/popeye/develop/py-engl.txt", note: "мануал розвʼязувача Popeye: Circe як база + групи опцій (королі, клітина відродження, зайнята клітина, тип відродженої)"}
  - {kind: other, url: "http://www.jurajlorinc.com/chess/fi_c.htm", note: "Chess Composition Microweb: індекс задач з Circe, Parrain, Rex Inclusive, Couscous, Clone, Chameleon за завданнями"}
  - {kind: other, url: "https://www.chessvariants.com/difftaking.dir/circe.html", note: "Chess Variant Pages (Bodlaender) — лінк з Вікіпедії; агентам віддає 403"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=circe+chess+fairy+problem", note: "пошук; розбори задач"}
stage: v1
coverage: 60
mechanics: [piece-move-patterns, piece-capture, respawn, no-move-into-check, check-stalemate, checkmate, castling, en-passant, pawn-promotion, legal-move-highlight, hot-seat, turn-enforcement, rule-variants, move-notation, level-solver, game-screen, editor-window, help-window, match-setup, +capture-rebirth, +rebirth-self-check, +stipulation-solver, +condition-options]
proposes: ["+cond:attacked", "+cond:moved", "+ui:rebirth-preview", "+feature:condition-stack", "+card:capture-rebirth", "+card:stipulation-solver", "+axis:capture-fate"]
author: opus
date: 2026-11-09
---

# Circe chess — взята фігура миттєво відроджується на своїй стартовій клітині, якщо та вільна

## Суть
Звичайні шахи з одним додатковим правилом: взята фігура не зникає, а одразу стає на «свою» стартову клітину; якщо там хтось стоїть — гине, як у шахах. Придумав французький задачист П'єр Монреаль (1967), правила опубліковано з Ж.-П. Буаєром у журналі *Problème* (1968); назва — від чарівниці Цирцеї, що навчила Одіссея спуститися в підземний світ і повернутися. Як гра для партій — рідкість (здебільшого в парі з Progressive chess), а в шаховій композиції Circe — найпоширеніша казкова умова з десятками різновидів. Для курсу — найчистіша вправа «ефект після взяття»: одна функція `rebirth_square()` і одна нова перевірка легальності поверх рушія [chess.md](chess.md).

## Поле і час
- Дошка 8×8, стандартна розстановка (у задачах — довільна позиція з діаграми); хід = півхід, як у шахах.
- Кожна фігура має «домашню» клітину відродження, обчислювану з типу, кольору сторони й **клітини взяття** (вертикаль для пішака, колір поля для тури/коня/слона).
- Колір поля стає частиною правил: тура, кінь і слон відроджуються на стартовій клітині того самого кольору, що й клітина, де їх узяли.
- Стан партії ширший за шаховий: право рокіровки й право подвійного кроку можуть **повертатися** після відродження.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фігури K Q R B N P | piece | сторона, тип | ортодоксальні патерни ходу й взяття |
| Пішак (взятий) | piece | вертикаль взяття | відроджується на 2-й горизонталі своєї сторони на тій самій вертикалі (b4 → b2; чорний a4/a5 → a7); знову має подвійний крок |
| Тура / кінь (взяті) | piece | колір клітини взяття | на свою стартову клітину того ж кольору (чорна тура a6 → a8, a7 → h8; кінь a8 → g8, f6 → b8) |
| Слон (взятий) | piece | — | на стартову клітину свого кольору; слон завжди на полях одного кольору, тож це його рідна клітина |
| Ферзь (взятий) | piece | — | на d1 / d8 |
| Перетворена фігура (взята) | piece | тип після перетворення | відроджується як фігура, якою стала, а не як пішак |
| Відроджена тура | piece | право рокіровки | може рокірувати (якщо король не ходив) |
| Король | piece | royal | у базовій Circe не відроджується (бити короля не можна, як у шахах); у Rex Inclusive — відроджується на e1/e8 |
| Казкова фігура з явною стартовою клітиною | piece | — | на свою клітину (нічний вершник замість коня — на клітину коня) |
| Казкова фігура без стартової клітини | piece | — | як перетворена: на останню горизонталь вертикалі взяття (коник-grasshopper) |
| Клітина відродження | zone | вільна / зайнята | вільна — фігура повертається; зайнята будь-ким — фігура гине назавжди |

## Правила (КОЛИ → ЯКЩО → ТО)
**Відродження**
- КОЛИ `contact(p, q)` (хід p на клітину ворожої q) → ЯКЩО `legal(move)` and `free(rebirth_sq(q))` → ТО `disappear(q)`, `respawn(q, rebirth_sq)` — `rebirth_sq` = `custom: «клітина відродження за типом q і клітиною взяття»`.
- КОЛИ `contact(p, q)` → ЯКЩО `occupied(rebirth_sq(q), any)` → ТО `disappear(q)` — фігура знята назавжди, як у шахах (своя чи чужа фігура на клітині — неважливо).
- Наслідок: фігура, взята **на власній** клітині відродження (пішак на своїй 2-й горизонталі, тура на a1), не повертається — клітину вже зайняв той, хто взяв.
- КОЛИ `contact(p, pawn)` → ЯКЩО `free(rebirth_sq)` → ТО `respawn(pawn, custom: «2-га горизонталь своєї сторони, вертикаль взяття»)`, `set_state(pawn, never_moved)` — подвійний крок повертається.
- КОЛИ `contact(p, q)` → ЯКЩО `custom: «q — тура, кінь або слон»` → ТО `respawn(q, custom: «стартова клітина типу q того ж кольору, що й клітина взяття»)`; ферзь — `respawn(queen, d1|d8)`.
- КОЛИ `after(respawn(rook))` → ТО `set_state(rook, never_moved)` — рокіровка з відродженою турою дозволена.
- КОЛИ `contact(p, promoted_q)` → ТО `respawn(promoted_q, custom: «клітина фігури, якою вона стала»)`; у Frischauf-Circe — на останню горизонталь вертикалі взяття (Janko).

**Легальність і шах**
- КОЛИ `input(move(p, to))` (взяття) → ЯКЩО `custom: «після відродження взятої фігури свій король під ударом»` → ТО `block` — взяття нелегальне, якщо відроджена фігура шахує королю того, хто взяв (Janko).
- Приклад Вікіпедії: білі погрожують 1.Re1#; чорні грають 1…Ba1!: тепер після 2.Re1+ тура не може відродитися на a1 (зайнято), тож 2…Kxe1 легально — без слона на a1 відроджена тура шахувала б по 1-й горизонталі (наслідок правила Janko).
- КОЛИ `check(side)` → ЯКЩО `custom: «шах знімається лише взяттям, а взята фігура відродилася б так, що знову атакує»` → ТО `custom: «таке взяття не рятує»` — захист від шаху враховує, куди стане відроджена фігура.
- En passant: КОЛИ `contact(pawn, pawn_ep)` → ТО `respawn(pawn_ep, 2nd_rank)` — пішак, що взяв, стає просто перед відродженим, обидва заблоковані (Вікіпедія).
- Пропозиція Філіпа Коена (не загальне правило): КОЛИ `input(move)` → ЯКЩО `custom: «хід просто скасовує попередній хід суперника»` → ТО `block` (1.Qxg4 — слон відродився на c8 — 1…Bxg4 заборонено).

**Королі (Circe Rex Inclusive)**
- КОЛИ `contact(p, king)` → ЯКЩО `free(king_home)` → ТО `respawn(king, e1|e8)` — короля можна «взяти», він повертається.
- КОЛИ `check(side)` → ЯКЩО `free(king_home)` → ТО `custom: «шаху нема»` — король під шахом лише тоді, коли його домашня клітина зайнята; мат вимагає зайнятої e1/e8.

**Кінець партії**
- Перемога: мат (у задачах — виконати завдання: #n, h#n, s#n, =n, серійні ходи) · Нічия: пат і решта — як у шахах.
- Нотація: клітина відродження — у дужках після ходу: `Rxe8(Ng8)` — тура взяла коня на e8, кінь відродився на g8.

## Керування і ввід
- Фізична дошка — як шахи; гравці самі переставляють взяту фігуру на клітину відродження.
- Цифрова версія: клік/drag фігури; при наведенні на взяття — показати, де відродиться взята фігура і чи відродиться взагалі; підсвітка легальних ходів практично обовʼязкова (заборони через відродження неочевидні).
- Розвʼязувач Popeye: текстовий блок задачі з `condition Circe` і опціями (`Circe Mirror`, `Circe Parrain`, `Circe RexInclusive`…), регістр неважливий.

## Вікна, меню, HUD
(цифрова версія; оригінал — діаграма в журналі й консольний розвʼязувач)
- `match-setup`: базова Circe або варіант, опції (королі вкл/викл, правило зайнятої клітини, тип відродженої).
- `game-screen`: дошка, `rebirth-preview` (контур фігури на клітині відродження при наведенні на взяття; хрестик — «загине»), `legal-move-highlight`, `move-list` з дужками `(Ng8)`, `captured-pieces` (лише ті, що загинули назавжди).
- `editor-window` — розстановка позиції задачі й завдання; `solutions-window` — знайдені розвʼязки.
- `help-window` — таблиця клітин відродження з прикладами; `end-screen` — мат, пат.
- Переходи: main-menu → match-setup → game-screen → end-screen; main-menu → editor-window → solutions-window.

## Фічі поза полем
- `custom-rules` — Circe як умова партії; кілька опцій одночасно (Popeye: база + опції, а Circe ще й комбінується з іншими умовами) — `+feature:condition-stack`.
- `mode-puzzle` — шахова композиція: прямий мат, допоміжний (h#), самомат (s#), пат, серійні ходи, ретро; задач з Circe — найбільше серед казкових умов.
- Цілі партії — зазвичай **Progressive Circe** (серії ходів 1, 2, 3… — [multi-move-chess.md](multi-move-chess.md)).
- Розвʼязувач (Popeye) — окрема програма; у Вікіпедії згадано Java-програму Еда Фрідлендера на Chess Variant Pages (не відкрив).

## Варіації й родичі
- [fairy-chess-conditions.md](fairy-chess-conditions.md) — інші умови композиції (Andernach, Madrasi, Grid); Circe там лише згадано, тут — окремо як найвідоміша.
- [lichess-variants.md](lichess-variants.md) (Crazyhouse — взята йде в руку суперника), [bughouse.md](bughouse.md), [chess-rule-twists.md](chess-rule-twists.md) (Hostage — взяту можна викупити) — інші відповіді на «куди дівається взята фігура». Карта Rebirth у [knightmare-chess.md](knightmare-chess.md) — та сама дія разово.
- **Хто відроджується**: взята (Circe) · та, що взяла, а взята зникає (Anticirce: Cheylan — брати на своїй клітині відродження не можна; Calvet — можна) · взята відроджується, та, що взяла, гине (Kamikaze) · бити можна лише зі своєї стартової клітини, взята зникає (Martian / Mars Circe).
- **Де відроджується**: стартова клітина (Circe) · клітина, де відродилася б фігура протилежного кольору (Mirror) · клітина взяття, віддзеркалена через центр дошки (Symmetrical) · клітина з діаграми задачі (Diagram) · клітина, з якої пішов той, хто взяв (Platzwechsel, PWC) · клітина за вектором **наступного** ходу суперника від клітини взяття (Parrain — відродження відкладене) · за вектором самого ходу-взяття, одразу (Equipollents) · клітина відродження того, хто взяв (CouCou / CousCous; взятий пішак стає на останню горизонталь і перетворюється) · на відстані (4,4) (Antipoden) · одразу дві клітини — звичайна й дзеркальна через лінію d/e (Hydra).
- **Якщо клітина зайнята**: фігура гине (Circe) · взяття нелегальне (Strict) · фігуру на клітині знято, відроджена стає замість неї (Assassin) · відроджена ховається під фігурою й виходить, коли та піде (Volcanic) · ще Parachute (у Popeye; визначення не бачив).
- **Яким відроджується**: тим самим · наступним у циклі кінь → слон → тура → ферзь → кінь (Chameleon; пішаки ні) · типом того, хто взяв (Clone) · Turncoat, Einstein (опції Popeye).
- **Королі**: Rex Exclusive (типово для Circe) · Rex Inclusive.
- Інші: Atom-Circe (на клітини відродження йдуть і фігури, сусідні з клітиною взяття) · Alsatian (взяття заборонене, якщо дає нелегальну за шахами позицію).
- Popeye зводить усе це до бази `Circe | AntiCirce | MarsCirce | AntiMarsCirce` + опції з груп «королі», «клітина відродження», «адаптація клітини», «тип відродженої», «зайнята клітина», «самоблок» — готова структура для конструктора правил.

## Цікавинки для курсу
- `rebirth_square(piece, capture_sq)`: таблиця за типом + колір поля + вертикаль для пішака — 🌱.
- Легальність з відродженням: зробити взяття, поставити відроджену, перевірити свого короля, відкотити — 📎 поверх готового `no-move-into-check`.
- Повернення прав: рокіровка відродженої тури, подвійний крок відродженого пішака — стан фігури, а не клітини — 📎.
- Rex Inclusive: «шах» залежить від того, чи зайнята домашня клітина короля — 📎.
- Circe як конструктор: стратегії «хто / де / якщо зайнято / яким» окремими функціями й комбінування (Mirror + Assassin + Chameleon) — 🥈.
- Parrain: відкладене відродження за вектором наступного ходу (стан «у підвішеному стані» між півходами); Volcanic — стек фігур у клітині — 🥉.
- Розвʼязувач «мат за N / допоміжний мат» з Circe (перебір з відсіканням, як Popeye) — 🥇.

## Мапа на каталог
- Є: `piece-move-patterns` · `piece-capture` ↔ взяття з подальшим відродженням · `respawn` ↔ відродження на стартовій клітині · `no-move-into-check` ↔ з перевіркою відродженої фігури · `check-stalemate` · `checkmate` · `castling` ↔ відроджена тура рокірує · `en-passant` ↔ блокування пішаків · `pawn-promotion` ↔ перетворена відроджується як нова фігура · `legal-move-highlight` · `hot-seat` · `turn-enforcement` · `rule-variants` ↔ варіанти Circe як перемикачі · `move-notation` ↔ `Rxe8(Ng8)` · `level-solver` ↔ Popeye · `game-screen` · `editor-window` · `help-window` · `match-setup`.
- **Нема** → пропозиції карток:
  - `+capture-rebirth` «Взята фігура відроджується на розрахованій клітині» · entities/death · 🥉 · слоти {who: captured | capturer | both; square: home | mirror | symmetry | diagram | pwc | parrain | equipollents; occupied: vanish | strict | assassin | volcanic; kings: bool; type: same | chameleon | clone}.
  - `+rebirth-self-check` «Взяття нелегальне, якщо відроджена фігура шахує» — слот у `no-move-into-check`, окремої картки не треба.
  - `+stipulation-solver` «Розвʼязувач задач: мат за N, допоміжний, самомат» · game-logic/opponent · 🥇 (уже пропонував fairy-chess-conditions).
  - `+condition-options` «Умова = база + опції з груп» · game-logic/constraints · 🥈 — родич `rule-variants`.

## Пропозиції до словників
- `+cond:attacked` — підтверджую (chess.md, fairy-chess-conditions): тут «відроджена фігура атакує свого короля».
- `+cond:moved` — підтверджую: після відродження тура й пішак знову «не ходили».
- `+ui:rebirth-preview` — контур фігури на клітині, куди вона відродиться, при наведенні на взяття (Circe; родич `ghost-piece` у Tetris).
- `+feature:condition-stack` — підтверджую (fairy-chess-conditions): кілька умов/опцій одночасно.
- `+card:capture-rebirth` · `+card:stipulation-solver` — див. «Мапа на каталог».
- `+axis:capture-fate` — вісь «доля взятої фігури»: зникає · відроджується (Circe) · у руку суперника (Crazyhouse) · переходить до суперника (Andernach) · викуп (Hostage).

## Джерела
- ⭐ [Wikipedia: Circe chess](https://en.wikipedia.org/wiki/Circe_chess) — Монреаль 1967, Монреаль і Буаєр у *Problème* 1968; клітини відродження, зайнята клітина, рокіровка й подвійний крок, перетворені фігури, en passant, пропозиція Коена, приклад 1…Ba1!, нотація, 17 варіантів.
- [Wikipedia FR: Échecs Circé](https://fr.wikipedia.org/wiki/Échecs_Circé) — ті самі правила, приклади f6 → b8 і h8; список варіантів (caméléon, parrain, clone, diagramme, kamikaze, koko, maléfique martien, miroir, Platzwechsel, symétrique).
- [Janko: Circe](https://www.janko.at/Retros/Glossary/Circe.htm) — взяття нелегальне через шах від відродженої; приклади a4/a5 → a7, a6 → a8, a7 → h8, a8 → g8; казкові фігури; Rex Inclusive; Atom-, Alsatian-, Hydra-, Antipoden-, Vulcan-, Frischauf-Circe.
- [Popeye: py-engl.txt](https://raw.githubusercontent.com/thomas-maeder/popeye/develop/py-engl.txt) — бази Circe/AntiCirce/MarsCirce/AntiMarsCirce і групи опцій; традиційні назви як комбінації опцій.
- [Chess Composition Microweb: C](http://www.jurajlorinc.com/chess/fi_c.htm) — індекс задач за умовами Circe і завданнями, без визначень.
- [Chess Variant Pages: Circe](https://www.chessvariants.com/difftaking.dir/circe.html) — лінк з Вікіпедії, агенту не відкрився.
- YouTube: пошук «circe chess fairy problem».

## Непевне
- (?) Королі в базовій Circe: Вікіпедія про це мовчить; «короля не беруть, як у шахах» — з Popeye (RexExclusive — типова опція) і Janko (Rex Inclusive як окремий варіант).
- (?) Приклад 1…Ba1!: що без слона відроджена на a1 тура шахувала б, — виведено з правила Janko, у Вікіпедії сказано лише «тура не може відродитися на a1».
- (?) Правило Коена — пропозиція, не стандарт; чи вживають його в партіях, не знайшов.
- (?) Визначення Super Circe, Parachute, Turncoat, Einstein — бачив лише назви опцій у Popeye.
- (?) Пішак, узятий на власній 2-й горизонталі, не відроджується — наслідок правила «клітина зайнята», прямо в джерелах не сказано.
- (?) Цифрових реалізацій для партій (не розвʼязувачів) не перевірив; вікна вище — проєкція.
