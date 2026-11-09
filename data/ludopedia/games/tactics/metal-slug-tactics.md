---
title: Metal Slug Tactics
slug: metal-slug-tactics
aka: [MST]
family: tactics
also: [roguelike]
klass: figure
axes:
  field: layers
  time: turn
  opponent: ai
  info: full
  random: setup
  goal: state
year: 2024
platforms: [Windows, Switch, PS4, PS5, Xbox One, Xbox Series X/S]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Metal_Slug_Tactics", best: true, note: "2 дії за хід (рух + дія), що далі пройшов — то вищий захист, sync-атаки, адреналін, танк з пальним, ревайв, роглайт-кампанія"}
  - {kind: other, url: "https://news.xbox.com/en-us/2024/11/06/five-things-before-you-dive-into-metal-slug-tactics/", note: "Xbox Wire: Dodge і Cover Points, укриття вибухає, sync — усі з лінією огляду, 9 героїв і їхні ролі, пасиви адреналіну"}
  - {kind: other, url: "https://www.rpgfan.com/2024/06/10/metal-slug-tactics-impressions/", note: "RPGFan: атаки лише на тій самій висоті, sync без ліміту, танк і пальне, типи місій, One-Up, вузли кампанії"}
  - {kind: steam, url: "https://store.steampowered.com/app/1590760/Metal_Slug_Tactics/", note: "110 мап, 20 типів місій, 36 зброї, 176 модів, 9 героїв"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Metal+Slug+Tactics+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [hp-damage, melee-vs-ranged, line-of-sight-attack, height-levels, destructible-blocks, explode-area, reachable-highlight, path-preview, ai-opponent, destroy-all-enemies, respawn, character-select, shop-between-levels, in-round-upgrades, run-relics, map-window, end-screen, +dodge-from-distance, +sync-attack, +adrenaline-resource, +cover-system, +cover-explodes, +move-then-act, +same-height-attack, +secondary-ammo, +fuel-ammo, +vehicle-eject, +support-strike-call, +revive-tokens, +bonus-action-on-kill, +escape-target, +turn-limit-survive, +bonus-objectives, +collapsing-floor, +node-map-run, +run-meta-carry, +decoy-summon, +delayed-damage-mine, +weapon-mods]
proposes: ["+trigger:moved", "+trigger:ally_attacked", "+cond:same_height", "+cond:cover", "+effect:sync_attack", "+effect:eject", "+effect:revive", "+ui:dodge-meter", "+ui:adrenaline-bar", "+ui:fuel-gauge", "+ui:sync-line", "+window:outpost-hub", "+window:run-map", "+window:level-up-choice", "+feature:run-reset"]
author: opus
date: 2026-11-09
---

# Metal Slug Tactics — біжи, щоб вижити: пройдена відстань стає захистом, а союзники в лінії огляду стріляють разом з тобою

## Суть
Покрокова тактика-роглайт за мотивами run-and-gun серії Metal Slug: загін з трьох «Peregrine Falcons» проходить регіони з місіями до боса. Головна ідея — **рух як захист**: що більше клітин герой пройшов за хід, то більше в нього Dodge (зниження шкоди) і адреналіну для спецдій; стояти на місці — смерть. Друга — **SYNC**: коли герой атакує, кожен союзник, що бачить ціль, безкоштовно стріляє своєю основною зброєю. Поразка всього загону — кінець забігу і повернення на базу.

## Поле і час
- Ізометрична клітинна мапа з **висотами**: атакувати можна лише ціль на тій самій висоті (окремі зброї/вміння — винятки); перехід між рівнями забирає час.
- Блакитні клітини — укриття; укриття руйнується (і вибухає), разом з ним зникає захист.
- Хід: усі герої гравця, потім вороги. У героя **2 дії**: рух і дія; після дії рухатися зазвичай не можна — спершу позиція, потім постріл.
- Мапи кампанії змінюються між забігами; деякі мапи змушують рухатися, бо підлога зникає.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Marco Rossi | piece | основна зброя ∞, другорядна з ammo, спецдії | підтримка й підсилення sync; Determination — −1 ціна спецдій за кожен sync |
| Eri Kasamoto | piece | гранати | вибухові вміння, що використовують висоту |
| Tarma Roving | piece | ближня дистанція | оборонний, накопичує Dodge, точні удари |
| Fio Germi | piece | кулемет по лінії | переставляє союзників і ворогів (Nudge — у перехресний вогонь) |
| Trevor Spacey | piece | — | контроль розуму: бʼє й переставляє, сильніший від кількості цілей |
| Nadia Cassel | piece | міни, роботи | приманки, підтримка, керовані бомби; відкладена шкода |
| Ralf Jones | piece | мілі-рухливий | бонусна дія за вбивство спецдією |
| Clark Still | piece | мілі-оборонний | кидає ворогів (Argentine Backbreaker), дебафи |
| Leona Heidern | piece | — | лишає «післяобрази», що теж роблять sync |
| Солдат Rebel Army | enemy | HP | стріляє, ховається в укриття |
| Гренадер | enemy | — | кидає гранати здалеку, ховається в укриття |
| Мечник | enemy | — | атакує першим (?) |
| Бос (лінкор із турелями) | boss | турелі | фінал регіону |
| Конвой | enemy | рух до краю | мета місії: знищити до втечі |
| Укриття | terrain | HP, Cover Points | дає захист тому, хто закінчив рух поруч; зруйноване вибухає |
| Небезпека середовища | hazard | — | шкодить ворогам, якщо їх туди загнати |
| Підлога, що зникає | terrain | — | змушує рухатися далі |
| METAL SLUG (танк SV) | ally | більше HP, пальне | пальне — і на рух, і на зброю; можна вистрілити всім за хід, поки є пальне; катапультуватися до знищення |
| Підтримка (артилерія, авіаудар) | projectile | — | виклик підкріплення на поле |
| Міна / робот-приманка | object | — | відкладена шкода / відволікає ворогів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `custom: «кожен герой: 1 дія руху + 1 дія атаки/вміння; після атаки зазвичай не рухається»`.
- КОЛИ `input(move, hero, cell)` → ЯКЩО `path_exists(hero, cell)` у межах руху → ТО `move(hero)`, `counter(dodge, +distance)`, `counter(adrenaline, +distance)` (темніша зелена клітина = більше).
- КОЛИ `custom: «герой закінчив рух на/біля блакитної клітини укриття»` → ТО `set_state(hero, cover_points)`.
- КОЛИ `custom: «ворог атакує героя»` → ТО `damage(hero, n − dodge − cover)` (?) — Dodge знижує або повністю скасовує шкоду.
- КОЛИ `input(attack_primary, hero, target)` → ЯКЩО `in_range(hero, target, weapon_range)` і `custom: «ціль на тій самій висоті»` → ТО `damage(target, weapon)`; набоїв нескінченно.
- КОЛИ `input(attack_secondary, hero, target)` → ЯКЩО `has(hero, ammo)` → ТО `damage(target, weapon)`, `take(hero, ammo)`; спецнабої не поповнюються між місіями забігу.
- КОЛИ `input(special, hero)` → ЯКЩО `counter(adrenaline, ≥, cost)` → ТО `counter(adrenaline, -cost)`, `custom: «ефект вміння: площа, переставлення, кидок, міни…»`.
- КОЛИ `custom: «герой атакує ціль (основна, другорядна або спецдія)»` → ЯКЩО `line_of_sight(ally, target)` → ТО `custom: «SYNC: союзник безкоштовно бʼє основною зброєю»`; ліміту учасників нема.
- КОЛИ `custom: «sync відбувся»` → ЯКЩО `has(hero, team_leader)` → ТО `counter(adrenaline, +2)`; ЯКЩО `custom: «Marco брав участь»` → ТО `custom: «ціна його спецдій −1»`.
- КОЛИ `input(special, marco)` → ЯКЩО `counter(special_cost, ==, 0)` → ТО `extra_move` (Efficiency).
- КОЛИ `died(enemy)` → ЯКЩО `custom: «вбито спецдією Ralf»` → ТО `extra_move`.
- КОЛИ `died(enemy)` → ЯКЩО `has(weapon, impressive_mod)` → ТО `counter(adrenaline, +1)`.
- КОЛИ `input(nudge|throw, hero, unit)` → ТО `push(unit)` — у перехресний вогонь або в небезпеку.
- КОЛИ `custom: «ворога загнано в небезпеку середовища»` → ТО `damage(enemy, n)`.
- КОЛИ `hp_zero(cover)` → ТО `explode(area)`, `custom: «Cover Points поруч зникають»`.
- КОЛИ `input(call_support, artillery|airstrike|metal_slug)` → ТО `spawn_at(support, target)`.
- КОЛИ `input(tank_action)` → ЯКЩО `counter(fuel, ≥, cost)` → ТО `custom: «рух або постріл будь-якою системою танка»`, `counter(fuel, -cost)`.
- КОЛИ `input(eject, hero)` → ЯКЩО `state(hero, in_tank)` → ТО `custom: «герой виходить з танка на сусідню клітину»`; знищений танк з героєм — `damage(hero)` (?).
- КОЛИ `hp_zero(hero)` → ЯКЩО `counter(revives, ≥, 1)` → ТО `respawn(hero)`, `counter(revives, -1)` (очки підкріплення / One-Up не поповнюються в межах забігу).
- КОЛИ `reach(convoy, edge)` → ЯКЩО `mode(convoy)` → ТО `lose`.
- КОЛИ `counter(turn, ==, n)` → ЯКЩО `mode(survive)` → ТО `win`.
- КОЛИ `custom: «ключових ворогів знищено»` → ЯКЩО `mode(eliminate)` → ТО `win`.
- КОЛИ `custom: «мету-опцію виконано (позначений ворог останнім, усі вижили)»` → ТО `custom: «бонусна нагорода»`.
- КОЛИ `custom: «усі герої загону вибиті»` → ТО `lose`, `custom: «кінець забігу — повернення на базу, кампанія з початку»`.
- КОЛИ `custom: «бос регіону переможений»` → ТО `next_level` (наступний регіон).
- Перемога: мета місії; забіг — усі регіони й боси · Поразка: загін вибито (кінець забігу) або провалено мету · Рахунок: досвід після бою → рівні, зброя, перки.

## Керування і ввід
- Курсор по клітинах: вибір героя → зона руху з градієнтом (темніше = більше Dodge/адреналіну) і `path-preview`; потім вибір зброї/вміння й цілі; превʼю показує, хто з союзників зробить sync (?).
- Правий стік (геймпад) — огляд прихованих клітин на іншій висоті.
- Перед місією: склад загону з трьох, лоадаут зброї й модів.

## Вікна, меню, HUD
- `custom-window` база Falcon (`+window:outpost-hub`): вибір загону, апгрейди вмінь, моди зброї, крамниці продавців.
- `character-select` — 3 з 9 героїв, лоадаути (36 комбінацій).
- `map-window` регіону (`+window:run-map`): вузли-місії, що проходяться в будь-якому порядку, бос у кінці.
- `game-screen` місії: ізометрична мапа, `hp-bar`, `+ui:dodge-meter`, `+ui:adrenaline-bar`, набої другорядної зброї, `+ui:fuel-gauge` танка, `objective-text`, лічильник ходів для «вижити N ходів», `+ui:sync-line` (?).
- `custom-window` рівень героя (`+window:level-up-choice`): нове вміння + випадковий мод або тактичний ресурс.
- `shop-window` — продавці зброї й предметів на базі; `end-screen` місії й забігу; `settings-window`.

## Фічі поза полем
- Роглайт-структура: забіг = регіони з вузлами місій і босом; поразка загону — `+feature:run-reset`; досвід і розблокування лишаються (`meta-progression`).
- Контент: 110 рукотворних мап, 20 типів місій, 36 зброї, 176 модів, 9 героїв.
- Моди зброї: пробивання, ігнорування укриття, додаткова шкода; здобуваються за певні місії.
- Підкріплення: важка артилерія, авіаудари, сам METAL SLUG.

## Варіації й родичі
- Родичі в корпусі: [XCOM](xcom.md) (укриття, загін, роглайт-кампанія — у Chimera Squad), [Into the Breach](into-the-breach.md) (штовхання ворога в небезпеку), [Persona 5 Tactica](persona-5-tactica.md) (атака з участю союзників — трикутник), [Triangle Strategy](triangle-strategy.md) (pincer), [Mario + Rabbids](mario-rabbids-kingdom-battle.md) (рух як атака), [Hoplite](hoplite.md).
- **Осі варіацій**: захист — укриття ([XCOM](xcom.md)) / укриття + пройдена відстань (MST) / позиція відносно атакувальника · спільна атака — sync усіх, хто бачить (MST) / формація трьох ([Persona 5 Tactica](persona-5-tactica.md)) / союзник з протилежного боку ([Triangle Strategy](triangle-strategy.md)) · ресурс спецдій — мана/SP / адреналін від руху (MST) / перезарядка.

## Цікавинки для курсу
- Dodge від пройденої відстані: довжина шляху цього ходу → знижка шкоди — 🌱; з градієнтом на зоні руху — 📎.
- SYNC: після атаки знайти всіх союзників з лінією огляду на ціль і виконати їхні постріли — 🥉 (LOS на сітці з висотами).
- Адреналін як валюта від руху й атак + пасиви, що міняють ціну — 📎.
- Атака лише на тій самій висоті — 🌱; винятки-зброя — слот.
- Танк з одним баком пального на рух і всі гармати — 📎.
- Роглайт-петля «база → регіон з вузлами → бос → смерть → база з розблокуваннями» — 🥈.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` (Clark, Ralf) · `line-of-sight-attack` (sync) · `height-levels` · `destructible-blocks` (укриття) · `explode-area` (укриття, гранати) · `reachable-highlight` · `path-preview` · `ai-opponent` · `destroy-all-enemies` · `respawn` (ревайв) · `character-select` · `shop-between-levels` · `in-round-upgrades` (рівень героя в забігу) · `run-relics` (моди й тактичні ресурси) · `map-window` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+dodge-from-distance` «Захист від пройденої відстані» · entities/state · 🌱 · слот {per_tile: n}.
  - `+sync-attack` «Союзники з лінією огляду атакують разом» · entities/combat · 🥉.
  - `+adrenaline-resource` «Ресурс спецдій від руху й атак» · game-logic/economy · 📎.
  - `+move-then-act` «Спершу рух, після дії рух заборонено» · game-logic/turns · 🌱.
  - `+same-height-attack` «Атака лише на своїй висоті» · entities/combat · 🌱.
  - `+cover-explodes` «Зруйноване укриття вибухає» · entities/interact · 🌱.
  - `+vehicle-eject` «Техніка з пальним; вихід до знищення» · entities/state · 📎.
  - `+support-strike-call` «Виклик авіаудару/артилерії» · entities/spawn · 📎.
  - `+revive-tokens` «Ревайви з обмеженого запасу на забіг» · game-logic/lose · 🌱.
  - `+bonus-action-on-kill` «Додаткова дія за вбивство» · game-logic/turns · 🌱.
  - `+escape-target` «Знищити ціль до втечі за край» · game-logic/win · 🌱.
  - `+collapsing-floor` «Підлога зникає — рухайся» · entities/legality · 📎.
  - `+node-map-run` «Мапа забігу з вузлами-місіями» · levels/progression · 🥉.
  - `+decoy-summon` / `+delayed-damage-mine` / `+weapon-mods` / `+secondary-ammo` — вміння й лоадаут.
  - `+cover-system` / `+fuel-ammo` / `+turn-limit-survive` / `+bonus-objectives` / `+run-meta-carry` — уже пропоновані корпусом.

## Пропозиції до словників
- `+trigger:moved` — сутність завершила рух (нарахування Dodge/адреналіну).
- `+trigger:ally_attacked` — союзник атакував ціль (запуск sync).
- `+cond:same_height` — дві сутності на одній висоті.
- `+cond:cover` — сутність в укритті / поруч з укриттям.
- `+effect:sync_attack` — безкоштовна атака союзника основною зброєю по тій самій цілі.
- `+effect:eject` — вийти з техніки на сусідню клітину; `+effect:revive` — повернути вибитого героя за ресурс.
- `+ui:dodge-meter` · `+ui:adrenaline-bar` · `+ui:fuel-gauge` · `+ui:sync-line` (хто долучиться до атаки).
- `+window:outpost-hub` — база між забігами; `+window:run-map` — вузли регіону; `+window:level-up-choice` — вибір нагороди за рівень.
- `+feature:run-reset` — поразка скидає кампанію, мета-прогрес лишається.

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Metal_Slug_Tactics) — 2 дії (рух + дія), захист від руху, sync з лінією огляду, адреналін, укриття ворогів, небезпеки, танк з пальним, ревайв за очки підкріплення, поразка → база, регіони з босами.
- [Xbox Wire: Five things](https://news.xbox.com/en-us/2024/11/06/five-things-before-you-dive-into-metal-slug-tactics/) — Dodge і Cover Points, укриття вибухає, sync усіх із лінією огляду, 9 героїв і їхні ролі, пасиви Team Leader/Impressive/Determination/Efficiency, моди.
- [RPGFan: impressions](https://www.rpgfan.com/2024/06/10/metal-slug-tactics-impressions/) — рух до дії, атаки лише на одній висоті, sync без ліміту, танк, типи місій, One-Up, вузли, бос-лінкор.
- [Steam](https://store.steampowered.com/app/1590760/Metal_Slug_Tactics/) — числа контенту, підкріплення, роглайт.

## Непевне
- (?) Умова sync: «лінія огляду» (Wikipedia, Xbox Wire) чи «у дальності основної зброї» (RPGFan); чи одна sync-атака на ворога за хід — лише сніпет гайда Prima, сторінка не відкрилась.
- (?) Формула шкоди з Dodge і Cover Points; чи Dodge сам може повністю скасувати шкоду (Xbox Wire — так, огляд — ні без укриття).
- (?) Чи укриття діє з усіх боків (джерела розходяться).
- (?) Що стається з героєм, якщо танк знищено разом з ним.
- (?) Поведінка мечників і склад ворогів — лише з одного огляду демо.
- (?) Рівні складності й превʼю sync-ліній — не перевіряв.
