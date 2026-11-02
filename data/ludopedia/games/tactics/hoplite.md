---
title: Hoplite
slug: hoplite
family: tactics
also: [roguelike, chess-abstract]
klass: figure
axes:
  field: hex
  time: turn
  opponent: ai
  info: full
  random: setup
  goal: state
year: 2013
platforms: [iOS, Android, web (Challenge Mode)]
links:
  - {kind: youtube, url: "https://www.youtube.com/watch?v=-ABUS0t0Qaw", best: true, note: "відео з офіційної сторінки — геймплей"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hoplite_(video_game)", note: "огляд: гекси, лава, спис/щит, вороги-демони, вівтарі"}
  - {kind: official, url: "https://www.magmafortress.com/p/hoplite.html", note: "сторінка автора, історія з 7DRL 2013, рецензії"}
  - {kind: official, url: "https://www.magmafortress.com/2013/11/hoplite-beta-summary.html", note: "журнал змін бети 2.0: вівтарі, ціни молитов, Fleece-бонус"}
  - {kind: play, url: "https://itunes.apple.com/au/app/hoplite/id782438457?mt=8&uo=4", note: "App Store"}
  - {kind: play, url: "https://play.google.com/store/apps/details?id=com.magmafortress.hoplite", note: "Google Play"}
  - {kind: other, url: "http://www.pockettactics.com/reviews/review-hoplite/", note: "рецензія Pocket Tactics (з офіційної сторінки; 403 при fetch)"}
stage: v1
coverage: 65
mechanics: [move-by-input, cell-click, push-object, piece-capture, melee-vs-ranged, projectile-shot, blast-wave, environment-death, hp-damage, reach-exit, dungeon-generation, sequential-levels, shop-between-levels, in-round-upgrades, event-points, time-bonus, daily-puzzle, save-autosave, game-screen, +move-attack, +threat-preview, +cooldown-ability, +energy-resource, +sacrifice-max-hp, +spear-retrieve]
proposes: ["+trigger:move_from_to", "+effect:stun", "+cond:cooldown", "+role:projectile", "+ui:attack-tiles-on-tap", "+window:altar-choice", "+feature:mode-challenge", "+card:move-attack"]
author: opus
date: 2026-11-02
---

# Hoplite — гоплит на гексах: атака лише рухом, кожен демон бʼє за видимим правилом

## Суть
Гоплит спускається в Аїд по рівнях-аренах з гексів, оточених лавою, і має дійти до сходів униз. Звичайної атаки «вдар сусіда» немає: вбиваєш **рухом** — обійти ворога впритул (stab) чи кинутись на нього з відстані два (lunge); є ще кидок списа, удар щитом-відштовхування і стрибок. Кожен тип ворога атакує за простою геометричною формулою, яку можна підсвітити, тож кожен хід — маленька шахова задача з повною інформацією. Перемога — дійти до Золотого руна на глибині 16 і вибратись.

## Поле і час
- Рівень — невелика гекс-арена фіксованого розміру (?), клітини: камінь, лава, сходи вниз, інколи вівтар; край мапи — межа.
- Покроково: гравець робить одну дію → усі демони діють (рухаються або атакують, якщо гравець у їхній зоні).
- Повна інформація: тап по демону показує клітини, які він атакує; при прицілюванні ходу клітини, де спрацює stab/lunge, підсвічені червоним, а кінцева позиція — синім.
- Генерація: рівні процедурні, з гарантією хоча б одного безпечного першого ходу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гоплит | player | HP 3 (+Fortitude), енергія для стрибка | рухається на сусідній гекс; атакує рухом, кидком, щитом, стрибком |
| Спис | projectile | кидається на відстань (≈3?) | вбиває ціль; лежить на клітині, доки гоплит не підбере; без списа нема lunge |
| Щит | — | cooldown | Bash: відштовхнути сусіднього демона на 1, оглушити |
| Footman / swordsman (мечник) | enemy | 1 удар (?) | ближній бій: атакує, якщо гоплит у сусідній клітині на його хід |
| Archer (лучник) | enemy | дальність лінія ≥2 (?) | стріляє по прямій гекс-лінії, коли гоплит не впритул; тримає дистанцію |
| Wizard (маг) | enemy | перезарядка | промінь по прямій лінії; після пострілу хід перезаряджається |
| Demolitionist (підривник) | enemy | перезарядка | кидає бомбу на клітину біля гоплита; вибух наступного ходу по сусідніх гексах |
| Бомба | hazard | таймер 1 хід | вибухає по сусідах; можна відштовхнути щитом на демонів (кіл зараховується) |
| Лава | hazard | — | гоплит або демон на лаві — смерть |
| Сходи вниз | static | — | перехід на наступну глибину |
| Вівтар | static | бог (Athena, Hephaestus, Apollo, Ares…) | молитва: вибір одного дару; часто за жертву max HP |
| Золоте руно | pickup | глибина 16 | взяти й вибратись = перемога; бонус за швидкість |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, hex)` → ЯКЩО `free(hex)` і сусідній → ТО `move(hoplite, hex)`; лава — `lose`.
- **Stab**: КОЛИ `custom: «рух з клітини, сусідньої з демоном D, у клітину, теж сусідню з D»` → ТО `damage(D)` (демон гине).
- **Lunge**: КОЛИ `move(hoplite, dir)` → ЯКЩО `has(hoplite, spear)` і демон D стоїть за 2 клітини в напрямку руху (тепер стане сусідом) → ТО `damage(D)`.
- **Throw**: КОЛИ `input(throw, D)` → ЯКЩО `has(spear)` і `in_range(D, n)` → ТО `damage(D)`, спис лягає на клітину; КОЛИ `contact(hoplite, spear)` → ТО `pickup`.
- **Bash**: КОЛИ `input(bash, dir)` → ЯКЩО `cond:cooldown(bash, ==, 0)` → ТО `push(neighbor, dir)`, `stun(neighbor, 1)`, `custom: «cooldown кілька ходів»`; у лаву — `disappear_b`; у край/вівтар — `stun` (з деякими дарами — смерть) (?).
- **Leap**: КОЛИ `input(leap, hex)` → ЯКЩО `counter(energy, ≥, cost)` і `in_range(hex, 2)` → ТО `teleport(hoplite, hex)` над будь-чим; `counter(energy, -cost)`.
- КОЛИ `enter(hoplite, hex)` → ЯКЩО `adjacent_count(hex, demon, ≥, 1)` → ТО `counter(energy, +10)`.
- Footman: КОЛИ `turn_start(demons)` → ЯКЩО `adjacent(footman, hoplite)` → ТО `damage(1)`; інакше `chase-greedy`.
- Archer: ЯКЩО `line_of_sight(archer, hoplite)` і `not adjacent` і `in_range(≤ n)` → ТО `damage(1)`; інакше крок, щоб стати на лінію / відійти.
- Wizard: ЯКЩО `line_of_sight` по прямій → ТО промінь `damage(1)`, далі `set_state(wizard, recharge, 1)`.
- Demolitionist: ЯКЩО `in_range(hoplite, n)` → ТО `spawn_at(bomb, near_hoplite)`; КОЛИ `timer(1)` → ТО `damage(1)` усім сусідам бомби (і демонам).
- КОЛИ `enter(hoplite, stairs)` → ТО `next_level` (глибина +1).
- КОЛИ `input(pray, altar)` → ТО `choose(prayers)`; ЯКЩО ціна > 0 → `custom: «−max HP і −HP на ціну»`; вибір не скасовується.
- КОЛИ `hp_zero(hoplite)` → ТО `lose` (permadeath, новий забіг).
- КОЛИ `contact(hoplite, fleece)` → ТО `pickup`; вихід з руном → `win`, бонус `×(1 + 10/√turns)`.
- Перемога: руно на глибині 16 і вихід (Premium — можна спускатись далі) · Поразка: HP = 0 · Рахунок: кілли, глибина, бонус за швидкість з руном.

## Керування і ввід
- Тач: тап по сусідньому гексу — рух (із превʼю stab/lunge: утримання показує червоні клітини атаки і синю кінцеву); тап по демону — показати його зону атаки.
- Окремі кнопки дій: Throw (потім тап по цілі), Bash (потім напрям), Leap (потім клітина) (?); Bash може замінити «чекати».
- На вівтарі — тап по вівтарю → вибір молитви.

## Вікна, меню, HUD
- `main-menu`: Play · Challenge Mode (Premium) · Daily · Achievements · Settings (?).
- `game-screen`: гекс-поле; `hp-bar` (серця), `energy-bar`, `ability-buttons` (throw/bash/leap з cooldown), `level-number` (глибина), `threat-range` по тапу, підсвітка stab/lunge.
- `custom-window` «Altar» — 2–3 молитви бога з ціною в серцях (жертва) і описом.
- `achievements-window` — досягнення, що відкривають нові молитви.
- `end-screen` — смерть / перемога з рахунком і бонусом руна.
- Переходи: main-menu → game-screen → сходи → game-screen (глибина +1) → … → end-screen.

## Фічі поза полем
- `achievements` → `unlockables`: досягнення (Flawless, Pacifist, Hoplite Master…) відкривають нові молитви для майбутніх забігів (`meta-progression`).
- Premium: глибина понад 16, більшість нових молитов, Challenge Mode — короткі підземелля на 3 рівні з випадковими стартовими дарами; `mode-daily` — щоденний виклик.
- `autosave` посеред забігу (продовжити після закриття), `mode-hardcore` за замовчуванням (permadeath).
- Молитви (дари вівтарів, частина): Fortitude (+max HP), Restoration (лікування, раз за глибину), Surge/Regeneration/Agility (за кілли кілька ходів поспіль), Bloodlust (енергія за кілли), Energy (більший запас), Winged Sandals (стрибок +1), Leap Strike (стрибок на демона вбиває), Swift Leap (вільна дія після стрибка), Plant Spear (кидок у землю оглушує сусідів), Wizard Beam (кидок → промінь), Recall/Follow (спис повертається), Slashing/Sword Lunge, Sweeping/Spinning/Mighty/Shielding Bash, Patience.

## Варіації й родичі
- 7DRL-версія 2013 → мобільна 2.0 з вівтарями й глибиною > 16.
- Родичі: Into the Breach (видимі наміри + штовхання), Pawnbarian/Shogun Showdown (фігура з патерном), Desktop Dungeons (пазл-роглайк), Hexcells (гекс), Tactical Breach Wizards.
- **Осі варіацій**: атака — bump / рухом (stab, lunge) / снарядом / штовханням у середовище · ворог — бʼє, коли ти в зоні (Hoplite) / оголошує заздалегідь (ITB) · зброя — завжди при собі / кинута й треба підібрати.

## Цікавинки для курсу
- Атака рухом: stab (обхід сусіда) і lunge (рух на ворога з відстані 2) на гекс-сітці — 🥉 (геометрія гекс-сусідства до і після ходу).
- Кожен ворог = функція «які клітини я атакую» + підсвітка по тапу — 🥉 за 4 типи, 🥈 якщо гравець бачить сумарну небезпечну зону.
- Бомба з таймером, яку можна відштовхнути щитом у ворогів — 📎.
- Кидок зброї з обовʼязковим поверненням (втрачаєш lunge, доки не підбереш) — 📎.
- Вівтар-вибір дару за жертву max HP — 📎 (`choose` + ціна у ресурсі життя).
- Генерація гекс-арени з гарантією безпечного першого ходу — 🥇.

## Мапа на каталог
- Є: `move-by-input` (гекс) · `cell-click` · `push-object` (bash) · `piece-capture` (вбивство однією дією) · `melee-vs-ranged` (мечник / лучник, маг) · `projectile-shot` (спис, стріла, промінь) · `blast-wave` (бомба радіус 1) · `environment-death` (лава) · `hp-damage` · `reach-exit` (сходи) · `dungeon-generation` · `sequential-levels` (глибини) · `shop-between-levels` (вівтар як «магазин» за HP) · `in-round-upgrades` · `event-points` + `time-bonus` (бонус руна) · `daily-puzzle` · `save-autosave` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+move-attack` «Атака рухом (обхід/випад)» · entities/combat · 🥉 · слот {kind: stab|lunge}.
  - `+threat-preview` «Зона атаки ворога на запит» · interface/hud · 📎 — сестра `telegraphed-intents`, але без часу наперед.
  - `+cooldown-ability` «Здібність з перезарядкою» · entities/state · 📎 · слот {cooldown}.
  - `+energy-resource` «Енергія за позицію (поряд з ворогом)» · entities/state · 📎.
  - `+sacrifice-max-hp` «Апгрейд за жертву max HP» · game-logic/economy · 📎.
  - `+spear-retrieve` «Кинута зброя, яку треба підібрати» · entities/combat · 📎.

## Пропозиції до словників
- `+trigger:move_from_to` — хід гравця з умовою на стартову й кінцеву клітину (stab: обидві сусідні з ворогом).
- `+effect:stun` уже ⏳ у словнику — тут вживано; `+cond:cooldown` — здібність готова (лічильник ходів).
- `+role:projectile` — спис як предмет-снаряд, що лишається на полі.
- `+ui:attack-tiles-on-tap` — тап по ворогу підсвічує його зону атаки.
- `+window:altar-choice` — вибір одного з дарів з ціною (близько до ⏳ `upgrade-window`).
- `+feature:mode-challenge` — короткі підземелля з випадковими стартовими дарами.
- `+card:move-attack` — див. «Мапа на каталог».

## Джерела
- ⭐ [Відео з офіційної сторінки](https://www.youtube.com/watch?v=-ABUS0t0Qaw) — геймплей (з magmafortress.com).
- [Wikipedia](https://en.wikipedia.org/wiki/Hoplite_(video_game)) — огляд механік, вороги, вівтарі, Premium/Challenge Mode.
- [Magma Fortress: Hoplite](https://www.magmafortress.com/p/hoplite.html) — історія з 7DRL, рецензії, посилання на стори.
- [Hoplite Beta Recap](https://www.magmafortress.com/2013/11/hoplite-beta-summary.html) — молитви, ціни, правила bash/leap, бонус руна.
- [Pocket Tactics review](http://www.pockettactics.com/reviews/review-hoplite/) — рецензія (не відкрилась, 403).

## Непевне
- (?) Точні дальності: кидок списа, лучник, маг, кидок бомби; лучник/маг не стріляють упритул — з памʼяті.
- (?) Стартове HP 3 і чи всі демони гинуть від одного удару — з памʼяті.
- (?) Що буває при bash у край мапи/вівтар без дарів (журнал каже «вбиває замість оглушення» — ймовірно, для певної версії/дару).
- (?) Розмір арени і як саме викликається bash/leap/throw в інтерфейсі.
- (?) Ціна стрибка в енергії (повна шкала 100?) — з памʼяті; підтверджено лише +10 енергії за крок поряд із демоном.
- (?) `klass: figure` за призначенням куратора; за суттю Hoplite — один аватар (`avatar`), фігурність — у правилах ворогів.
