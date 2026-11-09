---
title: Rift of the NecroDancer
slug: rift-of-the-necrodancer
aka: [RotN, Rift]
family: tower-lanes
also: []
klass: cursor
axes:
  field: square
  time: rhythm
  opponent: none
  info: partial
  random: none
  goal: survive
year: 2025
platforms: [PC, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Rift_of_the_NecroDancer", best: true, note: "3 смуги, вороги міняють смугу або потребують кількох ударів, HP і їжа, режими: сюжет, вибір етапу з 4 складностями, практика, Remix, daily, боси, мініігри, власні етапи"}
  - {kind: steam, url: "https://store.steampowered.com/app/2073250/Rift_of_the_NecroDancer/", note: "Brace Yourself Games / Tic Toc, Klei, 05.02.2025; 4 складності, Remix, Daily, редактор, Workshop, 5 босів, 5 мініігор"}
  - {kind: other, url: "https://jovixie.pages.dev/posts/every-enemy-type-movement-pattern-and-trap-in-rift-of-the-necrodancer", note: "фан-гайд: 23 вороги з кількістю ударів і рухом, тіні (on/off-beat), пастки"}
  - {kind: other, url: "https://www.siliconera.com/review-rift-of-the-necrodancer-can-be-a-lot/", note: "огляд: 10 HP, їжа лікує, кажани за кольором, блейдмайстер, боси dodge→counter, мініігри"}
  - {kind: other, url: "https://rogueliker.com/rift-of-the-necrodancer-review/", note: "огляд: зомбі по діагоналі, гарпії з паузою, Remix, Workshop"}
  - {kind: other, url: "https://steamcommunity.com/app/2073250/guides/", note: "гайди Steam: очки, калібрування затримки, редактор"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Rift+of+the+NecroDancer+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [hp-damage, enemy-waves, last-line-defense, enemy-reached-base, pattern-automaton, speed-per-type, teleport-pair, combo-multiplier, event-points, difficulty-levels, daily-puzzle, in-game-editor, level-exchange, level-select, leaderboard, background-music, game-screen, end-screen, mode-select, +lane-grid, +beat-tick, +missed-beat, +lane-switch-on-hit, +hold-note, +multi-hit-enemy, +split-on-death, +off-beat-movement, +lane-redirect-trap, +masked-enemy, +boss-fight, +practice-mode, +remix-generator, +latency-calibration, +workshop-sharing]
proposes: ["+trigger:beat", "+trigger:missed_beat", "+trigger:song_end", "+cond:on_beat", "+effect:reset_combo", "+effect:hold", "+role:food", "+ui:action-row", "+ui:timing-indicator", "+ui:vibe-meter", "+window:calibration-window", "+feature:custom-music", "+feature:latency-calibration", "+card:hold-note", "+card:lane-switch-on-hit"]
author: opus
date: 2026-11-09
---

# Rift of the NecroDancer — ритм-оборона на 3 смугах: монстри спускаються в такт, бий у смугу, коли ворог у рядку дії

## Суть
Спін-оф Crypt of the NecroDancer у жанрі «нотної доріжки», де ноти — це монстри: вони спускаються трьома смугами до нижнього **рядка дії**, і гравець тисне кнопку смуги в такт, коли ворог там. Кожен вид ворога — свій автомат руху й реакції на удар: кажан після удару перескакує в іншу смугу, скелет відбігає, череп розпадається на два скелети, броненосця треба вдарити тричі за один біт. Пропущений ворог ранить Каденс; HP = 0 — етап провалено.

## Поле і час
- Поле — сітка 3 смуги × N рядів; рядок дії — нижній, лише там удар зараховується. Ворог зʼявляється згори й рухається вниз на 1 ряд за крок (гарпії — на 2).
- Тік = біт музики (`time: rhythm`); тінь ворога визначає, на яку долю він ходить: на біт, на офбіт або рідкісна «ні на біт, ні на офбіт».
- Біти розписані в бітмапі етапу (кожен обʼєкт має точний номер біта); Remix генерує нову розкладку з тим самим ритмом.
- Інформація частково прихована: пастка «?» маскує вид ворога; решта видно наперед.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Каденс (Cadence) | player | 10 HP | стоїть під полем; удар у смугу за кнопкою |
| Зелений слиз | enemy | 1 удар (?) | спускається на біт |
| Синій слиз | enemy | 2 удари (?) | спускається на біт |
| Жовтий скелет | enemy | 2 удари | на біт; після 1-го удару біжить назад до упору |
| Чорний скелет | enemy | 3 удари | як жовтий, відбігає після 2-го удару |
| Скелет зі щитом (жовтий / чорний / подвійний щит) | enemy | щит — 2 удари в рядку дії (подвійний — 3) | після щита — як відповідний скелет |
| Синій кажан | enemy | 2 удари, напрям погляду | після удару перескакує в сусідню смугу за поглядом |
| Червоний кажан | enemy | 3 удари | після 1-го — у смугу за поглядом, після 2-го — назад |
| Жовтий кажан | enemy | 3 удари | після 1-го і 2-го — у смугу за поглядом |
| Зомбі | enemy | 1 удар | щобіт стрибає вбік, міняючи смугу |
| Червоний зомбі | enemy | 1 удар | як зомбі, але через край — на протилежну смугу (тор) |
| Вірм | enemy | довжина (налаштовується в редакторі) | тримати кнопку від голови до хвоста в рядку дії |
| Гарпія / синя / червона | enemy | 1 / 2 / 1 удар | ривок на 2 ряди з паузою; червона — без паузи |
| Блейдмайстер / синій | enemy | 1 / 2 удари | виймає меч (телеграф), потім ковзає з будь-якої відстані в рядок дії — бити наступного біта |
| Череп / червоний / синій | enemy | 1 / 2 / 2 удари | знищений — розпадається на 2 скелети в двох інших смугах; червоний після 1-го удару змінює ряд |
| Броненосець жовтий / синій / червоний | enemy | 3 удари за біт / лише перші 2 / лише 1-й і 3-й | бити в межах одного біта |
| Їжа | pickup (`+role:food`) | лікування | спускається смугою; влучити — `heal`; частина Vibe Chain |
| Пастка-стрілка | terrain | напрям | переводить ворога в смугу за стрілкою |
| Вогняна пастка | terrain | — | підпалює ворога, той біжить уперед швидко |
| Портал входу / виходу | terrain | колір | ворог зникає у вході й виходить з виходу того ж кольору |
| Пастка «?» | terrain | — | ворог стає знаком питання, рух і удари — ті самі |
| Бос | boss | фази | атакує; гравець ухиляється в такт, потім контратакує |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «beat»` → ЯКЩО `state(enemy, on_beat_shadow)` → ТО `move(enemy, down)`; тінь off-beat — на офбіт.
- КОЛИ `input(lane)` → ЯКЩО `occupied(action_row[lane], enemy)` and `custom: «у вікні влучання навколо біта»` → ТО `damage(enemy, 1)`, `score(+n)`, `counter(combo, +1)`.
- КОЛИ `input(lane)` → ЯКЩО `custom: «поза вікном»` → ТО `custom: «MISS з позначкою E/L (рано/пізно)»`.
- КОЛИ `reach(enemy, below_action_row)` → ТО `damage(cadence, 1)`, `custom: «reset_combo»`.
- КОЛИ `hp_zero(cadence)` → ЯКЩО `not mode(practice)` → ТО `lose`; у практиці HP іде в мінус (показ «наскільки близько»).
- КОЛИ `custom: «song_end»` → ЯКЩО `custom: «HP > 0»` → ТО `win`, `window(end-screen)`.
- КОЛИ `input(lane)` → ЯКЩО `occupied(action_row[lane], bat)` and `custom: «удар не останній»` → ТО `damage(bat, 1)`, `move(bat, facing_lane)`; червоний після 2-го — `move(bat, back)`.
- КОЛИ `input(lane)` → ЯКЩО `occupied(action_row[lane], yellow_skeleton)` and `custom: «перший удар»` → ТО `damage(skeleton, 1)`, `custom: «біжить назад угору до упору»`.
- КОЛИ `tick` → ЯКЩО `state(zombie, alive)` → ТО `move(zombie, side)`; червоний — `wrap(zombie)`.
- КОЛИ `enter(wyrm_head, action_row)` → ТО `custom: «hold: тримати кнопку до хвоста»`; відпустив раніше → пропуск.
- КОЛИ `destroyed(skull)` → ТО `spawn_at(skeleton ×2, дві інші смуги)`.
- КОЛИ `input(lane)` на броненосці → ЯКЩО `custom: «3 удари в межах одного біта (синій — 2, червоний — 1-й і 3-й)»` → ТО `disappear`.
- КОЛИ `state_on(blademaster, sword_drawn)` → ТО `custom: «наступного біта ковзає в рядок дії»`.
- КОЛИ `enter(enemy, arrow_trap)` → ТО `move(enemy, arrow_lane)`; `enter(enemy, fire_trap)` → ТО `speed(enemy, +n)`.
- КОЛИ `enter(enemy, portal_in[c])` → ТО `teleport(enemy, portal_out[c])`.
- КОЛИ `enter(enemy, mystery_trap)` → ТО `custom: «вигляд → ?, поведінка без змін»`.
- КОЛИ `input(lane)` на їжі → ТО `heal(cadence, n)`.
- КОЛИ `custom: «влучено всі обʼєкти Vibe Chain (їжу — влучити, вірма — дотримати)»` → ТО `counter(vibe, +1)`; КОЛИ `input(vibe)` → ЯКЩО `counter(vibe, >, 0)` → ТО `multiplier(×k)` (?) на час дії.
- Бос: КОЛИ `custom: «атака боса»` → ЯКЩО `input(dodge)` у такт → ТО `custom: «вікно контратаки»`; інакше `damage(cadence, n)`.
- Перемога: дожити до кінця пісні · Поразка: HP = 0 · Рахунок: очки за влучання + комбо + Vibe; таблиці рекордів (daily — глобальна).

## Керування і ввід
- Три кнопки смуг (напрямки на клавіатурі/геймпаді); утримання — для вірмів; окрема дія Vibe (?).
- Налаштування Invert Up/Down, калібрування затримки аудіо/вводу, індикатор E/L для промахів.
- У меню утримання Up/Down — автопрокрутка, F — додати етап в улюблені.

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Story · Rhythm Rifts (вибір етапу) · Remix · Daily Challenge · Practice · Minigames · Custom (Workshop).
- `level-select` + `difficulty-select`: Easy / Medium / Hard / Impossible на кожен етап; улюблені.
- `game-screen`: 3 смуги, `+ui:action-row`, `hp-bar` (серця), `combo-meter`, `score`, `+ui:vibe-meter`, `+ui:timing-indicator` (Perfect/MISS, E/L), фото-портрети персонажів.
- `end-screen`: очки, влучання, їжа й Vibe-ланцюги (лічильник по всьому бітмапу), рекорд.
- `leaderboard` — глобальні таблиці Daily; `shop-window`-подібне розблокування за діаманти (Impossible — 100, Remix — 60).
- `dialogue-window` — сюжетні катсцени у стилі візуальної новели; `+window:calibration-window` — калібрування затримки.
- `editor-window` — редактор Rifted (окремий застосунок): шари ворогів / пасток / спецобʼєктів, номер біта на кожному обʼєкті, параметри (довжина вірма, ривок блейдмайстра).
- `settings-window`: Invert Up/Down, E/L-індикатор, швидкість відтворення (практика).

## Фічі поза полем
- `mode-practice` (без поразки, з 50 % швидкістю відтворення), `mode-daily` (Remix зі спільним seed + таблиця), `difficulty-presets` ×4, assist mode у важких мініграх.
- Remix — процедурна розкладка ворогів із ритмом оригінального етапу (`+remix-generator`).
- `level-editor` + `level-sharing` через Steam Workshop; власна музика для етапів (`+feature:custom-music`).
- Модифікатори (Coda, Golden Lute) — змінюють умови/нагороди (?); профільні предмети за daily; досягнення; `cloud-save`.

## Варіації й родичі
- Батько: [crypt-of-the-necrodancer](../roguelike/crypt-of-the-necrodancer.md) — ті самі вороги, але там вони ходять полем-підземеллям навколо аватара; тут — трьома смугами до рядка дії. Cadence of Hyrule — ритм-роглайк, не смуговий.
- Жанрові родичі: нотні доріжки (Guitar Hero, osu!mania) — ноти без поведінки; тут кожна «нота» має автомат.
- Родичі в сімʼї: [plants-vs-zombies](plants-vs-zombies.md) (вороги йдуть смугами до краю), [mega-man-star-force](mega-man-star-force.md) (3 смуги, ухил у бік).
- **Осі варіацій**: реакція ворога на удар — зникає / потребує N ударів / міняє смугу / відступає / розпадається · такт руху — біт / офбіт / рідше · ввід — тап / утримання / серія в одному біті.

## Цікавинки для курсу
- Тік = біт: метроном + вікно влучання + калібрування затримки — 🥉 (аудіосинхронізація).
- Ворог як автомат «рух у такт + реакція на удар» (кажан, скелет, зомбі-тор, череп-розпад) — 📎 кожен, 🥉 за родину.
- Утримання для вірма (head→tail) — 🌱.
- Броненосець: 3 удари всередині одного біта з масками «які з трьох потрібні» — 📎.
- Пастки на смугах (стрілка, портали за кольором, «?» маскування) — 📎.
- Remix: згенерувати бітмап, зберігши ритм і змінивши ворогів/смуги, з перевіркою прохідності — 🥇.
- Редактор бітмапів із шарами обʼєктів і номером біта — 🥈.

## Мапа на каталог
- Є: `hp-damage` ↔ HP Каденс і удари по ворогах; `enemy-waves` + `last-line-defense` + `enemy-reached-base` ↔ ворог пройшов рядок дії; `pattern-automaton` + `speed-per-type` ↔ поведінки ворогів; `teleport-pair` ↔ портали; `combo-multiplier` + `event-points` ↔ очки; `difficulty-levels`; `daily-puzzle` ↔ Daily Challenge; `in-game-editor` + `level-exchange` ↔ редактор і Workshop; `level-select`, `leaderboard`, `background-music`, `game-screen`, `end-screen`, `mode-select`.
- Уже в корпусі як `+`: `+lane-grid`, `+beat-tick`, `+missed-beat`, `+boss-fight`, `+practice-mode`, `+workshop-sharing`.
- **Нема** → пропозиції карток:
  - `+lane-switch-on-hit` «Ворог після удару перескакує в іншу смугу» · entities/move · 📎 · слот {after_hits, dir: facing|back}.
  - `+hold-note` «Утримати ввід від голови до хвоста» · interface/input · 🌱.
  - `+multi-hit-enemy` «Ворог потребує N влучань (у т. ч. в одному біті)» · entities/combat · 🌱.
  - `+split-on-death` «Знищений ворог розпадається на кількох» · entities/spawn · 📎.
  - `+off-beat-movement` «Рух на офбіт / рідше за біт» · entities/move · 🌱.
  - `+lane-redirect-trap` «Пастка переводить ворога в іншу смугу» · entities/interact · 🌱.
  - `+masked-enemy` «Ворог під маскою, поведінка та сама» · interface/render · 🌱.
  - `+remix-generator` «Перегенерувати рівень, зберігши ритм» · levels/generation · 🥇.
  - `+latency-calibration` «Калібрування аудіо/ввідної затримки» · interface/settings · 📎.

## Пропозиції до словників
- `+trigger:beat` — настав біт (повтор із Crypt); `+trigger:missed_beat` — ввід поза вікном; `+trigger:song_end` — пісня скінчилась.
- `+cond:on_beat` — ввід у вікні влучання навколо біта.
- `+effect:reset_combo` — скинути серію; `+effect:hold` — почати утримання (довга нота).
- `+role:food` — предмет на смузі, що лікує, якщо влучити.
- `+ui:action-row` — рядок, де удар зараховується; `+ui:timing-indicator` — Perfect/MISS з рано/пізно; `+ui:vibe-meter` — шкала Vibe.
- `+window:calibration-window` — екран калібрування затримки.
- `+feature:custom-music` (повтор), `+feature:latency-calibration`.
- `+card:hold-note`, `+card:lane-switch-on-hit`.

## Джерела
- ⭐ [Wikipedia: Rift of the NecroDancer](https://en.wikipedia.org/wiki/Rift_of_the_NecroDancer) — 3 смуги, вороги міняють смугу / потребують кількох ударів, HP і їжа, усі режими, платформи й дати.
- [Steam](https://store.steampowered.com/app/2073250/Rift_of_the_NecroDancer/) — опис: кажани міняють смугу при ударі, 4 складності, Remix, Daily, 5 босів, 5 мініігор, редактор і Workshop.
- [jovixie: every enemy type](https://jovixie.pages.dev/posts/every-enemy-type-movement-pattern-and-trap-in-rift-of-the-necrodancer) — фан-гайд: кількість ударів і рух 23 ворогів, тіні, пастки.
- [Siliconera: огляд](https://www.siliconera.com/review-rift-of-the-necrodancer-can-be-a-lot/) — 10 HP, їжа, кажани за кольором, блейдмайстер, боси, мініігри.
- [Rogueliker: огляд](https://rogueliker.com/rift-of-the-necrodancer-review/) — зомбі, гарпії, Remix, Workshop.
- [Steam: гайди](https://steamcommunity.com/app/2073250/guides/) — очки, калібрування затримки, редактор (самі гайди віддали 429).
- Steam News API (appid 2073250) — патчноти: Vibe Chain (їжа, вірм), HP у мінус у практиці, E/L-індикатор, ціни розблокування в діамантах, шари редактора, модифікатори Coda / Golden Lute.

## Непевне
- (?) Таблиця ворогів — з фан-гайду (pages.dev, низька надійність); кажани й блейдмайстер підтверджені оглядом Siliconera, решта — ні. Удари слизів (1 і 2) — з пошукового фрагмента.
- (?) Що саме дає Vibe Power (множник очок, тривалість) і якою кнопкою вмикається — у джерелах лише Vibe Chain і «тривалість при 50 %».
- (?) Третя «тінь» і точні вікна влучання (Perfect/Great/…), шкала оцінок етапу.
- (?) Кількість рядів поля і розкладка кнопок за замовчуванням.
- (?) Ефекти модифікаторів Coda і Golden Lute.
