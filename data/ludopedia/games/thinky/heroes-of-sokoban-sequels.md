---
title: "Heroes of Sokoban II: Monsters і III: The Bard and the Druid"
slug: heroes-of-sokoban-sequels
aka: ["Heroes of Sokoban II: Monsters", "Heroes of Sokoban III: The Bard and the Druid", Heroes of Sokoban II, Heroes of Sokoban III]
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
year: 2013
platforms: [web]
links:
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=6910207", best: true, note: "II: Monsters — грати в браузері; 22 рівні, кожен новий монстр і Жрець вводяться підписом"}
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=7072276", note: "III: The Bard and The Druid — грати в браузері; 22 рівні"}
  - {kind: other, url: "https://api.github.com/gists/6910207", note: "код II (gist, 2013-10-09): дракони, гобліни, Жрець, двері монстрів, скасування «порожнього» ходу"}
  - {kind: other, url: "https://api.github.com/gists/7072276", note: "код III (gist, 2013-10-20): ноти Барда в квадраті 5×5, перетворення Друїда, коментарі автора"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Heroes+of+Sokoban+II+Monsters+puzzlescript", note: "пошук; проходження II"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Heroes+of+Sokoban+III+Bard+Druid", note: "пошук; проходження III"}
stage: v1
coverage: 85
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, pull-object, party-switch, swap-on-contact, line-of-sight-attack, beam-tracing, touch-death, button-toggle, key-and-door, impassable-cells, all-on-targets, coverage-area, freeze-into-block, undo-unlimited, restart-level, sequential-levels, sound-effects, +heroes-as-objects, +chain-push, +line-of-sight-swap, +hold-all-switches, +monster-door, +adjacent-kill, +protect-adjacent, +charm-lead, +transmute-on-bump, +no-op-move-cancel]
proposes: ["+effect:cast_ray", "+effect:charm", "+window:message-screen", "+axis:actors", "+card:monster-door", "+card:adjacent-kill", "+card:protect-adjacent", "+card:charm-lead", "+card:transmute-on-bump"]
author: opus
date: 2026-11-19
---

# Heroes of Sokoban II і III — що два сиквели додають до трьох героїв-дієслів: нерухомі монстри-вбивці, Жрець-оберіг, Бард, що веде за собою стадо, і Друїд, що робить з дерева камінь

## Суть
В обох частинах діють правила [Heroes of Sokoban](heroes-of-sokoban.md): Воїн штовхає ланцюг, Злодій тягне, Чарівник міняється з першим рухомим на лінії, неактивні герої — такі самі обʼєкти, як ящики, кольорові кнопки тримають двері, мета — усі герої на цілях. **II: Monsters** додає монстрів, які самі не ходять, але вбивають: гоблін — кожного сусіда, дракон — першого на своєму ряду. Четвертий герой, Жрець, рятує себе й сусідніх героїв, а смерть будь-кого — рестарт рівня. **III: The Bard and the Druid** прибирає драконів і додає двох героїв: Бард «зачаровує» все рухоме в квадраті 5×5 і веде його за собою, Друїд ударом перетворює ящик на стіну, стіну на ящик, а монстра чи героя — на камінь.

## Поле і час
- Як у першій частині: квадратна сітка, один екран на рівень, по 22 рівні в кожній грі.
- Покроково: тік = ввід. Монстри не мають власного руху — усе, що вони роблять, стається в фазі `late` наприкінці кожного ходу.
- Порядок ходу (з коду): дія активного героя (штовхання, тягнення, обмін, удар Друїда, крок Барда із зачарованими) → перемикання героя → нові ноти навколо активного Барда (III) → `late`: вогонь драконів → удари гоблінів → порятунок Жерцем → загибель → перерахунок дверей.
- Шари колізій II: тло → службові `Warpball`, `Dying` → цілі, кнопки, відчинені двері → тверді (зачинені двері, герої, ящики, стіни, монстри, труп) → вогонь і службові позначки. III додає шар нот.
- II: якщо активний герой лишився на місці (уперся в стіну) і не перемикався, хід скасовується повністю — дракони не отримують «порожнього» ходу. Перемикання героя — повноцінний хід.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Воїн, Злодій, Чарівник, ящик, стіна, кнопки, двері, ціль | — | — | як у [Heroes of Sokoban](heroes-of-sokoban.md); монстри теж рухомі: Воїн їх штовхає, Злодій тягне, Чарівник міняється з ними |
| Жрець (жовтий) — II, III | player | діє й неактивним | ходить без власного дієслова; сам невразливий; сусідні герої теж уціліють |
| Гоблін — II, III | enemy | — | не ходить; наприкінці ходу вбиває кожного вразливого сусіда — героя чи монстра, і інших гоблінів |
| Дракон ліворуч / праворуч — II | enemy | напрям вогню | не ходить; щоходу дихає вогнем у свій бік уздовж ряду |
| Вогонь — II | projectile | ліво / право | службовий: за один хід летить порожніми клітинами; вразливого вбиває, на ящику, стіні чи зачинених дверях гасне |
| Двері монстрів (M) — II, III | gate | — | непрохідні, поки на рівні є хоч один монстр; потім зникають назавжди |
| Труп — II, III | object | — | лишається від загиблого героя; наступний ввід перезапускає рівень |
| Бард (фіолетовий) — III | player | квадрат нот 5×5 | крок 4 напрямки; усе рухоме з нотою крокує разом із ним |
| Нота — III | zone | — | службова: стоїть лише на рухомих у квадраті 5×5 навколо активного Барда |
| Друїд (помаранчевий) — III | player | — | хід у ящик, стіну, монстра чи героя — перетворення замість кроку |

## Правила (КОЛИ → ЯКЩО → ТО)
- Рух, штовхання, тягнення, обмін Чарівника, кнопки й двері — як у [Heroes of Sokoban](heroes-of-sokoban.md); кнопку тиснуть ящик, герой і монстр, а в III ще й стіна (камінь, зроблений Друїдом).
- КОЛИ `input(action)` → ТО `custom: «керування до наступного героя в циклі Воїн → Злодій → Чарівник → Жрець (II) або … → Жрець → Бард → Друїд (III), відсутніх пропустити»`.
- КОЛИ `turn_end(hero)` → ЯКЩО `custom: «активний герой стоїть там, де стояв, і не перемикався»` → ТО `custom: «скасувати весь хід»` (II).
- КОЛИ `turn_end(hero)` → ТО `custom: «кожен дракон пускає вогонь у свій бік»` (II).
- КОЛИ `line_of_sight(dragon, x)` → ЯКЩО `custom: «x — герой або монстр, перший на лінії»` → ТО `set_state(x, dying)` — дракон теж гине від чужого вогню (II).
- КОЛИ `adjacent(goblin, x)` → ЯКЩО `custom: «x — герой або монстр»` → ТО `set_state(x, dying)`; два гобліни поруч убивають один одного.
- КОЛИ `state_on(x, dying)` → ЯКЩО `custom: «x — Жрець»` or `adjacent_count(x, priest, >=, 1)` and `custom: «x — герой»` → ТО `clear_state(x, dying)`, `sound(saved)`.
- КОЛИ `state_on(monster, dying)` → ТО `disappear`, `sound(kill)`.
- КОЛИ `state_on(hero, dying)` → ТО `transform(hero, corpse)`, `sound(dying)`.
- КОЛИ `input(any)` → ЯКЩО `count(corpse, >=, 1)` → ТО `restart`.
- КОЛИ `turn_end(hero)` → ЯКЩО `count(monster, ==, 0)` → ТО `disappear(monster_door)`, `sound(open)`.
- КОЛИ `input(dir)` → ЯКЩО `turn_of(druid)` and `occupied(cell_ahead, crate)` → ТО `transform(crate, wall)`; Друїд стоїть (III).
- КОЛИ `input(dir)` → ЯКЩО `turn_of(druid)` and `occupied(cell_ahead, wall)` → ТО `transform(wall, crate)` — будь-яка стіна, і межа рівня теж (III).
- КОЛИ `input(dir)` → ЯКЩО `turn_of(druid)` and `occupied(cell_ahead, goblin)` → ТО `transform(goblin, wall)` (III).
- КОЛИ `input(dir)` → ЯКЩО `turn_of(druid)` and `occupied(cell_ahead, hero)` and `not custom: «це Жрець або поруч стоїть Жрець»` → ТО `transform(hero, wall)` — герой вибуває з партії (III).
- КОЛИ `turn_end(hero)` → ЯКЩО `turn_of(bard)` → ТО `mark(square_5x5_around_bard, note)`, `custom: «ноту лишити лише на рухомих: ящик, неактивний герой, гоблін»` (III).
- КОЛИ `input(dir)` → ЯКЩО `turn_of(bard)` and `free(cell_ahead_of_charmed)` → ТО `move(charmed, dir)` — повторно, доки ланцюг звільняє місце; потім `move(bard, dir)` (III).
- КОЛИ `blocked(bard)` → ТО `custom: «скасувати весь хід — зачаровані теж лишаються»` (III).
- КОЛИ `input(dir)` → ЯКЩО `turn_of(wizard)` and `custom: «промінь дійшов до краю екрана»` → ТО `move(wizard, dir)` (III).
- Перемога: усі герої на цілях і всі цілі зайняті; скамʼянілий герой більше не герой · Поразка: загибель будь-якого героя → труп → рестарт · Рахунку нема.

## Керування і ввід
- Стрілки / WASD — крок активного героя (Чарівник — «постріл» обміном, Друїд — удар-перетворення, Бард — крок разом із зачарованими).
- X / пробіл (action) — передати керування наступному героєві; у II це повний хід, на який відповідають монстри.
- Z — undo, R — рестарт, Esc — меню (стандарт PuzzleScript); після загибелі Z до наступного вводу ще повертає хід (?).

## Вікна, меню, HUD
- `splash-screen` — титул PuzzleScript: назва, автор Jonah Ostroff, start / continue.
- `game-screen` — лише поле; активного героя видно за яскравим спрайтом, неактивні — темніші `S*`-версії; зачаровані Бардом обʼєкти мають ноту (III).
- `custom-window` — повідомлення-навчання між рівнями. II: «Welcome back.», «You've played the original, yes?», «Watch out for goblins.», «Goblins attack each other too.», «Dragons breath fire.», «Fire hurts enemies.», «Think fast!», «Kill monsters to open the M wall.», «Yellow priest is protected.», «Heroes next to a priest are safe.», «The final challenge.». III: вступ про зниклих драконів, «Purple bard charms nearby crates.», «Monsters may also be charmed.», «No one can resist the bard's music.», «Orange druid turns stone into wood, wood into stone.», «Living things may also be turned into stone.», «Get ready.».
- Переходи: титул → рівні підряд із повідомленнями → «Thanks for playing!» → титул.

## Фічі поза полем
- `undo` ∞, `restart-level` — стандарт рушія; смерть героя теж закінчується рестартом.
- `levels-sequential`: по 22 рівні без вибору; `tutorial` — підписами, кожна сутність вводиться окремим рівнем.
- Відкритий код (`mod-support` через «hack» у редакторі PuzzleScript); автор лишив коментарі про задум («What strategic purpose could it serve…»).

## Варіації й родичі
- Основа: [Heroes of Sokoban](heroes-of-sokoban.md). Пізніше всі три частини стали одним зі світів [Order of the Sinking Star](order-of-the-sinking-star.md).
- Родичі за механіками: [Adventures of Lolo](../push-slide/adventures-of-lolo.md) (Медуза бʼє по лінії), [Kickle Cubicle](../grid-platformer/kickle-cubicle.md) (ворог → блок), [DROD](drod.md) (монстри з правилами), [Baba Is You](baba-is-you.md) (дієслова як властивості).
- Осі варіацій:
  - **розмір партії**: 3 героя (I) / 4 (II) / 6 (III);
  - **як бʼє монстр**: по сусідству (гоблін) / по лінії до першої перешкоди (дракон) / нерухомий, але його можна пересунути героєм;
  - **що рятує**: нічого / аура Жерця на сусідів / undo;
  - **як рухається гурт**: ланцюгом поштовху (Воїн) / тягом (Злодій) / зоною зачарування навколо лідера (Бард);
  - **перетворення**: ворог → блок в один бік (Kickle Cubicle) / ящик ↔ стіна в обидва боки плюс живе → камінь (Друїд).

## Цікавинки для курсу
- Двофазна смерть: спершу позначка `dying`, потім порятунок аурою Жерця, і лише тоді загибель — 📎 (порядок фаз у кінці ходу).
- Вогонь дракона як промінь до першої перешкоди: за хід гине лише перший на лінії, тож ряд гоблінів працює як годинник («Think fast!») — 🥉.
- Двері монстрів: перевірка «на рівні не лишилось монстрів» щоходу — 🌱.
- Ноти Барда: квадрат 5×5 одним обʼєктом через чотири «вітряки» відносних напрямків (улюблене місце автора в коді) — 🥉; груповий рух зачарованих з повтором, доки ланцюг звільняє місце, і скасування ходу, якщо Бард не зрушив — 🥈.
- Друїд: перетворення за типом цілі (ящик ↔ стіна, живе → камінь) з винятком «поруч із Жерцем» — 📎.
- Скасування ходу, у якому активний герой не зрушив (II), щоб монстри не мали зайвого тіку — 🌱.
- Розвʼязувач BFS по станах (позиції до 6 героїв + ящиків + монстрів + активний герой) з відсіканням станів із трупом — 🥇.

## Мапа на каталог
- Є: `move-4dir` + `move-by-input` + `keyboard-controls`; `push-object` (Воїн) · `pull-object` (Злодій) · `swap-on-contact` (Чарівник) · `party-switch` (action); `line-of-sight-attack` + `beam-tracing` ↔ вогонь дракона; `touch-death` ↔ гоблін; `button-toggle` + `key-and-door` ↔ кольорові кнопки й двері; `impassable-cells`; `all-on-targets`; `coverage-area` ↔ квадрат нот Барда; `freeze-into-block` ↔ Друїд робить з гобліна стіну (ящик ↔ стіна — нова картка нижче); `undo-unlimited`, `restart-level`, `sequential-levels`, `sound-effects`.
- **Нема** → пропозиції карток:
  - `+monster-door` «Двері зникають, коли на рівні не лишилось монстрів» · entities/interact · 🌱 — родич `destroy-all-enemies`, але як ключ, а не перемога.
  - `+adjacent-kill` «Нерухомий ворог убиває всіх вразливих сусідів наприкінці ходу» · entities/combat · 📎 · слот {adjacency: 4|8, hits_allies: bool}.
  - `+protect-adjacent` «Аура: носій і його сусіди не гинуть» · entities/state · 📎 · слот {radius}.
  - `+charm-lead` «Обʼєкти в зоні навколо лідера крокують разом з ним» · entities/move · 🥈 · слот {shape: 5x5}.
  - `+transmute-on-bump` «Хід у ціль перетворює її за таблицею типів» · entities/interact · 📎 · слот {table}.
  - `+no-op-move-cancel` «Хід без зміни позиції не віддає тік ворогам» · game-logic/turn · 🌱.
  - Повтори корпусу: `+heroes-as-objects`, `+chain-push`, `+line-of-sight-swap`, `+hold-all-switches` — див. heroes-of-sokoban.md.

## Пропозиції до словників
- `+effect:cast_ray` — промінь до першої перешкоди (Чарівник, вогонь дракона; повтор Heroes of Sokoban).
- `+effect:charm` — позначити обʼєкти в зоні, щоб вони повторили наступний крок лідера (Бард).
- `+window:message-screen` — екран-повідомлення PuzzleScript (повтор).
- `+axis:actors` — `party`: 4 (II) і 6 (III) героїв по черзі.
- `+card:monster-door`, `+card:adjacent-kill`, `+card:protect-adjacent`, `+card:charm-lead`, `+card:transmute-on-bump` — див. вище.
- ⏳-слова, вжиті тут: `input`, `turn_end`, `adjacent`, `line_of_sight`, `state_on`, `blocked`, `turn_of`, `occupied`, `free`, `count`, `adjacent_count`, `move`, `set_state`, `clear_state`, `mark`, `sound`, `restart`; ролі `projectile`, `gate`, `zone`.

## Джерела
- ⭐ [Heroes of Sokoban II на puzzlescript.net](https://www.puzzlescript.net/play.html?p=6910207) — гра в браузері.
- [Heroes of Sokoban III на puzzlescript.net](https://www.puzzlescript.net/play.html?p=7072276) — гра в браузері.
- [Gist II через GitHub API](https://api.github.com/gists/6910207) — повний код: обʼєкти, легенда (`Moveable`, `Vulnerable`, `Healer`), правила драконів, гоблінів, Жерця, `DidNotMove`, дверей монстрів, умови перемоги, 22 рівні, тексти повідомлень.
- [Gist III через GitHub API](https://api.github.com/gists/7072276) — повний код: Бард (ноти, груповий крок, скасування), Друїд (перетворення, захист Жерцем), шість героїв у циклі, 22 рівні.
- YouTube: пошук «Heroes of Sokoban II Monsters puzzlescript» і «Heroes of Sokoban III Bard Druid».

## Непевне
- (?) Рік виходу — за датами gist (II: 2013-10-09, III: 2013-10-20); окремої сторінки автора не знайдено.
- (?) Чи Z після загибелі повертає хід до того, як наступний ввід запустить рестарт, — так поводиться рушій PuzzleScript, у грі не перевірено.
- (?) Порядок, у якому зачаровані Бардом обʼєкти займають звільнені клітини в довгих ланцюгах, — з коду (повтор правила до стабільності); чи бувають неочевидні випадки, у грі не перевірено.
- (?) Скамʼянілий герой лишається стіною назавжди; повернути його можна лише в ящик, не в героя — з коду, у рівнях не перевірено.
