---
title: Persona 5 Tactica
slug: persona-5-tactica
aka: [P5T, P5 Tactica, "ペルソナ5 タクティカ"]
family: tactics
also: []
klass: figure
axes:
  field: layers
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 2023
platforms: [Switch, PS4, PS5, Windows, Xbox One, Xbox Series X/S]
links:
  - {kind: other, url: "https://samurai-gamers.com/persona-5-tactica/p5t-battle-system-guide/", best: true, note: "Samurai Gamers: рух до атаки, мілі відкидає, Down → 1 MORE, скидання з висоти + Follow-Up, Triple Threat, Charge, Voltage, елементи сцени"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Persona_5_Tactica", note: "загін до 3, укриття, 1 More, Triple Threat, Persona/SP, Sub-Persona, фʼюжн, DLC, платформи"}
  - {kind: other, url: "https://www.gamerguides.com/persona-5-tactica/guide/getting-started/basics/all-elements-buffs-and-debuffs-explained-in-persona-5-tactica", note: "таблиця заклять → дебафів (Sweep, Burn, Shock, Freeze, Vortex, Hypno, Despair, Dizzy, Forget, Sleep), бафи 3 ходи"}
  - {kind: other, url: "https://www.gamerguides.com/persona-5-tactica/guide/getting-started/basics/one-more-explained-in-persona-5-tactica", note: "умови 1 More, типи ворогів (Shielder, Revenger, Launcher, Teleporter, боси)"}
  - {kind: other, url: "https://www.gamerguides.com/persona-5-tactica/guide/getting-started", note: "Triple Threat: трикутник, хто бере участь, R2/Cross; 15 квестів-головоломок"}
  - {kind: other, url: "https://www.gamerguides.com/persona-5-tactica/guide/getting-started/basics/how-to-unlock-ultimate-skills-in-persona-5-tactica", note: "ультимативні навички: квести 13–15, ціни GP/SP"}
  - {kind: steam, url: "https://store.steampowered.com/app/2254740/Persona_5_Tactica/", note: "Steam; DLC Repaint Your Heart"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Persona+5+Tactica+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [hp-damage, melee-vs-ranged, legal-move-highlight, reachable-highlight, path-preview, threat-range, height-levels, status-effects, explode-area, spawner-entity, button-toggle, destroy-all-enemies, reach-exit, ai-opponent, character-select, level-select, sequential-levels, achievements-window, +cover-system, +extra-turn-on-down, +triangle-formation-attack, +knockback, +knock-off-height, +follow-up-attack, +free-move-until-act, +charge-on-wait, +retaliation, +flanking, +status-displacement, +team-gauge-ultimate, +sub-persona-equip, +persona-fusion, +skill-tree, +turn-limit-objectives, +puzzle-missions, +carry-item-to-goal, +new-game-plus]
proposes: ["+trigger:attacked", "+trigger:damaged", "+cond:cover", "+cond:from_behind", "+cond:in_triangle", "+effect:knockback", "+effect:steal_move", "+effect:lure", "+effect:random_walk", "+effect:disarm", "+ui:formation-line", "+ui:voltage-gauge", "+window:fusion-window", "+window:skill-tree", "+window:hideout-hub", "+feature:new-game-plus"]
author: opus
date: 2026-11-09
---

# Persona 5 Tactica — збий ворога з укриття, отримай ще хід і замкни його в трикутник трьох героїв

## Суть
Тактичний спін-оф Persona 5: загін до трьох Фантомних Злодіїв на клітинній карті з висотами проти армії Легіонерів. Ядро — механіка **Down → 1 MORE**: удар по ворогу **поза укриттям** збиває його й дає герою ще одну дію з повним рухом. Тому вся гра — про те, як вибити ворога з-за стіни (мілі відкидає, закляття штовхають, тягнуть, заманюють), а потім оточити збитого трикутником героїв для **Triple Threat** — удару по всіх ворогах усередині трикутника. Закляття тут не мають «стихійної шкоди» — кожне накладає дебаф, що здебільшого **рухає** ціль.

## Поле і час
- Квадратна сітка з висотами: сходи, піднесення, ліфти; «dash-клітини» перекидають між піднесеннями. Скинутий з висоти ворог падає вниз.
- Укриття — стіни/обʼєкти на клітинах; ворог в укритті «Resist»: шкода зменшена або заблокована, Down неможливий.
- Хід: усі герої гравця (у будь-якому порядку, керованого можна міняти будь-коли), потім вороги. Рух вільний у межах дальності, доки герой не атакує — атака закінчує його хід (крім 1 MORE).
- Повна інформація про поле; випадковість — у ефектах деяких навичок і зброї (Dizzy — випадковий рух, Freeze зі зброї «не гарантований»).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Joker | piece | HP, SP, рух, Eiha → Despair | лідер; змінює Sub-Persona, найгнучкіший набір навичок |
| Morgana | piece | Garu → Sweep | здуває ціль у напрямку атаки |
| Ryuji | piece | Zio → Shock | паралізує: ціль не рухається 1 хід |
| Ann | piece | Agi → Burn | відкидає від себе і палить 1 хід |
| Yusuke | piece | Bufu → Freeze | ціль не діє 1 хід; будь-яка шкода розморожує |
| Makoto | piece | Frei → Vortex | стягує ворогів навколо до цілі, шкода всім у вирі |
| Haru | piece | Psi → Hypno | ціль іде до кастера, обходячи перешкоди |
| Erina | piece | Partisan → Forget | лідерка повстанців; заряджена атака збиває навіть в укритті |
| Toshiro | ally | Megido | гість наприкінці Kingdom 3; запускає Triple Threat будь-де, але не утворює трикутник |
| Sub-Persona | object | навички, пасиви | екіпірується на будь-якого героя; здобувається з боїв або фʼюжном |
| Legionnaire / Support / Teleporter | enemy | HP | збиваються, щойно поза укриттям; Teleporter після Down переносить героя на свою клітину |
| Shielder | enemy | щит спереду | Down лише ударом збоку чи ззаду |
| Revenger | enemy | контратака | контратакує першого нападника; контратака оновлюється щоходу |
| Launcher | enemy | — | імунний до Down |
| Бос | boss | фази | імунний до Down поза сценарними подіями |
| Укриття | terrain | — | ховає ворога/героя: Resist, шкода від зброї менша (?) |
| Камера спостереження | spawner | кольорова зона | герой у зоні → викликає ворогів |
| Вибухова бочка | hazard | міцність | вибухає після певної шкоди |
| Dash-клітина | terrain | пара піднесень | стрибок з одного піднесення на інше |
| Сходи | terrain | — | підйом на висоту |
| Ліфт + перемикач | switch | — | натиснути перемикач → ліфт рухається вертикально |
| Trial Gear | object | — | квестовий предмет: донести до цілі |
| Ціль (target) | zone | — | клітина/зона, куди треба дійти або донести |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `custom: «кожен герой ходить окремо: вільний рух у межах дальності, доки не атакує; керованого героя можна змінити будь-коли»`.
- КОЛИ `input(attack, hero, target)` → ТО `end_turn` для цього героя (крім 1 MORE).
- КОЛИ `input(melee, hero, enemy)` → ЯКЩО `in_range(hero, enemy, 1)` → ТО `damage(enemy, melee)`, `push(enemy)`; мілі ефективна проти ворога в укритті.
- КОЛИ `input(gun, hero, enemy)` → ЯКЩО `line_of_sight(hero, enemy)` і `in_range(hero, enemy, gun_range)` → ТО `damage(enemy, gun)`; ЯКЩО `custom: «ціль в укритті»` → ТО `custom: «шкода зменшена, ціль лишається в укритті»`.
- КОЛИ `custom: «атака завдала шкоди ворогу»` → ЯКЩО `custom: «ціль не в укритті»` і `not state(enemy, down)` → ТО `set_state(enemy, down)`, `extra_move` (1 MORE: ще одна дія і повний рух від місця удару).
- КОЛИ `turn_start(enemy)` → ТО `clear_state(enemy, down)`; до того збитий ворог не дає нового 1 MORE (на інших ворогах — скільки завгодно за хід).
- КОЛИ `custom: «удар по Shielder»` → ЯКЩО `not facing(shielder, away)` (удар спереду) → ТО `custom: «Down неможливий»`.
- КОЛИ `custom: «перша атака по Revenger за хід»` → ТО `custom: «контратака по нападнику; Down стає можливим лише після неї»`.
- КОЛИ `custom: «Down по Teleporter»` → ТО `teleport(hero, teleporter_cell)`.
- КОЛИ `custom: «збитого ворога скинуто з висоти»` → ТО `extra_move`; ЯКЩО `custom: «біля місця падіння стоїть союзник»` → ТО `damage(enemy, follow_up)`.
- КОЛИ `input(triple_threat, hero)` → ЯКЩО `state(hero, one_more)` і `custom: «збитий ворог усередині трикутника з трьох героїв»` → ТО `damage(enemies_in_triangle, melee+gun)`; учасник із дебафом (крім Burn і Despair) не бере участі.
- КОЛИ `input(skill, hero, target)` → ЯКЩО `counter(SP, ≥, cost)` → ТО `counter(SP, -cost)`, `damage(area, n)` і дебаф закляття.
- КОЛИ `custom: «Sweep (Garu)»` → ТО `push(target)` у напрямку атаки.
- КОЛИ `custom: «Burn (Agi)»` → ТО `push(target)` від кастера, `set_state(target, burn, 1)` (шкода).
- КОЛИ `custom: «Shock (Zio)»` → ТО `set_state(target, no_move, 1)`.
- КОЛИ `custom: «Freeze (Bufu)»` → ТО `stun(target, 1)`.
- КОЛИ `custom: «замороженому завдано шкоди»` → ТО `clear_state(target, freeze)`.
- КОЛИ `custom: «Vortex (Frei)»` → ТО `pull(enemies_around, target)`, `damage(enemies_in_vortex, n)`.
- КОЛИ `custom: «Hypno (Psi)»` → ТО `custom: «ціль іде до кастера, обходячи перешкоди»`.
- КОЛИ `custom: «Despair (Eiha)»` → ТО `custom: «ціль втрачає рух, кастер отримує +рух наступного ходу»`.
- КОЛИ `custom: «Dizzy (Kouga)»` → ТО `custom: «1 хід рухається випадково, але атакує»`; `custom: «Forget (Partisan)»` → `custom: «не атакує 1 хід»`; `custom: «Sleep (зброя)»` → `stun(target, 2)`.
- КОЛИ `input(buff, hero)` → ТО `set_state(allies, attack_up|defense_up|move_up, 3)` (Tarukaja / Rakukaja / Sukukaja; Ma- — на весь загін); дебафів характеристик у грі нема, бафи не знімаються.
- КОЛИ `turn_end(hero)` → ЯКЩО `custom: «герой не діяв цього ходу»` → ТО `set_state(hero, charge, 1)` — наступна атака сильніша; заряджена атака Erina збиває навіть в укритті.
- КОЛИ `counter(voltage, ==, max)` → ТО `custom: «доступна унікальна навичка героя (атака або підтримка)»`.
- КОЛИ `enter(hero, camera_zone)` → ТО `spawn(enemies)`.
- КОЛИ `custom: «бочка отримала достатньо шкоди»` → ТО `explode(area, n)`.
- КОЛИ `enter(hero, dash_square)` → ТО `move(hero, other_height)`.
- КОЛИ `input(switch)` → ТО `custom: «ліфт везе вгору/вниз»`.
- КОЛИ `all_gone(enemy)` → ЯКЩО `mode(defeat_all)` → ТО `win`.
- КОЛИ `reach(hero, target)` → ЯКЩО `mode(reach)` → ТО `win`.
- КОЛИ `reach(trial_gear, target)` → ЯКЩО `mode(carry)` → ТО `win`.
- КОЛИ `counter(turn, >, limit)` → ЯКЩО `mode(turn_limit)` → ТО `lose` (квести: «дійти за 1 хід», «перемогти за 4 ходи»).
- Перемога: ціль місії (усіх / дійти / донести / за N ходів) · Поразка: провал цілі або загін вибито (?) · Рахунок: —; нагороди — досвід, Persona, валюта.

## Керування і ввід
- Геймпад або клавіатура: курсор по клітинах, вибір героя, синя зона руху і `path-preview`; рух не фіксується, доки герой не атакує.
- Перед атакою — вибір: мілі, зброя, закляття Persona (з ціною SP), навички Sub-Persona.
- Triple Threat: R2 — превʼю трикутника (лінія червоніє й «горить», коли він валідний), Cross — підтвердити.
- Кінець ходу героя без дії → Charge.

## Вікна, меню, HUD
- `game-screen` бою: сітка з висотами, `hp-bar` і SP героїв, `legal-move-highlight` руху, `threat-range` ворогів, позначка «в укритті», лінія трикутника (`+ui:formation-line`), шкала Voltage (`+ui:voltage-gauge`), `objective-text` і `turn-counter` для місій з лімітом.
- `custom-window` «Хованка» (`+window:hideout-hub`): вхід у місії, квести, Velvet Room, магазин/крафт зброї (?).
- `custom-window` Velvet Room (`+window:fusion-window`): фʼюжн Persona, спадкування пасивів.
- `custom-window` дерево навичок (`+window:skill-tree`): вузли за GP; ультимативна навичка — після всіх заклять двох рядів вище.
- `level-select` місій по королівствах (Kingdom 1–4) і `puzzle-select` квестів.
- `dialogue-window` — сюжетні сцени у стилі візуальної новели.
- `character-select` — склад загону з трьох; `end-screen` місії з нагородами; `settings-window`; `achievements-window` (Steam).

## Фічі поза полем
- Прогресія: місії сюжету по чотирьох королівствах + 15 квестів-головоломок (ліміт ходів, донести предмет, дійти за 1 хід); квести 13–15 (Lavenza's trials після місії 45) відкривають ультимативні навички.
- `+feature:new-game-plus`, «missables» і точка неповернення (за назвою сторінки гайда).
- Persona: збір з боїв, фʼюжн, Sub-Persona на будь-якого героя; GP → дерево навичок; бафи-пасиви (Auto-Mataru, Auto-Riser).
- DLC Repaint Your Heart (Akechi, Kasumi, «remixed battle elements»); перший тираж — Persona Izanagi Picaro і Orpheus Picaro.
- Steam: хмарні сейви, досягнення, 13 мов.

## Варіації й родичі
- Ядро серії Persona: «1 More» за влучання в слабкість і All-Out Attack по всіх збитих — тут перенесено на сітку: слабкість = «поза укриттям», All-Out = Triple Threat у трикутнику.
- Родичі в корпусі: [Mario + Rabbids](mario-rabbids-kingdom-battle.md) (рух як атака, укриття, сплеш), [XCOM](xcom.md) (укриття), [Triangle Strategy](triangle-strategy.md) (pincer — удар союзника з протилежного боку), [Fire Emblem](fire-emblem.md), [Into the Breach](into-the-breach.md) (штовхання як головна зброя), [Metal Slug Tactics](metal-slug-tactics.md) (синхронна атака союзників).
- **Осі варіацій**: додатковий хід — за Down поза укриттям (P5T) / за вбивство / нема · атака формацією — трикутник з трьох (P5T) / pincer з двох ([Triangle Strategy](triangle-strategy.md)) / союзник у лінії огляду ([Metal Slug Tactics](metal-slug-tactics.md)) · закляття — шкода стихією / дебаф-переміщення (P5T).

## Цікавинки для курсу
- Down → 1 MORE з винятками (вже збитий, в укритті, Shielder спереду, Revenger до контратаки, бос) — 📎: стан + таблиця імунітетів.
- Triple Threat: перевірка «точка в трикутнику з трьох клітин героїв» і шкода всім усередині — 🥉 (геометрія на сітці).
- Закляття-переміщення: штовхнути в напрямку атаки / від кастера / стягнути вир / заманити в обхід перешкод (BFS до кастера) — 🥉 за набір.
- Вільний рух до атаки: хід героя фіксується лише дією, до того позицію можна міняти — 🌱.
- Charge за пропуск дії і Voltage-шкала загону — 📎.
- Камера спостереження: зона, вхід у яку спавнить ворогів — 🌱.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` · `legal-move-highlight` + `reachable-highlight` · `path-preview` · `threat-range` · `height-levels` · `status-effects` (Burn, Freeze, Shock…) · `explode-area` (бочки, площа заклять) · `spawner-entity` (камера) · `button-toggle` (ліфт) · `destroy-all-enemies` · `reach-exit` · `ai-opponent` · `character-select` · `level-select` · `sequential-levels` · `achievements-window`; вікно `dialogue-window` — з `vocab/windows.md`.
- **Нема** → пропозиції карток:
  - `+extra-turn-on-down` «Збий — отримай ще дію» · game-logic/turns · 📎 · слот {immune: list}.
  - `+triangle-formation-attack` «Атака площею трикутника з трьох союзників» · entities/combat · 🥉.
  - `+knock-off-height` «Скинути з висоти: падіння + бонус» · entities/legality · 📎.
  - `+follow-up-attack` «Союзник добиває поруч із місцем падіння» · entities/combat · 🌱.
  - `+free-move-until-act` «Рух не фіксується до дії» · game-logic/turns · 🌱.
  - `+charge-on-wait` «Пропуск дії заряджає наступну» · entities/state · 🌱.
  - `+status-displacement` «Дебаф, що переміщує ціль (здути, стягнути, заманити)» · entities/move · 🥉 · слот {mode: push|pull|lure|random}.
  - `+team-gauge-ultimate` «Спільна шкала загону відкриває унікальну дію» · entities/state · 📎.
  - `+sub-persona-equip` / `+persona-fusion` «Друга душа з навичками; злиття двох у нову» · game-logic/progress · 🥉.
  - `+puzzle-missions` «Квести-головоломки з фіксованою ситуацією» · levels/bank · 📎.
  - `+carry-item-to-goal` «Донести предмет до цілі» · game-logic/win · 🌱.
  - `+cover-system` / `+knockback` / `+retaliation` / `+flanking` / `+skill-tree` / `+turn-limit-objectives` / `+new-game-plus` — уже пропоновані корпусом.

## Пропозиції до словників
- `+trigger:attacked` — сутність атакована (контратака Revenger).
- `+trigger:damaged` — сутності завдано шкоди (розморожування Freeze, вибух бочки).
- `+cond:cover` — ціль в укритті відносно атакувальника (Resist).
- `+cond:from_behind` — удар збоку/ззаду (Shielder).
- `+cond:in_triangle` — клітина всередині трикутника трьох сутностей.
- `+effect:knockback` — відкинути від атакувальника (Burn, мілі).
- `+effect:steal_move` — забрати частину руху цілі собі (Despair).
- `+effect:lure` — ціль сама йде до джерела в обхід перешкод (Hypno).
- `+effect:random_walk` — ціль рухається випадково N ходів (Dizzy).
- `+effect:disarm` — ціль не атакує N ходів (Forget).
- `+ui:formation-line` — лінія між союзниками, що показує валідну формацію; `+ui:voltage-gauge` — шкала загону.
- `+window:fusion-window` — злиття Persona; `+window:skill-tree` — дерево навичок за GP; `+window:hideout-hub` — хаб між місіями.
- `+feature:new-game-plus` — повторне проходження з перенесенням прогресу.

## Джерела
- ⭐ [Samurai Gamers: Battle System Guide](https://samurai-gamers.com/persona-5-tactica/p5t-battle-system-guide/) — вільний рух до атаки, «хід закінчується атакою», мілі відкидає, Down → 1 MORE, скидання з висоти + Follow-Up, Triple Threat, Charge (Erina), Voltage, камери, бочки, dash-клітини, сходи, ліфти.
- [Wikipedia](https://en.wikipedia.org/wiki/Persona_5_Tactica) — загін до 3, укриття зменшує/блокує шкоду, 1 More, Triple Threat, Persona і SP, стихії рухають ворогів, Sub-Persona, фʼюжн, DLC, платформи, дата.
- [Gamer Guides: елементи, бафи й дебафи](https://www.gamerguides.com/persona-5-tactica/guide/getting-started/basics/all-elements-buffs-and-debuffs-explained-in-persona-5-tactica) — закляття → дебаф і точні формулювання ефектів, бафи 3 ходи.
- [Gamer Guides: One More](https://www.gamerguides.com/persona-5-tactica/guide/getting-started/basics/one-more-explained-in-persona-5-tactica) — умови Down, імунітети, типи ворогів.
- [Gamer Guides: getting started / Triple Threat](https://www.gamerguides.com/persona-5-tactica/guide/getting-started) — учасники трикутника, превʼю R2, шкода = мілі + зброя, Toshiro, 15 квестів.
- [Gamer Guides: ультимативні навички](https://www.gamerguides.com/persona-5-tactica/guide/getting-started/basics/how-to-unlock-ultimate-skills-in-persona-5-tactica) — квести 13–15 з цілями, ціни GP/SP.
- [Steam](https://store.steampowered.com/app/2254740/Persona_5_Tactica/) — опис, функції Steam, мови.

## Непевне
- (?) Укриття: Wikipedia — «зменшує або блокує повністю»; чи є два рівні укриття (низьке/високе) — не підтвердив.
- (?) Чи стрільба по ворогу в укритті завдає шкоди взагалі («guns neither dislodge nor strike through cover» у гайді).
- (?) Умова поразки (вибито весь загін чи лише Joker) — не бачив.
- (?) Voltage — лише в одному гайді; як наповнюється і чи спільна шкала — не знайшов.
- (?) Магазин/крафт зброї в Хованці — відомо лише, що Sleep «є на деяких скрафчених зброях».
- (?) Рівні складності й пункти головного меню — не перевіряв.
- (?) Zio: «Shock — не рухається 1 хід» (Gamer Guides) vs «paralysis» (Samurai Gamers) — те саме чи ні.
