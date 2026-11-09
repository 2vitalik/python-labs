---
title: Dungeon Raid
slug: dungeon-raid
aka: []
family: falling-match
also: [roguelike]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: runtime
  goal: survive
year: 2010
platforms: [iOS, Android]
links:
  - {kind: other, url: "https://www.pocketgamer.com/dungeon-raid/review/", best: true, note: "PocketGamer, огляд 2010: шлях з діагоналями, мечі проти черепів, зілля, щити, золото, рівні"}
  - {kind: other, url: "https://www.pocketgamer.com/articles/037786/r/", note: "PocketGamer: класи на старті, рандомні апгрейди, пермасмерть"}
  - {kind: other, url: "https://www.gamepressure.com/games/dungeon-raid/z142d7", note: "опис механіки, розробник Fireflame Games, дати iOS/Android"}
  - {kind: other, url: "https://toucharcade.com/community/threads/dungeon-raid-by-fireflame-games.73155/page-52", note: "форумний тред TouchArcade (стратегії, оновлення)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=dungeon+raid+ios+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [path-drawing, path-cut, move-8dir, hp-damage, gravity-fall, spawn-random-cell, in-round-upgrades, unit-xp-skills, round-currency, progress-acceleration, permadeath, character-select, achievements-window, score-records, combo-multiplier, +path-match-clear, +mixed-type-chain, +monster-tiles, +overflow-meters, +armor-absorb]
proposes: ["+cond:compatible", "+effect:armor", "+trigger:path_released", "+ui:meter-bars", "+window:skill-choice"]
author: opus
date: 2026-11-09
---

# Dungeon Raid — match-3 малюванням шляху; черепи на полі — монстри, мечі їх бʼють, після ходу монстри бʼють тебе

## Суть
Поле заповнене плитками п'яти видів: мечі, черепи-монстри, зілля, щити, золото. Хід — провести пальцем шлях через 3+ сусідні (з діагоналями) плитки одного виду; шлях може петляти. Мечі й черепи в'яжуться в один ланцюг: монстри в ньому отримують шкоду, що росте з кількістю мечів. Після кожного ходу живі монстри на полі атакують героя; броня поглинає частину шкоди. Це роглайт: пермасмерть, рівні героя, навички, крамниця — і нескінченний потік дедалі сильніших ворогів.

## Поле і час
- Квадратна сітка, 6×6 за фан-вікі (сніпет у пошуку); сусідство 8 (вертикаль, горизонталь, діагональ).
- Покроково, без таймера: хід = один намальований шлях; далі фаза ворогів, потім осідання й досипання плиток згори.
- Шари: поле плиток + HUD героя (HP, броня, смуги прогресу) над/під полем.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Меч | tile | — | у ланцюгу додає шкоду всім черепам ланцюга; зникає |
| Череп (монстр) | enemy | атака, HP, броня (?) | стоїть як плитка; після ходу гравця атакує героя; убитий у ланцюгу — зникає, дає досвід |
| Зілля | pickup | — | ланцюг відновлює HP героя |
| Щит | pickup | — | ланцюг відновлює броню; надлишок — у смугу апгрейду (?) |
| Золото | resource | — | ланцюг додає монети; повна смуга → крамниця |
| Бос / спецмонстр | boss | особливі здібності (?) | зʼявляється періодично (?) |
| Герой | player | HP, броня, зброя, клас, рівень | не на полі; його статистики визначають шкоду й захист |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag_path)` → ЯКЩО `custom: «наступна плитка сусідня (8) і ще не в шляху»` and `same(prev, next, kind)` or `custom: «меч ↔ череп»` → ТО `custom: «плитку додано до шляху»`; повернення пальцем назад скорочує шлях.
- КОЛИ `custom: «path_released»` → ЯКЩО `custom: «довжина шляху ≥ 3»` → ТО `clear(path)`; інакше `block` (хід не відбувся).
- КОЛИ `after(clear)` → ЯКЩО `custom: «у шляху є мечі й черепи»` → ТО `damage(n)` кожному черепу шляху, `n` росте з кількістю мечів і силою зброї; вижилий череп лишається на полі (?).
- КОЛИ `hp_zero(skull)` → ТО `disappear_b`, `counter(xp, +1)`.
- КОЛИ `after(clear)` → ЯКЩО `custom: «шлях із зілля»` → ТО `heal(hero, n)` за кількість зілля.
- КОЛИ `after(clear)` → ЯКЩО `custom: «шлях зі щитів»` → ТО `custom: «armor + n»`; надлишок понад максимум → `counter(upgrade, +n)` (?).
- КОЛИ `after(clear)` → ЯКЩО `custom: «шлях із золота»` → ТО `currency(+n)`, `counter(gold_bar, +n)`.
- КОЛИ `after(clear)` → ТО `fall(all_unsupported)`, `spawn_at(random_tile, top)` у порожні клітини.
- КОЛИ `turn_end(player)` → ТО кожен живий череп: `damage(attack)` герою; `custom: «спершу знімається броня, решта — HP»`.
- КОЛИ `counter(xp, >=, threshold)` → ТО `choose(skill)` — нова навичка або її рівень (рандомні варіанти).
- КОЛИ `counter(gold_bar, >=, threshold)` → ТО `window(shop-window)` → `choose(equipment)`.
- КОЛИ `counter(upgrade, >=, threshold)` → ТО `choose(upgrade)` спорядження (?).
- КОЛИ `input(skill_button)` → ЯКЩО `custom: «навичка не на перезарядці»` → ТО `custom: «ефект навички над полем»`, `custom: «cooldown N ходів»` (?).
- КОЛИ `custom: «минають ходи»` → ТО `custom: «нові монстри сильніші»` (вороги «покращуються з часом»).
- КОЛИ `hp_zero(hero)` → ТО `lose`; забіг втрачено разом з усіма речами (пермасмерть).
- Рахунок: (?) кількість пережитих ходів / убитих монстрів; мети нема — вижити якомога довше.

## Керування і ввід
- Тач: провести пальцем через ланцюг плиток, відпустити — хід; рух назад по шляху знімає останні плитки (як `path-cut`).
- Тап по іконці навички — застосувати (?).
- Попередній перегляд шкоди під час малювання шляху (?).

## Вікна, меню, HUD
- `main-menu`: Нова гра · Продовжити · досягнення · налаштування (?).
- `character-select` — клас героя (з v1.3 — 10 класів з уміннями, перками, вадами).
- `game-screen`: поле 6×6; HUD — `hp-bar`, `shield-bar` (броня), `custom: «три смуги-лічильники: досвід, золото, апгрейд»`, `turn-counter` (?), `skill-bar` з cooldown.
- `custom: «skill-choice»` — модал вибору навички при рівні; `shop-window` — вибір речі за золото; `upgrade-window` — апгрейд спорядження за щити.
- `end-screen` — смерть героя, підсумок забігу; `achievements-window` (75 досягнень з v1.3).
- Переходи: main-menu → character-select → game-screen ⇄ модали вибору → end-screen.

## Фічі поза полем
- `mode-endless` — єдиний описаний режим; `meta-progression` у вигляді відкриття класів (класи відкриваються поступово).
- `achievements`, `autosave` / `continue` забігу (?), `leaderboard-local` (?).
- `difficulty-presets` (?).

## Варіації й родичі
- Родичі в корпусі: Bejeweled / Candy Crush (свап замість шляху), Puzzle & Dragons (тягнення однієї кулі шляхом), Triple Town (злиття), Two Dots (шлях без діагоналей) — у черзі.
- Нащадки й клони: 10000000, You Must Build a Boat, Dungelot (?), Dungeon Raid-подібні «match-RPG».
- **Осі варіацій**: як формується збіг (свап / шлях / клік-група) · сусідство (4 / 8) · хто ворог (окремий бос поза полем / монстри як плитки) · змішування видів (лише однакові / меч+череп) · економіка (одна валюта / кілька смуг-переповнень).

## Цікавинки для курсу
- Малювання шляху по сітці з 8-сусідством, відкат назад, мін. довжина — 📎.
- Змішаний ланцюг «меч+череп»: таблиця сумісності видів — 🌱.
- Монстр як плитка поля зі статами й атакою після ходу — 🥉 (стан плитки + фаза ворогів).
- Три смуги-переповнення (досвід → навичка, золото → крамниця, щити → апгрейд) з модалами вибору — 🥉.
- Броня поверх HP і перезарядка навичок — 📎.
- Наростання сили ворогів з часом — 🌱.

## Мапа на каталог
- Є: `path-drawing` ↔ шлях пальцем · `path-cut` ↔ відкат шляху · `move-8dir` (сусідство з діагоналями) · `hp-damage` · `gravity-fall` + `spawn-random-cell` (досипання) · `in-round-upgrades` · `unit-xp-skills` (рівні героя) · `round-currency` · `progress-acceleration` · `permadeath` · `character-select` · `achievements-window` · `score-records` · `combo-multiplier` (довший ланцюг — сильніше).
- **Нема** → пропозиції карток:
  - `+path-match-clear` «Збіг шляхом через сусідні однакові» · entities/interact · 📎 · слоти {min: 3, adjacency: 4|8}.
  - `+mixed-type-chain` «Ланцюг з сумісних видів» · entities/legality · 🌱 · слоти {pairs}.
  - `+monster-tiles` «Вороги як плитки поля» · entities/combat · 🥉.
  - `+overflow-meters` «Смуги-переповнення відкривають вибір» · game-logic/economy · 📎.
  - `+armor-absorb` «Броня поглинає шкоду до HP» · entities/state · 🌱.

## Пропозиції до словників
- `+cond:compatible` — два види плиток можна в'язати в один ланцюг (меч ↔ череп).
- `+effect:armor` — ±броня, окремо від HP (поглинає шкоду першою).
- `+trigger:path_released` — гравець відпустив намальований шлях (кінець вводу drag-path).
- `+ui:meter-bars` — кілька смуг накопичення під HUD (досвід/золото/апгрейд).
- `+window:skill-choice` — модал вибору навички з рандомних варіантів при рівні.

## Джерела
- ⭐ [PocketGamer: Dungeon Raid review](https://www.pocketgamer.com/dungeon-raid/review/) — шлях з діагоналями, мечі/черепи/зілля/щити/золото, рівні, режим Endless.
- [PocketGamer: огляд 2012](https://www.pocketgamer.com/articles/037786/r/) — класи на старті, рандомні навички, пермасмерть.
- [Gamepressure](https://www.gamepressure.com/games/dungeon-raid/z142d7) — «gold buys equipment, shields upgrade it», досвід за ворогів, Fireflame Games, iOS 14.11.2010, Android 29.01.2012.
- [TouchArcade thread](https://toucharcade.com/community/threads/dungeon-raid-by-fireflame-games.73155/page-52) — обговорення гри (у пошуку; сторінку не відкрито).

## Непевне
- (?) Wikipedia-статті нема (⭐ з черги — 404); фан-вікі dungeonraid.fandom.com віддає 402. Розмір 6×6 — лише зі сніпета пошуку.
- (?) Рік: черга каже 2011, джерела — iOS 14.11.2010 (Firemint у черзі ≠ Fireflame Games у джерелах).
- (?) Стати черепа (атака/HP/броня на плитці), формула шкоди (зброя + за меч), чи бʼють усі черепи поля — з памʼяті.
- (?) Смуга апгрейду від надлишку щитів, пороги смуг, перезарядка навичок, боси й спецмонстри — не підтверджено.
- (?) Що саме є рахунком (ходи / вбивства) — не знайдено.
