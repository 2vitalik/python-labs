---
title: Patrick's Parabox
slug: patricks-parabox
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: graph
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2022
platforms: [PC, Switch, PS5]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Patrick%27s_Parabox", best: true, note: "суть: Sokoban, де ящики містять рівні; вхід/вихід, самовкладення, умова перемоги, 364 рівні"}
  - {kind: official, url: "https://www.patricksparabox.com/", note: "офіційний сайт: boxes within boxes, нескінченність"}
  - {kind: steam, url: "https://store.steampowered.com/app/1260520/Patricks_Parabox/", note: "350+ рівнів, досягнення, Steam Cloud"}
  - {kind: other, url: "https://www.gamedeveloper.com/disciplines/road-to-the-igf-patrick-traynor-s-i-patrick-s-parabox-i-", note: "інтервʼю: shrink/grow між шарами, ідея з Sokosoko (juner), крайові випадки рекурсії"}
  - {kind: other, url: "https://igf.com/Patricks-Parabox", note: "сторінка IGF (Excellence in Design 2020)"}
  - {kind: other, url: "https://thinkygames.com/games/patricks-parabox/", note: "Thinky Games — картка гри"}
  - {kind: other, url: "https://parallax.bearblog.dev/review-patricks-parabox/", note: "рецензія: epsilon-простір, infinity як плитка, Appendix-світи"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=patrick%27s+parabox+gameplay", note: "пошук; геймплей і доповідь розробника"}
stage: v1
coverage: 60
mechanics: [move-4dir, keyboard-controls, push-object, impassable-cells, all-on-targets, sequential-levels, level-unlock, level-select, save-progress, movement-animation, player-camera, field-scaling, +undo-redo, +recursive-boxes, +enter-box, +box-eat, +box-clone, +infinity-box, +epsilon-box, +flip-box, +multi-player-sync, +world-map]
proposes: ["+trigger:input", "+trigger:paradox", "+cond:free", "+cond:has_opening", "+effect:enter", "+effect:exit", "+effect:mirror", "+effect:move", "+role:container", "+window:map-window", "+feature:undo", "+feature:world-map", "+axis:field-nested", "+axis:undo"]
author: opus
date: 2026-11-02
---

# Patrick's Parabox — Sokoban, де ящики містять рівні, а рівень може містити сам себе

## Суть
Гравець — сам ящик, що штовхає інші ящики до цілей, як у Sokoban. Але частина ящиків порожниста: всередині кожного — повноцінна сітка, і в неї можна **увійти** (зменшившись) або вштовхнути інший ящик; вийти за край внутрішньої сітки — означає опинитися в батьківському рівні поруч із ящиком. Ящик може містити копію самого себе, тож вихід «назовні» і вхід «усередину» стають нескінченними — гра робить із цього окремі механіки (∞-ящик, ε-ящик). Ядро — рекурсивна топологія поля, де «сусідня клітина» залежить від вкладення.

## Поле і час
- Кожен рівень — дерево (або граф із циклами) квадратних сіток: корінь і ящики-підрівні, кожен зі своєю сіткою (розміри різні, типово 5×5…9×9) і отворами в стінах по краях.
- Сусідство нестандартне: крок за край внутрішньої сітки веде в клітину батьківської сітки біля ящика; крок у ящик з отвором — у крайову клітину його сітки (позиція по краю — пропорційно точці входу (?)).
- Камера зумить на сітку, де стоїть гравець; батьківські рівні видно довкола, вкладені — мініатюрами всередині ящиків (рендер рекурсивний до певної глибини).
- Покроково: хід = один крок усіх гравців-ящиків; без часу й випадковості.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | ящик з очима; може бути порожнистим | крок у 4 напрямки; штовхає, входить, виходить; кілька гравців ходять синхронно |
| Суцільний ящик | object | — | штовхається на 1 (ланцюгом), можна вштовхнути в порожнистий ящик |
| Порожнистий ящик (рівень) | container | своя сітка, отвори по краях, колір | штовхається як ящик; у нього входять через отвір; вміст рухається разом із ним |
| Стіна | static | — | непрохідна в межах своєї сітки |
| Ціль ящика | static | контур | має бути накрита будь-яким ящиком |
| Ціль гравця | static | контур з обличчям | має бути зайнята гравцем |
| Клон (reference) | container | посилання на ту саму сітку; один — оригінал | вигляд і вміст спільні з оригіналом; вихід зсередини веде до оригіналу (?) |
| Самовкладений ящик | container | містить себе | вхід/вихід через нього не закінчуються — породжує ∞ і ε |
| ∞-ящик (infinity) | container | порядок нескінченності | «рівень над собою»: куди потрапляє той, хто виходить із самовкладеного ящика нескінченно (?) |
| ε-ящик (epsilon) | container | — | «рівень усередині себе»: куди потрапляє той, хто входить у самовкладений ящик нескінченно (?) |
| Віддзеркалений ящик (flip) | container | дзеркало по горизонталі | сітка всередині дзеркальна; напрямок «ліво/право» при вході/виході міняється |
| Possess-ящик | container | — | гравець може «вселитися» і керувати іншим ящиком (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО для кожного гравця `move(player, dir)` за правилами нижче (синхронно).
- КОЛИ `contact(a, wall)` → ТО `block`.
- КОЛИ `contact(a, box)` → ЯКЩО `free(cell_behind)` по всьому ланцюгу → ТО `push` (ланцюг ящиків).
- КОЛИ `contact(a, box)` і `push` неможливий → ЯКЩО `has_opening(box, side)` і клітина входу вільна → ТО `enter(a, box)` (a зменшується і стає в крайову клітину сітки box).
- КОЛИ `contact(a, box)`, ні `push`, ні `enter` неможливі → ЯКЩО `has_opening(a, side)` (a — порожнистий) → ТО `custom: «eat — box входить усередину a»` (?).
- КОЛИ `edge(a)` усередині сітки ящика B → ТО `exit(a)`: a збільшується і стає в клітину батьківської сітки біля B з того ж боку; там знову діють push/enter/eat.
- КОЛИ ящик штовхають усередині власної сітки за край (вихід із себе) → ТО `custom: «потрапляє в ∞-рівень»`; КОЛИ входить у себе нескінченно → ТО `custom: «потрапляє в ε-рівень»` (?).
- КОЛИ `enter|exit` через flip-ящик → ТО `mirror(dir)` для лівого/правого.
- КОЛИ `paradox` (рух веде в цикл без розвʼязку) → ТО `block` або перехід у ∞/ε — залежно від глави (?).
- КОЛИ `all_on(box, box_goal)` і `all_on(player, player_goal)` → ТО `win`, повернення в хаб.
- Поразки нема: глухий кут лікується undo/restart. Рахунку нема.

## Керування і ввід
- Стрілки/WASD — крок (усі гравці одночасно).
- Z — undo без ліміту; R — рестарт (скасовується undo) (?); Esc — меню.
- Геймпад; на Switch/PS5 — стік/хрестовина.

## Вікна, меню, HUD
- `splash-screen` / `main-menu` — Continue · Settings · Quit (?).
- `map-window` — хаб: області (глави), рівні як ящики-вузли; щоб відкрити наступну область, треба пройти частину рівнів поточної; необовʼязкові бічні рівні.
- `game-screen` — рівень на весь екран з рекурсивним рендером; назва рівня; HUD мінімальний (підказки клавіш undo/restart).
- `pause-menu` — повернутись, рестарт, у хаб, налаштування.
- `settings-window` — гучність, повноекранний режим, мова (10 мов), керування (?).
- Переходи: main-menu → map-window → (вузол) game-screen → (усі цілі) map-window; після фіналу — Appendix-світи з іншими правилами.

## Фічі поза полем
- `undo` ∞ + `restart-level`; `autosave` прогресу (Steam Cloud); `achievements`.
- `world-map` (хаб із главами) + `level-unlock` за кількістю пройдених; основний шлях + бічні рівні; post-game «Appendix» змінює правила.
- `localization` (10 мов); музика Priscilla Snow реагує на нові механіки.
- Редактора рівнів у грі — не підтверджено (?).

## Варіації й родичі
- Предок — Sokosoko (juner): ящик, що містить себе; Recursed (кімнати в скринях), Sokoban.
- Глави (назви з памʼяті, ?): Enter, Empty, Eat, Reference/Clone, Center, Transfer, Open, Flip, Cycle, Swap, Player, Possess, Wall, Infinite Exit, Infinite Enter, Multi Infinite, Appendix.
- **Осі варіацій:** вкладення — немає / дерево / самовкладення / граф клонів; що при блокуванні — нічого / enter / eat; кілька гравців — один / синхронні копії; орієнтація всередині — та сама / дзеркальна.

## Цікавинки для курсу
- Поле як дерево сіток: «сусідня клітина» через вхід/вихід ящика — 🥇 (структура даних + рекурсивна функція переходу).
- Порядок спроб при блокуванні: push → enter → eat — 🥈 (рекурсія з відкатом).
- Рекурсивний рендер «ящик у ящику» до глибини N — 🥈 (графіка, обмеження глибини).
- Клон як посилання на спільну сітку (aliasing) — 🥈: добре пояснює посилання vs копію в Python.
- Самовкладення і виявлення циклу (∞/ε) — 👑 як повна механіка; 🥇 за просте «виявити цикл і заблокувати хід».
- Кілька синхронних гравців — 📎.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ крок; `push-object` ↔ ланцюг ящиків; `impassable-cells` ↔ стіни; `all-on-targets` ↔ цілі ящиків і гравця; `sequential-levels` + `level-unlock` + `level-select` + `save-progress` ↔ хаб; `movement-animation` ↔ анімація shrink/grow; `player-camera` + `field-scaling` ↔ зум на поточну сітку.
- **Нема** → пропозиції карток:
  - `+undo-redo` «Undo ходів у грі» · game-logic/flow · 📎.
  - `+recursive-boxes` «Ящик містить сітку-рівень» · entities/state · 🥇 — батько сімʼї нижче.
  - `+enter-box` «Вхід у ящик / вихід за край» · entities/move · 🥈 — дитина `recursive-boxes`.
  - `+box-eat` «Ящик поглинає перешкоду» · entities/legality · 🥉.
  - `+box-clone` «Клон — посилання на ту саму сітку» · entities/state · 🥈.
  - `+infinity-box` «Нескінченний вихід (∞)» · entities/state · 👑.
  - `+epsilon-box` «Нескінченний вхід (ε)» · entities/state · 👑.
  - `+flip-box` «Дзеркальна сітка» · entities/state · 🥉.
  - `+multi-player-sync` «Кілька аватарів ходять одночасно» · entities/move · 📎 — і в Baba Is You (кілька YOU).
  - `+world-map` «Мапа/хаб із вузлами-рівнями» · levels/progression · 🥉.

## Пропозиції до словників
- `+trigger:input`; `+trigger:paradox` — рух породжує нескінченний цикл переходів.
- `+cond:free`; `+cond:has_opening(box, side)` — у стіні ящика є отвір з цього боку.
- `+effect:enter(a, box)` / `+effect:exit(a)` — зміна рівня вкладення сутності (не те саме, що `teleport`: зберігається напрямок і масштаб).
- `+effect:mirror(dir)` — дзеркальне відображення напрямку (flip).
- `+effect:move` — кандидат, основний.
- `+role:container` — порожнистий ящик-рівень (кандидат ⏳, тут центральний).
- `+window:map-window`, `+feature:undo`, `+feature:world-map`.
- `+axis:field-nested` — нове значення осі `field`: `nested` (сітки вкладені одна в одну, можливо циклічно); зараз записано як `graph`.
- `+axis:undo` — `unlimited`.

## Джерела
- ⭐ [Wikipedia: Patrick's Parabox](https://en.wikipedia.org/wiki/Patrick%27s_Parabox) — вхід/вихід із ящиків, самовкладення й парадокси, умова перемоги, 364 рівні, хаб із бічними рівнями, дати.
- [Офіційний сайт](https://www.patricksparabox.com/) — «boxes within boxes», нескінченність.
- [Steam](https://store.steampowered.com/app/1260520/Patricks_Parabox/) — 350+ рівнів, досягнення, 10 мов.
- [Game Developer: Road to the IGF](https://www.gamedeveloper.com/disciplines/road-to-the-igf-patrick-traynor-s-i-patrick-s-parabox-i-) — shrink/grow, Sokosoko як джерело, крайові випадки (ящик із двома копіями себе).
- [Рецензія parallax](https://parallax.bearblog.dev/review-patricks-parabox/) — epsilon-простір, «infinity як плитка», Appendix.
- [Thinky Games](https://thinkygames.com/games/patricks-parabox/) · [IGF](https://igf.com/Patricks-Parabox).
- YouTube: [пошук «patrick's parabox gameplay»](https://www.youtube.com/results?search_query=patrick%27s+parabox+gameplay).

## Непевне
- (?) Механіки eat, clone (хто «оригінал» для виходу), possess, flip, ∞/ε — описані з памʼяті; джерела лише згадують epsilon і infinity без правил.
- (?) Точний порядок push → enter → eat і як обирається клітина входу для сіток різного розміру.
- (?) Перелік і назви глав.
- (?) Наявність вбудованого редактора рівнів — не знайдено в джерелах.
- (?) Клавіші undo/restart і пункти меню — з памʼяті.
