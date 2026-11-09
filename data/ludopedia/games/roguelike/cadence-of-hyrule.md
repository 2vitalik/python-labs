---
title: "Cadence of Hyrule: Crypt of the NecroDancer Featuring The Legend of Zelda"
slug: cadence-of-hyrule
aka: [Cadence of Hyrule, CoH]
family: roguelike
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: rhythm
  opponent: ai
  info: hidden
  random: setup
  goal: state
year: 2019
platforms: [Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Cadence_of_Hyrule", best: true, note: "ритм лише коли на екрані вороги, fixed-beat, світ із готових регіонів у випадковому порядку, смерть = втрата рупій, діаманти, камені Шейка, кооп, DLC"}
  - {kind: official, url: "https://braceyourselfgames.com/cadence-of-hyrule/", note: "Brace Yourself Games: 25 реміксів Zelda, Link/Zelda, предмети Zelda + закляття NecroDancer, DLC"}
  - {kind: other, url: "https://www.nintendo.com/us/store/products/cadence-of-hyrule-crypt-of-the-necrodancer-featuring-the-legend-of-zelda-switch/", note: "eShop: випадкові світ і підземелля, патерни ворогів, боси, 1–2 гравці на одній консолі"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=cadence+of+hyrule+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, hp-damage, pattern-automaton, chase-greedy, speed-per-type, combo-multiplier, round-currency, shop-catalog, inventory-items, item-pickup, dungeon-generation, world-map, teleport, respawn, checkpoint, dig-terrain, player-death, permadeath, background-music, player-camera, +beat-tick, +rhythm-only-in-combat, +fixed-beat-mode, +world-from-prefab-regions, +rule-twist-character]
proposes: ["+cond:enemies_on_screen", "+feature:fixed-beat-mode", "+effect:fast_travel(to)"]
author: opus
date: 2026-11-09
---

# Cadence of Hyrule — ритм-хід NecroDancer у відкритому світі Zelda: такт обовʼязковий лише там, де є вороги

## Суть
Спільна гра Brace Yourself Games і Nintendo (2019, Switch). Ядро бою — з [Crypt of the NecroDancer](crypt-of-the-necrodancer.md): крок і удар на біт (25 реміксів мелодій Zelda), вороги з патернами, множник за влучання. Тут — **лише відмінності**: замість спуску поверхами — **відкритий світ Хайрула** з екранів-регіонів, ритм потрібен **тільки коли на екрані є вороги**, є **fixed-beat** режим без ритму, смерть не кінець гри (повернення до каменя Шейка з утратою рупій).

## Поле і час
- Квадратна сітка екранів-регіонів, як у класичній Zelda; регіони (Hyrule Castle, Death Mountain…) — готові, а їхнє **взаємне розміщення генерується на кожне нове збереження** і далі фіксоване.
- Підземелля-храми **перегенеровуються при кожному вході**.
- Тік: біт пісні, як у NecroDancer, **але лише за присутності ворогів у зоні**; на чистому екрані рух вільний.
- Fixed-beat: перемикач, що прибирає вимогу ритму — гра стає покроковою.

## Сутності
Спільні з NecroDancer (слизи, скелети, кажани, двері, стіни під лопату, крамарі) — див. [crypt-of-the-necrodancer.md](crypt-of-the-necrodancer.md). Відмінні:

| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Link / Zelda | player | серця, стамина (?), унікальні здібності | основні герої; кожен зі своїми вміннями |
| Cadence | player | — | відкривається сюжетом/квестами |
| DLC-герої (Octavo, Impa, Shadow Link, Shadow Zelda, Aria, Frederick, Skull Kid) | player | спецприйоми | інші правила (Aria — як у NecroDancer (?)) |
| Вороги Zelda (Bokoblin, Lizalfos, Lynel, Hyrule Soldier…) | enemy | HP, патерн | рухаються на біт за своїм патерном |
| Боси (перетворені магією Octavo) | boss | фази | сильніші форми класичних босів Zelda |
| Камінь Шейка | static / switch | активований? | швидке переміщення між активованими; точка відродження |
| Рупії | pickup | купка | валюта; губляться при смерті |
| Діамант | resource | — | лишається після смерті; з підземель або за зачистку всіх ворогів зони |
| Лопата | pickup | сила | копати (як у NecroDancer) |
| Смолоскип | pickup | — | показує вміст скринь |
| Лук, бомби, гак-кішка, бумеранг (?) | pickup | заряди | класичні предмети Zelda для бою й проходу |
| Тимчасові предмети | pickup | — | губляться при смерті |

## Правила (КОЛИ → ЯКЩО → ТО)
Відмінності від [crypt-of-the-necrodancer.md](crypt-of-the-necrodancer.md):
- КОЛИ `input(dir)` → ЯКЩО `custom: «на екрані нема ворогів»` → ТО `move(player, dir)` без перевірки біта.
- КОЛИ `input(dir)` → ЯКЩО `custom: «на екрані є вороги»` and `custom: «ввід у вікні біта»` → ТО дія як у NecroDancer + `combo(+1)` / `multiplier`.
- КОЛИ `input(dir)` → ЯКЩО `mode(fixed_beat)` → ТО `custom: «світ робить крок лише після ходу гравця»` (?).
- КОЛИ `custom: «зачищено всіх ворогів зони»` → ТО `spawn(diamond)`.
- КОЛИ `contact(player, sheikah_stone)` → ТО `set_state(stone, active)`; КОЛИ `input(travel, stone)` → ЯКЩО `state(stone, active)` → ТО `teleport`.
- КОЛИ `hp_zero(player)` → ТО `custom: «втрата рупій і тимчасових предметів»`, `respawn(player, active_stone)`; діаманти лишаються.
- КОЛИ `hp_zero(player)` → ЯКЩО `mode(permadeath)` → ТО `lose`.
- КОЛИ `enter(player, temple)` → ТО `custom: «храм генерується заново»`.
- КОЛИ `input(use, torch)` → ТО `reveal(chests)` — видно вміст скринь.
- КОЛИ `died(boss)` → ТО `custom: «інструмент Octavo знешкоджено»` (?); фінальний бос → `win`.
- Перемога: сюжет (перемогти Octavo / Ganon (?)). Поразка: лише в режимі permadeath. Рахунок: явного нема.

## Керування і ввід
- Хрестовина/стік — 4 напрямки на біт (як у NecroDancer); кнопки — предмети й спецприйоми героя (?).
- Кооп: другий гравець на тій самій Switch, кожен з одним Joy-Con.

## Вікна, меню, HUD
- `game-screen`: поле-екран, смуга бітів (`beat-bar` з NecroDancer), серця, рупії, діаманти, слоти предметів.
- `map-window` — карта Хайрула з активованими каменями Шейка (точки переміщення).
- `shop-window` — крамарі за рупії / діаманти (?).
- `save-slots` — кожне збереження = своє розміщення регіонів.
- `settings-window` — fixed-beat перемикач (?), калібрування.
- `character-select` — DLC-герої, режим Dungeons.

## Фічі поза полем
- `fixed-beat-mode` (без ритму), `mode-hardcore` (permadeath-кампанія), режим Dungeons (безкоштовне DLC), `mode-coop` (локальний), 25+ реміксів, музичний DLC, сюжетне DLC Symphony of the Mask.

## Варіації й родичі
- [Crypt of the NecroDancer](crypt-of-the-necrodancer.md) — оригінал; [Theseus and the Minotaur](theseus-and-the-minotaur.md) — «хід-у-відповідь» без музики.
- Осі (нові відносно NecroDancer): **коли діє ритм** (завжди / лише з ворогами на екрані / вимкнено fixed-beat); **світ** (поверхи униз / відкритий світ з готових регіонів, перемішаних на сейв); **смерть** (кінець забігу / відкат до чекпоінта з утратою валюти / permadeath-опція).

## Цікавинки для курсу
- Ритм вмикається лише при ворогах на екрані — 🌱 (умова переходу між real-time і rhythm-тіком).
- Світ із готових регіонів, перемішаних сідом збереження, — 📎 (граф сусідства регіонів + сід).
- Камені Шейка: активація = чекпоінт + точка телепорту — 🌱.
- Смерть з утратою «мʼякої» валюти і збереженням «твердої» (рупії vs діаманти) — 🌱.

## Мапа на каталог
- Є (нові відносно NecroDancer): `world-map` · `teleport` (камені Шейка) · `respawn` · `checkpoint` · `dig-terrain` · `permadeath` · `player-camera`; решта — як у crypt-of-the-necrodancer.md.
- **Нема** → пропозиції карток:
  - `+rhythm-only-in-combat` «Ритм-тік лише за присутності ворогів» · core/loop · 🌱 (дитина `+beat-tick`).
  - `+fixed-beat-mode` «Ритм-гра як покрокова» · game-logic/difficulty · 🌱.
  - `+world-from-prefab-regions` «Світ із готових регіонів у випадковому порядку на сейв» · levels/generation · 📎.

## Пропозиції до словників
- `+cond:enemies_on_screen` — у видимій зоні є вороги (перемикає режим часу).
- `+feature:fixed-beat-mode` — вимкнути вимогу ритму.
- `+effect:fast_travel(to)` — переміщення між відкритими точками мапи (вужче за `teleport`).

## Джерела
- ⭐ [Wikipedia: Cadence of Hyrule](https://en.wikipedia.org/wiki/Cadence_of_Hyrule) — ритм лише з ворогами, fixed-beat, регіони, храми, смерть, діаманти, камені Шейка, кооп, DLC.
- [Brace Yourself Games](https://braceyourselfgames.com/cadence-of-hyrule/) — 25 реміксів, Link/Zelda, предмети й закляття, DLC.
- [Nintendo eShop](https://www.nintendo.com/us/store/products/cadence-of-hyrule-crypt-of-the-necrodancer-featuring-the-legend-of-zelda-switch/) — випадковий світ, патерни ворогів, боси, 1–2 гравці.
- YouTube: [пошук «cadence of hyrule gameplay»](https://www.youtube.com/results?search_query=cadence+of+hyrule+gameplay).

## Непевне
- (?) Теза черги «вороги стоять поза біт-логікою» не підтверджена: джерела кажуть лише, що ритм обовʼязковий, коли на екрані вороги; чи стоять вороги, коли гравець не ходить, і що саме робить fixed-beat (крок світу після ходу гравця) — з памʼяті. Фан-вікі (zeldawiki 403, fandom 402) і WebSearch (бюджет вичерпано) недоступні.
- (?) Стамина, спецприйоми Link/Zelda, бумеранг, магазин за діаманти, фінальний бос — з памʼяті.
- (?) `random: setup` — випадковість генерації світу/храмів; бойова випадковість (лут) імовірна, але не підтверджена.
