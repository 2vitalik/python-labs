---
title: Ticket to Earth
slug: ticket-to-earth
aka: []
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: setup
  goal: state
year: 2017
platforms: [iOS, Android, PC, macOS]
links:
  - {kind: other, url: "https://www.pocketgamer.com/ticket-to-earth/ticket-to-earth-review-a-magnificent-puzzling-rpg-hybrid/", best: true, note: "огляд: шлях лише по одному кольору, 2 очки дії, довжина шляху = сила удару, 4 типи плиток"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Ticket_to_Earth", note: "коротка стаття: Robot Circus, епізоди, дати виходу, «рух по плитках однакового кольору заряджає вміння»"}
  - {kind: steam, url: "https://store.steampowered.com/app/636390/Ticket_to_Earth/", note: "ПК-версія 2017, уся сага, понад 100 полів бою"}
  - {kind: other, url: "https://www.hookedgamers.com/pc/ticket_to_earth/review/article-1831.html", note: "огляд ПК: Hand/Eye/Heart/Mind, шкали вмінь, Talent-токени, зброя за кредити"}
  - {kind: other, url: "https://gameranx.com/updates/id/128201/article/ticket-to-earth-impressions-an-original-demanding-sci-fi-statement/", note: "кольори плиток, Justice-токени за 8+ клітин, нема undo, режими місій"}
  - {kind: other, url: "https://www.imore.com/ticket-earth-review", note: "випадкова розкладка плиток, предмети з убитих ворогів, ChatLink між місіями"}
  - {kind: other, url: "https://www.digitallydownloaded.net/?p=44917", note: "вороги грають за тими самими правилами, хід із двох дій"}
  - {kind: other, url: "http://www.148apps.com/reviews/ticket-to-earth-episode-2-review/", note: "епізод 2: укриття, крафт, нові цілі місій, перенос прокачки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Ticket+to+Earth+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [path-drawing, hp-damage, ai-opponent, melee-vs-ranged, floor-types, cell-transform, drop-on-death, destroy-all-enemies, reinforcements, shop-between-levels, sequential-levels, level-select, tutorial-window, game-screen, end-screen, +color-path-move, +path-length-power, +charge-meter-special, +action-points, +screen-clear-special, +turn-limit-objectives, +talent-tokens, +cover-system, +crafting]
proposes: ["+cond:color", "+trigger:meter_full", "+ui:special-meter", "+window:chat-link", "+card:color-path-move"]
author: opus
date: 2026-11-09
---

# Ticket to Earth — покрокова тактика, де шлях можна прокласти лише по плитках одного кольору, а довжина шляху стає силою удару

## Суть
Покрокова тактична RPG від Robot Circus (Мельбурн) зі «зшитою» механікою match-пазла: поле бою — сітка кольорових плиток, і герой ходить **лише шляхом з плиток одного кольору**. Що довший пройдений одноколірний слід, то більше очок атаки на цей раунд і то повніше наповнюється шкала вміння цього кольору (Hand — ближній бій, Eye — дистанційний, Heart — здоровʼя, Mind — перефарбування плиток). Кожен персонаж має дві дії на хід, вороги ходять за тими самими правилами. Гра вийшла епізодами (сага з чотирьох частин), між місіями — прокачка талантів і купівля зброї.

## Поле і час
- Квадратна сітка в ізометричному вигляді; кожна клітина — плитка одного з **чотирьох кольорів** (типів), розкладених випадково на старті бою.
- Шари: плитка (колір) + юніти (герої, вороги) + предмети, що лишаються після вбитих ворогів; в епізоді 2 додано укриття.
- Хід: у кожного героя дві дії (рух, атака, вміння); потім ходять вороги. Чи плитки під пройденим шляхом змінюють колір після руху — (?).
- Темп повільний, без таймера; частина місій обмежена кількістю раундів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Rose | player | HP, зброя (меч), шкали 4 кольорів, 2 дії | ближній бій і трохи дистанційних умінь; рух одноколірним шляхом |
| Wolf | player | HP, зброя (пістолет/гвинтівка) | дистанційний боєць; ті самі правила руху |
| Інші герої (усього чотири в сазі; новий з епізоду 2) | player | клас, вміння | приєднуються з епізодами (?) |
| Плитка Hand (помаранчева) | terrain | колір | заряджає вміння ближнього бою |
| Плитка Eye (фіолетова) | terrain | колір | заряджає дистанційні вміння |
| Плитка Heart (рожева) | terrain | колір | заряджає вміння здоровʼя; талант автолікування діє лише на ній |
| Плитка Mind (зелена) | terrain | колір | заряджає вміння, що перефарбовують плитки |
| Ворог (роботи, мутанти, кримінал, тарган-мутанти) | enemy | HP, атака | ходить і бʼє за тими самими правилами; може зменшити очки атаки героя |
| Бос | boss | більше HP, сильніші атаки | як ворог, ціль окремих місій |
| Предмет з ворога | pickup | — | зʼявляється на полі після вбивства ворога |
| Укриття (епізод 2) | static | — | система укриттів, деталі (?) |
| Justice-токен | resource | лічильник | перевертається за кожен шлях з 8+ клітин; набір — вміння Justice |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag_path, hero)` → ЯКЩО `custom: «кожна наступна клітина сусідня з попередньою і того ж кольору, що й перша»` і `free(path)` → ТО `move(hero, path_end)`, `counter(actions, -1)`.
- КОЛИ `input(drag_path, hero)` → ЯКЩО `occupied(path, enemy)` → ТО `block` (вороги перекривають шляхи відступу).
- КОЛИ `custom: «рух завершено»` → ТО `counter(attack_points, +path_len)` — сила наступного удару в цьому раунді.
- КОЛИ `custom: «рух завершено»` → ТО `counter(meter[color], +path_len)` — шкала того кольору, по якому йшов герой.
- КОЛИ `counter(meter[color], ==, full)` → ТО `custom: «доступне вміння цього кольору»` (Hand — удар, Eye — постріл, Heart — лікування, Mind — перефарбування).
- КОЛИ `input(attack, hero, enemy)` → ЯКЩО `in_range(hero, enemy, weapon_range)` і `counter(actions, >=, 1)` → ТО `damage(enemy, attack_points)`, `counter(actions, -1)`.
- КОЛИ `input(ability, hero)` → ЯКЩО `custom: «вміння активне (атака або бафф)»` → ТО `custom: «ефект вміння»`, `counter(actions, -1)`; пасивні вміння й баффи дій не коштують.
- КОЛИ `input(mind_ability, cells)` → ТО `paint(cells, better_color)` — перефарбувати плитки під потрібний шлях.
- КОЛИ `enter(hero, heart_tile)` → ЯКЩО `has(hero, auto_heal_talent)` → ТО `heal(hero, n)`.
- КОЛИ `counter(path_len, >=, 8)` → ТО `counter(justice_tokens, +1)`.
- КОЛИ `counter(justice_tokens, ==, full)` → ТО `custom: «вміння Justice знищує всіх ворогів на полі»`.
- КОЛИ `counter(actions, ==, 0)` → ТО `end_turn` (для героя).
- КОЛИ `turn_start(enemy)` → ТО `custom: «ворог рухається одноколірним шляхом і атакує за тими самими правилами»`; удар може `counter(attack_points, -n)` і `damage(hero, n)`.
- КОЛИ `died(enemy)` → ТО `spawn(item, cell)`.
- КОЛИ `schedule(waves)` → ЯКЩО `custom: «ціль місії ще не виконана»` → ТО `spawn_at(enemy, edge)` — у частині місій вороги прибувають, доки не виконано ціль.
- КОЛИ `all_gone(enemy)` → ТО `win`; інші цілі: «вбий 4 ворогів за 6 раундів», виживання, елімінація.
- КОЛИ `counter(rounds, >, limit)` → ЯКЩО `custom: «ціль на раунди не виконана»` → ТО `lose`.
- КОЛИ `level_end` → ЯКЩО `custom: «перемога»` → ТО `give(team, talent_token)`, `currency(+n)`; поразка забирає токени, здобуті в цьому бою.
- Перемога: ціль місії (зазвичай знищити всіх) · Поразка: герої впали (?) або провалено ліміт раундів · Рахунок: нема; нагороди — Talent-токени, кредити/золото, побічні цілі.

## Керування і ввід
- Тач/миша: натиснути на героя й протягнути шлях пальцем по сітці (`path-drawing`); кінець шляху — нова клітина героя.
- Вибір атаки або вміння з панелі героя, потім ціль.
- Кнопки undo нема — помилковий шлях не скасовується (оглядачі це критикують).
- ПК-версія — миша (?).

## Вікна, меню, HUD
- `game-screen`: ізометрична сітка кольорових плиток; HUD — `hp-bar` героїв і ворогів, `+ui:special-meter` для кожного кольору, `action-points` (дві дії), лічильник очок атаки (?), `objective-text` для цілі місії.
- `+window:chat-link` — ChatLink між місіями: діалоги з варіантами відповіді.
- `upgrade-window`: витрата Talent-токенів на стати й уміння.
- `shop-window`: зброя за кредити (HP, дальність); з епізоду 2 — крафт спорядження.
- `map-window` / `level-select` (?): список місій, повтор пройдених.
- `tutorial-window` у перших боях; `end-screen` — результат місії й нагороди.

## Фічі поза полем
- `levels-sequential`: глави сюжету, понад 100 полів бою на всю сагу; місії можна переграти.
- `meta-progression`: прокачка (уміння, зброя) переходить з епізоду в епізод.
- Талант-токени за місію + побічні цілі; кредити → зброя; крафт (епізод 2) з високими вимогами, що змушують переграти рівні.
- `tutorial`; досягнення й хмарні збереження Steam.

## Варіації й родичі
- Епізоди 1–4; епізод 2 додає укриття, новий тип ворогів, нового героя й місії з нескінченним підкріпленням.
- Родичі в корпусі: [hoplite](hoplite.md) (тактика, де позиція — головне), [into-the-breach](into-the-breach.md), [card-hunter](card-hunter.md), [fights-in-tight-spaces](fights-in-tight-spaces.md); з поза тактики — match-RPG типу Puzzle & Dragons (шлях по плитках).
- **Осі варіацій**: рух — дальність за статом / лише по одному кольору (Ticket to Earth) / за картками; сила удару — фіксована / від довжини пройденого шляху; заряд вміння — кулдаун / від клітин свого кольору / від шкоди.

## Цікавинки для курсу
- Шлях drag-ом лише по сусідніх клітинах того ж кольору, що й стартова — 📎 (перевірка сусідства й кольору на кожен крок).
- Довжина шляху → очки атаки раунду + заповнення шкали кольору — 🌱.
- Плитка Mind: перефарбувати клітини, щоб відкрити довший шлях — 📎.
- Justice-токен за шлях 8+ і «очищення поля» — 🌱.
- AI ворога, що шукає найдовший одноколірний шлях до клітини атаки (DFS по компонентах кольору) — 🥈.
- Генерація розкладки кольорів, що дає достатньо довгих шляхів обом сторонам — 🥇.

## Мапа на каталог
- Є: `path-drawing` ↔ протягування шляху; `hp-damage`; `ai-opponent`; `melee-vs-ranged` ↔ Hand/Eye; `floor-types` ↔ кольори плиток з різним ефектом; `cell-transform` ↔ перефарбування Mind; `drop-on-death` ↔ предмети з ворогів; `destroy-all-enemies`; `reinforcements` ↔ підкріплення до виконання цілі; `shop-between-levels` ↔ зброя за кредити; `sequential-levels`, `level-select`, `tutorial-window`, `game-screen`, `end-screen`.
- **Нема** → пропозиції карток:
  - `+color-path-move` «Рух лише по клітинах одного кольору» · entities/legality · 📎 · слот {colors: 4}.
  - `+path-length-power` «Сила дії = довжина пройденого шляху» · entities/combat · 🌱.
  - `+charge-meter-special` «Шкала, що заряджає вміння» · entities/state · 📎 · слот {source: tiles|damage|kills}.
  - `+action-points` (уже в корпусі) · слот {per_unit: 2}.
  - `+screen-clear-special` «Супервміння прибирає всіх ворогів» · entities/combat · 🌱.
  - `+turn-limit-objectives`, `+cover-system` — уже в корпусі.
  - `+talent-tokens` «Токен за місію → стат/уміння» · game-logic/economy · 🌱.
  - `+crafting` «Крафт спорядження з ресурсів» · game-logic/economy · 🥉.

## Пропозиції до словників
- `+cond:color` — клітина/плитка має колір (уже пропоновано в корпусі); тут — перевірка кольору кожної клітини шляху.
- `+trigger:meter_full` — шкала вміння заповнилась (уже пропоновано).
- `+ui:special-meter` — шкала заряду вміння кожного кольору (уже пропоновано).
- `+window:chat-link` — екран діалогу-месенджера між місіями з вибором реплік.
- `+card:color-path-move` — механіка, якої в каталозі нема.

## Джерела
- ⭐ [Pocket Gamer: огляд](https://www.pocketgamer.com/ticket-to-earth/ticket-to-earth-review-a-magnificent-puzzling-rpg-hybrid/) — «рухатися можна лише шляхами того самого відтінку», 2 очки дії, 4 типи плиток, довжина шляху = сила.
- [Wikipedia](https://en.wikipedia.org/wiki/Ticket_to_Earth) — розробник, дати iOS/ПК/Android 2017, суть механіки одним реченням.
- [Steam](https://store.steampowered.com/app/636390/Ticket_to_Earth/) — опис ПК-видання, понад 100 полів бою, сага завершена.
- [Hooked Gamers](https://www.hookedgamers.com/pc/ticket_to_earth/review/article-1831.html) — значення кольорів, шкали вмінь, дві дії на персонажа, Talent-токени, зброя за кредити.
- [Gameranx](https://gameranx.com/updates/id/128201/article/ticket-to-earth-impressions-an-original-demanding-sci-fi-statement/) — кольори (помаранчевий/зелений/фіолетовий/рожевий), Justice-токени, автолікування лише на Heart, нема undo, цілі місій.
- [iMore](https://www.imore.com/ticket-earth-review), [Digitally Downloaded](https://www.digitallydownloaded.net/?p=44917), [148Apps (епізод 2)](http://www.148apps.com/reviews/ticket-to-earth-episode-2-review/) — випадкова розкладка, предмети з ворогів, вороги за тими ж правилами, укриття й крафт.
- YouTube: пошук «Ticket to Earth gameplay».

## Непевне
- (?) Чи рух лише ортогональний, чи діагоналі теж рахуються сусідами; чи шлях може проходити через ту саму клітину двічі.
- (?) Що стається з пройденими плитками: лишаються, змінюють колір чи «збираються» й поповнюються новими.
- (?) Точні розміри полів, обсяг шкал, скільки Justice-токенів треба для Justice — у джерелах немає.
- (?) Як саме працює укриття з епізоду 2 і як підбираються предмети з убитих ворогів.
- (?) Умова поразки (усі герої впали чи впав головний), чи вороги теж заряджають шкали кольорів.
- (?) Склад героїв: Steam згадує чотирьох, огляди епізоду 1 — Rose і Wolf, епізоду 2 — ще одного.
