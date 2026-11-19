---
title: Cats Organized Neatly
slug: cats-organized-neatly
aka: []
family: board-digital
also: [pencil-logic]
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2020
platforms: [PC, Switch]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1369340/Cats_Organized_Neatly/", best: true, note: "опис, трейлер, 5 скриншотів: 80 рівнів, 30 котів, ЛКМ/ПКМ, обертання"}
  - {kind: official, url: "https://duandigames.com/our-games/cats-organized-neatly.html", note: "DU&I: «fit cats of all different shapes and sizes into the play area», 80 рівнів"}
  - {kind: steam, url: "https://store.steampowered.com/app/1628050/Cats_Organized_Neatly_Paper_Edition/", note: "Paper Edition: PDF з правилами, 80 рівнями й аркушами котів для вирізання"}
  - {kind: other, url: "https://www.nintendo.com/en-gb/Games/Nintendo-Switch-download-software/Cats-Organized-Neatly-2545536.html", note: "Switch eShop: реліз 04.04.2024, Pro Controller"}
  - {kind: other, url: "https://professionalmoron.com/2021/05/16/cats-organised-neatly/", note: "огляд: поле «(usually) square», мяв при кожному русі"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Cats+Organized+Neatly+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [polyomino-placement, piece-rotate-flip, multi-cell-size, cursor-place, completion-detection, satisfy-constraints, sequential-levels, level-select, game-screen, main-menu, achievements-window, background-music, sound-effects, volume-control, save-progress, +fill-all-cells, +shaped-items, +collect-characters, +printable-edition]
proposes: ["+cond:covers_exactly", "+feature:printable-edition", "+card:exact-tiling"]
author: opus
date: 2026-11-09
---

# Cats Organized Neatly — склади котів-поліміно в кімнату-сітку без накладань, обертаючи їх правою кнопкою

## Суть
Затишний пазл-тайлінг: на кожному з 80 рівнів є область-сітка («(usually) square») і набір котів різних форм — кожен кіт займає кілька клітин, як поліміно. Котів треба взяти, повернути й покласти так, щоб усі вмістились без накладань. Керування — лише ліва (взяти/покласти) і права (повернути) кнопки миші; ворогів, часу й ходів нема. 30 мальованих котів поступово «збираються» в колекцію.

## Поле і час
- Поле — квадратна сітка довільної маски (часто квадрат/прямокутник), окремо — зона з котами рівня.
- Кіт — фігура з клітин сітки (силует намальованого кота), без віддзеркалення (?).
- Статичний пазл (`time: static`): стан = розкладка; перевірки ходів нема, лише «всі вмістились».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кіт | piece | форма (набір клітин), орієнтація 0/90/180/270 | береться ЛКМ, повертається ПКМ, кладеться на вільні клітини |
| Клітина кімнати | static | вільна / зайнята | приймає одну клітину кота |
| Кімната (маска рівня) | zone | форма, розмір | має вмістити всіх котів рівня |
| Запас котів рівня | supply | набір котів | звідси беруть котів; порожній — рівень складено |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(lmb(cat))` → ТО `set_state(cat, held)` (кіт іде за курсором).
- КОЛИ `input(rmb)` → ЯКЩО `state(cat, held)` → ТО `rotate(cat, 90)`.
- КОЛИ `input(lmb(cells))` → ЯКЩО `state(cat, held)` і `fits(cat, cells)` → ТО `place(player, cat)`, `sound(meow)`; інакше `block`.
- КОЛИ `input(lmb(placed_cat))` → ТО `set_state(cat, held)` (кота можна переставити) (?).
- КОЛИ `custom: «усі коти рівня лежать у кімнаті»` → ЯКЩО `cover_all(cat)` (?) → ТО `win`, `next_level`.
- Перемога: усі коти вміщено без накладань · Поразка: нема · Рахунок: нема.

## Керування і ввід
- Лише миша: ЛКМ — взяти/покласти кота, ПКМ — повернути (Steam: «Mouse Only Option», «Touch Only Option»).
- Switch — геймпад (Pro Controller), режими TV/настільний/портативний.

## Вікна, меню, HUD
- `main-menu`: Play, налаштування гучності, вихід.
- `level-select`: 80 рівнів (відкриваються послідовно (?)).
- `game-screen`: кімната-сітка, коти рівня поруч; `drag-ghost` кота під курсором.
- `custom-window` колекції котів (30 «друзів») (?).
- `achievements-window` (Steam, 20 досягнень).
- `settings-window`: гучність музики й звуків (категорія «Custom Volume Controls»).

## Фічі поза полем
- `levels-sequential` 80 ручних рівнів; `collectibles` — 30 котів для колекції.
- `cloud-save` (Steam Cloud, Switch Save Data Cloud), `achievements`, `localization` (23 мови).
- `+feature:printable-edition`: Paper Edition — PDF з правилами, усіма 80 рівнями й аркушами котів (кольоровими й порожніми для розфарбовування) — та сама гра на папері.
- Undo/підказки/редактор — не згадані (?).

## Варіації й родичі
- Серія DU&I з тим самим ядром (кожна — 30 тварин, 80 рівнів, ЛКМ/ПКМ): Dogs Organized Neatly (2021), Birds Organized Neatly (2024, + Daily Puzzle), Cats Organized Neatly 2 (анонс); у кожної є Paper Edition. Сиквели без нових механік — підрозділ нижче, окремих файлів нема.
- Осі варіацій: **перетворення фігури** (лише поворот / поворот + дзеркало — Blokus, Ubongo) · **поле** (точне покриття / з порожніми клітинами) · **набір** (фіксований на рівень / вибір з більшого запасу — Outpacked).
- Родичі в корпусі: `ubongo.md` (вкласти задані поліміно в контур), `iq-puzzler-pro.md`, `pentomino.md`, `daedalian-opus.md` (тайлінг поліміно), `patchwork.md`, `the-isle-of-cats.md` (коти-поліміно на кораблі), `outpacked.md` (пакування з обмеженнями).

### Dogs Organized Neatly (2021) і Birds Organized Neatly (2024) — лише відмінності
- **Dogs** (DU&I, 01.11.2021): те саме ядро — 30 нових собак «у всіх формах і розмірах», 80 нових рівнів, «взяти й покласти на сітку», поворот, лише ліва й права кнопки миші; 20 досягнень, картки Steam, DLC Paper Edition. Нових правил чи елементів поля опис не згадує — окремого файла нема (пачка I007, 2026-11-19).
- **Birds** (DU&I, 16.12.2024): 30 птахів, 80 рівнів і **Daily Puzzle** — «щодня новий пазл» (`daily-puzzle`); решта — як у Cats.
- Steam-категорії всіх трьох однакові (Mouse Only, Touch Only, Steam Cloud, Trading Cards) — схоже, один рушій (?).
- Джерела: [Steam: Dogs](https://store.steampowered.com/app/1597730/Dogs_Organized_Neatly/) · [Steam: Birds](https://store.steampowered.com/app/2707110/Birds_Organized_Neatly/).

## Цікавинки для курсу
- Фігура як множина клітин + поворот на 90° (x, y) → (y, −x) з нормалізацією — 🌱.
- Перевірка «вміщається»: усі клітини фігури всередині маски й вільні — 🌱 (картка `polyomino-placement`).
- Взяти → повернути → покласти однією мишею, привид фігури під курсором — 📎.
- Розвʼязувач точного покриття (backtracking або Algorithm X) і перевірка єдиності розвʼязку рівня — 🥇.
- Рівень як текст: маска + список фігур — 🌱.

## Мапа на каталог
- Є: `polyomino-placement` ↔ коти на сітці; `piece-rotate-flip` (лише поворот) ↔ ПКМ; `multi-cell-size`; `cursor-place`; `completion-detection` + `satisfy-constraints` ↔ усі вмістились; `sequential-levels` + `level-select`; `game-screen`, `main-menu`, `achievements-window`; `background-music` (кото-кавʼярня), `sound-effects` (мяв), `volume-control`, `save-progress`.
- **Нема** → пропозиції карток:
  - `+exact-tiling` «Точне покриття маски набором фігур» · game-logic/win · 📎 (уточнення `+fill-all-cells`).
  - `+collect-characters` «Колекція персонажів, що відкриваються рівнями» · levels/progression · 🌱.
  - `+printable-edition` «Друкована версія рівнів і фігур» · support/docs · 🌱.
  - `+fill-all-cells`, `+shaped-items` — наявні в корпусі теги.

## Пропозиції до словників
- `+cond:covers_exactly` — фігури покривають маску повністю й без накладань.
- `+feature:printable-edition` — друкована версія рівнів (Paper Edition).
- `+card:exact-tiling` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Cats Organized Neatly](https://store.steampowered.com/app/1369340/Cats_Organized_Neatly/) — 2D-пазл, 30 котів, 80 рівнів, ЛКМ/ПКМ, обертання, музика кото-кавʼярні; реліз 12.10.2020, DU&I; JSON appdetails — категорії (Mouse Only, Touch Only), 20 досягнень.
- [DU&I: сторінка гри](https://duandigames.com/our-games/cats-organized-neatly.html) — «fit cats of all different shapes and sizes into the play area».
- [Steam: Paper Edition](https://store.steampowered.com/app/1628050/Cats_Organized_Neatly_Paper_Edition/) — PDF з правилами, 80 рівнів, аркуші котів.
- [Nintendo eShop UK](https://www.nintendo.com/en-gb/Games/Nintendo-Switch-download-software/Cats-Organized-Neatly-2545536.html) — Switch-версія 04.04.2024, «rotate them».
- [Professional Moron](https://professionalmoron.com/2021/05/16/cats-organised-neatly/) — форма поля «(usually) square», коти «at various angles», мяв на кожен рух.
- Steam-сторінки Dogs (2021), Birds (2024, Daily Puzzle), Cats 2 (TBA) — для «Варіацій».

## Непевне
- (?) Чи обовʼязково заповнити **всі** клітини (точне покриття), чи досить вмістити всіх котів — джерела кажуть лише «fit all cats without overlaps».
- (?) Чи є віддзеркалення — у джерелах лише поворот.
- (?) Чи бувають у кімнаті заблоковані клітини/меблі.
- (?) Чи можна переставити вже покладеного кота і чи є кнопка рестарту рівня.
- (?) Як відкриваються рівні й коти колекції (послідовно / за рівнями).
- (?) Рік Switch-версії: Nintendo UK — 2024; один агрегатор каже 2020 — взято офіційну сторінку.
