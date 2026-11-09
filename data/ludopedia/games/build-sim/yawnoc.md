---
title: Yawnoc
slug: yawnoc
aka: [Yawnoc Jam Version]
family: build-sim
also: [roguelike]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: both
  goal: survive
year: 2024
platforms: [PC (Windows, Linux)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2824730/Yawnoc/", best: true, note: "опис: машини живуть за Life, Brian's Brain, LowDeath; правило міняється з просуванням; «необережна атака — смерть від власного творіння»; 50+ апгрейдів, зачарування між забігами, напарники; реліз 13.11.2024"}
  - {kind: itch, url: "https://dafluffypotato.itch.io/yawnoc", note: "DaFluffyPotato, pygame; ті самі тези, налаштовуване керування, інтерактивне навчання"}
  - {kind: itch, url: "https://dafluffypotato.itch.io/yawnoc-jam-version", note: "джем-версія (колаборація з Blackthornprod): клітини гинуть і народжуються без переміщення, подія HighLife від маяка, «ферма» з блоку 2×2"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Yawnoc+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [projectile-shot, shoot-modes, shoot-spread, hp-damage, enemy-waves, destroy-all-enemies, progress-acceleration, run-relics, shop-catalog, permadeath, tutorial-window, controls-remap, +cellular-automaton-rule, +rule-string, +zone-rulesets, +run-meta-carry, +ca-enemy-colony, +rule-swap-event, +weapon-enchant, +dash, +ally-recruit]
proposes: ["+effect:swap_ruleset", "+trigger:cycle_end", "+effect:dash", "+card:ca-enemy-colony", "+card:rule-swap-event", "+ui:cycle-indicator"]
author: opus
date: 2026-11-09
---

# Yawnoc — роглайт-шутер, де вороги — клітини автомата Конвея: вбиєш не ту клітину — колонія виросте ще більшою

## Суть
Top-down шутер-роглайт DaFluffyPotato (pygame, 2024; назва — «Conway» навпаки). Ліс захопили «машини» — живі клітини клітинного автомата: на кожному циклі вони не ходять, а гинуть і народжуються за правилом Life, Brian's Brain чи LowDeath, і правило міняється з просуванням. Гравець бігає й стріляє вільно поверх сітки; ядро для корпусу — **колонія ворогів як CA-стан**, де кожен постріл міняє наступне покоління: «необережна атака — і тебе вбʼє створіння, яке ти сам виростив». Це межа сімʼї: CA-шар — від [game-of-life](game-of-life.md), обгортка — бойова арена хвилями.

## Поле і час
- Шар машин — квадратна сітка клітин; аватар, кулі й інші вороги (напр., «стоноги») рухаються вільно поверх.
- Час реальний; машини оновлюються дискретними **циклами** з власним темпом (гравці просили індикатор «коли цикл» і повільніший цикл при великій колонії).
- Бої — обмежені зони з хвилями; рух машин «стрибками» без анімації — навмисно (клітина зникає тут і зʼявляється там).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | HP, зброя, здібності, ривок | вільний рух, стрільба, ривок |
| Машина-клітина | enemy | HP (?) | займає клітину; на циклі живе/гине/народжується за правилом зони; не переміщується |
| Колонія машин | zone | правило B/S | множина клітин; знищення частини змінює наступне покоління |
| Маяк | switch | випадковий | запускає подію HighLife |
| Стонога та ін. рухомі вороги | enemy | — | не CA; дріб їх «легше влучити» (слова автора) |
| Напарник (місцевий) | ally | — | приєднується, додає вогневої сили |
| Скриня · дроп здібності | pickup | — | предмети й здібності; дроп зникає з часом |
| Крамниця | static | ціни | купівля одного з двох однакових товарів часом здорожчує інший |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(cycle)` → ТО `custom: «нове покоління всіх машин зони за її правилом; клітини не рухаються — лише гинуть і народжуються»`.
- Life (B3/S23): КОЛИ `timer(cycle)` → ЯКЩО `free(x)` and `adjacent_count(x, machine, ==, 3)` → ТО `spawn(machine, x)`.
- Life: КОЛИ `timer(cycle)` → ЯКЩО `occupied(x, machine)` and `custom: «сусідів-машин не 2 і не 3»` → ТО `disappear(machine)`.
- Brian's Brain: КОЛИ `timer(cycle)` → ЯКЩО `state(x, off)` and `adjacent_count(x, on, ==, 2)` → ТО `set_state(x, on)`; далі сама «on → dying → off» (як у [brians-brain-seeds](brians-brain-seeds.md)); як три стани показано машинами — (?).
- КОЛИ `contact(projectile, machine)` → ТО `damage(machine, n)`; КОЛИ `hp_zero(machine)` → ТО `disappear(machine)`, `custom: «наступний цикл рахується вже без неї — довкола можуть народитися нові»`.
- КОЛИ `custom: «з блоку 2×2 знищено одну клітину»` → ТО `custom: «наступний цикл її відроджує (у порожньої клітини рівно 3 сусіди) — нескінченне "фермерство" ворогів»`; відповідь автора — складність росте з часом.
- КОЛИ `custom: «маяк спрацював (випадково)»` → ТО `custom: «подія HighLife — агресивніші правила росту (як B36/S23)»`.
- КОЛИ `level_start` → ЯКЩО `level(>=, n)` → ТО `custom: «машини переходять на інше правило (Life → Brian's Brain → LowDeath …)»`.
- КОЛИ `custom: «машина вражає гравця»` → ТО `damage(player, n)`; КОЛИ `hp_zero(player)` → ТО `lose` — забіг закінчено, зачарування зброї лишаються.
- КОЛИ `all_gone(machine)` → ТО `custom: «зону очищено → далі лісом»`.
- Перемога: очистити зони лісу · Поразка: смерть · Рахунок: — (?).

## Керування і ввід
- Клавіатура або геймпад (повна підтримка контролера), налаштовувані клавіші; рух, приціл, постріл, ривок (dash), здібності.
- Інтерактивне навчання на старті.

## Вікна, меню, HUD
- `game-screen`: ліс зверху, сітка машин, HP, зброя; `+ui:cycle-indicator` — коли наступний цикл (у джем-версії його бракувало).
- `shop-window` (ціни взаємозалежні), `tutorial-window`, `settings-window` (`options-controls`), `achievements-window` (16 у Steam).
- Вікно зачарувань (постійних між забігами) — `custom-window` (?).

## Фічі поза полем
- `meta-progression`: зачарування зброї переносяться між забігами («тисячі комбінацій»: снайперка кличе блискавку, дробовик — армію стоног).
- 50+ апгрейдів у забігу, багато зброї; напарники; досягнення й хмарні сейви Steam.
- Джем-версія (окрема сторінка itch) — прототип з Blackthornprod.

## Варіації й родичі
- **Осі варіацій «вороги як CA»**: правило (Life / HighLife / Brian's Brain / LowDeath) · хто змінює колонію (лише цикл / постріли гравця / події-маяки) · темп циклу (сталий / сповільнення при великій колонії) · шкода (клітина-ворог з HP / миттєва смерть клітини).
- Родичі в корпусі: [game-of-life](game-of-life.md), [brians-brain-seeds](brians-brain-seeds.md), [critters-block-ca](critters-block-ca.md); блок 2×2 як «натюрморт» Life, що відновлюється з трьох клітин, — класика Life.

## Цікавинки для курсу
- Вороги як шар CA поверх вільного руху: двигун Life + стрілянина, що видаляє клітини — 🥉.
- Індикатор і таймер циклу; сповільнення циклу пропорційно розміру колонії — 📎.
- Перемикання правила за подією/рівнем (Life → HighLife) без зміни двигуна — 🌱 (рядок B/S як параметр).
- Детектор «ферм»: знайти натюрморти, що відроджуються після видалення клітини, — 🥈.

## Мапа на каталог
- Є: `projectile-shot` · `shoot-modes` + `shoot-spread` (дробовик) · `hp-damage` · `enemy-waves` · `destroy-all-enemies` · `progress-acceleration` (складність росте з часом) · `run-relics` (апгрейди) · `shop-catalog` · `permadeath` · `tutorial-window` · `controls-remap`.
- Перевикористано з корпусу: `+cellular-automaton-rule`, `+rule-string`, `+zone-rulesets`, `+run-meta-carry`.
- **Нема** → пропозиції карток:
  - `+ca-enemy-colony` «Вороги — живі клітини CA, оновлюються циклами» · entities/spawn · 🥉 · слоти {rule: B/S, cycle}.
  - `+rule-swap-event` «Подія тимчасово міняє правило CA» · game-logic · 🌱.
  - `+weapon-enchant` «Постійні модифікатори зброї між забігами» · game-logic/economy · 📎.
  - `+dash` «Ривок з перезарядкою» · entities/move · 🌱.
  - `+ally-recruit` «Напарник приєднується в забігу» · entities/spawn · 📎.

## Пропозиції до словників
- `+effect:swap_ruleset` — замінити правило автомата (уже в корпусі).
- `+trigger:cycle_end` — кінець циклу оновлення CA в реальному часі (уже в корпусі).
- `+effect:dash` — ривок (уже в корпусі).
- `+ui:cycle-indicator` — показ, коли наступне покоління.
- `+card:ca-enemy-colony`, `+card:rule-swap-event` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Yawnoc](https://store.steampowered.com/app/2824730/Yawnoc/) — опис гри: правила Life, Brian's Brain, LowDeath, зміна правил з просуванням, «смерть від власного творіння», зброя, 50+ апгрейдів, зачарування, напарники, реліз 13.11.2024.
- [itch.io: Yawnoc](https://dafluffypotato.itch.io/yawnoc) — pygame, Windows/Linux, клавіатура/геймпад, налаштовуване керування, інтерактивне навчання.
- [itch.io: Yawnoc Jam Version](https://dafluffypotato.itch.io/yawnoc-jam-version) — коментарі автора: клітини «гинуть і народжуються без переміщення», подія HighLife від маяка, «ферма» з блоку 2×2 і зростання складності, прохання про індикатор циклу.
- YouTube: пошук «Yawnoc gameplay».

## Непевне
- (?) Правило LowDeath — за памʼяттю B368/S238 (каталог правил Mirek's Cellebration); сайт не відкрився, LifeWiki — 403.
- (?) Як три стани Brian's Brain і «вмираючий» стан показано машинами; чи мають клітини HP, чи гинуть від одного влучання.
- (?) Як машини шкодять гравцеві (контакт, постріли) і чи є рахунок — у джерелах не сказано.
- (?) Порядок правил по зонах лісу і кількість зон — не знайшов.
