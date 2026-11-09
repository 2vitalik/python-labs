---
title: Spherical
slug: spherical
aka: [Spherical Remastered]
family: grid-platformer
also: [thinky]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: coop
  info: full
  random: none
  goal: state
year: 1989
platforms: [Amiga, Atari ST, C64, ZX Spectrum, Amstrad CPC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Spherical_(video_game)", best: true, note: "суть: блоки створюються й знищуються, щоб провести Starball до виходу; кооператив з окремим набором кімнат; платформи, автори"}
  - {kind: other, url: "https://spectrumcomputing.co.uk/zxdb/sinclair/entries/0004746/Spherical(EN).txt", note: "інструкція: керування, HUD (пляшки магії, двері часу, годинник, енергія), усі предмети, меню F1–F8, паролі"}
  - {kind: other, url: "https://mirror.cyberbits.eu/textfiles.com/games/REVIEWS/sphercal.rev", note: "огляд: 20 с до старту кулі, котиться «як вода», вороги, боси кожні 10 рівнів, 2P — Findar і Karl"}
  - {kind: other, url: "https://everygamegoing.com/larticle/Spherical-000/33674", note: "Your Sinclair: 80 рівнів + 10 секретних, 2P-рівні проходяться лише разом"}
  - {kind: other, url: "https://spectrumcomputing.co.uk/entry/4746/ZX-Spectrum/Spherical", note: "картка ZX: автори, натхнення Solomon's Key, мапа, інлеї"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Spherical+1989+Rainbow+Arts+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [gravity-fall, item-pickup, key-and-door, touch-death, environment-death, hp-damage, temporary-modes, timed-despawn, restart-level, level-password, sequential-levels, round-currency, status-panel, game-screen, main-menu, attract-demo, tutorial-window, help-window, +create-destroy-block, +auto-walker-guide, +escort-npc, +shifting-gravity, +retry-token, +coop-only-levels, +orbit-shield, +delayed-start-timer]
proposes: ["+effect:reorient_gravity", "+feature:retry-token", "+card:coop-only-levels", "+card:orbit-shield", "+card:delayed-start-timer", "+card:guide-rolling-ball"]
author: opus
date: 2026-11-09
---

# Spherical — чарівник ставить і знищує камені, щоб скотити не себе, а зоряну кулю до виходу, поки не скінчилась її магія

## Суть
Одноекранний платформер у дусі [Solomon's Key](solomons-key.md), але ціль — не дійти самому, а **провести Starball**: на старті кімнати куля пульсує на місці, і за кілька секунд починає котитися блоками вниз, «як вода, що шукає найнижчий рівень». Чарівник (Findar; у 2P — ще Karl) за цей час і далі будує з магічних каменів сходи, стіни й жолоби та знищує зайві, щоб куля дісталась клітини-цілі IN. Паралельно треба виживати серед монстрів і кислоти. Ядро — непряме керування: гравець керує полем, по якому рухається автономний обʼєкт.

## Поле і час
- Один екран-зал замку дракона на кімнату, вигляд збоку; поле з клітин-каменів (сітка блоків як у Solomon's Key).
- Real-time: стартовий відлік до руху кулі (огляд YS: 20 с), далі куля котиться сама; магія, що тримає кулю «в цьому вимірі», витрачається з часом.
- Гравітація: діє на чарівника й кулю; перемикачі гравітації змінюють її **лише для кулі**.
- Кооператив: 2P грають на **іншому наборі кімнат**, розрахованому на двох.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Чарівник (Findar / Karl) | player | енергія, сила стрибка | ходить, стрибає (вгору + вбік — через провалля), чаклує камінь перед собою або під собою; може чаклувати в стрибку й падінні |
| Starball | object | магія (2 пляшки), годинник старту | чекає відліку, потім котиться під гравітацією до нижчих місць |
| Ціль IN | static | — | куля на ній → вихід для чарівника |
| Магічний камінь | object | — | створюється й знищується заклинанням; по ньому ходять і чарівник, і куля |
| Твердий камінь | static | — | магією не прибрати |
| Камінь, що зникає | terrain | — | зникає від магії (частина стартових) |
| Кислотний камінь | hazard | — | капає кислотою; дотик забирає енергію |
| Двері з діамантом | gate | колір | відчиняє амулет того ж кольору, із затримкою |
| Амулет | pickup | колір | відчиняє двері свого кольору |
| Перемикач гравітації | switch | односторонній / туди-назад | обертає гравітацію кулі |
| Діамант | pickup | колір і форма → цінність | багатство; частина — нічого не варта |
| Пісочний годинник | pickup | — | продовжує час кулі / скидає відлік |
| Графин | pickup | — | відновлює енергію чарівника |
| Сувій | pickup | — | відновлює силу стрибка |
| Документ | pickup | слово | показує пароль залу |
| Жезл | pickup | — | переносить чарівника одразу в наступну кімнату |
| Червона пляшка (Helping hand) | pickup | лічильник | на короткий час знищує всіх монстрів кімнати |
| Зелена пляшка (Timestop) | pickup | — | ненадовго зупиняє час |
| Магічний ліхтар | pickup | тривалість | коротка невразливість, зокрема від «злих очей» |
| Бенгальський вогонь (sparkler) | pickup | горить | куля-охоронець кружляє навколо чарівника й знищує монстрів; два вогні — куля літає вільно |
| Монстри (привиди, глобуси, очі, чаклуни з вогнем) | enemy | — | дотик забирає енергію; чаклуни стріляють вогняними кулями |
| Страж (павук, кіт, дракон) | boss | кожен 10-й рівень | великий, стріляє вогнем прицільно |
| Дракон (фінал) | boss | — | остання кімната; з двома гравцями сильніший |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(fire)` → ЯКЩО `free(cell_front)` → ТО `place(wizard, stone)` на висоті чарівника.
- КОЛИ `input(fire+down)` → ЯКЩО `free(cell_below)` → ТО `place(wizard, stone)` під собою — сходинка в стрибку чи падінні.
- КОЛИ `input(fire)` → ЯКЩО `occupied(cell_front, magic_stone)` → ТО `disappear_b`; ЯКЩО `occupied(cell_front, solid_stone)` → ТО `block`.
- КОЛИ `level_start` → ТО `timer(start)` відліку кулі; КОЛИ `timer(start_delay)` → ТО `set_state(starball, rolling)`.
- КОЛИ `tick` → ЯКЩО `state(starball, rolling)` і `not supported(starball)` → ТО `fall(starball)`; інакше `custom: «котиться в бік нижчого рівня»` (?).
- КОЛИ `enter(starball, gravity_switch)` → ТО `custom: «гравітація кулі обертається»`; ЯКЩО `state(gravity_switch, toggle)` → наступний прохід повертає назад.
- КОЛИ `enter(starball, target_in)` → ТО `unlock(exit)`; КОЛИ `enter(wizard, exit)` → ТО `next_level`.
- КОЛИ `tick` → ЯКЩО `state(starball, rolling)` → ТО `counter(magic, -1)`; КОЛИ `counter(magic, =, 0)` → ТО `custom: «куля повертається у свій вимір»` — кімнату не пройдено (?).
- КОЛИ `contact(wizard, enemy)` або `contact(wizard, acid)` → ЯКЩО `not state(wizard, invulnerable)` → ТО `hp(wizard, -n)`; КОЛИ `hp_zero(wizard)` → ТО `game_over` («покинути замок»).
- КОЛИ `input(esc)` → ЯКЩО `counter(time_doors, >, 0)` → ТО `restart`, `counter(time_doors, -1)` — назад у момент входу в кімнату.
- КОЛИ `picked(wizard, amulet)` → ЯКЩО `same(amulet, door, color)` → ТО `custom: «двері відчиняються із затримкою»`; деякі треба відчинити у правильний момент.
- КОЛИ `contact(wizard, diamond)` → ТО `pickup`, `currency(+value)`.
- КОЛИ `contact(wizard, hourglass)` → ТО `pickup`, `timer(+n)` для кулі.
- КОЛИ `contact(wizard, decanter)` → ТО `heal(wizard, n)`; КОЛИ `contact(wizard, scroll)` → ТО `set_state(wizard, jump_power, full)`.
- КОЛИ `contact(wizard, document)` → ТО `message(password)`.
- КОЛИ `contact(wizard, wand)` → ТО `next_level`.
- КОЛИ `input(red_bottle)` → ЯКЩО `has(wizard, red_bottle)` → ТО `custom: «усі монстри кімнати зникають на короткий час»`, `take(wizard, red_bottle)`.
- КОЛИ `contact(wizard, green_bottle)` → ТО `freeze(enemies, n)`; КОЛИ `contact(wizard, lantern)` → ТО `set_state(wizard, invulnerable, n)`.
- КОЛИ `input(hold_fire)` → ЯКЩО `has(wizard, sparkler)` → ТО `spawn(orbit_ball)`; КОЛИ `contact(orbit_ball, enemy)` → ТО `disappear_b`; КОЛИ `timer(sparkler)` → ТО `disappear_a`.
- 2P: КОЛИ `custom: «кімната кооперативна»` → ТО ціль — куля на IN або знищення монстра; пройти можна лише вдвох.
- Перемога: пройти всі зали до кімнати дракона. Поразка: енергія = 0. Рахунок: багатство з діамантів (окремо на кожного гравця).

## Керування і ввід
- Джойстик: ліво/право — хода; вгору — стрибок (з напрямком — через провалля); кнопка — камінь перед собою / зняти камінь; кнопка + вниз — камінь під собою.
- Утримання кнопки — випустити бенгальський вогонь; повторне натискання — відкликати.
- ESC — повернутися в момент входу в кімнату (витрачає двері часу); `*` на клавіатурі — червона пляшка (Amiga/ST огляд).
- 2P — два джойстики одночасно.

## Вікна, меню, HUD
- `main-menu` (F-клавіші): F1 — 1 гравець · F2 — 2 гравці · F3 — тренування в порожньому залі (`tutorial-window`) · F4 — пояснення магічних засобів (`help-window`, частина підказок навмисно прихована) · F5 — інформація й клавіші · F6 — ввід пароля (`level-password`) · F7 — музика · F8 — демо майбутніх залів (`attract-demo`).
- `game-screen`: зал + HUD — дві пляшки магії кулі, камені «дверей часу», годинник старту кулі, багатство (на кожного), номер кімнати, пробірки енергії (на кожного), кількість червоних пляшок.
- Переходи: main-menu → game-screen → (куля на IN, вихід) наступна кімната → … → кімната дракона.

## Фічі поза полем
- `level-password`: слова з документів → F6 → переносить до відповідного залу; звичайного збереження нема.
- `retry-token`: обмежена кількість «дверей часу» — рестартів кімнати.
- `mode-coop`: окремий набір кімнат для двох; кооператив обовʼязковий.
- `tutorial`: тренувальний порожній зал; `codex`-подібна довідка предметів.
- Секретні рівні за кодовим словом (YS).

## Варіації й родичі
- Предок: [solomons-key](solomons-key.md) (створи/знищ блок, але веде себе сам); [fire-n-ice](fire-n-ice.md) — той самий блоковий інструмент без кулі.
- Непряме керування автономним обʼєктом: [troddlers](troddlers.md), Lemmings, [toki-tori](toki-tori.md) (будування мостів), [catrap](catrap.md).
- Спільнотний мод: Spherical Remastered (ZX, 2016).
- Осі: **кого ведеш** (себе / автономну кулю / натовп); **коли стартує обʼєкт** (одразу / після відліку / за кнопкою); **гравітація** (спільна / лише для керованого обʼєкта); **кооп** (ті самі рівні / окремі, непрохідні поодинці).

## Цікавинки для курсу
- Будуй-поки-чекає: камінь `place`/`disappear` + автономна куля, що вирушає за таймером — 🥉 (два цикли: гравця й кулі).
- Куля, що котиться «до нижчого рівня» по клітинах — 📎 (локальне правило руху: униз, інакше вбік).
- Гравітація лише для однієї сутності + перемикачі туди/назад — 📎.
- Обмежені рестарти кімнати як ресурс («двері часу») — 🌱.
- Куля-охоронець по орбіті навколо гравця — 🌱.
- Кооперативні рівні, які поодинці непрохідні — 🥈 (дизайн рівнів + синхронний ввід двох).

## Мапа на каталог
- Є: `gravity-fall` · `item-pickup` · `key-and-door` (амулет → двері кольору) · `touch-death` / `environment-death` / `hp-damage` (енергія) · `temporary-modes` (ліхтар, timestop) · `timed-despawn` (бенгальський вогонь) · `restart-level` · `level-password` · `sequential-levels` · `round-currency` (діаманти) · `status-panel` · `game-screen` · `main-menu` · `attract-demo` · `tutorial-window` · `help-window`.
- **Нема** → пропозиції карток (частково вже є в корпусі з `+`):
  - `+create-destroy-block` — магічний камінь (як Solomon's Key).
  - `+auto-walker-guide` / `+escort-npc` — провести автономну кулю.
  - `+shifting-gravity` — гравітація кулі за перемикачем.
  - `+retry-token` — рестарти кімнати як ресурс.
  - `+coop-only-levels` «Рівні лише для двох» · game-logic/multiplayer · 🥈.
  - `+orbit-shield` «Куля-охоронець навколо гравця» · entities/combat · 🌱.
  - `+delayed-start-timer` «Обʼєкт вирушає після відліку» · entities/move · 🌱.

## Пропозиції до словників
- `+effect:reorient_gravity` — змінити напрямок гравітації для сутності (тут — лише для кулі).
- `+feature:retry-token` — обмежені рестарти рівня.
- `+card:coop-only-levels`, `+card:orbit-shield`, `+card:delayed-start-timer` — див. вище.
- `+card:guide-rolling-ball` «Провести автономну кулю до цілі, змінюючи поле» · entities/move · 🥉.

## Джерела
- ⭐ [Wikipedia: Spherical](https://en.wikipedia.org/wiki/Spherical_(video_game)) — ідея, кооператив з іншими екранами, платформи, автори.
- [Інструкція (Spectrum Computing)](https://spectrumcomputing.co.uk/zxdb/sinclair/entries/0004746/Spherical(EN).txt) — керування, HUD, предмети, меню, паролі, двері часу.
- [Огляд (textfiles)](https://mirror.cyberbits.eu/textfiles.com/games/REVIEWS/sphercal.rev) — 20 с відліку, рух кулі «як вода», вороги, боси, 2P.
- [Your Sinclair](https://everygamegoing.com/larticle/Spherical-000/33674) — кількість рівнів, кооп-рівні.
- [Spectrum Computing: картка](https://spectrumcomputing.co.uk/entry/4746/ZX-Spectrum/Spherical).

## Непевне
- (?) Точне правило кочення кулі (вбік на рівній поверхні? зупиняється в ямі?) — джерела кажуть лише «до найнижчого рівня».
- (?) Що стається, коли магія кулі скінчилась — рестарт кімнати чи втрата «дверей часу».
- (?) Кількість рівнів: 100 (огляд, ST), 80 + 10 секретних (YS, ZX), «понад 200» з урахуванням 2P (інструкція).
- (?) Імʼя фінального дракона: Akarom (огляд) / Mirgal (інструкція).
- (?) Чи «restart jewels» з огляду (до 4 повторів) — те саме, що «двері часу» інструкції.
- (?) Розробник: Electronic Zoo (Wikipedia) чи Probe (ZX/CPC).
