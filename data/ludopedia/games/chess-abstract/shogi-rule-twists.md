---
title: Шогі з твістом руху — Kyoto shogi і Annan shogi (Кіото-шогі, Аннан-шогі)
slug: shogi-rule-twists
aka: [Kyoto shogi, Kyotoshogi, 京都将棋, Annan shogi, Annanshogi, 安南将棋, Korean shogi, Anhoku shogi, 安北将棋, Кіото-шогі, Аннан-шогі]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: online
  info: full
  random: none
  goal: state
year: 1926
platforms: [board, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Kyoto_shogi", best: true, note: "Kyoto: 5×5, розстановка T S K G P, пари перевертання, дроп будь-яким боком, повторення, розвʼязана як перемога першого"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Annan_shogi", note: "Annan: фігура ходить як своя, що стоїть позаду; варіант «як будь-яка, що захищає»"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/安南将棋", note: "автор Судзукі Сінтаро (~1926), новий і класичний варіант розстановки, Anhoku shogi (зворотне правило)"}
  - {kind: play, url: "https://lishogi.org/variant/kyotoshogi", note: "Lishogi: правила Kyotoshogi, онлайн-гра"}
  - {kind: play, url: "https://lishogi.org/variant/annanshogi", note: "Lishogi: правила Annanshogi — розстановка, nifu лише для дропу, мертві ряди, вихід з шаху взяттям фігури позаду"}
  - {kind: play, url: "https://www.pychess.org/variants/kyotoshogi", note: "pychess: Kyoto shogi, ходи всіх 9 типів, вибір боку при дропі"}
  - {kind: other, url: "https://ludii.games/details.php?keyword=Kyoto%20Shogi", note: "Ludii: автор, 1976, мета — мат"}
  - {kind: other, url: "https://www.pychess.org/variants/chennis", note: "Chennis (2021) — нащадок Kyoto на 7×7 з корт-обмеженнями короля"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=kyoto+shogi+annan+shogi", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [piece-move-patterns, piece-capture, piece-drop, pocket, pawn-promotion, no-move-into-check, check-stalemate, checkmate, repetition-draw, legal-move-highlight, selection-highlight, drag-drop-piece, cell-click, turn-enforcement, move-timer, ai-opponent, online-multiplayer, rating-system, move-notation, rule-variants, game-screen, end-screen, help-window, state-as-data, unit-tests, +flip-every-move, +double-sided-drop, +borrowed-movement, +dead-square-allowed, +capture-supporter-escape, +promotion-zone]
proposes: ["+cond:behind(a, kind)", "+cond:in_zone", "+effect:choose_promotion", "+ui:flip-preview", "+ui:effective-move-hint", "+ui:drop-side-picker", "+window:variant-select", "+card:flip-every-move", "+card:double-sided-drop", "+card:borrowed-movement", "+card:dead-square-allowed", "+card:capture-supporter-escape"]
author: opus
date: 2026-11-09
---

# Шогі з твістом руху — фігура міняє тип після кожного ходу (Kyoto) або ходить як та, що стоїть позаду (Annan)

## Суть
Огляд двох варіантів, що лишають ядро [shogi](shogi.md) — руку з взятими фігурами, дропи, мат королю — і ламають одне припущення: «тип фігури сталий». У **Kyoto shogi** (Тамія Кацуя, ~1976) на полі 5×5 кожна фігура, крім короля, **перевертається після кожного свого ходу** на парний тип: пішак ↔ тура, срібло ↔ слон, золото ↔ кінь, токін ↔ лансер. В **Annan shogi** (Судзукі Сінтаро, ~1926) на звичайній дошці 9×9 фігура, за якою **прямо позаду** стоїть своя, ходить не як сама, а як та, що позаду. Нижче — лише дельта до shogi.md.

## Поле і час
- **Kyoto**: 5×5 без кольору; у кожного 5 фігур на першому ряду, зліва направо від себе: токін, срібло, король, золото, пішак. Зони перетворення нема — перевертання замість неї.
- **Annan**: 9×9, набір і розстановка шогі, але пішаки перед турою й слоном стоять на крок ближче до центру («новий тип»); «класичний» Annan — зі звичайною розстановкою. Зона перетворення — як у шогі (?).
- В обох — комадай (рука) поза дошкою; хід = рух або дроп; черга, годинник — як у шогі.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Король (Kyoto) | piece | royal; не перевертається | 1 клітина в 8 напрямках |
| Пішак ↔ Тура (Kyoto) | piece | пара; старт — пішак | пішак: 1 уперед; тура: будь-яка відстань ортогонально; після ходу — інший бік |
| Срібло ↔ Слон (Kyoto) | piece | пара | срібло: 1 по діагоналі або 1 уперед; слон: будь-яка відстань по діагоналі |
| Золото ↔ Кінь (Kyoto) | piece | пара | золото: 1 ортогонально або 1 по діагоналі вперед; кінь: стрибок 2 уперед + 1 убік |
| Токін ↔ Лансер (Kyoto) | piece | пара; старт — токін | токін: як золото; лансер: будь-яка відстань прямо вперед |
| Фігури шогі (Annan) | piece | 8 типів + перетворені | власний патерн — лише коли позаду нема своєї фігури |
| «Опора» позаду (Annan) | piece | своя фігура на клітині прямо позаду | віддає свій патерн ходу передній; сама ходить за своїм (або за своєю опорою) |
| Рука / комадай | zone | взяті фігури | Kyoto: пара, дроп будь-яким боком; Annan: як у шогі |

## Правила (КОЛИ → ЯКЩО → ТО)
**Kyoto shogi**
- КОЛИ `input(move(piece, to))` → ЯКЩО `turn_of(side)` and `legal(move)` → ТО `move`, `transform(piece, paired_type)` — крім короля, після **кожного** ходу, зокрема зі взяттям.
- КОЛИ `contact(piece, enemy)` → ТО `disappear(b)`, `give(capturer, b_pair)` — у руку йде пара, без «боку».
- КОЛИ `input(drop(pair, cell))` → ЯКЩО `has(side, pair)` and `free(cell)` → ТО `choose(side_up)`, `place(piece, cell)`, `take(side, pair)`; обмежень на клітину нема: два пішаки в одній вертикалі й мат дропом пішака дозволені.
- КОЛИ `input(move|drop)` → ЯКЩО `custom: «фігура опиниться там, звідки не зможе походити»` → ТО дозволено (у шогі — `block`): напр. тура, що дійшла до останнього ряду, стає пішаком без ходу, доки її не візьмуть.
- КОЛИ `no_moves(side)` → ЯКЩО `in_check(side)` → ТО `lose(side)` (мат).
- КОЛИ `repetition(position, 3)` → ТО `draw` (оригінал і Lishogi); альтернатива автора — поразка того, хто повторює, а при вічному шаху — того, хто шахує.

**Annan shogi**
- КОЛИ `input(move(piece, to))` → ЯКЩО `custom: «на клітині прямо позаду (з боку власника) стоїть своя фігура R»` → ТО `custom: «piece ходить патерном R замість власного»`; інакше — власний патерн.
- На старті тура й слон ходять як коні (позаду них — кінь), а пішак, що стояв би впритул перед турою, ходив би як тура й перетворився б першим ходом (2c) — тому «новий тип» розстановки відсуває ці пішаки.
- КОЛИ `input(move)` → ЯКЩО `custom: «хід створює два своїх пішаки в одній вертикалі»` → ТО дозволено.
- КОЛИ `input(drop(pawn, file))` → ЯКЩО `occupied(file, own_pawn)` → ТО `block` (nifu лише для дропу).
- КОЛИ `input(move(piece, last_ranks))` або `input(drop(piece, last_ranks))` → ЯКЩО `custom: «piece — пішак / лансер / кінь»` → ТО `custom: «дозволено без перетворення — опора позаду може дати фігурі хід»`.
- Вихід з шаху: КОЛИ `check` → ТО легальні звичайні відповіді **і** `custom: «взяти фігуру, що стоїть позаду шахуючої, якщо після цього шаху нема»` (шахуюча втрачає позичений патерн).
- КОЛИ `no_moves(side)` → ЯКЩО `in_check(side)` → ТО `lose(side)`.
- Варіант: фігура ходить як **будь-яка** своя фігура, що її захищає.
- Перемога: мат (обидва). · Нічия: Kyoto — триразове повторення; Annan — як у шогі (?). · Рахунку нема.

## Керування і ввід
- Як у Lishogi-шогі: клік/drag фігури → `legal-move-highlight` → клік цілі; дроп — з комадаю.
- **Kyoto**: при дропі — вибір боку пари (дві фішки над клітиною); у підсвітці ходу корисно показувати, **якою** стане фігура після ходу (`flip-preview`).
- **Annan**: підсвітка легальних ходів рахує позичений патерн; підказка «ходить як X» (`effective-move-hint`) — інакше хід виглядає нелегальним.
- Діалогу перетворення в Kyoto нема (переворот обовʼязковий і автоматичний).

## Вікна, меню, HUD
- (цифрова версія — Lishogi / pychess)
- `variant-select` у «Create a game»: Standard / Minishogi / Chushogi / Annanshogi / Kyotoshogi / Checkshogi / Dobutsu (див. shogi.md).
- `game-screen`: дошка 5×5 або 9×9, два `pocket`, два `player-clock`, `move-list`, `last-move-highlight`; Kyoto — фішки з обома назвами пари, рука показує пару без боку.
- `drop-side-picker` (Kyoto) — модальний вибір боку пари при дропі.
- `help-window`: сторінка `/variant/<назва>` з правилами й діаграмами.
- `end-screen`: мат / повторення; рейтинг варіанта окремо.

## Фічі поза полем
- `online-multiplayer`, рейтинг за варіантом (`rating-system`), `ai-opponent-levels` (Lishogi/pychess — Fairy-Stockfish (?)), `replay`, `custom-rules` (Annan — класична / нова розстановка).
- Kyoto **слабко розвʼязана** як перемога першого гравця — цікаво для курсу як ціль для solver.

## Варіації й родичі
- **Anhoku shogi** (安北将棋) — зворотне Annan: **задня** фігура ходить як передня; звичайна розстановка (тура й слон на старті без ходу); неперевірені правила — без nifu, дропи на мертві ряди (JA-вікі, «потрібні джерела»).
- JA-вікі згадує ще варіант, де передня фігура **зберігає** власний хід і **додає** позичений (?).
- **Chennis** (Couch Tomato, 2021) — нащадок Kyoto на 7×7 «тенісному корті»: пари тура-пішак, слон-солдат, кінь-мер, гармата-ферзь, корти для королів, пат = поразка.
- Сусіди: [shogi.md](shogi.md) (база), [large-shogi-variants.md](large-shogi-variants.md), [lichess-variants.md](lichess-variants.md) (Crazyhouse — дропи в шахах), The Duke (плитка перевертається після ходу — у черзі); Minishogi 5×5 — того ж розміру, що Kyoto, але з класичним перетворенням.
- **Осі варіацій**:
  - коли міняється тип фігури: у зоні (шогі) / після кожного ходу (Kyoto) / залежно від сусіда (Annan);
  - звідки патерн ходу: власний / від фігури позаду (Annan) / від фігури попереду (Anhoku) / від будь-якого захисника (варіант Annan);
  - обмеження дропу: мертві ряди + nifu + uchifuzume (шогі) / лише nifu (Annan) / жодних (Kyoto);
  - бік фігури при дропі: завжди неперетворена (шогі) / на вибір (Kyoto).

## Цікавинки для курсу
- Перевертання після кожного ходу: генератор ходів бере патерн поточного боку, після ходу — `transform` у пару — 🌱 (поверх шогі).
- Дроп з вибором боку + підсвітка обох наборів легальних клітин — 📎.
- Позичений патерн (Annan): патерн фігури = функція від клітини позаду; атаки й шах рахуються так само — 🥈 (легальність залежить від сусідів і змінюється від чужих ходів).
- Вихід з шаху взяттям «опори» шахуючої фігури — 🥉 (перевірка шаху після кожного кандидата).
- Розвʼязувач Kyoto 5×5 (retrograde / proof-number search) — 👑.
- `flip-preview` / `effective-move-hint` — UI, без якого правила не видно — 📎.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ 9 типів Kyoto / 14 Annan · `piece-capture` · `piece-drop` + `pocket` ↔ рука · `pawn-promotion` ↔ зона Annan (у Kyoto — замінено) · `no-move-into-check` + `check-stalemate` + `checkmate` · `repetition-draw` ↔ 3 повторення · `legal-move-highlight` + `selection-highlight` + `drag-drop-piece` + `cell-click` · `move-timer` · `ai-opponent` + `online-multiplayer` + `rating-system` · `move-notation` · `rule-variants` ↔ вибір варіанта / розстановки · `game-screen` / `end-screen` / `help-window` · `state-as-data` + `unit-tests`.
- **Нема** → пропозиції карток:
  - `+flip-every-move` «Фігура перевертається на парний тип після кожного ходу» · entities/state · 📎 · слоти {pairs, except: king} (родич: The Duke).
  - `+double-sided-drop` «Дроп з вибором боку» · entities/legality · 📎.
  - `+borrowed-movement` «Фігура ходить патерном сусіда позаду» · entities/legality · 🥈 · слоти {source: behind|front|any_defender}.
  - `+dead-square-allowed` «Можна стати туди, звідки нема ходу» · entities/legality · 🌱 — перемикач до правила шогі.
  - `+capture-supporter-escape` «Зняти шах, узявши опору шахуючої» · game-logic/constraints · 🥉.
  - `+promotion-zone` (див. shogi) — у Annan без змін.

## Пропозиції до словників
- `+cond:behind(a, kind)` — на клітині прямо позаду A (з боку власника) стоїть сутність виду (Annan; Anhoku — дзеркально `front`).
- `+cond:in_zone` (див. shogi) — Annan: перетворення в зоні; `+effect:choose_promotion` (див. shogi, checkers).
- `+ui:flip-preview` — показ, на що перевернеться фігура після ходу; `+ui:effective-move-hint` — «зараз ходить як X»; `+ui:drop-side-picker` — вибір боку при дропі.
- `+window:variant-select` — вибір варіанта перед партією (див. chess-rule-twists, checkers).
- `+card:flip-every-move`, `+card:double-sided-drop`, `+card:borrowed-movement`, `+card:dead-square-allowed`, `+card:capture-supporter-escape`.

## Джерела
- ⭐ [Wikipedia: Kyoto shogi](https://en.wikipedia.org/wiki/Kyoto_shogi) — автор і рік, 5×5, розстановка T S K G P, пари, переворот після кожного ходу, дроп будь-яким боком без обмежень, мертві фігури легальні, повторення (оригінал і альтернатива), назва-каламбур 香+と = 京都, слабко розвʼязана.
- [Lishogi: Kyotoshogi](https://lishogi.org/variant/kyotoshogi) — ті самі правила, триразове повторення = нічия, «правила для вічного шаху нема».
- [pychess: Kyoto shogi](https://www.pychess.org/variants/kyotoshogi) — ходи всіх девʼяти типів, вибір боку при дропі.
- [Ludii: Kyoto Shogi](https://ludii.games/details.php?keyword=Kyoto%20Shogi) — автор, 1976, мета — мат.
- [Wikipedia: Annan shogi](https://en.wikipedia.org/wiki/Annan_shogi) — основне правило й варіант «як захисник»; «also called Korean shogi».
- [JA-Wikipedia: 安南将棋](https://ja.wikipedia.org/wiki/安南将棋) — Судзукі Сінтаро, ~1926 (стаття в Асахі 1930), нова/класична розстановка, приклад «тура й слон ходять як коні», Anhoku shogi.
- [Lishogi: Annanshogi](https://lishogi.org/variant/annanshogi) — пішаки ближче до центру, nifu лише для дропу, мертві ряди легальні, взяття опори як відповідь на шах.
- [pychess: Chennis](https://www.pychess.org/variants/chennis) — нащадок Kyoto (2021).
- YouTube: [пошук «kyoto shogi annan shogi»](https://www.youtube.com/results?search_query=kyoto+shogi+annan+shogi).

## Непевне
- (?) Annan: як працює правило з королем (фігура перед королем ходить як король; король з опорою позаду ходить як вона?) — у відкритих джерелах не описано.
- (?) Annan: перетворення — за власним типом фігури чи з урахуванням позиченого ходу, і чи діють uchifuzume та джішогі — не описано.
- (?) Kyoto: чи перевертається фігура при самому дропі — джерела кажуть «після ходу» й «обираєш бік при дропі», тобто ні.
- (?) Назва «Korean shogi» для Annan (EN-вікі) дивна: 安南 = Аннам (вʼєтнамська назва); не перевіряв походження.
- (?) Рушій AI на Lishogi/pychess для цих варіантів — з памʼяті.
- (?) Варіант JA-вікі «передня фігура зберігає свій хід + позичає задній» — у статті названо так само, як Tenjiku shogi; не плутати з 16×16 (див. large-shogi-variants).
