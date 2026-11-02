---
title: Шахи з твістом правил (Duck, Kung-Fu, Quantum, Kriegspiel/Dark, Alice, Avalanche, Hostage)
slug: chess-rule-twists
family: chess-abstract
also: [hidden-deduction]
klass: figure
axes:
  field: square
  time: turn
  opponent: online
  info: hidden
  random: runtime
  goal: state
year: 1899
platforms: [board, web, PC]
links:
  - {kind: other, url: "https://www.chess.com/terms/duck-chess", best: true, note: "Duck Chess: правила одним екраном (качка, взяття короля, пат = перемога)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Kung-fu_chess", note: "Kung-Fu Chess: без черги, кулдаун фігури, IGF 2002"}
  - {kind: other, url: "https://arxiv.org/abs/1906.05836", note: "Cantwell: Quantum Chess — математична рамка й правила (split/merge/measure)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Kriegspiel_(chess)", note: "Kriegspiel: арбітр, «No», «Try», напрям шаху"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dark_chess", note: "Dark chess / Fog of War: видно лише досяжне, взяття короля"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Alice_chess", note: "Alice chess: дві дошки, перехід після ходу"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Avalanche_chess", note: "Avalanche: після ходу штовхнути ворожого пішака"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hostage_chess", note: "Hostage: тюрма, аеродром, обмін заручників"}
  - {kind: other, url: "http://www.chessvariants.com/incinf.dir/kriegspiel.html", note: "Chess Variant Pages: Kriegspiel (лінк зі статті Wikipedia)"}
  - {kind: other, url: "http://www.chessvariants.com/mvopponent.dir/avalanche.html", note: "Chess Variant Pages: Avalanche (лінк зі статті Wikipedia)"}
  - {kind: play, url: "https://www.pychess.org/variants/alice", note: "Alice chess онлайн (лінк з черги куратора)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=duck+chess+explained", note: "пошук; Duck Chess"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=kung+fu+chess+gameplay", note: "пошук; Kung-Fu Chess"}
stage: v1
coverage: 55
mechanics: [piece-move-patterns, piece-capture, no-move-into-check, check-stalemate, checkmate, move-timer, realtime-ai, ai-opponent, drag-drop-piece, legal-move-highlight, cell-click, game-settings, game-screen, end-screen, help-window, +pawn-promotion, +piece-drop, +rule-variants, +king-capture-win, +stalemate-win, +neutral-blocker, +piece-cooldown, +superposition-move, +fog-of-war, +referee-arbiter, +linked-boards, +move-opponent-piece, +prisoner-exchange]
proposes: ["+role:neutral", "+role:zone", "+effect:place", "+effect:split", "+effect:measure", "+effect:hide", "+effect:reveal", "+cond:visible", "+cond:value_ge", "+trigger:cooldown_end", "+trigger:check", "+ui:cooldown-ring", "+ui:probability-label", "+ui:fog-overlay", "+ui:board-pair", "+ui:pocket", "+ui:umpire-log", "+window:variant-select", "+axis:info", "+axis:turn-structure", "+axis:win-condition", "+axis:field-boards"]
author: opus
date: 2026-11-02
---

# Шахи з твістом правил — сім варіантів, кожен ламає рівно одне припущення шахів

## Суть
Парасолька над сімома варіантами, що лишають шаховий рух фігур, але виймають одне базове припущення: «на дошці лише фігури» (Duck), «ходять по черзі» (Kung-Fu), «фігура в одній клітині» (Quantum), «бачиш усю дошку» (Kriegspiel/Dark), «дошка одна» (Alice), «рухаєш лише свої» (Avalanche), «взята фігура зникає» (Hostage). Разом із [lichess-variants.md](lichess-variants.md) (умови перемоги, доля взяття) дає повний набір осей «шахи як параметризований рушій». Для кожного варіанта нижче — дельта правил і слово граматики, якого бракує.

## Поле і час
- Базово — дошка 8×8 і шаховий рух ([chess.md](chess.md)).
- **Kung-Fu**: `time: realtime` — черги нема, кожна фігура після ходу має кулдаун; рух триває в часі.
- **Kriegspiel/Dark**: `info: hidden` — Kriegspiel: три дошки (по одній у гравців, повна — в арбітра); Dark: кожен бачить лише свої фігури й клітини, куди може сходити.
- **Quantum**: стан клітини — амплітуда/ймовірність; вимірювання (взяття/блок) — `random: runtime`.
- **Alice**: дві дошки A і B (`field: layers` за суттю), фігура після ходу переходить на відповідну клітину іншої дошки.
- **Hostage**: поза дошкою — тюрма й аеродром кожної сторони (як кишеня Crazyhouse, але з обміном).
- **Duck**: на дошці нейтральна фігура-блокер, яку переставляє той, хто щойно сходив.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Шахові фігури K Q R B N P | piece | як у стандарті | патерни ходу без змін (крім Kung-Fu — у часі) |
| Качка (Duck) | neutral | 1 на дошці | після кожного ходу переставляється на **іншу** порожню клітину; ніхто не може стати на неї чи пройти крізь; кінь перестрибує |
| Кулдаун фігури (Kung-Fu) | — | тривалість | після руху фігура «відпочиває»; поки йде таймер — не ходить |
| Квантова фігура (Quantum) | piece | ймовірність у кожній клітині | split → у двох клітинах одразу; merge — назад; при вимірюванні «колапсує» |
| Арбітр (Kriegspiel) | neutral | бачить усе | відповідає «No» / «Hell no», оголошує взяття (клітину), шах (напрям), «Try» для пішаків |
| Туман (Dark) | zone | на сторону | приховує все, крім своїх фігур і клітин, куди вони можуть сходити |
| Дошка B (Alice) | zone | порожня на старті | дзеркальна пара до A; фігура після ходу переходить між ними |
| Ворожий пішак під штовханням (Avalanche) | piece | належить супернику | рухається на 1 вперед за волею того, хто сходив |
| Тюрма (Hostage) | zone | на сторону | тут лежать взяті ворожі фігури — «заручники» |
| Аеродром (Hostage) | supply | на сторону | свої фігури, повернуті з обміну; звідси — дроп |

## Правила (КОЛИ → ЯКЩО → ТО)
Дельта-таблиця (усе інше — як у [chess.md](chess.md)):

| Варіант | Рік, автор | Що змінено | Слово граматики |
|---|---|---|---|
| Duck Chess | 2016, Tim Paulden | після ходу — обовʼязково переставити качку-блокер; шаху нема, мета — взяти короля; пат = перемога запатованого | `+role:neutral`, `place`, `+axis:win-condition: king-capture` |
| Kung-Fu Chess | 2002, Dan і Joshua Goldstein (Shizmoo) | черги нема, будь-яка готова фігура ходить будь-коли; після руху — кулдаун; рух не миттєвий; шаху й пату нема, мета — взяти короля | `time: realtime`, `timer`, `+trigger:cooldown_end`, `+axis:turn-structure: free-realtime` |
| Quantum Chess | 2016, Chris Cantwell | split-хід у дві клітини, merge, рух крізь суперпозицію; взяття/блок — вимірювання; шаху нема, мета — взяти короля | `+effect:split`, `+effect:measure`, `rng` |
| Kriegspiel | 1899, Henry Michael Temple | бачиш лише свої; арбітр відхиляє нелегальні спроби й оголошує взяття, шах (напрям), «Any?/Try» | `hide`, `+cond:visible`, `message`, `+ui:umpire-log` |
| Dark chess | 1989, Jens Bæk Nielsen і Torben Osted | бачиш свої + досяжні клітини; про шах не кажуть; мета — взяти короля | `reveal`, `+cond:visible`, `+axis:info` |
| Alice chess | 1953, V. R. Parton | дві дошки; хід легальний на своїй дошці, ціль на іншій дошці порожня; після ходу — перехід | `teleport` (між дошками), `+axis:field-boards` |
| Avalanche | 1977, Ralph Betza | після ходу — обовʼязково штовхнути ворожого пішака на 1 вперед | `+card:move-opponent-piece`, `push` |
| Hostage chess | 1997, John A. Leslie | взяті → у тюрму; хід = рух, або дроп з аеродрому, або обмін заручників (Q > R > B = N > P) | `place`, `give`, `take`, `+cond:value_ge` |

**Duck**
- КОЛИ `move_done(side)` → ТО `input(duck_to)` → ЯКЩО `free(duck_to)` and `duck_to != duck_cell` → ТО `move(duck, duck_to)`, `end_turn`; перший хід білих — `place(duck)` будь-куди.
- КОЛИ `input(move)` → ЯКЩО `custom: «шлях або ціль — качка»` and `not knight` → ТО `block`.
- КОЛИ `contact(piece, enemy_king)` → ТО `win`; КОЛИ `turn_start(side)` → ЯКЩО `no_moves(side)` → ТО `win(side)` (запатований виграє).
- Король може йти під удар і рокіруватись через биті поля (шаху як поняття нема).

**Kung-Fu**
- КОЛИ `input(move(p, to))` → ЯКЩО `not state(p, cooldown)` and `custom: «шлях за патерном»` → ТО `move(p, to)` протягом часу ∝ відстані (?), потім `set_state(p, cooldown, T)`.
- КОЛИ `timer(T)` для p → ТО `clear_state(p, cooldown)`.
- КОЛИ `contact(piece, enemy_king)` → ТО `win`; шаху, звʼязок, мату й пату нема.
- Хто першим прибув у клітину — той бʼє (взяття залежить від таймінгу) (?).

**Quantum**
- КОЛИ `input(split(p, a, b))` → ЯКЩО `p in {K, N, B, R, Q}` and `free(a)` and `free(b)` → ТО `split(p → a, b)` (пішаки не діляться).
- КОЛИ `input(merge(p@a, p@b → c))` → ЯКЩО `same(type)` → ТО `custom: «обʼєднати амплітуди»`.
- КОЛИ `input(move)` → ЯКЩО `custom: «хід може дати подвійне заповнення клітини»` (взяття, блок) → ТО `measure(source|target|path)` → результат вирішує, чи хід відбувся.
- КОЛИ `measure(enemy_king)` → ЯКЩО `custom: «король узятий»` → ТО `win`; шаху нема.

**Kriegspiel / Dark**
- Kriegspiel: КОЛИ `input(try(move))` → ЯКЩО `not legal(move)` (з урахуванням невидимих ворожих) → ТО `message("No")`, той самий гравець пробує ще; ЯКЩО хід неможливий у принципі → `message("Hell no")`.
- КОЛИ `contact(piece, enemy)` → ТО `message("Piece/Pawn gone at <cell>")` обом.
- КОЛИ `check(side)` → ТО `message(direction)`: вертикаль / горизонталь / довга чи коротка діагональ / кінь.
- КОЛИ `input("Any?")` → ЯКЩО є взяття пішаком → ТО `message("Try")`, гравець мусить спробувати хоч одне; інакше `message("No")`.
- Dark: КОЛИ `turn_start(side)` → ТО `hide(all)`, `reveal(own pieces ∪ cells reachable by own moves)`; КОЛИ `contact(piece, enemy_king)` → ТО `win` (про шах не попереджають).

**Alice**
- КОЛИ `input(move(p, to))` → ЯКЩО `legal(move)` на дошці p and `free(to on other board)` → ТО `move(p, to)`, `teleport(p, other_board[to])`.
- Взяття — лише на своїй дошці; після переходу власний король не може бути під шахом на жодній з дошок.

**Avalanche**
- КОЛИ `move_done(side)` → ТО `input(push(enemy_pawn))` → ЯКЩО `free(cell in front of pawn)` → ТО `move(enemy_pawn, forward)` (без взяття); нема можливого — фаза пропускається.
- ЯКЩО штовхання перетворює пішака → вибір фігури робить **власник**; ЯКЩО **кожне** можливе штовхання дає шах тому, хто штовхає → `win(owner)`.

**Hostage**
- КОЛИ `contact(piece, enemy)` → ТО `disappear_b`, `give(capturer.prison, b)`.
- КОЛИ `input(drop(kind, cell))` → ЯКЩО `has(own.airfield, kind)` and `free(cell)` and `not (P on rank 1/8)` → ТО `place(kind, cell)`.
- КОЛИ `input(exchange(x, y, cell))` → ЯКЩО `has(own.prison, x)` and `has(enemy.prison, y)` and `value_ge(x, y)` → ТО `give(enemy.airfield, x)`, `take(enemy.prison, y)`, `place(y, cell)`.
- Перетворення пішака — лише у фігуру, що сидить у тюрмі суперника; пішак іде в ту тюрму.

- Перемога: мат (Kriegspiel, Alice, Avalanche, Hostage) · взяття короля (Duck, Kung-Fu, Quantum, Dark) · пат = перемога (Duck) · примусовий шах при штовханні (Avalanche).

## Керування і ввід
- Duck: хід у дві дії — фігура, потім drag/клік качки на нову клітину (Chess.com).
- Kung-Fu: клік/drag будь-якої «готової» фігури в будь-який момент; кулдаун показується на фігурі; жодної кнопки «кінець ходу».
- Quantum: окремі режими вводу «split» (дві цілі) і «merge» (два джерела) поверх звичайного drag.
- Kriegspiel: спроба ходу → відповідь арбітра; кнопка «Any?» для пішаків. Dark: звичайний drag, туман малює клієнт.
- Alice: вибір дошки неявно — фігура лежить на одній із двох; дві дошки поруч.
- Hostage/Avalanche: додаткова дія — drag з тюрми/аеродрому, вибір пари обміну; клік по ворожому пішаку для штовхання.

## Вікна, меню, HUD
- `variant-select` — вибір варіанта при створенні партії (Chess.com Variants: Duck, Fog of War тощо).
- `game-screen`: дошка + для Duck — фігура качки; Kung-Fu — `cooldown-ring` на кожній фігурі; Quantum — `probability-label` (% у клітині); Dark — `fog-overlay`; Kriegspiel — `umpire-log` (стрічка оголошень арбітра); Alice — `board-pair` (дві дошки поруч); Hostage — `pocket` ×4 (тюрма й аеродром кожної сторони).
- `help-window` — правила варіанта; `end-screen` — причина (взяття короля, пат-перемога, мат).
- Переходи: main-menu → variant-select → lobby/пошук → game-screen → end-screen.

## Фічі поза полем
- `custom-rules` — варіант як параметр партії; окремі рейтинги варіантів (Chess.com) (?).
- `online-multiplayer` — для прихованих варіантів обовʼязковий (комп'ютер = арбітр; за дошкою — три набори і людина-арбітр).
- `turn-timer` у Kung-Fu не потрібен — сам час є ресурсом; `speed-control` (стандарт/блискавичний темп) (?).
- `replay` прихованої партії — показ з точки зору кожного гравця або повний (?).

## Варіації й родичі
- [lichess-variants.md](lichess-variants.md) (Crazyhouse ~ Hostage, Atomic, Antichess), шогі (дропи), Bughouse; Stratego — прихована інформація; Tsuitate shogi — Kriegspiel для шогі.
- Kriegspiel має гілки: Wild 16 (ICC), Modern kriegspiel (1986), Crazyhouse Kriegspiel; Dark chess — Fog of War на Chess.com.
- **Осі варіацій** (кожен варіант — одне значення):
  - **Хто на дошці**: лише фігури сторін · + нейтральний блокер (Duck).
  - **Черговість**: строго по черзі · real-time з кулдауном (Kung-Fu).
  - **Положення фігури**: одна клітина · суперпозиція клітин (Quantum).
  - **Видимість**: повна · лише свої + арбітр (Kriegspiel) · свої + досяжні (Dark).
  - **Кількість дощок**: одна · дві з переходом (Alice) · дві пари (Bughouse).
  - **Чиї фігури рухаєш**: свої · + одну ворожу щоходу (Avalanche).
  - **Доля взятої**: зникає · кишеня суперника (Crazyhouse) · заручник для обміну (Hostage).
  - **Ціль**: мат · взяття короля · пат = перемога.

## Цікавинки для курсу
- Duck: другий крок ходу (нейтральний блокер) + взяття короля замість мату — 📎 поверх готового шахового рушія.
- Kung-Fu: перевести покроковий рушій у real-time з кулдаунами й рухом у часі — 🥈 (конфлікти «хто перший прибув»).
- Dark chess: туман як множина досяжних клітин, рендер прихованих клітин — 🥉; Kriegspiel-арбітр з відповідями й напрямком шаху — 🥈.
- Alice: дві дошки з перевіркою «ціль на іншій дошці порожня» і шаху на обох — 🥈.
- Avalanche: друга фаза ходу з фігурою суперника + рідкісний «примусовий програш» — 🥉.
- Hostage: тюрма/аеродром, обмін за цінністю, обмежене перетворення — 🥈.
- Quantum: стан як вектор амплітуд, split/merge, вимірювання з ймовірністю — 👑.

## Мапа на каталог
- Є: `piece-move-patterns` · `piece-capture` · `no-move-into-check` (Alice, Avalanche, Hostage, Kriegspiel) · `check-stalemate` · `checkmate` · `move-timer` · `realtime-ai` ↔ Kung-Fu проти бота · `ai-opponent` · `drag-drop-piece` · `legal-move-highlight` · `cell-click` · `game-settings` ↔ вибір варіанта · `game-screen` · `end-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+king-capture-win` «Перемога взяттям короля (без шаху)» · game-logic/win · 🌱 — Duck, Kung-Fu, Quantum, Dark.
  - `+stalemate-win` «Пат = перемога запатованого» · game-logic/win · 🌱 — Duck.
  - `+neutral-blocker` «Нейтральний блокер, якого переставляє той, хто сходив» · entities/legality · 📎 — качка.
  - `+piece-cooldown` «Кулдаун фігури після ходу» · game-logic/opponent · 🥈 · слоти {cooldown, move_speed} — Kung-Fu.
  - `+superposition-move` «Хід у суперпозицію й вимірювання» · entities/state · 👑 — Quantum.
  - `+fog-of-war` «Туман: видно лише досяжне» · interface/render · 🥉 · слоти {reveal: own|reachable|radius} — Dark.
  - `+referee-arbiter` «Арбітр відповідає на спроби ходу» · game-logic/constraints · 🥈 — Kriegspiel.
  - `+linked-boards` «Дві дошки з переходом фігури» · entities/move · 🥈 — Alice.
  - `+move-opponent-piece` «Рух фігури суперника як частина ходу» · game-logic/opponent · 🥉 — Avalanche.
  - `+prisoner-exchange` «Обмін заручників» · entities/combat · 🥈 · слоти {values: Q>R>B=N>P} — Hostage.
  - (`+piece-drop`, `+pawn-promotion`, `+rule-variants` — див. chess.md / lichess-variants.md.)

## Пропозиції до словників
- `+role:neutral` (⏳ є) — качка й арбітр: ні сторона, ні «ворог».
- `+effect:place` — качка, дроп з аеродрому; `+effect:split` / `+effect:measure` — квантовий хід і колапс (з `rng`).
- `+effect:hide` / `+effect:reveal` (⏳ є) — туман Dark chess; `+cond:visible(cell, side)` — чи бачить сторона клітину.
- `+cond:value_ge(x, y)` — порівняння цінності фігур (обмін Hostage; родич `+cond:stronger` з arimaa.md).
- `+trigger:cooldown_end(p)` — фігура знову готова (Kung-Fu); також для `skill-bar`-кулдаунів у тактиках.
- `+trigger:check` — підтверджую (Kriegspiel оголошує напрям шаху).
- `+ui:cooldown-ring` — індикатор кулдауну на фігурі; `+ui:probability-label` — % присутності; `+ui:fog-overlay` (⏳ є); `+ui:board-pair` — дві дошки поруч; `+ui:pocket` — підтверджую (тюрма/аеродром); `+ui:umpire-log` — стрічка оголошень арбітра.
- `+window:variant-select` — підтверджую.
- `+axis:info` — нове значення `refereed` (Kriegspiel: інформація через арбітра).
- `+axis:turn-structure` — значення `free-realtime` (без черги, з кулдауном).
- `+axis:win-condition` — значення `king-capture`, `stalemate-win`.
- `+axis:field-boards` — кількість звʼязаних дощок (1 / 2 Alice / 2×2 Bughouse).

## Джерела
- ⭐ [Chess.com: Duck Chess](https://www.chess.com/terms/duck-chess) — правила качки, взяття короля, пат = перемога, історія (Paulden 2016, вірусність 2022).
- [Wikipedia: Kung-fu chess](https://en.wikipedia.org/wiki/Kung-fu_chess) — без черги, кулдаун, без шаху/пату, Shizmoo, IGF 2002.
- [arXiv: Cantwell, Quantum Chess](https://arxiv.org/abs/1906.05836) — split/merge jump/slide, вимірювання при можливому подвійному заповненні, без шаху; HTML-версія — повні правила.
- [Wikipedia: Kriegspiel](https://en.wikipedia.org/wiki/Kriegspiel_(chess)) — три дошки, оголошення арбітра, «Any?/Try», варіанти.
- [Wikipedia: Dark chess](https://en.wikipedia.org/wiki/Dark_chess) — видимість, взяття короля, en passant, Fog of War на Chess.com.
- [Wikipedia: Alice chess](https://en.wikipedia.org/wiki/Alice_chess) — дві дошки, умови легальності, рокіровка.
- [Wikipedia: Avalanche chess](https://en.wikipedia.org/wiki/Avalanche_chess) — обовʼязкове штовхання, промоція власником, примусовий шах.
- [Wikipedia: Hostage chess](https://en.wikipedia.org/wiki/Hostage_chess) — тюрма, аеродром, обмін, обмежене перетворення.
- [Chess Variant Pages: Kriegspiel](http://www.chessvariants.com/incinf.dir/kriegspiel.html) · [Avalanche](http://www.chessvariants.com/mvopponent.dir/avalanche.html) — лінки зі статей Wikipedia.
- [PyChess: Alice](https://www.pychess.org/variants/alice) — грати онлайн (лінк з черги, сам не відкривав).
- YouTube: пошуки «duck chess explained», «kung fu chess gameplay».

## Непевне
- (?) Kung-Fu: тривалість кулдауну, чи можна взяти фігуру «в польоті», хто бʼє при одночасному прибутті — Wikipedia не уточнює.
- (?) Quantum: дата й платформи комерційної версії (Quantum Realm Games, Steam), точне правило перемоги при «напівприсутньому» королі, рокіровка/en passant — повних правил не дочитав (обрізана HTML-версія статті).
- (?) Hostage: формулювання «рівна або **більша** цінність» віддаваної фігури — у статті Wikipedia тіло й підсумок суперечать; узяв тіло.
- (?) Alice: тонкощі «шаху на першій дошці до переходу» — переказано спрощено.
- (?) Duck: en passant і перетворення як у стандарті — з памʼяті.
- Шапка: `info: hidden`, `random: runtime`, `opponent: online` — за найнезвичнішими членами набору (Kriegspiel/Dark, Quantum); решта — як у шахах.
