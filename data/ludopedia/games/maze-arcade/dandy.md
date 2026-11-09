---
title: Dandy / Dark Chambers
slug: dandy
aka: [Dark Chambers, Dandy Dungeon, Thesis of Terror]
family: maze-arcade
also: [roguelike]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: coop
  info: partial
  random: none
  goal: score
year: 1983
platforms: [Atari 8-bit, Atari 2600, Atari 7800, Atari XEGS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dandy_(video_game)", best: true, note: "Dandy: 26 підземель A–Z, генератори-черепи, деградація монстрів, серце для воскресіння, кооп на 4, редактор; Dark Chambers"}
  - {kind: other, url: "https://atariage.com/manual_html_page.php?SoftwareLabelID=122", note: "мануал Dark Chambers (2600): ghoul-и й очки, сила 31, прокляття, ключі/бомби до 15, зброя, скарби, правила двох"}
  - {kind: other, url: "https://atariage.com/software_list.php?SystemID=2600&searchValue=dark+chambers", note: "AtariAge: картка Dark Chambers 2600, скани"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=dandy+atari+800+1983+gameplay", note: "пошук; Dandy"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=dark+chambers+atari+7800+gameplay", note: "пошук; Dark Chambers"}
stage: v1
coverage: 65
mechanics: [move-8dir, projectile-shot, shoot-modes, hp-damage, item-pickup, inventory-items, inventory-limit, key-and-door, spawner-entity, hidden-under-block, reach-exit, stairs-levels, sequential-levels, player-camera, event-points, status-panel, in-game-editor, difficulty-select, +devolve-on-hit, +smart-bomb, +shoot-items, +shared-camera, +revive-ally, +stat-upgrade-pickup, +drain-hazard, +fake-door, +restart-at-last-level, +carried-food]
proposes: ["+effect:revive", "+cond:ally_dead", "+ui:strength-bar", "+feature:shared-keys"]
author: opus
date: 2026-11-09
---

# Dandy / Dark Chambers — протогаунтлет: до чотирьох лучників у підземеллях A–Z, генератори-черепи і монстри, що «деградують» від пострілу

## Суть
Гравець (або до 4 разом на Atari 8-bit) веде лучника через 26 підземель-лабіринтів зверху (A–Z): шукає вихід, відмикає двері ключами, стріляє монстрів, які плодяться з генераторів-черепів. Удар монстра не вбиває, а забирає здоровʼя; їжа/зілля його повертають. Ключова механіка, що перейшла в Gauntlet (1985): поцілений монстр не гине одразу, а «деградує» на слабшу форму, а генератор треба зруйнувати, щоб потік припинився. Предок `gauntlet.md` — та сама основа без класів героїв і танення здоровʼя.

## Поле і час
- Рівень — клітинний лабіринт, більший за екран; камера скролить за групою: з 2+ гравцями — за середньою позицією групи (Dandy); у Dark Chambers без партнера не можна відійти далі видимого екрана.
- Real-time; гравці й монстри ходять у 8 напрямках.
- 26 рівнів, позначених літерами A–Z; повернення на вищі рівні вирізане ще в розробці (тестувальники ним не користувались).
- Касетна версія: стрічку зупиняють між рівнями і довантажують наступний.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Лучник (Dandy) / герой (DC) | player | здоровʼя / сила (DC: шкала до 31) | рух 8 напрямків; стріли в 8 напрямків, нескінченні; у DC не може йти, поки стріляє |
| Монстр (ghoul) | enemy | рівень сили; Dandy — види лише графічні | іде до гравця; дотик забирає здоровʼя; влучання → на рівень нижче, найнижчий гине |
| Zombie (DC) | enemy | найслабший | при вбивстві вибухає |
| Wraith (DC) | enemy | 20 очок, дотик −1 | деградує в Zombie |
| Skeleton (DC) | enemy | 30 очок, дотик −3 | деградує у Wraith |
| Wizard (DC) | enemy | 50 очок, дотик −4 | деградує в Skeleton |
| Grim Reaper (DC) | enemy | 100 очок, дотик −5 | найсильніший; деградує у Wizard |
| Генератор-череп / Spawner | spawner | DC: 100 очок | породжує монстрів; знищений — може відкрити те, що ховав (скарб, зброю, прокляття, вихід) |
| Стіна | static | — | непрохідна |
| Двері | gate | — | відчиняються ключем; DC: ведуть у секретну кімнату, на ранніх рівнях є фальшиві |
| Ключ | pickup | DC: до 15 | витрачається на одні двері |
| Їжа (Dandy) | pickup | — | збирається, зʼїдається клавішею → здоровʼя |
| Зілля (DC) | pickup | +3 сили | відновлює силу |
| Бомба / зілля-бомба | pickup | DC: до 15 | клавіша (Dandy) / подвійний Fire (DC) → знищує всіх монстрів на екрані; Dandy: можна підірвати стрілою на місці |
| Серце із золота (Dandy) | pickup | — | взяте / прострелене → воскрешає загиблого союзника |
| Зброя (DC) | pickup | gun / dagger / shield | постріл частіше / сильніше / менше втрати сили від дотику |
| Скарб (DC) | pickup | 100 / 500 / 1000 / 3000 | лише очки (скринька, срібна чаша, амулет, золота чаша) |
| Пастка (DC curse) | hazard | −6 сили | шкодить при дотику |
| Отрута (DC curse) | hazard | −4 сили | шкодить при дотику |
| Вихід / прихована брама | static | — | перехід на наступну літеру; у DC брама захована і часто під генератором |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(fire, player)` → ТО `spawn(arrow, facing)`; DC: ЯКЩО `state(player, shooting)` → ТО `block` (рух на час пострілу).
- КОЛИ `contact(arrow, monster)` → ЯКЩО `custom: «монстр не найнижчого рівня»` → ТО `transform(monster, weaker)`, `score(n)`; інакше `disappear(monster)`.
- КОЛИ `died(zombie)` → ТО `custom: «вибухає»` (DC; можливо, лише анімація (?)).
- КОЛИ `contact(monster, player)` → ТО `damage(player, n)`; DC: n за типом 1/3/4/5, ЯКЩО `has(player, shield)` → ТО менше.
- КОЛИ `contact(player, trap|poison)` → ТО `damage(player, 6|4)`.
- КОЛИ `timer(spawn)` → ЯКЩО `free(cell)` → ТО `spawn_at(monster, next_to_generator)`.
- КОЛИ `contact(arrow, generator)` → ТО `disappear(generator)`, `score(100)`, `reveal(cell)` — під ним скарб / зброя / прокляття / брама (DC).
- КОЛИ `contact(player, key)` → ЯКЩО `counter(keys, <, 15)` → ТО `pickup(player, key)`.
- КОЛИ `contact(player, door)` → ЯКЩО `has(player, key)` → ТО `take(player, key)`, `set_cell(door, floor)`; інакше `block` (фальшиві двері DC не відчиняються ніколи).
- КОЛИ `contact(player, food)` → ТО `pickup(player, food)`; КОЛИ `input(eat)` → ЯКЩО `has(player, food)` → ТО `use(player, food)`, `heal(player, n)` (Dandy).
- КОЛИ `contact(player, potion)` → ТО `heal(player, 3)` (DC).
- КОЛИ `input(bomb)` → ЯКЩО `has(player, bomb)` → ТО `take(player, bomb)`, `custom: «знищити всіх монстрів (DC — і прокляття) на екрані»`.
- КОЛИ `contact(arrow, potion)` → ТО `custom: «бомба спрацьовує на місці»` (Dandy).
- КОЛИ `contact(player|arrow, heart)` → ЯКЩО `custom: «є загиблий союзник»` → ТО `custom: «воскресити союзника»` (Dandy).
- КОЛИ `contact(player, weapon)` → ТО `set_state(player, faster_shot|stronger_shot|shielded)` (DC).
- КОЛИ `contact(player, treasure)` → ТО `score(100|500|1000|3000)`, `disappear(treasure)`.
- КОЛИ `enter(player, exit)` → ТО `next_level` (A → B → … → Z).
- КОЛИ `hp_zero(player)` → ЯКЩО `custom: «живий партнер є»` → ТО `give(partner, keys)`; КОЛИ `enter(partner, exit)` → ТО `custom: «загиблий воскресає на новому рівні»` (DC).
- КОЛИ `hp_zero(all_players)` → ТО `game_over`; DC: наступна гра стартує з останнього рівня.
- Перемога: пройти Z. Поразка: сила/здоровʼя всіх героїв = 0. Рахунок: монстри, генератори, скарби.

## Керування і ввід
- Dandy: джойстик на кожного з 4 гравців — рух і постріл у напрямку джойстика; клавіші клавіатури — зʼїсти їжу, підірвати бомбу.
- Dark Chambers: джойстик + Fire; Fire двічі швидко — бомба; Select у будь-який момент — назад на титул.
- Дружній вогонь вирізали після тестів («гра швидко вироджувалась у всі проти всіх»).

## Вікна, меню, HUD
- `main-menu` (DC, титульний екран): Select + джойстик вгору/вниз — 1 чи 2 гравці; вліво/вправо — складність Low/Medium/High (показує мордочка ведмедя); Fire/Reset — старт.
- `game-screen`: лабіринт, `+ui:strength-bar` (шкала сили до 31), `score`, лічильники ключів і бомб (`inventory-bar`), літера рівня (`level-number`).
- `editor-window` (Dandy): редактор підземель.
- Переходи: титул → гра → вихід → наступна літера → … → сила 0 → титул (рестарт з останнього рівня).

## Фічі поза полем
- `mode-coop`: Dandy — до 4 одночасно, DC — 2; спільний екран.
- `level-editor` (Dandy) — створення нових підземель; за задумом мав бути і 5-й гравець-«майстер підземелля», не реалізовано.
- `difficulty-presets` (DC): Low / Medium / High.
- `+feature:shared-keys` (DC): ключі загиблого переходять живому.
- `continue` у вигляді рестарту з останнього рівня (DC).

## Варіації й родичі
- Dandy (1983, Atari 8-bit, APX; 1985 у журналі Antic як Dandy Dungeon; порти Electric Dreams 1986 (?)).
- Dark Chambers (1988, Atari Corp., 2600/7800/XE) — переробка за ліцензією: 1–2 гравці, менше ворогів на екрані, деталізована таблиця ghoul-ів, прокляття, зброя.
- Наступник за духом — `gauntlet.md` (1985): класи героїв, HP-таймер, Death, Lobber; Ед Лог на GDC 2012 назвав Dandy прямим натхненням, позов Палевича врегульовано поза судом.
- Родичі: `atari-adventure.md` (ключі й двері), `wizard-of-wor.md` (кооп у лабіринті), `venture.md` (кімнати й скарби).
- **Осі варіацій:** загибель монстра (одразу / деградація по рівнях); смерть союзника (вибув / воскресає серцем / воскресає на новому рівні); їжа (діє одразу / несеться й зʼїдається клавішею); камера (центр групи / межа екрана тримає партнерів).

## Цікавинки для курсу
- Деградація монстра від пострілу (ланцюг transform сильний → слабший → смерть) — 🌱: таблиця «вид → наступний».
- Генератор, що ховає під собою вихід/скарб (`reveal` після знищення) — 📎.
- Бомба на весь екран, яку можна нести або підірвати стрілою на місці — 📎.
- Воскресіння союзника предметом / на наступному рівні — 📎.
- Камера за середньою позицією 4 гравців — 🥈 (і обмеження руху краєм кадру в DC).
- Їжа в інвентарі, зʼїсти — окрема дія: ресурс-аптечка замість миттєвого бонусу — 🌱.
- Редактор підземель на 26 рівнів — 🥈.

## Мапа на каталог
- Є: `move-8dir` · `projectile-shot` · `shoot-modes` (DC: gun/dagger) · `hp-damage` · `item-pickup` · `inventory-items` · `inventory-limit` (15 ключів/бомб) · `key-and-door` · `spawner-entity` · `hidden-under-block` (брама під генератором) · `reach-exit` · `stairs-levels` (лише вниз) · `sequential-levels` · `player-camera` · `event-points` · `status-panel` · `in-game-editor` · `difficulty-select`.
- **Нема** → пропозиції карток:
  - `+devolve-on-hit` «Ворог від влучання слабшає на рівень» · entities/combat · 🌱 · слот {chain}.
  - `+smart-bomb` «Предмет уражає всіх на екрані» · entities/combat · 📎 (як у Gauntlet).
  - `+shoot-items` «Постріл активує предмет» · entities/interact · 📎.
  - `+shared-camera` «Камера тримає всіх гравців» · interface/render · 🥈.
  - `+revive-ally` «Воскресіння союзника» · entities/death · 📎 · слот {how}.
  - `+stat-upgrade-pickup` «Предмет підсилює героя» · entities/state · 📎.
  - `+drain-hazard` «Пастка забирає HP, не вбиває» · entities/combat · 🌱.
  - `+fake-door` «Фальшиві двері» · entities/interact · 🌱.
  - `+restart-at-last-level` «Нова гра з останнього рівня» · levels/progression · 🌱.
  - `+carried-food` «Аптечка в інвентарі, використати дією» · entities/state · 🌱.

## Пропозиції до словників
- `+effect:revive` — повернути загиблого союзника (серце Dandy, перехід рівня в DC).
- `+cond:ally_dead` — є загиблий член партії (умова для серця).
- `+ui:strength-bar` — шкала сили з поділками (31 у DC); можливо, різновид `hp-bar`.
- `+feature:shared-keys` — інвентар загиблого переходить живому партнеру.

## Джерела
- ⭐ [Wikipedia: Dandy](https://en.wikipedia.org/wiki/Dandy_(video_game)) — 26 рівнів A–Z, ключі й двері, генератори-черепи, деградація монстрів, їжа, зілля-бомби, серце, кооп 4, камера за середнім, редактор, історія з Gauntlet.
- [AtariAge: мануал Dark Chambers](https://atariage.com/manual_html_page.php?SoftwareLabelID=122) — ghoul-и й очки, сила 31, прокляття, ліміт 15, зброя, скарби, правила двох гравців, складність.
- YouTube: пошук «dandy atari 800 1983 gameplay», «dark chambers atari 7800 gameplay».

## Непевне
- (?) Dandy: стаття плутає «бомби» і «зілля» — чи це один предмет (бомба = зілля-бомба) чи два різні.
- (?) Скільки рівнів сили мають монстри Dandy і скільки очок дають — не знайдено; таблиця Zombie…Grim Reaper — лише з мануала DC.
- (?) Zombie: дотик у мануалі не має ціни; «вибухає» — можливо, лише анімація.
- (?) Як саме серце воскрешає: взяти чи прострелити (стаття каже обидва).
- (?) Чи брама/скарб у DC справді ховається саме під генератором — у мануалі «spawners hide treasures, weapons, curses, gates».
- (?) Чи Dandy має обмеження інвентаря; порти Electric Dreams 1986 — платформи не перевірені.
- WebSearch-ліміт сесії вичерпано; перевірено по Wikipedia і мануалу AtariAge.
