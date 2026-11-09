---
title: MOLEK-SYNTEZ
slug: molek-syntez
aka: [Molek-Syntez, МОЛЕК-СИНТЕЗ]
family: program-robots
also: [thinky]
klass: cursor
axes:
  field: hex
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2019
platforms: [PC, Mac, Linux]
links:
  - {kind: official, url: "https://www.zachtronics.com/molek-syntez/", best: true, note: "суть: програмований синтезатор молекул з бензолу, ацетону, HCl; гістограми, GIF, пасьянс"}
  - {kind: steam, url: "https://store.steampowered.com/app/1168880/MOLEKSYNTEZ/", note: "реліз 19.11.2019 (EA з 4.11), лідерборди друзів, GIF-експорт"}
  - {kind: other, url: "https://www.xanthir.com/b53d0", note: "«Unstated Priorities»: порядок дій у такті, черговість емітерів, правила вибору сусіда для звʼязку"}
  - {kind: other, url: "https://www.gog.com/game/moleksyntez", note: "GOG: опис, відгуки про рух модулів і вільне обертання звʼязків"}
  - {kind: itch, url: "https://zachtronics.itch.io/molek-syntez", note: "itch.io (з результатів пошуку)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=molek-syntez+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [command-program, step-execution, code-editor-window, stick-together, cell-transform, sequential-levels, level-unlock, level-select, leaderboard, replay, game-screen, end-screen, +swarm-separate-programs, +instruction-timeline, +emitter-beam-target, +rotate-shift-whole-molecule, +implicit-hydrogen-valence, +bond-unbond, +bond-partner-priority, +action-phase-order, +molecule-match-output, +collision-halt, +solution-metrics, +metric-histograms, +gif-export, +solitaire-minigame]
proposes: ["+trigger:phase(name)", "+cond:valence_free(atom)", "+effect:add_hydrogen(atom)", "+effect:remove_hydrogen(atom)", "+effect:bond_to_neighbor(atom)", "+effect:shift(molecule, dir)", "+role:emitter", "+ui:emitter-beam", "+feature:card-cheat-move"]
author: opus
date: 2026-11-09
---

# MOLEK-SYNTEZ — нерухомі емітери на гекс-полі обертають і зсувають молекулу променями й перебудовують її звʼязки через водень

## Суть
Пізня гра Zachtronics про синтез ліків у румунській квартирі 2092 року. Гравець програмує синтезатор: навколо гекс-поля стоять **емітери** (модулі), кожен зі своїм рядком інструкцій; на відміну від Opus Magnum, вони не носять атоми, а діють променем на молекулу — зсувають, обертають, додають або забирають водень, створюють звʼязки. Із вхідних реагентів (бензол, ацетон, соляна кислота…) треба зібрати цільову молекулу. Порядок дій усередині такту не задокументовано, і спільнота розібрала його експериментами.

## Поле і час
- Поле — **гексагональна сітка**; у центрі — робоча зона з молекулою, по краях — емітери з променями вздовж осей (?).
- Водень **неявний**: на полі видно лише важкі атоми (C, N, O, S, Cl), а H — лічильник валентності атома (?).
- Час `programmed`: такт — усі емітери виконують по інструкції; у межах такту дії йдуть фазами (вилучення/вихід → зняття й переміщення водню → додавання водню → рух і обертання → нові звʼязки → вхід), а емітери однієї фази — за номером (1 першим).
- Детермінізм повний.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Емітер (модуль) | player | номер, напрямок променя, рядок інструкцій | виконує свою програму циклічно, діє на атом, у який влучає промінь |
| Промінь | — | вісь гекса | визначає, на яку молекулу/атом діє емітер (?) |
| Атом C / N / O / S / Cl | object | валентність, кількість H | частина молекули; пріоритет для звʼязку C > N > O > S > Cl |
| Водень | mark | лічильник на атомі | знімання H звільняє валентність → звʼязок із сусідом; додавання H розриває звʼязок |
| Звʼязок | mark | кратність 1–3 (?) | склеює атоми в молекулу; обертається вільно |
| Молекула | object | граф атомів | рухається й обертається як ціле |
| Вхід | spawner | реагент | подає нову молекулу (остання фаза такту) |
| Вихід | sink | цільова молекула, квота (?) | приймає й вилучає молекулу, що збігається (перша фаза) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `custom: «фази такту по черзі: delete/output → hydrogen shunt/remove → hydrogen add → move/rotate → bond → input; у фазі емітери діють за номером»`.
- КОЛИ `exec(delete)` → ТО `disappear(molecule)`; клітина вільна для руху лише з наступного такту.
- КОЛИ `exec(output)` → ЯКЩО `same(molecule, target, structure)` → ТО `disappear(molecule)`, `counter(produced, +1)` (?).
- КОЛИ `exec(remove_H)` → ЯКЩО `custom: «в атома є водень»` → ТО `custom: «H знято, атом звʼязується з сусідом за пріоритетом»`.
- КОЛИ `custom: «атом обирає сусіда для звʼязку»` → ТО `custom: «спершу найменша кратність, далі тип C>N>O>S>Cl, далі напрямок від 4 години за годинниковою»`; для розриву — спершу найбільша кратність.
- КОЛИ `exec(add_H)` → ТО `custom: «атом отримує H і розриває один звʼязок за тим самим пріоритетом»` (?).
- КОЛИ `exec(move)` → ЯКЩО `free(cell_ahead)` → ТО `shift(molecule, beam_dir)` (?).
- КОЛИ `exec(rotate cw|ccw)` → ЯКЩО `custom: «є місце для обертання»` → ТО `rotate(molecule, ±60°)` (?).
- КОЛИ `exec(bond)` → ТО `attach(atom, neighbor)` за пріоритетом.
- КОЛИ `exec(input)` → ЯКЩО `free(input_zone)` → ТО `spawn_at(reagent, input)`.
- КОЛИ `custom: «рух або обертання в зайняту клітину»` → ТО `crash` (?).
- КОЛИ `counter(produced, ==, quota)` → ТО `win`, `window(end-screen)` з гістограмами.
- Перемога: потрібна кількість цільових молекул · Поразка: нема, лише зупинка симуляції · Рахунок: кілька метрик розвʼязку на гістограмах (?).

## Керування і ввід
- Розстановка/вибір емітерів і таймлайн інструкцій під полем (як в Opus Magnum) (?).
- Кнопки інструкцій рухають модулі в різні боки — гравці скаржаться, що «ліво/право» залежить від положення модуля.
- Запуск, крок, прискорення (?).

## Вікна, меню, HUD
- `level-select` — список замовлень-ліків (?).
- `game-screen`: гекс-поле з емітерами й променями (`emitter-beam`, custom); `instruction-timeline`; ціль-молекула; кнопки запуску.
- `end-screen` + гістограми метрик; GIF-експорт.
- `custom-window`: пасьянс Zachtronics (можна «чітити» — класти карту будь-куди).
- `settings-window` (?).

## Фічі поза полем
- `solution-metrics` + гістограми; `leaderboard-online` (друзі).
- `gif-export` розвʼязку.
- Пасьянс з чит-ходом; `achievements`, `cloud-save`.
- Нема мануалу й повного туторіалу — правила вивчаються експериментом (і з постів спільноти).

## Варіації й родичі
- Прямий родич: [opus-magnum](opus-magnum.md) — гекс, таймлайн, метрики, GIF, пасьянс; різниця — руки носять атоми там, а тут емітери діють на молекулу на місці.
- [spacechem](spacechem.md) (звʼязки й вальдо), [infinifactory](infinifactory.md), [tis-100](tis-100.md).
- Осі варіацій: **маніпулятор** (рука хапає / промінь діє на відстані); **звʼязки** (гліф-бондер / неявний водень); **порядок у такті** (документований / фазовий з пріоритетами).

## Цікавинки для курсу
- Фазовий такт: дії сортуються за фазою, потім за номером актора — 🥈.
- Неявний водень як валентність атома й вибір партнера для звʼязку за трьома ключами — 🥈.
- Обертання молекули-графа навколо атома на гекс-сітці (кубічні координати) — 🥈.
- Звірка молекули з ціллю як ізоморфізм графів з мітками — 🥇.
- Гістограма метрик + GIF — 📎 / 🥉.

## Мапа на каталог
- Є: `command-program` · `step-execution` · `code-editor-window` · `stick-together` (звʼязки) · `cell-transform` (водень змінює атом) · `sequential-levels` / `level-unlock` / `level-select` · `leaderboard` · `replay` (GIF) · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+emitter-beam-target` «Нерухомий актор діє променем на першу ціль» · entities/interact · 🥉.
  - `+rotate-shift-whole-molecule` «Зсув/обертання цілої звʼязної групи» · entities/move · 🥈.
  - `+implicit-hydrogen-valence` «Валентність як лічильник на атомі» · entities/state · 🥉.
  - `+bond-partner-priority` «Вибір сусіда за ключами» · entities/interact · 🥉; `+action-phase-order` «Фази такту» · game-logic · 🥈.
  - `+swarm-separate-programs`, `+instruction-timeline`, `+bond-unbond`, `+molecule-match-output`, `+collision-halt`, `+solution-metrics`, `+metric-histograms`, `+gif-export`, `+solitaire-minigame` — як в Opus Magnum.

## Пропозиції до словників
- `+trigger:phase(name)` — фаза всередині такту (ширше за `phase_start`: впорядкований список фаз).
- `+cond:valence_free(atom)` — атом має вільну валентність.
- `+effect:add_hydrogen(atom)` / `+effect:remove_hydrogen(atom)` — зміна лічильника H, що тягне розрив/утворення звʼязку.
- `+effect:bond_to_neighbor(atom)` — звʼязатися з сусідом за пріоритетом.
- `+effect:shift(molecule, dir)` — зсув групи (≠ `shift` ряду поля).
- `+role:emitter`; `+ui:emitter-beam`.
- `+feature:card-cheat-move` — чит-хід у пасьянсі.

## Джерела
- ⭐ [Zachtronics: MOLEK-SYNTEZ](https://www.zachtronics.com/molek-syntez/) — суть, реагенти, гістограми, GIF, пасьянс з читом.
- [Steam](https://store.steampowered.com/app/1168880/MOLEKSYNTEZ/) — дата релізу, лідерборди, сетинг.
- [xanthir.com: Molek-Syntez Unstated Priorities](https://www.xanthir.com/b53d0) — фази такту, черговість емітерів, правила вибору сусіда.
- [GOG](https://www.gog.com/game/moleksyntez) — відгуки про керування й вільне обертання звʼязків.
- [itch.io](https://zachtronics.itch.io/molek-syntez) — сторінка гри (з результатів пошуку).
- YouTube: пошук «molek-syntez gameplay».

## Непевне
- (?) Набір інструкцій емітера (move, rotate, add/remove H, bond, delete, output, input) виведено з фаз xanthir; точні назви й аргументи — невідомі.
- (?) Геометрія: де стоять емітери, як промінь обирає атом, чи емітер рухається — з памʼяті й відгуків.
- (?) Метрики гістограм (назви, кількість) і квота виходу — офіційні сторінки кажуть лише «score histograms».
- (?) Реакція на зіткнення (зупинка чи блок) — з памʼяті.
- (?) Wikipedia-статті нема (404); Thinky Games і GiantBomb недоступні.
