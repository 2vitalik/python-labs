---
title: Rondo of Swords
slug: rondo-of-swords
aka: [偽りの輪舞曲, Itsuwari no Rondo, Rondo of Deception]
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: runtime
  goal: state
year: 2007
platforms: [Nintendo DS]
links:
  - {kind: other, url: "https://lparchive.org/Rondo-of-Swords/Update%2001/", best: true, note: "Let's Play з поясненнями: удар проходом крізь ворога, без вороття, ZOC і порядок виштовхування, контратака, MC, OB 0–3, фази"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Rondo_of_Swords", note: "Route Maneuver System, контратака зупиняє, кілька цілей за хід, OverBreak з трьома рангами, доручення неактивним"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/偽りの輪舞曲", note: "JA: маршрут у межах руху, бій при проході, ZOC зупиняє й зсуває у вільну клітину, パシリ-система, до 6 у бою"}
  - {kind: other, url: "https://www.rpgfan.com/review/rondo-of-swords/", note: "огляд: одна атака проходить крізь цілу армію, ZOC, маги не ходять і не чаклують в один хід, рестарт бою"}
  - {kind: other, url: "https://lparchive.org/Rondo-of-Swords/Update%2014/", note: "туторіали 1–4: підтримка проходом крізь союзника, кут атаки, шанс контратаки"}
  - {kind: other, url: "https://lparchive.org/Rondo-of-Swords/Update%2016/", note: "туторіали 5–8: ZOC, магія і MP, friendly fire, шкала OB, MC"}
  - {kind: other, url: "https://lparchive.org/Rondo-of-Swords/Update%2019/", note: "туторіали 9–10: лінійні заклинання, магія крізь стіни, Wasteland = 3 руху"}
  - {kind: other, url: "https://lparchive.org/Rondo-of-Swords/Update%2007/", note: "доручення: квести, тренування, покупки, випробування для промоцій"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Rondo+of+Swords+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [path-drawing, no-reverse-turn, hp-damage, ai-opponent, unit-xp-skills, status-effects, explode-area, restart-level, sequential-levels, drop-on-death, tutorial-window, game-screen, end-screen, +pass-through-attack, +zone-of-control, +facing-hit-bonus, +reaction-attack, +nearest-free-displace, +support-pass-buff, +friendly-fire, +terrain-move-cost, +charge-meter-special, +aggro-meter, +mage-no-move-cast, +event-trigger-lines, +leader-death-lose, +victory-rank, +offscreen-errands, +class-promotion, +support-conversations, +new-game-plus, +multiple-endings]
proposes: ["+trigger:pass_through", "+effect:counterattack", "+effect:displace", "+ui:momentum-counter", "+ui:special-meter", "+window:errands-window", "+feature:offscreen-errands", "+card:pass-through-attack"]
author: opus
date: 2026-11-09
---

# Rondo of Swords — малюєш маршрут юніта наперед, і він бʼє кожного ворога, крізь якого пробігає, доки контратака чи ZOC не зупинить

## Суть
Тактична RPG для Nintendo DS (Success / Atlus) з **Route Maneuver System**: замість «підійти й ударити» гравець креслить маршрут у межах руху юніта, і кожен ворог на цьому маршруті отримує удар — один юніт може «прорізати» цілий стрій. Маршрут не може повертати назад; контратака або вміння ZOC зупиняють рух і викидають юніта на найближчу вільну клітину — часто посеред ворогів. Поверх — кут атаки (збоку/ззаду сильніше), шкала OverBreak, лічильник «моменту» (MC), що притягує ворогів, і система доручень для тих, хто не пішов у бій.

## Поле і час
- Квадратна сітка; ландшафт має вартість руху (Wasteland — 3 руху за клітину), дерева утворюють коридори в одну клітину.
- Хід: фаза гравця (кожен юніт — маршрут-атака, або вміння, або магія) → фаза ворога. Події мапи спрацьовують, коли гравець перетинає невидимі лінії (зазвичай наприкінці ходу).
- Інформація часткова: дальність ворожих лучників (Aimsman) прихована; вороги часто стоять, доки гравець не зайде в їхній радіус.
- Два екрани DS: верхній — стати, шкала OB, MC; нижній — поле (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Юніт гравця | piece | HP, Attack, Defense, Magic, Move, MP (лише маги), клас, напрям | маршрут у межах Move; бʼє кожного ворога на шляху |
| Serdic (лідер) | piece | — | його смерть — поразка; не ходить на доручення |
| Маг (Raine, Igraine…) | piece | MP, заклинання з формою області | не може рухатись і чаклувати в один хід |
| Ворог | enemy | ті ж стати, напрям, шанс контратаки | атакує в радіусі агро; ціль — за MC |
| Ворожий лучник (Aimsman) | enemy | прихована дальність | стріляє, коли юніт зайшов у радіус |
| Юніт із ZOC | enemy | вміння ZOC | крізь нього не пройти: рух зупиняється |
| Бос | boss | OB, власні навички | лишає предмет (Alberich — Black Ring) |
| Цивільний | neutral | вміння Aggressor | прохід крізь нього підсилює атаку |
| Ліс / дерева | static | — | непрохідні; утворюють вузькі алеї |
| Пустир (Wasteland) | terrain | 3 руху за клітину | гальмує переслідування |
| Невидима лінія події | zone | — | перетин запускає подію/підкріплення |
| Предмет (Alchemiracle, Peach Nectar, медалі) | pickup | ефект | 80 % HP / MP / «+атака −захист» |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(draw_route, unit)` → ЯКЩО `custom: «сума вартості клітин маршруту ≤ Move»` і `custom: «маршрут ніде не повертає назад»` → ТО `move(unit, route)` (покроково).
- КОЛИ `contact(unit, enemy)` (маршрут проходить крізь ворога) → ТО `damage(enemy, n)` — шкода ≈ атака − захист з множниками; рух триває далі маршрутом.
- КОЛИ `contact(unit, enemy)` → ЯКЩО `facing(enemy, side)` або `facing(enemy, back)` → ТО `custom: «більша шкода й точність»`; спереду — найгірше.
- КОЛИ `contact(unit, enemy)` → ЯКЩО `prob(counter_rate)` (спереду значно вища) → ТО `damage(unit, n)`, `block` для решти маршруту, `custom: «юніта відкидає назад у бік, звідки він атакував»`.
- КОЛИ `contact(unit, zoc_unit)` → ТО `block`, `custom: «поставити на першу вільну клітину за порядком: верх, низ, ліво, право, далі по кільцях назовні»`.
- КОЛИ `custom: «прямий маршрут крізь ряд ZOC-юнітів»` → ТО `custom: «юніта відбиває назад у коридор, звідки прийшов»`.
- КОЛИ `contact(unit, ally)` → ЯКЩО `has(ally, support_skill)` → ТО `set_state(unit, attack_bonus)` — Aggressor до +15 %, Valor Bonds +10 % за рівень; бонуси цивільних складаються.
- КОЛИ `contact(Serdic, Igraine)` → ЯКЩО `has(Igraine, torus_spell)` → ТО `heal(Serdic, 25%)`.
- КОЛИ `custom: «маршрут завершено»` → ТО `face(unit, last_dir)`; повернутись на місці не можна.
- КОЛИ `input(skill, unit)` → ТО `custom: «ефект вміння»` замість руху або атаки.
- КОЛИ `input(cast, mage, area)` → ЯКЩО `custom: «маг цього ходу не рухався»` і `counter(MP, >=, cost)` → ТО `damage(all_in_area, n)` — включно із союзниками, крізь стіни; `counter(MP, -cost)`.
- Форми області: квадрат (Megido Nova 5×5 → 11×11 з рівнем), прямокутник (Taion Raioh 3×4 → 3×5), лінія (Ice Spear, Yumil Ymir Magna).
- КОЛИ `custom: «юніт завдав або отримав шкоду»` → ТО `counter(OB, +small)`; КОЛИ `died(enemy)` від його удару → ТО `counter(OB, +big)`; максимум 3.
- КОЛИ `input(overbreak, unit)` → ТО `custom: «використати найбільший цілий рівень OB (1–3)»`, `counter(OB, -level)` (2.80 → рівень 2, лишається 0.80).
- КОЛИ `counter(MC, >=, 50)` і `counter(MC, <=, 80)` → ЯКЩО `prob(p)` → ТО `set_state(unit, crazed)` — усі стати −30 % до початку його наступного ходу.
- КОЛИ `counter(MC, >=, 81)` → ТО `set_state(unit, boost)` — імунітет до статусів; КОЛИ `counter(MC, ==, 99)` → ТО `set_state(unit, hero)`.
- КОЛИ `turn_start(enemy)` → ЯКЩО `in_range(enemy, unit, aggro)` → ТО `custom: «атакує, віддаючи перевагу юніту з вищим MC»`; інакше стоїть на місці.
- КОЛИ `reach(unit, event_line)` → ТО `custom: «подія мапи: засідка, підкріплення, діалог»`.
- КОЛИ `custom: «два певні персонажі закінчили хід поруч»` → ТО `custom: «відкрито розмову підтримки»` (без індикатора).
- КОЛИ `hp_zero(enemy)` → ТО `disappear(enemy)`; бос — `spawn(item, cell)`.
- КОЛИ `hp_zero(Serdic)` або `hp_zero(designated_unit)` → ТО `lose`.
- КОЛИ `custom: «ціль мапи виконана»` → ТО `win`, `custom: «ранг перемоги (Complete Victory — найвищий; менше ходів — краще)»`, `custom: «бонусний досвід усім»`.
- Перемога: ціль мапи (знищити ворогів, вбити лідера, вижити…) · Поразка: смерть лідера або позначеного юніта · Рахунок: ранг перемоги за кількістю ходів і умовами.

## Керування і ввід
- Стилус: креслити маршрут юніта на нижньому екрані в межах його руху; кнопки D-pad — альтернатива (?).
- Меню юніта: маршрут-атака / вміння / магія (з вибором області) / OverBreak / очікування.
- Між боями — меню доручень, навичок і спорядження.

## Вікна, меню, HUD
- `game-screen` (нижній екран): поле, маршрут-превʼю (`path-preview`), ворожі юніти з напрямом погляду.
- Верхній екран: `stat-panel` юніта, `+ui:special-meter` (OB з числом 1–3), `+ui:momentum-counter` (MC), вікно передбачуваної шкоди (обрізаної до поточного HP).
- `objective-text` / брифінг: умови перемоги й поразки мапи (туторіали мають власні цілі).
- `dialogue-window` — сюжетні сцени (нижній екран, без перемотки).
- `+window:errands-window` — доручення: Quests · Train · Shopping · Trials.
- `custom-window` навичок: SP за рівні → нові вміння й підсилення наявних.
- `end-screen` — ранг перемоги; повтор бою з початку зі збереженням досвіду.

## Фічі поза полем
- **Доручення (パシリ)**: у бій ідуть до 6 юнітів, решта отримує завдання. Quests — до 4 одночасно, виконавець пропускає наступну мапу, успіх залежить від Charisma; є ланцюги квестів, ковальські (+атака/точність зброї до 9 разів), «карткові» (3/6 карток → вроджене вміння), печатки для третього класу.
- Train — 1–3 очки до Attack/Defense/Magic на вибір; Shopping — єдиний спосіб витратити гроші, за похід або купівля, або продаж, бюджет ділиться автоматично.
- Trials → промоція класу на 15-му і 30-му рівнях (Proofs + печатка); рівень не скидається.
- `restart-level` з утриманням досвіду; сюжетні розгалуження й кілька фіналів; `+new-game-plus`.
- Юнітів на мапу ставить сама гра — розстановки нема.

## Варіації й родичі
- Родичі в корпусі: [fire-emblem](fire-emblem.md), [tactics-ogre](tactics-ogre.md) (сітка, кут атаки), [knights-in-the-nightmare](knights-in-the-nightmare.md) (незвичний ввід на DS), [yggdra-union](yggdra-union.md) (бій формуванням), [ticket-to-earth](ticket-to-earth.md) (шлях креслиться пальцем і задає силу).
- **Осі варіацій**: атака — сусідня клітина / прохід крізь ворога (Rondo) / шлях одного кольору · хто зупиняє рух — ніхто / контратака з шансом / вміння ZOC · куди дівається зупинений — на місці / відкидання назад / найближча вільна клітина за порядком · кут атаки — нема / бонус збоку й ззаду.

## Цікавинки для курсу
- Маршрут drag-ом у межах руху з вартістю клітин і забороною вороття — 📎.
- Удар по кожному ворогу на маршруті + обрив маршруту контратакою з шансом за кутом — 🥉.
- ZOC: виштовхнути на першу вільну клітину за фіксованим порядком обходу кілець — 📎.
- Бонус за кут атаки (спереду / збоку / ззаду) і «юніт дивиться туди, куди йшов» — 🌱.
- MC як «агро-лічильник»: пороги станів і вибір цілі ворогом — 📎.
- Заклинання з формами області (квадрат, прямокутник, лінія), що ростуть з рівнем і бʼють своїх — 🥉.
- AI, що креслить вигідний маршрут крізь найбільше слабких ворогів, уникаючи ZOC (пошук шляху з оцінкою) — 🥇.
- Доручення поза боєм: юніт зайнятий на N мап і повертається з результатом — 📎.

## Мапа на каталог
- Є: `path-drawing` ↔ креслення маршруту; `no-reverse-turn` ↔ маршрут не повертає назад; `hp-damage`; `ai-opponent`; `unit-xp-skills` ↔ SP і навички; `status-effects` ↔ Crazed, Boost, Glass; `explode-area` ↔ області заклинань; `restart-level`; `sequential-levels` ↔ глави; `drop-on-death` ↔ предмет з боса; `tutorial-window`; `game-screen`, `end-screen`.
- **Нема** → пропозиції карток:
  - `+pass-through-attack` «Удар кожного ворога на маршруті» · entities/combat · 🥉 · слот {stop_on: counter|zoc}.
  - `+zone-of-control`, `+facing-hit-bonus`, `+reaction-attack`, `+friendly-fire`, `+terrain-move-cost`, `+leader-death-lose` — уже в корпусі.
  - `+nearest-free-displace` «Виштовхнути на найближчу вільну клітину за порядком» · entities/move · 📎.
  - `+support-pass-buff` «Прохід крізь союзника дає бафф» · entities/state · 🌱.
  - `+charge-meter-special` «Шкала супервміння (OB 0–3)» · entities/state · 📎.
  - `+aggro-meter` «Лічильник, що притягує ворогів і дає стани» · entities/state · 📎.
  - `+mage-no-move-cast` «Або рух, або закляття за хід» · entities/legality · 🌱.
  - `+event-trigger-lines` «Невидимі лінії запускають події мапи» · game-logic/waves · 🌱.
  - `+victory-rank` «Ранг перемоги за ходами» · game-logic/score · 🌱.
  - `+offscreen-errands` «Неактивні юніти на дорученнях між боями» · game-logic/economy · 🥉.
  - `+class-promotion`, `+support-conversations`, `+new-game-plus`, `+multiple-endings` — прогресія поза полем.

## Пропозиції до словників
- `+trigger:pass_through` — A проходить крізь клітину B маршрутом, не зупиняючись (відмінне від `contact`, бо рух триває).
- `+effect:counterattack` — ціль відповідає ударом і обриває дію (уже пропоновано в корпусі).
- `+effect:displace` — перемістити сутність у найближчу вільну клітину за порядком обходу.
- `+ui:momentum-counter` — лічильник «моменту/агро» юніта з порогами станів.
- `+ui:special-meter` — шкала OB з рівнем 1–3 (уже пропоновано).
- `+window:errands-window` — екран доручень для неактивних юнітів.
- `+feature:offscreen-errands` — юніти поза боєм виконують завдання з таймером у мапах.
- `+card:pass-through-attack` — механіка, якої в каталозі нема.

## Джерела
- ⭐ [LP Archive: Update 01](https://lparchive.org/Rondo-of-Swords/Update%2001/) — атака лише проходом, «не можна повертати назад», ZOC і порядок виштовхування, контратака відкидає назад, MC (Crazed/Boost/Hero), OB 0–3, фази, лідер.
- [Wikipedia](https://en.wikipedia.org/wiki/Rondo_of_Swords) — Route Maneuver System, контратака/блок зупиняє, кілька цілей за хід, OB з трьома рангами, навички за SP, доручення, кінцівки.
- [Wikipedia JA](https://ja.wikipedia.org/wiki/偽りの輪舞曲) — маршрут у межах руху, ZOC зупиняє й переносить у вільну клітину, до 6 у бою, パシリ-система.
- [RPGFan](https://www.rpgfan.com/review/rondo-of-swords/) — один юніт крізь цілу армію, ZOC, розстановка автоматична, маги, рестарт бою з досвідом.
- [LP: туторіали 1–4](https://lparchive.org/Rondo-of-Swords/Update%2014/), [5–8](https://lparchive.org/Rondo-of-Swords/Update%2016/), [9–10](https://lparchive.org/Rondo-of-Swords/Update%2019/) — підтримка, кут атаки, магія й області, friendly fire, OB, MC, Wasteland.
- [LP: Errands](https://lparchive.org/Rondo-of-Swords/Update%2007/) — квести, тренування, покупки, випробування й промоції.
- YouTube: пошук «Rondo of Swords gameplay».

## Непевне
- (?) Чи смерть юніта гравця остаточна (permadeath) — джерела не кажуть.
- (?) Чи контратака після обриву лишає юніта на клітині перед ворогом, чи саме «відкидає» на попередню клітину маршруту — LP описує як «відкидання назад».
- (?) Точна формула шансу контратаки, зростання OB і MC; вплив ландшафту на захист.
- (?) Чи D-pad може заміняти стилус при кресленні маршруту; розподіл інформації між двома екранами.
- (?) Чи можна закінчити маршрут на клітині ворога, і чи союзника можна «проходити» без підтримки (в туторіалі — так, без бонусу).
