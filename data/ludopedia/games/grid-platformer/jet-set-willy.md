---
title: Jet Set Willy
slug: jet-set-willy
aka: [JSW]
family: grid-platformer
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: none
  goal: collect
year: 1984
platforms: [ZX Spectrum, C64, Amstrad CPC, Dragon 32/64]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Jet_Set_Willy", best: true, note: "вільний маєток із 60 екранів, сходи й мотузки, смерть від падіння, відродження на вході в кімнату, кодова картка, Attic Bug"}
  - {kind: other, url: "https://skoolkit.ca/disassemblies/jet_set_willy/reference/facts.html", note: "дизасемблер: кінець о 1:00, мотузки вгору/вниз, рампи й конвеєри, нескінченні цикли смертей, WRITETYPER і телепорт"}
  - {kind: other, url: "https://skoolkit.ca/disassemblies/jet_set_willy/asm/41984.html", note: "таблиця предметів: 83 записи, біт «зібрано»"}
  - {kind: other, url: "https://skoolkit.ca/disassemblies/jet_set_willy/reference/glossary.html", note: "guardian горизонтальний/вертикальний, nasty"}
  - {kind: other, url: "https://worldofspectrum.org/pub/sinclair/games-info/j/JetSetWilly.txt", note: "оригінальна інструкція: мета, Марія, клавіші"}
  - {kind: other, url: "https://www.c64-wiki.com/wiki/Jet_Set_Willy", note: "C64: 9 життів, клавіші, пауза, баг відродження"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Jet+Set+Willy+ZX+Spectrum+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [gravity-fall, item-pickup, collect-all, enemy-patrol, touch-death, environment-death, player-death, carrier-platform, respawn, checkpoint, teleport, cheat-codes, game-pause, music-toggle, status-panel, goal-counter, game-screen, keyboard-controls, +flip-screen-rooms, +fall-height-kill, +fixed-arc-jump, +rope-swing, +ramp-walk, +respawn-death-loop, +copy-protection-code, +game-clock-deadline, +guardian-blocks-exit]
proposes: ["+trigger:landed", "+card:rope-swing", "+card:ramp-walk", "+card:respawn-death-loop", "+card:copy-protection-code", "+card:game-clock-deadline", "+window:code-card-entry"]
author: opus
date: 2026-11-09
---

# Jet Set Willy — Віллі нишпорить відкритим маєтком із 60 кімнат і збирає всі предмети в будь-якому порядку, щоб Марія пустила його спати

## Суть
Сиквел [manic-miner](manic-miner.md): той самий Віллі, ті самі «ліво / право / стрибок», смертельні «nasties» і guardians на жорстких маршрутах. Але замість 20 печер підряд — **вільний маєток**: кімнати-екрани зʼєднані краями (flip-screen), і миготливі предмети (83 у таблиці гри) можна збирати в будь-якому порядку. Нові елементи руху — сходи-рампи й мотузки, що гойдаються. Таймера повітря нема, є внутрішній годинник: гра обривається о 1:00 ночі.

## Поле і час
- Мапа — граф кімнат (60 екранів: маєток, дах, сад, пляж, яхта…); кожна кімната — нескролений тайловий екран, вихід краєм веде в сусідню.
- Видно лише поточну кімнату; мапи в грі нема.
- Real-time на кадрах; guardians детерміновані; годинник гри йде від старту до кінця сесії.
- Гравітація; фіксована дуга стрибка; падіння з висоти, більшої за межу, вбиває.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Віллі | player | життя | ходить ліво/право, стрибає фіксованою дугою; лізе сходами й мотузками |
| Підлога / платформа | terrain | — | опора |
| Стіна | static | — | блокує рух |
| Сходи (рампа) | terrain | напрямок | іти в них — підйом; стрибок крізь — оминути; у деяких кімнатах зсувають униз |
| Конвеєр | terrain | напрямок | везе того, хто стоїть (ліжко в спальні — теж конвеєр) |
| Мотузка | object | фаза гойдання | Віллі чіпляється й гойдається; рух за/проти гойдання — вниз/вгору |
| Nasty | hazard | — | нерухомий; дотик — смерть |
| Guardian горизонтальний | enemy | межі, швидкість | туди-сюди по ряду |
| Guardian вертикальний | enemy | межі, швидкість | вгору-вниз |
| Стріла (arrow) | projectile | ряд | летить через кімнату горизонтально; дотик — смерть |
| Марія (економка) | enemy | — | стоїть біля спальні; дотик — смерть; зникає, коли все зібрано |
| Предмет | pickup | — | миготить; зникає при дотику |
| Ліжко / туалет | static | — | фінал: Віллі йде спати |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `free(next)` → ТО `move(willy, dir)`; на сходах — `custom: «крок по діагоналі вгору/вниз»`.
- КОЛИ `input(jump)` → ТО `custom: «стрибок фіксованою дугою, без керування в повітрі»`; крізь сходи — пролітає, не чіпляючись.
- КОЛИ `tick` → ЯКЩО `not supported(willy)` → ТО `fall(willy)`.
- КОЛИ `custom: «приземлився після падіння довшого за межу»` → ТО `lives(-1)`, `respawn(willy, room_entry)`.
- КОЛИ `contact(willy, rope)` → ТО `attach(willy, rope)`; КОЛИ `input(dir)` → ЯКЩО `moving(rope, dir)` → ТО `move(willy, down_rope)`, інакше `move(willy, up_rope)`; КОЛИ `input(jump)` → ТО `detach(willy, rope)`.
- КОЛИ `tick` → ЯКЩО `occupied(below, conveyor)` → ТО `move(willy, conveyor_dir)`.
- КОЛИ `contact(willy, item)` → ТО `pickup`, `counter(items, +1)`.
- КОЛИ `contact(willy, guardian)` або `contact(willy, nasty)` або `contact(willy, arrow)` або `contact(willy, maria)` → ТО `lives(-1)`, `respawn(willy, room_entry)`.
- КОЛИ `edge(willy)` → ТО `custom: «перехід у сусідню кімнату»`, `checkpoint` (точка входу).
- КОЛИ `custom: «відродження в точці, де смерть неминуча»` → ТО `custom: «смерть повторюється до втрати всіх життів»`.
- КОЛИ `counter(items, =, all)` → ТО `disappear(maria)`; КОЛИ `reach(willy, bed)` → ТО `custom: «Віллі йде в туалет і спати»`, `win`.
- КОЛИ `counter(clock, =, 01:00)` → ТО `game_over` — навіть якщо Віллі вже йде до туалету.
- КОЛИ `counter(lives, =, 0)` → ТО `game_over`.
- КОЛИ `game_start` → ТО `window(code-card)`; ЯКЩО `custom: «введено код з клітинки картки»` → ТО гра стартує.
- КОЛИ `input("WRITETYPER")` → ЯКЩО `occupied(here, first_landing_floor)` → ТО `set_state(game, cheat)`; КОЛИ `input(room_code)` → ЯКЩО `state(game, cheat)` → ТО `teleport(willy, room)`.
- Перемога: зібрати всі предмети й дійти до ліжка. Поразка: життя скінчились або настала 1:00. Рахунок: кількість зібраних предметів + час.

## Керування і ввід
- ZX: Q/E/T/U/O — ліворуч, W/R/Y/I/P — праворуч, нижній ряд (Shift…Space) — стрибок; джойстики Kempston, Interface II, AGF, Protek.
- C64: Q–P — ліво/право, Z–M — стрибок, Return — старт і звук, A–L — пауза.
- Пауза в ZX — лише після бездіяльності з вимкненою музикою; BREAK — вихід.

## Вікна, меню, HUD
- `custom-window` «кодова картка»: після завантаження просить колір-код з указаної клітинки картки (180 кодів).
- `splash-screen` / титул з бігучим рядком і музикою (Moonlight Sonata на C64).
- `game-screen`: кімната + назва кімнати + HUD: зібрані предмети, годинник гри, життя-фігурки (?).
- `end-screen` — після 1:00 або 0 життів (?).
- Переходи: картка → титул → game-screen ↔ (край) інша кімната → фінал у спальні.

## Фічі поза полем
- `cheat-codes`: WRITETYPER у First Landing → телепорт у будь-яку кімнату цифровими клавішами.
- Захист від копіювання кодовою карткою.
- `music-toggle`, `pause`; збереження нема.
- Баги ZX-версії (Attic Bug) робили гру непрохідною; видавець випустив POKE-виправлення.

## Варіації й родичі
- Предок: [manic-miner](manic-miner.md) (лінійні печери, повітря). Наступник: Jet Set Willy II (з CPC-версії The Final Frontier); Dragon-версія з додатковими кімнатами.
- Родичі «відкритий маєток із flip-screen кімнат»: [montezumas-revenge](montezumas-revenge.md), [knight-lore](knight-lore.md), [treasure-island-dizzy](treasure-island-dizzy.md), Starquake ([starquake](starquake.md)).
- Осі: **структура** (лінійні екрани / відкритий граф кімнат); **ліміт** (повітря на рівень / годинник на всю гру); **точка відродження** (старт рівня / вхід у кімнату — ризик циклу смертей).

## Цікавинки для курсу
- Граф кімнат, перехід краєм екрана зі збереженням позиції — 🥉.
- Відродження на вході в кімнату + перевірка «чи не вічна смерть» (цикл) — 📎.
- Мотузка-маятник: фаза гойдання визначає, вгору чи вниз — 🥉.
- Діагональні сходи як окремий тип клітини (зайти — підйом, стрибок — крізь) — 📎.
- Таблиця предметів з бітом «зібрано» замість обʼєктів на мапі — 🌱.
- Глобальний годинник, що обриває гру — 🌱.

## Мапа на каталог
- Є: `gravity-fall` · `item-pickup` · `collect-all` · `enemy-patrol` · `touch-death` · `environment-death` · `player-death` · `carrier-platform` (конвеєр) · `respawn` · `checkpoint` (вхід у кімнату) · `teleport` (чит) · `cheat-codes` · `game-pause` · `music-toggle` · `status-panel` · `goal-counter` · `game-screen` · `keyboard-controls`.
- Уже запропоновано в корпусі: `+flip-screen-rooms` · `+fall-height-kill` · `+fixed-arc-jump` · `+guardian-blocks-exit` (Марія).
- **Нема** → пропозиції карток:
  - `+rope-swing` «Мотузка-маятник» · entities/move · 🥉.
  - `+ramp-walk` «Сходи-рампа: зайти — підйом, стрибок — крізь» · entities/move · 📎.
  - `+respawn-death-loop` «Відродження на вході й цикл смертей» · entities/death · 📎.
  - `+copy-protection-code` «Код з картки на старті» · interface/menus · 🌱.
  - `+game-clock-deadline` «Годинник гри обриває сесію» · game-logic/win · 🌱.

## Пропозиції до словників
- `+trigger:landed` — приземлення після падіння з висотою (смерть від падіння; вже пропоновано Manic Miner).
- `+window:code-card-entry` — ввід коду з паперової картки.
- `+card:rope-swing`, `+card:ramp-walk`, `+card:respawn-death-loop`, `+card:copy-protection-code`, `+card:game-clock-deadline` — див. вище.

## Джерела
- ⭐ [Wikipedia: Jet Set Willy](https://en.wikipedia.org/wiki/Jet_Set_Willy) — вільний маєток, сходи, мотузки, смерті, відродження, кодова картка, баги, сиквели.
- [SkoolKit: trivia](https://skoolkit.ca/disassemblies/jet_set_willy/reference/facts.html) — 1:00, мотузки, рампи, конвеєри, цикли смертей, WRITETYPER.
- [SkoolKit: таблиця предметів](https://skoolkit.ca/disassemblies/jet_set_willy/asm/41984.html) — 83 предмети.
- [SkoolKit: глосарій](https://skoolkit.ca/disassemblies/jet_set_willy/reference/glossary.html) — guardians, nasties.
- [Інструкція (WoS)](https://worldofspectrum.org/pub/sinclair/games-info/j/JetSetWilly.txt) — мета, Марія, клавіші.
- [C64-Wiki](https://www.c64-wiki.com/wiki/Jet_Set_Willy) — життя, клавіші, пауза.

## Непевне
- (?) Час старту годинника (7:00?) і точний склад HUD — бачив лише «кінець о 1:00» і «годинник і лічильник предметів».
- (?) Кількість життів у ZX-версії; C64-Wiki каже 9, без додаткових.
- (?) Межа висоти смертельного падіння.
- (?) Чи всі 83 записи таблиці досяжні (дубль у The Beach, кімната 47 не використовується).
- (?) Чи стріли летять лише горизонтально.
