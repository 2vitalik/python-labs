---
title: Gobblet (Гоблет)
slug: gobblet
aka: [Гоблет, Gobblet Gobblers, Gobblet Jr., Gobblet X4]
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
year: 2001
platforms: [board, mobile, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Gobblet", best: true, note: "4×4, 12 фігур різного розміру на гравця, більша накриває меншу, 4 у ряд; Denoual 2001, Gobblet Jr. 3×3, Gobblers / X4"}
  - {kind: other, url: "https://www.ultraboardgames.com/gobblet/game-rules.php", note: "повні правила: 3 зовнішні стеки по 4, виняток «3 в ряд», touch-move, програш при відкритті лінії суперника, нічия повторенням"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Gobblet+board+game+rules", note: "пошук; правила й партії"}
stage: v1
coverage: 70
mechanics: [hot-seat, turn-enforcement, ai-opponent, ai-random, ai-greedy, ai-minimax, cell-click, drag-drop-piece, hover-highlight, selection-highlight, legal-move-highlight, last-move-highlight, repetition-draw, field-size-picker, rule-variants, game-screen, main-menu, end-screen, help-window, settings-window, replay, state-as-data, unit-tests, level-solver, +place-stone, +line-win, +stack-by-size, +reserve-stacks, +reveal-on-lift, +touch-move, +reveal-loses, +reserve-exception]
proposes: ["+effect:cover", "+effect:uncover", "+cond:bigger", "+cond:top_of_stack", "+trigger:revealed", "+trigger:touched", "+ui:stack-view", "+ui:reserve-stacks", "+card:reserve-stacks", "+card:reveal-on-lift", "+card:touch-move", "+card:reveal-loses", "+card:reserve-exception"]
author: opus
date: 2026-11-09
---

# Gobblet — хрестики-нулики 4×4, де більша фігура «ковтає» меншу, а підняти її — означає відкрити те, що під нею

## Суть
Двоє складають 4 у ряд на полі 4×4, але фігури бувають чотирьох розмірів: більша може **накрити** («зʼїсти», gobble) меншу — і чужу, і свою. Можна ставити нову фігуру з зовнішніх стеків або **переносити** вже поставлену на будь-яку клітину — і тоді відкривається те, що було під нею. Тримати в голові, що сховано під кожною вежею, — половина гри: підняв не ту фігуру — відкрив супернику готову лінію і програв. Найближчий родич — `line-games.md` (N-in-a-row); новизна — накривання за розміром і памʼять.

## Поле і час
- Поле 4×4 (16 клітин); на клітині — **стек** фігур, видно лише верхню; глибина стеку до 4 (?).
- Поза полем у кожного — 3 зовнішні стеки по 4 вкладені фігури; на старті видно лише 3 найбільші (верхівки).
- Покроково, двоє; хід = одна дія однією фігурою.
- Інформація формально повна (обидва бачили кожну постановку), але практично прихована — фігури під верхньою не видно, тож гра тестує памʼять.
- Gobblet Jr. / Gobblet Gobblers — 3×3, для дітей (від 2003 / 2009).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гоблет | piece | колір; розмір 1–4 | ставиться з зовнішнього стеку або переходить по полю; накриває будь-яку меншу (свою чи чужу) |
| Зовнішній стек | container | 4 вкладені фігури, від найбільшої вгорі | грати можна лише верхню; 3 стеки на гравця |
| Клітина-стек | container | фігури одна на одній | видно й рахується лише верхня |
| Накрита фігура | piece | під іншою | не рахується в лінію; оживає, коли верхню знімуть |
| Лінія з 4 | zone | 4 верхні фігури одного кольору в ряд / стовпець / діагональ | перемога; розміри можуть бути різні |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, gobblet, cell)` → ЯКЩО `custom: «gobblet — верхній у своєму зовнішньому стеку»` (`+cond:top_of_stack`) і `free(cell)` → ТО `place(gobblet, cell)`, `end_turn`.
- Виняток з запасу: КОЛИ `input(place, gobblet, cell)` → ЯКЩО `pattern(line(3))` суперника і `custom: «cell — одна з трьох фігур цієї лінії, і вона менша за gobblet»` → ТО `custom: «накрити з запасу»` (`+effect:cover`).
- КОЛИ `input(move, gobblet, cell)` → ЯКЩО `custom: «gobblet — свій і верхній на клітині»` і `free(cell)` → ТО `move(gobblet, cell)`, `end_turn`.
- КОЛИ `input(move, gobblet, cell)` → ЯКЩО `occupied(cell, smaller)` (`+cond:bigger`: верхня в cell менша, будь-якого кольору) → ТО `custom: «накрити»` (`+effect:cover`), `end_turn`; розмір може бути на кілька менший, не лише на один.
- КОЛИ `input(move, gobblet, cell)` → ЯКЩО `custom: «верхня в cell рівна або більша»` → ТО `block`.
- КОЛИ `after(move)` → ТО `custom: «відкрити фігуру, що лежала під gobblet»` (`+effect:uncover`, `+trigger:revealed`) — вона знову в грі.
- КОЛИ `input(touch, gobblet)` (`+trigger:touched`) → ТО `custom: «мусиш зіграти саме цю фігуру»`; ЯКЩО `not legal(any_move(gobblet))` → ТО `lose`.
- Фігура переміщується лише одна за раз: підняти верхню, не захоплюючи нижні.
- КОЛИ `after(move)` → ЯКЩО `custom: «відкрилась лінія з 4 фігур суперника»` → ТО `lose`, крім випадку, коли фігура, якою ходили, сама накрила одну з фігур цієї лінії.
- КОЛИ `pattern(line(4))` (верхні фігури одного кольору, будь-якого розміру) → ТО `win`.
- КОЛИ `custom: «усі 12 фігур виставлено»` → ТО гра триває лише переміщеннями по полю.
- КОЛИ `repetition(3)` (обидві сторони тричі повторили ті самі ходи) → ТО `draw`; також нічия за згодою.
- Перемога: 4 у ряд · Поразка: відкрив лінію суперника / торкнувся фігури без легального ходу · Рахунок: партія 1 / ½ / 0.

## Керування і ввід
- Настільна: підняти верхню фігуру зі стеку чи з клітини й поставити; touch-move — торкнувся, мусиш ходити.
- (цифрова версія) Клік по верхній фігурі свого зовнішнього стеку або поля → підсвічуються легальні клітини (порожні + з меншою верхньою; для запасу — лише порожні та фігури лінії-трійки суперника).
- Touch-move у цифровій версії — це «вибір зафіксовано»: після виділення скасувати не можна (опція) (?).
- Drag-n-drop; наведення на стек показує його вміст (опція «підказка памʼяті», вимикається для чесної гри).

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Проти AI · Двоє · Правила · Налаштування.
- `match-setup` / `settings-window`: варіант (Gobblet 4×4 / Gobblers 3×3), рівень AI, touch-move увімк/вимк, показ вмісту стеків увімк/вимк.
- `game-screen`: поле 4×4 зі стеками; `reserve-stacks` — по 3 зовнішні стеки кожного гравця поруч із полем; `turn-indicator`; `selection-highlight`; `legal-move-highlight`; `stack-view` (вміст стеку при наведенні, якщо дозволено); `last-move-highlight`; `win-line`.
- `end-screen`: перемога / поразка з причиною (лінія / відкрив лінію суперника / touch-move); Реванш.
- `help-window`: розміри, виняток «3 в ряд», відкриття лінії.
- `replay-window`: перегляд партії зі стеками.
- Переходи: main-menu → match-setup → game-screen → end-screen → game-screen.

## Фічі поза полем
- `rule-variants`: 4×4 / 3×3, touch-move, показ стеків, виняток із запасу.
- `ai-opponent-levels`, `undo` проти AI, `replay`, `hint`.
- `assist-mode` — «рентген» стеків для дітей / навчання.

## Варіації й родичі
- **Gobblet Jr.** (2003) — 3×3, молодший вік; з 2009 Gobblet і Jr. замінені на **Gobblet X4** і **Gobblet Gobblers**.
- Родичі: хрестики-нулики / N-in-a-row (`line-games.md`) — та сама ціль без накривання; Quarto (4×4, фігуру обирає суперник) (?); стовпові ігри Lasca (`lasca.md`), Tak (`tak.md`) — стек із верхньою фігурою як власником.
- **Осі варіацій**: поле (3×3 / 4×4) · розмірів (3 / 4) · запас (стеки з порядком / вільна рука) · виняток «накрити з запасу» (лише по лінії-трійці / завжди) · touch-move (так / ні) · кара за відкриту лінію суперника (програш / виграш суперника лише якщо не перекрив).

## Цікавинки для курсу
- Клітина як стек фігур з порівнянням розміру при постановці — 🌱.
- Зовнішні стеки з порядком (лише верхня) — 🌱.
- Відкриття фігури під знятою і перевірка ліній **обох** сторін після ходу, з винятком «накрив фігуру лінії» — 📎.
- Виняток «з запасу можна накрити лише фігуру лінії-трійки суперника» — 📎.
- Touch-move як фіксація вибору в UI — 🌱.
- Повний розвʼязувач Gobblers 3×3 / AI minimax для 4×4 зі стеками — 🥈 / 🥇.

## Мапа на каталог
- Є: `hot-seat`, `turn-enforcement` · `ai-opponent`, `ai-random`, `ai-greedy`, `ai-minimax` · `cell-click`, `drag-drop-piece`, `hover-highlight`, `selection-highlight`, `legal-move-highlight`, `last-move-highlight` · `repetition-draw` ↔ 3 повторення · `field-size-picker` ↔ 3×3/4×4 · `rule-variants` · `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window` · `replay`, `state-as-data`, `unit-tests` · `level-solver` ↔ розвʼязання 3×3.
- **Нема** → пропозиції карток:
  - `+place-stone`, `+line-win` (див. `line-games.md`).
  - `+stack-by-size` (уже в корпусі) — більша накриває меншу.
  - `+reserve-stacks` «Запас у стеках, грається лише верхня» · entities/legality · 🌱.
  - `+reveal-on-lift` «Зняв верхню — відкрив нижню» · entities/interact · 🌱.
  - `+touch-move` «Торкнувся — ходи» · interface/input · 🌱.
  - `+reveal-loses` «Відкрив лінію суперника — програв» · game-logic/lose · 📎.
  - `+reserve-exception` «Із запасу накривати лише фігуру загрозливої лінії» · entities/legality · 📎.

## Пропозиції до словників
- `+effect:cover` — уже в `cottage-garden.md` / `copenhagen.md` (клітини); тут — фігура накриває фігуру.
- `+effect:uncover` — знята верхня відкриває нижню.
- `+cond:bigger` — розмір A більший за верхню B.
- `+cond:top_of_stack` — сутність верхня у стеку / запасі.
- `+trigger:revealed` — уже в корпусі; тут — фігура стала верхньою після зняття накривки.
- `+trigger:touched` — гравець торкнувся / виділив фігуру (touch-move).
- `+ui:stack-view` (уже в корпусі) · `+ui:reserve-stacks` — запас гравця стеками поруч з полем.
- `+card:reserve-stacks` · `+card:reveal-on-lift` · `+card:touch-move` · `+card:reveal-loses` · `+card:reserve-exception` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Gobblet](https://en.wikipedia.org/wiki/Gobblet) — 4×4, 12 фігур різного розміру, більша накриває меншу, 4 у ряд; Thierry Denoual, Gigamic / Blue Orange 2001, фіналіст Jeu de l'année 2004; Gobblet Jr. 2003 (3×3), заміна на Gobblet X4 і Gobblet Gobblers 2009.
- [UltraBoardGames: правила Gobblet](https://www.ultraboardgames.com/gobblet/game-rules.php) — 3 зовнішні стеки по 4, на старті видно 3 найбільші, постановка лише на порожнє (виняток — фігура лінії-трійки суперника), перенос на порожнє / накриття меншої будь-якого кольору, touch-move з програшем, програш при відкритті лінії суперника (крім накриття фігури цієї лінії), гра без запасу, нічия трьома повтореннями.
- YouTube: пошук «Gobblet board game rules».

## Непевне
- (?) Чотири розміри фігур — висновок з «3 стеки по 4 вкладені»; явно числа розмірів у відкритих джерелах не бачив.
- (?) Gobblet Gobblers: 3×3, по 6 фігур трьох розмірів, без обмеження «лише по лінії-трійці» для запасу — з памʼяті, сторінку правил не відкрив.
- (?) Gobblet X4 (для 4 гравців?) — у статті лише назва.
- (?) Що буде, якщо хід одночасно склав свою лінію й відкрив лінію суперника, — у джерелах окремо не розібрано (за правилом — програш, якщо не накрив фігуру тієї лінії).
- (?) Розвʼязаність Gobblet / Gobblers — у джерелах нема.
- (?) Quarto як родич — з памʼяті.
