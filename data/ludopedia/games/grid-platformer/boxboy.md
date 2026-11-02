---
title: BoxBoy! (ハコボーイ!)
slug: boxboy
family: grid-platformer
also: [thinky]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 2015
platforms: [3DS (BoxBoy! 2015, BoxBoxBoy! 2016, Bye-Bye BoxBoy! 2017), Switch (BoxBoy! + BoxGirl! 2019), mobile (Uniqlo x HakoBoy! 2017)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/BoxBoy!_(video_game)", best: true, note: "ланцюг коробок, ліміт на рівень, міст/сходи/щит/гак, корони, медалі, підказки"}
  - {kind: other, url: "https://ja.wikipedia.org/wiki/ハコボーイ!", note: "JP: 7–8 «Box Skills», причини смерті, магазин, Time/Score Attack"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/BoxBoy!", note: "серія: два набори коробок, спец-коробки, кооп"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/BoxBoxBoy!", note: "два набори коробок одночасно"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bye-Bye_BoxBoy!", note: "типи коробок, супровід Qbabies"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/BoxBoy!_%2B_BoxGirl!", note: "кооп, Qudy з прямокутними коробками, 270 рівнів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=boxboy+3ds+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-4dir, gravity-fall, reach-exit, push-object, item-pickup, touch-death, environment-death, checkpoint, respawn, sequential-levels, level-unlock, level-select, shop-between-levels, shop-catalog, shop-window, avatar-picker, background-music, time-bonus, event-points, help-window, multi-cell-size, stick-together, +box-chain-extrude, +box-budget-crowns, +retract-to-chain-end, +rigid-shape-fall, +shield-block, +carrier-platform, +party-switch, +hint-purchase, +world-map, +stamps-challenges]
proposes: ["+effect:extrude", "+effect:retract", "+effect:detach", "+effect:fall", "+cond:charges", "+trigger:input", "+role:hazard", "+role:switch", "+role:gate", "+ui:box-counter", "+ui:crown-counter", "+window:skill-book", "+feature:hint", "+feature:stars-rating", "+axis:actors", "+card:box-chain-extrude"]
author: opus
date: 2026-11-02
---

# BoxBoy! — квадратний герой видавлює з себе ланцюжок коробок і будує ними міст, сходи, щит чи гак

## Суть
Qbby — квадрат на ніжках у чорно-білому бічному світі. Головна дія — **видавити з тіла ланцюг до N коробок** розміром із себе, малюючи форму напрямками; ланцюг лишається приклеєним до героя або відчіплюється й стає твердою фігурою під гравітацією. Тією самою формою роблять міст через прірву, сходи на уступ, щит від лазера, гак за край, «змію» у вузький прохід, натискач кнопки. Ліміт коробок на одночасний ланцюг + окремий бюджет коробок на рівень за корони перетворюють платформер на пазл «найдешевша форма».

## Поле і час
- Бічний вид, квадратна сітка розміром «одна коробка = один Qbby»; рівні з кількох екранів, камера слідує.
- Real-time з гравітацією, але без тиску часу: усе детерміноване, вороги/лазери/крани — за фіксованим розкладом.
- Шари: рельєф (стіни, ями, шипи), механізми (лазери, крани, кнопки, двері, липкі й електричні блоки), рухомі обʼєкти (dummy-блоки, ланцюг коробок), герой.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Qbby | player | 1 «життя» до чекпойнта | ходить, стрибає на 1 клітину, падає; видавлює коробки |
| Коробка (ланцюг) | object | ліміт N на ланцюг (за рівнем) | кожна наступна — сусідня до попередньої; разом — жорстка поліоміно-форма |
| Ланцюг прикріплений | object | — | рухається разом із Qbby, може звисати як гак/щит |
| Ланцюг відчеплений | object | — | падає як ціле, лягає опорою; Qbby може штовхати його |
| Стіна / підлога | static | — | опора, непрохідна |
| Яма | hazard | — | падіння = смерть |
| Шипи | hazard | — | дотик Qbby = смерть; коробкам не шкодять (?) |
| Лазер | hazard | напрям, увімк/вимк | промінь убиває Qbby, коробка блокує промінь (щит) |
| Електричний блок | hazard | — | дотик = смерть |
| Липкий блок | terrain | — | Qbby прилипає; виривається власним ланцюгом коробок (Escape) |
| Dummy-блок | object | — | штовхається коробками; переноситься, зачеплений ланцюгом |
| Кнопка | switch | → двері/механізм | натискається Qbby або коробкою, доки на ній вага (?) |
| Двері/бар'єр | gate | зв'язок з кнопкою | відкриті, поки кнопка натиснута (?) |
| Кран | object | траєкторія | везе Qbby/коробки, якщо зачепитись (?) |
| Ворог | enemy | патруль (?) | дотик = смерть (JP wiki) |
| Корона | pickup | — | необовʼязкова; зникає, коли бюджет коробок рівня вичерпано |
| Вихід (двері кінця) | static | — | дійти = рівень пройдено |
| Чекпойнт | static | — | точка респавну після смерті |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(make_mode)` → ТО `custom: «режим видавлювання: напрямки додають коробку до кінця ланцюга»`.
- КОЛИ `input(dir)` у режимі → ЯКЩО `count(chain, <, max_boxes)` і `free(cell_next_to_chain_end)` → ТО `custom: extrude(box)`, `counter(level_boxes, -1)`; клітина вже з коробкою ланцюга → `custom: «прибрати останню»` (?).
- КОЛИ `input(drop)` → ТО `custom: detach(chain)`, `fall(chain)` як одне тіло.
- КОЛИ `input(retract|pull)` → ЯКЩО кінець ланцюга спирається/зачеплений → ТО `move(qbby, chain_end)`, `disappear(chain)` — гак і «змія» (Bye-Bye: Qbby переходить у найдальшу коробку).
- КОЛИ `input(make_mode)` при наявному ланцюгу → ТО `disappear(old_chain)`, новий ланцюг — з нуля.
- КОЛИ `contact(qbby|chain, block)` при русі → ЯКЩО `free(cell_behind)` → ТО `push` (Push-skill).
- КОЛИ `contact(laser, box)` → ТО `block` (промінь зупинено); КОЛИ `contact(laser, qbby)` → ТО `lose`.
- КОЛИ `contact(qbby, spikes|enemy|electric)` або `enter(qbby, pit)` → ТО `respawn(qbby, checkpoint)`.
- КОЛИ `custom: «Qbby затиснуто між блоком і стіною»` → ТО `respawn` (JP wiki).
- КОЛИ `occupied(button, qbby|box)` → ТО `set_state(gate, open)`; звільнено → `close` (?).
- КОЛИ `contact(qbby, crown)` → ЯКЩО `counter(level_boxes, >, 0)` → ТО `pickup`; КОЛИ `counter(level_boxes, ==, 0)` → ТО `disappear(all crowns)`.
- КОЛИ `contact(qbby, exit)` → ТО `win`, `currency(+medals за прохід + корони)`, `next_level`.
- КОЛИ `input(hint)` → ЯКЩО `has(play_coins|medals)` → ТО `custom: «показати розвʼязок»`.
- Перемога: дійти до виходу. Поразка: нема остаточної — респавн на чекпойнті. Рахунок: медалі (прохід + корони), у Time/Score Attack — час і очки.

## Керування і ввід
- Хрестовина/стік — ходьба, A — стрибок.
- B — увійти в режим створення: напрямки «малюють» ланцюг від тіла; повтор B — завершити (?).
- Окремі кнопки: відчепити ланцюг (drop), скасувати ланцюг, «стягнутись» до кінця ланцюга (?).
- 3DS: Play Coins / медалі → підказка; Switch-кооп: кожен гравець — свій герой і свій ліміт коробок.

## Вікна, меню, HUD
- `splash-screen` → `main-menu`/`level-select`: світи списком/мапою (`world-map`), рівні всередині з позначками корон.
- `game-screen`: рівень; HUD — `custom: «ліміт ланцюга N»` іконками коробок, `remaining-counter` бюджету коробок рівня (для корон), зібрані корони.
- `shop-window` (відкривається після світу 1): костюми, музика, челенджі Time Attack / Score Attack (інверсні кольори), 4-панельні комікси (BoxBoxBoy!), «Box Skill Book».
- `custom-window` «Box Skill Book» — 8 «скілів» коробок з анімацією-поясненням (кодекс прийомів).
- `hints-window` — підказка-розвʼязок рівня за монети.
- `pause-menu`: продовжити · рестарт · вийти на мапу.
- `end-screen` рівня: медалі, корони; фінальний — рекорди і титул.
- Переходи: level-select → game-screen → (вихід) end-screen → level-select; level-select → shop-window.

## Фічі поза полем
- Прогресія: світи по одній механіці (лазери, крани, липкі блоки…), перший рівень світу навчальний; `levels-sequential` + `level-unlock`.
- `stars-rating`-аналог: корони за малий бюджет коробок → медалі (метавалюта).
- `shop`: костюми (декілька змінюють здібності: Hakosennin, Ninja, Rabbit), музика, комікси, челенджі.
- `mode-time-attack`, `mode-score-attack` — окремі челенджі; Challenge Worlds після проходження (Bye-Bye).
- `hint` за валюту; `checkpoint`-респавн; amiibo-костюми (Bye-Bye).
- Кооп (Switch): «A Tale for Two» — два гравці або соло з перемиканням героїв.

## Варіації й родичі
- BoxBoxBoy! — **два ланцюги одночасно**; Bye-Bye BoxBoy! — спеціальні коробки (вибухові, телепорт — за статтею серії; інші (?)) і супровід Qbaby до виходу; BoxBoy! + BoxGirl! — кооп Qbby+Qucy і Qudy з прямокутними коробками, що повертаються 90° (270 рівнів).
- Uniqlo x HakoBoy! — коробки свайпом, герой іде сам (непряме керування).
- Родичі: Snakebird (тіло як інструмент), Toki Tori (бюджет інструментів), Lemmings (будівельник сходів), Tetris/поліоміно (форма з клітин).
- Осі: **скільки ланцюгів** (1 / 2 / кооп по одному); **форма коробки** (квадрат / прямокутник з поворотом); **тип коробки** (звичайна / спец); **що буде зі старим ланцюгом** (зникає / лишається).

## Цікавинки для курсу
- Ланцюг-«поліоміно», що росте від героя напрямками з лімітом N і перевіркою вільних клітин — 🥉.
- Відчеплена форма падає як тверде тіло (перевірка опори для всієї фігури, не для клітини) — 🥈.
- Стягування героя до кінця ланцюга (гак/змія) — переміщення аватара вздовж власного тіла — 🥉.
- Два бюджети: на одночасний ланцюг і на весь рівень (корони гаснуть на нулі) — 📎.
- Коробка як щит від лазера: промінь (ray-cast) зупиняється першою коробкою — 🥉.
- Кооп з окремим лімітом коробок у кожного й двома ланцюгами, що взаємодіють — 🥇.

## Мапа на каталог
- Є: `move-4dir` (ходьба+стрибок) · `gravity-fall` · `reach-exit` · `push-object` · `item-pickup` (корони) · `touch-death` · `environment-death` (яма, затиснення) · `checkpoint` + `respawn` · `sequential-levels` · `level-unlock` · `level-select` · `shop-between-levels` + `shop-catalog` + `shop-window` · `avatar-picker` (костюми) · `background-music` · `help-window` (Skill Book) · `multi-cell-size` (ланцюг як фігура) · `stick-together` (коробки злиплі в одне тіло).
- **Нема** → пропозиції карток:
  - `+box-chain-extrude` «Видавити ланцюг клітин від героя» · entities/interact · 🥉 · слоти {max_boxes, shapes: square|rect}.
  - `+box-budget-crowns` «Бюджет дій на рівень за бонус» · game-logic/score · 📎 — корони гаснуть після N коробок.
  - `+retract-to-chain-end` «Стягнутись до кінця ланцюга» · entities/move · 🥉.
  - `+rigid-shape-fall` «Тверда фігура падає цілою» · entities/move · 🥈.
  - `+shield-block` «Обʼєкт перекриває промінь» · entities/combat · 📎.
  - `+carrier-platform` «Платформа, що везе» · entities/move · 📎 — крани.
  - `+party-switch` «Кілька аватарів з перемиканням» · entities/move · 🥉 — соло-режим кооп-кампанії.
  - `+hint-purchase` «Підказка за ігрову валюту» · game-logic/economy · 📎.
  - `+world-map` «Мапа світу з вузлами-рівнями» · levels/progression · 🥉.
  - `+stamps-challenges` «Челенджі поза кампанією» · levels/progression · 📎 — Time/Score Attack.

## Пропозиції до словників
- `+effect:extrude(a, dir)` — додати клітину до тіла-ланцюга; `+effect:retract(a)` — стягнути ланцюг/героя до кінця; `+effect:detach(chain)` — відчепити (є `detach` ⏳ — уточнити, що для фігури).
- `+effect:fall` — падіння всієї фігури до опори.
- `+cond:charges(boxes, op, n)` — лишилось коробок (ланцюг/рівень).
- `+trigger:input` — режим видавлювання і напрямки.
- `+role:hazard` (лазер, шипи, електричний блок), `+role:switch` (кнопка), `+role:gate` (бар'єр).
- `+ui:box-counter` — іконки ліміту ланцюга; `+ui:crown-counter` — зібрані корони.
- `+window:skill-book` — кодекс прийомів (підвид `codex-window`).
- `+feature:hint` за валюту; `+feature:stars-rating` = корони.
- `+axis:actors` = `party` у кооп-кампанії.
- `+card:box-chain-extrude` — див. вище.

## Джерела
- ⭐ [Wikipedia: BoxBoy! (video game)](https://en.wikipedia.org/wiki/BoxBoy!_(video_game)) — ланцюг, ліміт на рівень, міст/сходи/щит/гак, нова → стара зникає, корони, медалі, Play Coins-підказки.
- [ja.wikipedia: ハコボーイ!](https://ja.wikipedia.org/wiki/ハコボーイ!) — «Box Skills» (Throw, Guard, Hook, Snake, Escape, Push, Carry), причини смерті, магазин, Time/Score Attack, розблокування світів.
- [Wikipedia: BoxBoy! (series)](https://en.wikipedia.org/wiki/BoxBoy!) — огляд серії і платформ.
- [Wikipedia: BoxBoxBoy!](https://en.wikipedia.org/wiki/BoxBoxBoy!) — два набори коробок, комікси.
- [Wikipedia: Bye-Bye BoxBoy!](https://en.wikipedia.org/wiki/Bye-Bye_BoxBoy!) — типи коробок, Qbaby, Challenge Worlds, amiibo.
- [Wikipedia: BoxBoy! + BoxGirl!](https://en.wikipedia.org/wiki/BoxBoy!_%2B_BoxGirl!) — кооп, Qudy, 270 рівнів, підказки за валюту.
- YouTube: пошук «boxboy 3ds gameplay».

## Непевне
- (?) Точні кнопки: який ввід відчіплює, скасовує, стягує ланцюг; чи можна «відмалювати» останню коробку назад.
- (?) Кнопки й двері: тримають лише під вагою чи перемикаються назавжди; поведінка кранів і ворогів.
- (?) Спец-коробки Bye-Bye: вибухова й телепорт підтверджені статтею серії; ракета, мерехтлива та інші — з памʼяті, не перевірено.
- (?) Чи шкодять шипи коробкам; як саме Qudy повертається.
