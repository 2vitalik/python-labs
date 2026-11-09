---
title: Gabbuchi
slug: gabbuchi
aka: [ガブッチ, Габуччі]
family: grid-platformer
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 2019
platforms: [Switch, PC (Steam), PS4]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/%E3%82%AC%E3%83%96%E3%83%83%E3%83%81", best: true, note: "базові правила: білий/червоний колір тіла, свій колір їсть, чужий — опора, шов, стрибок 2,5 зросту, 3 серця ситості, Perfect, 180 = 15×12, редактор"}
  - {kind: steam, url: "https://store.steampowered.com/app/1069970/Gabbuchi/", note: "180 стадій, редактор рівнів, досягнення, Steam Cloud"}
  - {kind: official, url: "https://www.aksysgames.com/gabbuchi/", note: "сторінка видавця Aksys: їсти необовʼязково, переїв — не дістанешся печива"}
  - {kind: other, url: "https://www.nintendo.com/en-gb/Games/Nintendo-Switch-download-software/Gabbuchi-1501435.html", note: "eShop: опис механіки, 1 гравець, демо"}
  - {kind: other, url: "https://midlifegamergeek.com/2019/06/13/gabbuchi-switch", note: "рецензія: L/R міняє колір, падіння з рівня = провал, швидкий рестарт, досягнення за ліміт змін"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Gabbuchi+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-by-input, gravity-fall, destructible-blocks, key-and-door, touch-death, environment-death, restart-level, sequential-levels, level-unlock, in-game-editor, editor-palette, game-screen, +eat-own-color, +color-switch-body, +seam-support, +appear-after-pass, +perfect-rating, +jump-fixed-height]
proposes: ["+cond:on_seam", "+effect:eat", "+ui:satisfaction-hearts", "+ui:color-change-counter", "+card:eat-own-color", "+card:color-switch-body", "+card:seam-support", "+card:appear-after-pass"]
author: opus
date: 2026-11-09
---

# Gabbuchi — квадратний обжера міняє колір тіла: блоки свого кольору зʼїдає, чужі — підлога під ногами

## Суть
Одноекранний пазл-платформер від H.A.N.D.: Габуччі має дістатися до печива-сердечка на кожній стадії. Тіло буває білим або червоним; торкнувшись блока свого кольору, він його **зʼїдає** (блок зникає), блок іншого кольору — тверда **опора**. Отже, перемикання кольору — це перемикання «що на полі тверде, а що прохідне-їстівне», і помилка у виборі, що зʼїсти, позбавляє шляху до печива. Додаткова мета — Perfect: змін кольору не більше за норму й повна ситість.

## Поле і час
- Поле — сітка квадратних блоків білого й червоного кольору плюс чорні «їжа»-предмети; одна стадія — один екран (рецензія Midlife Gamer Geek).
- Вигляд збоку, гравітація; Габуччі стрибає на висоту 2,5 власного зросту (JA-вікі).
- Real-time: стрибки й рухомі вороги частини стадій; рецензія відзначає стадії, де колір треба перемкнути вчасно.
- Межа поля відкрита: випасти за низ рівня — провал спроби.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Габуччі | player | колір: білий / червоний; ситість 0–3 | ходить, стрибає (2,5 зросту); перемикає колір; зʼїдає блок свого кольору при дотику |
| Білий блок | tile | колір | їстівний для білого Габуччі, опора для червоного |
| Червоний блок | tile | колір | їстівний для червоного, опора для білого |
| Шов між білим і червоним | terrain | — | на ньому можна стояти за будь-якого кольору тіла |
| Чорна їжа | pickup | — | зʼїдається, додає ситості |
| Печиво-сердечко | pickup | — | мета стадії: зʼїв — стадію пройдено |
| Ключ | pickup | — | узяв — зникають повʼязані блоки |
| Блок, що зникає від ключа | gate | — | тверда перешкода до взяття ключа |
| Блок, що зʼявляється | terrain | порожній / твердий | зʼявляється, коли Габуччі пройде повз |
| Ворог | enemy | — | рухається по стадії (лише частина стадій) |
| Шипи | hazard | лише редактор | у кампанії нема |
| Ворог, що ходить вгору-вниз | enemy | лише редактор | у кампанії нема |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(L|R)` → ТО `set_state(gabbuchi, color, white↔red)`, `counter(color_changes, +1)`.
- КОЛИ `contact(gabbuchi, block)` → ЯКЩО `same(gabbuchi, block, color)` → ТО `disappear(block)`, `counter(satisfaction, +1)` — зʼїв.
- КОЛИ `contact(gabbuchi, block)` → ЯКЩО `not same(gabbuchi, block, color)` → ТО `block` — блок тримає й зупиняє.
- КОЛИ `tick` → ЯКЩО `custom: «Габуччі на шві білого й червоного блоків»` → ТО `custom: «шов тримає за будь-якого кольору»`.
- КОЛИ `tick` → ЯКЩО `not supported(gabbuchi)` → ТО `fall(gabbuchi)`.
- КОЛИ `input(jump)` → ЯКЩО `supported(gabbuchi)` → ТО `custom: «стрибок до 2,5 зросту»`.
- КОЛИ `contact(gabbuchi, food)` → ТО `disappear(food)`, `counter(satisfaction, +1)`.
- КОЛИ `picked(gabbuchi, key)` → ТО `disappear(key_blocks)`.
- КОЛИ `leave(gabbuchi, appear_block)` → ТО `set_cell(appear_block, solid)` — прохід за спиною закривається.
- КОЛИ `contact(gabbuchi, enemy)` → ТО `restart` (?).
- КОЛИ `edge(gabbuchi)` (випав за низ) → ТО `restart`.
- КОЛИ `contact(gabbuchi, heart_cookie)` → ТО `win`, `next_level`.
- КОЛИ `contact(gabbuchi, heart_cookie)` → ЯКЩО `counter(color_changes, <=, quota)` and `counter(satisfaction, ==, 3)` → ТО `custom: «оцінка Perfect»`.
- Перемога: зʼїдено печиво. · Поразка: падіння з рівня (і, ймовірно, дотик ворога) → миттєвий рестарт. · Рахунку нема; якість — Perfect.

## Керування і ввід
- Рух ліворуч/праворуч і стрибок; L або R — перемкнути колір (рецензія Midlife Gamer Geek).
- Їсти окремою кнопкою не треба: досить торкнутися блока свого кольору.
- Рецензії скаржаться на «плавучий» стрибок — точність руху частина складності.

## Вікна, меню, HUD
- `game-screen`: стадія; HUD — три серця ситості в лівому верхньому куті (JA-вікі); лічильник змін кольору (?).
- `level-select` / `puzzle-select`: 15 світів по 12 стадій; світи відкриваються за кількістю пройдених стадій.
- `editor-window` («Стадію створити»): розстановка Габуччі й обʼєктів, у тому числі шипів і вертикального ворога.
- `main-menu` (?): кампанія · редактор · налаштування.
- Переходи: main-menu → вибір світу/стадії → game-screen → (печиво) наступна стадія / вибір.

## Фічі поза полем
- `levels-sequential` + `level-unlock`: 180 стадій у 15 світах по 12; спочатку лише світ 1.
- `level-editor` з двома ексклюзивними елементами (шипи, вертикальний ворог); чи можна ділитися рівнями — (?).
- `stars-rating`-подібна оцінка Perfect і `achievements` (Steam; рецензія — досягнення за обмежену кількість змін кольору й повну ситість).
- `restart-level` миттєвий; `cloud-save` (Switch, Steam); `localization` — 13 мов у Steam.

## Варіації й родичі
- Родичі в корпусі: [Boxboy](boxboy.md) (свої блоки як інструмент), [Solomon's Key](solomons-key.md) і [Wrecking Crew](wrecking-crew.md) (створити/зруйнувати блок), [Toki Tori](toki-tori.md) (одноекранні пазли з обмеженими засобами).
- Ширше: ігри «полярності кольору» (Ikaruga — поглинання кулі свого кольору) і фазові платформери, де зміна кольору робить блоки прохідними (Hue) (?).
- Осі варіацій:
  - **що робить свій колір**: зʼїдає назавжди (Gabbuchi) / пропускає тимчасово, доки колір той самий (фазові платформери) / вбиває;
  - **ціна зміни кольору**: безкоштовно, але з нормою для Perfect (Gabbuchi) / жорсткий ліміт / таймер;
  - **ресурс поїдання**: ситість як бонус-ціль (Gabbuchi) / голод як таймер / місткість.

## Цікавинки для курсу
- Колір тіла = маска твердості: ті самі клітини для одного стану тверді, для іншого — їстівні — 🥉 (колізія залежить від стану аватара).
- Шов двох кольорів як опора за будь-якого стану — 📎 (перевірка двох клітин під ногами).
- Поїдання як незворотна зміна поля: зʼїв зайве — рівень нерозвʼязний — 📎 (+ детектор глухого кута — 🥇).
- Блок, що зʼявляється за спиною, і блоки, що зникають від ключа — 🌱 кожен.
- Оцінка Perfect: норма змін кольору + повна ситість — 🌱.
- Редактор стадій з палітрою обʼєктів — 🥈.

## Мапа на каталог
- Є: `move-by-input` · `gravity-fall` · `destructible-blocks` (зʼїдений блок) · `key-and-door` (ключ прибирає блоки) · `touch-death` (ворог, ?) · `environment-death` (випав за низ) · `restart-level` · `sequential-levels` · `level-unlock` · `in-game-editor` + `editor-palette` (вільна розстановка обʼєктів) · `game-screen`.
- **Нема** → пропозиції карток:
  - `+eat-own-color` «Аватар зʼїдає клітини свого кольору, чужі — опора» · entities/interact · 🥉 · слоти {colors: 2}.
  - `+color-switch-body` «Аватар перемикає власний колір кнопкою» · entities/state · 🌱 · слот {count_limit}.
  - `+seam-support` «Межа двох різних клітин тримає за будь-якого стану» · entities/legality · 📎.
  - `+appear-after-pass` «Клітина стає твердою, коли аватар пройшов» · entities/interact · 🌱.
  - `+perfect-rating` (є в корпусі) · `+jump-fixed-height` (є в корпусі) — 2,5 зросту.

## Пропозиції до словників
- `+cond:on_seam` — аватар стоїть на межі двох клітин різного типу (шов Gabbuchi).
- `+effect:eat` — аватар поглинає клітину чи предмет із приростом лічильника (відрізняти від `pickup` в інвентар і `disappear` без наслідку).
- `+ui:satisfaction-hearts` — серця ситості, що заповнюються поїданням.
- `+ui:color-change-counter` — лічильник змін стану проти норми (?).
- `+card:eat-own-color`, `+card:color-switch-body`, `+card:seam-support`, `+card:appear-after-pass` — див. вище.

## Джерела
- ⭐ [Wikipedia JA: ガブッチ](https://ja.wikipedia.org/wiki/%E3%82%AC%E3%83%96%E3%83%83%E3%83%81) — колір тіла білий/червоний, свій колір їсть, чужий — опора, шов, стрибок 2,5 зросту, 3 серця ситості, Perfect (норма змін кольору + повна ситість), вороги, ключ-блоки, блоки, що зʼявляються, 180 стадій = 15×12 з відкриттям світів, редактор з шипами й вертикальним ворогом, дати й платформи.
- [Steam: Gabbuchi](https://store.steampowered.com/app/1069970/Gabbuchi/) — 180 стадій, редактор, досягнення, Steam Cloud, 13 мов.
- [Aksys: Gabbuchi](https://www.aksysgames.com/gabbuchi/) — їсти необовʼязково, блок можна лишити як опору; переїсти — значить не дістатися печива.
- [Nintendo eShop (UK)](https://www.nintendo.com/en-gb/Games/Nintendo-Switch-download-software/Gabbuchi-1501435.html) — опис механіки, 1 гравець, демо, хмарні сейви.
- [Midlife Gamer Geek: рецензія](https://midlifegamergeek.com/2019/06/13/gabbuchi-switch) — L/R міняє колір, один екран, падіння з рівня = провал, швидкий рестарт, досягнення.
- YouTube: пошук «Gabbuchi gameplay».

## Непевне
- (?) Норма змін кольору — число на стадію невідоме; жорсткого ліміту нема (рецензія: обмеження лише для досягнення), тож «ліміт змін кольору» з черги — це норма Perfect, а не правило поразки.
- (?) Чи падають блоки, коли під ними зʼїли опору, і чи зʼїдає Габуччі блок свого кольору, стоячи на ньому згори.
- (?) Що буває від дотику ворога (рестарт чи інше); чи є лічильник змін кольору в HUD.
- (?) Фраза Aksys/eShop «переїв — не дістанеться печива» прочитана як «зʼїв потрібну опору»; можлива і інша механіка (обмежена місткість) — не перевірено.
- (?) Чи можна ділитися рівнями з редактора; склад головного меню.
