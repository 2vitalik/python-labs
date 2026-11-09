---
title: TZAAR
slug: tzaar
aka: [Тзаар, Цаар]
family: chess-abstract
also: []
klass: figure
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: full
  random: setup
  goal: state
year: 2007
platforms: [board, web]
links:
  - {kind: other, url: "https://www.gipf.com/tzaar/rules/rules.html", best: true, note: "офіційні правила: 30 фішок трьох типів, випадковий / фіксований / турнірний старт, хід = обовʼязкове взяття + друга дія, висота вирішує взяття, кінець гри"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/TZAAR", note: "60 точок без центру, схема фіксованого старту кільцями, 2007/2008, сьома гра GIPF Project замість TAMSK, Game of the Year 2009"}
  - {kind: play, url: "https://www.boardspace.net/english/about_tzaar.html", note: "BoardSpace: онлайн, робот для новачків, рейтинг і архів партій"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=TZAAR+board+game+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 70
mechanics: [piece-move-patterns, piece-capture, legal-move-highlight, selection-highlight, last-move-highlight, hover-highlight, cell-click, drag-drop-piece, mode-indicator, hot-seat, turn-enforcement, move-timer, ai-opponent, ai-minimax, online-multiplayer, rating-system, move-notation, replay, match-setup, game-screen, main-menu, end-screen, help-window, settings-window, state-as-data, unit-tests, +hex-grid-render, +random-setup, +setup-presets, +placement-phase, +forced-capture, +two-phase-turn, +first-turn-exception, +piece-stacking, +stack-height-capture, +lose-piece-type, +no-capture-lose]
proposes: ["+cond:can_capture", "+cond:stack_height", "+effect:capture", "+effect:stack_onto", "+trigger:type_extinct", "+ui:stack-height-label", "+ui:type-counter", "+feature:setup-presets", "+card:stack-height-capture", "+card:lose-piece-type", "+card:no-capture-lose"]
author: opus
date: 2026-11-09
---

# TZAAR — щоходу спершу обовʼязково бʼєш, потім бʼєш ще раз або нарощуєш свій стос; втратив усі фішки одного типу — програв

## Суть
Поле заповнене повністю: 60 фішок двох кольорів, у кожного три типи — 6 Tzaar, 9 Tzarra, 15 Tott. Хід — дві дії: спершу **обовʼязкове взяття** (фішка або стос летить прямою до першої зайнятої точки й бʼє чужу ціль не вищу за себе), потім друге взяття, **нарощення** свого стосу або пас. Типи однаково сильні, сила — лише висота стосу; але програєш, коли зникли всі твої фішки хоч одного типу або нема чим бити на початку ходу. Ключове питання кожного ходу (з правил): «зробити себе сильнішим чи суперника слабшим?» — сьома гра GIPF Project Kris Burm.

## Поле і час
- Гексагон на трикутній сітці: фішки стоять на перетинах ліній, 60 точок, **центру нема** — і ходити через центр не можна. Точки утворюють 4 кільця навколо центру: 6 + 12 + 18 + 24 (за схемою фіксованого старту).
- Рух — по лініях сітки, 6 напрямків (`field: hex`).
- На старті зайняті всі 60 точок; кожен хід звільняє точку, а порожня точка лишається порожньою до кінця гри — поле лише рідшає.
- Покроково, двоє. Хід білих на старті — одна дія; далі кожен хід = 2 дії (`phase_start(capture)` → `phase_start(second)`). Партія ~30 хв.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Tzaar | piece | ×6 у кожного; колір | ходить і бʼє як усі; тип рахується для умови поразки |
| Tzarra | piece | ×9 у кожного | так само |
| Tott | piece | ×15 у кожного | так само |
| Стос | piece | висота h ≥ 1; колір один; тип = верхня фішка | рухається й гине цілим; висота — його сила |
| Точка (intersection) | terrain | 60 | зайнята або порожня; порожня назавжди |
| Центр | static | — | точки нема; лінії через центр не проходять для руху |
| Взяті фішки | zone | — | вибули з гри; поза полем |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ЯКЩО `mode(random)` → ТО `custom: «усі 60 фішок розкладаються випадково, вільних точок нема; колір тягнуть жеребом, починають білі»` (`random: setup`).
- КОЛИ `game_start` → ЯКЩО `mode(fixed)` → ТО `custom: «кільця від центру: 6 Tott через одну, 12 Tzaar парами, 18 Tzarra трійками, 24 Tott четвірками»`.
- КОЛИ `game_start` → ЯКЩО `mode(tournament)` → ТО поле порожнє; `input(place, type, cell)` → ЯКЩО `free(cell)` → ТО `place(piece, cell)` по черзі, тип — будь-який, доки не поставлено все; далі звичайна гра.
- КОЛИ `turn_start(white)` → ЯКЩО `first_time` → ТО лише одна дія — взяття; на повному полі це завжди взяття сусідньої чорної фішки.
- КОЛИ `turn_start(side)` → ЯКЩО `not custom: «є хоч одне легальне взяття»` (`+cond:can_capture`) → ТО `lose`.
- КОЛИ `phase_start(capture)` → ТО `input(move, stack, dir)` мусить бути взяттям; `pass_turn` у цій фазі — `block`.
- КОЛИ `input(move, stack, dir)` → ТО `custom: «ціль — перша зайнята точка на прямій через порожні точки»`; зупинитись на порожній, перестрибнути фішку чи перетнути центр — `block`.
- КОЛИ `input(move, stack, target)` → ЯКЩО `occupied(target, enemy)` і `custom: «висота мого стосу ≥ висоти цілі»` (`+cond:stack_height`) → ТО `disappear(target)` (`+effect:capture`), `move(stack, target)`; інакше `block`.
- Тип не впливає на взяття: Tott бʼє Tzaar, якщо висоти рівні; одиночна фішка не бʼє стос висоти 2+.
- КОЛИ `phase_start(second)` → ТО `choose(capture | stack | pass)`.
- КОЛИ `input(move, stack, target)` → ЯКЩО `occupied(target, own)` і `phase_start(second)` → ТО `custom: «стос стає зверху свого: висота = сума, тип = нова верхня фішка»` (`+effect:stack_onto`; близько до `merge`); висота необмежена.
- КОЛИ `input(move, stack, target)` → ЯКЩО `occupied(target, own)` і `phase_start(capture)` → ТО `block` — нарощувати можна лише другою дією.
- КОЛИ `input(pass)` → ЯКЩО `phase_start(second)` → ТО `pass_turn`, `end_turn`.
- КОЛИ `after(move)` → ТО `custom: «точка, звідки пішов стос, порожня до кінця гри»`; ставити фішки на поле під час гри не можна.
- КОЛИ `custom: «у гравця не лишилось жодної одиночної фішки чи верху стосу якогось типу»` (`+trigger:type_extinct`) → ТО `lose`; фішки під верхом стосу не рахуються.
- Перемога: у суперника зник один з трьох типів (серед одиночних і верхів стосів) або на початку свого ходу він не має взяття · Поразка: дзеркально · Рахунок: нема; нічиї в правилах не згадано.

## Керування і ввід
- Настільна: взяти фішку / стос рукою і пересунути по лінії на ціль; взяту ціль зняти з дошки, свій стос поставити зверху свого.
- (цифрова версія) Клік по своєму стосу → підсвітка до 6 цілей (перші зайняті точки по лініях): червоним — можливі взяття, іншим кольором — нарощення (лише в другій дії); клік по цілі — хід. Кнопка «Пас» активна лише в другій дії.
- Індикатор фази (`mode-indicator`): «Взяття (обовʼязково)» / «Друга дія».

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Грати → `match-setup` (людина / робот, годинник, старт: випадковий / фіксований / турнірний) · Правила → `help-window` · `settings-window`.
- `game-screen`: гекс-поле з порожнім центром; `stack-height-label` на кожному стосі; `type-counter` — скільки видимих Tzaar / Tzarra / Tott лишилось у кожного (головний індикатор небезпеки); `turn-indicator` + фаза; `legal-move-highlight`; `last-move-highlight` (обидві дії ходу); `captured-pieces`; `player-clock`; `move-list`.
- `lobby-window` і рейтинг — BoardSpace.
- `end-screen`: причина — «зник тип» або «нема взяття»; реванш.
- Переходи: main-menu → match-setup → game-screen → end-screen.

## Фічі поза полем
- `online-multiplayer`, `ai-opponent-levels` (BoardSpace: «робот достатньо сильний для новачків»), рейтинг і архів партій (`replay`).
- `setup-presets`: три стартові режими — випадковий (базовий), фіксований (кільця), турнірний (почергова розстановка з порожнього поля).
- `turn-timer` / годинник — у цифровій версії (?).

## Варіації й родичі
- Старти: **випадковий** (за замовчуванням) · **фіксований** · **турнірний** (`placement-phase` як у [dvonn](dvonn.md)).
- Серія GIPF Project (Kris Burm): [gipf](gipf.md), [dvonn](dvonn.md) (стоси, що летять на висоту, і чий верх — того стос), [yinsh](yinsh.md), [zertz](zertz.md), [tamsk](tamsk.md) — TZAAR замінив TAMSK у серії; PÜNCT, LYNGK.
- Інші родичі: [lasca](lasca.md) і стоси в [checkers-variants](checkers-variants.md) (стос-колона з полоненими — тут стоси одноколірні), сила за рангом у [jungle](jungle.md) і [banqi](banqi.md) (тут «ранг» — динамічна висота), примусове взяття — [checkers](checkers.md).
- **Осі варіацій**: сила (тип фігури / висота стосу) · стоси (одноколірні — TZAAR / змішані — DVONN, Lasca) · поразка (король / будь-який тип вимер / нема ходу) · старт (повне поле випадково / порожнє з розстановкою).

## Цікавинки для курсу
- Генератор ходів «до першої зайнятої точки» в 6 напрямках на гекс-сітці без центру — 📎.
- Стос як `(колір, висота, верхній тип)`; взяття за висотою, нарощення = додавання висот — 🌱.
- Хід із двох фаз з обовʼязковим взяттям, винятком першого ходу і пасом лише в другій фазі — 📎.
- Перевірка поразки «вимер тип» по видимих фішках (верх стосу) + «нема взяття на старті ходу» — 🌱.
- Випадкова розстановка 60 фішок і фіксована схема кільцями — 🌱.
- AI: minimax з оцінкою «баланс типів × висоти, загроза останній фішці типу»; гілкування велике на старті — 🥇.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ рух прямою до першої фішки · `piece-capture` ↔ взяття · `legal-move-highlight`, `selection-highlight`, `last-move-highlight`, `hover-highlight`, `cell-click`, `drag-drop-piece` · `mode-indicator` ↔ фаза ходу · `hot-seat`, `turn-enforcement`, `move-timer` · `ai-opponent`, `ai-minimax` · `online-multiplayer`, `rating-system` ↔ BoardSpace · `move-notation`, `replay` · `match-setup` · `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window` · `state-as-data`, `unit-tests`.
- **Нема** → пропозиції карток:
  - `+hex-grid-render` (див. [hex](hex.md)), `+random-setup` (див. [banqi](banqi.md)), `+placement-phase` (див. [dvonn](dvonn.md)), `+forced-capture` (див. [checkers](checkers.md)), `+two-phase-turn` і `+first-turn-exception` (див. [neutron](neutron.md)), `+piece-stacking` (див. [octi](octi.md)).
  - `+stack-height-capture` «Бити можна ціль не вищу за себе» · entities/legality · 🌱 · слоти {compare: ≥ | >}.
  - `+lose-piece-type` «Вимер один тип фігур — поразка» · game-logic/lose · 🌱 · слоти {count: visible | all}.
  - `+no-capture-lose` «Нема обовʼязкового взяття — поразка» · game-logic/lose · 🌱 — дзеркало `no-moves-left`.
  - `+setup-presets` «Кілька стартових розстановок» · game-logic/constraints · 🌱 · слоти {random, fixed, draft}.

## Пропозиції до словників
- `+cond:can_capture` — у сторони є хоч одне легальне взяття (TZAAR: інакше поразка; шашки).
- `+cond:stack_height` — порівняння висот стосів (TZAAR — бити не вищий; DVONN — дальність руху).
- `+effect:capture` — ціль знята з гри, нападник стає на її місце (шахове взяття одним словом).
- `+effect:stack_onto` — фішка/стос стає зверху іншого, висоти додаються (DVONN, TZAAR).
- `+trigger:type_extinct` — у гравця не лишилось (видимих) фігур одного типу.
- `+ui:stack-height-label` — число висоти на стосі; `+ui:type-counter` — лишок кожного типу в кожного гравця.
- `+feature:setup-presets` — вибір стартової розстановки.
- `+card:stack-height-capture`, `+card:lose-piece-type`, `+card:no-capture-lose` — див. «Мапа на каталог».

## Джерела
- ⭐ [gipf.com: TZAAR rules](https://www.gipf.com/tzaar/rules/rules.html) — 6/9/15 фішок, випадковий / фіксований / турнірний старт, хід білих з одного взяття, обовʼязкове взяття + (взяття | нарощення | пас), взяття за висотою, точки не заповнюються, дві умови перемоги.
- [Wikipedia: TZAAR](https://en.wikipedia.org/wiki/TZAAR) — 60 точок, центру нема, схема фіксованого старту кільцями, висота необмежена, стоси одноколірні, Kris Burm / SmartGames, 1000 підписаних копій на Spiel 2007, реліз 2008, Games Magazine Game of the Year 2009.
- [BoardSpace: about TZAAR](https://www.boardspace.net/english/about_tzaar.html) — коротко правила, робот «для новачків», рейтинг і архів.

## Непевне
- (?) Рік: передреліз на Spiel 2007, офіційний реліз 2008 — у шапці 2007.
- (?) Чи поразка настає, якщо гравець сам накрив свою останню фішку типу власним стосом: формула «рахуються лише верхи стосів» це означає, але офіційна сторінка каже «capturing all of one type».
- (?) Розмір гексагона «сторона 5 без центру» — висновок із кілець 6+12+18+24, прямо в джерелах не написано.
- (?) Функції цифрових версій (годинник, нотація, рівні робота) — бачив лише опис BoardSpace; окремі застосунки не перевіряв.
- (?) Нічия (повторення, взаємна неможливість) у правилах не згадана.
