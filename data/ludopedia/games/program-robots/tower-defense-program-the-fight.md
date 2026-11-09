---
title: "tower.defense(): Program The Fight"
slug: tower-defense-program-the-fight
aka: ["tower.defense()", "Program The Fight"]
family: program-robots
also: [tower-lanes]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: survive
year: 2026
platforms: [PC (Windows)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/4409920/Towerdefense_Program_The_Fight/", best: true, note: "опис: вежі Sentry / Lance / Warden, контролер IF/ELSE з візуальних блоків, висота й лінія видимості, лабораторні прогони з паузою / кроком / перемоткою; 8 скриншотів усіх фаз місії"}
  - {kind: other, url: "https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1843481262690098", note: "пост розробника: гру перебудовано з нуля, нове демо — 20 місій і три програмовані вежі"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=tower.defense()+Program+The+Fight", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [tower-placement, tower-range, line-of-sight-attack, height-levels, enemy-reached-base, spawn-schedule, sensor-predicates, step-execution, rewind, undo-redo, replay-window, codex-window, tutorial-window, end-screen, game-screen, keyboard-controls, threat-range, +visual-rule-blocks, +per-tower-controller, +target-priority-selector, +program-blueprints, +block-budget, +deterministic-rehearsal, +causal-inspection, +lab-vs-live-run, +optional-objectives, +placement-zones, +sight-checks]
proposes: ["+role:base", "+effect:fire(target, ammo)", "+cond:target_rank(prop, op)", "+trigger:decision(tower)", "+window:controller-panel", "+window:run-inspector", "+ui:sight-checks", "+ui:block-budget", "+feature:lab-rehearsal"]
author: opus
date: 2026-11-09
---

# tower.defense(): Program The Fight — tower defense, де вежа не цілиться сама: кожній збираєш правило IF/ELSE з візуальних блоків

## Суть
Соло-проєкт SofiaStudio (демо 2026, реліз — «2026»): машини йдуть маршрутом до реле, а гравець ставить вежі в зони обслуговування й **програмує контролер кожної** — без синтаксису, з блоків «вогонь → ціль → вибірка ворогів → набій». Програма росте від «стріляй у найближчого» до компактних IF/ELSE з порівняннями й логічними операторами за бронею, позицією й тиском. Поле — частина коду: висота розширює корисну дальність, барʼєри й дахи ріжуть лінію видимості. Перед справжнім запуском — детермінована лабораторна репетиція з паузою, кроком, перемоткою й поясненням «чому вежа обрала саме цю ціль».

## Поле і час
- Квадратна сітка плиток в ізометрії (тег «Grid-Based Movement»), з коридорами-маршрутом (intake line, стрілки напрямку), позначеними **зонами обслуговування** для веж, перепадами висоти, барʼєрами й дахами.
- Відстані — в метрах уздовж маршруту («covers 17 m of the 60 m intake line»).
- Час `programmed`: гравець планує й програмує, потім прогін іде тіками («Tick 153 of 184», «Moment 496 of 591»); прогін можна паузити, крокувати й перемотувати.
- Детермінізм: репетиція й живий прогін з тією ж програмою дають той самий результат.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Sentry | tower | залізо (hardware 40/40), бюджет блоків (3/3), дальність, набої | пряма стрільба; вибір цілі й типу набою важливі |
| Lance | tower | — | обдуманий лінійний постріл: важать таймінг і вирівнювання (?) |
| Warden | tower | — | підтримка: сканує, мітить і сповільнює загрози для решти плану |
| Машина (напр. Courier) | enemy | позиція на маршруті, броня | іде intake line одна за одною або групами; доходить до реле — шкодить |
| Реле (relay) | static | цілісність 20 | ціль оборони; кожна машина, що дійшла, знімає частину цілісності |
| Маршрут (intake line) | zone | довжина (23 м, 60 м) | шлях машин зі стрілками; може петляти (Switchback) |
| Зона обслуговування | zone | — | лише тут можна ставити вежу («This spot works») |
| Підвищення | terrain | висота | розширює корисну дальність вежі |
| Барʼєр / дах | static | — | перериває лінію видимості |
| Точка входу | spawner | розклад груп | звідки виходять машини («Two groups arrive far apart») |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, sentry, cell)` → ЯКЩО `custom: «клітина в позначеній зоні обслуговування»` і `has(player, hardware)` → ТО `place(player, sentry)`; підказка показує покриття маршруту і скільки з N «перевірок видимості» вільні.
- КОЛИ `input(program_tower)` → ТО `window(controller)`; блоки додаються в дерево правила, бюджет блоків «3 / 3 — exactly on budget».
- КОЛИ `tick` → ТО `custom: «кожна вежа виконує свій контролер — приймає рішення цього тіку»`.
- КОЛИ `custom: «вибірка Enemies in range»` → ТО `custom: «множина ворогів у дальності вежі»` — `in_range(tower, machine, r)` і `line_of_sight(tower, machine)`.
- КОЛИ `custom: «селектор цілі»` → ТО `custom: «з множини обрати: найдальшого вздовж маршруту / найменш просунутого / найближчого»`.
- КОЛИ `custom: «умова IF (броня, позиція, тиск) істинна»` → ТО `custom: «виконати гілку IF, інакше ELSE»`.
- КОЛИ `custom: «дія Fire a shot»` → ЯКЩО `custom: «ціль обрано»` → ТО `damage(target, n)` набоєм обраного типу (Standard rounds…); інакше `custom: «вежа нічого не робить цей тік»`.
- КОЛИ `custom: «барʼєр або дах між вежею й ціллю»` → ТО `block` (лінія видимості перервана).
- КОЛИ `custom: «вежа на підвищенні»` → ТО `custom: «корисна дальність більша»`.
- КОЛИ `custom: «Warden діє на машину»` → ТО `set_state(machine, marked)`, `speed(machine, −n)`.
- КОЛИ `reach(machine, relay)` → ТО `damage(relay, n)`, `disappear(machine)`.
- КОЛИ `hp_zero(relay)` → ТО `lose`.
- КОЛИ `all_gone(machine)` → ТО `window(end-screen)`: «Stopped 4, let through 0. Relay integrity 20 of 20».
- КОЛИ `level_end` → ТО `custom: «нагороди-цілі: Relay held · Relay untouched · Program within budget · No help needed»` (+ без зайвих живих змін).
- КОЛИ `input(start_lab_test)` → ТО `custom: «репетиція: нічого не записується в результат; pause / step / rewind»`.
- КОЛИ `input(deploy)` → ТО `custom: «живий прогін — цей рахується»`; КОЛИ `custom: «зміна програми під час живого бою»` → ТО `counter(live_changes, +1)` (знижує оцінку).

## Керування і ввід
- Мишею або клавіатурою: рамку місця рухають мишею чи стрілками, Build here / Cancel; Tab — навігація, Space — активувати, Esc — закрити (є «Mouse Only Option»).
- Програмування: дерево блоків у панелі контролера — дія («Fire a shot»), під нею слоти Target («The enemy furthest along the route»), Enemies («Enemies in range»), Ammunition («Standard rounds»); кожен слот — випадний список; ✕ видаляє блок; Show blocks · Undo · Redo.
- Креслення (Blueprints): зберегти програму, повторно використати, змінити локальну копію без зміни оригіналу.
- Прогін: Start lab test · Play / Pause · Step · Rewind · Speed 1x; Edit & retry; Deploy.

## Вікна, меню, HUD
- `game-screen`: угорі — назва місії й фаза (PLANNING — Changes are safe · PROGRAMMING · LAB TEST — Nothing is recorded · LIVE RUN — This one counts · DEBRIEF · INSPECTING), рядок поточної підказки, кнопки Machine cards · Contacts · Display; канал «SOFIA // MAINTENANCE CHANNEL» з кроками навчання (Step 1 of 2, Hide tips).
- Ліва панель: Mission (брифінг: скільки машин, цілісність реле, ціль), This spot (hardware, blocks, coverage, `+ui:sight-checks`, «Runs its own rules»), дії Place Sentry · Move selected · Program tower · Blueprints.
- Низ: керування прогоном, лічильники «Tick N of M · Moment N of M», статус (Ready / Done), Edit & retry, Deploy; підказка клавіш.
- `+window:controller-panel` — «Sentry 1 controller»: `+ui:block-budget`, Tower program, «Applied: Added Enemies in range to the program».
- `end-screen` (debrief «Intake line held»): зупинено / пропущено, цілісність, нагороди; Inspect run · Restart mission · Edit & retry · Return to network.
- `+window:run-inspector` — «WHY THIS TICK»: вибір вежі й тіку з позначками подій, кроки рішення («This step found no enemy at all…»), «The cause»; блоки програми показують «FOUND NOTHING» (`replay-window`).
- `codex-window` — Machine cards (картки ворогів); мапа мережі місій (Return to network) (?); Display — налаштування відображення (?).

## Фічі поза полем
- `tutorial` — канал SOFIA веде крок за кроком; `onboarding-hints` (Hide tips / Show tips).
- `+feature:lab-rehearsal` — безпечна детермінована репетиція з `rewind` і `step-mode`, потім Deploy.
- `replay` з причинним поясненням кожного тіку (inspect run).
- Необовʼязкові цілі оптимізації: бюджет заліза й блоків, мінімум живих змін — як `par-target`.
- Кампанія: демо — 20 місій, 3 вежі; `localization` — 10 мов.

## Варіації й родичі
- Родичі в корпусі: `tower-lanes` (`gem-td`, `fieldrunners`, `desktop-tower-defense` — розстановка веж без програмування), `gladiabots` (поведінкові дерева з умов і цілей), `carnage-heart`, `robot-rumble`, `screeps` (програмовані бойові агенти); з сімʼї — `lightbot` / `cargo-bot` (візуальні блоки замість тексту).
- Межа сімʼї: поле й хвилі — з `tower-lanes`, але головна дія — правило вибору цілі, а не розстановка й апгрейди.
- Осі варіацій: **хто цілиться** (вежа сама / пріоритет зі списку / програма IF/ELSE); **мова** (візуальні блоки / текст); **перевірка** (одразу бій / репетиція → живий бій).

## Цікавинки для курсу
- Селектор цілі: з множини ворогів у дальності обрати найдальшого / найменш просунутого вздовж маршруту — 📎.
- Лінія видимості з барʼєрами й висотою на сітці — 🥉.
- Контролер вежі як дерево блоків (дія → ціль → фільтр → набій) з бюджетом блоків — 🥈.
- Детермінований прогін з перемоткою (зберігати стан на кожен тік) — 🥈.
- «Чому цей тік»: журнал кроків рішення з причиною для кожного блоку — 🥇.
- Нагороди-цілі на debrief (реле ціле, у бюджеті, без допомоги) — 🌱.

## Мапа на каталог
- Є: `tower-placement` · `tower-range` · `line-of-sight-attack` · `height-levels` · `enemy-reached-base` · `spawn-schedule` · `sensor-predicates` · `step-execution` · `rewind` · `undo-redo` (редактор програми) · `replay-window` · `codex-window` (Machine cards) · `tutorial-window` · `end-screen` · `game-screen` · `keyboard-controls` · `threat-range` (покриття).
- **Нема** → пропозиції карток:
  - `+visual-rule-blocks` «Правило з візуальних блоків без синтаксису» · game-logic/program · 🥉.
  - `+per-tower-controller` «Кожна вежа має власну програму» · game-logic/program · 🥉.
  - `+target-priority-selector` «Вибір цілі за пріоритетом (найдальший, найближчий…)» · entities/combat · 📎.
  - `+program-blueprints` «Зберегти програму як шаблон, локальні копії» · game-logic/program · 📎.
  - `+block-budget` «Ліміт блоків програми й заліза» · game-logic/constraints · 🌱.
  - `+deterministic-rehearsal` «Детермінований прогін з перемоткою» · game-logic/history · 🥈.
  - `+causal-inspection` «Пояснення рішення агента на кожен тік» · interface/results · 🥇.
  - `+lab-vs-live-run` «Безпечна репетиція, потім залікова спроба» · game-logic/win · 📎.
  - `+optional-objectives` «Нагороди-цілі на підсумку місії» · game-logic/score · 🌱.
  - `+placement-zones` «Ставити лише в позначених зонах» · entities/legality · 🌱.
  - `+sight-checks` «Підрахунок вільних ліній видимості з точки» · entities/combat · 📎.

## Пропозиції до словників
- `+role:base` — ціль оборони з цілісністю (реле, база TD).
- `+effect:fire(target, ammo)` — постріл вежі з типом набою.
- `+cond:target_rank(prop, op)` — ціль — найбільша/найменша за властивістю (просування маршрутом, відстань).
- `+trigger:decision(tower)` — вежа приймає рішення цього тіку.
- `+window:controller-panel` — панель програми окремої вежі / агента.
- `+window:run-inspector` — розбір записаного прогону «чому цей тік».
- `+ui:sight-checks` — скільки ліній видимості вільні з точки.
- `+ui:block-budget` — шкала використаних блоків програми.
- `+feature:lab-rehearsal` — репетиція без наслідків перед заліковим запуском.

## Джерела
- ⭐ [Steam: tower.defense(): Program The Fight](https://store.steampowered.com/app/4409920/Towerdefense_Program_The_Fight/) — опис механік (3 вежі, контролери, креслення, зони, висота, лінія видимості, репетиції, бюджети), 8 скриншотів фаз місії «Switchback» і «Two arrivals», вимоги, 10 мов.
- [Пост «Rebuilt from scratch — the new demo is live»](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1843481262690098) — 20 місій демо, кіберпанк-сетинг, візуальні блоки, «very early demo».
- YouTube: пошук «tower.defense() Program The Fight».

## Непевне
- (?) Гра ще не вийшла (Steam: «2026», доступне демо); механіки можуть змінитися.
- (?) Як саме працюють Lance і Warden (довжина лінії, сила сповільнення, мітка) — лише опис Steam.
- (?) Повний перелік блоків умов (броня, тиск), селекторів і типів набоїв; як виглядає IF/ELSE в інтерфейсі — на скриншотах лише просте правило з 3 блоків.
- (?) Наскільки висота збільшує дальність; чи кожна машина знімає однакову цілісність реле.
- (?) Що таке Contacts і мапа мережі місій («Return to network»).
