---
title: Joshua & the Battle of Jericho
slug: joshua-battle-of-jericho
aka: [Joshua, Joshua and the Battle of Jericho]
family: dig-gravity
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: hidden
  random: none
  goal: collect
year: 1992
platforms: [NES, Game Boy, MS-DOS, Mega Drive]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Joshua_%26_the_Battle_of_Jericho", best: true, note: "геймплей: ріг-«toots», квота металів, 5 «Joshua questions», вікторина між рівнями, паролі, 100 рівнів, лінія Crystal Mines → Exodus → Joshua"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Exodus:_Journey_to_the_Promised_Land", note: "попередник на двіжку Crystal Mines: W-постріли, манна, 5 знаків питання, вікторина → життя"}
  - {kind: other, url: "https://lutris.net/games/joshua-and-the-battle-of-jericho/", note: "опис: мішки в лабіринті, стрільба, питання між рівнями"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Joshua+Battle+of+Jericho+NES+gameplay", note: "пошук; геймплей NES"}
stage: v1
coverage: 45
mechanics: [move-4dir, shoot-forward, projectile-shot, destructible-blocks, hidden-under-block, push-object, impassable-cells, item-pickup, collect-quota, reach-exit, time-out, touch-death, player-death, sequential-levels, level-password, hot-seat, status-panel, goal-counter, +multi-resource-quota, +quiz-between-levels, +engine-reskin]
proposes: ["+window:quiz-window", "+feature:quiz-between-levels", "+card:multi-resource-quota", "+card:quiz-between-levels", "+card:engine-reskin"]
author: opus
date: 2026-11-09
---

# Joshua & the Battle of Jericho — Crystal Mines у біблійному скіні: квота металів, ріг руйнує стіни, вікторина між рівнями

## Суть
Ісус Навин ходить лабіринтом Єрихона, сурмить у шофар (ноти-«toots» летять уперед), руйнує блоки стіни й перешкоди, збирає **квоту чотирьох металів** (золото, срібло, мідь, залізо) і **п'ять знаків-питань**, а потім іде до виходу до кінця часу. Між рівнями — **вікторина**: п'ять питань з вибором відповіді з Книги Ісуса Навина. Двіжок — Crystal Mines (Color Dreams, 1989) через Exodus (1991): та сама клітинна шахта з руйнівними блоками, перемальована під інший сюжет. Для корпусу гра цікава двома речами: квотою кількох видів ресурсів і вікном-вікториною, яке не впливає на прохід.

## Поле і час
- Лабіринт-шахта на квадратній сітці зі скролом (успадковано від Crystal Mines (?)).
- Real-time з таймером рівня.
- `info: hidden` — частина предметів схована під блоками й зʼявляється після руйнування.
- Гравітація для валунів — як у Crystal Mines (?): у джерелах про Joshua сказано лише «рухомі валуни».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Joshua | player | життя (?) | рух 4 напрямки; сурмить уперед; штовхає валуни |
| Нота-«toot» (білий восьмий знак) | projectile | — | летить уперед; знищує ворогів і руйнівні блоки |
| Блок стіни Єрихона | static | руйнівний | ламається нотою; може ховати предмет |
| «Israelite discontent», «Achan's sin», «foreign idols» | static | руйнівні | тематичні перешкоди; ламаються нотою |
| Рухомий валун | object | — | штовхається (падіння — (?)) |
| Нерухома перешкода | static | — | непрохідна, незнищенна |
| Золото · срібло · мідь · залізо | pickup | квота кожного виду | збираються до своїх лічильників |
| Знак-питання («Joshua question») | pickup | 5 на рівень | потрібні всі п'ять для виходу |
| Предмети й посилення | pickup | види (?) | зʼявляються з-під зруйнованих блоків |
| Аморейці, хетти, ханаанці, солдати | enemy | — | дотик шкодить (?); гинуть від ноти |
| Валаам | enemy | сильніший | потребує більше влучань (?) |
| Мешканці, кози | neutral (?) | — | заважають рухом (?) |
| Вихід | gate | обидві квоти | веде на вікторину й наступний рівень |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(target)` → ТО `move(joshua, dir)`.
- КОЛИ `contact(joshua, boulder)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `input(fire)` → ТО `spawn_at(toot, ahead)` у напрямку погляду.
- КОЛИ `contact(toot, breakable)` → ТО `disappear_both`; ЯКЩО `occupied(cell, hidden_item)` → ТО `reveal(cell)`.
- КОЛИ `contact(toot, enemy)` → ТО `damage(1)`; `hp_zero(enemy)` → `disappear`.
- КОЛИ `contact(joshua, metal[k])` → ТО `pickup`, `counter(metal[k], +1)`.
- КОЛИ `contact(joshua, question)` → ТО `pickup`, `counter(questions, +1)`.
- КОЛИ `contact(joshua, exit)` → ЯКЩО `counter(metal[k], >=, quota[k])` для всіх k and `counter(questions, ==, 5)` → ТО `window(quiz-window)`; інакше `block` (?).
- КОЛИ `contact(enemy, joshua)` → ТО `lives(-1)`, `restart` (?).
- КОЛИ `counter(time_left, ==, 0)` → ТО `lose`, `lives(-1)` (?).
- КОЛИ `input(answer)` у вікторині → ЯКЩО `custom: «відповідь правильна»` → ТО `counter(bibles, +1)`; інакше нічого; після 5 питань — `next_level` у будь-якому разі.
- Перемога (рівень): обидві квоти + вихід до кінця часу. Поразка: вороги/час (?) → −життя. Рахунок: Біблії за правильні відповіді; інше — (?).

## Керування і ввід
- NES-хрестовина — рух; кнопка — сурма (нота вперед); друга кнопка — (?) (у Crystal Mines — бомба).
- У вікторині — вибір варіанта відповіді курсором.
- Два гравці грають по черзі.

## Вікна, меню, HUD
- `main-menu`: 1/2 гравці, пароль (`level-password`) для повернення на досягнутий рівень.
- `game-screen`: лабіринт зі скролом; HUD — `timer-countdown`, лічильники чотирьох металів і знаків-питань (`goal-counter`), `lives` (?).
- `custom-window` → пропоную `+window:quiz-window`: питання + чотири (?) варіанти; правильна відповідь → Біблія; хибна не блокує прохід.
- `end-screen` / `game-over-continue` — (?).
- Переходи: main-menu → game-screen → (вихід) → quiz-window × 5 питань → game-screen наступного рівня; кожен 10-й (?) — бонусний етап.

## Фічі поза полем
- `levels-sequential`: 100 рівнів, 100 вікторин, 10 бонусних етапів.
- `level-password`: повернення на досягнутий рівень.
- `hotseat`: до двох гравців по черзі.
- Музики на рівнях нема (на відміну від Exodus).

## Варіації й родичі
- Лінія одного двіжка: [Crystal Mines](crystal-mines-ii.md) (NES, 1989; описаний у файлі сиквела) → Exodus: Journey to the Promised Land (1991; Мойсей, постріли «W», манна як квота, вікторина дає життя) → Joshua (1992; ноти, метали, Біблії) — **рескін**: правила поля майже ті самі, міняються спрайти, назви ресурсів і вікно між рівнями.
- Родичі: [Boulder Dash](boulder-dash.md) (квота → вихід), [Crystal Mines II](crystal-mines-ii.md) (постріл + руйнівні блоки), [Mr. Do!](mr-do.md) (стрільба в лабіринті).
- **Осі варіацій**: квота — «один вид (BD) / сума вартостей (CM II) / кілька видів окремо (Joshua)»; між рівнями — «нічого / пароль / вікторина без наслідку / вікторина → бонус (Exodus)».

## Цікавинки для курсу
- Квота кількох видів ресурсів, кожен зі своїм лічильником, + умова «і ще 5 жетонів» — 🌱.
- Вікно-вікторина між рівнями з банком питань і нагородою без штрафу — 📎: окреме вікно, дані питань з файла.
- Рескін як вправа: той самий двіжок, інший набір спрайтів, назв і вікон (тема як дані) — 📎; добре показує `logic-render-split`.
- Предмет під руйнівним блоком — 🌱 (картка `hidden-under-block` є).

## Мапа на каталог
- Є: `move-4dir` · `shoot-forward` + `projectile-shot` ↔ ноти · `destructible-blocks` ↔ стіна й «гріхи» · `hidden-under-block` · `push-object` ↔ валуни · `impassable-cells` · `item-pickup` · `collect-quota` ↔ метали · `reach-exit` · `time-out` · `touch-death` · `player-death` · `sequential-levels` · `level-password` · `hot-seat` · `status-panel` + `goal-counter`.
- **Нема** → пропозиції карток:
  - `+multi-resource-quota` «Квота кількох видів ресурсів» · game-logic/win · 🌱 · слот {kinds: {name: n}} — дитина `collect-quota`.
  - `+quiz-between-levels` «Вікторина між рівнями» · interface/menus · 📎 · слоти {questions_per_round, reward, penalty: none|life}.
  - `+engine-reskin` «Рескін: та сама механіка, інша тема» · code/architecture · 📎 — тема (спрайти, назви, тексти) як дані поверх двіжка.

## Пропозиції до словників
- `+window:quiz-window` — вікно питання з варіантами відповіді (між рівнями; у Pokémon — ворота-вікторина на полі).
- `+feature:quiz-between-levels` — вікторина як частина прогресії (бонус за правильні відповіді, без блокування).
- `+card:multi-resource-quota`, `+card:quiz-between-levels`, `+card:engine-reskin` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Joshua & the Battle of Jericho](https://en.wikipedia.org/wiki/Joshua_%26_the_Battle_of_Jericho) — шофар і «toots», руйнування стін і тематичних плиток, приховані предмети, вороги, квота металів, 5 «Joshua questions», вікторина з Біблією-нагородою, паролі, 100 рівнів / 100 вікторин / 10 бонусних, 2 гравці по черзі, лінія Crystal Mines → Exodus.
- [Wikipedia: Exodus](https://en.wikipedia.org/wiki/Exodus:_Journey_to_the_Promised_Land) — двіжок Crystal Mines, постріли «W», манна і 5 знаків питання, вікторина дає життя, Joshua — «трохи покращена графіка й геймплей».
- [Lutris](https://lutris.net/games/joshua-and-the-battle-of-jericho/) — мішки в лабіринті, стрільба по ворогах і перешкодах, питання між рівнями.

## Непевне
- (?) Чи падають валуни й кристали-метали, як у Crystal Mines, — джерела про Joshua гравітацію не згадують; мануалу (nesworld) не відкрив (403).
- (?) Друга кнопка, кількість життів, що саме дають Біблії, чи блокує вихід при неповній квоті — не перевірено.
- (?) Кількість варіантів відповіді у вікторині й ритм бонусних етапів.
- (?) Поведінка ворогів (погоня/патруль), роль мешканців і кіз, міцність Валаама.
