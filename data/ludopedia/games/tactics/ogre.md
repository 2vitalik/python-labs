---
title: Ogre
slug: ogre
aka: [OGRE, "Ogre (Steve Jackson)", Ogre Sixth Edition, Ogre Designer's Edition, Ogre Pocket Edition]
family: tactics
also: [board-digital]
klass: figure
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: full
  random: runtime
  goal: state
year: 1977
platforms: [board, Apple II, C64, Amiga, Atari ST, DOS, Mac, PC, PS4, Switch, Xbox One]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Ogre_(board_game)", best: true, note: "один кібертанк проти загону, підсистеми Огра, стати юнітів, CRT, сценарії, видання, цифрові версії"}
  - {kind: official, url: "https://www.sjgames.com/ogre/resources/", note: "SJ Games: ресурси — PDF правил 6-го видання, Designer's Edition, турнірні правила, шпаргалка"}
  - {kind: other, url: "https://www.sjgames.com/ogre/products/ogredesigner/QuickPlaySheet-Ogre.pdf", note: "шпаргалка правил SJ Games: черга фаз, стекування, CRT, таран, базовий сценарій"}
  - {kind: other, url: "https://www.sjgames.com/ogre/resources/img/Ogre_6th_Battlefields_Rules.pdf", note: "повна книга правил 6-го видання (PDF >10 МБ, не прочитано цілком)"}
  - {kind: steam, url: "https://store.steampowered.com/app/517780", note: "цифрова версія Auroch Digital (2017): кампанія, скірміш з AI, hotseat, асинхронний онлайн, редактор сценаріїв"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Ogre+Steve+Jackson+board+game+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 70
mechanics: [hp-damage, piece-capture, impassable-cells, melee-vs-ranged, legal-move-highlight, reachable-highlight, threat-range, hot-seat, turn-enforcement, ai-opponent, async-multiplayer, placement-screen, match-setup, in-game-editor, level-exchange, tutorial-window, sequential-levels, rule-variants, +subsystem-damage, +combat-results-table, +odds-ratio, +combined-attack, +ram-overrun, +tread-movement-loss, +disabled-state, +double-move-unit, +stack-limit, +asymmetric-sides, +point-buy-setup, +edge-side-block]
proposes: ["+cond:odds(atk, def, op, ratio)", "+effect:disable(a)", "+effect:recover(a)", "+trigger:ram(a, b)", "+role:subsystem", "+ui:record-sheet", "+ui:odds-preview", "+window:scenario-editor", "+feature:print-map-export", "+axis:sides=asymmetric", "+card:combat-results-table", "+card:subsystem-damage"]
author: opus
date: 2026-11-09
---

# Ogre — гекс-варгейм «один проти всіх»: гігантський кібертанк з окремими гарматами й гусеницями проти загону, що захищає командний пункт

## Суть
Асиметрична дуель двох гравців на гекс-мапі. Один веде **єдиний Ogre** — величезний робот-танк, у якого кожна гармата й гусениці мають власний захист і знищуються окремо (записується на листку). Інший розставляє за бюджетом загін — танки, ховеркрафти GEV, гаубиці, піхоту — і захищає **командний пункт (CP)**. Бій — без HP: атака сумує силу, ділить на захист цілі й кидає d6 за **таблицею результатів (CRT)**. Головний вибір захисника — бити гусениці (сповільнити до CP) чи гармати (обеззброїти).

## Поле і час
- Гекс-мапа (оригінал — 15 гексів завширшки, 22 ряди з 2-го видання); Ogre заходить з південного краю, захисник — на півночі.
- Рельєф: **кратери** — непрохідні для всіх, навіть Огра; **хребти** — на ребрах між гексами, їх перетинають лише Ogre і піхота. Пізніші видання — місто, ліс, вода, болото (?).
- Стекування: не більше одного юніта на гекс; виняток — до 3 очок піхоти. Свої юніти можна проходити наскрізь, якщо хід закінчено без порушення ліміту.
- Хід гравця = фази: **Recovery** (відновити оглушених до попереднього свого ходу) → **Movement** (рух, тарани) → **Combat** (стрільба) → **Second Movement** (лише GEV). Потім те саме робить інший гравець.
- Випадковість — d6 у кожній атаці й тарані.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ogre Mark III | piece | 45 гусеничних очок, M3; набір гармат на листку | рухається, таранить, стріляє кожною гарматою окремо; знищений, коли втратив усі гармати й гусениці |
| Main Battery (Огра) | piece | ATK 4, R 3, D4 | ціль атаки окремо від корпусу |
| Secondary Battery | piece | ATK 3, R 2, D3 (D2 у деяких виданнях) | те саме |
| Anti-personnel (AP) | piece | ATK 1, R 1, D1 | лише по піхоті й CP; дає право «давити» піхоту рухом |
| Ракета (зовнішня / в стелажі) | piece | ATK 6, R 5, D3 (стелаж D4) | одноразова; знищений стелаж знищує одну ракету |
| Гусениці (treads) | piece | тричі по ¼ запасу | кожна втрачена ¼ — −1 очко руху; атака по них завжди 1:1 |
| Heavy Tank | piece | 4/2 D3 M3 | найкраще співвідношення атаки до ціни; таран коштує Огру 2 гусениці |
| Missile Tank | piece | 3/4 D2 M2 | дальність |
| Light Tank / Superheavy | piece | 2/2 D2 M3 / 6(×2)/3 D5 M3 | з розширень і нових видань |
| GEV (ховеркрафт) | piece | 2/2 D2 M4+3 | рухається двічі: до і після бою (hit-and-run) |
| Howitzer | piece | 6/8 D1 M0, ціна ×2 | нерухомий, найдальший; таран Огра знищує автоматично |
| Mobile Howitzer | piece | 6/6 D2 M1 | — |
| Піхота | piece | n/1 Dn M2, 1–3 загони в гексі | перетинає хребти; не таранять, але Ogre з AP «давить» по загону |
| Командний пункт (CP) | static | D0/D1, M0 | мета Огра; таран знищує автоматично |
| Кратер | static | — | непрохідний для всіх |
| Хребет | static | на ребрі гекса | блокує перехід усім, крім Огра й піхоти |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(recovery)` → ЯКЩО `state(unit, disabled)` → ТО `clear_state(unit, disabled)`.
- КОЛИ `input(move, unit, hex)` → ЯКЩО `legal(move)` і `custom: «шлях ≤ M, без кратерів; хребет — лише Ogre/піхота»` → ТО `move(unit, hex)`; ЯКЩО `state(unit, disabled)` → ТО `block`.
- КОЛИ `enter(unit, hex)` → ЯКЩО `occupied(hex, friendly)` і `custom: «хід закінчується тут і ліміт стеку порушено»` → ТО `block`.
- Таран: КОЛИ `enter(ogre, hex)` → ЯКЩО `occupied(hex, armor)` and `prob(1/2)` (d6 = 1–3) → ТО `set_state(armor, disabled)`; інакше (4–6) → `disappear(armor)`; Ogre може витратити ще 1 очко руху й таранити знову; не більше 2 таранів за хід.
- КОЛИ `enter(ogre, hex)` → ЯКЩО `occupied(hex, howitzer)` або `occupied(hex, cp)` → ТО `disappear_b` (автоматично).
- КОЛИ `enter(armor, ogre_hex)` (таранить сам) → ТО `disappear(armor)`.
- КОЛИ `custom: «таран з Missile Tank / GEV / Howitzer / CP (у будь-який бік)»` → ТО `counter(treads, −1)`; з Heavy Tank → `counter(treads, −2)`.
- КОЛИ `enter(ogre, hex)` → ЯКЩО `occupied(hex, infantry)` і `has(ogre, ap)` → ТО `custom: «піхота −1 загін»`; можна витратити ще 1 очко й повторити.
- КОЛИ `input(attack, attackers, target)` → ЯКЩО `in_range(each, target, R)` → ТО `custom: «odds = Σ ATK : DEF, округлено на користь цілі; кидок d6 → CRT»`.
- КОЛИ `custom: «odds < 1:2»` → ТО `custom: «NE (без ефекту)»`; КОЛИ `custom: «odds ≥ 5:1»` → ТО `custom: «X автоматично»`.
- Результат `D`: ЯКЩО ціль — armor і `not state(t, disabled)` → ТО `set_state(t, disabled)`; ЯКЩО вже `disabled` → `disappear(t)`; піхота → `custom: «−1 очко сили»`; підсистема Огра → `custom: «без ефекту»`.
- Результат `X`: armor → `disappear(t)`; уся піхота в гексі → `disappear`; підсистема Огра → `custom: «закреслити на листку»`.
- КОЛИ `input(attack, a, ogre_treads)` → ТО `custom: «атака завжди 1:1, без обʼєднання»`; ЯКЩО результат `X` → ТО `counter(treads, −ATK атакувальника)`.
- КОЛИ `counter(treads, <=, ¾ / ½ / ¼ запасу)` → ТО `speed(ogre, −1)` на кожному порозі; 0 гусениць → `speed(ogre, 0)`.
- КОЛИ `input(fire, missile)` → ТО `take(ogre, missile)` — ракета одноразова.
- Обʼєднання: кілька атакувальників (і кілька гармат Огра) можуть сумувати ATK на одну ціль; сусідні цілі захист не сумують.
- Відстань для Огра-мініатюри — від переднього гекса моделі.
- КОЛИ `phase_start(second_movement)` → ЯКЩО `custom: «юніт — GEV і не оглушений»` → ТО `move(gev, ≤3)`.
- Перемога Огра: `destroyed(cp)` → `win` (у частині сценаріїв ще й знищити сили захисника) · Перемога захисника: `custom: «Ogre втратив усі гармати й гусениці»` → `win`.
- Базовий сценарій: захисник ставиться першим — 20 загонів піхоти + 12 armor (гаубиця = 2), до 20 ATK між сірими стрілками, решта північніше, CP будь-де; Ogre Mark III ходить першим, заходить з південного краю, перший хід ≤ 3 гекси.

## Керування і ввід
- Настолка: фішки на гекс-мапі, листок Огра з клітинками-галочками для кожної підсистеми й гусениць; d6.
- Цифрова (Auroch Digital): вибір юніта → підсвічені досяжні гекси → клік; у фазі бою — вибір цілі й додавання атакувальників у групу з показом odds; для Огра — вибір окремої гармати і підсистеми-цілі.
- Захисник перед грою «купує» склад за бюджетом і розставляє в зонах.

## Вікна, меню, HUD
- `main-menu` (цифрова версія): Campaign, Skirmish, Multiplayer (hotseat / онлайн), Tutorial, Scenario Creator, Settings.
- `match-setup` — сторона (North American Combine / Paneuropean), Mark Огра, сценарій, AI.
- `placement-screen` — купівля й розстановка захисника за бюджетом у зонах.
- `game-screen`: гекс-мапа з рельєфом; `record-sheet` Огра (гармати, ракети, гусениці); `reachable-highlight`, `threat-range`; `odds-preview` перед атакою; індикатор фази; кнопка завершення фази.
- `end-screen` — переможець; `tutorial-window`; `editor-window` (Scenario Creator) з експортом мапи в друк; `lobby-window` для онлайну (?).

## Фічі поза полем
- Сценарії: базовий (Mark III) і просунутий (Mark V проти більшого загону); Mark I–VI.
- `custom-rules` / `rule-variants`: розширення G.E.V. (рельєф, стекування), Shockwave (крилаті ракети, будівлі), Battlefields (ополчення, інженери).
- Цифрова версія: кампанія, `ai-opponent-levels` (?), `hotseat`, асинхронний `online-multiplayer` з рейтингом, редактор сценаріїв + Steam Workshop, експорт мапи в друк.

## Варіації й родичі
- G.E.V. (1978) — сумісний сиквел; Ogre Miniatures; Ogre Designer's Edition (2013), Pocket Edition (2013), Sixth Edition (2016).
- Родичі в корпусі: [battle-isle](battle-isle.md), [steel-panthers](steel-panthers.md) (гекс-варгейми з таблицями), [memoir-44](memoir-44.md) (гекс + кубики), [heroes-of-might-and-magic-3](heroes-of-might-and-magic-3.md) (гекс-бої стеків).
- **Осі варіацій**: симетрія сторін (дзеркальні армії / один гігант проти багатьох) · модель шкоди (HP / CRT з оглушенням / підсистеми) · удар (сума ATK : DEF + d6 / фіксована шкода) · рух після бою (нема / окремий клас із подвійним рухом).

## Цікавинки для курсу
- CRT: odds-співвідношення з округленням на користь цілі + d6 → NE/D/X, межі 1:2 і 5:1 — 📎 (таблиця як дані).
- Боса з підсистем: кожна гармата — ціль з власним D, смерть = нема гармат і гусениць — 🥉.
- Гусениці як «HP руху»: кожна ¼ знімає 1 очко руху; атака по них завжди 1:1 — 🌱.
- Таран і «давити піхоту» як рух, що є атакою, з можливістю повторити за очко руху — 📎.
- Оглушення: перше D — оглушений, друге D — знищений; відновлення у фазі Recovery — 🌱.
- GEV з другим рухом після бою — 🌱.
- Хребти на ребрах гексів (стіна між клітинами, а не в клітині) — 📎.
- AI за Огра або за захисника (оцінка «куди йти до CP» проти «збити гусениці») — 🥇.

## Мапа на каталог
- Є: `hp-damage` (частково — тут CRT) · `piece-capture` ↔ X знімає фішку · `impassable-cells` ↔ кратер · `melee-vs-ranged` ↔ R 1…8 · `legal-move-highlight` + `reachable-highlight` · `threat-range` · `hot-seat` · `turn-enforcement` ↔ фази · `ai-opponent` · `async-multiplayer` · `placement-screen` · `match-setup` · `in-game-editor` + `level-exchange` ↔ Scenario Creator + Workshop · `tutorial-window` · `sequential-levels` ↔ кампанія · `rule-variants` ↔ G.E.V./Shockwave.
- **Нема** → пропозиції карток:
  - `+combat-results-table` «Таблиця результатів за odds і кидком» · entities/combat · 📎 · слоти {columns, die, results}.
  - `+odds-ratio` «Співвідношення сили до захисту з округленням на користь цілі» · entities/combat · 🌱.
  - `+combined-attack` «Кілька атакувальників сумують силу на одну ціль» · entities/combat · 🌱.
  - `+subsystem-damage` «Велика сутність з окремими цілями-підсистемами» · entities/state · 🥉.
  - `+tread-movement-loss` «Втрата ¼ гусениць = −1 руху» · entities/state · 🌱.
  - `+ram-overrun` «Таран/переїзд рухом як атака, з повтором за очко руху» · entities/combat · 📎.
  - `+disabled-state` «Оглушення: друге влучання знищує, відновлення в окремій фазі» · entities/state · 🌱.
  - `+double-move-unit` «Юніт рухається до і після бою» · game-logic/opponent · 🌱.
  - `+stack-limit` «Ліміт стеку в клітині за типом» · entities/legality · 🌱.
  - `+asymmetric-sides` «Сторони з різними силами й цілями» · game-logic/opponent · 📎.
  - `+point-buy-setup` «Купівля загону за бюджетом перед боєм» · game-logic/economy · 📎.
  - `+edge-side-block` «Перешкода на ребрі між клітинами» · entities/legality · 📎.

## Пропозиції до словників
- `+cond:odds(atk, def, op, ratio)` — співвідношення сили атаки до захисту порівняно з порогом.
- `+effect:disable(a)` — оглушити до наступної фази відновлення (відрізняється від `stun(n)`: друге влучання знищує).
- `+effect:recover(a)` — зняти оглушення у фазі Recovery (поки — `clear_state`).
- `+trigger:ram(a, b)` — таран: рух у клітину ворога як атака.
- `+role:subsystem` — частина великої сутності, що є окремою ціллю.
- `+ui:record-sheet` — листок стану сутності з клітинками втрат; `+ui:odds-preview` — співвідношення й шанси перед атакою.
- `+window:scenario-editor` — редактор мапи й складу сторін (дитина `editor-window`).
- `+feature:print-map-export` — експорт мапи для друку настільної версії.
- `+axis:sides=asymmetric` — сторони несиметричні за силами й метою.
- `+card:combat-results-table`, `+card:subsystem-damage` — див. вище.

## Джерела
- ⭐ [Wikipedia: Ogre (board game)](https://en.wikipedia.org/wiki/Ogre_(board_game)) — асиметрична дуель, мапа й рельєф, стати всіх юнітів (S/R Dx My), підсистеми Огра й ракети, CRT-правила, сценарії, видання 1977–2021, G.E.V., цифрові версії.
- [SJ Games: шпаргалка Ogre](https://www.sjgames.com/ogre/products/ogredesigner/QuickPlaySheet-Ogre.pdf) — фази ходу, стекування, хребти/кратери, CRT по стовпцях 1-2…4-1, D і X, атака по гусеницях 1:1, таран і втрата гусениць, давлення піхоти, базовий сценарій.
- [SJ Games: Ogre resources](https://www.sjgames.com/ogre/resources/) — лінки на повну книгу правил 6-го видання, Designer's Edition, турнірні правила.
- [Steam: Ogre (Auroch Digital)](https://store.steampowered.com/app/517780) — кампанія, скірміш з AI, hotseat, асинхронний онлайн, юніти Mark I–VI, G.E.V.-правила, Scenario Creator і експорт мапи.
- YouTube: пошук «Ogre Steve Jackson board game how to play».

## Непевне
- (?) Набір гармат Mark III (кількість Secondary, AP, ракет) — у Wikipedia лише Mark III = 45 гусениць, M3; точні числа — у PDF правил, який не прочитано (>10 МБ).
- (?) Точний поріг гусениць: «¼ втрачених гусениць = −1 руху» — з прикладу правил; округлення для Mark V (60) не перевірено.
- (?) Умови перемоги за рівнями (CP знищено + Ogre втік / не втік) у 6-му виданні; D CP (D0 чи D1) різниться між виданнями.
- (?) Рельєф пізніших видань (місто, ліс, болото, вода) і його вплив на рух.
- (?) Рівні AI і лобі в цифровій версії.
