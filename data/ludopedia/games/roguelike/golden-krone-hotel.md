---
title: Golden Krone Hotel
slug: golden-krone-hotel
aka: [GKH]
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2014
platforms: [PC (Windows, macOS, Linux)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/497800/Golden_Krone_Hotel/", best: true, note: "людина/вампір у кожному забігу, сонце як зброя, динамічне світло, без інвентаря, 40 зілль з ідентифікацією, 10 поверхів + гілки, weekly, 4/8 напрямків"}
  - {kind: wiki, url: "https://www.roguebasin.com/index.php/Golden_Krone_Hotel", note: "RogueBasin: форми, сонце, стелс від світла, зілля «одне з трьох», реліз 2014, автор Jeremiah Reid"}
  - {kind: official, url: "https://www.goldenkronehotel.com/", note: "офіційний сайт: вампір бачить у темряві, пʼє кров, вразливий до сонця й води"}
  - {kind: fandom, url: "https://www.goldenkronehotel.com/wiki/index.php?title=Tips", note: "офіційна вікі: сонце 6:00–18:00 зі сходу→півдня→заходу, скло розбивається, шкала вампіра, кров висихає, торгівець"}
  - {kind: fandom, url: "https://www.goldenkronehotel.com/wiki/index.php?title=Stats", note: "вікі: стати, формули атаки/захисту, бонуси форми, розмір (кажан/вовкулака)"}
  - {kind: fandom, url: "https://www.goldenkronehotel.com/wiki/index.php?title=Walkthrough", note: "вікі: гілки, боси з перснями, умова перемоги (поверх 10, ≥4 персні, Фейн)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=golden+krone+hotel+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-by-input, move-4dir, move-8dir, hp-damage, item-pickup, item-identification, status-effects, temporary-modes, unit-xp-skills, melee-vs-ranged, projectile-shot, line-of-sight-attack, chase-bfs, destructible-blocks, floor-types, environment-death, dungeon-generation, stairs-levels, round-currency, shop-catalog, permadeath, player-death, score-records, leaderboard, difficulty-levels, character-select, daily-puzzle, gui-render, console-render, keyboard-controls, controls-remap, +dual-form, +form-meter, +sunlight-beams, +day-night-clock, +dynamic-lighting, +stealth-by-light, +blood-pool-heal, +hp-decay, +auto-equip, +potion-of-three, +break-window, +branch-levels, +morgue-file]
proposes: ["+trigger:form_meter_full", "+cond:lit(cell, light)", "+cond:form(a, f)", "+cond:sees(a, b)", "+cond:time_of_day(op, t)", "+effect:switch_form(a, f)", "+effect:toggle_light(source)", "+effect:drink_blood", "+role:light-source", "+role:window", "+ui:form-meter", "+ui:clock", "+ui:hidden-indicator", "+window:morgue", "+window:weekly-window", "+feature:weekly-challenge", "+feature:morgue-file", "+axis:light=dynamic", "+card:dual-form", "+card:sunlight-beams"]
author: opus
date: 2026-11-09
---

# Golden Krone Hotel — роглайк, де ти по черзі людина й вампір, а сонячні промені з вікон — зона, що вбиває вампірів (і тебе)

## Суть
Герой спускається поверхами готелю «Золота корона», повного вампірів, і **в кожному забігу буває і людиною, і вампіром**. Людина слабка, але чаклує й регенерує; вампір сильний і швидкий, бачить у темряві, та втрачає HP з часом і лікується лише кровʼю. **Сонце — механіка поля**: з 6:00 до 18:00 промені падають з вікон і рухаються від східних стін до західних, і вампір (ворог або ти) у промені горить. Світло факелів визначає стелс: гасиш — ховаєшся.

## Поле і час
- Квадратна сітка; поверхи з кімнатами; 4 або 8 напрямків руху (опція).
- Покроково з швидкостями (актор діє частіше/рідше, 50–150 % базової швидкості).
- **Годинник доби**: день 6:00–18:00 — сонячні промені; ранок — зі східних стін, полудень — з південних, вечір — із західних, з півночі — ніколи; уночі — місячне світло (повня — перевертні).
- **Динамічне світло**: факели (вмикаються/вимикаються), сонце, місяць, світні заклинання; видимість і стелс залежать від освітлення клітини.
- 10 основних поверхів + гілки (сад-лабіринт, оранжерея, лазні, каналізація, бібліотека, кладовище…), частина випадково вибирається; підземний світ — нескінченний.
- Шари: підлога / стіни / скло (розбивається) / вода / калюжі крові (висихають) / предмети / монстри.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой (людина) | player | HP, мана, Str/Dex/Int, рівень ≤ 15, шкала вампіра | регенерує; чаклує; погано бачить у темряві |
| Герой (вампір) | player | Str ×1.5, швидкість +2, Int ×0.5, ідеальний нічний зір | не чаклує, не регенерує, втрачає HP з часом; лікується, пʼючи кров |
| Кажан / вовкулака (форми) | player | розмір 0 / 3 | інші форми вампіра/перевертня |
| Вампір-ворог | enemy | — | горить на сонці; уникає світла (?) |
| Зелені люди | enemy | — | сонце їх лікує й посилює |
| Балаури | enemy | бачать лише в темряві | — |
| Поганки (toadstools) | enemy | — | зʼявляються й рухаються лише вночі |
| Варколак | enemy | — | уночі стає вовкулакою |
| Маги-вороги | enemy | заклинання | влучають лише по прямій лінії від себе — можна відступити вбік |
| Боси гілок | boss | — | вбитий дає перстень |
| Фейн, вигнаний принц вампірів | boss | поверх 10 | фінальний бій |
| Торговець (hawker) | neutral | ціни ×2 для людини | продає |
| Сонячний промінь | zone | напрям за годинником | шкода вампірам на клітинах |
| Скло / вікно | static | ціле / розбите | розбити кулею чи BLAST — впустити сонце/місяць |
| Факел | switch | увімк/вимк | освітлює радіус; гасиш — тінь для стелсу |
| Вода | hazard | — | шкодить вампірам |
| Калюжа крові | pickup | висихає з часом | вампір пʼє → лікування |
| Зілля (40 видів) | pickup | невідоме — одне з трьох можливих | ефект і впізнання при вжитку; Blood — стати вампіром, Soul Elixir — людиною |
| Зброя / броня / сувої заклинань | pickup | — | **автопідбір і автоекіпірування**, інвентаря нема |
| Сходи | static | — | на наступний поверх або в гілку |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(target)` → ТО `move(hero, dir)`; ЯКЩО `occupied(target, enemy)` → ТО `custom: «удар впритул»`.
- КОЛИ `contact(hero, item)` → ТО `pickup(item)`; ЯКЩО спорядження → `custom: «автоматично вдягнути»`.
- КОЛИ `tick` → ЯКЩО `state(hero, human)` → ТО `counter(vamp, +1)`; КОЛИ `counter(vamp, ≥, max)` → ТО `transform(hero → vampire)`.
- КОЛИ `input(quaff Blood potion)` → ТО `transform(hero → vampire)`; `input(quaff Soul Elixir)` → ТО `transform(hero → human)`.
- КОЛИ `tick` → ЯКЩО `state(hero, vampire)` → ТО `hp(hero, −1)` (без регенерації); ЯКЩО `state(hero, human)` → ТО `heal(hero, n)`.
- КОЛИ `contact(vampire, blood pool)` → ТО `heal(vampire, n)`, `disappear_b`; КОЛИ `timer(every)` → ТО `custom: «кров висихає»`.
- КОЛИ `died(enemy)` → ТО `spawn_at(blood pool, cell)` (?).
- КОЛИ `custom: «годинник у 6:00–18:00»` → ТО `custom: «промені з вікон з боку сонця: схід → південь → захід»`.
- КОЛИ `enter(a, sunbeam)` → ЯКЩО `state(a, vampire)` → ТО `damage(sunlight)`; ЯКЩО `same(a, Green Man)` → ТО `heal(a, n)`; інші — імунні.
- КОЛИ `enter(vampire, water)` → ТО `damage(n)`.
- КОЛИ `input(shoot|BLAST, glass)` → ТО `set_cell(glass, broken)`, `custom: «сонце / місяць проходять у кімнату»`.
- КОЛИ `input(toggle torch)` → ТО `custom: «освітлення радіуса змінюється»`.
- КОЛИ `custom: «ворог не бачить героя (клітина в тіні, ворог без нічного зору)»` → ТО `set_state(hero, hidden)`: ворог не переслідує й не атакує; ЯКЩО `adjacent(enemy, hero)` або `custom: «шум»` → ТО стелс не рятує.
- КОЛИ `input(cast)` → ЯКЩО `state(hero, human)` and `custom: «мана ≥ ціна»` → ТО `custom: «ефект заклинання»`; вампір — `block`.
- КОЛИ `custom: «ворог чаклує»` → ЯКЩО `line_of_sight(enemy, hero)` and `custom: «на одній прямій»` → ТО `damage(n)`; інакше промах.
- КОЛИ `input(quaff unknown)` → ТО `custom: «один із трьох можливих ефектів; вид стає відомим»`.
- КОЛИ `custom: «ніч повні»` → ЯКЩО `custom: «перевертень / деякі люди»` → ТО `transform(→ werewolf)`; КОЛИ `custom: «ніч»` → ТО `spawn(toadstools)`, `transform(Varcolac → werewolf)`.
- КОЛИ `counter(xp, ≥, threshold)` → ТО `choose(primary stat +1)` (рівень ≤ 15).
- КОЛИ `died(branch boss)` → ТО `give(hero, ring)`.
- КОЛИ `custom: «поверх 10, Фейн»` → ЯКЩО `has(hero, 4 rings)` → ТО `custom: «фінальна розмова й вибір → фінал»`; `died(Fane)` → `win`.
- КОЛИ `hp_zero(hero)` → ТО `lose`, `window(morgue)`.
- Перемога: Фейн переможений на 10-му поверсі з ≥ 4 перснями (опційно — 9 типів перснів і нескінченний підземний світ). Поразка: смерть. Рахунок — `leaderboard` (?).

## Керування і ввід
- Клавіатура, миша або геймпад; перепризначення клавіш; 4 / 8 напрямків — опція.
- Пробіл — відпочинок (людина відновлює HP між боями).
- Заклинання з книги/слотів, зілля, вмикання факела — окремі дії (?).

## Вікна, меню, HUD
- `game-screen`: мапа (тайли або ASCII) з освітленням, `hp-bar`, мана, `form-meter` (шкала вампіра), `clock` (час доби), `hidden-indicator` (статус Hidden / «?» над ворогами), `message-log`, `tooltip` на монстрах.
- `character-select` — 18 маскувань/класів; `difficulty-select` — 3 режими.
- `shop-window` — торговець (ціни ×2 людині).
- Вибір стату при підвищенні рівня (`upgrade-window`).
- `weekly-window` — щотижневий челендж; `leaderboard`; `morgue` — файл-звіт забігу, яким можна поділитись.
- `tutorial-window`, `help-window` (підказки, описи монстрів), `settings-window` (тайли/ASCII, напрямки, керування), `main-menu`, `end-screen`.
- Переходи: `main-menu` → маскування → складність → гра; смерть/перемога → `morgue` → меню.

## Фічі поза полем
- `mode-daily`-подібне: Weekly challenge з онлайн-таблицею.
- `difficulty-presets` (3), `remap-controls`, `gamepad-support`, вибір тайли/ASCII, 4/8 напрямків.
- `tutorial`, `onboarding-hints`, `codex`-описи монстрів у підказках.
- Morgue-файли (shareable), таблиці рекордів.

## Варіації й родичі
- [brogue](brogue.md) — динамічне світло й стелс-радіус; [sil](sil.md) — стелс і світло; [dungeon-crawl-stone-soup](dungeon-crawl-stone-soup.md) — форми й гілки; [nethack](nethack.md) — перевертні й полікомбінація форм.
- Форма як стан з власними правилами: вовкулака в NetHack, «дві форми» — Ikaruga-подібна полярність.
- Осі варіацій: **форма** (одна / перемикання гравцем / за таймером / за предметом) · **світло** (статичне / факели / рухоме сонце за годинником) · **ідентифікація** (повна сліпа / «одне з трьох» / нема).

## Цікавинки для курсу
- Сонячні промені за годинником: напрям від часу доби, промінь з вікна до першої стіни — 🥉 (трасування з рухомим джерелом).
- Дві форми героя з різними правилами (регенерація vs розпад HP, магія vs сила) і шкала, що сама перемикає — 📎.
- Калюжі крові, що висихають, як ресурс лікування на мапі — 🌱.
- Стелс від освітлення: ворог без нічного зору не бачить тебе в тіні — 📎.
- Ідентифікація «одне з трьох»: обмежена невизначеність замість сліпого вгадування — 🌱.
- Розбити скло, щоб впустити сонце на ворогів-вампірів — 🌱.
- Без інвентаря: автопідбір і автоекіпірування — 🌱.

## Мапа на каталог
- Є: `move-4dir` + `move-8dir` (опція) · `hp-damage` · `item-pickup` · `item-identification` · `status-effects` · `temporary-modes` · `unit-xp-skills` · `melee-vs-ranged` · `projectile-shot` + `line-of-sight-attack` (заклинання лише по прямій) · `chase-bfs` · `destructible-blocks` (скло) · `floor-types` + `environment-death` (сонце, вода) · `dungeon-generation` · `stairs-levels` · `shop-catalog` · `permadeath` · `leaderboard` · `difficulty-levels` · `character-select` · `daily-puzzle` (weekly) · `controls-remap` · `console-render` + `gui-render`.
- **Нема** → пропозиції карток:
  - `+dual-form` «Дві форми героя з різними правилами» · entities/state · 📎 · слоти {forms, switch}.
  - `+form-meter` «Шкала, що з часом перемикає форму» · entities/state · 🌱.
  - `+sunlight-beams` «Сонячні промені з вікон за годинником» · entities/visibility · 🥉 · слоти {schedule, dirs}.
  - `+day-night-clock` «Годинник доби змінює правила» · game-logic/time · 📎.
  - `+dynamic-lighting`, `+stealth-by-light` «Невидимий у тіні для ворогів без нічного зору» · entities/visibility · 📎.
  - `+blood-pool-heal` «Калюжі-ресурс, що висихають» · entities/interact · 🌱.
  - `+hp-decay` «HP падає з часом» · entities/state · 🌱.
  - `+auto-equip` «Без інвентаря: автопідбір і автоекіпірування» · entities/interact · 🌱.
  - `+potion-of-three` «Невідоме зілля — одне з трьох» · entities/interact · 🌱.
  - `+break-window` «Розбите скло пропускає світло» · entities/interact · 🌱.
  - `+branch-levels` «Гілки, вибрані випадково з набору» · game-logic/levels · 📎.
  - `+morgue-file` «Текстовий звіт забігу» · game-logic/saves · 🌱.

## Пропозиції до словників
- `+trigger:form_meter_full` — шкала форми заповнилась.
- `+cond:lit(cell, light)` — клітина освітлена (сонцем/факелом/місяцем); `+cond:form(a, f)` — герой у формі; `+cond:sees(a, b)` — A бачить B з урахуванням світла й нічного зору (ширше за `line_of_sight`); `+cond:time_of_day(op, t)`.
- `+effect:switch_form(a, f)` (окремо від `transform`: зберігає героя, міняє набір правил); `+effect:toggle_light(source)`; `+effect:drink_blood`.
- `+role:light-source` — факел/вікно, що світить радіусом/променем; `+role:window` — скло, що пропускає сонце й розбивається.
- `+ui:form-meter`, `+ui:clock`, `+ui:hidden-indicator`.
- `+window:morgue`, `+window:weekly-window`.
- `+feature:weekly-challenge`, `+feature:morgue-file`.
- `+axis:light=dynamic` — світло як правило поля.
- `+card:dual-form`, `+card:sunlight-beams`.

## Джерела
- ⭐ [Steam](https://store.steampowered.com/app/497800/Golden_Krone_Hotel/) — дві форми, сонце як зброя, динамічне світло, без інвентаря, 40 зілль, 31 заклинання, 17 здібностей вампіра, 18 маскувань, 10 поверхів + 22 гілки, weekly, 3 складності.
- [RogueBasin](https://www.roguebasin.com/index.php/Golden_Krone_Hotel) — стелс від світла, зілля «одне з трьох», реліз 16.03.2014, автор.
- [Офіційний сайт](https://www.goldenkronehotel.com/) — вампір: темрява, кров, сонце, вода.
- [Вікі: Tips](https://www.goldenkronehotel.com/wiki/index.php?title=Tips) — годинник сонця, скло, шкала вампіра, кров висихає, Hidden, заклинання по прямій, нічні монстри.
- [Вікі: Stats](https://www.goldenkronehotel.com/wiki/index.php?title=Stats) — формули, бонуси форми, розмір форм.
- [Вікі: Walkthrough](https://www.goldenkronehotel.com/wiki/index.php?title=Walkthrough) — гілки, персні, Фейн, умова перемоги.

## Непевне
- (?) Чи кров зʼявляється з кожного вбитого ворога і скільки лікує — «пʼє пролиту кров» без деталей.
- (?) Як саме керувати заклинаннями (слоти/книга), чи є явна команда перемикання форми, окрім зілль і шкали.
- (?) Як вороги-вампіри уникають світла; що дає кажан-форма, крім розміру 0.
- (?) Рахунок для таблиці рекордів — сторінку Score не відкривав.
- (?) Гілки: Steam каже 22, RogueBasin — 7 (старіша версія), вікі — 20 назв.
