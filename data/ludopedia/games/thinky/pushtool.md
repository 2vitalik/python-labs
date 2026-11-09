---
title: PushTOOL
slug: pushtool
aka: [Push TOOL]
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2021
platforms: [web]
links:
  - {kind: itch, url: "https://auroriax.itch.io/pushtool", best: true, note: "грати в браузері; правило одним рядком, керування, devlog v5"}
  - {kind: play, url: "https://auroriax.github.io/PuzzleScript/play.html?p=9574acce1d96d07528525b68d09130bb", note: "окремий плеєр PuzzleScriptPlus, v5"}
  - {kind: other, url: "https://auroriax.github.io/PuzzleScript/editor.html?hack=9574acce1d96d07528525b68d09130bb", note: "сирці PuzzleScript (правила, wincondition, назви рівнів)"}
  - {kind: other, url: "https://itch.io/jam/thinky-puzzle-game-jam/rate/1110965", note: "сторінка на Thinky Puzzle Game Jam (2021)"}
  - {kind: other, url: "https://github.com/Auroriax/PuzzleScriptPlus", note: "рушій PuzzleScriptPlus (форк автора, дає level_select)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=PushTOOL+auroriax+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, impassable-cells, undo-unlimited, restart-level, level-select, sequential-levels, sound-effects, +color-group-move, +extrude-numbered-tile, +hollow-block-cells, +cross-color-push, +all-counters-zero]
proposes: ["+effect:extrude", "+effect:retract", "+cond:same_group", "+card:extrude-numbered-tile", "+card:hollow-block-cells", "+card:cross-color-push", "+card:all-counters-zero"]
author: opus
date: 2026-11-09
---

# PushTOOL — Sokoban з мультиблоками, які ростуть: відійди від числа, і блок витягнеться за тобою

## Суть
Покрокова PuzzleScript-головоломка з видом згори. На полі — багатоклітинні блоки двох кольорів (червоні й сині), частина клітин яких несе **число**. Коли гравець відходить від пронумерованої клітини, блок **витягується** на звільнену клітину, а число переїжджає на нову клітину й зменшується на 1. Мета — звести всі числа до 0, тобто «розгорнути» кожен блок на повну довжину. Перешкоди — стіни, інші блоки (червоний штовхає синій і навпаки) і власні **порожнини** блока, у які він не може витягнутись.

## Поле і час
- Квадратна сітка, один екран на рівень, стіни по периметру й усередині.
- Шари (за COLLISIONLAYERS): фон → блоки/стіни → червона порожнина → синя порожнина → гравець → числа й стрілки-сліди → службові маркери.
- Хід = натискання; без вводу нічого не рухається. Відміна ходу (`cancel`) скасовує його цілком, якщо хоч одна клітина блока впирається в стіну.
- Повна інформація, без випадковості.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | 1 клітина | рух 4 напрямки; штовхає блок; відхід від пронумерованої клітини витягує блок |
| Стіна | static | — | непрохідна для гравця й блоків |
| Червоний блок | object | звʼязна група червоних клітин довільної форми | рухається цілою групою; штовхає синій блок |
| Синій блок | object | звʼязна група синіх клітин | те саме, штовхає червоний |
| Число | mark | 0–6, на клітині блока | показує, на скільки клітин ще можна витягти блок із цього місця; рухається разом із блоком |
| Стрілка-слід | mark | напрям (L/R/U/D), на клітині блока | лишається там, звідки число витягли; через неї число можна заштовхнути назад |
| Червона порожнина | zone | напівпрозора, частина червоної групи | рухається разом із червоним блоком; гравець стоїть у ній; червона клітина в неї не заходить; може накладатися на стіну |
| Синя порожнина | zone | те саме для синього | — |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `cell(next, wall)` → ТО `block`.
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(player, dir)`.
- КОЛИ `contact(player, block)` → ТО `push` усієї групи: `custom: «рух поширюється на всі сусідні клітини й порожнини того ж кольору»`; червона клітина, що рухається, штовхає синю, і навпаки (ланцюг через кольори).
- КОЛИ `after(push)` → ЯКЩО `custom: «будь-яка клітина блока впирається в стіну або червона клітина потрапляє на червону порожнину (синя — на синю)»` → ТО `custom: «скасувати весь хід»`.
- КОЛИ `input(dir)` → ЯКЩО `custom: «позаду гравця клітина блока з числом > 0»` and `not state(player, in_same_color_hollow)` → ТО після кроку `extrude`: `spawn_at(block_cell, vacated_cell)`, число переходить на нову клітину з `set_value(n − 1)`, на старій лишається `mark(arrow)`.
- Витягування не відбувається, ЯКЩО звільнена клітина зайнята (гравець, стіна, будь-який блок, порожнина того ж кольору).
- КОЛИ `input(dir)` → ЯКЩО `custom: «гравець відходить від пронумерованої клітини і водночас штовхає ту саму кольорову групу»` → ТО витягування нема, лише `push`.
- КОЛИ `contact(player, number_cell)` → ЯКЩО `custom: «за числом — клітина зі стрілкою, що вказує назад на нього»` → ТО `retract`: пронумерована клітина зникає, число переходить на клітину стрілки з `set_value(n + 1)`, гравець стає на звільнене місце.
- КОЛИ `after(move)` → ЯКЩО `occupied(player_cell, block)` → ТО `custom: «скасувати хід»` (гравця не можна «задавити» блоком).
- КОЛИ `counter(positive_numbers, =, 0)` → ЯКЩО `count(number, >, 0)` → ТО `win`, `next_level`.
- КОЛИ `input(z)` → ТО `custom: «undo одного ходу»`; `input(r)` → `restart`; `input(esc)` → `window(level-select)`.
- Перемога: усі числа на полі дорівнюють 0. · Поразка: нема; глухий кут — undo/restart. · Рахунку нема.

## Керування і ввід
- Стрілки або WASD — крок; Z — undo; R — рестарт; Esc — вибір рівня.
- Окремої кнопки «тягнути» нема: витягування — побічний наслідок кроку від блока, заштовхування числа назад — наслідок кроку в нього.

## Вікна, меню, HUD
- `splash-screen` — титульний екран PuzzleScript «PushTOOL v5 by Tom Hermans [@Auroriax]» зі стартом/продовженням.
- `level-select` (PuzzleScriptPlus, `level_select`): секції 1A–1D, 2A–2D, 3A–3D з назвами (Practice Path … Hollow Hole), Credits і прихована «?. Traffic».
- `game-screen`: поле без HUD; числа на клітинах самі є лічильником решти.
- `custom-window` — текстові повідомлення-перебивки PuzzleScript («Game by Tom Hermans for the Thinky Puzzle Jam (2021)», «The End!»).
- Переходи: splash → game-screen → (усі нулі) наступний рівень; Esc → level-select.

## Фічі поза полем
- `undo` ∞ і `restart-level` (стандарт PuzzleScript); `level-select` з розділами; автозбереження прогресу браузером (?).
- Автор радить пропускати рівні, якщо застряг (вибір рівня відкритий).
- v5 — пост-джемова версія з виправленням крайових випадків штовхання/тягнення чисел; v4 — джемова, лишилася окремим лінком.

## Варіації й родичі
- Сімʼя: [patricks-parabox](patricks-parabox.md) і [recursed](recursed.md) — блоки зі «внутрішнім» простором; [sokobond](sokobond.md) — групи, що злипаються й рухаються разом; [a-good-snowman-is-hard-to-build](a-good-snowman-is-hard-to-build.md) — обʼєкт, що росте від дій гравця; [stephens-sausage-roll](stephens-sausage-roll.md) — багатоклітинні обʼєкти з обмеженнями повороту.
- Поза thinky: BoxBoy! (видавлювання ланцюга клітин від героя), Pushmo (тягнення блоків).
- **Осі варіацій**: як блок змінює розмір — не змінює (Sokoban) / росте від витягування числа (PushTOOL) / видавлюється героєм (BoxBoy); що задає межу росту — число на клітині / бюджет рівня; кольорові групи — один колір / кілька, що штовхають одна одну / злипаються; порожнини — нема / рухомі порожнини всередині блока.

## Цікавинки для курсу
- Рух звʼязної кольорової групи цілком (flood-fill по сусідах того ж кольору, далі перевірка всіх фронтових клітин) — 📎.
- Ланцюговий поштовх через кольори (червоний штовхає синій, той — червоний) з відміною всього ходу при одному упорі — 🥉.
- Витягування числа: клітина народжується позаду гравця, число −1, слід-стрілка; і зворотна операція через стрілку — 🥉.
- Порожнини блока: прохідні для гравця, рухаються з блоком, забороняють своєму кольору — 📎.
- Умова перемоги «усі лічильники нуль» — 🌱.
- Розвʼязувач BFS по станах (форми груп змінюються, стан росте швидко) — 🥇.

## Мапа на каталог
- Є: `move-4dir` + `move-by-input` + `keyboard-controls` ↔ крок; `push-object` ↔ штовхання блоків; `impassable-cells` ↔ стіни; `undo-unlimited` + `restart-level` ↔ Z/R; `level-select` + `sequential-levels` ↔ секції; `sound-effects` ↔ звуки витягування/штовхання.
- **Нема** → пропозиції карток:
  - `+color-group-move` (вже пропонована Lock and Pin) — звʼязна група одного кольору рухається цілком.
  - `+extrude-numbered-tile` «Витягти пронумеровану клітину: блок росте, число −1» · entities/state · 🥉 · слоти {max_n: 6, retract: bool}.
  - `+hollow-block-cells` «Порожнина блока: рухається з ним, прохідна для гравця, заборонена своєму кольору» · entities/legality · 📎.
  - `+cross-color-push` «Групи різних кольорів штовхають одна одну ланцюгом» · entities/legality · 📎.
  - `+all-counters-zero` «Перемога: усі числа на полі звелись до 0» · game-logic/win · 🌱.

## Пропозиції до словників
- `+effect:extrude` — сутність видавлює/витягує нову клітину групи (вже пропоноване для BoxBoy!; тут — від відходу гравця).
- `+effect:retract` — зворотне до `extrude`: клітина групи втягується назад.
- `+cond:same_group` — клітини належать одній звʼязній групі одного кольору (для поширення руху).
- Карткові пропозиції — див. «Мапа на каталог».

## Джерела
- ⭐ [itch.io: PushTOOL](https://auroriax.itch.io/pushtool) — «Enlarge the multiblocks by pulling out the numbered tiles», мета «reduce all the numbers to 0», керування, порада пропускати рівні, devlog v5 (05.07.2021), коментарі.
- [Сирці v5 у редакторі PuzzleScriptPlus](https://auroriax.github.io/PuzzleScript/editor.html?hack=9574acce1d96d07528525b68d09130bb) — OBJECTS/LEGEND/RULES: поширення руху кольором, взаємний поштовх кольорів, маркери витягування, порожнини (RedThrough/BlueThrough), WINCONDITIONS `No PosNumber / Some Number`, назви секцій; gist створено 05.07.2021.
- [Окремий плеєр v5](https://auroriax.github.io/PuzzleScript/play.html?p=9574acce1d96d07528525b68d09130bb) — гра.
- [Сторінка на Thinky Puzzle Game Jam](https://itch.io/jam/thinky-puzzle-game-jam/rate/1110965) — джемова подача.
- [PuzzleScriptPlus](https://github.com/Auroriax/PuzzleScriptPlus) — форк рушія.

## Непевне
- (?) Кількість рівнів: 12 названих секцій + прихована «?. Traffic»; чи в секції по одному рівню — з сирців не порахував надійно.
- (?) Назву «порожнина» дав я: у коді обʼєкти звуться RedThrough/BlueThrough (напівпрозорі); що вони рухаються з блоком і не перекриваються своїм кольором — прочитано з правил, у грі не перевірено.
- (?) Максимум числа 6 — за набором спрайтів One…Six; чи бувають числа > 6 у рівнях — ні.
- (?) Збереження прогресу між сесіями — стандарт PuzzleScript (localStorage), не перевірено.
