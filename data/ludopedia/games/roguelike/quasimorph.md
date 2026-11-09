---
title: Quasimorph
slug: quasimorph
aka: []
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
year: 2023
platforms: [Windows]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2059170/Quasimorph/", best: true, note: "опис: контракти корпорацій, тримаєш лише винесене, смерть — втрата взятого, друк нового клона, аугментації, флагман; EA 2.10.2023, 1.0 — 31.07.2026"}
  - {kind: other, url: "https://ingamescientist.substack.com/p/fast-paced-turn-based-rogue-like", note: "огляд: «за кожен крок — хід ворогів», крок на одну клітину, рани окремих частин тіла, інфекція, голод"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=3194551184", note: "гайд «How to not get shafted instantly»: AP ходьби/бігу, режим крадькома, двері, стрільба крізь стіни, вибухові бочки"}
  - {kind: other, url: "https://turnbasedlovers.com/review/quasimorph-impressions-2/", note: "огляд: квазиморфи з помираючих людей за зростаючим лічильником, туман війни, флагман, мапа Сонячної системи, бартер"}
  - {kind: other, url: "https://www.noobfeed.com/reviews/quasimorph-review", note: "огляд: екстракція, класи й ранги клонів, механічні й квазиморфні аугментації, зношення спорядження"}
  - {kind: other, url: "https://playtested.pages.dev/article/2023-06-23-a-fusion-of-turn-based-roguelike-rpg-and-extraction-game-elements-demo-impressions-qua", note: "демо 2023: клік по клітинах, рани кожної частини тіла, процедурні рівні"}
  - {kind: other, url: "https://vaporlens.app/app/2347110/quasimorph_end_of_dream", note: "зведення відгуків про Quasimorph: End of Dream — режими руху й AP, лічильник мутації"}
  - {kind: steam, url: "https://steamcommunity.com/app/2059170/guides/", note: "гайди спільноти: класи, пакти, типи шкоди фракцій"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=quasimorph+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [cell-click, hp-damage, status-effects, hunger-clock, inventory, inventory-items, inventory-limit, item-pickup, drop-on-death, dungeon-generation, fog-of-war, projectile-shot, shoot-modes, explode-area, destructible-blocks, unit-xp-skills, character-select, shop-catalog, map-window, in-game-editor, +action-points, +movement-modes, +extraction-keep-loot, +lose-carried-on-death, +clone-reprint, +run-meta-carry, +limb-wounds, +amputation, +infection-timer, +bionic-implants, +weapon-durability, +ammo-limit, +escalation-counter, +corpse-spawns-enemy, +corpse-to-ally, +shoot-through-walls, +door-blocks-sight, +faction-reputation, +home-ship-upgrades]
proposes: ["+role:body-part", "+trigger:ap_zero", "+cond:ap(op, n)", "+effect:spend_ap", "+effect:extract", "+effect:reclone", "+effect:amputate(part)", "+window:ship-hub", "+window:contract-board", "+window:stock-market", "+ui:ap-counter", "+ui:paper-doll", "+feature:workshop", "+axis:session=extraction-run"]
author: opus
date: 2026-11-09
---

# Quasimorph — покроковий екстракшн-роглайк: клон-найманець виносить лут з місії або втрачає все, що взяв

## Суть
Гравець — бос космічної приватної військової компанії: бере контракти корпорацій, відправляє клона-найманця на планетарні бази, у таємні лабораторії й уламки кораблів. Місія — покрокова на клітинах, з туманом війни, патронами впритул і ранами окремих частин тіла. Ядро — **екстракція**: виконав контракт і повернувся — лишаєш усе винесене й посилюєш компанію; загинув — втрачаєш усе, що мав при собі, і друкуєш нового клона. Поверх тактики — **лічильник квазиморфозу**: чим довше місія, тим частіше з помираючих людей виростають демони.

## Поле і час
- Місія — процедурна карта з квадратних клітин, вид згори; рух — «по одній клітині», ціль руху/взаємодії/атаки — клік по клітині.
- Покроково: «за кожен ваш крок вороги роблять один хід»; поза боєм гра чекає. Хід поділено на очки дії (AP): ходьба дає 2 AP, біг — 3 AP; перезаряджання й ремонт теж коштують хід.
- Видимість: туман війни, невідомі зони ховаються, доки не увійдеш; двері блокують лінію зору; у режимі крадькома видно позиції ворогів крізь стіни.
- Мета-шар: постійна мапа Сонячної системи (корабель-флагман, корпорації, порти) — між місіями, без сітки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Найманець-клон | player | клас, ранг, навички класу, HP, частини тіла, голод, AP | рух клітинами в одному з режимів, стрільба, ближній бій, предмети |
| Частина тіла (органічна / роботизована) | body-part (+) | рана, перелом, інфекція, ампутація | перелом ноги — −HP за кожен крок і схильність до інфекції; поріз руки — −HP за кожну дію |
| Солдати корпорацій | enemy | тип шкоди / опори фракції | бʼють, щойно ваш хід закінчився; «уся карта знає, де ти», коли почалась стрілянина |
| Квазиморф (демон) | enemy | опори за видом | виростає з помираючих людей залежно від лічильника; із ростом впливу — частіше й сильніші |
| Союзні солдати місії | ally | — | бʼються поряд, предметів не беруть |
| Підконтрольний союзник | ally | — | можна передати й екіпірувати предмет, стоячи поруч |
| Двері | gate | міцність | відчинення коштує AP; зачинені блокують зір; пошкоджені — граната перелітає |
| Стіна | static | — | непрохідна; стріляти крізь стіни й двері можна |
| Бочка | hazard | — | вибухає: вогонь, переломи |
| Вогонь | hazard | — | підпалює найманця |
| Вихід / евакуація | zone | — | місце, куди треба донести лут, щоб зарахувати контракт |
| Зброя, броня, гаджети, гранати | pickup | калібр, режими вогню, міцність | зношуються; ремонт знижує максимум міцності |
| Патрони | pickup | калібр | обмежені, «рахуй патрони» |
| Аптечки, антибіотики, антивірус, ізолента, ремкомплект інженера | pickup | — | лікують рани й інфекцію; ізолента — органічні й роботизовані рани |
| Їжа | pickup | — | метаболізм клона прискорений, їжа скінченна |
| Аугментації та імпланти | pickup | механічні / квазиморфні | роботизовані кінцівки, «гігантська рука» з ампутованого ворога |
| Труп | object | — | дефібрилятор/реаніматрон робить із ворожого трупа союзника |
| Корабель-флагман | static | дерево апгрейдів, склад, рециклер | база між місіями |
| Корпорації | neutral | сила, репутація | дають контракти, торгують; місія проти корпорації знижує репутацію з нею |

## Правила (КОЛИ → ЯКЩО → ТО)
Хід і рух:
- КОЛИ `input(click, tile)` → ЯКЩО `free(tile)` and `counter(ap, >=, cost)` → ТО `move(merc, tile)`, `counter(ap, -cost)`.
- КОЛИ `input(mode, walk)` → ТО `custom: «2 AP на хід»`; `input(mode, run)` → `custom: «3 AP на хід, −20 % точності»`; `input(mode, sneak)` → `custom: «видно ворогів крізь стіни»`.
- КОЛИ `counter(ap, ==, 0)` → ТО `end_turn`; КОЛИ `turn_end(player)` → ТО `custom: «вороги рухаються й стріляють»`.
- КОЛИ `input(open, door)` → ТО `set_state(door, open)`, `counter(ap, -n)`; зачинені двері → `custom: «блокують лінію зору»` (порада — входити з ≥ 1 AP у запасі).
- КОЛИ `input(reload | repair)` → ТО `counter(ap, -n)`; ремонт → `custom: «міцність ↑, максимум міцності ↓»`.

Бій:
- КОЛИ `input(shoot, target)` → ЯКЩО `has(merc, ammo)` → ТО `damage(target, n)`, `counter(ammo, -n)`, `counter(durability, -n)`; режими вогню — у зброї; крізь стіни й двері — `custom: «теж можна»`.
- КОЛИ `input(throw, grenade, tile)` → ЯКЩО `custom: «двері на шляху пошкоджено достатньо»` → ТО `custom: «граната перелітає двері»`, `explode(area, n)`.
- КОЛИ `destroyed(barrel)` → ТО `explode(area, n)`, `set_state(nearby, burning)`.
- КОЛИ `died(human)` → ЯКЩО `mode(quasimorphosis)` and `custom: «лічильник квазиморфозу достатній»` → ТО `spawn_at(quasimorph, corpse)`.
- КОЛИ `turn_end(player)` → ЯКЩО `mode(quasimorphosis)` → ТО `counter(quasimorphosis, +1)` (вороги сильнішають і частіше мутують).
- КОЛИ `input(use, defibrillator, enemy_corpse)` → ТО `transform(enemy_corpse, ally)`.
- КОЛИ `input(give, item, ally)` → ЯКЩО `in_range(merc, ally, 1)` → ТО `give(ally, item)` (союзники місії — `block`).

Рани і потреби:
- КОЛИ `custom: «влучання по частині тіла»` → ТО `set_state(body_part, wound | fracture)`.
- КОЛИ `input(move)` → ЯКЩО `state(leg, fracture)` → ТО `hp(merc, -n)`; КОЛИ `input(action)` → ЯКЩО `state(arm, cut)` → ТО `hp(merc, -n)`.
- КОЛИ `state_on(merc, infected)` → ТО `custom: «обмежений час знайти антивірус, інакше смерть»`; КОЛИ `custom: «вилікувано всі рани»` → ТО `clear_state(merc, infected)`.
- КОЛИ `custom: «частину тіла відірвано»` → ЯКЩО `custom: «це голова, і вона не роботизована»` → ТО `lose`; роботизовані рани — ремкомплект інженера або ізолента.
- КОЛИ `custom: «ворогу ампутовано кінцівку»` → ЯКЩО `prob(p)` → ТО `give(merc, augment)`.
- КОЛИ `timer(n)` → ТО `counter(hunger, +1)`; `input(eat, food)` → `counter(hunger, -n)`.

Контракт і мета:
- КОЛИ `reach(merc, exit)` → ЯКЩО `custom: «ціль контракту виконано»` → ТО `win`, `custom: «усе винесене — на склад флагмана»`.
- КОЛИ `hp_zero(merc)` → ТО `lose`, `take(merc, all_carried)`, `custom: «можна надрукувати нового клона й повторити контракт»`.
- КОЛИ `input(reclone, merc)` → ТО `take(merc, inventory)`, `take(merc, augments)`, `custom: «ранги й навички класу лишаються, зміни геному застосовано»`.
- КОЛИ `counter(rank_xp, >=, n)` → ТО `custom: «новий ранг відкриває перк класу»`.
- КОЛИ `custom: «контракт проти корпорації»` → ТО `custom: «репутація з нею падає»`; низька → `custom: «закриває порти й торгівлю»`.
- КОЛИ `input(recycle, item)` → ТО `custom: «рециклер флагмана завжди дає всі ресурси предмета»`.
- Перемога: місії — виконати ціль і евакуюватись; кампанія — посилити компанію аж до контролю над корпорацією. Поразка місії: смерть клона, втрата всього взятого. Рахунок: нема; мірило — склад, репутація, апгрейди.

## Керування і ввід
- Клік по клітині — рух, взаємодія або атака; перемикач режиму руху (крадькома / ходьба / біг).
- Слоти жилета для метальних предметів — клавіші-цифри.
- `H` на екрані Magnum — біржа корпорацій.
- Між місіями — керування флагманом, торгівля, вибір контракту й клона.

## Вікна, меню, HUD
- `main-menu` → `+window:ship-hub` (флагман: склад, апгрейди, рециклер, друк клонів) → `+window:contract-board` / `map-window` (Сонячна система, корпорації) → `character-select` (клон і клас) → `game-screen`.
- `game-screen`: карта місії під туманом, `+ui:ap-counter`, режим руху, `inventory-bar` (слоти жилета з `item-hotkeys`), стан частин тіла (`+ui:paper-doll`), лічильник квазиморфозу.
- `inventory-window` — спорядження й лут з обмеженою місткістю.
- `shop-window` — бартер із корпораціями; `+window:stock-market` — біржа (`H`).
- `editor-window` — редактор рівнів; Steam Workshop.
- `end-screen` — підсумок місії: евакуація з лутом або смерть.
- Переходи: ship-hub → contract → game-screen → (евакуація) ship-hub зі здобиччю / (смерть) ship-hub без узятого.

## Фічі поза полем
- `+axis:session=extraction-run`: кожна місія — ставка спорядженням; прогрес компанії між місіями (`meta-progression`): флагман, ресурси, технології, репутація.
- Друк і передрук клонів: класи (десятки), ранги з перками; передрук знімає спорядження, аугментації й імпланти, але лишає ранги й навички.
- `level-editor` + `+feature:workshop` (Steam Workshop), `achievements`, `cloud-save`.
- Місії на час; захист власної проксі-компанії як окремий тип місії; режим квазиморфозу вмикається для частини місій.

## Варіації й родичі
- Quasimorph: End of Dream (окремий продукт у Steam, app 2347110) — відгуки описують ті самі режими руху й AP і лічильник мутації.
- Родичі в корпусі: [cogmind](cogmind.md) (тіло з частин, лут як ресурс виживання), [cataclysm-dark-days-ahead](cataclysm-dark-days-ahead.md) і [stoneshard](stoneshard.md) (рани частин тіла, інфекція, голод), [doomrl](doomrl.md) (покроковий шутер на клітинах), [infra-arcana](infra-arcana.md) (жах, зростання загрози).
- Осі варіацій: **ціна смерті** (остаточна / втрата лише взятого / нема) · **хід** (1 дія / AP за режимом) · **загроза в часі** (нема / таймер місії / лічильник, що спавнить демонів) · **лінія зору** (вільна / двері блокують / крізь стіни для шпигуна).

## Цікавинки для курсу
- Екстракція: інвентар місії відокремлено від складу; евакуація переносить, смерть обнуляє — 📎 (два інвентарі й одна транзакція).
- Режими руху з різним AP і штрафом точності (крадькома / ходьба 2 / біг 3, −20 %) — 🌱.
- Рана як податок на дію: перелом ноги — −HP за крок, поріз руки — −HP за дію — 🌱 (статус, що чіпляється до типу вводу).
- Лічильник квазиморфозу: росте щохід і перетворює смерть людини на спавн демона — 📎.
- Передрук клона: що лишається (ранг, навички) і що зникає (спорядження, імпланти) — 🌱 (поділ стану на постійний і ресурсний).
- Стрільба крізь стіни й двері + двері, що блокують зір — 🥉 (окремі правила проходу кулі й погляду).

## Мапа на каталог
- Є: `cell-click` · `hp-damage` · `status-effects` (інфекція, горіння) · `hunger-clock` · `inventory` + `inventory-items` + `inventory-limit` · `item-pickup` · `drop-on-death` (ампутована кінцівка → аугмент) · `dungeon-generation` (процедурні місії) · `fog-of-war` · `projectile-shot` + `shoot-modes` · `explode-area` (бочки, гранати) · `destructible-blocks` (двері) · `unit-xp-skills` (ранги клона) · `character-select` · `shop-catalog` · `map-window` · `in-game-editor`.
- **Нема** → пропозиції карток:
  - `+action-points` «Очки дії на хід» · game-logic/opponent · 📎; `+movement-modes` «Режими руху з різною ціною й штрафами» · entities/move · 🌱.
  - `+extraction-keep-loot` «Лут зараховується лише після евакуації» · game-logic/win · 📎; `+lose-carried-on-death` «Смерть забирає лише взяте» · game-logic/lose · 🌱; `+clone-reprint` · 🌱; `+run-meta-carry` · 📎.
  - `+limb-wounds` «Рана частини тіла — штраф на тип дії» · entities/state · 🥉; `+amputation` · 📎; `+infection-timer` · 🌱.
  - `+bionic-implants` · 🥉; `+weapon-durability` «Знос і ремонт з падінням максимуму» · entities/state · 📎; `+ammo-limit` · 🌱.
  - `+escalation-counter` «Загроза росте щохід» · game-logic/waves · 📎 (родич `timeout-punisher`); `+corpse-spawns-enemy` · 📎; `+corpse-to-ally` · 📎.
  - `+shoot-through-walls` «Куля проходить крізь стіну, погляд — ні» · entities/combat · 🥉; `+door-blocks-sight` · 🌱.
  - `+faction-reputation` · 📎; `+home-ship-upgrades` «База-корабель з деревом апгрейдів» · game-logic/economy · 🥉.

## Пропозиції до словників
- `+role:body-part` — частина тіла (органічна/роботизована) з раною, переломом, ампутацією.
- `+trigger:ap_zero` — у сторони скінчились очки дії (кінець ходу); `+cond:ap(op, n)` — вистачає AP на дію; `+effect:spend_ap` — списати AP.
- `+effect:extract` — перенести інвентар місії на постійний склад; `+effect:reclone` — новий клон зі збереженням рангу; `+effect:amputate(part)` — відрізати частину тіла.
- `+window:ship-hub`, `+window:contract-board`, `+window:stock-market` — див. «Вікна».
- `+ui:ap-counter` — лишок AP; `+ui:paper-doll` — частини тіла.
- `+feature:workshop` — обмін рівнями через Steam Workshop.
- `+axis:session=extraction-run` — сесія = вилазка зі ставкою спорядженням.

## Джерела
- ⭐ [Steam](https://store.steampowered.com/app/2059170/Quasimorph/) — офіційний опис, теги (Turn-Based, Extraction Shooter, Roguelike), редактор рівнів, Workshop, дати EA і 1.0, Magnum Scriptum / HypeTrain Digital.
- [In-Game Scientist](https://ingamescientist.substack.com/p/fast-paced-turn-based-rogue-like) — крок = хід ворогів, клітини, рани ніг і рук, інфекція, голод, перезаряджання як хід.
- [Steam-гайд «How to not get shafted instantly»](https://steamcommunity.com/sharedfiles/filedetails/?id=3194551184) — AP ходьби/бігу, крадькома, двері, стрільба крізь стіни, бочки, репутація, біржа.
- [Turn Based Lovers](https://turnbasedlovers.com/review/quasimorph-impressions-2/) · [NoobFeed](https://www.noobfeed.com/reviews/quasimorph-review) · [demo impressions](https://playtested.pages.dev/article/2023-06-23-a-fusion-of-turn-based-roguelike-rpg-and-extraction-game-elements-demo-impressions-qua) — квазиморфи, флагман, класи й ранги, аугментації, клік по клітинах.
- [Vaporlens: End of Dream](https://vaporlens.app/app/2347110/quasimorph_end_of_dream) — зведення відгуків: три режими руху, AP, лічильник мутації.

## Непевне
- (?) Офіційна вікі (wiki.gg) агенту недоступна; правила зібрано з оглядів і гайдів спільноти, точні ціни AP за дії й пороги лічильника квазиморфозу невідомі.
- (?) Як саме відбувається евакуація (точка виходу, ліфт, таймер) — джерела кажуть лише «повернутись із зібраним».
- (?) Ампутація голови «переживається з роботизованою головою», роботизовані рани, «гігантська рука» з ампутованого ворога, рециклер — з гайда «Small Things You Might Not Know», позначеного у Steam як видалений.
- (?) Режим крадькома й «тетріс-інвентар» — частково зі зведення відгуків про End of Dream; чи інвентар основної гри теж фігурний — не перевірено.
- (?) «SEAR packages — коробки, що дають за смерть» — природа цих посилок не зрозуміла з гайда.
- (?) Рік: у черзі 2026 (реліз 1.0, 31.07.2026); тут — 2023 (early access 2.10.2023).
- (?) Рух у 8 напрямків — не підтверджено; джерела кажуть лише «одна клітина за крок».
