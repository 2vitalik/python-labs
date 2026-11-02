---
title: Pengo
slug: pengo
family: push-slide
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: partial
  random: setup
  goal: score
year: 1982
platforms: [arcade, Atari 2600, Atari 5200, Atari 8-bit, Game Gear, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pengo_(video_game)", best: true, note: "правила раунду, діамантові блоки, Blob-и, 16 раундів"}
  - {kind: other, url: "https://pixelatedarcade.com/games/pengo/documents/instruction-manual/6/", note: "інструкція: таблиця очок, бонус за час, 5 життів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=pengo+arcade+1982+gameplay", note: "пошук; геймплей аркади"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=pengo+arcade+longplay", note: "пошук; повне проходження 16 раундів"}
stage: v2
coverage: 70
mechanics: [move-4dir, keyboard-controls, push-object, inertia-slide, impassable-cells, destroy-all-enemies, touch-death, player-death, spawn-points, reinforcements, temporary-modes, time-bonus, event-points, combo-multiplier, score-records, sequential-levels, progress-acceleration, +crush-by-slide, +break-block, +wall-shake-stun, +line-up-bonus, +flee-when-last]
proposes: ["+trigger:input", "+trigger:after", "+trigger:pattern", "+trigger:counter", "+trigger:timer", "+cond:free", "+cond:occupied", "+effect:slide", "+effect:stun", "+effect:transform", "+effect:spawn_at", "+effect:score", "+role:container", "+trigger:crushed_by", "+window:intermission", "+ui:egg-counter"]
author: opus
date: 2026-11-02
---

# Pengo — пінгвін штовхає крижини, що ковзають до упору і розчавлюють Sno-Bee

## Суть
Пінгвін Pengo в лабіринті з крижаних блоків бʼється з Sno-Bee: штовхнутий блок **ковзає до упору** й чавить усіх ворогів на своєму шляху, а блок, якому нема куди їхати, розбивається. Вороги вилуплюються з яєць, схованих у блоках, і самі ламають лід, щоб дістатися гравця. Раунд закінчується, коли знищено всіх Sno-Bee (з яйцями); додаткові способи — оглушити ворогів ударом об стіну-борт і вишикувати три діамантові блоки в лінію.

## Поле і час
- Квадратна сітка, цілком заповнена лабіринтом крижаних блоків; поле обнесене «електричною» стіною-бортом (приблизно 13×15 клітин (?)). Усе видно, але які блоки з яйцями — видно лише на мить на старті раунду (`info: partial`).
- Real-time: Pengo і Sno-Bee рухаються клітинами з плавною анімацією; блок, що ковзає, рухається швидко до упору.
- Таймер раунду неявний: < 60 с — бонус за час; 2 хв без смерті й перемоги — Sno-Bee перетворюються на Blob-ів і тікають.
- Розстановка діамантових блоків і блоків з яйцями — фіксована/випадкова за раундом (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Pengo | player | 5 життів (інструкція) | рух 4 напрямки; кнопка біля блоку — штовхнути/розбити; кнопка біля борту — трусити стіну |
| Крижаний блок | object | — | штовх → ковзає до першої перешкоди; нема куди — розбивається |
| Блок з яйцем | container | яйце Sno-Bee | як крижаний; блимає на старті; розбитий — яйце знищене (зараховано) |
| Діамантовий блок | object | 3 на раунд | ковзає, але не розбивається; три в лінію → бонус |
| Борт (стіна поля) | static | 4 сторони | непрохідний; Pengo «трусить» його → оглушує ворогів, що торкаються цього борту |
| Sno-Bee | enemy | колір/тип за раундом (?) | ходить до Pengo, ламає блоки на шляху; дотик → смерть Pengo |
| Яйце (у блоці) | spawner | — | вилуплюється в Sno-Bee на заміну знищеним |
| Оглушений Sno-Bee | enemy | стан stunned, час | нерухомий; Pengo проходить крізь нього й знищує; блок чавить |
| Blob | enemy | швидший | Sno-Bee після 2 хв або останній живий: біжить до борту, ламає лід, потім у кут і зникає |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(pengo, dir)`.
- КОЛИ `input(push)` + `adjacent(pengo, block)` → ЯКЩО `free(cell_behind_block)` → ТО `slide(block, dir)`; інакше `disappear_b` (розбити; діамантовий — `block`).
- КОЛИ `contact(sliding_block, sno_bee)` → ТО `custom: «Sno-Bee несеться блоком і гине при зупинці»`; після зупинки `score(400 | 1600 | 3200)` за 1 / 2 / 3 Sno-Bee одним блоком.
- КОЛИ `destroyed(block)` → ТО `score(30)`; ЯКЩО `has(block, egg)` → ТО `custom: «яйце знищене»`, `counter(eggs_left, -1)`, `score(500)`.
- КОЛИ `died(sno_bee)` → ЯКЩО `count(eggs, >, 0)` → ТО `spawn_at(sno_bee, egg_block)` (вилуплення на заміну).
- КОЛИ `contact(sno_bee, block)` → ТО `custom: «Sno-Bee розбиває лід на шляху до Pengo»`.
- КОЛИ `input(push)` + `adjacent(pengo, border)` → ТО `stun(sno_bee, n)` для всіх, хто торкається цього борту.
- КОЛИ `contact(pengo, sno_bee)` → ЯКЩО `state(sno_bee, stunned)` → ТО `disappear_b`, `score(100)` (розчавити блоком — 400); інакше `lose` (`lives(-1)`).
- КОЛИ `pattern(line(3, diamond))` → ЯКЩО `custom: «жоден не торкається борту»` → ТО `score(10000)`; інакше `score(5000)`; і `stun(all_sno_bees, n)`.
- КОЛИ `timer(120 s)` без смерті й перемоги → ТО `transform(sno_bee → blob)` для всіх; Blob — `custom: «до борту, ламаючи лід, далі в кут і зникнути»`.
- КОЛИ `died(sno_bee)` → ЯКЩО `count(sno_bee, ==, 1)` (знищено одного з двох останніх) → ТО через 12 с `transform(last → blob)`; якщо за раз знищено кількох і лишився один — одразу.
- КОЛИ `all_gone(sno_bee)` (і яйця) або всі Blob-и втекли/знищені → ТО `win` раунду, `next_level`; ЯКЩО `timer(<, 60 s)` → ТО `score(5000 | 2000 | 1000 | 500 | 10)` за 0–19 / 20–29 / 30–39 / 40–49 / 50–59 с.
- Кожні 2 раунди — інтермісія (одна з 6 анімацій); 16 раундів, далі послідовність повторюється.
- Перемога: очистити раунд. · Поразка: дотик неоглушеного Sno-Bee/Blob → `lives(-1)`; 0 → `game_over`. · Рахунок: блок 30, розчавлені 400/1600/3200, яйце 500, оглушений 100, діаманти 5000/10000, бонус за час 10…5000.

## Керування і ввід
- Джойстик 4 напрямки — рух; одна кнопка — дія в напрямку погляду: штовхнути блок / розбити блок / трусити борт.
- Дія контекстна: ефект залежить від того, що перед Pengo і чи вільно за ним.

## Вікна, меню, HUD
- `splash-screen` / attract mode з демо й таблицею рекордів (аркада).
- `game-screen`: поле; HUD — `score`, `hi-score`, `lives`, `level-number` (раунд), лічильник яєць, що лишились (`+ui:egg-counter`, (?)).
- `custom-window` «інтермісія»: анімація кожні 2 раунди, одна з 6 (`+window:intermission`).
- `end-screen`: бонус за час після раунду (?).
- `leaderboard`: ввід ініціалів після game over.
- Переходи: attract → (монета) game-screen раунд 1 → … → інтермісія → наступний раунд; смерть → той самий раунд; 0 життів → leaderboard → attract.

## Фічі поза полем
- `levels-sequential` 16 раундів із зростанням темпу (`progress-acceleration`); `leaderboard-local` ініціали.
- DIP-перемикачі аркади: кількість життів, бонусне життя, складність (?) — `difficulty-presets` на рівні оператора.
- Нема паузи/undo/збережень (аркада).

## Варіації й родичі
- Порти: Atari 2600/5200/8-bit, Game Gear (з новими режимами (?)), мобільні; клони на ZX/Amstrad тощо.
- Осі варіацій: **блок, якому нема куди їхати**: розбивається (Pengo) / стоїть (Sokoban) / не штовхається; **ковзання**: на 1 клітину / до упору (Pengo, Atomix, лід у Pokémon); **хто ламає лід**: лише гравець / і вороги; **шкода блоком**: чавить ворогів / ні.
- Родичі: Atomix (ковзання до упору як ядро пазла), Kickle Cubicle, Bomberman (руйнівний лабіринт), Dig Dug (вороги в лабіринті, що його гравець змінює).

## Цікавинки для курсу
- Ковзання блоку до упору з переносом ворогів на шляху і «розбити, якщо нема куди» — 📎.
- Sno-Bee, що ламають лід на шляху до гравця (погоня з модифікацією поля) — 🥉.
- Трусіння борту: оглушення всіх ворогів, які торкаються конкретної стіни — 🌱.
- Три діаманти в лінію (детектор шаблону серед рухомих блоків) + різний бонус «торкається борту чи ні» — 📎.
- Яйця в блоках: прихований спавн з поповненням до ліміту — 🥉.
- Анти-затягування: таймер 2 хв → вороги тікають; останній ворог тікає — 🌱.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls`; `push-object` + `inertia-slide` ↔ крижини ковзають до упору; `impassable-cells` ↔ борт; `destroy-all-enemies` ↔ ціль раунду; `touch-death` + `player-death` ↔ дотик Sno-Bee, життя; `spawn-points` + `reinforcements` ↔ яйця в блоках, поповнення; `temporary-modes` ↔ оглушення; `time-bonus` ↔ < 60 с; `event-points` + `combo-multiplier` ↔ кілька Sno-Bee одним блоком; `score-records`; `sequential-levels` + `progress-acceleration` ↔ 16 раундів.
- **Нема** → пропозиції карток:
  - `+crush-by-slide` «Розчавити ковзним обʼєктом» · entities/combat · 📎.
  - `+break-block` «Розбити блок, якому нема куди їхати» · entities/legality · 🌱 · слот {who: player|enemy|both}.
  - `+wall-shake-stun` «Удар по стіні оглушує ворогів біля неї» · entities/combat · 🌱.
  - `+line-up-bonus` «Бонус за вишикувані обʼєкти» · game-logic/score · 📎 · слот {n, touching_wall}.
  - `+flee-when-last` «Ворог тікає (останній / за таймером)» · entities/move · 📎.

## Пропозиції до словників
- `+trigger:input` — кнопка дії; `+trigger:after` — ворог гине по завершенні ковзання блоку; `+trigger:pattern` — `line(3, diamond)`; `+trigger:counter` — лишилось 2/1 Sno-Bee; `+trigger:timer` — 2 хв раунду.
- `+cond:free` / `+cond:occupied` — чи є куди ковзати.
- `+effect:slide`, `+effect:stun`, `+effect:transform` (Sno-Bee → Blob), `+effect:spawn_at` (вилуплення з конкретного блоку), `+effect:score`.
- `+role:container` — блок з яйцем.
- `+trigger:crushed_by` — сутність знищена обʼєктом, що рухається (подія для очок і комбо).
- `+window:intermission` — анімаційна вставка між раундами (аркади).
- `+ui:egg-counter` — лишилось яєць (?).

## Джерела
- ⭐ [Wikipedia: Pengo](https://en.wikipedia.org/wiki/Pengo_(video_game)) — керування, ковзання/розбиття, яйця, діаманти (10 000 / 5 000), оглушення бортом, Blob-и (2 хв, 12 с), 16 раундів, 6 інтермісій, порти.
- [Інструкція Pengo (Pixelated Arcade)](https://pixelatedarcade.com/games/pengo/documents/instruction-manual/6/) — очки (30 / 400 / 1600 / 3200 / 100 / 500), таблиця бонусу за час, 5 життів на старті.
- YouTube: пошук «pengo arcade 1982 gameplay» і «pengo arcade longplay».

## Непевне
- (?) Розмір поля (~13×15) і чи розстановка яєць випадкова — не перевірено.
- (?) 6400 за 4 Sno-Bee одним блоком — є лише в пошукових підсумках; інструкція доходить до 3 (3200). Чи інструкція аркадна, чи від порту — сторінка не каже; звідти ж «5 життів» (на аркаді — DIP?).
- (?) Лічильник яєць у HUD, окремий екран бонусу за час, DIP-налаштування, режими Game Gear — не перевірено.
- StrategyWiki і Sega Retro віддають 403 — не відкрились.
