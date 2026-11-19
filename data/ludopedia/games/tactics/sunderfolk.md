---
title: Sunderfolk
slug: sunderfolk
aka: []
family: tactics
also: []
klass: figure
axes:
  field: hex
  time: turn
  opponent: coop
  info: partial
  random: runtime
  goal: state
year: 2025
platforms: [PC (Steam), Switch, PS5, Xbox Series X/S, телефон / планшет як контролер]
links:
  - {kind: other, url: "https://dreamhaven.com/sunderfolk/beginners-guide", best: true, note: "офіційний гайд: раунд (герої → монстри → союзники), герої без порядку ходу, гекс-сусідство, 1 рух = 1 гекс, штовхнути ворога чи помінятися з союзником — теж 1 рух, лава й слиз, трінкети, страви, зброя з Energize, будівлі Ардена, Mission Guide у телефоні"}
  - {kind: steam, url: "https://store.steampowered.com/app/2414270/Sunderfolk/", note: "трейлер, опис: застосунок-контролер (рука карт, довідник), QR-приєднання, обраний порядок ходів, Арден, кооп до 4, безкоштовна проба на 4 місії"}
  - {kind: official, url: "https://dreamhaven.com/games/sunderfolk", note: "сторінка гри: шість героїв і їхні ролі, оновлення 2.0"}
  - {kind: other, url: "https://dreamhaven.com/sunderfolk/meet-your-heroes-the-arcanist", note: "Fate Card тягнеться на кожну атаку; ультимейт з 6 рівня, кулдаун, один на раунд; Mana, телепорт, обмін, приманки"}
  - {kind: other, url: "https://dreamhaven.com/sunderfolk/meet-your-heroes-berserker", note: "Protector's Fury після удару, Provoke, Fling, Long Haul, ультимейт Roar"}
  - {kind: other, url: "https://dreamhaven.com/sunderfolk/meet-your-heroes-the-pyromancer", note: "Firepower +2 за стек до 3, вогонь на гексах, Cauterize: поглинути вогонь і лікуватись"}
  - {kind: other, url: "https://dreamhaven.com/sunderfolk/meet-your-heroes-the-rogue", note: "Shroud: ухил від першої шкоди, лише не поруч з ворогами; страта при HP < 8; золото, приманки"}
  - {kind: other, url: "https://dreamhaven.com/sunderfolk/meet-your-heroes-the-ranger", note: "Precision і Expose (+1 отриманої шкоди), лози з Root, стрибки"}
  - {kind: other, url: "https://dreamhaven.com/sunderfolk/meet-your-heroes-bard", note: "Two-Step, музичні ноти на мапі, які топчуть вороги, переставлення союзників і ворогів"}
  - {kind: other, url: "https://dreamhaven.com/sunderfolk/sunderfolk-update-5---2-0-patch-notes-summary", note: "2.0: визначення Knockback у гексах, герой Vanguard, миша й клавіатура, онлайн для ПК, режими Single / Online / Couch Co-op"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Sunderfolk", note: "огляд: Secret Door / Dreamhaven, 23.04.2025, платформи, телефон як контролер"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Sunderfolk+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [hp-damage, push-object, pull-object, swap-on-contact, teleport, status-effects, melee-vs-ranged, explode-area, drop-on-death, inventory-items, shop-between-levels, shop-window, unit-xp-skills, difficulty-levels, online-multiplayer, lobby-window, character-select, game-screen, main-menu, end-screen, settings-window, +phone-controller, +free-hero-order, +move-budget-actions, +terrain-absorb-heal, +one-ultimate-per-round, +execute-threshold, +attack-modifier-deck, +character-classes, +local-coop, +shared-screen-coop, +knockback, +push-chain, +summon-creature, +mana-pool-spells, +taunt-targeting, +retaliation, +cooldown-ability, +town-hub, +town-builder]
proposes: ["+trigger:attacked", "+effect:knockback", "+effect:draw_card", "+effect:buff", "+effect:root", "+effect:taunt", "+effect:shield", "+cond:hp_below", "+ui:hand-cards", "+ui:modifier-reveal", "+window:town-screen", "+window:qr-join", "+feature:companion-app", "+axis:turn-structure", "+card:phone-controller", "+card:free-hero-order", "+card:one-ultimate-per-round"]
author: opus
date: 2026-11-19
---

# Sunderfolk — кооп-тактика на гексах, де рука карт — у твоєму телефоні, а герої ходять у будь-якому порядку

## Суть
Покрокова кооперативна тактика до чотирьох гравців на одному спільному екрані (ТВ), а телефон кожного — контролер, приватна рука Skill Cards і довідник. Хід героя — одна Skill Card: рух по гексах плюс дія (удар, телепорт, штовхання, створення вогню чи лоз); кожна атака тягне **Fate Card** з колоди модифікаторів героя. Порядку ходу героїв нема: хто першим обрав карту, той і ходить, потім — фаза монстрів і союзників. Між місіями — містечко Арден, яке партія відбудовує заради крамниць, крафту, страв і нових умінь.

## Поле і час
- Поле — гекси; сусіди — гекси зі спільною стороною; один гекс руху = 1 очко руху, штовхнути ворога чи помінятися з союзником — теж 1.
- Раунд: фаза героїв (у будь-якому порядку, по одному) → фаза монстрів → фаза NPC-союзників (якщо є).
- Небезпеки на гексах: лава, слиз; частину створюють самі герої (вогонь Pyromancer, лози Ranger, музичні ноти Bard).
- Інформація часткова: Mission Guide у телефоні показує вміння й Skill Cards ворогів і небезпеки мапи; випадкова лише Fate Card, яку тягнуть на атаку.
- Кампанія: місії в Сандерлендах, між ними — Арден; режим One Shot (1.5) і сценарії (2.0) — окремі місії без міста.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Arcanist | piece | Mana | маг: телепорт, обмін місцями, приманки; найсильніші заклинання коштують багато Mana |
| Bard | piece | пасивка Two-Step | лишає музичні ноти-баффи на гексах; переставляє союзників і ворогів |
| Berserker | piece | Rage, Protector's Fury | танк: після удару по ньому — менше шкоди й сильніші удари; Provoke, Fling, Long Haul |
| Pyromancer | piece | Firepower 0–3 (+2 до атаки за стек) | палить гекси вогнем, стрибає, бʼє площею; поглинає вогонь заради лікування |
| Ranger | piece | Precision | лук: з потрібної дистанції — більша шкода й Expose; лози-пастки |
| Rogue | piece | Shroud | одиночна шкода, страта, телепорт, крадіжка баффів, створює золото |
| Vanguard (з 2.0) | piece | Grit | танк: менше шкоди й відповідь атакуючому, кожен удар −1 Grit; Knockback |
| Монстр / еліта | enemy | HP, власні Skill Cards | діє у фазі монстрів за своєю картою |
| Бос (Warrior Twins, Arena Champion; Wurm (?)) | boss | власний набір дій | бої кампанії й арена One Shot (Arena Rumble) |
| NPC-союзник (Oozling) | ally | на Brightstone безсмертний | діє у фазі союзників |
| Приманка (Decoy) | ally | — | Arcanist / Rogue створюють; відволікає ворогів, приманка Rogue ще й бʼє |
| Лава | hazard | — | шкода тому, хто в ній (Protector's Fury її зменшує) |
| Слиз | hazard | — | небезпека мапи (?) |
| Вогонь на гексі | hazard | — | створює Pyromancer; поглинання лікує його |
| Лоза | hazard | — | ворогу — Root; союзнику (Nock Back) — додатковий рух |
| Музична нота | pickup | — | бафф союзнику; ворог, що наступив, її знищує |
| Святилище лікування | pickup | — | лікує героя, який його взяв |
| Золото | pickup | — | з ворогів і вмінь (Pennypinch) |
| Skill Card | supply | рух + дія, у телефоні | хід героя = одна карта; нові — з рівнями |
| Fate Card | supply | позитивна / нейтральна / негативна, спецефекти | тягнеться з колоди героя на кожну атаку |
| Трінкет | supply | — | бойовий бонус; з луту, Market або крафту у Workshop |
| Страва | supply | меню змінюється після місії | бафф на місію (Sinclair's Tavern) |
| Зброя | supply | умова Energize | після Energize дає опцію (напр. додатковий рух) |
| Будівля Ардена | static | рівень відбудови | відкриває бонус: крамниця, крафт, страви, зброя |

## Правила (КОЛИ → ЯКЩО → ТО)
Раунд:
- КОЛИ `phase_start(heroes)` → ТО `custom: «герої ходять по одному в будь-якому порядку; першим іде той, хто першим обрав Skill Card»`.
- КОЛИ `phase_start(monsters)` → ТО `custom: «кожен монстр діє за своєю Skill Card»`.
- КОЛИ `phase_start(allies)` → ТО `custom: «діють NPC-союзники»`.

Хід героя:
- КОЛИ `input(play, skill_card)` → ТО `custom: «рух і дія в порядку, надрукованому на картці»` (частини можна пропустити (?)).
- КОЛИ `input(move, hex)` → ЯКЩО `free(hex)` → ТО `move(hero, hex)`, `counter(move, -1)`.
- КОЛИ `input(move, hex)` → ЯКЩО `occupied(hex, enemy)` → ТО `push(enemy)`, `counter(move, -1)`.
- КОЛИ `input(move, hex)` → ЯКЩО `occupied(hex, ally)` → ТО `swap(hero, ally)`, `counter(move, -1)`.
- КОЛИ `custom: «дія картки містить атаку»` → ТО `custom: «тягнеться Fate Card з колоди героя й змінює атаку»`, `damage(target, n)`.
- КОЛИ `custom: «Knockback N»` → ЯКЩО `free(path)` → ТО `move(target, N гексів від джерела)`.
- КОЛИ `custom: «Knockback N»` → ЯКЩО `occupied(path, character)` → ТО `push` або `swap` тих, хто на шляху, можлива `damage`; ціль однаково доходить до кінцевого гекса.
- КОЛИ `enter(character, lava)` → ТО `damage(character, n)`.
- КОЛИ `input(play, ultimate)` → ЯКЩО `custom: «кулдаун минув і в цьому раунді ультимейт ще ніхто не грав»` → ТО `custom: «ультимейт героя»` — доступний з 6 рівня.
- КОЛИ `turn_end(hero)` → ЯКЩО `adjacent_count(hero, ally, >=, 1)` → ТО `set_state(hero, shield)` — приклад страви з таверни.
- КОЛИ `custom: «умову зброї виконано (напр., завдано N шкоди)»` → ТО `unlock(weapon_option)` — Energize.
- КОЛИ `contact(hero, heal_shrine)` → ТО `heal(hero, n)`, `disappear_b`.

Герої:
- Berserker: КОЛИ `custom: «Берсерка вдарили»` → ТО `set_state(berserker, protector_fury)` — менше шкоди (і від лави та вогню), більше удар.
- Berserker: КОЛИ `input(play, provoke)` → ТО `custom: «ворог наступного ходу атакує Берсерка»`.
- Berserker: КОЛИ `input(play, fling)` → ТО `throw(target)` — ворога чи союзника.
- Berserker: КОЛИ `input(play, long_haul)` → ТО `pull(enemies)`.
- Pyromancer: КОЛИ `input(play, trailblaze)` → ТО `set_cell(3 hexes, fire)`, `move(pyromancer, fire_hex)`, `damage(in_range, n)`.
- Pyromancer: КОЛИ `input(play, cauterize)` → ТО `set_cell(fire_hexes, empty)`, `heal(pyromancer, 2 × fire)`; пасивка Firepower: `custom: «+2 до кожної атаки за стек, до 3 стеків»`.
- Rogue: КОЛИ `custom: «Rogue відійшов від ворогів»` → ЯКЩО `adjacent_count(rogue, enemy, ==, 0)` → ТО `set_state(rogue, shroud)`.
- Rogue: КОЛИ `custom: «шкода по Rogue»` → ЯКЩО `state(rogue, shroud)` → ТО `block`, `clear_state(rogue, shroud)`.
- Rogue: КОЛИ `custom: «удар Rogue»` → ЯКЩО `custom: «HP цілі після удару < 8»` → ТО `disappear_b` (страта; Thousand Cuts тоді повторюється).
- Ranger: КОЛИ `custom: «атака з дистанції ≥ вимоги Precision»` → ТО `damage(target, n + bonus)`, `set_state(target, expose)` (?) — Expose: +1 до будь-якої отриманої шкоди, і від середовища.
- Ranger: КОЛИ `input(play, snaring_vines)` → ТО `spawn_at(vine, 3 гекси в радіусі 3)`.
- Ranger: КОЛИ `enter(enemy, vine)` → ТО `set_state(enemy, root)`.
- Arcanist: КОЛИ `input(play, stargate)` → ТО `teleport(arcanist, hex)`, `swap(character, character)`.
- Arcanist: КОЛИ `input(play, gravity_nexus)` → ТО `pull(enemies в радіусі 3)`, `damage(area, n)`, `teleport(arcanist, hex)`.
- Arcanist: КОЛИ `input(play, mana_spring)` → ТО `counter(mana, +n × сусіди)` — рахуються й вороги.
- Bard: КОЛИ `input(play, sharp_refrain)` → ТО `damage(target, n)`, `spawn_at(music_note, поруч із ціллю)`.
- Bard: КОЛИ `enter(enemy, music_note)` → ТО `disappear_b`.
- Vanguard: КОЛИ `custom: «Vanguard вдарили»` → ЯКЩО `counter(grit, >, 0)` → ТО `custom: «менше шкоди й відповідь атакуючому»`, `counter(grit, -1)`.
- Arcanist: КОЛИ `input(play, starfall)` → ТО `set_state(targets, confused)`, `stun(center, 1)` — ультимейт; сплутаний ворог може вдарити своїх.

Монстри й кінець місії:
- КОЛИ `custom: «сплячого монстра атакували або герой підійшов на 2 гекси»` → ТО `clear_state(monster, asleep)` (?).
- КОЛИ `phase_start(monsters)` → ТО `custom: «монстр іде на найближчого героя, далі — на того, хто ходив раніше»` (?).
- КОЛИ `hp_zero(hero)` → ТО `custom: «герой пропускає раунд і повертається з половиною HP; витрачається життя партії»` (?).
- КОЛИ `counter(party_lives, ==, 0)` → ТО `lose` (?).
- КОЛИ `custom: «ціль місії виконано»` → ТО `win`, `custom: «нагорода й повернення в Арден»`.
- Перемога: ціль місії, далі — кампанія · Поразка: місію провалено (життя партії, на Challenging — ще й ліміт раундів (?)) · Рахунку нема.

## Керування і ввід
- Кожен гравець сканує QR-код зі спільного екрана застосунком Sunderfolk Controller (телефон або планшет); на ТВ — поле, у телефоні — Skill Cards, пасивки, предмети, Fate Cards і довідник по ворогах.
- Хід: обрати Skill Card у телефоні → провести героя гексами (клітини руху підсвічено) → обрати ціль дії; Fate Card тягнеться сама.
- Couch Co-op: гру купує лише хост, решта — телефони; Online (2.0, ПК): копія в кожного, лобі за invite-кодом; Single Player: один гравець веде до 4 героїв.
- ПК з 2.0: миша й клавіатура без застосунку — Skill Cards прямо на екрані.

## Вікна, меню, HUD
- `main-menu` (2.0): Single Player · Online Multiplayer · Couch Co-op.
- `custom-window` QR-приєднання: код на ТВ, гравці сканують телефонами.
- `lobby-window` (Online): invite-код, «Ready Up».
- `character-select`: герой на гравця (соло — до 4).
- `game-screen` (ТВ): гекси, герої, вороги, небезпеки, зона пробудження ворогів (?); емоції гравців (1.4).
- `custom-window` у телефоні: рука Skill Cards, Mission Guide (свої карти, пасивки, предмети, лишок Fate Cards; уміння й Skill Cards ворогів, небезпеки), інвентар.
- `custom-window` «Арден» (town-screen): будівлі, мешканці, відбудова; `shop-window` (Market), крафт і апгрейд трінкетів (Workshop), страви (Sinclair's Tavern), зброя (Smithy).
- `dialogue-window`: розмови з мешканцями й сюжет.
- `end-screen`: результат місії й нагорода.
- `settings-window`; перед One Shot — вибір складності й героїв, заміна спорядження (Skill Cards, Fate Cards, трінкети).
- Переходи: `main-menu` → QR / лобі → `character-select` → Арден → місія (`game-screen`) → `end-screen` → Арден → …

## Фічі поза полем
- Кампанія з місій у Сандерлендах; безкоштовна проба — перші 4 місії, прогрес переходить у повну гру.
- Прогресія: рівні героїв (нові Skill Cards; ультимейт з 6 рівня), Fate Cards для збірки героя, трінкети, страви, зброя з Energize; відбудова будівель Ардена.
- `mode-coop`: до 4 гравців; Remote Play Together; онлайн для ПК з 2.0; `mouse-and-keyboard` (ПК).
- One Shot (1.5): окремі місії поза кампанією, рівень героя не залежить від кампанії, без таверни — без страв; сценарії 2.0 (Arena Rumble, Sacred Sand) — серії повʼязаних місій.
- `difficulty-presets`: Brightstone (найлегша) і складніші рівні з обмеженими життями (?).
- `achievements`, `cloud-save`, 8 мов (озвучення — 6).

## Варіації й родичі
- [Gloomhaven](gloomhaven.md) — найближчий родич: гекси, кооп, карти з рухом і дією, колода модифікаторів атаки ≈ Fate Deck; різниця — вільний порядок героїв замість ініціативи й одна карта на хід.
- [D&D grid combat](dnd-grid-combat.md) — настільне натхнення («грати з друзями за столом»); [Into the Breach](into-the-breach.md) — позиціювання штовханням.
- Jackbox-подібні ігри — телефон як контролер на спільному екрані.
- Shadowstone (анонс 2026) — наступна гра студії (?).
- **Осі варіацій**: порядок героїв «ініціатива карт (Gloomhaven) / вільний у фазі (Sunderfolk) / суворий» · дія на хід «дві карти з виснаженням руки / одна Skill Card» · випадковість атаки «кубики / колода модифікаторів / нема (ITB)» · інтерфейс «спільний екран / приватна рука на телефоні».

## Цікавинки для курсу
- Телефон як приватна рука й довідник: сервер гри на ТВ + клієнти-телефони за QR — 🥇 (синхронізація стану, приватні дані на клієнті).
- Фаза героїв без порядку: «хто першим обрав карту — той ходить», решта чекає — 📎.
- Рух як бюджет гексів: крок, штовхнути ворога, помінятися з союзником — однаково 1 очко — 📎.
- Fate Deck: колода модифікаторів атаки, яку герой збирає між місіями — 🥉.
- Knockback по гексах з ланцюгом push / swap і шкодою по дорозі — 🥉.
- Вогонь на гексах: створити й поглинути заради лікування — 📎.
- Ультимейт з кулдауном і правилом «один на раунд на всю партію» — 🌱.
- Місто-хаб: відбудова будівель відкриває крамниці, крафт і страви — 🥉.

## Мапа на каталог
- Є: `hp-damage` · `push-object` ↔ штовхнути ворога рухом · `pull-object` ↔ Long Haul, Gravity Nexus · `swap-on-contact` ↔ рух у гекс союзника = обмін · `teleport` · `status-effects` ↔ Shield, Strength, Haste, Slow, Root, Expose, Stun, Confusion · `melee-vs-ranged` · `explode-area` ↔ площинні атаки · `drop-on-death` ↔ трінкети з ворогів · `inventory-items` · `shop-between-levels` + `shop-window` ↔ Market · `unit-xp-skills` ↔ рівні й нові карти · `difficulty-levels` · `online-multiplayer` + `lobby-window` · `character-select` · `game-screen` · `main-menu` · `end-screen` · `settings-window`.
- **Нема** → пропозиції карток:
  - `+phone-controller` «Телефон як контролер і приватна рука» · interface/input · 🥇.
  - `+free-hero-order` «Герої ходять у будь-якому порядку в межах фази» · game-logic/opponent · 📎.
  - `+move-budget-actions` «Штовхнути / помінятися коштує ті самі очки руху» · entities/move · 📎.
  - `+terrain-absorb-heal` «Поглинути клітини-стихію заради лікування» · entities/interact · 📎.
  - `+one-ultimate-per-round` «Одна ультимативна здібність на раунд на всю партію» · game-logic/opponent · 🌱.
  - `+execute-threshold` «Страта: ціль з HP нижче порогу після удару гине» · entities/combat · 🌱 · слот {threshold: 8}.
  - Повтори з корпусу: `+attack-modifier-deck` (Gloomhaven), `+character-classes`, `+local-coop`, `+shared-screen-coop`, `+knockback`, `+push-chain`, `+summon-creature` (приманки), `+mana-pool-spells`, `+taunt-targeting` (Provoke), `+retaliation` (Vanguard), `+cooldown-ability`, `+town-hub`, `+town-builder`.

## Пропозиції до словників
- `+trigger:attacked` — героя вдарили (Protector's Fury, Grit, втрата Shroud).
- `+effect:knockback` — відкинути на N гексів від джерела, штовхаючи чи міняючи тих, хто на шляху.
- `+effect:draw_card` — потягнути Fate Card на атаку.
- `+effect:buff` · `+effect:shield` · `+effect:root` · `+effect:taunt` — статуси Sunderfolk, частіші за загальний `set_state`.
- `+cond:hp_below` — HP цілі нижче порогу (страта Rogue, Fate Card «добити, якщо HP < 5»).
- `+ui:hand-cards` — рука Skill Cards у телефоні; `+ui:modifier-reveal` — показ витягнутої Fate Card.
- `+window:town-screen` — Арден з будівлями; `+window:qr-join` — приєднання телефоном за QR.
- `+feature:companion-app` — застосунок-контролер з приватною інформацією (Cryptid — застосунок-суддя).
- `+axis:turn-structure` — значення `free-order-phases`: фаза героїв у вільному порядку, потім фази монстрів і союзників.
- `+card:phone-controller` · `+card:free-hero-order` · `+card:one-ultimate-per-round`.

## Джерела
- ⭐ [Dreamhaven: Beginner's Guide](https://dreamhaven.com/sunderfolk/beginners-guide) — раунд із трьох фаз, герої без порядку, гекс-сусідство, ціна руху, штовхання й обмін, лава і слиз, трінкети, страви, зброя з Energize, будівлі, Mission Guide.
- [Steam: Sunderfolk](https://store.steampowered.com/app/2414270/Sunderfolk/) — застосунок-контролер, QR, обраний порядок ходів, Арден, кооп до 4, онлайн і couch co-op, безкоштовна проба (4 місії), мови.
- [Dreamhaven: Sunderfolk](https://dreamhaven.com/games/sunderfolk) — шість героїв і їхні ролі, оновлення.
- Сторінки героїв Dreamhaven: [Arcanist](https://dreamhaven.com/sunderfolk/meet-your-heroes-the-arcanist) · [Berserker](https://dreamhaven.com/sunderfolk/meet-your-heroes-berserker) · [Pyromancer](https://dreamhaven.com/sunderfolk/meet-your-heroes-the-pyromancer) · [Rogue](https://dreamhaven.com/sunderfolk/meet-your-heroes-the-rogue) · [Ranger](https://dreamhaven.com/sunderfolk/meet-your-heroes-the-ranger) · [Bard](https://dreamhaven.com/sunderfolk/meet-your-heroes-bard) — пасивки, карти, ультимейти з 6 рівня, Fate Cards на атаку.
- [Dreamhaven: 2.0 Patch Notes](https://dreamhaven.com/sunderfolk/sunderfolk-update-5---2-0-patch-notes-summary) — Knockback, Vanguard, миша й клавіатура, онлайн, режими меню.
- [Wikipedia: Sunderfolk](https://en.wikipedia.org/wiki/Sunderfolk) — студія, видавець, дата, платформи.
- Steam News (API) — One Shot (1.5), Vanguard і Grit, Knockback у гексах, Fate Card «Cleanse».
- [GameBrief: beginner guide](https://www.gamebrief.net/blog/sunderfolk-beginner-guide-best-party-2026) — сторонній гайд: розмір руки, склад Fate Deck, пробудження монстрів, падіння героя, рівні складності; дані з нього — у «Непевне».
- YouTube: пошук «Sunderfolk gameplay».

## Непевне
- (?) Лише GameBrief (сторонній гайд): рука 3 → 4 → 5 Skill Cards + ультимейт; свіжа Fate Deck — 10 карт (3 позитивні, 3 негативні, 4 нейтральні); монстри сплять, доки їх не вдарили чи не підійшли на 2 гекси; падіння героя — пропуск раунду й повернення з половиною HP за рахунок життів партії; складності Brightstone (без ліміту) / Balanced (3 життя) / Challenging (2 життя, ліміт раундів, Frenzy) / Shadowstone (1 життя, еліти).
- (?) Чи Skill Card після використання недоступна (кулдаун) чи рука багаторазова — офіційні джерела не кажуть.
- (?) Що робить слиз; скільки шкоди дає лава.
- (?) Порядок «хто першим обрав карту — той ходить» — зі сніпета статті підтримки Dreamhaven (сторінка віддала 403) і GameBrief.
- (?) Висота / прицільні бонуси за рельєф — у джерелах не знайдено.
- (?) Shadowstone — окрема гра чи режим; герої Witch / Assassin — з новин, не перевірено.
