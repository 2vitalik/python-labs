---
title: Dungeons of Daggorath
slug: dungeons-of-daggorath
aka: [DoD, Daggorath]
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: hidden
  random: runtime
  goal: state
year: 1982
platforms: [TRS-80 Color Computer, Dragon 32/64, PC (фан-порт)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dungeons_of_Daggorath", best: true, note: "суть: серцебиття замість HP, непритомність, текстові команди, звуки ворогів, 5 рівнів, два чарівники"}
  - {kind: other, url: "https://colorcomputerarchive.com/repo/Documents/Manuals/Games/Dungeons%20of%20Daggorath%20%28Tandy%29.txt", note: "мануал Tandy 1983 (текст): усі команди й скорочення, серце, факели, персні, сувої, фляги, істоти"}
  - {kind: other, url: "https://archive.org/stream/Dungeons_of_Daggorath_1983_Tandy/Dungeons_of_Daggorath_1983_Tandy_djvu.txt", note: "той самий мануал на Internet Archive (бачив у пошуку, не відкривав)"}
  - {kind: other, url: "https://daggorath.online/how.html", note: "фан-сайт: таблиця команд (бачив у пошуку, не відкривав)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=dungeons+of+daggorath+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, orientation-state, impassable-cells, chase-player, hp-damage, inventory, inventory-items, inventory-limit, item-pickup, item-identification, stairs-levels, player-death, permadeath, save-game, keyboard-controls, sound-warnings, fog-of-war, player-camera, +heartbeat-stamina, +faint-state, +typed-commands, +two-hand-slots, +light-source, +ring-incantation, +magic-passages, +first-person-grid, +strength-from-kills]
proposes: ["+trigger:heart(op, n)", "+effect:pulse(±n)", "+effect:faint(a)", "+effect:incant(item, word)", "+effect:identify(item)", "+cond:light(kind)", "+ui:heart-monitor", "+ui:command-prompt", "+ui:hand-slots", "+axis:control=typed", "+axis:view=first-person", "+card:heartbeat-stamina", "+card:typed-commands", "+card:ring-incantation"]
author: opus
date: 2026-11-09
---

# Dungeons of Daggorath — підземелля в реальному часі, де твоє здоровʼя — це серце, що б'ється

## Суть
Перший-особовий данжен-кроулер на клітинному лабіринті: гравець набирає текстові команди («ATTACK RIGHT», «TURN LEFT»), а вороги підходять у реальному часі, видаючи звук, що гучнішає з наближенням. Замість HP — **серцебиття**: рух, вантаж, удари, перстені й отримані удари розганяють пульс; час і відпочинок його знижують. Надто швидке серце — **непритомність** (вороги бʼють далі), ще швидше — серце розривається, кінець гри. Мета — знайти й перемогти чарівника на останньому рівні.

## Поле і час
- Лабіринт із клітин; гравець у клітині з орієнтацією (N/E/S/W); крок вперед/назад/вбік, поворот на місці. Вид — каркасний 3D від першої особи (кути ліній задають глибину).
- Кілька рівнів-поверхів: діри (лише вниз) і драбини (вгору/вниз). Мануал: 3 відомі рівні + «чутки» про глибші; Wikipedia — 5 рівнів.
- Real-time: вороги рухаються й атакують незалежно від вводу; серце повільно сповільнюється з часом.
- Видимість залежить від світла: без факела — темрява, натикаєшся на стіни; звичайне світло показує звичайні проходи, магічне — магічні (трикутні).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | серце (пульс), сила, 2 руки, рюкзак, орієнтація | команди: рух, поворот, взяти/кинути, атака лівою/правою |
| Серце | — | пульс | ↑ від руху, вантажу, ударів, перснів, отриманих ударів; ↓ з часом |
| Істоти: гадюка, павук, злий лицар, усміхнений слиз, камʼяний велетень, скорпіон, примара, галдрог | enemy | сила (скільки ударів треба) | підходять з будь-якого боку, звук гучнішає; у твоїй клітині атакують; обходять і стають перед тобою |
| Чарівник (і демон у його образі) | boss | сильніший за всіх | спершу демон-двійник, потім справжній; підйом драбиною його дратує — посилає сильніших |
| Факел (сосновий / місячний / сонячний) | pickup | 15 / 30 / 60 хв | світло; місячний і сонячний — магічне світло, видно магічні двері й істот |
| Меч (деревʼяний / залізний / ельфійський) | pickup | сила удару | атака; сила росте з силою гравця |
| Щит (шкіряний / бронзовий / мітриловий) | pickup | захист | зменшує силу вхідних ударів; можна ним бити |
| Фляга (Hale / Abye / Thews) | pickup | ефект | випити (USE): ефект корисний або шкідливий, тимчасовий або постійний |
| Сувій (Vision / Seer) | pickup | — | спершу REVEAL, потім USE (карта/бачення (?)) |
| Перстень | pickup | сила, магічне слово | REVEAL коштує сили; INCANT правильного слова перетворює перстень; удари ним напружують серце |
| Діра | terrain | — | `CLIMB DOWN` лише вниз |
| Драбина | static | — | `CLIMB UP`/`CLIMB DOWN` |
| Стіна / магічний прохід | static | — | звичайна стіна блокує; магічний прохід прохідний навіть невидимим |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(MOVE [BACK|LEFT|RIGHT])` → ЯКЩО `free(target)` → ТО `move(player, dir)`, `custom: «пульс +»`; інакше `block` («bump»).
- КОЛИ `input(TURN LEFT|RIGHT|AROUND)` → ТО `face(player, dir)`.
- КОЛИ `input(CLIMB DOWN)` → ЯКЩО `cell(here, hole|ladder)` → ТО `custom: «на рівень нижче»`; КОЛИ `input(CLIMB UP)` → ЯКЩО `cell(here, ladder)` → ТО `custom: «на рівень вище; чарівник посилає сильніших»`.
- КОЛИ `input(GET L|R obj)` → ЯКЩО `custom: «рука порожня»` → ТО `pickup`; `DROP` — на підлогу; `PULL` — з рюкзака в руку; `STOW` — з руки в рюкзак.
- КОЛИ `input(ATTACK L|R)` → ТО `custom: «удар предметом у руці (голіруч — ляпас)»`, `custom: «пульс +»`; ЯКЩО влучив → `damage(n)` (`!!!` на екрані), інакше свист.
- КОЛИ `input(ATTACK)` → ЯКЩО `custom: «факел тьмяний»` → ТО `custom: «більше промахів»`.
- КОЛИ `contact(creature, player)` → ТО `custom: «удар: пульс +, щит зменшує силу»`; ЯКЩО `custom: «пульс високий»` → ТО `custom: «удар з більшою ймовірністю вбиває або валить з ніг»`.
- КОЛИ `custom: «пульс вище порогу непритомності»` → ТО `set_state(player, fainted)` — дії неможливі, істоти атакують далі.
- КОЛИ `custom: «пульс ще вищий»` → ТО `lose` (серце розривається).
- КОЛИ `tick` → ТО `custom: «пульс −»` (відпочинок).
- КОЛИ `hp_zero(creature)` → ТО `disappear_b`, `custom: «сила гравця +»`, `spawn_at(its items, cell)` (істоти підбирають предмети й лишають при смерті).
- КОЛИ `input(USE torch)` → ТО `custom: «світло на 15/30/60 хв»`, `reveal(passages)` за типом світла.
- КОЛИ `input(REVEAL L|R)` → ТО `custom: «визначити справжній тип предмета (перстень — коштує сили пропорційно його потузі)»`.
- КОЛИ `input(INCANT word)` → ЯКЩО `custom: «слово відповідає перстню»` → ТО `transform(ring)`; інакше нічого.
- КОЛИ `input(USE flask|scroll)` → ЯКЩО scroll `custom: «вже REVEAL»` → ТО ефект предмета.
- КОЛИ `died(wizard)` → ТО `win`.
- Перемога: убити справжнього чарівника (після демона-двійника). Поразка: смерть від удару або розрив серця. Рахунку нема.

## Керування і ввід
- Набір команд у 4-рядковій зоні внизу екрана, Enter — виконати: `MOVE`, `TURN`, `CLIMB`, `EXAMINE`, `LOOK`, `GET`, `DROP`, `PULL`, `STOW`, `ATTACK`, `USE`, `REVEAL`, `INCANT`, `ZSAVE`, `ZLOAD`.
- Скорочення до найкоротшого однозначного: `M`, `M B`, `T L`, `T A`, `C U`, `G L T`, `A R`, `I S`…; `SWORD` не можна скоротити до `S` (конфлікт із `SHIELD`); незрозуміле — `???`.
- Ліва/права рука — аргумент майже кожної команди.

## Вікна, меню, HUD
- `game-screen`: вгорі — 3D-вид коридору; по краях — предмети в лівій і правій руці (`hand-slots`); у центрі — серце, яке видно й чути (`heart-monitor`); внизу — `command-prompt` на 4 рядки.
- `EXAMINE` — режим огляду: список предметів на підлозі клітини й у рюкзаку (запалений факел виділено) → `inventory-window`; `LOOK` — назад до виду.
- `save-slots`-подібне: `ZSAVE імʼя`/`ZLOAD імʼя` на касету.
- Звук як HUD: кроки істот гучнішають з наближенням; свист промаху.

## Фічі поза полем
- `save-game` на касету за іменем файла.
- Нема меню, налаштувань, рекордів — один забіг до перемоги чи смерті.

## Варіації й родичі
- Родичі: [dungeon-master](dungeon-master.md) (1987) — real-time клітинний кроулер від першої особи з загоном; [legend-of-grimrock](legend-of-grimrock.md) — сучасний нащадок; [rogue](rogue.md) (ідентифікація предметів, ресурси).
- Осі варіацій: **життя** (HP / серцебиття-навантаження / голод) · **ввід** (текстові команди / клавіші / миша) · **видимість** (світло з таймером / типи світла відкривають різне) · **магія** (перстень зі словом / руни / сувої).

## Цікавинки для курсу
- Серце як єдиний ресурс: дії піднімають, час знижує, пороги непритомності й смерті — 📎 (один лічильник з двома порогами).
- Парсер команд зі скороченнями до найкоротшого однозначного префікса — 🥉 (таблиця команд, конфлікти префіксів).
- Факели з таймером і типами світла, що відкривають різні проходи — 📎.
- REVEAL/INCANT: ідентифікація предмета й магічне слово-ключ — 🌱.
- Звук-підказка, гучність за відстанню до ворога — 🌱 (у консолі — текст «шерех ближче»).
- Ворог, що обходить і стає перед гравцем — 📎.

## Мапа на каталог
- Є: `move-4dir` + `orientation-state` (поворот на місці) · `impassable-cells` · `chase-player` · `hp-damage` (≈ удари) · `inventory`/`inventory-items`/`inventory-limit` (2 руки + рюкзак) · `item-pickup` · `item-identification` (REVEAL) · `stairs-levels` (діри, драбини) · `player-death`/`permadeath` · `save-game` · `keyboard-controls` · `sound-warnings` (звук істот) · `fog-of-war` (світло) · `player-camera` (вид від першої особи).
- **Нема** → пропозиції карток:
  - `+heartbeat-stamina` «Пульс замість HP: дії піднімають, час знижує» · entities/state · 📎 · слоти {faint, burst}.
  - `+faint-state` «Непритомність: гравець не діє, вороги — так» · entities/state · 🌱.
  - `+typed-commands` «Ввід текстовими командами зі скороченнями» · interface/input · 🥉.
  - `+two-hand-slots` «Ліва/права рука як окремі слоти дій» · entities/state · 🌱.
  - `+light-source` «Факел з таймером, тип світла відкриває різне» · interface/render · 📎.
  - `+ring-incantation` «Предмет активується правильним словом» · entities/interact · 🌱.
  - `+magic-passages` «Проходи, видимі лише при магічному світлі» · entities/legality · 🌱.
  - `+first-person-grid` «Вид від першої особи на клітинній мапі» · interface/render · 🥈.
  - `+strength-from-kills` «Перемога над істотою дає силу» · entities/state · 🌱.

## Пропозиції до словників
- `+trigger:heart(op, n)` — пульс перетнув поріг (непритомність / смерть).
- `+effect:pulse(±n)` — змінити пульс; `+effect:faint(a)` — непритомність на час; `+effect:incant(item, word)` — вимовити слово над предметом; `+effect:identify(item)` — розкрити справжній тип.
- `+cond:light(kind)` — є світло потрібного типу (звичайне/магічне).
- `+ui:heart-monitor` — анімоване серце зі звуком як індикатор стану; `+ui:command-prompt` — рядок вводу текстових команд; `+ui:hand-slots` — ліва/права рука.
- `+axis:control=typed` — керування набором команд; `+axis:view=first-person`.
- `+card:heartbeat-stamina` · `+card:typed-commands` · `+card:ring-incantation`.

## Джерела
- ⭐ [Wikipedia: Dungeons of Daggorath](https://en.wikipedia.org/wiki/Dungeons_of_Daggorath) — серцебиття, непритомність, команди, звуки, 5 рівнів, DynaMicro/Tandy.
- [Мануал Tandy (текст, colorcomputerarchive)](https://colorcomputerarchive.com/repo/Documents/Manuals/Games/Dungeons%20of%20Daggorath%20%28Tandy%29.txt) — повний список команд і скорочень, екран, серце, факели 15/30/60 хв, мечі, щити, фляги, сувої, персні, істоти, діри й драбини, чарівник.

## Непевне
- (?) Рік: Wikipedia в інфобоксі — 1982 (без джерела), у тексті — 1983.
- (?) Кількість рівнів: мануал — 3 відомі + чутки; Wikipedia — 5.
- (?) Розмір лабіринту рівня й чи він генерується, чи фіксований — не знайшов.
- (?) Що саме роблять фляги Hale/Abye/Thews і сувої Vision/Seer (за памʼяттю — Seer/Vision показують карту рівня з істотами чи без) — мануал навмисно не розкриває.
- (?) Числових порогів пульсу мануал не дає.
- (?) Чи серце саме по собі є «HP» (чи є окрема шкода) — мануал описує удари через пульс і силу; трактую серце як єдиний життєвий ресурс.
