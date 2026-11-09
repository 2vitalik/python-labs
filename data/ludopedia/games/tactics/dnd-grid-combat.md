---
title: D&D grid combat (Dungeons & Dragons 5e)
slug: dnd-grid-combat
aka: [Dungeons & Dragons, D&D, DnD, 5e, Підземелля і дракони, SRD 5.1 combat]
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: coop
  info: hidden
  random: runtime
  goal: state
year: 1974
platforms: [board, VTT (Roll20, Foundry, D&D Beyond Maps)]
links:
  - {kind: other, url: "https://www.dndbeyond.com/sources/dnd/basic-rules-2014/combat", best: true, note: "Basic Rules 2014, розділ Combat: ініціатива, дія/бонус/реакція, рух, розміри, варіант сітки 5 футів, укриття, opportunity attack, grapple/shove, смерть"}
  - {kind: other, url: "https://www.dndbeyond.com/sources/dnd/basic-rules-2014/spellcasting", note: "Basic Rules 2014, Spellcasting: шаблони площ (cone, cube, cylinder, line, sphere), точка походження, чистий шлях, концентрація"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dungeons_%26_Dragons_gameplay", note: "d20, раунд 6 секунд, ініціатива, AC і HP по редакціях, death saves у 5e"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=DnD+5e+grid+combat+explained", note: "пошук; пояснення бою на сітці"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=attacks+of+opportunity+explained", note: "пошук; opportunity attack"}
stage: v1
coverage: 55
mechanics: [hp-damage, melee-vs-ranged, line-of-sight-attack, explode-area, multi-cell-size, floor-types, impassable-cells, status-effects, unit-xp-skills, inventory-items, reachable-highlight, threat-range, fog-of-war, turn-enforcement, rule-variants, hot-seat, online-multiplayer, +initiative-order, +action-economy, +opportunity-attack, +reach, +area-templates, +cover-system, +flanking, +advantage-disadvantage, +dice-roll-vs-target, +difficult-terrain, +grapple-shove, +death-saves, +ready-action]
proposes: ["+trigger:leave_reach", "+trigger:round_start", "+trigger:readied", "+cond:in_reach", "+cond:cover", "+cond:flanked", "+cond:roll_vs", "+effect:roll_dice", "+effect:reaction_attack", "+effect:set_advantage", "+effect:prone", "+effect:grapple", "+effect:death_save", "+ui:initiative-tracker", "+ui:aoe-template", "+ui:dice-roller", "+ui:condition-tokens", "+ui:measure-ruler", "+window:character-sheet", "+window:dm-screen", "+role:dm", "+axis:referee=human"]
author: opus
date: 2026-11-09
---

# D&D grid combat — бій «Підземель і драконів» на сітці 5 футів: дія, бонусна дія, реакція й атака при виході з досяжності

## Суть
Не відеогра, а **система бою** настільної рольової гри (тут — 5-та редакція, SRD/Basic Rules 2014). Кілька гравців ведуть по одному персонажу, ведучий (DM) — усіх супротивників і світ; бій іде раундами за порядком ініціативи. Кожен хід — бюджет: рух до своєї швидкості, одна дія, можливо бонусна дія, плюс одна реакція на раунд поза своїм ходом. На сітці 5 футів зʼявляються клітинні механіки, з яких виросли тактичні відеоігри: досяжність (reach) і **атака при виході** з неї, шаблони площ заклинань, укриття, розміри істот у клітинах, флангування як опційне правило.

## Поле і час
- Варіант сітки: квадрат = 5 футів; швидкість 30 футів = 6 клітин; діагональ = 1 клітина; вхід у складний ландшафт = 2 клітини; діагональ не можна різати через кут стіни; дальність — найкоротшим шляхом по клітинах.
- Опційно (DMG) — діагоналі 5-10-5 і без сітки «театр уяви» (?).
- Розміри: Tiny 2½×2½ ft (кілька в клітині) · Small/Medium 1 клітина · Large 2×2 · Huge 3×3 · Gargantuan 4×4 і більше.
- Раунд ≈ 6 секунд; кожен учасник має один хід на раунд; порядок ініціативи фіксований на весь бій.
- Видимість: темрява, укриття, сховані (Hide) істоти; DM знає більше, ніж гравці.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Персонаж гравця | piece | HP, AC, швидкість, досяжність 5 ft, ініціатива (Dex), бонус майстерності, вміння класу | хід: рух + дія + (бонусна дія) + реакція в раунді |
| Монстр / NPC | enemy | HP, AC, швидкість, розмір, reach, атаки | веде DM; більшість гине на 0 HP |
| Союзний NPC / прикликана істота | ally | як монстр | діє за своєю ініціативою або разом з власником (?) |
| Ведучий (DM) | neutral | — | вирішує сховки, складність, порядок рівних ініціатив монстрів, імпровізовані дії |
| Складний ландшафт | terrain | ×2 вартість руху | кожен фут коштує 2; клітина іншої істоти теж складний ландшафт |
| Стіна / повне укриття | static | — | не можна ціляти; блокує шаблон площі |
| Половинне / ¾ укриття | terrain | +2 / +5 AC і Dex-сейвів | найкраще укриття, не сумуються |
| Шаблон площі (cone, cube, cylinder, line, sphere) | zone | точка походження, розмір у футах | накриває клітини; ефект по всіх у зоні, шкода кидається один раз |
| Зона досяжності | zone | 5 ft (або 10+ для reach-зброї й великих) | вихід звідси провокує opportunity attack |
| Стан (prone, grappled, unconscious, …) | mark | тривалість | змінює правила руху/атак |

## Правила (КОЛИ → ЯКЩО → ТО)
- Старт бою: КОЛИ `custom: «бій починається»` → ТО `custom: «DM визначає, хто заскочений (Stealth проти пасивної Perception)»`, `custom: «кожен кидає ініціативу d20 + Dex; однакові монстри — один кидок»`.
- КОЛИ `custom: «заскочений у першому раунді»` → ТО `custom: «не рухається, не діє, без реакції до кінця свого першого ходу»`.
- Хід: КОЛИ `turn_start(a)` → ТО `custom: «рух ≤ speed, 1 дія, ≤1 бонусна дія (якщо дає вміння), 1 вільна взаємодія з обʼєктом»`; рух можна ділити до і після дії та між атаками.
- КОЛИ `turn_start(a)` → ТО `custom: «реакція a знову доступна (1 на раунд)»`.
- Рух: КОЛИ `input(move, a, cell)` → ЯКЩО `custom: «лишок швидкості ≥ вартості (2 за складний ландшафт)»` → ТО `move`; ЯКЩО `occupied(cell, hostile)` → ТО `block`, крім `custom: «різниця розмірів ≥ 2»`; закінчити хід у чужій клітині не можна.
- Дії: `input(attack|cast|dash|disengage|dodge|help|hide|ready|search|use_object)` — Dash: + ще швидкість руху; Disengage: рух цього ходу не провокує; Dodge: атаки по тобі з disadvantage до наступного ходу.
- Атака: КОЛИ `input(attack, a, t)` → ЯКЩО `in_range(a, t, reach|range)` і `custom: «є чистий шлях (не повне укриття)»` → ТО `custom: «d20 + модифікатор + майстерність ≥ AC цілі (з укриттям)»` → `damage(t, dice + mod)`.
- КОЛИ `custom: «натуральна 20»` → ТО `custom: «влучання завжди; критичне: кістки шкоди ×2»`; КОЛИ `custom: «натуральна 1»` → ТО `custom: «промах завжди»`.
- Advantage/disadvantage: ЯКЩО `custom: «перевага»` → ТО `custom: «кинути 2d20, взяти більше»`; disadvantage — менше; невидима ціль → disadvantage; невидимий нападник → advantage.
- Дальні атаки: ЯКЩО `custom: «ціль за нормальною дальністю, але в межах дальньої»` → ТО `custom: «disadvantage»`; ЯКЩО `adjacent(a, hostile)` (ворог у 5 ft бачить тебе) → ТО `custom: «disadvantage на дальню атаку»`.
- **Opportunity attack**: КОЛИ `custom: «ворожа істота, яку бачиш, виходить з твоєї досяжності»` → ЯКЩО `custom: «реакція доступна»` і not `state(mover, disengaged)` → ТО `custom: «одна атака в ближньому бою перед тим, як вона вийде»`; телепорт і примусовий рух не провокують.
- Reach: ЯКЩО `custom: «зброя reach або велика істота»` → ТО `custom: «досяжність 10 ft і більше»` — атакує і провокує на ширшому кільці.
- Ready: КОЛИ `input(ready, trigger, action)` → ТО `custom: «дія відкладається до тригера»`; КОЛИ тригер стався → ТО `custom: «виконати як реакцію або відмовитись»`.
- Шаблони: КОЛИ `input(cast, area, origin)` → ТО `custom: «накрити клітини формою від точки походження (конус: ширина = відстань від точки)»`; ЯКЩО `custom: «між точкою і клітиною повне укриття»` → ТО клітина не в зоні; `custom: «сейв: d20 + мод ≥ DC = 8 + мод + майстерність»` → половина/нічого.
- Укриття: ЯКЩО `custom: «половинне / ¾ укриття»` → ТО `custom: «+2 / +5 до AC і Dex-сейвів»`; повне — не можна ціляти напряму.
- Grapple/Shove: КОЛИ `input(grapple|shove, a, t)` → ЯКЩО `custom: «t не більше ніж на розмір більша і в досяжності»` → ТО `custom: «Athletics проти Athletics/Acrobatics»`; grapple → `set_state(t, grappled)` (швидкість 0); shove → `push(t)` на 5 ft або `set_state(t, prone)`.
- Prone: ЯКЩО `state(a, prone)` → ТО `custom: «встати коштує половину швидкості; повзти — 2 фути за фут»`; атаки впритул по ньому з advantage, здалеку — з disadvantage (?).
- Тісний прохід: ЯКЩО `custom: «протискається в простір на розмір менший»` → ТО `custom: «рух ×2, disadvantage на атаки, атаки по ньому з advantage»`.
- 0 HP: КОЛИ `hp_zero(pc)` → ЯКЩО `custom: «залишок шкоди ≥ max HP»` → ТО `custom: «миттєва смерть»`; інакше `set_state(pc, unconscious)`.
- Death saves: КОЛИ `turn_start(pc)` → ЯКЩО `state(pc, unconscious)` і `hp_zero` → ТО `custom: «d20: ≥10 успіх, ≤9 провал; 3 успіхи — стабільний, 3 провали — смерть; nat 1 = 2 провали, nat 20 = 1 HP»`.
- КОЛИ `damage(unconscious_pc)` → ТО `custom: «+1 провал (крит — +2)»`; КОЛИ `heal(pc, n)` → ТО `clear_state(pc, unconscious)`.
- Опційно — **флангування** (DMG): ЯКЩО `custom: «ти і союзник поруч з ворогом на протилежних боках/кутах його простору»` → ТО `custom: «advantage на ближні атаки по ньому»`.
- Перемога: мета сцени (вороги переможені, втекли, здались, ціль досягнута) · Поразка: загибель/полон партії — сюжетно, не жорстко · Рахунок: досвід (XP) після бою.

## Керування і ввід
- За столом: мініатюри на мапі з клітинами; гравець оголошує рух (лічить клітини) і дію, кидає d20 і кістки шкоди; DM оголошує результат і ходить монстрами.
- Шаблони площ — пластикові/паперові шаблони або лінійка; у VTT — інструмент шаблону, що підсвічує клітини.
- Ініціатива — трекер (картки, дошка або панель VTT); реакції — гравець каже «атакую при виході», коли ворог іде повз.
- Цифрова версія: клік по клітині руху з лічильником футів, кнопки дій, кидок кубиків одним кліком.

## Вікна, меню, HUD
- (цифрова версія, VTT) `game-screen`: мапа з `grid-lines`, токени, `fog-overlay` / динамічне освітлення, інструмент вимірювання, шаблони площ, `turn-indicator` у вигляді трекера ініціативи, `hp-bar` на токенах, значки станів.
- `custom-window` «Character sheet» — характеристики, AC, HP, атаки, заклинання, інвентар.
- `custom-window` «DM screen» — таблиці й приховані кидки ведучого.
- `custom-window` «Dice roller» / `message-log` — історія кидків.
- `lobby-window` — кампанія, учасники; `settings-window`.
- Переходи: лобі → сцена (мапа) → бій (трекер активний) → кінець бою → нагорода XP/скарб.

## Фічі поза полем
- `custom-rules`: опційні правила DMG — флангування, діагоналі 5-10-5, facing (?); «театр уяви» без сітки.
- Прогресія: `xp-level` 1–20, класи й підкласи, заклинання; інвентар і магічні предмети.
- `mode-coop` — гравці проти світу ведучого; `online-multiplayer` через VTT; `level-editor` — карти й енкаунтери (бюджет XP енкаунтера (?)).
- Відпочинки (short/long rest) — відновлення HP і ресурсів між боями.

## Варіації й родичі
- Редакції: OD&D (1974, виріс із варгейму Chainmail) · AD&D · 3e/3.5 (2000/2003: сітка обовʼязкова, attacks of opportunity, flanking +2) (?) · 4e (2008: бій на сітці як ядро) (?) · 5e (2014, сітка — варіант) · ревізія 2024 (?).
- Похідні: Pathfinder 1e/2e (три дії, flanking як «flat-footed»), [gloomhaven](gloomhaven.md) (картки дій замість кубиків), [heroquest-space-hulk](heroquest-space-hulk.md) (настільний данжен на сітці), Baldur's Gate 3 і Solasta (5e-правила у відеогрі), Pool of Radiance / Gold Box, Temple of Elemental Evil (3.5e на сітці).
- **Осі варіацій**: діагоналі — 1 / 5-10-5 / заборонені · реакції — нема / opportunity attack / будь-яка підготовлена дія · флангування — нема / +2 / advantage · рух і дія — фіксований порядок / вільне ділення / три дії (PF2).

## Цікавинки для курсу
- Бюджет ходу «рух + дія + бонусна + реакція» як машина станів ходу — 📎.
- Opportunity attack: подія «вийшов з досяжності» між клітинами шляху, перевірка реакції — 🥉.
- Шаблони площ на сітці: конус, лінія, сфера з точкою походження й блокуванням стінами — 🥈 (растеризація форм, line of effect).
- Розміри істот 1×1…4×4 і рух через простір з різницею розмірів — 📎.
- Advantage/disadvantage (2d20 max/min) замість купи модифікаторів — 🌱.
- Death saves: лічильник 3 успіхи / 3 провали з особливими кидками — 🌱.
- Флангування за протилежними сторонами простору — 📎.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` · `line-of-sight-attack` (чистий шлях) · `explode-area` (шаблони) · `multi-cell-size` (Large–Gargantuan) · `floor-types` (складний ландшафт) · `impassable-cells` · `status-effects` (prone, grappled, unconscious) · `unit-xp-skills` · `inventory-items` · `reachable-highlight` · `threat-range` (досяжність) · `fog-of-war` (VTT) · `turn-enforcement` · `rule-variants` (опційні правила) · `hot-seat` (одна мапа на столі) · `online-multiplayer` (VTT).
- **Нема** → пропозиції карток:
  - `+initiative-order` «Порядок ініціативи кидком на весь бій» · game-logic/turns · 🌱.
  - `+action-economy` «Бюджет ходу: рух, дія, бонусна дія, реакція» · game-logic/turns · 📎.
  - `+opportunity-attack` «Атака при виході з досяжності» · entities/combat · 🥉.
  - `+reach` «Досяжність ближньої атаки більше 1 клітини» · entities/combat · 🌱.
  - `+area-templates` «Шаблони площ: конус, лінія, куб, сфера» · entities/combat · 🥈.
  - `+cover-system` / `+flanking` — спільні з XCOM.
  - `+advantage-disadvantage` «Кинути двічі, взяти більше/менше» · game-logic/random · 🌱.
  - `+dice-roll-vs-target` «Кидок d20 + мод проти AC/DC» · game-logic/random · 🌱.
  - `+difficult-terrain` «Подвійна вартість руху» · entities/move · 🌱.
  - `+grapple-shove` «Захоплення і поштовх зустрічною перевіркою» · entities/combat · 📎.
  - `+death-saves` «Кидки проти смерті на 0 HP» · entities/state · 🌱.
  - `+ready-action` «Підготовлена дія на тригер» · game-logic/turns · 📎.

## Пропозиції до словників
- `+trigger:leave_reach` — сутність вийшла з досяжності іншої (opportunity attack).
- `+trigger:round_start` — початок раунду (повтор із tactics) · `+trigger:readied` — спрацював тригер підготовленої дії.
- `+cond:in_reach` — ціль у досяжності ближньої атаки · `+cond:cover` — рівень укриття · `+cond:flanked` — ворог між двома нападниками · `+cond:roll_vs` — кидок + мод ≥ цілі.
- `+effect:roll_dice` (повтор) · `+effect:reaction_attack` · `+effect:set_advantage` · `+effect:prone` · `+effect:grapple` · `+effect:death_save`.
- `+role:dm` — людина-рефері, що керує світом і ворогами.
- `+ui:initiative-tracker` · `+ui:aoe-template` · `+ui:dice-roller` · `+ui:condition-tokens` · `+ui:measure-ruler`.
- `+window:character-sheet` · `+window:dm-screen`.
- `+axis:referee=human` — правила частково застосовує людина-ведучий.

## Джерела
- ⭐ [D&D Basic Rules 2014: Combat](https://www.dndbeyond.com/sources/dnd/basic-rules-2014/combat) — порядок бою, заскочення, ініціатива, бюджет ходу, дії, рух, розміри, варіант сітки 5 ft, атаки, укриття, opportunity attack, grapple/shove, 0 HP, death saves.
- [D&D Basic Rules 2014: Spellcasting](https://www.dndbeyond.com/sources/dnd/basic-rules-2014/spellcasting) — шаблони площ і точка походження, блокування повним укриттям, DC сейву, концентрація.
- [Wikipedia: Dungeons & Dragons gameplay](https://en.wikipedia.org/wiki/Dungeons_%26_Dragons_gameplay) — d20, раунди, AC і HP по редакціях, death saves.
- YouTube: пошуки «DnD 5e grid combat explained», «attacks of opportunity explained».

## Непевне
- (?) Флангування (advantage, протилежні боки/кути) і діагоналі 5-10-5, facing — правила DMG, не SRD; 5e.tools віддав 403, тож формулювання з памʼяті.
- (?) Prone: ближні атаки з advantage, дальні з disadvantage — з розділу Conditions (Appendix), не відкривав.
- (?) Історія сітки по редакціях (3e — flanking +2 і обовʼязкова сітка, 4e — бій як ядро, ревізія 2024) — з памʼяті.
- (?) Союзні прикликані істоти: власна ініціатива чи разом із власником — залежить від заклинання.
- (?) Бюджет XP енкаунтера в DMG — з памʼяті.
