---
title: BattleCON
slug: battlecon
aka: ["BattleCON: War of Indines", "BattleCON: Devastation of Indines", "BattleCON: Fate of Indines", "BattleCON Online"]
family: tactics
also: [board-digital]
klass: avatar
axes:
  field: 1d
  time: wego
  opponent: hotseat
  info: hidden
  random: none
  goal: state
year: 2009
platforms: [board, PC]
links:
  - {kind: other, url: "https://rulespal.com/battlecon-war-of-indines/rulebook", best: true, note: "RulesPal: правила War of Indines — бит, ante, пріоритет, clash, кроки атаки, stun guard, soak, рух, 2 купи скиду, 20 життя, 15 бітів, варіанти"}
  - {kind: other, url: "https://cdn.shopify.com/s/files/1/0277/6724/2855/files/BattleCON-Web-Rulebook-v4.pdf", note: "офіційний web-rulebook v4.2 (2020): Force-годинник 45, Overload-и, Switch-фінішер, tiebreaker ▲, Dodge, рух і стіни, командна гра на 9 клітинах"}
  - {kind: other, url: "https://rulespal.com/battlecon-devastation-of-indines/rulebook", note: "RulesPal: Devastation of Indines"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=BattleCON+Online"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=BattleCON+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 70
mechanics: [hp-damage, melee-vs-ranged, push-object, pull-object, hot-seat, online-multiplayer, character-select, pocket, +lane-grid, +simultaneous-hidden-orders, +double-blind-choice, +card-pair-attack, +priority-resolution, +clash-replay, +stun-guard, +armor-absorb, +discard-cooldown-piles, +hop-over-opponent, +edge-walls, +variable-player-powers, +ante-bidding, +desperation-finisher, +turn-limit, +best-of-series, +team-play]
proposes: ["+trigger:priority_tie", "+trigger:beat_end", "+effect:recycle_pair", "+effect:chip", "+effect:advance", "+effect:retreat", "+effect:ante", "+cond:range_band", "+cond:life_le", "+ui:discard-piles", "+ui:force-pool", "+ui:attack-pair-slots", "+window:reference-card", "+feature:special-actions-variant", "+axis:turn-structure=simultaneous-select-then-priority"]
author: opus
date: 2026-11-09
---

# BattleCON — файтинг на смузі з клітин: таємно складаєш атаку зі стилю й бази, швидший за пріоритетом бʼє першим

## Суть
Двоє бійців стоять на лінії клітин. Кожен **бит** гравці одночасно й таємно кладуть **пару карток — стиль + база**; їхні числа складаються в дальність, силу, **пріоритет** і guard атаки. Вищий пріоритет — активний гравець, бʼє першим; якщо влучив і шкода перевищила guard суперника, той **оглушений** і свою атаку не робить. Рівність пріоритетів — **clash**: обидва докладають нову базу поверх. Зіграна пара йде в скид і повертається в руку лише через **два бити** — отже, суперник знає, чого в тебе зараз нема. Випадковості нема зовсім: це гра читання суперника.

## Поле і час
- Лінія клітин; у War of Indines бійці стартують на 2-й і 6-й (дистанція 4), у v4 — на 3-й і 5-й. Командна гра — на 9 клітинах (зворот поля). Краї — стіни.
- Дальність рахується від своєї клітини (= 0); атака бʼє лише вказані відстані (`1~4` — від 1 до 4).
- Бит: Set → Ante → Reveal (+ Clash) → Start of Beat → атака активного → атака реактивного → End of Beat → Recycle.
- Годинник: War of Indines — 15 бітів; v4 — пул 45 Force, що вичерпується щобіта, потім один фінальний бит.
- Приховане — лише пари на час вибору; рука й скид відкриті через картку-довідку бійця.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Боєць (standup) | player | Life 20, клітина, унікальна здібність (UA) | рухається лише ефектами карток; двоє не стоять в одній клітині |
| Стиль ×5 + Switch | supply | дальність, сила, пріоритет, guard, тригери | половина пари; Switch (v4) викликає фінішер або дає Force |
| База: Strike, Shot, Drive, Burst, Grasp, Dash/Dodge + унікальна | supply | ті самі стати | друга половина пари; у clash докладається нова |
| Пара атаки | object | сума статів обох карток | визначає бит |
| Купа скиду 1 і 2 | zone | — | зіграна пара: в 1 → у 2 → у руку |
| Клітина поля | zone | — | позиція; дальність |
| Край поля | static | — | стіна: рух назад обривається |
| Фінішер (Overdrive) | object | — | підпис-атака раз на дуель; при ≤ 7 життя; виграє нічию без clash |
| Жетони/маркери UA (Iron Body, Time, Gate Trap, ammo…) | resource | ліміти бійця | ставки в ante, маркери на полі |
| Force (v4) | resource | пул 45, ≤ 10 у гравця | Overload-и за 2 Force; годинник дуелі |
| Overload Tiles (v4): Power Up, Defense Up, Speed Up | switch | раз на бит кожен | бонус до атаки за 2 Force |
| Маркер активного гравця | mark | — | хто бʼє першим; у v4 — нічия в кінці на користь реактивного |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(set)` → ТО `custom: «обидва одночасно кладуть сорочкою 1 стиль + 1 базу»`.
- КОЛИ `phase_start(ante)` → ТО `custom: «по черзі ставлять жетони UA / Overload за 2 Force; кінець — два паси поспіль; ставку не забрати»`.
- КОЛИ `phase_start(reveal)` → ТО `custom: «відкрити пари; тригери Reveal; пріоритет = база + стиль (+ модифікатори)»`; вищий → `custom: «активний гравець»`.
- КОЛИ `custom: «пріоритети рівні»` → ЯКЩО `custom: «нема tiebreaker ▲ і фінішера»` → ТО `custom: «clash: обидва кладуть нову базу поверх, перерахунок; повтор, доки рівно»`; ЯКЩО `custom: «бази в руці скінчились»` → ТО `custom: «одразу Recycle»`.
- КОЛИ `phase_start(start_of_beat)` → ТО `custom: «тригери Start: спершу активний, потім реактивний (і оглушений теж)»`.
- КОЛИ `custom: «крок атаки a»` → ЯКЩО `not state(a, stunned)` → ТО `custom: «Before → перевірка дальності → On Hit → шкода → On Damage → After»`.
- КОЛИ `custom: «перевірка дальності»` → ЯКЩО `custom: «відстань до b ∈ дальності атаки»` and `not state(b, avoid)` → ТО `damage(b, power − armor/soak)`; armor витрачається.
- КОЛИ `custom: «b отримав шкоду»` → ЯКЩО `custom: «шкода > guard b»` → ТО `set_state(b, stunned)` — `custom: «b не атакує цей бит»`; stun immunity скасовує.
- КОЛИ `counter(life, ≤, 0)` → ТО `lose` — дуель закінчується одразу.
- Chip / Lose life: `custom: «втрата життя без шкоди: не оглушує, не зменшується бронею, не опускає нижче 1»`.
- Рух: `custom: «advance — до суперника, retreat — від нього, pull/push — суперника, close — до впритул, teleport — одразу в клітину»`; `move(a, toward|away)`, `pull(b)`, `push(b)`.
- КОЛИ `custom: «рух через клітину суперника»` → ТО `custom: «перестрибнути, клітину суперника не рахувати»`; advance далі за суперника → `custom: «опиняєшся по той бік»`.
- КОЛИ `custom: «рух упирається в край»` → ТО `custom: «retreat/push — наскільки можна; обовʼязковий рух, якщо легальний варіант існує»`; нелегальний «рівно N» — `block`.
- КОЛИ `phase_start(end_of_beat)` → ТО `custom: «тригери End: активний, потім реактивний»`.
- КОЛИ `phase_start(recycle)` → ТО `custom: «купа 2 → у руку; купа 1 → у купу 2; зіграна пара → у купу 1»` — `custom: «пара недоступна 2 бити»`.
- v4: КОЛИ `phase_start(recycle)` → ТО `counter(force, +1)`; ЯКЩО `counter(life, ≤, 7)` → ТО `counter(force, +1)`; понад 10 — у смітник.
- КОЛИ `counter(beat, ==, 15)` (WoI) / `custom: «пул Force порожній»` (v4) → ТО `custom: «ще один фінальний бит»`; більше життя → `win`; v4: рівність — перемагає реактивний.
- Фінішер (варіант Special Actions): КОЛИ `custom: «Finish + Strike / Drive / унікальна база»` → ЯКЩО `counter(life, ≤, 7)` → ТО `custom: «Overdrive Finisher замість пари»`; інакше як Cancel.
- Pulse: КОЛИ `custom: «Special Action + Burst/Dash»` → ТО `custom: «скасувати пару суперника, обох відштовхнути»`; Cancel: КОЛИ `custom: «Special Action + Grasp/Shot»` → ТО `custom: «вибрати нову пару, побачивши суперникову»`.
- Перемога: життя суперника 0 · Таймаут: більше життя · Матч: 2 з 3 дуелей (`+best-of-series`).

## Керування і ввід
- Настільна: гравець кладе дві картки сорочкою (червона й синя сорочки — стиль і база), ставить жетони, переставляє standup за ефектами.
- Цифрова (BattleCON Online): вибір стилю й бази з руки, ставки, автоматичне розвʼязання біта.
- Довідкові картки суперника відкриті — що в нього в руці, видно за скидом.

## Вікна, меню, HUD
- `game-screen` (цифрова версія): лінія клітин зі standup-ами; `pocket` — рука стилів і баз; `+ui:attack-pair-slots` — 2 слоти пари; `+ui:discard-piles` — купи 1 і 2 обох; `hp-bar` / лічильник Life; `+ui:force-pool` (v4); `turn-indicator` активного гравця; жетони UA.
- `character-select` — вибір бійця (рівні складності UA: Novice / Intermediate / Advanced).
- `+window:reference-card` — довідка бійця з усіма стилями і базами (настільні гравці обмінюються нею).
- `tutorial-window` (онлайн), `end-screen` — переможець дуелі/матчу; `lobby-window` (онлайн).

## Фічі поза полем
- Варіанти: Character Teams, Tag Teams, Arenas, мультиплеєр 3–4 (WoI — дві смуги, v4 — 9 клітин, спільний пул Force), Tournament Mode, EX Duel (30 життя), Almighty Duel (40), боси 2v1 / 3v1 (Super/Ultra).
- `+feature:special-actions-variant` — Pulse / Cancel / Finish.
- Онлайн-версія BattleCON Online — `online-multiplayer`.

## Варіації й родичі
- Набори серії: War of Indines, Devastation of Indines, Trials of Indines, Fate of Indines, Wanderers of Indines, Strikers (окремі коробки з бійцями й незначними правками); v4 web-rulebook зводить правила: Force-годинник, Overload-и, Switch-фінішер, Dodge замість Dash.
- Родичі: [Fights in Tight Spaces](fights-in-tight-spaces.md) (картки + позиція на тісній сітці), [Duelyst](duelyst.md), [Summoner Wars](summoner-wars.md); одновимірні поля в корпусі — [Flamme Rouge](../board-digital/flamme-rouge.md), [Hare and Tortoise](../board-digital/hare-and-tortoise.md).
- **Осі варіацій**: хто бʼє першим — ініціатива по черзі / пріоритет суми карток (тут) / одночасно · нічия — clash із новою базою (тут) / tiebreaker / активний зберігає · доступ до карток — колода / книга ([mage-wars](mage-wars.md)) / фіксований набір із 2-бітним cooldown (тут).

## Цікавинки для курсу
- Атака як сума двох карток (дальність, сила, пріоритет, guard) і розвʼязання біта за пріоритетом — 📎.
- Clash: рекурсивний перевибір бази до нерівності з виходом, коли бази скінчились — 🌱.
- Скид у дві купи як cooldown на 2 ходи — 🌱 (черга довжини 2).
- Рух на 1D-смузі з перестрибуванням суперника, стінами й «обовʼязковим, якщо можна» — 📎 (багато крайових випадків).
- Оглушення «шкода > guard» скасовує відповідну атаку — 🌱.
- AI для одночасного вибору без випадковості: мінімакс за матрицею виплат / змішана стратегія — 🥇.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` ↔ дальності `1` / `1~4` · `push-object` + `pull-object` ↔ push/pull суперника · `hot-seat` · `online-multiplayer` · `character-select` · `pocket` ↔ рука.
- **Нема** → пропозиції карток:
  - `+lane-grid`, `+simultaneous-hidden-orders`, `+double-blind-choice`, `+armor-absorb`, `+edge-walls`, `+variable-player-powers`, `+turn-limit` ↔ 15 бітів / пул Force, `+best-of-series`, `+team-play` — уже в корпусі.
  - `+card-pair-attack` «Атака = сума двох карток (стиль + база)» · entities/combat · 📎.
  - `+priority-resolution` «Хто бʼє першим — за пріоритетом атаки» · game-logic/opponent · 🌱.
  - `+clash-replay` «Нічия пріоритету → нова база поверх» · game-logic/opponent · 🌱.
  - `+stun-guard` «Шкода > guard оглушує: атака скасована» · entities/combat · 🌱.
  - `+discard-cooldown-piles` «Картка повертається через N ходів (черга купок)» · game-logic/economy · 🌱 · слот {beats: 2}.
  - `+hop-over-opponent` «Рух перестрибує суперника на лінії» · entities/legality · 🌱.
  - `+ante-bidding` «Ставки ресурсом після вибору, до відкриття» · game-logic/opponent · 📎.
  - `+desperation-finisher` «Супер-атака лише при малому життя, раз за бій» · entities/combat · 🌱 · слот {life_le: 7}.

## Пропозиції до словників
- `+trigger:priority_tie` — рівність пріоритетів (clash); `+trigger:beat_end` — кінець біта перед recycle.
- `+effect:recycle_pair` — зсув купок скиду; `+effect:chip` — втрата життя без шкоди, не нижче 1; `+effect:advance` / `+effect:retreat` — рух відносно суперника (не абсолютний напрям); `+effect:ante` — поставити ресурс.
- `+cond:range_band` — відстань у діапазоні `a~b`; `+cond:life_le` — життя ≤ N (фінішер, бонус Force).
- `+ui:discard-piles` — дві купи скиду обох гравців; `+ui:force-pool`; `+ui:attack-pair-slots`.
- `+window:reference-card` — довідка бійця; `+feature:special-actions-variant`.
- `+axis:turn-structure=simultaneous-select-then-priority` — одночасний вибір, послідовне виконання за пріоритетом.

## Джерела
- ⭐ [RulesPal: BattleCON: War of Indines](https://rulespal.com/battlecon-war-of-indines/rulebook) — 5 стилів і 7 баз, 20 життя, старт 2/6, кроки біта, clash, Stun Guard і Soak, рух із перестрибуванням, recycle на 2 бити, 15 бітів, Special Actions, варіанти, список бійців.
- [BattleCON Web Rulebook v4.2](https://cdn.shopify.com/s/files/1/0277/6724/2855/files/BattleCON-Web-Rulebook-v4.pdf) — старт 3/5, 45 Force як годинник, Overload-и, tiebreaker ▲, Switch-фінішер раз на дуель, Armor, Avoid, Chip, Close/Teleport, стіни, 9 клітин для команд, нічия в кінці → реактивний.
- [RulesPal: Devastation of Indines](https://rulespal.com/battlecon-devastation-of-indines/rulebook) — інша коробка серії (бачено в результатах пошуку).
- YouTube: пошук «BattleCON how to play».

## Непевне
- (?) Кількість клітин дуельного поля (7 — за чергою і з симетрії старту 2/6 і 3/5); у правилах числа нема.
- (?) Стати шести стандартних баз (Strike, Shot, Drive, Burst, Grasp, Dash/Dodge) — у прочитаних текстах лише назви.
- (?) Рік першого видання (2009 — з черги); дизайнер — D. Brad Talton Jr., видавець — Level 99 Games (за текстом правил, прямо не сказано).
- (?) Чи BattleCON Online досі доступна в Steam.
