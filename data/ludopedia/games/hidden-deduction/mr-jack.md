---
title: Mr. Jack (Містер Джек)
slug: mr-jack
aka: [Містер Джек, Mr. Jack London]
family: hidden-deduction
also: [board-digital]
klass: figure
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: hidden
  random: both
  goal: state
year: 2006
platforms: [board (Hurrican 2006, Asmodee), web (Board Game Arena), iOS/Android (Mr Jack Pocket, 2014)]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/mr-jack/game-rules.php", best: true, note: "правила: компоненти, порядок A-B-B-A / B-A-A-B, виклик свідків, ліхтарі, кордони, люки, три кінцівки"}
  - {kind: other, url: "https://www.ultraboardgames.com/mr-jack/the-characters.php", note: "8 персонажів: рух 1–3 (Stealthy 1–4) і здібності з таймінгом"}
  - {kind: other, url: "https://en.doc.boardgamearena.com/Gamehelpmrjack", note: "довідка BGA: Watson і ліхтар, вихід у кутах, одне обвинувачення за гру"}
  - {kind: play, url: "https://en.boardgamearena.com/gamepanel?game=mrjack", note: "грати в браузері (Board Game Arena)"}
  - {kind: other, url: "https://apps.apple.com/app/id853246110", note: "Mr Jack Pocket (Asmodee Digital, 2014): соло проти AI і онлайн"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=mr+jack+board+game+how+to+play", note: "пошук; правила"}
stage: v1
coverage: 65
mechanics: [move-by-input, impassable-cells, teleport, legal-move-highlight, reachable-highlight, cell-click, drag-drop-piece, hot-seat, turn-enforcement, ai-opponent, online-multiplayer, fog-of-war, objective-text, game-screen, end-screen, main-menu, help-window, tutorial-window, character-select, +shared-pieces-draft, +turn-order-abba, +witness-yes-no-filter, +light-source-visibility, +lantern-cone, +hidden-identity-among-pieces, +one-shot-accusation, +exit-escape-condition, +blocker-relocation]
proposes: ["+trigger:witness_call", "+trigger:accuse", "+cond:lit", "+cond:seen", "+effect:relocate_token", "+role:light", "+ui:witness-card", "+ui:suspect-tokens", "+ui:turn-track", "+window:character-draft", "+window:accusation-dialog", "+card:shared-pieces-draft", "+card:turn-order-abba", "+card:witness-yes-no-filter", "+card:light-source-visibility", "+card:lantern-cone", "+card:hidden-identity-among-pieces", "+card:exit-escape-condition", "+card:blocker-relocation"]
author: opus
date: 2026-11-09
---

# Mr. Jack — 8 персонажів на гексах Вайтчепела, Джек — один із них; кожен хід «видно Джека чи ні?» відсіює половину підозрюваних

## Суть
Асиметрична дуель: Джек таємно знає, кого з 8 персонажів він грає; інспектор — ні. Обидва гравці по черзі обирають і рухають **тих самих** персонажів (кожен має свою здібність). Наприкінці раунду Джек мусить чесно сказати, чи його персонаж **видимий** (стоїть на освітленій клітині або поруч з іншим персонажем); усі, хто не збігається з відповіддю, стають «невинними». Інспектор виграє, коли персонажем стає на клітину Джека і правильно його називає; Джек — коли тікає непомітним крізь вихід або виживає 8 раундів.

## Поле і час
- Гексова мапа кварталу: вуличні гекси (світло-сірі й з люками) прохідні; будинки, ліхтарі, сади — ні (крім Miss Stealthy).
- Світло: гекси, суміжні із запаленим ліхтарем, освітлені; решта — темні. 6 запалених ліхтарів (4 з номерами 1–4, 2 без номерів).
- Виходи — 4 кутові гекси; 2 поліцейські кордони закривають два з них.
- Люки: 2 накриті, решта відкриті; з відкритого люка за 1 очко руху — на будь-який інший відкритий.
- Час: до 8 раундів, у раунді 4 ходи персонажами (по 2 на гравця). Ліхтар з номером раунду гасне в кінці раундів 1–4.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Sherlock Holmes | piece | рух 1–3 | після руху обовʼязково тягне алібі-карту: Джек — тримає приховано, інспектор — дізнається невинного |
| John H. Watson | piece | рух 1–3 | ліхтар: освітлює всіх персонажів по прямій у напрямку, який обирає той, хто ним ходив; сам Watson не освітлений |
| John Smith | piece | рух 1–3 | до або після руху переносить запалений ліхтар на згаслий ліхтарний гекс |
| Inspector Lestrade | piece | рух 1–3 | до або після руху переносить кордон: відкриває один вихід, закриває інший |
| Miss Stealthy | piece | рух 1–4 | може проходити крізь будинки, ліхтарі, сади; зупиняється лише на вулиці |
| Sergeant Goodley | piece | рух 1–3 | свисток: 3 очки руху на інших персонажів, кожен крок — ближче до Goodley |
| Sir William Gull | piece | рух 1–3 | замість руху може помінятися місцем із будь-яким персонажем |
| Jeremy Bert | piece | рух 1–3 | до або після руху переносить кришку люка на інший відкритий люк |
| Жетон персонажа | mark | бік «підозрюваний» / «невинний» | перевертається на «невинний» після виклику свідків |
| Запалений ліхтар | switch | 4 з номерами + 2 без | освітлює суміжні гекси; номерні гаснуть у раунди 1–4 |
| Кордон | gate | ×2 | закриває кутовий вихід |
| Люк | terrain | відкритий / накритий (2 кришки) | телепорт-мережа між відкритими люками |
| Будинок / сад | static | — | непрохідний, крім Stealthy |
| Вихід | static | 4 кути | Джек виходить, якщо невидимий і вихід відкритий |
| Карта персонажа | supply | 8, зелені | 4 на раунд; вибір визначає, ким ходити |
| Алібі-карта | supply | 8, червоні | одна в Джека (його особа); решта — для Holmes |
| Карта свідка | mark | «Бачили» / «Не бачили» | фіксує відповідь Джека в раунді |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «Джек таємно тягне алібі-карту — це його персонаж»`; 4 персонажі в тіні, 4 на світлі; усі — «підозрювані».
- КОЛИ `turn_start(round)` → ЯКЩО `custom: «раунд непарний»` → ТО `custom: «відкрити 4 карти персонажів»`, порядок вибору: інспектор, Джек, Джек, інспектор; ЯКЩО парний → ТО решта 4 карти, порядок: Джек, інспектор, інспектор, Джек.
- КОЛИ `input(pick, card)` → ЯКЩО `turn_of(side)` → ТО `custom: «походити персонажем і/або застосувати здібність»`, карта — долілиць.
- Рух: КОЛИ `input(move, c, to)` → ЯКЩО `path_exists(street, c, to)` у межах очок руху → ТО `move(c, to)`; ЯКЩО `cell(to, building)` і `not same(c, stealthy)` → ТО `block`.
- КОЛИ `input(move, c, manhole)` → ЯКЩО `cell(c, open_manhole)` і `cell(manhole, open_manhole)` → ТО `teleport(c, manhole)` за 1 очко руху.
- КОЛИ `input(ability, gull, target)` → ТО `swap(gull, target)` замість руху.
- КОЛИ `input(ability, goodley)` → ТО `custom: «3 кроки іншими персонажами, кожен ближче до Goodley»`.
- КОЛИ `input(ability, smith|lestrade|bert, from, to)` → ТО `custom: «перенести ліхтар / кордон / кришку люка з from на to»`.
- КОЛИ `input(face, watson, dir)` → ТО `custom: «освітлені всі персонажі в лінії dir»`.
- КОЛИ `input(ability, holmes)` → ТО `custom: «взяти верхню алібі-карту»`; ЯКЩО `turn_of(inspector)` → ТО `set_state(card_character, innocent)`; ЯКЩО `turn_of(jack)` → ТО карта лишається прихованою (менше алібі для інспектора).
- Виклик свідків: КОЛИ `turn_end(round)` → ТО `custom: «Джек оголошує, чи видно його персонажа»`, де видно = освітлений гекс (суміжний із запаленим ліхтарем або в лінії Watson) або `adjacent(c, any_character)`.
- КОЛИ `custom: «Бачили»` → ТО `set_state(all_not_seen, innocent)`; КОЛИ `custom: «Не бачили»` → ТО `set_state(all_seen, innocent)`.
- КОЛИ `turn_end(round)` → ЯКЩО `level(<=, 4)` → ТО `custom: «згасити ліхтар з номером раунду»`; ЯКЩО раунд парний → ТО `custom: «перетасувати карти персонажів»`.
- Обвинувачення: КОЛИ `input(move, c, to)` → ЯКЩО `turn_of(inspector)` і `occupied(to, character)` → ТО `custom: «обвинуватити персонажа в to»`: ЯКЩО це Джек → `win` (інспектор), інакше `lose` (інспектор). Одне на гру.
- Втеча: КОЛИ `edge(jack_character)` → ЯКЩО `custom: «на початку раунду Джек був невидимий»` і `custom: «вихід без кордону»` → ТО `win` (Джек).
- КОЛИ `custom: «кінець 8-го раунду»` → ЯКЩО Джека не спіймано → ТО `win` (Джек).
- Перемога інспектора: правильне обвинувачення · Перемога Джека: втеча, хибне обвинувачення або 8 раундів · Рахунок: нема.

## Керування і ввід
- Настолка: гравці по черзі обирають карту персонажа з відкритих, рухають жетон гексами вулиць, застосовують здібність (до/після/замість руху — за символом на карті).
- Цифрова версія: клік по карті персонажа → підсвітка досяжних гексів → клік по цілі; здібність — окремою кнопкою або drag обʼєкта (ліхтар, кордон, кришка); Watson — вибір напрямку ліхтаря стрілками.
- Відповідь свідків у цифровій версії рахує гра сама (вона знає особу Джека) — гравцеві за Джека нічого чесно казати не треба.

## Вікна, меню, HUD
- `main-menu` (цифрова версія): Онлайн / Проти AI / Туторіал → `tutorial-window`; Правила → `help-window`.
- `character-select` (цифрова версія): вибір ролі — Джек або інспектор.
- `game-screen` (цифрова версія): гексова мапа з ліхтарями, люками, кордонами; 8 жетонів (`suspect-tokens` — підозрюваний/невинний); ряд із 4 відкритих карт раунду (`character-draft`); `turn-track` 1–8 з позначками згасання ліхтарів; `witness-card`; для Джека — його алібі-карта в кутку; `turn-indicator`; `legal-move-highlight`.
- `accusation-dialog` (цифрова версія): підтвердження «звинуватити X?».
- `end-screen` (цифрова версія): хто виграв, як (втеча / обвинувачення / 8 раундів), особа Джека.
- Переходи: main-menu → character-select → game-screen (draft ↔ хід ↔ свідки) → end-screen.

## Фічі поза полем
- `online-multiplayer` (BGA, мобільна Pocket), `ai-opponent-levels` (?) у Mr Jack Pocket (соло офлайн).
- `tutorial` (Mr Jack Pocket).
- Розширення й редакції — нові персонажі (?) і Revised Edition.

## Варіації й родичі
- Mr. Jack Pocket — коротка версія на вуличних плитках замість гексів (?); Mr. Jack in New York — інша мапа й персонажі (?).
- Родичі: [Cluedo](cluedo.md) — дедукція особи через спростування; [Guess Who?](guess-who.md) — так/ні відсікає підмножину облич; [Scotland Yard](scotland-yard.md) — асиметрія «один знає, інші шукають»; [Stratego](stratego.md) — особа фігури прихована.
- **Осі варіацій**: хто ходить персонажами «спільні для обох / власні»; запитання «одне за раунд, фіксоване (видимість) / вільне (Guess Who)»; сигнал «світло ліхтарів / сусідство / промінь»; виграш Джека «втеча / виживання / хибне звинувачення».

## Цікавинки для курсу
- Виклик свідків: множина підозрюваних ∩ (видимі чи невидимі) — один фільтр, що ріже множину навпіл — 📎.
- Освітленість: гекси, суміжні з ліхтарями, плюс промінь Watson по лінії гексів, плюс «поруч з іншим» — 🥉 (гекс-сусідство і лінія на гексах).
- Спільні фігури з драфтом A-B-B-A / B-A-A-B: обидві сторони рухають тих самих персонажів із протилежними цілями — 🥉.
- Мережа люків як телепорт з кришками, які можна переносити — 📎.
- Здібності 8 персонажів як окремі правила (swap, перенос обʼєкта, тяга до себе) — 🌱 кожна.
- AI за Джека: обирати хід, що зберігає найбільшу множину підозрюваних і близькість до відкритого виходу — 🥇.

## Мапа на каталог
- Є: `move-by-input` · `impassable-cells` (будинки) · `teleport` (люки) · `legal-move-highlight` + `reachable-highlight` · `cell-click` + `drag-drop-piece` · `hot-seat` + `turn-enforcement` · `ai-opponent` · `online-multiplayer` · `fog-of-war` (особа Джека) · `objective-text` · `game-screen` / `end-screen` / `main-menu` / `help-window` / `tutorial-window` / `character-select`.
- **Нема** → пропозиції карток:
  - `+shared-pieces-draft` «Спільні фігури, гравці по черзі обирають, ким ходити» · game-logic/turns · 🥉.
  - `+turn-order-abba` «Порядок ходів A-B-B-A / B-A-A-B» · game-logic/turns · 🌱.
  - `+witness-yes-no-filter` «Відповідь так/ні відсікає підозрюваних» · game-logic/info · 📎.
  - `+light-source-visibility` «Клітини, суміжні з джерелом світла, освітлені» · field/visibility · 📎.
  - `+lantern-cone` «Промінь у вибраному напрямку освітлює лінію» · field/visibility · 📎 (на гексах).
  - `+hidden-identity-among-pieces` «Одна з фігур — таємна ціль» · game-logic/info · 🌱.
  - `+one-shot-accusation` — як у Cluedo.
  - `+exit-escape-condition` «Втеча крізь відкритий вихід за умови» · game-logic/win · 🌱.
  - `+blocker-relocation` «Перенос блокера: відкрити одне, закрити інше» · entities/interact · 🌱.

## Пропозиції до словників
- `+trigger:witness_call` — фаза кінця раунду, коли прихована сторона дає відповідь так/ні.
- `+trigger:accuse` — обвинувачення (див. Cluedo); тут — хід на клітину підозрюваного.
- `+cond:lit` — клітина освітлена (суміжна з джерелом світла або в його промені).
- `+cond:seen` — персонаж видимий: `lit` або сусід іншого персонажа.
- `+effect:relocate_token` — перенести обʼєкт поля (ліхтар, кордон, кришку) з однієї позиції на іншу дозволену.
- `+role:light` — джерело світла з радіусом/променем.
- `+ui:witness-card` — індикатор відповіді «Бачили / Не бачили»; `+ui:suspect-tokens` — жетони з боками «підозрюваний/невинний»; `+ui:turn-track` — трек раундів із подіями.
- `+window:character-draft` — вибір карти персонажа з відкритих; `+window:accusation-dialog` — підтвердження звинувачення.

## Джерела
- ⭐ [UltraBoardGames: правила Mr. Jack](https://www.ultraboardgames.com/mr-jack/game-rules.php) — компоненти, сетап, порядок вибору, виклик свідків, ліхтарі, кордони, люки, кінцівки.
- [UltraBoardGames: персонажі](https://www.ultraboardgames.com/mr-jack/the-characters.php) — рух і здібності 8 персонажів із таймінгом.
- [BGA: довідка Mr. Jack](https://en.doc.boardgamearena.com/Gamehelpmrjack) — ліхтар Watson, кутові виходи, одне обвинувачення, умова втечі.
- [BGA: Mr. Jack](https://en.boardgamearena.com/gamepanel?game=mrjack) — онлайн-версія.
- [App Store: Mr Jack Pocket](https://apps.apple.com/app/id853246110) — мобільна адаптація (Asmodee Digital, 2014).
- Автори: Bruno Cathala, Ludovic Maublanc; видавець Hurrican (з результатів пошуку).

## Непевне
- (?) Кількість гексів, люків і точні стартові позиції — у джерелах не дано.
- (?) Чи може персонаж проходити крізь інших або зупинятися на зайнятому гексі (окрім обвинувачення) — джерела мовчать.
- (?) Чи може Джек тікати лише тоді, коли сам ходить своїм персонажем, — не уточнено.
- (?) Чи отримує Джек щось від алібі-карти, яку взяв Holmes на його ході (у деяких редакціях — пісочні годинники), — не перевірено.
- (?) Mr. Jack Pocket і Mr. Jack in New York — правила не читав; назва «Mr. Jack London» — з памʼяті.
- (?) Інтерфейс цифрових версій описано як «(цифрова версія)», а не з побаченого.
