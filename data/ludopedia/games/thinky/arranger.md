---
title: "Arranger: A Role-Puzzling Adventure"
slug: arranger
aka: [Arranger]
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
year: 2024
platforms: [PC, Mac, Switch, PS5, iOS, Android]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2596420/Arranger_A_RolePuzzling_Adventure/", best: true, note: "опис: усе в рядку/стовпці Джемми рухається з нею, петля через край; RPG без XP й інвентаря; assist-опції"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Arranger:_A_Role-Puzzling_Adventure", note: "ряди й стовпці з загортанням, нерухомі барʼєри, меч у монстра, пропуск рівнів; платформи, Netflix, оцінки"}
  - {kind: other, url: "https://press-start.com.au/reviews/nintendo-switch/2024/07/22/arranger-a-role-puzzling-adventure-review-the-good-kind-of-sliding-block-puzzle/", note: "рецензія: нерухоме каміння, мечі проти кількох монстрів, кнопки під обʼєктами, боси, skip, buddy mode, hard mode, лічильник кроків"}
  - {kind: other, url: "https://www.rpgfan.com/review/arranger-a-role-puzzling-adventure/", note: "рецензія: статичні обʼєкти, гаки, двері-телепорти, плоти; смерті нема; пропуск пазлів в опціях"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Arranger+Role-Puzzling+Adventure+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, move-by-input, keyboard-controls, swipe-gestures, row-conveyor, wrap-edges, impassable-cells, crush-by-slide, key-and-door, button-toggle, teleport, reach-exit, skip-level, restart-level, move-counter, game-screen, settings-window, achievements-window, save-autosave, +row-shift-push, +avatar-drags-line, +assist-skip, +buddy-pointer-coop]
proposes: ["+effect:shift_line", "+cond:in_line", "+card:avatar-drags-line", "+card:assist-skip", "+card:buddy-pointer-coop", "+feature:buddy-mode"]
author: opus
date: 2026-11-09
---

# Arranger — пригодницька RPG, де крок героїні зсуває весь її рядок або стовпець світу по колу

## Суть
Джемма подорожує світом, що весь є однією сіткою. Кожен її крок вліво/вправо зсуває **весь рядок**, у якому вона стоїть, а крок вгору/вниз — **весь стовпець**; що вийшло за край, зʼявляється з протилежного боку. Нерухомі барʼєри, монстри й дивна сила «статика» не зсуваються — об них і будуються пазли: підвести меч у ряд до монстра й «наїхати» ним, засунути обʼєкт на кнопку, протягнути ключ до дверей. Бої, рух і дослідження — один механізм; XP та інвентаря нема, усе «в світі».

## Поле і час
- Квадратна сітка; кімната/екран — окремий пазл, кімнати складаються в регіони й підземелля (кластери повʼязаних кімнат, кожна вводить нову механіку).
- Кожен рядок і стовпець — кільце: зсув на 1 із загортанням (тор по лінії).
- Покроково: тік = крок Джемми; рух без таймера («Playable without Timed Input»), вороги нерухомі.
- Мальовані фони з коміксовими панелями; камера показує кімнату.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Джемма | player | — | крок 4 напрямки = зсув свого рядка/стовпця разом із собою; не гине |
| Рухомий обʼєкт (кущ, ящик, предмет) | object | — | їде разом із рядком/стовпцем Джемми, загортається через край |
| Нерухомий камінь / барʼєр | static | — | не зсувається; може зупинити зсув лінії (?) |
| Статика | hazard | — | сюжетна сила, що «пришпилює» людей; на полі — нерухомий барʼєр |
| Меч | object | — | рухається з лінією; наїхавши на монстра, знищує його; одним рядом можна вразити кількох |
| Монстр | enemy | нерухомий | перекриває шлях; гине від меча |
| Бос | boss | фази (?) | окремі бої на тій самій механіці |
| Ключ | object | — | доставлений до замкнених дверей — відчиняє (?) |
| Замкнені двері | gate | — | прохід після ключа |
| Кнопка | switch | — | натиснута, поки на ній обʼєкт; зсув лінії зіштовхує обʼєкт — кнопка відпускається |
| Двері / механізм за кнопкою | gate | — | відкриті, поки кнопка натиснута |
| Гак (grappling hook) | object | — | механіка регіону (?) |
| Двері-телепорт | static | пара | переносять (?) |
| Пліт | terrain | — | перетин води (?) |
| Мешканці (NPC) | neutral | — | їдуть разом із лінією, як обʼєкти; діалоги |
| Вихід кімнати | static | — | мета пазла |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ТО `shift(row_of_jemma, dir)` — Джемма й усе рухоме в рядку зсуваються на 1.
- КОЛИ `input(up|down)` → ТО `shift(col_of_jemma, dir)`.
- КОЛИ `edge(a)` під час зсуву → ТО `wrap(a)` — зʼявляється з протилежного кінця лінії.
- КОЛИ `custom: «зсув лінії, у якій є нерухомий камінь»` → ТО `block` (?) — див. «Непевне».
- КОЛИ `contact(sword, monster)` → ТО `disappear(monster)` — шлях відкрито.
- КОЛИ `contact(key, locked_door)` → ТО `disappear(locked_door)` (?).
- КОЛИ `enter(object, button)` → ТО `set_state(gate, open)`; КОЛИ `leave(object, button)` → ТО `clear_state(gate, open)`.
- КОЛИ `enter(jemma, teleport_door)` → ТО `teleport(jemma, pair)` (?).
- КОЛИ `reach(jemma, exit)` → ТО `custom: «наступна кімната / регіон»`.
- КОЛИ `input(skip)` → ТО `custom: «пазл зараховано без розвʼязку»` (assist-опція).
- Перемога: дійти до виходу кімнати; фінал — сюжет · Поразки нема: Джемма не гине, глухий кут — рестарт кімнати · Рахунку нема; лічильник кроків і таймер — для челенджів.

## Керування і ввід
- Хрестовина / стрілки / стік — крок (= зсув лінії); на Switch — HD-вібрація на неможливий хід.
- Тач-режим (мобільні, Switch); на мобільних — свайпи (?).
- Buddy mode: другий гравець-фея вказує на деталі або «відволікає» — без впливу на правила.
- Hard mode: інвертоване керування й значно швидший рух (рецензія) (?).

## Вікна, меню, HUD
- `game-screen`: кімната-сітка на мальованому фоні; опційно `move-counter` і `timer-elapsed` (для спідранерів).
- `dialogue-window` — діалоги мешканців і сюжетні сцени-комікси.
- `settings-window` / опції доступності: пропуск пазлів, тач-режим, buddy mode, hard mode, розмір тексту, гучність.
- `pause-menu` з пропуском пазла (?).
- `achievements-window` (Steam Achievements).

## Фічі поза полем
- `skip-level` без ліміту як assist-опція («only get as stuck as you want to be»); `assist-mode`.
- `move-counter` + `timer-elapsed` вмикаються для челенджів; необовʼязкові складні кімнати.
- `autosave` («Save Anytime»), `cloud-save`, `achievements`, `localization` (13 мов), `font-scale`, `touch-controls`, `gamepad-support`.
- Мобільна версія — у підписці Netflix Games.

## Варіації й родичі
- Механіка зсуву рядів: [MazezaM](../push-slide/mazezam.md) (ряд штовхається цілим, без загортання), [пʼятнашки й Loopover](../push-slide/sliding-tile-permutation.md) (зсув ряду по колу як хід), [Labyrinth](../board-digital/labyrinth.md) (вставка плитки зсуває ряд).
- Родичі «пригода з пазл-кімнатами»: Zelda-подібні данжі; [Void Stranger](void-stranger.md), [Isles of Sea and Sky](isles-of-sea-and-sky.md).
- **Осі варіацій** зсуву ліній: хто ініціює — аватар своїм кроком / курсор / вставка плитки; край — загортання / упор / випадання; нерухоме в лінії — блокує / ділить лінію на сегменти.

## Цікавинки для курсу
- Крок = циклічний зсув рядка/стовпця з аватаром — 📎 (`deque.rotate` на рядку й стовпці).
- Нерухомі клітини в кільці: блок усього зсуву чи сегменти між ними — 🥉 (правило має бути однозначним і тестованим).
- Меч, що вбиває при наїзді, і кнопка, що тримається, поки на ній обʼєкт — 📎 (взаємодії після зсуву).
- Пропуск пазла як опція доступності — 🌱.
- Розвʼязувач кімнати BFS по станах сітки — 🥈 (стан = вся сітка; кільця множать сусідів).

## Мапа на каталог
- Є: `move-4dir`, `move-by-input`, `keyboard-controls`, `swipe-gestures` ↔ крок · `row-conveyor` ↔ уся смуга зсувається разом · `wrap-edges` ↔ петля через край · `impassable-cells` ↔ нерухомі барʼєри · `crush-by-slide` ↔ меч, наїжджаючи, вбиває монстра · `key-and-door` · `button-toggle` ↔ кнопка під обʼєктом · `teleport` ↔ двері-телепорти · `reach-exit` · `skip-level` · `restart-level` · `move-counter` · `game-screen`, `settings-window`, `achievements-window`, `save-autosave`.
- **Нема** → пропозиції карток:
  - `+row-shift-push` (уже з MazezaM) — тут із загортанням.
  - `+avatar-drags-line` «Крок аватара зсуває весь його рядок/стовпець по колу» · entities/move · 📎 · слоти {axis: row|col|both, edge: wrap|stop}.
  - `+assist-skip` «Пропуск пазла без ліміту як опція доступності» · game-logic/difficulty · 🌱 (на відміну від `skip-level` з лімітом).
  - `+buddy-pointer-coop` «Другий гравець лише вказує на поле» · game-logic/opponent · 📎.

## Пропозиції до словників
- `+effect:shift_line(a, axis, dir)` — зсув рядка/стовпця, у якому стоїть A (відмінне від `shift`: лінію визначає позиція сутності, а не номер).
- `+cond:in_line(a, b)` — B у тому самому рядку або стовпці, що й A.
- `+card:avatar-drags-line`, `+card:assist-skip`, `+card:buddy-pointer-coop` — див. вище.
- `+feature:buddy-mode` — кооп-помічник без впливу на стан гри.

## Джерела
- ⭐ [Steam](https://store.steampowered.com/app/2596420/Arranger_A_RolePuzzling_Adventure/) — суть механіки, «static», RPG без XP/інвентаря, assist-опції, мови, Save Anytime.
- [Wikipedia](https://en.wikipedia.org/wiki/Arranger:_A_Role-Puzzling_Adventure) — ряди/стовпці з загортанням, нерухомі барʼєри, меч проти нерухомого монстра, пропуск рівнів; Unity, платформи, Netflix, оцінки.
- [Press Start](https://press-start.com.au/reviews/nintendo-switch/2024/07/22/arranger-a-role-puzzling-adventure-review-the-good-kind-of-sliding-block-puzzle/) — каміння, що ламає петлю; мечі проти кількох монстрів; кнопки; боси; skip, тач, buddy, hard mode, лічильник кроків і таймер.
- [RPGFan](https://www.rpgfan.com/review/arranger-a-role-puzzling-adventure/) — статичні обʼєкти, гаки, двері-телепорти, плоти, відсутність смерті, пропуск в опціях.
- YouTube: [пошук «Arranger Role-Puzzling Adventure gameplay»](https://www.youtube.com/results?search_query=Arranger+Role-Puzzling+Adventure+gameplay).

## Непевне
- (?) Що робить нерухомий обʼєкт у лінії: блокує весь зсув чи лінія зсувається сегментами між нерухомими (рецензії кажуть лише «камінь ламає петлю»).
- (?) Ключ і двері — згадка з рецензії, точне правило не описане.
- (?) Гаки, двері-телепорти, плоти — лише назви механік регіонів.
- (?) Що буває, коли Джемма в лінії наїжджає на монстра без меча.
- (?) Hard mode «інвертоване керування й швидкість» — одне джерело; undo в кімнаті — не підтверджено.
