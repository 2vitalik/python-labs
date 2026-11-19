---
title: Campfire Cooking
slug: campfire-cooking
aka: []
family: thinky
also: [push-slide]
klass: figure
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2017
platforms: [iOS, Android, PC, Mac, Steam Deck]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/679500/Campfire_Cooking/", best: true, note: "опис, трейлер, знімки; оновлення 2.0 — клавіатура й контролер"}
  - {kind: official, url: "http://www.laytonhawkes.com/campfire-cooking/", note: "100+ рівнів, ~8 годин, платформи, оцінки преси, пресскіт"}
  - {kind: itch, url: "https://hawkes.itch.io/campfire", note: "версія для Windows і macOS"}
  - {kind: other, url: "https://itunes.apple.com/us/app/campfire-cooking/id1226277306?mt=8", note: "App Store (iOS)"}
  - {kind: other, url: "https://www.pocketgamer.com/articles/075643/campfire-cooking-review-good-enough-to-eat/", note: "рецензія Pocket Gamer: рух шампурів, поворот за наявності місця, казанки, undo, підказка"}
  - {kind: other, url: "https://www.levelwinner.com/?p=12116", note: "поради: штовхання шампурів, підгоряння від зайвих ходів, необмежений undo, вільний порядок страв"}
  - {kind: other, url: "https://www.dropbox.com/s/42wq1buufot13ty/Campfire_Cooking_Presskit.zip?dl=1", note: "пресскіт: опис, 8 знімків, 3 GIF геймплею"}
  - {kind: youtube, url: "https://youtu.be/sGUl36nkyb8", note: "тизер-трейлер (з пресскіту)"}
stage: v1
coverage: 50
mechanics: [move-4dir, move-by-input, keyboard-controls, swipe-gestures, party-switch, push-object, orientation-state, button-toggle, puzzle-select, level-unlock, undo-unlimited, restart-level, movement-animation, +face-cooking, +skewer-piece, +pivot-rotate, +magnet-hold, +chapter-unlock-quota, +intermission-cutscene]
proposes: ["+effect:flip", "+feature:cutscene-replay", "+card:skewer-piece"]
author: opus
date: 2026-11-19
---

# Campfire Cooking — шампури над вогнищем: підсмаж кожен бік маршмелоу, не спаливши жодного

## Суть
Покрокова головоломка Layton Hawkes на маленькій сітці-вогнищі. Гравець по черзі керує кількома шампурами з їжею (маршмелоу, далі інші страви): рухає їх уперед, назад і вбік, повертає, коли є місце, штовхає одним шампуром інші. Рух убік перевертає їжу на інший бік, рух уздовж шампура — ні; бік, що опинився над вогнем, підсмажується, а повторне смаження палить їжу. Пізніші стежки додають казанки з фондю, які треба заштовхати на вогонь, магніти на шампурах і туристичні плити з кнопками. Між стравами — сценки з родиною, що мандрує рік стежками від лісу до гір.

## Поле і час
- Квадратна сітка клітин-вогнища (3D-сцена під кутом); частина клітин горить, частина — каміння, нерозпалені купки хмизу чи ряди конфорок плити. Ручки шампурів лежать за межею сітки, їжа — на кінці шампура.
- Покроково: хід = один рух або поворот вибраного шампура з усіма поштовхами; час над вогнем не важить — палить лише зайвий хід на вогонь.
- Видно все поле; випадковості нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Шампур | piece | колір ручки; активний / ні; 1–2 шматки їжі (?) | рух уперед, назад, убік; поворот, якщо є місце; штовхає інші шампури й казанки |
| Маршмелоу (та інша їжа) | object | стан кожного боку: сирий / підсмажений / згорілий | убік — перевертається, уздовж — ні; нижній бік над вогнем підсмажується |
| Вогонь | terrain | — | підсмажує нижній бік їжі, що опинилась на клітині; той самий бік удруге — згорів |
| Казанок з фондю | object | вміст (сир, ягоди, перець…) | штовхається; на вогні готується |
| Магніт на шампурі | object | замість їжі | притягує металевий казанок і тягне його за шампуром |
| Туристична плита | terrain | колір; увімкнена / вимкнена | ряд конфорок — вогонь, коли увімкнена (?) |
| Кнопка | switch | колір | вмикає плиту свого кольору, коли на ній їжа чи шампур (?) |
| Камінь / вугілля | static | — | перешкода на клітині (?) |
| Нерозпалений хмиз | terrain | — | не гріє (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(select)` → ТО `set_state(next_skewer, active)` — керувати можна лише активним шампуром.
- КОЛИ `input(dir)` → ЯКЩО `facing(skewer, ±dir)` (рух уздовж) and `free(cells_ahead)` → ТО `move(skewer, dir)`; їжа не перевертається.
- КОЛИ `input(dir)` → ЯКЩО `not facing(skewer, ±dir)` (рух убік) and `free(cells_ahead)` → ТО `move(skewer, dir)`, `custom: «їжа перевертається на інший бік»`.
- КОЛИ `contact(skewer, other_skewer)` → ЯКЩО `free(cell_behind)` → ТО `push` — штовхнутий шампур їде, не перевертаючи своєї їжі.
- КОЛИ `input(rotate_left|rotate_right)` → ЯКЩО `free(swept_cells)` → ТО `rotate(skewer, ±90)`; інакше `block`.
- КОЛИ `enter(food, fire)` → ЯКЩО `state(food.bottom, raw)` → ТО `set_state(food.bottom, toasted)`.
- КОЛИ `enter(food, fire)` → ЯКЩО `state(food.bottom, toasted)` → ТО `set_state(food, burnt)`, `lose` — далі лише undo чи рестарт.
- КОЛИ `contact(skewer, pot)` → ЯКЩО `free(cell_behind)` → ТО `push`.
- КОЛИ `enter(pot, fire)` → ТО `set_state(pot, simmered)` (?).
- КОЛИ `adjacent(magnet, pot)` → ТО `attach(pot, magnet)` — казанок їде разом із шампуром (?).
- КОЛИ `enter(food|skewer, button)` → ТО `set_state(stove_of_color, on)` (?).
- КОЛИ `counter(uncooked, ==, 0)` (жодного сирого боку, жодного неготового казанка) → ТО `win`, `window(dialogue-window)` (якщо є сценка), `next_level`.
- КОЛИ `input(Z)` → ТО `undo(1)`.
- КОЛИ `input(R)` → ТО `restart`.
- КОЛИ `input(C)` → ТО `window(dialogue-window)` — повтор сценки.
- Перемога: уся їжа приготована. · Поразка: згорілий бік — стан до undo/рестарту. · Рахунку нема.

## Керування і ввід
- ПК, версія 2.0 (2023): Space / A — вибрати чи перемкнути шампур; стрілки / WASD / лівий стік — рух; Q, E / правий стік — поворот; Z / B — undo; R / Y — рестарт; C / X — повтор сценки; Esc / Select / Start — меню; Enter / A — далі в сценці.
- Мобільні: свайпи; рецензія Destructoid (цитата зі сніпета пошуку) скаржиться, що свайп повороту часто сприймається як поштовх уперед і палить маршмелоу.

## Вікна, меню, HUD
- `puzzle-select` — сторінка стежки: назва («Pine Peak Trail»), «Meals Cooked 9/15», 15 мініатюр страв (жовта рамка — приготовано, значок репліки — є сценка), стрілки й точки для гортання стежок, замок «Next Trail: Solve 1 More», шестерня налаштувань, «назад».
- `game-screen` — вогнище з шампурами, без лічильників.
- `dialogue-window` — сценка: родина біля вогнища, репліки в бульбашках («How do we check PoseBook out here?»).
- `settings-window` — за шестернею (зміст (?)); `pause-menu` — меню на Esc (?).
- Переходи: стежка → страва → (усе приготовано) сценка → стежка; квота страв → відкрито наступну стежку.

## Фічі поза полем
- Понад 100 страв на кількох стежках по 15 (~8 годин); у межах стежки — вільний порядок, наступна стежка — після квоти розвʼязаних.
- `undo` без ліміту, `restart-level`, `hint` — підказка, коли зовсім застряг (Pocket Gamer; форма (?)).
- Сюжет сценками між стравами з повтором на C (`+feature:cutscene-replay`).
- 9 досягнень Steam (Mountaineer, Highlander, Voyager, Explorer, Expeditioner, Alpinist, Navigator, Volcanologist, Only We Few); 5 мов (EN, FR, IT, DE, ES); повна підтримка контролера з 2.0.

## Варіації й родичі
- Найближчий родич у корпусі — [Stephen's Sausage Roll](stephens-sausage-roll.md): гриль, боки, підгоряння, виделка-шампур; також [Kye](../push-slide/kye.md) (`+magnet-hold`), [Sokobond](sokobond.md) (`+pivot-rotate`).
- Осі варіацій:
  - **хто тримає шампур**: аватар з виделкою (Sausage Roll) / сам шампур — фігура гравця (тут);
  - **скільки боків**: 2 / 4 (`+face-cooking` слот faces);
  - **що гріє**: постійний вогонь / плита за кнопкою / нерозпалене вогнище (тут — усі);
  - **перепечене**: згорає й програш (тут, Sausage Roll) / без кари.

## Цікавинки для курсу
- Шампур як довга фігура: рух уздовж — без перевертання, убік — перевертає їжу — 🥉.
- Стан кожного боку (сирий / підсмажений / згорілий) і перемога «кожен бік рівно раз» — 🥉.
- Поштовх шампура шампуром без перевертання їжі штовхнутого — 📎.
- Поворот на 90°, лише якщо вільні клітини, які замітає шампур — 🥉.
- Магніт, що тягне казанок; кнопка кольору вмикає ряд конфорок — 📎 кожне.
- Розвʼязувач BFS: стан = позиції й орієнтації шампурів + боки всієї їжі + казанки — 🥈.

## Мапа на каталог
- Є: `move-4dir` · `move-by-input` · `keyboard-controls` · `swipe-gestures` ↔ рух шампура; `party-switch` ↔ вибір шампура; `push-object` ↔ шампури й казанки; `orientation-state` ↔ боки їжі; `button-toggle` ↔ кнопка й плита; `puzzle-select` + `level-unlock` ↔ стежки; `undo-unlimited` · `restart-level` · `movement-animation`.
- **Нема** → пропозиції карток:
  - `+skewer-piece` «Шампур: довга фігура з їжею на кінці, рух убік перевертає їжу» · entities/move · 🥉 · слоти {food: 1..2}.
  - `+face-cooking` (вже в корпусі, Sausage Roll) · `+pivot-rotate` · `+magnet-hold` · `+chapter-unlock-quota` · `+intermission-cutscene` — вже в корпусі.

## Пропозиції до словників
- `+effect:flip` — перевернути обʼєкт на інший бік (тут `custom: «їжа перевертається на інший бік»`).
- `+feature:cutscene-replay` — повторити сюжетну сценку рівня окремою клавішею.
- `+card:skewer-piece` — див. «Мапа на каталог».
- ⏳-слова, вжиті тут: `input`, `facing`, `adjacent`, `counter`, `set_state`, `attach`, `rotate`, `window`, `undo`, `restart`, `next_level`.

## Джерела
- ⭐ [Steam: Campfire Cooking](https://store.steampowered.com/app/679500/Campfire_Cooking/) — опис («Twist, rotate and jostle skewers around the fire… Push fondue pots, play with magnets or maybe just use a camping stove if the fire won't light»), дата 18.10.2017; новина «Campfire Cooking 2.0» з повною розкладкою керування (прочитано через Steam API).
- [Офіційна сторінка](http://www.laytonhawkes.com/campfire-cooking/) — 100+ рівнів, ~8 годин, iOS/Android/Steam/Steam Deck, Metascore 84, Game of the Day в App Store.
- [Пресскіт](https://www.dropbox.com/s/42wq1buufot13ty/Campfire_Cooking_Presskit.zip?dl=1) — опис, 8 знімків (вогнище, казанки, магніти, плити з кнопками, вибір страв, сценка), 3 GIF (рух шампурів, поворот, магніт тягне казанок на вогонь).
- [Pocket Gamer](https://www.pocketgamer.com/articles/075643/campfire-cooking-review-good-enough-to-eat/) — шампури рухаються вперед, назад і вбік, повертаються, якщо є місце; казанки треба «заштовхати на місце»; undo, рестарт, підказка; кожен набір рівнів додає механіку.
- [Levelwinner](https://www.levelwinner.com/?p=12116) — поштовх шампура зсуває інші й не перевертає маршмелоу; палять зайві ходи, а не час; undo без ліміту; вільний порядок рівнів.
- [itch](https://hawkes.itch.io/campfire) · [App Store](https://itunes.apple.com/us/app/campfire-cooking/id1226277306?mt=8) · [тизер](https://youtu.be/sGUl36nkyb8).
- Рецензії Destructoid і appunwrapper (403 у фетчі) — цитати про «обидва боки» маршмелоу й свайп повороту відомі лише зі сніпетів пошуку.

## Непевне
- (?) Скільки боків має їжа (2 чи 4) і на скільки повертає крок убік: джерела кажуть «flip» і «both sides», GIF цього не розрізняють.
- (?) Точне правило підгоряння (другий захід того самого боку на вогонь) — за аналогією зі Sausage Roll і словами «палять зайві ходи»; чи буває «перепечений, але не згорілий» стан — невідомо.
- (?) Поведінка казанка на вогні, магніту (тягне чи лише тримає), кнопок і плит (перемикач чи тримання), каміння й нерозпаленого хмизу — зі знімків і GIF, без тексту правил.
- (?) Скільки шматків їжі на шампурі (на знімку — до двох) і що стається з їжею за межею сітки.
- (?) Кількість стежок (на знімку 8 точок-сторінок, стежка по 15 страв) і форма підказки.
- (?) Android — лише зі слів офіційного сайту («delivered the title across 5 platforms»).
