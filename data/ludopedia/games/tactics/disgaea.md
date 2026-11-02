---
title: "Disgaea: Hour of Darkness"
slug: disgaea
family: tactics
also: [roguelike]
klass: figure
axes:
  field: iso
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 2003
platforms: [PS2, PSP, DS, PC, PS4, Switch, iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Disgaea:_Hour_of_Darkness", best: true, note: "Geo Panels/Symbols, ланцюги, підняти й кинути, базова панель, Item World, Dark Assembly"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Disgaea", note: "серія: командні атаки, стоси, бонус-шкала, рівні до 9999"}
  - {kind: fandom, url: "https://disgaea.fandom.com/wiki/Special:Search?query=Geo+Panel", note: "пошук по вікі серії"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Disgaea", note: "пошук; Disgaea PC (2016) і Complete"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=disgaea+hour+of+darkness+geo+panel+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [hp-damage, legal-move-highlight, melee-vs-ranged, destroy-all-enemies, floor-types, chain-detonation, cell-transform, interaction-table, combo-multiplier, event-points, shop-between-levels, shop-window, dungeon-generation, sequential-levels, level-select, save-multi-slot, +geo-panels, +lift-throw, +base-panel-deploy, +team-attack, +bonus-gauge, +item-world, +action-queue, +capture-by-throw, +vote-assembly]
proposes: ["+trigger:symbol_destroyed", "+effect:recolor_region", "+effect:lift", "+effect:throw", "+effect:execute_queue", "+cond:color", "+role:geo-symbol", "+axis:field=layers", "+ui:bonus-gauge", "+ui:geo-effect-list", "+window:item-world", "+window:dark-assembly", "+feature:new-game-plus"]
author: opus
date: 2026-11-02
---

# Disgaea — ізометрична тактика, де клітини мають колір і правила, а юнітів можна кидати

## Суть
Загін демонів Лахарля виходить з базової панелі на ізометричну карту й бʼється з ворогами покроково. Ядро незвичності — **Geo Panels**: кольорові клітини з правилами («+50 % атаки», «невразливість», «−20 % HP щоходу»), які задають Geo Symbols; знищення символу перефарбовує панелі й запускає **ланцюгову реакцію** з шкодою. Друге — **підняти і кинути**: юніти носять і кидають одне одного (ворогів, союзників, символи) через карту, будують стоси. Третє — нескінченне прокачування: рівні до 9999, Item World — підземелля **всередині предмета**.

## Поле і час
- Ізометрична сітка з **висотою** клітин (`field: iso`, фактично `layers`): висота обмежує стрибок (Jump) і кидок; карти невеликі (≈10×10–20×20).
- Хід гравця: юніти рухаються й обирають дію в будь-якому порядку; атаки **ставляться в чергу** й розігруються командою Execute (або в кінці ходу) — порядок черги важливий для комбо. Рух можна скасувати, доки юніт не діяв.
- Потім хід ворога (ШІ). Повна інформація; випадковість — влучність, крит, приєднання до командної атаки, захоплення кидком.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Людиноподібні класи (Warrior, Mage, Cleric, Thief, Archer…) | piece | Lv 1–9999, HP/SP/ATK/DEF/INT/SPD/HIT/RES, Move, Jump, Throw | можуть піднімати й кидати; зброя + вміння |
| Монстри (Prinny, Imp, Dragon…) | piece | ті ж + без зброї людського типу | не піднімають (?), але можна кидати; Prinny вибухає при кидку |
| Prinny | piece | — | кинутий — вибухає з шкодою по області |
| Ворог | enemy | ті ж класи | ШІ: атакує досяжних |
| Бос мапи | boss | — | сюжетний; інколи вбити = перемога |
| Базова панель | spawner | до 10 юнітів на карті | звідси виходять юніти; кинутий туди ворог → спроба захоплення |
| Geo Panel | terrain | колір (червоний, синій, зелений, жовтий, фіолетовий…) | має ефект, якщо на панелі цього кольору стоїть Geo Symbol |
| Geo Symbol | object | колір, ефект | поширює ефект на всі панелі свого кольору під ним; можна підняти, кинути, знищити |
| Прозорий символ | object | без кольору | при знищенні панелі стають звичайними |
| Ефекти Geo | zone | — | ATK +50 %, DEF +50 %, Invincible, No Lift, Ally/Enemy Damage 20 %, Ally/Enemy Recover 20 %, EXP +50 %, Warp, Clone (?) |
| Скриня/предмет на карті | container | — | (?) |
| Specialist (резидент предмета) | neutral/enemy | вид, рівень | у Item World: перемога над ним → підпорядкування, бонус статів предмета |
| Gate Keeper | enemy | — | блокує вихід на поверх у Item World |
| Портал (gate) | static | — | вихід з карти Item World на наступний поверх |
| Предмет (зброя, броня) | container | рівень, поверхи всередині | Item World: поверхи = світ усередині предмета |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(deploy, unit)` → ЯКЩО `count(units_on_map, <, 10)` і `free(base_panel)` → ТО `spawn_at(unit, base_panel)`.
- КОЛИ `input(move, unit, cell)` → ЯКЩО `custom: «шлях ≤ Move і перепад висоти ≤ Jump»` → ТО `move`.
- КОЛИ `input(attack|skill, target)` → ТО `custom: «додати в чергу»`; КОЛИ `input(execute)` → ТО черга розігрується по порядку.
- КОЛИ атака → ЯКЩО союзники стоять у сусідніх клітинах навколо атакуючого → ТО `prob(p)`: `custom: «team attack — до 4 учасників»` (більше шкоди, +бонус-шкала).
- КОЛИ атака ближнього бою влучає і ціль вижила → ЯКЩО ціль дістає → ТО `prob(counter)`: контратака (?).
- КОЛИ `input(lift, adjacent_unit|symbol)` → ЯКЩО клас людиноподібний і `not geo(No Lift)` → ТО `custom: «підняти»` (несучий стоїть під ним); піднятий може підняти наступного → стос.
- КОЛИ `input(throw, cell)` → ЯКЩО `in_range(cell, Throw)` і висота дозволяє → ТО `move(lifted, cell)`; кинутий союзник може ще ходити (?); кинутий ворог — без шкоди (?).
- КОЛИ `turn_end` → ЯКЩО юніт досі тримає іншого → ТО `damage(carrier)` (?) (за серією; для D1 — непевно).
- КОЛИ кинутий ворог потрапляє на базову панель → ТО `prob(capture)`: успіх → `set_side(enemy, player)`; провал → ворог убиває тих, хто в панелі (?), і лишається.
- КОЛИ кинутий монстр падає на монстра того ж виду (?) → ТО `merge(a, b → c)` (сильніший).
- КОЛИ `contact(prinny_thrown, cell)` → ТО `custom: «вибух по області»`.
- Geo: КОЛИ `occupied(panel[c], symbol)` → ТО усі панелі кольору `c` отримують ефект символу; ефекти кількох символів сумуються.
- КОЛИ `destroyed(symbol, on panel[c])` → ЯКЩО `color(symbol) ≠ c` → ТО `custom: «панелі кольору c перефарбовуються в колір символу, по черзі від місця знищення»` і `damage(units_on_changed_panels)`, `counter(chain, +1)`; прозорий символ → панелі зникають (стають звичайними).
- КОЛИ перефарбування накриває інший символ → ТО `disappear(symbol)` і його колір/панелі запускають наступну ланку (ланцюг довільної довжини).
- КОЛИ панелей не лишилось → ТО `custom: «Panel Termination Bonus»`: шкода всім ворогам, великий бонус.
- КОЛИ ланка / командна атака / комбо / вбивство → ТО `counter(bonus_gauge, +n)`; кінець карти → нагороди за рівень шкали (предмети, EXP, гроші).
- Item World: КОЛИ `input(enter, item)` → ТО генерація поверху; КОЛИ `contact(unit, gate)` → `next_level` (поверх +1, `item.level +1`); кожен 10-й поверх — бос предмета; вихід — після боса або предметом Mr. Gency's Exit.
- КОЛИ `all_gone(enemy)` → ТО `win` (карта); інші умови — переможи боса. Поразка: усі юніти на карті впали (?) · Рахунок: бонус-шкала.
- Dark Assembly (поза картою): КОЛИ `input(propose, bill)` → ЯКЩО `counter(mana, ≥, cost)` → ТО голосування сенаторів (симпатія ↔ рівень, хабарі); провал → «переконати силою» = бій.

## Керування і ввід
- Курсор по ізометричній сітці (повертання/зум камери), X на юніті → меню: Move · Attack · Special · Lift/Throw · Item · Equip · Status · Defend (?) · End.
- Базова панель → список загону → вийти на карту; повернути юніта — завести на панель.
- Команда **Execute** — розіграти накопичені дії; **End Turn** — розіграти й передати хід.
- Трикутник/кнопка «Geo Effects» — показати ефекти кольорів на карті.

## Вікна, меню, HUD
- `main-menu`: New Game · Load · (Options) → `save-slots`.
- Хаб «Netherworld castle» (`custom-window`): NPC — Rosen Queen (`shop-window` зброї/броні/предметів), Hospital (лікування за гроші, нагороди), Dark Assembly (`custom-window`: пропозиції, сенатори з симпатією синій/червоний, голосування), Character World/Creation (створити юніта за ману), Item World (`custom-window`: вибір предмета, рівень, поверхи), Dimensional Gate (`level-select` епізодів і карт).
- `game-screen`: ізометрична карта; вікно юніта (Lv, HP/SP, стати); `custom-window`/HUD «Geo Effects» (список кольорів і ефектів); **bonus-gauge** (шкала 0–10 з превʼю нагороди); `legal-move-highlight`; `turn-counter`.
- `custom-window` «Attack forecast» — шкода, шанс, учасники командної атаки (?).
- `custom-window` «Stage clear» — бонус-предмети за шкалою, EXP, HL (гроші).
- `dialogue-window` — сюжетні сцени; `end-screen` — Game Over / кінцівки (кілька).

## Фічі поза полем
- `xp-level` до 9999; перевтілення (transmigration/reincarnation) зі скиданням рівня й бонусами (?).
- Item World: процедурні поверхи всередині предмета (до 100) — `dungeon-generation`; Specialists як модулі статів, що переносяться між предметами.
- Dark Assembly: `unlockables` (нові класи, кращий асортимент магазину, нові карти) через голосування.
- `save-slots`, `level-select` (повтор старих карт — фарм), New Game+ (рівні переносяться, кілька кінцівок).
- Створення персонажів (класи відкриваються за умовами); Hospital — нагороди за витрачене лікування.

## Варіації й родичі
- Серія Disgaea 2–7: tower attacks (стоси атакують разом), Magichange, Evility, Cheat Shop.
- Родичі від Nippon Ichi: Phantom Brave, Makai Kingdom, La Pucelle Tactics (Purification); Final Fantasy Tactics / Tactics Ogre (ізометрія + висота).
- **Осі варіацій**: клітина з властивістю — статична (FE ландшафт) / керована кольором і символом (Geo) · переміщення інших — нема / штовхання (ITB) / підняти й кинути · виконання — одразу / черга з Execute · прогресія — кампанія / нескінченний гринд (9999).

## Цікавинки для курсу
- Geo Panels: символ на кольоровій панелі дає ефект усім клітинам цього кольору — 🥉 (карта кольорів + мапа ефектів).
- Ланцюгове перефарбування з шкодою й підрахунком ланок — 🥈 (BFS по кольору, черга символів, каскад).
- Підняти й кинути (стоси, дальність кидка, висота) — 🥈.
- Черга дій з Execute і командні атаки за сусідством — 🥉.
- Item World: процедурні поверхи всередині предмета, кожен поверх підвищує рівень предмета — 🥇 (генерація + звʼязок «прохід ↔ стат»).
- Bonus gauge: шкала за стиль гри з нагородою наприкінці — 📎.
- Захоплення ворога кидком на базову панель з шансом — 📎.

## Мапа на каталог
- Є: `hp-damage` · `legal-move-highlight` · `melee-vs-ranged` · `destroy-all-enemies` · `floor-types` (кольорові панелі як типи підлоги з ефектами) · `chain-detonation` (ланцюг Geo) · `cell-transform` (перефарбування) · `interaction-table` (колір × символ) · `combo-multiplier` (ланцюг/командна атака) · `event-points` (бонус-шкала) · `shop-between-levels` + `shop-window` · `dungeon-generation` (Item World) · `sequential-levels` · `level-select` · `save-multi-slot` · `game-screen` · `main-menu`.
- **Нема** → пропозиції карток:
  - `+geo-panels` «Кольорові панелі з ефектом від символу» · entities/interact · 🥉 · слоти {colors, effects}.
  - `+lift-throw` «Підняти й кинути юніт» · entities/interact · 🥈 · слот {range, stack}.
  - `+base-panel-deploy` «Вихід з бази з лімітом юнітів» · entities/spawn · 🌱 · слот {max_on_map: 10}.
  - `+team-attack` «Спільна атака сусідів» · entities/combat · 📎.
  - `+bonus-gauge` «Шкала бонусу за стиль» · game-logic/score · 📎.
  - `+item-world` «Рівні всередині предмета» · levels/generation · 🥇.
  - `+action-queue` «Черга дій з виконанням» · game-logic/opponent · 🥉.
  - `+capture-by-throw` «Захоплення ворога на базі» · entities/interact · 📎.
  - `+vote-assembly` «Голосування за відкриття» · game-logic/economy · 🥉.

## Пропозиції до словників
- `+trigger:symbol_destroyed` — знищено символ-джерело ефекту (частковий `destroyed`, але запускає каскад).
- `+effect:recolor_region` — перефарбувати всі клітини кольору (з порядком поширення); `+effect:lift` / `+effect:throw` — підняти/кинути сутність; `+effect:execute_queue` — розіграти накопичені дії.
- `+cond:color` — клітина/символ має колір (близько до `same(a, b, color)`).
- `+role:geo-symbol` — обʼєкт-джерело ефекту для зони (можна замінити `object` + `zone`).
- `+axis:field=layers` — підтримую ⏳ `layers` як висоту клітин (Jump, кидок через перепад); тут обрано `iso`.
- `+ui:bonus-gauge` — шкала стилю з превʼю нагороди; `+ui:geo-effect-list` — легенда «колір → ефект».
- `+window:item-world` — вхід у предмет із вибором; `+window:dark-assembly` — голосування сенату.
- `+feature:new-game-plus` — перенесення загону в нове проходження.

## Джерела
- ⭐ [Wikipedia: Disgaea: Hour of Darkness](https://en.wikipedia.org/wiki/Disgaea:_Hour_of_Darkness) — Geo Panels/Symbols, ланцюги, Panel Termination Bonus, підняти й кинути, захоплення, Item World, Dark Assembly.
- [Wikipedia: Disgaea](https://en.wikipedia.org/wiki/Disgaea) — командні атаки, стоси, бонус-шкала, рівні до 9999.
- Steam: пошук «Disgaea» — Disgaea PC і Complete.
- YouTube: пошук «disgaea hour of darkness geo panel gameplay».

## Непевне
- (?) Повний список Geo-ефектів D1 і кольорів — з памʼяті; Wikipedia дає лише приклади (невразливість, −20 % HP).
- (?) Чи бʼє перефарбування лише ворогів чи всіх юнітів на панелях; порядок поширення (спіраллю від символу).
- (?) Tower attack (стос атакує разом) — з'явилось, здається, у Disgaea 2; у D1 стоси — лише для переміщення.
- (?) Злиття однакових монстрів при кидку, шкода тому, хто тримає наприкінці ходу, контратаки, «Defend» — з памʼяті/з опису серії.
- (?) Ліміт 10 юнітів на карті — з памʼяті; Wikipedia про нього мовчить.
- (?) Поверхів у предметі: до 100 (Wikipedia), залежність від рідкості — не перевірено.
