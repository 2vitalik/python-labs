---
title: Tales of Maj'Eyal
slug: tales-of-maj-eyal
aka: [ToME, ToME4, T-Engine 4]
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2012
platforms: [Windows, macOS, Linux]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tales_of_Maj%27Eyal", best: true, note: "суть, GUI з мишею, permadeath з додатковими життями, онлайн-профіль і анлоки, T-Engine (C + Lua), доповнення"}
  - {kind: official, url: "https://te4.org/wiki/Main_Page", note: "офіційна вікі: таланти, ресурси, складність, permadeath, зони"}
  - {kind: other, url: "https://te4.org/wiki/Talent", note: "вікі: active / sustained / passive, кулдаун, резерв ресурсу сустейнами, очки талантів, мастерність, категорії"}
  - {kind: other, url: "https://te4.org/wiki/Resource", note: "вікі: 14 ресурсів (Stamina, Mana, Equilibrium, Paradox, Hate, Vim…) і їхні незвичні правила"}
  - {kind: other, url: "https://te4.org/wiki/Permadeath", note: "вікі: режими Exploration / Adventure / Roguelike, 7 життів на рівнях 1, 2, 5, 7, 14, 24, 35"}
  - {kind: other, url: "https://te4.org/wiki/Difficulty", note: "вікі: Easier…Madness, кулдаун сходів після вбивства, % рідкісних ворогів"}
  - {kind: other, url: "https://te4.org/wiki/Zones", note: "вікі: карта світу, зони з рівнями, скейлінг до рівня героя в межах floor/ceiling, тіри, Infinite Dungeon"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Tales+of+Maj%27Eyal", note: "пошук"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tales+of+Maj%27Eyal+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-by-input, move-8dir, cell-click, gui-render, dungeon-generation, stairs-levels, hp-damage, inventory, inventory-items, item-pickup, status-effects, unit-xp-skills, melee-vs-ranged, projectile-shot, explode-area, line-of-sight-attack, fog-of-war, message-log, status-panel, keyboard-controls, difficulty-levels, difficulty-select, character-select, achievements-window, profile-stats, leaderboard, permadeath, player-death, extra-life-threshold, world-map, map-window, rule-variants, +talent-cooldown, +sustained-talent, +resource-per-class, +talent-points, +zone-level-scaling, +overworld-travel, +stairs-lock-after-kill, +unlockables, +mod-support]
proposes: ["+trigger:cooldown_ready(talent)", "+trigger:sustain_on(talent)", "+effect:cooldown(talent, n)", "+effect:reserve(resource, n)", "+effect:fizzle", "+effect:anomaly", "+cond:cooldown(talent, op, n)", "+cond:resource(name, op, n)", "+cond:extra_lives(op, n)", "+window:talents-window", "+window:levelup-window", "+window:eidolon-plane", "+ui:hotbar", "+ui:resource-bars", "+feature:lives-mode", "+feature:online-profile", "+feature:class-unlocks", "+card:talent-cooldown", "+card:sustained-talent", "+card:zone-level-scaling"]
author: opus
date: 2026-11-09
---

# Tales of Maj'Eyal — тактичний роглайк, де бій — це панель талантів з кулдаунами й сустейнами, а в кожного класу свій ресурс зі своєю фізикою

## Суть
Від [angband](angband.md) і [dungeon-crawl-stone-soup](dungeon-crawl-stone-soup.md) ToME відрізняє **бойова система талантів**: майже кожна дія — талант на гарячій панелі з **кулдауном** (перезарядка в ходах) і, можливо, ціною в ресурсі. Таланти бувають активні, пасивні й **сустейни** — увімкнені постійно, вони резервують частину пулу ресурсу. Ресурс у кожного класу свій і поводиться по-своєму: Stamina й Mana відновлюються, Equilibrium росте з використанням і дає шанс зірвати каст, Paradox після порогів викликає аномалії, Hate набирається вбивствами. Світ — карта з зонами, які скейляться під рівень героя; смерть за замовчуванням не остаточна — є запас життів.

## Поле і час
- Квадратна сітка; **карта світу** (континенти Maj'Eyal, Var'Eyal) з входами в **зони**; зона = один або кілька рівнів, зʼєднаних сходами; частина зон — міста з крамницями.
- Рівень зони при вході скейлиться під рівень героя в межах floor/ceiling зони; кожен поверх глибше +1 рівень ворогам. Тіри: Tier 1 — рівні 1–7, Tier 2 — 7–16.
- Предмети на землі зазвичай **зникають**, коли покидаєш рівень (крім сховищ і складу фортеці Sher'Tul).
- Зони: фіксовані (міста, іменовані підземелля), випадкові в дикій місцевості, події від NPC/предмета, вбудовані з шансом +5…15 %; альтернативні плани Tier-1 зон; Infinite Dungeon (1 → ∞), Arena (1–50).
- Покроково, тактичний бій; швидкість впливає на частоту ходів (?); видимість — світло й поле зору (окрема сторінка Vision).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | раса (9 на старті), клас (25 на старті), стати, Life, 1–2 ресурси класу, таланти, інскрипції, життя | рух/атака; дії — таланти з панелі |
| Звичайний ворог | enemy | рівень (скейл зони), ранг 1 | таланти теж з кулдаунами (?) |
| Рідкісний ворог (rare) | enemy | — | посилений; 4 % на Normal, 12,5 % на Nightmare |
| Випадковий бос | boss | — | зʼявляється з Insane: 5 % придатних ворогів |
| Унікальний бос | boss | ранг 4, бонусні класи | фіксований у зоні; на високій складності росте швидше |
| Талант active | supply | кулдаун, ціна ресурсу, 1 хід або миттєво | дія, після якої чекає перезарядку |
| Талант sustained | supply | резерв ресурсу | діє, доки не вимкнеш; ворог іноді може зняти |
| Талант passive | supply | — | діє завжди, ворог не зніме |
| Інскрипції (infusion, rune) | pickup | слоти | миттєві «таланти» з предмета; слот = ціна категорійного очка |
| Сходи | static | блок N ходів після вбивства | перехід між рівнями зони |
| Вхід у зону на карті світу | static | діапазон рівнів | вхід → зона |
| Місто | zone | крамниці | торгівля, NPC, квести |
| Вода / пісок / стіна | terrain | — | забирають Air; без повітря — шкода від 20 % Life +5 %/хід |
| Eidolon Plane | zone | — | куди йде герой після смерті, якщо є життя |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(talent)` → ЯКЩО `custom: «кулдаун = 0»` and `custom: «ресурсу вистачає»` → ТО `custom: «ефект таланту»`, `custom: «ціна ресурсу»`, `custom: «кулдаун = N»`; інакше `block`.
- КОЛИ `turn_end(hero)` → ТО `custom: «кулдауни всіх талантів −1»`.
- КОЛИ `input(toggle sustain)` → ЯКЩО `custom: «вимкнено»` → ТО `custom: «увімкнути; резерв: макс. Mana/Stamina −X»` (Blur Sight: 200 → 170).
- КОЛИ `custom: «сустейн Equilibrium / Paradox»` → ТО `custom: «ресурс не опускається нижче X»` (Icy Skin: Equilibrium ≥ 30).
- КОЛИ `custom: «ворог знімає ефект»` → ЯКЩО `custom: «сустейн»` → ТО `custom: «вимкнено»`; ЯКЩО `custom: «пасив»` → ТО `block`.
- КОЛИ `input(nature talent)` → ТО `counter(equilibrium, +cost)`; ЯКЩО `custom: «Equilibrium > Willpower»` and `prob(sqrt(Eq − Wil) / 60)` → ТО `custom: «зрив (fizzle)»`.
- КОЛИ `input(chronomancy talent)` → ТО `counter(paradox, +cost)`; ЯКЩО `custom: «mP > 300»` and `prob((mP/300)³)` → ТО `custom: «випадкова аномалія, Paradox −2×ціна»`; ЯКЩО `custom: «mP > 200»` and `prob((mP/200)²)` → ТО `custom: «провал, хід втрачено»`; ЯКЩО `custom: «mP > 400»` and `prob((mP/400)⁴)` → ТО `custom: «талант бʼє по кастеру»`.
- КОЛИ `died(enemy)` → ЯКЩО `custom: «клас на Hate»` → ТО `counter(hate, +8)` (бос — +24); ЯКЩО `custom: «клас на Vim»` → ТО `counter(vim, +50 % (Wil+1) × ранг)`.
- КОЛИ `input(vim talent)` → ЯКЩО `custom: «Vim не вистачає»` → ТО `hp(hero, −2×ціна)`.
- КОЛИ `tick` → ТО `custom: «регенерація Life; Stamina +0,3; Mana лише в магів»`; КОЛИ `input(rest)` → ТО `custom: «швидша регенерація»`.
- КОЛИ `enter(hero, water)` → ТО `counter(air, −n)`; ЯКЩО `counter(air, =, 0)` → ТО `damage(20 % Life, +5 %/хід)`.
- КОЛИ `custom: «рівень героя +1»` → ТО `custom: «+3 очки статів, +1 класове, +1 загальне (на 5, 10, 15… — 2 класові, 0 загальних)»`; макс. рівень таланту 5.
- КОЛИ `custom: «рівень героя ∈ {10, 20, 34}»` → ТО `custom: «+1 категорійне очко: відкрити категорію або мастерність +0,2»`, `custom: «−1 слот інскрипції»`.
- КОЛИ `custom: «вхід у зону / поверх»` → ТО `custom: «рівень = clamp(рівень героя, floor, ceiling) + глибина − 1»`.
- КОЛИ `leave(hero, level)` → ТО `custom: «предмети на землі зникають»` (крім сховищ).
- КОЛИ `died(enemy)` → ТО `custom: «сходи заблоковано на 2 / 3 / 5 / 9 ходів (Normal / Nightmare / Insane / Madness)»`; на Easier — одразу.
- КОЛИ `hp_zero(hero)` → ЯКЩО `mode(Exploration)` → ТО `teleport(hero, Eidolon Plane)`; ЯКЩО `mode(Adventure)` and `custom: «є життя»` → ТО `lives(−1)`, `teleport(hero, Eidolon Plane)`, `custom: «вороги на місці смерті вилікувані»`; ЯКЩО `mode(Roguelike)` → ТО `lose`.
- КОЛИ `custom: «рівень героя ∈ {1, 2, 5, 7, 14, 24, 35}»` → ЯКЩО `mode(Adventure)` → ТО `lives(+1)` (до 7).
- КОЛИ `custom: «3 боси Tier-1 вбито»` → ТО `custom: «вхід у Tier-1 зону пропонує одразу останній поверх»`.
- КОЛИ `custom: «досягнення в онлайн-профілі»` → ТО `unlock(race | class)`; КОЛИ `custom: «перемога на Nightmare»` → ТО `unlock(Insane)`; Insane → `unlock(Madness)`.
- Перемога: пройти сюжетну кампанію (?). Поразка: смерть без життів. Рахунок: онлайн-профіль, досягнення, рекорди.

## Керування і ввід
- Гібрид: класичні клавіатурні команди + миша; можна грати майже лише мишею (клік по клітині — рух / атака, клік по іконці таланту).
- Гаряча панель талантів (`hotbar`) з клавішами; ціль таланту — курсором (?).
- Відпочинок `r`; автодослідження (?).

## Вікна, меню, HUD
- `game-screen`: мапа з тайлами, `hotbar` талантів з кулдаунами на іконках (`skill-bar`), `resource-bars` (Life + ресурси класу), `message-log`, мінікарта (?), ефекти-іконки.
- `character-create`: раса → підраса → клас → складність → режим життів (`lives-mode`) (?); частина варіантів закрита до анлоку.
- `levelup-window` / `talents-window`: дерева категорій, вкладання очок, мастерність.
- `character-sheet` (power, damage, saves, armor), `inventory-window` з лялькою, `map-window` (карта світу), крамниці (`shop-window`).
- `eidolon-plane` — екран-зона після смерті з вибором (?).
- `achievements-window`, онлайн-профіль (`profile-stats`), чат у грі; `end-screen`.

## Фічі поза полем
- `difficulty-presets`: Easier / Normal / Nightmare / Insane / Madness (дві останні — анлок перемогою на попередній); Madness: +500 золота, +100 Life, вороги ×3 Life (+200 %), поблизу вороги випадково дізнаються, де герой.
- `lives-mode`: Exploration (нескінченно, донат), Adventure (за замовчуванням, до 7), Roguelike (одна).
- `online-profile`: персонажі, досягнення, статистика сервера, чат; анлоки рас і класів через досягнення / донат / покупку.
- `mod-support`: T-Engine 4 (C), модулі на Lua; аддони міняють графіку, інтерфейс, баланс і контент; рушій GPLv3.
- Доповнення: Ashes of Urh'Rok (2014), Embers of Rage (2016), Forbidden Cults (2018) — нові класи й ресурси (Steam, Insanity).

## Варіації й родичі
- Історично — гілка ZAngband → ToME (Tolkien) → власний світ; родич [angband](angband.md).
- Кулдауни замість витратних заклять — рух у бік [rift-wizard](rift-wizard.md) (заряди), [path-of-achra](path-of-achra.md), [cogmind](cogmind.md) (?).
- Протилежність щодо смерті: життя Adventure ↔ чистий permadeath [nethack](nethack.md), [rogue](rogue.md).
- Осі варіацій: **ціна дії** (мана-пул / заряди / кулдаун / кулдаун + ресурс) · **ресурс** (один спільний / свій у класу з власною фізикою) · **смерть** (permadeath / ліміт життів / нескінченно) · **скейл світу** (глибина / рівень героя в межах зони).

## Цікавинки для курсу
- Таланти з кулдауном: одна модель «дія — ціна — перезарядка» для всіх класів — 📎.
- Сустейни, що резервують частину пулу (або ставлять нижню межу для Equilibrium/Paradox) — 📎.
- Paradox: три пороги з шансами `(mP/200)²`, `(mP/300)³`, `(mP/400)⁴` → провал / аномалія / відбій — 🥉.
- Ресурси з різною фізикою (регенерація / росте від дій / від вбивств / платиш Life) як інтерфейс з кількома реалізаціями — 🥉.
- Скейлінг зони під героя з floor/ceiling і +1 на поверх — 🌱.
- Блок сходів N ходів після вбивства як параметр складності — 🌱.
- Ліміт життів, що поповнюється на заданих рівнях героя — 🌱.

## Мапа на каталог
- Є: `cell-click` · `gui-render` · `move-8dir` · `stairs-levels` · `dungeon-generation` · `hp-damage` · `status-effects` · `unit-xp-skills` (очки талантів) · `melee-vs-ranged` · `projectile-shot` · `explode-area` · `difficulty-levels` + `difficulty-select` · `character-select` · `achievements-window` · `profile-stats` · `permadeath` (режим Roguelike) · `extra-life-threshold` (життя на порогах рівня героя, не очок) · `world-map` + `map-window`.
- **Нема** → пропозиції карток:
  - `+talent-cooldown` «Дія з перезарядкою в ходах (узагальнення `shoot-cooldown` на будь-яку дію)» · entities/combat · 📎 · слоти {cooldown, cost}.
  - `+sustained-talent` «Увімкнений ефект резервує частину пулу ресурсу» · entities/state · 📎.
  - `+resource-per-class` «Свій ресурс у класу з власними правилами росту й штрафів» · entities/state · 🥉.
  - `+talent-points` «Очки статів / класові / загальні / категорійні на рівнях» · entities/state · 📎.
  - `+zone-level-scaling` «Рівень зони = рівень героя в межах floor/ceiling + глибина» · levels/generation · 🌱.
  - `+stairs-lock-after-kill` «Сходи блоковано N ходів після вбивства» · game-logic/difficulty · 🌱.
  - `+unlockables` «Раси/класи/складності відкриваються досягненнями» · levels/progression · 🌱.
  - `+mod-support` «Модулі й аддони на скриптовій мові» · interface/settings · 🥇. Перевикористано: `+overworld-travel`.

## Пропозиції до словників
- `+trigger:cooldown_ready(talent)` — талант перезарядився; `+trigger:sustain_on(talent)`.
- `+effect:cooldown(talent, n)` — поставити перезарядку; `+effect:reserve(resource, n)` — зарезервувати частину пулу; `+effect:fizzle` — дія зірвалась, хід втрачено; `+effect:anomaly` — випадковий ефект з таблиці аномалій.
- `+cond:cooldown(talent, op, n)`; `+cond:resource(name, op, n)` — значення іменованого ресурсу (ширше за `counter`, бо з max і резервом); `+cond:extra_lives(op, n)`.
- `+window:talents-window`, `+window:levelup-window`, `+window:eidolon-plane`.
- `+ui:hotbar` — панель дій з клавішами й кулдаунами; `+ui:resource-bars`.
- `+feature:lives-mode`, `+feature:online-profile`, `+feature:class-unlocks`.
- `+card:talent-cooldown`, `+card:sustained-talent`, `+card:zone-level-scaling`.

## Джерела
- ⭐ [Wikipedia: Tales of Maj'Eyal](https://en.wikipedia.org/wiki/Tales_of_Maj%27Eyal) — тактичний бій, GUI з мишею, permadeath з життями, 9 рас × 25 класів, онлайн-профіль, T-Engine 4, доповнення.
- [te4 wiki: Talent](https://te4.org/wiki/Talent) — active / sustained / passive, кулдаун, резерв, очки на рівнях, мастерність, категорійні очки 10/20/34, інскрипції.
- [te4 wiki: Resource](https://te4.org/wiki/Resource) — Air, Equilibrium, Feedback, Hate, Insanity, Life, Mana, Paradox, Psi, Souls, Stamina, Steam, Vim з формулами.
- [te4 wiki: Permadeath](https://te4.org/wiki/Permadeath) — три режими, рівні отримання життів, Eidolon Plane.
- [te4 wiki: Difficulty](https://te4.org/wiki/Difficulty) — п'ять складностей, блок сходів, % рідкісних і босів, анлок Insane/Madness.
- [te4 wiki: Zones](https://te4.org/wiki/Zones) — карта світу, зони, скейлінг, тіри, зникнення предметів, Infinite Dungeon, Arena.
- [te4 wiki: Main Page](https://te4.org/wiki/Main_Page) — навігація по механіках.

## Непевне
- (?) Чи вороги теж мають кулдауни й наскільки симетрична система — не перевірено.
- (?) Автодослідження, ціль таланту курсором, мінікарта — з памʼяті.
- (?) Порядок вибору в створенні героя й екран Eidolon Plane — не перевірено.
- (?) Рік: Wikipedia — реліз 2012 (розробка з 2009), WP-список — 2011; queue — 2011.
- (?) Умова перемоги сюжетної кампанії — не читав.
- (?) Порівняння з rift-wizard / path-of-achra / cogmind щодо кулдаунів — з памʼяті.
