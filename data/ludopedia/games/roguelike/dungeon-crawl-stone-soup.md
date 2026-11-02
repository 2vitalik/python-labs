---
title: Dungeon Crawl Stone Soup
slug: dungeon-crawl-stone-soup
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2006
platforms: [Windows, macOS, Linux, Android, web (WebTiles), SSH]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dungeon_Crawl_Stone_Soup", best: true, note: "огляд: мета (3 з 15 рун → Орб Зота), види/передісторії/боги, філософія «без нудьги», автодослідження"}
  - {kind: docs, url: "https://raw.githubusercontent.com/crawl/crawl/master/crawl-ref/docs/crawl_manual.rst", note: "офіційний посібник: екран, усі клавіші, навички, релігія, Зот"}
  - {kind: docs, url: "https://raw.githubusercontent.com/crawl/crawl/master/crawl-ref/source/dat/descript/features.txt", note: "описи всіх клітин: вода, лава, двері, дерева, пастки, люки, телепорти, стіни"}
  - {kind: official, url: "http://crawl.develz.org/", note: "сайт гри, завантаження"}
  - {kind: other, url: "https://github.com/crawl/crawl", note: "сирці (C++/Lua), GPL"}
  - {kind: play, url: "http://crawl.akrasiac.org/", note: "публічний сервер: WebTiles у браузері, рекорди, записи ігор"}
  - {kind: fandom, url: "http://crawl.chaosforge.org/", note: "CrawlWiki — довідник спільноти (агенту не відкрився)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=dungeon+crawl+stone+soup+webtiles+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-8dir, dungeon-generation, hp-damage, inventory-items, item-pickup, chase-bfs, floor-types, environment-death, impassable-cells, teleport-random-exit, melee-vs-ranged, projectile-shot, shop-catalog, sequential-levels, player-death, collect-quota, minimap-radar, status-panel, console-render, gui-render, +auto-explore, +travel-command, +fov-shadowcast, +item-identification, +skills-training]
proposes: ["+trigger:noise", "+trigger:stairs_taken", "+trigger:zot_attention", "+cond:can_swim", "+cond:flying", "+cond:piety", "+effect:identify", "+effect:fall_levels", "+effect:alert", "+effect:cloud", "+role:cloud", "+role:altar", "+role:stairs", "+ui:noise-bar", "+ui:monster-list", "+window:skills-window", "+window:god-window", "+window:dungeon-overview", "+window:map-window", "+window:character-select", "+feature:auto-explore", "+feature:travel", "+feature:online-spectate", "+axis:control=indirect"]
author: opus
date: 2026-11-02
---

# Dungeon Crawl Stone Soup — класичний великий роглайк, з якого прибрали нудьгу: автодослідження, подорожі, навички, боги

## Суть
Вільний роглайк (форк Linley's Dungeon Crawl 1997, з 2006): персонаж = вид × передісторія, що спускається Підземеллям і бічними гілками, збирає щонайменше 3 з 15 рун Зота, бере Орб Зота й тікає на поверхню. Від класики відрізняється філософією «прибери все, що нудне або завжди однаково правильне»: автодослідження й подорож однією клавішею, ніякої їжі, навички тренуються розподілом досвіду, боги — це окремі набори правил. Ядро на клітинах — тактика місцевості: двері, коридори, сходи, вода, лава, хмари, пастки й люки.

## Поле і час
- Квадратна сітка поверху (≈80×70 (?)), 8 напрямків; вид — консоль (ASCII) або тайли, локально чи в браузері (WebTiles).
- Видимість — поле зору з лінією видимості навколо `@` (яскраве); поза ним — сірий «памʼятний» шар з уже баченим; стіни, дерева, закриті двері, дим блокують зір.
- Покроково з **тривалістю дій**: хід має «вартість» (у панелі `Time` і в дужках — тривалість останньої дії); швидкі монстри діють частіше.
- Структура світу: Dungeon (15 поверхів) + гілки (Temple, Lair, Orcish Mines, Elven Halls, 2 з 4 «рунних» Swamp/Shoals/Snake/Spider, Vaults, Crypt, Tomb, Slime Pits, Depths, Zot) + Abyss, Pandemonium, Hells + тимчасові портали (базар, сховище тощо).
- Зот-«годинник»: довге перебування на одному місці — Зот помічає; спуск/нова область скидає; контакт — постійна втрата здоровʼя.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Персонаж `@` | player | вид (27), передісторія (26), XL, HP/MP, AC/EV/SH, Str/Int/Dex, навички 0–27, бог+побожність | рух/удар 8 напрямків; закляття, предмети, здібності |
| Монстр (літера) | enemy | HP, швидкість, атаки, закляття, сприйняття | спить / блукає / помітив → переслідує найкоротшим шляхом; кидає закляття з лінії видимості |
| Унікальний / бос | boss | імʼя | особливий монстр з набором заклять |
| Союзник | ally | — | від бога / закляття; йде за тобою, сходами — якщо поряд |
| Підлога `.` / стіна `#` | terrain / static | стіна: камінь, кристал (відбиває вогонь/холод), метал (заземлює блискавку), вічна | стіна — блокує рух і зір; кам'яна руйнується копанням |
| Двері `+` / `'` | gate | закриті / відчинені / зламані / рунні / запечатані | відкриваються кроком; закриті блокують зір; монстри з руками відчиняють |
| Мілка вода | terrain | — | не-плавці бредуть повільно й можуть промахнутися в ближньому бою; великі — без штрафу |
| Глибока вода | terrain | — | лише велетні бредуть, плавці пливуть, решта — летіти |
| Лава | terrain | — | перетнути — політ або іммунітет; ступити — смерть |
| Токсичне болото | terrain | — | шкода й отрута всім у ньому |
| Дерево / мангр | static | горить | блокує рух і зір; вогонь поширюється на сусідні дерева |
| Хмара (вогонь, холод, отрута, пара, дим…) | hazard | тривалість | шкода/стан тому, хто стоїть; дим блокує зір |
| Сходи `<` `>` | static | 3 пари на поверх (?) | перехід; сусідні монстри йдуть слідом (крім безмозкої нежиті) |
| Люк (escape hatch) | static | вгору/вниз, односторонній | швидкий вихід на сусідній поверх |
| Шахта (shaft) | hazard | — | падаєш на 1+ поверхів униз |
| Пастки | hazard | alarm, net, web, teleport (разова/постійна), dispersal, zot, pressure plate, archmage's, harlequin's, tyrant's, devourer's | спрацьовують при вході; багато видимі й можуть спрацювати від монстрів |
| Транспортер / прохід Голубрії | terrain | односторонній | переносить в іншу точку поверху |
| Арка порталу / ворота гілки `\` | static | — | вхід у гілку, портал, крамницю |
| Вівтар `_` | static | бог | крок + `<`/`>` — стати послідовником |
| Крамниця | static | лише продаж | купити за золото; `$` — список бажаного |
| Предмети | pickup | `)` зброя, `(` метальні, `[` броня, `?` сувої, `!` зілля, `/` жезли, `=` кільця, `"` амулети, `|` посохи, `:` книги, `%` талісмани, `}` різне, `$` золото | підбираються `g`/`,` (і автопідбір) |
| Руна Зота | pickup | 15 у грі | 3+ відкривають Realm of Zot |
| Орб Зота | pickup | — | взяв — тікай до D:1 |
| Самоцвіт гілки | pickup | — | Зот розбиває, якщо задовго в гілці (без Орба) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `occupied(cell, monster)` → ТО удар (влучання vs EV, шкода − AC); ЯКЩО `cell(closed_door)` → ТО `set_cell(open_door)`; ЯКЩО `free(cell)` → ТО `move(player, dir)`.
- КОЛИ `input(o)` (автодослідження) → ТО `custom: «кроки до найближчої недослідженої клітини, підбір предметів»` доки `line_of_sight(player, hostile)` або нове цікаве → стоп.
- КОЛИ `input(G|X+Enter|_)` → ТО `custom: «подорож найкоротшим шляхом (між поверхами — теж)»`, зупинка при ворогові.
- КОЛИ `enter(a, shallow_water)` → ЯКЩО `not can_swim(a)` і `not large(a)` → ТО `speed(a, slow)`, `custom: «штраф ближнього бою»`.
- КОЛИ `input(dir into deep_water|lava)` → ЯКЩО `not can_swim` і `not flying` → ТО `block` (лава: свідомо — смерть).
- КОЛИ `turn_end` → ЯКЩО `occupied(cell, cloud)` → ТО ефект хмари (`damage`, `set_state(poisoned|confused)`); хмара: `timer` → `disappear`.
- КОЛИ `enter(a, trap)` → ТО ефект пастки: alarm — `alert(all monsters on level)`; net/web — `set_state(a, caught)`; teleport — `teleport(a, random)`; dispersal — `teleport(all in view, nearby)`; zot — `custom: «випадкове лихо»`.
- КОЛИ `enter(player, shaft)` → ТО `fall_levels(1+)`; КОЛИ `input(<|>)` на люку → ТО односторонній перехід.
- КОЛИ `input(<|>)` на сходах → ТО новий поверх; `adjacent(monster, player)` → монстр іде слідом; на новому поверсі гравець ходить першим (тактика «сходовий танець»).
- КОЛИ дія → ТО `noise(level)`; КОЛИ `noise` досягає монстра → ЯКЩО `prob(perception vs stealth)` → ТО `set_state(monster, awake)` → `chase-bfs`.
- КОЛИ `hp_zero(monster)` → ТО `counter(xp, +n)` → розподіл по навичках, що тренуються (виділені — більша частка); КОЛИ `counter(xp_pool, >=, threshold)` → ТО XL +1 (HP/MP/характеристики).
- КОЛИ `input(q|r)` невідомого зілля/сувою → ТО ефект, `identify(type)` назавжди для партії; сувій identify — розкриває обраний предмет; жезли показують заряди при підборі.
- КОЛИ `input(z)` → ЯКЩО `count(mp, >=, cost)` → ТО закляття; `prob(fail%)` → провал/miscast (шанс залежить від навичок шкіл, Int, броні).
- КОЛИ `contact(player, altar)` + `input(<|>)` → ТО `custom: «стати послідовником бога»`; дії, які бог любить → `piety(+)`; `input(a: renounce)` → ТО `custom: «кара покинутого бога»`.
- КОЛИ `turns_in_area(> limit)` → ТО `custom: «Зот помітив»` → `drain(max_hp)`; КОЛИ `stairs_taken` у нову область → ТО лічильник скинуто.
- КОЛИ `counter(runes, >=, 3)` → ТО `unlock(Zot)`; КОЛИ `picked(orb)` і `reach(player, D:1 exit)` → ТО `win`.
- КОЛИ `hp_zero(player)` → ТО `lose` (permadeath; на сервері лишається «привид» для інших гравців).
- Перемога: Орб + вихід на поверхню (більше рун — більше очок). Поразка: смерть. Рахунок: функція рун, глибини, XL і швидкості (кількості ходів).

## Керування і ввід
- Рух `hjklyubn` / цифрова клавіатура / стрілки; `Shift+напрям` — біг (стоп, щойно видно ворога); миша (тайли) — клік по клітині: подорож.
- Автоматизація: `o` — автодослідження, `G`/`Ctrl-G` — подорож на будь-який поверх, `X` — мапа поверху з курсором (Enter — йти; `<` `>` — до сходів), `Tab` — автобій з найближчим, `Shift-Tab`/`p` — автопостріл, `5` — відпочити до повних HP/MP.
- Бій і цілі: `f`/`F`/`v` стріляти, `Q` колчан, `+`/`-` перемикати ціль, `Esc` — скасувати без втрати ходу.
- Предмети: `g`/`,` підібрати, `d` кинути, `i` інвентар, `w W T P R r q V`, `{` підписати, `\` відкриття (відомі типи).
- Закляття: `M` вивчити з книги, `z` кастувати, `I` список. Релігія: `^`; здібності: `a`.
- Інфо: `x` оглянути, `Ctrl-X` список монстрів/обʼєктів, `Ctrl-O` огляд підземелля, `Ctrl-F` пошук предметів/крамниць/вівтарів, `m` навички, `@`/`%` персонаж, `A` мутації, `?` довідка.

## Вікна, меню, HUD
- `game-screen` — мапа (`fog-overlay`: яскраве видиме / сіре памʼятне) + права панель (`stat-panel`: імʼя, вид, бог + `piety`-зірочки, HP, MP, AC, EV, SH, Str/Int/Dex, XL, Place `Dungeon:1`, `noise-bar`, Time; статуси нижче) + `monster-list` (видимі монстри з кольоровою оцінкою загрози) + `message-log` знизу.
- `map-window` (`X`) — мапа поверху на весь екран з курсором для подорожі.
- `dungeon-overview` (`Ctrl-O`) — дерево відвіданих гілок/поверхів, вівтарі, крамниці, руни.
- `skills-window` (`m`) — список навичок з рівнем, аптитудами, перемикачем авто/вручну, ціллю тренування.
- `god-window` (`^`) — бог, побожність, можливості, що він любить і ненавидить.
- `inventory-window` (`i`), `spell-list` (`I`/`z`), `character-sheet` (`%`), `log-window` (`Ctrl-P`), `help-window` (`?`).
- `shop-window` — товари з літерами, ціни, `$`-список бажаного.
- `character-select` — вид → передісторія (з рекомендаціями), або випадково; `mode-select`: звичайна гра, туторіал, Sprint, seeded.
- `end-screen` — морг-файл: причина смерті, характеристики, історія; `leaderboard` на сервері.
- Переходи: `main-menu` → `mode-select` → `character-select` → `game-screen` ⇄ модальні вікна (Esc назад); смерть/перемога → `end-screen` → меню.

## Фічі поза полем
- `auto-explore`, `travel` (і між поверхами), автопідбір, автобій — автоматизація нудних дій як принцип дизайну.
- Режими: класична гра, `tutorial`, Sprint (короткі арени), `seed-input` (seeded game, `?V` — показати seed).
- Онлайн-сервери: `online-spectate` (дивитися чужу гру наживо), записи ігор (`replay`), `leaderboard-online`, привиди загиблих гравців, турніри двічі на рік.
- `remap-controls` (keymaps і макроси `~`), налаштування в init-файлі, консоль/тайли (`theme-select`).
- Без `undo`; сейв — лише при виході (`mode-hardcore`).

## Варіації й родичі
- Linley's Dungeon Crawl (1997) → DCSS (2006, вільна розробка, ~2 релізи на рік); видалення видів, шкіл, їжі як ідеологія (менше роздутості).
- Родичі: Rogue/NetHack (класика), Brogue (рідини й гази як автомати), Angband (глибина), Tales of Maj'Eyal.
- Осі варіацій: **автоматизація** (нема / біг / автодослідження + подорож + автобій) · **тиск часу** (голод / Зот-годинник / нема) · **прогресія** (класи / вид×передісторія + навички довільно) · **ідентифікація** (усе / лише зілля й сувої / нема).

## Цікавинки для курсу
- Автодослідження: BFS до найближчої недослідженої клітини з правилами зупинки (ворог, предмет, небезпека) — 🥉.
- Подорож між поверхами: граф поверхів + шлях на кожному поверсі — 🥈.
- Поле зору (shadowcasting) + памʼятна мапа + блокування зору дверима/деревами/димом — 🥉.
- Вода/лава/болото: прохідність за властивостями сутності (плаває, летить, велика) — 📎 (таблиця «клітина × властивість → дозвіл/штраф»).
- Хмари як тимчасові клітинні сутності з тривалістю й ефектом; вогонь, що перекидається на дерева — 🥈 (клітинний автомат).
- Пастки-сімейство (тривога, сітка, телепорт, розсіювання, шахта на N поверхів) — 📎 кожна, 🥉 за сімʼю.
- Навички: розподіл досвіду між вибраними навичками з аптитудами — 📎; боги з побожністю — 🥈.
- Шум і стелс: дія → гучність → монстри в радіусі прокидаються з імовірністю — 📎.

## Мапа на каталог
- Є: `move-8dir` · `dungeon-generation` (поверхи + вольти) · `hp-damage` · `inventory-items` · `item-pickup` · `chase-bfs` · `floor-types` (вода, лава, болото) · `environment-death` (лава, утоплення) · `impassable-cells` · `teleport-random-exit` (пастка телепорту) · `melee-vs-ranged` · `projectile-shot` (метальні, закляття) · `shop-catalog` · `sequential-levels` · `player-death` · `collect-quota` (3 з 15 рун) · `minimap-radar` (тайли) · `status-panel` · `console-render` + `gui-render` (дві оболонки — близько до `dual-frontends`).
- **Нема** → пропозиції карток:
  - `+auto-explore` «Автодослідження до недослідженого з правилами зупинки» · interface/input · 🥉.
  - `+travel-command` «Подорож до точки/поверху найкоротшим шляхом» · interface/input · 🥈 · слот {interlevel}.
  - `+fov-shadowcast` «Поле зору тіньовим литтям + памʼятна мапа» · entities/visibility · 🥉 · слот {radius}.
  - `+item-identification` «Невідомі типи предметів» · entities/state · 📎.
  - `+skills-training` «Досвід розподіляється по вибраних навичках» · entities/state · 📎.
  - `+cloud-cells` «Хмари: тимчасові клітинні ефекти з тривалістю» · entities/hazard · 🥈.
  - `+terrain-permits` «Прохідність клітини за властивістю сутності (плаває/летить/велика)» · entities/legality · 📎.
  - `+trap-family` «Пастки з різними ефектами (тривога, сітка, телепорт, шахта)» · entities/interact · 🥉.
  - `+noise-stealth` «Шум дій будить монстрів» · entities/ai · 📎.
  - `+stairs-follow` «Сусідні монстри йдуть слідом сходами» · rules/progress · 🌱.
  - `+god-piety` «Бог: побожність, дари, заборони» · rules/meta · 🥈.

## Пропозиції до словників
- `+trigger:noise` — дія створила шум рівня N; `+trigger:stairs_taken` — сутність перейшла сходами; `+trigger:zot_attention` — лічильник перебування в області перевищено.
- `+cond:can_swim`, `+cond:flying` — властивості пересування для прохідності клітин; `+cond:piety` — побожність ≥ N.
- `+effect:identify` — розкрити тип предмета; `+effect:fall_levels` — впасти на N поверхів; `+effect:alert` — розбудити/привернути всіх на поверсі; `+effect:cloud` — створити хмару на клітинах з тривалістю.
- `+role:cloud` — тимчасова сутність-клітина зі строком життя (ширше за `hazard`); `+role:altar`; `+role:stairs`.
- `+ui:noise-bar` — індикатор гучності останньої дії; `+ui:monster-list` — список видимих ворогів з оцінкою загрози.
- `+window:skills-window`, `+window:god-window`, `+window:dungeon-overview` — огляд гілок і поверхів; `+window:map-window` (⏳), `+window:character-select` (⏳).
- `+feature:auto-explore`, `+feature:travel`, `+feature:online-spectate` — дивитися чужі ігри наживо на сервері.
- `+axis:control=indirect` — тут і `direct` (клавіші), і `indirect` (автодослідження, подорож, клік).

## Джерела
- ⭐ [Wikipedia: Dungeon Crawl Stone Soup](https://en.wikipedia.org/wiki/Dungeon_Crawl_Stone_Soup) — мета, види/передісторії/боги (0.33), філософія дизайну, сервери.
- [Crawl manual (rst)](https://raw.githubusercontent.com/crawl/crawl/master/crawl-ref/docs/crawl_manual.rst) — панель, клавіші, навички, шум, двері/сходи, релігія, Зот.
- [features.txt](https://raw.githubusercontent.com/crawl/crawl/master/crawl-ref/source/dat/descript/features.txt) — описи всіх клітин: вода, лава, болото, двері, дерева, пастки, шахти, люки, транспортери, стіни.
- [crawl.develz.org](http://crawl.develz.org/) · [GitHub](https://github.com/crawl/crawl) · [CAO-сервер](http://crawl.akrasiac.org/) — гра, сирці, онлайн.
- YouTube: пошук «dungeon crawl stone soup webtiles gameplay».

## Непевне
- (?) Розмір поверху ≈80×70, «3 пари сходів на поверх», точні глибини гілок і 4 «рунні» гілки, з яких 2 на гру — з памʼяті; посібник цього не перелічує.
- (?) Перелік хмар (вогонь, холод, отрута, мефітна — сплутання, пара, дим, міазми) — з памʼяті; features.txt хмар не описує.
- (?) Школи магії (Conjurations, Hexes, Summonings, Necromancy, Translocations, Fire, Ice, Air, Earth, Alchemy, Forgecraft) змінювались між версіями — склад для 0.33/0.34 не звірено.
- (?) Деталі Зот-годинника (ліміт ходів, скільки max HP знімає) — посібник описує лише якісно.
- (?) Символ вівтаря `_` і дверей `'` — з памʼяті (посібник не називає).
