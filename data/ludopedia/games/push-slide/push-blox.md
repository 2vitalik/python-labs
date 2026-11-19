---
title: Push Blox / Push Blox 2
slug: push-blox
aka: [Push Blox 2]
family: push-slide
also: [thinky, dig-gravity]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 2018
platforms: [PC (Windows), macOS, iOS, Android]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/894430/", best: true, note: "Push Blox 2 (27.05.2020): опис (зʼєднати однокольорові блоки; замки, конвеєри, лазери; 75 % = перемога), керування, застереження про елемент реального часу; трейлер 45 с переглянуто покадрово"}
  - {kind: steam, url: "https://store.steampowered.com/app/1366070/Push_Blox/", note: "Push Blox на Steam (02.06.2022): той самий опис, трейлер, 5 знімків (дзеркала й лазери, замки)"}
  - {kind: itch, url: "https://lonelydeckchair.itch.io/push-blox", note: "оригінал 2018: «blocks fall under gravity and stick together once in contact», 4 світи, LÖVE, демо світу 1, color-blind friendly, посилання на iOS і Android"}
  - {kind: itch, url: "https://lonelydeckchair.itch.io/push-blox-2", note: "сиквел: опис, devlog-и про бонус-рівні гравців і Hall of Push Blox Masters"}
  - {kind: other, url: "https://gottasolveit.blogspot.com/2018/09/push-blox-by-andrew-duff-199.html", note: "огляд 2018: Your Man, сірі клітини їдять, червоні в одну грудку, зібрані сині зникають, лазери, конвеєри, ключі й замки, 34 рівні"}
  - {kind: other, url: "https://lonelydeckchair.itch.io/push-blox/devlog/54299/push-blox-update-infinite-undos-undo-laser-death-keyboard-short-cuts", note: "оновлення: undo без ліміту (було 2), скасування смерті від лазера, R — рестарт, Esc — у меню"}
  - {kind: other, url: "https://lonelydeckchair.itch.io/push-blox-2/devlog/162573/bonus-level-2-reflect", note: "бонус-рівень за кодом REFLECT на екрані вибору рівня"}
  - {kind: youtube, url: "https://youtu.be/HXRYAiMVn5s", note: "Push Blox 2 Trailer (посилання з devlog автора)"}
stage: v1
coverage: 55
mechanics: [move-4dir, keyboard-controls, push-object, gravity-fall, stick-together, multi-cell-size, dig-terrain, connectivity-check, completion-detection, beam-tracing, mirror-reflect, environment-death, player-death, key-and-door, undo-unlimited, restart-level, sequential-levels, level-select, level-password, keep-playing-after-win, +connectivity-goal, +laser-blocking, +undo-after-death, +conveyor-belt, +pressure-plate, +avatar-supports-blocks, +fall-delay, +group-vanish, +hall-of-masters]
proposes: ["+trigger:beam_hit", "+effect:emit_beam", "+effect:reflect", "+axis:time=hybrid", "+card:avatar-supports-blocks", "+card:fall-delay", "+card:group-vanish", "+feature:hall-of-masters", "+feature:completion-threshold"]
author: opus
date: 2026-11-19
---

# Push Blox / Push Blox 2 — зліпи всі блоки одного кольору в одну грудку, хоча вони падають, а ти літаєш і штовхаєш

## Суть
Вид збоку з гравітацією, але лише для блоків: аватар («Your Man», кружечок) вільно літає в чотири боки, штовхає й піднімає кольорові блоки, а ті падають без опори й **злипаються з блоками свого кольору назавжди**. Мета рівня — щоб кожен колір став однією звʼязною групою. Опорою служать стіни й сірі клітини, які аватар «їсть», — і саме так він скидає блоки вниз.

Серія Lonely Deckchair (Andrew Duff): Push Blox (2018; переможець PAGY 2018 «Must Solve All the Levels»; на Steam — 2022) і Push Blox 2 (2020). Ядро однакове; сиквел додає рівнів, лазерів із дзеркалами, конвеєрів, замків і бонус-рівнів. Оглядач GottaSolveIt: серед «stick 'em»-ігор (Denki Blocks та ін.) першою з гравітацією.

## Поле і час
- Квадратна сітка, вид збоку; кімната з чорних стін на кольоровому хвилястому тлі (свій колір на світ); рівень видно цілком.
- Ходи покрокові (клітина на натиск), але падіння й конвеєри йдуть у реальному часі з короткою затримкою: розробник попереджає про «minor real-time element» без вимог до спритності. Вісь `time` поставлено `realtime` саме через це.
- Сірі клітини — шар «ґрунту»: тримають блоки, поки їх не зʼїли.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Your Man (кружечок у PB2, квадрат з обвідкою у PB 2018) | player | — | літає в 4 боки без гравітації; штовхає блоки, зокрема вгору; їсть сірі клітини; гине в промені |
| Червоний блок | object | форма з 1+ клітин | падає без опори; злипається з червоними; штовхається цілим |
| Синій блок | object | форма | так само; у PB 2018 сині, зібрані в одну грудку, зникають |
| Стіна (чорна) | static | — | непрохідна; опора |
| Сіра клітина | terrain | — | опора для блоків; Your Man її «зʼїдає» |
| Лазер (випромінювач і промінь) | hazard | напрям | промінь до першої стіни чи блока; торкнувся — смерть |
| Дзеркало: клітина з діагоналлю чи блок із діагоналлю | static | нахил | повертає промінь на 90° (кадри PB і PB2); чи рухається дзеркальний блок — (?) |
| Конвеєр (жовта стрічка з шевронами) | terrain | напрям | везе те, що на ньому лежить (?) |
| Ключ (рожева мітка в клітині) | switch | — | спрацьовує, коли клітину займає блок |
| Замок (рожевий блок із замковою щілиною) | gate | закритий / відкритий | відкривається, коли зайнято всі ключі |
| Череп (сірий значок біля конвеєрів, PB2) | hazard | — | (?) |
| Чорний одноклітинний блок (PB2) | object | — | рухається, ні з чим не злипається (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(man, dir)` — Your Man висить у повітрі: гравітація на нього не діє (кадри трейлера).
- КОЛИ `input(dir)` → ЯКЩО `cell(next_cell, gray)` → ТО `set_cell(next_cell, empty)`, `move(man, dir)` — сіру клітину зʼїдено (огляд: «Gray squares can be eaten»).
- КОЛИ `contact(man, block)` → ЯКЩО `free(cells_ahead_of_block)` → ТО `push` — блок їде цілим у будь-який бік, зокрема вгору разом із тим, що на ньому лежить; інакше `block`.
- КОЛИ `tick` → ЯКЩО `not supported(block)` → ТО `fall(block)` — опора: стіна, сіра клітина, інший блок, сам Your Man (?); падіння починається з короткою затримкою, і за неї блок ще встигають штовхнути вбік (огляд: «slide left then right immediately»).
- КОЛИ `adjacent(block_a, block_b)` → ЯКЩО `same(block_a, block_b, colour)` → ТО `merge(block_a, block_b)` — злипаються назавжди й далі падають і штовхаються одним тілом («stick together once in contact»).
- Блоки різних кольорів не злипаються: синій може лежати на червоному й їхати на ньому вгору (трейлер).
- КОЛИ `tick` → ТО `custom: «кожен випромінювач прокладає промінь по прямій до першої стіни чи блока; дзеркало повертає його на 90°»` — блоки перекривають промінь, тож їх ставлять щитом.
- КОЛИ `enter(man, beam)` → ТО `lose`, `message(«You died: press Z to undo»)` — поле сіріє (трейлер).
- КОЛИ `custom: «кожну клітину-ключ займає окремий блок»` → ТО `set_state(locks, open)` — замки бліднуть і пропускають (огляд: два ключі — по блоку на кожен; кадри трейлера).
- КОЛИ `tick` → ЯКЩО `occupied(belt_top, block)` → ТО `move(block, belt_dir)` (?) — конвеєр везе блок у бік шевронів.
- КОЛИ `settled` → ЯКЩО `connected(red)` і `connected(blue)` → ТО `win`, `next_level` — кожен колір — одна звʼязна група.
- КОЛИ `custom: «усі сині зібрано в одну грудку»` → ТО `disappear` — сині зникають (PB 2018, огляд); чи так у PB2 — (?).
- КОЛИ `input(undo)` → ТО `undo` — з оновлення 2018 без ліміту (спочатку — 2 кроки) і крізь смерть від лазера.
- КОЛИ `input(restart)` → ТО `restart`.
- Перемога: кожен колір — одна група · Поразка: смерть у промені, лікується undo · Рахунку нема; у PB2 75 % рівнів = перемога в грі, 100 % — імʼя в «Hall of Push Blox Masters».

## Керування і ввід
- WASD / стрілки — рух (у PB 2018 спершу лише стрілки, WASD додано оновленням); Z / Backspace (у PB 2018 і «u») — undo; R — рестарт; Esc — у меню; F — вікно / повний екран; Space — «run» (?).
- Один аватар; блоки рухає лише поштовхом тілом, курсора нема.
- Мобільні версії PB 2018 (iOS, Android) — дотиком (?).

## Вікна, меню, HUD
- `main-menu` — Esc з рівня повертає сюди (раніше — вихід із гри).
- `level-select` — світи й рівні з номерами «світ-рівень» (3-5, 4-4); поле для коду бонус-рівня (`level-password`: «Enter REFLECT on the level select»).
- `game-screen` — поле на хвилястому тлі; HUD нема; на першому рівні під полем — `hint-text` «Push blocks together...».
- Смерть — сіре затемнення поля з написом «You died: press Z to undo» (`custom-window`).
- Hall of Push Blox Masters — список тих, хто пройшов усе (`custom-window`) (?).
- Переходи: меню → вибір рівня → рівень → (кольори зібрано) наступний рівень; Esc → меню.

## Фічі поза полем
- `undo` без ліміту з відкатом смерті, `restart-level`, повноекранний режим (F).
- PB 2018: 4 світи, 11 гітарних тем, 34 рівні (огляд 2018); демо — світ 1; Mac-версія і демо — старіша графіка.
- PB2: щонайменше 39 рівнів (devlog «Adjustment to level 39»); 75 % → перемога, 100 % → Hall of Push Blox Masters (нові імена додаються оновленнями — devlog «New Push Blox Master!»); бонус-рівні гравців за кодом (REFLECT, набір Mountebank).
- Доступність: color-blind friendly (позначка itch).

## Варіації й родичі
- **PB 2018 → PB2**: те саме ядро; у PB2 кружечок замість квадрата, більше рівнів і механік (дзеркала, бонус-рівні), поріг перемоги 75 %.
- [Jelly no Puzzle](../thinky/jelly-no-puzzle.md) — желе падають і злипаються за кольором, але їх рухає курсор, а не аватар; коментатори itch порівнюють саме з ним.
- [Boulder Dash](../dig-gravity/boulder-dash.md) — земля, яку риє аватар, тримає камені; тут сірі клітини тримають блоки.
- [Hanano Puzzle](../thinky/hanano-puzzle.md) — гравітація й кольорові блоки; [Spell Slide](../word-number/spell-slide.md) — інша гра Lonely Deckchair з аватаром-кругляшем.
- «Stick 'em»-родичі за оглядом GottaSolveIt: Denki Blocks, Tile'M All, Jelly Slide, Blockoban, Move on Green — без гравітації.
- Осі варіацій:
  - **злипання**: нема / з усім підряд (Sokobond) / лише свій колір (тут);
  - **гравітація**: нема (Denki Blocks) / на блоки, аватар літає (тут) / на все;
  - **хто рухає**: курсор (Jelly) / аватар штовхає й піднімає (тут);
  - **мета**: блоки на цілях / кожен колір — одна група (тут) / зібрана група зникає (сині в PB 2018).

## Цікавинки для курсу
- Злипання блоків свого кольору в одне жорстке тіло й рух багатоклітинного тіла цілим — 🥉.
- Гравітація лише для блоків: аватар літає, опора з ґрунту, який аватар їсть, — 📎.
- Затримка падіння в реальному часі (вікно, щоб штовхнути вбік) поверх покрокового руху — 🥉.
- Перемога «кожен колір — одна звʼязна компонента» (flood fill) — 📎.
- Лазер із дзеркалами, перекриття блоками, смерть і undo смерті — 🥉.
- Ключі-клітини й замки — 🌱; розвʼязувач BFS зі станом «аватар + блоки + зʼїдений ґрунт» — 🥇.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ рух; `push-object` ↔ поштовх блоків; `gravity-fall` ↔ падіння; `stick-together` ↔ злипання за кольором; `multi-cell-size` ↔ злиплі тіла; `dig-terrain` ↔ сірі клітини; `connectivity-check` + `completion-detection` ↔ перевірка «колір — одна група»; `beam-tracing` + `mirror-reflect` ↔ лазер і дзеркала; `environment-death` + `player-death` ↔ смерть у промені; `key-and-door` ↔ ключі й замки; `undo-unlimited` + `restart-level`; `sequential-levels` + `level-select`; `level-password` ↔ код бонус-рівня; `keep-playing-after-win` ↔ 75 % перемога, далі до 100 %.
- Наявні нові теги: `+connectivity-goal`, `+laser-blocking`, `+undo-after-death`, `+conveyor-belt`, `+pressure-plate` (ключ-клітина).
- **Нема** → пропозиції карток:
  - `+avatar-supports-blocks` «Аватар без гравітації тримає блоки знизу й піднімає їх» · entities/move · 📎.
  - `+fall-delay` «Блок без опори падає із затримкою — за неї його ще можна штовхнути» · entities/move · 📎 · слот {delay}.
  - `+group-vanish` «Колір, зібраний в одну групу, зникає з поля» · entities/interact · 🌱.
  - `+hall-of-masters` «Імена тих, хто пройшов усе, додаються в гру оновленнями» · interface/results · 🌱.

## Пропозиції до словників
- `+trigger:beam_hit` — промінь досяг сутності (аватар у промені гине).
- `+effect:emit_beam` — випромінювач прокладає промінь до першої перешкоди; `+effect:reflect` — дзеркало повертає промінь.
- `+axis:time=hybrid` — покроковий рух аватара, але падіння й конвеєри йдуть за таймером (між `turn` і `realtime`; у шапці — `realtime`).
- `+feature:completion-threshold` — гру «виграно» на 75 % рівнів, решта — для 100 %; `+feature:hall-of-masters`.
- `+card:avatar-supports-blocks`, `+card:fall-delay`, `+card:group-vanish` — див. «Мапу на каталог».

## Джерела
- ⭐ [Steam: Push Blox 2](https://store.steampowered.com/app/894430/) — опис, керування, застереження про реальний час; трейлер 45 с (переглянуто покадрово: навчальний рівень «Push blocks together...», піднімання блоків, смерть у промені й «You died: press Z to undo», ключі й замки, конвеєри з черепами, дзеркальні блоки, фінальний рівень «PUSH BLOX»).
- [Steam: Push Blox](https://store.steampowered.com/app/1366070/Push_Blox/) і [itch.io: Push Blox](https://lonelydeckchair.itch.io/push-blox) — опис оригіналу (гравітація, злипання, 4 світи), LÖVE, демо, мобільні версії; знімки з дзеркалами.
- [GottaSolveIt: огляд Push Blox](https://gottasolveit.blogspot.com/2018/09/push-blox-by-andrew-duff-199.html) — Your Man, кольори клітин, сині зникають, лазери, конвеєри, ключі й замки, 34 рівні, ліміт undo, родичі «stick 'em».
- [itch.io: Push Blox 2](https://lonelydeckchair.itch.io/push-blox-2) і devlog-и — 75 % / 100 %, бонус-рівні, нові «майстри», рівень 39.
- [Devlog: infinite undos](https://lonelydeckchair.itch.io/push-blox/devlog/54299/push-blox-update-infinite-undos-undo-laser-death-keyboard-short-cuts) — undo, R, Esc, WASD, перестановка рівнів світів 3–4.

## Непевне
- (?) Чи тримає Your Man блок, що стоїть на ньому, і скільки триває затримка падіння; що робить «SPACE to run».
- (?) Що саме роблять черепи біля конвеєрів, чорний одноклітинний блок і помаранчеві кільця на стінах у PB2; чи везе конвеєр самого Your Man.
- (?) Чи рухаються дзеркальні блоки і чи злипаються вони за кольором.
- (?) Чи зникають зібрані сині в PB2; скільки рівнів і світів у PB2.
- (?) Чи штовхає Your Man ряд із кількох блоків різних кольорів.
