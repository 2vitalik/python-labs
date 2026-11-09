---
title: DoomRL / DRL → Jupiter Hell
slug: doomrl
aka: [DRL, Doom, the Roguelike, Jupiter Hell, Jupiter Hell Classic]
family: roguelike
also: [tactics]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2002
platforms: [PC (Windows, Linux, macOS), Switch (Jupiter Hell)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/DoomRL", best: true, note: "суть: покроковий шутер-роглайк за Doom, трейти, обмежений інвентар без стаків, тайли Derek Yu / ASCII, історія, звʼязок з Jupiter Hell"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Jupiter_Hell", note: "Jupiter Hell: черга ходів з ціною дій, укриття, дерева навичок, 3 класи"}
  - {kind: wiki, url: "https://www.roguebasin.com/index.php/DoomRL", note: "RogueBasin: 25 рівнів на один екран, рюкзак 19, 4 слоти, класи, спецрівні"}
  - {kind: fandom, url: "https://drl.chaosforge.org/wiki/DRL_Wiki", note: "DRL Wiki: зброя, броня, моди, асамблеї, рівні, складності, механіки"}
  - {kind: other, url: "https://drl.chaosforge.org/wiki/Accuracy", note: "3d6 на влучання, −1 за кожні 3 клітини, модифікатори"}
  - {kind: other, url: "https://drl.chaosforge.org/wiki/Game_Settings", note: "5 складностей з множниками, Angel-челенджі"}
  - {kind: steam, url: "https://store.steampowered.com/app/811320/", note: "Jupiter Hell у Steam"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=doomrl+drl+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-by-input, move-8dir, projectile-shot, shoot-spread, melee-vs-ranged, line-of-sight-attack, explode-area, chain-detonation, blast-wave, push-object, destructible-blocks, floor-types, environment-death, hp-damage, inventory, inventory-items, inventory-limit, item-pickup, temporary-modes, status-effects, unit-xp-skills, chase-bfs, dungeon-generation, stairs-levels, sequential-levels, fog-of-war, permadeath, player-death, difficulty-levels, rule-variants, score-records, message-log, status-panel, keyboard-controls, console-render, gui-render, button-toggle, +hit-chance, +ammo-reload, +weapon-mods, +item-assembly, +trait-pick, +tactics-stance, +special-level-stairs, +challenge-modes, +rank-unlocks, +cover-system, +action-cost-queue]
proposes: ["+trigger:shot(a, target)", "+cond:hit_roll(acc)", "+cond:ammo(a, op, n)", "+cond:stance(a, s)", "+effect:reload", "+effect:fire(weapon, target)", "+effect:apply_mod(item, mod)", "+effect:assemble(item, mods)", "+role:barrel", "+role:special-stairs", "+ui:ammo-counter", "+ui:target-line", "+ui:hit-chance", "+window:trait-select", "+window:challenge-select", "+window:mortem", "+feature:challenge-modes", "+feature:rank-unlocks", "+feature:permadeath", "+axis:session=run", "+card:item-assembly", "+card:tactics-stance"]
author: opus
date: 2026-11-09
---

# DoomRL → Jupiter Hell — Doom у вигляді покрокового роглайка: стрільба з шансом влучання на сітці, бочки, моди зброї й короткий забіг на 25 рівнів

## Суть
Морпіх зачищає 25 рівнів-екранів від Фобоса через Деймос до Пекла, переважно **стріляючи**: кожен постріл — хід, влучання — кидок 3d6 проти точності, що падає з відстанню. Бочки з паливом/кислотою/напалмом можна штовхати й підривати, лишаючи калюжі кислоти чи лави. Зброю вдосконалюють **мод-паками**, а певні комбінації модів дають **асамблеї** — рецепти нових предметів. Режим «біг» (tactics) дає ухилення ціною точності на 30 дій. Jupiter Hell (2019/2021) — 3D-наступник з укриттями й чергою ходів за ціною дії.

## Поле і час
- Квадратна сітка; **рівень = один екран**; 8 напрямків.
- 25 рівнів (за RogueBasin: 24 поверхи + секретні; три етапи Phobos / Deimos / Hell), фінал — бій з Кібердемоном; + опційні спецрівні через червоні спецсходи.
- Покроково: кожна дія має тривалість (рух, постріл, перезаряджання), швидкість впливає на частоту ходів; у Jupiter Hell — явна черга ходів за ціною дії.
- Видимість: поле зору, туман на невідвіданому; поза полем зору постріл має +50 % шанс промаху.
- Шари: підлога / стіни (частина руйнується вибухами) / рідини (кислота, лава, вода) / бочки / предмети (1 на клітину) / монстри.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Морпіх `@` | player | клас (Marine / Scout / Technician), HP, броня, точність, стан тактики, трейти | рух 8 напрямків, стрільба по цілі, ближній бій |
| Зброя (пістолет, дробовик, кулемет, ракетниця, плазма, BFG…) | pickup | шкода (кубики), точність, магазин, тип набоїв, альт-вогонь | стріляє по лінії; дробовик — конусом; ракети — вибух |
| Набої | pickup | тип, кількість | для перезаряджання |
| Броня / чоботи | pickup | захист, опори (стихії) | слот броні / чобіт; зношується (?) |
| Мод-пак (Power, Agility, Bulk, Technical, Firestorm, Sniper, Onyx, Nano) | pickup | тип | кладеться на зброю/броню; комбінація → асамблея |
| Аптечка / сфери | pickup | — | лікування, тимчасові режими (берсерк, невидимість (?)) |
| Ворог (колишні люди, імп, демон, какодемон, барон…) | enemy | HP, точність, швидкість, атака | наближається, стріляє, якщо бачить; деякі — ближній бій |
| Кібердемон / боси | boss | — | фінал і спецрівні |
| Бочка паливна / кислотна / напалмова | object | HP | штовхається; знищена — вибух; кислотна лишає кислоту, напалмова — лаву |
| Кислота / лава / вода | hazard | шкода за хід | шкодить, коли стоїш; біг зменшує шкоду вдвічі |
| Двері | gate | відкриті / закриті / замкнені (більше броні) | відкрити, закрити, вибити |
| Важіль | switch | — | одноразовий ефект на рівень (?) |
| Сходи вниз | static | — | наступний рівень |
| Спецсходи (червоні) | static | на випадковій клітині | вхід у спецрівень з нагородою |
| Укриття (Jupiter Hell) | static | ящики, колони | зменшують шанс влучити в того, хто за ними (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(target)` → ТО `move(marine, dir)`; ЯКЩО `occupied(target, enemy)` → ТО `custom: «удар впритул»`; ЯКЩО `occupied(target, barrel)` → ТО `push(barrel)`.
- КОЛИ `input(fire, target)` → ЯКЩО `custom: «у магазині є набій»` → ТО `custom: «кидок 3d6 ≤ точність → влучання»`; інакше `custom: «клац, треба перезарядити»`.
- КОЛИ `custom: «рахується точність»` → ТО `custom: «база 10 + бонус зброї + трейти − 1 за кожні 3 клітини − 2, якщо біжиш; −4, якщо ціль біжить; +3 прицільний постріл»`; 3–4 — завжди влучання, 17–18 — завжди промах.
- КОЛИ `custom: «постріл поза полем зору»` → ТО `custom: «ще +50 % шанс промаху»` (снайперські моди знімають).
- КОЛИ `input(reload)` → ЯКЩО `has(marine, ammo of type)` → ТО `custom: «магазин повний, витрачено час дії»`.
- КОЛИ `custom: «влучив вибуховий снаряд або промах біля цілі»` → ТО `explode(area)`; `damage(n)` усім у радіусі.
- КОЛИ `destroyed(barrel)` → ТО `explode(area)`; ЯКЩО кислотна → `set_cell(area, acid)`; ЯКЩО напалмова → `set_cell(area, lava)`; поруч бочка → `trigger(chain)`.
- КОЛИ `enter(a, acid|lava)` → ТО `damage(n)`; ЯКЩО `state(marine, running)` → ТО шкода ×½.
- КОЛИ `input(tactics: run)` → ЯКЩО `state(marine, cautious)` → ТО `set_state(marine, running, 30 actions)`: +30 % швидкості руху, +20 % ухилення, −4 точності ворогам по тобі, −2 своєї точності, ближній бій ×½.
- КОЛИ `state_off(marine, running)` → ТО `set_state(marine, tired)`; КОЛИ `level_start` або `custom: «лікувальний предмет»` → ТО `clear_state(marine, tired)` (повертає cautious).
- КОЛИ `input(apply mod, item)` → ЯКЩО `custom: «броня/чоботи/ближня зброя: не більше одного моду кожного типу»` → ТО `custom: «покращення предмета»`.
- КОЛИ `custom: «набір модів на предметі збігся з рецептом асамблеї»` → ТО `transform(item → assembly)` (Basic — 2 моди, Advanced — 3 + трейт Whizkid, Master — 4 + 2 рівні Whizkid).
- КОЛИ `counter(xp, ≥, threshold)` → ТО `choose(trait)` (з деревом передумов; майстер-трейти) (?).
- КОЛИ `line_of_sight(enemy, marine)` → ТО `custom: «ворог стріляє або йде на зближення»`; КОЛИ `custom: «Nightmare!»` → ТО `custom: «вороги воскресають»`.
- КОЛИ `enter(marine, stairs)` and `input(descend)` → ТО `next_level`; ЯКЩО спецсходи → `custom: «спецрівень, потім далі вниз»`.
- КОЛИ `died(Cyberdemon)` (фінальний рівень) → ТО `win`; секретна кінцівка — через приховані рівні/боси (?).
- КОЛИ `hp_zero(marine)` → ТО `lose`, `window(mortem)`.
- КОЛИ `custom: «Angel of Red Alert»` and `level_start` → ТО `timer(start 5 min)`; КОЛИ `timer(0)` → ТО `custom: «ядерний вибух на весь рівень»`.
- Jupiter Hell: КОЛИ `input(action)` → ТО `custom: «наступний хід актора відсувається на ціну дії»`; КОЛИ `custom: «ціль за укриттям»` → ТО `custom: «шанс влучити менший»` (?).
- Перемога: пройти 25 рівнів і вбити фінального боса. Поразка: смерть. Рахунок: множник складності × досвід/кілли (?), ранги й бейджі гравця між партіями.

## Керування і ввід
- Клавіатура: рух (цифри/стрілки), `f` — стріляти (вибір цілі, ціль за замовчуванням — найближча), `F` — альтернативний вогонь, `r` — перезарядити, `R` — альтернативне перезаряджання, `t` — тактика (біг), `z` — перемкнути зброю на запасну, `i` — інвентар, `e` — екіпірування, `u` — використати, `>` — спуск (?).
- Миша: клік — ціль/рух (?).
- Jupiter Hell: миша й геймпад, курсор цілі з показом шансу влучання (?).

## Вікна, меню, HUD
- `game-screen`: мапа (тайли Derek Yu або ASCII), нижня панель `stat-panel` (HP, броня, зброя з `ammo-counter`, стан тактики, рівень/етап), `message-log`.
- `character-select` (клас), `difficulty-select` (5 рівнів), `challenge-select` (Angel / Dual Angel / Archangel, відкриваються рангом).
- `trait-select` — вибір трейта при підвищенні рівня.
- `inventory-window` (рюкзак 19) і екіпірування (4 слоти: зброя, запасна зброя, броня, чоботи).
- `mortem` — текстовий звіт смерті/перемоги (кілли, предмети, трейти); `stats-window` / ранги й бейджі (`achievements-window`); `leaderboard`.
- `main-menu`, `help-window`, `settings-window` (тайли/ASCII, звук).
- Переходи: `main-menu` → клас → складність → (челендж) → гра; смерть → `mortem` → меню.

## Фічі поза полем
- `difficulty-presets`: I'm Too Young to Die (×0.5 рахунку, ×2 набоїв) … Nightmare! (×4, вороги воскресають); Ultra-violence і Nightmare! відкриваються рангом.
- `challenge-modes`: Angel of Berserk (лише ближній бій), Marksmanship (пістолети), Shotgunnery, Light Travel (інвентар 5), Impatience (споживане — одразу), Purity, Red Alert (ядерний таймер), Darkness (зір 6), Max Carnage, 100 (100 поверхів), Pacifism, Humanity (10 HP), Confidence/Overconfidence (старт на Деймосі/в Пеклі); Dual-Angel — комбінації; Archangel — жорсткіші.
- `rank-unlocks`: ранги гравця (Private … Captain) і бейджі між партіями відкривають челенджі й складності.
- Відкритий код (GPL, 2016), моди (Lua) (?).
- Jupiter Hell Classic (2025) — рімейк на рушії DRL.

## Варіації й родичі
- [rogue](rogue.md), [nethack](nethack.md) — ближній бій як ядро; тут — дальній; [cogmind](cogmind.md) — теж стрільба з шансом і компоненти; [brogue](brogue.md) — вибухи й рідини.
- Наступники: Jupiter Hell (2021, 3D, укриття, дерева навичок), Jupiter Hell Classic (2025).
- Тактичні родичі з укриттями: XCOM (шанс влучання, half/full cover) → `tactics`.
- Осі варіацій: **влучання** (завжди / кубик проти точності / залежить від укриття) · **набої** (безкінечні / магазин і запас) · **рівень** (один екран / прокрутка) · **вдосконалення** (трейти / моди / асамблеї-рецепти).

## Цікавинки для курсу
- Шанс влучання 3d6 проти точності з модифікаторами відстані й тактики — 📎 (дзвоноподібний розподіл замість рівномірного).
- Бочки: штовхання, вибух, ланцюг, калюжі кислоти/лави — 🥉.
- Мод-паки й асамблеї: збіг мультимножини модів з рецептом → новий предмет — 📎.
- Стан «біг» на 30 дій з фазою втоми до наступного рівня — 🌱.
- Магазин і перезаряджання як окрема дія з ціною часу — 🌱.
- Челенджі як конструктор правил (обмеження зброї, інвентаря, таймер) — 📎.
- Укриття (Jupiter Hell): лінія від стрільця до цілі через клітину укриття — 🥉.

## Мапа на каталог
- Є: `move-8dir` · `projectile-shot` · `shoot-spread` (дробовик) · `melee-vs-ranged` · `line-of-sight-attack` · `explode-area` · `chain-detonation` (бочки) · `blast-wave` · `push-object` (бочки) · `destructible-blocks` (стіни під вибухом) · `floor-types` + `environment-death` (кислота, лава) · `hp-damage` · `inventory` + `inventory-limit` (19) · `temporary-modes` (сфери) · `status-effects` · `unit-xp-skills` (трейти) · `chase-bfs` · `stairs-levels` · `sequential-levels` · `fog-of-war` · `permadeath` · `difficulty-levels` · `rule-variants` (челенджі) · `score-records` · `message-log` · `console-render` + `gui-render` · `button-toggle` (важелі).
- **Нема** → пропозиції карток:
  - `+hit-chance` «Шанс влучання кидком проти точності» · entities/combat · 📎 · слоти {dice, modifiers}.
  - `+ammo-reload` «Магазин, запас і перезаряджання» · entities/combat · 🌱 · слоти {clip, ammo_type}.
  - `+weapon-mods` «Мод-паки на зброю/броню з лімітом за типом» · game-logic/economy · 📎.
  - `+item-assembly` «Рецепт: набір модів → новий предмет» · game-logic/economy · 📎 · слоти {recipes}.
  - `+trait-pick` «Вибір трейта за рівень з деревом» · game-logic/economy · 📎.
  - `+tactics-stance` «Стійка з бонусами/штрафами й тривалістю» · entities/combat · 🌱.
  - `+special-level-stairs` «Спецсходи у бічний рівень» · game-logic/levels · 🌱.
  - `+challenge-modes` «Челенджі-обмеження з рангом відкриття» · game-logic/settings · 📎.
  - `+rank-unlocks` «Ранги гравця між партіями відкривають режими» · game-logic/progress · 📎.
  - `+cover-system` «Укриття зменшує шанс влучання» · entities/combat · 🥉.
  - `+action-cost-queue` «Черга ходів за ціною дії» · game-logic/turns · 📎.

## Пропозиції до словників
- `+trigger:shot(a, target)` — сутність вистрілила (для правил реакції).
- `+cond:hit_roll(acc)` — кидок влучання вдався; `+cond:ammo(a, op, n)`; `+cond:stance(a, s)` (cautious/running/tired; вужче за `state`, але читається краще — на розсуд куратора).
- `+effect:reload`, `+effect:fire(weapon, target)`, `+effect:apply_mod(item, mod)`, `+effect:assemble(item, mods)`.
- `+role:barrel` — штовхана вибухова сутність; `+role:special-stairs`.
- `+ui:ammo-counter`, `+ui:target-line` (лінія до цілі), `+ui:hit-chance` (шанс над ціллю).
- `+window:trait-select`, `+window:challenge-select`, `+window:mortem` (текстовий звіт партії).
- `+feature:challenge-modes`, `+feature:rank-unlocks`, `+feature:permadeath`.
- `+axis:session=run`.
- `+card:item-assembly`, `+card:tactics-stance`.

## Джерела
- ⭐ [Wikipedia: DoomRL](https://en.wikipedia.org/wiki/DoomRL) — покроковий шутер, трейти, обмежений інвентар, тайли/ASCII, історія, перейменування на DRL, Jupiter Hell (Classic).
- [Wikipedia: Jupiter Hell](https://en.wikipedia.org/wiki/Jupiter_Hell) — черга ходів за ціною дії, укриття, 3 класи, дерева навичок.
- [RogueBasin: DoomRL](https://www.roguebasin.com/index.php/DoomRL) — 25 рівнів на екран, рюкзак 19, 4 слоти, класи, спецрівні, челенджі.
- [DRL Wiki: Accuracy](https://drl.chaosforge.org/wiki/Accuracy) — 3d6, таблиця шансів, −1/3 клітини, модифікатори.
- [DRL Wiki: Tactics](https://drl.chaosforge.org/wiki/Tactics) — cautious / running (30 дій, +30 % руху, +20 % ухилення) / tired.
- [DRL Wiki: Assemblies](https://drl.chaosforge.org/wiki/Assemblies) — 8 типів модів, Basic/Advanced/Master, Whizkid.
- [DRL Wiki: Levels](https://drl.chaosforge.org/wiki/Levels) — етапи, спецрівні й червоні спецсходи, бочки, двері, важелі.
- [DRL Wiki: Game Settings](https://drl.chaosforge.org/wiki/Game_Settings) — 5 складностей з множниками, усі челенджі.
- [Steam: Jupiter Hell](https://store.steampowered.com/app/811320/) — «коли дієш ти, діють вороги», permadeath.

## Непевне
- (?) Клавіші (`f`/`F`/`r`/`R`/`t`/`z`), миша — з памʼяті.
- (?) Як саме працює укриття в Jupiter Hell (half/full, кути) — Вікіпедія лише згадує «cover provides protection».
- (?) Рахунок і бейджі: формула, перелік — Achievements-сторінку не відкривав.
- (?) Важелі (ефекти), зношування броні, сфери (які саме), майстер-трейти — не перевірено.
- (?) Рік: Вікіпедія дає 2002 у вступі й 2005 в інфобоксі.
