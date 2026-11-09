---
title: Rick Dangerous
slug: rick-dangerous
aka: [Рік Денджерес]
family: grid-platformer
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: hidden
  random: none
  goal: state
year: 1989
platforms: [Amiga, Atari ST, MS-DOS, ZX Spectrum, C64, Amstrad CPC, Acorn Archimedes]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Rick_Dangerous", best: true, note: "пістолет, динаміт, палиця; приховані пастки, що вбивають і ворогів; 4 рівні"}
  - {kind: other, url: "https://www.rickdangerous.co.uk/how2.htm", note: "фан-сайт «Rick Dangerous Resurrected»: керування на всіх платформах, 6 куль і 6 динамітів на старті"}
  - {kind: other, url: "https://www.breadbox64.com/c64-games/rick-dangerous", note: "C64: палиця штовхає/оглушує, ящики поповнюють набої, 4 рівні = 85 екранів"}
  - {kind: other, url: "https://www.tvtropes.org/pmwiki/pmwiki.php/VideoGame/RickDangerous", note: "TV Tropes: типи пасток (з пошуку, не відкривав)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Rick+Dangerous+1989+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [gravity-fall, ladder-climb, projectile-shot, bomb-fuse, explode-area, destructible-blocks, push-object, touch-death, environment-death, player-death, item-pickup, inventory-items, chase-player, enemy-patrol, respawn, checkpoint, event-points, sequential-levels, status-panel, game-screen, game-pause, keyboard-controls, +hidden-trigger-trap, +trap-kills-enemies, +blast-flings-blocks, +fire-plus-direction, +limited-ammo-refill, +rolling-boulder-chase]
proposes: ["+trigger:enter_hidden", "+role:trigger-cell", "+card:hidden-trigger-trap", "+card:trap-kills-enemies", "+card:blast-flings-blocks", "+card:fire-plus-direction", "+card:limited-ammo-refill", "+card:rolling-boulder-chase"]
author: opus
date: 2026-11-09
---

# Rick Dangerous — пародія на Індіану Джонса: флікскрін-платформер, де кожна клітина може приховувати пастку, а патронів і динаміту — по шість

## Суть
Рік біжить екранами-кімнатами печери, піраміди, замку й ракетної бази, стрибає й лазить драбинами. Головний ворог — не люди, а **пастки, що спрацьовують, коли Рік стає на певну клітину**: шипи з «звичайної» стіни, дротики, списи, ворота, що падають, камені, що зсуваються. Попереджень зазвичай нема, тож гра — це запамʼятовування («trial and error»). Пастки вбивають і ворогів — їх можна заманювати; динаміт розчищає завали, але відкинуті вибухом блоки можуть убити самого Ріка.

## Поле і час
- Флікскрін: рівень — ланцюг екранів (усього 85 на 4 рівні за Breadbox64), вигляд збоку, тайлова сітка.
- Real-time; пастки — тайлові тригери: клітина-спусковий гачок і клітини, де зʼявляється шкода.
- Інформація прихована: тригер пастки виглядає як звичайна підлога/стіна.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Рік | player | життя, 6 куль, 6 динамітів | біжить, стрибає, лазить драбинами; стріляє, ставить динаміт, тицяє палицею |
| Підлога / платформа | terrain | — | опора |
| Стіна | static | — | блокує |
| Драбина | terrain | — | вертикальний рух |
| Руйнований блок / завал | object | — | зникає від вибуху динаміту |
| Рухомий блок | object | — | можна штовхнути палицею (?); вибух його відкидає — може вбити Ріка |
| Клітина-тригер пастки | switch | прихована | при вході запускає пастку |
| Шипи (зі стіни/підлоги) | hazard | — | висуваються за тригером; смерть |
| Дротик / спис | projectile | — | вилітає зі стіни за тригером, летить по прямій |
| Ворота, що падають | hazard | — | падають за тригером, перекривають/розчавлюють |
| Камінь, що котиться | hazard | — | у першому екрані женеться за Ріком |
| Камінь, що зсувається | hazard | — | ковзає за тригером (?) |
| Вогонь / полумʼя | hazard | — | смерть при дотику (?) |
| Ворог (Гулу, єгиптяни, нацисти) | enemy | — | патрулює або біжить на Ріка; гине від кулі, динаміту, пастки |
| Кажан / невбивний ворог | enemy | — | деякі не вмирають (?) |
| Ящик з набоями | pickup | — | поповнює кулі або динаміт |
| Скарб / бонус | pickup | очки | (?) |
| Полонений солдат | neutral | — | рятується в замку (рівень 3) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `free(next)` → ТО `move(rick, dir)`.
- КОЛИ `input(up)` → ЯКЩО `cell(here, ladder)` → ТО `move(rick, up)`; інакше `custom: «стрибок»`.
- КОЛИ `tick` → ЯКЩО `not custom: «є опора»` → ТО `fall(rick)`.
- КОЛИ `input(fire+up)` → ЯКЩО `counter(bullets, >, 0)` → ТО `spawn(bullet, front)`, `counter(bullets, -1)`.
- КОЛИ `input(fire+down)` → ЯКЩО `counter(dynamite, >, 0)` → ТО `place(rick, dynamite)`, `counter(dynamite, -1)`.
- КОЛИ `timer(fuse)` → ТО `explode(area, empty)` — завали й вороги поруч зникають.
- КОЛИ `after(explode)` → ЯКЩО `custom: «поруч рухомий блок»` → ТО `custom: «блок летить у бік вибуху»`; КОЛИ `contact(block, rick)` → ТО `lives(-1)`.
- КОЛИ `custom: «гравець у зоні вибуху»` → ТО `lives(-1)`.
- КОЛИ `input(fire+left|right)` → ТО `custom: «тицяння палицею»`; ЯКЩО `adjacent(rick, enemy)` → ТО `stun(enemy, n)` або `push(enemy)`.
- КОЛИ `contact(bullet, enemy)` → ТО `disappear_both`, `score(n)`.
- КОЛИ `enter(rick, trigger_cell)` → ТО `custom: «пастка спрацьовує: шипи/дротик/ворота/камінь у фіксованих клітинах»` (`+trigger:enter_hidden`).
- КОЛИ `enter(enemy, trigger_cell)` → ТО `custom: «пастка спрацьовує і для ворога»` — пастка вбиває будь-кого.
- КОЛИ `contact(rick, hazard)` → ТО `lives(-1)`, `respawn(rick, screen_start)` (?).
- КОЛИ `contact(rick, enemy)` → ЯКЩО `not state(enemy, stunned)` → ТО `lives(-1)`.
- КОЛИ `contact(rick, crate)` → ТО `counter(bullets|dynamite, +6)` (?), `disappear_b`.
- КОЛИ `contact(rick, treasure)` → ТО `score(n)`, `disappear_b`.
- КОЛИ `edge(rick)` → ТО `custom: «перехід на сусідній екран»`.
- КОЛИ `reach(rick, level_exit)` → ТО `next_level`.
- Перемога: пройти 4 рівні (зупинити ракету на Лондон). Поразка: 0 життів. Рахунок: вороги, скарби (?).

## Керування і ввід
- Джойстик, одна кнопка; дії — кнопка + напрямок: FIRE+вгору — постріл, FIRE+вниз — динаміт, FIRE+вліво/вправо — палиця.
- Без кнопки: вліво/вправо — біг, вгору — стрибок / драбина, вниз — драбина / присісти (?).
- Клавіатура (ZX/CPC/PC): O — вгору, K — вниз, Z — вліво, X — вправо, SPACE/ENTER — вогонь, P/H — пауза.
- Amiga: «Lock Fire» (утримання вогню) — Рік махає палицею замість утечі.

## Вікна, меню, HUD
- `splash-screen` / заставка з таблицею рекордів (?).
- `game-screen`: екран рівня + HUD угорі: `lives` (голови Ріка), кулі й динаміт (`inventory-bar`), `score`.
- `pause-menu` — пауза (P), вихід (E/Q).
- `end-screen` — game over / фінал.
- Переходи: заставка → рівень 1 (печера) → … → рівень 4 → фінал; 0 життів → game over.

## Фічі поза полем
- `levels-sequential`: 4 рівні (печера джунглів, піраміда, замок Шварцендумпф, ракетна база); між ними — продовження з початку рівня (?).
- `pause`, Atari ST/Amiga — SPACE перемикає кольоровий/чорно-білий режим.
- Збережень і паролів нема (?).

## Варіації й родичі
- Сиквел Rick Dangerous 2 (1990): палиця → кулак, кулі → лазер, динаміт → бомби, які можна копнути.
- Фан-ремейк xrick (?).
- Родичі в корпусі: [prince-of-persia](prince-of-persia.md) (пастки на клітинах, плити-тригери), [montezumas-revenge](montezumas-revenge.md) (кімнати-екрани), [kings-valley](kings-valley.md).
- Осі: **видимість пастки** (видно / прихована / фейкова); **на кого діє пастка** (лише гравець / усі); **вибух** (лише руйнує / відкидає блоки); **набої** (фіксовано / поповнюються ящиками).

## Цікавинки для курсу
- Прихована клітина-тригер, що запускає шкоду в інших клітинах (таблиця тригер → ефект) — 📎.
- Пастка вбиває і ворогів: заманити ворога на тригер — 🌱.
- Вибух відкидає блоки, які вбивають гравця — 📎.
- Дія = кнопка + напрямок (одна кнопка — три дії) — 🌱.
- Обмежені набої з поповненням ящиками — 🌱.
- Валун, що женеться за гравцем через екран — 📎.

## Мапа на каталог
- Є: `gravity-fall` · `ladder-climb` · `projectile-shot` · `bomb-fuse`, `explode-area`, `destructible-blocks` · `push-object` (палиця, ?) · `touch-death`, `environment-death`, `player-death` · `item-pickup`, `inventory-items` · `chase-player`, `enemy-patrol` · `respawn`, `checkpoint` (?) · `event-points` · `sequential-levels` · `status-panel`, `game-screen`, `game-pause` · `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+hidden-trigger-trap` «Прихована клітина-тригер запускає пастку в інших клітинах» · entities/interact · 📎 · слот {trigger, cells, effect}.
  - `+trap-kills-enemies` «Пастки діють на всіх сутностей» · entities/interact · 🌱.
  - `+blast-flings-blocks` «Вибух відкидає блоки як снаряди» · entities/combat · 📎.
  - `+fire-plus-direction` «Дія = вогонь + напрямок» · interface/input · 🌱.
  - `+limited-ammo-refill` «Ліміт набоїв з поповненням підбиранням» · entities/state · 🌱.
  - `+rolling-boulder-chase` «Валун котиться за гравцем» · entities/move · 📎.

## Пропозиції до словників
- `+trigger:enter_hidden(a, cell)` — сутність стала на приховану клітину-тригер (Rick Dangerous, Prince of Persia, Spelunky).
- `+role:trigger-cell` — невидима клітина-спусковий гачок, відмінна від видимої `switch`.
- `+card:hidden-trigger-trap`, `+card:trap-kills-enemies`, `+card:blast-flings-blocks`, `+card:fire-plus-direction`, `+card:limited-ammo-refill`, `+card:rolling-boulder-chase` — див. вище.

## Джерела
- ⭐ [Wikipedia: Rick Dangerous](https://en.wikipedia.org/wiki/Rick_Dangerous) — пістолет, обмежений динаміт, блоки, що летять від вибуху, палиця паралізує, пастки без попередження й діють на ворогів, 4 рівні, сиквел.
- [rickdangerous.co.uk: How to play](https://www.rickdangerous.co.uk/how2.htm) — 6 куль і 6 динамітів на старті, FIRE+напрямок, клавіші всіх портів, зміни Rick 2.
- [Breadbox64](https://www.breadbox64.com/c64-games/rick-dangerous) — палиця штовхає/оглушує, ящики поповнюють набої, 85 екранів.
- [TV Tropes](https://www.tvtropes.org/pmwiki/pmwiki.php/VideoGame/RickDangerous) — (з пошуку) шипи зі стін, дротики, списи, ворота, що падають, камені, фейкова пастка в Єгипті.

## Непевне
- (?) Кількість життів (пошук: 6) і чи є бонусні життя.
- (?) Куди повертає після смерті (початок екрана?) і скільки дає ящик.
- (?) Скарби/бонуси й таблиця очок; невбивні кажани.
- (?) Чи палиця штовхає блоки, чи лише ворогів; чи Рік повзає/присідає.
- (?) Типи пасток — лише з пошукових анотацій, сторінки не відкривав.
