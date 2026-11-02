---
title: Caves of Qud
slug: caves-of-qud
family: roguelike
also: [build-sim]
klass: avatar
axes:
  field: layers
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2015
platforms: [PC, Mac, Linux, Switch]
links:
  - {kind: fandom, url: "https://wiki.cavesofqud.com/wiki/Liquids", best: true, note: "офіційна вікі: драми, калюжа/басейн/глибина, змішування, випаровування, слизьке/липке"}
  - {kind: fandom, url: "https://wiki.cavesofqud.com/wiki/Zone", note: "зона, парасанг 3×3, карта світу 80×25 парасангів, «загубитись»"}
  - {kind: fandom, url: "https://wiki.cavesofqud.com/wiki/Temperature", note: "пороги займання/замерзання/випаровування, дрейф до 25°"}
  - {kind: fandom, url: "https://wiki.cavesofqud.com/wiki/Burning", note: "шкода горіння за перевищенням порога"}
  - {kind: fandom, url: "https://wiki.cavesofqud.com/wiki/Electrical_Generation", note: "дуги: стрибки по сусідах, пріоритет калюж, крізь стіни"}
  - {kind: fandom, url: "https://wiki.cavesofqud.com/wiki/Mutations", note: "очки мутацій, рівні, приклади, що міняють правила"}
  - {kind: fandom, url: "https://wiki.cavesofqud.com/wiki/Reputation", note: "пороги репутації фракцій і їх ефект"}
  - {kind: other, url: "https://www.roguebasin.com/index.php/Caves_of_Qud", note: "RogueBasin: огляд систем"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Caves_of_Qud", note: "історія, early access 2015, 1.0 у 2024"}
  - {kind: official, url: "http://www.cavesofqud.com/"}
  - {kind: steam, url: "https://store.steampowered.com/app/333640/Caves_of_Qud/"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=caves+of+qud+liquids+fire+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-8dir, hp-damage, inventory, inventory-items, inventory-limit, item-pickup, dungeon-generation, chase-bfs, floor-types, environment-death, temporary-modes, round-currency, shop-catalog, player-death, save-autosave, checkpoint, console-render, gui-render, cell-click, interaction-table, cell-transform, +permadeath, +hunger-clock, +item-identification, +fire-spread, +gas-diffusion, +liquid-volume, +liquid-mixing, +temperature-field, +electric-arc, +mutation-tree, +cybernetic-slots, +faction-reputation, +world-map-travel, +procedural-history, +legendary-variant, +dig-walls, +rewind-checkpoint, +auto-explore, +tinkering-craft]
proposes: ["+trigger:threshold(temp, t)", "+trigger:poured", "+cond:volume(op, n)", "+cond:conductive", "+cond:reputation(faction, op, n)", "+cond:material(x)", "+effect:spread", "+effect:ignite", "+effect:mix(liquid)", "+effect:arc(n)", "+effect:evaporate", "+effect:heat(±t)", "+effect:reputation(faction, ±n)", "+effect:identify", "+role:liquid", "+role:neutral", "+window:inventory-window", "+window:journal-window", "+window:factions-window", "+window:skills-window", "+window:map-window", "+window:dialogue-window", "+ui:status-line", "+ui:temperature-readout", "+feature:mode-roleplay", "+feature:permadeath", "+feature:auto-explore", "+axis:session=run"]
author: opus
date: 2026-11-02
---

# Caves of Qud — світ-симуляція, де в кожній клітині лежить рідина, температура й матеріал

## Суть
Мутант або «чистий» людина (True Kin) мандрує постапокаліптичним світом-сіткою з екранів-зон, бʼється, торгує водою, виконує квести й копає вглиб. Ядро для корпусу — **клітинна фізика**: рідини вимірюються в драмах, розливаються, змішуються й випаровуються; кожен обʼєкт має температуру з порогами займання/замерзання; електрика стрибає по провідних сусідах і віддає перевагу калюжам. Мутації й кібернетика — це не числові бонуси, а **зміни правил** (проходити крізь стіни, копати, відмотати час). Фракції памʼятають, що ти зробив, і через репутацію міняють, хто ворог.

## Поле і час
- **Зона** — один екран 80×25 клітин (?) (класичний розмір консолі); зони стикуються краями. **Парасанг** — 3×3 зони = одна клітина карти світу; карта світу — 80×25 парасангів (вікі). Під кожною зоною — шари вглиб («many, many layers downward»), тож `field: layers`.
- Карта світу — окремий режим: крок по ній коштує 300–900 ходів за типом місцевості; шанс «загубитись» 12 % (10 % у соляних дюнах) кидає в зону, яку перетинаєш.
- Клітина має шари: місцевість (підлога/стіна з матеріалом) · рідина з обʼємом і сумішшю · обʼєкти/предмети · істота · газ (?).
- Час покроковий з енергією: швидкість (Quickness) визначає, як часто ходить істота (?); температура кожного обʼєкта дрейфує до навколишньої щоходу.
- Видимість — поле зору й освітлення (`info: hidden`); поверхня частково рукотворна, решта й підземелля — генеровані (`random: both`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | генотип (Mutant / True Kin), каста/покликання, атрибути, HP, Quickness, температура, голод/спрага | рух 8 напрямків, бій, вміння мутацій, торгівля водою |
| Істота фракції | enemy / neutral | фракція, рівень, мутації | ставлення залежить від репутації гравця з фракцією |
| Легендарна істота | boss | пурпурове імʼя, +1 атрибути, ×2 HP, рівень ×1.5, XP = рівень×250, 0–2 фіз. + 0–2 мент. мутацій | фракції її люблять/ненавидять — вбивство/ритуал міняє репутацію |
| Калюжа / басейн рідини | terrain | драми (<200 калюжа, 200–1999 вбрід, ≥2000 — плавати), суміш | змішується з сусідніми, обливає того, хто стоїть, випаровується |
| Вода | terrain | негорюча; чиста — слабкий провідник, з домішками — добрий | гасить/охолоджує (?), провідник дуг |
| Сіль | terrain | — | робить рідини солонуватими; великий обʼєм замерзає в кам'яну сіль |
| Кислота | hazard | — | шкода при контакті; пропалює органічні контейнери |
| Лава | hazard | 1000°, світиться | нищить контейнери, підпалює непридатну тару |
| Олія | terrain | найлегше займається; слизька | паливо для вогню; посковзнутись при провалі кидка |
| Слиз / чорнило / гель | terrain | слизькі | ковзання при провалі збереження; слиз — п'ється з Confusion 5 |
| Мед / смола / віск / асфальт | terrain | липкі | застрягнути до 12 ходів, кожну клітину вибиратись окремо |
| Трава / рослини | terrain | горючі | займаються від тепла (?) |
| Стіна | static | матеріал | непрохідна; Burrowing Claws — 4 удари прокопують; Phasing — прохід |
| Газ (хмара) | hazard | тип, концентрація | розходиться по сусідах (?), впливає на тих, хто в ньому |
| Контейнер (бурдюк) | container | 64 драми | налити/вилити/випити; вода = гроші |
| Артефакт | pickup | невідомий | треба ідентифікувати перед використанням |
| Ніша «становлення» (becoming nook) | static | — | встановлення/зняття кібер-імплантів, підвищення ліцензії |
| Торговець | neutral | товар | торгівля на воду; ціна залежить від Ego і репутації |
| Сходи / вхід униз | static | — | перехід між шарами |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(pour, n)` → ТО `spawn_at(liquid n drams, cell)`; КОЛИ дві рідини `adjacent`/в одній клітині → ТО `mix(liquid)`: суміш отримує всі префікси й підсумовує ефекти («inky sugary bloody water»).
- КОЛИ `counter(volume, <, 200)` → калюжа (ходити); `200..1999` → вбрід; `>= 2000` → `custom: «плавати»`.
- КОЛИ `tick` → ЯКЩО суміш і `volume(<=, 199)` → ТО кожен драм `evaporate` з ймовірністю = зважена за обʼємом випаровуваність (олія/лава/сіль = 0).
- КОЛИ `enter(a, slippery)` (гель, чорнило, олія, слиз, лід із них) → ЯКЩО `not prob(save)` → ТО `slide(a)`.
- КОЛИ `enter(a, sticky)` (мед, смола, віск, асфальт) → ТО `set_state(a, stuck, ≤12)`.
- КОЛИ `contact(a, acid)` → ТО `damage(n)`; органічний контейнер з кислотою → `destroyed`.
- КОЛИ `tick` → ТО температура кожного обʼєкта, відмінна від 25° більш ніж на 5°, зсувається до 25° на `max(diff/50, 5)`.
- КОЛИ `threshold(temp, ≥ flame_temp)` (типово 350°) → ТО `ignite(a)`; щоходу `damage(1..6)` за перевищенням (1–100° → 1; 901°+ → 5–6).
- КОЛИ горить обʼєкт → ТО `heat(adjacent)` → сусідні горючі (трава, олія) `ignite` — `fire-spread` (?) (вікі «Temperature» про поширення мовчить).
- КОЛИ `threshold(temp, ≤ 0°)` → ТО `speed(a, −k)` пропорційно холоду; `≤ −100°` → `set_state(a, frozen)`: жодних фізичних дій, ментальні можна.
- КОЛИ `threshold(temp, ≥ 10000°)` → ТО `destroyed(a)` (випаровування).
- КОЛИ `input(discharge, target adjacent)` → ТО `damage(1d4 × charge/1000)`; далі `arc(n)`: кожні 1000 заряду — стрибок на випадкового провідного сусіда цілі; **калюжі мають пріоритет перед істотами**; дуга йде крізь стіни й обʼєкти краще, ніж повітрям; може влучити в союзника.
- КОЛИ `enter(world_map step)` → ТО `custom: «+300..900 ходів»`; `rng(0.12)` → `custom: «загубився → зона під тобою»`.
- КОЛИ `input(spend mutation point)` → ЯКЩО `level(mut) < floor(L/2)+1` і `≤ 10` → ТО `custom: «рівень мутації +1»`; 4 очки → `choose(3 random mutations)`.
- КОЛИ `input(precognition)` → ТО `checkpoint`; пізніше — `custom: «відмотати стан до точки»` (cooldown 500).
- КОЛИ `input(install implant)` біля ніші → ЯКЩО `count(license_points, >=, cost)` і слот частини тіла вільний → ТО `custom: «імплант встановлено»`.
- КОЛИ `died(legendary)` від гравця → ТО `reputation(faction_that_hates, +)`, `reputation(faction_that_loves, −)`.
- КОЛИ `reputation(faction, op, n)`: ≤ −600 усі ворожі · −599..−250 нападають агресивні · −249..249 нейтрально · 250..599 агресивні не нападають, пускають у святині · ≥ 600 «свій».
- КОЛИ `counter(thirst|hunger, >, t)` → ТО `custom: «штрафи → шкода»` (?).
- КОЛИ `hp_zero(player)` → ТО `lose` (Classic); у Roleplay — повернення до точки збереження в поселенні (?).
- Перемога: сюжетна лінія має фінал, але гра відкрита (`goal: state` умовно). Поразка: смерть (permadeath у Classic). Рахунок: очки забігу в «Tombstone»/хроніці (?).

## Керування і ввід
- Клавіатура: numpad/стрілки — 8 напрямків; `+`/`−` — вниз/вгору шарами й на карту світу; Look-режим (`L`) — опис клітини.
- Меню дій над предметом/рідиною: налити, наповнити, випити, кинути; активовані вміння — гарячі клавіші.
- Миша: клік по клітині — автошлях (?); auto-explore і travel.
- Діалоги з NPC: водний ритуал, торгівля, квести — вибір реплік.

## Вікна, меню, HUD
- `game-screen` — зона 80×25 + бічна панель: `hp-bar`, `stat-panel`, температура, `hunger-bar`/спрага, Quickness, `message-log`, `minimap` (?).
- `inventory-window` + екіпірування за частинами тіла (руки, голова, ноги — кількість залежить від мутацій).
- `skills-window` / сторінка мутацій і кібернетики; `character-select`/творення: генотип → покликання/каста → атрибути → мутації або імплант.
- `journal-window` — локації, хроніка, історія султанів, рецепти, секрети.
- `factions-window` — репутація з кожною фракцією.
- `map-window` — карта світу (окремий режим руху).
- `dialogue-window` — розмова, водний ритуал; `shop-window` — торгівля на драми води.
- `custom-window` Tinkering — розбирання артефактів на біти, збирання предметів за схемою (?).
- `mode-select` — Classic / Roleplay / Wander / Daily (?); `end-screen` — надгробок з хронікою; `settings-window`, `main-menu`.

## Фічі поза полем
- `permadeath` (Classic), `mode-roleplay` — чекпоінти в поселеннях (?), Wander — без XP за вбивства (?), `mode-daily` (?).
- `auto-explore`, `travel`, `autosave`; `seed-input` (?).
- Процедурна історія: 5 султанів, біографії й реліквії сіл генеруються щозабігу, джерела можуть суперечити (WP).
- `mod-support` (XML-моди) (?), тайлсет і ASCII-режим (`theme-select`).

## Варіації й родичі
- Dwarf Fortress (температура, рідини, історія), Brogue (вогонь і газ на клітинах), Noita (піксельна фізика), Cataclysm: DDA (світ з зон).
- Осі варіацій **клітинної фізики**: рідина булева (вода/нема) / з обʼємом / з сумішшю · температура як стан (горить/ні) / як число з порогами · провідність — нема / сусіди / граф провідників з пріоритетами.
- Осі **будови персонажа**: числа (сила +1) / правила (прохід крізь стіни, відмотка часу, додатковий удар).

## Цікавинки для курсу
- Рідина як обʼєм у драмах з порогами глибини й змішуванням назв/ефектів — 🥈 (структура «суміш = словник компонент→обʼєм»).
- Температура кожного обʼєкта з дрейфом до 25° і порогами 350° / 0° / −100° / 10000° — 🥈 (просте поле чисел + події перетину порогів).
- Дуга електрики: N стрибків по провідних сусідах, калюжі першими — 🥇 (пошук на графі з пріоритетами й випадковістю, легко зламати союзників).
- Вогонь, що перекидається на траву й олію — 🥉 (клітинний автомат поширення).
- Репутація як таблиця порогів → ставлення NPC — 📎.
- Precognition: точка збереження стану й відмотка — 🥉 (`state-as-data` у дії).
- Зона/парасанг/карта світу як три масштаби з «загубитись» при переході — 🥈.

## Мапа на каталог
- Є: `move-8dir` · `hp-damage` · `inventory` + `inventory-items` + `inventory-limit` (вага) · `item-pickup` · `dungeon-generation` · `chase-bfs` · `floor-types` (слизьке/липке) · `environment-death` · `temporary-modes` · `round-currency` (драми води) · `shop-catalog` · `player-death` · `save-autosave` · `checkpoint` (Roleplay) · `console-render`/`gui-render` · `keyboard-controls` · `cell-click` · `interaction-table` (рідина × обʼєкт) · `cell-transform` (сіль → кам'яна сіль, копання стін).
- **Нема** → пропозиції карток:
  - `+liquid-volume` «Рідина з обʼємом і порогами глибини» · entities/interact · 🥈 · слоти {thresholds}.
  - `+liquid-mixing` «Змішування рідин з ефектами компонент» · entities/interact · 🥈.
  - `+temperature-field` «Температура обʼєктів з порогами й дрейфом» · entities/state · 🥈.
  - `+electric-arc` «Дуга по провідних сусідах з пріоритетом» · entities/combat · 🥇 · слоти {arcs, priority}.
  - `+fire-spread`, `+gas-diffusion` — як у Brogue.
  - `+mutation-tree` «Мутації-правила з очками й рівнями» · entities/state · 🥉.
  - `+cybernetic-slots` «Імпланти за частинами тіла з ліміт-очками» · entities/state · 📎.
  - `+faction-reputation` «Репутація з фракціями й пороги ворожості» · game-logic/opponent · 📎.
  - `+world-map-travel` «Карта світу з переходом у зони» · levels/generation · 🥉.
  - `+procedural-history` «Генерована історія світу» · levels/generation · 👑.
  - `+legendary-variant` «Посилена іменна версія звичайного ворога» · entities/spawn · 🌱.
  - `+dig-walls` «Прокопування стін» · entities/legality · 📎.
  - `+rewind-checkpoint` «Відмотка до збереженої точки як вміння» · entities/state · 🥉.
  - `+tinkering-craft` «Розібрати предмет на ресурси, зібрати за схемою» · game-logic/economy · 🥉.
  - `+permadeath`, `+hunger-clock`, `+item-identification`, `+auto-explore` — як у Rogue/Brogue.

## Пропозиції до словників
- `+trigger:threshold(temp, t)` — значення перетнуло поріг (займання, замерзання, випаровування); `+trigger:poured` — рідину вилито в клітину.
- `+cond:volume(op, n)` — обʼєм рідини в клітині; `+cond:conductive` — обʼєкт проводить струм; `+cond:reputation(faction, op, n)`; `+cond:material(x)` — матеріал стіни/контейнера (органічний → кислота пропалює).
- `+effect:spread`, `+effect:ignite`, `+effect:identify` — як у Brogue; `+effect:mix(liquid)` — злити рідини в суміш; `+effect:arc(n)` — ланцюговий стрибок шкоди; `+effect:evaporate`; `+effect:heat(±t)`; `+effect:reputation(faction, ±n)`.
- `+role:liquid` — terrain з обʼємом і складом (інакше рідину не описати); `+role:neutral` (⏳) — вжито.
- `+window:inventory-window`, `+window:map-window`, `+window:dialogue-window` (⏳) · `+window:journal-window` — журнал локацій/хронік · `+window:factions-window` · `+window:skills-window` — мутації/навички.
- `+ui:status-line`, `+ui:temperature-readout` — температура героя в панелі.
- `+feature:mode-roleplay` — смерть повертає до чекпоінта поселення; `+feature:permadeath`, `+feature:auto-explore`.
- `+axis:session=run`.

## Джерела
- ⭐ [Qud wiki: Liquids](https://wiki.cavesofqud.com/wiki/Liquids) — драми, пороги 200/2000, змішування, випаровування, слизьке/липке, кислота, лава.
- [Qud wiki: Zone](https://wiki.cavesofqud.com/wiki/Zone) — зона, парасанг 3×3, карта 80×25 парасангів, час подорожі, «загубитись».
- [Qud wiki: Temperature](https://wiki.cavesofqud.com/wiki/Temperature) · [Burning](https://wiki.cavesofqud.com/wiki/Burning) — пороги, дрейф, шкода горіння.
- [Qud wiki: Electrical Generation](https://wiki.cavesofqud.com/wiki/Electrical_Generation) — дуги, калюжі першими, крізь стіни.
- [Qud wiki: Mutations](https://wiki.cavesofqud.com/wiki/Mutations) · [Cybernetics](https://wiki.cavesofqud.com/wiki/Cybernetics) · [Reputation](https://wiki.cavesofqud.com/wiki/Reputation) · [Legendary](https://wiki.cavesofqud.com/wiki/Legendary).
- [RogueBasin](https://www.roguebasin.com/index.php/Caves_of_Qud) — огляд генотипів, 21 дерево навичок, підземелля.
- [Wikipedia](https://en.wikipedia.org/wiki/Caves_of_Qud) · [Офіційний сайт](http://www.cavesofqud.com/) · [Steam](https://store.steampowered.com/app/333640/Caves_of_Qud/).

## Непевне
- (?) Розмір зони 80×25 клітин — класичний, у прочитаних сторінках прямо не названо (вікі дає 80×25 для карти світу в парасангах).
- (?) Механіка поширення вогню на сусідів (трава, олія) — вікі-сторінки Temperature/Burning про неї мовчать; описано з памʼяті.
- (?) Енергетична система ходу (Quickness 100 = норма), гази, голод/спрага і їх штрафи — з памʼяті/RogueBasin коротко.
- (?) Режими Classic/Roleplay/Wander/Daily і їх точні правила; Tinkering-вікно; клік-автошлях — з памʼяті.
- (?) Рік у шапці — early access 2015; розробка з 2007, 1.0 — 5 грудня 2024.
