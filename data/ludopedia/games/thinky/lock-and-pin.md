---
title: Lock & Pin
slug: lock-and-pin
aka: [Lock and Pin, locknpin]
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
year: 2023
platforms: [web]
links:
  - {kind: itch, url: "https://clickmazes.itch.io/locknpin", best: true, note: "грати в браузері; керування з клавіатури й тачу, 8 рівнів, Thinky Puzzle Game Jam 3"}
  - {kind: other, url: "https://api.github.com/gists/11118b5d6e0d22b5bfc26f3043c888db", note: "вихідний код PuzzleScript (gist): кольорові блоки, тунелі, замки, шпильки"}
  - {kind: other, url: "https://www.puzzlescript.net/editor.html?hack=11118b5d6e0d22b5bfc26f3043c888db", note: "код у редакторі PuzzleScript"}
  - {kind: other, url: "https://itch.io/jam/thinky-puzzle-game-jam-3", note: "джем, тема «chalk and cheese»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Lock+%26+Pin+clickmazes+puzzlescript", note: "пошук; проходження"}
stage: v1
coverage: 65
mechanics: [move-4dir, move-by-input, push-object, multi-cell-size, impassable-cells, one-way-cell, all-on-targets, undo-unlimited, restart-level, sequential-levels, keyboard-controls, swipe-gestures, sound-effects, +color-group-move, +directional-lock, +pass-through-tunnel]
proposes: ["+card:color-group-move", "+card:directional-lock", "+card:pass-through-tunnel", "+window:title-screen", "+window:message-screen"]
author: opus
date: 2026-11-09
---

# Lock & Pin — штовхнеш один кольоровий шматок — рушать усі того ж кольору; замок насаджується на шпильку лише зі свого боку

## Суть
Sokoban від Andrea Gilbert (clickmazes) на тему «chalk and cheese»: «обʼєкти, що схожі на вигляд, поводяться однаково й мають спільну мету». Кожен колір — одне розкидане по полю тіло: штовхнув будь-яку частину — усі частини цього кольору зсуваються на клітину разом. Частини бувають трьох видів: суцільні (впираються в шпильки), тунелі (проходять над шпильками й пускають гравця всередину) і замки, які мають «сісти» на нерухомі шпильки. Замок кожного кольору сідає на шпильку лише в одному напрямку руху: червоний — рухаючись ліворуч, синій — униз, зелений — праворуч.

## Поле і час
- Квадратна сітка, один екран на рівень; 8 рівнів.
- Шари колізій (з коду): фон → усі кольорові блоки (`blockX`) → стіна / гравець / шпилька → анімація → маркер `ok`.
- Гравець і шпильки — в іншому шарі, ніж блоки: тому гравець може стояти в тунелі, а шпилька — сидіти в тунелі чи замку.
- Покроково: тік = ввід; службові маркери `ouch` (скасувати рух) і `ok` (законний вхід шпильки) живуть один хід.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець (`Player`) | player | — | крок 4 напрямки; штовхає суцільні блоки й замки; заходить у тунелі; не заходить на шпильку |
| Суцільний блок (`SolidA/B/C`) | object | колір A/B/C (червоний / синій / зелений) | рушає разом з усіма блоками свого кольору; не їде на шпильку |
| Тунель (`TunnelA/B/C`) | object | колір | частина кольорового тіла; гравець ходить крізь нього, шпилька проходить крізь нього |
| Замок (`lockA/B/C`) | object | колір → напрямок входу | частина кольорового тіла; сідає на шпильку лише в напрямку свого кольору, знімається лише назад |
| Шпилька (`pin`) | static | — | нерухома; ціль для замка; перешкода для суцільних блоків і гравця |
| Стіна (`wall`) | static | — | непрохідна для гравця й блоків |
| `ouch` / `ok` | mark | — | службові: «рух заборонено» / «шпилька входить законно» |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell_ahead)` → ТО `move(player, dir)`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(cell_ahead, tunnel)` → ТО `move(player, dir)` — гравець заходить у тунель будь-якого кольору, нічого не штовхаючи.
- КОЛИ `contact(player, pin)` → ТО `block`, `sound(ouch)`.
- КОЛИ `contact(player, block_X)` → ТО `push`, `custom: «усі блоки кольору X на полі рушають у тому ж напрямку»`.
- КОЛИ `custom: «блок кольору X рушає в клітину з блоком іншого кольору або стіною»` → ТО `block` — усього ходу.
- КОЛИ `custom: «суцільний блок рушає на шпильку»` → ТО `block`, `sound(ouch)`.
- КОЛИ `custom: «тунель рушає на шпильку»` → ТО `move` — шпилька опиняється всередині тунелю.
- КОЛИ `custom: «червоний замок рушає на шпильку»` → ЯКЩО `moving(lock, left)` → ТО `custom: «поставити ok — шпилька входить»`; інакше `block`, `sound(ouch)`.
- КОЛИ `custom: «синій замок рушає на шпильку»` → ЯКЩО `moving(lock, down)` → ТО `custom: «ok»`; інакше `block`.
- КОЛИ `custom: «зелений замок рушає на шпильку»` → ЯКЩО `moving(lock, right)` → ТО `custom: «ok»`; інакше `block`.
- КОЛИ `custom: «замок, що сидить на шпильці, рушає»` → ЯКЩО `custom: «рух протилежний напрямку входу (червоний — праворуч, синій — угору, зелений — ліворуч)»` → ТО `move` — замок знімається; інакше `block`.
- КОЛИ `custom: «будь-де поставлено ouch»` → ТО `block` — увесь хід скасовано (кольорове тіло рухається цілим або ніяк).
- КОЛИ `custom: «шпилька сидить у замку»` → ТО `sound(click)`.
- КОЛИ `all_on(pin, lock)` → ЯКЩО `custom: «кожен замок на шпильці і анімація завершена»` → ТО `win`, `next_level` (умови коду: «no anim», «all pin on lock», «all lock on pin»).
- Перемога: кожна шпилька в замку й кожен замок на шпильці · Поразки нема · Рахунку нема.

## Керування і ввід
- Клавіатура: стрілки / WASD — крок або поштовх; `Z` — undo; `R` — рестарт.
- Тач: тап у головному меню, свайп — рух, меню-вкладка вгорі ліворуч — undo / restart.

## Вікна, меню, HUD
- `title-screen` (custom, стандарт PuzzleScript): назва, автор; на тачі — тап для старту.
- `game-screen`: поле без HUD; на мобільному — вкладка-меню з undo / restart (`undo-button`, `restart-button`).
- `message-screen` (custom): «Engage all pins in locks» на старті, фінал «Thank you for playing :)».
- Переходи: title → 8 рівнів підряд → фінал.

## Фічі поза полем
- `undo` ∞, `restart-level`, `touch-controls` (свайпи) поруч з клавіатурою.
- `levels-sequential`: 8 рівнів, ~30 хв гри (за сторінкою).
- Відкритий код (hack у редакторі PuzzleScript).

## Варіації й родичі
- Родичі в корпусі: [Sokoban](../push-slide/sokoban.md); [Rush Hour](../push-slide/rush-hour.md) і [Klotski](../push-slide/klotski.md) (багатоклітинні тіла); [Jelly no Puzzle](jelly-no-puzzle.md) (однаковий колір = одне тіло, але лише при дотику); [Baba Is You](baba-is-you.md) (усі обʼєкти одного типу поводяться однаково).
- Інші ігри автора — сайт clickmazes.com (механічні лабіринти й пазли).
- Осі варіацій: **що звʼязує частини** — дотик (Jelly) / колір на відстані (тут) / ланцюг; **проникність для шпильки** — суцільне / тунель / замок зі стороною; **напрямок входу** — будь-який / за кольором (тут) / за орієнтацією обʼєкта.

## Цікавинки для курсу
- Рух «усіх одного кольору» одним поштовхом з атомарним скасуванням, якщо хоч одна частина впирається, — 🥉.
- Три види частин з різною проникністю для шпильок (суцільне / тунель / замок) — таблиця взаємодій — 📎.
- Замок, що приймає шпильку лише з одного боку й відпускає лише назад, — 📎 (умова на напрямок руху).
- Два шари на клітині: гравець і шпилька всередині тунелю, блоки — окремо — 📎.
- Розвʼязувач: стан = зсуви трьох кольорових тіл + позиція гравця — 🥈 (малий простір, ідеальний для BFS).

## Мапа на каталог
- Є: `move-4dir` · `move-by-input` · `push-object` · `multi-cell-size` (розкидане кольорове тіло) · `impassable-cells` · `one-way-cell` (найближче до замка з одним напрямком входу) · `all-on-targets` · `undo-unlimited` · `restart-level` · `sequential-levels` · `keyboard-controls` · `swipe-gestures` · `sound-effects`.
- **Нема** → пропозиції карток:
  - `+color-group-move` «Поштовх однієї частини рухає всі частини того ж кольору» · entities/move · 🥉 · слоти {link: color|touch}.
  - `+directional-lock` «Замок сідає на шпильку лише з одного напрямку» · entities/legality · 📎 · слот {dir_by: color|orientation}.
  - `+pass-through-tunnel` «Частина тіла, прозора для гравця й шпильок» · entities/legality · 🌱.

## Пропозиції до словників
- `+card:color-group-move`, `+card:directional-lock`, `+card:pass-through-tunnel` — див. вище.
- `+window:title-screen`, `+window:message-screen` — повтор (Mirror Isles).
- ⏳-слова, вжиті тут: `input`, `free`, `occupied`, `moving`, `move`, `sound`, `all_on`, `next_level`.

## Джерела
- ⭐ [Сторінка на itch.io](https://clickmazes.itch.io/locknpin) — гра, опис теми, керування (клавіатура + тач), 8 рівнів, ~30 хв, червень 2023, коментарі гравців про напрямки кольорів.
- [Gist з кодом через GitHub API](https://api.github.com/gists/11118b5d6e0d22b5bfc26f3043c888db) — автор Andrea Gilbert, обʼєкти, шари, правила (поштовх кольорового тіла, тунелі, `ouch`, напрямки замків), умови перемоги, повідомлення.
- [Thinky Puzzle Game Jam 3](https://itch.io/jam/thinky-puzzle-game-jam-3) — джем і тема.

## Непевне
- (?) Відповідність A/B/C ↔ червоний/синій/зелений — з опису фетчу коду й коментарів гравців («blue always down», «red always left, green always right»); кольори спрайтів не перевірені.
- (?) Що стається з гравцем, що стоїть у тунелі, коли тіло цього кольору зсувається, — правила цього не описують; за шарами гравець, найпевніше, лишається на місці.
- (?) Чи блок може наїхати на гравця (гравець в іншому шарі колізій) — у правилах заборони не знайдено.
- (?) Черга дала рік 2025 — сторінка каже червень 2023 (Thinky Puzzle Game Jam 3).
