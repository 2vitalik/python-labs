---
title: Burger Maker
slug: burger-maker
aka: [バーガーメーカー, BurgerMaker]
family: falling-match
also: [build-sim]
klass: cursor
axes:
  field: 1d
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: score
year: 2003
platforms: [PC]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/バーガーメーカー", best: true, note: "кільце з 10 тарілок з булкою, до 3 клієнтів, стрес, репутація → ранг, chain/combo, атмосфера (1.03) і чому її додали"}
  - {kind: other, url: "https://forest.watch.impress.co.jp/article/2003/10/23/burgermaker.html", note: "огляд 2003: ←/→ крутять стіл, Space викидає, Z/X/C віддають клієнту ліворуч/центр/праворуч, «おまかせ», кінець «閉店»"}
  - {kind: other, url: "https://www.vector.co.jp/magazine/softnews/031105/n0311054.html", note: "огляд Vector 1.05: порядок відкриття меню, стрес, атмосфера"}
  - {kind: official, url: "https://mclover.hateblo.jp/BurgerMaker", note: "сторінка автора: Shift — детальні дані, Tab — пауза, Esc, історія версій 1.00–1.40"}
  - {kind: other, url: "https://mclover.hateblo.jp/entry/20261023/1792738247", note: "гайд автора: рецепти, тарілка-смітник, адаптивне випадання інгредієнтів"}
  - {kind: itch, url: "https://dikushima.itch.io/burgermaker", note: "завантаження 1.40, опис EN/JA"}
  - {kind: steam, url: "https://store.steampowered.com/app/4872590/Burger_Maker/", note: "Steam-реліз 2026, клавіатура або контролер"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=バーガーメーカー+ikushima", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [gravity-fall, weighted-spawn, keyboard-controls, combo-multiplier, time-bonus, event-points, progress-acceleration, level-unlock, score-records, leaderboard, game-pause, confirm-dialog, main-menu, game-screen, end-screen, language-picker, game-settings, +ring-turntable, +stack-recipe-match, +customer-orders, +patience-gauge, +reputation-rank, +demand-weighted-spawn, +discard-stack]
proposes: ["+axis:field=ring", "+effect:stack_push(v)", "+effect:discard", "+cond:recipe_match", "+trigger:meter_full", "+ui:recipe-table", "+ui:patience-gauge", "+window:name-entry", "+card:demand-weighted-spawn", "+card:ring-turntable"]
author: opus
date: 2026-11-09
---

# Burger Maker — крутиш кільце з 10 тарілок під падаючі інгредієнти; стос має збігтися з рецептом замовлення

## Суть
Інгредієнти випадково падають в одну точку — на передню тарілку кільцевого столу. Гравець обертає стіл, обираючи, на яку з 10 тарілок ляже наступний шар, і так збирає стоси-бургери за зразками меню. Готовий бургер віддається одному з трьох клієнтів; правильні подачі піднімають репутацію й ранг (до 5 зірок), кожен ранг додає нові рецепти. Це межова гра сімʼї: «поле» — кільце стосів (як колонки Hatris), а падіння лише обирає стос; головний конфлікт — порядок шарів і тиск часу.

## Поле і час
- Поле — 10 тарілок по колу (`1d`-кільце); кожна тарілка — стос шарів, на старті з нижньою булкою. Падіння — одна точка над передньою тарілкою.
- Тарілка тримає до 10 шарів (гайд автора); переповнена автоматично викидається (?) — поріг не перевірено.
- Real-time: інгредієнти падають безперервно, стрес клієнтів і атмосфера тікають; швидша робота → інгредієнти частіше.
- Зверху/збоку — зразки меню, знизу — 3 каси з клієнтами, ліворуч — вертикальна шкала репутації.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Стіл (кільце) | player | 10 тарілок, поворот ←/→ | визначає, яка тарілка під точкою падіння |
| Тарілка | zone | стос до 10 шарів, нижня булка | приймає шар згори; Space викидає вміст |
| Інгредієнт | tile | тип: котлета, сир, салат, кетчуп, булка (?) | падає на передню тарілку й стає верхнім шаром |
| Рецепт (зразок меню) | mark | порядок шарів | гамбургер, W-бургер, чизбургер, W-чизбургер, «чиз-спешл» |
| Клієнт | neutral | замовлення-список, стрес | чекає на касі; повний стрес → іде геть |
| Шкала репутації | zone | 0…max | правильна подача ↑, клієнт пішов ↓↓; max → ранг +1; 0 → кінець |
| Атмосфера | zone | спадає з часом | низька → стрес росте швидше; комбо й ранг відновлюють |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ТО `rotate(ring, ±36)` — під точкою падіння інша тарілка.
- КОЛИ `timer(every)` → ТО `spawn_at(ingredient, drop_point)`, `fall(ingredient)`; ЯКЩО `custom: «інгредієнт потрібен хоча б одному бургеру на тарілках»` — вага типу ∝ кількості тарілок, яким він підходить (гайд).
- КОЛИ `contact(ingredient, front_plate)` → ТО `custom: «стає верхнім шаром стосу»`.
- КОЛИ `counter(stack_height, >, 10)` → ТО `custom: «стос автоматично викидається»`, `custom: «chain := 0»` (?).
- КОЛИ `input(space)` → ТО `custom: «викинути стос передньої тарілки, лишається нижня булка»`, `custom: «chain := 0»`.
- КОЛИ `input(Z|X|C)` → ЯКЩО `custom: «стос на передній тарілці = бургер із замовлення клієнта на касі ліворуч/центр/праворуч (або будь-який готовий для «おまかせ»)»` → ТО `disappear(stack)`, `score(n)`, `counter(reputation, +n)`, `counter(chain, +1)`.
- КОЛИ `input(Z|X|C)` → ЯКЩО `custom: «бургер не той»` → ТО `set_state(customer, angry)` — стрес росте швидше, `counter(mistakes, +1)`.
- КОЛИ `input(Z|X|C)` → ЯКЩО `custom: «на касі нікого»` → ТО `sound(miss)`, `message(key)` (з 1.33).
- КОЛИ `tick` → ТО `counter(stress, +n)` у кожного клієнта; ЯКЩО `counter(atmosphere, <, low)` → швидше.
- КОЛИ `counter(stress, ==, max)` → ТО `disappear(customer)`, `counter(reputation, −big)`.
- КОЛИ `counter(reputation, ==, max)` → ТО `counter(rank, +1)`, `unlock(recipe)`, `custom: «шкала скидається; очікування клієнтів := 0 (1.34)»`, `counter(atmosphere, +n)`.
- КОЛИ `counter(reputation, <=, 0)` → ТО `game_over` («閉店», звук ролети), `window(end-screen)`.
- КОЛИ `tick` → ТО `counter(atmosphere, −n)`; ЯКЩО `counter(rank, ==, 5)` → спад пришвидшується з часом (1.06).
- КОЛИ `input(Z|X|C)` → ЯКЩО `timer(since_last_serve, <, window)` → ТО `combo(+1)`, `score(n)`, `counter(atmosphere, +n)`.
- КОЛИ `custom: «замовлення виконано підряд без викидання й помилок»` → ТО `score(n·chain)` — бонус росте з номером chain.
- КОЛИ `timer(every)` → ЯКЩО `count(customer, <, 3)` → ТО `spawn_at(customer, free_counter)`; із рангом клієнти частіше й з довшими замовленнями.
- Перемоги нема (мета — 5 зірок і рекорд) · Поразка: репутація 0 · Рахунок: продажі + chain + combo.

## Керування і ввід
- ←/→ — повернути стіл; Space — викинути бургер з передньої тарілки; Z / X / C — віддати клієнту ліворуч / по центру / праворуч.
- Shift (утримувати) — вікно детальних даних; Tab — пауза («一時休業»); Esc — на титул з підтвердженням (і ввід імені, якщо рекорд).
- З 1.39 — контролер (Xbox).

## Вікна, меню, HUD
- `main-menu` (титул): Старт · мова JA/EN/ZH · вікно/повний екран · рейтинг · титри (з 4★).
- `game-screen`: кільце тарілок, `custom: «зразки меню»` (`+ui:recipe-table`), 3 каси з клієнтами і `+ui:patience-gauge`, список замовлень із позначкою OK!, вертикальна шкала репутації, шкала атмосфери з підписами, зірки рангу, `score`, `combo-meter`, лічильник chain, `toast` «SLOW PLAY» і заклик до комбо при низькій атмосфері.
- `custom-window` детальних даних (Shift).
- `pause-menu` (Tab), `confirm-dialog` (Esc).
- `end-screen`: рахунок, продажі, кількість помилок, сума комбо, макс. chain; далі `+window:name-entry` (до 8 символів) → `leaderboard` (показує лише продані бургери).
- Переходи: титул → гра → (репутація 0) end-screen → name-entry → рейтинг → титул.

## Фічі поза полем
- `leaderboard-local` з іменами; `unlockables`: титри з 4 зірок.
- `localization` (JA/EN/ZH), `fullscreen` / `window-size` (зберігається), `gamepad-support`.
- `pause`; Steam Cloud у Steam-версії.

## Варіації й родичі
- Версії: 1.00 (2003, Vector) → 1.03 (атмосфера й комбо проти «вічної гри» на 9 повних тарілках) → 1.22 (DirectX 9, 60 fps) → 1.33 (EN/ZH) → 1.39 (контролер) → 1.40 (itch, 2026); Steam 2026. Гран-прі Indies CESA Game Awards 2004.
- Родичі в корпусі: [klax](klax.md) (ловиш падаючі плитки й розкладаєш по колонках), [hatris](hatris.md) (стоси на кількох «головах», порядок шарів), [tetris](tetris.md) — жанр падіння.
- **Осі варіацій**: куди падає (у стовпець під курсором / в одну точку, а рухається приймач) · мета стосу (однакові → зникають / **точний порядок шарів = рецепт**) · хто «споживає» стос (саме поле / **клієнт із терпінням**) · генератор (випадковий / **за попитом тарілок**).

## Цікавинки для курсу
- Кільцевий буфер тарілок і поворот на одну позицію — 🌱.
- Перевірка «стос = рецепт» і «стос ще може стати рецептом» (префікс) — 📎.
- Генератор інгредієнтів, зважений попитом відкритих стосів, — 🥉: класичний баланс «не дати застрягти», і баг-експлойт 9 тарілок з історії версій.
- Клієнти з чергою, терпінням і замовленням-списком + репутація з рангами — 🥉.
- Chain (без помилок підряд) і combo (швидко підряд) як два різні лічильники — 🌱.

## Мапа на каталог
- Є: `gravity-fall` ↔ падіння на тарілку; `weighted-spawn` ↔ зважене випадання; `keyboard-controls`; `combo-multiplier` ↔ chain (подачі підряд без помилок); `time-bonus` ↔ combo (подачі швидко одна за одною); `event-points` ↔ очки за продаж; `progress-acceleration` ↔ ранги прискорюють; `level-unlock` ↔ нові рецепти; `score-records` + `leaderboard`; `game-pause`; `confirm-dialog`; `main-menu`; `game-screen`; `end-screen`; `language-picker`; `game-settings`.
- **Нема** → пропозиції карток:
  - `+ring-turntable` «Кільце стосів, що обертається під точку падіння» · entities/move · 🌱.
  - `+stack-recipe-match` «Стос шарів має збігтися з рецептом» · game-logic/win · 📎 · слоти {recipes}.
  - `+customer-orders` «Клієнти із замовленнями на касах» · game-logic/opponent · 🥉.
  - `+patience-gauge` «Шкала терпіння: повна → клієнт іде» · entities/state · 🌱.
  - `+reputation-rank` «Репутація → ранг → нові рецепти; 0 → кінець» · game-logic/score · 📎.
  - `+demand-weighted-spawn` «Генератор зважений тим, що зараз потрібно» · entities/spawn · 🥉.
  - `+discard-stack` «Викинути стос/тарілку з втратою chain» · entities/interact · 🌱.

## Пропозиції до словників
- `+axis:field=ring` — поле-кільце позицій (уже пропонувалось у корпусі).
- `+effect:stack_push(v)` — шар лягає на верх стосу; `+effect:discard` — викинути вміст.
- `+cond:recipe_match` — стос/набір збігся з рецептом.
- `+trigger:meter_full` — шкала (стрес, репутація) дійшла до максимуму.
- `+ui:recipe-table` — зразки меню на екрані; `+ui:patience-gauge` — терпіння клієнта.
- `+window:name-entry` — ввід імені для рекорду.
- `+card:demand-weighted-spawn`, `+card:ring-turntable` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia JA: バーガーメーカー](https://ja.wikipedia.org/wiki/バーガーメーカー) — кільце з 10 тарілок з булкою, до 3 клієнтів, стрес, репутація й ранг, chain, combo й атмосфера (1.03) та причина — експлойт 9 тарілок, екран результату, титри з 4★.
- [Mado no Mori, 2003](https://forest.watch.impress.co.jp/article/2003/10/23/burgermaker.html) — керування ←/→, Space, Z/X/C, «おまかせ», гнів за неправильний бургер, «閉店».
- [Vector Soft News](https://www.vector.co.jp/magazine/softnews/031105/n0311054.html) — версія 1.05, порядок меню (гамбургер → чиз → дабл → дабл-чиз).
- [Сторінка автора](https://mclover.hateblo.jp/BurgerMaker) — Shift/Tab/Esc, історія версій до 1.40.
- [Гайд автора](https://mclover.hateblo.jp/entry/20261023/1792738247) — рецепти відносно гамбургера, тарілка-смітник на 10 шарів, правило випадання за попитом.
- [itch.io](https://dikushima.itch.io/burgermaker) · [Steam](https://store.steampowered.com/app/4872590/Burger_Maker/) (через appdetails API) — описи, мови, контролер.

## Непевне
- (?) Повний склад гамбургера й порядок шарів (з гайду: має салат і кетчуп; верхня булка — ?), чи падає верхня булка окремим інгредієнтом.
- (?) Поріг автовикидання стосу (10 шарів — з гайду про тарілку-смітник) і чи викидання Space теж скидає chain.
- (?) Поворот за натиск — на одну тарілку (36°) — висновок з «10 тарілок по колу».
- (?) Числа очок, тривалість вікна combo, швидкість стресу — у джерелах нема.
- (?) Чи видно наступний інгредієнт заздалегідь (`info: full` — припущення).
