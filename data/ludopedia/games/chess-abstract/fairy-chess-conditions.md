---
title: Казкові умови шахів — Andernach, Madrasi, Grid
slug: fairy-chess-conditions
aka: [Fairy chess conditions, Казкові умови, Andernach chess, Андернахські шахи, Anti-Andernach, Super-Andernach, Madrasi chess, Шахи Мадрасі, Madrasi RI, Madrasi rex inclusive, Isardam, Grid chess, Ґраткові шахи]
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
year: 1953
platforms: [board, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Madrasi_chess", best: true, note: "Madrasi: паралізація однойменних (не ходить, не бʼє, не шахує), зняття взяттям і перекриттям, en passant, Madrasi RI, приклад з матом"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Andernach_chess", note: "Andernach: фігура, що взяла, міняє колір (крім короля); пішак — спершу перетворення; Anti- і Super-Andernach, тибетські шахи; доказова партія Caillaud 1993"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Grid_chess", note: "Grid: 16 областей 2×2, хід мусить перетнути лінію; шах і королі поруч; Stead 1953, допоміжний мат Ternblad 1954"}
  - {kind: wiki, url: "https://fr.wikipedia.org/wiki/Échecs_d'Andernach", note: "перефарбована фігура — «нова, що не ходила» (рокіровка можлива); ~2000 задач; Andernach — конгрес задачистів"}
  - {kind: wiki, url: "https://uk.wikipedia.org/wiki/Ґраткові_шахи", note: "UA-назва; слон і кінь у прикладі, маршрут короля в допоміжному маті"}
  - {kind: other, url: "https://www.janko.at/Retros/Glossary/Andernach.htm", note: "глосарій Janko: Andernach і Anti-Andernach, ретро-задачі 1993–1996"}
  - {kind: other, url: "https://www.janko.at/Retros/Glossary/Madrasi.htm", note: "глосарій Janko: паралізована фігура паралізує, en passant і пів-ходу паралізації, Isardam"}
  - {kind: other, url: "https://www.janko.at/Retros/Glossary/Grid.htm", note: "глосарій Janko: казковий шах, королі поруч в одній області, король і пішак не досягають кута"}
  - {kind: other, url: "https://raw.githubusercontent.com/thomas-maeder/popeye/develop/py-engl.txt", note: "мануал розвʼязувача Popeye: умови Andernach, AntiAndernach, Madrasi (+RexInclusive), Isardam (+TypeB), GridChess і варіанти сітки"}
  - {kind: other, url: "http://www.jurajlorinc.com/chess/fi_m.htm", note: "Chess Composition Microweb: задачі з Madrasi і Madrasi RI"}
  - {kind: other, url: "http://www.jurajlorinc.com/chess/fi_g.htm", note: "Chess Composition Microweb: задачі Grid chess"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=madrasi+chess+fairy+problem", note: "пошук; розбори казкових задач"}
stage: v1
coverage: 55
mechanics: [piece-move-patterns, piece-capture, legal-move-highlight, no-move-into-check, check-stalemate, checkmate, pawn-promotion, castling, en-passant, hot-seat, rule-variants, move-notation, game-screen, editor-window, help-window, +capturer-switches-side, +mutual-paralysis, +region-cross-move, +stipulation-solver, +proof-game]
proposes: ["+cond:attacked", "+cond:crosses_border", "+cond:moved", "+ui:paralysis-marker", "+ui:region-grid-overlay", "+feature:condition-stack", "+card:capturer-switches-side", "+card:mutual-paralysis", "+card:region-cross-move", "+card:stipulation-solver", "+card:proof-game"]
author: opus
date: 2026-11-09
---

# Казкові умови шахів — одне нове правило поверх звичайних шахів: перефарбування, паралізація, сітка

## Суть
Казкова умова (fairy condition) — додаткове правило, яке задачист накладає на звичайні шахи; фігури, дошка й мета лишаються. Три умови: **Andernach** (1993) — фігура, що взяла, переходить до суперника; **Madrasi** (1979) — фігура, атакована однойменною ворожою, паралізована; **Grid** (1953) — дошку поділено на 16 областей 2×2, і хід легальний, лише якщо перетинає лінію сітки. Живуть переважно в шаховій композиції (мат за N, допоміжний мат, доказові партії), хоча цілі партії грати можна. Для курсу — найкоротший шлях до «шахового рушія з плагіном правил»: кожна умова — один ефект або один фільтр поверх генератора ходів [chess.md](chess.md).

## Поле і час
- Дошка 8×8, стандартна розстановка (у задачах — довільна позиція з діаграми); хід = півхід, як у шахах.
- **Grid**: поверх дошки — лінії між вертикалями b|c, d|e, f|g і горизонталями 2|3, 4|5, 6|7, тобто 16 областей 2×2; на діаграмі сітку завжди малюють. Інші розбиття — у «Варіаціях».
- **Madrasi**: стан «паралізована» перераховується після кожного півходу з карти атак.
- **Andernach**: сторона фігури — змінне поле; склад армій міняється з кожним взяттям, тож «інвентар» матеріалу рахувати складно (Janko).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фігури K Q R B N P | piece | сторона, тип | ортодоксальні патерни ходу й взяття |
| Фігура, що взяла (Andernach) | piece | сторона змінна | після взяття стоїть на клітині взятої і належить стороні взятої |
| Король (Andernach) | piece | — | не міняє кольору ніколи |
| Пішак, що взяв на останній горизонталі (Andernach) | piece | — | спершу перетворюється, потім міняє колір |
| Паралізована фігура (Madrasi) | piece | стан `paralysed` | не ходить, не бʼє, не шахує; сама далі паралізує |
| Король (Madrasi) | piece | — | не паралізується; у Madrasi RI — паралізується теж |
| Пішак після подвійного кроку (Madrasi) | piece | паралізований на пів-ходу | не паралізує сусіднього ворожого пішака — тому en passant можливе |
| Область сітки 2×2 (Grid) | zone | 16 шт. | хід усередині однієї області заборонено; нападник в одній області з королем не шахує |
| Лінія сітки (Grid) | static | 3 вертикальні + 3 горизонтальні | хід має перетнути хоча б одну |

## Правила (КОЛИ → ЯКЩО → ТО)
Дельта до [chess.md](chess.md):

| Умова | Рік, автор | Що змінено | Слово граматики |
|---|---|---|---|
| Andernach | 1993, конгрес задачистів в Андернаху (автора не названо) | фігура, що взяла (крім короля), переходить до суперника | `set_side` |
| Anti-Andernach | — | колір міняє хід **без** взяття; взяття — звичайне | `set_side` |
| Super-Andernach | 2006, John Rice | колір міняє будь-який хід (крім короля) | `set_side` |
| Madrasi | 1979, Abdul Jabbar Karwatkar (Мадрас) | атакована однойменною ворожою — паралізована | `set_state`, +cond:attacked |
| Madrasi RI | — | паралізуються й королі | `set_state` |
| Isardam | — | заборонено ходи, що створюють паралізацію | `block` |
| Grid | 1953, Walter Stead | хід мусить перетнути лінію сітки 2×2; шах — лише якщо нападник міг би взяти | +cond:crosses_border |

**Andernach**
- КОЛИ `contact(p, enemy)` (хід зі взяттям) → ЯКЩО `custom: «p — не король»` → ТО `disappear_b`, `set_side(p, enemy_side)` — фігура лишається на клітині взяття, але вже чужа.
- КОЛИ `reach(pawn, last_rank)` → ЯКЩО `custom: «пішак прийшов взяттям»` → ТО `choose(Q|R|B|N)`, `transform(piece)`, `set_side(piece, enemy_side)` — спершу перетворення, потім зміна кольору.
- КОЛИ `after(set_side)` → ТО `set_state(p, never_moved)` — перефарбована фігура вважається новою, що не ходила (FR-вікі: рокіровка з нею можлива).
- КОЛИ `input(move(p, to))` → ЯКЩО `custom: «після взяття й перефарбування p атакує свого колишнього короля»` → ТО `block` — це хід під власний шах (наслідок правила, (?)).
- Приклад (Caillaud 1993, доказова партія 3.0): 1.Nf3 Nc6 2.Ne5 Nxe5 (чорний кінь став білим) 3.Nxd7 (білий кінь став чорним) Nb8.
- Anti-Andernach: КОЛИ `input(move(p, to))` → ЯКЩО `free(to)` and `custom: «p — не король»` → ТО `move(p, to)`, `set_side(p, enemy_side)`; взяття — як у шахах.
- Super-Andernach: КОЛИ `input(move(p, to))` → ЯКЩО `custom: «p — не король»` → ТО `move(p, to)`, `set_side(p, enemy_side)` — після будь-якого ходу.

**Madrasi**
- КОЛИ `after(move)` → ЯКЩО `custom: «ворожа q атакує p за своїм патерном»` and `same(p, q, type)` and `custom: «p — не король»` → ТО `set_state(p, paralysed)`; інакше `clear_state(p, paralysed)`.
- КОЛИ `input(move(p, to))` → ЯКЩО `state(p, paralysed)` → ТО `block` — паралізована не ходить і не бʼє.
- КОЛИ `check(side)` → ЯКЩО `custom: «кожна фігура, що атакує короля, паралізована»` → ТО `custom: «шаху нема — король може стояти під такою атакою»`.
- Паралізована фігура паралізує далі, навіть того, хто паралізував її (взаємна паралізація однойменних — звичайний випадок); у карту паралізації вона входить, у генератор ходів і перевірку шаху — ні.
- Різні типи не паралізують: кінь, що атакує слона, нічого не робить; слони різнопольні ніколи не паралізують один одного.
- КОЛИ `contact(free_piece, paralyser)` → ТО `disappear_b`, `clear_state(p, paralysed)` — взяття паралізатора вільною фігурою знімає паралізацію.
- КОЛИ `custom: «третя фігура перекрила лінію атаки»` → ТО `clear_state(p, paralysed)` — приклад Вікіпедії: 1.Be5 перекриває лінію g5–c5, тура c5 оживає й шахує; 1…Rc4 паралізує її знову; 2.bxc4#.
- КОЛИ `input(move(pawn, +2))` → ЯКЩО `custom: «поруч на тій самій горизонталі ворожий пішак, що може взяти на проході»` → ТО `set_state(pawn, paralysed, 1)` — пішак, що пройшов двома, паралізований на пів-ходу (не шахує), а сам ворожого пішака на 5-й горизонталі не атакує, тож en passant можливе.
- Madrasi RI: перше правило без умови «не король» — паралізуються й королі.
- Isardam: КОЛИ `input(move(p, to))` → ЯКЩО `custom: «після ходу виникла б хоч одна Madrasi-паралізація»` → ТО `block`; те саме обмеження діє на «взяття короля» при перевірці шаху (Janko).

**Grid**
- КОЛИ `input(move(p, to))` → ЯКЩО `custom: «from і to лежать в одній області 2×2»` (кандидат +cond:crosses_border) → ТО `block`.
- КОЛИ `check(side)` → ЯКЩО `custom: «нападник і король в одній області»` → ТО `custom: «шаху нема»` — шах казковий: атакує лише той, хто міг би взяти за правилом сітки.
- Королі можуть стояти поруч, якщо вони в одній області. Від шаху тури з c8 король тікає на d7/d8 (у її ж область), але не на e7/f7 (хід без перетину лінії).
- Рокіровка — за звичними умовами, з казковим шахом (у прикладі Janko O-O-O нелегальна через поле під шахом, O-O — легальна).
- Наслідки самого правила: хід коня завжди виходить за межі 2×2, тож кінь не обмежений; заборонено лише короткі ходи всередині області (король, пішак, хід лінійної фігури на 1); король і пішак ніколи не досягають кута (Janko).
- Допоміжний мат Ternblad (Fairy Chess Review 1954): 1.Ke2 Bc4+ 2.Kd3 Bxb5+ 3.Ke4 Bc6+ 4.Kd5 Bxb7# — слон шахує, відступаючи через лінію; король ховається в області слона.

- Перемога: мат з урахуванням умови (у задачах — виконати завдання: #n, h#n, доказова партія, «чи можлива позиція?») · Нічия: пат, повторення — як у шахах.

## Керування і ввід
- Фізична дошка — як шахи; для Grid сітку малюють на дошці.
- Цифрова версія: клік/drag фігури; підсвітка легальних ходів практично обовʼязкова (умови неінтуїтивні); перед партією — вибір умови.
- Розвʼязувач Popeye: задача — текстовий блок `BeginProblem … EndProblem`, ключове слово `condition` і список умов з опціями (`condition grid orthogonal bdf246`); регістр не важливий, слова можна скорочувати, поки скорочення однозначне; вивід — текст або LaTeX (`WriteGrid` друкує розбиття на області, `SuppressGrid` ховає лінії).

## Вікна, меню, HUD
(цифрова версія; оригінал — діаграма в журналі й консольний розвʼязувач)
- `match-setup`: умова або кілька умов, Madrasi RI вкл/вимк, тип сітки.
- `game-screen`: дошка + `region-grid-overlay` (Grid) + `paralysis-marker` на паралізованих (Madrasi) + перефарбування фігури на очах (Andernach, `toast` «тура b5 стала чорною»); `legal-move-highlight`, `move-list`.
- `editor-window` — розстановка позиції задачі й вибір завдання; `solutions-window` — знайдені розвʼязки.
- `help-window` — визначення умови з прикладом; `end-screen` — мат, пат.
- Переходи: main-menu → match-setup → game-screen → end-screen; main-menu → editor-window → solutions-window.

## Фічі поза полем
- `custom-rules` — умова як параметр партії; кілька умов одночасно (Popeye приймає список) — кандидат `+feature:condition-stack`.
- `mode-puzzle` — шахова композиція: задачі з умовою на мат, допоміжний мат, доказові партії, ретро «чи можлива позиція?»; тематичні турніри (Andernach — з 1993; перший турнір Grid-задач — 1954).
- `hotseat` — цілі партії можливі (Вікіпедія про Grid і Madrasi), але онлайн-платформ не знайшов (?).
- Задачі зберігають у нотації з умовою в заголовку; розвʼязувач — окрема програма.

## Варіації й родичі
- [chess-rule-twists.md](chess-rule-twists.md) (Duck, Alice, Hostage, Avalanche) і [lichess-variants.md](lichess-variants.md) (Atomic, Antichess, Crazyhouse) — варіанти для гри, тут — умови для композиції. [wraparound-chess.md](wraparound-chess.md) — інша геометрія дошки замість сітки-фільтра.
- **Andernach-сімʼя**: тибетські шахи (Pritchard: чорні «лами» при взятті іншого типу міняють колір і тип) — попередник; Anti-Andernach; Super-Andernach (The Problemist, 2006).
- **Madrasi-сімʼя**: Madrasi RI; Isardam («Madrasi навпаки», у Popeye ще `TypeB`).
- **Grid-сімʼя** (опції Popeye): `VerticalShift` / `HorizontalShift` / `DiagonalShift` — сітка, зсунута на одну вертикаль/горизонталь; `orthogonal` — довільний набір ліній (`bdf246`); `irregular` — області як довільні групи клітин; `GridLine` — окремі відрізки ліній.
- Інші умови зі статті Fairy chess: Circe, patrol, monochromatic, Einstein, Descartes (лише назви).
- **Осі варіацій**:
  - **Доля фігури при взятті**: взята зникає · та, що взяла, міняє сторону (Andernach) · колір міняє тихий хід (Anti-) · будь-який хід (Super-) · взята відроджується на старті (Circe) · у руку суперника (Crazyhouse).
  - **Що обмежує фігуру**: нічого · атака однойменної паралізує (Madrasi) · + королів (RI) · заборона створювати паралізацію (Isardam).
  - **Геометрія легальності**: будь-яка клітина за патерном · хід мусить перетнути межу області (Grid; 2×2, зсунута, довільна).

## Цікавинки для курсу
- Andernach: `set_side` після взяття + перевірка «чи не атакує тепер перефарбована фігура свого колишнього короля» — 📎 поверх готового рушія.
- Madrasi: стан `paralysed` з карт атак «того ж типу», з винятками (король, en passant), окремо для паралізації, ходів і шаху — 🥉.
- Isardam поверх Madrasi: фільтр ходів, що створюють паралізацію — 📎.
- Grid: фільтр `region(from) ≠ region(to)` і казковий шах — 🌱; довільні області (мапа клітина → id області) і зсунуті сітки — 📎.
- Казкова умова як плагін: інтерфейс «фільтр ходу / ефект після ходу / перевірка шаху» й комбінування кількох умов — 🥈.
- Розвʼязувач «мат за N / допоміжний мат» з умовою (перебір з відсіканням, як Popeye) — 🥇.
- Доказова партія: знайти найкоротшу гру, що веде до діаграми (Caillaud 3.0) — 👑.

## Мапа на каталог
- Є: `piece-move-patterns` · `piece-capture` · `legal-move-highlight` ↔ обовʼязкова для неочевидних заборон · `no-move-into-check` ↔ з казковим шахом · `check-stalemate` · `checkmate` · `pawn-promotion` ↔ Andernach: спершу перетворення · `castling` ↔ перефарбована тура «не ходила» · `en-passant` ↔ виняток Madrasi · `hot-seat` · `rule-variants` ↔ умова як перемикач · `move-notation` · `game-screen` · `editor-window` ↔ позиція задачі · `help-window`.
- **Нема** → пропозиції карток:
  - `+capturer-switches-side` «Фігура, що взяла, переходить до суперника» · entities/combat · 📎 · слоти {when: capture | non-capture | any; kings: false}.
  - `+mutual-paralysis` «Атакована однойменною ворожою — паралізована» · entities/legality · 🥉 · слоти {kings: bool, mode: paralyse | forbid (Isardam)}.
  - `+region-cross-move` «Хід легальний, лише якщо перетинає межу області» · entities/legality · 🌱 · слоти {grid: 2×2 | shifted | lines | irregular}.
  - `+stipulation-solver` «Розвʼязувач задач: мат за N, допоміжний, самомат» · game-logic/opponent · 🥇.
  - `+proof-game` «Доказова партія: найкоротша гра до заданої позиції» · levels/solvability · 👑.

## Пропозиції до словників
- `+cond:attacked(cell|p, by)` — підтверджую (chess.md): тут «атакована фігурою того ж типу» в парі з `same(p, q, type)`.
- `+cond:crosses_border(move)` — підтверджую (puzz.link: лінія через жирну межу); тут хід перетинає межу області сітки.
- `+cond:moved(p)` — підтверджую (chess.md): перефарбована фігура Andernach вважається такою, що не ходила.
- `+ui:paralysis-marker` — позначка на паралізованій фігурі (Madrasi); родич `+ui:cooldown-ring`.
- `+ui:region-grid-overlay` — товсті лінії областей поверх клітинної дошки (Grid; також регіони судоку).
- `+feature:condition-stack` — кілька правил-умов одночасно, порядок застосування (Popeye: список після `condition`).
- `+card:capturer-switches-side` · `+card:mutual-paralysis` · `+card:region-cross-move` · `+card:stipulation-solver` · `+card:proof-game` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Madrasi chess](https://en.wikipedia.org/wiki/Madrasi_chess) — визначення, приклад з діаграмою (тури c5/g5, коні d8/f7, пішаки c2/d3), зняття паралізації, en passant, Madrasi RI, Karwatkar 1979.
- [Wikipedia: Andernach chess](https://en.wikipedia.org/wiki/Andernach_chess) — правило, винятки (король, перетворення), Caillaud 1993, Anti-/Super-Andernach, тибетські шахи.
- [Wikipedia: Grid chess](https://en.wikipedia.org/wiki/Grid_chess) — сітка 2×2, шах, сусідні королі, Stead 1953, допоміжний мат Ternblad.
- [Wikipedia FR: Échecs d'Andernach](https://fr.wikipedia.org/wiki/Échecs_d'Andernach) — «нова фігура, що не ходила», ~2000 задач, історія конгресу.
- [Wikipedia UK: Ґраткові шахи](https://uk.wikipedia.org/wiki/Ґраткові_шахи) — UA-назва, розбір маршруту короля.
- [Janko: Andernach](https://www.janko.at/Retros/Glossary/Andernach.htm) · [Madrasi](https://www.janko.at/Retros/Glossary/Madrasi.htm) · [Grid](https://www.janko.at/Retros/Glossary/Grid.htm) — глосарій ретро-задач: точні визначення, en passant у Madrasi, Isardam, король і пішак не досягають кута в Grid.
- [Popeye: py-engl.txt](https://raw.githubusercontent.com/thomas-maeder/popeye/develop/py-engl.txt) — назви умов і опції (RexInclusive, TypeB, варіанти сітки), синтаксис вводу; визначень правил там нема.
- [Wikipedia: Fairy chess](https://en.wikipedia.org/wiki/Fairy_chess) — перелік «нових умов» (Circe, Madrasi, Andernach, monochromatic, patrol, Einstein, Descartes), визначень нема.
- [Chess Composition Microweb: M](http://www.jurajlorinc.com/chess/fi_m.htm) · [G](http://www.jurajlorinc.com/chess/fi_g.htm) — індекси задач, без визначень.
- YouTube: пошук «madrasi chess fairy problem».

## Непевне
- (?) Andernach: en passant, рокіровка правом «нової» фігури (є лише у FR-вікі), подвійний крок пішака, що став чужим на своїй 2-й горизонталі, — EN-вікі й Janko мовчать.
- (?) «Хід під власний шах після перефарбування» — виведено з правил шахів, прямо в джерелах не сказано.
- (?) Andernach: автора не названо, рік 1993 у EN-вікі з позначкою «citation needed».
- (?) Madrasi: рокіровка, а також чи можуть королі в Madrasi RI стояти поруч (Вікіпедія лише каже, що без RI — не можуть, як у шахах).
- (?) Madrasi: EN-вікі називає статус en passant «відкритим питанням»; Janko дає чітке правило — узято Janko.
- (?) Grid: en passant і перетворення джерела не описують; з правила випливає, що пішак не ступає з 7-ї на 8-му прямо (обидві в одній області) і перетворюється лише взяттям через вертикальну лінію — перевірити на задачах.
- (?) Цифрових реалізацій для гри (не розвʼязувачів) не знайшов; вікна вище — проєкція.
