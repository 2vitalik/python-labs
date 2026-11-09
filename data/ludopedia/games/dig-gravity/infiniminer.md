---
title: Infiniminer
slug: infiniminer
aka: []
family: dig-gravity
also: [build-sim]
klass: avatar
axes:
  field: 3d
  time: realtime
  opponent: online
  info: partial
  random: setup
  goal: race
year: 2009
platforms: [PC (Windows, XNA)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Infiniminer", best: true, note: "дві команди в процедурному блоковому світі, руда → гроші, виграє команда з грошима; витік коду; вплив на Minecraft"}
  - {kind: official, url: "https://www.zachtronics.com/infiniminer/", note: "Zachtronics: «змагальна гра копання від першої особи в процедурному блоковому світі», лише історично"}
  - {kind: other, url: "https://github.com/craftworkgames/infiniminer", note: "відкритий код v1.5 (експорт code.google.com): класи, ціни блоків, банк, лава, вибухи, радар"}
  - {kind: other, url: "https://github.com/gibbed/Infiniminer", note: "ще одне дзеркало коду"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Infiniminer+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-by-input, keyboard-controls, gravity-fall, dig-terrain, destructible-blocks, cursor-place, impassable-cells, ladder-climb, floor-types, explode-area, chain-detonation, environment-death, player-death, respawn, inventory-limit, round-currency, collect-quota, online-multiplayer, minimap-radar, message-log, status-panel, game-settings, controls-remap, lobby-window, character-select, help-window, +team-play, +character-classes, +first-person-view, +fall-damage, +core-deposit, +ore-vein-generation, +procedural-world, +liquid-flow, +team-force-field, +jump-pad, +prospecting-radar, +build-cost-resource, +remote-detonation, +surface-auto-deposit]
proposes: ["+effect:deposit", "+effect:withdraw", "+trigger:landed", "+effect:flow", "+window:team-select", "+ui:radar-meter", "+ui:team-cash", "+feature:team-chat", "+card:team-force-field", "+card:jump-pad", "+card:prospecting-radar", "+card:build-cost-resource", "+card:surface-auto-deposit"]
author: opus
date: 2026-11-09
---

# Infiniminer — дві команди копають воксельний куб за золото й діаманти, а руду витрачають на будівлі й пастки

## Суть
Мережева гра від першої особи (Zachtronics, 2009): червона й синя команди в процедурному блоковому світі копають кіркою, несуть золото й діаманти на поверхню й заробляють гроші команді; перша команда, що набрала поріг, виграє. Друга валюта — руда: її кладуть у банк команди й витрачають на блоки (драбини, дороги, стрибкові плити, силові поля, електроблоки, вибухівку). Чотири класи ділять ролі: копач, розвідник із радаром, інженер-будівничий, сапер. Боротьба з суперником — непряма: вибухи, лава й пастки, зброї нема. Саме блоковий вигляд, вид від першої особи й будування Маркус Перссон назвав впливом на Minecraft.

## Поле і час
- Поле — воксельний куб 64 × 64 × 64 блоки (`MAPSIZE = 64` у коді); рівень землі — 8 шарів від верху (`GROUND_LEVEL = 8`), над ним гори й поверхня, під ним шахта.
- Генерація (`CaveGenerator`): суцільний ґрунт → жили руди випадковим блуканням по шуму Перліна (`orefactor` = 10 жил) → золото «смугами» на середній глибині, діаманти глибоко → гори над землею → печери → валуни каменю, зміщені вглиб → лавові джерела на середній глибині (камінь із лавою зверху). `random: setup`: після старту випадковості нема.
- Рух гравця неперервний (фізика від першої особи: гравітація, стрибок, біг), блоки — клітини сітки. Камера — очі гравця; крізь блоки не видно, звідси `info: partial` (частину знань дає радар).
- Real-time на сервері; лава розтікається кроками серверного циклу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | команда, клас; ore ≤ OreMax, weight ≤ WeightMax, loot $ | ходить, стрибає, лазить; кирка досягає 2 блоки, будівельна гармата — 6 |
| Prospector | player | ore 200, weight 4 | кирка, будівельна гармата (Solid, Force Field, Beacon, Ladder), радар |
| Miner | player | ore 200, weight 8 | кирка (перезарядка × 0,4 — копає вдвічі з лишком швидше), гармата (Solid, Force Field, Ladder) |
| Engineer | player | ore 350, weight 4 | кирка, гармата з 9 блоків (+ Road, Jump, Shock, Beacon, Bank), деконструктор |
| Sapper | player | ore 200, weight 4 | кирка, гармата (Solid, Force Field, Ladder, Explosive), детонатор |
| Ґрунт (Dirt) | terrain | — | кирка → порожньо |
| Камінь (Rock) | static | — | кирка не бере; лише вибух |
| Руда (Ore) | resource | +20 руди | кирка → порожньо, руда в запас гравця до OreMax |
| Золото (Gold) | resource | +$100, вага 1 | копається, лише якщо є вільна вага |
| Діамант (Diamond) | resource | +$1000, вага 1 | як золото; вибух не руйнує |
| Лава | hazard | — | дотик = смерть; тече вниз, а з опорою — убік |
| Solid (червоний/синій) | static | 10 руди | стіна команди; руйнують вибух і деконструктор своєї команди |
| Force Field (Trans) | gate | 25 руди | прохідний для своєї команди, стіна для чужої |
| Road | terrain | 10 руди | швидкість ходьби × 2 |
| Ladder | terrain | 25 руди | при контакті — підйом угору |
| Jump | terrain | 25 руди | підкидає на 2,5 × висоти стрибка, без ефекту удару при приземленні |
| Shock | hazard | 50 руди | удар головою знизу = смерть («WAS ELECTROCUTED!») |
| Explosive | object | 100 руди | детонатор сапера підриває всі свої; ланцюг через сусідні |
| Bank (команди) | static | 50 руди | термінал: внести/зняти руду; вибух не руйнує |
| Beacon (команди) | static | 50 руди | мітка з текстом на радарі своєї команди |
| Metal | static | — | вибух не руйнує; генератор у цій версії не ставить (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(fire, pickaxe)` → ЯКЩО `in_range(player, target, 2)` and `cell(target, dirt)` → ТО `set_cell(target, empty)`.
- КОЛИ `input(fire, pickaxe)` → ЯКЩО `cell(target, ore)` → ТО `set_cell(target, empty)`, `counter(ore, +20)` (обрізається до OreMax).
- КОЛИ `input(fire, pickaxe)` → ЯКЩО `cell(target, gold|diamond)` and `counter(weight, <, WeightMax)` → ТО `set_cell(target, empty)`, `counter(weight, +1)`, `counter(loot, +100|+1000)`; інакше `block` (блок лишається).
- КОЛИ `input(fire, pickaxe)` → ЯКЩО `cell(target, rock|team_block)` → ТО `block`.
- КОЛИ `input(fire, construction_gun)` → ЯКЩО `counter(ore, >=, cost)` and `free(build_cell)` and `not occupied(build_cell, player)` → ТО `place(player, block)`, `set_side(block, team)`, `counter(ore, -cost)`; інакше `custom: «гармата смикається, нічого не стається»`.
- КОЛИ `input(fire, deconstruction_gun)` → ЯКЩО `same(target, player, team)` and `cell(target, construction_block)` → ТО `set_cell(target, empty)` (руда не повертається).
- КОЛИ `contact(player, force_field)` → ЯКЩО `same(force_field, player, team)` → ТО `custom: «проходить крізь блок»`; інакше `block`.
- КОЛИ `enter(player, road)` → ТО `speed(player, ×2)`; біг (Shift) — ще × 1,5.
- КОЛИ `enter(player, jump)` → ТО `custom: «вертикальна швидкість = 2,5 × швидкості стрибка»`.
- КОЛИ `contact(player, ladder)` → ТО `custom: «підйом зі швидкістю лазіння»`.
- КОЛИ `custom: «приземлення»` → ЯКЩО `custom: «швидкість падіння ≥ смертельної»` → ТО `custom: «смерть гравця»`; від половини смертельної — лише струс екрана.
- КОЛИ `contact(player_head, shock)` → ТО `custom: «смерть гравця»`.
- КОЛИ `contact(player, lava)` → ТО `custom: «смерть гравця»` (і коли лава натекла на нерухомого).
- КОЛИ `edge(player)` (нижче дна мапи) → ТО `custom: «смерть гравця»`.
- КОЛИ `died(player)` → ТО `counter(ore, =0)`, `counter(loot, =0)`, `counter(weight, =0)`, `message(«… WAS KILLED BY …»)`; після кліку `respawn(player, «випадкова безпечна точка на поверхні»)`.
- КОЛИ `input(fire, detonator)` → ТО для кожної своєї вибухівки `explode(cube 5×5×5, 2)`: руйнує ґрунт, камінь, руду, лаву, блоки команд, драбини, дороги, Jump, Shock; не руйнує золото, діаманти, банки, маяки, Metal.
- КОЛИ `custom: «вибух зачепив інший Explosive»` → ТО `explode(...)` і для нього (`chain-detonation`).
- КОЛИ `custom: «вибух»` → ЯКЩО `in_range(explosion, player, 3)` → ТО `custom: «смерть гравця»`; у радіусі 8 — струс екрана.
- КОЛИ `input(deposit)` → ЯКЩО `custom: «дивиться на банк своєї команди ≤ 2,5 блоки»` → ТО `counter(ore, -50)`, `counter(team_ore, +50)` (команда тримає ≤ 9999).
- КОЛИ `input(withdraw)` → ЯКЩО той самий банк → ТО `counter(team_ore, -50)`, `counter(ore, +50)` (не більше OreMax).
- КОЛИ `tick` → ЯКЩО `custom: «гравець над рівнем землі»` and `counter(loot, >, 0)` → ТО `currency(+loot)` команді, `score(+loot)` гравцю, `message(«SERVER: … HAS EARNED $… FOR THE … TEAM!»)`, `counter(loot, =0)`, `counter(weight, =0)`.
- КОЛИ `counter(team_cash, >=, winningcash)` (за замовчуванням $10 000) → ТО `win` команди, `message(«GAME OVER – …»)`; за 10 с сервер зберігає мапу й перезапускається з новою.
- КОЛИ `timer(1)` (кожен серверний крок) → ЯКЩО `cell(below_lava, empty)` → ТО `set_cell(below_lava, lava)`; інакше ЯКЩО `not cell(below_lava, lava)` → ТО `set_cell(side_empty ×4, lava)` (тече по опорі, у порожнечі — лише вниз).
- КОЛИ `input(fire, radar)` → ТО `custom: «скан 7 × 7 променів уздовж погляду до 30 м»`; ЯКЩО `custom: «промінь зачепив золото/діамант»` → ТО `sound(radar-low|radar-high)` і показ відстані.
- КОЛИ `input(ping)` → ТО `custom: «мітка гравця блимає на радарі команди»`.
- КОЛИ `input(change_class)` → ЯКЩО `custom: «гравець на поверхні»` → ТО `window(character-select)`; інакше `message(«YOU CANNOT CHANGE YOUR CLASS BELOW THE SURFACE»)`.
- Перемога: команда першою зібрала поріг грошей. · Поразка: суперник зібрав раніше. · Рахунок: внесені гроші гравця (`Score`) на табло.

## Керування і ввід
- WASD — рух у напрямку погляду, миша — огляд, Space — стрибок, Shift — біг, Ctrl — присід (розкладка `keymap.txt`, перепризначається).
- ЛКМ/ПКМ — застосувати інструмент; 1–5 — інструмент напряму, E — наступний; коліщатко / R — тип блока для гармати.
- 8 — внести руду в банк, 9 — зняти; Q — пінг на радарі; Y / U — чат усім / команді; M — змінити клас, N — команду; F1 (утримати) — довідка; Ctrl-S — зберегти мапу локально.
- Інструменти мають перезарядку: кирка 0,55 с (Miner × 0,4), гармата й деконструктор 0,5 с, радар 0,5 с.

## Вікна, меню, HUD
- `splash-screen` / титул «INFINIMINER» з музикою.
- `lobby-window` — браузер серверів (публічний список, повні сервери притемнені, «Connecting…»).
- `custom-window` → `+window:team-select`: червоні / сині.
- `character-select`: Prospector · Miner · Engineer · Sapper (повторно — M, лише на поверхні).
- `loading-screen` — отримання мапи (стиснення в гілці v1.5).
- `game-screen`: вид від першої особи; HUD — `ORE`, `LOOT: $`, `WEIGHT`, `TEAM ORE`, гроші обох команд (`+ui:team-cash`), `minimap` радар з гравцями (вище/нижче/той самий рівень), маяками й пінгами, позначка NORTH, іконка інструмента й обраного блока, `+ui:radar-meter` (відстань і цінність знахідки), `message-log` (чат і смерті), іменні таблички.
- `help-window` — довідка поверх гри (F1).
- `leaderboard`-табло з назвою сервера вгорі (гравці, рахунок).
- `confirm-dialog` виходу: «PRESS Y TO CONFIRM…», там же «PRESS K TO COMMIT PIXELCIDE» (самогубство-респавн).
- `settings-window` — у гілці v1.5 меню з усіма полями `client.config.txt` і чутливістю миші.
- Переходи: титул → сервери → команда → клас → завантаження → гра → GAME OVER у HUD → перезапуск сервера.

## Фічі поза полем
- `online-multiplayer`: виділений сервер (`maxplayers` 16, порт 5565), публічний список серверів; `+feature:team-chat`.
- `custom-rules` через `server.config.txt`: `winningcash`, `includelava`, `orefactor`, `sandbox` (усі блоки безкоштовні, перемоги нема), `notnt`; консоль сервера, адміни, бан/кік, автобекап мапи кожні 5 хв, завантаження збереженої мапи.
- `remap-controls` (`keymap.txt`), налаштування клієнта.
- Нема сингла, ботів, прогресії між матчами.

## Варіації й родичі
- Гілка v1.5 спільноти (той самий код): лава тече по Shock-блоках убік і вгору («труби» лави), Road над лавою поглинає її, «insane lava» заливає будь-яку яму, сферичні вибухи радіусом 3 замість куба 5 × 5 × 5, лаву можна копати.
- Наступники: Minecraft (той самий блоковий світ, сингл і крафт; див. [minecraft-redstone.md](../build-sim/minecraft-redstone.md)), Infinifactory від того ж автора ([infinifactory.md](../program-robots/infinifactory.md)), моди й клони (Infinifortress, Minetest/Luanti).
- У сімʼї: [mine-blocks.md](mine-blocks.md) (2D-копання з крафтом), [motherload.md](motherload.md) (руда → гроші → апгрейди, сингл), [dig-dug.md](dig-dug.md).
- **Осі варіацій**: валюта — одна / дві (руда-будматеріал + гроші-очки); доставка — автоматично на поверхні / через термінал банку; прохідність блока — для всіх / лише своєї команди; суперник — прямий бій / лише пастки й вибухи.

## Цікавинки для курсу
- Дві валюти: руда (будівельний ресурс, спільний банк команди) і гроші (очки, що зараховуються лише на поверхні) — 🥉, бо потрібні спільний стан команди й зона зарахування.
- Класи як набори інструментів і лімітів (OreMax, WeightMax, перезарядка) — 📎.
- Лава-автомат: униз у порожнечу, убік лише з опорою, за кроки серверного циклу з прапорцем «вже текла цього кроку» — 🥉.
- Блок, прохідний лише для своєї команди, — 🌱.
- Вибух кубом 5 × 5 × 5 з таблицею «що руйнується» і ланцюгом підривів — 📎.
- Радар-промені в конусі погляду до цінних блоків — 🥉.
- Мережева синхронізація зміни блоків (сервер авторитетний, клієнт шле дію) — 🥇.

## Мапа на каталог
- Є: `move-by-input` · `keyboard-controls` · `gravity-fall` · `dig-terrain` ↔ кирка · `destructible-blocks` ↔ вибухи · `cursor-place` ↔ будівельна гармата · `impassable-cells` ↔ камінь, Metal · `ladder-climb` · `floor-types` ↔ Road, Jump · `explode-area` + `chain-detonation` ↔ Explosive · `environment-death` ↔ лава, Shock, падіння · `player-death` + `respawn` · `inventory-limit` ↔ OreMax/WeightMax · `round-currency` ↔ руда · `collect-quota` ↔ $10 000 команди · `online-multiplayer` · `minimap-radar` · `message-log` · `status-panel` · `game-settings` · `controls-remap` · `lobby-window` · `character-select` ↔ класи · `help-window`.
- **Нема** → пропозиції карток:
  - `+team-force-field` «Блок прохідний лише для своєї команди» · entities/legality · 🌱 · слот {team}.
  - `+jump-pad` «Плита, що підкидає» · entities/move · 🌱 · слот {power}.
  - `+prospecting-radar` «Радар показує відстань до цінного блока в напрямку погляду» · interface/hud · 🥉 · слоти {range, cone}.
  - `+build-cost-resource` «Кожен поставлений блок коштує ресурсу» · game-logic/economy · 🌱 · слот {cost_table}.
  - `+surface-auto-deposit` «Здобич зараховується, коли носій повернувся в зону» · game-logic/economy · 📎 · родич `+core-deposit`.
  - `+remote-detonation` (повтор) — детонатор підриває всі свої заряди.
  - `+team-play`, `+character-classes`, `+first-person-view`, `+fall-damage`, `+ore-vein-generation`, `+procedural-world`, `+liquid-flow` — повтори з інших файлів.

## Пропозиції до словників
- `+effect:deposit` — віддати ресурс зі свого запасу в спільний (банк команди; повтор).
- `+effect:withdraw` — узяти ресурс зі спільного запасу у свій.
- `+trigger:landed` — приземлення після падіння (смерть за швидкістю; повтор).
- `+effect:flow` — рідина займає сусідню порожню клітину за правилом опори (лава; повтор).
- `+window:team-select` — вибір команди перед класом.
- `+ui:radar-meter` — показ відстані/цінності знахідки радара; `+ui:team-cash` — рахунок кожної команди в HUD.
- `+feature:team-chat` — чат лише своїй команді (повтор).

## Джерела
- ⭐ [Wikipedia: Infiniminer](https://en.wikipedia.org/wiki/Infiniminer) — команди, процедурний світ, руда → гроші, перемога команди з найбільшими грошима, витік і відкриття коду, вплив на Minecraft.
- [Zachtronics: Infiniminer](https://www.zachtronics.com/infiniminer/) — авторський опис жанру, статус «лише історично».
- [GitHub: craftworkgames/infiniminer](https://github.com/craftworkgames/infiniminer) — код v1.5: `BlockInformation.cs` (типи й ціни блоків), `Player.cs` і `PropertyBag.cs` (класи, інструменти, ліміти, радар, банк), `InfiniminerServer.cs` (кирка, гармата, деконструктор, вибух, лава, депозит, перемога), `MainGameState.cs` (рух, Road, Jump, Ladder, Shock, падіння), `CaveGenerator.cs` (генерація), `server.config.txt`, `keymap.txt`, `changelog.txt`.
- [GitHub: gibbed/Infiniminer](https://github.com/gibbed/Infiniminer) — дзеркало коду.
- YouTube: пошук «Infiniminer gameplay».

## Непевне
- (?) Відкритий код — гілка v1.5 зі змінами спільноти (меню налаштувань, опції лави, сферичні вибухи); у первісному релізі 2009 р. частина опцій могла бути іншою. Класи, ціни й правила грошей — у ядрі, без позначок «мод».
- (?) Значення змінних DIEVELOCITY, JUMPVELOCITY, MOVESPEED у секундах/блоках не виписано; поріг смерті від падіння — лише як «≥ смертельної швидкості».
- (?) Metal у генераторі не використовується (закоментовані «домівки» команд); де він зʼявляється — невідомо.
- (?) Чи стартові банки команд ставить генератор, чи їх будують інженери з нуля, — у прочитаних файлах не видно.
- (?) Як саме вважається, що гравець «на поверхні» для зміни класу, — у коді клієнта не дочитано.
