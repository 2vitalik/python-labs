---
title: Knightmare Chess
slug: knightmare-chess
aka: [Tempête sur l'échiquier, Storm on the Chessboard, Knightmare Chess 2, More Chaos on the Chessboard, KC]
family: chess-abstract
also: [board-digital]
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: hidden
  random: runtime
  goal: state
year: 1996
platforms: [board]
links:
  - {kind: official, url: "https://www.sjgames.com/knightmare/img/knightmare-chess-rules.pdf", best: true, note: "правила 3-го видання (v3.0, 2014): колода на 150 очок, рука 5, одна карта на свій і одна на чужий хід, Checkmate Rule, конфлікти, пішаки, рокіровка, пат, варіанти, карта Knightmare"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Knightmare_Chess", note: "Faidutti і Cléquin, переклад французької Tempête sur l'échiquier; SJG 1996; набори по 80 карт; очки й унікальні карти; приклад Demotion; рецензії"}
  - {kind: official, url: "https://www.sjgames.com/knightmare/", note: "сторінка SJG: 160 карт (158 + 2 порожні), лінки на правила, FAQ, errata, списки карт, варіанти"}
  - {kind: other, url: "https://www.sjgames.com/knightmare/kc_rules.pdf", note: "правила 2-го видання (1996–1997), приклад карти Blessing"}
  - {kind: other, url: "https://www.sjgames.com/knightmare/kc2_rules.pdf", note: "правила Knightmare Chess 2 (1998): «goal»-карти в Checkmate Rule, порожні карти, приклад Second Sight"}
  - {kind: other, url: "https://www.sjgames.com/knightmare/kc_faq.html", note: "офіційний FAQ: мат і втеча картою, пат, пішаки, рокіровка через шах"}
  - {kind: other, url: "https://www.sjgames.com/knightmare/cards.html", note: "офіційні рішення по окремих картах (Bog, Forbidden City, Seat of Power, Coup, King of the Mountain…)"}
  - {kind: other, url: "https://www.sjgames.com/knightmare/errata.html", note: "errata: Under Elf Hill, Unbeliever, Fatal Attraction; конфлікти й призупинення ефектів"}
  - {kind: other, url: "https://www.sjgames.com/knightmare/list_sets.html", note: "списки назв карт обох наборів"}
  - {kind: other, url: "https://www.sjgames.com/knightmare/2nded.html", note: "зміни 2-го видання (вересень 1997)"}
  - {kind: other, url: "https://www.sjgames.com/knightmare/kc_intro.html", note: "вступ: Fireball, Under Elf Hill, Crab, Madman; варіант з відкритими картами"}
  - {kind: bgg, url: "https://www.boardgamegeek.com/boardgame/227", note: "BGG (лінк з Вікіпедії)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Knightmare+Chess+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [piece-move-patterns, piece-capture, checkmate, check-stalemate, no-move-into-check, castling, en-passant, pawn-promotion, hot-seat, turn-enforcement, rule-variants, explode-area, impassable-cells, floor-types, temporary-modes, respawn, pocket, game-screen, help-window, codex-window, match-setup, end-screen, +card-hand, +deck-builder, +card-modifies-rules, +continuing-effect-card, +rule-precedence, +card-timing-windows, +cancel-opponent-turn, +deck-point-budget, +goal-card]
proposes: ["+trigger:card_played", "+trigger:deck_empty", "+effect:draw_card", "+effect:discard", "+effect:cancel_turn", "+cond:card_window", "+ui:card-hand", "+ui:deck-counter", "+ui:continuing-effects-row", "+ui:transform-marker", "+window:deck-builder", "+window:response-prompt", "+card:card-modifies-rules", "+card:continuing-effect-card", "+card:rule-precedence"]
author: opus
date: 2026-11-09
---

# Knightmare Chess — шахи, де кожен хід можна супроводити картою, що ламає одне правило

## Суть
Звичайні шахи плюс у кожного гравця власна колода карт; на свій хід можна зіграти одну карту, і ще одну — на хід суперника. Карта змінює рух фігури, переставляє чужі фігури, створює спеціальні клітини, перетворює фігуру на нову або діє до кінця гри; мета лишається — мат. Головне правило гри — **Checkmate Rule**: звичайна карта не може сама дати мат чи взяти короля. Французький оригінал *Tempête sur l'échiquier* (П'єр Клекен, Бруно Файдутті), англійське видання Steve Jackson Games 1996 року; не плутати з [capablanca-chess.md](capablanca-chess.md) — тут дошка й фігури стандартні, змінюються правила.

## Поле і час
- Дошка 8×8 і стандартна розстановка; поза дошкою — у кожного колода, рука з 5 карт, скид; праворуч від дошки — ряд карт з тривалим ефектом (Continuing Effect).
- Хід (turn) = один хід фігурою **і** за бажанням одна карта (до, замість або після ходу) або скидання однієї карти; суперник може зіграти одну карту під час або одразу після твого ходу.
- Деякі карти змінюють саму дошку: заборонена клітина, клітина-пастка, стіна між клітинами, «стиснення» дошки до прямокутника з усіма фігурами, поворот дошки (за офіційними рішеннями по картах).
- Темп — шаховий без годинника; партії коротші за шахи, бо довгі плани ламаються за кілька ходів (вступ SJG).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фігури K Q R B N P | piece | сторона, тип | шахові патерни з поправками на активні карти |
| Пішак на 1-й або 2-й горизонталі | piece | — | завжди може зробити подвійний крок, навіть якщо вже ходив; такий хід можна взяти на проході |
| Перетворена фігура (Crab, Prince, Amazon, Princess…) | piece | нова назва, маркер під фігурою | нові вміння від карти з тривалим ефектом; карти, що називають вихідну фігуру, діють і на неї |
| Нейтральна фігура (карта Neutrality) | neutral | — | нічия; власник може її бити (офіційні рішення) |
| Карта | resource | очки 2–10, `*` — унікальна, час гри, тривалий ефект так/ні | у руці, грається в момент, написаний на карті |
| Колода | supply | сума очок (типово 150) | з неї добирають до 5; вичерпана — не перетасовується |
| Рука | supply | 5 карт | завжди 5, доки є колода; прихована від суперника |
| Скид | supply | відкритий | сюди йде зіграна й скинута карта; деякі карти повертають звідти |
| Карта з тривалим ефектом | zone | умова дії | лежить праворуч від дошки; коли умова не виконана — ефект призупинено, карта лишається |
| Маркер (монетка, фішка, стікер) | mark | — | під перетвореною фігурою й на карті, що її перетворила |
| Взята фігура | piece | — | її можна повернути картою (Return, Resurrection, Rebirth) |
| Мертва фігура (dead) | piece | — | відкладена назавжди, жодна карта її не поверне |
| Клітина Forbidden City | static | — | туди не може стати жодна фігура (офіційні рішення) |
| Клітина Seat of Power | terrain | — | фігура на ній ходить як ферзь (офіційні рішення) |
| Клітина Man-Trap | hazard | — | бере фігуру, що на неї стала (офіційні рішення) |
| Fortification | static | між клітинами | стіна, яку не можна перетнути ортогонально (офіційні рішення) |

## Правила (КОЛИ → ЯКЩО → ТО)
**Підготовка і цикл карт**
- КОЛИ `game_start` → ТО `custom: «поділити карти навпіл; кожен збирає колоду на 150 очок; карта з * — не більше однієї в колоді»`, `custom: «перетасувати свою колоду, взяти 5 карт»`; решта карт — поза грою.
- КОЛИ `input(play_card)` → ЯКЩО `turn_of(side)` and `custom: «цього ходу карта ще не зіграна»` and `custom: «момент гри збігається з написаним на карті»` → ТО `custom: «ефект карти одразу»`, `custom: «карта у скид»`, `custom: «добрати 1 карту»`.
- Моменти гри (з карт і правил): до ходу · замість ходу · після ходу · одразу після ходу суперника · у відповідь на карту суперника · на хід суперника, навіть до його карти.
- КОЛИ `input(play_card)` → ЯКЩО `not turn_of(side)` and `custom: «на цей хід суперника карта ще не зіграна»` → ТО `custom: «ефект карти»` — не більше однієї карти на свій хід і однієї на чужий.
- КОЛИ `turn_end(side)` → ЯКЩО `custom: «цього ходу карту не грав»` → ТО `choose(skip | discard)`: `custom: «скинути 1 карту, добрати 1»`; на хід суперника скидати не можна.
- КОЛИ `custom: «колода вичерпана»` (кандидат +trigger:deck_empty) → ТО `custom: «скид не перетасовується; рука догравається»`; коли рука порожня — далі звичайні шахи з активними тривалими ефектами.
- Карта ніколи не обовʼязкова: без карти хід — за шахами з поправками на активні тривалі ефекти.

**Тривалі ефекти й перетворення**
- КОЛИ `input(play_card)` → ЯКЩО `custom: «карта з Continuing Effect»` → ТО `custom: «покласти праворуч від дошки, діє до скасування»`.
- КОЛИ `custom: «умова тривалого ефекту перестала виконуватись»` → ТО `custom: «ефект призупинено, карта не скидається; умова повернулась — ефект знову діє»`.
- КОЛИ `input(play_card)` → ЯКЩО `custom: «карта перетворює фігуру»` → ТО `transform(piece, new_type)`, `custom: «маркер під фігурою й на карті»`.
- КОЛИ `contact(enemy, transformed)` → ЯКЩО `custom: «фігуру одразу врятовано картою (того ж або наступного ходу)»` → ТО `custom: «вміння зберігаються»`; інакше `custom: «повернута пізніше — як вихідна фігура»`.

**Checkmate Rule (вища за все)**
- КОЛИ `input(play_card)` → ЯКЩО `custom: «звичайна карта прямо дає мат, «гол»-перемогу або бере короля»` → ТО `custom: «карта без ефекту, але вважається зіграною: у скид, добрати нову»`.
- КОЛИ `custom: «карта «до ходу» дала шах»` → ТО `custom: «взяти короля звичайним ходом не можна — король не береться»`; але карта «до ходу» (прибрати фігуру-перешкоду) + звичайний хід з матом — легально.
- КОЛИ `custom: «тривалий ефект спричиняє або допомагає мату»` → ТО `win` — мат дійсний, карта лишається в грі.
- КОЛИ `check(side)` → ЯКЩО `custom: «тим самим ходом зіграно карту, що знімає шах»` → ТО `custom: «можна поставити або лишити короля під шахом»`; КОЛИ `turn_end(side)` → ЯКЩО `in_check(side)` → ТО `block` (FAQ: наприкінці ходу король не може бути під шахом).
- Фігура не шахує ходом, який карта зробила неможливим (заблокована картою фігура не шахує взагалі).

**Конфлікти**
- КОЛИ `custom: «карта суперечить правилам шахів»` → ТО `custom: «діє карта»`.
- КОЛИ `custom: «дві карти суперечать одна одній»` → ЯКЩО `custom: «одна з тривалим ефектом, інша ні»` → ТО `custom: «діє тривала»`; інакше `custom: «діє остання зіграна»`.

**Пішаки, рокіровка, пат**
- КОЛИ `input(move(pawn, +2))` → ЯКЩО `custom: «пішак на 1-й або 2-й горизонталі власника»` → ТО `move(pawn, +2)` — навіть якщо вже ходив; можна взяти на проході.
- КОЛИ `reach(pawn, last_rank)` → ЯКЩО `custom: «звичайним ходом пішака»` → ТО `choose(Q|R|B|N)`, `transform(piece)` — лише стандартні фігури; карта переносить пішака на останню горизонталь — перетворення лише якщо карта так каже і не на фігуру, що дає миттєвий мат; на хід суперника — одразу; одночасно в обох — першим оголошує той, хто ходить.
- КОЛИ `input(castle)` → ЯКЩО `not in_check(side)` (наприкінці ходу) → ТО `custom: «рокіровка дозволена через, із та під шах»` (3-тє видання).
- КОЛИ `repetition(position)` → ТО `draw` — повторення рахується лише за дошкою, рука не впливає.
- КОЛИ `no_moves(side)` → ЯКЩО `not in_check(side)` → ТО `choose(card | draw)` — пат за браком ходів можна (за бажанням) уникнути картою.
- КОЛИ `no_moves(side)` → ЯКЩО `in_check(side)` → ТО `custom: «мат, якщо й карта з руки не рятує на своєму ході»` (FAQ: партія не скінчена, доки матований не спробує втекти картою на своєму ході).

**Приклади карт (тексти з правил SJG)**
- Blessing (6): КОЛИ `input(play_card)` (замість ходу) → ТО `custom: «одна твоя фігура ходить на будь-яку відстань по діагоналі, як слон; бити не можна»`.
- Demotion (Вікіпедія): замість ходу → `transform(enemy_piece, pawn)` — `custom: «замінити фігуру суперника (крім K, Q) на одного з його взятих пішаків»`.
- Second Sight (4): одразу після ходу суперника → `custom: «подивитись 4 верхні карти колоди, одну взяти замість цієї, колоду перетасувати»`.
- Knightmare (10, порожня карта): одразу після ходу суперника → `custom: «його хід скасовано; він ходить інакше тією чи іншою фігурою; зіграну карту може забрати»`.
- Fireball (вступ SJG): `explode(square3x3)` — `custom: «твоя фігура вибухає і зникає разом з усіма фігурами на 8 сусідніх клітинах»`.
- Under Elf Hill (вступ SJG, errata): `custom: «король зникає з дошки на хід і повертається на будь-яку вільну крайову клітину»`; не може піти після повернення — хід = пас.

- Перемога: мат (з урахуванням карт) · «гол»-карта (King of the Mountain — король у центрі наприкінці твого третього ходу, (?)) · Нічия: пат, повторення.

## Керування і ввід
- Фізична гра: шахівниця + карти; гравець оголошує карту, кладе її у скид або праворуч від дошки й добирає; перетворену фігуру позначає монеткою чи стікером, такий самий маркер — на карті.
- Суперник може втрутитися карткою під час або одразу після твого ходу — в цифровій версії це вікно відповіді з паузою на рішення.
- Підготовка — збирання колоди за очками: вибрати карти до суми 150, унікальні не дублювати.
- Цифрової версії не знайшов (?); вікна нижче — проєкція.

## Вікна, меню, HUD
(цифрова версія)
- `match-setup`: бюджет очок для кожного (гандикап), варіант колоди (власна / спільна / зі скинутими 15–20), набори карт.
- `deck-builder`: усі карти з очками й позначкою `*`, лічильник «використано / 150», фільтр за моментом гри.
- `game-screen`: дошка, `card-hand` (5 карт, приховано від суперника), `deck-counter`, відкритий скид, `continuing-effects-row` з картами праворуч від дошки, `transform-marker` на фігурах, `legal-move-highlight` з урахуванням активних карт, `turn-indicator`, `move-list`.
- `response-prompt`: «Суперник зіграв карту / зробив хід — відповісти?» з картами, які зараз можна зіграти.
- `codex-window` — каталог карт з повним текстом і рішеннями FAQ; `help-window` — правила, Checkmate Rule, конфлікти.
- `end-screen` — мат, «гол»-карта, пат.
- Переходи: main-menu → match-setup → deck-builder → game-screen ⇄ response-prompt → end-screen.

## Фічі поза полем
- `custom-rules` — кожна карта — модуль правил; колода — набір модулів на партію.
- `difficulty-presets` через бюджет очок: «рейтинговий гравець з колодою 80–100 очок проти нерейтингового з 200».
- Варіанти правил: Extra Discards (перед поділом скинути 15–20 верхніх карт) · Common Deck (спільна колода, як у французькому оригіналі; скидати можна й на хід суперника, скид перетасовується) · Personal Sets (у кожного свій набір) · Multiple Sets (кілька копій, але `*` — одна) · порожні карти для власних правил.
- На сайті SJG — сторінки «Two-Player Variants» і «Multiplayer Knightmare Chess» (не відкривав).

## Варіації й родичі
- Видання: 1996 (80 карт) · 2-ге видання (1997: призупинення тривалих ефектів, новий розділ про пішаків, «turn» замість «move») · Knightmare Chess 2 (80 карт: 78 + 2 порожні, «goal»-карти) · 3-тє видання (2014, правила v3.0: обидва набори, 158 карт + 2 порожні; рокіровка через шах дозволена).
- Французький оригінал *Tempête sur l'échiquier* — спільна колода без збирання.
- Родичі: [onitama.md](onitama.md) (карти задають рух фігур, зіграна йде супернику) · [shotgun-king.md](shotgun-king.md) (карти-апгрейди між поверхами) · [chess-rule-twists.md](chess-rule-twists.md) і [lichess-variants.md](lichess-variants.md) (одне правило змінено на всю партію, а не картою на хід) · [really-bad-chess.md](really-bad-chess.md) (випадкові армії) · [circe-chess.md](circe-chess.md) (карта Rebirth — разове відродження на стартовій клітині) · [fairy-chess-conditions.md](fairy-chess-conditions.md).
- **Осі варіацій**:
  - **Як довго діє правило**: один хід · тривалий ефект з призупиненням · вся партія (казкові умови).
  - **Що змінює карта**: рух своєї фігури · чужі фігури (переставити, заморозити, замінити) · клітини дошки · тип фігури · ціль гри («гол»-карти) · сам хід суперника (скасування).
  - **Звідки карти**: власна колода за бюджетом · спільна колода · відкритий драфт.
  - **Коли грати**: на свій хід (до / замість / після) · на хід суперника · у відповідь на карту.

## Цікавинки для курсу
- Карта як плагін правил з точками входу «до ходу / замість / після / на хід суперника / відповідь» — 🥈 (рушій подій поверх шахового генератора ходів).
- Реєстр тривалих ефектів: умова дії, призупинення й відновлення, маркер на фігурі — 🥉.
- Розвʼязувач конфліктів: Checkmate Rule > карта > шахи; тривала > звичайна; інакше остання зіграна — 🥉.
- Перевірка Checkmate Rule: застосувати карту, перевірити мат/взяття короля за **зміненими** правилами, відкотити й анулювати карту — 🥇.
- Збирання колоди з бюджетом очок, унікальними картами й гандикапом — 📎.
- Окремі карти: Fireball (вибух 3×3) · Forbidden City (непрохідна клітина) · Seat of Power (клітина-«ферзь») — 🌱 кожна.
- Карта Knightmare: скасувати щойно зроблений хід суперника й змусити піти інакше — 🥉 (undo + заборона того самого ходу).

## Мапа на каталог
- Є: `piece-move-patterns` ↔ базовий рух, змінюваний картами · `piece-capture` · `checkmate` · `check-stalemate` ↔ пат можна оминути картою · `no-move-into-check` ↔ лише наприкінці ходу · `castling` ↔ через шах дозволена · `en-passant` ↔ після подвійного кроку з 1–2-ї горизонталі · `pawn-promotion` ↔ лише Q/R/B/N, через карту — лише якщо карта каже · `hot-seat` · `turn-enforcement` ↔ одна карта на хід · `rule-variants` ↔ варіанти колоди · `explode-area` ↔ Fireball · `impassable-cells` ↔ Forbidden City · `floor-types` ↔ Seat of Power, Man-Trap · `temporary-modes` ↔ захист фігури на хід · `respawn` ↔ повернення взятої фігури · `pocket` ↔ рука карт поза дошкою · `game-screen` · `help-window` · `codex-window` ↔ каталог карт · `match-setup` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+card-modifies-rules` «Карта змінює правило на хід або назавжди» · game-logic/constraints · 🥈 · слоти {timing: before | instead | after | opponent | response; duration: move | continuing}.
  - `+continuing-effect-card` «Тривалий ефект з призупиненням за умовою» · entities/state · 🥉.
  - `+rule-precedence` «Пріоритет правил при конфлікті» · game-logic/constraints · 🥉 · слоти {order: list}.
  - `+deck-point-budget` «Колода за бюджетом очок + унікальні карти» · interface/menus · 📎 · слоти {budget, unique_marker}.
  - `+card-hand` · `+deck-builder` — 🔥 у корпусі (Onitama, Gwent, Duelyst…).
  - `+card-timing-windows` · `+cancel-opponent-turn` · `+goal-card` — дрібні, слоти `+card-modifies-rules`.

## Пропозиції до словників
- `+trigger:card_played` — підтверджую (Onitama, Gwent…): тут на нього відповідають картою суперника.
- `+trigger:deck_empty` — підтверджую: колода вичерпана, скид не перетасовується.
- `+effect:draw_card` · `+effect:discard` — підтверджую: добір до 5 після кожної зіграної, скидання замість карти.
- `+effect:cancel_turn` — скасувати щойно зроблений хід суперника, він ходить інакше (Knightmare, Think Again!, Chaos).
- `+cond:card_window(timing)` — зараз дозволений момент гри карти (до / замість / після ходу, хід суперника, відповідь).
- `+ui:card-hand` · `+ui:deck-counter` — підтверджую.
- `+ui:continuing-effects-row` — ряд активних карт біля дошки з посиланням на фігури; `+ui:transform-marker` — маркер перетвореної фігури, парний з маркером на карті.
- `+window:deck-builder` — підтверджую; `+window:response-prompt` — вікно «відповісти картою?» на хід суперника.
- `+card:card-modifies-rules` · `+card:continuing-effect-card` · `+card:rule-precedence` — див. «Мапа на каталог».

## Джерела
- ⭐ [SJG: правила 3-го видання (PDF)](https://www.sjgames.com/knightmare/img/knightmare-chess-rules.pdf) — повні правила v3.0 (вересень 2014): колода, рука, моменти гри, скидання, тривалі ефекти, перетворені фігури, Checkmate Rule з «goal»-картами, конфлікти, пішаки, рокіровка, пат, варіанти, карта Knightmare.
- [Wikipedia: Knightmare Chess](https://en.wikipedia.org/wiki/Knightmare_Chess) — автори, переклад, SJG 1996, набори по 80 карт, очки й унікальність, Demotion, рецензії.
- [SJG: сторінка гри](https://www.sjgames.com/knightmare/) — склад 3-го видання, лінки на правила, FAQ, errata, списки карт.
- [SJG: правила 2-го видання (PDF)](https://www.sjgames.com/knightmare/kc_rules.pdf) — текст 1996–1997, карта Blessing; [правила KC2 (PDF)](https://www.sjgames.com/knightmare/kc2_rules.pdf) — Second Sight, порожні карти.
- [SJG: FAQ](https://www.sjgames.com/knightmare/kc_faq.html) — мат і втеча картою, пат, рокіровка, пішаки; [рішення по картах](https://www.sjgames.com/knightmare/cards.html) — Bog, Forbidden City, Seat of Power, Man-Trap, Fortification, Coup, Neutrality, King of the Mountain; [errata](https://www.sjgames.com/knightmare/errata.html); [зміни 2-го видання](https://www.sjgames.com/knightmare/2nded.html).
- [SJG: списки карт](https://www.sjgames.com/knightmare/list_sets.html) — лише назви; [вступ](https://www.sjgames.com/knightmare/kc_intro.html) — Fireball, Under Elf Hill, Crab, Madman.
- YouTube: пошук «Knightmare Chess gameplay».

## Непевне
- (?) Рік французької *Tempête sur l'échiquier* — не знайшов; рік KC2: у Вікіпедії лютий 1997, у правилах KC2 — копірайт 1998.
- (?) Ефекти карт Bog, Forbidden City, Seat of Power, Man-Trap, Fortification, Neutrality, Coup, Heir, King of the Mountain — відновлені з офіційних рішень по картах; повних текстів карт не бачив.
- (?) King of the Mountain: «король на центральній клітині наприкінці твого третього ходу» — з переказу рішень, точний текст не бачив.
- (?) Madman («пішак ходить як дамка в шашках») і Crab («пішак ходить вперед по діагоналі») — з переказу вступу SJG.
- (?) Діапазон очок карт 2–10 і «20–30 карт у колоді на 150 очок» — зі вступу SJG, не з правил.
- (?) Цифрових реалізацій не знайшов; вікна — проєкція.
