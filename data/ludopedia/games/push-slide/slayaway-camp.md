---
title: Slayaway Camp
slug: slayaway-camp
aka: ["Slayaway Camp: Butcher's Cut", "Slayaway Camp 2", "Slayaway Camp II", "Slayaway Camp 2: Netflix & Kill"]
family: push-slide
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2016
platforms: [web (Kongregate), PC (Windows, macOS, Linux), iOS, Android, Xbox One, PS4, Switch, PS Vita]
links:
  - {kind: other, url: "https://www.imore.com/slayaway-camp-game-guide", best: true, note: "гайд: ковзання до упору, налякати жертву збоку, копи, вода, вогонь, дірки, шафи, парні телефони, QTE і гроші"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Slayaway_Camp", note: "сітка в ізометрії, «не може зупинитись до зіткнення», 10 відеокасет по 10–15 рівнів, монети на підказки й косметику, хронологія портів"}
  - {kind: steam, url: "https://store.steampowered.com/app/530390/", note: "оригінал: пастки, копи, SWAT, міни, телефони, коти; NC-17-режим, deleted scenes, набори вбивць"}
  - {kind: steam, url: "https://store.steampowered.com/app/2737140/", note: "Slayaway Camp 2 (2024): 5 класів вбивць, покроковий рух поруч із «льодовим», ящики, валуни, трава, плити-перемикачі, Endless"}
  - {kind: other, url: "https://www.pocketgamer.com/slayaway-camp-netflix-kill/review", note: "огляд мобільного сиквела: мисливці стріляють по лінії, підказка «перемотка» в 1 і 2 тапи, зірки відкривають жанри"}
  - {kind: other, url: "https://gamepretty.com/slayaway-camp-walkthrough-with-all-levels/", note: "проходження: назви рівнів показують порядок появи механік (SWAT, міни, коти, телепорти, електроограда, світло)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Slayaway+Camp+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [inertia-slide, move-4dir, keyboard-controls, swipe-gestures, impassable-cells, destroy-all-enemies, reach-exit, player-death, environment-death, line-of-sight-attack, teleport-pair, undo-redo, sequential-levels, level-select, level-unlock, shop-window, avatar-picker, +flee-player, +topple-crush, +noise-lure, +lights-off-stealth, +must-not-kill, +paid-hint, +qte-finisher, +hard-mode, +character-classes]
proposes: ["+effect:flee", "+effect:topple", "+effect:lure", "+cond:from_behind", "+trigger:spotted", "+ui:timing-bar", "+feature:paid-hint", "+card:flee-player", "+card:topple-crush", "+card:lights-off-stealth", "+card:must-not-kill", "+card:qte-finisher"]
author: opus
date: 2026-11-09
---

# Slayaway Camp — «льодяний» пазл у слешер-обгортці: маніяк ковзає до упору, а жертва гине від зіткнення

## Суть
Гравець керує вбивцею Skullface на квадратній сітці (рендер — ізометричні воксельні кімнати). Вбивця «не може зупинитись, доки не зіткнеться з перешкодою» — класичне Inertia-ковзання, де перешкодою можуть бути й жертви: вʼїхав у жертву — вбив. Мета рівня — прибрати всіх жертв і дійти до порталу, що зʼявляється після останньої. Головне розширення жанру — **живі цілі**: жертва, біля якої вбивця зупинився, тікає в протилежний бік і може сама загинути у воді чи вогні, а копи, SWAT, коти й телефони перетворюють ковзання на керування чужими рухами.

## Поле і час
- Логіка — квадратна сітка 4-зв'язна; рендер — ізометрична діорама, камера статична (на мобільних — свайп по екрану).
- Шари: підлога (звичайна / вода / вогонь / дірка / міна / телепорт / вимикач світла) + обʼєкти (стіни, меблі-шафи, телефони, ящики в сиквелі) + персонажі (вбивця, жертви, копи, SWAT, коти).
- Хід = одне ковзання вбивці до упору; після нього реагують інші (жертви тікають, копи «бачать»). Без вводу світ стоїть — `time: turn`.
- Рівні згруповано у «відеокасети» по 10–15 рівнів, кожна — своя локація; в оригіналі 10 касет і понад 200 рівнів (Wikipedia, Steam).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вбивця (Skullface та інші) | player | скін / клас (сиквел) | ковзає в 1 з 4 напрямків до першої перешкоди; вʼїзд у жертву — вбивство |
| Жертва (табірник) | neutral | — | стоїть; якщо вбивця зупинився поруч — тікає в протилежний бік; гине у воді, вогні, дірці |
| Коп | enemy | напрям погляду | не лякається; зупинився прямо перед ним — поразка; вбивається ударом збоку чи ззаду; для перемоги не обовʼязковий |
| SWAT | enemy | лінія охорони | охороняє лінію перед собою, вбиває того, хто пробує його атакувати; вразливий лише в темряві |
| Кіт | neutral | — | вбивати й губити не можна («Don't Zap The Cats!», «Cats Can't Get Wet!»); бачить у темряві |
| Стіна, дерево, огорожа | static | — | зупиняє ковзання |
| Шафа / холодильник / комод | object | орієнтація | удар спереду чи ззаду — падає й роздавлює того, хто по той бік; відкриває прохід |
| Телефон | switch | пара | удар по одному — дзвонить парний; до нього біжить найближчий персонаж |
| Вода | hazard | — | вбивця гине; налякана жертва, що вбігла, гине |
| Вогнище / вогонь | hazard | — | вбиває і жертву, і вбивцю |
| Дірка | hazard | — | будь-хто, хто пробіг по ній, гине |
| Міна | hazard | — | вибухає під тим, хто наступив (?) |
| Електроограда | hazard | — | убиває при контакті; небезпечна для котів (?) |
| Телепорт | terrain | пара | переносить на парний (?) |
| Вимикач світла | switch | — | вимикає світло: вбивцю не помічають (крім котів) |
| Портал-вихід | static | зʼявляється після останньої жертви | вхід — рівень пройдено |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `slide(killer, dir)` до першої непрохідної клітини.
- КОЛИ `blocked(killer)` → ЯКЩО `occupied(next_cell, victim)` → ТО `disappear_b` (жертву вбито); вбивця лишається у своїй клітині (?).
- КОЛИ `blocked(killer)` → ЯКЩО `adjacent_count(killer, victim, >=, 1)` і жертва не була ціллю удару → ТО `slide(victim, away_from_killer)` (`custom: «жертва тікає в протилежний від вбивці бік»`).
- КОЛИ `enter(victim, water|fire|hole|mine)` → ТО `disappear_a` (зараховано як вбивство).
- КОЛИ `enter(killer, water|fire|hole)` → ТО `lose`.
- КОЛИ `blocked(killer)` → ЯКЩО `facing(cop, killer)` і `custom: «вбивця в сусідній клітині прямо перед копом»` → ТО `lose`.
- КОЛИ `contact(killer, cop)` → ЯКЩО `custom: «удар збоку або ззаду»` → ТО `disappear_b`; спереду — `lose` (?).
- КОЛИ `blocked(killer)` → ЯКЩО `adjacent_count(killer, cop, >=, 1)` → ТО `custom: «коп не тікає»` — правило втечі на копів не діє.
- КОЛИ `line_of_sight(swat, killer)` → ЯКЩО `not state(room, dark)` → ТО `lose`; ЯКЩО `state(room, dark)` → `contact(killer, swat)` → ТО `disappear_b` (єдиний спосіб убити SWAT).
- КОЛИ `contact(killer, light_switch)` → ТО `set_state(room, dark)`; ЯКЩО `state(room, dark)` → ТО `custom: «вбивцю не помічають, крім котів»`.
- КОЛИ `died(cat)` → ТО `lose` (котів треба зберегти).
- КОЛИ `contact(killer, bookcase)` → ЯКЩО `custom: «удар спереду або ззаду шафи»` → ТО `custom: «шафа падає на клітину по той бік»`; ЯКЩО `occupied(that_cell, person)` → ТО `disappear` (роздавлено).
- КОЛИ `contact(killer, phone)` → ТО `custom: «дзвонить парний телефон»`, `custom: «найближчий персонаж у тому ж рядку чи стовпці біжить до нього»` (?) — так вбивця переставляє людей.
- КОЛИ `enter(a, teleporter)` → ТО `teleport(a, pair)` і ковзання триває (?).
- КОЛИ `all_gone(victim)` → ТО `spawn(exit_portal)`; КОЛИ `enter(killer, exit_portal)` → ТО `win`, `window(end-screen)`.
- Фінал рівня: КОЛИ `input(tap)` → ЯКЩО `custom: «черепок на шкалі в червоній зоні»` → ТО `currency(+n)`, `custom: «бонусне вбивство-катсцена»`.
- КОЛИ `input(hint)` → ТО `currency(-n)`, `custom: «підказка або повне проходження рівня»`.
- КОЛИ `input(rewind)` → ТО `undo(1)` (?); порядок вбивств важливий — хибний порядок лікується перемоткою.
- Перемога: усі жертви мертві + вхід у портал; копів убивати не обовʼязково. · Поразка: вода/вогонь/дірка для вбивці, зупинка перед копом, лінія SWAT при світлі, загибель кота. · Рахунок: нема; монети лише з фінальної QTE.

## Керування і ввід
- ПК: стрілки / WASD — напрямок ковзання (?); мобільні: свайп (iMore).
- Окремі кнопки: перемотка назад, підказка за монети, меню (?).
- Фінальна QTE: один тап у момент, коли черепок на смузі в червоній зоні.

## Вікна, меню, HUD
- `splash-screen` → `main-menu` (?): Грати · Магазин · Налаштування.
- `level-select`: полиця з 10 відеокасетами (плюс deleted scenes), всередині — список рівнів зі статусом; NC-17-версії відкриваються після проходження (Steam).
- `game-screen`: діорама рівня; HUD — кнопка перемотки, кнопка підказки, лічильник монет (?).
- `end-screen`: катсцена-«кадр» вбивства + QTE зі смугою (`+ui:timing-bar`) → монети → наступний рівень.
- `shop-window`: вбивці (зокрема за мотивами культових хорорів), gore-паки анімацій (дробарка, газонокосарка), підказки й проходження.
- `character-select`: вибір вбивці перед рівнем (?).
- `hints-window`: підказка / покрокове проходження за монети.
- `settings-window`, `pause-menu` (рестарт, вихід) (?).
- Переходи: level-select → game-screen → (останнє вбивство + портал) end-screen/QTE → game-screen наступного рівня; поразка → той самий рівень.

## Фічі поза полем
- `levels-sequential` у межах касети, `level-unlock` касет, бонус `deleted scenes`.
- `mode-hardcore`-подібний NC-17-режим: важчі версії рівнів кожної касети (Steam).
- `hint` / `show-solution` за внутрішню валюту (`+feature:paid-hint`); `undo` — перемотка.
- `unlockables`: вбивці й gore-паки, частина — платні DLC-набори.
- Сиквел Slayaway Camp 2: `mode-endless`, міні-ігри-випробування з нагородами, 25 касет.

## Варіації й родичі
- **Slayaway Camp 2** (iOS/Android 2023, Steam 2024): 36 вбивць у 5 класах — Slasher (класика), Sorcerer (снаряд руйнує перешкоди й перетворює табірників на туман), Beast (рик заморожує табірників), Monster (робить з мертвих зомбі-союзників), Ghost (проходить крізь перешкоди); **новий покроковий рух на 1 клітину** поруч зі старими «льодовими» пазлами; ящики й валуни, що котяться й давлять; трава й дерева лякають табірників із сусідніх клітин; плити-перемикачі відкривають пастки й двері; газонокосарки.
- Мобільна версія сиквела (огляд Pocket Gamer): мисливці періодично стріляють уздовж лінії й можуть убити жертву; налякана жертва може втекти за край мапи; зірка за рівень відкриває нові «жанри».
- Осі варіацій:
  - **цілі ковзання**: стіни (Inertia) / стіни + жертви, які гинуть від удару (Slayaway) / вороги, яких давить ковзний блок (Pengo);
  - **чужий рух**: нема / жертва тікає від сусіда (Slayaway) / тікає за лінією зору (Pâquerette);
  - **охорона**: нема / коп бачить 1 клітину / SWAT — лінію / мисливець стріляє по лінії;
  - **рух аватара**: до упору / на 1 клітину (Slayaway 2) / обидва в одній грі.
- Родичі: [ice-sliding-puzzles](ice-sliding-puzzles.md), [pengo](pengo.md), [tomb-of-the-mask](tomb-of-the-mask.md), [hitman-go](hitman-go.md) (копи-охоронці, шум-приманка), [helltaker](helltaker.md).

## Цікавинки для курсу
- Ковзання до упору, де ціль-жертва — і перешкода, і обʼєкт удару — 🌱: Inertia з одним новим `if`.
- Втеча жертви від сусіда з подальшою смертю в небезпеці (другий «ковзний» актор) — 📎.
- Коп «бачить» лише сусідню клітину перед собою, вбивається ззаду/збоку + SWAT із лінією і темрявою — 🥉 (орієнтація як стан + умова з боку удару).
- Шафа, що падає на сусідню клітину й давить — 📎.
- Парні телефони: дзвінок кличе найближчого в рядку/стовпці — 🥉 (вибір найближчого + рух до цілі).
- Розвʼязувач рівня BFS по станах (позиція вбивці + множина живих + стан світла) — 🥈.
- QTE-смуга з таймінгом як нагорода між рівнями — 🌱.

## Мапа на каталог
- Є: `inertia-slide` ↔ ковзання до упору; `move-4dir` + `keyboard-controls` + `swipe-gestures` ↔ ввід; `impassable-cells` ↔ стіни/дерева; `destroy-all-enemies` ↔ «убити всіх жертв»; `reach-exit` ↔ портал; `player-death` + `environment-death` ↔ вода, вогонь, дірки; `line-of-sight-attack` ↔ SWAT/мисливці; `teleport-pair` ↔ телепорти; `undo-redo` ↔ перемотка; `sequential-levels` + `level-select` + `level-unlock` ↔ касети; `shop-window` + `avatar-picker` ↔ магазин вбивць.
- **Нема** → пропозиції карток:
  - `+flee-player` (вже пропонована DROD) «Сутність тікає від гравця» · entities/move · 📎 · слот {trigger: adjacent|sight, mode: slide|step}.
  - `+topple-crush` «Меблі падають на сусідню клітину й давлять» · entities/interact · 📎.
  - `+noise-lure` (Hitman GO) — телефонний дзвінок кличе найближчого.
  - `+lights-off-stealth` «Вимкнене світло вимикає виявлення» · entities/state · 🥉 · слот {sees_in_dark: kinds}.
  - `+must-not-kill` «Сутність, загибель якої = поразка» · game-logic/lose · 🌱 — коти.
  - `+paid-hint` (Chuzzle, Mekorama) · слот {levels: hint|full_solution}.
  - `+qte-finisher` «QTE-смуга з таймінгом після рівня» · game-logic/score · 🌱.
  - `+hard-mode` — NC-17-версії рівнів; `+character-classes` — 5 класів вбивць сиквела.

## Пропозиції до словників
- `+effect:flee` — жертва тікає в протилежний бік до упору (тут записано через `slide`, але дієслово «тікати від» повторюється в DROD, Pâquerette).
- `+effect:topple` — обʼєкт падає на сусідню клітину (шафа), родич `tip_over` у Pipe Push Paradise.
- `+effect:lure` — дзвінок / приманка кличе сутність до точки.
- `+cond:from_behind` — удар з боку чи ззаду (коп).
- `+trigger:spotted` — охоронець помітив гравця (коп спереду, SWAT на лінії).
- `+ui:timing-bar` — смуга з рухомим маркером для QTE.
- `+feature:paid-hint` — підказка/проходження за ігрову валюту.
- `+card:flee-player`, `+card:topple-crush`, `+card:lights-off-stealth`, `+card:must-not-kill`, `+card:qte-finisher` — див. вище.

## Джерела
- ⭐ [iMore: Slayaway Camp game guide](https://www.imore.com/slayaway-camp-game-guide) — правила: ковзання до упору, вбити всіх, крім копів, налякати збоку, копи спереду = кінець, вода/вогонь/дірки, шафи падають і давлять, парні телефони, QTE і гроші на gore-паки, перемотка після хибного порядку.
- [Wikipedia: Slayaway Camp](https://en.wikipedia.org/wiki/Slayaway_Camp) — квадратна сітка в ізометрії, «unable to stop moving until colliding», копи, шафи, коти, касети по 10–15 рівнів, монети на косметику й підказки, дати портів і сиквела.
- [Steam: Slayaway Camp](https://store.steampowered.com/app/530390/) — «Traps! Cops! SWAT teams! Land mines! Rotary telephones! Cats!», 10 касет, 200+ рівнів, NC-17, deleted scenes.
- [Steam: Slayaway Camp 2](https://store.steampowered.com/app/2737140/) — класи вбивць, покроковий рух, ящики, валуни, трава, плити, газонокосарки, Endless.
- [Pocket Gamer: огляд мобільного сиквела](https://www.pocketgamer.com/slayaway-camp-netflix-kill/review) — мисливці, втеча жертви за край, підказка 1/2 тапи, зірки.
- [GamePretty: проходження всіх рівнів](https://gamepretty.com/slayaway-camp-walkthrough-with-all-levels/) — назви рівнів (SWAT, міни, коти, електроограда, телепорти, світло, вибухівка, втеча).
- YouTube: пошук «Slayaway Camp gameplay».

## Непевне
- (?) Де зупиняється вбивця після вбивства: у своїй клітині чи в клітині жертви — джерела кажуть лише «sliding into a victim disposes of them».
- (?) Точна умова втечі: лише ортогональне сусідство після зупинки і чи жертва тікає до упору (так у гайді — «run in the opposite direction»), чи на 1 клітину.
- (?) Хто відповідає на дзвінок: «найближчий» (iMore) vs «будь-хто в рядку/стовпці» (TV Tropes, лише фрагмент у пошуку — сторінка 403).
- (?) Механіка мін, електроогорож і телепортів — відомі лише з назв рівнів; чи ковзання триває після телепорту — не перевірено.
- (?) Що саме робить кіт у темряві (лише «бачить вбивцю») і чи смерть кота = миттєва поразка.
- (?) Перемотка — на один хід чи до початку; клавіші на ПК; наявність `pause-menu` і `character-select` як окремих екранів.
- (?) Назва «Slayaway Camp 2: Netflix & Kill» — з адреси огляду Pocket Gamer; Wikipedia називає сиквел «Slayaway Camp II».
