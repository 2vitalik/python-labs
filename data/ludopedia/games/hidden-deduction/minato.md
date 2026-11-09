---
title: Minato
slug: minato
aka: []
family: hidden-deduction
also: [roguelike]
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: hidden
  random: both
  goal: state
year: 2024
platforms: [web (itch.io, HTML5), PC (Windows, Linux), Steam (14.12.2026, анонс)]
links:
  - {kind: itch, url: "https://noshuio.itch.io/minato", best: true, note: "грати в браузері; опис: класи з артефактами-зарядами, consumables, relics, прокляття (обмежена видимість, порожні клітини, випадкові числа), боси"}
  - {kind: steam, url: "https://store.steampowered.com/app/3165740/Minato/", note: "noshuio, реліз 14.12.2026 (анонс), демо; гардіани, що міняють правила; achievements, leaderboards, stats"}
  - {kind: official, url: "https://noshuio.itch.io/minato/devlog", note: "девлог 0.2.0 (06.08.2024) – 0.6.6 (18.10.2026): класи, артефакти, реліквії, стадії, режими"}
  - {kind: official, url: "https://noshuio.itch.io/minato/devlog/1608560/update-060", note: "0.6.0: випадкові мапи, Guardian, вівтар із пастками, артефакти — предмети магазину, no-flags, seed"}
  - {kind: official, url: "https://noshuio.itch.io/minato/devlog/1122700/update-050", note: "0.5.0: поверх = звичайні стадії + магазин + 2 челенджі + бос, 5 поверхів, апгрейд артефактів, Hard"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Minato+minesweeper+roguelike+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [cell-click, neighbor-count-clue, flood-reveal, chord-click, run-relics, inventory-items, shop-between-levels, shop-catalog, character-select, map-window, world-map, seed-share, mode-select, difficulty-levels, player-death, fog-of-war, leaderboard, achievements-window, tutorial-window, controls-remap, game-screen, end-screen, +rule-curse, +artifact-charges, +shop-reroll, +class-unlock-by-feat, +challenge-stage, +no-flags-mode, +exploded-mine-counts]
proposes: ["+trigger:stage_start", "+effect:apply_curse", "+effect:charge", "+effect:lock_cell", "+effect:reroll", "+window:run-map", "+feature:no-flags", "+card:rule-curse", "+card:artifact-charges", "+card:shop-reroll", "+card:class-unlock-by-feat", "+card:challenge-stage", "+card:no-flags-mode", "+card:exploded-mine-counts"]
author: opus
date: 2026-11-09
---

# Minato — сапер-роглайт: забіг через поверхи дошок, клас з артефактом на зарядах, реліквії й прокляття, що ламають правила

## Суть
Кожна стадія — звичайна дошка сапера, але дошки зібрані в **забіг**: мапа поверху з кількома стадіями, магазином, челенджами й гардіаном-босом. Гравець стартує класом з **артефактом** — активною здібністю на зарядах (Scythe, Drill відкривають клітини; Metal Detector «замикає» міни), купує реліквії (пасивні зміни правил: Safe Start, Chord Nullifier…) і витратні предмети. Між стадіями гардіани накладають **прокляття** — обмежена видимість, порожні клітини, випадкові числа, «гниюча земля», що прибирає частину клітин. Вибух міни коштує серце, а не гру; 0 сердець — кінець забігу. Темп спокійний, але гра винагороджує швидкість і мінімум кліків.

## Поле і час
- Дошка сапера (квадратна (?)); щільність мін залежить від світу (у світі 3 її зменшували).
- Статичний пазл, без тиску часу; таймер і лічильник кліків — для нагород/рейтингу (?).
- Метарівень: забіг = поверхи (5 у 0.5.0; базова гра закінчується 4-м у 0.6.0, далі можна продовжувати); мапа поверху з 0.6.0 генерується випадково, гардіан і скрині — сховані на мапі.
- Шари: прихований вміст + числа + прапорці/«замки» + накладені прокляття.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець (клас) | player | серця, щити, золото, мана (?) | курсор; клас визначає стартовий артефакт |
| Закрита клітина | static | прихований вміст | відкриття / прапорець (F) |
| Число | mark | n = міни серед 8 сусідів | підказка; прокляття «random numbers» спотворює (?) |
| Міна | hazard | — | відкриття → −серце (щит поглинає (?)); опційно далі рахується в числах сусідів |
| Прапорець | mark | — | позначка; є режим без прапорців |
| «Замок» Metal Detector | mark | — | виглядає інакше, але рахується як прапорець для акорду |
| Артефакт | pickup | заряди, рівень апгрейду | активується кліком по іконці; 6 штук, 2 стартові, решта — за секретною стадією |
| Реліквія | pickup | рідкість | пасивна зміна правил до кінця забігу; стакаються |
| Витратний предмет | pickup | рідкість | разовий ефект (Golden Heart → 10 золота, «Select»-ефекти, Player Madness) |
| Серце / щит | pickup | — | життя / захист; стакаються |
| Скриня | container | схована на мапі | дає предмет/золото |
| Стадія | zone | тип: звичайна / магазин / челендж / вівтар / секрет / гардіан | вузол мапи поверху |
| Вівтар | zone | пастки | пастка миттєво провалює стадію без втрати HP, але без нагороди |
| Гардіан | boss | 6 варіантів (0.4.0) | стадія-бос поверху; накладає прокляття-правило |
| Прокляття | zone | вид | змінює правила стадії: limited visibility · empty cells · random numbers · Decaying Ground (−10 % клітин) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(open, c)` → ЯКЩО `not cell(c, mine)` → ТО `reveal(c)` зі значенням `adjacent_count(c, mine)`; нуль → `custom: «flood reveal»` (?).
- КОЛИ `input(open, c)` → ЯКЩО `cell(c, mine)` → ТО `lives(-1)` (або `custom: «щит поглинає»`), `reveal(c)`.
- КОЛИ `custom: «міна вибухнула»` → ЯКЩО `mode(exploded_counts)` → ТО міна лишається в числах сусідів; інакше числа ігнорують її.
- КОЛИ `counter(hearts, ==, 0)` → ТО `lose`, `window(end-screen)` «Game Over»; продовжити не можна.
- КОЛИ `input(flag, c)` → ЯКЩО `not mode(no_flags)` → ТО `mark(c, flag)`.
- КОЛИ `input(chord, c)` → ЯКЩО `custom: «прапорців/замків навколо = n»` → ТО `reveal(neighbors8)`.
- КОЛИ `input(use, artifact)` → ЯКЩО `has(artifact, charge)` → ТО `custom: «ефект артефакта»` (Scythe/Drill — `reveal(cells)`; Metal Detector — `custom: «замкнути клітину з міною»`), `counter(charges, -1)`.
- КОЛИ `custom: «стадія почалась»` → ЯКЩО `custom: «діє прокляття»` → ТО `custom: «модифікувати правило: сховати частину поля / прибрати клітини / спотворити числа»`.
- КОЛИ `custom: «всі безпечні клітини відкрито»` → ТО `currency(+reward)`, `window(map-window)`; челендж — нагорода лише ЯКЩО `custom: «виконано умову челенджу»`.
- КОЛИ `enter(player, shop)` → ТО `window(shop-window)`: купити предмет / артефакт / апгрейд, `custom: «reroll вітрини за золото»`.
- КОЛИ `counter(rerolls, >=, 8)` → ТО `unlock(class_gambler)`.
- КОЛИ `custom: «переможено гардіана останнього поверху»` → ТО `win`, `window(end-screen)` «Victory»; можна продовжити далі.
- Перемога: пройти фінальний поверх. · Поразка: 0 сердець. · Рахунок: швидкість і мінімум кліків (?), очки таблиці лідерів.

## Керування і ввід
- Миша: лівий клік — відкрити, правий / F — прапорець, клік по числу — акорд (?), клік по іконці артефакта — активація.
- Клавіатура й геймпад (з 0.6.0), перепризначення клавіш; масштаб інтерфейсу (2× за замовчуванням), зум поля.

## Вікна, меню, HUD
- `character-select`: вибір класу; розділ customize — ввід seed.
- `map-window`: мапа поверху з вузлами стадій (звичайні, магазин, челенджі, вівтар, секрет, гардіан).
- `game-screen`: дошка, `lives` (серця), щити, `coins`, іконка артефакта з зарядами, реліквії, `toast` прокляття (іконки в нотифікаціях).
- `shop-window`: предмети з ціною й рідкістю, reroll, апгрейд артефакта.
- `end-screen`: Victory / Game Over.
- `settings-window`: анімації поля, туторіал вкл/викл, мова, повний екран, клавіші.
- `leaderboard`, `achievements-window`, `stats-window` (Steam), форма відгуку в грі.

## Фічі поза полем
- `meta-progression` (?) / `unlockables`: клас Gambler відкривається за 8 rerollʼів; артефакти — за секретною стадією.
- Режими: Standard, Hard (після проходження Standard), no-flags; `seed-input`.
- `tutorial` вбудований у перший забіг (для новачків у сапері), `localization` (8 мов на Steam).
- `leaderboard-online`, `achievements`, `stats`, `cloud-save` (Steam).

## Варіації й родичі
- [demoncrawl](demoncrawl.md) — найближчий родич: сапер-роглайт із предметами й поверхами; [dragonsweeper](dragonsweeper.md), [mamono-sweeper](mamono-sweeper.md) — сапер з HP; [minesweeper](minesweeper.md) — ядро однієї стадії; [dungeon-squire](dungeon-squire.md).
- Історія: класи → артефакти (0.6.0 зробив артефакти предметами магазину, клас Tracker прибрали як дубль Oracle); стадій 8×4 → 3×4 (0.4.0a).
- Осі варіацій: **ціна помилки** гра / серце / щит · **модифікатор правил** нема / реліквія (гравець обирає) / прокляття (гра нав'язує) · **прапорці** є / no-flags · **структура забігу** послідовність дошок / мапа поверху з вузлами.

## Цікавинки для курсу
- Прокляття як модифікатори правил (сховати клітини, «шум» у числах, видалити 10 % клітин) поверх одного двіжка — 🥉.
- Артефакт на зарядах з апгрейдом (активна здібність, що відкриває/замикає клітини) — 📎.
- Реліквії як пасивні прапорці правил (Safe Start, Chord Nullifier, Flag Nullifier) — 🥉: система хуків на подіях.
- Магазин з reroll і рідкістю предметів — 📎; клас, що відкривається за подвиг («8 rerollʼів») — 🌱.
- Опція «вибухнула міна далі рахується в числах» — 🌱, гарний приклад налаштування правила.
- Мапа поверху з типами вузлів (челендж з умовою, вівтар-пастка, секрет) — 🥈.

## Мапа на каталог
- Є: `cell-click` · `neighbor-count-clue` · `flood-reveal` (?) · `chord-click` ↔ акорд з урахуванням «замків» · `run-relics` ↔ реліквії · `inventory-items` ↔ consumables · `shop-between-levels` + `shop-catalog` ↔ магазин · `character-select` ↔ класи · `map-window` + `world-map` ↔ мапа поверху · `seed-share` ↔ seed у customize · `mode-select` + `difficulty-levels` ↔ Standard / Hard / no-flags · `player-death` ↔ серця · `fog-of-war` ↔ прокляття limited visibility · `leaderboard` · `achievements-window` · `tutorial-window` · `controls-remap` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+rule-curse` «Прокляття: стадія з модифікатором правил» · game-logic/difficulty · 🥉 · слот {kind}.
  - `+artifact-charges` «Активна здібність із зарядами й апгрейдом» · entities/state · 📎.
  - `+shop-reroll` «Перекинути вітрину за плату» · game-logic/economy · 🌱.
  - `+class-unlock-by-feat` «Клас відкривається за подвиг у забігу» · levels/progression · 🌱.
  - `+challenge-stage` «Стадія з умовою: нагорода лише за виконання» · levels/progression · 📎.
  - `+no-flags-mode` «Режим без прапорців» · game-logic/difficulty · 🌱.
  - `+exploded-mine-counts` «Опція: підірвана міна лишається в числах» · game-logic/constraints · 🌱.

## Пропозиції до словників
- `+trigger:stage_start` — початок стадії в забігу (момент накладання прокляття; ширше за `level_start`, бо стадія — частина поверху).
- `+effect:apply_curse` — накласти модифікатор правил на стадію.
- `+effect:charge` — витратити/додати заряд активного предмета.
- `+effect:lock_cell` — замкнути клітину від кліку (не прапорець, але рахується як він).
- `+effect:reroll` — перекинути випадковий набір (вітрина, нагорода).
- `+window:run-map` — мапа поверху забігу з вузлами різних типів (вужче за `map-window`).
- `+feature:no-flags` — режим без позначок.

## Джерела
- ⭐ [itch.io: Minato](https://noshuio.itch.io/minato) — HTML5/Windows/Linux, «in development», класи з артефактами-зарядами, consumables і relics, прокляття (limited visibility, empty cells, random numbers), бос світу, швидкість і мінімум кліків; коментарі — туторіал, Hard, leaderboard points.
- [Steam: Minato](https://store.steampowered.com/app/3165740/Minato/) — реліз 14.12.2026 (анонс), демо, гардіани з прокляттями, achievements / leaderboards / stats / cloud, 8 мов.
- [Девлог](https://noshuio.itch.io/minato/devlog) — патчі 0.2.0–0.6.6: Gambler за 8 rerollʼів, Scythe/Drill відкривають клітини, Hawk Eye, реліквії Mine Sweeper / Safe Start / Chord Nullifier / Flag Nullifier / Mana Band / Counting Lens, Decaying Ground 10 %, «exploded mines can still count», F — прапорець, 0 сердець — без продовження, стадії 8×4 → 3×4.
- [Update 0.6.0](https://noshuio.itch.io/minato/devlog/1608560/update-060) — випадкові мапи, Guardian, вівтар, 6 артефактів, Metal Detector «замикає», no-flags, seed, геймпад.
- [Update 0.5.0](https://noshuio.itch.io/minato/devlog/1122700/update-050) — структура поверху, 5 поверхів, апгрейд артефактів, Hard, рідкість предметів.
- [Update 0.4.0](https://noshuio.itch.io/minato/devlog/780536/update-040) — 6 босів, режими, seed, мапа світу, сховані скрині.

## Непевне
- (?) Форма поля (квадрат) і сусідство 8 — опис не каже; виходжу з «classic minesweeper».
- (?) Імена класів, крім Gambler / Oracle / Tracker (прибраний), і що робить кожна реліквія — лише назви.
- (?) Як саме працюють прокляття «empty cells» і «random numbers» (порожні без числа? числа з шумом?).
- (?) Чи щит поглинає вибух міни; що таке мана (Mana Band) — ймовірно, ресурс зарядів.
- (?) Кількість поверхів суперечлива: 5 (0.5.0) проти «last base game floor (floor 4)» (0.6.0).
- (?) Рахунок: як саме швидкість і кількість кліків переводяться в очки.
- (?) Рік: 2024 — дата першого девлогу (0.2.0, 06.08.2024); гра досі в розробці.
