---
title: Prison Architect — шар кімнат і зон
slug: prison-architect-rooms
family: build-sim
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: score
year: 2015
platforms: [PC, macOS, Linux, PS4, Xbox One, Switch, iPad, Android]
links:
  - {kind: fandom, url: "https://prisonarchitect.paradoxwikis.com/Rooms", best: true, note: "офіційна вікі: усі типи кімнат із мінімальним розміром і обовʼязковими обʼєктами"}
  - {kind: fandom, url: "https://prisonarchitect.paradoxwikis.com/Regime", note: "розклад по годинах: Sleep, Lockup, Eat, Shower, Yard, Free Time, Work"}
  - {kind: fandom, url: "https://prisonarchitect.paradoxwikis.com/Sector", note: "сектор = область, замкнена стінами й дверима; рівні доступу"}
  - {kind: fandom, url: "https://prisonarchitect.paradoxwikis.com/Deployment", note: "рівні безпеки секторів, пости й патрулі охорони, розмітка підлоги"}
  - {kind: fandom, url: "https://prisonarchitect.paradoxwikis.com/Utilities", note: "електрика й вода, кабелі/труби, з'єднання обʼєктів (серво, камери, логіка)"}
  - {kind: fandom, url: "https://prisonarchitect.paradoxwikis.com/Doors", note: "типи дверей, режими Locked Open/Normal/Locked Shut, локдаун"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Prison_Architect"}
  - {kind: steam, url: "https://store.steampowered.com/app/233450/Prison_Architect/"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=prison+architect+beginner+guide+rooms+regime", note: "пошук; гайди для початківців"}
stage: v1
coverage: 65
mechanics: [multi-cell-size, impassable-cells, cell-click, drag-drop-piece, hover-highlight, key-and-door, round-currency, game-pause, save-game, game-loop, state-as-data, field-scaling, minimap-radar, status-panel, +room-requirements, +zone-paint, +sector-flood-fill, +hourly-schedule, +fluid-network, +coverage-area, +drag-build-line, +entity-rotate, +door-access-rules, +wire-link, +job-queue, +room-grading]
proposes: ["+trigger:schedule", "+trigger:input", "+trigger:counter", "+trigger:after", "+cond:fits", "+cond:has", "+cond:connected", "+cond:count", "+cond:state", "+cond:free", "+effect:place", "+effect:set_cell", "+effect:set_state", "+effect:move", "+effect:message", "+effect:currency", "+role:zone", "+role:source", "+role:sink", "+role:conduit", "+role:gate", "+role:switch", "+role:neutral", "+ui:tool-palette", "+ui:conflict-highlight", "+ui:tooltip", "+ui:timer-elapsed", "+window:schedule-window", "+window:stats-window", "+feature:speed-control", "+feature:mode-sandbox", "+feature:level-sharing", "+axis:control", "+card:room-requirements"]
author: opus
date: 2026-11-02
---

# Prison Architect (кімнати) — кімната = прямокутник клітин із вимогами, а розклад гонить людей між кімнатами

## Суть
Описано **лише просторовий шар** Prison Architect: гравець малює фундаменти (стіни + підлога + дах), ставить двері, позначає прямокутники клітин як кімнати певного типу (камера, їдальня, двір, душ, кухня…), кожен тип вимагає мінімального розміру, замкненості/даху та обовʼязкових обʼєктів. Окремо — сектори доступу (замкнені області з рівнем безпеки), комунікації під підлогою (кабелі, труби) і погодинний розклад, що визначає, в яку кімнату мусять іти вʼязні. Люди не керуються: гравець будує середовище, а агенти (вʼязні, охорона, робітники) живуть у ньому. Потреби вʼязнів, бунти, бандити, сюжет — лише як наслідки, поза детальним описом.

## Поле і час
- Квадратна сітка зверху; розмір мапи обирається при створенні (?); межа ділянки — спочатку стіни-паркан і дорога з доставкою.
- **Шари клітини**: ґрунт/матеріал підлоги (трава, бетон, плитка…) · фундамент (indoor = під дахом) · стіна/двері (займає клітину) · обʼєкти 1×1…3×3 (ліжко, унітаз, плита, стіл…) · комунікації (кабель, велика/мала труба — видно у режимі Utilities) · позначка кімнати (оверлей) · сектор/рівень безпеки (оверлей Deployment) · розмітка підлоги.
- Real-time з годинником доби (години й дні), пауза й 3 швидкості (?). Розклад діє погодинно.
- Будівництво не миттєве: план (привид) → робітники несуть матеріали з доставки → будують.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фундамент | terrain | прямокутник W×H, матеріал стіни | drag → по периметру стіни, всередині підлога під дахом (indoors) |
| Стіна (цегла, бетон, паркан, периметр) | static | матеріал, міцність | непрохідна; разом із дверима замикає сектор |
| Двері / ґрати / ворота | gate | тип, режим (Locked Open / Normal / Locked Shut) | хто відчиняє — за типом (див. нижче); локдаун зачиняє все |
| Jail Door | gate | — | відмикають охоронці; дверi камер — автоматично за розкладом |
| Staff Door | gate | — | як Jail Door, але відчиняє будь-який персонал |
| Remote Door + Servo | gate | звʼязок із пультом | відчиняється з Door Control System або гравцем |
| Кімната (позначка) | zone | тип, прямокутник, мін. розмір, вимоги | валідна, коли виконано розмір + обʼєкти + enclosed/indoors |
| Обʼєкт кімнати | object | розмір N×M, поворот, потреба у воді/струмі | задовольняє вимогу кімнати; агенти користуються |
| Сектор | zone | рівень доступу (Unlocked / Min / Med / Max / Protective / SuperMax / Staff Only / Death Row) | область, замкнена стінами й дверима; визначає, хто може ввійти |
| Електростанція + конденсатори | source | потужність | живить мережу кабелів; перевантаження → вимикається |
| Кабель / вимикач | conduit / switch | — | передає живлення; вимикач розриває гілку |
| Насосна станція | source | потребує прямого живлення | гонить воду великими трубами |
| Труба (велика / мала) + вентиль | conduit / switch | — | вода до раковин, унітазів, душів |
| Споживачі (унітаз, душ, плита, двері-серво, камера) | sink | вода/струм | без ресурсу не працюють (?) |
| Вʼязень | neutral | категорія безпеки, потреби | іде в кімнату, яку диктує розклад; у незахищеному секторі тікає |
| Охоронець | ally | пост/патруль | відмикає двері, ескортує; стоїть на посту сектора |
| Робітник (Workman) | ally | — | носить матеріали, будує за чергою |
| Пост / маршрут патруля | zone | — | малюється в Deployment, охоронець стоїть/ходить |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, foundation)` → ЯКЩО `currency ≥ cost` → ТО `place(blueprint)`; робітники: `custom: «доставка матеріалів → побудова стін по периметру, підлоги й даху всередині»`.
- КОЛИ `input(drag, room_type, rect)` → ТО `set_state(cells, room=type)` (безкоштовно); ПЕРЕВІРКА: ЯКЩО `fits(rect, min_size)` і `has(rect, required_objects)` і (`enclosed` / `indoors` / `outdoors` за типом) → кімната діє; інакше значок-попередження з переліком нестач.
- Приклади вимог: камера ≥2×3, enclosed, indoors, ліжко + унітаз · двір ≥5×5, secure · кухня — плита, холодильник, раковина · їдальня — стіл подачі, стіл, лавка · офіс ≥4×4 — стіл, стілець, шафа · каплиця ≥6×6. Зовнішні двері в прямокутник кімнати **не** входять.
- КОЛИ змінено стіну/двері/фундамент → ТО `custom: «перерахувати сектори: flood fill областей, замкнених стінами й дверима; область без дверей → No Access, без стін → Unsecured»`.
- КОЛИ `enter(prisoner, sector)` → ЯКЩО рівень сектора не дозволяє його категорію → ТО `block` (обходить; під ескортом — проходить).
- КОЛИ `state(prisoner, in_unsecured_sector)` → ТО `custom: «одразу пробує втекти»`.
- КОЛИ `schedule(hour → activity)` → ТО для категорії: Sleep/Lockup → двері камер замкнені, вʼязні в камерах; Eat → `move` до їдальні; Shower → до найближчого душу; Yard → можна у двір; Work → на роботу (кухня, пральня, майстерня); Free Time → куди хочуть.
- КОЛИ `schedule(eat - 4h)` → ТО кухарі починають готувати; без Eat у розкладі їжі нема.
- КОЛИ `contact(person, door)` → ЯКЩО тип дверей дозволяє цю роль (або Locked Open) → ТО прохід; Jail Door — `custom: «чекати охоронця»`; локдаун → `set_state(all_doors, closed)`.
- КОЛИ `counter(power_load, >, capacity)` → ТО `set_state(power_station, off)` — уся мережа без струму; насос без прямого живлення → `set_state(water, off)`.
- КОЛИ `input(connect, a, b)` → ТО `custom: «лінк source→target (пульт→серво, монітор→камера, вимикач→лампа); порядок кліків визначає, хто керує»`.
- Перемоги нема (пісочниця); рахунок — бюджет (дотації за кількість вʼязнів і гранти), оцінка вʼязниці (рецидивізм, щастя, насильство). Поразка — звільнення CEO за погану оцінку (?) або банкрутство.

## Керування і ввід
- Курсор + drag-прямокутник: фундамент, кімната, підлога, видалення; drag-лінія: стіни, кабелі, труби, маршрути патрулів, розмітка підлоги.
- Клік: поставити обʼєкт (поворот перед установкою), двері (по стіні), вибрати агента/двері (режим дверей).
- Права кнопка + drag — зняти позначку кімнати/маршрут/розмітку.
- Режими-шари перемикаються вкладками нижньої панелі: Foundations · Materials · Objects · Rooms · Utilities · Staff · Deployment · Logistics · Planning · Reports.

## Вікна, меню, HUD
- `main-menu`: Story/Prison Story, New Prison (налаштування мапи й правил), Load, Escape Mode, World of Wardens (обмін вʼязницями), Settings.
- `game-screen`: поле зверху, нижня `tool-palette` з вкладками шарів, верхня панель — гроші, час доби (`timer-elapsed`), кількість вʼязнів/персоналу, швидкість.
- Оверлеї на полі: назва кімнати, значок нестачі (`conflict-highlight` + `tooltip` «треба: унітаз»), кольори секторів, комунікації.
- Reports: Regime (`schedule-window` — сітка 24 год × категорія безпеки), Bureaucracy (дерево досліджень → відкриває Deployment, Regime, Prison Labour), Finance, Grants, Policy, Needs (`stats-window`), Prison Grading.
- Deployment (`custom-window` поверх поля): сектори × рівні, пости, патрулі, розклад деплоїв по годинах.
- Logistics (`custom-window`): привʼязка кімнат одна до одної (яка кухня обслуговує яку їдальню, який склад приймає доставку).
- Переходи: main-menu → New Prison → game-screen; game-screen ↔ Reports/Deployment/Logistics (немодальні).

## Фічі поза полем
- `speed-control`, `pause`, `save-slots`, `mode-sandbox` (безкоштовне будівництво/туман вимкнено як опції створення (?)), `level-sharing` через World of Wardens / Steam Workshop.
- Дослідження Bureaucracy як дерево розблокування інструментів (`meta-progression` у межах гри).
- Escape Mode — та сама вʼязниця, тепер ти вʼязень (`avatar`-режим).
- Planning — інструмент «малювати план» кольором без витрат.

## Варіації й родичі
- Prison Architect 2 (2025?, 3D, поверхи), Two Point Hospital (кімнати з обовʼязковими обʼєктами), Theme Hospital, RimWorld (кімнати за стінами + якість), Dwarf Fortress (зони з меблів), Oxygen Not Included (кімнати з вимогами й газові/рідинні мережі), Rimworld/ONI — найближчі родичі «кімнати як предикат».
- **Осі варіацій**: кімната задається явною позначкою (PA, Two Point) / автоматично flood fill стін (RimWorld, ONI) · вимоги: розмір / обʼєкти / замкненість / дах · доступ: за сектором / за дверима / за роллю агента · комунікації: окремий шар під клітиною / обʼєкти на клітині.

## Цікавинки для курсу
- Валідація кімнати: прямокутник ≥ мін. розміру + набір обовʼязкових обʼєктів + enclosed/indoors → список нестач — 🥉 (предикат над регіоном, дані з таблиці).
- Сектори як flood fill від стін і дверей, з особливими станами «немає дверей» / «не замкнено» — 🥉.
- Двері з таблицею доступу (тип дверей × роль агента × режим) — 📎 (`key-and-door` узагальнено).
- Погодинний розклад: категорія × година → активність → цільова кімната; агенти переходять при зміні години — 🥈 (планувальник + пошук шляху).
- Мережі струму й води: звʼязність від джерела, ліміт потужності, вимикачі — 🥈 (з `+fluid-network`).
- Черга робіт для робітників: план → доставка → будівництво — 🥈.
- Лінки «пульт → двері/камери» з напрямком керування — 📎.

## Мапа на каталог
- Є: `multi-cell-size` (обʼєкти й фундаменти N×M) · `impassable-cells` (стіни) · `cell-click` · `drag-drop-piece` · `hover-highlight` · `key-and-door` (двері за ролями) · `round-currency` · `game-pause` · `save-game` · `game-loop` · `state-as-data` · `field-scaling` · `minimap-radar` (?) · `status-panel`.
- **Нема** → пропозиції карток:
  - `+room-requirements` «Кімната = регіон із вимогами» · game-logic/constraints · 🥉 · слоти {min_size, required_objects, enclosed, indoors} — Two Point, ONI, RimWorld.
  - `+zone-paint` «Розфарбувати клітини як зону/кімнату» · interface/input · 🌱 — drag-прямокутник позначки.
  - `+sector-flood-fill` «Області, замкнені стінами й дверима» · game-logic · 🥉.
  - `+hourly-schedule` «Розклад за годинами для груп агентів» · game-logic · 🥈 · слоти {groups, activities}.
  - `+door-access-rules` «Таблиця доступу дверей за роллю» · entities/interact · 📎 — дитина `key-and-door`.
  - `+wire-link` «Логічне зʼєднання обʼєктів» · entities/interact · 📎 (пульт→серво; також Terraria-дроти).
  - `+job-queue` «Черга робіт для агентів-будівельників» · game-logic · 🥈 (RimWorld, DF, ONI).
  - `+room-grading` «Оцінка якості кімнати за обʼєктами» · game-logic/score · 📎.
  - `+fluid-network` (Factorio) — труби й кабелі; `+coverage-area` (камера CCTV, зона поста); `+drag-build-line`; `+entity-rotate` — повторно.

## Пропозиції до словників
- `+trigger:schedule` (година розкладу), `+trigger:input`, `+trigger:counter` (навантаження мережі), `+trigger:after` (перерахунок секторів після зміни стін).
- `+cond:fits` (прямокутник ≥ мін. розміру), `+cond:has` (у кімнаті є обʼєкт), `+cond:connected` (споживач у мережі з джерелом / сектор замкнений), `+cond:count`, `+cond:state`, `+cond:free`.
- `+effect:place`, `+effect:set_cell` (фундамент/підлога), `+effect:set_state` (кімната, двері, живлення), `+effect:move`, `+effect:message`, `+effect:currency`.
- `+role:zone` (кімната, сектор, пост), `+role:source`/`+role:sink`/`+role:conduit` (мережі), `+role:gate`, `+role:switch`, `+role:neutral` (вʼязні як агенти з власною волею).
- `+ui:tool-palette`, `+ui:conflict-highlight` (кімната з нестачами), `+ui:tooltip` (перелік вимог), `+ui:timer-elapsed` (годинник доби).
- Новий `+window:schedule-window` — сітка розкладу «година × група»; `+window:stats-window` (потреби, оцінка); Deployment і Logistics — поки `custom-window`.
- `+feature:speed-control`, `+feature:mode-sandbox`, `+feature:level-sharing`.
- `+axis:control` = `indirect` (агентами не керують).
- `+card:room-requirements` — див. вище.

## Джерела
- ⭐ [Prison Architect Wiki: Rooms](https://prisonarchitect.paradoxwikis.com/Rooms) — таблиця всіх кімнат із мін. розміром і обовʼязковими обʼєктами, загальні правила позначення.
- [Regime](https://prisonarchitect.paradoxwikis.com/Regime) — активності розкладу та винятки.
- [Sector](https://prisonarchitect.paradoxwikis.com/Sector) — визначення сектора, No Access / Unsecured.
- [Deployment](https://prisonarchitect.paradoxwikis.com/Deployment) — 9 рівнів безпеки, пости, патрулі, розмітка підлоги.
- [Utilities](https://prisonarchitect.paradoxwikis.com/Utilities) — електрика, вода, зʼєднання обʼєктів.
- [Doors](https://prisonarchitect.paradoxwikis.com/Doors) — типи дверей і локдаун.
- [Wikipedia](https://en.wikipedia.org/wiki/Prison_Architect) — історія, платформи, режим втечі, оцінка вʼязниці.
- [Steam](https://store.steampowered.com/app/233450/Prison_Architect/).

## Непевне
- (?) Розміри мапи, кількість швидкостей, наявність мінімапи — з памʼяті.
- (?) Чи проходять кабелі/труби «під» стінами й обʼєктами — вікі Utilities цього не каже; у грі вони в окремому шарі перегляду.
- (?) Що саме ламається без води/струму (двері-серво, камери — так; унітази — без води не працюють) — деталі не перевірено.
- (?) Поразка «звільнення CEO» — з Wikipedia про оцінювання; чи це кінець гри в пісочниці — залежить від режиму.
- (?) Рік і формат Prison Architect 2 — лише видно в Steam-пошуку, деталей не читав.
