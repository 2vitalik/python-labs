---
title: 3D Lemmings
slug: 3d-lemmings
aka: [Lemmings 3D, 3D Лемінги]
family: dig-gravity
also: [grid-platformer]
klass: cursor
axes:
  field: 3d
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 1995
platforms: [MS-DOS, PlayStation, Sega Saturn]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/3D_Lemmings", best: true, note: "огляд: 4 камери, Virtual Lemming, нове вміння Turner (90°), діагональні блоки, 4 × 20 рівнів + 20 практики, паролі, повтор"}
  - {kind: other, url: "https://archive.org/stream/3d_lemmings_english/3d_lemmings_english_djvu.txt", note: "мануал (OCR): панелі, 9 умінь, камери, батути, пружини, телепорти, мати, сплітери, слизькі блоки, канатки, меню й опції"}
  - {kind: other, url: "https://archive.org/stream/1995_Lemmings_3D_Companion_Draft/1995_Lemmings_3D_Companion_Draft_djvu.txt", note: "неопублікований гайд Prima (OCR): блоки й пів-блоки, односторонні, дефлектори, падіння «оглушення / смерть», ліміти часу, цілі рівнів"}
  - {kind: other, url: "https://www.lemmingsforums.net/index.php?board=40.0", note: "Loap — фанатське відтворення 3D Lemmings у стилі NeoLemmix (дошка форуму)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=3D+Lemmings+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [gravity-fall, move-auto, turn-when-blocked, dig-terrain, dig-hole, destructible-blocks, impassable-cells, one-way-cell, height-levels, inertia-slide, teleport-pair, bomb-fuse, explode-area, environment-death, time-out, reach-exit, collect-quota, spawn-points, cell-click, game-pause, level-password, sequential-levels, difficulty-levels, status-panel, minimap-radar, replay, +assign-skill, +tool-allotment, +release-rate, +nuke-all, +fall-height-death, +camera-orbit, +first-person-view, +multi-camera, +turner-redirect, +deflector-block, +splitter-balance, +spring-jump, +rope-slide, +crash-mat]
proposes: ["+trigger:landed", "+cond:fall_height", "+effect:excavate", "+ui:camera-buttons", "+feature:replay-to-last-action", "+axis:control", "+axis:actors", "+card:multi-camera", "+card:turner-redirect", "+card:deflector-block", "+card:rope-slide", "+card:crash-mat"]
author: opus
date: 2026-11-19
---

# 3D Lemmings — ті самі лемінги, але рівень зібрано з блоків у 3D: уміння Turner повертає юрбу на 90°, а камер чотири

## Суть
Сиквел [Lemmings](lemmings.md) від Clockwork Games (Psygnosis, 1995), що виріс із прототипу Cubewalker. Ядро те саме: лемінги виходять із люка й ідуть самі, гравець курсором роздає їм уміння з ліміту рівня, щоб довести до виходу потрібну кількість. Нове — **рівень як тривимірна сітка блоків**: юрба йде по верхніх гранях у чотирьох напрямках, тому зʼявились повороти на 90° (уміння **Turner**, блоки-дефлектори, сплітери), пристрої (батути, пружини, телепорти, канатки, мати) і **керування камерами** — чотири вільні камери та вид очима лемінга. Тут — лише відмінності від першої частини.

## Поле і час
- Рівень — 3D-сітка блоків із пів-блоками; лемінг переступає перепад у пів-блока. Будівник і копачі працюють «клітинами сітки» (grid squares); блок приблизно дві клітини заввишки для частини дій (гайд).
- Край блока — прірва: лемінг, якого нічого не зупинило, сходить і падає; стіна — розворот на 180°.
- Падіння двоступеневе: помірне — лемінг «оглушений» на мить, далеке — гине; Floater і мат рятують з будь-якої висоти.
- Real-time; пауза зупиняє лемінгів і таймер, але камери далі рухаються. Ліміт часу рівня — від 4:00 до 12:00 (гайд).
- Видимість: стан рівня відкритий, але 3D-перекриття ховає частину; до деяких кімнат камера не проходить — дивитись у вікна або очима лемінга.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Лемінг | ally | напрямок N/E/S/W; стан-уміння; прапорці Climber/Floater | іде вперед гранями блоків; стіна → розворот; край → падіння |
| Люк | spawner | кількість, release rate | випускає лемінгів по одному |
| Вихід | gate | — | лемінг заходить → врятований |
| Звичайний блок | terrain | — | копається Basher / Miner / Digger, руйнується вибухом |
| Незнищенний блок | static | «дзенькає» при ударі | не копається; незнищенні також земля, входи, виходи, пастки |
| Пів-блок | terrain | висота ½ | на нього можна переступити (?) |
| Односторонній блок | terrain | стрілка | пробивають лише Basher, Bomber, Miner і лише з боку стрілки |
| Слизький блок («лід») | terrain | — | лемінг ковзає в напрямку ходу до звичайного блока |
| Блок-дефлектор | static | скошена / пласка грань | скошена грань повертає на 90°, пласка — на 180° |
| Блок-сплітер | static | 4 проходи | ділить потік на дві колони: наступний лемінг повертає в інший бік |
| Батут червоний / синій | object | ±1 блок за відскок | підкидає вперед-угору; червоний додає висоту й дальність, синій забирає; багато лемінгів разом |
| Пружина | object | ціль — задана точка | кидає одного лемінга в задане місце; решта йде повз |
| Телепорт | gate | пара | переносить одного лемінга за раз; виходить у тому ж напрямку |
| Канатна дорога | object | один напрямок | везе одного лемінга за раз до кінця |
| Мат | terrain | — | падіння з будь-якої висоти без оглушення й смерті |
| Вода · лава · грязь | hazard | — | лемінг гине |
| Пастки (капкани, стомпери, лазерні промені) | hazard | — | убивають лемінга, що зайшов |
| Turner | — (стан лемінга) | ліво / право на вибір | стоїть; кожного, хто підійшов, повертає на 90°; знімається лише вибухом або підкопом |
| Blocker | — (стан лемінга) | діє з двох напрямків | стоїть; розвертає на 180° тих, хто йде на нього вздовж його осі (?) |
| Builder | — (стан лемінга) | 6 сходинок | будує сходи під фіксованим кутом; стоп — стіна, стеля, кінець цеглин; далі знову ходить |
| Basher | — (стан лемінга) | — | б'є тунель уперед по пів блока; шукає блок лише на 1 клітину попереду |
| Miner | — (стан лемінга) | ≈ 30° | копає по діагоналі вниз: ⅓ блока вниз — і вперед |
| Digger | — (стан лемінга) | — | копає шахту вниз із центру клітини; незнищенне зупиняє, порожнеча — падає |
| Climber · Floater · Athlete | — (стан лемінга) | постійні | лізе стінами, що торкаються площини ходу / парасолька / обидва |
| Bomber | — (стан лемінга) | відлік 5 | іде ще ≈ 1,5 клітини, вибухає; руйнує сусідні блоки й підлогу під собою |
| Камера ×4 | — (інструмент гравця) | позиція, кут | рухається й обертається, не нахиляється, має «масу» — не пролазить у вузькі дірки |

## Правила (КОЛИ → ЯКЩО → ТО)
Лише нове відносно [Lemmings](lemmings.md).
- КОЛИ `tick` → ЯКЩО `state(lemming, walker)` і `custom: «попереду край блока»` → ТО `move(lemming, facing)`, `fall(lemming)` (на краю не розвертається).
- КОЛИ `custom: «лемінг приземлився»` (`+trigger:landed`) → ЯКЩО `custom: «висота між порогами»` (`+cond:fall_height`) → ТО `stun(lemming, n)`; вище за верхній поріг → `disappear`.
- КОЛИ `custom: «лемінг приземлився»` → ЯКЩО `state(lemming, floater)` або `cell(landing, crash_mat)` → ТО `custom: «без оглушення й смерті»`.
- КОЛИ `input(turner, lemming)` → ТО `choose(left|right)` (екранна стрілка, другий клік), `set_state(lemming, turner)`, `counter(turner_left, -1)`.
- КОЛИ `contact(walker, turner)` → ТО `face(walker, turner_dir)` (90°); Turner сам знімається лише `explode` або підкопом.
- КОЛИ `contact(walker, blocker)` → ЯКЩО `custom: «іде вздовж осі блокера»` → ТО `face(walker, reverse)`.
- КОЛИ `input(blocker, lemming)` → ЯКЩО `state(lemming, walker|builder|basher|miner)` → ТО `set_state(lemming, blocker)`; інакше `sound(«Uh Oh»)`, `block`.
- КОЛИ `custom: «під Blocker прибрано опору»` → ТО `set_state(blocker, walker)`.
- КОЛИ `tick` → ЯКЩО `state(lemming, builder)` і `counter(steps, <, 6)` → ТО `set_cell(step, terrain)`, `move(lemming, step_up)`; 6 сходинок, стіна або стеля → `set_state(lemming, walker)`.
- КОЛИ `contact(lemming, deflector)` → ЯКЩО `custom: «скошена грань»` → ТО `face(lemming, ±90)`; інакше `face(lemming, reverse)`.
- КОЛИ `enter(lemming, splitter)` → ТО `face(lemming, left|right)`, `custom: «наступному — протилежний бік»`.
- КОЛИ `enter(lemming, slippery)` → ТО `slide(lemming, facing)` до звичайного блока; під час ковзання — лише Bomber (мануал: ще Climber і Floater).
- КОЛИ `custom: «Basher / Miner / Bomber бʼє в односторонній блок»` → ЯКЩО `facing(lemming, arrow_dir)` → ТО `set_cell(block, empty)`; інакше `block`, `set_state(lemming, walker)`.
- КОЛИ `custom: «копач бʼє в незнищенне»` → ТО `sound(clank)`, `set_state(lemming, walker)`.
- КОЛИ `enter(lemming, trampoline)` → ТО `bounce(lemming)`, `custom: «висота й дальність відскоку: червоний +1 блок, синій −1»`.
- КОЛИ `enter(lemming, spring)` → ЯКЩО `free(spring)` → ТО `custom: «кидок у задану точку»`; інакше `custom: «іде повз»`.
- КОЛИ `enter(lemming, teleporter)` → ЯКЩО `free(teleporter)` → ТО `teleport(lemming, pair)`, `face(lemming, same)`.
- КОЛИ `enter(lemming, rope_slide)` → ЯКЩО `free(rope_slide)` → ТО `move(lemming, rope_end)` (лише в один бік).
- КОЛИ `enter(lemming, water|lava|mud|trap)` → ТО `disappear`, `counter(dead, +1)`.
- КОЛИ `input(bomber, lemming)` → ТО `set_state(lemming, countdown, 5)`.
- КОЛИ `state_off(lemming, countdown)` → ТО `explode(area, into: empty)` (сусідні блоки й підлога під ним, крім незнищенних), `disappear`.
- КОЛИ `counter(time_left, ==, 0)` → ТО `custom: «усі лемінги на полі стають Bomber»`.
- КОЛИ `input(nuke)` (подвійний клік) → ТО `custom: «Armageddon: усі вибухають»`, `restart`.
- КОЛИ `input(release_plus|release_minus)` → ЯКЩО `custom: «люк ще випускає»` і `custom: «не нижче стартового, не вище 99»` → ТО `counter(release_rate, ±1)`.
- КОЛИ `input(virtual, lemming)` → ТО `camera(first_person(lemming))`; уміння, призначені в цьому режимі, йдуть цьому лемінгу; голову можна повернути на 90° (крім Basher, Digger, Miner).
- КОЛИ `input(highlight, lemming)` → ТО `set_state(lemming, selected)`: усі наступні вміння — йому, доки не зняти.
- КОЛИ `input(retry)` → ЯКЩО `custom: «повтори увімкнено»` → ТО `custom: «автоповтор записаних дій до останньої, потім керування гравцеві»`.
- КОЛИ `custom: «лемінгів на полі нема й люк порожній»` → ЯКЩО `counter(saved, >=, target)` → ТО `win`, `next_level`; інакше `lose`, `restart`.
- Перемога: врятовано не менше цілі рівня (у гайді — числом, напр. «10 з 10», «60 з 80»). · Поразка: ціль не набрано. · Рахунок: лише IN / OUT.

## Керування і ввід
- Миша: лівий клік — вибір, правий — назад; утримання правої + рух — обертання й рух камери, смуга прокрутки — висота камери. Джойпад: X / O, L2/R2 — перебір умінь, R1 — іконки, L1 — вільніший рух камери, Start — пауза.
- Turner — два кліки: лемінг, потім стрілка напрямку. Highlight Lemming (стрілка) — закріпити одного лемінга під усі вміння.
- Чотири камери: перемикання іконкою / R1; на деяких рівнях камери фіксовані; нахилити вгору-вниз не можна.
- Virtual Lemming (іконка-обличчя) → клік по лемінгу: вид його очима (до 180°), поворот голови на 90°.
- Керування **непряме**, як у першій частині; новий навик — **читати 3D-сцену** камерою, щоб влучити в потрібного лемінга й момент.

## Вікна, меню, HUD
- `main-menu`: Play · Level Select · Codes · Options · Load/Save.
- `level-select`: рейтинги FUN / TRICKY / TAXING / MAYHEM + PRACTICE.
- `level-password` (Codes): пароль, щоб перескочити пройдені рівні.
- `settings-window` (Options): Mono/Stereo, гучність музики й звуку, швидкість курсора, положення екрана, порт контролера, повтори On/Off, прозорість мапи, налаштування кнопок (джойпад), ліво-/праворука миша.
- `game-screen`: 3D-вид камери; нижня панель — Highlight, Virtual Lemming, 9 умінь із лишком на кожному (`ability-buttons`); права панель — `remaining-counter` IN (скільки ще треба врятувати, зеленіє після цілі), OUT (скільки на полі), `timer-countdown`, бомба (нюк / рестарт), `fast-forward`, камера (`+ui:camera-buttons`), мапа, `pause-button`, обертання вліво/вправо, потік +/−.
- `minimap` — огляд згори в лівому верхньому куті, типово вимкнений.
- Повтор спроби (`replay-window`): автоповтор, X — перехопити керування, O — прискорити.
- Катсцени на певних віхах (`dialogue-window`).
- Переходи: main-menu → level-select / Codes → рівень → (ціль набрано) наступний рівень / (ні) повтор з автоповтором.

## Фічі поза полем
- `levels-sequential`: 4 рейтинги × 20 рівнів + 20 практичних (`mode-practice`); `level-password`; Load/Save (`save-slots`?).
- `replay` з перехопленням керування (`+feature:replay-to-last-action`), `speed-control` (fast forward), `pause`.
- `remap-controls` (джойпад), ліво-/праворука миша, прозорість мінімапи.
- 3D Lemmings Winterland (ПК) — пак із 6 зимових рівнів з тим самим геймплеєм.
- Фанатське відтворення Loap (у стилі NeoLemmix) — сирці й збірки на archive.org.

## Варіації й родичі
- Базовий файл: [Lemmings](lemmings.md); паралельна гілка — [Lemmings 2: The Tribes](lemmings-2-the-tribes.md) (51 уміння, вентилятор).
- Відмінності-осі відносно L1: поле — «піксельна маска збоку» → «3D-сітка блоків»; повороти — «лише 180°» → «90° (Turner, дефлектори, сплітери) і 180°»; камера — «скрол площини» → «4 камери + очима лемінга»; падіння — «смерть понад поріг» → «оглушення / смерть»; новий шар пристроїв (батути, пружини, телепорти, канатки, мати); «один лемінг за раз» як обмеження потоку.
- Родичі: [Survivors](survivors.md) (дроїди з уміннями), [Boulder Dash](boulder-dash.md) і [Dig Dug](dig-dug.md) (копання як основа).

## Цікавинки для курсу
- Автоходець на 3D-сітці блоків: чотири напрямки, стіна → розворот, край → падіння, пів-блок → крок — 🥉.
- Сімʼя «поворот при контакті»: Turner (вибір ліво/право), дефлектор (90° / 180° за гранню), сплітер (по черзі) — 📎 кожен, 🥉 сімʼя.
- Чотири незалежні камери з «масою» + вид очима лемінга — 🥈 (рендер 3D-сітки з кількох точок, колізія камери).
- Батут, що змінює висоту відскоку на ±1 блок, — 📎; пристрої «один за раз» (пружина, телепорт, канатка) з чергою — 📎.
- Двоступеневе падіння й мат як «скасування шкоди» — 🌱.
- Автоповтор спроби: запис дій з тіками і відтворення до останньої, потім передача керування — 🥉.

## Мапа на каталог
- Є (як у Lemmings): `gravity-fall` · `move-auto` · `turn-when-blocked` · `dig-terrain` ↔ Basher/Digger · `dig-hole` ↔ Miner · `destructible-blocks` · `impassable-cells` ↔ незнищенні блоки · `bomb-fuse` + `explode-area` ↔ Bomber · `environment-death` · `time-out` · `reach-exit` + `collect-quota` · `spawn-points` · `cell-click` · `game-pause` · `level-password` · `sequential-levels` + `difficulty-levels` · `status-panel` · `minimap-radar`.
- Нове серед наявних: `one-way-cell` ↔ односторонні блоки · `height-levels` ↔ пів-блоки · `inertia-slide` ↔ слизькі блоки · `teleport-pair` ↔ телепорти · `replay` ↔ автоповтор.
- **Нема** → пропозиції карток:
  - Повтори: `+assign-skill`, `+tool-allotment`, `+release-rate`, `+nuke-all`, `+fall-height-death` (два пороги, мат), `+camera-orbit`, `+first-person-view` (Virtual Lemming), `+splitter-balance` (сплітер по черзі), `+spring-jump` (батути й пружини).
  - `+multi-camera` «Кілька незалежних камер з перемиканням» · interface/render · 🥈 · слоти {count: 4, fixed_levels, tilt: no}.
  - `+turner-redirect` «Сутність-стрілка повертає інших на 90°» · entities/move · 📎 · слот {dir: left|right}.
  - `+deflector-block` «Блок повертає за гранню: 90° / 180°» · entities/move · 📎.
  - `+rope-slide` «Транспорт в один бік, одна сутність за раз» · entities/move · 🌱.
  - `+crash-mat` «Клітина скасовує шкоду падіння» · entities/state · 🌱.

## Пропозиції до словників
- `+trigger:landed` — повтор (Lemmings, L2, Troddlers): приземлення з перевіркою висоти.
- `+cond:fall_height(a, op, n)` — повтор.
- `+effect:excavate(a, shape, dir)` — повтор: вигризти форму в напрямку (Basher по пів блока, Miner по діагоналі, Digger вниз).
- `+ui:camera-buttons` — іконки перемикання й обертання камер на HUD.
- `+feature:replay-to-last-action` — після провалу спроба відтворюється до останньої дії, далі — гравець.
- `+axis:control` = `indirect`; `+axis:actors` = `swarm` — повтори з Lemmings.
- `+card:multi-camera`, `+card:turner-redirect`, `+card:deflector-block`, `+card:rope-slide`, `+card:crash-mat` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: 3D Lemmings](https://en.wikipedia.org/wiki/3D_Lemmings) — Clockwork Games / Psygnosis, прототип Cubewalker, 4 камери (не нахиляються, на деяких рівнях фіксовані), Virtual Lemming, Turner на 90° (знімається вибухом або підкопом), діагональні блоки, 4 × 20 рівнів + 20 практики, паролі, release rate, повтор, fast forward, Winterland.
- [Мануал (archive.org, OCR)](https://archive.org/stream/3d_lemmings_english/3d_lemmings_english_djvu.txt) — керування мишею й джойпадом, обидві панелі HUD, 9 умінь, камери й мапа, батути (червоний +1, синій −1), пружини, телепорти, мати, сплітери, слизькі блоки, канатки, меню й опції, автоповтор.
- [The 3D Lemmings Companion, чернетка (archive.org, OCR)](https://archive.org/stream/1995_Lemmings_3D_Companion_Draft/1995_Lemmings_3D_Companion_Draft_djvu.txt) — пів-блоки, незнищенне «дзенькає», односторонні блоки, дефлектори 90°/180°, «оглушення / смерть» при падінні, Builder на 6 сходинок, Bomber іде ще 1,5 клітини, Blocker з двох напрямків, Armageddon, ліміти часу 4–12 хв, цілі «10 з 10», «60 з 80», пастки.
- [Lemmings Forums: Loap](https://www.lemmingsforums.net/index.php?board=40.0) — фанатське відтворення (посилання з archive.org).
- YouTube: пошук «3D Lemmings gameplay».

## Непевне
- (?) Сплітер: мануал — по черзі ліво/право; гайд в іншому місці — «у випадкових напрямках».
- (?) Під час ковзання на льоду: гайд — лише Bomber, мануал — Bomber, Climber, Floater.
- (?) Іконка-бомба: мануал називає її рестартом (подвійний клік), гайд — Armageddon «усі вибухають»; найімовірніше, це нюк, що завершує спробу.
- (?) Blocker «діє з двох напрямків» — що буває з лемінгом, який підходить збоку, джерела не кажуть.
- (?) Пів-блок: гайд і «можна переступити», і «лемінги від нього відбиваються» — залежить від напрямку (?).
- (?) Точні пороги падіння й розмір блока в клітинах сітки не знайдено; перелік пасток (капкани, стомпери, лазери) — з проходження, неповний.
- (?) Load/Save — слоти збереження чи лише паролі; перший гайд згадує 100 рівнів, Wikipedia — 80 + 20 практики (те саме число).
