---
title: Theme Hospital
slug: theme-hospital
aka: [CorsixTH, Тема лікарні]
family: build-sim
also: []
klass: cursor
axes:
  field: iso
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: constraints
year: 1997
platforms: [PC, PlayStation]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Theme_Hospital", best: true, note: "кімнати з креслення, коридорні обʼєкти, персонал, діагноз → лікування, події, цілі рівнів, CorsixTH"}
  - {kind: other, url: "https://github.com/CorsixTH/CorsixTH/wiki/Room-List", note: "CorsixTH wiki: усі кімнати — ціна, мін. розмір, обовʼязкові обʼєкти"}
  - {kind: other, url: "https://github.com/CorsixTH/CorsixTH/wiki/Heating", note: "CorsixTH wiki: тепло по тайлах, батареї, стіни ослаблюють, комфорт 11–18 °C"}
  - {kind: other, url: "https://github.com/CorsixTH/CorsixTH", note: "відкритий рушій (MIT), редактор мап"}
  - {kind: other, url: "https://github.com/CorsixTH/CorsixTH/wiki", note: "CorsixTH wiki: хвороби, епідемії, дослідження, кінцеві умови"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Theme+Hospital", note: "пошук"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Theme+Hospital+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [multi-cell-size, impassable-cells, cell-click, drag-drop-piece, hover-highlight, chase-bfs, round-currency, game-pause, save-game, save-multi-slot, objective-text, status-panel, sequential-levels, level-unlock, in-game-editor, conflict-highlight, spawn-schedule, time-out, +room-requirements, +room-blueprint, +heat-diffusion, +agent-needs, +queue-line, +breakdown-repair, +job-queue, +entity-rotate, +tech-tree, +diagnosis-pipeline, +machine-wear]
proposes: ["+card:room-blueprint", "+card:heat-diffusion", "+card:diagnosis-pipeline", "+card:machine-wear", "+card:room-requirements", "+cond:enclosed", "+effect:diffuse", "+effect:queue_join", "+role:visitor", "+ui:thought-bubble", "+ui:heat-overlay", "+window:town-map", "+window:research-window", "+window:finance-window", "+window:staff-hire", "+feature:year-end-awards"]
author: opus
date: 2026-11-09
---

# Theme Hospital — кімната як прямокутне креслення мінімального розміру з обовʼязковими предметами, а пацієнти течуть чергами від діагнозу до лікування

## Суть
Гравець будує лікарню в порожній будівлі: малює креслення кімнат (прямокутник ≥ мінімуму), ставить двері й вікна, потім обовʼязкові та додаткові предмети; у коридорах — лави, батареї, рослини, вогнегасники. Наймає лікарів, медсестер, прибиральників, реєстраторів; пацієнти з комічними хворобами проходять **конвеєр**: реєстратура → кабінет терапевта (GP) → діагностичні кімнати → кімната лікування. Механіка клітин — **предикат кімнати** (розмір + предмети) і **тепло, що розтікається тайлами** від батарей і слабшає крізь стіни. Ціль рівня — пороги грошей, репутації, вилікуваних і вартості лікарні.

## Поле і час
- Ізометрична квадратна сітка всередині заданої будівлі; ділянки-корпуси купуються (?); поза будівлею — вулиця.
- Шари тайла: підлога · стіна/двері/вікно на ребрі тайла (?) · предмет N×M з поворотом · позначка кімнати (креслення) · **тепло** (число на тайлі) · сміття/блювота.
- Real-time, календар місяцями; кінець року — огляд і нагороди. Пауза, швидкості (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кімната (креслення) | zone | тип, прямокутник ≥ мін. (4×4 / 5×5 / 6×6), двері, вікна | діє, коли поставлено двері й обовʼязкові предмети; приймає чергу |
| Двері / вікно | gate | — | вхід у кімнату; вікно — світло й вигляд (?) |
| Предмет кімнати (стіл, шафа, ліжко, сканер, рентген, душ, «Inflator»…) | object | розмір, поворот, ціна | обовʼязковий для типу кімнати; машини мають міцність |
| Машина | object | міцність (strength), лічильник використань | зношується; без обслуговування вибухає і вбиває всіх у кімнаті |
| Коридорний обʼєкт (лава, рослина, вогнегасник, урна, автомат) | object | — | лави — сидіти в черзі; рослини — настрій, треба поливати (?) |
| Батарея | source | температура (12,5–27,5 °C на всю лікарню) | тайл тягнеться до вищої з температур батареї й повітря |
| Тайл тепла | terrain | heat | змішується з середнім сусідів; через стіну/предмет — ¼ впливу |
| Пацієнт | neutral | хвороба, гроші, щастя, температура, певність діагнозу, здоровʼя | реєстратура → GP → діагностика → лікування; іде геть, якщо чекає довго/нещасний (?) |
| Лікар | ally | навичка, спеціалізація (хірург, психіатр, дослідник), втома | працює в кімнаті; спеціалізації потрібні для деяких кімнат |
| Медсестра | ally | — | працює в палаті, аптеці (?) |
| Прибиральник (handyman) | ally | пріоритети: чистити / поливати / ремонт | ремонтує машини, прибирає сміття й блювоту |
| Реєстратор | ally | — | без реєстратури пацієнти не потрапляють у чергу |
| Щури | enemy | — | зʼявляються в брудній лікарні; гравець відстрілює кліком |
| VIP, інспектор | neutral | — | VIP оцінює і нагороджує; інспектор шукає приховану епідемію |
| Сміття / блювота | hazard | — | знижує чистоту й настрій |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag_room, type, rect)` → ЯКЩО `fits(rect, min_size)` and `free(rect)` → ТО `place(blueprint)`; інакше червоне креслення і `block`.
- КОЛИ `input(place, door|window, wall_tile)` → ТО `place(door)`; без дверей кімнату не підтвердити (?).
- КОЛИ `input(confirm_room)` → ЯКЩО `has(room, required_objects)` (GP: стіл, шафа, стілець; Ward: стіл, ліжко; Operating Theatre: X-ray Viewer, операційний стіл, раковина, ширма; Toilets: унітаз, раковина…) → ТО `set_state(room, open)`, `currency(-cost)`; інакше `custom: «перелік нестач»`.
- КОЛИ `input(place, object)` → ЯКЩО `fits(object, cells)` and `custom: «біля предмета лишився прохід для використання»` → ТО `place(object)`; `rotate(object, 90)` перед установкою.
- КОЛИ `spawned(patient)` → ТО `custom: «іде до реєстратури»`; без реєстратора — `custom: «чекає / іде геть»`.
- КОЛИ `custom: «пацієнт у GP»` → ТО `custom: «певність діагнозу +n»`; ЯКЩО `counter(certainty, <, policy)` → ТО `custom: «направлення в діагностичну кімнату»`; інакше → кімната лікування.
- КОЛИ `custom: «потрібна кімната ще не побудована / не досліджена»` → ТО `custom: «пацієнт чекає або йде додому»` (?) — гравець може відправити додому.
- КОЛИ `reach(patient, room)` → ТО `custom: «стати в чергу кімнати»` (`+effect:queue_join`); гравець може переставляти пацієнтів у черзі.
- КОЛИ `custom: «лікування»` → ЯКЩО `prob(cure_chance)` → ТО `currency(+fee)`, `custom: «вилікувано +1»`; інакше `custom: «смерть, −репутація»`.
- КОЛИ `custom: «машину використано»` → ТО `counter(machine.uses, +1)`; ЯКЩО `counter(machine.uses, >=, strength)` → ТО `explode(room, rubble)` — усі в кімнаті гинуть, кімната непридатна.
- КОЛИ `contact(handyman, machine)` → ТО `set_value(machine.uses, 0)` (?); міцність падає з кожним ремонтом (?).
- КОЛИ `timer(several_per_day)` → ТО `custom: «тепло тайла = змішати попереднє з середнім сусідів; сусід крізь стіну/предмет — ¼ ваги; тайл батареї тягнеться до max(батарея, повітря); надворі — температура повітря; усередині — повільна втрата»` (`+effect:diffuse`).
- КОЛИ `timer(day)` → ТО `custom: «температура людини наближається до тепла тайла»`; ЯКЩО `custom: «поза 11–18 °C»` → ТО `custom: «щастя −2 % за кожні 7° поза межею»`; у межах — щастя повільно росте.
- КОЛИ `rng(p)` → ТО `custom: «епідемія»`; гравець може приховати — вилікувати всіх заражених до інспектора; інакше штраф і −репутація.
- КОЛИ `schedule(emergency)` → ТО `spawn_at(patients, entrance)`, `timer(start)`; вилікувати всіх до кінця таймера → бонус.
- КОЛИ `custom: «бруд»` → ТО `spawn_at(rat, wall)`; КОЛИ `input(click, rat)` → ТО `disappear_b`.
- КОЛИ `custom: «візит VIP»` → ТО `custom: «оцінка лікарні → нагорода/репутація»`.
- КОЛИ `input(fund_research, category)` → ТО `custom: «наукові бали → нова кімната / ліки / покращення машин»`; дослідницький відділ потребує лікаря-дослідника.
- КОЛИ `custom: «персонал втомився»` → ЯКЩО `custom: «є кімната відпочинку»` → ТО `custom: «відпочити на дивані»`; нещасні просять підвищення.
- КОЛИ `all_constraints_met` (гроші, репутація, вилікувані, вартість лікарні) → ТО `win` → наступний рівень; КОЛИ `counter(money, <, 0)` (довго (?)) або `custom: «забагато смертей»` → ТО `lose`.
- КОЛИ `timer(year)` → ТО `window(custom: «річний огляд: трофеї, бонуси»)`.

## Керування і ввід
- Миша: нижня панель — Build room (категорії: діагностика, лікування, клініки, сервіс) → drag прямокутника → двері/вікна → предмети з переліку (обовʼязкові відмічені) → Confirm.
- Furnish Corridor — розставити коридорні предмети; Hire Staff — вибрати з кандидатів (навичка, зарплата), потім кинути людину на тайл.
- Клік по людині — вікно з характеристиками; підхопити й перенести працівника; клік по кімнаті — редагування, черга (перетягнути пацієнтів у черзі).
- Клік по щуру — постріл; права кнопка — скасувати (?).

## Вікна, меню, HUD
- `main-menu`: нова кампанія (`difficulty-select` (?)) · завантажити · налаштування · мультиплеєр (патч, до 4).
- `game-screen`: ізометрія + нижня панель (кнопки, гроші, дата, `toast`-повідомлення факсом (?)).
- Вікно кімнати (`custom-window`): стан, черга, персонал.
- Вікно людини: пацієнт — хвороба, певність, термометр (тримати в середній третині), гроші; працівник — навичка, втома, зарплата.
- `+window:town-map` — мапа лікарні: налаштування батарей, `+ui:heat-overlay`, ділянки для купівлі.
- `+window:research-window`, `+window:finance-window` (баланс, кредит), `+window:staff-hire`, Policy (поріг певності діагнозу, у т. ч. >100 %), Status (цілі рівня — `objective-text`), Charts/Statistics (`stats-window`).
- `end-screen` рівня, `+feature:year-end-awards` (річні трофеї).
- HUD-підказки: гримаса «холодно» (синє) / «жарко» (червоне); `conflict-highlight` червоного креслення.

## Фічі поза полем
- `levels-sequential` + `level-unlock` (кампанія), `save-slots`, `pause`, `speed-control` (?).
- Мультиплеєр до 4 гравців (патч): сміттєві бомби, переманювання персоналу.
- CorsixTH: сучасні ОС, високі роздільності, `level-editor`, власні рівні й кампанії; Android (2012).

## Варіації й родичі
- Two Point Hospital (2018) — та сама модель + престиж кімнати від предметів; Theme Park (1994) — попередник Bullfrog; Prison Architect, RimWorld — кімнати як предикат.
- У корпусі: `prison-architect-rooms` (кімната = прямокутник з вимогами, позначка явна), `rimworld-rooms` (кімната = flood fill стін, температура на кімнату), `rollercoaster-tycoon` (агенти з потребами, черги), `oxygen-not-included-cells` (температура на клітину).
- **Осі варіацій «кімната»**: креслення фіксованого прямокутника (Theme Hospital) / позначка на довільній області (Prison Architect) / автоматично з замкнених стін (RimWorld) · **«тепло»**: на тайл з дифузією (Theme Hospital, ONI) / одне на кімнату (RimWorld) / радіус (Frostpunk).

## Цікавинки для курсу
- Креслення кімнати: прямокутник ≥ мін. розміру, без перекриття, двері на периметрі — 🌱.
- Валідація кімнати за таблицею обовʼязкових предметів → список нестач — 📎.
- Дифузія тепла по тайлах з ослабленням через стіни — 🥉 (згортка-усереднення, як Life, але з числом).
- Конвеєр пацієнта: GP → діагностика до порогу певності → лікування — 📎 (автомат станів + черги).
- Машина з лічильником зносу, ремонт і вибух — 🌱.
- Черги кімнат з ручним перевпорядкуванням — 📎.

## Мапа на каталог
- Є: `multi-cell-size` (кімнати й предмети) · `impassable-cells` (стіни) · `cell-click` + `drag-drop-piece` + `hover-highlight` · `chase-bfs` (пацієнт іде до кімнати) · `round-currency` · `conflict-highlight` (червоне креслення) · `spawn-schedule` (надходження пацієнтів, екстрені) · `time-out` (таймер екстреного) · `game-pause` · `save-game` + `save-multi-slot` · `objective-text` + `status-panel` · `sequential-levels` + `level-unlock` · `in-game-editor` (CorsixTH).
- **Нема** → пропозиції карток:
  - `+room-blueprint` «Креслення: прямокутник ≥ мін., потім двері й предмети» · interface/input · 🌱.
  - `+room-requirements` — уже пропоновано (Prison Architect); друга гра.
  - `+heat-diffusion` «Тепло на тайлі змішується з сусідами» · entities/state · 🥉 · слоти {weights, wall_factor, sources}.
  - `+diagnosis-pipeline` «Агент проходить станції, доки параметр не досягне порогу» · game-logic · 📎.
  - `+machine-wear` «Лічильник зносу → поломка/вибух» · entities/state · 🌱.
  - `+agent-needs`, `+queue-line`, `+breakdown-repair`, `+job-queue`, `+entity-rotate`, `+tech-tree` — пропоновані в інших файлах, підтвердження.

## Пропозиції до словників
- `+card:room-blueprint`, `+card:heat-diffusion`, `+card:diagnosis-pipeline`, `+card:machine-wear`, `+card:room-requirements` — див. вище.
- `+cond:enclosed` — область замкнена стінами/дверима (Prison Architect, RimWorld, Theme Hospital).
- `+effect:diffuse` — значення клітини змішується з сусідами (тепло, газ, запах).
- `+effect:queue_join` — стати в кінець черги (RCT, Theme Hospital).
- `+role:visitor` — автономний клієнт з потребами (пацієнт, гість парку).
- `+ui:thought-bubble` — гримаса/думка над агентом; `+ui:heat-overlay` — теплова мапа.
- `+window:town-map`, `+window:research-window`, `+window:finance-window`, `+window:staff-hire`.
- `+feature:year-end-awards` — річний огляд з трофеями/бонусами.

## Джерела
- ⭐ [Wikipedia: Theme Hospital](https://en.wikipedia.org/wiki/Theme_Hospital) — креслення → двері/вікна → предмети, коридорні предмети, персонал, GP і діагностика, політика >100 %, вибух машин, епідемії, VIP, щури, цілі й поразка, мультиплеєр, CorsixTH.
- [CorsixTH wiki: Room List](https://github.com/CorsixTH/CorsixTH/wiki/Room-List) — 23 кімнати: ціна, мін. розмір 4×4/5×5/6×6, обовʼязкові предмети.
- [CorsixTH wiki: Heating](https://github.com/CorsixTH/CorsixTH/wiki/Heating) — алгоритм тепла, ¼ через стіну, батареї 12,5–27,5 °C, комфорт 11–18 °C, −2 % щастя за 7°.
- [CorsixTH на GitHub](https://github.com/CorsixTH/CorsixTH) і [wiki](https://github.com/CorsixTH/CorsixTH/wiki) — рушій, редактор, інші сторінки механік.

## Непевне
- (?) Чи двері обовʼязкові для підтвердження кімнати і чи стіни ставляться на ребро тайла — з памʼяті.
- (?) Як саме відновлюється міцність машини при ремонті й чи падає її максимум — з памʼяті.
- (?) Коли пацієнт іде додому (довге очікування, нещастя, відсутня кімната) — з памʼяті.
- (?) Межа «гроші < 0» як поразка — миттєва чи після періоду; Wikipedia каже лише «negative funds».
- (?) Факс-повідомлення, рослини, що вʼянуть без поливу, швидкості гри — з памʼяті.
