---
title: "Kingdom Death: Monster"
slug: kingdom-death-monster
aka: [KDM, KD:M, Kingdom Death]
family: tactics
also: [build-sim]
klass: figure
axes:
  field: square
  time: turn
  opponent: coop
  info: hidden
  random: both
  goal: survive
year: 2015
platforms: [board]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Kingdom_Death:_Monster", best: true, note: "три фази (полювання, бій, поселення), колода ШІ монстра, кінець кампанії"}
  - {kind: other, url: "https://rulespal.com/kingdom-death-monster/rulebook", note: "зміст правил: Monster AI, Showdown Round, Monster Turn, Pick Target, Critical Wounds, Survival, Hit Locations"}
  - {kind: other, url: "https://rulespal.com/kingdom-death-monster/faq", note: "FAQ: локації ударів, Failure/Reflex/Trap, сліпа зона, знешкодження, вичерпання колоди ШІ"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Kingdom+Death+Monster+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 50
mechanics: [hp-damage, status-effects, permadeath, inventory-items, shop-between-levels, world-map, sequential-levels, save-progress, +deck-draw, +monster-ai-deck, +hit-location-deck, +facing-hit-bonus, +body-part-armor, +injury-table, +survival-reactions, +knockdown, +settlement-timeline, +gear-grid-adjacency, +crafting-from-loot, +hunt-track, +sanity-meter, +death-countdown]
proposes: ["+trigger:card_drawn", "+trigger:attacked", "+trigger:deck_empty", "+effect:draw_card", "+effect:roll_dice", "+effect:discard", "+cond:in_blind_spot", "+cond:card_says", "+role:card", "+role:settlement", "+ui:ai-deck-counter", "+ui:hit-location-silhouette", "+ui:survival-tokens", "+window:settlement-screen", "+window:gear-grid", "+window:timeline-window", "+window:hunt-board", "+feature:campaign-timeline", "+axis:session:campaign"]
author: opus
date: 2026-11-09
---

# Kingdom Death: Monster — кооп-бій проти монстра, чий «мозок» — колода карт, а здоровʼя — та сама колода

## Суть
Гравці (1–4) ведуть ватагу голих і беззбройних вцілілих у темному світі: полюють на монстра, бʼються з ним на клітинковому полі, а з трофеїв будують поселення й кують спорядження. Поведінку монстра задає **колода ШІ**: на початку бою її тасують, щоходу витягують карту — вона каже, кого атакувати й як. Ця сама колода — його здоровʼя: кожна рана знімає карту, тож що більше поранень, то бідніший його репертуар. Удари вцілілих тягнуть карти з **колоди локацій ударів** — частина з них вмикає реакції монстра чи пастку. Кампанія вимірюється роками-«ліхтарями»; загиблих заміняють новими з поселення, кінець — фінальний бос або населення 0. Тут описано як цифрову версію: офіційної нема.

## Поле і час
- Три фази на рік: **полювання** (Hunt) — доріжка подій, що зближує ватагу з монстром; **бій** (Showdown) — квадратна дошка з місцевістю, монстр на великій основі; **поселення** (Settlement) — подія таймлайну, крафт, винаходи, народження.
- Бій покроковий раундами: хід монстра (витягнути карту ШІ, обрати ціль, рухатись, атакувати) → хід вцілілих (кожен має рух і активацію в будь-якому порядку).
- Монстр має **напрямок** (facing): передня зона огляду і **сліпа зона** за спиною. Розмір основи (квадрат кількох клітин) залежить від монстра (?).
- Інформація: колоди ШІ й локацій закриті й перетасовані; поле відкрите. Випадковість — кубики d10 і колоди.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вцілілий (survivor) | piece | рух, точність, сила, ухилення, удача, швидкість; броня й травми на 5 локаціях; виживання; безумство | рух + активація за хід; атака зброєю, реакції виживання |
| Монстр (квоботуна, лев, антилопа…; рівні 1–3) | boss | рух, токсичність, ухилення, точність, сила, швидкість атаки; колода ШІ = здоровʼя | щоходу карта ШІ: ціль → рух → атака; повертається до цілі |
| Карта ШІ | card | ціль, рух, удар, ефект | визначає дію монстра; знята в стос ран при пораненні |
| Basic Action | card | — | дія монстра за замовчуванням (?) |
| Карта локації удару | card | частина тіла, реакції (Reflex/Failure/Wound), крит | тягнеться за кожне влучання вцілілого |
| Пастка (Trap) | card | — | у колоді локацій: удар зривається, монстр діє (?) |
| Місцевість (каміння, стовп, кущі…) | terrain | — | блокує рух/огляд за правилами карти місцевості (?) |
| Зброя / броня (gear) | pickup | швидкість, точність, сила; ключові слова; кольорові звʼязки | у сітці 3×3 спорядження вцілілого |
| Ресурс (шкура, кістка, орган) | resource | тип, ключові слова | трофей бою; витрачається на крафт і будівлі |
| Поселення | zone | населення, винаходи, будівлі-локації, таймлайн | дає крафт і бонуси; населення 0 = кінець |
| Рана травми (severe injury) | mark | локація | постійна травма з таблиці (зламана рука, втрачене око) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(showdown)` → ТО `custom: «перетасувати колоду ШІ (склад за рівнем монстра) і колоду локацій»`.
- КОЛИ `turn_start(monster)` → ТО `custom: «витягнути верхню карту ШІ»`; карта задає ціль, рух, удар.
- КОЛИ `custom: «карта ШІ витягнута»` → ЯКЩО `custom: «є ціль за пріоритетом карти (найближчий / загроза / у полі зору)»` → ТО `face(monster, target)`, `move(monster, toward target)` до значення руху, атака.
- КОЛИ `custom: «монстр атакує»` → ТО `custom: «кинути d10 × швидкість атаки; влучання = ≥ точність монстра + ухилення цілі»`.
- КОЛИ `custom: «монстр влучив»` → ТО `custom: «кидок локації на вцілілому (голова/руки/тіло/пояс/ноги)»`, `damage(n)` спершу по броні локації, потім травма.
- КОЛИ `custom: «рана понад шкалу локації»` → ТО `custom: «кидок по таблиці тяжких травм»` → `set_state(survivor, injury)` або `lose` для вцілілого.
- КОЛИ `input(attack, survivor, weapon)` → ЯКЩО `in_range(survivor, monster, weapon_range)` → ТО `custom: «кинути d10 × швидкість зброї; влучання ≥ точність зброї + ухилення монстра»`.
- КОЛИ `input(attack, …)` → ЯКЩО `custom: «вцілілий у сліпій зоні монстра»` → ТО `custom: «бонус до влучання»` (?).
- КОЛИ `custom: «вцілілий влучив»` → ТО `custom: «витягнути карту локації за кожне влучання»`, далі `custom: «кидок рани: d10 + сила ≥ стійкість монстра»`.
- КОЛИ `custom: «рана монстру»` → ТО `custom: «верхня карта ШІ → стос ран»`; КОЛИ `custom: «рана, а колода ШІ і скид порожні»` → ТО `disappear_a`, `win` бою.
- КОЛИ `custom: «рана d10 = 10 (ліхтар)»` → ЯКЩО `custom: «карта локації має крит»` → ТО `custom: «критичний ефект з карти»`.
- КОЛИ `custom: «карта локації з Reflex»` → ТО `custom: «реакція монстра незалежно від рани»`; `Failure` → ЯКЩО рану не завдано → ТО реакція.
- КОЛИ `custom: «витягнуто Trap»` → ТО `custom: «удар скасовано, монстр діє негайно, колоду локацій перетасовано»` (?).
- КОЛИ `input(survival, dodge)` → ЯКЩО `has(survivor, survival ≥ 1)` → ТО `take(survivor, survival)`, `custom: «ігнорувати одне влучання»`; аналогічно encourage / surge / dash (?).
- КОЛИ `custom: «вцілілого збито»` → ТО `set_state(survivor, knocked_down)`; `clear_state` наприкінці наступного ходу монстра (?).
- КОЛИ `custom: «шкода по мозку»` → ТО `custom: «зменшити безумство»`; ЯКЩО безумство вичерпано → ТО `custom: «таблиця травм мозку»`.
- КОЛИ `died(survivor)` → ТО `disappear_a`; вцілілий втрачений назавжди; поселення втрачає населення.
- КОЛИ `custom: «бій виграно»` → ТО `give(settlement, resources)`; поразка (усі вцілілі загинули) → `custom: «повернення без трофеїв»`.
- КОЛИ `phase_start(settlement)` → ТО `custom: «подія року з таймлайну»`, `custom: «винаходи, будівлі, крафт за ресурси»`.
- КОЛИ `input(craft, gear)` → ЯКЩО `has(settlement, resources)` and `custom: «є потрібна будівля»` → ТО `take(settlement, resources)`, `give(settlement, gear)`.
- КОЛИ `custom: «спорядження в сітці 3×3»` → ЯКЩО `custom: «кольорові напівзвʼязки сусідніх предметів утворюють повну звʼязку»` → ТО `custom: «бонус спорядження»`.
- КОЛИ `counter(population, ≤, 0)` → ТО `lose` кампанії · КОЛИ `died(final_boss)` → ТО `win` кампанії.
- Перемога: фінальний бос кампанії · Поразка: населення 0 · Рахунок: —.

## Керування і ввід
- (цифрова версія) Вибір вцілілого → підсвітка досяжних клітин → клік; дія «атака» з вибором зброї з сітки спорядження; кидок кубиків анімовано; витягнуті карти показано крупним планом.
- Реакції виживання — кнопки-запити, що зʼявляються, коли монстр влучив (dodge) або в хід вцілілих.
- Поселення — меню будівель і крафту, перетягування предметів у сітку 3×3 вцілілого.
- Кооператив: гравці керують своїми вцілілими по черзі, монстр — колода.

## Вікна, меню, HUD
- (цифрова версія) `main-menu`: Нова кампанія, Продовжити → `save-slots`, Довідка → `help-window`.
- `hunt-board`: доріжка полювання з фігурками ватаги й монстра, карта події.
- `game-screen` (бій): квадратна дошка, монстр з позначеною сліпою зоною, `ai-deck-counter` (скільки карт ШІ = здоровʼя), стос ран, `hit-location-silhouette` вцілілих з бронею й травмами, `survival-tokens`, `turn-indicator`, `message-log`.
- `settlement-screen`: населення, будівлі-локації, винаходи, ресурси; `timeline-window` — роки-ліхтарі з подіями; `gear-grid` — сітка 3×3 вцілілого; `inventory-window` — сховище ресурсів і спорядження.
- `codex-window` — картки монстрів, спорядження, бійцівські мистецтва, розлади.
- `end-screen` бою з трофеями; `end-screen` кампанії.

## Фічі поза полем
- `campaign-timeline` — кампанія з фіксованих подій на роки-ліхтарі; `save-progress` поселення.
- `permadeath` вцілілих; `meta-progression` через поселення (винаходи, будівлі).
- Рівні монстрів 1–3 (`difficulty-presets` на кожне полювання); розширення додають монстрів, карти й спорядження.
- `mode-coop` 1–4 гравці, варіант на 5–6.

## Варіації й родичі
- Родичі: [Gloomhaven](gloomhaven.md) (кооп, монстри за картами дій — пише B003), [HeroQuest / Space Hulk](heroquest-space-hulk.md) (данж-кроул з кубиками), Monster Hunter (полювання → крафт з частин).
- Осі варіацій:
  - **ШІ ворога**: детермінований сценарій / колода карт поведінки (KDM, Gloomhaven) / мінімакс;
  - **здоровʼя боса**: число HP / колода, яка тоншає з ранами і обмежує його ходи;
  - **влучання**: одна таблиця / колода частин тіла з реакціями й пастками;
  - **позиція**: без напрямку / фасінг зі сліпою зоною (KDM, [FFT](final-fantasy-tactics.md)).

## Цікавинки для курсу
- Колода ШІ = здоровʼя: рана знімає карту поведінки — 📎 (колода, стос, перетасування).
- Колода локацій ударів з реакціями Reflex/Failure і пасткою — 🥉 (ланцюг подій, що перериває атаку).
- Сліпа зона великого монстра з напрямком і поворотом до цілі — 🥉 (геометрія багатоклітинної основи на сітці).
- Броня й травми по 5 локаціях тіла з таблицею тяжких травм — 📎.
- Сітка спорядження 3×3 з кольоровими звʼязками сусідів — 🥉 (перевірка сусідства в інвентарі).
- Таймлайн кампанії: події за роками, поселення як мета-прогресія — 🥈.

## Мапа на каталог
- Є: `hp-damage` ↔ броня й травми · `status-effects` ↔ збиття, травми, розлади · `permadeath` ↔ загиблі вцілілі · `inventory-items` ↔ сховище · `shop-between-levels` ↔ крафт у поселенні · `world-map` ↔ доріжка полювання · `sequential-levels` ↔ роки кампанії · `save-progress`.
- **Нема** → пропозиції карток:
  - `+monster-ai-deck` «Колода поведінки ворога» · game-logic/opponent · 📎 · слот {cards, deck_as_hp: bool}.
  - `+hit-location-deck` «Колода частин тіла» · entities/combat · 🥉 · слот {reactions: reflex|failure|trap}.
  - `+facing-hit-bonus` «Бонус за удар зі спини» · entities/combat · 📎 — як у FFT.
  - `+body-part-armor` «Броня по частинах тіла» · entities/state · 📎 · слот {parts: 5}.
  - `+injury-table` «Таблиця тяжких травм» · entities/state · 🌱.
  - `+survival-reactions` «Ресурс реакцій» · entities/state · 📎 · слот {dodge, encourage, surge}.
  - `+knockdown` «Збиття з ніг» · entities/state · 🌱.
  - `+settlement-timeline` «Таймлайн подій кампанії» · levels/progression · 🥉.
  - `+gear-grid-adjacency` «Сітка спорядження зі звʼязками» · entities/state · 🥉 — родич Backpack Hero.
  - `+crafting-from-loot` «Крафт з трофеїв» · game-logic/economy · 📎.
  - `+hunt-track` «Доріжка наближення» · levels/progression · 🌱.
  - `+sanity-meter` «Безумство / мозок» · entities/state · 🌱.
  - `+deck-draw`, `+death-countdown` — як в інших тактиках корпусу.

## Пропозиції до словників
- `+trigger:card_drawn` — витягнуто карту (ШІ, локації) як подія; `+trigger:deck_empty` — колода вичерпалась (смерть монстра, перетасування).
- `+trigger:attacked` — початок атаки як подія (реакції, dodge).
- `+effect:draw_card` · `+effect:discard` — колоди; `+effect:roll_dice` — кидок кубиків.
- `+cond:in_blind_spot` — атакувальник у сліпій зоні цілі; `+cond:card_says` — умова, що бере пріоритет цілі з карти ШІ.
- `+role:card` — карта як сутність; `+role:settlement` — база між боями з будівлями.
- `+ui:ai-deck-counter` — лишок колоди ШІ як шкала здоровʼя; `+ui:hit-location-silhouette` — силует тіла з бронею й травмами; `+ui:survival-tokens`.
- `+window:settlement-screen`, `+window:gear-grid`, `+window:timeline-window`, `+window:hunt-board`.
- `+feature:campaign-timeline` — кампанія з фіксованих подій за роками.
- `+axis:session:campaign` — нове значення: кампанія з таймлайном.

## Джерела
- ⭐ [Wikipedia: Kingdom Death: Monster](https://en.wikipedia.org/wiki/Kingdom_Death:_Monster) — фази, колода ШІ визначає ціль і атаку, перемога пораненням монстра чи вичерпанням колоди, заміна загиблих, кінець кампанії, 1–4 гравці, невдалий Kickstarter iOS-застосунку.
- [RulesPal: зміст правил](https://rulespal.com/kingdom-death-monster/rulebook) — назви розділів (Monster AI, Pick Target, Critical Wounds, Survival, Survivor Death, Hit Locations); текст агенту недоступний.
- [RulesPal: FAQ](https://rulespal.com/kingdom-death-monster/faq) — питання підтверджують сутності: карти локацій, Failure/Reflex, Trap, сила проти стійкості, сліпа зона, поворот монстра, збиття, dodge/Block, безумство.
- YouTube: пошук «Kingdom Death Monster how to play».

## Непевне
- (?) Усі числа й процедури бою — за памʼяттю, правила агенту не відкрились: d10, формула влучання (швидкість × кидок, точність + ухилення), рана d10 + сила проти стійкості, крит на 10.
- (?) Бонус сліпої зони (+1 до влучання) і чи може монстр цілити в сліпу зону — питання є у FAQ, відповіді не бачив.
- (?) Дія Trap (скасувати атаку, монстр діє, перетасувати) і Basic Action при порожній руці ШІ.
- (?) Набір реакцій виживання (dodge, encourage, surge, dash, endure) і коли збитий вцілілий встає.
- (?) Поле бою 22×16 клітин, розміри основ монстрів, довжина доріжки полювання — не перевірено, тому без чисел у тексті.
- (?) Офіційної цифрової версії нема; фанатські модулі для Tabletop Simulator — не перевіряв.
