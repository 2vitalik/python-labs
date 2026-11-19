---
title: Vext Edit
slug: vext-edit
aka: [VEXT EDIT]
family: thinky
also: [push-slide]
klass: hybrid
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2019
platforms: [web]
links:
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=9eb8f8f3df4efb450b798a279eeba2e0", best: true, note: "грати в браузері (PuzzleScript); 32 сторінки-рівні у 8 «книжках»"}
  - {kind: other, url: "https://api.github.com/gists/9eb8f8f3df4efb450b798a279eeba2e0", note: "вихідний код як gist (JSON), JackLance, 11.07.2019: усі правила, шари, умови перемоги, рівні"}
  - {kind: other, url: "https://www.bontegames.com/2019/07/vext-edit-browser.html", note: "Bart Bonte, 12.07.2019: «Push everything into place»; Z — undo, R — рестарт; коментарі: жовті стіни для гравця, червоні — для курсора, «1» під стіною робить її доступною"}
  - {kind: other, url: "https://twitter.com/Jack_L_Lance", note: "автор, Jack Lance (лінк зі статті Bonte)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Vext+Edit+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, impassable-cells, multi-cell-size, stick-together, fill-hole, all-on-targets, cursor-place, editor-palette, party-switch, undo-unlimited, restart-level, sequential-levels, save-progress, level-from-txt, sound-effects, +self-built-level, +nested-editors, +copy-counter-palette, +placeable-numbers, +layer-walls, +pit-underlayer, +control-handover, +multi-agent-sync, +ghost-preview, +push-chain, +cross-layer-crate]
proposes: ["+role:cursor", "+effect:possess", "+axis:actors", "+card:nested-editors", "+card:copy-counter-palette", "+card:placeable-numbers"]
author: opus
date: 2026-11-19
---

# Vext Edit — Sokoban, де посеред рівня береш курсор редактора й домальовуєш собі ящики, гравців і навіть сам редактор

## Суть
PuzzleScript-гра Jack Lance: звичайний Sokoban із зчепленими ящиками та ямами, але на рівні лежить **палітра** — обʼєкти з числами під ними. Гравець перетворюється на червоний курсор, бере обʼєкт із палітри й ставить його копії, поки не скінчиться лічильник; потім повертається в гравця і штовхає те, що собі намалював.

Далі зʼявляється синій курсор, який редагує вже сам редактор: ставить червоні курсори, стіни й числа. Мета кожної «сторінки» — усі цілі накриті, і її спершу треба зрозуміти.

## Поле і час
- Квадратна сітка, вигляд згори; сторінки від 6×6 до 23×20 клітин (за кодом рівнів); ранні обведено жовтими стінами, сторінки з курсором — чорними клітинами, а палітра лежить під кімнатою.
- Три **шари одного поля** з окремою фізикою (кольором): жовтий — гра (гравець, ящики, жовті стіни, ями, цілі); червоний — редактор (червоний курсор, червоні ящики, стіни, ями, цілі, числа); синій — мета-редактор (синій курсор, сині стіни, сині числа). Стіна блокує лише свій шар; чорне блокує всіх.
- Коли активний гравець, червоні ящики, стіни й ями стають «примарами» й не заважають; коли активний курсор — повертаються.
- Покроково: хід = натискання; PuzzleScript, `run_rules_on_level_start`, `norepeat_action`.
- 8 «книжок» по 4 сторінки: BASE · EDIT · DUAL · WHAT · UHHH · BLUE · ?!?! · (RE)STAR(TS) — остання повторює ранні сторінки з меншими запасами.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | активний / неактивний; у ямі | 4 напрямки; штовхає ящики й інших гравців ланцюгом; X — стати курсором |
| Червоний курсор | player | порожній / тримає взірець | ходить крізь жовті стіни й обʼєкти; штовхає червоні ящики; бере й ставить копії |
| Синій курсор | player | порожній / тримає | ставить копії червоного курсора, червоних стін і ящиків, чисел; X на червоному курсорі — передати керування |
| Ящик | object | зчеплення з сусідами | штовхається; зчеплені частини рухаються разом; без опори над ямою падає |
| Впалий ящик | terrain | зчеплення | засипає яму: по ньому ходять; гравець у ямі його штовхає |
| Червоний ящик | object | — | штовхає лише червоний курсор; падає в червону яму |
| Червоно-жовтий ящик | object | — | живе в обох шарах; рухається, лише якщо вільно в обох |
| Яма жовта / червона | hazard | — | гравець або курсор падає, але далі ходить по ямі; ящик її засипає |
| Стіна жовта / червона / синя | static | шар | блокує лише сутності свого шару |
| Чорна клітина | static | — | блокує всіх |
| Число: червоне 1–7 або ∞, синє 1–3 | supply | значення | обʼєкт над числом — взірець палітри; саме число теж можна брати й ставити |
| Ціль для ящика · ціль для гравця · червона ціль | zone | шар | умова перемоги |
| Мітки рівня «можна в курсор» / «можна в синій» | zone | — | невидимі; вмикають перемикання керування на сторінці |

## Правила (КОЛИ → ЯКЩО → ТО)
Гра (жовтий шар):
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(player, dir)`; інакше `block`.
- КОЛИ `contact(player, crate)` → ЯКЩО `free(cell_behind_chain)` → ТО `push(crate)` — ящик штовхає ящик і гравця, гравець штовхає гравця.
- КОЛИ `after(push)` → ЯКЩО `custom: «будь-яка зчеплена частина впирається»` → ТО `block` для всього ящика.
- КОЛИ `enter(crate, pit)` → ЯКЩО `not supported(crate)` (жодна зчеплена частина не стоїть на підлозі чи впалому ящику) → ТО `fall(crate)`, `transform(crate, fallen_crate)`.
- КОЛИ `enter(player, pit)` → ЯКЩО `not occupied(pit, fallen_crate)` → ТО `fall(player)`, `set_state(player, in_pit)` — далі ходить лише ямою й штовхає впалі ящики.
Перемикання керування:
- КОЛИ `input(action)` → ЯКЩО `custom: «на сторінці дозволено курсор, під гравцем нема червоних обʼєктів»` → ТО `spawn(red_cursor, player_cell)`, `custom: «керування — курсору»`.
- КОЛИ `input(action)` → ЯКЩО `occupied(cursor_cell, player)` → ТО `disappear(red_cursor)`, `custom: «керування — цьому гравцеві»` — так перемикаються між кількома гравцями.
- КОЛИ `input(action)` → ЯКЩО `custom: «дозволено синій курсор»` → ТО `spawn(blue_cursor, cursor_cell)`; синій на червоному курсорі + X → назад у червоний.
Редагування:
- КОЛИ `input(action)` → ЯКЩО `custom: «курсор над обʼєктом, під яким число»` → ТО `set_state(cursor, holding)`, `custom: «показати примару обʼєкта під курсором»`.
- КОЛИ `input(action)` → ЯКЩО `state(cursor, holding)` і `free(cursor_cell)` (нема обʼєкта шару й числа) → ТО `place(cursor, copy)`, `counter(number, -1)`.
- КОЛИ `counter(number, ==, 0)` → ТО `disappear(sample)`, `disappear(number)` — остання копія фактично переносить взірець.
- КОЛИ `after(place(cursor, crate))` → ЯКЩО `adjacent_count(new_crate, crate, >=, 1)` → ТО `attach(new_crate, crate)` — поставлений ящик зчіплюється з сусідами.
- КОЛИ `after(place(cursor, number))` → ТО `custom: «обʼєкт над новим числом стає взірцем палітри»`.
- КОЛИ `contact(red_cursor, red_crate)` → ЯКЩО `free(cell_behind)` і `not occupied(red_crate_cell, number)` → ТО `push(red_crate)`.
- КОЛИ `enter(red_cursor, red_pit)` → ТО `fall(red_cursor)`, `transform(red_cursor, dead_cursor)` — мертвий курсор ходить лише червоною ямою.
- КОЛИ `input(dir)` → ЯКЩО `count(active_cursor, >, 1)` → ТО `custom: «обидва курсори рухаються разом»` (TWIN).
Перемога:
- КОЛИ `all_on(crate, target)` і `all_on(red_crate, red_target)` і `all_on(player, player_target)` → ЯКЩО `custom: «червоний курсор не стоїть на цілі»` → ТО `win`, `next_level`.
- Перемога: усі три види цілей накриті. · Поразка: нема; глухий кут → undo / рестарт. · Рахунку нема.

## Керування і ввід
- Стрілки / WASD — крок активного гравця чи курсора; X — дія: взяти, поставити, перемкнути керування; Z — undo без ліміту; R — рестарт (стандарт PuzzleScript; Bonte: «Z key to undo a move, R key to restart»).
- Утримання X не повторює дію (`norepeat_action`).
- На сторінках TWIN і VARY активних курсорів два — рухаються синхронно.

## Вікна, меню, HUD
- `main-menu` (титул PuzzleScript): VEXT EDIT · JACK; start / continue.
- `custom-window` повідомлення: «Book N: …», «Page N.M: …» перед кожною сторінкою.
- `game-screen`: поле без HUD; лічильники — самі числа-обʼєкти на полі, примара взятого обʼєкта під курсором (`drag-ghost`), підсвітка пари «взірець + число» (`selection-highlight`).
- Переходи: титул → повідомлення книжки → сторінка → (перемога) → наступна сторінка.

## Фічі поза полем
- `levels-sequential` (32 сторінки), `continue` у браузері.
- `undo` ∞, `restart-level`.
- Код відкритий: gist читається в редакторі PuzzleScript.

## Варіації й родичі
- [Baba Is You](baba-is-you.md) — правила як обʼєкти; тут **редактор як обʼєкти**.
- [Ice path](ice-path.md) — гравець будує рівень, який потім розвʼязує; [RE:COPY](recopy.md) — копіювання ділянок поля.
- [One More Button](one-more-button.md) — керування як обʼєкти на полі; [Patrick's Parabox](patricks-parabox.md) — вкладеність.
- [0PLAYER](0player.md) (2025) — присвячена памʼяті Jack Lance.
- **Осі варіацій:** хто редагує — гравець-курсор / мета-курсор / ніхто · запас — лічильник / ∞ / саме число як ресурс · падіння в яму — смерть / нова підлога / рух усередині ями (тут).

## Цікавинки для курсу
- Палітра з лічильниками: обʼєкт над числом → взяти, поставити копію, −1; остання копія переносить оригінал — 🥉.
- Числа теж беруться й ставляться: поставив «1» під стіну — і стіна стала взірцем — 🥈.
- Вкладене керування гравець ⇄ червоний ⇄ синій курсор зі стінами кожного шару — 🥈.
- Зчеплені ящики: рух цілим і падіння, лише коли без опори всі частини — 🥉.
- Падіння без смерті: рух усередині ями, впалі ящики штовхаються — 📎.
- Розвʼязувач: кожне розміщення додає обʼєкт, простір станів росте не лише рухом — 🥇.

## Мапа на каталог
- Є: `move-4dir`, `move-by-input`, `keyboard-controls` · `push-object` + `multi-cell-size` + `stick-together` ↔ зчеплені ящики · `fill-hole` ↔ ящик у ямі · `all-on-targets` · `cursor-place` + `editor-palette` ↔ курсор і палітра · `party-switch` ↔ кілька гравців через курсор · `impassable-cells`, `undo-unlimited`, `restart-level`, `sequential-levels`, `save-progress`, `level-from-txt`, `sound-effects`.
- **Нема** → пропозиції карток:
  - `+nested-editors` «Курсор редактора й мета-курсор як режими гравця» · levels/editor · 🥈 · слоти {layers: 2..3}.
  - `+copy-counter-palette` «Палітра на полі: взірець + лічильник копій» · entities/legality · 🥉.
  - `+placeable-numbers` «Лічильник — теж обʼєкт: створи нову палітру» · entities/interact · 🥈.
  - `+layer-walls` «Стіни, що блокують лише свій шар» · entities/legality · 📎.
  - `+pit-underlayer` «Яма як нижній шар: упав — ходиш там» · entities/move · 📎.
  - `+control-handover` «Передати керування сутності, на якій стоїш» · entities/state · 📎.
  - `+cross-layer-crate` «Ящик у двох шарах одразу» · entities/legality · 🌱.

## Пропозиції до словників
- `+role:cursor` — курсор як сутність поля: штовхає, падає, тримає (тут) — відрізняти від «руки» класу `cursor`.
- `+effect:possess(a)` — керування переходить до сутності A (повтор з інших файлів).
- `+axis:actors` — `party` з шарами: гравці й курсори різних шарів по черзі.
- `+card:nested-editors`, `+card:copy-counter-palette`, `+card:placeable-numbers` — див. вище.

## Джерела
- ⭐ [puzzlescript.net: play](https://www.puzzlescript.net/play.html?p=9eb8f8f3df4efb450b798a279eeba2e0) — гра в браузері.
- [Вихідний код (gist API)](https://api.github.com/gists/9eb8f8f3df4efb450b798a279eeba2e0) — шари `x0` / `x1` / `x2`, примари червоних обʼєктів, `pick up ready icon` / `place mark` / `decrement`, зчеплення `connect cratemark`, падіння з `supported`, перемикання `player -> cursor` / `red -> blue`; умови перемоги `All Target1 on Crateorfell1`, `All target0 on crate0`, `All PlayerTarget1 on Playerormark1`, `no Cursor0 on target1`; 32 сторінки.
- [Bart Bonte](https://www.bontegames.com/2019/07/vext-edit-browser.html) — дата, автор, керування Z/R; коментарі гравців про жовті й червоні стіни, «1» під стіною, найважчу сторінку 8.3.

## Непевне
- (?) Умову перемоги для цілі гравця задовольняє й примара гравця під курсором (`Playerormark1`); коментатор Bonte згадує, що в рівнях із синім курсором наведення на ціль зараховувалось як перемога — схоже на ваду.
- (?) Сторінка 5.3 LOCK містить червоні числа без обʼєкта над ними — роль такого «вільного» числа не перевірена грою.
- (?) Розміри поля взято з тексту рівнів; як PuzzleScript масштабує великі сторінки — не дивився.
