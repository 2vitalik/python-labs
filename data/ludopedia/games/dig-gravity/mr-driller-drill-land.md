---
title: Mr. Driller Drill Land
slug: mr-driller-drill-land
aka: [Mr. DRILLER DrillLand, ミスタードリラー ドリルランド, Drill Land]
family: dig-gravity
also: [falling-match]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: setup
  goal: state
year: 2002
platforms: [GameCube, Switch, Windows, PS4, PS5, Xbox One, Xbox Series]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mr._Driller_Drill_Land", best: true, note: "п'ять атракціонів і їхні правила, штампи → бос, валюта й магазин, ремастер 2020 з Casual-режимом"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ミスタードリラー_ドリルランド", note: "JA: правила атракціонів (HP, привиди в блоках, свята вода, без повітря), персонаж на атракціон, характеристики персонажів, Drill Camp"}
  - {kind: steam, url: "https://store.steampowered.com/app/1126750/Mr_DRILLER_DrillLand/", note: "ремастер 2020: 5 атракціонів, до 4 гравців локально (Race, Free-for-All, Doubles), Casual-режим, лідерборди"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mr+Driller+DrillLand+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-4dir, gravity-fall, environment-death, player-death, item-pickup, key-and-door, hp-damage, timed-despawn, round-currency, shop-between-levels, character-select, mode-select, difficulty-levels, level-unlock, leaderboard, +connected-group-pop, +group-support, +hunger-clock, +delayed-fall, +depth-goal, +character-classes, +boss-fight, +shared-field-versus, +attraction-rulesets, +ghost-in-block, +stamp-unlock-boss]
proposes: ["+card:attraction-rulesets", "+card:ghost-in-block", "+card:stamp-unlock-boss", "+feature:mode-casual"]
author: opus
date: 2026-11-09
---

# Mr. Driller Drill Land — підземний парк розваг: п'ять атракціонів, кожен міняє одне правило Mr. Driller

## Суть
Сиквел [Mr. Driller](mr-driller.md), зібраний як парк із п'яти «атракціонів»: базове буріння крізь кольорові блоки лишається, але кожен атракціон **підміняє одну деталь ядра** — замість повітря HP, блоки з привидами, яких виганяють святою водою, пастки замість годинника-повітря, ключ і двері, зіркові блоки, що блимають і зникають. Атракціон привʼязаний до свого персонажа з власними характеристиками. Тут описано лише відмінності від базового файла.

## Поле і час
- Та сама вертикальна шахта з кольоровими блоками, групами одного кольору, падінням груп без опори і ланцюгами 4+ (див. базовий файл).
- Атракціони змінюють шари поля: темрява з привидами всередині блоків (Horror Night House), пастки (Drindy Adventure), ключ/двері (Hole of Druaga), блоки з таймером зникнення (Star Driller).
- Real-time; у кожної стадії — обрана складність.

## Сутності
Лише нове відносно Mr. Driller.
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Сусуму | player | середні; мало витрачає повітря | для новачків; єдиний у Star Driller |
| Анна | player | трохи швидше вбік; трохи більше повітря | єдина в Hole of Druaga |
| Атару | player | найшвидший; багато повітря | єдиний у Horror Night House |
| Тайдзо | player | найшвидше вниз; повільний вбік; багато повітря | єдиний у Drindy Adventure |
| Horinger Z | player | барʼєр | один раз переживає розчавлення; без барʼєра витрата повітря зростає |
| Кролик (Usagi) | player | відкривається умовою | високий стрибок, бурить у три боки, багато повітря |
| Ключ | pickup | — | Hole of Druaga: треба дістати |
| Двері | gate | — | відчиняються ключем — вихід зі стадії Druaga |
| Druaga (Еґурі) | boss | — | бос Hole of Druaga; перемога — прохід атракціону |
| Привид у блоці | enemy | рухається всередині блоків | Horror Night House: вибурив блок із привидом — усі привиди атакують, мінус HP |
| Святий блок | static | — | привиди не можуть у нього зайти |
| Свята вода | pickup | — | влита в блок ослаблює привида; потім вибурити — вигнати |
| Дрістал (кристал) | pickup | — | випадає з вигнаного привида |
| Пастки Drindy: камені, що котяться; шипи | hazard | — | Drindy Adventure: повітря нема, загроза — пастки |
| Зірковий блок | tile | короткий час | Star Driller: блимає й невдовзі зникає |
| «?»-предмет | pickup | — | Star Driller: випадковий ефект (?) |
| Події: «повне затемнення», «біла комета» | hazard | — | Star Driller: заважальні події (ефект не описано) |
| Тобі Масуйо | ally | — | помічник у Star Driller |
| Dr. Manhole | boss | — | після 5 штампів; перемога відкриває наступний рівень парку |

## Правила (КОЛИ → ЯКЩО → ТО)
Лише нове відносно [Mr. Driller](mr-driller.md).
- КОЛИ `input(attraction)` → ТО `custom: «атракціон задає персонажа й набір правил»`, `window(game-screen)`.
- World Drill Tour: як Mission-режим серії — стадії за країнами, будь-який персонаж; правила базові.
- Hole of Druaga: КОЛИ `contact(anna, key)` → ТО `pickup`; КОЛИ `contact(anna, door)` → ЯКЩО `has(anna, key)` → ТО `disappear_b`, `next_level`; інакше `block`. Фінал — бій з Druaga (`custom: «перемогти боса»` → `win`).
- Horror Night House: КОЛИ `input(drill, block)` → ЯКЩО `occupied(block, ghost)` and `not state(ghost, weakened)` → ТО `custom: «усі привиди на екрані атакують»`, `damage(atal, n)`.
- Horror Night House: КОЛИ `input(holy_water, block)` → ЯКЩО `occupied(block, ghost)` → ТО `set_state(ghost, weakened)`; КОЛИ `input(drill, block)` → ЯКЩО `state(ghost, weakened)` → ТО `disappear`, `spawn(drystal)`.
- Horror Night House: КОЛИ `custom: «привид рухається в сусідній блок»` → ЯКЩО `cell(target, holy_block)` → ТО `block`.
- Horror Night House: КОЛИ `hp_zero(atal)` → ТО `lose` (HP замість повітря).
- Horror Night House, Drindy Adventure: КОЛИ `pattern(group(4))` → ТО `custom: «блоки не зникають»` (правило ядра вимкнене).
- Drindy Adventure: `custom: «лічильника повітря нема»`; КОЛИ `contact(boulder|spike, taizo)` → ТО `lose` (?) — загроза лише пастки й падаючі блоки.
- Star Driller: КОЛИ `spawned(star_block)` → ТО `set_state(star_block, blinking, n)`; КОЛИ `state_off(star_block, blinking)` → ТО `disappear` (опора під групою зникає сама).
- Star Driller: КОЛИ `contact(susumu, item_q)` → ТО `custom: «випадковий ефект»` (?); КОЛИ `schedule(events)` → ТО `custom: «затемнення / біла комета заважають»` (?).
- Horinger Z: КОЛИ `contact(falling_block, horinger)` згори → ЯКЩО `state(horinger, barrier)` → ТО `clear_state(horinger, barrier)`; інакше `lose`.
- КОЛИ `custom: «атракціон пройдено»` → ТО `give(player, stamp)`, `currency(+n)`; КОЛИ `counter(stamps, ==, 5)` → ТО `unlock(boss_manhole)`; перемога над ним → `unlock(next_park_level)`.
- Перемога: дно стадії (база) або ціль атракціону (двері, бос, привиди). Поразка: розчавлення, 0 повітря / 0 HP, пастка. Рахунок і очки — як у базі (?).

## Керування і ввід
- Як у Mr. Driller: хрестовина / стік — рух, кнопка — бурити в напрямку; Кролик — стрибок і буріння у три боки, Еґурі — бурить два блоки попереду, Ковас — три напрямки вперед (з JA-вікі, ролі в атракціонах — (?)).
- Свята вода в Horror Night House — окрема дія на блок (?).
- До 4 гравців на одній консолі.

## Вікна, меню, HUD
- `map-window` — парк Drill Land: атракціони як вузли, штампи, нічний парад персонажів.
- `character-select` — у більшості атракціонів персонаж заданий; вільний вибір — у World Drill Tour.
- `difficulty-select` — складність кожної стадії.
- `shop-window` — сувенірна крамниця: покращення, сувеніри, колекційні картки персонажів за валюту атракціонів.
- `game-screen`: шахта; праворуч `air-gauge` (повітря) або `hp-bar` (Horror Night House), глибина, очки (?).
- `mode-select` Drill Camp: Race · Battle (медалі на одному екрані); ремастер: Race, Free-for-All, Doubles.
- `leaderboard` (ремастер, онлайн-таблиці).

## Фічі поза полем
- `world-map` парку + `level-unlock`: 5 штампів → бос Dr. Manhole → наступний рівень парку.
- `round-currency` + `shop-between-levels`: валюта з атракціонів, крамниця з покращеннями й колекційними картками (`collectibles`).
- `local-multiplayer` до 4 гравців (Drill Camp: Race, Battle); GameCube — звʼязок з GBA: імпорт вихованців Pacteria з Mr. Driller A у парад, ексклюзивні покращення.
- Ремастер 2020 (Switch/PC), 2021 (PS/Xbox): оновлена графіка, `+feature:mode-casual` (Casual — повільніший темп для новачків), `leaderboard-online`, `cloud-save`, 13 мов.

## Варіації й родичі
- Базовий файл: [Mr. Driller](mr-driller.md) — група 4+ одного кольору зникає, повітря й капсули, X-блоки, падіння груп.
- Відмінності-осі атракціонів: годинник — «повітря (база) / HP (Horror) / нема, лише пастки (Drindy)»; правило 4+ — «увімкнене / вимкнене (Horror, Drindy)»; ціль — «глибина / двері з ключем (Druaga) / боси»; блок — «вічний / зникає за часом (Star)»; персонаж — «вільний вибір / заданий атракціоном».
- Кросовери атракціонів: The Tower of Druaga (Hole of Druaga), Star Trigon (Star Driller); родичі серії — Mr. Driller 2 / G / A, [Dig Dug](dig-dug.md) (Тайдзо — батько Сусуму).

## Цікавинки для курсу
- Атракціони як «той самий двіжок, інший набір правил»: перемикач правил ядра (вимкнути 4+, замінити повітря на HP) — 🥈 (архітектура: правила як конфіг).
- Привиди всередині блоків + святі блоки, куди їм не можна, + «влий воду, потім бури» — 🥉 (сутність у шарі блоків, двокрокове знищення, штраф усім за помилку).
- Зірковий блок із таймером зникнення — опора зникає сама й запускає падіння груп — 📎.
- Персонажі зі статами (швидкість вбік / вниз, витрата повітря, барʼєр на один удар) — 📎.
- Мета-прогресія парку: штампи → бос → наступний рівень + валюта → крамниця — 🥉.

## Мапа на каталог
- Є: `move-4dir` · `gravity-fall` · `environment-death` ↔ розчавлення, пастки · `player-death` · `item-pickup` ↔ ключ, свята вода, дрістали · `key-and-door` ↔ Hole of Druaga · `hp-damage` ↔ HP у Horror Night House · `timed-despawn` ↔ зіркові блоки · `round-currency` + `shop-between-levels` ↔ валюта й крамниця · `character-select` · `mode-select` ↔ Drill Camp · `difficulty-levels` · `level-unlock` ↔ штампи → бос · `leaderboard` (ремастер).
- **Нема** → пропозиції карток:
  - Повтори з бази: `+connected-group-pop`, `+group-support`, `+hunger-clock` (повітря), `+delayed-fall`, `+depth-goal`; з корпусу: `+character-classes` (стати персонажів), `+boss-fight` (Druaga, Dr. Manhole), `+shared-field-versus` (Battle на одному екрані).
  - `+attraction-rulesets` «Режими-атракціони: той самий двіжок, підмінене правило і персонаж» · game-logic/modes · 🥈 · слоти {rule_overrides, fixed_character}.
  - `+ghost-in-block` «Ворог живе всередині блоків; святі блоки його не пускають; ослабити → знищити» · entities/interact · 🥉 · слоти {weaken: holy_water, punish: all_attack}.
  - `+stamp-unlock-boss` «Штампи за режими відкривають боса й наступний рівень» · levels/progression · 🌱 · слот {stamps: 5}.

## Пропозиції до словників
- `+feature:mode-casual` — повільніший «легкий» темп як окремий режим для новачків (ремастер DrillLand); не те саме, що `mode-zen` (тут програш лишається).
- `+card:attraction-rulesets`, `+card:ghost-in-block`, `+card:stamp-unlock-boss` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Mr. Driller Drill Land](https://en.wikipedia.org/wiki/Mr._Driller_Drill_Land) — ядро серії, п'ять атракціонів (World Tour, Hole of Druaga — ключ і двері, Horror Night House — свята вода, Drindy Adventure — камені й шипи, Star Driller — зіркові блоки), складність стадій, штампи → Dr. Manhole, валюта й крамниця, парад, звʼязок з GBA, ремастер з Casual-режимом.
- [Wikipedia JA](https://ja.wikipedia.org/wiki/ミスタードリラー_ドリルランド) — персонаж на кожен атракціон, HP і атака всіх привидів, святі блоки, вигнання й дрістали, вимкнене правило 4+ у Horror і Drindy, відсутність повітря в Drindy, події Star Driller, характеристики дев'яти персонажів, Drill Camp (Race, Battle).
- [Steam: Mr. DRILLER DrillLand](https://store.steampowered.com/app/1126750/Mr_DRILLER_DrillLand/) — 5 атракціонів і фінальний бос, до 4 гравців локально (Race, Free-for-All, Doubles), Casual-режим, лідерборди, 13 мов.
- YouTube: пошук «Mr Driller DrillLand gameplay».

## Непевне
- (?) Що роблять «?»-предмети, «затемнення» і «біла комета» в Star Driller — JA-вікі лише називає.
- (?) Чим закінчується стадія Drindy і що саме вбиває (камінь, шипи) — EN-вікі називає пастки, JA — лише «уникати пасток».
- (?) Чи є HUD-лічильник HP у Horror Night House як шкала, а не як цифра.
- (?) Хто з Еґурі, Коваса, Кіла Саака доступний гравцеві і де — JA-вікі дає стати, без привʼязки до атракціонів.
- (?) Вікіпедія каже, що ремастер у Японії вийшов як «Mr. Driller Encore» — не звірено з JA-джерелом.
- (?) Очки, ціни в крамниці, як Battle-режим нараховує медалі — не знайдено.
