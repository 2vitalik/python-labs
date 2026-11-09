---
title: Moai-kun
slug: moai-kun
aka: [モアイくん, Moai Kun, Моаї-кун]
family: grid-platformer
also: [push-slide]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 1990
platforms: [Famicom]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Moai-kun", best: true, note: "правила: обмежений стрибок, удар головою, бомби під собою, блок, притиснутий до перешкоди, більше не рухається, причини втрати життя, Select = рестарт за життя, +1 життя за рівень, 56 рівнів, паролі, таймер"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/モアイくん", note: "JP: врятувати всіх Пучі й увійти в двері; список ворогів Skull Empire"}
  - {kind: other, url: "https://www.arcade-history.com/game/54396/", note: "крихітний стрибок, валуни головою, пружини, землетрусні камені, особливі блоки (незламні, осипні, крижані), паролі кожні ~4 рівні"}
  - {kind: other, url: "https://www.destructoid.com/uncover-the-block-moving-secrets-of-the-rapa-nui-in-konamis-moai-kun/", note: "огляд: один екран, одне рішення, кнопка самогубства, нескінченні продовження"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Moai-kun+Famicom+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-by-input, gravity-fall, push-object, destructible-blocks, collect-all, reach-exit, touch-death, environment-death, player-death, time-out, impassable-cells, floor-types, timed-despawn, enemy-patrol, projectile-shot, spawner-entity, restart-level, level-password, sequential-levels, game-screen, +headbutt-break, +freeze-on-contact, +bomb-drop-below, +bounce-pad, +stun-item, +crush-by-falling-object, +reset-costs-life, +extra-life-per-stage, +exit-opens-after-quota]
proposes: ["+card:freeze-on-contact", "+card:bomb-drop-below", "+card:reset-costs-life", "+card:stun-item"]
author: opus
date: 2026-11-09
---

# Moai-kun — моаї з Gradius рятує малих моаї: блок, що вперся в перешкоду, застигає назавжди

## Суть
Однокімнатний бічний пазл-платформер Konami (спін-оф Gradius, де моаї — вороги): Моаї-кун має врятувати всіх полонених малих моаї (Пучі) і вийти через двері до кінця таймера. Стрибає він ледь на висоту перед собою, тож рельєф міняє головою — розбиває одні блоки, штовхає валуни, бʼє ворогів, — а в частині рівнів кладе під себе бомбу. Ключова вада-механіка: **блок, дотиснутий до іншого обʼєкта, більше не рухається**, тож кожен поштовх незворотний і рівень легко «зламати» — звідси рестарт за ціну життя.

## Поле і час
- Один екран на рівень, бічний вид, квадратна сітка блоків; 56 рівнів.
- Час іде безперервно: вороги рухаються й стріляють, у кожного рівня є таймер; вичерпання — втрата життя.
- Шари: тло · блоки й валуни (руйнівні, рухомі, незламні, осипні, крижані) · пружини, шипи, ями · сутності (Моаї-кун, Пучі, вороги, бомби, предмети).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Моаї-кун | player | життя | ходить, робить крихітний стрибок (≈ на висоту перед собою (?)), бʼє головою; падає без опори |
| Пучі (малий моаї) | pickup | кількість на рівні | рятується дотиком (?); коли врятовано всіх — можна виходити |
| Двері | gate | закриті / відкриті | відчиняються, коли врятовано всіх Пучі; вхід = кінець рівня |
| Руйнівний блок | object | — | розбивається ударом головою або вибухом бомби |
| Валун / рухомий блок | object | рухомий / застиглий | удар головою зсуває його; притиснутий до іншого обʼєкта — застигає назавжди; падає без опори (?) |
| Незламний блок | static | — | не руйнується |
| Осипна платформа | terrain | — | обвалюється, коли на ній стоять (?) |
| Крижана платформа | terrain | — | ковзка (?) |
| Пружина | terrain | — | дає високий стрибок |
| Шипи | hazard | — | дотик/приземлення = втрата життя |
| Яма | hazard | — | падіння = втрата життя |
| Бомба | pickup | обмежений запас на рівні | підібрати; покласти під себе → руйнує блоки під Моаї-куном |
| Землетрусний камінь | pickup | — | на короткий час оглушує ворогів |
| Солдат Skull A | enemy | — | рядовий; дотик = втрата життя; удар головою знищує |
| Солдат Skull B | enemy | швидший за A | як A, швидший |
| Вартовий Skull | enemy | — | стереже Пучі, щоб ті не втекли |
| Капітан Skull | enemy | — | випльовує мечі (снаряди) |
| Генерал Skull | enemy | — | випльовує зграї кажанів |
| Вогнедишна статуя моаї | enemy | імунна до удару головою | регулярно плює вогнем |
| Кажан / меч / вогонь | projectile | — | летить від стрільця; дотик = втрата життя |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `free(next)` → ТО `move(moai, dir)`; КОЛИ `input(jump)` → ТО `custom: «стрибок лише на невелику висоту, ледь на виступ попереду»`.
- КОЛИ `after(move)` → ЯКЩО `not supported(a)` → ТО `fall(a)`.
- КОЛИ `input(headbutt)` → ЯКЩО `occupied(front, breakable_block)` → ТО `disappear(block)`.
- КОЛИ `input(headbutt)` → ЯКЩО `occupied(front, boulder)` і `not state(boulder, fixed)` і `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `blocked(boulder)` (дотиснутий до іншого обʼєкта) → ТО `set_state(boulder, fixed)` — більше не рухається ніколи; рівень може стати нерозвʼязним.
- КОЛИ `input(headbutt)` → ЯКЩО `occupied(front, enemy)` і `not state(enemy, headbutt_immune)` → ТО `disappear(enemy)`.
- КОЛИ `contact(moai, bomb)` → ТО `pickup(moai, bomb)`; КОЛИ `input(bomb)` → ЯКЩО `has(moai, bomb)` → ТО `place(moai, bomb)` під собою, `explode(down, 1, empty)` — руйнує блок під ним (форма вибуху — (?)).
- КОЛИ `contact(moai, quake_stone)` → ТО `stun(enemy, n)` для всіх ворогів (тривалість — (?)).
- КОЛИ `enter(moai, spring)` → ТО `custom: «високий стрибок»`.
- КОЛИ `contact(moai, puchi)` → ТО `disappear(puchi)`, `counter(puchi_left, -1)` (?).
- КОЛИ `counter(puchi_left, =, 0)` → ТО `set_state(door, open)`.
- КОЛИ `enter(moai, door)` → ЯКЩО `state(door, open)` → ТО `win`, `lives(+1)`, `next_level`.
- КОЛИ `contact(moai, enemy|projectile)` або `enter(moai, spike|pit)` → ТО `lives(-1)`, `restart`.
- КОЛИ `custom: «на Моаї-куна впав обʼєкт»` → ТО `lives(-1)`, `restart`.
- КОЛИ `counter(time_left, =, 0)` → ТО `lives(-1)`, `restart`.
- КОЛИ `input(select)` → ТО `lives(-1)`, `restart` — «самогубство», коли рівень зламано.
- КОЛИ `custom: «життя скінчились»` → ТО `game_over`, `custom: «продовження з останнього пароля, назад на кілька рівнів»`.
- Перемога: врятовано всіх Пучі й Моаї-кун вийшов у двері. · Поразка: життя скінчились (продовження нескінченні). · Рахунок: очки — (?).

## Керування і ввід
- Хрестовина — ходьба; кнопка стрибка; удар головою — окрема кнопка (?); бомба — кнопка/напрям униз (?).
- Select — миттєвий рестарт рівня за одне життя.
- На титулі — введення шестисимвольного пароля.

## Вікна, меню, HUD
- `splash-screen` → `main-menu`: Start · Password (?).
- `level-password` — 6 символів (цифри й літери A–F), видається приблизно кожні 4 рівні.
- `game-screen` — кімната; HUD — `timer-countdown`, `lives`, `level-number` (?), `remaining-counter` Пучі (?), бомби (?).
- `end-screen` / `game-over-continue` — після втрати всіх життів: продовжити з пароля.
- Переходи: титул → (пароль) → game-screen → (двері) → наступний рівень → … → фінал проти Skull King (?).

## Фічі поза полем
- `levels-sequential`: 56 рівнів; пароль-чекпойнт приблизно кожні 4.
- `restart-level` через Select, але за ціну життя; `+1` життя за кожен пройдений рівень — економіка життів як «бюджет помилок».
- Продовження нескінченні, але відкидають до останнього пароля.
- Музика: непарні рівні — тема шоу «Warai», парні — «Somebody Stole My Gal».
- Нема редактора, undo, збереження (лише паролі).

## Варіації й родичі
- Лише Японія (1990), майже весь текст англійською; є фан-переклади.
- Родичі: Solomon's Key (бічна кімната, удар головою по блоках), Catrap і Block Dude (пазл з гравітацією без високого стрибка), Popils (руйнування блоків), Kickle Cubicle (рятувати й виходити), Lode Runner (бомби/копання вниз).
- Осі варіацій:
  - **поштовх блока**: вільно туди-сюди (Sokoban) / лише поки не вперся, далі застиг (Moai-kun) / ковзає до упору (Pengo).
  - **рух вниз крізь рельєф**: копати (Lode Runner) / бомба під себе (Moai-kun) / удар знизу (Popils).
  - **ціна рестарту**: безкоштовно (сучасні) / одне життя (Moai-kun) / нема рестарту.

## Цікавинки для курсу
- Блок, що застигає після першого упору: стан `fixed` у сутності + перевірка в правилі поштовху — 🌱.
- Детектор «рівень зламано» (жоден Пучі чи двері недосяжні після застигання) — 🥇 (досяжність по станах).
- Бомба під себе, що руйнує лише блок під гравцем, і обмежений запас бомб — 📎.
- Економіка життів: рестарт за −1, вихід за +1, паролі-чекпойнти — 📎.
- Вороги-стрільці різних типів (мечі, кажани, вогонь за таймером) і імунітет до удару — 🥉.
- Предмет, що оглушує всіх ворогів на N тіків — 🌱.

## Мапа на каталог
- Є: `move-by-input` + `gravity-fall` ↔ ходьба й падіння; `push-object` ↔ валуни; `destructible-blocks` ↔ удар головою; `collect-all` + `reach-exit` ↔ усі Пучі → двері; `touch-death` / `environment-death` / `player-death` ↔ вороги, шипи, ями, розчавлення; `time-out` ↔ таймер; `floor-types` ↔ крижані й осипні платформи; `timed-despawn` ↔ осипні (?); `enemy-patrol` ↔ солдати (?); `projectile-shot` ↔ мечі, вогонь; `spawner-entity` ↔ Генерал з кажанами; `restart-level` ↔ Select; `level-password` ↔ паролі; `sequential-levels` ↔ 56 рівнів.
- **Нема** → пропозиції карток:
  - `+freeze-on-contact` «Обʼєкт застигає, коли його дотиснули до перешкоди» · entities/legality · 🌱 · слот {permanent: bool}.
  - `+bomb-drop-below` «Бомба під себе руйнує клітину знизу» · entities/combat · 📎 · слот {supply}.
  - `+reset-costs-life` «Рестарт рівня коштує життя» · game-logic/lose · 🌱.
  - `+extra-life-per-stage` «+1 життя за пройдений рівень» · game-logic/score · 🌱.
  - `+exit-opens-after-quota` «Двері відчиняються, коли зібрано всіх» · game-logic/win · 🌱 (родич `collect-quota`).
  - `+stun-item` «Предмет оглушує всіх ворогів» · entities/state · 🌱.
  - `+bounce-pad` (пропонували Kula World) — пружина; `+crush-by-falling-object` — смерть від обʼєкта, що впав; `+headbutt-break` (Solomon's Key).

## Пропозиції до словників
- `+card:freeze-on-contact` — механіка, якої в каталозі нема; у правилі — наявні `blocked` + `set_state(fixed)`.
- `+card:bomb-drop-below`, `+card:reset-costs-life`, `+card:stun-item` — див. вище.
- Наявні слова, вжиті без пропозиції: `supported`, `explode`, `stun`, `place`, `lives`, `restart`, `game_over`, `level-password`, `game-over-continue`, `timer-countdown`, `remaining-counter`.

## Джерела
- ⭐ [Wikipedia: Moai-kun](https://en.wikipedia.org/wiki/Moai-kun) — обмежений стрибок, удар головою по блоках і ворогах, бомби під собою, «притиснутий до обʼєкта блок більше не рухається», причини втрати життя (ворог, яма, шипи, розчавлення, час), Select = рестарт за життя, +1 життя за рівень, 56 рівнів, паролі, спін-оф Gradius.
- [Wikipedia JA: モアイくん](https://ja.wikipedia.org/wiki/モアイくん) — врятувати всіх Пучі й увійти в двері; вороги Skull Empire (солдати A/B, вартовий, капітан з мечами, генерал з кажанами, вогнедишна статуя, імунна до голови); музика.
- [Arcade History](https://www.arcade-history.com/game/54396/) — крихітні стрибки, валуни головою, обмежені бомби, пружини, шипи, землетрусні камені, незламні/осипні/крижані блоки, пароль кожні ~4 рівні.
- [Destructoid](https://www.destructoid.com/uncover-the-block-moving-secrets-of-the-rapa-nui-in-konamis-moai-kun/) — один екран, одне рішення, кнопка самогубства, нескінченні продовження.
- YouTube: пошук «Moai-kun Famicom gameplay».

## Непевне
- (?) Як саме рятують Пучі (дотиком чи ударом по клітці/вартовому) і чи відчиняються двері лише після всіх — JA-вікі: «врятувати всіх, потім у двері».
- (?) Чи валун падає без опори і чи «застигає» лише після поштовху, чи й після падіння; чим відрізняються руйнівний блок і валун зовні.
- (?) Розкладка кнопок (окрема кнопка удару/бомби), висота стрибка в клітинах, стартова кількість життів, наявність очок.
- (?) Поведінка осипних і крижаних платформ, тривалість оглушення, рух солдатів (патруль чи погоня).
- (?) Чи Skull King — бос фінального рівня.
