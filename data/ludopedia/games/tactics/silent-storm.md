---
title: Silent Storm
slug: silent-storm
aka: [S2, "Silent Storm: Sentinels", Операция Silent Storm]
family: tactics
also: [roguelike]
klass: figure
axes:
  field: layers
  time: turn
  opponent: ai
  info: hidden
  random: runtime
  goal: state
year: 2003
platforms: [PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Silent_Storm", best: true, note: "загін до 6, 6 професій, майже все руйнівне, стрільба крізь стіни на звук, рикошети, панцеркляйни, база"}
  - {kind: steam, url: "https://store.steampowered.com/app/254960/Silent_Storm_Gold_Edition/", note: "Gold Edition (гра + Sentinels): 24 місії, 75+ зброї, балістика траєкторія/швидкість/пробиття"}
  - {kind: other, url: "https://rpgcodex.net/article.php?id=95", note: "огляд RPG Codex: 4 пози, шум, 10 навичок, 3 атрибути, режими прицілювання, вибухівка"}
  - {kind: other, url: "https://caltrops.com/review0027.php", note: "огляд Caltrops: AP та interrupt, 0 AP → непритомність/смерть, кровотеча, сейви F5–F8"}
  - {kind: other, url: "https://lilura1.blogspot.com/2019/08/Silent-Storm-Retrospective-Review-Walkthrough-Guide-Tips-Cheats-Mods-Builds.html", note: "ретроспектива: атрибути 2–10, пул AP 57→77, панцеркляйн і хедшот пілоту"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Silent+Storm+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [hp-damage, destructible-blocks, line-of-sight-attack, blast-wave, melee-vs-ranged, height-levels, inventory-items, inventory-limit, unit-xp-skills, status-effects, fog-of-war, difficulty-levels, save-game, save-autosave, save-multi-slot, ai-opponent, world-map, character-select, player-camera, +action-points, +interrupt-turn, +stance-system, +aimed-shot-ap, +body-part-targeting, +noise-lure, +cover-system, +hit-chance, +shoot-through-walls, +ricochet-ballistics, +ragdoll-knockback, +realtime-to-turn-switch, +skill-by-use, +power-armor, +leader-death-lose, +bleed-out-revive, +ability-perks]
proposes: ["+trigger:sighted", "+trigger:noise", "+effect:interrupt", "+cond:skill_check", "+effect:knock_out", "+role:vehicle", "+ui:ap-cost-preview", "+window:base-screen", "+window:squad-select", "+axis:time=realtime-until-contact"]
author: opus
date: 2026-11-09
---

# Silent Storm — загін у повністю руйнівному 3D-місті: AP, пози, стрільба крізь стіни на звук

## Суть
Покрокова тактика з загоном до 6 бійців у Другій світовій з наукфантастичним відтінком (альтернативна історія). Головне — **фізичне поле**: майже кожна стіна, підлога, двері й паркан руйнуються, кулі мають траєкторію і пробиття, рикошетять і влучають у те, що на шляху. Боєць витрачає **очки дій (AP)** на рух, позу, прицілювання й постріл; збережені AP дають **interrupt** — позачергову дію під час ходу ворога. Поза боєм загін рухається в реальному часі, бій вмикається, коли хтось когось побачить.

## Поле і час
- Поле — 3D-сітка з **поверхами** (будинки, дахи, підвали, драбини); руйнування змінює прохідність і видимість: діра в підлозі — новий шлях і новий кут стрільби.
- Укриття — фізичне з усіх кутів (3D-обструкція), а не позначка на ребрі; поза змінює, скільки тіла видно з-за перешкоди.
- Два режими часу: **real-time** поки загін не помічений → **покроковий бій** (хід гравця, потім хід ворогів), коли ворог побачив бійця.
- Видимість — поле зору кожного бійця + **слух**: шум від бігу, пострілів і вибухів чути крізь стіни; почутого ворога можна обстріляти крізь стіну сусідньої кімнати.
- Камера — вільна 3D (обертання, наближення); кінематографічно перебільшена фізика тіл (ragdoll, відкидання від влучання).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Головний герой | piece | атрибути, навички, AP, Vitality | загинув → гра закінчена |
| Soldier | piece | автомати, Burst | швидко освоює зброю, «танк» загону |
| Sniper | piece | далекий огляд, Snipe | прицілювання кілька ходів підвищує шанс; додатковий режим прицілу |
| Scout | piece | Hide, ближній бій, метальні | тихо підкрадається, бачить першим |
| Grenadier | piece | Throwing | точніше кидає гранати |
| Engineer | piece | Engineering | міни, пастки, відмички, найбільше навичок для панцеркляйна |
| Medic | piece | Medicine, аптечки | лікує VP, зупиняє кровотечу, знімає сліпоту |
| Ворожий солдат | enemy | ті самі правила | чує шум і йде перевіряти, перериває ваш хід |
| Панцеркляйн | piece | майже імунний до стрілецької, високе ухилення | «маленький танк»-костюм: пілот сідає/виходить; без пози, драбин, повільний, гучний |
| Стіна / підлога / двері | terrain | міцність | руйнується кулями і вибухом → діра/прохід |
| Вікно / паркан / ліхтар | terrain | слабка міцність | розбивається; крізь вікно можна залізти |
| Замкнені двері | gate | — | відмичка або розстріляти (руками не виламати) |
| Міна / пастка | hazard | — | вибух при контакті; Spot знаходить, Engineer ставить і знешкоджує |
| Бочка з пальним | hazard | — | постріл → вибух, руйнує підлогу |
| Зброя / набої / аптечка | pickup | вага, калібр | набої переважно під конкретну зброю |
| Підказка / предмет місії | pickup | — | відкриває нові локації на карті світу |
| Зона місії / вихід | zone | — | виконав цілі → місія завершена |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `line_of_sight(enemy, unit)` у real-time → ТО `custom: «перемикання в покроковий бій»`.
- КОЛИ `turn_start(side)` → ТО `counter(ap, =max)` для кожного бійця сторони (max від Dexterity/Intelligence і рівня).
- КОЛИ `input(move, unit, cell)` → ЯКЩО `path_exists(unit, cell)` і `counter(ap, ≥, cost)` → ТО `move`, `counter(ap, −cost)`; ціна кроку залежить від пози (біг дешевший, повзком дорожче).
- КОЛИ `input(stance, unit, s)` → ТО `set_state(unit, s)` (run / walk / crouch / prone), `counter(ap, −k)`.
- КОЛИ `input(fire, unit, target, mode)` → ЯКЩО `counter(ap, ≥, cost(mode))` → ТО `custom: «шанс = навичка × режим прицілу × поза × відстань × видима частина цілі»`, `counter(ammo, −1)`.
- КОЛИ `input(aim, sniper, target)` → ЯКЩО `line_of_sight(sniper, target)` → ТО `counter(aim, +ap)`; накопичений приціл переходить у наступний хід, поки ціль видно.
- КОЛИ `custom: «куля летить по траєкторії»` → ЯКЩО `occupied(cell_on_path, object)` → ТО `damage(object, n)`; `custom: «пробиття — летить далі зі зменшеною силою, або рикошет»`.
- КОЛИ `hp_zero(wall)` → ТО `set_cell(wall, hole)`; `reveal(cells)` за ним; КОЛИ `hp_zero(floor)` → ТО `fall(objects_above)`.
- КОЛИ `input(throw|place, explosive, cell)` → ЯКЩО `custom: «двері, вікно чи підлога; не стіна і не колона»` → ТО після вибуху `explode(area)`, `set_cell(area, ruin)`.
- КОЛИ `custom: «шум: біг, постріл, вибух»` → ЯКЩО `in_range(enemy, noise, n)` → ТО `custom: «ворог іде на звук»`; приглушена зброя шуму не дає.
- КОЛИ `custom: «ворог діє в полі зору бійця»` → ЯКЩО `counter(ap, >, 0)` і `custom: «перевірка Interrupt»` → ТО `custom: «interrupt: боєць діє позачергово залишком AP (стріляти або тікати)»`.
- КОЛИ `custom: «влучання»` → ТО `damage(target, n)` за зброєю й частиною тіла; голова → `custom: «можливе миттєве вбивство»`; сильне влучання → `push(target)` (відкидання).
- КОЛИ `custom: «серйозна рана»` → ТО `set_state(target, bleeding)`; КОЛИ `turn_start` → ЯКЩО `state(unit, bleeding)` → ТО `damage(unit, n)` (або втрата зору/AP/навичок).
- КОЛИ `input(heal, medic, ally)` → ЯКЩО `adjacent(medic, ally)` і `has(medic, medkit)` → ТО `heal(ally, n)`, `clear_state(ally, bleeding)`.
- КОЛИ `custom: «AP після шкоди < 0»` → ЯКЩО `mode(normal)` → ТО `set_state(unit, unconscious)`; ЯКЩО `mode(hard)` → `custom: «смерть»`.
- КОЛИ `input(board, pilot, panzerklein)` → ЯКЩО `adjacent(pilot, panzerklein)` → ТО `custom: «пілот сідає: броня майже імунна до куль, без поз і драбин»`.
- КОЛИ `custom: «влучання в панцеркляйн зі стрілецької зброї»` → ТО `damage(panzerklein, ≈0)`; хедшот пілоту або промінева зброя → `custom: «пілот вибуває»`.
- КОЛИ `input(use_skill, unit)` → ТО `counter(skill, +xp)` (навички ростуть від вживання, швидше з Intelligence).
- КОЛИ `counter(xp, ≥, level_threshold)` → ТО `choose(ability)` у дереві професії.
- КОЛИ `picked(squad, clue)` → ТО `unlock(location)` на карті світу.
- КОЛИ `died(lead_character)` → ТО `lose`.
- Перемога: виконати цілі місії → `win` місії; кампанія — ланцюг місій до фіналу · Поразка: загинув головний герой або весь загін · Рахунок: досвід і медалі після місії.

## Керування і ввід
- Мишка: клік бійця → клік клітини (рух) / цілі (атака); вибір пози і режиму пострілу (snap / звичайний / careful / прицільний снайпера; burst для автоматів) на панелі дій.
- Вибір частини тіла для прицільного пострілу (голова / руки / ноги / тулуб) (?).
- Перемикання поверхів і вільна камера; ALT — підсвітити лут.
- Кнопка «кінець ходу»; AP, що лишились, автоматично стають резервом для interrupt (без окремого режиму, як Overwatch).
- F5 — швидкий сейв (2 слоти автосейву по колу), F6 — ручний, F7/F8 — завантаження.

## Вікна, меню, HUD
- `splash-screen` → `main-menu`: Нова гра (вибір сторони: Allies / Axis) · Завантажити · Налаштування · Вихід.
- `character-select` — створення головного героя: професія, атрибути (пул очок, 2–10), голос, зовнішність; або готовий персонаж.
- `custom-window` «База» (`+window:base-screen`): медпункт · арсенал · відділ кадрів (найм/звільнення) · ангар панцеркляйнів.
- `custom-window` «Відбір загону» — до 6 із пулу персонажів.
- `map-window` — карта світу з точками місій (від Британії до СРСР); нові точки зʼявляються за знайденими підказками.
- `game-screen`: 3D-поле; портрети загону з VP/AP; `action-points`; панель дій (поза, режим пострілу, зброя); `tooltip` з шансом влучання (?); `message-log` (?); `fog-overlay`.
- `inventory-window` — спорядження бійця з вагою.
- `custom-window` «Objectives» — цілі місії.
- `stats-window` — характеристики, навички, дерево здібностей; `end-screen` місії з досвідом і медалями.
- `save-slots` · `settings-window` (`difficulty-select` — 3 рівні).

## Фічі поза полем
- `difficulty-presets` (3): на нормальній 0 AP → непритомність, на важкій — смерть.
- `save-slots` + `autosave` (2 швидкі слоти по колу).
- `xp-level`: рівень → очко у дерево здібностей професії; навички ростуть від вживання (пістолет — навіть від промахів).
- Арсенал без грошей: зброя з трофеїв або постачання своєї сторони; набої — головне обмеження.
- Дві кампанії (Allies / Axis) з тими ж місіями в іншому порядку; випадкові події в місіях.
- Розширення Sentinels (2004): післявоєнна кампанія.

## Варіації й родичі
- Наступник: Hammer & Sickle (2005). Духовні родичі: X-COM / UFO (AP, interrupt), Jagged Alliance 2 (AP, interrupt, шум) — у корпусі [xcom](xcom.md), Jagged Alliance 2 (C002), [Invisible Inc.](invisible-inc.md) (тихе проникнення), [Fights in Tight Spaces](fights-in-tight-spaces.md).
- Нащадки руйнівності: Phoenix Point, Xenonauts, Door Kickers (?), Breach & Clear (?).
- **Осі варіацій**: руйнування — нема / укриття ламається ([xcom](xcom.md)) / уся геометрія фізична (Silent Storm) · реакція — Overwatch на одну дію / interrupt з будь-якою дією за залишок AP · видимість — лише зір / зір + слух.

## Цікавинки для курсу
- Руйнування клітин-стін з міцністю: куля/вибух зменшує HP клітини, при нулі — діра і перерахунок прохідності/LOS — 🥈.
- Трасування кулі по 3D-сітці з пробиттям і рикошетом (Брезенгем у 3D, втрата енергії) — 🥇.
- Очки дій з ціною за позу і режим прицілу + перенесення залишку в interrupt — 🥉.
- Слух: хвиля шуму з радіусом, що проходить крізь стіни (BFS з послабленням) і будить ворогів — 🥈.
- Перемикання real-time ↔ покроковий бій за подією «побачили» — 🥉.
- Навички, що ростуть від вживання (лічильник на кожну дію) — 📎.
- Пілот у броні-костюмі: сутність усередині сутності, вразливе місце — голова — 📎.

## Мапа на каталог
- Є: `hp-damage` · `destructible-blocks` (майже все руйнується) · `line-of-sight-attack` · `blast-wave` (гранати, вибух руйнує) · `melee-vs-ranged` · `height-levels` (поверхи) · `inventory-items` + `inventory-limit` (вага) · `unit-xp-skills` · `status-effects` (кровотеча, сліпота, непритомність) · `fog-of-war` · `difficulty-levels` · `save-game` + `save-autosave` + `save-multi-slot` · `ai-opponent` · `world-map` · `character-select` · `player-camera`.
- **Нема** → пропозиції карток:
  - `+action-points` «Очки дій із ціною кожної дії» — спільна з [xcom](xcom.md).
  - `+interrupt-turn` «Позачергова дія залишком AP» · game-logic/turns · 🥉.
  - `+stance-system` «Пози (біг/крок/присід/лежачи): ціна, шум, укриття» · entities/state · 📎.
  - `+aimed-shot-ap` / `+body-part-targeting` — прицілювання за AP, постріл у частину тіла.
  - `+noise-lure` «Шум із радіусом, вороги йдуть на звук» · entities/ai · 🥈.
  - `+shoot-through-walls` «Стрільба крізь руйнівні перешкоди» · entities/combat · 🥈.
  - `+ricochet-ballistics` «Траєкторія, пробиття, рикошет» · entities/combat · 🥇.
  - `+ragdoll-knockback` «Відкидання тіла від влучання» · render/fx · 📎.
  - `+realtime-to-turn-switch` «Real-time до контакту, далі покроково» · game-logic/turns · 🥉.
  - `+skill-by-use` «Навичка росте від вживання» · entities/state · 📎.
  - `+power-armor` «Броня-костюм з пілотом усередині» · entities/state · 📎.

## Пропозиції до словників
- `+trigger:sighted` — сторону помітили (вмикання бою, тривога; Silent Storm, XCOM).
- `+trigger:noise` — у радіусі пролунав шум (біг, постріл, вибух) — для AI ворогів.
- `+effect:interrupt` — позачергова дія під час чужого ходу.
- `+cond:skill_check` — кидок/перевірка навички (Interrupt, Spot, Hide).
- `+effect:knock_out` — непритомність замість смерті (лікується після бою).
- `+role:vehicle` — сутність, у яку сідає інша (панцеркляйн, танк, мех).
- `+ui:ap-cost-preview` — скільки AP коштує дія під курсором.
- `+window:base-screen` — база між місіями з відділами (медпункт, арсенал, найм, ангар).
- `+window:squad-select` — відбір загону з пулу перед місією.
- `+axis:time=realtime-until-contact` — real-time, поки нема бою, далі покроково.

## Джерела
- ⭐ [Wikipedia: Silent Storm](https://en.wikipedia.org/wiki/Silent_Storm) — загін до 6 з пулу 20, 6 професій, база, руйнівність, стрільба на звук крізь стіну, рикошети, панцеркляйни, Sentinels, без мультиплеєра.
- [Steam: Silent Storm Gold Edition](https://store.steampowered.com/app/254960/Silent_Storm_Gold_Edition/) — 2 кампанії, 24 місії з випадковими подіями, 3 складності, 75+ зброї, балістика.
- [RPG Codex review](https://rpgcodex.net/article.php?id=95) — 4 пози і шум, слух ворогів, 10 навичок, атрибути, режими прицілу, вибухівка не на стіни, база.
- [Caltrops review](https://caltrops.com/review0027.php) — AP, interrupt залишком, 0 AP → непритомність/смерть, кровотеча, клас-навички, сейви.
- [Lilura: retrospective](https://lilura1.blogspot.com/2019/08/Silent-Storm-Retrospective-Review-Walkthrough-Guide-Tips-Cheats-Mods-Builds.html) — атрибути 2–10 з пулу 14, AP 57→77, панцеркляйн і хедшот пілоту.
- YouTube: пошук «Silent Storm gameplay».

## Непевне
- (?) Точна формула шансу влучання і ціни AP за дії — не бачив у джерелах.
- (?) Вибір частини тіла (руки/ноги) і його ефекти — лише згадка в пошуковому зведенні; хедшот підтверджено.
- (?) Як саме вирішується interrupt (рівень, навичка, кількість кандидатів) — джерела розходяться.
- (?) Наявність журналу подій і показ шансу у тултіпі — з памʼяті.
- (?) Розміри мап, кількість поверхів, радіус слуху — не перевіряв.
- (?) Старий Steam-лінк з черги (app 1255250) веде на чужу гру — замінено на Gold Edition.
