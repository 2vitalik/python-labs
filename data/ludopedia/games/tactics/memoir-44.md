---
title: "Memoir '44 / Commands & Colors"
slug: memoir-44
aka: [Memoir 44, M44, "Commands & Colors: Ancients", C&C, CCA, Мемуари 44]
family: tactics
also: []
klass: figure
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: hidden
  random: runtime
  goal: score
year: 2004
platforms: [board, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Memoir_%2744", best: true, note: "поле 13×9 і три секції, 60 карт наказів, типи юнітів, медалі"}
  - {kind: other, url: "https://rulespal.com/memoir-44/rulebook", note: "правила: порядок ходу, кубики за дальністю, лінія бачення, відступ, take ground, overrun, місцевість"}
  - {kind: other, url: "https://lehi-innovation.github.io/boardgame-rules/rules/memoir-44/", note: "стислий конспект правил з таблицями"}
  - {kind: other, url: "https://cdn.svc.asmodee.net/production-daysofwonder/uploads/2024/09/M44_REFRESH_RULES_EN_LD.pdf", note: "офіційні правила (refresh 2024), PDF"}
  - {kind: other, url: "https://www.orderofgamers.com/games/memoir-44/", note: "довідкові аркуші правил"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Commands_%26_Colors:_Ancients", note: "сестринська гра серії: банери, командна величина"}
  - {kind: other, url: "https://rulespal.com/commands-and-colors-ancients/rulebook", note: "правила C&C Ancients: лідери, battle back, evade, momentum"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Memoir+44", note: "пошук; цифрова версія"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Memoir+44+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 70
mechanics: [piece-move-patterns, impassable-cells, floor-types, melee-vs-ranged, legal-move-highlight, threat-range, hot-seat, ai-opponent, online-multiplayer, sequential-levels, match-setup, mode-select, save-game, +hex-grid-render, +deck-draw, +sector-orders, +dice-symbol-hits, +line-of-sight-fire, +forced-retreat, +terrain-dice-reduction, +take-ground, +medal-victory, +retaliation, +evade-retreat, +leader-attach]
proposes: ["+effect:draw_card", "+effect:roll_dice", "+cond:in_section", "+trigger:dice_face", "+role:card", "+role:leader", "+ui:hand-of-cards", "+ui:dice-tray", "+ui:medal-track", "+ui:section-lines", "+window:scenario-briefing", "+feature:mirror-match", "+axis:turn-structure:card-driven"]
author: opus
date: 2026-11-09
---

# Memoir '44 / Commands & Colors — карта наказу каже, яким флангом ти ходиш цього ходу

## Суть
Двоє гравців ведуть загони на гексовому полі, розрізаному на три секції: лівий фланг, центр, правий фланг. Хід починається з розіграшу **однієї карти наказу** з руки: вона дозволяє наказати N юнітам у певній секції — тож навіть сильна армія стоїть, якщо на руці нема карт «свого» флангу. Бій — кидок спеціальних кубиків із символами типів військ; гранати бʼють усіх, прапор змушує відступити. Перемога — набрати сценарне число медалей (зазвичай 4–6), кожна — за знищений загін. Серія Commands & Colors Річарда Борґа переносить ту саму систему в Античність (Ancients), Середньовіччя, Наполеонівські війни; тут описано Memoir '44 як цифрову версію, з осями варіацій із C&C Ancients.

## Поле і час
- Гексове поле **13 гексів завширшки × 9 углиб**, двостороннє (сільська місцевість / пляж). Дві червоні пунктирні лінії ділять його на три секції: лівий фланг, центр, правий фланг; гекс, що перетинає лінія, належить обом секціям.
- Сценарій кладе на поле гекс-плитки місцевості (ліс, село, пагорб, живопліт, річка, бункер…) і перешкоди (мішки з піском, дріт, їжаки) та розставляє юніти. Ліва/права — з погляду кожного гравця.
- Час — поперемінні ходи; хід = зіграти карту → наказати → рухати всіх → бити всіма → добрати карту. Ходи йдуть, доки хтось не добере медалей.
- Інформація прихована лише в руках: карти суперника невідомі; поле повністю відкрите. Випадковість — кубики й колода.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Піхота | piece | 4 фігурки; дальність 3; кубики 3/2/1 | 1 гекс і бій або 2 гекси без бою; може take ground |
| Спецпризначенці (Special Forces) | piece | значок; 4 фігурки | до 2 гексів і бій |
| Бронетехніка | piece | 3 фігурки; дальність 3; кубики 3/3/3 | до 3 гексів і бій; take ground + armor overrun |
| Артилерія | piece | 2 фігурки; дальність 6; кубики 3/3/2/2/1/1 | 1 гекс **або** бій; не потребує лінії бачення; ніколи не take ground |
| Карта секції (40) | card | секція(ї), N юнітів | наказ N юнітам у вказаній секції; Recon-1 — 1 юніт і вибір 1 з 2 карт при доборі |
| Карта тактики (20) | card | ефект | особливий наказ/бій (+кубик, Armor Assault, Ambush у чужий хід…) |
| Бойовий кубик | object | 6 граней: піхота ×2, танк, граната, зірка, прапор | грань = влучання за типом цілі / відступ / промах |
| Медаль | resource | — | за знищений юніт або утримання цільового гекса |
| Ліс / село | terrain | −1 кубик піхоті, −2 танку | вхід = зупинка й без бою цього ходу; блокує лінію бачення |
| Живопліт (hedgerow) | terrain | як ліс | вхід лише з сусіднього гекса і зупинка; вихід на 1 гекс |
| Пагорб | terrain | −1 кубик знизу вгору (піхота, танки) | без обмежень руху; блокує бачення, крім юнітів на тому ж пагорбі |
| Річка | static | — | непрохідна без мосту; бачення не блокує |
| Океан | terrain | — | рух на нього лише на 1 гекс; без бою; непрохідний для відступу |
| Пляж | terrain | — | рух на нього до 2 гексів; бій без обмежень |
| Бункер | terrain | −1 піхоті / −2 танку; ігнорує 1 прапор | лише піхота може зайти; належить стороні з брифінгу |
| Мішки з піском | object | −1 кубик; ігнорує 1 прапор | знімаються, коли юніт іде |
| Колючий дріт | hazard | — | вхід = зупинка; піхота може зняти замість бою; танк знімає й бʼється |
| Їжак (hedgehog) | static | ігнорує 1 прапор | лише піхота може зайти |
| Цільовий гекс | zone | медаль | дає медаль, поки утримується (за сценарієм) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(side)` → ТО `choose(card from hand)`; гравець грає рівно одну карту (виняток — Ambush у хід суперника).
- КОЛИ `input(play, section_card)` → ТО `custom: «можна наказати до N юнітів у секціях карти; зайві накази згоряють»`.
- КОЛИ `input(order, unit)` → ЯКЩО `custom: «юніт у секції зіграної карти»` and `not state(unit, ordered)` → ТО `set_state(unit, ordered)`; кожен юніт — один наказ за хід.
- КОЛИ `input(move, unit, hex)` → ЯКЩО `state(unit, ordered)` and `free(hex)` and `custom: «шлях не через зайняті гекси й ≤ ліміту типу»` → ТО `move(unit, hex)`; юніт рухається цілим, без поділу; спершу всі рухи, потім усі бої.
- КОЛИ `input(move, infantry, 2 hexes)` → ТО `set_state(infantry, no_battle)`.
- КОЛИ `enter(unit, forest|village|hedgerow|wire)` → ТО `custom: «рух закінчено»`; для лісу/села/живоплоту ще `set_state(unit, no_battle)`.
- КОЛИ `enter(unit, bunker|hedgehog)` → ЯКЩО `not same(unit, infantry, type)` → ТО `block`.
- КОЛИ `input(battle, a, b)` → ЯКЩО `in_range(a, b, range(a))` and (`line_of_sight(a, b)` or `same(a, artillery, type)`) → ТО `custom: «кинути dice(тип a, відстань) − захист місцевості b»`; найкращий захист, не сума.
- КОЛИ `input(battle, a, b)` → ЯКЩО `custom: «поруч з a є ворог»` and `not in_range(a, b, 1)` → ТО `block` (обовʼязковий ближній бій).
- КОЛИ `custom: «кидок завершено»` → ЯКЩО `custom: «грань = символ типу b або граната»` → ТО `hp(b, −1)` за кожну таку грань; зірка — промах (крім окремих карт тактики).
- КОЛИ `custom: «кидок завершено»` → ЯКЩО `custom: «випав прапор»` → ТО `move(b, toward own edge)` на 1 гекс за прапор, після влучань.
- КОЛИ `custom: «відступ»` → ЯКЩО `not free(cell_behind)` or `edge(b)` or `cell(cell_behind, ocean)` → ТО `hp(b, −1)` за кожен незроблений гекс.
- КОЛИ `custom: «перший прапор»` → ЯКЩО `cell(b, bunker|sandbags|hedgehog)` → ТО `custom: «ігнорується»`; КОЛИ прапор → ЯКЩО `cell(artillery, bunker)` → ТО `hp(artillery, −1)` замість відступу.
- КОЛИ `hp_zero(unit)` → ТО `disappear_a`, `counter(medals, +1)` для суперника.
- КОЛИ `custom: «ближній бій знищив або відкинув ціль»` → ЯКЩО `same(a, infantry|armor, type)` → ТО `move(a, vacated_hex)` (take ground, за бажанням).
- КОЛИ `after(take_ground)` → ЯКЩО `same(a, armor, type)` and `not state(a, overrun_used)` → ТО `custom: «ще один бій (armor overrun)»`, `set_state(a, overrun_used)`.
- КОЛИ `enter(unit, objective)` → ЯКЩО `custom: «сценарій дає медаль за гекс»` → ТО `counter(medals, +1)`; КОЛИ `leave(unit, objective)` → ТО `counter(medals, −1)`.
- КОЛИ `turn_end(side)` → ТО `custom: «скинути зіграну карту, добрати одну»`; колода скінчилась → перетасувати скид.
- КОЛИ `counter(medals, ≥, target)` → ТО `win`; перевірка миттєва.
- C&C Ancients: КОЛИ `custom: «захисник вижив і не відступив»` → ТО `custom: «battle back — відповідний удар»`; КОЛИ `input(battle, a, light_unit)` → ЯКЩО `custom: «ціль може ухилитися»` → ТО `move(b, 2 hexes back)` і бʼє лише меч/грань за половину (?).
- Перемога: медалі (Memoir) / банери (Ancients) до цілі сценарію · Поразка: суперник першим набрав · Рахунок: у матч-грі — сценарій двічі зі зміною сторін, сума медалей.

## Керування і ввід
- Цифрова версія: рука карт унизу; клік по карті — розіграти; доступні до наказу юніти підсвічено в секції; клік по юніту — наказ, далі клік по гексу — рух (підсвічено досяжні); потім фаза бою: клік по своєму юніту → по цілі, з показом кількості кубиків.
- Кидок кубиків — анімація; гравець вибирає гекс відступу, якщо є варіанти, і чи брати землю.
- Карти, що грають у чужий хід (Ambush), — запит-реакція.
- Сторони: hotseat на одному пристрої, онлайн, проти AI.

## Вікна, меню, HUD
- (цифрова версія) `main-menu`: Кампанії / Сценарії → `level-select`; Онлайн → `lobby-window`; Тренування; Налаштування → `settings-window`; Довідка → `help-window`.
- `scenario-briefing` (цифрова версія): історична довідка, ціль медалей, хто ходить першим, спецправила — потім `match-setup` (сторона, AI/людина).
- `game-screen`: гексове поле з лініями секцій (`section-lines`); `hand-of-cards`; `medal-track` обох сторін; `dice-tray` з результатом; `turn-indicator`; `legal-move-highlight`, `threat-range` (дальність/кубики до цілі); `message-log` дій.
- `confirm-dialog` для закінчення фази / ходу; `end-screen` з медалями й переходом до другої половини матчу.
- `codex-window` — довідка місцевості й значків (у настолці — summary-карти).

## Фічі поза полем
- `sequential-levels` — сценарії за історичними битвами, кампанії; `custom-rules` через розширення (Terrain Pack, Equipment Pack, Air Pack, Battle Maps).
- `mirror-match` — сценарій грається двічі зі зміною сторін, рахують суму медалей.
- `hotseat`, `online-multiplayer`, `ai-opponent-levels` (цифрова версія), `save-slots`.
- `rules-page` / `tutorial` для перших сценаріїв.

## Варіації й родичі
- Серія Commands & Colors: Ancients (2006, блоки замість фігурок, 7 кубиків з кольоровими символами легка/середня/важка + шолом лідера + мечі + прапор), Napoleonics, Medieval, Samurai Battles; BattleLore — фентезі.
- Родичі в корпусі: [Battle for Wesnoth](battle-for-wesnoth.md) (гекс, але бій кидками з шансом від місцевості цілі), [Advance Wars](advance-wars.md) (детермінований бій, без карт), [HeroQuest / Space Hulk](heroquest-space-hulk.md) (кубики з символами черепів/щитів).
- Осі варіацій:
  - **хто може діяти**: усі юніти (Wesnoth) / N юнітів у секції з карти (Memoir) / очки команд (Space Hulk);
  - **кубик**: число з порогом / символ, що бʼє лише певний тип / прапор = відступ;
  - **захист**: кубики віднімаються місцевістю цілі / ігнор першого прапора / підтримка двох сусідів (Ancients);
  - **реакція**: нема (Memoir) / battle back і evade (Ancients);
  - **ціль**: медалі/банери за знищення / утримання гексів.

## Цікавинки для курсу
- Секційні накази: рука карт обмежує, які фігури можна рухати — 📎 (колода + перевірка секції; гекс на межі в двох секціях).
- Кубик із символами й «таблиця дальності» тип × відстань → кількість кубиків — 🌱.
- Відступ за прапором з втратою фігурки за кожен заблокований гекс — 📎 (напрямок «до свого краю» на гексах).
- Лінія бачення по центрах гексів з правилом «по ребру — блокує лише з обох боків» — 🥉.
- Take ground + armor overrun: ланцюг атак одного юніта з обмеженням «раз за хід» — 📎.
- Найкращий захист з кількох джерел (місцевість ∪ перешкода), не сума — 🌱.
- AI, що оцінює руку карт і вибирає флангову атаку, — 🥈.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ ліміт руху за типом · `impassable-cells` ↔ річка, океан для відступу · `floor-types` ↔ ліс/село/пляж/океан · `melee-vs-ranged` ↔ обовʼязковий ближній бій і різні кубики за відстанню · `legal-move-highlight`, `threat-range` · `hot-seat`, `ai-opponent`, `online-multiplayer` · `sequential-levels` ↔ кампанії · `match-setup`, `mode-select`, `save-game`.
- **Нема** → пропозиції карток:
  - `+sector-orders` «Накази по секціях» · game-logic/opponent · 📎 · слот {sections: 3, n_units} — карта визначає, кого можна рухати.
  - `+deck-draw` «Колода й рука» · game-logic/random · 🌱 · слот {hand_size, reshuffle}.
  - `+dice-symbol-hits` «Кубики з символами» · entities/combat · 🌱 · слот {faces} — грань бʼє лише свій тип.
  - `+line-of-sight-fire` «Лінія бачення між гексами» · entities/combat · 🥉 · слот {edge_rule}.
  - `+forced-retreat` «Примусовий відступ» · entities/combat · 📎 · слот {hexes_per_flag, blocked_cost}.
  - `+terrain-dice-reduction` «Місцевість зменшує атаку» · entities/combat · 🌱 · слот {table, stack: best}.
  - `+take-ground` «Зайняти звільнений гекс» · entities/combat · 🌱 · слот {overrun: 1}.
  - `+medal-victory` «Медалі до цілі» · game-logic/win · 🌱 · слот {target, objectives}.
  - `+retaliation` / `+evade-retreat` / `+leader-attach` — C&C Ancients: battle back, ухилення легких, лідер, приєднаний до загону.

## Пропозиції до словників
- `+effect:draw_card` — добрати карту з колоди (Memoir, Gloomhaven, KDM).
- `+effect:roll_dice` — кинути N кубиків як ефект (не `roll` ⏳, що означає скочування з округлого).
- `+trigger:dice_face` — на кубику випала грань (прапор, граната, шолом).
- `+cond:in_section` — юніт у секції поля (флангова зона карти наказу).
- `+role:card` — карта як сутність гри; `+role:leader` — фігура, що приєднується до загону й дає бонус.
- `+ui:hand-of-cards` — рука карт гравця; `+ui:dice-tray` — результат кидка; `+ui:medal-track` — медалі обох сторін; `+ui:section-lines` — межі секцій поля.
- `+window:scenario-briefing` — історична довідка й умови сценарію.
- `+feature:mirror-match` — та сама місія двічі зі зміною сторін.
- `+axis:turn-structure:card-driven` — нове значення осі: що дозволено цього ходу, визначає карта.

## Джерела
- ⭐ [Wikipedia: Memoir '44](https://en.wikipedia.org/wiki/Memoir_%2744) — поле 13×9 і три секції, 40+20 карт, типи юнітів з рухом і кубиками, медалі 4–6.
- [RulesPal: Memoir '44 rulebook](https://rulespal.com/memoir-44/rulebook) — порядок ходу, лінія бачення, відступ, ігнор прапора, take ground, overrun, уся таблиця місцевості.
- [Конспект правил (lehi-innovation)](https://lehi-innovation.github.io/boardgame-rules/rules/memoir-44/) — грані кубика, таблиці руху й дальності.
- [Офіційні правила refresh 2024 (PDF)](https://cdn.svc.asmodee.net/production-daysofwonder/uploads/2024/09/M44_REFRESH_RULES_EN_LD.pdf) — агенту не розпарсився, людині відкривається.
- [Wikipedia: Commands & Colors: Ancients](https://en.wikipedia.org/wiki/Commands_%26_Colors:_Ancients) і [RulesPal: C&C Ancients](https://rulespal.com/commands-and-colors-ancients/rulebook) — лідери, battle back, evade, momentum advance, банери 5–8.
- [Order of Gamers](https://www.orderofgamers.com/games/memoir-44/) — довідкові аркуші.
- YouTube: пошук «Memoir 44 how to play»; Steam: пошук «Memoir 44».

## Непевне
- (?) Зірка: конспект каже «промах, крім карт тактики», один пошуковий уривок офіційного refresh-правила — «влучання»; у тексті — версія RulesPal.
- (?) Точна дія Ambush (захисник бʼє першим; якщо відкинув — атака скасована) — за памʼяттю.
- (?) Ancients: ухилення бʼє лише мечем/половиною — за памʼяттю; RulesPal підтверджує лише, хто може ухилятися й на скільки гексів.
- (?) Набір вікон і режимів цифрової версії (Memoir '44 Online) — з памʼяті, сторінку Steam не відкривав.
- (?) Скільки кубиків на гравця: компонентний список каже 8 кубиків, розклад — «по 4 кожному».
