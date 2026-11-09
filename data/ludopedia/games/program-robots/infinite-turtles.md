---
title: Infinite Turtles
slug: infinite-turtles
aka: []
family: program-robots
also: [thinky, connect-rotate]
klass: cursor
axes:
  field: nested
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2022
platforms: [PC, Mac, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1952740/Infinite_Turtles/", best: true, note: "опис базових блоків (clone, filter, lock, switch, inc/dec, nullifier), рекурсія «downie», скриншоти сітки й панелі тестів"}
  - {kind: other, url: "https://steamcommunity.com/app/1952740/discussions/0/3600093929978346271/", note: "розробник: ліміт downie 1 000 000 і 10 000 рівнів вкладення, розвʼязки > 1 млн тіків не йдуть на сервер"}
  - {kind: other, url: "https://steamcommunity.com/app/1952740/discussions/0/3777994239406611295/", note: "розробник: одна точка зупинки й один watchpoint на дизайн"}
  - {kind: other, url: "https://steamcommunity.com/app/1952740/discussions/0/4039229863731709864/", note: "розробник: подвійний клік перемикає фільтр Nul ↔ нуль"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1952740&count=20&maxlength=4000", note: "новини: community levels, 80 рівнів, ліміт downie, прискорення симуляції"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Infinite+Turtles+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [path-drawing, cell-click, piece-rotate-flip, user-procedures, step-execution, sequential-levels, level-unlock, level-select, game-screen, help-window, undo-redo, redo, state-string, level-exchange, in-game-editor, +token-flow-paths, +design-as-component, +self-recursion-downie, +token-clone, +token-filter-zero-nul, +token-lock, +token-switch, +nul-terminated-lists, +port-spec-tests, +recursion-depth-limit, +breakpoint-watchpoint, +skip-idle-steps, +community-levels, +friend-solutions-delay, +custom-path-colors]
proposes: ["+effect:route(a, dir)", "+cond:value(a, op, n)", "+role:token", "+window:test-cases", "+ui:token-queue", "+feature:breakpoint", "+axis:signal"]
author: opus
date: 2026-11-09
---

# Infinite Turtles — токени-числа котяться доріжками сітки, а готова схема вкладається сама в себе («downie») до нескінченності

## Суть
Пазл Charlie Brej (автор [ComPressure](compressure.md)) про обчислення на токенах: на клітинному полі гравець розставляє кілька базових блоків (клон, фільтр, замок, перемикач, ±1, нуліфікатор) і зʼєднує їх кольоровими доріжками, якими біжать токени-числа або порожній токен Nul. Кожна пройдена схема стає блоком наступних, а **поточну схему можна поставити всередину неї самої** — «downie», менша копія тебе, що робить те саме: так розвʼязуються додавання, ділення, списки й паліндроми рекурсією замість циклів. Решта гри — тести на 4 портах і рекорди.

## Поле і час
- Дизайн — квадратна сітка ≈9×9 клітин (за скриншотами); блок займає клітину, доріжки йдуть клітинами між блоками й можуть перетинатися мостами.
- 4 порти на краях: ↑ (жовтий, верх), ← (зелений, ліво), → (червоний, право), ↓ (синій, низ); рівень каже, які з них входи, а які виходи.
- `nested`: блок-дизайн (свій або «downie» — той самий дизайн) — це повне поле 9×9 всередині клітини; вкладення до 10 000 рівнів, загалом до 1 000 000 downie.
- Час `programmed`: покрокова симуляція; токени рухаються доріжками; кроки без видимої активності пропускаються.
- Детерміновано; тест — фіксовані черги вхідних токенів і очікувані черги вихідних.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Токен | object | число (00, 01, …) або Nul (∅) | рухається доріжкою від виходу блока до входу наступного |
| Доріжка | conduit | колір (налаштовується) | веде токени; кілька доріжок перетинаються без зʼєднання |
| Клон | spawner | 1 вхід → 2 виходи | розмножує токен |
| Фільтр | switch | режим Nul або нуль (подвійний клік) | токен 0 або Nul — на іншу доріжку, решта — прямо |
| Замок | gate | закритий / відкритий | не пускає токен, доки його не відімкне токен збоку |
| Перемикач | switch | ліво / право | спрямовує токени ліворуч або праворуч; напрямок задає токен, поданий з іншого кінця |
| Інкремент / декремент | object | +1 / −1 | змінює значення токена |
| Нуліфікатор | object | 0 ↔ Nul | перетворює нуль на Nul і навпаки |
| Дизайн-компонент | container | пройдений рівень, 4 порти | виконує свою схему всередині клітини |
| Downie | container | поточний дизайн | рекурсивний виклик самого себе |
| Порт-вхід | source | черга токенів тесту | подає токени в поле |
| Порт-вихід | sink | очікувана черга | записує токени й порівнює |
| Коментар | mark | текст | підпис на полі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, block)` → ТО `place(player, block)`; КОЛИ `input(drag_path)` → ТО `custom: «доріжка між виходом і входом»`.
- КОЛИ `tick` → ТО `move(token, along_path)`; `custom: «кроки без змін пропускаються у візуалізації»`.
- КОЛИ `enter(token, clone)` → ТО `clone(token)` — копія йде на другий вихід.
- КОЛИ `enter(token, filter)` → ЯКЩО `custom: «токен = 0 (режим нуля) або Nul (режим Nul)»` → ТО `move(token, side_exit)`; інакше `move(token, straight)`.
- КОЛИ `enter(token, lock)` → ЯКЩО `state(lock, locked)` → ТО `block` (токен чекає); КОЛИ `enter(token, lock_side)` → ТО `clear_state(lock, locked)`.
- КОЛИ `enter(token, switch_control)` → ТО `set_state(switch, left|right)`; КОЛИ `enter(token, switch)` → ТО `move(token, switch_state)`.
- КОЛИ `enter(token, inc)` → ТО `set_value(token, v+1)`; декремент — `set_value(token, v−1)`.
- КОЛИ `enter(token, nullifier)` → ЯКЩО `custom: «токен = 0»` → ТО `transform(token, nul)`; ЯКЩО Nul → ТО `transform(token, zero)`.
- КОЛИ `enter(token, component_port)` → ТО `custom: «токен входить у вкладене поле через відповідний порт; вихід підсхеми — на доріжку зовні»`.
- КОЛИ `enter(token, downie)` → ТО `spawn(downie_instance)` — `custom: «менша копія того самого дизайну обробляє токен»`.
- КОЛИ `counter(downies, >, 1000000)` або `counter(depth, >, 10000)` → ТО `custom: «помилка виходу (ліміт downie)»`.
- КОЛИ `enter(token, output_port)` → ЯКЩО `custom: «не збігається з наступним очікуваним»` → ТО `custom: «тест провалено»`.
- КОЛИ `custom: «усі тест-кейси дали очікувані черги»` → ТО `win`, `custom: «рівень відкриває наступний, дизайн стає блоком»`.
- КОЛИ `custom: «розвʼязок довший за 1 000 000 тіків»` → ТО `custom: «не надсилається в рекорди»` (часу симуляції ліміту нема).
- Перемога: усі тест-кейси пройдено · Поразка: нема (тест червоний — правиш) · Рахунок: рекорди з друзями й глобальні (?).

## Керування і ввід
- Миша: вибрати блок у палітрі й поставити на клітину; протягнути доріжку від порту до порту; подвійний клік по фільтру — Nul ↔ нуль.
- Вкладка редагування: виділення, гумка, undo, redo, віддзеркалення по горизонталі/вертикалі, коментар, пензель кольору доріжок; копіювання й вставка між дизайнами, переміщення блоків.
- Запуск: ▶ пауза ⏮ (на початок), `speed-slider`, лічильник downie; одна точка зупинки (breakpoint) і один watchpoint на дизайн.
- Під час прогону можна зайти всередину підкомпонента й дивитися його роботу.

## Вікна, меню, HUD
- `level-select` (кнопка-сітка): рівні з назвами («Division», «List Equal», «Prime»…), user/community levels.
- `game-screen`: поле з 4 кольоровими портами; ліворуч угорі іконка поточного дизайну (стек вкладення); праворуч вкладки — рівні, редагування (ключ), тест (касета), ?; палітра базових блоків і сітка пройдених дизайнів (прокрутка).
- `test-cases` (custom): вкладки тест-кейсів (червона — провалений), черги токенів на кожному порту (`token-queue` custom) — входи й очікувані виходи.
- `dialogue-window`: персонаж-астронавт з текстом завдання («Let's try adding two numbers…»), кнопки BLAH (історія) і HINT.
- `help-window` «?»; `editor-window`: свій рівень із тест-кейсами, публікація в community levels.
- Переходи: level-select → game-screen ⇄ вкладки; подвійний клік по блоку → його вміст → назад іконкою дизайну.

## Фічі поза полем
- Глобальні рекорди й рекорди друзів; рішення нових community-рівнів приховані від друзів тиждень.
- Обмін дизайнами рядками (`state-string`), копіювання між дизайнами, коментарі й кольори.
- 80 рівнів (останні 8 — надскладні, після всіх інших) (?); досягнення Steam; демо-версія.
- Мови: англійська, японська, китайська (спр. і трад.).

## Варіації й родичі
- Автор: [compressure](compressure.md) — та сама оболонка, аналоговий тиск замість токенів.
- Корпус: [human-resource-machine](human-resource-machine.md) і [7-billion-humans](7-billion-humans.md) (обчислення над числами-предметами), [manufactoria](manufactoria.md) (стрічка й маршрутизація), [tis-100](tis-100.md) (вузли й порти), [turing-complete](turing-complete.md), [befunge](befunge.md) (потік керування по сітці). Поза корпусом: Patrick's Parabox (поле в полі), λ-числення.
- Осі варіацій: **повторне використання** (лише готові блоки / свій дизайн як блок / виклик самого себе — рекурсія); **дані** (біти / числа / числа + Nul-термінатор для списків); **керування потоком** (фільтр за значенням / перемикач, керований токеном / замок).

## Цікавинки для курсу
- Рекурсія через «downie» — поле, що містить себе, з лімітами глибини й кількості — 🥇.
- Потік токенів по доріжках з клон/фільтр/замок/перемикач — 🥈 (dataflow-машина з синхронізацією).
- Nul як термінатор списку; ділення повторним відніманням, порівняння списків токен за токеном — 🥉 (задачі-тести).
- Стек вкладення при інспекції (зайти в підкомпонент під час прогону) — 🥉.
- Пропуск «порожніх» кроків візуалізації — 📎.

## Мапа на каталог
- Є: `path-drawing` (доріжки) · `cell-click` · `piece-rotate-flip` (віддзеркалення блоків) · `user-procedures` (пройдені дизайни, рекурсія) · `step-execution` (пауза, на початок, швидкість) · `sequential-levels` / `level-unlock` / `level-select` · `game-screen` · `help-window` · `undo-redo` / `redo` · `state-string` · `level-exchange` · `in-game-editor`.
- **Нема** → пропозиції карток:
  - `+token-flow-paths` «Токени біжать доріжками між блоками» · game-logic/program · 🥈.
  - `+self-recursion-downie` «Дизайн вкладає сам себе» · game-logic/program · 🥇; `+recursion-depth-limit` · 📎.
  - `+token-clone` · `+token-filter-zero-nul` · `+token-lock` · `+token-switch` — базові блоки dataflow · entities/interact · 📎 кожен.
  - `+nul-terminated-lists` «Список як черга токенів з Nul у кінці» · game-logic/program · 🥉.
  - `+port-spec-tests` «Тест-кейси: черги на портах» · game-logic/win · 🥉; `+breakpoint-watchpoint` · interface/input · 🥉; `+skip-idle-steps` · 📎.
  - `+community-levels` + `+friend-solutions-delay` · levels/bank · 🥉; `+custom-path-colors` · 🌱; `+design-as-component` · 🥈.

## Пропозиції до словників
- `+effect:route(a, dir)` — спрямувати токен на один із виходів блока (фільтр, перемикач); у правилах поки `move`.
- `+cond:value(a, op, n)` — значення токена порівняно з N (0, Nul).
- `+role:token` — дані, що рухаються провідниками (токен, літера, кулька), відмінні від `object`.
- `+window:test-cases` — вкладки тест-кейсів з чергами портів; `+ui:token-queue` — черга значень на порту.
- `+feature:breakpoint` — точка зупинки / watchpoint у симуляції.
- `+axis:signal` — тут `number-token` (див. ComPressure: `analog`).

## Джерела
- ⭐ [Steam: Infinite Turtles](https://store.steampowered.com/app/1952740/Infinite_Turtles/) — опис базових блоків, рекурсія, інструменти, тести, обмін рядками, рекорди; 5 скриншотів (сітка, порти, палітра, тест-панель, діалог).
- [Обговорення: Output error](https://steamcommunity.com/app/1952740/discussions/0/3600093929978346271/) — ліміти downie і тіків від розробника.
- [Обговорення: breakpoints](https://steamcommunity.com/app/1952740/discussions/0/3777994239406611295/) · [фільтр нуля](https://steamcommunity.com/app/1952740/discussions/0/4039229863731709864/) · «Division», «List Equal (Level 35)» — поради розробника.
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1952740&count=20&maxlength=4000) — реліз 19 червня 2022, community levels, 80 рівнів.
- YouTube: пошук «Infinite Turtles gameplay».

## Непевне
- (?) Розмір поля 9×9 — порахував за скриншотами, у тексті ніде не названо.
- (?) Точна семантика замка й перемикача (з якого боку «відмикають» і «вибирають») — лише за фразами опису Steam; входи/виходи клона — з іконки.
- (?) Метрики рекордів (кроки, кількість блоків?) — у джерелах не названі.
- (?) Чи доріжка вміщує кілька токенів (черга) і що буде при зустрічі токенів — не перевірено.
- (?) 80 рівнів — з анонсу (липень 2022) про 8 додаткових; фінальну кількість не перевірив.
