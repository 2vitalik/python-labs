---
title: Moria / Angband
slug: angband
aka: [Angband, Moria, UMoria, VMS Moria]
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
year: 1990
platforms: [PC (Windows, macOS, Linux, Unix), Android, DOS, Amiga, Atari ST (Moria)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Angband_(video_game)", best: true, note: "суть: місто з крамницями, 100 поверхів до Морґота, процедурні рівні, сейв лише живого героя, варіанти"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Moria_(1983_video_game)", note: "Moria: перше місто з 6 крамницями, рівень перегенеровується на кожних сходах, Балроґ на дні"}
  - {kind: official, url: "https://angband.readthedocs.io/en/latest/", note: "офіційний мануал Angband 4.2"}
  - {kind: other, url: "https://angband.readthedocs.io/en/latest/dungeon.html", note: "мануал: 8 будівель міста, 50 футів на рівень, символи рельєфу/предметів/монстрів, світло, Word of Recall, відчуття рівня, Саурон і Морґот"}
  - {kind: other, url: "https://angband.readthedocs.io/en/latest/option.html", note: "мануал: опції народження (connected stairs, force descent, persistent levels, no selling, randarts) і автодослідження"}
  - {kind: other, url: "https://angband.readthedocs.io/en/latest/playing.html", note: "мануал: команди, відпочинок, переривання, лог повідомлень, знання"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=angband+4.2+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-by-input, move-8dir, dungeon-generation, stairs-levels, hp-damage, inventory, inventory-items, inventory-limit, item-pickup, item-identification, hunger-clock, status-effects, unit-xp-skills, melee-vs-ranged, projectile-shot, chase-bfs, random-walk, impassable-cells, dig-terrain, round-currency, shop-catalog, shop-buyback, shop-between-levels, permadeath, player-death, score-records, save-single-slot, fog-of-war, message-log, status-panel, keyboard-controls, console-render, gui-render, difficulty-levels, rule-variants, codex-window, character-select, +town-level, +level-regenerate, +connected-stairs, +level-feeling, +word-of-recall, +light-source, +home-storage, +birth-options, +auto-explore, +remembered-map, +search-hidden, +run-command, +character-dump]
proposes: ["+trigger:level_feeling", "+effect:regenerate_level", "+effect:recall(delay)", "+effect:identify", "+cond:lit", "+cond:depth(op, n)", "+role:stairs", "+role:shop-entrance", "+window:store-window", "+window:home-window", "+window:knowledge-menu", "+window:character-sheet", "+window:character-create", "+window:birth-options", "+ui:level-feeling-indicator", "+ui:depth-indicator", "+ui:more-prompt", "+feature:birth-options", "+feature:character-dump", "+feature:permadeath", "+axis:session=run", "+card:level-regenerate", "+card:level-feeling"]
author: opus
date: 2026-11-09
---

# Moria / Angband — спуск у нескінченне підземелля, де кожні сходи створюють новий рівень, а глибина в футах — і є шкала складності

## Суть
Герой (раса + клас) починає в місті з крамницями й спускається по сходах. **Рівні не постійні**: зійшов зі сходів — старий рівень зник, на тій самій глибині можна згенерувати скільки завгодно нових. Тому гра зводиться до одного числа — **глибини** (50 футів на рівень): що глибше, то сильніші монстри й кращі скарби, і гравець сам вирішує, коли пірнати. У Moria (1983) мета — Балроґ на дні; в Angband (1990) — Саурон на 99-му і Морґот на 100-му рівні.

## Поле і час
- Квадратна сітка; рівень займає кілька екранів (камера прокручується) (?); 8 напрямків руху.
- Місто — постійний рівень 0 з 8 входами в будівлі (цифри `1`–`8`); підземелля — рівні 1–100 і далі (?), Lev 1 = 50 ft, Саурон — 4950 ft.
- **Перегенерація:** покинув рівень сходами — повернутися в той самий регіон неможливо. Монстри користуються сходами, але не женуться крізь них.
- Видимість: без джерела світла чи освітленої кімнати не бачиш; світло — факел/лампа з паливом; бачене памʼятається на мапі.
- Покроково: швидкість героя й монстрів визначає, як часто хто діє (?).
- Шари клітини: рельєф (граніт, жили магми/кварцу зі скарбом, щебінь, двері, пастки, лава, гліф) + предмет (один на клітину) + монстр.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой `@` | player | раса, клас, HP, мана, стати, рівень, ситість, світло | рух 8 напрямків; атака входом у клітину монстра |
| Монстр (`a`–`Z`, ~60 класів символів) | enemy | HP, швидкість, атаки, заклинання | помічає й переслідує; деякі блукають, деякі кличуть інших |
| Унікальний монстр | boss | імʼя з легендаріуму | гарантовано один; дає артефакти (?) |
| Саурон | boss | рівень 99 | вбивство створює сходи на 100-й |
| Морґот | boss | рівень 100 | глибше не пустить, доки живий; може прийти сам |
| Балроґ (Moria) | boss | найнижчий рівень | вбив — перемога |
| Міщани `t` | neutral | — | дрібні, крадуть або заважають (?) |
| Стіна граніт `#` | static | — | блокує рух і погляд |
| Жила `%` / зі скарбом `*` | static | — | копається; `*` дає золото |
| Щебінь `:` | static | звичайний / прохідний | розчищається або проходиться повільно (?) |
| Двері `+` / `'` | gate | закриті / замкнені / відкриті / зламані | відкрити, зламати замок, вибити |
| Таємні двері | gate | вигляд стіни | знаходиться, коли поруч (?) |
| Пастка `^` / прихована | hazard | тип | шкода, телепорт, провал на нижчий рівень (?) |
| Лава `#` | hazard | — | шкода вогнем (?) |
| Гліф `;` | static | — | монстри не можуть ступити (?) |
| Сходи `<` / `>` | static | — | перехід на ±1 рівень і генерація нового |
| Вхід у будівлю `1`–`8` | static | номер | відкриває крамницю / дім |
| Предмети (`!` `?` `=` `"` `-` `_` `|` `(` `[` `$` …) | pickup | невідомий вид, руни, зачарування | пʼють, читають, вдягають, кидають; невідомі — до вжитку |
| Артефакт | pickup | унікальний | можна втратити, якщо лишив на рівні (опція) |
| Дім `8` | container | склад | зберігає предмети між спусками |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(target)` → ТО `move(hero, dir)`; ЯКЩО `occupied(target, monster)` → ТО `custom: «атака впритул»`; ЯКЩО `cell(target, door)` → ТО `custom: «відчинити»` (?).
- КОЛИ `enter(hero, stairs down)` and `input(>)` → ТО `custom: «створити новий рівень на глибині +1»`, старий рівень зникає.
- КОЛИ `input(<)` на сходах вгору → ТО `custom: «новий рівень на глибині −1»`; рівень 0 — місто.
- КОЛИ `level_start` → ЯКЩО `custom: «опція connected stairs»` → ТО `spawn_at(hero, stair of opposite kind)`.
- КОЛИ `level_start` → ТО `message(danger feeling 1–9)` за монстрами при вході й глибиною; КОЛИ `custom: «досліджено досить»` → ТО `message(object feeling)`; артефакт — `$`.
- КОЛИ `input(read Word of Recall)` → ТО `custom: «через затримку: з підземелля — у місто; з міста — на найбільшу досягнуту глибину»`; повторне читання скасовує.
- КОЛИ `input(enter shop)` → ТО `window(store-window)`: `currency(−price)`, `give(item)` / продаж `currency(+n)` (з опцією no selling — лише ідентифікація).
- КОЛИ `custom: «нема світла ні освітленої кімнати»` → ТО `custom: «не бачиш, не читаєш, не чаклуєш»`; КОЛИ `timer(every)` → ТО `counter(fuel, −1)`; ЯКЩО мало — `message`.
- КОЛИ `timer(every)` → ТО `counter(food, −)`; ЯКЩО 0 → `set_state(hero, faint)` (переривання) (?).
- КОЛИ `input(eat|quaff|read)` → ЯКЩО `custom: «вид невідомий»` → ТО `custom: «ефект + вид стає відомим»`.
- КОЛИ `input(tunnel)` → ЯКЩО `cell(target, vein|rubble)` → ТО `set_cell(target, floor)`; ЯКЩО `cell(target, treasure vein)` → ТО `currency(+n)`.
- КОЛИ `contact(hero, hidden trap)` → ТО `reveal(trap)`, `custom: «ефект пастки»`.
- КОЛИ `custom: «монстр бачить героя»` → ТО `move(monster, toward hero)` (шляхом) або `custom: «заклинання / дихання / виклик»`.
- КОЛИ `input(rest|run|repeat)` → ТО `custom: «повторювати, доки не перервуть»`; КОЛИ `custom: «монстр у полі зору / удар / втрата HP / пастка / знахідка»` → ТО `custom: «переривання»`.
- КОЛИ `died(monster)` → ТО `custom: «досвід»`; ЯКЩО `counter(xp, ≥, threshold)` → ТО `custom: «рівень +1»`; ЯКЩО `prob(p)` → ТО `spawn(item)`.
- КОЛИ `died(Sauron)` → ТО `spawn(stairs to 100)`.
- КОЛИ `died(Morgoth)` → ТО `win` (статус WINNER; `Q` — у таблицю рекордів).
- КОЛИ `hp_zero(hero)` → ТО `lose`; сейв героя більше не відкривається (permadeath).
- КОЛИ `custom: «опція force descent»` → ТО `custom: «сходи вгору не діють; вниз — на 1 нижче максимуму»`.
- КОЛИ `custom: «опція lose artifacts»` and `leave(hero, level)` → ЯКЩО `custom: «невідомий артефакт лишився на рівні»` → ТО `custom: «артефакт втрачено назавжди»`.
- Перемога: вбити Морґота (Angband) / Балроґа (Moria). Поразка: смерть героя. Рахунок: таблиця рекордів (досвід, глибина) (?).

## Керування і ввід
- Клавіатура: цифри/стрілки (оригінальна розкладка) або `hjklyubn` (roguelike-розкладка); `R` — відпочинок, `E` — їсти, `F` — заправити світильник, `C` — лист персонажа, `~` — знання, `[` — список монстрів у полі зору, `l` — оглянути, `^p` — історія повідомлень, `^f` — відчуття рівня, `Q` — відставка.
- Біг (Shift+напрям), повторні команди з лічильником, ціль за замовчуванням.
- Опція autoexplore_commands: команди сходів ведуть до найближчих відомих сходів, `p` — до найближчої недослідженої клітини.
- Миша в тайловому клієнті (?).

## Вікна, меню, HUD
- `game-screen`: мапа (ASCII або тайли), бічна панель `stat-panel` (раса, клас, рівень, стати, HP/SP, AC, золото), рядок `message-log` з `more-prompt`, нижній рядок статусів (`depth-indicator` у футах, голод, `level-feeling-indicator` LF:x-y, «Recall»).
- `character-create`: раса, клас, стати (point-based / roller) (?), `birth-options`.
- `store-window` (1–7) і `home-window` (8): список товарів з цінами, купити/продати/оглянути.
- `inventory-window` / екіпірування; `character-sheet` (`C`); `knowledge-menu` (`~`: відомі предмети, монстри, артефакти, руни) = `codex-window`; історія повідомлень (`log-window`); `settings-window` (опції інтерфейсу).
- `end-screen`: надгробок / дамп персонажа; `leaderboard` (рекорди).
- Переходи: старт → `character-create` → місто → сходи → підземелля; `Q` або смерть → `end-screen`.

## Фічі поза полем
- `birth-options`: connected stairs, force descent, no recall (разом = ironman), persistent levels (експериментально), lose artifacts, no selling, randarts, percent damage, знати всі руни/види з народження.
- Опції інтерфейсу: автопідбір, переривання на рух видимого монстра, auto-more, показ шкоди.
- `save-single-slot` з permadeath; дамп персонажа в текстовий файл (?).
- Численні варіанти (140+): Zangband, MAngband (мультиплеєр), NPPAngband, Sil.
- Відкритий код (GPLv2), борг — ШІ, що грає сам (у мануалі).

## Варіації й родичі
- Rogue → Moria (місто й перегенерація) → Angband → варіанти; [sil](sil.md) (Angband за Толкіном зі стелсом), Tales of Maj'Eyal.
- Протилежність: [nethack](nethack.md), [brogue](brogue.md) (постійні поверхи); [rogue](rogue.md); [dungeon-crawl-stone-soup](dungeon-crawl-stone-soup.md) (постійні рівні, автодослідження).
- Вплив: Diablo (рандомні рівні й предмети, за словами Brevik).
- Осі варіацій: **рівні** (постійні / перегенеруються на сходах / одноразові «лише вниз») · **глибина** (фіксований фінал / нескінченна) · **хаб** (нема / місто з крамницями / дім-склад) · **складність** (пресети / опції народження).

## Цікавинки для курсу
- Перегенерація рівня на кожних сходах + seed на глибину: генерація як функція від числа — 📎.
- Глибина як шкала складності: таблиці монстрів/предметів за мінімальною глибиною — 📎.
- Відчуття рівня: оцінка небезпеки за вмістом при генерації, 9 градацій — 🌱.
- Word of Recall з затримкою: телепорт місто ⇄ найглибший рівень — 🌱.
- Опції народження як конструктор варіантів правил (connected stairs, force descent, persistent levels) — 📎.
- Переривання повторних дій (біг, відпочинок) за подіями — 📎.
- Автодослідження до найближчої невідомої клітини — 🥇 (BFS по памʼяті мапи).

## Мапа на каталог
- Є: `move-8dir` · `dungeon-generation` · `stairs-levels` · `hp-damage` · `inventory` + `inventory-items` + `inventory-limit` · `item-pickup` · `item-identification` · `hunger-clock` · `status-effects` · `unit-xp-skills` · `melee-vs-ranged` · `projectile-shot` · `chase-bfs` · `random-walk` · `dig-terrain` (жили й щебінь) · `round-currency` · `shop-catalog` + `shop-buyback` (продаж) · `permadeath` · `score-records` · `fog-of-war` · `message-log` · `status-panel` · `console-render` + `gui-render` · `rule-variants` (опції народження) · `codex-window` (знання) · `character-select`.
- **Нема** → пропозиції карток:
  - `+town-level` «Місто-рівень 0 з входами в крамниці» · interface/menus · 📎.
  - `+level-regenerate` «Покинутий рівень зникає; новий на тій самій глибині» · game-logic/levels · 📎.
  - `+connected-stairs` «Стартуєш на сходах протилежного типу» · game-logic/levels · 🌱.
  - `+level-feeling` «Оцінка небезпеки/скарбів рівня при вході» · game-logic/levels · 🌱 · слоти {grades}.
  - `+word-of-recall` «Відкладений телепорт хаб ⇄ максимальна глибина» · entities/interact · 🌱 · слот {delay}.
  - `+light-source` «Світло з паливом визначає видимість» · entities/visibility · 📎.
  - `+home-storage` «Дім-склад між спусками» · game-logic/economy · 🌱.
  - `+birth-options` «Опції народження змінюють правила забігу» · game-logic/settings · 📎.
  - `+character-dump` «Текстовий дамп персонажа» · game-logic/saves · 🌱.
  - Перевикористано: `+auto-explore`, `+remembered-map`, `+search-hidden`, `+run-command`.

## Пропозиції до словників
- `+trigger:level_feeling` — рівень повідомив свою оцінку при вході.
- `+effect:regenerate_level` — створити новий рівень на глибині; `+effect:recall(delay)` — відкладений телепорт хаб ⇄ глибина; `+effect:identify`.
- `+cond:lit` — клітина/герой освітлені; `+cond:depth(op, n)` — глибина порівняно з N (ширше за `level`, бо рівні нескінченні й безіменні).
- `+role:stairs`; `+role:shop-entrance` — клітина-вхід у вікно крамниці.
- `+window:store-window`, `+window:home-window`, `+window:knowledge-menu`, `+window:character-sheet`, `+window:character-create`, `+window:birth-options`.
- `+ui:level-feeling-indicator`, `+ui:depth-indicator` (глибина у футах), `+ui:more-prompt`.
- `+feature:birth-options`, `+feature:character-dump`, `+feature:permadeath`.
- `+axis:session=run`.
- `+card:level-regenerate`, `+card:level-feeling`.

## Джерела
- ⭐ [Wikipedia: Angband](https://en.wikipedia.org/wiki/Angband_(video_game)) — мета (100 рівнів, Морґот), місто, процедурні рівні, сейв лише живого героя, варіанти, історія.
- [Wikipedia: Moria](https://en.wikipedia.org/wiki/Moria_(1983_video_game)) — 6 крамниць, перегенерація рівня, Балроґ, раси/класи, сейв лише при виході.
- [Мануал: Exploring the Dungeon](https://angband.readthedocs.io/en/latest/dungeon.html) — 8 будівель, 50 ft, символи, світло, Word of Recall, відчуття рівня (9+9 градацій), Саурон 99, Морґот 100.
- [Мануал: опції](https://angband.readthedocs.io/en/latest/option.html) — опції народження, автодослідження, переривання.
- [Мануал: Playing the Game](https://angband.readthedocs.io/en/latest/playing.html) — команди, відпочинок і переривання, лог, знання, лист персонажа.

## Непевне
- (?) Система енергії/швидкості, розмір рівня й прокрутка, гліф (монстри не ступають), лава — у прочитаних сторінках без деталей.
- (?) Ідентифікація через руни (4.2) і чи типи предметів невідомі до вжитку — з памʼяті.
- (?) Пастка-провал на нижній рівень, таємні двері знаходяться автоматично поруч (4.2 прибрала пошук) — з памʼяті.
- (?) Голод: стани й непритомність — у мануалі лише згадка «fainting from hunger».
- (?) Дамп персонажа при смерті, формула рахунку, створення персонажа (point-based/roller) — не перевірено.
- (?) `year` — Angband 1990 (Moria 1983); файл описує обидві як одну лінію.
