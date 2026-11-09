---
title: Mega Man Star Force (Ryuusei no Rockman)
slug: mega-man-star-force
aka: [Ryuusei no Rockman, 流星のロックマン, Star Force, MMSF, Мегамен Стар Форс]
family: tower-lanes
also: [tactics]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 2006
platforms: [DS, Legacy Collection (2026)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mega_Man_Star_Force", best: true, note: "SF1: сітка 3×5 з виглядом з-за спини, рух лише вліво-вправо рядом, Custom Gauge, класи карт, Brother Band, версії Pegasus/Leo/Dragon"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mega_Man_Star_Force_2", note: "SF2: щит і самонавідні атаки, бастер, Star Cards, Tribe On / Double Tribe / Tribe King, Link Power і здібності"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mega_Man_Star_Force_3", note: "SF3: 6 карт на Custom Screen, вибір за розташуванням і кольором, Dimming-карти, Galaxy Advance, коло елементів, Noise 50/100/200 %, фінальна форма на 3 ходи, White Cards"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mega+Man+Star+Force+battle+gameplay", note: "пошук; бої"}
stage: v1
coverage: 55
mechanics: [hp-damage, shoot-forward, line-of-sight-attack, temporary-modes, status-effects, player-death, save-game, codex-window, game-screen, online-multiplayer, +deck-draw, +lane-dodge-row, +behind-view-grid, +lock-on-dash, +shield-block, +charge-shot, +hand-select-by-layout, +program-advance, +damage-type-wheel, +form-change, +noise-meter, +folder-limits, +random-encounter, +friend-link-bonus, +physical-code-cards]
proposes: ["+role:card", "+trigger:gauge_full", "+effect:draw_card", "+cond:card_layout", "+ui:noise-meter", "+window:custom-screen", "+feature:friend-link"]
author: opus
date: 2026-11-09
---

# Mega Man Star Force — Battle Network, розвернутий «з-за спини»: поле 3×5 у глибину, герой ходить лише своїм рядом, вороги — на рядах попереду

## Суть
Спадкоємець [mega-man-battle-network](mega-man-battle-network.md) з тим самим ядром: real-time бій на клітинах, Custom Gauge, папка з 30 карт, класи Standard/Mega/Giga, елементи ×2. Головна зміна — геометрія: камера стоїть за спиною Мегамена, поле 3×5 іде в глибину, герой рухається **лише вліво-вправо** в одному ряду, а вороги займають ряди попереду. Ухилення — зміна «смуги», захист — щит, ближні атаки — lock-on, що підводить героя до ворога. Файл описує серію (SF1–SF3) як відмінності від MMBN.

## Поле і час
- Бій — сітка 3×5 (3D-вид з-за спини Мегамена); герой — у своєму ряду, рух лише ліворуч/праворуч; ворогам доступно більше клітин попереду.
- SF3: Мегамен може коротко «стрибнути» на ворожу сторону (lock-on атаки).
- Час — real-time; на повній Custom Gauge відкривається Custom Screen (бій на паузі). Тривалість форм рахується в «ходах» — циклах Custom Screen (Tribe King, фінальна форма SF3 — 3 ходи).
- Поза боєм — ізометричний 2D-світ; Wave World (світ EM-хвиль) — вхід через точки EM Wave Change; бої — зустрічі з вірусами у Wave World.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мегамен (Geo + Omega-Xis) | player | HP, бастер (швидкість, сила, заряд) | рух 3 клітинами свого ряду; бастер будь-коли, утримання — швидкий вогонь; щит; HP 0 → видалений, рестарт зі збереження |
| Вірус | enemy | HP, елемент | на рядах попереду; патерн атак |
| Бос (FM-ian) | boss | HP, елемент | сильний противник; у SF3 оверкіл по ньому дає Noise |
| Battle Card | card (`+role:card`) | клас Standard / Mega / Giga, елемент Heat / Aqua / Elec / Wood | одноразова дія за бій; ліміти копій у папці за класом |
| Lock-on карта (меч тощо) | card | — | герой підходить до цілі й бʼє впритул |
| Dimming-карта (SF3) | card | — | використовується одна або в парі з будь-якою, незалежно від розташування |
| Star Card (SF2) | card | ≤3 у папці | підсилює однойменні карти |
| White Card (SF3) | card | фізична картка + код | дає 4 спеціальні карти понад 30 у папці |
| Папка (folder) | supply | 30 карт | джерело випадкових карт на Custom Screen |
| Форма: Tribe (SF2) | — | Thunder Zerker / Wood Ninja / Fire Saurian | інші атаки й слабкість; Double Tribe, Tribe King |
| Форма: Noise (SF3) | — | 10 форм FM-ian | > 50 % Noise; заряджені постріли, броня, контрудари |
| Фінальна форма (SF3) | — | Black Ace / Red Joker | ≥ 200 % Noise через Meteor Server, 3 ходи, без слабкості |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, left|right)` → ЯКЩО `free(target)` and `custom: «клітина свого ряду»` → ТО `move(megaman, dir)`; інакше `block`.
- КОЛИ `input(buster)` → ТО `custom: «постріл уздовж смуги; утримання — швидкий вогонь»`; КОЛИ `custom: «заряд»` → ТО `damage(enemy, charged)`.
- КОЛИ `input(shield)` → ТО `set_state(megaman, shield, dur)` — атака блокується (SF2+).
- КОЛИ `custom: «використано lock-on карту»` → ТО `move(megaman, target_front)`, `damage(target, n)`, `move(megaman, home_row)`.
- КОЛИ `custom: «trigger gauge_full»` → ТО `custom: «можна відкрити Custom Screen; бій на паузі»`, `custom: «effect draw_card: випадкові карти з папки (SF3 — 6)»`.
- КОЛИ `input(select, card)` → ЯКЩО `custom: «cond card_layout: дозволено розташуванням на екрані (і кольором — SF3)»` or `custom: «Dimming-карта»` → ТО `custom: «карта в чергу»`; інакше `block`.
- КОЛИ `input(ok)` → ЯКЩО `custom: «3 карти рецепта в заданому порядку»` → ТО `merge(cards → galaxy_advance)` (SF3; у SF1 — комбінації за розташуванням).
- КОЛИ `contact(attack, enemy)` → ЯКЩО `custom: «елемент атаки сильний проти цілі (Heat→Aqua→Elec→Wood→Heat)»` → ТО `damage(enemy, ×2)`; у PvP SF3 — `set_value(noise, 0)` замість ×2.
- КОЛИ `hp_zero(virus)` → ЯКЩО `custom: «оверкіл неелементною не-Dimming картою»` → ТО `counter(noise, +overkill)` (SF3).
- КОЛИ `counter(noise, >, 50)` → ТО `custom: «доступна Noise-форма (1 з 10)»`; КОЛИ `counter(noise, >=, 100)` → ТО `custom: «бій закінчується з випадковою картою»`; КОЛИ `counter(noise, >=, 200)` → ТО `custom: «Meteor Server на Custom Screen»`.
- КОЛИ `input(meteor_server)` → ТО `set_state(megaman, final_form, 3)`; `custom: «lock-on карти ×2, слабкості нема»`; КОЛИ `state_off(megaman, final_form)` → ТО `set_value(noise, 0)`.
- КОЛИ `custom: «зіграно brother-карту іншого племені в Tribe On»` → ТО `set_state(megaman, double_tribe)` (SF2); КОЛИ `custom: «третє плем'я / усі OOPArt»` → ТО `set_state(megaman, tribe_king, 3)`.
- КОЛИ `contact(weak_element_attack, megaman)` → ЯКЩО `state(megaman, tribe)` → ТО `clear_state(megaman, tribe)` (SF2).
- КОЛИ `all_gone(virus)` → ТО `win`, `window(end-screen)`; КОЛИ `hp_zero(megaman)` → ТО `lose`, `game_over` → останнє збереження.
- КОЛИ `custom: «крок у Wave World»` → ЯКЩО `prob(p)` → ТО `custom: «зустріч з вірусами → бій»` (?).
- Перемога: видалити всіх ворогів · Поразка: HP 0 → game over · Рахунок: —.

## Керування і ввід
- Хрестовина вліво/вправо — зміна клітини ряду; кнопки — бастер (утримання — заряд/швидкий вогонь), використати карту, щит (SF2+).
- Custom Screen — вибір карт курсором за правилом розташування (SF3 — ще й кольору); SF3: тач-екран для White Cards (ввести код послідовністю торкань).
- Поза боєм — прямий рух Geo/Мегамена; Transer — меню (папка, Brother Band, пошта).

## Вікна, меню, HUD
- `game-screen` (бій): вид з-за спини на сітку 3×5, `hp-bar` Мегамена (число), `+ui:custom-gauge`, назва поточної карти, `+ui:noise-meter` (SF3, %).
- `+window:custom-screen`: випадкові карти (SF3 — 6) з підсвіткою доступних за розташуванням, слоти вибраних, OK; SF3 — кнопка Meteor Server на ≥ 200 %.
- `+window:deck-builder` (папка 30) · `codex-window` (бібліотека карт) · Brother Band-меню (брати, улюблені карти, Link Power, здібності) · `shop-window` · `end-screen` бою · game over.
- Переходи: Wave World → зустріч → Custom Screen ↔ бій → end-screen; HP 0 → game over → останнє збереження.

## Фічі поза полем
- `+feature:friend-link`: Brother Band — брати (живі гравці через бездротовий звʼязок/Wi-Fi і NPC) дають обмін і бої, спільні улюблені карти, трансформації й апгрейди; у SF2–3 — Link Power, що обмежує кількість здібностей (як Navi Customizer у BN3).
- SF3: Multi-Noise — 100 комбінацій форм з братами; Rogue Noise (10 %) для тих, у кого нема живих братів.
- Версії: SF1 — Pegasus / Leo / Dragon; SF2 — Zerker × Ninja / Zerker × Saurian; SF3 — Black Ace / Red Joker (різні карти, фінальні форми, шанси Noise-форм).
- `save-game`; Legacy Collection (2026) — усі три гри, повернено вирізаний поза Японією Cross Brother Band з Lunar Knights.

## Варіації й родичі
- SF1 (2006): 3×5 з-за спини, рух лише рядом, класи карт, елементи, улюблені карти в Wi-Fi-бою, Brother Band.
- SF2 (2007): щит і самонавідні атаки, Star Cards, Tribe On → Double Tribe → Tribe King (3 ходи), Link Power.
- SF3 (2008): 6 карт за раз, вибір за розташуванням і кольором, Dimming-карти, Galaxy Advance (3 карти), Noise 50/100/200 %, фінальна форма на 3 ходи, трансформація будь-коли, White Cards.
- Родичі: [mega-man-battle-network](mega-man-battle-network.md) (6×3 з двома половинами), [one-step-from-eden](one-step-from-eden.md) (дві половини 4×4, мана замість паузи), [plants-vs-zombies](plants-vs-zombies.md) (смуги в глибину до гравця).
- **Осі варіацій**: геометрія — вид збоку 6×3 з половинами (BN) / з-за спини 3×5 з рухом лише рядом (SF) · захист — рух / рух + щит · вибір карт — за назвою/кодом (BN) / за розташуванням на екрані й кольором (SF3) · шкала форми — немає / Noise із порогами 50/100/200.

## Цікавинки для курсу
- Поле в глибину, де гравець рухається лише в одному ряду, а ухилення = зміна смуги — 🌱 (найпростіший «lane-dodge»).
- Lock-on: герой підходить до цілі, бʼє і повертається на свій ряд — 📎 (тимчасовий вихід з дозволеної зони).
- Шкала Noise з трьома порогами (форма / бонус / фінальна форма на 3 ходи з ресетом) — 📎.
- Таймер форми в «ходах» Custom Screen посеред real-time бою — 🌱.
- Вибір карт за розташуванням у сітці Custom Screen (і кольором), Dimming-карта як джокер — 🥉.
- Коло елементів Heat→Aqua→Elec→Wood: ×2 у PvE, обнулення шкали в PvP — 🌱.

## Мапа на каталог
- Є: `hp-damage` · `shoot-forward` + `line-of-sight-attack` ↔ бастер уздовж смуги · `temporary-modes` ↔ Tribe/Noise/фінальна форма · `status-effects` ↔ щит · `player-death` · `save-game` · `codex-window` ↔ бібліотека карт · `game-screen` · `online-multiplayer` ↔ Wi-Fi-бої.
- **Нема** → пропозиції карток:
  - `+deck-draw` · `+charge-shot` · `+program-advance` · `+damage-type-wheel` · `+form-change` · `+folder-limits` · `+random-encounter` · `+shield-block` — уже пропонувались корпусом (MMBN, Element TD 2, BoxBoy!); тут: ті самі з SF-відмінностями.
  - `+lane-dodge-row` «Гравець ходить лише своїм рядом; ухилення = зміна смуги» · entities/move · 🌱 · слот {lanes: 3}.
  - `+behind-view-grid` «Сітка з камерою з-за спини, поле в глибину» · interface/render · 🥉.
  - `+lock-on-dash` «Атака підводить героя до цілі й повертає назад» · entities/combat · 📎.
  - `+hand-select-by-layout` «Вибір карт за розташуванням у сітці руки» · interface/input · 🥉 · слоти {rule: column|adjacent, color}.
  - `+noise-meter` «Шкала з порогами, що відкривають форми й бонуси» · entities/state · 📎 · слоти {thresholds: 50|100|200}.
  - `+friend-link-bonus` «Звʼязки з друзями дають ресурс для пасивок» · game-logic/opponent · 🥉.
  - `+physical-code-cards` «Фізична картка-код відкриває вміст» · game-logic/economy · 🌱.

## Пропозиції до словників
- `+role:card` — Battle Card як сутність поза полем (підтвердження корпусу).
- `+trigger:gauge_full` — шкала (Custom Gauge) заповнилась (підтвердження MMBN).
- `+effect:draw_card` — видати випадкові карти з папки.
- `+cond:card_layout` — карту дозволено вибрати за її позицією в сітці руки (і кольором).
- `+ui:noise-meter` — шкала у відсотках з порогами форм.
- `+window:custom-screen` — модал вибору карт, що ставить real-time на паузу (підтвердження MMBN).
- `+feature:friend-link` — соціальні звʼязки (Brother Band) як ігровий ресурс.

## Джерела
- ⭐ [Wikipedia: Mega Man Star Force](https://en.wikipedia.org/wiki/Mega_Man_Star_Force) — сітка 3×5, вид з-за спини, рух лише вліво-вправо рядом, Custom Gauge, класи й елементи, улюблені карти, Brother Band, версії, Legacy Collection (2026).
- [Wikipedia: Star Force 2](https://en.wikipedia.org/wiki/Mega_Man_Star_Force_2) — щит, бастер, Star Cards, Tribe On / Double Tribe / Tribe King, Link Power.
- [Wikipedia: Star Force 3](https://en.wikipedia.org/wiki/Mega_Man_Star_Force_3) — 6 карт, правило розташування й кольору, Dimming, Galaxy Advance, коло елементів, Noise, Meteor Server, White Cards, відмінності версій.
- YouTube: [пошук «Mega Man Star Force battle gameplay»](https://www.youtube.com/results?search_query=Mega+Man+Star+Force+battle+gameplay).

## Непевне
- (?) Орієнтація 3×5: Wikipedia каже «3-by-5 grid» і рух «left to right in one row»; що ряд героя має 3 клітини, а 5 — глибина, — з памʼяті.
- (?) Точне правило вибору карт за розташуванням у SF1 (стовпець? сусідні?) — у джерелах лише «залежить від розташування на екрані».
- (?) Кількість карт на Custom Screen у SF1–2 і чи бої у Wave World — випадкові зустрічі на кроці (як у MMBN) — не перевірено.
- (?) «≥ 100 % Noise — бій закінчується з випадковою картою» — формулювання Wikipedia неоднозначне (ймовірно, нагорода наприкінці бою).
- (?) Механіка lock-on (підхід і повернення) — з опису «Mega (Lock-on) Attack» і «briefly jump into the enemies' side»; деталі не перевірено.
