---
title: Gyromancer
slug: gyromancer
aka: []
family: falling-match
also: [connect-rotate]
klass: hybrid
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 2009
platforms: [PC, Xbox 360]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Gyromancer", best: true, note: "обертання блоку з 4 самоцвітів, шкали гравця й ворога, атакувальний камінь, кольори монстрів, черепи з лічильником, необертні камені, 12 етапів-мап, загін із 3 монстрів"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bejeweled_Twist", note: "базова механіка обертання 2×2 за годинниковою, хід без збігу дозволено"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Gyromancer", note: "пошук"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Gyromancer+gameplay", note: "пошук; геймплей (відео не відкривав)"}
stage: v1
coverage: 55
mechanics: [line-match-clear, gravity-fall, chain-reaction, spawn-random-cell, hp-damage, unit-xp-skills, character-select, world-map, map-window, inventory-items, time-out, level-unlock, game-screen, end-screen, +rotate-2x2, +cascade-refill, +countdown-tile, +attack-gauge, +enemy-gauge-per-move, +color-affinity, +unrotatable-tile, +recruit-defeated, +party-of-three]
proposes: ["+effect:fill_gauge", "+trigger:gauge_full", "+ui:countdown-on-tile", "+card:attack-gauge", "+card:enemy-gauge-per-move", "+card:color-affinity", "+card:recruit-defeated"]
author: opus
date: 2026-11-09
---

# Gyromancer — Bejeweled Twist як бій: обертаєш блоки 2×2, щоб наповнити шкалу атаки раніше, ніж ворог наповнить свою

## Суть
Спільний проєкт PopCap і Square Enix, натхненний Puzzle Quest. Бій іде на полі самоцвітів, як у [bejeweled](bejeweled.md) Twist: гравець вибирає блок із 4 каменів і обертає його за годинниковою; лінії 3+ однакових зникають, згори падають нові. Збіги наповнюють шкалу гравця, повна шкала кладе на поле **атакувальний камінь** — шкода ворогу лише тоді, коли гравець складе з ним лінію. Ворог не ходить по полю: його шкала росте від **кожного повороту** гравця, тож кожен хід — витрата часу. Клас `hybrid`: `cursor` на дошці + рух між точками мапи етапу.

## Поле і час
- Бій: квадратна сітка самоцвітів кількох кольорів (розмір і число кольорів — «Непевне»).
- Хід = один поворот блоку 2×2; каскади після нього — частина того ж ходу.
- Над полем — дві шкали (гравця і ворога) та HP обох монстрів.
- Поза боєм — мапа етапу: граф точок-зірок, рух між сусідніми точками; 12 етапів у лісі Aldemona.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Самоцвіт | tile | колір | обертається в блоці 2×2; лінія 3+ зникає; падає вниз |
| Атакувальний камінь | tile | — | зʼявляється, коли шкала гравця повна; лінія з ним = шкода ворогу |
| Череп | hazard | лічильник ходів | ворог перетворює камінь на череп; не прибраний вчасно — шкода гравцю |
| Необертний камінь | gate | — | (пізні етапи) блок із ним не обертається (?) |
| Монстр гравця | player | колір, HP, сила атаки/захисту, досвід | бʼється; колір прискорює власну шкалу |
| Ворожий монстр | enemy | колір, HP, шкала | атакує, коли шкала повна; ставить черепи |
| Загін | zone | 3 монстри з колекції | обирається перед етапом; перед боєм — один боєць |
| Точка мапи | terrain | бій / пазл на час / прихований монстр / предмет | рух лише до сусідньої точки |
| Бойовий предмет | pickup | — | знайдений на мапі; застосування в бою (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(rotate block 2×2)` → ЯКЩО `not occupied(block, unrotatable)` → ТО `rotate(block, +90)`, `counter(enemy_gauge, +n)`; хід зараховано і без збігу.
- КОЛИ `pattern(line(3+))` → ТО `clear(line)`, `counter(player_gauge, +n)`.
- КОЛИ `pattern(match(player_monster.color, 3+))` → ТО `counter(player_gauge, +більше)` — колір свого монстра прискорює шкалу.
- КОЛИ `pattern(match(enemy_monster.color, 3+))` → ТО `custom: «шкала ворога росте повільніше»`.
- КОЛИ `custom: «поворот без збігу»` (пізні етапи) → ТО `custom: «шкала ворога росте швидше»`.
- КОЛИ `after(clear)` → ТО `fall(gems_above)`, `spawn_at(random_gem, top)`; КОЛИ `settled` → ЯКЩО `pattern(line(3+))` → ТО `clear`, повтор (каскад).
- КОЛИ `counter(player_gauge, ==, full)` → ТО `spawn_at(attack_gem, board)`, `counter(player_gauge, =0)` (?).
- КОЛИ `custom: «лінія містить атакувальний камінь»` → ТО `damage(enemy, attack)` — розмір шкоди залежить від монстрів.
- КОЛИ `counter(enemy_gauge, ==, full)` → ТО `damage(player_monster, enemy_attack)`, `counter(enemy_gauge, =0)` (?).
- КОЛИ `custom: «атака ворога-закляття»` → ТО `transform(gem, skull)` з лічильником ходів.
- КОЛИ `turn_end` → ТО `counter(skull, −1)`; КОЛИ `counter(skull, ==, 0)` → ТО `damage(player_monster, n)`; `clear(skull)` у лінії знешкоджує його.
- КОЛИ `hp_zero(enemy)` → ТО `win`, `counter(xp, +n)`, `give(roster, enemy_monster)` — переможений приєднується до колекції.
- КОЛИ `hp_zero(player_monster)` → ТО `lose` (бій можна переграти (?)).
- КОЛИ `custom: «точка — пазл на час»` → ЯКЩО `timer(==, 0)` → ТО `lose`.
- КОЛИ `counter(xp, >=, threshold)` → ТО `custom: «монстр сильнішає»`.
- КОЛИ `custom: «головну ціль етапу виконано»` → ТО `next_level`; замкнені ділянки мапи відкриваються при повторі етапу пізніше.

## Керування і ввід
- Курсор на перетині чотирьох каменів, кнопка — поворот блоку за годинниковою (Twist-ввід).
- На мапі — вибір сусідньої точки; перед етапом — вибір трьох монстрів, перед боєм — одного.

## Вікна, меню, HUD
- `game-screen` (бій): поле, HP і портрети обох монстрів, шкала гравця, шкала ворога, лічильники на черепах (`countdown-on-tile`).
- `map-window`: мапа етапу з точками-зірками, головна й додаткові цілі (`objective-text`).
- `character-select`: загін із 3 монстрів перед етапом; вибір бійця перед боєм.
- `dialogue-window`: катсцени між боями.
- `end-screen`: перемога/поразка бою, досвід, новий монстр.
- `main-menu`, `settings-window`, `tutorial-window` (критики його лаяли) — деталі не звірено (?).

## Фічі поза полем
- `levels-sequential`: 12 етапів; `level-unlock` — частина ділянок доступна лише при повторному проходженні.
- `meta-progression`: колекція монстрів з досвідом, поповнюється переможеними; приховані монстри й предмети на мапах (`collectibles`).
- Додаткові етапи — DLC.

## Варіації й родичі
- Двигун — [bejeweled](bejeweled.md) Twist (обертання 2×2, хід без збігу); бойова обгортка — від [puzzle-quest](puzzle-quest.md), але без спільної дошки: ворог не ходить, а «тікає» за кожен поворот гравця.
- Відмінності від Twist: нема бомб/вугілля/Doom; замість них черепи від ворога і атакувальний камінь, який ще треба вбудувати в лінію.
- У сімʼї connect-rotate обертання — для зʼєднань ([infinity-loop](../connect-rotate/infinity-loop.md)); тут — лише як ввід match-3.
- **Осі варіацій**: шкода (прямо від збігу — PQ / через спецкамінь — Gyromancer) · темп ворога (по черзі ходить сам / шкала за ходи гравця / real-time) · колір (нейтральний / спорідненість із монстром).

## Цікавинки для курсу
- Обертання блоку 2×2 і перевірка ліній після нього — 🌱.
- Дві шкали: гравця за збіги, ворога за кожен хід — простий «бій без AI» — 📎.
- Атакувальний камінь, що спавниться і має увійти в лінію — 📎.
- Черепи з лічильником ходів, які ставить ворог — 📎.
- Колекція монстрів: перемога додає ворога в загін, досвід посилює — 🥉.
- Мапа-граф етапу з точками-подіями й замкненими ділянками — 🥉.

## Мапа на каталог
- Є: `line-match-clear` · `gravity-fall` · `chain-reaction` · `spawn-random-cell` · `hp-damage` · `unit-xp-skills` · `character-select` · `world-map` · `map-window` · `inventory-items` (бойові предмети) · `time-out` (пазли на час) · `level-unlock` · `game-screen` · `end-screen`.
- Повтор чужих: `+rotate-2x2`, `+cascade-refill`, `+countdown-tile` (Bejeweled).
- **Нема** → пропозиції карток:
  - `+attack-gauge` «Шкала за збіги → спецкамінь атаки» · game-logic/score · 📎.
  - `+enemy-gauge-per-move` «Ворог атакує, коли його шкала від ходів гравця повна» · game-logic/opponent · 📎.
  - `+color-affinity` «Колір бійця прискорює/сповільнює шкали» · entities/state · 🌱.
  - `+unrotatable-tile` «Плитка, що блокує поворот блоку» · entities/legality · 🌱.
  - `+recruit-defeated` «Переможений ворог поповнює колекцію» · entities/state · 📎.
  - `+party-of-three` «Загін із N з колекції перед етапом» · interface/menus · 🌱.

## Пропозиції до словників
- `+trigger:gauge_full(a)` — шкала сутності заповнена (атака, спецкамінь).
- `+effect:fill_gauge(a, n)` — додати до шкали; відрізняти від загального `counter`, бо шкала має поріг і скидання.

## Джерела
- ⭐ [Wikipedia: Gyromancer](https://en.wikipedia.org/wiki/Gyromancer) — обертання 4 каменів, лінії 3+, шкали, атакувальний камінь, кольори монстрів, черепи, необертні камені, загін, 12 етапів, DLC, автори.
- [Wikipedia: Bejeweled Twist](https://en.wikipedia.org/wiki/Bejeweled_Twist) — обертання 2×2 за годинниковою, хід без збігу, спецкамені Twist.

## Непевне
- (?) Розмір поля і кількість кольорів — не названо.
- (?) Чи скидаються шкали після атаки і чи є в монстрів окремі навички (skills) — стаття не описує; StrategyWiki 403, японської статті нема.
- (?) Чи переповнення шкали гравця кладе один атакувальний камінь, чи кілька; де він зʼявляється.
- (?) Бойові предмети: як застосовуються.
- (?) Поразка в бою: чи можна змінити монстра з загону, чи бій переграється.
- (?) Лічильник черепа і шкода від нього — числа не названо.
