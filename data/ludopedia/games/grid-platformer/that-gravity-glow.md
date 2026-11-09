---
title: That Gravity Glow
slug: that-gravity-glow
aka: []
family: grid-platformer
also: [thinky, push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2021
platforms: [web (PuzzleScript)]
links:
  - {kind: itch, url: "https://toombler.itch.io/that-gravity-glow", best: true, note: "грати в браузері; керування, лінк на код і прохідні відео"}
  - {kind: other, url: "https://pancelor.com/PuzzleScript/editor.html?hack=fd938453944f9e2473a594274ea9bb80", note: "вихідний скрипт PuzzleScript + невикористані рівні 31–35"}
  - {kind: other, url: "https://toombler.itch.io/that-gravity-glow/devlog/334116/post-jam-update", note: "post-jam оновлення: +15 рівнів, кінцева кат-сцена"}
  - {kind: other, url: "https://itch.io/jam/lowrezjam-2021/rate/1159021", note: "сторінка в LOWREZJAM 2021 (тема «Gravity is the enemy»)"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=41dIwyHJ5Rk", note: "Joe Plays Puzzle Games — проходження (спойлери)"}
stage: v1
coverage: 75
mechanics: [move-4dir, gravity-fall, push-object, ladder-climb, reach-exit, undo-unlimited, restart-level, level-select, level-from-txt, sound-effects, game-screen, keyboard-controls, +gravity-shifting, +gravity-from-anchors, +wall-attach-unique, +zero-g-float, +stomp-attack, +push-chain, +gravity-indicator]
proposes: ["+effect:set_gravity", "+axis:gravity=entity-driven", "+ui:gravity-indicator", "+card:gravity-from-anchors", "+card:wall-attach-unique", "+card:zero-g-float", "+card:gravity-indicator"]
author: opus
date: 2026-11-09
---

# That Gravity Glow — гравітацію задають вороги, що прилипли до стін: розчави їх або перечепи — і світ падає в інший бік

## Суть
Покроковий бічний пазл-платформер на 12×12 клітин: гравітації як сталої нема, її тягнуть «паростки» — вороги, прикріплені до стін. Кожен прикріплений ворог тягне світ у бік своєї стіни, протилежні гасять один одного, а коли прикріплених нема — гравець плаває в невагомості. Гравець штовхає ворогів на інші стіни (міняє гравітацію) або падає на них згори (вбиває, і гравітація може зникнути просто в польоті), щоб дістатися виходу на краю рівня. Зроблено в PuzzleScript для LOWREZJAM 2021 (тема «Gravity is the enemy», екран 60×60 px).

## Поле і час
- Квадратна сітка 12×12 клітин по 5×5 px (обмеження джему 64×64, гра — 60×60); бічний вид без скролу.
- Покроково: тік = натискання; падіння анімується серією `again`-кроків (по клітині), доки щось рухається.
- Гравітація — **глобальний вектор**, що перераховується на початку кожного кроку з прикріплених ворогів; може бути ↓ ↑ ← → або нуль (по кожній осі окремо).
- Шари: фон · вихід · драбина · тверді (гравець, ворог, стіни) · трава-індикатор на стінах · спрайти.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | — | рух у 4 боки; під гравітацією падає, доки є вільно; спрайт повертається «ногами» до гравітації |
| Ворог-паросток | enemy | вільний / прикріплений ↓↑←→ | сам не ходить; прикріплюється до єдиної сусідньої «#»-стіни; прикріплений тягне гравітацію у свій бік; вільний падає за гравітацією; штовхається гравцем |
| Стіна «#» (притягальна) | static | світиться, коли тримає ворога | до неї можна прикріпитись |
| Стіна «%» (з червоною травою) | static | — | прикріплення не приймає; трава на ній росте в бік поточної гравітації (у невагомості — на всі боки) |
| Драбина | terrain | — | гравець на ній не падає |
| Вихід | static | смуга клітин на краю | гравець на виході → перемога |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(attach)` → ЯКЩО `state(enemy, attached_dir)` і `not occupied(dir, wall_attachable)` → ТО `clear_state(enemy, attached)` — відштовхнутий від стіни відлипає.
- КОЛИ `phase_start(attach)` → ЯКЩО `not state(enemy, attached)` і `adjacent_count(enemy, wall_attachable, ==, 1)` → ТО `set_state(enemy, attached_dir)`; дві й більше «#»-стін поруч — лишається вільним.
- КОЛИ `phase_start(gravity)` → ТО `custom: «g по вертикалі = знак(прикріплених ↓ − прикріплених ↑), по горизонталі — знак(→ − ←); нуль — невагомість»`.
- КОЛИ `tick` → ЯКЩО `custom: «g ≠ 0»` і `free(cell_g)` і `not cell(player, ladder)` → ТО `move(player, g)` замість вводу (падіння клітина за клітиною).
- КОЛИ `tick` → ЯКЩО `custom: «g ≠ 0»` і `not state(enemy, attached)` і `free(cell_g)` → ТО `move(enemy, g)`; гравець, стіна чи інший ворог — опора.
- КОЛИ `contact(player, enemy)` → ЯКЩО `moving(player, g)` → ТО `disappear(enemy)`, `move(player, g)` — «стомп»: тільки падаючи, не кроком.
- КОЛИ `input(dir)` → ЯКЩО `custom: «g = 0»` і `free(next)` → ТО `move(player, dir)` — у невагомості зупиняється одразу, нічого не падає.
- КОЛИ `input(dir)` → ЯКЩО `occupied(next, enemy)` → ТО `push(enemy)` — ланцюгом через кількох ворогів; уперлись у стіну → `block`.
- КОЛИ `input(dir)` → ЯКЩО `custom: «dir проти g, гравець стоїть»` і `free(next)` → ТО `move(player, dir)`, далі `fall(player)` назад (?) — справжнього стрибка нема.
- КОЛИ `destroyed(enemy)` → ЯКЩО `state(enemy, attached)` → ТО `custom: «гравітація перераховується; може зникнути посеред падіння — гравець зависає»`.
- КОЛИ `contact(enemy, enemy)` → ЯКЩО `moving(enemy, g)` → ТО `block` — вороги складаються в стовпчик.
- КОЛИ `enter(player, exit)` → ТО `win`, `next_level` (умова скрипту: `all player on Exit`).
- Перемога: гравець на клітині виходу. Поразки нема (смертельних клітин у грі нема) — застряг → undo/рестарт. Рахунку нема.

## Керування і ввід
- Стрілки / WASD — крок; під горизонтальною гравітацією «ліво/право» гравця фактично вгору/вниз по стіні.
- Z — undo (без ліміту), R — рестарт, Esc — вихід у вибір рівня / меню, M — вимкнути звук. Клавіші дії нема (`noaction`).

## Вікна, меню, HUD
- `main-menu` — титул PuzzleScript (Start / Continue).
- `level-select` — сітка рівнів (форк PuzzleScript від Pancelor: точки `level_select_point`), Esc з рівня повертає сюди.
- `game-screen` — 60×60 px без цифр: стан передають саме поле — червона трава на «%»-стінах показує напрям гравітації, «#»-стіна світиться, коли до неї прикріплено ворога.
- `custom-window` — кінцева кат-сцена, написана в самому PuzzleScript (рівень 30), далі повідомлення «THE END. Thanks For Playing!».
- Переходи: main-menu → level-select → game-screen → (вихід) → наступний рівень → … → кат-сцена → end.

## Фічі поза полем
- `undo` (∞), `restart-level`, `level-select` з вільним вибором пройдених (форк Pancelor), автопродовження PuzzleScript.
- `sound-toggle` (M); звуки на кожну подію: прилипання/відлипання ворога, стомп, приземлення гравця й ворога, поштовх.
- Дві збірки на itch: джем-версія (2021) і post-jam (11.01.2022: +15 рівнів, нові спрайти виходу, «трава» гравітації, частинки стомпу, кат-сцена).
- 30 рівнів у скрипті; колишні бонусні 31–35 винесено в «невикористані рівні» вихідного коду.

## Варіації й родичі
- Родичі: VVVVVV і Gravity Guy (перемикання гравітації кнопкою), Bone Cruncher і Crystal Mines II (зміна гравітації в сітці), Catrap / Toki Tori (покроковий бічний пазл), Sokoban (штовхання ворогів як ящиків).
- Осі: **хто задає гравітацію** (стала / кнопка гравця / клітини-перемикачі / **сутності на полі**); **чи складається вектор** (останній виграє / сума з гасінням); **що робить невагомість** (нема / плавання з зупинкою / інерція); **як вбити ворога** (дотик / лише падінням на нього / блоком).

## Цікавинки для курсу
- Гравітація як похідна від стану сутностей (сума прикріплених, протилежні гасяться) — 🥉: перерахунок глобального параметра щокроку.
- Прикріплення «лише якщо стіна-кандидат одна» — 📎: підрахунок сусідів певного типу.
- Стомп тільки в падінні (треба памʼятати, що гравець рухався під гравітацією минулого кроку) — 📎: прапорець «рухався минулого тіку».
- Ланцюгове штовхання ворогів із гравітацією — 🥉: класична складність порядку рухів у сітці.
- Індикатор стану світу без HUD (трава росте в бік гравітації) — 🌱, але гарний урок «поле як інтерфейс».
- Гра в 12×12 під обмеження 60×60 px — 🌱: приклад дизайну під жорсткий ліміт.

## Мапа на каталог
- Є: `move-4dir` · `gravity-fall` · `push-object` · `ladder-climb` · `reach-exit` · `undo-unlimited` · `restart-level` · `level-select` · `level-from-txt` (рівні — символьні мапи PuzzleScript) · `sound-effects` · `game-screen` · `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+gravity-from-anchors` «Гравітацію задають сутності на полі» · entities/move · 🥉 · слоти {combine: sum|last, zero: float|none} — прикріплені вороги, протилежні гасяться.
  - `+wall-attach-unique` «Прилипання до єдиної сусідньої стіни» · entities/state · 📎.
  - `+zero-g-float` «Невагомість: крок без падіння» · entities/move · 🌱.
  - `+gravity-indicator` «Індикатор напряму гравітації на полі» · interface/hud · 🌱.
  - `+gravity-shifting` (уже пропонувалась: Bone Cruncher, Crystal Mines II), `+stomp-attack` (Snake Rattle 'n' Roll), `+push-chain` — збіг із наявними пропозиціями корпусу.

## Пропозиції до словників
- `+effect:set_gravity` — перерахувати/встановити глобальний вектор гравітації (тут — щокроку з прикріплених ворогів).
- `+axis:gravity=entity-driven` — нове значення наявної осі `gravity`: напрям задають сутності на полі.
- `+ui:gravity-indicator` — візуальний показник напряму гравітації (трава на стінах).
- `+card:gravity-from-anchors`, `+card:wall-attach-unique`, `+card:zero-g-float`, `+card:gravity-indicator` — див. вище.

## Джерела
- ⭐ [itch.io: That Gravity Glow](https://toombler.itch.io/that-gravity-glow) — гра в браузері, керування, PuzzleScript (форк Pancelor), джем і лінки.
- [Вихідний скрипт](https://pancelor.com/PuzzleScript/editor.html?hack=fd938453944f9e2473a594274ea9bb80) — прочитано через GitHub Gist API: обʼєкти, усі правила прикріплення/гравітації/стомпу/поштовху, умова перемоги, 30 точок вибору рівня.
- [Devlog «Post Jam Update»](https://toombler.itch.io/that-gravity-glow/devlog/334116/post-jam-update) — що додано після джему.
- [LOWREZJAM 2021 — сторінка гри](https://itch.io/jam/lowrezjam-2021/rate/1159021) — джем-контекст.
- [YouTube: Joe Plays Puzzle Games](https://www.youtube.com/watch?v=41dIwyHJ5Rk) — проходження (лінк зі сторінки itch).

## Непевне
- (?) Діагональна гравітація (вертикальна й горизонтальна складові одночасно): скрипт рахує осі окремо, але як рухається гравець, коли обидві ненульові, і чи бувають такі рівні — не перевірено.
- (?) Крок «проти гравітації» стоячи — з коду виходить підскок на 1 клітину з поверненням наступним `again`-кроком; у грі не перевірено.
- (?) Коментарі на itch згадують «червоний» і «зелений» фінали — у скрипті видно лише одну кат-сцену й «THE END».
- (?) Рік: джем — серпень 2021 (Gamebrain: 14.08.2021, з пошуку), post-jam — 11.01.2022.
- Thinky Games (⭐ черги) віддає 403 — джерелом правил став вихідний код.
