---
title: "X-Morph: Defense"
slug: x-morph-defense
aka: [X-Morph, XMorph Defense]
family: tower-lanes
also: []
klass: hybrid
axes:
  field: free
  time: realtime
  opponent: none
  info: full
  random: none
  goal: survive
year: 2017
platforms: [PC, PS4, Xbox One, Switch]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/408410/XMorph_Defense/", best: true, note: "суть: шутер + TD, лазерні паркани між вежами, фаза підготовки без таймера, 4 форми корабля, руйнування мостів і будівель, боси-мехи, split-screen co-op, DLC"}
  - {kind: official, url: "https://www.xmorphdefense.com/", note: "ядра-харвестери, вежі «майже будь-де», апгрейди після кожного ядра, платформи, co-op не на Switch, безкоштовний Survival"}
  - {kind: other, url: "https://www.mygamer.com/x-morph-defense-switch-review/", note: "рецензія: тінь корабля як курсор будівництва, продаж/перенесення веж без штрафу, невидимість, ~дюжина етапів"}
  - {kind: other, url: "https://gameluster.com/?p=31764", note: "рецензія: обмежені ресурси, повернення за знищену вежу, 5 хвиль на місію, мех-бос наприкінці, новий корабель з бази"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=X-Morph+Defense+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [tower-placement, enemy-waves, enemy-reached-base, chase-bfs, destructible-blocks, shop-buyback, explode-area, temporary-modes, respawn, game-screen, +maze-by-towers, +laser-fence, +twin-stick-shooter, +build-phase-untimed, +collapse-to-reroute, +avatar-forms, +charged-special, +free-tower-relocate, +tech-unlock-per-mission, +boss-mech, +local-coop]
proposes: ["+effect:link_fence", "+trigger:collapsed", "+effect:recompute_path", "+ui:ship-shadow-cursor"]
author: opus
date: 2026-11-09
---

# X-Morph: Defense — межа сімʼї: вільний TD, де лабіринт будують лазерні паркани між вежами й обвалені мости, а гравець ще й літає кораблем-шутером

## Суть
Гравець — інопланетний загарбник: між хвилями ставить вежі «майже будь-де» на мапі міста, зʼєднує сусідні вежі лазерними парканами й так перекриває вулиці, а під час хвилі сам літає кораблем (twin-stick shooter) і добиває людські танки, авіацію й мехи, що йдуть до ядра-харвестера. Друга сила лабіринту — руйнування: обвалені будівлі й знесені мости змінюють доступні шляхи. Клас `hybrid`: `cursor` (будівництво веж) + `avatar` (корабель). Сітки клітин у джерелах нема — тому файл короткий, як межа поруч із [fieldrunners](fieldrunners.md) і [defense-grid](defense-grid.md).

## Поле і час
- 3D-мапи реальних міст і промзон, вид згори; розміщення веж вільне — клітинну сітку джерела не згадують (?).
- Мапа змінюється під час гри: фізика руйнування валить будівлі, паркани й мости — це перебудовує шляхи, а не лише картинку.
- Час: фаза підготовки перед кожною хвилею **без ліміту часу** (видно типи ворогів і їхні шляхи) → хвиля в real-time; вежі можна ставити й посеред бою.
- Місія — кілька хвиль (рецензія: 5) і бос-мех наприкінці (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Корабель X-Morph | player | форма (4), базова атака + заряджена | літає над мапою, стріляє twin-stick; знищений — новий вилітає з бази |
| Ядро-харвестер | static | — | ціль ворогів; захистити будь-що |
| Вежа (базова) | tower | ціна | ставиться вільно; зʼєднується парканом із сусідньою |
| Вогнемет | tower | — | проти швидких наземних |
| Артилерія / бомбомет | tower | далекобійна | проти великих повільних груп |
| Протиповітряний лазер | tower | — | проти важких бомбардувальників |
| Гармата | tower | — | базова наземна |
| Лазерний паркан | gate | між двома близькими вежами | перекриває прохід; ворог шукає інший шлях |
| Будівля / міст | static | руйнована | обвал блокує вулицю або шкодить; знесений міст прибирає шлях |
| Наземний ворог (танки тощо) | enemy | HP | іде шляхом до ядра |
| Повітряний ворог | enemy | HP | летить, паркани не зупиняють (?) |
| Мех-бос | boss | розміром з будівлю | руйнує місто, унікальна тактика |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(setup)` → ТО `custom: «показати склад хвилі й шляхи; час не обмежений»`.
- КОЛИ `input(build, tower, where)` → ЯКЩО `custom: «вистачає енергії»` → ТО `place(player, tower)`; інакше `block`.
- КОЛИ `custom: «дві вежі поставлено близько»` → ТО `custom: «effect link_fence: між ними вмикається лазерний паркан»`.
- КОЛИ `custom: «паркан або обвал перекрив вулицю»` → ТО `custom: «effect recompute_path: вороги йдуть довшим шляхом»`.
- КОЛИ `input(sell|move, tower)` → ТО `custom: «вежу продано або перенесено без штрафу»`, `currency(+price)` (?).
- КОЛИ `destroyed(tower)` → ТО `currency(+price)` — енергію повернуто.
- КОЛИ `input(fire)` → ТО `custom: «базова атака форми»`; КОЛИ `input(charged)` → ТО `custom: «заряджена атака форми»`.
- КОЛИ `input(bomber_special)` → ТО `custom: «уповільнення часу»`, `explode(area)` — бомба валить будівлі.
- КОЛИ `input(destroyer_special)` → ТО `custom: «гравітаційна аномалія затягує дрібних ворогів»`.
- КОЛИ `input(stealth)` → ТО `set_state(ship, invisible)` — швидкий рух, ворожий вогонь мимо, атаки вимкнено.
- КОЛИ `custom: «trigger collapsed: будівлю або міст обвалено»` → ТО `custom: «шлях змінюється; уламки шкодять тим, хто під ними»`.
- КОЛИ `hp_zero(ship)` → ТО `respawn(ship, base)`.
- КОЛИ `reach(enemy, core)` → ТО `custom: «шкода ядру»`; КОЛИ `custom: «ядро знищено»` → ТО `lose` (?).
- КОЛИ `wave_cleared` → ТО `custom: «наступна фаза підготовки»`; КОЛИ `destroyed(boss_mech)` → ТО `win` місії, `unlock(upgrades)`.

## Керування і ввід
- Twin-stick: рух корабля + приціл окремо; перемикання 4 форм; базова і заряджена атака.
- Будівництво: тінь корабля на землі — курсор, куди стане вежа; кнопки поставити / продати / перенести.
- Миша й клавіатура з перепризначенням (PC); геймпад; split-screen для двох.

## Вікна, меню, HUD
- `main-menu` → `level-select` / мапа кампанії → `game-screen`: мапа зверху, корабель, вежі й паркани, шляхи ворогів у фазі підготовки, лічильник енергії, `wave-counter`, `next-wave-preview`.
- `upgrade-window` — апгрейди корабля й веж (RPG-елементи) після кожного захопленого ядра; `pause-menu`; `settings-window`; `end-screen` місії.

## Фічі поза полем
- Кампанія з місіями-містами; `mode-coop` split-screen (окремо задумані місії, вороги з нових напрямків; не на Switch).
- DLC: European Assault, Survival of the Fittest, Last Bastion; безкоштовний режим Survival (`mode-endless` (?)).
- `remap-controls`, 21:9, без обмеження FPS (PC).

## Варіації й родичі
- Сітковий родич — [fieldrunners](fieldrunners.md) (лабіринт з веж на клітинах), [defense-grid](defense-grid.md) (лабіринт + повітряні шляхи), [orcs-must-die](orcs-must-die.md) і [anomaly-warzone-earth](anomaly-warzone-earth.md) (герой на полі TD).
- **Осі варіацій**: стіна лабіринту — сама вежа (Fieldrunners) / паркан між вежами (X-Morph) · перебудова шляху — лише гравцем / ще й руйнуванням мапи · участь гравця — курсор / курсор + аватар-шутер.

## Цікавинки для курсу
- Паркан як ребро графа між двома вежами в радіусі зʼєднання: стіна = відрізок, не клітина — 📎 (на сітці — 🌱: заблокувати ребра між клітинами).
- Обвал будівлі / мосту перебудовує граф шляхів посеред хвилі — 🥉 (перерахунок BFS після зміни мапи).
- Фаза підготовки без таймера з показом шляхів ворогів — 🌱.
- Корабель-аватар + вежі в одному real-time циклі — 🥉.
- Продаж і перенесення без штрафу: TD як вільна чернетка між хвилями — 🌱.

## Мапа на каталог
- Є: `tower-placement` ↔ вежі будь-де · `enemy-waves` · `enemy-reached-base` ↔ ядро · `chase-bfs` ↔ перерахунок шляху · `destructible-blocks` ↔ будівлі й мости · `shop-buyback` ↔ продаж веж · `explode-area` ↔ бомба · `temporary-modes` ↔ невидимість, уповільнення · `respawn` ↔ новий корабель · `game-screen`.
- **Нема** → пропозиції карток:
  - `+maze-by-towers` · `+local-coop` — уже пропонувались корпусом; тут: лабіринт парканами, split-screen.
  - `+laser-fence` «Стіна-ребро між двома сусідніми вежами» · entities/combat · 📎 · слот {link_range}.
  - `+twin-stick-shooter` «Рух і приціл двома стіками» · interface/input · 🥉.
  - `+build-phase-untimed` «Підготовка між хвилями без таймера» · game-logic/waves · 🌱.
  - `+collapse-to-reroute` «Руйнування мапи перекриває шлях ворогам» · entities/interact · 🥉.
  - `+avatar-forms` «Перемикання форм аватара з різними атаками» · entities/state · 📎.
  - `+charged-special` «Базова атака + заряджена спецатака» · entities/combat · 🌱.
  - `+free-tower-relocate` «Перенести/продати вежу без втрат» · game-logic/economy · 🌱.
  - `+tech-unlock-per-mission` «Апгрейди відкриваються за пройдену місію» · levels/progression · 🌱.
  - `+boss-mech` «Бос наприкінці місії, що руйнує мапу» · game-logic/waves · 🥉.

## Пропозиції до словників
- `+effect:link_fence` — зʼєднати дві сутності бар'єром-ребром.
- `+trigger:collapsed` — обвал статичної сутності (будівлі, мосту) під дією фізики.
- `+effect:recompute_path` — вороги перераховують шлях (у корпусі вже пропонувалось, Defense Grid).
- `+ui:ship-shadow-cursor` — тінь аватара як курсор будівництва.

## Джерела
- ⭐ [Steam: X-Morph: Defense](https://store.steampowered.com/app/408410/XMorph_Defense/) — шутер + TD, лазерні паркани, підготовка без ліміту, вежі проти типів ворогів, 4 форми з атаками, руйнування мостів і будівель, боси-мехи, split-screen co-op, DLC, дата 30.08.2017.
- [Офіційний сайт](https://www.xmorphdefense.com/) — ядра-харвестери, вежі «майже будь-де», апгрейди після кожного ядра, платформи, co-op не на Switch, безкоштовний Survival.
- [MyGamer: Switch review](https://www.mygamer.com/x-morph-defense-switch-review/) — тінь корабля як курсор, типи веж, паркан між двома вежами, продаж/перенесення без штрафу, невидимість, обвали будівель.
- [GameLuster: review](https://gameluster.com/?p=31764) — обмежені ресурси, повернення енергії за знищену вежу, 5 хвиль на місію, мех наприкінці, новий корабель з бази.
- YouTube: [пошук «X-Morph Defense gameplay»](https://www.youtube.com/results?search_query=X-Morph+Defense+gameplay).

## Непевне
- (?) Чи є під вежами будівельна сітка — джерела кажуть лише «майже будь-де»; тому `field: free`.
- (?) Економіка: «енергія на хвилю, повертається за знищену вежу» (GameLuster, TV Tropes у сніпеті пошуку) проти «уламки ворогів — валюта для апгрейдів» (MyGamer) — можливо, дві різні валюти.
- (?) Чи можна парканами перекрити шлях повністю і що тоді роблять вороги (атакують паркан?); чи зупиняють паркани повітряних.
- (?) Умова поразки (знищення ядра) прямо не названа в жодному відкритому джерелі.
- (?) Кількість етапів («близько дюжини») і «5 хвиль на місію» — з рецензій.
