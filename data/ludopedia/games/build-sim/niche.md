---
title: Niche – a genetics survival game
slug: niche
aka: [Niche]
family: build-sim
also: [tactics]
klass: figure
axes:
  field: hex
  time: turn
  opponent: none
  info: hidden
  random: both
  goal: survive
year: 2017
platforms: [PC, Switch, PS4, Xbox One, mobile (Breed and Evolve, 2021)]
links:
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=1073431418", best: true, note: "Steam-гайд «Creating A Successful Pack»: енергія на дію, гніздо й народження, полювання, лизання, мандрівники за 5 їжі, острови, хвороби від однакового імунітету, ранги A/B/C, меню мутацій, родовід"}
  - {kind: other, url: "https://www.pcgamer.com/niche-blends-turn-based-strategy-roguelike-survival-and-genetic-mutations/", note: "PC Gamer (EA, 2016): дії на раунд, гекси під високою травою, ягоди/кущ, полювання, мутації, інбридинг"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=799896214", note: "Steam-гайд «Niche Genetics Guide»: алелі, домінування, кодомінування, неповне домінування, усі атрибути з межами, імунітет A–K, фертильність, прадавні гени, гібриди"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=2505176938", note: "Steam-гайд про порти подорожей: стела + зона порту, 1 нічелінг на клітину, повернення нема"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Niche_(video_game)", note: "Stray Fawn Studio, EA 2016 → 21.09.2017, понад 100 генів, біоми, режими"}
  - {kind: steam, url: "https://store.steampowered.com/app/440650/Niche__a_genetics_survival_game/"}
  - {kind: official, url: "https://niche-game.com/"}
  - {kind: other, url: "https://www.gog.com/game/niche", note: "GOG: опис + відгуки (гекс-сітка, 3 ходи на тварину)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Niche+a+genetics+survival+game+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [hp-damage, hunger-clock, fog-of-war, status-effects, spawn-random-cell, chase-player, item-pickup, permadeath, save-game, difficulty-levels, mode-select, tutorial-window, achievements-window, +animal-breeding, +mutations, +mendelian-inheritance, +immunity-allele-sickness, +energy-per-action, +sense-ranges, +pack-rank-feeding, +invite-wanderer, +nest-birth, +lifespan-death, +island-travel-port, +family-tree-sort, +resource-regrowth, +hybrid-breeding, +thorns-counter-damage, +infection-spread, +gene-pool-drift]
proposes: ["+effect:breed", "+effect:mutate", "+effect:infect", "+effect:eat", "+effect:sense", "+cond:sensed", "+trigger:night_start", "+window:family-tree", "+window:mutation-menu", "+window:gene-panel", "+ui:action-pips", "+ui:perception-toggle", "+card:mendelian-inheritance", "+card:immunity-allele-sickness", "+card:sense-ranges"]
author: opus
date: 2026-11-09
---

# Niche — покрокове виживання зграї на гексах: годуй, схрещуй і веди генофонд, доки вид не вимер

## Суть
Покрокова стратегія-симуляція з елементами роглайку від Stray Fawn Studio (виросла з дипломної роботи Філомени Шваб про популяційну генетику). Гравець керує зграєю «нічелінгів» на гексовій карті острова: кожна тварина за день має кілька дій — рух, збирання, полювання, бій, спарювання, — а потомство успадковує алелі батьків за справжніми правилами Менделя. Мета — не дати виду вимерти перед хижаками, голодом, хворобами й кліматом, підбираючи пари й мутації під біом. Ядро для курсу — **генотип як дані клітини-тварини** і **спадкування як функція двох генотипів**.

## Поле і час
- Гексова карта острова (процедурна); клітини: трава, висока трава (заступає огляд, перериває рух), пісок/берег, річка, мілина, глибоке море, болото, сніг, гори.
- Видимість — спільна для зграї, але три **режими сприйняття**: зір, слух, нюх; клітину, яку не відчуває жодне чуття, не можна обрати для дії.
- Хід = день: кожна тварина має запас енергії (зелені овали), кожна дія коштує 1; кнопка «захід сонця» — ніч: сон відновлює енергію, вагітні в гнізді народжують, усі старшають, хворі втрачають HP.
- Острови йдуть ланцюгом через порти-стели; новий острів — нова карта (з півдня), назад не повернутись.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Нічелінг | player | генотип (понад 100 генів), вік, HP, енергія, ранг A/B/C, стать | рух ≤ speed клітин за дію, збирає, полює, бʼється, спарюється, лиже рани |
| Дитинча | player | вік | перші дні в гнізді, не ходить; росте |
| Гніздо | static | 10 матеріалу на гніздо | вагітна самка в гнізді вночі народжує |
| Кущ ягід | resource | ягоди | збирання дає їжу = вмінню collecting; «порубати» — усі ягоди одразу, але кущ довго відростає |
| Дуб / кокос / мушля / устриця | resource | — | горіхи й мушлі треба «розколоти» (cracking) |
| Висока трава | terrain | — | ховає вміст, перериває рух; розчищена — часом матеріал для гнізда |
| Вода (річка / море) | terrain | — | плавання (swimming), у глибокому морі — лише з підводним диханням |
| Кріт / кролик | neutral | — | здобич; повертається/тікає після кожного ходу гравця |
| Косяк риби · водорості | resource | — | риба — їжа (fishing); водорості — матеріал для гнізда (webbed paw) |
| Бірієна (Bearyena) | enemy | сила, HP | хижак, нападає на зграю; дитинча без дорослого можна приручити |
| Ведмеді (мирний, захисник, баланс) | neutral | — | захисник кидається на того, хто вбив у нього на очах; баланс атакує до знесилення, дає мʼясо |
| Арктичні рамфокси | enemy | зграя | полюють групою, оточують (сніг) |
| Мавпи (зір / нюх / слух) | enemy | — | помічають за своїм чуттям; камуфляж / беззапашність / тиша ховають, «відштовхувальний» вигляд/запах лякає |
| Хижий птах | enemy | — | майже на всіх островах |
| П'явка, разоранія | hazard | — | п'явка висмоктує, знімає сусід або атака |
| Хижа рослина | hazard | стан дружня/зла | зірвеш останній плід — може стати злою й зʼїсти (50 %) |
| Цілюща рослина / водна цілюща | pickup | регенерує довго | лікує й знімає застуду / трохи лікує й дає дихання під водою |
| Самотній мандрівник | neutral | генотип | приєднується за 5 їжі; новий імунітет у генофонд |
| Rogue male | enemy | гени Derp Snout + Deformed Paw | не запрошується; сусідню самку запліднює сам |
| Льодовик (сніг) | container | — | розбити → нічелінг з прадавнім геном одразу в зграї |
| Порт подорожі | zone | стела + N клітин | 1 нічелінг на клітину переходить на новий острів |
| Скелет | static | — | лишається після смерті; хвороба на кістках не живе |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(action, a)` → ЯКЩО `counter(energy_a, >, 0)` → ТО `custom: «дія»`, `counter(energy_a, -1)`; інакше `block`.
- КОЛИ `input(move, a, hex)` → ЯКЩО `custom: «до hex ≤ speed (на суші) / swimming (у воді); висока трава зупиняє»` and `custom: «hex відчутий хоча б одним чуттям зграї»` → ТО `move(a, to: hex)`.
- КОЛИ `input(collect, bush)` → ЯКЩО `in_range(a, bush, 1)` → ТО `counter(food, +collecting_a)`; інакше — «низький шанс успіху» без уміння.
- КОЛИ `input(slash, bush)` → ТО `counter(food, +all_berries)`, `set_state(bush, regrowing, long)`.
- КОЛИ `input(attack, a, b)` → ЯКЩО `in_range(a, b, 1)` → ТО `damage(b, strength_a − defense_b)`; venomous — `set_state(b, poisoned, n)`.
- КОЛИ `hp_zero(prey)` → ТО `custom: «туша → їжа зграї»`.
- КОЛИ `contact(any, spiky_nicheling)` → ТО `damage(any, 1)` — навіть свої, що лижуть рану; КОЛИ `contact(attacker, toxic_body)` → ТО `set_state(attacker, poisoned)`.
- КОЛИ `input(growl, a)` → ЯКЩО `custom: «Strong Voice»` → ТО `custom: «хижак переключає ціль на іншу тварину»`.
- КОЛИ `input(lick, a, b)` → ЯКЩО `in_range(a, b, 1)` → ТО `clear_state(b, bleeding)`.
- КОЛИ `input(mate, a, b)` → ЯКЩО `in_range(a, b, 1)` and `custom: «стать різна, фертильність обох > 0»` and `prob(fertility)` → ТО `set_state(female, pregnant)`.
- КОЛИ `custom: «ніч»` → ЯКЩО `state(female, pregnant)` and `occupied(nest, female)` → ТО `spawn(cub, nest)`; поза гніздом — пологів нема.
- КОЛИ `spawned(cub)` → ТО `custom: «кожен ген = по алелю від кожного батька: домінантний/рецесивний (вуха, роги, голова, тіло…), кодомінантний (ліва/права лапа, фертильність, імунітет), неповне домінування (кольори)»`.
- КОЛИ `spawned(cub)` → ЯКЩО `custom: «в меню мутацій обрано ген у слоті 50 %»` → ТО `custom: «підвищений шанс цього алеля в дитинчати, навіть якщо в батьків його нема»`.
- КОЛИ `spawned(cub)` → ЯКЩО `same(allele1, allele2, immunity)` → ТО `set_state(cub, sick, forever)` — шкода щоходу, заражає сусідів.
- КОЛИ `turn_end` → ЯКЩО `state(a, sick)` and `adjacent_count(a, nicheling, >=, 1)` → ТО `set_state(neighbor, sick, few_days)`.
- КОЛИ `turn_end` → ЯКЩО `counter(food, <, pack_size)` → ТО `custom: «їдять за рангом A → B → C; кому не вистачило — голод і шкода»`.
- КОЛИ `turn_end` → ТО `counter(age, +1)`; КОЛИ `counter(age, >=, lifespan)` → ТО `custom: «смерть від старості, лишається скелет»`.
- КОЛИ `input(invite, loner)` → ЯКЩО `counter(food, >=, 5)` → ТО `counter(food, -5)`, `set_side(loner, pack)`.
- КОЛИ `adjacent(rogue_male, female)` → ТО `custom: «самка вагітніє від ізгоя — дитя з поганими генами»`.
- КОЛИ `input(break, glacier)` → ТО `spawn(nicheling_with_prehistoric_gene)`, `set_side(it, pack)`.
- КОЛИ `input(collect, carnivorous_plant)` → ЯКЩО `custom: «зірвано останній плід»` and `prob(0.5)` → ТО `set_state(plant, hostile)`; поруч зла — `custom: «рослина хапає нічелінга»`.
- КОЛИ `input(travel, stele)` → ТО `custom: «на новий острів переходять ті, хто стоїть у зоні порту (1 на клітину); решта лишаються назавжди»`, `next_level`.
- КОЛИ `all_gone(nicheling)` → ТО `lose` — вид вимер, новий світ з нуля.
- КОЛИ `reach(pack, home_island)` → ЯКЩО `mode(story)` → ТО `win`.
- Перемога: (сюжет) дійти до Home Island · Поразка: вимирання виду · Рахунку нема.

## Керування і ввід
- Мишею: обрати тварину → клітина руху; «…» під твариною/обʼєктом → кнопки дій (серце — спарювання, лапа з плодом — збирати, кігті — атака, язик — лизати; на стелі порту — пальма «подорож»).
- Пробіл або кнопка «захід сонця» — кінець дня.
- Перемикач режиму сприйняття (зір / нюх / слух) у правому нижньому куті: показує, що чує/бачить/нюхає зграя.
- Меню мутацій: окрема кнопка → клік по слоту «50 %» на ДНК-смузі → вибір гена → галочка.

## Вікна, меню, HUD
- `main-menu`: сюжет, швидке навчання (`tutorial-window`), sandbox (вибір тварин і рельєфу) — `mode-select`.
- `game-screen`: гекс-карта, над тваринами — `+ui:action-pips` (овали енергії), іконки станів (вагітна, хвора — червона/зелена пляма, кровотеча, отруєна), `turn-counter` (день), запас їжі й матеріалу для гнізд.
- `+window:gene-panel`: генотип і фенотип обраної тварини — ДНК-смуга з двома алелями на ген (активний і неактивний), значки умінь (швидкість, плавання, копання, сила, фертильність, імунітет, зір, слух, нюх, стелс, беззапашність, холод, жара), ранг A/B/C, друга вкладка — вигляд (хутро, візерунок, роги).
- `+window:mutation-menu`: слоти 50 % на ДНК і список доступних генів.
- `+window:family-tree`: живі й нещодавно мертві тварини, сортування за геном/умінням (числа на іконках, яскраві — носії активного гена, темні — прихованого).
- `confirm-dialog`: «хто поза зоною порту — лишиться».
- `settings-window` (складність), `save-slots`/збереження будь-коли, `achievements-window`, `end-screen` вимирання.
- Переходи: main-menu → game-screen ↔ gene-panel / mutation-menu / family-tree; game-screen → (порт) confirm-dialog → game-screen нового острова.

## Фічі поза полем
- `mode-sandbox` (власні тварини й рельєф), сюжет-навчання; складність; збереження будь-коли; `achievements`; хмарні сейви.
- Безкоштовна освітня версія для шкіл (та сама, що в Steam); вбудована консоль розробника (гайд спільноти).
- `codex`-подібне: підказки при наведенні на іконку гена.

## Варіації й родичі
- **Niche – Breed and Evolve** (2021, мобільна): 2D, полювання, збирання, хижаки.
- **Осі варіацій «спадкування»**: тип взаємодії алелів (домінування / кодомінування / неповне) · хвороба від гомозиготи (імунітет A–K) · джерело нових алелів (мутація-вибір / мандрівник / гібрид / прадавній ген із льоду) · відбір (середовище / рішення гравця про пари).
- Гібриди: бірієна + нічелінг — гібрид завжди отримує частину генів бірієни (сила, але повільність).
- Розблокування генів дією (за відгуком GOG: 30 запливів → перетинчасті лапи) — див. «Непевне».
- Родичі в корпусі: [sugarscape](sugarscape.md) (агенти з генами, імунітет бітовими рядками, розмноження), [viva-pinata](viva-pinata.md) (розведення видів під умови), [rimworld-rooms](rimworld-rooms.md) (потреби колоністів), [simant](simant.md) (колонія проти хижаків).

## Цікавинки для курсу
- Генотип як два алелі на ген + домінування за ланцюжком порядку («Medium > Big > Round > Bearyena») — 📎.
- Спарювання = функція двох генотипів; кодомінування (лапи ліва/права) і неповне домінування (змішування кольорів RGB) — 🥉.
- Однаковий алель імунітету → хворе дитя назавжди + зараження сусідів у кінці ходу — 🌱.
- Три режими сприйняття з різними радіусами (зір 0–2, слух 3–8, нюх 0–5) і заборона дії на невідчуту клітину — 🥉.
- Ранг A/B/C як черга годування при нестачі їжі — 🌱.
- Родовід із фарбуванням носіїв прихованого гена — 🥈 (обхід дерева предків + відображення).
- Порт подорожі: «береш лише тих, хто в зоні», назад дороги нема — 📎.

## Мапа на каталог
- Є: `hp-damage` · `hunger-clock` (їжа зграї) · `fog-of-war` (висока трава, радіуси чуттів) · `status-effects` (кровотеча, отрута, хвороба, вагітність) · `spawn-random-cell` (мандрівники, хижаки) · `chase-player` (хижаки) · `item-pickup` · `permadeath` (вимирання = новий світ) · `save-game` · `difficulty-levels` · `mode-select` · `tutorial-window` · `achievements-window`.
- Перевикористано з корпусу: `+animal-breeding`, `+mutations`, `+resource-regrowth`.
- **Нема** → пропозиції карток:
  - `+mendelian-inheritance` «Нащадок бере по алелю від кожного з батьків; домінування за порядком» · entities/state · 📎 · слоти {interaction: dominant|codominant|partial}.
  - `+immunity-allele-sickness` «Гомозигота за імунітетом = хворе дитя» · entities/state · 🌱.
  - `+energy-per-action` «Енергія на день, кожна дія −1» · game-logic · 🌱 (родич `action-points`).
  - `+sense-ranges` «Кілька чуттів з різними радіусами; дія лише на відчуту клітину» · interface/render · 🥉.
  - `+pack-rank-feeding` «Черга годування за рангом при нестачі» · game-logic/economy · 🌱.
  - `+invite-wanderer` «Найняти мандрівника за ресурс» · entities/interact · 🌱.
  - `+nest-birth` «Народження лише в гнізді вночі» · entities/spawn · 🌱.
  - `+lifespan-death` «Смерть від віку» · entities/state · 🌱.
  - `+island-travel-port` «Перехід на нову карту лише з зони порту, без повернення» · levels/progression · 📎.
  - `+family-tree-sort` «Родовід із сортуванням за ознакою» · interface/menus · 🥈.
  - `+hybrid-breeding` · `+thorns-counter-damage` · `+infection-spread` · `+gene-pool-drift` — гібриди з іншим видом; шкода тому, хто торкнувся; зараження сусідів у кінці ходу; потік генів через мандрівників.

## Пропозиції до словників
- `+effect:breed` — спарювання двох сутностей із результатом-нащадком (уже в корпусі); `+effect:mutate` — змінити алель/ознаку (уже); `+effect:infect` — передати хворобу (уже); `+effect:eat` — спожити їжу (уже).
- `+effect:sense` (уже) і `+cond:sensed(cell, mode)` — клітину відчуто зором/слухом/нюхом хоча б однієї тварини зграї; без неї дія заборонена.
- `+trigger:night_start` — кінець дня: сон, пологи, старіння (уже в корпусі).
- `+window:family-tree` — родовід із сортуванням; `+window:mutation-menu` — вибір генів для наступних нащадків; `+window:gene-panel` — генотип/фенотип особини.
- `+ui:action-pips` — овали енергії над фігурою (уже в корпусі); `+ui:perception-toggle` — перемикач режиму сприйняття карти.
- `+card:mendelian-inheritance`, `+card:immunity-allele-sickness`, `+card:sense-ranges` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam-гайд «Creating A Successful Pack» (! Winter)](https://steamcommunity.com/sharedfiles/filedetails/?id=1073431418) — старт Адам і Єва, енергія (кожна дія −1), гніздо (10 матеріалу) і пологи вночі, полювання на кротів і кроликів, риболовля, лизання кровотечі, мандрівник за 5 їжі, порти островів, хвороба від однакового імунітету, ранги A/B/C, значки умінь, меню мутацій, родовід.
- [PC Gamer: Niche blends turn-based strategy, roguelike survival, and genetic mutations](https://www.pcgamer.com/niche-blends-turn-based-strategy-roguelike-survival-and-genetic-mutations/) — дії на раунд, висока трава як туман, порубати кущ, інбридинг, меню мутацій.
- [Steam-гайд «Niche Genetics Guide» (W-Cactus)](https://steamcommunity.com/sharedfiles/filedetails/?id=799896214) — алелі й три типи взаємодії, порядки домінування, межі атрибутів (зір 0–2, слух 3–8, нюх 0–5, швидкість 1–6, сила 0–12, захист 0–3), режими сприйняття, імунітет A–K + Home Island, фертильність, 6 прадавніх генів, гібриди.
- [Steam-гайд про порти подорожей (Jekkil)](https://steamcommunity.com/sharedfiles/filedetails/?id=2505176938) — стела й зона порту, рівні островів за стелою, біом за плиткою, 1 нічелінг на клітину, прибуття з півдня, повернення нема.
- [Steam-гайд «Beginner's Guide to the world of Niche» (al)](https://steamcommunity.com/sharedfiles/filedetails/?id=2540225276) — ізгої, хижаки й мавпи за чуттями, хижі рослини, п'явки, льодовики, цілющі рослини.
- [Wikipedia: Niche (video game)](https://en.wikipedia.org/wiki/Niche_(video_game)) · [Steam](https://store.steampowered.com/app/440650/Niche__a_genetics_survival_game/) · [GOG](https://www.gog.com/game/niche) · [офіційний сайт](https://niche-game.com/).
- YouTube: пошук «Niche a genetics survival game gameplay».

## Непевне
- (?) Скільки енергії на день: відгук GOG — «рівно 3 ходи на тварину»; гайди лише показують овали; можливо, залежить від генів.
- (?) Кількість біомів: Wikipedia — 4, Steam і прескіт — 5.
- (?) Розблокування генів повторенням дії (30 запливів → перетинчасті лапи) — лише з відгуку користувача GOG.
- (?) Голод у саванні/снігу «5 % втратити всю їжу» — із застарілого (за словами автора) гайду; не вніс у правила.
- (?) Точна формула шкоди (сила − захист) і шанс зачаття від фертильності — у гайдах «To Do: confirm».
- (?) Платформи консолей — за посиланнями офіційного сайту, роки консольних версій не перевірено.
