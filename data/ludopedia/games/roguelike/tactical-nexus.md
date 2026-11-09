---
title: Tactical Nexus
slug: tactical-nexus
aka: []
family: roguelike
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: score
year: 2019
platforms: [PC (Windows)]
links:
  - {kind: other, url: "https://smithgift.substack.com/p/review-tactical-nexus", best: true, note: "детальний огляд: бій, ключі, виходи й рахунок, Nexus-крамниця, медалі, сонячні камені, Pure-забіг"}
  - {kind: steam, url: "https://store.steampowered.com/app/1141290/Tactical_Nexus/", note: "Team-Tactical Nexus, 11.11.2019, free to play; 12 веж, undo/redo, мемо"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tactical+Nexus+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-4dir, key-and-door, hp-damage, item-pickup, impassable-cells, round-currency, shop-catalog, stairs-levels, reach-exit, player-death, event-points, score-records, undo-redo, undo-unlimited, redo, save-multi-slot, level-select, achievements-window, +deterministic-combat, +damage-preview, +critical-value, +multi-exit-score, +meta-currency-gates, +pure-run-bonus, +tile-memo]
proposes: ["+trigger:bump", "+cond:can_damage(a, b)", "+effect:fight(a, b)", "+effect:stat(a, name, ±n)", "+trigger:exit_reached(kind)", "+feature:route-memo", "+feature:pure-run", "+ui:drop-preview", "+card:multi-exit-score"]
author: opus
date: 2026-11-09
---

# Tactical Nexus — Magic Tower для мазохістів: детермінований бій, undo/redo і рахунок за кожну одиницю HP

## Суть
Сучасна безкоштовна Magic Tower (див. [magic-tower](magic-tower.md)): герой іде ручною вежею, вороги стоять і видні наперед, бій — чиста арифметика ATK−DEF, ключів **менше, ніж дверей**. Нового три речі: **повний undo/redo** (бо нема жодної випадковості), **кілька виходів з різними формулами рахунку** і **мета-прогресія медалями й сонячними каменями між вежами**. «Софтлок» тут чесний: гра не ховає, що ресурси скінченні, — вежа просто стає непрохідною, і гравець відкочує ходи.

## Поле і час
- Вежа = набір ручних поверхів-сіток, зʼєднаних сходами; карта памʼятає прогрес попередніх забігів.
- Покроково, але темп не важить: вороги нерухомі, хід = крок героя або бій.
- `random: none` — кожна вежа однакова щоразу; `info: full` — видно ворогів, дропи й ціну бою.
- База: 12 веж (від навчальних до Tactical Tower K); платні DLC-розділи складніші.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | HP, ATK, DEF, рівень, EXP, ключі | рух 4 напрямки; крок у ворога = бій |
| Ворог | enemy | HP, ATK, DEF, EXP, дроп | стоїть; бій лише за ініціативою гравця; дроп видно наперед |
| Двері | gate | колір (?) | відкриваються ключем; ключів на всі двері не вистачає |
| Ключ | pickup | — | +1 до запасу; також купується за рівень-ап |
| Предмет статів | pickup | +ATK / +DEF / +HP | постійне посилення |
| Golden Feather | pickup | множник | множить здобуток EXP |
| Heart Crown | pickup | множник | множить здобуток HP |
| Сходи | static | — | на інший поверх |
| Вихід | static | 1–3 на вежу, своя формула | кінець забігу, підрахунок рахунку |
| Nexus | neutral | — | крамниця, доступна будь-коли; рідкісні товари — за дверима медалей |
| Sunwisher | neutral | — | +стати за сонячні камені (мета-валюта) |
| Двері медалей | gate | ранг медалі | відкриваються витратою медалей |
| Мемо | mark | текст | нотатка гравця на будь-якій клітині, ділиться з іншими |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(hero, dir)`.
- КОЛИ `contact(hero, enemy)` → ЯКЩО `custom: «ATK героя ≤ DEF ворога»` → ТО `block` (атакувати не можна).
- КОЛИ `contact(hero, enemy)` → ТО `custom: «обмін ударами: герой бʼє ATK−DEF, ворог відповідає, доки хтось не впаде»`, `damage(hero, n)` — n показано до бою.
- КОЛИ `died(enemy)` → ТО `counter(exp, +n × feather)`, `give(hero, drop)`, `disappear(enemy)`.
- КОЛИ `counter(exp, >=, n)` → ТО `choose(options)` — стати або ключі (рівень-ап витрачається на одне з двох).
- КОЛИ `contact(hero, door)` → ЯКЩО `has(hero, key)` → ТО `take(hero, key)`, `disappear(door)`; інакше `block`.
- КОЛИ `picked(hero, stat_item)` → ТО `custom: «стат +n (HP × crown)»`.
- КОЛИ `input(nexus)` → ТО `window(shop-window)`; ЯКЩО `has(hero, medal)` → ТО `custom: «відчинити двері медалей у Nexus»`.
- КОЛИ `contact(hero, sunwisher)` → ЯКЩО `has(player, sunstones)` → ТО `custom: «+стат за сонячні камені»`.
- КОЛИ `reach(hero, exit)` → ТО `custom: «рахунок = f_exit(HP, стати, рівень)»`, `window(end-screen)`.
- КОЛИ `level_end` → ЯКЩО `counter(score, >=, threshold)` → ТО `give(player, medal)` рангу за рахунком.
- КОЛИ `level_end` → ЯКЩО `custom: «жодної медалі не витрачено (Pure Nexus)»` or `custom: «рахунок аномально високий»` → ТО `currency(+sunstones)`; інакше нічого.
- КОЛИ `input(undo)` → ТО `undo(1)`; КОЛИ `input(redo)` → ТО `custom: «redo»`.
- КОЛИ `hp_zero(hero)` → ТО `lose` (на практиці — undo).
- Перемога: дійти до будь-якого виходу. Поразка: HP = 0 або вежа стала непрохідною (ресурсів не вистачає) — гра не завершує, гравець відкочує. Рахунок: найкращий окремий забіг, без накопичення.

## Керування і ввід
- Клавіші/миша: крок, бій «у ворога», undo/redo миттєво (будь-яку кількість дій).
- Збереження/завантаження станів; мемо — поставити нотатку на клітину й поділитися планом маршруту.
- На іконці ворога — ціна бою в HP і скільки ATK треба, щоб бій став коротшим.

## Вікна, меню, HUD
- `game-screen` — поверх, `stat-panel` (HP, ATK, DEF, рівень, EXP, ключі), прогноз втрат і дропу на ворогах (`damage-preview`, `drop-preview`), мемо-позначки.
- `level-select` — вибір вежі; `shop-window` — Nexus і Sunwisher.
- `end-screen` — вихід, формула, рахунок, медаль; `achievements-window` / медалі (?).
- `save-slots` — збережені стани.
- Переходи: `main-menu` → `level-select` → `game-screen` ⇄ `shop-window`; вихід → `end-screen` → `level-select`.

## Фічі поза полем
- `undo` (∞) + `redo`, `save-slots`, `cloud-save` (Steam Cloud).
- `meta-progression`: медалі (ранги за рахунок) і сонячні камені переносяться між вежами й відкривають глибші поверхи; **Pure-забіг** без медалей дає бонус — добровільний hard-mode.
- `level-sharing`-подібне: мемо маршрутів можна ділити (`+feature:route-memo`).
- `localization` (EN, JA); free to play без мікротранзакцій, DLC-вежі.

## Варіації й родичі
- [magic-tower](magic-tower.md) — жанр і формула бою; [h5mota](h5mota.md) — китайська спільнота веж; DungeonUp — процедурний нащадок.
- Відмінність від класики: формула бою спрощена до «обмін ATK−DEF» (без описаних спецздібностей), рівні-апи замість купівлі в вівтаря, кілька виходів, undo/redo вбудовано.
- Осі варіацій: **відкат** (сейви → повний undo/redo) · **мета** (нема → медалі/камені між вежами) · **фініш** (один вихід → 1–3 виходи з різними формулами) · **рахунок** (HP лишок → функція від HP, статів і рівня).

## Цікавинки для курсу
- Детермінований бій ATK−DEF з прогнозом втрат на іконці — 🌱.
- Undo/redo як стек станів (бо світ детермінований, достатньо логу дій) — 📎.
- Рівень-ап: стати **або** ключі — дилема ресурсу — 🌱.
- Кілька виходів із різними формулами рахунку — 🌱.
- Мета-валюта, що відкриває двері в інших рівнях, і бонус «Pure» за відмову від неї — 📎.
- Детектор софтлоку: чи досяжний бодай один вихід з поточного стану — 👑 (пошук у просторі «зібрано/відчинено/вбито», як розвʼязувач Magic Tower).

## Мапа на каталог
- Є: `move-4dir` · `key-and-door` · `hp-damage` · `item-pickup` · `impassable-cells` · `round-currency` (EXP/рівні) · `shop-catalog` (Nexus) · `stairs-levels` · `reach-exit` · `player-death` · `event-points` · `score-records` · `undo-redo` + `undo-unlimited` + `redo` · `save-multi-slot` · `level-select` · `achievements-window` (медалі).
- **Нема** → пропозиції карток:
  - `+deterministic-combat`, `+damage-preview`, `+critical-value` — як у [magic-tower](magic-tower.md).
  - `+multi-exit-score` «Кілька виходів, кожен зі своєю формулою рахунку» · rules/goal · 🌱.
  - `+meta-currency-gates` «Двері, що відкриває валюта з інших рівнів» · progression/meta · 📎.
  - `+pure-run-bonus` «Бонус за забіг без мета-допомоги» · progression/meta · 🌱.
  - `+tile-memo` «Нотатка гравця на клітині, якою можна поділитись» · interface/input · 🌱 (родич `dot-mark`).

## Пропозиції до словників
- `+trigger:bump` — рух у клітину, зайняту ворогом/дверима (бій, відкриття).
- `+cond:can_damage(a, b)` — ATK A > DEF B.
- `+effect:fight(a, b)` — атомарний розрахунок бою й застосування втрат.
- `+effect:stat(a, name, ±n)` — змінити ATK/DEF (бо `hp`/`heal` не покривають).
- `+trigger:exit_reached(kind)` — досягнуто виходу певного виду (формула рахунку залежить від виду); `reach` не несе вид.
- `+feature:route-memo` — нотатки гравця на клітинах, якими можна ділитися.
- `+feature:pure-run` — режим/позначка забігу без мета-бонусів.
- `+ui:drop-preview` — що випаде з ворога, видно до бою.
- `+card:multi-exit-score` — див. картку.

## Джерела
- ⭐ [Review: Tactical Nexus (smithgift)](https://smithgift.substack.com/p/review-tactical-nexus) — бій, дефіцит ключів, рівень-ап «стати або ключі», виходи й рахунок, Nexus, медалі, сонячні камені, Pure, мемо, undo/redo, складність окремих веж.
- [Steam: Tactical Nexus](https://store.steampowered.com/app/1141290/Tactical_Nexus/) — 12 веж, «без рандому», undo/redo, мемо, медалі/камені, free to play, DLC.

## Непевне
- (?) Кольори дверей і ключів, точний набір предметів, наявність спецздібностей ворогів — огляд їх не згадує.
- (?) Хто бʼє першим у бою й чи відповідає ворог після смертельного удару.
- (?) Формули рахунку для різних виходів — у джерелах лише «HP, стати й рівні».
- (?) Чи медалі показано окремим вікном досягнень, чи лише на `end-screen`.
- (?) Запит черги «чесний софтлок» — прочитано як «ресурси скінченні, гра не рятує, виручає undo»; явного детектора софтлоку в джерелах нема.
