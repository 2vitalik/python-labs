---
title: Circuit Maze
slug: circuit-maze
aka: []
family: tower-lanes
also: [thinky]
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: score
year: 2025
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3421850/Circuit_Maze/", best: true, note: "TD без бою: найдовший лабіринт з виданих блоків, 80 рівнів, демо"}
  - {kind: other, url: "https://steamcommunity.com/app/3421850/discussions/0/604150260655204642/", note: "розробник про телепорти: стартова й цільова плити, Сигнал біжить назад лабіринтом; зірки відкривають рівні; секції A–D"}
  - {kind: other, url: "https://steamcommunity.com/app/3421850/discussions/0/604149834549562344/", note: "розробник: натхнення — WC3-мапа Mazing Contest; мультиплеєра нема"}
  - {kind: other, url: "https://steamcommunity.com/app/3421850/reviews/?browsefilter=toprated", note: "огляди: лазер з радіусом 3, warp-зони, змагання за десяті секунди"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Circuit+Maze+Patrik+Windahl", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [cursor-place, impassable-cells, chase-bfs, reachability-check, teleport-pair, level-select, level-unlock, sequential-levels, +maze-by-towers, +fixed-block-budget, +path-time-score, +stars-rating, +star-gate-unlock, +slow-zone-block]
proposes: ["+trigger:run_start", "+effect:recompute_path", "+role:signal", "+role:blocker", "+ui:best-time"]
author: opus
date: 2026-11-09
---

# Circuit Maze — tower defense без бою: з виданих блоків збудуй лабіринт, яким Сигнал біжитиме найдовше

## Суть
Інді-пазл Патріка Віндаля (Швеція) за мотивами WC3-мапи Mazing Contest: від TD лишилось тільки mazing-ядро. На кожному рівні є старт, ціль і фіксований набір блоків; гравець розставляє їх так, щоб найкоротший шлях Сигналу від старту до цілі став якнайдовшим. Результат — час пробігу в секундах (до десятих), за нього дають зірки. Спецблоки (лазер з радіусом дії, телепорти) додають до лабіринту «друге проходження» тих самих коридорів.

## Поле і час
- Квадратна сітка в ізометрії (теги Steam: Grid-Based Movement, Isometric, Top-Down); клітини стартової й цільової плит, перешкоди й особливі тайли задає рівень.
- Без тиску часу: фаза планування статична; потім Сигнал проходить лабіринт, і рахується час.
- Рівні поділені на секції (A, B, C, D…), кожна будує на попередніх і ускладнює комбінації; усього 80 рівнів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Сигнал (жовта куля) | enemy (`+role:signal`) | швидкість | біжить від старту до цілі найкоротшим шляхом через лабіринт |
| Стартова плита | spawner | — | звідси виходить Сигнал |
| Ціль | static | — | Сигнал дійшов → зупинка годинника |
| Звичайний блок | static (`+role:blocker`) | ліміт на рівень | займає клітину, непрохідний; формує коридори |
| Лазер | tower | радіус 3 блоки | діє на Сигнал у радіусі (уповільнює (?)); ефект можна отримати кілька разів, якщо шлях проходить повз нього знову |
| Телепорт / warp-зона | terrain | пара «вхід → цільова плита» | Сигнал переноситься на цільову плиту й біжить далі |
| Перешкода рівня | static | — | задана рівнем непрохідна клітина |
| Особливі тайли | terrain | — | у рівнях є «різні тайли» з властивостями (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, block, cell)` → ЯКЩО `free(cell)` and `counter(block_left, >, 0)` → ТО `place(block, cell)`, `counter(block_left, -1)`.
- КОЛИ `input(place, block, cell)` → ЯКЩО `not path_exists(start, goal)` → ТО `block` (?) — закрити шлях не можна.
- КОЛИ `input(remove, block)` → ТО `disappear(block)`, `counter(block_left, +1)`.
- КОЛИ `custom: «trigger run_start: гравець запускає Сигнал»` → ТО `spawn_at(signal, start)`, `timer(start)`.
- КОЛИ `tick` → ТО `move(signal, next_on_shortest_path)`.
- КОЛИ `enter(signal, teleport_in)` → ТО `teleport(signal, destination_plate)`, `custom: «effect recompute_path від цільової плити»`.
- КОЛИ `in_range(laser, signal, 3)` → ТО `custom: «лазер затримує Сигнал (?)»`.
- КОЛИ `reach(signal, goal)` → ТО `timer(stop)`, `score(run_time)`, `custom: «зірки за порогами часу»`.
- КОЛИ `counter(stars_on_level, >=, 1)` → ТО `unlock(next_level)`.
- Перемога: дійти до порогу хоча б 1 зірки · Поразка: — · Рахунок: час пробігу в секундах (вище — краще), особистий рекорд рівня.

## Керування і ввід
- Миша: вибрати блок з набору рівня → клік по клітині ставить; прибрати поставлене, щоб перебудувати.
- Запуск Сигналу й перегляд пробігу; рівень можна переграти скільки завгодно, щоб «вичавити» десяті секунди.

## Вікна, меню, HUD
- `level-select`: секції A–D з рівнями й зірками.
- `game-screen`: ізометрична сітка, панель блоків з лишком кількості, кнопка запуску, час пробігу й `+ui:best-time` (?).
- `end-screen` (?) — час і зірки після пробігу.
- `achievements-window` — досягнення Steam (системні).

## Фічі поза полем
- `stars-rating`: зірки за час; щонайменше 1 зірка відкриває наступний рівень (гравці просили відкривати секції за сумою зірок).
- `level-unlock`, `levels-sequential` за секціями; хмарні збереження Steam; демо з частиною рівнів.
- Мультиплеєра нема; у 2025 розробник сказав, що «дуже рано» досліджує його.

## Варіації й родичі
- Натхнення — WC3-мапа Mazing Contest (змагання: хто збудує довший лабіринт); TD-корені — [desktop-tower-defense](desktop-tower-defense.md), [mazing-td-modern](mazing-td-modern.md), [gem-td](gem-td.md) (стіни з невдалих самоцвітів).
- Сусіди за ідеєю «максимізуй шлях»: Pathery (браузерний пазл на найдовший шлях (?)).
- **Осі варіацій**: мета — вижити / максимізувати довжину чи час шляху · ресурс — гроші / фіксований набір блоків · спецблоки — лише стіни / стіни + зони дії + телепорти · оцінка — пройдено/ні / зірки за час.

## Цікавинки для курсу
- Довжина найкоротшого шляху як функція розстановки: BFS після кожної посадки + заборона закрити шлях — 🥉.
- Оптимізаційний пазл «максимізуй BFS-відстань фіксованим числом стін» — 🥇 (пошук розвʼязку / локальний пошук, порівняння з рекордом).
- Телепорт з поверненням Сигналу назад у лабіринт (шлях = сума сегментів) — 📎.
- Лазер з радіусом, повз який шлях проходить кілька разів, — 📎 (кількість входів у зону вздовж шляху).
- Зірки за пороги часу + відкриття рівнів — 🌱.

## Мапа на каталог
- Є: `cursor-place` ↔ блок на клітину · `impassable-cells` ↔ блоки й перешкоди · `chase-bfs` ↔ найкоротший шлях Сигналу · `reachability-check` ↔ шлях не можна закрити · `teleport-pair` ↔ warp-зони · `level-select` + `level-unlock` + `sequential-levels`.
- **Нема** → пропозиції карток:
  - `+maze-by-towers` — уже пропонувалась сімʼєю.
  - `+fixed-block-budget` «Рівень видає фіксований набір блоків» · levels/format · 🌱 · слот {blocks}.
  - `+path-time-score` «Очки = довжина/час найкоротшого шляху» · game-logic/score · 📎.
  - `+stars-rating` «1–3 зірки за пороги» · levels/progression · 🌱 · слот {thresholds}.
  - `+star-gate-unlock` «Наступний рівень — за ≥1 зірку» · levels/progression · 🌱.
  - `+slow-zone-block` «Блок з радіусом, що затримує бігуна» · entities/combat · 📎 · слот {radius}.

## Пропозиції до словників
- `+trigger:run_start` — гравець запускає симуляцію після фази планування.
- `+effect:recompute_path` — підтвердження сімʼї.
- `+role:signal` — бігун-«ворог», який не шкодить, а лише міряє лабіринт; `+role:blocker` — підтвердження.
- `+ui:best-time` — найкращий результат рівня поруч із поточним.

## Джерела
- ⭐ [Steam: Circuit Maze](https://store.steampowered.com/app/3421850/Circuit_Maze/) — мета «найдовший лабіринт з виданих ресурсів», 80 рівнів, різні блоки з особливостями, без стресу, теги.
- [Steam-обговорення B07](https://steamcommunity.com/app/3421850/discussions/0/604150260655204642/) — розробник: телепорти, стартова й цільова плити, Сигнал, ≥1 зірка для наступного рівня, секції A–D.
- [Steam-обговорення «Multiplayer?»](https://steamcommunity.com/app/3421850/discussions/0/604149834549562344/) — Mazing Contest як натхнення, мультиплеєр не планувався, згодом «дуже рано досліджується».
- [Steam-огляди](https://steamcommunity.com/app/3421850/reviews/?browsefilter=toprated) — лазер з радіусом 3 блоки, warp-зони, «десяті секунди», нечасті неточності таймінгів.
- YouTube: [пошук «Circuit Maze Patrik Windahl»](https://www.youtube.com/results?search_query=Circuit+Maze+Patrik+Windahl).

## Непевне
- (?) Що саме робить лазер (сповільнює, зупиняє, повертає Сигнал) — огляди кажуть лише про радіус 3 і багаторазове використання.
- (?) Чи гра забороняє закрити шлях, чи просто не дає запустити Сигнал.
- (?) Повний список блоків і тайлів; пороги зірок (на D10 — «3 зірки»); кількість секцій понад A–D.
- (?) Pathery як родич — з памʼяті, сторінку не відкривав.
- (?) Сигнал іде найкоротшим шляхом — випливає з жанру mazing, явно в джерелах не сказано.
