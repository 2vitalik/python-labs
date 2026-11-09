---
title: Wario's Woods
slug: warios-woods
aka: [Wario no Mori, "Wario's Forest", "Wario's Woods Again", "Wario's Woods Bakushou Version"]
family: falling-match
also: [grid-platformer]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: state
year: 1994
platforms: [NES, SNES, Satellaview, Wii Virtual Console, Nintendo Switch Online]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Wario%27s_Woods", best: true, note: "ядро: Тоад носить і штовхає, збіг 3 з бомбою, діагоналі, Thwomp-стеля, VS"}
  - {kind: fandom, url: "https://www.mariowiki.com/Wario%27s_Woods_(Nintendo_Entertainment_System)", note: "Super Mario Wiki: типи монстрів, діамант, фази Birdo/Wario, монети, усі режими NES"}
  - {kind: fandom, url: "https://www.mariowiki.com/Wario%27s_Woods_(Super_Nintendo_Entertainment_System)", note: "Super Mario Wiki: SNES-відмінності, VS COM, яйце Pidgit"}
  - {kind: other, url: "https://en.wikibooks.org/wiki/Wario%27s_Woods/Gameplay", note: "Wikibooks: VS-атаки — 4 за раз, діамант, «breakfast» і яйця"}
  - {kind: other, url: "https://snescentral.com/1/0/1/1019/pdf/warioswoods.pdf", note: "мануал SNES (PDF), бачив у пошуку, не відкривав"}
  - {kind: other, url: "https://www.nintendolife.com/games/nes/warios_woods/review", note: "огляд NES: розкладка кнопок (бачив у пошуку)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=wario%27s+woods+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-by-input, keyboard-controls, gravity-fall, inertia-slide, line-match-clear, chain-reaction, spawn-schedule, spawner-entity, item-pickup, timed-despawn, garbage-attack, simultaneous-versus, ai-opponent, difficulty-levels, mode-select, tutorial-window, game-over-continue, leaderboard, score-records, time-bonus, sequential-levels, destroy-all-enemies, +carry-stack, +climb-stack, +catalyst-match, +diagonal-only-tile, +two-hit-tile, +ceiling-descend, +phase-timer-antagonist, +color-clear-special, +multi-direction-clear-bonus]
proposes: ["+effect:lift_stack", "+effect:ceiling_down", "+cond:contains", "+role:ceiling", "+card:carry-stack", "+card:catalyst-match", "+card:diagonal-only-tile", "+card:two-hit-tile", "+card:ceiling-descend", "+card:phase-timer-antagonist", "+card:multi-direction-clear-bonus", "+feature:technical-rank"]
author: opus
date: 2026-11-09
---

# Wario's Woods — ти не керуєш падаючою фігурою, а бігаєш по колодязю аватаром і переносиш стовпчики монстрів і бомб

## Суть
Колодязь як у Dr. Mario: зверху падають монстри й бомби кольорів, збіг 3+ в лінії (горизонталь, вертикаль, **діагональ**) прибирає їх — але лише якщо в лінії є **хоча б одна бомба**; три монстри без бомби не рахуються. Гравець — не курсор, а **Тоад**, що ходить по дну й по верхівках стосів, піднімає один обʼєкт або **цілий стовпчик**, переносить і ставить, копає ногою обʼєкт, щоб той ковзав до упору, видирається на стоси. Темп задає **фазовий таймер**: поки «добрий» Birdo тримає час, Sprite скидає бомби; коли таймер добігає — приходить Wario, замість бомб сиплються монстри, а стеля-Thwomp опускається. Мета раунду — знищити всіх монстрів; поразка — поле так забите, що Тоад не може рухатись.

## Поле і час
- Колодязь шириною 7 стовпців у Round Game і Time Race, 6 — у VS (NES, Mario Wiki); висота й масштаб SNES — див. «Непевне».
- Два шари: поле обʼєктів (монстри, бомби, діаманти, монети) + аватар Тоад, що стоїть на дні або на верхівці стосу; згори — Thwomp-стеля, рухома межа.
- Real-time: обʼєкти падають з верху; збіги перевіряються після кожного розміщення/падіння; каскади через гравітацію.
- Фази часу: таймер Birdo → фаза Wario (свій таймер) → знову Birdo; цикл до кінця раунду. Ланцюги подовжують «добру» фазу або скорочують «злу».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Тоад | player | позиція, що несе (нічого / 1 обʼєкт / стовпчик) | ходить уліво-вправо, лізе вгору по боці стосу чи стіни, піднімає, ставить, копає; не дістає те, до чого не може дотягтись |
| Монстр простий (Fuzz, Spud, Squeak) | tile | колір | падає; зникає в лінії 3+ одного кольору з бомбою — будь-якого напряму |
| Монстр діагональний (Beaker, Scram) | tile | колір | зникає **лише** в діагональній лінії |
| Dovo | tile | колір, стан | після першого збігу з бомбою міняє колір; другий збіг (з бомбою нового кольору) знищує |
| Spook | tile | колір, стан «блимає» | після удару блимає; другий удар має прийти, поки блимає, інакше стан скидається |
| Бомба | tile | колір | каталізатор збігу: без неї лінія не спрацьовує; зникає разом з лінією; після перемоги решта бомб зникає сама |
| Діамант | tile | колір (незалежний від лінії-джерела) | зʼявляється за лінію 5+; лінія з діамантом знищує всіх монстрів його кольору; у VS ще й перетворює бомби суперника на монстрів |
| Sprite | spawner | — | у фазі Birdo скидає згори бомби |
| Birdo | neutral | таймер фази | «добрий» таймер; коли заповнюється — його місце займає Wario |
| Wario | enemy | таймер фази | у своїй фазі бʼє бік коробки → Thwomp опускається; таймер скінчився — іде |
| Black Bat (NES) / Pidgit (SNES) | spawner | — | замість Sprite у фазі Wario скидає монстрів |
| Thwomp-стеля | hazard | висота | опускається на кілька рядів від ударів Wario (і атак у VS); певні знищення піднімають її назад |
| Монета | pickup | — | падає згори, зникає за кілька секунд; 30 (NES) / 50 (SNES) монет = continue |
| Яйце (SNES, VS) | container | таймер вилуплення | Pidgit (або атака суперника) скидає; вилуплюється в монстра кольору, що вже є на полі; якщо підняти й поставити до вилуплення — не скидає ряд монстрів |
| Бос (Round Game B) | boss | HP | зʼявляється раз на 10 раундів; шкоди — коли потрапляє в лінію, що зникає; падає на Тоада → поразка |

## Правила (КОЛИ → ЯКЩО → ТО)
Збіги:
- КОЛИ `pattern(line(3+))` (горизонталь / вертикаль / діагональ) → ЯКЩО `same(cells, color)` and `custom: «у лінії ≥1 бомба»` → ТО `clear(line)`.
- КОЛИ `pattern(line(3, monsters))` → ЯКЩО `not custom: «є бомба»` → ТО нічого (лінія без каталізатора).
- КОЛИ `after(clear)` → ЯКЩО `state(monster, diagonal_only)` and `custom: «лінія не діагональна»` → ТО монстр лишається; діагональна → `disappear_a`.
- КОЛИ `after(clear)` → ЯКЩО `occupied(line, dovo)` and `not state(dovo, hit)` → ТО `set_state(dovo, hit)`, `custom: «змінити колір»`; інакше `disappear_a`.
- КОЛИ `after(clear)` → ЯКЩО `occupied(line, spook)` and `state(spook, flashing)` → ТО `disappear_a`; інакше `set_state(spook, flashing, duration)`.
- КОЛИ `pattern(line(5+))` → ТО `spawn_at(diamond)`; колір діаманта — не обовʼязково колір лінії.
- КОЛИ `after(clear)` → ЯКЩО `occupied(line, diamond)` → ТО `custom: «clear_color — усі монстри кольору діаманта зникають»`.
- КОЛИ `after(clear)` → ТО `fall(objects)`; КОЛИ знову `pattern` → `clear`, `combo(+1)` (ланцюг).
Тоад:
- КОЛИ `input(lift)` → ЯКЩО `occupied(front, object)` → ТО `custom: «lift_stack — підняти один обʼєкт або весь стовпчик від рівня Тоада вгору»`, `carry(stack)`.
- КОЛИ `input(put)` → ЯКЩО `has(toad, stack)` → ТО `place(stack, front)`; далі `fall`.
- КОЛИ `input(kick)` → ЯКЩО `occupied(front, object)` → ТО `slide(object, dir)` до першого обʼєкта.
- КОЛИ `input(move)` → ЯКЩО `blocked(toad)` and `custom: «збоку стос або стіна»` → ТО `custom: «climb — Тоад вилазить на верхівку»`.
- КОЛИ `input(hop)` при перенесенні → ТО `custom: «Тоад залазить на верх перенесеного стосу»` (дістати недосяжне).
Фази й стеля:
- КОЛИ `counter(birdo_timer, ==, full)` → ТО `custom: «фаза Wario»`: `transform(sprite → bat|pidgit)`, джерело спавну — монстри.
- КОЛИ `rng(p)` → ЯКЩО `state(game, wario_phase)` → ТО `custom: «ceiling_down — Thwomp на N рядів нижче»`.
- КОЛИ `after(clear)` → ЯКЩО `chain(2+)` → ТО `timer(+birdo)` у фазі Birdo / `timer(−wario)` у фазі Wario.
- КОЛИ `custom: «певні знищення»` → ТО `custom: «ceiling_up»` (Thwomp піднімається).
- КОЛИ `counter(wario_timer, ==, full)` → ТО `custom: «фаза Birdo»`; цикл повторюється.
Кінець раунду:
- КОЛИ `all_gone(monster)` → ТО `win`, `disappear(bombs)`, `next_level` (наступний раунд з більшою кількістю монстрів).
- КОЛИ `custom: «поле заповнене, Тоад не може рухатись»` → ТО `lose`.
- КОЛИ `contact(boss, toad)` (падіння боса на Тоада, Type B) → ТО `lose`; КОЛИ `hp_zero(boss)` → ТО `win`.
Монети (Round Game):
- КОЛИ `level_start` → ТО `counter(gold_bonus, max)`; КОЛИ `custom: «зʼява Wario»` → ТО `counter(gold_bonus, −20% від старту)`; три зʼяви — бонус нуль (NES).
- КОЛИ `contact(toad, coin)` → ТО `pickup`; КОЛИ `timer(coin_lifetime)` → ТО `disappear_a`.
- КОЛИ `counter(coins, ≥, 30)` (SNES 50) → ТО `give(continue)`; КОЛИ `lose` → ЯКЩО `has(continue)` → ТО `restart`.
VS:
- КОЛИ `after(clear)` → ЯКЩО `chain(4+)` or `custom: «4 обʼєкти за раз»` → ТО `send_garbage(column of monsters)` / `custom: «ceiling_down(opponent, 1)»`.
- КОЛИ `spawned(diamond)` → ЯКЩО `mode(vs)` → ТО `custom: «ceiling_down(opponent, 2)»` (Wikibooks); лінія з діамантом → `transform(opponent bombs → monsters)`.
- КОЛИ `custom: «одна бомба чистить лінії у 2–3 напрямках (breakfast)»` → ТО `send_garbage(egg ×1|×2)`.
- КОЛИ `all_gone(monster)` → ЯКЩО `mode(vs)` (або суперник не може рухатись) → ТО `custom: «раунд виграно»`; КОЛИ `counter(rounds_won, ==, 3)` → ТО `win`.
- Рахунок: у Time Race — час проходження набору раундів; у Round Game — золотий бонус і монети; формула очок у джерелах не описана.

## Керування і ввід
- Хрестовина: Тоад ходить уліво-вправо; біг у бік стосу/стіни — лізе вгору.
- NES (Nintendo Life): B — взяти один обʼєкт перед собою; A — взяти все на рівні Тоада й вище; при перенесенні B міняє лише нижній, A ставить усе; вгору (або A+B) — стрибнути на верх перенесеного стосу (?).
- SNES (мануал, retro-replay): A — підняти стос, B — взяти один обʼєкт з будь-якого місця стосу, Y — удар ногою / вирватись з-під стосу нагору, X — «пірнути» в стос, щоб дістати недосяжне (?).
- Удар: вниз + кнопка удару — обʼєкт перед Тоадом ковзає до першого обʼєкта.
- Lesson Mode вчить «взяти / лізти / копнути» (A/B, A+вниз на NES).

## Вікна, меню, HUD
- `main-menu` NES: Round Game (A/B) · Time Race · VS · Lesson Mode · Option. SNES: VS COM · VS 2P · Round Game · Time Race · Lesson · Option.
- `game-screen`: колодязь, Тоад, Thwomp зверху, бічна панель з Birdo/Wario і таймером фази (`timer-countdown`), лічильник монет (`coins`), золотий бонус, номер раунду (`level-number`).
- VS: два колодязі поруч (`opponent-boards`), у кожного свій таймер, лічильник виграних раундів.
- `difficulty-select` (VS: кожен гравець — свою складність; Time Race: Easy/Normal/Hard) · `custom: «monster-type-select»` — VS: вибір двох типів монстрів.
- `tutorial-window` — Lesson: Learn Moves + 12 практичних раундів (NES) / уроки по 9 прикладів (SNES).
- `leaderboard` — Player Records і All-Time Records (топ-7, Gold/Silver/Bronze) + `custom: «Technical Rank Certification»`.
- `game-over-continue` — continue за накопичені монети; меню дозволяє продовжити з кожного 5-го раунду (`level-password`-подібно).
- `dialogue-window` — катсцени, де Wario кепкує перед кожним 10-м раундом.
- `settings-window` (Option) — зміст не описаний.
- Переходи: main-menu → режим → game-screen → (всі монстри) наступний раунд / (затиснуто) game-over-continue → main-menu.

## Фічі поза полем
- `mode-classic` (Round Game A), Round Game B з босами, `mode-time-attack` (Time Race: набори з 2–5 раундів), `mode-versus` (2P; SNES — також проти CPU-босів на 3 складностях, `ai-opponent-levels`), `tutorial`.
- `continue` — за монети; продовження з кожного 5-го раунду.
- `leaderboard-local` + `custom: «technical-rank»` — оцінка майстерності за Time Race.
- `custom-rules` (легкий): у VS обрати 2 типи монстрів і свою складність.
- Satellaview-версії (Bakushou Version, Again) — трансляційні перевидання (?).

## Варіації й родичі
- Родичі в корпусі: `dr-mario` (віруси + капсули: «ціль» і «каталізатор» тих самих кольорів), `puyo-puyo` (ланцюги й атаки), `panel-de-pon` (курсор, а не падіння), `tetris` (класика колодязя).
- Найближчий за ідеєю «аватар у колодязі»: `zoop` (стрілок у центрі), Mr. Driller (копає вниз, `dig-gravity`).
- **Осі варіацій**: хто діє (курсор фігури / курсор-обмін / **аватар**) · умова збігу (будь-які 3 / **з каталізатором** / лише діагональ) · як обʼєкт сприймає удар (1 удар / 2 удари / 2 удари у вікні часу) · джерело тиску (швидкість падіння / **стеля, що опускається** / сміття суперника).

## Цікавинки для курсу
- Аватар, що піднімає стовпчик від свого рівня вгору й ставить в іншому місці — 🥉 (стан «несу стос», колізії з полем, гравітація для решти).
- Збіг лише з каталізатором (бомба в лінії) — 📎 (одна умова поверх line-match).
- Типи монстрів з різними правилами зникнення: лише діагональ, два удари, два удари у вікні часу — 📎 за тип, 🥉 за всі.
- Діамант за 5+: знищити всіх монстрів свого кольору — 🌱.
- Фазовий таймер Birdo/Wario: ланцюги подовжують добру фазу, у злій — інший спавн і стеля опускається — 🥉 (машина станів + таймери).
- Thwomp-стеля як рухома межа поля, що опускається й піднімається — 📎.
- Удар ногою: обʼєкт ковзає до упору — 🌱.

## Мапа на каталог
- Є: `move-by-input` · `keyboard-controls` · `gravity-fall` · `inertia-slide` (удар ногою) · `line-match-clear` · `chain-reaction` · `spawn-schedule` · `spawner-entity` (Sprite / Bat) · `item-pickup` + `timed-despawn` (монети) · `garbage-attack` · `simultaneous-versus` · `ai-opponent` (SNES VS COM) · `difficulty-levels` · `mode-select` · `tutorial-window` · `game-over-continue` · `leaderboard` · `score-records` · `time-bonus` (золотий бонус тане з фазами Wario) · `sequential-levels` · `destroy-all-enemies` (раунд = прибрати всіх монстрів).
- **Нема** → пропозиції карток:
  - `+carry-stack` «Аватар піднімає й переносить стовпчик» · entities/move · 🥉 · слот {lift: one|stack_above}.
  - `+climb-stack` «Лізти на стос/стіну» · entities/move · 🌱 (родич `ladder-climb`, але без драбин).
  - `+catalyst-match` «Збіг рахується лише з плиткою-каталізатором» · entities/interact · 📎 · слот {catalyst_kind}.
  - `+diagonal-only-tile` «Плитка зникає лише в діагональній лінії» · entities/interact · 🌱.
  - `+two-hit-tile` «Плитка на два удари, з вікном часу» · entities/state · 📎 · слот {window_ticks}.
  - `+ceiling-descend` «Стеля опускається / піднімається» · game-logic/lose · 📎.
  - `+phase-timer-antagonist` «Фазовий таймер: добра / зла фаза зі своїм спавном» · game-logic/waves · 🥉.
  - `+color-clear-special` (як у Candy Crush / Magical Drop) — діамант.
  - `+multi-direction-clear-bonus` «Бонус за лінії в кількох напрямках від однієї плитки» · game-logic/score · 🌱 («breakfast»).

## Пропозиції до словників
- `+effect:lift_stack` — підняти стовпчик обʼєктів від клітини вгору як одне ціле (інакше — 3 речення `carry` + `custom`).
- `+effect:ceiling_down` — зсунути верхню межу поля вниз на N рядів (Wario's Woods; родич підйому поля в Panel de Pon).
- `+cond:contains` — лінія/група містить ≥1 сутність виду (бомба в лінії; родич `has` для множини клітин).
- `+role:ceiling` — рухома межа поля, що звужує простір (Thwomp); не `hazard`, бо не шкодить контактом.
- `+card:carry-stack` · `+card:catalyst-match` · `+card:diagonal-only-tile` · `+card:two-hit-tile` · `+card:ceiling-descend` · `+card:phase-timer-antagonist` · `+card:multi-direction-clear-bonus` — див. «Мапу».
- `+feature:technical-rank` — сертифікат-оцінка майстерності за результатом режиму на час.

## Джерела
- ⭐ [Wikipedia: Wario's Woods](https://en.wikipedia.org/wiki/Wario%27s_Woods) — Тоад піднімає/штовхає/лізе, збіг 3+ у 3 напрямках з ≥1 бомбою, Thwomp-стеля, VS, платформи й назви.
- [Super Mario Wiki: NES](https://www.mariowiki.com/Wario%27s_Woods_(Nintendo_Entertainment_System)) — типи монстрів і як їх знищити, діамант 5+, фази Birdo/Wario, Black Bat, золотий бонус −20 %, монети 30 = continue, Type B боси, Time Race з рекордами, VS (6 стовпців, 3 перемоги), Lesson.
- [Super Mario Wiki: SNES](https://www.mariowiki.com/Wario%27s_Woods_(Super_Nintendo_Entertainment_System)) — Pidgit і яйце, VS COM на 3 складностях, 50 монет, меню з 6 пунктів.
- [Wikibooks: Gameplay](https://en.wikibooks.org/wiki/Wario%27s_Woods/Gameplay) — VS-атаки: 4 за раз → стеля суперника −1, діамант → −2 і перетворення бомб, «breakfast» → яйця.
- Мануал SNES ([snescentral PDF](https://snescentral.com/1/0/1/1019/pdf/warioswoods.pdf)) і [Nintendo Life](https://www.nintendolife.com/games/nes/warios_woods/review) — розкладка кнопок (лише з пошукового резюме).

## Непевне
- (?) Висота колодязя й ширина в SNES; кількість рядів, на які Wario опускає Thwomp; які саме знищення її піднімають.
- (?) Розкладка кнопок: джерела суперечать (NES vs SNES vs MobyGames); «пірнути в стос» (X на SNES) і стрибок на перенесений стос — з пошукового резюме, не з першоджерела.
- (?) Як саме лінія 4 атакує у VS: «стовпчик монстрів» (Mario Wiki) чи «стеля −1 ряд» (Wikibooks) — можливо, різні версії.
- (?) Чи монстр-«ціль» сам по собі може бути частиною лінії «2 бомби + 1 монстр» для діагональних типів — правило «лише діагональ» стосується самого монстра.
- (?) Раунд з босом у Type B: «round 9 of every 10» — точна нумерація; зміст Option; формула очок.
