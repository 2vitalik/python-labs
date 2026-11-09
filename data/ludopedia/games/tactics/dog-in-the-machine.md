---
title: Dog in the Machine
slug: dog-in-the-machine
aka: [AutoDog]
family: tactics
also: [roguelike]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: setup
  goal: state
year: 2026
platforms: [Windows, macOS]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/4613180/Dog_in_the_Machine/", best: true, note: "офіційний опис: малі сітки, доміно-зіткнення, конвеєри, кнопки, вибухівка, превʼю послідовності, трюки й їх злиття, 8 порід; реліз 29.09.2026"}
  - {kind: other, url: "https://www.keengamer.com/articles/reviews/pc-reviews/dog-in-the-machine-review-a-tactical-roguelite-where-everything-can-go-boom-boom-pc/", note: "огляд: Energy і Alarm Level, типи ворогів, стрілки й лазери, трюки Boom Boom / Hunt Survivors, undo з поверненням енергії, складності, мета-валюти"}
  - {kind: other, url: "https://www.absolutegeeks.com/?p=173328", note: "огляд: те саме + породи (Wrecker/Shover і гілки), Irondog, seeded run"}
  - {kind: other, url: "https://www.dlcompare.com/gaming-news/dog-in-the-machine-turns-robot-dogs-into-tactical-masterminds-85268", note: "новина: ланцюг зіткнень від одного штовхання, перемикачі, злиття трюків"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Dog+in+the+Machine+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [push-object, hp-damage, explode-area, chain-detonation, chain-reaction, status-effects, telegraphed-intents, telegraph-marker, threat-range, carrier-platform, beam-tracing, melee-vs-ranged, spawner-entity, undo-unlimited, difficulty-levels, seed-share, match-setup, character-select, map-window, shop-between-levels, in-round-upgrades, game-screen, main-menu, end-screen, +action-points, +attack-modifier-trick, +trick-fusion, +alarm-meter, +retaliation, +domino-collision, +deck-builder, +meta-progression, +procedural-levels, +energy-refund-on-kill, +breed-unlock-tree]
proposes: ["+trigger:attacked", "+ui:alarm-bar", "+card:attack-modifier-trick", "+card:trick-fusion", "+card:alarm-meter", "+feature:mode-ironman"]
author: opus
date: 2026-11-09
---

# Dog in the Machine — один робопес на малій сітці: трюки на наступну атаку і ланцюгові реакції замість сили

## Суть
АвтоПес тікає з механічного міста крізь серію боїв на **компактних ізометричних сітках**, повних реактивних обʼєктів: стрілок-конвеєрів, лазерів, шипів, вибухівки, кнопок. Енергія оплачує і крок, і атаку, тож сили на всіх не вистачає — виграє той, хто штовхне одного робота так, щоб той збив інших («доміно»), або підпалить вибуховий ланцюг. Між боями пес вчиться **трюкам**, що чіпляються до наступної атаки, і зливає їх з атаками в нові. Поразка — не смерть пса, а заповнена шкала **тривоги** (Alarm).

## Поле і час
- Малі квадратні сітки в ізометрії (Steam: «compact grids»; огляд: «small isometric grids»); рівні генеруються процедурно.
- Покроково: хід гравця (дії за енергію, кожну можна скасувати) → кінець ходу фіксує стан → вороги виконують показані наміри.
- Інформація часткова: наміри ворогів і приріст тривоги від дії показано заздалегідь, але превʼю **не** показує всіх ланцюгових реакцій від твого ходу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| АвтоПес | player | HP, Energy; порода | рух і атаки породи (укус по площі, копняк, кидок, захоплення) |
| Робот ближнього бою | enemy | — | бʼє сусідню клітину |
| Дальній / площинний робот | enemy | — | бʼє з відстані або кілька клітин одразу |
| Реактивний робот | enemy | — | у відповідь на удар бʼє все навколо, хоч би хто стояв поруч |
| Штовхач | enemy | — | штовхає обʼєкти по сітці |
| Спавнер | spawner | — | посеред бою додає юнітів або обʼєкти |
| Охоронець / бос | boss | — | напр., при ударі шкодить усім сусідам — включно з власним ескортом |
| Ящик | object | — | штовхається |
| Вибухова перешкода | object | — | вибухає, запускає ланцюг |
| Стрілка | terrain | напрям | зсуває того, хто стоїть, у фіксованому напрямку |
| Стаціонарний лазер | hazard | лінія видима | неактивний, доки його не вдарять; тоді стріляє по лінії |
| Шипи | hazard | — | пастка, шкодить |
| Кнопка / перемикач | switch | — | вмикає ефект на полі (?) |
| Трюк | supply | бібліотека трюків | модифікує наступну атаку (Boom Boom, Hunt Survivors, Wide Bite…) |
| Кістки | resource | — | валюта забігу: Blueprint-и на Training Station |
| TechShards · Dog XP · Nexus Intel | resource | мета | постійні апгрейди · рівні породи · сюжетний вузол Nexus |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, cell)` → ЯКЩО `counter(energy, >=, cost)` → ТО `move(dog, cell)`, `counter(energy, -cost)`.
- КОЛИ `input(attack, a, target)` → ЯКЩО `counter(energy, >=, cost)` → ТО `damage(target, n)` за патерном атаки, `counter(energy, -cost)`.
- КОЛИ `input(attack, a, target)` → ЯКЩО `state(dog, trick_armed)` → ТО `custom: «ефект трюку на всі цілі атаки»`, `clear_state(dog, trick_armed)`.
- Boom Boom: КОЛИ `input(attack, a, target)` → ЯКЩО `state(dog, boom_boom)` → ТО `set_state(hit, explosive)`; КОЛИ `destroyed(a)` → ЯКЩО `state(a, explosive)` → ТО `damage(adjacent8(a), 2)` (сусіди з діагоналями).
- Hunt Survivors: КОЛИ `input(attack, a, target)` → ЯКЩО `state(dog, hunt)` → ТО `set_state(hit, hunted)`; КОЛИ `destroyed(a)` → ЯКЩО `state(a, hunted)` → ТО `counter(energy, +2)`.
- КОЛИ `after(push(a))` → ЯКЩО `occupied(cell_behind, b)` → ТО `custom: «зіткнення; b може полетіти далі — ланцюг доміно»` (шкода — (?)).
- КОЛИ `enter(a, arrow)` → ТО `move(a, arrow_dir)`.
- КОЛИ `contact(attack, laser)` → ТО `custom: «лазер стріляє по видимій лінії»`, `damage` кожному на лінії.
- КОЛИ `enter(a, spikes)` → ТО `damage(a, n)` (?).
- КОЛИ `destroyed(explosive_obstacle)` → ТО `explode(area, n)` → `trigger(chain)` сусідніх вибухівок.
- КОЛИ `contact(a, button)` → ТО `custom: «вмикає звʼязаний ефект»` (?).
- КОЛИ `after(damage(reactive))` → ТО `damage(adjacent(reactive), n)` — `custom: «відповідь бʼє всіх сусідів, і ворогів теж»`.
- КОЛИ `turn_start(player)` → ТО `custom: «кожен ворог показує наступну дію»`; КОЛИ `turn_end(player)` → ТО вороги виконують показане.
- КОЛИ `custom: «атака ворога»` → ТО `counter(alarm, +n)`; шкода, завдана гравцем, `custom: «гасить приріст, але не знижує накопичене»`.
- КОЛИ `counter(alarm, >=, max)` → ТО `lose` (кінець забігу).
- КОЛИ `counter(alarm, >=, threshold)` → ЯКЩО `not difficulty(puppy)` → ТО `custom: «ефект порогу тривоги»`.
- КОЛИ `input(undo)` → ЯКЩО `not mode(irondog)` → ТО `undo(1)`, `counter(energy, +refund)`; після `end_turn` — `block`.
- КОЛИ `custom: «бій виграно»` → ТО `choose(new_trick)` (новий трюк після кожного бою).
- КОЛИ `input(fuse, blueprint)` → ЯКЩО `counter(bones, >=, cost)` → ТО `custom: «трюк назавжди вплавлено в атаку»` (Wide Bite → Wide Bite+ з Boom Boom).
- КОЛИ `game_over` → ТО `currency(techshards, +n)`, `counter(dog_xp, +n)`, `counter(nexus_intel, +n)`.
- КОЛИ `counter(dog_xp_level, ==, 2|3|4)` → ТО `unlock(breed)` у гілці породи.
- Перемога: саботувати вузол Nexus (сюжетна мета забігів) · Поразка: шкала тривоги заповнена · Рахунок: мета-валюти забігу.

## Керування і ввід
- Мишею: вибір атаки (кнопки атак породи) → клітина-ціль з превʼю шкоди, намірів і приросту тривоги; клік по клітині — рух.
- Кожну дію можна скасувати окремо з поверненням енергії (без ліміту в стандартному режимі); «End turn» фіксує хід.
- Run Settings: складність, Irondog (без вільного скасування), seeded run.

## Вікна, меню, HUD
- `main-menu` → `match-setup` «Run Settings» (складність Puppy / Doggo / Elite Dog 1, Irondog, seed) → `character-select` (8 порід: Wrecker → Ravager, Corroder, Hound; Shover → Jungler, Toy Master, Wrestler).
- `map-window` — райони міста з вузлами: бої, Training Station, персонажі, Nexus.
- `dialogue-window` — дивакуваті персонажі: купити, обміняти, вкрасти, прокачати трюк.
- `upgrade-window` / `shop-window` — Training Station: Blueprint-и за кістки; постійні AutoDog Upgrades за TechShards (Custom Training 100, Wealthy Dog 400, Second Chance 600, More Attacks 1000).
- `inventory-window` — Trick Library.
- `game-screen`: ізометрична сітка; `hp-bar`; `energy-bar`; шкала тривоги; `telegraph-marker` (наміри ворогів); `threat-range`; `ability-buttons` (атаки); `undo-button`; `end-turn-button`.
- `end-screen` — підсумок забігу: TechShards, Dog XP, Nexus Intel.

## Фічі поза полем
- `difficulty-presets`: Puppy (без модифікаторів районів і ефектів тривоги, +6 max HP) → Doggo → Elite Dog 1 (кожна відкривається після попередньої, кращі нагороди).
- Irondog — без вільного скасування; `seed-input` (seeded run).
- `meta-progression`: TechShards → постійні апгрейди; Dog XP → трюки, чипсети, породи; Nexus Intel → сюжетний вузол.
- Процедурні рівні, «нескінченна» кількість.

## Варіації й родичі
- Родичі: [Into the Breach](into-the-breach.md) (наміри ворога + середовище), [Fights in Tight Spaces](fights-in-tight-spaces.md) (один герой, штовхання, реталіація), [Tactical Breach Wizards](tactical-breach-wizards.md) (необмежений відкат ходу), [ENYO](enyo.md) (один герой, середовище як зброя), [Mech Armada](mech-armada.md) (роглайт з малими полями).
- **Осі варіацій**: ресурс програшу — HP героя / спільна шкала (тривога тут, мережа ITB) · модифікатор атаки — постійний / разовий трюк / вплавлений назавжди · відкат — нема / кожна дія з поверненням ресурсу / весь хід раз за бій.

## Цікавинки для курсу
- Трюк-модифікатор: стан «наступна атака має ефект X», що знімається після атаки — 📎; злиття трюку з атакою в нову атаку (композиція ефектів) — 🥈.
- Boom Boom: позначка «вибуховий» + вибух при знищенні, що ланцюжить інші позначені — 🥉 (черга подій знищення).
- Шкала тривоги, яку ворожі атаки наповнюють, а шкода гравця лише гальмує — 🌱, але змінює стиль гри.
- Undo кожної дії з поверненням енергії до кінця ходу — 📎 (стек станів у межах ходу).
- Реталіація реактивного ворога по всіх сусідах — 📎 (ворога можна обернути проти ескорту).
- Превʼю, яке свідомо не показує ланцюгів, — тема для дискусії «скільки показувати гравцеві» — 🥉.

## Мапа на каталог
- Є: `push-object` · `hp-damage` · `explode-area` + `chain-detonation` + `chain-reaction` · `status-effects` (Hunted, Explosive) · `telegraphed-intents` + `telegraph-marker` + `threat-range` · `carrier-platform` (стрілки) · `beam-tracing` (лазер) · `melee-vs-ranged` · `spawner-entity` · `undo-unlimited` · `difficulty-levels` · `seed-share` · `character-select` · `map-window` · `shop-between-levels` · `in-round-upgrades` (трюки).
- **Нема** → пропозиції карток:
  - `+attack-modifier-trick` «Трюк на наступну атаку» · entities/combat · 📎 · слот {effect}.
  - `+trick-fusion` «Злиття трюку з атакою» · game-logic/economy · 🥈 — композиція ефектів.
  - `+alarm-meter` «Спільна шкала тривоги = програш» · game-logic/lose · 🌱 · слот {max, thresholds}.
  - `+domino-collision` «Штовхнутий збиває наступного» · entities/combat · 🥉.
  - `+retaliation` «Удар у відповідь по сусідах» · entities/combat · 📎.
  - `+energy-refund-on-kill` «Енергія за вбивство позначеного» · game-logic/economy · 🌱.
  - `+breed-unlock-tree` «Рівень персонажа відкриває його варіанти» · levels/progression · 📎.

## Пропозиції до словників
- `+trigger:attacked` — сутність щойно отримала удар (реталіація; вже пропонували Fights in Tight Spaces, Persona 5 Tactica).
- `+ui:alarm-bar` — шкала глобальної тривоги з порогами й превʼю приросту від дії.
- `+card:attack-modifier-trick` · `+card:trick-fusion` · `+card:alarm-meter` — див. «Мапа на каталог».
- `+feature:mode-ironman` — режим без скасувань (Irondog; Ironman у Zero Orders Tactics).

## Джерела
- ⭐ [Steam: Dog in the Machine](https://store.steampowered.com/app/4613180/Dog_in_the_Machine/) — опис елементів поля, превʼю і повтор, трюки, 8 порід, дата.
- [KeenGamer: огляд](https://www.keengamer.com/articles/reviews/pc-reviews/dog-in-the-machine-review-a-tactical-roguelite-where-everything-can-go-boom-boom-pc/) — Energy/Alarm, вороги, стрілки, лазери, трюки, undo, складності, мета-валюти й ціни апгрейдів.
- [Absolute Geeks: огляд](https://www.absolutegeeks.com/?p=173328) — те саме, гілки порід, Irondog, seeded run.
- [DLCompare](https://www.dlcompare.com/gaming-news/dog-in-the-machine-turns-robot-dogs-into-tactical-masterminds-85268) — ланцюг зіткнень від штовхання, перемикачі.

## Непевне
- (?) Умова перемоги окремого бою (знищити всіх? протриматись?) — у джерелах лише «серія зіткнень».
- (?) Шкода від зіткнення в «доміно», від шипів і лазера; що роблять кнопки.
- (?) Що буде при HP пса = 0 (окремо від тривоги).
- (?) Чипсети — лише згадка (Dog XP їх відкриває, патч про «нескінченний рух»).
