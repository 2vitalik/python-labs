---
title: Ancient Domains of Mystery (ADOM)
slug: adom
aka: [ADOM, Ancient Domains of Mystery Deluxe, ADOM II, JADE, Ultimate ADOM]
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
year: 1994
platforms: [PC (DOS, Windows, Linux, macOS), Amiga, OS/2, BeOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Ancient_Domains_of_Mystery", best: true, note: "корупція й мутації, трави за Life, смітинг, памʼять монстрів, квести й мировоззрення, кінцівки, сейв що стирається"}
  - {kind: other, url: "https://www.roguebasin.com/index.php/ADOM", note: "RogueBasin: оверворлд і Терінйо, напівпостійні рівні, Infinite Dungeon, 50 рівнів Caverns of Chaos, 12 рас × 22 класи, таланти кожні 3 рівні"}
  - {kind: official, url: "https://www.ancientdomainsofmystery.com/2014/01/preparing-adom-for-more-interesting.html", note: "блог автора: швидкість корупції для рівнів 30+ знижено до 80–33 %, нова формула розподілу монстрів"}
  - {kind: other, url: "https://en.wikipedia.org/wiki/List_of_roguelikes", note: "WP-список: роки 1994–2018, платформи"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Ancient+Domains+of+Mystery", note: "пошук; ADOM Deluxe"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=ADOM+Ancient+Domains+of+Mystery+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-by-input, move-8dir, dungeon-generation, stairs-levels, hp-damage, inventory, inventory-items, inventory-limit, item-pickup, item-identification, hunger-clock, status-effects, unit-xp-skills, melee-vs-ranged, explode-area, permadeath, player-death, save-single-slot, score-records, fog-of-war, message-log, status-panel, keyboard-controls, console-render, gui-render, character-select, codex-window, map-window, shop-catalog, round-currency, +overworld-travel, +semi-persistent-levels, +corruption-clock, +mutations, +alignment-shift, +quest-giver, +multiple-endings, +talent-tree, +item-degradation, +smithing-upgrade, +cellular-automaton-rule, +birth-sign]
proposes: ["+trigger:corruption_threshold", "+effect:mutate", "+effect:shift_alignment(dir, n)", "+cond:alignment(op, x)", "+cond:carried(item)", "+role:quest-giver", "+role:herb", "+window:overworld-map", "+window:quest-log", "+window:talent-select", "+ui:corruption-list", "+feature:multiple-endings", "+card:corruption-clock", "+card:overworld-travel", "+card:herb-life-growth"]
author: opus
date: 2026-11-09
---

# ADOM — роглайк з картою світу, квестами й корупцією Хаосу, яка росте з часом і врешті перетворює героя на чудовисько

## Суть
Від [nethack](nethack.md) і [angband](angband.md) ADOM відрізняють три речі: **оверворлд** (карта дикої місцевості з поселеннями й десятком окремих підземель), **сюжет із квестами** (видача залежить від рівня й мировоззрення, спосіб розвʼязання зсуває мировоззрення) і **корупція Хаосу** — прихований годинник забігу. Корупція накопичується з часом, глибиною й носінням хаотичних артефактів, дає мутації (частина корисна, більшість ні) і на максимумі завершує гру. Мета — дійти до Брами Хаосу (Chaos Gate) і закрити її; є й інші, складніші кінцівки.

## Поле і час
- Два масштаби: **карта дикої місцевості** (один крок — великий відрізок часу (?)) і **локальні рівні** (підземелля, поселення); вхід у локацію з карти — окремий рівень.
- Рівні підземель **не більші за екран** — прокрутки нема (RogueBasin).
- **Напівпостійні рівні**: згенерований рівень зберігається до кінця гри й при поверненні такий, яким його лишив. Виняток — Infinite Dungeon: новий рівень на кожних сходах; там не буває вівтарів, сховищ і крамниць.
- Головне підземелля — Caverns of Chaos, 50 рівнів, зі спецрівнями (місто Dwarftown всередині); більшість малих підземель привʼязані до квестів.
- Покроково; швидкість героя й монстрів визначає частоту дій (?). Туман: бачене памʼятається.
- Корупція як другий годинник: росте від ігрового часу; якщо надто довго не закривати Браму, швидкість «різко зростає».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой `@` | player | раса (12), клас (22), стать, стати, HP, PP, рівень, мировоззрення, корупції, таланти | рух 8 напрямків; бій входом у клітину |
| Монстр | enemy | HP, швидкість, досвід | помічає й переслідує; знання про нього накопичується в памʼяті монстрів |
| Хаотична істота | enemy | — | шкодять кинуті зілля cure corruption |
| Нежить | enemy | — | святий символ спалює в попіл |
| Квестодавець (староста, король, NPC) | neutral | які квести дає | видає квест за рівнем / мировоззренням героя |
| Фермер / мешканці поселень | neutral | — | беруть насіння (зсув до lawful) |
| Хаотичний артефакт (сильний) | pickup | — | корумпує власника, поки той його несе |
| Хаотичний артефакт (слабший) | pickup | — | корумпує лише при вдяганні / застосуванні |
| Звичайний предмет | pickup | стан, зачарування | може бути пошкоджений боєм чи пастками; покращується смітингом |
| Особливий артефакт | pickup | — | не псується, але й не покращується |
| Трава | object | вид | росте на деяких рівнях за модифікованим Conway's Life; збирається будь-ким |
| Насіння | pickup | — | посадити (дерево → міст, стріли) або віддати фермеру |
| Сходи `<` `>` | static | — | перехід між рівнями; в Infinite Dungeon — новий рівень |
| Вхід у локацію на карті | static | — | перехід з оверворлду на локальний рівень |
| Брама Хаосу | static | — | закрити → кінцівка; увійти → особливі кінцівки |
| Вівтар | static | бог, мировоззрення | взаємодія з божеством (?) |
| Крамниця | static | — | торгівля (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` на карті світу → ТО `move(hero, dir)`, `custom: «час іде у масштабі карти»` (?); КОЛИ `input(enter)` → ЯКЩО `custom: «на клітині локація»` → ТО `custom: «перейти на локальний рівень»`.
- КОЛИ `custom: «крок на карті»` → ЯКЩО `prob(p)` → ТО `custom: «випадкова зустріч на тактичному рівні»` (?).
- КОЛИ `input(stairs)` → ЯКЩО `custom: «рівень уже відвідано»` → ТО `custom: «завантажити збережений стан рівня»`; ЯКЩО `custom: «Infinite Dungeon»` → ТО `custom: «згенерувати новий рівень»`.
- КОЛИ `tick` → ТО `counter(corruption, +rate)`; ЯКЩО `custom: «рівень підземелля 30+»` → ТО `custom: «rate × 0,8…0,33»` (блог).
- КОЛИ `tick` → ЯКЩО `custom: «Брама Хаосу ще не закрита, час великий»` → ТО `custom: «rate різко зростає»`.
- КОЛИ `tick` → ЯКЩО `has(hero, strong chaotic artifact)` → ТО `counter(corruption, +n)`.
- КОЛИ `input(wield|invoke)` → ЯКЩО `custom: «слабший хаотичний артефакт»` → ТО `counter(corruption, +n)`.
- КОЛИ `counter(corruption, ≥, threshold)` → ТО `custom: «нова мутація»` (вусики, хвіст, змінені частини тіла, магічні здібності).
- КОЛИ `counter(corruption, =, max)` → ТО `lose` («writhing mass of primal chaos», герой — слуга Хаосу).
- КОЛИ `input(throw, potion of cure corruption)` → ЯКЩО `occupied(target, chaos being)` → ТО `damage(n)`.
- КОЛИ `tick` → ТО `custom: «трави на рівні ростуть за модифікованим правилом Life»`; КОЛИ `input(harvest)` → ТО `give(hero, herb)`; ЯКЩО `custom: «навичка / клас»` → ТО `custom: «сильний бонус, можна садити насіння»`.
- КОЛИ `input(give seed, farmer)` → ТО `custom: «мировоззрення трохи до lawful»`.
- КОЛИ `custom: «розмова з NPC»` → ЯКЩО `custom: «рівень героя / мировоззрення підходить»` → ТО `custom: «видати квест»`; КОЛИ `custom: «квест розвʼязано»` → ТО `custom: «зсув мировоззрення за способом розвʼязання»`, нагорода.
- КОЛИ `custom: «бій / пастка / стихія»` → ТО `custom: «предмет пошкоджено або знищено»`; ЯКЩО `custom: «особливий артефакт»` → ТО `block`.
- КОЛИ `input(smith, item)` → ЯКЩО `custom: «навичка смітингу»` → ТО `custom: «покращення предмета»`, `custom: «минає час → корупція»`.
- КОЛИ `died(monster)` → ТО `custom: «досвід; памʼять монстрів поповнюється (HP, досвід, швидкість: мін/макс/середнє)»`.
- КОЛИ `custom: «рівень героя кратний 3»` → ТО `choose(talent)`; ЯКЩО `custom: «пререквізити таланту виконані»` → ТО `custom: «талант доступний»`.
- КОЛИ `custom: «створення героя»` → ТО `custom: «стартові таланти з раси, класу, гороскопа, мани, удачі»`.
- КОЛИ `custom: «вдягнуто прокляте спорядження / стан doomed»` → ЯКЩО `prob(p)` → ТО `lose` (миттєва смерть).
- КОЛИ `contact(hero, chaos gate)` and `input(close)` → ТО `win` (звичайна кінцівка).
- КОЛИ `custom: «герой входить у Браму»` → ТО `custom: «шлях до особливих кінцівок (напівбог, героїчна жертва)»`; хаотична кінцівка вимагає майже повної корупції.
- КОЛИ `hp_zero(hero)` → ТО `lose`; сейв стирається при завантаженні — по суті один сейв на героя.
- Перемога: одна з кількох кінцівок. Поразка: смерть або повна корупція. Рахунок: таблиця рекордів (?).

## Керування і ввід
- Клавіатура, рух — цифровий блок (без нього грати незручно — Wikipedia); одно- й багатолітерні команди.
- Окремі команди карти світу: увійти в локацію, подорож (?).
- Пізні версії: тайли, звук; миша (?).

## Вікна, меню, HUD
- `game-screen`: локальний рівень або карта світу, `message-log` угорі, `stat-panel` унизу (стати, HP/PP, швидкість, ситість, мировоззрення (?)).
- `character-create`: стать → раса (12) → клас (22) → гороскоп/дата народження (?) → стартові таланти.
- `overworld-map` — карта дикої місцевості як ігровий екран іншого масштабу.
- `inventory-window` і паперова лялька спорядження (?); `codex-window` (памʼять монстрів); `quest-log` (?); вибір таланту (`talent-select`).
- Список корупцій / мутацій (`corruption-list`) (?).
- `end-screen`: опис кінцівки / смерті; `leaderboard`.

## Фічі поза полем
- `permadeath`: сейв лише на вихід і стирається при завантаженні.
- Кілька кінцівок (`multiple-endings`): закрити Браму, напівбог, жертва, хаотична.
- Памʼять монстрів як накопичувальна енциклопедія (`codex`).
- Пізні версії (Deluxe): тайли, звук, карта світу в новій графіці; класична версія безкоштовна (текст і графіка).
- Наступники: JADE → ADOM II; Ultimate ADOM. Код закритий навмисно (менше несанкціонованих варіантів).

## Варіації й родичі
- Нащадок [nethack](nethack.md) з більшим сюжетом; оверворлд як ідея — з Omega ([omega](omega.md)).
- Напівпостійні рівні — середина між [nethack](nethack.md) (постійні) і [angband](angband.md) (перегенерація); Infinite Dungeon — Angband-режим усередині ADOM.
- Годинник забігу: корупція ADOM · голод [rogue](rogue.md) · дедлайн [larn](larn.md).
- Осі варіацій: **годинник забігу** (нема / голод / дедлайн / корупція з мутаціями) · **світ** (одне підземелля / мережа підземель на карті) · **персистентність** (повна / напівпостійна / регенерація) · **кінцівки** (одна / кілька за умовами).

## Цікавинки для курсу
- Корупція як прихований таймер з порогами мутацій і зростанням швидкості — 📎 (лічильник + таблиця ефектів).
- Трави, що ростуть за модифікованим Life, на рівні гри — 🥉 (клітинний автомат усередині роглайка).
- Два масштаби карти: оверворлд → локальний рівень зі збереженим станом — 🥉.
- Напівпостійні рівні + один «нескінченний» виняток — 📎 (кеш рівнів за ключем).
- Памʼять монстрів з мін/макс/середнім по спостереженнях — 🌱.
- Квести з умовами видачі й зсувом мировоззрення за способом розвʼязання — 🥈 (стан-машина квестів).
- Таланти з деревом пререквізитів кожні 3 рівні — 📎.

## Мапа на каталог
- Є: `move-8dir` · `dungeon-generation` · `stairs-levels` · `hp-damage` · `inventory` · `item-identification` · `hunger-clock` · `status-effects` (хвороба) · `unit-xp-skills` (навички за зброєю) · `explode-area` (кульові заклинання навколо героя, його не ранять) · `permadeath` · `save-single-slot` · `codex-window` (памʼять монстрів) · `map-window` · `character-select` · `console-render` + `gui-render`.
- **Нема** → пропозиції карток:
  - `+corruption-clock` «Прихований лічильник забігу з порогами мутацій; швидкість росте з часом» · game-logic/lose · 📎 · слоти {rate, thresholds}.
  - `+mutations` «Таблиця випадкових змін героя: плюс і мінус» · entities/state · 📎.
  - `+overworld-travel` «Карта світу як окремий масштаб, вхід у локації» · levels/progression · 🥉.
  - `+semi-persistent-levels` «Рівень генерується раз і кешується до кінця гри» · levels/generation · 📎.
  - `+herb-life-growth` (тег `+cellular-automaton-rule`) «Рослини на рівні ростуть за правилом автомата» · entities/spawn · 🥉.
  - `+alignment-shift`, `+quest-giver`, `+multiple-endings`, `+talent-tree`, `+item-degradation`, `+smithing-upgrade`, `+birth-sign` — одним рядком кожна в «Пропозиціях».

## Пропозиції до словників
- `+trigger:corruption_threshold` — лічильник корупції перейшов черговий поріг.
- `+effect:mutate` — додати герою випадкову мутацію з таблиці.
- `+effect:shift_alignment(dir, n)` — зсув мировоззрення (lawful / chaotic) на N.
- `+cond:alignment(op, x)` — мировоззрення героя (видача квестів, реакція богів).
- `+cond:carried(item)` — предмет просто в інвентарі (не вдягнутий) — ширше за `has`, бо діє пасивно щотіку.
- `+role:quest-giver` — NPC, що видає й приймає квест.
- `+role:herb` — рослина-обʼєкт, що росте сама.
- `+window:overworld-map`, `+window:quest-log`, `+window:talent-select` (памʼять монстрів — це `codex-window`).
- `+ui:corruption-list` — список отриманих мутацій.
- `+feature:multiple-endings`.
- `+card:corruption-clock`, `+card:overworld-travel`, `+card:herb-life-growth`.

## Джерела
- ⭐ [Wikipedia: ADOM](https://en.wikipedia.org/wiki/Ancient_Domains_of_Mystery) — корупція й мутації, хаотичні артефакти, трави за Life, смітинг, памʼять монстрів, квести, мировоззрення, кінцівки, сейв, платформи.
- [RogueBasin: ADOM](https://www.roguebasin.com/index.php/ADOM) — Терінйо, напівпостійні рівні, Infinite Dungeon, Caverns of Chaos (50), розмір рівня = екран, раси/класи, таланти кожні 3 рівні, школи магії.
- [Блог автора, 2014](https://www.ancientdomainsofmystery.com/2014/01/preparing-adom-for-more-interesting.html) — корупція на рівнях 30+ сповільнена до 80–33 %; формула ймовірності монстрів за рівнем героя й рівнем підземелля.
- [WP: List of roguelikes](https://en.wikipedia.org/wiki/List_of_roguelikes) — роки й платформи.

## Непевне
- (?) Точна формула корупції, пороги мутацій, «ліміт 90 днів» (згадка в коментарі до блогу) — не перевірено.
- (?) Чи час на карті світу йде швидше за локальний і чи є випадкові зустрічі на тактичній мапі — з памʼяті.
- (?) Боги, вівтарі, жертви, молитви, гороскоп за датою народження — RogueBasin лише посилається на сторінку «God»; деталі не читав.
- (?) Як герой сам знімає корупцію (Wikipedia: «обмежено»), хто й як видає конкретні квести — не перевірено.
- (?) Розмітка HUD, наявність миші й журналу квестів у Deluxe — не бачив.
- (?) RogueBasin пише «ten races / twenty classes», а список має 12 і 22; узято 12 × 22 (Wikipedia так само).
