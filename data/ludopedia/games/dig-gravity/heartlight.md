---
title: Heartlight
slug: heartlight
family: dig-gravity
also: [thinky]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 1990
platforms: [Atari 8-bit, MS-DOS, Amiga, Android, iOS, web]
links:
  - {kind: play, url: "https://www.classicdosgames.com/game/Heartlight.html", best: true, note: "опис, вільне завантаження (CC BY-SA 2.5) і запуск у браузері"}
  - {kind: play, url: "https://www.classicdosgames.com/online/hl.html", note: "грати Heartlight PC онлайн"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Heartlight_(video_game)", note: "поле 12×20, без часу й лімиту життів, версії"}
  - {kind: wiki, url: "https://pl.wikipedia.org/wiki/Heartlight", note: "сюжет, пропуск рівнів, ESC при глухому куті, кількість рівнів"}
  - {kind: other, url: "https://www.classicdosgames.com/files/games/chaosworks/hl.zip", note: "архів: README.TXT і LEVELS.HL — текстовий формат рівнів із легендою"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Heartlight+game+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [move-4dir, gravity-fall, push-object, collect-all, reach-exit, touch-death, environment-death, chain-detonation, impassable-cells, level-from-txt, map-validation, level-select, save-progress, music-toggle, goal-counter, +dig-terrain, +roll-off-rounded, +explode-3x3, +buoyant-rise, +one-way-tunnel, +free-level-order, +manual-restart]
proposes: ["+effect:fall", "+effect:rise", "+effect:explode", "+trigger:smashed", "+trigger:enter", "+cond:free", "+role:hazard", "+card:buoyant-rise", "+card:one-way-tunnel", "+card:free-level-order", "+card:manual-restart", "+feature:profile-slots"]
author: opus
date: 2026-11-02
---

# Heartlight — Boulder Dash без часу, де повітряні кулі падають угору

## Суть
Гном Персиваль копає траву, збирає всі серця на рівні й іде до дверей, які відчиняються лише після останнього серця. Знайома фізика rocks-and-diamonds (падають камені, серця й бомби; вибух руйнує цеглу) з одним інверсним елементом: **повітряна куля рухається вгору**, тобто має гравітацію з протилежним знаком. Часу й ліміту життів нема — це логічна головоломка, а не аркада: застряг — ESC, рівень з початку.

## Поле і час
- Поле 20×12 клітин, увесь рівень на одному екрані без скролу.
- Один шар: у клітині один із 13 символів текстової карти (див. «Сутності»).
- Real-time: падіння і підйом відбуваються тіками; таймера рівня нема.
- Рівень задається текстом у `LEVELS.HL`: 12 рядків по 20 символів між `{` і `}`, перед ним — `author:`.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гном `*` | player | безліч життів | рух 4 напрямки; копає траву; штовхає деякі обʼєкти, якщо за ними порожньо |
| Порожнеча ` ` | terrain | — | сюди падають і піднімаються обʼєкти |
| Трава `.` | terrain | diggable | гном проходить → порожнеча; тримає обʼєкти на місці |
| Серце `$` | pickup | falling | падає як камінь і може вбити гнома; збір +1 до лічильника |
| Камінь `@` | object | falling, pushable | падає, скочується (?); давить гнома, підриває бомби |
| Бомба `&` | object | falling, pushable (?) | вибухає, коли її розчавити або коли вона впаде на тверде; вибух руйнує цеглу (?) |
| Повітряна куля `0` | object | buoyant | піднімається, доки над нею порожньо; гном може штовхати (?) |
| Плазма `=` | hazard | — | смертельна/поглинає (?) — у файлі рівнів лише назва |
| Цегляна стіна `#` | static | destructible | непрохідна; вибух руйнує |
| Металева стіна `%` | static | indestructible | рамка рівня; вибух не бере |
| Тунель `<` / `>` | static | напрямок | прохід крізь стіну лише в один бік (?) |
| Двері-вихід `!` | gate | треба всі серця | відчиняються після збору квоти; знищені вибухом → рівень непрохідний |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `cell(target, grass)` → ТО `move`, `set_cell(empty)`; ЯКЩО `cell(target, empty)` → `move`.
- КОЛИ `contact(dwarf, rock|bomb|balloon)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `contact(dwarf, heart)` → ТО `pickup`, `counter(hearts, +1)`.
- КОЛИ `tick` → ЯКЩО `free(below)` → ТО `fall(rock|heart|bomb)`.
- КОЛИ `tick` → ЯКЩО `free(above)` → ТО `rise(balloon)` — дзеркальне падіння.
- КОЛИ `contact(falling rock|heart, dwarf)` → ТО `lose`.
- КОЛИ `smashed(bomb)` або `custom: «бомба впала на тверде»` → ТО `explode(3×3)` (?) радіус; цегла, трава, двері в зоні → `set_cell(empty)`; метал лишається; сусідні бомби — `chain-detonation`.
- КОЛИ `enter(dwarf, tunnel[dir])` → ЯКЩО `moving(dwarf, dir)` → ТО `custom: «пройти на клітину за тунелем»`; інакше `block` (?).
- КОЛИ `contact(dwarf, plasma)` → ТО `lose` (?).
- КОЛИ `counter(hearts, ==, total)` → ТО `set_state(exit, open)`; КОЛИ `contact(dwarf, exit)` → ЯКЩО відкрито → ТО `win`, рівень зараховано в слот гравця.
- КОЛИ `input(esc)` → ТО `restart` (вихід із глухого кута: засипало, двері знищено).
- Перемога: усі серця + вихід. Поразка: розчавлення/вибух → рівень знову, без втрати прогресу. Рахунок: кількість пройдених рівнів у слоті гравця.

## Керування і ввід
- Стрілки — рух гнома; Space на титулі — старт.
- Space + ←/→ — попередній/наступний рівень (рівні можна проходити в будь-якому порядку).
- ESC — рестарт рівня; F10 — на титул; Alt-X — вихід у DOS; F6 — музика; F7 — звуки.
- Enter на титулі — вибір слота гравця і зміна імені.

## Вікна, меню, HUD
- `splash-screen` / `main-menu`: титул; Space — грати; Enter — `profile-window` (3 слоти з іменами й лічильником пройдених рівнів).
- `game-screen`: поле 20×12 + нижній рядок: `remaining-counter` / `progress-bar` «потрібно сердець / зібрано», `level-number`.
- `level-select` вбудований у гру (Space+стрілки), без окремого екрана.
- Переходи: титул → рівень → (вихід) → наступний; ESC → той самий рівень; F10 → титул.

## Фічі поза полем
- `free-level-order` — рівні в будь-якому порядку; гра пройдена, коли пройдені всі.
- `save-progress` у 3 іменованих слотах (кількість пройдених рівнів).
- `level-editor` у вигляді **текстового файла**: `LEVELS.HL` редагується блокнотом; на старті гра валідує файл («No hero on level», «No exit on level», «Invalid object», «Not enough lines», «Too many levels»).
- `music-toggle`, `sound-toggle`.
- 20 рівнів у shareware, 60/70 у повних версіях; з 2006 — вільна гра CC BY-SA 2.5.

## Варіації й родичі
- Heartlight (Atari 8-bit, Польща, Janusz Pelc) → Heartlight PC (Xland / Epic MegaGames, 1994, у складі Epic Puzzle Pack) → Amiga (1993), Android/iOS (2012), браузерний ремейк (2020).
- Родичі: Boulder Dash, Supaplex, Emerald Mine (балони/вітер в EMC — інша ідея: дрейф за вітром, а не підйом).
- **Осі варіацій**: напрям гравітації обʼєкта — «вниз (камінь) / вгору (куля) / за вітром (EMC) / перемикач для гравця (Supaplex)»; тиск часу — «таймер (BD) / нема, лише логіка (Heartlight)»; ціна помилки — «життя / безкінечні спроби + ESC».

## Цікавинки для курсу
- Повітряна куля: той самий код падіння з параметром напрямку — 🌱, але красивий доказ, що «гравітація» — властивість елемента.
- Рівень як txt-файл з легендою символів і валідацією («нема героя / виходу / невідомий символ») — 🥉: парсер + зрозумілі помилки.
- Вільний порядок рівнів + слоти гравців — 📎.
- Тунель-клапан: прохід крізь стіну лише в один бік — 📎.
- Вибух, що може зробити рівень нерозвʼязним (знищені двері), і ручний рестарт замість детектора — 🌱; детектор «двері знищено → рестарт» — 📎.

## Мапа на каталог
- Є: `move-4dir` · `gravity-fall` · `push-object` · `collect-all` (серця) · `reach-exit` · `touch-death` · `environment-death` (камінь, вибух) · `chain-detonation` · `impassable-cells` · `level-from-txt` (LEVELS.HL) · `map-validation` (повідомлення про битий файл) · `level-select` (Space+стрілки) · `save-progress` (слоти) · `music-toggle` · `goal-counter`.
- **Нема** → пропозиції карток:
  - `+buoyant-rise` «Обʼєкт падає вгору» · entities/move · 🌱 · слот {dir: up} — дитина `gravity-fall`.
  - `+one-way-tunnel` «Односторонній прохід крізь стіну» · entities/legality · 📎 · слот {dir} — споріднено з `+one-way-port` (Supaplex).
  - `+free-level-order` «Рівні в будь-якому порядку» · levels/progression · 🌱.
  - `+manual-restart` «Рестарт з глухого кута» · game-logic/lose · 🌱.
  - `+dig-terrain`, `+roll-off-rounded`, `+explode-3x3` — повтори з Boulder Dash.

## Пропозиції до словників
- `+effect:fall` ⏳ і `+effect:rise` — підйом як дзеркало падіння (або `fall(a, dir)` з параметром — тоді `rise` не потрібен).
- `+effect:explode(area, into)` — повтор.
- `+trigger:smashed(a)` — повтор з Rocks'n'Diamonds / Emerald Mine.
- `+trigger:enter` ⏳ — вхід у тунель.
- `+cond:free` ⏳ — порожньо над кулею / під каменем.
- `+role:hazard` ⏳ — плазма.
- `+feature:profile-slots` — кілька іменованих профілів з прогресом на титулі.

## Джерела
- ⭐ [Classic DOS Games: Heartlight PC](https://www.classicdosgames.com/game/Heartlight.html) — опис, вільне завантаження, гра онлайн.
- [Архів hl.zip](https://www.classicdosgames.com/files/games/chaosworks/hl.zip) — README.TXT (клавіші, 3 слоти, безкінечні життя, вільний порядок рівнів) і LEVELS.HL (легенда 13 символів, поле 20×12).
- [Wikipedia EN](https://en.wikipedia.org/wiki/Heartlight_(video_game)) — серця падають і вбивають, бомби вибухають від удару, без часу; версії й ліцензія.
- [Wikipedia PL](https://pl.wikipedia.org/wiki/Heartlight) — сюжет (Персиваль/Мосєк), ESC при глухому куті, знищені двері.
- YouTube: пошук «Heartlight game gameplay».

## Непевне
- (?) Поведінка плазми (`=`): смертельна для гнома чи поглинає обʼєкти — у джерелах лише назва.
- (?) Тунелі `<` `>`: переносять крізь стіну чи працюють як односторонній порт; PL-вікі згадує «телепортацію без шляху назад».
- (?) Чи піднімає куля обʼєкт, що лежить на ній; чи можна штовхати кулю й бомбу.
- (?) Радіус вибуху бомби (3×3?) і чи руйнує він траву.
- (?) Рік Atari-версії: EN-вікі 1990, PL-вікі 1991; кількість рівнів: 60 (Classic DOS Games, PL) vs 70 (README, Deluxe).
- (?) Чи скочуються камені й серця з круглих обʼєктів (як у BD).
