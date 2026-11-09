---
title: "Labyrinth of Refrain: Coven of Dusk"
slug: labyrinth-of-refrain
aka: [Refrain no Chika Meikyuu to Majo no Ryodan, LoR]
family: roguelike
also: [tactics]
klass: hybrid
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: runtime
  goal: state
year: 2016
platforms: [PS Vita (JP 2016), PS4, Switch, PC (2018)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Labyrinth_of_Refrain:_Coven_of_Dusk", best: true, note: "суть: книга-командир, ляльки-солдати, кроки від першої особи, випадкові бої, фасети-класи, переходи в інші світи"}
  - {kind: steam, url: "https://store.steampowered.com/app/566540", note: "ламати стіни, перестрибувати барикади, небезпека росте від зібраного скарбу, загони й формації, синтез, Witch Petitions"}
  - {kind: other, url: "https://www.imore.com/labyrinth-refrain-coven-dusk-beginners-guide", note: "гайд новачка: до 40 ляльок, фасети з ролями, 4 пакти діють разом, Mud Exit"}
  - {kind: other, url: "https://www.rpgsite.net/feature/7772-labyrinth-of-refrain-coven-of-dusk-true-ending-guide", note: "пазли з руйнованими стінами, координати клітин (X, Y), провали на нижній поверх, точки подій"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=labyrinth+of+refrain+coven+of+dusk+gameplay+wall+break", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-by-input, move-4dir, orientation-state, destructible-blocks, impassable-cells, hp-damage, inventory, inventory-items, item-pickup, key-and-door, stairs-levels, fog-of-war, minimap-radar, map-window, character-select, unit-xp-skills, status-effects, player-death, sequential-levels, gui-render, keyboard-controls, +first-person-grid, +wall-break-cost, +random-encounter, +party-formation, +squad-command, +danger-gauge, +barricade-jump, +pit-drop, +return-to-town-item, +gear-synthesis, +town-hub]
proposes: ["+effect:break_wall", "+effect:start_battle", "+effect:return_to_town", "+cond:mana(op, n)", "+trigger:danger_level", "+ui:danger-gauge", "+ui:mana-counter", "+ui:cell-coordinates", "+window:battle-screen", "+window:town-hub", "+window:petition-window", "+window:puppet-create", "+feature:wall-break", "+axis:view=first-person", "+card:wall-break-cost", "+card:danger-gauge"]
author: opus
date: 2026-11-09
---

# Labyrinth of Refrain — клітинний кроулер від першої особи, де майже будь-яку стіну можна проломити за ману, тож топологію лабіринту робить сам гравець

## Суть
Гравець — жива книга Tractatus de Monstrum, яку відьма Дронья посилає в лабіринт під містом; битися ходять **ляльки-солдати** (до 40), згруповані в загони, що атакують разом. Рух — кроками по сітці від першої особи, бої — випадкові й покрокові. Головна незвичність: **стіни ламаються** за ману (Witch Petition), тож будь-яка дорога може стати шорткатом, а будь-який закуток — входом у сховище; планування маршруту = вибір, яку стіну пробити. Небезпека лабіринту росте від зібраного скарбу, тому вчасно повернутися — частина гри.

## Поле і час
- Квадратна сітка з координатами клітин (X, Y), багато поверхів у кількох «світах»-данжах, з'єднаних передпокоями (antechambers).
- Вид від першої особи, загін має орієнтацію; крок = 1 клітина; поворот 90°.
- Покроково: крок = тік; випадкові бої за кроками; фіксовані «точки подій» з боями.
- Шари: підлога/стіни (ламані й неламані) + барикади (перестрибнути) + провали (падіння на нижній поверх) + пастки + скрині.
- Мапа будується автоматично (?), з туманом на невідвіданому.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Tractatus de Monstrum (загін) | player | орієнтація, мана (?), рівень небезпеки | рух як одна фігура; ламає стіни, перестрибує барикади |
| Лялька-солдат | ally | фасет-клас, HP, стати, природа, ріст статів | діє в бою у складі пакту/загону |
| Пакт / ковен (загін ляльок) | ally | до 4 пактів (iMore) | командуєш пактом, не лялькою; пакт атакує й рухається разом |
| Фасет Aster Knight | ally | дворучна зброя | баланс атаки й захисту; витримує один крит |
| Фасет Shinobushi | ally | дві зброї | швидкий, крихкий |
| Фасет Theatrical Star | ally | Spell Bells | підтримка: статуси, лікування щоходу |
| Фасет Peer Fortress | ally | важка броня | танк; лікується в захисті |
| Фасет Marginal Maze | ally | Donum, Eclipse Stands | заклинання підтримки, вогонь/бруд/туман |
| Фасет Mad Raptor | ally | Hyakka Yumi | дальні атаки стихіями (відкривається пізніше) |
| Монстр | enemy | HP, стихії | випадковий бій |
| Бос / подія | boss | — | фіксована точка події на мапі |
| Стіна звичайна | static | ламана за ману | після пролому — підлога |
| Стіна неламана | static | — | межа, `block` (?) |
| Барикада | gate | — | перестрибнути (рух через клітину) |
| Провал | hazard | — | падіння на нижній поверх (у т. ч. прихований поверх) |
| Пастка | hazard | — | у кутах і вузьких місцях (за гайдами) |
| Скриня | container | вміст; деякі — потрібен ключ | дає предмет; підвищує небезпеку (?) |
| Точка скарбу | pickup | — | рідкі предмети лише тут |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(forward|back|strafe)` → ЯКЩО `free(target)` → ТО `move(party, dir)`; інакше `block`.
- КОЛИ `input(turn)` → ТО `face(party, ±90°)`.
- КОЛИ `input(break wall)` → ЯКЩО `cell(ahead, breakable wall)` and `custom: «мана ≥ ціна»` → ТО `set_cell(ahead, floor)`, `custom: «мана − ціна»`; інакше `block`.
- КОЛИ `input(jump)` → ЯКЩО `cell(ahead, barricade)` → ТО `move(party, over barricade)`.
- КОЛИ `enter(party, pit)` → ТО `fall(party)` на нижній поверх.
- КОЛИ `enter(party, trap)` → ТО `damage(n)` або `set_state(party, ailment)` (?).
- КОЛИ `turn_end(party)` → ЯКЩО `rng(p)` → ТО `custom: «випадковий бій»` → `window(battle-screen)`.
- КОЛИ `enter(party, event point)` → ТО `custom: «фіксований бій / подія»`.
- КОЛИ `picked(party, treasure)` → ТО `counter(danger, +n)` (Steam: «що більше скарбу, то небезпечніше»).
- КОЛИ `counter(danger, ≥, threshold)` → ТО `custom: «вороги сильніші / небезпечні монстри»` (?).
- КОЛИ `input(order to pact)` → ТО `custom: «пакт діє як одне ціле: атака, навичка, захист»`; `input(all-out attack)` → ТО `custom: «усі пакти разом»`.
- КОЛИ `input(change formation)` → ТО `swap(pact, pact)` між переднім і заднім рядом (?).
- КОЛИ `hp_zero(puppet)` → ТО `set_state(puppet, down)`; ЯКЩО `count(active puppets, =, 0)` → ТО `lose` (?).
- КОЛИ `input(Mud Exit)` → ТО `teleport(party, base)`, `custom: «скарб зберігається; потім можна повернутись у точку виходу»`.
- КОЛИ `contact(party, chest)` → ЯКЩО `has(party, key)` або `custom: «замка нема»` → ТО `pickup(item)`.
- КОЛИ `input(petition)` (на базі) → ЯКЩО `custom: «досить мани»` → ТО `unlock(skill)` (у т. ч. пролом стін).
- Перемога: пройти сюжетні світи й фінального боса (є справжня кінцівка й пост-гра). Поразка: загинув загін (?).

## Керування і ввід
- Кнопки/клавіші: крок, поворот, стрейф; дія — пролом стіни, стрибок через барикаду, відкрити скриню.
- Бій: команда кожному пакту; спеціальні навички; all-out attack; зміна формації.
- База: створення ляльки (вигляд, імʼя, природа, ріст статів), розподіл по пактах, синтез спорядження, прохання містян, Witch Petitions.

## Вікна, меню, HUD
- `game-screen`: вид від першої особи, `minimap` з координатами (`cell-coordinates`), `danger-gauge` (?), `mana-counter` (?).
- `battle-screen`: вороги, пакти з `hp-bar`, меню команд, `message-log`.
- `town-hub` (база відьми): `petition-window` (купівля навичок за ману), `puppet-create`, склад пактів, синтез, квести містян.
- `inventory-window`, `map-window` (повна мапа поверху) (?).
- `main-menu`, `save-slots` (?), `end-screen`.
- Переходи: база → лабіринт (`game-screen`) ⇄ `battle-screen`; Mud Exit → база.

## Фічі поза полем
- Створення до 40 ляльок, 4 пакти; фасети відкриваються з прогресом.
- Прогресія: рівні ляльок, синтез спорядження, петиції (навички за ману).
- Пост-гра: збережений «clear data» відкриває подальший вміст.

## Варіації й родичі
- Наступник: Labyrinth of Galleria: The Moon Society (той самий рушій).
- Родичі: [etrian-odyssey](etrian-odyssey.md) (той самий жанр, але мапу малюєш ти, стіни — незмінні), [dungeon-master](dungeon-master.md), [legend-of-grimrock](legend-of-grimrock.md); пролом стін як ресурс — споріднено з копанням у [nethack](nethack.md) (кирка) і [cogmind](cogmind.md) (руйнування середовища).
- Осі варіацій: **стіни** (незмінні / руйнуються за ресурс / копаються інструментом / руйнуються вибухами) · **хто б'ється** (герої / загони-юніти) · **тиск часу** (голод / небезпека від зібраного / нема).

## Цікавинки для курсу
- Пролом стіни за ресурс: шлях на мапі як задача найкоротшого шляху з ціною пролому — 🥉 (Dijkstra з вагами стін).
- Небезпека, що росте від зібраного скарбу: «push your luck» — 🌱.
- Загони замість героїв: команда пакту = одна дія кількох ляльок — 📎.
- Провали на нижній поверх і барикади як інші види переходів — 🌱.
- Повернення на базу зі збереженням скарбу й поверненням у точку виходу — 📎.

## Мапа на каталог
- Є: `move-4dir` + `orientation-state` · `destructible-blocks` (стіни, що ламаються) · `impassable-cells` · `hp-damage` · `inventory` · `item-pickup` · `key-and-door` (скрині з ключем) · `stairs-levels` · `fog-of-war` · `minimap-radar` · `map-window` · `unit-xp-skills` · `status-effects` · `player-death`.
- **Нема** → пропозиції карток:
  - `+wall-break-cost` «Пролом стіни за ресурс» · entities/interact · 📎 · слоти {cost, unbreakable}.
  - `+danger-gauge` «Небезпека росте від зібраного» · game-logic/economy · 🌱 · слоти {per_item, threshold}.
  - `+squad-command` «Команда загону = дія кількох юнітів» · entities/combat · 📎.
  - `+barricade-jump` «Перестрибнути барикаду» · entities/move · 🌱.
  - `+pit-drop` «Провал на нижній поверх» · entities/interact · 🌱.
  - `+gear-synthesis` «Синтез спорядження» · game-logic/economy · 📎.
  - Перевикористано: `+first-person-grid`, `+random-encounter`, `+party-formation`, `+return-to-town-item`, `+town-hub`.

## Пропозиції до словників
- `+effect:break_wall` — стіна попереду стає підлогою (з ціною; ширше за `set_cell`, бо є неламані стіни).
- `+effect:start_battle`, `+effect:return_to_town` (як в Etrian Odyssey).
- `+cond:mana(op, n)` — у гравця досить мани.
- `+trigger:danger_level` — рівень небезпеки досяг порогу.
- `+ui:danger-gauge`, `+ui:mana-counter`, `+ui:cell-coordinates`.
- `+window:battle-screen`, `+window:town-hub`, `+window:petition-window` (купівля навичок за ману), `+window:puppet-create`.
- `+feature:wall-break`, `+axis:view=first-person`.
- `+card:wall-break-cost`, `+card:danger-gauge`.

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Labyrinth_of_Refrain:_Coven_of_Dusk) — книга-гравець, ляльки, кроки від першої особи, випадкові бої, фасети, передпокої між світами, дати релізів.
- [Steam](https://store.steampowered.com/app/566540) — пролом стін, барикади, пазли, небезпека від скарбу, загони й формації, синтез, Witch Petitions, all-out attack.
- [iMore: гайд новачка](https://www.imore.com/labyrinth-refrain-coven-dusk-beginners-guide) — до 40 ляльок, ролі фасетів, 4 пакти, Mud Exit.
- [RPG Site: true ending](https://www.rpgsite.net/feature/7772-labyrinth-of-refrain-coven-of-dusk-true-ending-guide) — координати клітин, пазли зі стінами, провал на прихований поверх, точки подій, ключі.

## Непевне
- (?) Ціна пролому в мані, звідки береться мана, чи вона спільна для пролому й інших петицій — пошук показав лише «навички петицій купуються за ману»; деталей не відкрив.
- (?) Як саме діє шкала небезпеки (пороги, що спавниться) — Steam лише каже, що небезпека росте від скарбу.
- (?) Ковен vs пакт: як називаються й скільки ляльок у пакті; чи передній/задній ряд — з памʼяті.
- (?) Неламані стіни (зовнішні/сюжетні), автомапа, умова поразки — з памʼяті.
- (?) Японська транслітерація в `aka` — з памʼяті.
