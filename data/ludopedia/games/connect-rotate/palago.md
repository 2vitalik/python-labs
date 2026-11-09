---
title: Palago
slug: palago
aka: [Mambo, Palagonia]
family: connect-rotate
also: [chess-abstract]
klass: cursor
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 2010
platforms: [board, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Palago", best: true, note: "48 однакових гекс-плиток, 2 плитки за хід, 3 базові правила, перемога/поразка/нічия, Mambo, Palagonia з кубиками"}
  - {kind: other, url: "https://www.boardspace.net/palago/english/Rules.htm", note: "офіційні правила: плитка = «tip + straight» обох кольорів, палаго не ділиться, дірки з однієї клітини, очі не рахуються"}
  - {kind: play, url: "https://www.boardspace.net/english/about_palago.html", note: "грати онлайн; боти Dumbot / Smartbot / Bestbot, рейтинг, архів партій"}
  - {kind: other, url: "https://calsboardgamemusings.blogspot.com/2009/12/review-palago.html", note: "рецензія: 3 різні орієнтації плитки, соло-пазли «істот», 3–5 гравців з кубиками"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Palago+game", note: "пошук; правила й партії"}
stage: v1
coverage: 70
mechanics: [tile-rotate, connectivity-check, cursor-place, hot-seat, turn-enforcement, ai-opponent, online-multiplayer, rating-system, replay, legal-move-highlight, satisfy-constraints, level-bank, game-screen, end-screen, match-setup, help-window, +edge-color-match, +two-placements-per-turn, +closed-shape-win, +double-close-loses, +single-tile-hole-rule, +identical-tiles]
proposes: ["+cond:edge_match", "+cond:enclosed", "+cond:adjacent", "+effect:roll_dice", "+card:two-placements-per-turn", "+card:closed-shape-win", "+card:double-close-loses"]
author: opus
date: 2026-11-09
---

# Palago — двоє кладуть однакові двоколірні гекс-плитки по дві за хід; хто першим замкне «істоту» свого кольору, той виграв

## Суть
У грі одна-єдина плитка: 48 однакових гексагонів, на кожному — дуга-«арка» синього й білого (жовтого) кольору (за правилами — «tip і straight обох кольорів»). Гравці по черзі кладуть **дві** плитки так, щоб усі дотичні ребра збігались кольором; кожен прагне замкнути з усіх боків (і всередині) фігуру-«істоту» свого кольору. Хто замикає обидва кольори одним ходом — програє, тож атака й захист тісно переплетені (порівнюють з го). Випадковості нема зовсім: усе різноманіття — від повороту однієї плитки.

## Поле і час
- Поле безмежне (стіл), гекс-суміжність; викладені плитки («палаго») завжди лишаються однією звʼязною групою.
- Плитка має 3 візуально різні орієнтації (кольори кутів однакові для кожного повороту на 120°).
- Покроково, двоє гравців; хід = 2 плитки, що торкаються одна одної (перемога однією плиткою — допустима).
- Повна інформація, рандому нема (жеребкування першого ходу витягом плитки — лише колір).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка | tile | 48 однакових; 2 кольори; 3 орієнтації | кладеться поруч з палаго; кольори всіх дотичних ребер збігаються |
| Область кольору | zone | синя / біла | формується дугами сусідніх плиток; закрита з усіх боків — «істота» |
| Істота | zone | колір; > 3 плиток (boardspace: петлі «розміру 3» не рахуються) | закрита ззовні й усередині — перемога власника кольору |
| Дірка | zone | порожня клітина всередині палаго | дірку з однієї клітини можна заповнити лише виграшною плиткою |
| Палаго | object | звʼязна група плиток | не може розпастися на дві групи |
| Мішок | supply | 48 плиток | плитки закінчились — нічия |
| Кубики Palagonia | object | 2 спецкубики: 2–5 + символи замість 1 і 6 | лише в режимі 3–5 гравців |

## Правила (КОЛИ → ЯКЩО → ТО)
- Старт: КОЛИ `game_start` → ТО `custom: «кожен обирає колір; хто ходить першим — витягом плитки»`; перший кладе 2 плитки в центр з однаковими кольорами на стику.
- КОЛИ `input(place, tile, cell, rot)` → ЯКЩО `turn_of(p)` and `free(cell)` and `custom: «кольори всіх дотичних ребер збігаються»` (+cond:edge_match) → ТО `place(p, tile)`; інакше `block`.
- КОЛИ `input(place, first, cell)` → ЯКЩО `custom: «клітина не торкається палаго»` → ТО `block`.
- КОЛИ `input(place, second, cell)` → ЯКЩО `custom: «не торкається першої плитки цього ходу»` (+cond:adjacent) → ТО `block`; одна з двох мусить торкатися палаго.
- КОЛИ `input(place)` → ЯКЩО `not connected(palago)` після ходу → ТО `block` — палаго не ділиться.
- КОЛИ `input(place, tile, hole)` → ЯКЩО `custom: «дірка з однієї клітини»` and `custom: «плитка не дає перемоги»` → ТО `block`.
- КОЛИ `pattern(region_closed)` кольору c → ЯКЩО `custom: «замкнена ззовні й усередині»` (+cond:enclosed) and `count(tiles_in_shape, >, 3)` → ТО `custom: «істота кольору c»`.
- КОЛИ `custom: «хід створив істоту лише свого кольору»` → ТО `win`; виграшною може бути вже перша плитка ходу — другу тоді не кладуть.
- КОЛИ `custom: «хід створив істоту лише кольору суперника»` → ТО `lose` — перемога суперника.
- КОЛИ `custom: «хід одночасно замкнув істоти обох кольорів»` → ТО `lose` для того, хто ходив.
- КОЛИ `custom: «плитки закінчились»` → ЯКЩО `custom: «ніхто не виграв»` → ТО `draw`.
- Palagonia (3–5 гравців, 1–2 кубики): КОЛИ `turn_start(p)` → ТО `custom: «кинути кубик»` (+effect:roll_dice): 2–5 → `custom: «покласти стільки плиток, усі торкаються одна одної»`; символ-1 → `custom: «зняти зовнішню плитку»`; символ-6 → `rotate(inner_tile, 120)`.
- Palagonia: КОЛИ `custom: «замкнено істоту»` → ЯКЩО `custom: «усі плитки цього ходу входять в істоту»` → ТО `score(n)` усім, хто до неї доклався; більша — дорожча; дубль на двох кубиках → `extra_move`; кінець — коли плитки скінчились.
- Перемога: перша власна замкнена істота · Поразка: замкнути чужу або обидві одразу · Нічия: скінчились плитки.

## Керування і ввід
- Настолка: взяти плитку, повернути (3 варіанти), прикласти; дві плитки за хід.
- Онлайн (boardspace.net): клік по клітині й обертання плитки (?), боти трьох рівнів, рейтинг і архів партій.

## Вікна, меню, HUD
- (цифрова версія, boardspace) `lobby-window`: суперники-люди й боти Dumbot / Smartbot / Bestbot, рейтинг.
- `match-setup`: колір, бот.
- `game-screen`: гекс-поле; `legal-move-highlight` — клітини й повороти, де збігаються ребра; лічильник плиток, що лишились (`remaining-counter`); `turn-indicator` і позначка «перша / друга плитка ходу».
- `end-screen`: переможець, підсвічена істота; зміна рейтингу.
- `replay-window`: архів партій boardspace (palago-viewer).
- `help-window`: три правила викладання й умови перемоги.

## Фічі поза полем
- `online-multiplayer` + `ai-opponent-levels` (3 боти) + рейтинг гравців + база перемог/поразок і архів партій на boardspace.net.
- Соло: `puzzle-bank` «Palagonian Puzzle Creatures» — скласти задану істоту з N плиток (буклет; візерунки на кшталт «Palaglyph»).
- Palagonia — `mode-versus` на 3–5 гравців з кубиками й очками за істоти.
- Нагорода: New Zealand «New Game of the Year» 2010.

## Варіації й родичі
- Mambo (2007, Cameron Browne) — попередник на двох: двосторонні плитки трьох кольорів (червоний, білий, синій) з розкладом serpentile 102 (одна пряма між протилежними сторонами + дві дуги між сусідніми), мета — «вбити» групи суперника замиканням чи нуль-точкою, іноді підрахунок території.
- Palagonia (2009, Browne + Mike McManaway, автор Tantrix) — багатокористувацька версія з кубиками.
- Родичі в корпусі: [tantrix](tantrix.md) (той самий тип плитки serpentile 102, ребра за кольором), [trax](trax.md) і [black-path-game](black-path-game.md) (зʼєднувальні ігри, згадані як близькі до Mambo), [entanglement](entanglement.md).
- Осі варіацій:
  - **набір плиток**: одна-єдина плитка (Palago) / 56 різних (Tantrix) / 2 типи (Trax);
  - **плиток за хід**: 1 / 2, що торкаються / за кубиком (Palagonia);
  - **мета**: замкнути свою область (Palago) / петля чи лінія свого кольору (Trax, Tantrix) / вбити групи (Mambo);
  - **самогубний хід**: замкнути обидва = поразка (Palago).

## Цікавинки для курсу
- Перевірка збігу кольорів на 6 ребрах гекса для 3 орієнтацій однієї плитки — 🌱.
- Пошук замкненої області кольору на гекс-полі: заливка з перевіркою «нема виходу на межу поля» й «закрита всередині» — 🥉.
- Хід із двох залежних розміщень + звʼязність палаго після ходу — 📎.
- Правило дірки з однієї клітини: заповнювати лише виграшно (перевірка «чи виграє плитка» до розміщення) — 📎.
- Бот: пошук виграшу за одну плитку, захист від подвійних загроз («double threat», «triple tip») — 🥇.

## Мапа на каталог
- Є: `tile-rotate` ↔ 3 орієнтації; `connectivity-check` ↔ палаго однією групою; `cursor-place` ↔ викладання; `hot-seat` + `turn-enforcement`; `ai-opponent` + `online-multiplayer` + `rating-system` + `replay` ↔ boardspace; `legal-move-highlight`; `satisfy-constraints` + `level-bank` ↔ соло-пазли істот; `game-screen` · `end-screen` · `match-setup` · `help-window`.
- **Нема** → пропозиції карток:
  - `+edge-color-match` (Tantrix) — кольори дотичних ребер збігаються.
  - `+two-placements-per-turn` «Хід = дві повʼязані дії (друга торкається першої)» · game-logic/opponent · 📎.
  - `+closed-shape-win` «Перемога — замкнена область свого кольору, більша за N» · game-logic/win · 🥉.
  - `+double-close-loses` «Хід, що дає виграш обом, — поразка того, хто ходив» · game-logic/win · 🌱.
  - `+single-tile-hole-rule` «Однокліткову дірку заповнювати лише виграшно» · entities/legality · 📎.
  - `+identical-tiles` «Усі плитки однакові, різниця лише в повороті» · entities/state · 🌱.

## Пропозиції до словників
- `+cond:edge_match` — кольори всіх дотичних ребер плитки й сусідів збігаються.
- `+cond:enclosed` — область кольору замкнена ззовні й усередині.
- `+cond:adjacent(a, b)` — дві сутності сусідять (зараз `adjacent` є лише тригером).
- `+effect:roll_dice` — Palagonia.
- `+card:two-placements-per-turn` · `+card:closed-shape-win` · `+card:double-close-loses`.

## Джерела
- ⭐ [Wikipedia: Palago](https://en.wikipedia.org/wiki/Palago) — 48 однакових плиток, перший хід, 3 правила викладання, перемога/поразка/нічия, Mambo і serpentile 102, Palagonia з кубиками й очками, нагорода 2010.
- [Boardspace: Palago Rules](https://www.boardspace.net/palago/english/Rules.htm) — офіційні правила: «tip and straight of both colours», палаго не ділиться, дірки, перемога однією плиткою, нічия.
- [Boardspace: About Palago](https://www.boardspace.net/english/about_palago.html) — онлайн-гра, боти, «петлі розміру 3 не рахуються», рейтинг і архів.
- [Cal's Board Game Musings: Review Palago](https://calsboardgamemusings.blogspot.com/2009/12/review-palago.html) — 3 орієнтації плитки, «surrounded island of their colour», соло-пазли, режим 3–5 з кубиками.

## Непевне
- (?) Точний малюнок плитки (як саме кольори лягають на кожне ребро) — у джерелах лише «арка», «tip + straight»; описано за ними.
- (?) «Очі не рахуються для замикання» (boardspace) — точний зміст «eyes» не зрозумів.
- (?) Мінімальний розмір істоти: Wikipedia — «більше трьох плиток», boardspace — «петлі розміру 3 не рахуються»; узгоджено як > 3.
- (?) Інтерфейс boardspace (як обертати плитку, чи є підсвітка легальних клітин) — не бачив.
- (?) Кількість соло-пазлів у буклеті — не бачив.
