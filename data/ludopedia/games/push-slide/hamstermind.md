---
title: HAMSTERMIND
slug: hamstermind
aka: [Hamstermind, "Hamster Jones"]
family: push-slide
also: [connect-rotate, thinky]
klass: hybrid
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: collect
year: 2026
platforms: [PC, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3555520/HAMSTERMIND/", best: true, note: "опис: «every room can be rotated», необовʼязкові й таємні пазли, журнал, 37 досягнень; трейлер і відео механік"}
  - {kind: other, url: "https://www.player2.net.au/2026/02/hamstermind-review-this-hamster-is-a-dark-horse/", note: "огляд: сітка 2×2 у кімнаті, світлові частинки, статуї блокують обертання поглядом, лазери, блоки; бокові пазли з ящиком, що обертається на 90°"}
  - {kind: other, url: "https://questdaily.com.au/review/review-hamstermind-tiny-paws-tough-puzzles-pc/", note: "огляд: чотири квадранти-«кімнати» обертаються, щоб вирівняти шляхи до сфер; скарабеї в клітках; коди скринь і журнал"}
  - {kind: other, url: "https://gamingfurever.com/news/reviews/hamstermind-a-sandy-yet-satisfying-puzzle-game", note: "огляд: Tournesol обертає секції підлоги, горгульї, блоки, клітки зі скарабеєм/скорпіоном/коброю, дрон-руйнівник стін"}
  - {kind: other, url: "https://steamcommunity.com/app/3555520/reviews/?browsefilter=toprated", note: "відгуки: 5 типів пазлів — обертання кімнат (обовʼязкові), дрон на сітці, ящик з гравітацією, декодування, загадки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=HAMSTERMIND+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 35
mechanics: [move-4dir, tile-rotate, collect-all, push-object, line-of-sight-attack, beam-tracing, gravity-fall, undo-step, restart-level, codex-window, achievements-window, +room-rotate, +rotate-only-occupied, +gaze-lock, +tilt-box, +drone-path-plan, +code-chest, +journal-clues, +cosmetic-unlock]
proposes: ["+cond:watched(a, by)", "+effect:rotate_room(section, deg)", "+window:journal", "+feature:cosmetic-outfits", "+card:room-rotate"]
author: opus
date: 2026-11-09
---

# HAMSTERMIND — хом'як-археолог обертає квадранти підлоги піраміди, щоб вирівняти шляхи до світлових сфер

## Суть
3D-пригода-головоломка французької студії Righteous Tree: Хамстер Джонс досліджує піраміду Charaon кімната за кімнатою. Головний пазл кожної кімнати — підлога, поділена на сітку 2×2 секцій: артефакт Tournesol повертає секцію на 90°, і коридори на сусідніх секціях стикуються по-новому; треба зібрати всі світлові сфери, щоб відкрити наступну кімнату. Поруч — бокові пазли (ящик-клітка, який обертають, і блоки падають; дрон на сітці; коди скринь), а над усім — мета-загадки з журналу. Клас `hybrid`: аватар ходить сам, але ядро — обертання й зсув частин поля.

## Поле і час
- Кімната = квадрат 2×2 секцій із коридорами-канавками; секція обертається навколо свого центру разом із вмістом. Сторонній опис згадує ще й зсув кімнат у порожні місця (?).
- Хамстер ходить у 3D, вид згори; для пазлів час не тисне («Playable without Timed Input»), стан змінюють лише дії гравця.
- Бокові пазли — окремі малі сітки: ящик-клітка (≈6×6 (?)) з камерою згори, павутина-граф, панелі символів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Хамстер Джонс | player | — | ходить коридорами; Tournesol обертає секцію |
| Секція підлоги («кімната») | tile | орієнтація 0/90/180/270 | обертається на 90°; коридори стикуються або перекриваються |
| Світлова сфера | pickup | кілька на кімнату | зібрати всі → відкривається прохід |
| Горгулья / статуя | hazard | напрям погляду | поки бачить Хамстера, обертати не можна; треба вийти з поля зору |
| Лазер | static | напрям | промінь треба навести на ціль, щоб відкрити шлях |
| Блок | object | — | у пізніх кімнатах штовхається (тягнення — (?)) |
| Ящик-клітка зі скарабеєм | zone | сітка, стінки | обертається на 90° за/проти годинникової; блоки падають донизу |
| Блок-тварина (скарабей, скорпіон, кобра) | object | символ | має впасти в лунку зі своїм символом; кобра може «випадково» впасти не туди |
| Жук-вентилятор | hazard | напрям | дме вітром у клітці (?) |
| Дрон-комаха | ally | запланований шлях | проходить по сітці через «вразливі місця» стіни й руйнує її |
| Скриня з кодом | gate | багатоцифровий код | відкривається кодом, виведеним з підказок |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(rotate_left | rotate_right)` → ЯКЩО `custom: «Хамстер стоїть на цій секції»` (?) and not `line_of_sight(gargoyle, player)` → ТО `rotate(section, ±90)` разом з усім на ній.
- КОЛИ `input(rotate)` → ЯКЩО `line_of_sight(gargoyle, player)` → ТО `block`.
- КОЛИ `input(dir)` → ЯКЩО `custom: «коридор продовжується на сусідню секцію»` → ТО `move(player, dir)`; інакше `block`.
- КОЛИ `enter(player, sphere)` → ТО `pickup`, `counter(spheres, +1)`.
- КОЛИ `all_gone(sphere)` → ТО `custom: «відкрити прохід у наступну кімнату»`.
- КОЛИ `contact(player, block)` → ЯКЩО `free(cell_behind)` → ТО `push`.
- КОЛИ `custom: «промінь лазера влучив у ціль»` → ТО `custom: «відкрити шлях»`.
- Клітка: КОЛИ `input(rotate_box, ±90)` → ТО `rotate(box, ±90)`, `fall(blocks)` до упору.
- Клітка: КОЛИ `enter(animal_block, same_symbol_hole)` → ТО `win` (скарабей вільний → нове вбрання).
- Дрон: КОЛИ `custom: «запущено запланований шлях»` → ТО `move(drone, path)`; КОЛИ `enter(drone, weak_spot)` → ТО `custom: «зруйнувати слабке місце стіни»`.
- Скриня: КОЛИ `input(code)` → ЯКЩО `custom: «код збігся»` → ТО `custom: «скриня відкрита, нагорода»`.
- Перемога: усі сфери кімнати зібрано (головні пазли); фінал гри — за обовʼязковими пазлами. · Поразка: нема; undo / reset. · Рахунок: нема; прогрес — кімнати, скарабеї, коди.

## Керування і ввід
- Геймпад рекомендований (повна підтримка, DualShock/DualSense); є варіант лише клавіатура.
- Клітка: кнопки «Rotate Left», «Rotate Right», «Undo», «Reset» і «Back» підписані на екрані (скриншот Steam).
- Панель символів: «Move», «Select», «Erase», «Reset», Q/E «Change Weight» (скриншот).

## Вікна, меню, HUD
- `splash-screen` / `dialogue-window` — мальований вступний ролик з озвученням, діалоги персонажів-портретами.
- `game-screen` — піраміда згори, кімната 2×2; окремі екрани-пазли (клітка, павутина-граф, панель символів, кодова скриня) з підказками кнопок.
- `codex-window` / `+window:journal` — блокнот Хамстера з вкладками: зібрані підказки, правила міні-ігор («Catsparov's Game»).
- `achievements-window` — Steam (37).
- Переходи: кімната → (усі сфери) → наступна кімната; бокові пазли й скрині — з кімнати; журнал — будь-коли.

## Фічі поза полем
- Необовʼязкові пазли й таємні кімнати; мета-код зі шматків по всій піраміді.
- Підказки для частини бокових пазлів (не для головних), відкриваються боковими пазлами.
- Вбрання (`unlockables`): скарабеї з кліток дають косметику й дрібні ігрові бонуси.
- Пост-гра з новими механіками; «Mastermind»-складність пізніх кімнат.
- `autosave` / «Save Anytime», `cloud-save`, 10 мов.

## Варіації й родичі
- [kwirk](kwirk.md) — турнікет, що обертається від поштовху; [paper-mario-the-origami-king](paper-mario-the-origami-king.md) — обертання кілець поля; [klotski](klotski.md) — зсув блоків; [aoc-2023-parabolic-reflector-dish](aoc-2023-parabolic-reflector-dish.md) і [ice-sliding-puzzles](ice-sliding-puzzles.md) — нахил/ковзання як у клітці; [rpg-dungeon-puzzle-rooms](rpg-dungeon-puzzle-rooms.md) — кімнати-пазли в пригоді; [board-digital/labyrinth](../board-digital/labyrinth.md) і [connect-rotate/infinity-loop](../connect-rotate/infinity-loop.md) — вирівнювання шляхів обертанням плиток; [chess-abstract/hexapawn](../chess-abstract/hexapawn.md) — родич міні-гри «Catsparov's Game» (3×3, по три фігури, перейти на інший бік).
- Осі варіацій: **що обертається** (плитка-шлях / секція з аватаром на ній / уся коробка з гравітацією); **хто може обертати** (будь-яку / лише ту, де стоїш / лише поза поглядом статуї); **мета** (зʼєднати шлях / зібрати все / довести блок у лунку).

## Цікавинки для курсу
- Секція 2×2, що обертається разом із вмістом (координати клітин і стін на 90°) — 🥉.
- «Обертати лише свою секцію» + блокування поглядом горгульї (line of sight після повороту) — 🥉.
- Клітка: поворот ящика = зміна напрямку гравітації, блоки падають до упору — 📎 (та сама задача, що нахил у AoC 2023/14).
- Дрон з планованим шляхом, що руйнує «вразливі місця» — 🥉 (місток до `program-robots`).
- Скриня з кодом і журнал підказок — 🌱.
- Розвʼязувач головного пазла (BFS по орієнтаціях 4 секцій × позиція Хамстера × зібрані сфери) — 🥈.

## Мапа на каталог
- Є: `move-4dir` ↔ ходіння коридорами; `tile-rotate` ↔ секція з орієнтацією; `collect-all` ↔ усі сфери; `push-object` ↔ блоки пізніх кімнат; `line-of-sight-attack` ↔ горгульї, що «ловлять» поглядом (тут блокують, а не бʼють); `beam-tracing` ↔ лазери; `gravity-fall` ↔ блоки в клітці; `undo-step` + `restart-level` ↔ Undo/Reset у клітці; `codex-window` ↔ журнал; `achievements-window`.
- **Нема** → пропозиції карток:
  - `+room-rotate` «Поворот секції поля разом з аватаром і вмістом» · entities/state · 🥉 · слот {section: 2×2}.
  - `+rotate-only-occupied` «Обертати можна лише секцію під аватаром» · entities/legality · 🌱.
  - `+gaze-lock` «Дія заборонена, поки спостерігач бачить гравця» · entities/legality · 📎.
  - `+tilt-box` «Поворот коробки змінює гравітацію, блоки падають» · entities/move · 📎.
  - `+drone-path-plan` · `+code-chest` · `+journal-clues` · `+cosmetic-unlock` — бокові системи, кожна 🌱–🥉.

## Пропозиції до словників
- `+cond:watched(a, by)` — A у полі зору спостерігача (заборона дії, а не атака); ближче до `line_of_sight`, але з іншою семантикою.
- `+effect:rotate_room(section, deg)` — поворот частини поля з усім вмістом (на відміну від `rotate` однієї сутності).
- `+window:journal` — журнал підказок і нотаток персонажа.
- `+feature:cosmetic-outfits` — вбрання за бокові пазли.
- `+card:room-rotate`.

## Джерела
- ⭐ [Steam: HAMSTERMIND](https://store.steampowered.com/app/3555520/HAMSTERMIND/) — «Pivot chambers to rearrange the pyramid», таємні й необовʼязкові пазли, журнал, реліз 16.02.2026, Windows/Linux, геймпад; скриншоти: кімната 2×2, клітка з кнопками Rotate/Undo/Reset, павутина-граф, панель символів, журнал з «Catsparov's Game».
- [Player 2](https://www.player2.net.au/2026/02/hamstermind-review-this-hamster-is-a-dark-horse/) — сітка 2×2, «light motes», статуї блокують обертання поглядом, лазери, блоки; ящик «rotating by 90 degrees clockwise or counterclockwise», вітряні жуки; підказки не для головних пазлів.
- [Quest Daily](https://questdaily.com.au/review/review-hamstermind-tiny-paws-tough-puzzles-pc/) — чотири квадранти, сфери, клітки скарабеїв і вбрання, коди скринь, мета-код, журнал.
- [Gaming Furever](https://gamingfurever.com/news/reviews/hamstermind-a-sandy-yet-satisfying-puzzle-game) — Tournesol, горгульї, блоки «need pushing», клітки зі скарабеєм/скорпіоном/коброю, дрон-комаха.
- [Steam-відгуки](https://steamcommunity.com/app/3555520/reviews/?browsefilter=toprated) — 5 типів пазлів і які з них обовʼязкові; «rotate a box and blocks fall due to gravity».

## Непевне
- (?) Чи обертати можна лише секцію, де стоїш (зі зведення пошуку), і чи Хамстер обертається разом із нею.
- (?) Зсув кімнат у порожні місця — лише в сторонньому лістингу; у джерелах, які відкрив, — тільки обертання.
- (?) Правила дрона, павутини-графа (лічильники обертів 3 і 2 на скриншоті) і панелі символів з «вагою» — не описані в джерелах.
- (?) Undo/Reset у головних кімнатах (бачив лише в клітці); розмір сітки клітки.
- (?) Чи `field: square` чесне для 3D-пригоди: сітка — лише рівень секцій 2×2 і бокових пазлів.
