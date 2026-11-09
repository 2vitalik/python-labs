---
title: Infra Arcana (огляд з The Ground Gives Way і Zorbus)
slug: infra-arcana
aka: [IA, The Ground Gives Way, TGGW, Zorbus]
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
year: 2011
platforms: [PC, Linux]
links:
  - {kind: other, url: "https://www.roguebasin.com/index.php/Infra_Arcana", best: true, note: "RogueBasin: шок і божевілля замість голоду, досвід не за вбивства (стелс), 6 класів, трейти, spirit points, рани"}
  - {kind: official, url: "https://sites.google.com/site/infraarcana", note: "сайт IA: сетинг, натхнення (Лавкрафт, B-хорор, Blood), завантаження v23 (2025)"}
  - {kind: other, url: "https://gitlab.com/martin-tornqvist/ia", note: "відкритий код Infra Arcana"}
  - {kind: official, url: "https://www.thegroundgivesway.com/", note: "TGGW: без XP і рівнів, тренування за гроші, без регенерації HP, ~700 предметів, 180+ монстрів"}
  - {kind: other, url: "https://www.roguebasin.com/index.php/The_Ground_Gives_Way", note: "RogueBasin: TGGW, 2014, coffeebreak, інтерактивні обʼєкти мапи"}
  - {kind: official, url: "https://zorbus.net/", note: "Zorbus: без класів, d20, динамічне світло, монстри бʼються між собою, рекрутинг, сейв видаляється при завантаженні"}
  - {kind: other, url: "https://www.roguebasin.com/index.php/Zorbus", note: "RogueBasin: Zorbus, Joonas Hirvonen, 2019"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=infra+arcana+roguelike+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-8dir, keyboard-controls, console-render, dungeon-generation, stairs-levels, hp-damage, status-effects, inventory-items, item-pickup, melee-vs-ranged, projectile-shot, explode-area, fog-of-war, line-of-sight-attack, chase-player, permadeath, player-death, message-log, unit-xp-skills, +sanity-meter, +stealth-awareness, +xp-from-discovery, +light-and-darkness, +wounds-need-treatment, +lethal-mana, +monster-infighting, +recruit-companion, +paid-training, +no-regen, +save-delete-on-load]
proposes: ["+trigger:noticed(a, b)", "+trigger:discovered(kind)", "+cond:aware(a, b)", "+cond:lit(cell)", "+effect:shock(+n)", "+effect:add_phobia", "+effect:recruit(a)", "+ui:shock-meter", "+ui:insanity-meter", "+ui:spirit-bar", "+feature:background-select", "+feature:trait-pick", "+feature:save-delete-on-load"]
author: opus
date: 2026-11-09
---

# Infra Arcana (і сусіди) — «тихі» сучасні роглайки: страх замість голоду, стелс замість гринду, досвід за відкриття

## Суть
Файл-огляд трьох інді-роглайків 2010-х, що переробляють класичну формулу Rogue заради **атмосфери й рішень без гринду**. Основа — **Infra Arcana** (Martin Törnqvist, 2011): Лавкрафт на початку XX ст., герой спускається в лігво Церкви Зоряної Мудрості по Сяючий Трапецоедр. Замість голоду — **шок і божевілля**; досвід дають **не вбивства**, а відкриття нових предметів і ворогів та спуск, тому стелс — повноцінна стратегія. Поруч: **The Ground Gives Way** (2014) — без XP і рівнів, сила лише з речей і платного тренування; **Zorbus** (2019) — «живе підземелля» з динамічним світлом, монстрами, що бʼються між собою й кличуть підмогу.

## Поле і час
- Квадратна сітка, консольна/тайлова графіка (TGGW — консольний інтерфейс без команд для заучування; Zorbus — тайли 32/48/64 px або ASCII).
- Час: класичний хід = дія; деталі швидкості не описані джерелами.
- IA: світло й темрява поверху — частина страху (темрява, ймовірно, підвищує шок (?)). Zorbus: **динамічне світло** — джерела є меблями або в руках істот, їх можна запалити/загасити; деякі істоти бачать у темряві.
- TGGW: рівні малі й нечисленні, повна гра — 1–2 години; авто-біг, мапа і портали для швидкого пересування.
- Zorbus: рівні різної форми з тематичними зонами (тронні зали, тюрми, сховки скарбів) і хорошою звʼязністю.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой IA | player | HP, spirit points, шок %, божевілля, клас, трейти, рани | 8 напрямків; бій, стрільба, закляття зі сувоїв |
| Клас IA: War Veteran / Rogue / Ghoul / Occultist / Exorcist / Flagellant | player | стартові речі, трейти | задає стиль (стрілок, тихий, маг, «гуль») |
| Культисти й чудовиська IA | enemy | — | помітивши, атакують; видовище тварюк росте шок |
| Сходи вниз | static | — | спуск: скидає шок рівня, дає досвід |
| Сувій заклинання | pickup | ціна в spirit points | можна запамʼятати й кастувати |
| Зброя XX ст. (вила, Томмі-ган, динаміт) | pickup / projectile | набої, вибух | мілі, стрільба, кидок вибухівки |
| Медичний набір (?) | pickup | заряди | лікує серйозні рани, що не гояться самі |
| Герой TGGW | player | HP без регенерації, речі | сила — лише предмети й тренування |
| Тренер TGGW | neutral | ціна | за гроші підвищує вміння |
| Інтерактивний обʼєкт мапи TGGW | static | рідкість | різні ефекти на гравця при взаємодії |
| Портал TGGW | static | — | швидке пересування між рівнями |
| Герой Zorbus | player | раса, рівень, навички й таланти (d20) | point-buy при кожному рівні |
| Істота Zorbus | enemy / neutral | світло/темнобачення, предмети | реагує на світло й звук, тікає, кличе союзників, бʼється з іншими, підбирає речі, коментує бульбашками |
| Компаньйон Zorbus | ally | — | завербована істота йде з героєм |
| Джерело світла Zorbus | object | запалене/згасле | освітлює клітини навколо |

## Правила (КОЛИ → ЯКЩО → ТО)
Infra Arcana — страх:
- КОЛИ `line_of_sight(hero, monster)` → ЯКЩО `first_time` (?) → ТО `counter(shock, +n)`.
- КОЛИ `timer(every N ходів)` на рівні → ТО `counter(shock, +n)` — затримуватися страшно.
- КОЛИ `input(stairs)` → ТО `counter(shock, =0)`, `next_level`, `counter(xp, +n)`.
- КОЛИ `counter(shock, >=, max)` → ТО `counter(insanity, +n)`, `custom: «негативний трейт або фобія»`.
- КОЛИ `counter(insanity, >=, max)` → ТО `lose` (?).

Infra Arcana — досвід і стелс:
- КОЛИ `hp_zero(enemy)` → ТО `custom: «досвіду не дає»`.
- КОЛИ `custom: «уперше побачено новий тип предмета чи ворога»` → ТО `counter(xp, +n)`; ЯКЩО `counter(xp, >=, threshold)` → ТО `choose(traits)`.
- КОЛИ `input(attack, enemy)` → ЯКЩО `custom: «ворог не помітив героя»` → ТО `custom: «підступний удар з бонусом»` (?).
- КОЛИ `line_of_sight(enemy, hero)` → ЯКЩО `custom: «перевірка стелсу провалена»` → ТО `set_state(enemy, hunting)`.

Infra Arcana — магія й рани:
- КОЛИ `input(cast, spell)` → ТО `counter(spirit, −cost)` + ефект; КОЛИ `counter(spirit, ==, 0)` → ТО `lose` — магія може вбити.
- КОЛИ `custom: «серйозна рана»` → ТО `set_state(hero, wounded)`; ЯКЩО `not has(hero, medical)` → ТО рана не гоїться сама.
- КОЛИ `input(throw, dynamite)` → ТО `custom: «таймер фітиля»` → `explode(area)`.

The Ground Gives Way:
- КОЛИ `hp_zero(enemy)` → ТО `custom: «досвіду й рівнів нема»`.
- КОЛИ `timer(every)` → ТО `custom: «HP не відновлюються самі»`; лікування — предмети, відпочинок і їжа як ресурс (?).
- КОЛИ `input(train, skill)` → ЯКЩО `has(hero, money >= price)` → ТО `currency(−price)`, `custom: «вміння +1»`.

Zorbus:
- КОЛИ `custom: «істоті загрожують»` → ТО `custom: «тікає або кличе союзників»`.
- КОЛИ `line_of_sight(monster_a, monster_b)` → ЯКЩО `custom: «ворожі між собою»` → ТО `damage(n)` один одному.
- КОЛИ `input(recruit, creature)` → ТО `custom: «істота стає компаньйоном»`.
- КОЛИ `input(toggle, light)` → ТО `set_state(light, lit|unlit)`; ЯКЩО `lit(cell)` → ТО `custom: «клітину видно істотам без темнобачення»`.
- КОЛИ `input(load_save)` → ТО `custom: «файл сейву видаляється»` — сейв лише для перерви, не для відкату.

Перемога / поразка:
- IA: знайти Сяючий Трапецоедр → `win`. Zorbus: знайти портал до Зорбуса → `win`. TGGW: дійти до кінця підземелля (?).
- Поразка — смерть (`permadeath` у всіх трьох); в IA ще й божевілля або виснаження духу.

## Керування і ввід
- Клавіатура (8 напрямків, команди). TGGW — інтерфейс «без клавіш для запамʼятовування» (контекстні дії). Zorbus — перепризначення клавіш, мишка (неідеальна), геймпад, система прицілювання для стрільби й талантів, швидкі слоти.

## Вікна, меню, HUD
- `main-menu` → IA: `character-select` (клас) → `game-screen`.
- `game-screen` IA: поле, рядок статусу з HP, spirit, `shock-meter` у %, `insanity-meter`, `message-log`.
- `inventory-window` + `equipment-slots`; вибір трейту на рівні — `upgrade-window`.
- TGGW: `map-window` + портали; Zorbus: `settings-window` (розмір екрана, шрифт, тайли/ASCII), онлайн-`help-window` (мануал, туторіал), `leaderboard` (онлайн).
- `end-screen` — смерть, причина, глибина.

## Фічі поза полем
- IA: `background-select` (6 класів), `trait-pick` при рівні; атмосферний звук; відкритий код.
- Zorbus: `save-delete-on-load`, `tutorial`, онлайн-генератор підземель і таблиця рекордів, 4000+ звукових ефектів, `font-scale`, `fullscreen`.
- TGGW: «coffee break»-довжина (до 2 год), без гринду.
- Свідомо прибране: IA — голод; Zorbus — ідентифікація предметів і голод; TGGW — XP, класи, раси, регенерація HP.

## Варіації й родичі
- Родичі в корпусі: [Sil](sil.md) (стелс і досвід не за вбивства — та сама ідея), [Brogue](brogue.md) (без класів, речі = білд), [Dungeon Crawl Stone Soup](dungeon-crawl-stone-soup.md) (без регенерації в певних видах), [Caves of Qud](caves-of-qud.md) (живий світ, фракції), [Rogue](rogue.md).
- Осі варіацій: **таймер-тиск** (голод — Rogue / шок і божевілля — IA / нема — Zorbus); **джерело досвіду** (вбивства / відкриття й спуск — IA / нема — TGGW); **сейв** (вільний / видаляється при завантаженні — Zorbus); **AI** (тупий переслідувач / тікає, кличе підмогу, бʼється з іншими — Zorbus); **світло** (статичне / динамічне з вимикачами — Zorbus).

## Цікавинки для курсу
- Шок-метр: росте від побаченого й від затримки, скидається сходами, переповнення → фобія — 📎 (лічильник із двома джерелами й порогом).
- Досвід за відкриття, не за вбивства — 🌱 (одна таблиця «бачено вперше»), але міняє всю стратегію.
- Стан «помітив / не помітив» для кожного ворога і підступний удар — 🥉.
- Динамічне світло, що впливає на видимість для всіх істот, — 🥈 (FOV з освітленістю клітин).
- Монстри, що бʼються між собою й кличуть підмогу, — 🥈 (фракції + відносини).
- Сейв, що видаляється при завантаженні, — 🌱.

## Мапа на каталог
- Є: `move-8dir` · `keyboard-controls` · `console-render` · `dungeon-generation` · `stairs-levels` · `hp-damage` · `status-effects` · `inventory-items` · `item-pickup` · `melee-vs-ranged` · `projectile-shot` · `explode-area` (динаміт) · `fog-of-war` · `line-of-sight-attack` · `chase-player` · `permadeath` · `player-death` · `message-log` · `unit-xp-skills`.
- **Нема** → пропозиції карток:
  - `+sanity-meter` «Шок/божевілля як таймер-тиск» · entities/state · 📎 · слоти {sources, reset_on, overflow_effect}.
  - `+stealth-awareness` «Стан уваги ворога й підступний удар» · entities/state · 🥉.
  - `+xp-from-discovery` «Досвід за перше бачене, не за вбивства» · entities/state · 🌱.
  - `+light-and-darkness` «Освітленість клітин впливає на видимість» · interface/render · 🥈.
  - `+wounds-need-treatment` «Рани, що не гояться без ліків» · entities/state · 📎.
  - `+lethal-mana` «Ресурс заклинань, нуль якого вбиває» · entities/state · 🌱.
  - `+monster-infighting` «Монстри ворожі між собою» · game-logic/opponent · 🥈.
  - `+recruit-companion` «Завербувати істоту в союзники» · entities/interact · 📎.
  - `+paid-training` «Сила за гроші замість XP» · game-logic/economy · 🌱.
  - `+no-regen` «HP не відновлюються самі» · entities/state · 🌱.
  - `+save-delete-on-load` «Сейв видаляється при завантаженні» · game-logic/save · 🌱.

## Пропозиції до словників
- `+trigger:noticed(a, b)` — A помітив B (стелс).
- `+trigger:discovered(kind)` — гравець уперше побачив тип предмета/ворога.
- `+cond:aware(a, b)` — A знає про B.
- `+cond:lit(cell)` — клітина освітлена.
- `+effect:shock(+n)` — додати до шок-метра.
- `+effect:add_phobia` — додати негативний трейт/фобію.
- `+effect:recruit(a)` — сутність стає союзником.
- `+ui:shock-meter` · `+ui:insanity-meter` · `+ui:spirit-bar` — індикатори IA.
- `+feature:background-select` — клас-передісторія на старті · `+feature:trait-pick` — вибір пасивного трейту при рівні · `+feature:save-delete-on-load`.

## Джерела
- ⭐ [RogueBasin: Infra Arcana](https://www.roguebasin.com/index.php/Infra_Arcana) — шок і божевілля, стелс, 6 класів, трейти, spirit points, рани, зброя, 2011.
- [Infra Arcana (сайт)](https://sites.google.com/site/infraarcana) — сетинг, натхнення, завантаження v23.0.0 (2025).
- [GitLab: martin-tornqvist/ia](https://gitlab.com/martin-tornqvist/ia) — код.
- [The Ground Gives Way](https://www.thegroundgivesway.com/) · [RogueBasin: TGGW](https://www.roguebasin.com/index.php/The_Ground_Gives_Way) — без XP, тренування, без регенерації, ~700 предметів.
- [Zorbus](https://zorbus.net/) · [RogueBasin: Zorbus](https://www.roguebasin.com/index.php/Zorbus) — d20, світло, AI, рекрутинг, сейв-видалення.
- YouTube: [пошук «infra arcana roguelike gameplay»](https://www.youtube.com/results?search_query=infra+arcana+roguelike+gameplay).

## Непевне
- (?) Статей у Wikipedia нема ні для однієї з трьох; WebSearch вичерпано; мануал Zorbus не віддав текст — деталі механік (швидкість, точні пороги шоку, умови «помітив») не підтверджені.
- (?) IA: що саме підвищує шок (темрява, першe бачення тварюки, закляття), чи божевілля 100 % = смерть, підступний удар, медичний набір, кількість рівнів — з памʼяті.
- (?) TGGW: як працюють відпочинок і їжа, мета гри, розробник (не названо на сторінках).
- (?) Zorbus: кількість рівнів, «вбудовані зони» з черги — тематичні частини рівнів (джерело), чи є префаби-вольти окремо — не підтверджено.
