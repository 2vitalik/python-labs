---
title: Jagged Alliance 2
slug: jagged-alliance-2
aka: [JA2, "Jagged Alliance 2: Unfinished Business", "Jagged Alliance 2: Wildfire", JA2 1.13, JA2 Stracciatella]
family: tactics
also: []
klass: figure
axes:
  field: layers
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 1999
platforms: [PC, Linux, Mac]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Jagged_Alliance_2", best: true, note: "AP за раунд від стану, перенос невитрачених AP і перехоплення, real-time ↔ turn-based, сектори, міліція, шахти, лептоп, рани й енергія, моди"}
  - {kind: other, url: "https://www.fadden.com/gaming/ja2/ja2-official-secrets.txt", note: "офіційні «секрети» 1999: прицілювання +10 за AP, штрафи по присілій/лежачій цілі, сошки, шок, дихання, рани"}
  - {kind: other, url: "https://jas-guide.pages.dev/en/resources/jaggedalliance.en/tips", note: "поради гравців: AP на «лягти», перехоплення під час очікування, двері, прострілювання наскрізь"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Jagged+Alliance+2"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Jagged+Alliance+2+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [hp-damage, projectile-shot, shoot-burst, line-of-sight-attack, fog-of-war, height-levels, orientation-state, destructible-blocks, explode-area, key-and-door, inventory, inventory-items, inventory-limit, item-pickup, status-effects, unit-xp-skills, ai-opponent, realtime-ai, permadeath, world-map, map-window, shop-window, round-currency, save-multi-slot, difficulty-levels, rule-variants, in-game-editor, message-log, +mod-support, +action-points, +ap-carryover, +stance-system, +interrupt-turn, +aimed-shot-ap, +body-part-targeting, +hit-chance, +realtime-to-turn-switch, +breath-energy, +bleeding-bandage, +merc-hiring-contracts, +militia-training, +sector-control-income, +merc-morale-relations]
proposes: ["+trigger:spotted", "+trigger:enemy_moved", "+cond:stance", "+effect:interrupt", "+effect:set_stance", "+effect:spend_ap", "+ui:ap-counter", "+ui:hit-chance", "+ui:stance-icon", "+ui:breath-bar", "+window:laptop", "+window:merc-hire", "+window:sector-map", "+window:imp-test", "+feature:time-compression", "+axis:time=hybrid-rt-turn"]
author: opus
date: 2026-11-09
---

# Jagged Alliance 2 — найманці з очками дії: поза, прицілювання й перехоплення ходу на клітинній мапі, війна за сектори острова

## Суть
Гравець наймає загін найманців, щоб звільнити острів Арулко сектор за сектором. На тактичній мапі всі дії коштують **очки дії (AP)**: крок, зміна пози (стоячи / присівши / лежачи), постріл, прицілювання, відкрити двері. Ворог, що зʼявився в полі зору, може **перехопити хід** (interrupt) посеред чужого руху. Дослідження йде в реальному часі, а бій вмикається покроково, щойно сторони помітили одна одну. Над тактикою — стратегічний шар: сектори, шахти й гроші, міліція, контракти найманців.

## Поле і час
- Тактична мапа сектора — ізометрична квадратна сітка з **дахами** (другий рівень, на який вилазять) і будівлями з дверима; стіни, паркани, кущі, дерева.
- Туман війни: видно те, що бачить хоч один найманець; дальність огляду менша вночі; напрям погляду важить (?).
- Час: real-time, поки ніхто нікого не бачить; КОЛИ одна сторона помітила іншу — покрокові раунди: хід сторони, усі її юніти витрачають AP у будь-якому порядку.
- Стратегічний шар — сітка секторів острова в реальному часі з прискоренням і паузою.
- Випадковість: влучання, шкода, частина перехоплень, поведінка AI.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Найманець (A.I.M., M.E.R.C., місцевий, I.M.P.) | piece | HP, AP, Breath, Agility, Dexterity, Strength, Leadership, Wisdom, Marksmanship, Explosives, Mechanical, Medical, рівень досвіду, спецнавички, морал | рух, пози, постріли, предмети; росте від використання навичок (?) |
| Солдат армії Дейдранни | enemy | ті самі, рівні якості (?) | AI: патрулі, укриття, обхід, перехоплення |
| Міліція | ally | навчені місцеві | обороняє сектор, AI-керована |
| Цивільний / NPC | neutral | діалог | квести, торгівля, найм |
| Створіння (sci-fi режим) | enemy | — | великі, перехоплення по них гарантовані (за порадами гравців) |
| Двері | gate | замок, пастка | відкрити/закрити за AP; відмичка, лом, вибухівка |
| Дах | terrain | рівень 2 | залізти за AP (?), огляд і бонус позиції |
| Стіна / огорожа | static | — | блокує рух і огляд; частина руйнується вибухом |
| Кущі, дерева | terrain | — | ховають, але майже не захищають від куль |
| Бочка з пальним | hazard | — | вибухає від пострілу, ранить сусідів |
| Зброя / броня / навіс | pickup | вага, AP на постріл, магазин | 1 велика зброя або 2 малі; броня на голову, груди, ноги; глушник, сошки |
| Шахта (стратегічна) | resource | дохід/день | дає гроші, якщо місто звільнене й шахтарі працюють |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «одна сторона помітила іншу»` → ТО `custom: «real-time → покрокові раунди»`; КОЛИ `all_gone(enemy)` → ТО назад у real-time, сектор звільнено.
- КОЛИ `turn_start(merc)` → ТО `custom: «AP = база від Agility/рівня, менше від ран і втоми; частина невитрачених AP переноситься»`.
- КОЛИ `input(move, merc, cell)` → ЯКЩО `path_exists(merc, cell)` and `counter(AP, >=, cost)` → ТО `move(merc, cell)`, `counter(AP, −cost)`; ціна кроку залежить від режиму (біг, хода, присівши, повзком) і терену (?).
- КОЛИ `input(stance, merc, s)` → ЯКЩО `counter(AP, >=, cost)` → ТО `set_state(merc, s)` (stand | crouch | prone), `counter(AP, −cost)`.
- КОЛИ `input(shoot, a, t)` → ЯКЩО `line_of_sight(a, t)` and `counter(AP, >=, shot_cost)` → ТО `prob(hit)` → `damage(t, n)`.
- Прицілювання: КОЛИ `input(aim, a, k)` → ТО `counter(AP, −k)`, `custom: «≈ +10 до шансу за кожне AP (до 4 кліків); +10, якщо та сама ціль, що й минулого пострілу»`.
- Поза цілі: ЯКЩО `state(t, crouch)` → ТО `custom: «до −20 % шансу»`; ЯКЩО `state(t, prone)` → ТО `custom: «до −40 %»`; штраф 0 на дальності ≤ 5 і +3 % за клітину далі.
- КОЛИ `input(shoot, a, t)` → ЯКЩО `state(a, prone)` and `has(a, bipod)` → ТО `custom: «+10 % до шансу»`.
- Черга: КОЛИ `input(burst, a, t)` → ТО `custom: «кілька куль; кожна наступна з штрафом 5–11 %»`.
- Частина тіла: КОЛИ `input(target, head|torso|legs)` → ТО `custom: «голова — більше шкоди й менший шанс; ноги — менший шанс падіння цілі (?)»`.
- Перехоплення: КОЛИ `custom: «ворог зʼявився в полі зору під час чужого ходу»` → ЯКЩО `prob(p)` (досвід, рефлекс, AP, Night Ops уночі) → ТО `custom: «хід переривається; перехоплювач діє своїми AP; потім хід повертається»`.
- Мод 1.13 (NIS): КОЛИ `custom: «ворог витратив N AP у полі зору»` → ТО `custom: «перехоплення»` — детермінованіше за кидок.
- Шок і дихання: КОЛИ `damage(merc, n)` → ТО `custom: «шок = 1/10 втраченого HP + 1/20 втраченого дихання; −5 % до шансу за 1 шок; половиниться кожного ходу»`.
- Рани: КОЛИ `custom: «поранено»` → ТО `set_state(merc, bleeding)`; КОЛИ `input(bandage, medic, merc)` → ТО `clear_state(merc, bleeding)` — HP не повертає.
- КОЛИ `hp_zero(merc)` → ТО `custom: «падає й помирає поступово без допомоги; смерть остаточна»`; критичні рани знімають атрибути.
- КОЛИ `counter(breath, ==, 0)` → ТО `custom: «найманець падає, доки не відновить енергію»`.
- КОЛИ `input(stealth, merc)` → ТО `set_state(merc, sneaking)` — рух дорожчий за AP, але тихіший.
- КОЛИ `input(open, merc, door)` → ЯКЩО `state(door, locked)` → ТО `custom: «відмичка / лом / вибухівка / ключ»`; пастка на дверях — перевірка навичок.
- Стратегія: КОЛИ `custom: «місто звільнене і шахтарі згодні»` → ТО `currency(+income)` щодня; КОЛИ `input(train_militia, merc, sector)` → ТО `spawn_at(militia, sector)`.
- Морал: КОЛИ `custom: «перемоги й убивства»` → ТО `custom: «морал ↑»`; ЯКЩО `custom: «поруч найманець, якого не любить»` → ТО `custom: «скарги, може піти»`.
- Перемога: звільнити острів і вбити королеву Дейдранну. Поразка: `custom: «загін знищено / гроші скінчились»` (?).

## Керування і ввід
- Миша по клітинах: клік — рух (режим ходи/бігу/присіду/повзання), клік по ворогу — постріл; ПКМ на цілі — клацання прицілювання (кожне додає AP); кнопки поз S / C / P (stand, crouch, prone).
- Вибір частини тіла, черга / одиночний; кидок гранати по клітині; дія «повернутись лицем».
- Інвентар: перетягування предметів між руками, жилетом і кишенями, обмін між найманцями.
- Покроковий режим: кнопка завершення ходу; у real-time — вільний рух загоном.

## Вікна, меню, HUD
- `main-menu`: New Game (складність, Realistic / Sci-Fi, сейви будь-де / Iron Man у пізніших версіях (?)), Load, Options.
- `game-screen`: ізометрична мапа; панель найманців унизу з портретами, `hp-bar`, `breath-bar`, `ap-counter`, `stance-icon`; `hit-chance` при наведенні (?); `fog-of-war`; `message-log`.
- `inventory-window` — тіло найманця зі слотами: руки, голова, груди, ноги, жилет, кишені.
- `sector-map` — стратегічна сітка острова: загони, маршрути, ворожі сили, лояльність міст (?), шахти; пауза й прискорення часу (`map-window`).
- `laptop` — внутрішньоігровий «комп’ютер»: пошта, `merc-hire` (A.I.M., M.E.R.C. — профілі, ціни, контракти), Bobby Ray's (`shop-window` зброї), страхування, фінанси.
- `imp-test` — анкета I.M.P. для створення власного найманця.
- Діалоги з NPC (`dialogue-window`); `save-slots`; `end-screen` / титри.

## Фічі поза полем
- Найм найманців на контракт (день / тиждень / 2 тижні (?)), звільнення; найманці мають характер, симпатії й антипатії.
- Економіка: шахти, продаж лута торговцям, щоденні витрати на контракти.
- Міліція захищає звільнені сектори; армія контратакує на стратегічній мапі.
- Лікування й ремонт між боями (медик з аптечкою, механік з ящиком); відпочинок для енергії.
- Unfinished Business — `level-editor` сценаріїв; Wildfire — відкритий код, загін до 10; v1.13 — налаштування в XML (`custom-rules`, `mod-support`), мультиплеєр; Stracciatella — кросплатформний порт.

## Варіації й родичі
- Серія: Jagged Alliance (1994), Deadly Games (1996, мультиплеєр), Back in Action (реальний час з паузою), Jagged Alliance 3 (2023).
- Родичі: X-COM: UFO Defense (очки часу, реакційний вогонь — порівняй з [xcom](xcom.md)), Silent Storm, Fallout 1–2 (AP і цільові частини тіла, не загін), [invisible-inc](invisible-inc.md) (AP і стелс).
- Осі варіацій:
  - **дії**: AP-пул на всі дії (JA2, X-COM) / 2 дії (XCOM) / рух + дія (FE);
  - **реакція**: перехоплення кидком при появі в полі зору (JA2) / за витраченими AP у полі зору (1.13 NIS, X-COM reaction fire) / Overwatch по руху (XCOM);
  - **пози**: нема / укриття ребрами (XCOM) / три пози з ціною в AP і штрафом по цілі (JA2);
  - **час**: тільки покроково / real-time поза боєм, покроково в бою (JA2).

## Цікавинки для курсу
- AP-пул з ціною кожної дії і частковим переносом на наступний хід — 📎.
- Три пози: ціна зміни, ціна руху, штраф по цілі від пози й дальності — 📎.
- Перехоплення ходу: зупинити рух сторони, віддати хід іншому юніту, повернути — 🥈 (стек ходів).
- Прицілювання «+10 за AP» і модифікатори шансу (поза, дальність, ніч, шок) — 📎.
- Перемикання real-time ↔ покроково за умовою «бачать один одного» — 🥉.
- Стратегічна сітка секторів: контроль, дохід шахт, міліція — 🥈.

## Мапа на каталог
- Є: `hp-damage` · `projectile-shot` + `shoot-burst` ↔ одиночний і черга · `line-of-sight-attack` · `fog-of-war` · `height-levels` ↔ дахи · `orientation-state` ↔ напрям погляду · `destructible-blocks` + `explode-area` ↔ вибухи стін і бочок · `key-and-door` ↔ замкнені двері · `inventory` + `inventory-items` + `inventory-limit` + `item-pickup` · `status-effects` ↔ кровотеча, шок, втома · `unit-xp-skills` · `ai-opponent` + `realtime-ai` · `permadeath` · `world-map` + `map-window` ↔ сектори · `shop-window` + `round-currency` ↔ Bobby Ray's і гроші · `save-multi-slot` · `difficulty-levels` · `rule-variants` ↔ Realistic / Sci-Fi · `in-game-editor` ↔ UB · `message-log`.
- **Нема** → пропозиції карток:
  - `+action-points` (з XCOM) — тут пул AP на всі дії.
  - `+ap-carryover` «Невитрачені AP частково переходять» · entities/combat · 🌱.
  - `+stance-system` «Пози стоячи/присід/лежачи» · entities/combat · 📎 · слот {stand, crouch, prone}.
  - `+interrupt-turn` «Перехоплення ходу» · game-logic/opponent · 🥈.
  - `+aimed-shot-ap` «Прицілювання за AP» · entities/combat · 🌱.
  - `+body-part-targeting` «Ціль: голова / тулуб / ноги» · entities/combat · 📎.
  - `+hit-chance` (з Wesnoth/XCOM).
  - `+realtime-to-turn-switch` «Real-time до контакту, далі покроково» · game-logic/loop · 🥉.
  - `+breath-energy` «Дихання/енергія як другий пул» · entities/combat · 🌱.
  - `+bleeding-bandage` «Кровотеча й перевʼязка» · entities/combat · 🌱.
  - `+merc-hiring-contracts` «Найм на контракт з оплатою за час» · progression · 📎.
  - `+militia-training` «Навчити міліцію для захисту сектора» · progression · 📎.
  - `+sector-control-income` «Контроль секторів дає дохід» · progression · 🥉.
  - `+merc-morale-relations` «Морал і стосунки найманців» · progression · 📎.
  - `+mod-support` «Моди: правила в зовнішніх файлах» · meta · 📎.

## Пропозиції до словників
- `+trigger:spotted(a, b)` — B уперше потрапив у поле зору A (старт бою, перехоплення; родич `sighted` з XCOM).
- `+trigger:enemy_moved(e)` (з XCOM) — ворог витратив AP / зробив крок у полі зору (1.13 NIS).
- `+cond:stance(a, s)` — поза юніта (stand / crouch / prone).
- `+effect:interrupt(a)` — перервати хід поточної сторони і віддати хід A.
- `+effect:set_stance(a, s)` — змінити позу; `+effect:spend_ap(a, n)` — витратити очки дії.
- `+ui:ap-counter` — залишок AP над/біля юніта; `+ui:hit-chance` (з XCOM); `+ui:stance-icon` — іконка пози; `+ui:breath-bar` — смуга дихання/енергії.
- `+window:laptop` — внутрішньоігровий «компʼютер» з сайтами; `+window:merc-hire` — каталог найманців з контрактами; `+window:sector-map` — стратегічна сітка секторів; `+window:imp-test` — анкета створення персонажа.
- `+feature:time-compression` — прискорення стратегічного часу.
- `+axis:time=hybrid-rt-turn` — real-time поза боєм, покроково в бою.

## Джерела
- ⭐ [Wikipedia: Jagged Alliance 2](https://en.wikipedia.org/wiki/Jagged_Alliance_2) — AP від стану, перенос і перехоплення, real-time ↔ turn-based, сектори, міліція, шахти, лептоп, 5 атрибутів і 4 навички, рани, енергія, морал, UB/Wildfire/1.13/Stracciatella.
- [JA2 Official Secrets](https://www.fadden.com/gaming/ja2/ja2-official-secrets.txt) — прицілювання +10/AP, штрафи по присілій (−20) і лежачій (−40) цілі з дальності 5, сошки +10, шок, дихання, рани, черга.
- [JA2 tactics tips](https://jas-guide.pages.dev/en/resources/jaggedalliance.en/tips) — AP на «лягти», перехоплення під час очікування, двері, кущі не захищають.
- Steam: пошук «Jagged Alliance 2».
- YouTube: пошук «Jagged Alliance 2 gameplay».

## Непевне
- (?) Точні ціни AP: крок по режимах, зміна пози, відкриття дверей, вилізти на дах; скільки AP переноситься.
- (?) Формула перехоплення в оригіналі (кидок за досвідом/рефлексом); у 1.13 NIS — за витраченими AP (з блогу розробника Merc Tactics у результатах пошуку, сторінку не відкрив).
- (?) Тривалість контрактів, лояльність міст, умова поразки кампанії.
- (?) Ріст атрибутів від використання; Iron Man лише в пізніших збірках.
- (?) Ефект пострілу в ноги.
