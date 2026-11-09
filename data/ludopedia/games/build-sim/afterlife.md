---
title: Afterlife
slug: afterlife
aka: ["Afterlife: The Last Word in Sims"]
family: build-sim
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: both
  goal: none
year: 1996
platforms: [DOS, Windows, Mac]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Afterlife_(video_game)", best: true, note: "огляд: 7 гріхів і 7 чеснот, тенети, vibes, робітники, Bad Things, умови поразки"}
  - {kind: other, url: "https://archive.org/details/afterlife-official-players-guide-jo-ashburn", note: "Official Player's Guide (1996, скан з OCR): пульт, дороги ≤3 клітини, vibes і радіуси, банки, Bad Things, формули ефективності й сусідства"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Afterlife+1996+LucasArts+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [cell-click, multi-cell-size, coverage-area, connectivity-check, round-currency, cell-transform, spawn-random-cell, difficulty-levels, game-pause, save-game, map-window, tutorial-window, cheat-codes, level-select, +realm-mirror, +zone-evolution, +vibes-aura, +adjacency-score, +walk-distance-score, +soul-routing, +worker-economy, +balance-slider, +lock-growth, +bank-loan, +disasters, +disaster-protection-radius, +population-milestone-reward, +planet-influence, +overflow-buffer]
proposes: ["+cond:field", "+card:vibes-aura", "+card:zone-evolution", "+window:advisor-window", "+window:graphs-window", "+window:query-window", "+feature:disaster-toggle", "+feature:loans", "+ui:loss-spikes"]
author: opus
date: 2026-11-09
---

# Afterlife — SimCity для Раю й Пекла: душі йдуть дорогами до зон своїх гріхів і чеснот, а зони ростуть лише під правильними vibes

## Суть
Гравець — Деміург, що будує загробний світ для мешканців однієї планети (EMBO). Душі приходять через Ворота й самі шукають дорогами зону своєї долі: 7 гріхів у Пеклі, 7 чеснот у Раю, плюс генеричні зони навпіл дешевші й навпіл місткіші. Гравець не будує будинки — він розмічає зони, тягне дороги й ставить службові споруди; зона «еволюціонує» у більші будівлі, якщо вона заповнена, має добрі vibes від сусідів, збалансована й живлена Ad Infinitum. Два царства — дзеркала: однакові споруди, але в Пеклі все навпаки (довгі дороги краще, однакові сусіди краще, «погані» vibes пришвидшують ріст). Перемоги нема, поразка — борг, бунт безробітних ангелів/демонів або загибель Планети.

## Поле і час
- Два квадратні поля-царства: Рай і Пекло; між ними — Карма-площина з Планетою й Карма-порталами. Кожна Карма-споруда тримається «якорями» в царствах; синя колія в царстві — лише тінь справжньої колії в площині.
- Ландшафт: Скелі (Rocks), Річки, Карма-портали — розкладені випадково на старті; новий старт = нова розкладка.
- Споруди й будівлі займають 1×1 … 7×7 клітин; клітини зони долі ростуть у будівлі до 4×4.
- Час real-time з «Tempo»: Divine Intervention — пауза, у якій можна будувати; найшвидший — Demonically Fast. Рік — облікова одиниця: зарплата, утримання, статистика й спроба еволюції кожної споруди — раз на рік.
- Камера: поворот усього царства стрілками пульта, зум +/−, Page Up/Down — між Раєм і Пеклом; кнопки «сплющити» ховають будівлі Раю, Пекла, Карма-споруди чи сітку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Зона долі (7 гріхів / 7 чеснот) | zone | колір: зелений Envy/Contentment · жовтий Avarice/Charity · помаранчевий Gluttony/Temperance · коричневий Sloth/Diligence · синій Pride/Humility · червоний Wrath/Peacefulness · фіолетовий Lust/Chastity | приймає душ лише свого кольору; росте в більші будівлі (до 12 стадій на долю) |
| Генерична зона | zone | ½ ціни, ½ місткості | приймає будь-яку душу; «латка» на час катастрофи |
| Душа (SOUL) | neutral | тенет (HAHA/HOHO/OCRA/OPRA × SUMA/SUSA × ALF/RALF), гріх/чеснота, тимчасова/постійна | входить у Ворота, іде дорогами до своєї долі; не знайшла місця — загублена |
| Ворота | spawner | класи (Пекло): 50 000¢ / 2 000 душ · 5 000K¢ / 200 000 · 50 000K¢ / 2 000K; анти-еволюційні vibes | точка входу; кожна душа приносить Pennies |
| Дорога | conduit | 100¢ за клітину; утримання від трафіку | душі ходять лише нею і ≤ 3 клітини вбік по прямій |
| Карма-станція (якір) | sink | 3 класи; потребує дороги й колії до порталу | забирає душ, що йдуть на реінкарнацію; сіра, доки не підʼєднана |
| Карма-колія | conduit | 500¢ за клітину; іде над скелями, річками, будівлями | звʼязує станцію з порталом; дуже довга — душі «забувають» минуле й стають постійними |
| Карма-портал | sink | місце випадкове | повертає душі на Планету |
| Topia (Utopia / Distopia) | static | vibes ±5…±8 на радіус 5–8 | житло ангелів/демонів; дорога не потрібна (вони літають) |
| Тренувальний центр | spawner | слайдер прийому; AQ/DQ 50–150 | робить зі «своїх» душ ангелів/демонів: дешевше, ніж імпорт, але гірша якість при масовому прийомі |
| Порт | conduit | приклади класів: 1 000 000¢ / 200 000 · 10 000K¢ / 2 000K | переправа через Річку: пара портів на двох берегах; поглинає зайвих робітників |
| Ad Infinitum Siphon | source | стоїть впритул до Скель; більше дотичних скель — експоненційно більше енергії | живить звʼязані дорогою споруди; у Раю анти-, у Пеклі про-еволюційний |
| Банк | static | 1×1 — позика 1 млн¢, 2×2 — 10 млн¢; до 20 банків | одна позика на 100 років; дорога не потрібна |
| Limbo-споруда | container | запас «пива» | рік тримає душ, які інакше загубились; пиво скінчилось — вибухає |
| Особлива будівля (дар) | static | vibes ±10…±18 на той самий радіус; радіус захисту 8–12 | дар TPTB за поріг душ; відганяє «свою» Bad Thing |
| Omnibolge / Love Dome | container | дар за 1 млрд душ у царстві | самодостатній міні-Ад/міні-Рай: без персоналу, завжди збалансований |
| Скеля · Річка | terrain | — | Скеля — джерело Ad Infinitum; Річка — перешкода й провідник Ad Infinitum |
| Ангел / Демон | ally | AQ/DQ; імпортований (оплата дороги) / свій | обслуговують споруди; безробітні йдуть у рейд на інше царство |
| Birds of Paradise / Bats out of Hell | hazard | до 75 років | гуано знижує ефективність (кажани — лише не-Покаранням, Покаранням навпаки підвищують) |
| Heaven Gets the Blues / Hell Freezes Over | hazard | до 75 років | вимикають усе під хмарою/кригою |
| Disco Inferno / Paradise Pair-o-Dice | hazard | — | Диско-демон іде полем і трощить будівлі; кубики вибивають шматки царства |
| Heaven Nose / Hell in a Handbasket | hazard | — | краде клітини одного царства й кидає їх випадково в інше |
| Планета (EMBO) | resource | населення, технологія (15 рівнів: вогонь → «Advanced Golf»), рівні гріхів, тенети | джерело душ; Деміург може купувати «впливових» EMBO |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(zone_tool, cells)` → ЯКЩО `free(cells)` and `has(player, pennies)` → ТО `place(player, fate_zone)`, `currency(-cost)`; генерична — `currency(-cost/2)`.
- КОЛИ `input(zap, cell)` → ТО `set_cell(cell, empty)`; зруйнована клітина колії рве всю приєднану ділянку колії.
- КОЛИ `enter(soul, gate)` → ТО `counter(souls_this_year, +1)`, `custom: «душа шукає зону своєї долі за тенетом (Рай / Пекло / обидва)»`.
- КОЛИ `tick` → ЯКЩО `path_exists(soul, fate_zone)` and `in_range(fate_zone, road, 3)` → ТО `move(soul, dir)`; рух лише по прямій, без діагоналей; від Воріт, портів і Карма-споруд — лише 1 клітина.
- КОЛИ `custom: «SUMA-душа відбула долю»` → ЯКЩО `state(soul, in_hell)` → ТО `custom: «наступна доля — від Envy до Pride (найгірший гріх)»`; у Раю порядок зворотний: від Humility до Contentment.
- КОЛИ `custom: «душа відбула всі долі»` → ЯКЩО `state(soul, RALF)` and `custom: «Карма-станція працює й не повна»` → ТО `teleport(soul, karma_portal)` — повернення на Планету; ЯКЩО `state(soul, ALF)` → ТО `set_state(soul, permanent)` у долі з найвищою вагою (Fate Weights).
- КОЛИ `custom: «душа не знайшла вільного місця своєї долі»` → ТО `counter(lost_souls, +1)`, `custom: «кольоровий шпиль над царством; штраф у бюджеті»`.
- КОЛИ `tick` → ЯКЩО `not connected(structure, road_network)` → ТО `set_state(structure, cracked)` — сіра й тріснута, не працює; винятки: Topia, банки, особливі будівлі.
- КОЛИ `rng(p)` → ЯКЩО `state(building, abandoned)` → ТО `transform(building, rock)` — протягом ~100 років.
- КОЛИ `tick` → ЯКЩО `in_range(tile, structure, vibe_radius)` → ТО `custom: «до vibe-рахунку клітини додається ±сила споруди»`; клітини зон долі мають радіус 1 (лише 4 сусіди).
- КОЛИ `custom: «знак vibes»` → ЯКЩО `state(realm, heaven)` → ТО `custom: «+ = про-еволюційні»`; у Пеклі `custom: «− = про-еволюційні»`: Ворота й Карма-якорі гальмують ріст в обох царствах, Topia, центри, порти, дари — пришвидшують.
- КОЛИ `tick` → ЯКЩО `adjacent_count(siphon, rock, >=, 1)` and `connected(building, siphon)` → ТО `set_state(building, empowered)`; без живлення `custom: «будівля росте лише до ½ потенціалу»`; Річка, зʼєднана з сифоном, проводить енергію далі.
- КОЛИ `timer(year)` → ЯКЩО `custom: «заповненість ≥ випадкове 50–100 %»` and `prob(25)` → ТО `custom: «спроба еволюції за ефективністю f»`: висока — `transform(tile, bigger_building)`, низька — `transform(tile, smaller_building)` (деградують лише 1×1, у генеричну).
- Ефективність: `custom: «f = бал дороги (walk distance; у Раю інвертовано) + vibes/4 (−4…+4) + баланс (1–6) + сусідство (0–3)»`; на мапі — оцінка A…F.
- КОЛИ `timer(year)` → ЯКЩО `state(realm, heaven)` and `adjacent_count(tile, other_virtue, >=, 1)` → ТО `counter(adjacency, +3)` за кожного сусіда іншої чесноти, `+1` за ту саму чесноту іншого виду; у Пеклі `+3` — той самий гріх і вид, `+1` — той самий гріх, інший вид; сума ділиться на 2·(розмір+1) і обрізається до 0–3.
- КОЛИ `input(balance_slider, tile)` → ТО `set_value(tile, production_vs_rnd)`; найкраще — дзеркало частки тимчасових/постійних душ (баланс 1–6).
- КОЛИ `input(lock, tile)` → ТО `set_state(tile, locked)` — не росте й не деградує; щороку `currency(-fee)`.
- КОЛИ `custom: «населення царства змінилось»` → ТО `custom: «множник місткості клітин: 5 % (< 10 000 душ) … 500 % (≥ 1 млрд)»`.
- КОЛИ `timer(year)` → ТО `currency(+souls_this_year × soul_rate)`; SOUL Rate падає, якщо середня заселеність відстає від очікуваної кривої.
- КОЛИ `timer(year)` → ТО `currency(-upkeep)`: робітники, дороги, замкнені клітини, загублені душі, позики; дорога коштує `custom: «4^⌊log10 W⌋, W — душ пройшло за рік»`.
- КОЛИ `timer(year)` → ТО `custom: «тренувальний центр бере частку душ за слайдером; 50 % прийому → AQ/DQ ≈ 100»`, `spawn(worker)`.
- КОЛИ `counter(idle_workers, >, n)` → ТО `custom: «рейд на протилежне царство: ореоли над будівлями, руйнування»`; невиправно — `lose` (Ragnarok n' Roll).
- КОЛИ `input(balance, bank)` → ТО `currency(+loan)`; Рай: відсоток 0,1 % за першу позику +0,1 % за кожну наступну, списується щороку; Пекло: 0 %, але вся сума за 100 років, інакше `custom: «(Amt + Amt/(10·NL)) / SR знімається з доходу»`.
- КОЛИ `counter(pennies, <, 0)` → ЯКЩО `custom: «глибокий борг ~50 років»` → ТО `lose` (Four Surfers of the Apocalypso).
- КОЛИ `custom: «ядерна війна або астероїд знищили EMBO»` → ТО `lose`.
- КОЛИ `rng(p)` → ЯКЩО `counter(souls, >=, difficulty_threshold)` and `not in_range(cell, special_building, r)` → ТО `spawn_at(bad_thing, random)`; або вручну з меню Global.
- КОЛИ `input(bad_things_off)` → ТО `custom: «SOUL Rate ×½»`.
- КОЛИ `counter(souls_in_realm, >=, 50000)` → ТО `give(player, special_building)`, `message(gift)`; далі 500 000, 5 млн, 50 млн, 500 млн; за 1 млрд — Omnibolge/Love Dome.
- КОЛИ `counter(limbo_beer, ==, 0)` → ТО `disappear(limbo)`, `custom: «розгублені душі висипаються на дороги»`.
- КОЛИ `input(influence, sector, pennies)` → ТО `custom: «впливовий винахідник / художник / політик зсуває технологію / гріх / тенет у секторі Планети»`; більше Lust → бум населення на століття; висока технологія → ризик ядерної війни.
- КОЛИ `input(type, "$@!")` → ТО `currency(+10000000)` (до 5 разів).
- Перемога: нема (мета — своя: рік, технологія, Love Dome) · Поразка: борг, бунт, загибель Планети · Рахунок: SOUL Rate, «Spiffiness» з 12 рівнями від Ultra Dork до Project Leader.

## Керування і ввід
- Миша: інструмент на пульті (Remote Control) → клік/протягування по сітці; Zap — гумка; Microview — клік по клітині для довідки й балансу.
- Клавіатура: стрілки — прокрутка, +/− — зум, Page Up/Down — Рай ↔ Пекло; набір чит-рядків.
- Типовий ритм: поставити Tempo на Divine Intervention → розмітити / сплющити будівлі й перевірити клітини → відпустити час.

## Вікна, меню, HUD
- `game-screen`: царство + пульт зліва: рік, Pennies, обраний інструмент і ціна, стовпчики ваг доль (Fate Weights), палітра 7 кольорів + генерична, кнопки споруд (дороги, ворота, центри, Topia, Карма-станції й колія, порти, сифони/банки, Limbo, дари, Omnibolge/Love Dome, Zap), кнопки вікон, перемикачі «сплющити», статус: населення загробного світу, загублені душі, населення Планети, SOUL Rate.
- `+window:query-window` (Microview): View · Description · Status (заповненість, персонал, баланс, різноманіття, walk distance, ефективність, живлення, vibes, дорога) · Balance (слайдер, замок; на банку — позика; на центрі — прийом; на воротах/портах — апгрейд) · Close-up.
- Soulview: одна душа — портрет, за що карається/нагороджується, скільки лишилось, віра, біографія, «стежити» за її шляхом.
- `+window:graphs-window` (Graphview): тенети, населення vs житло за долями, заповненість споруд, історія (25 / 500 / 10 000 років), праця (зайняті/безробітні, імпорт, AQ/DQ), бюджет.
- `map-window` (Mapview): тимчасові/постійні, ефективність A–F, vibes, місткість, зонування, трафік, Карма-споруди, заряд Ad Infinitum.
- Planetview: мапи населення, технології, гріхів, тенетів + слайдер «впливу» в Pennies.
- MacroManager: баланс усіх клітин однієї долі, AutoBalance, масовий замок; ціна внизу.
- `+window:advisor-window`: Aria (ангел) і Jasper (демон) — до 5 порад; меню Tutorials → `tutorial-window`.
- `difficulty-select` на старті (Easy / Medium / Hard); меню Global: Bad Things (вимкнути / викликати), AutoScroll; `level-select` сценаріїв.
- HUD-сигнал втрат: `+ui:loss-spikes` — кольорові шпилі над царством за кольором долі, що губить душі.

## Фічі поза полем
- `difficulty-presets`: стартові 9 999 999 / 6 666 666 / 3 333 333 Pennies; поріг появи Bad Things (Easy — після 50 000 душ, Hard — одразу всі чотири перші); кількість великих скупчень Скель.
- `pause` (Divine Intervention) і `speed-control` (Tempo); `tutorial` від радників.
- Сценарії: Dante's (?) (красиве, але неефективне концентричне Пекло), Dusk of the Demiurges (надлишок робітників), 2 Evil 2 Live (лавина душ після катастроф), Splitsville (пусте півцарства за Річкою).
- `+feature:disaster-toggle` з ціною (SOUL Rate ×½); `+feature:loans`; чити й секретний «Diversity Bonus» (7×7 блок з усіх гріхів у Пеклі).

## Варіації й родичі
- Родичі в корпусі: `simcity-1989` (зони, що ростуть самі, бюджет, катастрофи), `theme-hospital` і `two-point-hospital` (потік відвідувачів через кімнати), `populous` (божество і планета), `islanders` / `civ6-districts` (очки за сусідство), `prison-architect-rooms`.
- Осі варіацій:
  - **поле:** одне / два дзеркальні з інвертованими знаками (Afterlife) / шари;
  - **вплив споруди:** радіус-аура зі знаком (vibes) · дифузія поля (SimCity) · лише 4 сусіди;
  - **сусідство:** різне краще (Рай) / однакове краще (Пекло);
  - **маршрут:** коротший краще / довший краще — та сама метрика з різним знаком.

## Цікавинки для курсу
- Два дзеркальні поля з однаковими спорудами й інвертованими знаками оцінок — 📎 (одна функція, параметр «царство»).
- Vibes: сума аур із радіусом і знаком над сіткою, що гальмує або пришвидшує ріст — 🥉.
- Ефективність клітини як сума 4 балів → оцінка A–F — 🥉.
- Маршрут душі: Ворота → дорога → ≤ 3 клітини по прямій → зона свого кольору, SUMA-порядок доль — 🥇 (пошук шляху з обмеженням і чергою цілей).
- Тенети як комбінаторика 4 × 2 × 2 = 16 вірувань, що визначають маршрут — 📎.
- Річний цикл: дохід за душі × SOUL Rate, утримання дороги 4^⌊log W⌋, дві схеми позик — 🥉.
- Bad Things і будівлі-«ліки» з радіусом захисту, привʼязані до 5 чуттів — 📎.

## Мапа на каталог
- Є: `cell-click` · `multi-cell-size` (споруди до 7×7) · `coverage-area` (vibes і радіус захисту дарів) · `connectivity-check` (дороги, колія до порталу) · `round-currency` (Pennies) · `cell-transform` (еволюція, покинуте → скеля) · `spawn-random-cell` (Bad Things) · `difficulty-levels` · `game-pause` · `save-game` · `map-window` · `tutorial-window` · `cheat-codes` · `level-select` (сценарії).
- **Нема** → пропозиції карток:
  - `+realm-mirror` «Два поля з інвертованими правилами» · game-logic · 📎.
  - `+zone-evolution` «Клітина росте стадіями за ефективністю» · entities/state · 🥉 · слоти {stages, threshold}.
  - `+vibes-aura` «Аура ± з радіусом над сіткою» · game-logic · 🥉 · слоти {strength, radius, sign}.
  - `+adjacency-score` «Очки за типи сусідів» · game-logic/score · 📎.
  - `+walk-distance-score` «Оцінка за довжиною шляху» · game-logic · 📎.
  - `+soul-routing` «Агенти самі йдуть до цілей свого типу» · entities/move · 🥇.
  - `+worker-economy` «Персонал: імпорт vs свій, безробіття → бунт» · game-logic/economy · 🥉.
  - `+balance-slider` «Слайдер балансу клітини» · interface/input · 🌱.
  - `+lock-growth` «Замкнути стадію клітини за плату» · game-logic · 🌱.
  - `+bank-loan` «Позика з терміном» · game-logic/economy · 📎.
  - `+disasters` · `+disaster-protection-radius` «Будівля-щит від своєї катастрофи» · entities/spawn · 📎.
  - `+population-milestone-reward` «Дар за поріг населення» · game-logic · 🌱.
  - `+planet-influence` «Купити вплив на джерело агентів» · game-logic · 📎.
  - `+overflow-buffer` «Буфер переповнення, що вибухає» · entities/state · 🌱.

## Пропозиції до словників
- `+cond:field` — значення поля над сіткою в клітині (vibes, заряд) порівняно з порогом.
- `+card:vibes-aura`, `+card:zone-evolution` — див. вище.
- `+window:advisor-window` — радники з порадами за темами (Aria/Jasper).
- `+window:graphs-window` — набір графіків міста/світу (населення, бюджет, історія).
- `+window:query-window` — довідка й дії по одній клітині (Microview, query в SimCity).
- `+feature:disaster-toggle` — вимкнути катастрофи (тут — з ціною).
- `+feature:loans` — позики з терміном, відсотком і штрафом.
- `+ui:loss-spikes` — сигнал втрат над полем кольором причини.

## Джерела
- ⭐ [Wikipedia: Afterlife (video game)](https://en.wikipedia.org/wiki/Afterlife_(video_game)) — Деміург, EMBO, 7+7 доль, генеричні зони, тенети, вплив, технологія, vibes, робітники й Topia, Micro/MacroManager, Bad Things, умови поразки, Death Star за чити.
- [Afterlife Official Player's Guide (Jo Ashburn, 1996), archive.org](https://archive.org/details/afterlife-official-players-guide-jo-ashburn) — пульт і кожна кнопка, тенети, ворота/порти з цінами, дороги 100¢ і правило 3 клітин, колія 500¢, сифони, банки й формула штрафу, Bad Things і дари з радіусами, складність, сценарії, інвентар будівель з vibes і розмірами, додаток з формулами ефективності, сусідства, місткості, утримання доріг і Spiffiness.
- YouTube: пошук «Afterlife 1996 LucasArts gameplay».

## Непевне
- (?) Як саме клітини блоку зливаються у будівлі 2×2…4×4 — гайд каже «еволюціонують», додаток дає розміри й шанс 25 %, механіки злиття не описано.
- (?) Перший сценарій — назва в OCR зіпсована («Dante's …»); чи це вибір зі списку на старті чи пункт меню File.
- (?) Класи раївських воріт і карма-станцій — ціни в OCR нечитабельні; наведено пекельні.
- (?) Платформа Mac — з власних знань; DOS/Windows підтверджують назви образів на archive.org.
- (?) Death Star за надмірні чити — лише Wikipedia; гайд каже «не більше 5 разів».
- (?) Поріг безробіття для рейдів: гайд радить ~30 % імпортних робітників як безпечний рівень, точного порогу нема.
