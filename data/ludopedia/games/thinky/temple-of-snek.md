---
title: Temple of Snek
slug: temple-of-snek
aka: [Temple Of Snek, Snek]
family: thinky
also: [maze-arcade]
klass: avatar
axes:
  field: layers
  time: rhythm
  opponent: none
  info: full
  random: none
  goal: state
year: 2023
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1208590/Temple_Of_Snek/", best: true, note: "опис: змія-охоронниця храму, пастки на ритм і довжину, 4 типи NPC, 5 середовищ, Classic, Mek-a-Snek, редактор; EA 18.08.2021, реліз 15.02.2023"}
  - {kind: itch, url: "https://pixeljam.itch.io/temple-of-snek", note: "той самий опис + коментарі: кнопки, що важчають з довжиною змії"}
  - {kind: other, url: "https://steamcommunity.com/app/1208590/reviews/?browsefilter=toprated", note: "відгуки: рух уперед на біт, покроковий режим, кнопки й шипи, висоти, чекпоінти, 3 підказки на кімнату"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1208590&count=25&maxlength=3000", note: "патчі: Fast mode ×4, one-step mode, 8 чекпоінтів, підказки в 3 рівні, Snek Workshop 20×20, нові NPC"}
  - {kind: other, url: "https://www.superjumpmagazine.com/temple-of-snek-review/", note: "рецензія: крок на сильну долю, висіти над порожнечею, поки частина тіла на висоті; смерті"}
  - {kind: other, url: "https://scottishgames.net/2023/03/18/temple-of-snek-the-sgn-review/", note: "рецензія: NPC ходять разом зі змією, «невірні» — 2 кроки на 1, двері на кілька кнопок, фракції"}
  - {kind: other, url: "https://gamingcypher.com/?p=166974", note: "прев'ю EA: WASD, Fast mode на F/Shift без поворотів, шипи від кнопок, довжина для кнопок"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Temple+of+Snek+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-auto, move-4dir, body-queue, self-collision, touch-death, environment-death, button-toggle, height-levels, checkpoint, pattern-automaton, chase-double-move, spawner-entity, map-window, in-game-editor, editor-playtest, level-exchange, avatar-picker, keyboard-controls, background-music, sound-effects, language-picker, +grow-on-eat, +rhythm-sync-tempo, +pressure-plate, +multi-switch-door, +toggle-spikes, +timed-button, +hang-over-edge, +checkpoint-rewind, +deathloop-detector, +hint-tiers, +fast-forward, +turn-based-toggle, +npc-faction-switches, +classic-snake-mode, +workshop-sharing, +skin-editor, +procedural-music]
proposes: ["+trigger:beat", "+cond:body_on", "+effect:checkpoint_rewind", "+feature:rhythm-toggle", "+feature:deathloop-detector", "+feature:hint-tiers", "+window:skin-editor", "+card:hang-over-edge", "+card:multi-switch-door"]
author: opus
date: 2026-11-09
---

# Temple of Snek — велика змія-охоронниця повзе на біт музики крізь клітинний храм, їсть грабіжників, росте й тілом тисне кнопки

## Суть
Пазл-підземелля Aetheric Games / Pixeljam: гравець — гігантська змія (Snek), що боронить храм від грабіжників. Як у класичній «Змійці», голова сама повзе вперед на кожен біт музики, гравець лише повертає; зʼїдений людина = +1 сегмент. Головний ресурс — **довжина тіла**: нею одночасно тиснуть кілька кнопок, перекривають шипи й висять над порожнечею, але в довгого тіла складніше розвернутись у вузьких коридорах. Кімнати сплетені в одну безперервну мапу (5 середовищ), NPC рухаються «годинниковим» ритуалом синхронно зі змією.

## Поле і час
- Клітинна (квадратна) сітка кімнат з висотами: уступи, рейки, ями з водою/нечистотами; камера 3D, зверху під кутом, місцями зум і майже від першої особи в тунелях.
- Тік = такт музики: на кожен біт голова робить крок, NPC — свої кроки (`time: rhythm`). Музика процедурна, змінюється від дій.
- Опції темпу: швидкість гри, Fast mode до ×4, покроковий / one-step режим (тап = 1 клітина, утримання = безперервно) — тоді світ стоїть без вводу (відгуки, патч 1.1.3).
- Шари: підлога й висоти · кнопки, шипи, двері, вода · змія, NPC, монети.
- Кімнати зʼєднані; на мапі в меню паузи — позначки потрібної довжини.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Snek | player | довжина L, напрям | щобіту крок уперед; тіло — черга; поворот 4 напрями; росте від їжі |
| Грабіжник / «невірний» | pickup | — | базовий беззахисний; зникає від дотику голови, змія +1; «невірні» ходять 2 кроки на 1 крок змії |
| Озброєна людина | enemy | — | пізніші загони; може вбити змію (уколоти) |
| Жриця | ally | маршрут | ходить ритуальним маршрутом, тисне кнопки «на допомогу»; зʼївши іншу фракцію, змушуєш їх тиснути кнопки |
| Капітан | boss | — | фінальна головоломка (?) |
| Щури, птахи кетцаль | neutral | — | дрібні тварини (патч 2023); роль у пазлах (?) |
| Двері-спавнер | spawner | ∞ | безкінечно випускають NPC у кімнату |
| Кнопка | switch | звичайна / довгий таймер | натиснута, поки на ній тіло або NPC; керує дверима й шипами |
| Двері / ґрати | gate | кількість кнопок | відкриті, поки натиснуті всі свої кнопки; закриваючись на тілі, розтинають змію |
| Шипи | hazard | висунуті / сховані | висунуті вбивають; перемикаються кнопками або магічними плитками |
| Магічна плитка | switch | — | вмикає шипи / слід (?) |
| Уступ / висота | terrain | висота | змія може висіти над нижчою клітиною, поки частина тіла лежить на висоті |
| Рейки / перила | static | — | непрохідні (?) |
| Вода / нечистоти | hazard | — | змія тоне; реагує на уламки (патч) |
| Подвійна стрілка на підлозі | switch | — | чекпоінт: засвічується, коли на неї наповзаєш |
| Монета | pickup | — | колекційна задачка з двома розвʼязками |
| Стіна | static | — | удар головою = смерть |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` (біт) → ТО `move(snek_head, facing)`, тіло `custom: «кожен сегмент на місце попереднього»`.
- КОЛИ `input(dir)` → ТО `face(snek_head, dir)` (наступний крок у новому напрямку; розворот назад — (?)).
- КОЛИ `contact(snek_head, wall)` або `contact(snek_head, snek_body)` → ЯКЩО `custom: «на тій самій висоті»` → ТО `lose`, `custom: «повернення на останній чекпоінт»`.
- КОЛИ `contact(snek_head, raider)` → ЯКЩО `not state(raider, armed)` → ТО `disappear_b`, `grow(snek, 1)`.
- КОЛИ `contact(snek_head, special_npc)` → ТО `custom: «змія коротшає»` (буває, за відгуками; який NPC — (?)).
- КОЛИ `adjacent(armed_human, snek)` → ТО `lose` (уколото).
- КОЛИ `enter(snek, spikes)` → ЯКЩО `state(spikes, up)` → ТО `lose`.
- КОЛИ `enter(snek|npc, button)` → ЯКЩО `custom: «натиснуті всі кнопки цих дверей одночасно»` → ТО `set_state(door, open)`, `custom: «повʼязані шипи ховаються / висуваються»`.
- КОЛИ `leave(snek|npc, button)` → ЯКЩО `not state(button, timed)` → ТО `clear_state(door, open)`.
- КОЛИ `enter(snek, timed_button)` → ТО `set_state(door, open, N)` (довгий таймер; N — (?)).
- КОЛИ `custom: «двері закриваються»` → ЯКЩО `occupied(door_cell, snek_body)` → ТО `lose` (розтинає).
- КОЛИ `tick` → ЯКЩО `not supported(snek)` → ТО `fall(snek)`; змія висить над порожнечею, поки хоч один сегмент на вищій клітині.
- КОЛИ `enter(snek, water)` → ЯКЩО `not supported(snek)` → ТО `lose` (тоне).
- КОЛИ `tick` → ТО `custom: «кожен NPC робить крок свого ритуального маршруту; невірні — два»`.
- КОЛИ `timer(n)` → ЯКЩО `custom: «двері-спавнер»` → ТО `spawn_at(raider, door)`.
- КОЛИ `enter(snek, checkpoint_arrows)` → ТО `checkpoint`.
- КОЛИ `repetition` (змія гине в тому самому місці по колу) → ТО `custom: «детектор смертельної петлі відкочує сейв на чекпоінт раніше»`.
- КОЛИ `input(load_previous_checkpoint)` → ТО `custom: «назад на попередній чекпоінт, до 8 кроків»`.
- Classic mode: КОЛИ `contact(snek_head, raider)` → ТО `grow(snek, 1)`, `score(+n)`; множники за налаштування (Obstacles, Ramps ×5).
- Перемога: пройти кімнату — відкрити вихід і доповзти; гра — дійти до фіналу (кінцівка з «твістом»). · Поразка: смерть → останній чекпоінт. · Рахунок: лише Classic.

## Керування і ввід
- WASD / стрілки / геймпад — повернути голову; рух сам на біт.
- F або Shift — Fast mode (до ×4 швидкості); у ньому WASD не повертає змію.
- Режими темпу в налаштуваннях: швидкість, покроковий (тап = крок, утримання = серія), вимкнути ритм.
- Підказка зупиняє змію; натиснувши рух, підказку скасовуєш.
- Undo нема — лише відкат на попередні чекпоінти (до 8).

## Вікна, меню, HUD
- `main-menu`: Story · Classic (відкривається) · Snek Workshop · Mek-a-Snek · налаштування.
- `game-screen`: 3D-кімната; HUD — `popup-text` лічильника довжини при зміні; режими камери kill-cam і snek-cam.
- `pause-menu`: продовжити, Load Previous Checkpoint, підказки, мапа, налаштування.
- `map-window` (мінімапа в паузі): кімнати й позначки потрібної довжини.
- `hints-window`: 3 рівні підказки на кімнату, третій — повний розвʼязок.
- `settings-window`: швидкість, Fast mode, one-step / ритм, мова (6 мов) + text-to-speech, кольорові альтернативи, гучність, складність.
- `editor-window` (Snek Workshop): поле до 20×20, теми dungeon/palace/temple/garden; опублікувати можна лише розвʼязаний рівень.
- `skin-select` / `custom-window` (Mek-a-Snek): редактор візерунка шкіри, тіла й голови, обмін через Workshop.
- `end-screen` — фінал кампанії (?); `mode-select` — Story/Classic у головному меню.

## Фічі поза полем
- `checkpoint`-система: подвійні стрілки, відкат до 8 попередніх, детектор смертельних петель, ліміт 6 з 8 сейвів на одному чекпоінті.
- `hint` у 3 рівні; `speed-control`; `assist-mode`-подібне вимкнення ритму (Steam: «Playable without Timed Input», «Adjustable Difficulty»).
- `mode-classic` — 2D-подібна «Змійка» на рахунок з налаштуваннями (Obstacles, множник Ramps).
- `level-editor` + `level-sharing` через Steam Workshop; `custom-skins` (Mek-a-Snek).
- `collectibles` (монети з двома розвʼязками), `achievements`, `cloud-save`, `gamepad-support`, `localization` + TTS, `colorblind-palette`.

## Варіації й родичі
- Осі варіацій «змійка-пазл»: рух — сам на біт (Temple of Snek, класична Snake) / лише за вводом (Snakebird, [would-you-love-me-if-i-was-a-snake](would-you-love-me-if-i-was-a-snake.md)); довжина — росте від їжі (тут) / фіксована / ріже себе; гравітація — нема / тіло падає ([snakebird](snakebird.md)) / висіти, поки частина тіла на висоті (тут).
- Родичі в теці: [snakebird](snakebird.md), [the-snake-that-eats-puzzle-game-mechanics](the-snake-that-eats-puzzle-game-mechanics.md), [a-monsters-expedition](a-monsters-expedition.md) (сплетена мапа), [void-stranger](void-stranger.md).
- Класична Snake — сімʼя `maze-arcade` (тут — режим Classic).

## Цікавинки для курсу
- Крок на біт: тік логіки від BPM, ввід лише змінює напрям наступного кроку — 📎.
- Кнопка, що тримає двері, поки на ній будь-який сегмент тіла; двері на N кнопок одночасно — 🥉.
- «Висить, поки хоч один сегмент на висоті»: перевірка опори для всієї черги тіла — 🥉.
- NPC з ритуальним маршрутом і «2 кроки на 1» — скінченний патерн на тіках — 📎.
- Чекпоінти зі стеком на 8 і детектор смертельної петлі (повторна смерть у тому самому стані) — 🥈.
- Редактор кімнат з перевіркою «опублікувати лише після власного проходження» — 🥈.

## Мапа на каталог
- Є: `move-auto` ↔ повзе сама; `move-4dir` ↔ повороти; `body-queue` ↔ тіло; `self-collision` ↔ удар у себе; `touch-death` + `environment-death` ↔ шипи, озброєні, вода; `button-toggle` ↔ кнопки → двері/шипи; `height-levels` ↔ уступи; `checkpoint` ↔ стрілки; `pattern-automaton` ↔ ритуальні маршрути NPC; `chase-double-move` ↔ «невірні» 2 кроки на 1; `spawner-entity` ↔ безкінечні двері; `map-window` ↔ мапа в паузі; `in-game-editor` + `editor-playtest` + `level-exchange` ↔ Snek Workshop; `avatar-picker` ↔ Mek-a-Snek; `keyboard-controls`; `background-music`, `sound-effects`, `language-picker`.
- **Нема** → пропозиції карток:
  - `+grow-on-eat` (є в корпусі), `+rhythm-sync-tempo` (є), `+pressure-plate` (є), `+toggle-spikes` (є), `+checkpoint-rewind` (є), `+fast-forward` (є), `+workshop-sharing` (є).
  - `+multi-switch-door` «Двері відкриває лише одночасне натискання N кнопок» · entities/interact · 🥉 · слот {n}.
  - `+timed-button` «Кнопка тримає стан N тіків після сходження» · entities/interact · 📎.
  - `+hang-over-edge` «Тіло висить над порожнечею, поки є опора хоч під одним сегментом» · entities/move · 🥉.
  - `+deathloop-detector`, `+hint-tiers`, `+turn-based-toggle` (вимкнути ритм), `+npc-faction-switches` (одна фракція тисне кнопки, коли зʼїдено іншу), `+classic-snake-mode`, `+skin-editor`, `+procedural-music`.

## Пропозиції до словників
- `+trigger:beat` — сильна доля музики як тік (уточнення `tick` для `time: rhythm`).
- `+cond:body_on` — на клітині лежить будь-який сегмент тіла (кнопки, опора).
- `+effect:checkpoint_rewind` — відкат на попередній чекпоінт зі стеку.
- `+feature:rhythm-toggle` — вимкнути ритм і грати покроково; `+feature:deathloop-detector`; `+feature:hint-tiers` — підказка в 3 рівні.
- `+window:skin-editor` — редактор шкіри персонажа (Mek-a-Snek).
- `+card:hang-over-edge`, `+card:multi-switch-door`.

## Джерела
- ⭐ [Steam: Temple of Snek](https://store.steampowered.com/app/1208590/Temple_Of_Snek/) — суть, пастки на ритм і довжину, 4 типи NPC, 5 середовищ, Classic, Mek-a-Snek, редактор; категорії доступності.
- [itch: Pixeljam](https://pixeljam.itch.io/temple-of-snek) — опис і коментарі.
- [Steam-відгуки](https://steamcommunity.com/app/1208590/reviews/?browsefilter=toprated) — рух уперед на біт, покроковий режим, шипи від кнопок, висоти й лазіння, чекпоінти-стрілки, 3 підказки, мінімапа.
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1208590&count=25&maxlength=3000) — Fast mode, one-step, 8 чекпоінтів, підказки, Workshop, нові NPC, TTS.
- [Superjump](https://www.superjumpmagazine.com/temple-of-snek-review/) — крок на сильну долю, висіння на висоті, види смерті.
- [SGN](https://scottishgames.net/2023/03/18/temple-of-snek-the-sgn-review/) — NPC рухаються зі змією, «невірні» ×2, двері на кілька кнопок, фракції.
- [Gaming Cypher](https://gamingcypher.com/?p=166974) — керування WASD, Fast mode на F/Shift.
- YouTube: пошук «Temple of Snek gameplay».

## Непевне
- (?) Чи можна розвернутись на 180° (у тіло) і як саме «залазити на себе» на вищий ярус — відгуки кажуть про лазіння, але удар у себе = смерть; ймовірно, різниця у висоті.
- (?) Хто з NPC зменшує змію; повний список 4 типів NPC (у джерелах: грабіжники/невірні, озброєні, жриці, капітан; плюс щури й кетцалі).
- (?) Що саме роблять магічні плитки і «сліди» (trails), рейки; тривалість довгих кнопок.
- (?) «Secret powers» з опису не названі в жодному джерелі.
- (?) Кількість кімнат і кінцівок; чи є окремий екран фіналу.
