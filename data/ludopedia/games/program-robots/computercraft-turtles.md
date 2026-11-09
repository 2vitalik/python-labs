---
title: ComputerCraft (turtles)
slug: computercraft-turtles
aka: [ComputerCraft, "CC: Tweaked", "CC: Restitched", Turtle, черепаха ComputerCraft]
family: program-robots
also: [build-sim]
klass: avatar
axes:
  field: 3d
  time: programmed
  opponent: none
  info: partial
  random: setup
  goal: none
year: 2011
platforms: [PC (мод Minecraft Java)]
links:
  - {kind: official, url: "https://tweaked.cc/module/turtle.html", best: true, note: "повний API черепахи CC: Tweaked: рух, dig/place/detect/compare/inspect у 3 напрямки, 16 слотів, паливо 20 000 / 100 000"}
  - {kind: wiki, url: "https://fr.wikipedia.org/wiki/ComputerCraft", note: "історія: Dan200, грудень 2011, типи компʼютерів, периферія, CraftOS, CC: Tweaked"}
  - {kind: other, url: "https://github.com/cc-tweaked/CC-Tweaked/tree/mc-1.20.x/projects/core/src/main/resources/data/computercraft/lua/rom/programs/turtle", note: "вбудовані програми черепахи: excavate, tunnel, go, turn, refuel, dance, craft, equip, unequip"}
  - {kind: other, url: "https://raw.githubusercontent.com/cc-tweaked/CC-Tweaked/mc-1.20.x/projects/core/src/main/resources/data/computercraft/lua/rom/programs/turtle/excavate.lua", note: "excavate: змійка шарами, облік позиції, повернення розвантажитись і заправитись"}
  - {kind: other, url: "https://tweaked.cc/module/gps.html", note: "GPS: трилатерація від компʼютерів-хостів через модеми"}
  - {kind: other, url: "https://tweaked.cc/module/rednet.html", note: "rednet: повідомлення між компʼютерами за ID, broadcast, протоколи"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=computercraft+turtle+mining+program", note: "пошук; програми черепах у дії"}
stage: v1
coverage: 60
mechanics: [command-program, user-procedures, sensor-predicates, orientation-state, dig-terrain, item-pickup, inventory, inventory-items, inventory-limit, gravity-fall, code-editor-window, help-window, game-loop, +real-language-code, +relative-moves-3d, +fuel-per-move, +three-direction-sensors, +selected-inventory-slot, +place-from-slot, +tool-upgrade-sides, +failure-as-return-value, +dead-reckoning-position, +return-home-unload, +gps-trilateration, +radio-messaging, +persistent-file-system, +startup-script, +event-wait, +craft-from-inventory, +sandbox-mode, +server-config-unlimited-fuel]
proposes: ["+effect:dig", "+effect:drop", "+effect:refuel", "+effect:select_slot", "+effect:equip", "+effect:craft", "+effect:send", "+trigger:event(name)", "+cond:has_space(slot)", "+window:terminal-shell", "+window:turtle-inventory", "+ui:selected-slot-highlight", "+feature:persistent-filesystem", "+feature:server-config"]
author: opus
date: 2026-11-09
---

# ComputerCraft (turtles) — робот-черепаха у воксельному світі Minecraft, якого ведеш Lua-програмою, а не клавішами

## Суть
ComputerCraft — мод до Minecraft, що додає програмовані компʼютери з Lua; **черепаха** (turtle) — компʼютер на «ногах»: блок, що рухається світом, копає, ставить, підбирає і бʼє лише тоді, коли так написано в програмі. Гравець пише код (вбудований редактор `edit`), запускає його в оболонці CraftOS і дивиться, як черепаха риє шахту, рубає ліс чи будує стіну. Ядро — мізерний сенсорний апарат (лише «попереду / над / під»), паливо як бюджет переміщень, 16 слотів інвентаря і невдача команди як **повернене `false`**, а не виняток. Мети гра не ставить: це пісочниця, де задачу вигадує гравець.

## Поле і час
- Поле — світ Minecraft, тривимірна сітка блоків (`field: 3d`); черепаха займає рівно одну клітину і рухається лише вздовж осей: вперед, назад, вгору, вниз.
- Орієнтація — 4 горизонтальні напрямки; `up`/`down` напрям не змінюють. Повороти — на 90° на місці.
- Шари клітини: блок (твердий / рідина / повітря) + сутності поверх (моби, предмети на землі) + інвентар контейнера всередині блоку (скриня).
- Час: світ Minecraft іде в реальному часі, програма — у співпрограмі (coroutine): кожна дія черепахи займає час і повертає результат після виконання (`time: programmed`). Скільки триває один крок — у «Непевне».
- Видимість: гравець бачить світ, а **програма — лише те, що повідомлять сенсори** в трьох напрямках і `gps.locate`; власну позицію код мусить рахувати сам (`info: partial`). Світ генерується випадково (`random: setup`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Черепаха | player | позиція (x,y,z), напрям, паливо 0…20 000, 16 слотів, вибраний слот, 2 боки для апгрейдів | виконує Lua-програму; рух 1 блок, поворот 90°; дії в 3 напрямки (front/up/down) |
| Розвинена черепаха | player | паливо до 100 000 | те саме, більший бак; розвинені компʼютери — 16 кольорів і миша |
| Твердий блок | object | тип, стан | `detect` → true; копається інструментом; блокує рух |
| Повітря | — | — | вільна клітина: `detect` → false, рух можливий |
| Рідина (вода, лава) | terrain | — | не тверда: `detect` → false; рух можливий (?) |
| Гравій / пісок | object | гравітація | після копання клітини під ним падає в неї — блок «відростає» попереду |
| Предмет на землі | pickup | стек | `suck` забирає в інвентар |
| Контейнер (скриня) | container | слоти | `drop` кладе вибраний стек усередину, `suck` забирає |
| Моб | enemy | HP | блокує рух без `detect` = true; `attack` б'є |
| Паливо (вугілля, відро лави) | resource | енергоємність | `refuel` спалює предмети з вибраного слота |
| Інструмент-апгрейд (кайло, сокира, лопата, меч, мотика) | pickup | бік left/right | визначає, які блоки ламає `dig` і чи бʼє `attack`; ставиться `equipLeft/Right` |
| Модем (апгрейд або периферія) | — (обладнання) | дротовий / бездротовий | канали rednet і GPS |
| Компʼютер / розвинений компʼютер | static | ID, файлова система | нерухомий; запускає програми, може бути GPS-хостом |
| GPS-хост | static | знає свої координати | відповідає на запит `gps.locate` |
| Периферія (монітор, дисковод, принтер, динамік) | static | — | зовнішній екран, дискета для перенесення програм, друк, звук |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `exec(forward|back)` → ЯКЩО `free(front|back)` і `counter(fuel, >, 0)` → ТО `move(turtle, dir)`, `counter(fuel, -1)` (?); інакше `block` + `custom: «повернути false і причину»` — програма не падає.
- КОЛИ `exec(up|down)` → ЯКЩО `free(up|down)` і `counter(fuel, >, 0)` → ТО `move(turtle, up|down)`, `counter(fuel, -1)` (?); напрям не змінюється.
- КОЛИ `exec(turnLeft|turnRight)` → ТО `face(turtle, ±90)`; паливо **не** витрачається.
- КОЛИ `exec(dig[Up|Down])` → ЯКЩО `cell(target, solid)` і `custom: «інструмент на боці може зламати блок»` → ТО `custom: «dig»`, `set_cell(target, air)`, `give(turtle, block_item)`; інакше `custom: «false, причина»`.
- КОЛИ `exec(place[Up|Down])` → ЯКЩО `free(target)` і `has(selected_slot, item)` → ТО `place(turtle, item)`, `take(turtle, item)`; для табличок аргумент — текст.
- КОЛИ `exec(detect[Up|Down])` → ЯКЩО `cell(target, solid)` → ТО `custom: «true»`; повітря й рідина → false.
- КОЛИ `exec(compare[Up|Down])` → ЯКЩО `same(target_block, selected_item, type)` → ТО `custom: «true»`.
- КОЛИ `exec(inspect[Up|Down])` → ЯКЩО `not free(target)` → ТО `custom: «таблиця: назва, стан і теги блоку»`; інакше false + повідомлення.
- КОЛИ `exec(attack[Up|Down])` → ЯКЩО `occupied(target, mob)` → ТО `damage(mob, n)`.
- КОЛИ `exec(suck[Up|Down](n))` → ЯКЩО `occupied(target, container|item)` → ТО `pickup(turtle, item)`; заповнює слоти від вибраного далі.
- КОЛИ `exec(drop[Up|Down](n))` → ТО `custom: «drop»`: стек з вибраного слота — у контейнер попереду або у світ.
- КОЛИ `exec(refuel(n))` → ЯКЩО `custom: «предмет у вибраному слоті горить»` → ТО `take(turtle, fuel_item)`, `counter(fuel, +value)`; `refuel(0)` лише перевіряє, чи предмет — паливо.
- КОЛИ `counter(fuel, >=, limit)` → ТО `block` (бак: 20 000 у звичайної, 100 000 у розвиненої); на сервері з вимкненим паливом рівень = «unlimited».
- КОЛИ `exec(select(slot))` → ЯКЩО `custom: «slot поза 1…16»` → ТО `crash` (помилка Lua); так само `drop`/`getItemCount` з хибним аргументом.
- КОЛИ `exec(transferTo(slot, n))` → ТО `custom: «перекласти n предметів з вибраного слота в інший»`.
- КОЛИ `exec(equipLeft|equipRight)` → ТО `swap(selected_item, side_upgrade)` — апгрейд і предмет міняються місцями.
- КОЛИ `exec(craft(n))` → ЯКЩО `custom: «предмети в інвентарі складають рецепт»` → ТО `transform(ingredients, result)`; `craft(0)` лише перевіряє рецепт.
- КОЛИ `custom: «змінився інвентар черепахи»` → ТО `custom: «подія turtle_inventory»` — програма може чекати на неї (`os.pullEvent`).
- КОЛИ `custom: «під гравієм / піском звільнилась клітина»` → ТО `fall(block)` — тому `tunnel` копає в циклі, поки `detect` = true, з паузою 0,5 с.
- КОЛИ `exec(gps.locate)` → ЯКЩО `custom: «відповіли GPS-хости в межах таймауту (2 с)»` → ТО `custom: «повернути x, y, z (трилатерація)»`; інакше nil.
- КОЛИ `exec(rednet.send(id, msg))` → ТО `custom: «повідомлення компʼютеру за ID; доставка не гарантована»`; `broadcast` — усім на каналі 65535.
- КОЛИ `custom: «завантаження компʼютера»` → ЯКЩО `custom: «є файл startup»` → ТО `custom: «запустити його автоматично»`.
- КОЛИ `exec(error)` або `custom: «необроблена помилка Lua»` → ТО `crash`, `program_end` — черепаха завмирає там, де стояла.
- Перемога / поразка / рахунок: нема — пісочниця; «рівень» = задача, яку гравець ставить собі сам (шахта, ферма, міст).

### Excavate — вбудована програма як еталон «робота-копача»
- Аргумент — діаметр d: квадрат d×d, шар за шаром униз змійкою (у ряду d−1 кроків, поворот через одну клітину, напрям чергується).
- Позицію веде мертвим рахунком: змінні xPos, zPos, depth, xDir, zDir оновлюються після кожного успішного кроку.
- Перед кожним кроком — `refuel` до цільового рівня `xPos + zPos + depth + 2`; не вистачає — «Not enough Fuel» і повернення.
- Рух заблоковано: блок → копати; копати не вийшло (напр. непробивний блок) → кінець розкопу; нічого не виявлено → атакувати (моб) і повторити через 0,5 с.
- Усі 16 слотів зайняті → повернутися на старт, вивантажити все `drop` у скриню **позаду старту**, повернутися на збережену позицію; бракує палива на дорогу → чекати подію `turtle_inventory`, поки гравець докине паливо.
- Кінець — додому, вивантажитись, запечатати отвір блоком знизу, «Mined N items total».

## Керування і ввід
- Гравець не рухає черепаху напряму: правий клік відкриває її термінал, де він пише й запускає програми (`edit prog`, `prog 5`).
- Вбудовані програми як «команди оболонки»: `go fd 3 up 2` (пари напрям-відстань), `turn`, `tunnel 20` (тунель 3×2), `excavate 8`, `refuel`, `craft`, `equip`, `unequip`, `dance`.
- Інтерактивний `lua` (REPL) — виконувати виклики `turtle.forward()` по одному: ручне «покрокове» керування через код.
- Переривання програми — подія `terminate` (комбінація клавіш — у «Непевне»).
- Кілька черепах координуються повідомленнями rednet; бездротова «кишенькова» версія компʼютера (`pocket`) — пульт у руці.

## Вікна, меню, HUD
- `game-screen` — світ Minecraft; черепаха видна як блок з обличчям-екраном, рухається анімовано.
- `+window:turtle-inventory` — GUI черепахи: термінал CraftOS + сітка 16 слотів з підсвіченим вибраним слотом (`+ui:selected-slot-highlight`) (?).
- `+window:terminal-shell` — оболонка CraftOS: подібна до MS-DOS (`ls`, `copy`, `delete`, `clear`), запуск програм за назвою, вкладки `multishell` на розвинених компʼютерах (?).
- `code-editor` — вбудований редактор `edit`: текст програми, збереження у файл компʼютера.
- `help-window` — програма `help` з довідкою по програмах і API.
- Монітор — зовнішній екран із кількох блоків; розвинений підтримує дотик і 16 кольорів.
- Переходи: світ → правий клік → термінал черепахи → `edit` / запуск програми → Esc у світ (черепаха працює далі без відкритого вікна).

## Фічі поза полем
- Файлова система компʼютера зберігає програми між сесіями; системна тека `rom` — лише для читання.
- `startup` — програма-автозапуск; `require` — модулі з кодом; `parallel` — кілька співпрограм одночасно (рух + слухати радіо).
- Обмін програмами: дискети в дисководі, HTTP-доступ (з версії 1.1), повідомлення модемів (бездротові — з 1.5.1).
- `+feature:server-config`: власник сервера може вимкнути витрату палива («unlimited»), дозволити локальні IP тощо; команда `/computercraft` для адміністрування.
- Апгрейди черепахи — інструменти та модем на лівому/правому боці; набір інструментів розширюється датапаками.
- `mode-sandbox` у чистому вигляді: ні рівнів, ні рахунку; задачі — у спільнот (сервери з таблицями рекордів шахт, конкурси ферм).

## Варіації й родичі
- ComputerCraft (Dan200, грудень 2011; остання оригінальна версія 1.79 для Minecraft 1.8.9, 2016) → **CC: Tweaked** (SquidDev, головний форк, понад 21,5 млн завантажень на липень 2022) і CC: Restitched. Документація й API, описані тут, — за CC: Tweaked.
- Родичі в корпусі: `robot-karol` (робот будує цеглою в 3D-кімнаті, теж «попереду» і висота), `the-farmer-was-replaced` (дрон на фермі, Python-подібний код, ресурси як бюджет), `screeps` (постійний світ, де код живе між сесіями), `autonauts` і `craftomation-101` (боти-працівники з візуальними програмами), `karel` (сенсори й дії лише «попереду»), `mindustry-logic` і `factorio-circuit-network` (програмування всередині чужої гри-будівництва).
- Осі варіацій: **сенсори** (лише попереду — Karel / три напрямки — CC / уся мапа — Screeps); **ціна дії** (паливо на крок — CC / час — Farmer / енергія — Screeps); **світ** (скінченний рівень з метою / вічна пісочниця); **невдача** (виняток і стоп / `false` і продовження).

## Цікавинки для курсу
- Мертвий рахунок позиції й орієнтації (`xPos/zPos/depth/xDir/zDir`) + повернення додому — 🥉 (векторна арифметика поворотів, тест на розбіжність).
- Excavate: змійка шарами, повернення при повному інвентарі, розрахунок палива «на дорогу назад», продовження з тієї ж точки — 🥈.
- Паливо як бюджет переміщень (поворот безкоштовний, копання безкоштовне) — 📎.
- Сенсори лише в 3 напрямки і `detect`/`compare`/`inspect` як три рівні деталізації — 🌱.
- Гравій, що падає в щойно звільнену клітину: копати в циклі, поки `detect` — 📎.
- Невдача як `false, reason` замість винятку (і `assert`, щоб не проґавити) — 🌱.
- GPS трилатерацією від відстаней до хостів — 🥇 (геометрія + шум/таймаут).
- Рій черепах з rednet-повідомленнями (розподіл ділянок, «я закінчив») — 🥈.

## Мапа на каталог
- Є: `command-program` (Lua-програма черепахи) · `user-procedures` (функції Lua) · `sensor-predicates` (detect/compare/inspect) · `orientation-state` (напрям черепахи) · `dig-terrain` (dig) · `item-pickup` (suck) · `inventory`, `inventory-items`, `inventory-limit` (16 слотів, ліміт стека) · `gravity-fall` (гравій/пісок) · `code-editor-window` (`edit`) · `help-window` (`help`) · `game-loop` (подієвий цикл `os.pullEvent`).
- **Нема** → пропозиції карток:
  - `+relative-moves-3d` «Рух вперед/назад/вгору/вниз + поворот 90° у 3D-сітці» · entities/move · 📎.
  - `+fuel-per-move` «Паливо витрачається на крок, поворот безкоштовний» · entities/state · 🌱.
  - `+three-direction-sensors` «Сенсори й дії лише попереду / над / під» · game-logic/program · 🌱.
  - `+selected-inventory-slot` «Вибраний слот як аргумент дій (place, drop, refuel)» · entities/state · 🌱.
  - `+place-from-slot` «Поставити блок з вибраного слота в сусідню клітину» · entities/interact · 🌱.
  - `+tool-upgrade-sides` «Два боки для інструментів-апгрейдів, обмін з інвентарем» · entities/state · 📎.
  - `+failure-as-return-value` «Команда повертає false і причину замість помилки» · game-logic/program · 🌱.
  - `+dead-reckoning-position` «Програма сама рахує позицію і напрям» · game-logic/program · 🥉.
  - `+return-home-unload` «Повернутись на базу, розвантажитись, продовжити з тієї ж точки» · game-logic/program · 🥈.
  - `+gps-trilateration` «Позиція з відстаней до відомих точок» · game-logic/program · 🥇.
  - `+radio-messaging` «Повідомлення між роботами за ID / broadcast» · game-logic/program · 🥉.
  - `+persistent-file-system` «Програми зберігаються у файлах компʼютера» · code/architecture · 📎.
  - `+startup-script` «Автозапуск програми при завантаженні» · game-logic/program · 🌱.
  - `+event-wait` «Програма чекає ігрову подію (зміна інвентаря, повідомлення)» · game-logic/program · 📎.
  - `+craft-from-inventory` «Крафт з предметів інвентаря за рецептом» · entities/interact · 🥉.
  - `+server-config-unlimited-fuel` «Налаштування сервера знімає ліміт палива» · game-logic/difficulty · 🌱.

## Пропозиції до словників
- `+effect:dig` — зламати блок у клітині й отримати предмет (CC, FORK BOMB, Farmer).
- `+effect:drop` — викласти стек з інвентаря в контейнер або у світ.
- `+effect:refuel` — спалити предмет у паливо (лічильник палива).
- `+effect:select_slot` — зробити слот інвентаря активним для наступних дій.
- `+effect:equip` — обміняти предмет і апгрейд на боці робота.
- `+effect:craft` — перетворити набір предметів інвентаря на результат за рецептом.
- `+effect:send` — надіслати повідомлення іншому роботу/компʼютеру (rednet; також FORK BOMB).
- `+trigger:event(name)` — програма отримала подію (turtle_inventory, modem_message, timer).
- `+cond:has_space(slot)` — у слоті / інвентарі є місце (excavate повертається, коли нема).
- `+window:terminal-shell` — текстова оболонка ОС усередині гри (CraftOS).
- `+window:turtle-inventory` — вікно робота: термінал + слоти інвентаря.
- `+ui:selected-slot-highlight` — підсвічений активний слот.
- `+feature:persistent-filesystem` — файли програм живуть у компʼютері між сесіями.
- `+feature:server-config` — правила гри (паливо, мережа) задає власник сервера.
- Вісь-кандидат `control: programmed` (`classes.md`) тут підтверджується: гравець лише пише код.

## Джерела
- ⭐ [tweaked.cc: модуль turtle](https://tweaked.cc/module/turtle.html) — усі виклики з сигнатурами й поверненням, паливо (20 000 / 100 000, «unlimited»), 16 слотів, `false, reason` замість помилок.
- [Wikipedia FR: ComputerCraft](https://fr.wikipedia.org/wiki/ComputerCraft) — автор, дата, типи компʼютерів, периферія, CraftOS, `rom`, `startup`, CC: Tweaked.
- [GitHub: rom/programs/turtle](https://github.com/cc-tweaked/CC-Tweaked/tree/mc-1.20.x/projects/core/src/main/resources/data/computercraft/lua/rom/programs/turtle) — список вбудованих програм; [excavate.lua](https://raw.githubusercontent.com/cc-tweaked/CC-Tweaked/mc-1.20.x/projects/core/src/main/resources/data/computercraft/lua/rom/programs/turtle/excavate.lua), [tunnel.lua](https://raw.githubusercontent.com/cc-tweaked/CC-Tweaked/mc-1.20.x/projects/core/src/main/resources/data/computercraft/lua/rom/programs/turtle/tunnel.lua), [go.lua](https://raw.githubusercontent.com/cc-tweaked/CC-Tweaked/mc-1.20.x/projects/core/src/main/resources/data/computercraft/lua/rom/programs/turtle/go.lua) — код алгоритмів.
- [tweaked.cc: gps](https://tweaked.cc/module/gps.html) і [rednet](https://tweaked.cc/module/rednet.html) — позиціювання та повідомлення.
- [tweaked.cc: data packs](https://tweaked.cc/reference/data_pack.html) — теги блоків для лопати / меча / мотики, що ставить і з чим взаємодіє `place`.
- YouTube: пошук «computercraft turtle mining program».

## Непевне
- (?) Витрата палива — 1 одиниця на блок і енергоємність вугілля (80) — з памʼяті; документація каже лише «рух витрачає паливо, поворот — ні»; на 1 за крок натякає цільовий рівень в excavate.
- (?) Тривалість однієї дії черепахи (≈0,4 с / 8 тіків) — з памʼяті, у документації не знайдено.
- (?) Черепаха не падає під дією гравітації і може зависати в повітрі — з памʼяті.
- (?) Чи може черепаха заходити в рідину — не перевірено; `detect` для рідини повертає false.
- (?) Для `craft` потрібен апгрейд-верстак, а для `attack` з шкодою — меч; повний перелік апгрейдів (модем, динамік, верстак) у відкритих сторінках не знайдено.
- (?) Вигляд GUI черепахи (термінал + сітка 4×4 слотів) і вкладки `multishell` — з памʼяті.
- (?) Переривання програми комбінацією Ctrl+T — з памʼяті; документація підтверджує лише подію `terminate`.
- (?) Скільки GPS-хостів потрібно (4 для однозначної 3D-позиції) — сторінка `gps` не каже, є окремий гайд.
