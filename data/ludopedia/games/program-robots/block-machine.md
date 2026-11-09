---
title: Block Machine
slug: block-machine
aka: []
family: program-robots
also: []
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: setup
  goal: state
year: 2023
platforms: [PC (Windows)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1584170/Block_Machine/", best: true, note: "опис (блоки = код і дані, усе паралельно), 5 скриншотів з підказками блоків MOVE / OUTPUT / WELD / UNWELD / ROTATE, екран LEVEL PASSED, карта рівнів, трейлер"}
  - {kind: steam, url: "https://store.steampowered.com/app/1593530/", note: "безкоштовне демо (Block Machine Demo)"}
  - {kind: other, url: "https://blog.s-schoener.com/", note: "блог автора (Sebastian Schöner, видавець kerntief): згадує свої «погано пояснені пазл-ігри» з лінком на Block Machine"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Block+Machine+kerntief+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 35
mechanics: [push-object, stick-together, cursor-place, step-execution, leaderboard, world-map, level-unlock, tutorial-window, end-screen, game-screen, keyboard-controls, +code-is-data-blocks, +parallel-block-eval, +signal-propagation, +entity-rotate, +io-test-streams, +solution-metrics, +step-run-speed, +sandbox-mode, +footprint-metric]
proposes: ["+role:instruction", "+trigger:signal(a)", "+effect:weld(a, b)", "+effect:append_output(a, list)", "+feature:solution-metrics", "+feature:random-test-cases"]
author: opus
date: 2026-11-09
---

# Block Machine — машина з блоків, де кожен блок водночас інструкція й дані, а всі виконуються паралельно

## Суть
Гравець розставляє на сітці блоки так, щоб машина перетворила вхідні списки блоків на потрібні вихідні списки (напр. «порахуй довжину входу за модулем 3 і виведи стрілку вгору в потрібний вихід»). Програми як тексту нема: **блоки самі є кодом і даними** — блок-стрілка може бути і значенням, яке виводиться, і частиною механізму, а команди (MOVE, WELD, ROTATE, OUTPUT) зсувають, зварюють і обертають інші блоки. Усе обчислюється **паралельно**, як у Redstone; автор сам називає гру «тюрінговою смолою» (Turing tarpit) і «погано поясненою». Мета на рівні — пройти тести, а далі — найменша й найшвидша машина у трьох глобальних рейтингах.

## Поле і час
- Квадратна сітка (у прикладах ≈12×12 видимих клітин; точний розмір — у «Непевне»); клітина — порожня або один блок. Блоки, зварені між собою, рухаються групою.
- Ліворуч від поля — **вхідні списки** (Input List 1–3, «N left») і вихідні (Output List 1–3): черги блоків, які машина забирає й наповнює.
- Час `programmed`: запуск = такти (Cycle N у верхній панелі), у кожному такті всі активовані блоки діють одночасно. Є покроковий режим і 4 швидкості відтворення.
- Задача має кілька тест-кейсів (поле «Test Case: N»); перевіряється кожен.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| ARROW (блок-стрілка) | object | напрям ↑ → ↓ ← | найпростіші дані: саме стрілки потрібної орієнтації часто треба вивести |
| MOVE-блок | instruction (⏳) | напрям | коли ACTIVATED сигналом — дає MOVE COMMAND блоку в указаному напрямку від себе (і всім привареним до нього) |
| Сигнальний блок (стрілка з рисками) | conduit | напрям | передає SIGNAL далі по ланцюгу, активуючи наступні блоки (?) |
| OUTPUT-блок | sink | номер вихідного списку (1–3) | коли ACTIVATED — забирає блок, що стоїть ліворуч, і дописує в кінець OUTPUT LIST |
| WELD-блок | instruction (⏳) | — | зварює блоки між собою |
| UNWELD-блок | instruction (⏳) | — | скасовує зварювання |
| ROTATE-блок | instruction (⏳) | — | обертає себе й усе, що до нього приварене |
| Батарея (заряджений блок) | object | число / заряд (у трейлері 26, −9, −5, 16, −24…) | «charged battery blocks» з опису; блок із числом і смужкою-зарядом (див. «Непевне») |
| Вхідний список | source | 1–3 списки, «N left» | подає блоки в машину по одному |
| Вихідний список | sink | 1–3 списки | накопичує виведені блоки; порівнюється з очікуваним |
| Порожня клітина | — | — | вільне місце для блоку або руху |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, block)` → ЯКЩО `free(cell)` → ТО `place(player, block)` (будування до запуску; палітра — лише блоки, дозволені рівнем).
- КОЛИ `input(run)` → ТО `custom: «усі блоки обчислюються паралельно; один такт = один крок усіх активованих блоків»`.
- КОЛИ `custom: «блок отримав SIGNAL»` → ТО `set_state(block, activated)`.
- КОЛИ `state_on(move_block, activated)` → ТО `push(block_in_dir)` + `custom: «разом з усіма блоками, привареними до нього»`; ЯКЩО `not free(cell_behind)` → ТО `block` (?).
- КОЛИ `state_on(output_block, activated)` → ЯКЩО `occupied(cell_left, block)` → ТО `custom: «забрати блок ліворуч і дописати в кінець вихідного списку N»`.
- КОЛИ `state_on(weld_block, activated)` → ТО `attach(a, b)`.
- КОЛИ `state_on(unweld_block, activated)` → ТО `detach(a, b)`.
- КОЛИ `state_on(rotate_block, activated)` → ТО `rotate(rotate_block, 90)` + `custom: «обертається вся приварена група»`.
- КОЛИ `custom: «машина бере наступний вхідний блок»` → ЯКЩО `counter(input_left, >, 0)` → ТО `spawn_at(block, input_slot)`, `counter(input_left, −1)` (?).
- КОЛИ `input(submit)` → ЯКЩО `custom: «вихідні списки збіглися з очікуваними на всіх тест-кейсах»` → ТО `win`, `window(end-screen)`.
- КОЛИ `custom: «вихід не збігся з очікуваним»` → ТО `custom: «тест не зараховано, повернення до редагування»` (?).
- Рахунок: `counter(blocks_used)`, `counter(cycles_per_input)`, `counter(footprint)` — три окремі глобальні рейтинги; на екрані LEVEL PASSED — This Machine / Personal Best / Global Best.
- Поразки нема; рівень можна переробляти заради кращих метрик.

## Керування і ввід
- Мишею: вибрати блок у палітрі (ліворуч угорі, набір залежить від рівня) і поставити на клітину; хотбар 1–0 внизу — швидкі слоти (?).
- Клавіші F1–F10 — колірні групи блоків (у трейлері бар з кольорами F1…F10; блоки підсвічені синім/жовтим/рожевим/зеленим) (?).
- Праворуч унизу: номер тест-кейсу, ▶ (запуск), ▶| (крок), ■ (стоп), 4 швидкості (› » ››› ››››), SUBMIT.
- Навчальні рівні показують підказки-оверлеї з BACK / NEXT; наведення на блок дає тултіп з описом («MOVE block — When ACTIVATED: …»).

## Вікна, меню, HUD
- `game-screen`: сітка-поле; палітра блоків; ліві списки входу/виходу з лічильником «N left»; кнопки списків (іконки input/output 1–3); верхня панель категорій блоків і лічильник Cycle (?); панель задачі праворуч (назва рівня й умова); блок керування запуском.
- `tooltip` — опис блоку при наведенні; `tutorial-window` — оверлеї «Tutorial — Output Blocks» тощо.
- `end-screen` «LEVEL PASSED»: таблиця Blocks used / Cycles per Input / Footprint × This Machine / Personal Best / Global Best, позначка «Global Highscore!», BACK / NEXT.
- `world-map`: дерево вузлів-рівнів з галочками; бічна панель — умова рівня, найкращі метрики (Blocks used, Cycles/Step, Footprint) і PLAY.
- Пісочниця — те саме поле без задачі й тестів (окремий режим у меню (?)).
- Переходи: карта рівнів → рівень (поле) → SUBMIT → LEVEL PASSED → NEXT / BACK.

## Фічі поза полем
- `leaderboard-online` — глобальні рекорди в трьох категоріях (розмір, швидкість, площа).
- `mode-sandbox` — «Build that 1000 block machine»: поле без задачі.
- `level-unlock` / `world-map` — 25+ рівнів «від HARD до REALLY HARD», розгалужене дерево.
- `achievements`, `cloud-save` (Steam); безкоштовне демо.
- Мова — лише англійська.

## Варіації й родичі
- Родичі в корпусі: `opus-magnum`, `spacechem`, `infinifactory` (машина з деталей + метрики й гістограми); `factorio-circuit-network`, `manufactoria` (сигнали й черги); `befunge` (код на сітці, що читається напрямками); `markov-alg`; `stack-machines`.
- Межа сімʼї: агента нема, як у `opus-magnum`; від `build-sim` відрізняється тим, що мета — обчислення над списками з тест-кейсами.
- Осі варіацій: **чим є програма** (текст / граф / блоки на полі, що самі є даними); **паралельність** (один виконавець / кілька / усе поле одночасно); **метрики** (розмір / такти / площа).

## Цікавинки для курсу
- Блоки-інструкції, що активуються сигналом і діють на сусідів — клітинний автомат з командами — 🥈.
- Зварювання блоків і рух усієї групи (MOVE тягне все приварене, ROTATE обертає групу) — 🥇 (обхід звʼязної групи + колізії при паралельному русі).
- Вхідні/вихідні списки + тест-кейси як перевірка рівня — 🥉.
- Три метрики (блоки, такти на вхід, площа обмежувального прямокутника) і порівняння з особистим/глобальним рекордом — 📎.
- Покроковий запуск з 4 швидкостями — 🌱.

## Мапа на каталог
- Є: `push-object` (MOVE штовхає блок) · `stick-together` (WELD) · `cursor-place` · `step-execution` · `leaderboard` · `world-map` · `level-unlock` · `tutorial-window` · `end-screen` · `game-screen` · `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+code-is-data-blocks` «Блок водночас інструкція і дані» · game-logic/program · 🥈.
  - `+parallel-block-eval` «Усі блоки поля виконуються одночасно щотакту» · game-logic/program · 🥇.
  - `+signal-propagation` «Сигнал іде ланцюгом блоків і активує їх» · entities/state · 🥉.
  - `+entity-rotate` «Поворот блоку разом з привареною групою» · entities/move · 🥉.
  - `+io-test-streams` «Вхідні й вихідні списки з тест-кейсами» · game-logic/win · 🥉.
  - `+solution-metrics` «Розмір / такти / площа як рахунок» · game-logic/score · 📎.
  - `+footprint-metric` «Площа обмежувального прямокутника машини» · game-logic/score · 🌱.
  - `+step-run-speed`, `+sandbox-mode` — спільні для сімʼї.

## Пропозиції до словників
- `+role:instruction` — блок-команда на полі, що водночас є даними (MOVE, WELD, ROTATE).
- `+trigger:signal(a)` — сутність отримала сигнал / активована (також Factorio, Mindustry).
- `+effect:weld(a, b)` — зварити блоки в групу, що рухається разом (окремо від `attach` при контакті).
- `+effect:append_output(a, list)` — дописати сутність у вихідний список (IO-пазли: Block Machine, TIS-100, Manufactoria).
- `+feature:solution-metrics` — метрики розвʼязку як рахунок.
- `+feature:random-test-cases` — кілька тест-кейсів на рівень.

## Джерела
- ⭐ [Steam: Block Machine](https://store.steampowered.com/app/1584170/Block_Machine/) — опис (блоки = код і дані, паралельні обчислення, 15+ типів блоків: стрілки, заряджені батареї; 25+ рівнів; 3 категорії рекордів; пісочниця); скриншоти з тултіпами MOVE і OUTPUT, підказкою «WELD / UNWELD / ROTATE blocks», екраном LEVEL PASSED і картою рівнів; трейлер (кадри з числовими блоками, лічильник Cycle).
- [Steam: Block Machine Demo](https://store.steampowered.com/app/1593530/) — демо, ті самі скриншоти.
- [Блог Sebastian Schöner](https://blog.s-schoener.com/) — автор називає свої ігри «poorly explained puzzle games».
- YouTube: пошук «Block Machine kerntief gameplay».

## Непевне
- (?) Повний список 15+ типів блоків не знайдено: бачили ARROW, MOVE, OUTPUT, WELD, UNWELD, ROTATE, сигнальні стрілки, числові «батареї», категорії палітри «+ − × ÷» і «=» (арифметика й порівняння?) та іконку-кліщі (захоплення?).
- (?) Як саме генерується SIGNAL і як блоки беруть вхід (сині блоки «□»» / ««□» схожі на вхід-вихід зі списку) — з тултіпів видно лише «Use a SIGNAL to ACTIVATE this block».
- (?) Чи тест-кейси випадкові чи фіксовані (`random: setup` — припущення).
- (?) Footprint = площа обмежувального прямокутника (196 = 14²) — здогад з чисел на скриншоті.
- (?) «Cycles per Input» на екрані LEVEL PASSED і «Cycles/Step» на карті — та сама метрика з різною назвою.
- (?) Що буває при колізії паралельних рухів (два MOVE в одну клітину) — не знайдено.
- (?) Розмір поля, роль хотбару 1–0 і клавіш F1–F10 — лише з картинок.
- Автор: Steam пише розробника й видавця «kerntief»; пошукові агрегатори — Sebastian Schöner (власник kerntief, судячи з його блогу).
