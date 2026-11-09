---
title: Myth Bearer
slug: myth-bearer
aka: []
family: roguelike
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: none
  goal: state
year: 2020
platforms: [PC (Windows)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1453450/Myth_Bearer/", best: true, note: "Moonskull Games (JC Bailey), 10.11.2020, безкоштовно; RPG + пазл, вороги не відроджуються, витрачене зникає назавжди, сиквенс-брейки, режим-виклик після проходження"}
  - {kind: other, url: "https://steamcommunity.com/app/1453450/reviews/?browsefilter=toprated&p=1", note: "відгуки: вороги стоять і не бʼють першими, прогноз втрат обох сторін, добивальний удар без відповіді, рівень-ап = повне HP, світ екранами як у Zelda 1"}
  - {kind: other, url: "https://steamcommunity.com/app/1453450/discussions/0/3194737075887979162/", note: "розробник: «Magic Tower style» — шукати найкращий маршрут, а не єдиний розвʼязок; слабкі вороги — запас лікування"}
  - {kind: other, url: "https://steamcommunity.com/stats/1453450/achievements", note: "16 досягнень: лук, місто, вся мапа, рівень 50, пропуск розділів, Start+"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1453450&count=15&maxlength=4000", note: "новини Steam: v1.21 — R скидає поточну кімнату; анонс Deep Rune як духовного наступника"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Myth+Bearer+Moonskull+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [move-4dir, cell-click, keyboard-controls, hover-highlight, hp-damage, item-pickup, inventory-items, item-identification, round-currency, shop-catalog, respawn, restart-level, save-game, map-window, achievements-window, music-toggle, +deterministic-combat, +damage-preview, +xp-level-up, +flip-screen-rooms, +new-game-plus, +permanent-kills, +sequence-break, +deathless-reward, +wall-hints, +story-world-change]
proposes: ["+effect:fight(a, b)", "+effect:reset_room", "+feature:room-reset", "+feature:deathless-reward"]
author: opus
date: 2026-11-09
---

# Myth Bearer — Magic Tower у відкритому світі: екрани як у Zelda, рівень-ап замість зілля, кожне вбивство назавжди

## Суть
Безкоштовна покрокова пригода JC Bailey (Moonskull Games), попередниця [deep-rune](deep-rune.md). Ядро — [magic-tower](magic-tower.md): вороги стоять на місці, бій передбачуваний, HP — головний ресурс, а гра — пошук найкращого порядку боїв. Замість вежі з поверхами — відкритий світ екранами (як Zelda 1 / Hydlide): локації зʼєднані між собою, можна пропускати сюжетні розділи. Нове відносно ядра: **рівень-ап повністю лікує**, тож слабких ворогів «бережуть» як аптечку, а все зроблене (убиті вороги, зʼїдені зілля, події сюжету) — незворотне.

## Поле і час
- Вид згори, рух сіткою («повільний олдскульний рух по клітинах», відгук); світ — набір екранів без прокрутки, перехід на краю екрана.
- Покроково: вороги не ходять і не атакують першими, бій починає лише гравець.
- Світ один і ручний; сюжетні події змінюють його (нові проходи, альтернативні «стадії» світу наприкінці).
- Видно поточний екран; решту світу — лише відвідавши (досягнення «Reveal the entire map»).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | HP, ATT, DEF, рівень, XP, золото, інвентар | ходить сіткою; атакує кліком; рівень-ап — повне HP |
| Ворог (кажани, сині й червоні слизи, гобліни…) | enemy | HP, ATT, DEF, XP | стоїть, перекриває двері, проходи й предмети; не відроджується |
| Тінь, Вартовий вежі Зора | boss | — | сюжетні бої (досягнення «Shadow?», «The Guardian») |
| Червоне зілля | pickup | +HP | лікування, обмежений запас |
| Лук і стріли | pickup | боєзапас | дистанційна атака (?) |
| Пропуск до міста (City Pass) | pickup | — | відкриває вхід у місто |
| Кільце вправності (Ring of Skill) | pickup | — | у вежі після розділу 7 лише без жодної смерті; у трьох боях його доводиться знімати (?) |
| Спорядження | pickup | +ATT / +DEF | «дуже малі» прирости за дослідження |
| Невідомий предмет | pickup | — | що робить — видно лише після використання |
| Золото | resource | — | обмежене; на зілля (?) |
| NPC / торговець | neutral | — | розмова, крамниця (?) |
| Напис на стіні | static | — | загадкова підказка |
| Секретна стіна | static | — | відкривається огляданням (перша ж камера гри) |
| Кольоровий камінь | static | колір | лише косметика: колір за станом світу (механіку спавну вирізали) |
| Екран | zone | — | край екрана = перехід на сусідній |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(hero, dir)`.
- КОЛИ `input(click, cell)` → ЯКЩО `path_exists(hero, cell)` → ТО `custom: «герой іде шляхом до клітини»`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(cell, enemy)` → ТО `block` (бій і розмова — лише кліком, відгук просить «бити рухом»).
- КОЛИ `input(hover, enemy)` → ТО `custom: «показати стати ворога і втрату HP кожної сторони»` (працює й на далеких ворогів).
- КОЛИ `input(attack, enemy)` → ЯКЩО `custom: «удар героя добиває ворога»` → ТО `disappear(enemy)`, `counter(xp, +n)` — без шкоди герою; інакше `damage(enemy, n)`, `damage(hero, m)` (?).
- КОЛИ `died(enemy)` → ТО `custom: «назавжди — ворог не відроджується»`.
- КОЛИ `counter(xp, >=, next_level)` → ТО `custom: «рівень +1, стати ростуть»`, `heal(hero, full)`.
- КОЛИ `input(use, potion)` → ТО `heal(hero, n)`, `take(hero, potion)`.
- КОЛИ `input(use, item)` → ЯКЩО `custom: «предмет ще не впізнаний»` → ТО `custom: «ефект розкривається лише використанням»`.
- КОЛИ `input(shoot, enemy)` → ЯКЩО `has(hero, bow)` → ТО `take(hero, arrow)`, `custom: «удар здалеку»` (?).
- КОЛИ `input(buy, item)` → ЯКЩО `counter(gold, >=, price)` → ТО `currency(-price)`, `give(hero, item)` (?).
- КОЛИ `contact(hero, city_gate)` → ЯКЩО `has(hero, city_pass)` → ТО `custom: «вхід у місто»`; інакше `block`.
- КОЛИ `input(inspect, wall_text)` → ТО `message(hint)`; КОЛИ `input(inspect, wall)` → ЯКЩО `custom: «секрет»` → ТО `set_cell(wall, floor)` (?).
- КОЛИ `edge(hero)` → ТО `custom: «перехід на сусідній екран»`, `reveal(map_screen)`.
- КОЛИ `custom: «сюжетна подія / новий розділ»` → ТО `custom: «світ змінюється: нові проходи, вороги, стадії»`.
- КОЛИ `reach(hero, area_of_later_chapter)` → ТО `custom: «розділи пропущено»` (заплановані сиквенс-брейки).
- КОЛИ `input(R)` → ТО `custom: «скинути поточну кімнату до стану на вході»` (v1.21).
- КОЛИ `hp_zero(hero)` → ТО `respawn(hero, custom)`, `counter(deaths, +1)` (місце відродження гравець не обирає).
- КОЛИ `reach(hero, tower)` → ЯКЩО `counter(deaths, ==, 0)` → ТО `give(hero, ring_of_skill)`.
- КОЛИ `custom: «фінал сюжету»` → ТО `win`, `unlock(start_plus)`.
- Перемога: пройти сюжет. Поразка: нема — смерть відкидає назад і закриває Кільце вправності та одне досягнення. Рахунку нема.

## Керування і ввід
- Повне керування мишею: наведення підсвічує, з чим можна взаємодіяти; клік — іти, атакувати, оглянути, говорити.
- Рух — опційно WASD або стрілки; контролер не підтримується.
- Наведення на ворога — його стати й прогноз бою; R — скинути кімнату (з v1.21).

## Вікна, меню, HUD
- `game-screen` — екран світу згори, `stat-panel` (HP, ATT, DEF, рівень, XP, золото) (?), `tooltip` зі статами ворога й прогнозом втрат при наведенні.
- `map-window` — мапа світу, що відкривається дослідженням (?).
- `inventory-window` — предмети й спорядження (?).
- `dialogue-window` — NPC, написи на стінах.
- `shop-window` — купівля зілля за золото (?).
- `mode-select` — звичайна гра / Start+ після проходження.
- `achievements-window` — 16 досягнень Steam; `settings-window` — вимкнути музику.
- Переходи: `main-menu` → `game-screen` ⇄ `map-window` / `inventory-window` / `dialogue-window`; фінал → відкривається Start+.

## Фічі поза полем
- Start+ — «unlockable challenge mode» після проходження (`new-game-plus`); у ньому гравці доходять до рівня 78.
- Нагорода за гру без смертей у будь-якому режимі — Кільце вправності.
- Збереження: гра «зроблена під save-scum» — зберегтись, випробувати невідомий предмет, завантажитись (відгук); `cloud-save` Steam.
- `restart-level` у масштабі кімнати (R), `achievements` (16, 4 приховані), `music-toggle`.
- Тривалість — 3–7 годин.

## Варіації й родичі
- [magic-tower](magic-tower.md) — ядро (розробник сам каже «Magic Tower style»); [desktop-dungeons](desktop-dungeons.md) і [drod-rpg](drod-rpg.md) — порівняння з відгуків (DROD RPG — і для самого автора); [deep-rune](deep-rune.md) — духовний наступник того ж автора (бічний розріз, гравітація).
- Відмінності від Magic Tower: світ екранами замість поверхів; лікування рівнем-апом (XP — валюта HP); удар кліком із прогнозом при наведенні; сиквенс-брейки замість лінійної вежі; невідомі предмети; смерть — не кінець, а відкат із втратою нагороди.
- Осі варіацій: **простір** (вежа поверхів / відкритий світ екранів) · **лікування** (зілля / рівень-ап / слабкі вороги як запас XP) · **смерть** (кінець / відродження зі штрафом) · **порядок** (лінійно / сиквенс-брейки).
- Інші родичі: Hydlide, Zelda 1 (структура світу), King's Field (натяки в світі).

## Цікавинки для курсу
- Рівень-ап = повне HP: «добити слабкого зараз чи залишити на потім» — 🌱 (поріг XP + `heal`).
- Прогноз бою при наведенні для обох сторін, добивальний удар без відповіді — 📎.
- Світ екранами зі збереженим станом кожного (убиті, взяті, відкриті) — 🥉 (словник стану на кімнату).
- Скидання кімнати до стану на вході — 📎 (знімок при переході через край).
- Невідомі предмети, що впізнаються використанням — 🌱.
- Нагорода лише для безсмертного проходження — 🌱 (лічильник смертей).
- Розвʼязувач маршруту з рівнями, що лікують, — 👑 (стан = убиті × рівень × HP).

## Мапа на каталог
- Є: `move-4dir` · `cell-click` · `keyboard-controls` · `hover-highlight` · `hp-damage` · `item-pickup` · `inventory-items` · `item-identification` · `round-currency` · `shop-catalog` (?) · `respawn` · `restart-level` (кімната) · `save-game` · `map-window` · `achievements-window` · `music-toggle`.
- **Нема** → пропозиції карток:
  - `+deterministic-combat`, `+damage-preview`, `+xp-level-up` (з `heal_on_level`), `+flip-screen-rooms`, `+new-game-plus` — уже пропоновані корпусом.
  - `+permanent-kills` «Убите й витрачене не повертається у відкритому світі» · game-logic/state · 🌱.
  - `+sequence-break` «Заплановані пропуски розділів сюжету» · levels/progression · 📎.
  - `+deathless-reward` «Предмет/досягнення лише за гру без смертей» · game-logic/score · 🌱.
  - `+wall-hints` «Підказки-написи у світі» · levels/content · 🌱.
  - `+story-world-change` «Сюжетні події переставляють світ» · levels/progression · 📎.

## Пропозиції до словників
- `+effect:fight(a, b)` — атомарний детермінований бій (пропозиція сімʼї Magic Tower).
- `+effect:reset_room` — повернути поточну кімнату до знімка при вході.
- `+feature:room-reset` — рестарт кімнати у відкритому світі (не рівня).
- `+feature:deathless-reward` — нагорода, що зникає після першої смерті.

## Джерела
- ⭐ [Steam: Myth Bearer](https://store.steampowered.com/app/1453450/Myth_Bearer/) — опис: RPG + пазл, назавжди витрачене, сиквенс-брейки, мінлива мапа, миша + WASD, режим-виклик; 16 досягнень, хмара.
- [Steam: відгуки](https://steamcommunity.com/app/1453450/reviews/?browsefilter=toprated&p=1) — стоячі вороги, прогноз бою, добивальний удар, рівень-ап = HP, стріли й зілля, невідомі предмети, Zelda 1, 3–7 годин.
- [Steam: «Impossible to do damageless»](https://steamcommunity.com/app/1453450/discussions/0/3194737075887979162/) — розробник про Magic Tower-логіку маршруту, ATT/DEF, слабкі вороги для лікування.
- [Steam: «How to get ring of skill?»](https://steamcommunity.com/app/1453450/discussions/0/598533649122559088/) і [«Killed all enemies…»](https://steamcommunity.com/app/1453450/discussions/0/6382186451012521860/) — Кільце вправності за гру без смертей, режим Start+.
- [Steam: «Colored rocks»](https://steamcommunity.com/app/1453450/discussions/0/5185299686172027347/) — вирізаний спавн, альтернативні стадії світу, NG+ до рівня 78, Пропуск і Лук під охороною.
- [Steam: «Can't pass the first screen»](https://steamcommunity.com/app/1453450/discussions/0/2965021152102313398/) — взаємодія лише мишею, секрет у стіні першої камери.
- [Steam: досягнення](https://steamcommunity.com/stats/1453450/achievements) · [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1453450&count=15&maxlength=4000) — v1.21, скидання кімнати.
- Покроковий гайд nana: [steamcommunity.com/sharedfiles/filedetails/?id=2772682313](https://steamcommunity.com/sharedfiles/filedetails/?id=2772682313) — агенту віддав 429, не прочитано.

## Непевне
- (?) Бій — один обмін ударами на клік (як у Desktop Dungeons) чи весь бій одразу: відгуки кажуть «скільки HP знімає один твій удар» і «добивальний удар без відповіді».
- (?) Формула бою, чи бʼє герой першим, чи лікують самі вбивства (переказ відгуку: «сильні вороги стають безкоштовними») чи лише рівень-ап.
- (?) Що саме дають лук і стріли, як працює магія («equipment upgrades, magic» — відгук), навіщо знімати Кільце вправності в трьох боях.
- (?) Де відроджується герой і що зберігається після смерті; є чи нема окремих слотів збереження.
- (?) Чи є крамниця з цінами, мапа на весь екран та інвентар-вікно — відгуки згадують золото й «Reveal the entire map», але не інтерфейс.
- (?) `info: partial` — через невідомі предмети й невідвідані екрани; стати ворогів видно наведенням.
