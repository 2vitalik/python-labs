---
title: Super Puzzle Fighter II Turbo
slug: super-puzzle-fighter-ii-turbo
aka: [Super Puzzle Fighter II X, Puzzle Fighter, SPF2T, スーパーパズルファイターIIX]
family: falling-match
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: survive
year: 1996
platforms: [arcade, PlayStation, Saturn, PC, Dreamcast, GBA, PS3, Xbox 360, Switch, PS4, Xbox One]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Super_Puzzle_Fighter_II_Turbo", best: true, note: "поле 6×12, crash gems, power gems ≥2×2, counter gems з лічильником 5, діамант кожні 25, sousai, режими X/Y/Z, HD Remix"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/スーパーパズルファイターIIX", note: "JA: 2 приховані ряди, counter gem зникає від сусіднього очищення будь-якого кольору, 72 сміття = KO, offset вимикається через 3 хв"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Capcom+Fighting+Collection", note: "пошук; перевидання 2022 у Capcom Fighting Collection"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=super+puzzle+fighter+ii+turbo+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [gravity-fall, multi-cell-size, chain-reaction, garbage-attack, simultaneous-versus, ai-opponent, hot-seat, character-select, mode-select, difficulty-levels, keyboard-controls, event-effects, online-multiplayer, leaderboard, end-screen, game-over-continue, next-queue, +crash-gem-detonate, +power-gem-merge, +counter-gem-countdown, +drop-pattern-per-character, +color-clear-item, +garbage-offset, +offset-timeout]
proposes: ["+trigger:pattern(rect)", "+effect:countdown(a, -1)", "+effect:clear_color(color)", "+cond:adjacent_cleared(a)", "+card:power-gem-merge", "+card:counter-gem-countdown", "+card:drop-pattern-per-character"]
author: opus
date: 2026-11-09
---

# Super Puzzle Fighter II Turbo — кольорові камені не зникають самі: їх підриває crash gem, а прямокутники зливаються в power gems

## Суть
Дуель 1×1 на двох полях: зверху падають пари камінців чотирьох кольорів. Звичайні камені самі не очищаються — лише коли до групи їхнього кольору торкнеться круглий crash gem того ж кольору: тоді зникає вся звʼязана група. Камені одного кольору, складені прямокутником ≥2×2, зливаються в один великий power gem, що дає більшу атаку. Атака приходить суперникові як counter gems з таймером: за N ходів вони стають звичайними каменями.

## Поле і час
- Поле 6 стовпців × 12 рядів на гравця (+2 приховані зверху); 4-й стовпець зліва вищий на клітину — точка появи пари. Заблоковано точку появи → поразка.
- Real-time падіння пари; після приземлення — фаза розвʼязання: окреме падіння каменів → підриви → осідання → повтор (ланцюг). Ввід на цей час вимкнено.
- Два поля поруч, між ними — персонажі-бійці, анімація атаки пропорційна кількості сміття (косметика).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пара каменів | player | 2 камені (normal/crash), орієнтація | зсув, поворот, прискорення; приземлилась → камені падають окремо |
| Звичайний камінь (gem) | tile | колір 1 з 4 | звʼязується з сусідами кольору (4-сусідство); сам не очищається |
| Crash gem | tile | колір | торкається каменя свого кольору → очищає всю звʼязану групу цього кольору |
| Power gem | tile | колір, розмір ≥2×2 | злиття прямокутника однакових; може рости, не розпадається; більша атака |
| Counter gem | hazard | колір, лічильник (зазв. 5) | сміття від суперника; −1 за кожну поставлену пару; на 0 → звичайний камінь |
| Діамант (rainbow gem) | pickup | кожні 25 пар | падає на камінь → очищає всі камені цього кольору на полі; атака ослаблена (50 %) |
| Точка появи | static | 4-й стовпець | зайнята → поразка |
| Шаблон сміття персонажа | spawner | 6×N кольорів | фіксований для кожного бійця: як розфарбовані counter gems |
| Черга вхідної атаки | spawner | к-сть | попередження над полем; падає разом після ходу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(shift)` → ЯКЩО `free(target)` → ТО `move(pair, dir)`; КОЛИ `input(rotate)` → ТО `rotate(pair, 90)`.
- КОЛИ `tick` → ТО `fall(pair)`; ↓ — швидше.
- КОЛИ `locked(pair)` → ТО `fall(each_gem)` до опори.
- КОЛИ `contact(crash_gem, gem)` → ЯКЩО `same(crash_gem, gem, color)` → ТО `clear(group)` — уся звʼязана група цього кольору, разом з power gems і crash gems.
- КОЛИ `after(clear)` → ТО `fall(all_unsupported)`; новий контакт crash gem → `combo(+1)` (ланцюг).
- КОЛИ `pattern(square, 4)` → ЯКЩО `same(gems, color)` and `custom: «прямокутник ≥2×2 зі звичайних каменів»` → ТО `merge(gems → power_gem)`; суміжні прямокутники розширюють power gem.
- КОЛИ `custom: «очищення в кроці»` → ТО `send_garbage(n)` — n росте з розміром power gems і ланцюгом; дрібні ланцюги без power gems шкодять мало.
- КОЛИ `custom: «вхідна атака у попередженні»` → ЯКЩО `custom: «гравець сам щось очистив»` → ТО `custom: «offset (sousai) — гасить вхідне; надлишок летить назад»`.
- КОЛИ `timer(180 s)` від початку матчу → ТО `custom: «offset вимкнено»`.
- КОЛИ `custom: «атака прийшла»` → ТО `spawn_at(counter_gem, top)` за шаблоном персонажа-суперника, з лічильником 5.
- КОЛИ `locked(pair)` → ТО `custom: «лічильник усіх counter gems −1»`; КОЛИ `counter(timer, ==, 0)` → ТО `transform(counter_gem, gem)`.
- КОЛИ `custom: «поруч очищено звичайний / power / crash камінь будь-якого кольору»` → ТО `disappear(counter_gem)`; crash gem свого кольору сам counter gem не очищає.
- КОЛИ `counter(pairs, ==, 25)` → ТО `spawn(diamond)`; КОЛИ `contact(diamond, gem)` → ТО `custom: «clear_color — усі камені кольору під діамантом»`, `send_garbage(n × 0.5)` (баг — без ослаблення).
- КОЛИ `count(unblocked_counter_gems, >=, 72)` → ТО `custom: «миттєвий KO»`.
- КОЛИ `spawned(pair)` → ЯКЩО `occupied(spawn_cell)` → ТО `lose`; у суперника `win` раунду. Матч — до N виграних раундів.
- Рахунок: очки за очищення й ланцюги; анімація «super combo» при ≥30 counter gems за раз.

## Керування і ввід
- Джойстик ←/→ — зсув, ↓ — швидше; кнопки — поворот за/проти годинникової. Обидва гравці одночасно (2 контролери) або проти CPU.
- Стратегія «запамʼятати шаблон сміття суперника» — шаблон фіксований на персонажа, тож гравець готує місця під його кольори.

## Вікна, меню, HUD
- `attract-demo` / `splash-screen` → `main-menu`: Arcade · Versus · Street Puzzle (PS/SS) · Options; HD Remix — онлайн, ранги.
- `character-select`: Ryu, Ken, Chun-Li, Sakura, Morrigan, Donovan, Hsien-Ko, Felicia (+ Mei-Ling, Anita на консолях; приховані Dan, Akuma, Devilotte).
- `difficulty-select` у Arcade: Easy (3 бої) · Normal/Hard (8 суперників + бос); Expert/Master — без offset.
- `game-screen`: два поля, `next-piece-preview` для кожного, `garbage-meter` (попередження атаки), `score`, бійці між полями, лічильники на counter gems.
- `end-screen` раунду → наступний раунд/суперник; `game-over-continue` в Arcade.
- `mode-select` (Dreamcast, HD Remix): X (оригінал) · X' (перебаланс) · Y (3 в лінію, як Columns) · Z (поле підіймається, курсор 2×2, як Panel de Pon).
- `settings-window`: швидкість падіння (прибрано в HD Remix), кількість раундів, складність.

## Фічі поза полем
- `mode-versus` локально, `online-multiplayer` і до 4 гравців, `spectator`, ранги (HD Remix).
- `ai-opponent-levels` (Easy/Normal/Hard, Expert/Master), приховані персонажі як `unlockables`.
- Street Puzzle (PS/SS) — режим з нагородами-ілюстраціями; HD Remix: редактор шаблонів сміття (`custom-rules`).
- Музика прискорюється, коли поле майже повне (оригінал; прибрано в HD Remix).

## Варіації й родичі
- Puzzle Fighter (2017, мобільна) — наступник; Capcom Fighting Collection і Capcom Arcade 2nd Stadium (2022) — перевидання.
- Родичі: Puyo Puyo 2 (звідки взято offset), Columns (режим Y), Panel de Pon (режим Z), Baku Baku Animal (очищення лише «ключем»).
- **Осі варіацій**: що очищує (групи самі / лише детонатор свого кольору) · бонус форми (прямокутник → power gem / нема) · сміття (одразу тверде / таймер-лічильник ходів) · шаблон сміття (випадковий / фіксований на персонажа) · offset (є / вимикається з часом / нема).

## Цікавинки для курсу
- Crash gem як детонатор: flood fill групи кольору лише з точки контакту — 📎.
- Злиття однакових у максимальні прямокутники ≥2×2 з ростом power gem — 🥇 (пошук і розширення прямокутників без розпаду).
- Counter gems з лічильником ходів, що «дозрівають» у звичайні — 🌱.
- Шаблон сміття на персонажа як дані (матриця кольорів) — 🌱.
- Offset з вимкненням через 3 хв — 📎.
- Діамант «очистити колір» кожні 25 пар — 🌱.

## Мапа на каталог
- Є: `gravity-fall` · `multi-cell-size` (power gem) · `chain-reaction` · `garbage-attack` · `simultaneous-versus` · `ai-opponent` · `hot-seat` (одночасно; найближча) · `character-select` · `mode-select` · `difficulty-levels` · `keyboard-controls` · `event-effects` (анімації атаки) · `online-multiplayer` · `leaderboard` · `end-screen` · `game-over-continue` · `next-queue`.
- **Нема** → пропозиції карток:
  - `+crash-gem-detonate` «Група очищається лише детонатором свого кольору» · entities/interact · 📎.
  - `+power-gem-merge` «Злиття однакових у прямокутник» · entities/state · 🥇 · слоти {min: 2×2}.
  - `+counter-gem-countdown` «Сміття з лічильником ходів до дозрівання» · game-logic/opponent · 🌱 · слоти {start: 5}.
  - `+drop-pattern-per-character` «Фіксований шаблон сміття на персонажа» · game-logic/opponent · 🌱.
  - `+color-clear-item` «Предмет очищує весь колір» · entities/interact · 🌱 (спільне з монетою Baku Baku).
  - `+garbage-offset` «Гасіння вхідного сміття своїм очищенням» · game-logic/opponent · 📎 (спільне з Puyo).
  - `+offset-timeout` «Offset вимикається з часом матчу» · game-logic/opponent · 🌱.

## Пропозиції до словників
- `+trigger:pattern(rect)` — форма шаблону «прямокутник ≥ w×h» (поруч з наявною `square`).
- `+effect:countdown(a, -1)` — зменшити лічильник на сутності (counter gems; бомби з лічильником ходів).
- `+effect:clear_color(color)` — очистити всі клітини кольору (діамант SPF2T, монета Baku Baku; пропонував і Columns).
- `+cond:adjacent_cleared(a)` — поруч з A очищено (пропонував Puyo; тут — для counter gems).
- `+card:power-gem-merge`, `+card:counter-gem-countdown`, `+card:drop-pattern-per-character` — див. вище.

## Джерела
- ⭐ [Wikipedia: Super Puzzle Fighter II Turbo](https://en.wikipedia.org/wiki/Super_Puzzle_Fighter_II_Turbo) — поле 6×12 (4-й стовпець 13), crash/power/counter gems, лічильник 5, діамант кожні 25 і його сила (50/80/100 %), sousai і «garbage overflow», персонажі, режими X/Y/Z, HD Remix, платформи.
- [Wikipedia JA: スーパーパズルファイターIIX](https://ja.wikipedia.org/wiki/スーパーパズルファイターIIX) — 2 приховані ряди, counter gem зникає від сусіднього очищення будь-якого кольору, 72 сміття — летально, offset вимикається після 3 хв, режими складності, шаблони сміття персонажів.

## Непевне
- (?) Формула атаки (скільки counter gems за power gem певного розміру й за крок ланцюга) — у джерелах нема.
- (?) StrategyWiki віддав 403 — шаблони сміття конкретних персонажів не бачив.
- (?) Розбіжність: EN каже, що counter gems прибирає crash gem їхнього кольору поруч з очищенням; JA — що crash gem того ж кольору їх не очищує, але зникають від будь-якого сусіднього очищення. Записано за JA.
- (?) Чи offset вимикається саме о 3:00 у всіх версіях (JA) — не звірено з EN.
