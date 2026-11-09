---
title: Hack
slug: hack
aka: [Hack 1.0, Hack 1.0.3, Fenlason's Hack]
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 1982
platforms: [Unix, MS-DOS, Amiga, Game Boy Advance]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hack_(video_game)", best: true, note: "автори й версії, що додав: магазини, класи, ліміт ваги, спецкімнати, пастки, болота, печиво з чутками"}
  - {kind: fandom, url: "https://nethackwiki.com/wiki/Hack_1.0", note: "NetHackWiki: 6 ролей, песик, магазини/зоопарки/сховища, 7 пасток, 62 монстри, числа предметів, відмінності від NetHack"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=hack+1984+roguelike+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-8dir, dungeon-generation, stairs-levels, push-object, hp-damage, inventory, inventory-items, inventory-limit, item-pickup, item-identification, hunger-clock, permadeath, round-currency, shop-catalog, character-select, thief, console-render, message-log, status-panel, score-records, save-single-slot, +pet-ally, +shopkeeper-shop, +special-rooms, +maze-levels-deep, +rumor-hints, +ball-and-chain]
proposes: ["+cond:in_shop(a)", "+cond:unpaid(item)", "+effect:bill(item)", "+effect:anger(a)", "+effect:tame(a)", "+role:shopkeeper", "+role:pet", "+feature:role-select", "+card:special-rooms"]
author: opus
date: 2026-11-09
---

# Hack — перехідна ланка Rogue → NetHack: улюбленець, магазини з продавцем, валуни й спецкімнати

## Суть
Hack (1982, Jay Fenlason з однокласниками; з 1984 — версії Андріса Брауера) — роглайк на основі [rogue](rogue.md), що додав у жанр **мешканців зі своїми правилами**: улюбленця, який бʼється за героя, і продавця, що стереже магазин. Тут же зʼявились ролі героя, валуни, які штовхають, спецкімнати (магазини, скарбниці-зоопарки, сховища з охоронцем) і ліміт ваги замість ліміту слотів. Цей файл — лише про різницю: базовий цикл (поверхи, голод, ідентифікація, permadeath) — у rogue.md, наступник — у [nethack](nethack.md).

## Поле і час
- Як у Rogue: ASCII-сітка, кімнати з коридорами, сходи вниз/вгору, покроково, 8 напрямків.
- Нове: підземелля без розгалужень (один шлях вниз), приблизно перші 25 поверхів — кімнати, глибше — **лабіринти**; Амулет Єндора — під валуном на поверсі-лабіринті.
- Нове на поверхах: спецкімнати, болота, склепи (за Wikipedia), 7 типів пасток.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | роль, рівень досвіду до 14, HP, AC, Str, вага ноші | як у Rogue + ліміт ваги |
| Ролі (6) | player | Tourist, Speleologist, Fighter, Knight, Cave-man, Wizard | різний стартовий набір і здібності |
| Песик (стартовий улюбленець) | ally | — | ходить за героєм, бʼється з монстрами |
| Продавець (shopkeeper) | neutral | гаманець обмежений | стоїть у дверях магазину; за крадіжку — розлючений і дуже сильний |
| Охоронець сховища (guard) | neutral | — | приходить, якщо герой у сховищі із золотом (?) |
| Магазин | zone | товари з цінами | взяте — в борг; вийти, не заплативши = крадіжка |
| Скарбниця-зоопарк (treasure zoo) | zone | сплячі монстри + золото | розбуджені — нападають гуртом |
| Сховище (vault) | zone | золото, замкнене | закрита кімната без входу |
| Валун | object | — | штовхається, якщо за ним вільно; Амулет — під одним із них |
| Пастки (7) | hazard | bear trap, arrow, dart, trapdoor, teleport, pit, sleeping gas | спрацьовують на вхід |
| Болото | terrain | — | особлива місцевість (?) |
| Залізна куля й ланцюг | object | важкі | прикуті до героя, тягнуться за ним (?) |
| Печиво з передбаченням | pickup | — | загадкова чутка-підказка |
| Золото й самоцвіти | pickup | вага | рахунок при смерті, але важать |
| Довгий черв, вампус | enemy | — | лише якщо гра зібрана без NOWORM |
| Монстри (62, включно з продавцем і охоронцем) | enemy | — | хобгобліни, лепрекони, кислотні слизні, кажани, кентаври, хамелеони, дракони, привиди, імпи, тролі… |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `choose(role)`, `spawn(little dog, near hero)`.
- КОЛИ `turn_end(hero)` → ТО `custom: «улюбленець іде за героєм і атакує сусідніх ворогів»`.
- КОЛИ `contact(hero, boulder)` → ЯКЩО `free(cell behind)` → ТО `push(boulder)`; інакше `block`.
- КОЛИ `input(pick up)` → ЯКЩО `custom: «вага ноші + предмет ≤ ліміт»` → ТО `pickup`; інакше `block`.
- КОЛИ `picked(hero, item)` → ЯКЩО `custom: «предмет у магазині»` → ТО `custom: «додати в рахунок»`.
- КОЛИ `input(pay)` → ЯКЩО `has(hero, gold ≥ bill)` → ТО `currency(−bill)`, `custom: «товар твій»`.
- КОЛИ `leave(hero, shop)` → ЯКЩО `custom: «є неоплачене»` → ТО `custom: «продавець розлючений і сильний»`, атакує.
- КОЛИ `custom: «продаж продавцю»` → ЯКЩО `custom: «у гаманці продавця достатньо»` → ТО `currency(+n)`; інакше менше (обмежений гаманець).
- КОЛИ `enter(hero, treasure zoo)` → ТО `custom: «монстри прокидаються»` (?).
- КОЛИ `enter(mob, trap)` → ТО за типом: `stun` (bear trap), `damage` (arrow/dart/pit), `custom: «падіння на поверх нижче»` (trapdoor), `teleport` (teleport), `set_state(sleep)` (sleeping gas).
- КОЛИ `input(eat fortune cookie)` → ТО `message(rumor)`.
- КОЛИ `timer(every)` → ТО `custom: «голод»` (як у Rogue); ЯКЩО `custom: «їжа = 0»` → ТО `lose`; трупи монстрів («dead foo») — теж їжа.
- КОЛИ `custom: «зброя на імʼя Orcrist»` → ЯКЩО `custom: «ціль — орк»` → ТО `damage(+d10)`.
- КОЛИ `custom: «досвід»` → ТО `custom: «рівень, здібності, рахунок і апетит ростуть»`.
- КОЛИ `custom: «Амулет Єндора в руках»` і `reach(hero, surface)` → ТО `win` (?).
- КОЛИ `died(hero)` → ТО `lose`, `score(gold + gems)`.

## Керування і ввід
- Однолітерні команди Rogue (рух `hjklyubn`, `,`/`i`/`e`/`q`/`r`/`z` тощо) — без змін по суті (?).
- Нове: оплата в магазині, вибір ролі на старті.

## Вікна, меню, HUD
- `game-screen`: ASCII-поле, `message-log` угорі, `status-line` унизу: «Level 1 Hp 15(15) Ac 9 Str 16 Exp 1».
- `character-select`: вибір однієї з 6 ролей.
- `inventory-window`, `end-screen` з таблицею рекордів — як у Rogue.

## Фічі поза полем
- Save-and-quit, рекорди (як у Rogue); ліцензія BSD, код розповсюджують з Unix-системами.
- Порти: MS-DOS (Don Kneller), Amiga з тайлами, Game Boy Advance.

## Варіації й родичі
- Лінія: [rogue](rogue.md) (1980) → Hack (1982; Brouwer 1.0 — грудень 1984, 1.0.3 — липень 1985) → [nethack](nethack.md) (1987).
- Чого в Hack ще нема порівняно з NetHack: розгалужень підземелля, Чарівника Єндора, харизми, живих ящірок; лише один артефакт (Orcrist).
- Осі варіацій: **NPC з правилами** (нема / улюбленець / продавець-охоронець) · **ліміт ноші** (слоти / вага) · **глибокі поверхи** (кімнати / лабіринти).

## Цікавинки для курсу
- Улюбленець: союзний AI, що тримається біля героя й атакує сусідніх ворогів — 📎.
- Магазин: зона з рахунком, борг за взяте, перевірка на виході, обмежений гаманець продавця — 📎.
- Спецкімнати як шаблони генерації (магазин, зоопарк, сховище) поверх звичайної генерації кімнат — 🥉.
- Ліміт ваги замість ліміту слотів: золото важить — 🌱.
- Печиво-чутки: таблиця підказок випадково — 🌱.

## Мапа на каталог
- Є: `move-8dir` · `dungeon-generation` · `stairs-levels` · `push-object` (валуни) · `hp-damage` · `inventory` / `inventory-items` / `inventory-limit` (вага) · `item-pickup` · `item-identification` · `hunger-clock` · `permadeath` · `round-currency` · `shop-catalog` · `character-select` (ролі) · `thief` (лепрекон (?)) · `console-render` · `message-log` · `status-panel` · `score-records` · `save-single-slot`.
- **Нема** → пропозиції карток:
  - `+pet-ally` · `+shopkeeper-shop` (як у NetHack).
  - `+special-rooms` «Кімнати-шаблони: магазин, зоопарк, сховище» · levels/generation · 🥉.
  - `+maze-levels-deep` «Глибше певного поверху — лабіринти замість кімнат» · levels/generation · 📎.
  - `+rumor-hints` «Випадкова підказка з таблиці (печиво)» · interface/hud · 🌱.
  - `+ball-and-chain` «Прикута куля, яку тягнеш» · entities/move · 📎.

## Пропозиції до словників
- `+cond:in_shop(a)` — сутність у зоні магазину; `+cond:unpaid(item)` — предмет не оплачено.
- `+effect:bill(item)` — додати в рахунок; `+effect:anger(a)` — NPC стає ворожим; `+effect:tame(a)` — приручити.
- `+role:shopkeeper` — нейтрал, що стереже зону й стає ворогом за крадіжку; `+role:pet` — союзник, що йде за героєм.
- `+feature:role-select` — вибір ролі зі стартовим набором.
- `+card:special-rooms`.

## Джерела
- ⭐ [Wikipedia: Hack](https://en.wikipedia.org/wiki/Hack_(video_game)) — автори (Fenlason, Woodland, Thome, Payne; Brouwer), дати, що додано (магазини, ролі, ліміт ваги, золото й самоцвіти в рахунок, магазини/склепи/сховища/пастки/болота, печиво з чутками), перелік монстрів, рядок стану, порти.
- [NetHackWiki: Hack 1.0](https://nethackwiki.com/wiki/Hack_1.0) — 6 ролей, рівень до 14, песик, магазини/зоопарки/сховища, гаманець продавця, 7 пасток, 62 монстри, ~25 поверхів кімнат і далі лабіринти, Амулет під валуном, Orcrist, кількості предметів, відмінності від NetHack.

## Непевне
- (?) Мета: Wikipedia — «забрати Амулет, увійшовши в Пекло», NetHackWiki — Амулет під валуном на поверсі-лабіринті; чи треба його винести нагору — не перевірив.
- (?) Поведінка зоопарку (сплячі монстри), охоронця сховища, болота й кулі з ланцюгом — з памʼяті про NetHack; для Hack 1.0 не перевірено.
- (?) Набір команд Hack 1.0 і що саме з них нове відносно Rogue — джерела не дають.
- (?) Лепрекон краде золото — з памʼяті.
