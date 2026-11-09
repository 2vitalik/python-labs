---
title: Shining Force
slug: shining-force
aka: ["Shining Force: The Legacy of Great Intention", "Shining Force: Resurrection of the Dark Dragon"]
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 1992
platforms: [Mega Drive/Genesis, GBA (ремейк 2004), PC, iOS, Wii VC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Shining_Force", best: true, note: "черга ходу за спритністю + випадковість, одна дія після руху, промоція, без Game Over, смерть Макса, Egress, ремейк GBA"}
  - {kind: other, url: "https://tartarus.rpgclassics.com/shiningforce/howtoplay.shtml", note: "RPGClassics How to Play: команди бою, меню опцій, Land Effect, EXP 100/рівень, церква, штаб, крамниця, тріщини предметів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Shining+Force+Genesis+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [piece-move-patterns, reachable-highlight, melee-vs-ranged, hp-damage, status-effects, unit-xp-skills, inventory-items, inventory-limit, shop-between-levels, shop-catalog, shop-buyback, destroy-all-enemies, reach-exit, player-death, sequential-levels, save-multi-slot, map-window, character-select, +initiative-order, +terrain-bonus, +class-promotion, +leader-death-lose, +retreat-keep-xp, +item-durability, +cursed-equipment, +revive-at-church, +party-reserve]
proposes: ["+trigger:unit_turn", "+effect:choose_promotion", "+effect:revive", "+effect:return_to_town", "+effect:repair", "+cond:agility", "+role:leader", "+ui:land-effect", "+ui:turn-order-bar", "+window:church", "+window:headquarters", "+window:battle-options"]
author: opus
date: 2026-11-09
---

# Shining Force — консольна SRPG без фаз сторін: юніти обох армій ходять по одному в черзі за спритністю

## Суть
Загін Шайнінг Форс (до ~12 у бою) воює на квадратних картах проти армій ШІ. Головна відмінність від Fire Emblem чи Advance Wars — **немає фаз сторін**: усі юніти, свої й ворожі, впорядковані в одну чергу за спритністю (AGI) з випадковим зсувом, тож ходи перемежовуються. Кожен юніт: рух у межах Move → одна дія (атака, магія, предмет, чекати). Поразка не карає назавжди: полеглих воскрешають у церкві, досвід зберігається навіть після втечі з бою.

## Поле і час
- Квадратна сітка, один юніт на клітину; ландшафт впливає на рух і дає **Land Effect** (захисний бонус у %), літуни ігнорують ціну руху.
- `turn-structure: sequential` — раунд = черга всіх юнітів за AGI + випадкове зерно; ворожі юніти ходять по одному за тими ж правилами.
- Видно всю карту (туману нема); меню «Map» показує розстановку (червоні — вороги, зелені — свої).
- Між боями — режим дослідження: Макс ходить світом (міста, розмови, скрині); лабіринтів майже нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Макс (герой) | piece | HP, MP, ATT, DEF, AGI, MOV, EXP, клас | загибель = поразка в бою |
| Боєць загону | piece | клас (лицар, лучник, маг, лікар, птахолюд…), рівень | рух + одна дія; EXP за атаку/лікування |
| Лікар / маг | piece | MP, список заклять | Heal / атакувальна магія з зоною |
| Літун | piece | — | ігнорує штраф ландшафту на рух |
| Ворожий юніт | enemy | ті самі стати | ходить у спільній черзі |
| Ворожий лідер | boss | — | у частині боїв: убити = перемога |
| Ландшафт (рівнина, ліс, гори, пісок…) | terrain | Land Effect %, ціна руху | захист і сповільнення |
| Скриня / прихований предмет | pickup | — | Search поруч / на клітині |
| Церква | static | — | Save · Promote · Raise · Cure |
| Штаб (HQ) | static | — | Advice · Item · Join (заміна складу) · Status |
| Крамниця | static | — | Buy · Sell · Deals · Repair |
| Зброя / кільце | object | тріщина | може тріснути → ремонт, інакше ламається; кільця унікальні |
| Проклятий предмет | object | — | не знімається до зняття прокляття |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «початок раунду»` → ТО `custom: «черга всіх юнітів за AGI × випадковий множник»`.
- КОЛИ `custom: «черга дійшла до юніта»` → ЯКЩО `turn_of(player)` → ТО `custom: «показати зону руху (MOV з ціною ландшафту)»`; інакше хід ШІ.
- КОЛИ `input(move, unit, cell)` → ЯКЩО `custom: «клітина в зоні руху»` і `free(cell)` → ТО `move`.
- КОЛИ `input(cancel)` після руху → ЯКЩО `custom: «дію ще не обрано»` → ТО `custom: «юніт повертається на старт»`.
- КОЛИ `input(attack, target)` → ЯКЩО `in_range(unit, target, weapon_range)` → ТО `damage(ATT − DEF з урахуванням Land Effect цілі)` (?), `end_turn`.
- Удар: `prob(AGI-залежна)` → `custom: «промах / ухил»`; `prob(p)` → `custom: «критичний удар»`; `prob(p)` → `custom: «подвійна атака / контратака цілі»` (?).
- КОЛИ `input(magic, spell, area)` → ЯКЩО `has(unit, MP ≥ ціна)` → ТО `damage(n)` / `heal(a, n)` / `set_state(a, s)` у зоні, `end_turn`.
- КОЛИ `input(item, use|give|equip|drop)` → ТО ефект; `give` лише сусідньому; `equip`/`drop` не витрачає дію, `use`/`give` — витрачає (?).
- КОЛИ `input(search)` → ЯКЩО `custom: «скриня/схованка на клітині»` → ТО `pickup`.
- КОЛИ `custom: «атака / лікування / магія»` → ТО `counter(EXP, +n)`; `counter(EXP, ≥, 100)` → `custom: «level up: усі стати ростуть випадково»`, `counter(EXP, =0)`.
- КОЛИ `input(promote)` у церкві → ЯКЩО `level(≥, 10)` → ТО `transform(unit, promoted_class)`, `custom: «рівень = 1, стати −фіксована частка»`.
- КОЛИ `hp_zero(ally)` → ТО `disappear_a` до кінця бою; `custom: «у церкві — Raise за гроші»`.
- КОЛИ `hp_zero(Max)` → ТО `lose` у бою, `currency(−половина)`, `custom: «повернення в останню церкву з досвідом»` (?).
- КОЛИ `input(egress)` або `custom: «Angel Wing»` → ТО `custom: «втеча з бою в місто, EXP зберігається»`.
- КОЛИ `custom: «використання тріснутого предмета»` → ЯКЩО `not custom: «відремонтовано»` → ТО `disappear_a` (зламано).
- КОЛИ `input(equip, cursed)` → ТО `set_state(unit, cursed)`; знімається `input(church, cure)` або закляттям Detox.
- КОЛИ `all_gone(enemy)` → ТО `win`; КОЛИ `died(enemy_leader)` → ТО `win` (у таких боях); КОЛИ `reach(Max, point)` → ТО `win` (у боях-проривах).
- Перемога: знищити всіх / лідера / дійти до точки · Поразка: загинув Макс (без Game Over — штраф грошима) · Рахунок: —.

## Керування і ввід
- D-pad + A/B/C. На ході юніта: підсвічена зона руху, курсор → клітина → меню хрестом: Attack · Magic · Item · Stay.
- A/C на порожній клітині → меню опцій: Map · Message (вкл/викл повідомлення) · Quit (сейв і вихід) · Speed (швидкість тексту 1–4).
- Курсором можна оглянути статистику будь-якого юніта.
- Поза боєм: хрест-меню Talk · Item · Magic · Search; Item → Use · Give · Equip · Drop.

## Вікна, меню, HUD
- `splash-screen` → `save-slots` (вибір сейву / нова гра).
- `game-screen` (бій): карта, курсор, `reachable-highlight`, хрест-меню команд; панель юніта (HP/MP, рівень); `custom-window` з Land Effect під курсором (?).
- `custom-window` «Battle scene» — бокова сцена удару з анімацією й HP обох.
- `custom-window` «Battle options»: Map · Message · Quit · Speed.
- `map-window` — уся карта з позначками сторін.
- `stats-window` / `inventory-window` — статистика й чотири слоти предметів юніта (?).
- `custom-window` «Church»: Save · Promote · Raise · Cure.
- `custom-window` «Headquarters»: Advice · Item · Join · Status — `character-select` складу на бій.
- `shop-window`: Buy · Sell · Deals (рідкісні товари) · Repair.
- `dialogue-window` — розмови в містах.
- Переходи: місто ↔ світ → бій → (перемога) місто наступної глави / (Egress, смерть Макса) церква.

## Фічі поза полем
- `save-slots` у церкві; Quit у бою — сейв посеред бою (suspend).
- `levels-sequential` по главах; повернення в міста; повторні бої після втечі (досвід зберігається).
- `custom-difficulty` у GBA-ремейку: кожне проходження додає зірку й посилює ворогів; там же черга ходу показана списком, нові персонажі й юніт з картами.
- Склад: резерв у штабі, у бій — обмежена кількість (?); `unlockables`: приховані персонажі за діалоги/місця.

## Варіації й родичі
- Серія: Shining in the Darkness (данжен-кроулер), Shining Force II (Caravan замість штабу, відкритий світ), Shining Force CD, Gaiden; GBA-ремейк Resurrection of the Dark Dragon.
- Родичі: [fire-emblem](fire-emblem.md) (фази сторін, остаточна смерть), [langrisser](langrisser.md), [final-fantasy-tactics](final-fantasy-tactics.md) (CT-шкала), [disgaea](disgaea.md), [tactics-ogre](tactics-ogre.md) (Wait Turn — теж черга за швидкістю).
- **Осі варіацій**: структура ходу — фази сторін (FE/AW) / черга за спритністю (SF) / шкала часу CT (FFT) · смерть — остаточна (FE) / воскресіння за гроші (SF) · поразка — Game Over / штраф і повернення.

## Цікавинки для курсу
- Спільна черга ходу всіх юнітів за AGI × випадковий множник — 🌱 (сортування з шумом).
- Land Effect як % зменшення шкоди + ціна руху ландшафту (BFS з вагами) — 📎.
- Промоція класу з ресетом рівня і зниженням статів — 🌱.
- Предмети, що тріскають і ламаються без ремонту; прокляте спорядження — 🌱.
- Поразка без Game Over: штраф і відкат у церкву, EXP лишається — 🌱.
- ШІ ворога, що ходить по одному в спільній черзі (ціль — найслабший у досяжності) — 📎.

## Мапа на каталог
- Є: `piece-move-patterns` · `reachable-highlight` · `melee-vs-ranged` (списи/луки/магія) · `hp-damage` · `status-effects` (отрута, сон, прокляття) · `unit-xp-skills` · `inventory-items` + `inventory-limit` · `shop-between-levels` + `shop-catalog` + `shop-buyback` (Sell) · `destroy-all-enemies` · `reach-exit` · `player-death` (Макс) · `sequential-levels` · `save-multi-slot` · `map-window` · `character-select` (Join у штабі).
- **Нема** → пропозиції карток:
  - `+initiative-order` «Спільна черга ходу за швидкістю» · game-logic/opponent · 🌱.
  - `+class-promotion` «Промоція класу з ресетом рівня» · entities/state · 🌱.
  - `+leader-death-lose` — спільна з корпусом (смерть Макса).
  - `+retreat-keep-xp` «Втеча з бою зі збереженням досвіду» · game-logic/lose · 🌱.
  - `+item-durability` «Тріщина → ремонт або злам» · entities/state · 🌱.
  - `+cursed-equipment` «Предмет, що не знімається» · entities/state · 🌱.
  - `+revive-at-church` «Воскресіння полеглих за гроші» · game-logic/economy · 🌱.
  - `+party-reserve` «Резерв загону поза боєм» · entities/state · 🌱.
  - `+terrain-bonus` — спільна з AW/FE.

## Пропозиції до словників
- `+trigger:unit_turn` — настав хід конкретного юніта в черзі ініціативи (на відміну від `turn_start(side)`).
- `+effect:choose_promotion` — промоція (уже просить корпус); `+effect:revive` — воскресити полеглого; `+effect:return_to_town` — відкат у місто; `+effect:repair` — відновити тріснутий предмет.
- `+cond:agility` — порівняння спритності (порядок, ухил).
- `+role:leader` — юніт, чия загибель = поразка (Макс).
- `+ui:land-effect` — % захисту клітини; `+ui:turn-order-bar` — черга ходів (GBA-ремейк).
- `+window:church` — сервіси церкви; `+window:headquarters` — штаб і склад; `+window:battle-options` — опції посеред бою.

## Джерела
- ⭐ [Wikipedia: Shining Force](https://en.wikipedia.org/wiki/Shining_Force) — черга ходу (AGI + випадкове зерно), одна дія після руху, EXP, промоція 10–20 з ресетом, цілі боїв, без Game Over, Макс і половина грошей, Egress, ремейк GBA.
- [RPGClassics: How to Play](https://tartarus.rpgclassics.com/shiningforce/howtoplay.shtml) — команди Attack/Magic/Item/Wait, меню Map/Message/Quit/Speed, Land Effect, ATT/DEF/AGI, 100 EXP/рівень, промоція з 10, меню поля, штаб, церква, крамниця з Deals і Repair, тріщини, прокляття.
- YouTube: пошук «Shining Force Genesis gameplay».

## Непевне
- (?) Формула шкоди (ATT − DEF, вплив Land Effect у % саме як множника) — з памʼяті.
- (?) Подвійна атака і контратака у SF1 — з памʼяті (точно є в SF2).
- (?) Розмір активного загону в бою (~12) і місткість інвентаря (4 предмети) — з памʼяті.
- (?) Повернення після смерті Макса — «в останню церкву» з памʼяті; Wikipedia каже лише про втрату половини грошей.
- (?) Чи витрачає дію Use/Give предмета — RPGClassics: «будь-яка команда завершує хід»; Wikipedia: equip/drop — не дія.
- (?) Множник випадковості AGI 50–150 % відомий лише для SF2 (фанатський розбір).
