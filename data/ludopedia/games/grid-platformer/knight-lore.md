---
title: Knight Lore
slug: knight-lore
aka: [KnightLore]
family: grid-platformer
also: [thinky]
klass: avatar
axes:
  field: iso
  time: realtime
  opponent: none
  info: partial
  random: none
  goal: collect
year: 1984
platforms: [ZX Spectrum, Amstrad CPC, BBC Micro, MSX, Famicom Disk System]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Knight_Lore", best: true, note: "128 кімнат, Filmation, день/ніч і перевертень, 40 днів, 14 предметів у казан, блоки, 5 життів, рахунок"}
  - {kind: other, url: "https://www.everygamegoing.com/larticle/Knight-Lore-000/31473", note: "огляд 1984: до 3 предметів, казан показує потрібний, вороги, пастки, тонучі плити"}
  - {kind: other, url: "https://rk.nvg.ntnu.no/sinclair/instructions/kghtlore.html", note: "інструкція: клавіші поворот/вперед/стрибок/взяти, режими керування, пастки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Knight+Lore+1984+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [inventory, inventory-items, inventory-limit, item-pickup, gravity-fall, push-object, touch-death, environment-death, player-death, time-out, enemy-patrol, chase-player, timed-despawn, carrier-platform, hidden-under-block, game-screen, status-panel, keyboard-controls, +day-night-cycle, +form-shift, +requested-item-sequence, +stack-to-climb, +tank-controls, +flip-screen-rooms]
proposes: ["+trigger:cycle(phase)", "+effect:switch_form", "+card:day-night-cycle", "+card:form-shift", "+card:requested-item-sequence", "+card:tank-controls", "+axis:control=tank"]
author: opus
date: 2026-11-09
---

# Knight Lore — ізометричний замок зі 128 кімнат, де Сабремен щоночі стає перевертнем і носить чарівнику предмети, які просить казан

## Суть
Перша гра на рушії Filmation: замок Melkhior з 128 ізометричних кімнат-екранів. Сабремен збирає предмети (до трьох за раз) і кидає в казан той, чий образ зараз показано над ним; потрібно 14 предметів поспіль за 40 днів. Кожної ночі він перетворюється на перевертня: стрибає вище, але деякі істоти й сам казан атакують лише перевертня. Кімнати — головоломки з камʼяних блоків: штовхати, ставити один на одного, ловити момент на плитах, що тонуть.

## Поле і час
- Мапа — граф кімнат (128), кожна — нескролінгова ізометрична коробка, монохромна.
- Рух плавний, але кімнати складені з однакових кубів-блоків; висота — третя вісь (блоки ставлять один на одного).
- Real-time; гравітація; годинник днів: сонце/місяць унизу екрана, цикл день → ніч.
- Ліміт — 40 днів і ночей; анімація сповільнюється, коли в кімнаті багато руху.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Сабремен (людина) | player | 5 життів; несе ≤3 | поворот ліво/право, вперед, стрибок, взяти/покласти |
| Сабремен (перевертень) | player | вищий стрибок | ніччю; деякі вороги атакують лише його; у кімнату казана не можна |
| Предмет-чар (кулі, зілля, чоботи, кристали, келих…) | pickup | тип | бере в інвентар (≤3); потрібен у казані у певний момент |
| Казан | static | показує потрібний предмет | приймає лише показаний; спалах заклинання атакує (?) перевертня |
| Чарівник Melkhior | neutral | — | ходить навколо казана; заважає підійти (?) |
| Камʼяний блок | object | — | платформа; частину штовхають гравець чи вороги; ставиться на інший |
| Блок, що рухається сам | terrain | маршрут | везе Сабремена між частинами кімнати |
| Блок, що тоне/зникає | terrain | — | осідає/зникає, коли на нього стрибнути; під ним буває предмет |
| Привид | enemy | швидкий | проноситься через кімнату |
| Броньований вартовий | enemy | — | ходить прямими лініями |
| Біла куля | enemy | — | відскакує по кімнаті |
| Шипи, міни | hazard | — | дотик — смерть |
| Колючі кулі зі стелі | hazard | — | падають; деякі предмети-пастки обвалюють їх, перекриваючи вихід |
| Бонус-життя | pickup | +1 життя | лежить у кімнатах |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ТО `rotate(sabreman, 90)` (?) — повертання на місці; КОЛИ `input(forward)` → ЯКЩО `free(next)` → ТО `move(sabreman, facing)`.
- КОЛИ `input(jump)` → ТО `custom: «стрибок; у перевертня — вищий»`; без опори — `fall(sabreman)`.
- КОЛИ `input(pickup)` → ЯКЩО `occupied(here, pickup)` і `counter(carried, <, 3)` → ТО `pickup(sabreman, item)`; інакше `custom: «покласти предмет»`.
- КОЛИ `contact(sabreman, block)` → ЯКЩО `free(behind)` → ТО `push(block)`.
- КОЛИ `enter(sabreman, sinking_block)` → ТО `custom: «блок осідає / зникає»`; ЯКЩО під ним предмет → `reveal(cells)`.
- КОЛИ `timer(every)` → ТО `custom: «сонце/місяць зсувається; на сході місяця — перевтілення»`, `transform(sabreman, werewolf)`; на світанку — назад.
- КОЛИ `contact(enemy, sabreman)` → ЯКЩО `custom: «ворог із тих, що полюють лише на перевертня»` і `not state(sabreman, werewolf)` → ТО `custom: «людину не чіпає»`.
- КОЛИ `contact(sabreman, hazard|enemy)` → ТО `lives(-1)`, `respawn(sabreman, room_entry)` (?).
- КОЛИ `custom: «Сабремен у казані з предметом, який зараз показано»` → ЯКЩО `has(sabreman, shown_item)` → ТО `take(sabreman, item)`, `counter(brew, +1)`, `custom: «казан показує наступний»`.
- КОЛИ `enter(sabreman, cauldron_room)` → ЯКЩО `state(sabreman, werewolf)` → ТО `custom: «казан атакує»`, `lives(-1)` (?) — інструкція забороняє заходити перевертнем.
- КОЛИ `picked(sabreman, trap_item)` → ТО `spawn(spiked_balls)` — обвал перекриває вихід.
- КОЛИ `counter(brew, =, 14)` → ТО `win`.
- КОЛИ `counter(days, =, 40)` → ТО `lose` — лишається перевертнем назавжди.
- КОЛИ `counter(lives, =, 0)` → ТО `game_over`.
- Перемога: 14 предметів у казані до кінця 40 днів. Поразка: 0 життів або час вийшов. Рахунок: за рештою часу й часткою виконаного квесту.

## Керування і ввід
- «Танкове» керування: дві клавіші повертають героя, одна — вперед, окремо стрибок і взяти/покласти; ряди клавіатури продубльовані.
- Режими: клавіатура, Kempston, курсорні; для джойстика — опція «directional movement» (8 напрямків ізометрії).
- Скинути предмет у казан: вибрати його «позицію скидання» у панелі стану й перестрибнути через край казана.

## Вікна, меню, HUD
- `main-menu` (?): вибір керування (Keyboard / Kempston / Cursor) і старт.
- `game-screen`: ізометрична кімната + `status-panel`: життя, 3 слоти предметів з позицією скидання, вікно сонце/місяць, лічильник днів (?).
- `end-screen`: рейтинг за часом і відсотком виконаного.

## Фічі поза полем
- Збережень нема; повторне проходження — щоб уміститись у менше днів.
- Інструкція — лише вірш на касеті: правила гравець відкриває сам.

## Варіації й родичі
- Alien 8 (1985), Nightshade, Pentagram — Ultimate на Filmation; Batman і [Head over Heels](head-over-heels.md) — Filmation II.
- [Solstice](solstice.md) — свідомий NES-нащадок «у стилі Knight Lore»; інвентар-ключі — [Treasure Island Dizzy](treasure-island-dizzy.md).
- Осі: **хто змінює тіло** (час доби / предмет / кнопка); **черга вимог** (довільний порядок / показана ціль); **керування** (танкове / за екраном).

## Цікавинки для курсу
- Цикл день/ніч, що змінює форму героя й відношення ворогів до нього — 📎.
- Казан із «поточним запитом»: приймає лише показаний предмет, далі — наступний — 🌱.
- Будувати сходи зі штовханих блоків у 3D-сітці висот — 🥈.
- Танкове керування (поворот + вперед) проти екранного — 🌱.
- Ізометричний рендер з порядком малювання (хто перед ким) — 🥈.
- Глобальний ліміт у днях і фінальний рейтинг за часом і прогресом — 🌱.

## Мапа на каталог
- Є: `inventory` · `inventory-items` · `inventory-limit` (3) · `item-pickup` · `gravity-fall` · `push-object` (блоки) · `touch-death` · `environment-death` (шипи, кулі) · `player-death` (5 життів) · `time-out` (40 днів) · `enemy-patrol` (вартові) · `chase-player` (?) · `timed-despawn` (тонучі плити) · `carrier-platform` (блоки, що їздять) · `hidden-under-block` · `game-screen` · `status-panel` · `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+day-night-cycle` «Цикл день/ніч змінює правила поля» · game-logic/time · 📎.
  - `+form-shift` «Герой змінює форму з іншими вміннями й вразливостями» · entities/state · 📎.
  - `+requested-item-sequence` «Приймач просить предмети по одному в показаному порядку» · game-logic/win · 🌱.
  - `+stack-to-climb` «Поставити обʼєкт на обʼєкт, щоб вилізти вище» · entities/move · 🥉.
  - `+tank-controls` «Поворот на місці + рух уперед» · interface/input · 🌱.
  - `+flip-screen-rooms` «Світ з кімнат-екранів» · levels/progression · 📎.

## Пропозиції до словників
- `+trigger:cycle(phase)` — змінилась фаза циклу (день → ніч), Knight Lore.
- `+effect:switch_form(a, form)` — A змінює форму з іншим набором умінь (перевертень).
- `+axis:control=tank` — значення осі `control`: поворот + вперед.
- `+card:day-night-cycle`, `+card:form-shift`, `+card:requested-item-sequence`, `+card:tank-controls` — див. вище.

## Джерела
- ⭐ [Wikipedia: Knight Lore](https://en.wikipedia.org/wiki/Knight_Lore) — 128 кімнат, Filmation, перевертень, 40 днів, 14 предметів, блоки, 5 життів, рахунок.
- [Everygamegoing: огляд PCG 1984](https://www.everygamegoing.com/larticle/Knight-Lore-000/31473) — до 3 предметів, казан показує предмет, привиди/вартові/кулі, шипи, кулі зі стелі, тонучі плити.
- [Інструкція ZX Spectrum](https://rk.nvg.ntnu.no/sinclair/instructions/kghtlore.html) — клавіші, режими керування, бонус-життя, міни, блоки, що рухаються магією.
- YouTube: пошук «Knight Lore 1984 gameplay».

## Непевне
- (?) Поворот — на 90° чи на 45°; що саме робить «directional movement».
- (?) Кількість предметів: Wikipedia — 14, одна інструкція — 6 (можливо, 14 вкидань із 6–7 типів предметів).
- (?) Що відбувається при смерті — повтор кімнати з входу.
- (?) Чи шкодить чарівник сам і як саме атакує казан перевертня.
- (?) Склад HUD і меню — з памʼяті.
