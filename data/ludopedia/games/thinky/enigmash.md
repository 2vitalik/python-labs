---
title: Enigmash
slug: enigmash
aka: [ENIGMASH]
family: thinky
also: [push-slide, grid-platformer]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2019
platforms: [web]
links:
  - {kind: play, url: "https://jacklance.github.io/PuzzleScript/play.html?p=cfdcc6e23f1fb3e9de2fd42fafaf4d4c", best: true, note: "грати в браузері (форк PuzzleScript автора)"}
  - {kind: other, url: "https://www.bontegames.com/2019/11/enigmash-browser.html", note: "огляд Bart Bonte, 2019-11-05: «one big mashup of puzzles», Z/R; коментарі гравців про зони, перемикачі, автосейв"}
  - {kind: other, url: "https://api.github.com/gists/cfdcc6e23f1fb3e9de2fd42fafaf4d4c", note: "вихідний код (gist JSON, JackLance, 2019-10-25…2020-04-11): шість наборів правил, перемикачі, тунелі, повідомлення"}
  - {kind: other, url: "https://pastebin.com/raw/uxxrRX9w", note: "подяки: ідея з Nitrome Mega Mash; графіка й звуки — Hazelden, Kutilek, Lavelle, Pedro PSI, Rosden, Steed"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Enigmash+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, move-by-input, keyboard-controls, impassable-cells, push-object, stick-together, inertia-slide, gravity-fall, body-queue, fill-hole, button-toggle, teleport, checkpoint, player-camera, undo-unlimited, restart-level, save-autosave, sound-effects, +push-chain, +mechanic-crossover, +zone-rulesets, +ruleset-toggle, +region-blackout, +softlock-guard, +open-world-puzzles, +step-up-climb]
proposes: ["+cond:in_zone", "+effect:swap_ruleset", "+axis:rules", "+ui:zone-border", "+feature:softlock-guard", "+card:zone-rulesets", "+card:ruleset-toggle"]
author: opus
date: 2026-11-09
---

# Enigmash — одна велика мапа, поділена на регіони з різними правилами Sokoban; червоні плитки перемикають регіону набір правил

## Суть
PuzzleScript-гра Jack Lance (2019), за подяками автора — ідея «more or less taken straight from» Nitrome Mega Mash. Уся гра — **одна мапа ≈100×100** з камерою 13×13; вона поділена межами на регіони, і в кожному діють правила однієї з шести міні-ігор (Sokoban, гравітація збоку, злипливі купи над водою, лід, змійка, склеєні блоки). Об'єкти скрізь ті самі — гравець, «річ», стіна, — змінюються лише правила й графіка; річ можна виштовхати з одного регіону в інший, і там вона житиме за новими законами. **Червоні плитки** міняють набір правил регіону на прихований, зокрема на «чорний», де нічого не рухається.

## Поле і час
- Квадратна сітка, вид згори (у регіоні 2 — вид збоку з гравітацією); мапа 102 стовпці × 100 рядків одним рівнем; камера `zoomscreen 13x13` іде за гравцем.
- Кожна клітина має **номер регіону** (видимий набір правил 1–6) і прихований номер (альтернативний набір або «чорний»); номери розливаються від насіння-цифр до меж на ребрах клітин.
- Межі регіонів намальовані лініями; рухові вони не заважають.
- Покроково; ковзання, падіння, перемикання й поїздки тунелями йдуть серіями `again`-кроків без вводу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | регіон під ним | рух 4 напрямки; поведінка залежить від регіону; вигляд — графіка регіону |
| Річ | object | регіон, звʼязки | штовхається; у регіонах 3/6 злипається, у 4 ковзає, у 2 падає, у 5 стає тілом змійки |
| Стіна | static | — | непрохідна; у регіоні 3 це вода/яма: річ туди заходить, гравець — ні |
| Затоплена клітина | terrain | — | купа, що вся над водою, тоне → клітина стає прохідною підлогою |
| Червона плитка (перемикач) | switch | регіон | гравець або річ на ній → регіон міняє видимий і прихований набір правил |
| Регіон 1–6 | zone | видимий / прихований набір | задає правила для всього, що в ньому стоїть |
| Чорний регіон | zone | — | після перемикання стає суцільною чорною стіною; гравець усередині не може рухатись |
| Чекпойнт | static | невидимий | гравець на ньому → точка, куди повертає R |
| Тунель (вхід/вихід) | gate | пара | везе гравця й камеру ланцюжком до далекої частини мапи («Left tunnel» / «Right tunnel») |
| Запобіжник | static | невидимий | річ у забороненій клітині → гра сама відкочує поштовх із повідомленням |
| Фінальна точка | static | — | активна, лише коли не лишилось жодного регіону з прихованим «чорним» набором |
| Літери титрів | static | — | слова з обʼєктів-літер на мапі |

## Правила (КОЛИ → ЯКЩО → ТО)
Спільне:
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(player, dir)`; правила руху — регіону, де стоїть гравець.
- КОЛИ `contact(player, wall)` → ТО `block`.
- Межу регіонів можна перетинати; річ, що перетнула межу, далі підкоряється правилам нового регіону.

Регіон 1 — Sokoban:
- КОЛИ `contact(player, thing)` → ЯКЩО `cell(thing, zone_1)` і `free(behind)` → ТО `push(thing)`; дві речі поспіль — `block`.

Регіон 2 — гравітація збоку:
- КОЛИ `tick` → ЯКЩО `cell(a, zone_2)` і `free(under_a)` → ТО `fall(a)` (гравець і речі).
- КОЛИ `contact(player, thing)` → ЯКЩО `custom: «збоку»` і `free(behind)` → ТО `push(thing)`.
- КОЛИ `blocked(player)` → ЯКЩО `custom: «збоку стіна або заблокована річ, над нею й над гравцем вільно»` → ТО `custom: «вилізти на сходинку в 1 клітину»`.
- КОЛИ `input(down)` → ЯКЩО `cell(player, zone_2)` → ТО `block`.

Регіон 3 — злипливі купи над водою:
- КОЛИ `after(push)` → ЯКЩО `cell(thing, zone_3)` → ТО `custom: «рухаються всі речі, що торкаються її, і весь ряд попереду»`; будь-яка заблокована — `block` для всієї купи.
- КОЛИ `settled` → ЯКЩО `custom: «жодна річ купи не стоїть на суші»` → ТО `disappear(clump)`, `set_cell(water_cells, floor)` — купа тоне й стає мостом.

Регіон 4 — лід:
- КОЛИ `after(push)` → ЯКЩО `cell(thing, zone_4)` → ТО `slide(thing, dir)` до речі, стіни або гравця.

Регіон 5 — змійка:
- КОЛИ `custom: «регіон стає регіоном 5»` → ТО `attach(player, chain_of_things)` — ланцюжок речей, що торкається гравця, стає тілом.
- КОЛИ `after(move)` → ЯКЩО `cell(player, zone_5)` → ТО `custom: «тіло йде за головою»`; КОЛИ `contact(player, loose_thing)` → ТО `push(loose_thing)`.

Регіон 6 — склеєні блоки:
- КОЛИ `custom: «річ у регіоні 6 поруч з іншою»` → ТО `attach(thing, neighbour)`; КОЛИ `after(push)` → ТО `custom: «рухається вся склеєна група»`.
- КОЛИ `enter(player, zone_6)` → ТО `custom: «гравець рухається далі в напрямку входу до упору; «ноги» тримають його відштовхнутим від опори»` (?).

Перемикачі й чорні регіони:
- КОЛИ `enter(player|thing, toggle)` → ЯКЩО `custom: «перемикач щойно не спрацьовував»` → ТО `custom: «регіон міняє видимий і прихований набори правил»` (`+effect:swap_ruleset`), `sound(switch)`; поки хвиля перемикання йде регіоном, нічого не рухається.
- КОЛИ `enter(player|thing, toggle)` → ЯКЩО `custom: «прихований набір регіону — чорний»` → ТО `set_cell(zone_cells, black_wall)`, `disappear(things_inside)`; гравець усередині — `block` на кожен хід.

Навігація, страховка, перемога:
- КОЛИ `enter(player, checkpoint)` → ТО `checkpoint`; R повертає до останнього.
- КОЛИ `enter(player, tunnel)` → ТО `teleport(player, pair)`, `camera(follow)`, `message(«Left tunnel»|«Right tunnel»)`.
- КОЛИ `enter(thing, forbidden_cell)` → ТО `message(«Hey, are you *trying* to softlock yourself? Let me undo that for you.»)`, `custom: «річ відкочується назад»`.
- КОЛИ `enter(thing, tunnel)` або `enter(thing, bad_cell)` → ТО `message(«…don't… (press Z to undo)»)` та подібні попередження.
- КОЛИ `input(action)` → ЯКЩО `count(hidden_black_zone, =, 0)` → ТО `win`.
- Перемога: усі регіони з прихованим «чорним» набором перемкнуто, потім X. · Поразка: нема; softlock → Z або R до чекпойнта. · Рахунку нема.

## Керування і ввід
- Стрілки — крок; Z — undo без ліміту; R — рестарт **до останнього чекпойнта**, не до початку; X — дія (лише для фіналу).
- Повідомлення радять перед дослідженням іншої зони повернутись R до свіжого чекпойнта, щоб не зіпсувати пазл і не записати чекпойнт поверх.

## Вікна, меню, HUD
- `main-menu` (титул PuzzleScript): ENIGMASH · Jack Lance; start / continue.
- `custom-window` повідомлення: «See link below for credits/thanks», про чекпойнти, тунелі, попередження «Er... that seems like a bad idea», жарт «Oops, puzzle design is hard…», секрет із посиланням на малюнок.
- `game-screen`: вікно 13×13 на велику мапу; кожен регіон — своя палітра й спрайти; межі регіонів — лінії (`+ui:zone-border`); HUD нема.
- Переходи: титул → мапа (усе в одному рівні) → фінал за X.

## Фічі поза полем
- `undo` ∞, `restart-level` до чекпойнта, `save-autosave` (прогрес у браузері; за коментарем гравця, автосейв може «зламати» гру після невдалого чекпойнта).
- `+feature:softlock-guard` — гра сама скасовує явні самоблокування й пише чому.
- Відкритий світ: зони проходяться в довільному порядку; за коментарями, три з чотирьох обовʼязкові, четверта дає секретну «синю X» (?).

## Варіації й родичі
- Nitrome **Mega Mash** — джерело ідеї (кожна ділянка — інша гра).
- [Order of the Sinking Star](order-of-the-sinking-star.md) — велике «схрещування» Sokoban-серій у відкритому світі, теж `+mechanic-crossover`.
- [Toodee and Topdee](toodee-and-topdee.md) — дві системи правил в одній кімнаті, але перемикає їх кнопка, а не плитка регіону.
- Регіони окремо: 1 — [Sokoban](../push-slide/sokoban.md); 2 — [Block Dude](../grid-platformer/block-dude.md); 3 — [Jelly no Puzzle](jelly-no-puzzle.md) (злипання) + `fill-hole`; 4 — [Ice-sliding puzzles](../push-slide/ice-sliding-puzzles.md); 5 — [Snakebird](snakebird.md) / [Snake](../maze-arcade/snake.md); 6 — склеєні групи.
- **Осі варіацій:** де живуть правила (уся гра / рівень / регіон мапи) · як міняються (ніяк / перемикач регіону / кнопка для всіх) · чи переходять обʼєкти між наборами (так — тут) · кінець набору (чорний регіон як «запечатування»).

## Цікавинки для курсу
- Номер регіону в клітині + диспетчер правил за номером (одні обʼєкти, шість наборів правил) — 🥉.
- Розлив номерів регіонів від насіння до меж на ребрах (flood fill з бар'єрами) — 📎.
- Перемикач, що міняє набір правил регіону, і хвиля перемикання, під час якої світ стоїть — 📎.
- Злиплива купа: «рухається вся компонента звʼязності, або ніхто» + тоне, якщо вся над водою — 🥈.
- Запобіжник від softlock: позначені клітини + автовідкат із повідомленням — 🌱; детектор deadlock замість ручних міток — 🥇.
- Камера 13×13 над великою мапою з тунелями-телепортами — 📎.

## Мапа на каталог
- Є: `move-4dir`, `move-by-input`, `keyboard-controls`; `impassable-cells`; `push-object` ↔ регіон 1; `stick-together` ↔ регіони 3 і 6; `inertia-slide` ↔ регіон 4; `gravity-fall` ↔ регіон 2; `body-queue` ↔ змійка регіону 5; `fill-hole` ↔ купа тоне у воді; `button-toggle` ↔ червоні плитки; `teleport` ↔ тунелі; `checkpoint`; `player-camera`; `undo-unlimited`, `restart-level`, `save-autosave`, `sound-effects`.
- **Нема** → пропозиції карток:
  - `+zone-rulesets` «Регіони мапи з різними правилами для тих самих обʼєктів» · game-logic · 🥈 · слоти {rulesets: n, transfer: bool}.
  - `+ruleset-toggle` «Плитка міняє набір правил регіону» · entities/interact · 🥉.
  - `+region-blackout` «Регіон запечатується в стіну» · entities/interact · 🌱.
  - `+softlock-guard` «Автовідкат самоблокування з поясненням» · game-logic/history · 🌱.
  - `+push-chain` (уже пропонувалась) — ряд речей у регіоні 3; `+step-up-climb` — підйом на сходинку в регіоні 2 (як Block Dude); `+mechanic-crossover`, `+open-world-puzzles` (уже пропонувались).

## Пропозиції до словників
- `+cond:in_zone(a, zone)` — А в регіоні виду (повтор; тут замінено `cell(a, zone_N)`).
- `+effect:swap_ruleset(zone)` — регіон обмінює видимий і прихований набір правил.
- `+axis:rules` — нове значення `zoned`: правила залежать від регіону мапи.
- `+ui:zone-border` — лінії меж регіонів (повтор).
- `+feature:softlock-guard` — див. вище.
- `+card:zone-rulesets`, `+card:ruleset-toggle` — див. «Мапа на каталог».

## Джерела
- ⭐ [Грати: Enigmash](https://jacklance.github.io/PuzzleScript/play.html?p=cfdcc6e23f1fb3e9de2fd42fafaf4d4c) — сама гра.
- [Bontegames, 2019-11-05](https://www.bontegames.com/2019/11/enigmash-browser.html) — «one big mashup of puzzles, a true ode to puzzlescript», Z/R; коментарі: два камені поспіль не штовхаються, перемикачі роблять секції чорними й забирають керування, «якщо не з іншої секції», 3 з 4 зон для фіналу, кімната з 6 секцій, автосейв.
- [Код (gist API)](https://api.github.com/gists/cfdcc6e23f1fb3e9de2fd42fafaf4d4c) — правила регіонів `(one)…(six)`, `(TOGGLE)` і обмін `one↔onehide`, `seven` → `sevenwall`, `checkpoin`, тунелі `connector1…7`/`awarpa…d`, `heydontputthatthere`, перемога `[action player][winner]` лише без `hideseven`, `zoomscreen 13x13`, мапа 102×100.
- [Подяки (pastebin)](https://pastebin.com/raw/uxxrRX9w) — Mega Mash; автори графіки/звуків; плейтестери.

## Непевне
- (?) Регіон 6: «ноги» й рух до упору реконструйовано з правил `legs`/`umark6`, грою не перевірено; можлива інша механіка (підпора-стовп).
- (?) Регіон 5: що стається з тілом змійки, коли голова виходить з регіону (у коді `exitmark` — речі тіла на виході зникають?), не перевірено.
- (?) Регіон 2: чи ↑ дає підскок, чи заблокований — у коді явного заборонного правила нема.
- (?) Котрі графічні теми від якого автора — подяки не кажуть.
- (?) У [Order of the Sinking Star](order-of-the-sinking-star.md) серед дизайнерів згадано «Zach Polansky (Enigmash)» — наші джерела дають автором Enigmash Jack Lance; можливо, інша людина або псевдонім.
