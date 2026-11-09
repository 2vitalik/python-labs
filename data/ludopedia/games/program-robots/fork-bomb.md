---
title: "FORK BOMB: A Programming Game"
slug: fork-bomb
aka: [FORK BOMB, Fork Bomb]
family: program-robots
also: [build-sim]
klass: avatar
axes:
  field: hex
  time: programmed
  opponent: none
  info: partial
  random: setup
  goal: collect
year: 2026
platforms: [PC (Windows, Linux/SteamOS, Steam Early Access)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/5189090/FORK_BOMB_A_Programming_Game/", best: true, note: "опис: одна машина будує копію, 17 викликів API, бюджет інструкцій на тік, 11 уроків, 39 сценаріїв, пісочниця"}
  - {kind: other, url: "https://steamcommunity.com/app/5189090/discussions/0/706660083369704668/", note: "look(dir, n) працює лише по 6 прямих (гекс)"}
  - {kind: other, url: "https://steamcommunity.com/app/5189090/discussions/0/588439869536167990/", note: "send(text, range) безкоштовний і без тіку, recv() → None, повідомлення [text, q, r]"}
  - {kind: other, url: "https://steamcommunity.com/app/5189090/discussions/0/588439869536378173/", note: "кнопки Deploy / Step / Reset, видимість бота #1, графік energy vs spent"}
  - {kind: other, url: "https://steamcommunity.com/app/5189090/reviews/?browsefilter=toprated", note: "огляди: «low stakes Screeps», малий API, кампанія, Daily, швидкості симуляції"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=fork+bomb+programming+game+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [dig-terrain, step-execution, code-editor-window, help-window, rule-variants, daily-puzzle, level-select, sequential-levels, game-screen, +hex-grid-render, +real-language-code, +self-replicating-robots, +swarm-same-program, +tick-cost-model, +instruction-budget-per-tick, +function-unlock-progression, +range-broadcast-message, +machine-lifespan-upkeep, +shared-colony-energy, +sandbox-mode, +deterministic-seed-run, +runtime-error-stop, +api-call-disable, +code-snippets-library]
proposes: ["+effect:send", "+effect:recv", "+effect:dig", "+cond:budget_left(n)", "+trigger:budget_exhausted", "+window:scenario-tiers", "+window:sandbox-settings", "+ui:energy-graph", "+ui:api-reference-panel", "+feature:api-locks", "+card:instruction-budget-per-tick", "+card:range-broadcast-message", "+card:machine-lifespan-upkeep", "+axis:actors"]
author: opus
date: 2026-11-09
---

# FORK BOMB — Python-подібний код однієї машини, що копіює себе: усе масштабування — лише в твоєму коді

## Суть
На мертвій скелі стоїть одна машина і текстовий редактор. Гравець пише програму Python-подібною мовою: машина вміє рухатись, копати, відчувати ґрунт під собою, читати енергію колонії, а з 4-го уроку — будувати власну копію, яка запускає **той самий код з початку**. Нема апгрейдів, множників і валюти «за прогрес»: зростає лише словник функцій (17 викликів). Ріст — і нагорода, і тиск: код, що працює для 4 машин, ламається на 400 через спільну руду, затори в коридорах, одночасні пробудження й фіксований бюджет інструкцій на тік.

## Поле і час
- Гексагональна сітка (координати повідомлень `[text, q, r]`, `look` — лише по 6 прямих); світ має радіус (налаштування пісочниці), ґрунт — скеля з рудою різної щільності й твердості.
- Шари: ґрунт (скеля / прокопаний коридор / руда) + машини; видимість — від машин (Reset повертає видимість лише бота #1) — тому `info: partial`.
- Час `programmed` у тіках: кожна машина на тік виконує інструкції свого коду в межах **фіксованого бюджету**; кілька швидкостей симуляції.
- Детермінізм: той самий seed і програма дають той самий забіг.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Машина | player | позиція q, r; вік; скринька повідомлень | виконує спільний код; рух, копання, сенсори, spawn |
| Копія машини | ally | — | народжується від `spawn()`, стартує код з першого рядка |
| Скеля | static | твердість | прокопується `dig` (?) |
| Руда | resource | щільність, твердість | спільна для всіх машин; дає енергію колонії (?) |
| Коридор | terrain | — | прохідна клітина; одна машина на клітину — затори |
| Енергія колонії | resource | спільний пул | читається з коду; витрачається на копії й утримання (?) |
| Ціль сценарію | zone | (якщо є) | умова перемоги сценарію |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `exec(move(dir))` → ЯКЩО `free(cell)` → ТО `move(machine, dir)`; інакше `block` (інша машина чи скеля).
- КОЛИ `exec(dig(dir))` → ЯКЩО `cell(target, rock)` → ТО `custom: «прокопати клітину (руда — у енергію колонії)»` (?).
- КОЛИ `exec(sense())` → ТО `custom: «повертає тип ґрунту під машиною»`.
- КОЛИ `exec(look(dir, n))` → ТО `custom: «повертає вміст клітини на одній з 6 прямих»`; поза прямими — недоступно.
- КОЛИ `exec(spawn())` → ЯКЩО `counter(energy, >=, price)` → ТО `spawn(machine)`, `currency(-price)`; копія — `custom: «виконує код з початку»`.
- КОЛИ `exec(send(text, range))` → ТО `custom: «повідомлення [text q r] у скриньки машин у радіусі — безкоштовно й без витрати тіку»`.
- КОЛИ `exec(recv())` → ЯКЩО `custom: «скринька порожня»` → ТО `custom: «повертає None»`; інакше — найстаріше повідомлення (?).
- КОЛИ `exec(cmd)` → ЯКЩО `custom: «бюджет інструкцій на цей тік вичерпано»` → ТО `custom: «машина чекає наступного тіку»`.
- КОЛИ `tick` → ТО `currency(-upkeep)` за кожну машину (?).
- КОЛИ `counter(age, >=, lifespan)` → ТО `disappear(machine)` (?).
- КОЛИ `custom: «синтаксична чи рантайм-помилка»` → ТО `crash`, `message(пояснення простою англійською + рядок)`.
- КОЛИ `exec(cmd)` → ЯКЩО `custom: «виклик заблоковано уроком / сценарієм / pro-рівнем»` → ТО `crash` (?).
- КОЛИ `custom: «ціль сценарію досягнуто»` → ТО `win`, `unlock(next)`.
- Перемога: ціль сценарію · Поразка: колонія вимерла / ціль недосяжна (?) · Рахунок: — (публічні лідерборди лише в планах).

## Керування і ввід
- Текстовий редактор коду; бібліотека **сніпетів** (свої функції-бібліотеки; ліміт 4000 символів зняли в 0.4.1).
- Кнопки **Deploy** (запустити), **Step** (один тік), **Reset** (світ у стан після Deploy); кілька швидкостей симуляції.
- Панелі API-довідки й Field Guide відкриті під час набору; гравці просять vi/Emacs-прив'язки й Ctrl-F.

## Вікна, меню, HUD
- `main-menu` (гравці просили кнопку виходу й навігацію стрілками).
- `level-select` — 11 уроків кампанії.
- Вибір сценаріїв (custom «scenario-tiers»): 39 сценаріїв у 4 рівнях складності, pro-рівень без сенсорів, ціни, позиції й ідентичності.
- Налаштування пісочниці (custom «sandbox-settings»): ~30 параметрів — радіус світу, щільність і твердість руди, тривалість життя, утримання, бюджет інструкцій, вимкнення окремих викликів API.
- `game-screen`: гекс-світ з машинами; `code-editor-window`; панель помилок; графік енергії «energy vs spent» (червона й жовта лінії); кнопки Deploy/Step/Reset; повзунок/перемикач швидкості.
- `help-window`: пошукова API-довідка з прикладами (позначено, які виклики ще закриті) + Field Guide.
- Daily — щоденна задача (чи реалізовано повністю — питають на форумі).
- Переходи: main-menu → урок / сценарій / пісочниця → game-screen ↔ редактор → Deploy → результат.

## Фічі поза полем
- `function-unlock-progression`: 15 викликів за 10 уроків, `send()`/`recv()` — на 11-му.
- `mode-sandbox` без цілей; `custom-rules` (налаштування світу й API); `daily-puzzle`.
- Детерміновані прогони (seed + програма) — основа для майбутніх серверно перевірених лідербордів.
- 23 досягнення; ранній доступ 12–18 місяців: програми у файлах на диску, публічні лідерборди, більше сценаріїв.

## Варіації й родичі
- У сімʼї: `screeps` (гравці: «Screeps з низькими ставками» — тут без PvP), `the-farmer-was-replaced` (Python-подібний код, мультидрони, відкриття функцій), `core-war` (програма, що копіює себе), `ai-challenge-ants` (рій з одним кодом), `codingame-cellularena`.
- Осі варіацій: **копіювання** (нема / спавн дронів / програма-копія себе); **ліміт** (тіки на дію / бюджет інструкцій на тік / памʼять); **звʼязок** (нема / спільна памʼять / повідомлення з радіусом); **сенсори** (повні / прибрані на pro-рівні).

## Цікавинки для курсу
- Рій машин з однією програмою, кожна — від початку коду: розподілені алгоритми без координатора — 🥇.
- Бюджет інструкцій на тік (кооперативне планування інтерпретатора) — 🥈.
- `send(text, range)` / `recv()` зі скринькою і координатами відправника — 📎.
- Гекс-сітка з осьовими координатами q, r і «погляд» по 6 прямих — 📎.
- Детермінований прогін за seed (повтор рішення) — 🥉.
- Пісочниця, що вмикає/вимикає виклики API — 🌱.

## Мапа на каталог
- Є: `dig-terrain` · `step-execution` · `code-editor-window` · `help-window` · `rule-variants` (пісочниця) · `daily-puzzle` · `level-select` · `sequential-levels` · `game-screen` · `+hex-grid-render` · `+real-language-code` · `+self-replicating-robots` · `+swarm-same-program` · `+tick-cost-model` · `+function-unlock-progression` · `+sandbox-mode` · `+runtime-error-stop` (уже в корпусі).
- **Нема** → пропозиції карток:
  - `+instruction-budget-per-tick` «Фіксований бюджет інструкцій агента на тік» · game-logic/program · 🥈.
  - `+range-broadcast-message` «Повідомлення в радіусі зі скринькою» · game-logic/program · 📎.
  - `+machine-lifespan-upkeep` «Тривалість життя й утримання агентів» · entities/state · 📎.
  - `+shared-colony-energy` «Спільний пул енергії колонії» · game-logic/economy · 🌱.
  - `+deterministic-seed-run` «Той самий seed + програма = той самий прогін» · game-logic/history · 🥉.
  - `+api-call-disable` «Вимкнення окремих викликів API у сценарії» · game-logic/program · 🌱.
  - `+code-snippets-library` «Бібліотека сніпетів коду гравця» · interface/input · 📎.

## Пропозиції до словників
- `+effect:send`, `+effect:recv` — повідомлення між агентами (уже пропоновані в сімʼї; ще одне підтвердження).
- `+effect:dig` — прокопати клітину (окремо від `set_cell`, бо має твердість і продукт).
- `+cond:budget_left(n)` / `+trigger:budget_exhausted` — бюджет інструкцій на тік.
- `+window:scenario-tiers`, `+window:sandbox-settings`.
- `+ui:energy-graph` — графік енергії й витрат у часі; `+ui:api-reference-panel` — довідка, відкрита поруч із редактором.
- `+feature:api-locks` — закриті виклики API за прогресом/сценарієм.
- `+axis:actors` — `swarm` (сотні однакових машин з одним кодом).

## Джерела
- ⭐ [Steam: FORK BOMB](https://store.steampowered.com/app/5189090/FORK_BOMB_A_Programming_Game/) — «ONE MACHINE BUILDS ONE MACHINE»; move/dig/sense/енергія, spawn з 4-го уроку, 17 викликів, send/recv з 11-го; бюджет інструкцій на тік; 11 уроків, 39 сценаріїв у 4 рівнях, pro-рівень; пісочниця ~30 параметрів; детермінізм; пояснення помилок; ранній доступ 02.10.2026.
- [Looking in hex](https://steamcommunity.com/app/5189090/discussions/0/706660083369704668/) — `look(dir, n)` лише по 6 прямих.
- [Tutorials thread](https://steamcommunity.com/app/5189090/discussions/0/588439869536167990/) — `send(text, range)` безкоштовний і без тіку, `recv()` → None, повідомлення `[text, q, r]`.
- [QoL UI/UX suggestions](https://steamcommunity.com/app/5189090/discussions/0/588439869536378173/) — Deploy/Step/Reset, видимість бота #1, графік energy vs spent.
- [Snippets 4000char limit](https://steamcommunity.com/app/5189090/discussions/0/706660083369807337/) — сніпети, ліміт знято в 0.4.1.
- [Огляди](https://steamcommunity.com/app/5189090/reviews/?browsefilter=toprated) — малий API, кампанія, Daily, швидкості, порівняння зі Screeps і The Farmer Was Replaced.

## Непевне
- (?) Повний список 17 викликів — відомі `move`, `dig`, `sense`, `look`, `spawn`, `send`, `recv` і читання енергії; решта не перелічена.
- (?) Чи руда перетворюється на енергію при копанні; ціна копії й утримання — числа не бачив.
- (?) Цілі сценаріїв (`goal: collect` — припущення: ціль/квота; бувають і «target»).
- (?) Що стається з машиною наприкінці lifespan і чи бувають «поразки».
- (?) Видимість: «туман» від машин виведено з опису Reset («only bot #1's visibility»).
- (?) Розробник Quiet Machines — сайт quietmachines.com належить іншій компанії (камери PTZ).
