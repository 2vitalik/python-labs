---
title: "UFO: Enemy Unknown (X-COM: UFO Defense)"
slug: ufo-enemy-unknown
aka: ["X-COM: UFO Defense", "X-COM", "UFO", "X-COM 1994"]
family: tactics
also: [build-sim]
klass: figure
axes:
  field: layers
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 1994
platforms: [DOS, Amiga, Amiga CD32, PlayStation, Windows]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/UFO:_Enemy_Unknown", best: true, note: "два шари гри, TU, руйнівний воксельний ландшафт, opportunity fire, ніч, мораль, контроль розуму, умови перемоги й поразки кампанії"}
  - {kind: wiki, url: "https://www.ufopaedia.org/index.php/Time_Units", note: "UFOpaedia: ціни дій у TU (фіксовані й % від максимуму), вага → TU"}
  - {kind: wiki, url: "https://www.ufopaedia.org/index.php/Reaction_Fire", note: "UFOpaedia: рахунок реакції = Reactions × TU_left / TU_max, хто вищий — стріляє snap-ом"}
  - {kind: wiki, url: "https://www.ufopaedia.org/index.php/Battlescape", note: "UFOpaedia: кнопки панелі, резерв TU, поверхи, інвентар, правила евакуації"}
  - {kind: wiki, url: "https://www.ufopaedia.org/index.php/Accuracy", note: "UFOpaedia: шанс = точність бійця × точність режиму, коліна ×1.15, рани"}
  - {kind: wiki, url: "https://www.ufopaedia.org/index.php/Chryssalid", note: "UFOpaedia: зомбування і вилуплення нового Chryssalid"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=X-COM+UFO+Defense"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=UFO+Enemy+Unknown+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [hp-damage, projectile-shot, shoot-modes, shoot-burst, line-of-sight-attack, fog-of-war, orientation-state, height-levels, destructible-blocks, explode-area, bomb-fuse, inventory, inventory-items, inventory-limit, item-pickup, status-effects, unit-xp-skills, permadeath, ai-opponent, destroy-all-enemies, event-points, shop-between-levels, map-window, save-game, game-screen, +action-points, +ap-percent-cost, +reaction-initiative, +reserve-tu, +hit-chance, +stance-system, +weight-speed, +stamina-energy, +morale-states, +possess-unit, +subdue-capture, +infect-convert, +light-source, +research-tree]
proposes: ["+trigger:enemy_moved", "+trigger:spotted", "+effect:interrupt", "+effect:spend_ap", "+effect:reserve_ap", "+cond:ap_left", "+cond:lit", "+ui:reserve-tu-buttons", "+ui:spotted-enemies", "+ui:floor-switch", "+ui:unit-bars", "+window:base-management", "+window:research-window", "+window:monthly-report", "+feature:roster-carryover", "+axis:session=campaign"]
author: opus
date: 2026-11-09
---

# UFO: Enemy Unknown — оригінальний X-COM: очки часу на кожен крок і поворот, руйнівний воксельний бій, реакційний вогонь за ініціативою

## Суть
Два шари: на глобусі (**Geoscape**) гравець будує бази, перехоплює НЛО, досліджує трофеї й живе з фінансування 16 країн; на місії (**Battlescape**) загін покроково зачищає ізометричну мапу від прибульців. Кожна дія бійця коштує **очки часу (TU)**: крок, поворот на 45°, присісти, перезарядити, звести гранату; постріли — частка від максимуму TU. Хто не витратив TU, може вистрілити в чужий хід, якщо його **рахунок реакції** вищий за рахунок того, хто діє. Майже все на мапі руйнується, ночі темні без освітлення, а мораль, рани й контроль розуму забирають бійця з-під керування.

Відмінність від [XCOM 2012](xcom.md): там дві дії й Overwatch-стан, тут — безперервна економіка TU і реакція порівнянням чисел.

## Поле і час
- Мапа — процедурно згенерований **воксельний 3D-світ** із кубів і вертикальних шарів, показаний ізометричними спрайтами; квадратна сітка клітин, сторона 40–60 клітин.
- Висоти: зовнішні мапи мають 4 рівні, внутрішні (бази) — 2; між рівнями — сходи, ліфти, літальна броня. Кнопка перемикає видимий поверх, окремо — показ/приховання даху.
- Хід стороною: гравець ходить усіма бійцями в будь-якому порядку, потім фаза прибульців (`End turn`). Реакційний вогонь вклинюється в чужу фазу.
- Видимість: бійці мають напрямок погляду; туман війни, лінія зору блокується стінами, димом; уночі видно лише освітлене (фальшфеєри, вогонь) або зблизька.
- Випадковість: генерація мапи, кидки влучання, шкоди, ран, моралі, псі.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Боєць X-COM | piece | TU 50–60 на старті (стеля 80), Energy, Health, Morale, Firing Accuracy, Reactions, Strength, псі; ранг; напрямок | ходить, повертається, присідає, стріляє, кидає, використовує предмети; стати ростуть від застосування |
| Танк (HWP) | piece | без досвіду | важка зброя, не росте |
| Прибулець (Sectoid, Floater, Snakeman, Muton, Ethereal) | enemy | ті самі стати | ховається в НЛО/будівлях, стріляє, частина має псі-атаки |
| Терор-юніт (Cyberdisc, Sectopod, Reaper, Celatid, Silacoid) | enemy | — | супроводжує раси; механічні або звірі |
| Chryssalid | enemy | ближній бій | удар по людині → зомбі |
| Зомбі | enemy | — | убитий — з нього вилуплюється новий Chryssalid |
| Цивільний | neutral | — | на терор-місіях; врятовані/загиблі — у рахунок |
| Транспорт (Skyranger) | zone | — | старт загону; `Dust off` рятує лише тих, хто всередині |
| Стіна, двері, меблі, дерево, земля | static | міцність | блокують рух і огляд; руйнуються шкодою |
| Сходи, ліфт | terrain | — | перехід між рівнями (ліфт: ↑/↓ за 8 TU) |
| Дим | hazard | — | закриває огляд, зʼїдає Energy |
| Вогонь | hazard | — | шкодить усім; світить уночі |
| Фальшфеєр (flare) | object | радіус світла | кинутий — освітлює клітини |
| Зброя (пістолет, гвинтівка, лазер, плазма, ракетниця, Heavy Cannon) | pickup | вага, обойма, % TU і точність для aimed/snap/auto | постріл; спецнабої (фугасні, запальні) |
| Граната (і вибухівка) | object | зведена / ні | вибухає в області, руйнує |
| Stun Rod, оглушувальна зброя | pickup | — | приспати, щоб взяти живим |
| Medi-kit | pickup | заряди | лікує, зупиняє кровотечу, 10 TU |
| Motion Scanner, Mind Probe, Psi Amp | pickup | % TU / 25 TU | сканер руху; стати прибульця; псі-атака |
| Труп / артефакт / компонент НЛО | pickup | — | після перемоги — на дослідження або продаж |
| Alien Brain (Cydonia) | boss | — | знищити — перемога в кампанії |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(xcom)` → ТО `custom: «TU = базові TU; якщо Strength / вага < 1 — TU × (Strength / вага)»`; кожна смертельна рана ноги −10 % TU; Energy відновлюється на ⌊стартові TU / 3⌋.
- КОЛИ `input(move, s, cell)` → ЯКЩО `free(cell)` and `custom: «TU ≥ ціни шляху»` → ТО `move(s, path)`, `custom: «−4…18 TU за клітину за ландшафтом, діагональ +50 %»`, `counter(energy, −n)`; інакше `block`.
- КОЛИ `input(turn, s, dir)` → ТО `face(s, dir)`, `counter(tu, −1)` за кожні 45°.
- КОЛИ `input(kneel, s)` → ТО `set_state(s, kneeling)`, `counter(tu, −4)`; встати — −8; рух з колін сам підіймає за 8 TU.
- КОЛИ `input(up|down, s)` → ЯКЩО `custom: «літальна броня або клітина ліфта»` → ТО `move(s, up|down)`, `counter(tu, −8)`.
- КОЛИ `input(fire, s, mode, t)` → ЯКЩО `line_of_sight(s, t)` and `has(s, ammo)` and `custom: «TU ≥ % від максимуму TU для режиму (18–80 %)»` and `prob(hit)` → ТО `damage(t, n)`; auto — `custom: «черга з кількох пострілів»`.
- Шанс: `custom: «Firing Accuracy × точність режиму × 1.15 (на колінах) × 0.8 (дворучна в одній руці) × 0.9 за кожну рану руки/голови; не менше 10 %»`.
- Фіксовані ціни: перезарядка 15 · розрядити 8 · Medi-kit 10 · Psi Amp 25; відсоткові: кинути 25 % · звести вибухівку 50 % · Motion Scanner 25 % · Stun Rod 30 % · Mind Probe 50 % — `custom: «відсоток від максимуму TU, не від залишку»`.
- КОЛИ `input(reserve, mode)` → ТО `custom: «відкласти TU на snap / aimed / auto: інші дії не можуть їх витратити»`.
- КОЛИ `custom: «боєць у полі зору ворога витрачає TU (крок)»` → ЯКЩО `line_of_sight(w, m)` and `custom: «Reactions × TU_left / TU_max у w > того ж у m»` and `custom: «у w вистачає TU на snap»` → ТО `custom: «w стріляє snap-ом у чужий хід»`; повторюється, доки рахунок w вищий; нічия — хід за тим, хто діє; працює для обох сторін.
- КОЛИ `line_of_sight(s, alien)` → ТО `reveal(alien)`, `custom: «кнопка-лічильник побачених у HUD»`.
- КОЛИ `custom: «нічна місія»` → ЯКЩО `custom: «клітина не освітлена»` → ТО `custom: «бачать лише на дуже короткій відстані»`; `throw(flare, cell)` → `custom: «клітини навколо освітлені»`.
- КОЛИ `input(prime, s, g)` → ТО `set_state(g, armed)`; КОЛИ `input(throw, s, g, cell)` → ТО `throw(g, cell)`; вибух → `explode(area)`, `damage(all_in_area, n)`, `set_cell(cell, rubble)` для того, що не витримало (і своїм).
- КОЛИ `custom: «шкода по обʼєкту ≥ його міцності»` → ТО `set_cell(cell, destroyed)` — стіни, дахи, підлоги, дерева.
- КОЛИ `enter(a, smoke)` → ТО `custom: «огляд закрито»`, `counter(energy, −n)`; КОЛИ `enter(a, fire)` → ТО `damage(a, n)`.
- КОЛИ `counter(morale, <, low)` → ТО `set_state(s, panicked)` — кидає зброю й тікає, або `set_state(s, berserk)` — стріляє в будь-кого; хід бійця втрачено.
- КОЛИ `custom: «боєць отримав шкоду»` → ЯКЩО `prob(wound)` → ТО `set_state(s, fatal_wound)` — `custom: «HP падає щоходу до лікування»`, рани знижують стати; КОЛИ `input(medikit, m, s)` → ТО `heal(s, n)` або `clear_state(s, fatal_wound)`.
- КОЛИ `custom: «оглушувальна шкода перевищила здоровʼя»` → ТО `set_state(a, unconscious)`; КОЛИ `level_end` → ЯКЩО `custom: «непритомного прибульця евакуйовано або місію виграно»` and `has(base, alien_containment)` → ТО `give(base, live_alien)`.
- КОЛИ `custom: «псі-атака прибульця вдалась»` → ТО `set_side(s, aliens, 1 хід)` або `set_state(s, panicked)`; після полону псі-прибульця — свої бійці тренують те саме.
- КОЛИ `custom: «удар Chryssalid по людині»` → ТО `transform(victim, zombie)` після серії ударів (живий чи мертвий); КОЛИ `died(zombie)` → ТО `spawn(chryssalid)` на тому ж місці.
- КОЛИ `all_gone(aliens)` (убиті або непритомні) → ТО `win`, `give(base, artefacts + UFO_parts)`.
- КОЛИ `all_gone(xcom_units)` → ТО `lose`: бійці, спорядження й транспорт втрачені.
- КОЛИ `input(dust_off)` → ТО `custom: «виживають лише ті, хто в транспорті; решта і компоненти НЛО втрачені»`.
- Рахунок місії: `score(n)` — `custom: «− загиблі бійці, ± цивільні, + убиті/полонені прибульці, + артефакти»`.
- КОЛИ `level_end` → ЯКЩО `custom: «боєць застосовував первинну навичку»` → ТО `custom: «стат росте»`; загиблі — назавжди (`permadeath` для бійця).
- КОЛИ `custom: «кінець місяця»` → ТО `custom: «16 країн збільшують або ріжуть фінансування за прогресом; країна з інфільтрованим урядом виходить»`.
- Поразка кампанії: КОЛИ `custom: «два місяці поспіль поганий рейтинг або глибокий дефіцит; усі бази втрачено; провал штурму Марса»` → ТО `game_over`.
- Перемога кампанії: КОЛИ `destroyed(alien_brain)` на Cydonia → ТО `win`.

## Керування і ввід
- Миша: ЛКМ по клітині — іти туди; ПКМ — повернутися обличчям; край екрана — прокрутка.
- Дія предметом: ЛКМ по слоту лівої/правої руки на панелі → меню режимів (Aimed / Snap / Auto / Throw / Prime) з TU і відсотком → ціль курсором.
- Кнопки панелі: ↑/↓ (літати, ліфт), поверх вище/нижче, мапа, присісти/встати, інвентар, центрувати, наступний боєць, «наступний і забути», дах, опції, End turn, Dust off, 4 кнопки резерву TU.
- Червоні квадрати праворуч — по одному на кожного побаченого прибульця (за рангом); клік центрує камеру.

## Вікна, меню, HUD
- `main-menu`: нова гра (складність), завантаження, вихід.
- `map-window` — Geoscape: глобус, час із прискоренням, НЛО, бази, літаки; кнопки Intercept, Bases, Graphs, Ufopaedia, Options, Funding.
- `+window:base-management`: сітка модулів бази (ангари, лабораторії, майстерні, житло, склади, утримання прибульців), найм солдат/науковців/інженерів, закупівля, продаж на чорному ринку (`shop-window`).
- `+window:research-window` — вибір теми і кількості науковців; виробництво — окремий екран майстерні; `codex-window` — Ufopaedia зі статтями про досліджене.
- `inventory-window` (перед місією і на ній): портрет, руки, плечі 1×2, пояс 6 клітин, ноги 1×2, рюкзак 3×3, земля з кнопкою «More»; Unload за 8 TU.
- `game-screen` Battlescape: ізометрична мапа; панель знизу — руки, ранг (клік → стати й броня), імʼя, `+ui:unit-bars` (TU зелена, Energy помаранчева, Health червона, Morale фіолетова) = `action-points` + `hp-bar` + `energy-bar`; `+ui:reserve-tu-buttons`; `+ui:spotted-enemies`; `+ui:floor-switch`.
- `end-screen` — підсумок місії: рахунок за категоріями, трофеї, загиблі; `+window:monthly-report` — підсумок місяця й рішення країн.
- `settings-window` (Options): швидкість стрільби, прокрутки, руху; збереження Battlescape — звідси, завантаження — лише з Geoscape або титулу.

## Фічі поза полем
- Кампанія з ростером (`+feature:roster-carryover`): ранги, ріст статів, поранені лікуються днями, загиблих заміняють новобранці.
- Дослідження трофеїв → нова зброя і броня, полонені прибульці → псі-навички; виробництво й продаж як економіка.
- `difficulty-presets` (кількість — у «Непевне»); відомий баг повертав «Beginner» після першої місії, фан-патчі це лагодять.
- `save-slots`; на PlayStation сейв місії займає 5 блоків карти памʼяті.

## Варіації й родичі
- Попередник — [Rebelstar / Laser Squad](laser-squad.md) (AP, opportunity fire з ½ AP); нащадки — X-COM: Terror from the Deep (4 рівні на всіх мапах, резерв на присідання, «TU Bleed»), [XCOM 2012](xcom.md) (дві дії), [Jagged Alliance 2](jagged-alliance-2.md), [Silent Storm](silent-storm.md), [Phoenix Point](phoenix-point.md); OpenXcom — відкритий рушій оригіналу.
- Осі варіацій:
  - **реакція**: залишок ≥½ AP ([laser-squad](laser-squad.md)) / порівняння Reactions × частки TU (тут) / Overwatch-стан ([xcom](xcom.md));
  - **ціна пострілу**: фіксовані AP / частка максимуму TU (тут) / дія із двох;
  - **висота**: одна площина / шари-поверхи з руйнівною підлогою (тут) / висота клітини ([final-fantasy-tactics](final-fantasy-tactics.md)).

## Цікавинки для курсу
- TU-економіка: фіксовані ціни кроку за ландшафтом + постріли у відсотках від максимуму + вага ріже TU — 📎 (Dijkstra з орієнтацією в стані).
- Реакційний вогонь порівнянням ініціатив, що падають з кожною дією, і повтор, доки вартовий «швидший» — 🥉.
- Резерв TU як запобіжник: інші дії не чіпають відкладене — 🌱.
- Руйнування клітин за міцністю + падіння, коли зникла підлога, на кількох рівнях — 🥈.
- Ніч і світло: радіус освітлення від кинутих фальшфеєрів і пожеж — 🥉 (освітленість як шар клітини).
- Chryssalid → зомбі → Chryssalid: ланцюг перетворень через `died` — 📎.
- Два шари: стратегічна мапа місяців і тактична місія, що віддає трофеї в дослідження — 🥇 (два ігрові цикли з обміном станом).

## Мапа на каталог
- Є: `hp-damage` · `projectile-shot` · `shoot-modes` + `shoot-burst` ↔ aimed/snap/auto · `line-of-sight-attack` · `fog-of-war` · `orientation-state` ↔ напрямок і поворот за TU · `height-levels` ↔ рівні мапи · `destructible-blocks` · `explode-area` + `bomb-fuse` ↔ гранати · `inventory` / `inventory-items` / `inventory-limit` ↔ слоти тіла · `item-pickup` · `status-effects` ↔ паніка, берсерк, рани, непритомність · `unit-xp-skills` ↔ ріст статів від застосування · `permadeath` ↔ боєць · `ai-opponent` · `destroy-all-enemies` · `event-points` ↔ рахунок місії · `shop-between-levels` ↔ закупівля і чорний ринок · `map-window` ↔ Geoscape · `save-game` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+action-points`, `+ap-percent-cost`, `+hit-chance`, `+stance-system`, `+weight-speed`, `+stamina-energy`, `+morale-states`, `+possess-unit`, `+subdue-capture`, `+light-source`, `+research-tree` — уже в корпусі.
  - `+reaction-initiative` «Реакція порівнянням ініціатив» · entities/combat · 🥉 · слот {score: reactions × tu_left / tu_max, mode: snap} — родич `+opportunity-fire`.
  - `+reserve-tu` «Резерв очок дії під постріл» · game-logic/opponent · 🌱 · слот {modes: none|snap|aimed|auto}.
  - `+infect-convert` «Удар перетворює жертву, смерть перетвореного породжує ворога» · entities/spawn · 📎.

## Пропозиції до словників
- `+trigger:enemy_moved` — ворог витратив TU в полі зору (тригер реакції); `+trigger:spotted` — прибулець уперше в полі зору.
- `+effect:interrupt` — постріл у чужу фазу; `+effect:spend_ap` — списати TU (фіксовано або % максимуму); `+effect:reserve_ap` — відкласти TU.
- `+cond:ap_left` — лишилось TU ≥ N; `+cond:lit` — клітина освітлена (ніч).
- `+ui:reserve-tu-buttons` — 4 кнопки резерву; `+ui:spotted-enemies` — ряд кнопок побачених ворогів; `+ui:floor-switch` — перемикач видимого рівня; `+ui:unit-bars` — 4 смуги TU/Energy/Health/Morale.
- `+window:base-management` (з xcom) — сітка модулів бази; `+window:research-window` — розподіл науковців; `+window:monthly-report` — підсумок фінансування країн.
- `+feature:roster-carryover` (з xcom); `+axis:session=campaign`.

## Джерела
- ⭐ [Wikipedia: UFO: Enemy Unknown](https://en.wikipedia.org/wiki/UFO:_Enemy_Unknown) — Geoscape і Battlescape, 16 країн, воксельна процедурна мапа, TU від статів і ваги, режими пострілу, opportunity fire, ніч, дим і вогонь, мораль, рани, контроль розуму, рахунок місії, умови перемоги/поразки.
- [UFOpaedia: Time Units](https://www.ufopaedia.org/index.php/Time_Units) — таблиця цін TU, відсоткові дії від максимуму, енкумбранс, стеля 80 TU.
- [UFOpaedia: Reaction Fire](https://www.ufopaedia.org/index.php/Reaction_Fire) — формула рахунку реакції, нічия за тим, хто ходить, лише snap shot, обидві сторони.
- [UFOpaedia: Battlescape](https://www.ufopaedia.org/index.php/Battlescape) — усі кнопки панелі, резерв TU, кольори смуг, 4/2 рівні, мапи 40–60, інвентар, Dust off і що рятується.
- [UFOpaedia: Accuracy](https://www.ufopaedia.org/index.php/Accuracy) — формула шансу, коліна +15 %, хват −20 %, рани −10 %, мінімум 10 %.
- [UFOpaedia: Chryssalid](https://www.ufopaedia.org/index.php/Chryssalid) — зомбування, вилуплення, список рас і терор-юнітів.
- YouTube: пошук «UFO Enemy Unknown gameplay».

## Непевне
- (?) Кількість рівнів складності (5 — з памʼяті); Wikipedia згадує лише «Beginner» у контексті бага.
- (?) Сектор огляду бійця (90°?) — джерела кажуть лише, що вартовий не реагує, «якщо дивиться в інший бік».
- (?) Промах — куля летить відхиленою траєкторією й може влучити в інше (з памʼяті; на сторінці Accuracy нема).
- (?) Падіння, коли підлогу під бійцем зруйновано, і шкода від падіння.
- (?) Хто з прибульців має псі (Sectoid-лідери, Ethereal — з памʼяті), чи літають Floater-и.
- (?) Вікно перехоплення НЛО на Geoscape (режими атаки літака) — у прочитаних джерелах не описане.
- (?) Від чого падає мораль (смерть союзника, рани) — Wikipedia каже лише про наслідки низької моралі.
