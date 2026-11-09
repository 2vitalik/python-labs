---
title: Candle Prick
slug: candle-prick
aka: []
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2022
platforms: [PC, Linux, web (демо)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1920700/Candle_Prick/", best: true, note: "повна гра: 60+ рівнів, 15+ палітр, відгуки з описом механіки"}
  - {kind: itch, url: "https://moraguma.itch.io/candle-prick", note: "демо в браузері (Godot 3.4); теги 1-bit, Sokoban"}
  - {kind: play, url: "https://html-classic.itch.zone/html/6086068/index.html", note: "збірка демо (з неї прочитано скрипти Lance/Enemy/Player/Candle)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Candle+Prick+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-4dir, move-by-input, keyboard-controls, controls-remap, push-object, enemy-patrol, fill-hole, impassable-cells, undo-unlimited, restart-level, level-select, level-unlock, save-progress, theme-select, language-picker, volume-control, main-menu, pause-menu, event-effects, particles, movement-animation, sound-effects, +spear-grab, +impale-attach, +body-extension, +pull-out-spear, +stab-to-win, +count-based-unlock]
proposes: ["+card:impale-attach", "+card:spear-grab", "+feature:palette-unlock"]
author: opus
date: 2026-11-09
---

# Candle Prick — підніми спис, проколи ворога, і він стане частиною твого тіла; дотягнись списом до свічки

## Суть
Покрокова Sokoban-головоломка moraguma у 1-бітній піксельній графіці. Герой підбирає **спис**, просто наступивши на нього: спис стирчить з героя в бік руху. Проколотий списом ворог перестає ходити й рухається разом із героєм як **продовження тіла**. Проколоті вороги самі можуть підхоплювати інші списи, тож тіло росте ланцюгом. Мета рівня — проколоти **свічку**. Рецензенти порівнюють гру з «дитячою версією» Stephen's Sausage Roll: усе тримається на двох механіках, списах і ворогах.

## Поле і час
- Квадратна сітка; у демо рівень займає 15×9 клітин (константи `H_TILES`, `V_TILES`). Вид згори.
- Клітина — або підлога (4 типи плиток, ходити можна), або **порожнеча/яма** (ходити не можна). Порожнеча, у яку впав ворог, стає підлогою.
- Хід: крок гравця → обробка списів (висмикування, вислизання) → крок кожного живого ворога → падіння в ями → розворот заблокованих ворогів. Часу нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | `controlled` | рух 4 напрямки лише по підлозі; штовхає; підбирає спис наступом; проколотий → втрачає керування |
| Спис | object | `holder`, `aim`, `stabbing` | лежить; підібраний — стирчить з власника в бік `aim`; колє того, хто в клітині попереду; висмикується, якщо ціль відстала |
| Ворог | enemy | напрям UP/DOWN/LEFT/RIGHT/DEAD | щоходу крок у своєму напрямку; уперся — розвертається; не сходить у порожнечу сам; може тримати спис |
| Проколотий ворог | object | `movement_vector = 0` | стоїть; прикріплений до списа — рухається разом із тілом; може підхопити інший спис |
| Свічка | object | — | штовхається; проколота → рівень пройдено |
| Валун | static | — | нерухомий, не колеться, не підбирається |
| Порожнеча (яма) | terrain | — | непрохідна для героя; ворог, що опинився над нею не прикріпленим до героя, падає й заповнює її |
| Заповнена яма | terrain | — | звичайна підлога (з тілом ворога всередині) |

## Правила (КОЛИ → ЯКЩО → ТО)
Рух героя:
- КОЛИ `input(dir)` → ЯКЩО `custom: «наступна клітина — підлога, і кожен прикріплений елемент та все, що попереду, може зсунутися»` → ТО `move(player, dir)`, `push` ланцюгом, рух усіх прикріплених; інакше `block`, `sound(nope)` і струс камери.

Спис:
- КОЛИ `contact(player|enemy, spear)` → ЯКЩО `state(spear, lying)` → ТО `attach(spear, holder)`, спис зсувається на 1 вперед і дивиться в бік руху (`face(spear, dir)`); якщо там стоїть ворог або свічка — ця ціль одразу проколюється.
- КОЛИ `input(dir)` → ЯКЩО `facing(spear, dir)` і `occupied(cell_ahead, enemy|candle|player)` → ТО `attach(spear, target)` (спис входить у клітину цілі), `set_state(target, impaled)`.
- КОЛИ `input(dir)` → ЯКЩО `facing(spear, dir)` і `custom: «попереду ціль, яку не можна проколоти»` → ТО `push(target)`; не зсувається → `block`.
- КОЛИ `input(dir)` → ЯКЩО `custom: «рух перпендикулярно до списа»` → ТО спис зсувається вбік разом із власником і штовхає те, що поруч.
- КОЛИ `input(dir)` → ЯКЩО `facing(spear, opposite(dir))` і `custom: «проколота ціль не може рушити»` → ТО `detach(spear, target)` — спис висмикується, бризкає кров.
- КОЛИ `contact(enemy, spear_tip)` → ЯКЩО `facing(spear, toward(enemy))` → ТО ворог сам наштрикується: `attach(spear, enemy)`.
- КОЛИ `custom: «власник опинився далі ніж за 1 клітину від списа»` → ТО `detach(spear, holder)`, `sound(slip)` — спис падає.

Вороги:
- КОЛИ `turn_end(player)` → ЯКЩО `not state(enemy, impaled)` → ТО `move(enemy, own_dir)`, штовхаючи те, що попереду (зокрема героя).
- КОЛИ `blocked(enemy)` → ТО `face(enemy, reverse)` — патруль туди-сюди між перешкодами.
- КОЛИ `turn_end(player)` → ЯКЩО `cell(enemy, void)` і `custom: «його група не прикріплена до героя»` → ТО `fall(enemy)`, `set_cell(cell, floor)`; прикріплені до нього списи падають разом і теж стають частиною підлоги.

Перемога і поразка:
- КОЛИ `custom: «спис проколов свічку»` → ТО `win`, `next_level` з круговою «шторкою» від свічки; на час анімації undo вимкнено.
- КОЛИ `custom: «чужий спис проколов героя»` → ТО `set_state(player, uncontrolled)` — фактично `lose`; лишаються undo чи рестарт.
- КОЛИ `input(undo)` → ТО `undo(1)` (стек до 100 станів на кожен елемент). КОЛИ `input(restart)` → ТО `restart`.

## Керування і ввід
- Стрілки/WASD або геймпад (стіки й D-pad): крок. Окремі дії: undo, restart, menu. Усі клавіші перепризначаються окремо для клавіатури й геймпада.
- Атаки як окремої дії нема: проколювання — наслідок кроку в бік списа.

## Вікна, меню, HUD
- `splash-screen` (Intro): «Made by Moraguma», «In partnership with».
- `main-menu`: PLAY · LEVEL SELECT · OPTIONS · CREDITS · EXIT (у демо — DEMO / FULL GAME).
- `level-select`: кнопки рівнів (номери й літери); рівень відкривається, коли пройдено достатньо інших.
- `pause-menu` (клавіша menu): CONTINUE · RESTART · OPTIONS · MENU · QUIT.
- `settings-window`: GAME (LANGUAGE PT/EN, PALETTE) · VIDEO (FULLSCREEN, SCALE) · AUDIO (MASTER, MUSIC) · CONTROLS (переназначення, CLEAR, ACCEPT, BACK).
- `about-window` (CREDITS): автор, key art Jana Marcato, музика kenney.nl, SFX beepyeah, шрифт codeman38.
- `game-screen`: поле без HUD; струс камери, кров, анімації «killed», «dropped», «pop».
- Переходи: кругова «шторка» між сценами з центром на гравці або свічці.

## Фічі поза полем
- `undo` (до 100 кроків), `restart-level`.
- Прогресія з лічильником: рівень N відкритий, якщо `N − 1 ≤ total_levels_beaten`. «Спеціальні» рівні важать 2, тож відкривають більше.
- Палітри (15+ у повній грі): деякі рівні відкривають палітру (`unlock_palette`); вибір палітри будь-коли. Рецензенти: опційні цілі нагороджуються палітрами (`+feature:palette-unlock`).
- Збереження: пройдені рівні, палітри, налаштування в одному файлі.
- `localization` PT/EN, `remap-controls`, `fullscreen`, `window-size`, `volume-sliders`, `gamepad-support`.

## Варіації й родичі
- `games/thinky/stephens-sausage-roll.md` — головний родич: «виделка» героя там теж є продовженням тіла, а ковбаски наштрикуються. Тут наштрикуються вороги, що ще й ходять.
- `games/thinky/snakebird.md`, `games/thinky/lime-rick.md` — тіло, що росте; тут тіло збирається з чужих сутностей.
- `games/push-slide/kwirk.md` — засипання ями обʼєктом (`fill-hole`); тут яму засипає ворог.
- **Осі варіацій:** звʼязок частин — злипання (Sokobond) / прокол (тут) / черга (Snake); хто може тримати зброю — лише герой / будь-яка жива сутність; ціль — вихід / проколоти предмет / засипати ями.

## Цікавинки для курсу
- Граф прикріплень (спис ↔ власник ↔ проколота ціль) і рекурсивні `can_move` / `move` із множиною вже викликаних — 🥇 (класична задача складеного тіла без нескінченної рекурсії).
- Спис як напрямлений обʼєкт: вперед — колоти, вбік — штовхати, назад — висмикувати — 🥈.
- Патруль ворога з розворотом при упорі й заборона ступати в порожнечу — 📎.
- Ворог у порожнечі → підлога (яма засипана тілом) — 🌱.
- Відкриття рівнів за лічильником пройдених, де «спеціальні» важать 2 — 🌱.
- Палітра з чотирьох кольорів як тема плюс кругова шторка-перехід (шейдер) — 📎.

## Мапа на каталог
- Є: `move-4dir`, `move-by-input`, `keyboard-controls`, `controls-remap`; `push-object` ↔ свічка, вороги, ланцюги; `enemy-patrol` ↔ вороги туди-сюди; `fill-hole` ↔ ворог у порожнечі; `impassable-cells` ↔ валуни, порожнеча; `undo-unlimited`, `restart-level`; `level-select`, `level-unlock`, `save-progress`; `theme-select` ↔ палітри; `language-picker`, `volume-control`; `main-menu`, `pause-menu`; `event-effects`, `particles` (кров), `movement-animation`, `sound-effects`.
- **Нема** → пропозиції карток:
  - `+spear-grab` «Підібрати спис наступом, він стирчить у бік руху» · entities/interact · 📎.
  - `+impale-attach` «Проколота сутність стає частиною тіла» · entities/interact · 🥈 (родич `stick-together`).
  - `+body-extension` «Тіло з чужих сутностей» · entities/move · 🥈.
  - `+pull-out-spear` «Висмикнути спис рухом назад» · entities/interact · 📎.
  - `+stab-to-win` «Проколоти ціль = перемога» · game-logic/win · 🌱.
  - `+count-based-unlock` «Рівні відкриваються за кількістю пройдених» · levels/progression · 🌱.

## Пропозиції до словників
- `+card:impale-attach`, `+card:spear-grab` — див. «Мапа на каталог».
- `+feature:palette-unlock` — палітри кольорів як нагорода за рівні чи опційні цілі.

## Джерела
- ⭐ [Steam: Candle Prick](https://store.steampowered.com/app/1920700/Candle_Prick/) — опис («stabbing enemies and using them as extensions of yourself»), 60+ рівнів, 15+ палітр, реліз 3.11.2022; відгуки: «only 2 mechanics: spears and enemies», опційні цілі → палітри, регіони оверворлду.
- [itch.io: Candle Prick DEMO](https://moraguma.itch.io/candle-prick) — теги, Godot; коментарі (джемове походження, порівняння з SSR).
- [Збірка демо](https://html-classic.itch.zone/html/6086068/index.html) — розібрано `Lance.gd`, `Enemy.gd`, `Player.gd`, `Candle.gd`, `LevelBase.gd`, `Save.gd`, тексти меню й налаштувань.
- YouTube: пошук «Candle Prick gameplay».

## Непевне
- (?) Правила взято з демо-збірки (рівні 1–18, A–P, x-рівні). У повній грі можуть бути нові елементи; рецензент каже, що механік лише дві.
- (?) У рядку черги «гасити всі свічки»; у коді демо свічка на рівні одна, і перемогу дає перший прокол.
- (?) Як саме позначено опційну ціль рівня в повній грі — не перевірено.
- (?) Гілка `delance`, де спис без цілі відскакує від валуна праворуч, у коді виглядає як особливий випадок; поведінку грою не перевірено, тому в правила не внесено.
