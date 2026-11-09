---
title: Signpost (Pfeilpfad)
slug: signpost
aka: [Pfeilpfad, Arrow Path, Стрілковий шлях]
family: pencil-logic
also: []
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: setup
  goal: constraints
year: null
platforms: [PC, web, mobile]
links:
  - {kind: other, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/signpost.html", best: true, note: "мануал Tatham: правила, керування ланцюгами, параметри"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/signpost.html", note: "грати в браузері (WASM-версія колекції)"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Pfeilpfad/index.htm", note: "Janko: Pfeilpfad — правила DE/EN, 310 пазлів, походження"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=simon+tatham+signpost+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 65
mechanics: [markup-validity, completion-detection, satisfy-constraints, legal-move-highlight, path-drawing, keyboard-controls, unique-puzzle-generation, level-solver, field-size-picker, game-settings, seed-share, save-game, undo-redo, level-bank, +arrow-successor-chain, +chain-letter-labels, +ray-successor-highlight, +solve-into-undo]
proposes: ["+cond:on_ray(a, b, dir)", "+ui:chain-letter-label", "+ui:needs-predecessor-dot", "+window:params-dialog", "+window:game-id-dialog", "+card:arrow-successor-chain", "+card:chain-letter-labels"]
author: opus
date: 2026-11-09
---

# Signpost — пронумеруй усі клітинки 1…N так, щоб стрілка кожної вказувала в бік наступної

## Суть
У кожній клітинці, крім останньої, стоїть стрілка; деякі клітинки вже мають номери (завжди перший і останній). Гравець зʼєднує клітинки в одну послідовність 1, 2, …, N: наступна клітинка може бути на будь-якій відстані, але точно в напрямку стрілки попередньої. Виходить гамільтонів шлях через усе поле з «вказівниками». Незвичне: цифровий інтерфейс Tatham дозволяє будувати безіменні фрагменти ланцюга з тимчасовими літерами `a`, `a+1` і зливати їх, коли номер стане відомим.

## Поле і час
- Прямокутна сітка W×H; N = W·H клітинок, кожна отримує рівно один номер.
- Стрілки — у клітинках, напрямки по прямих і діагоналях (?: 8 напрямків).
- Шари: стрілки й дані номери (незмінні) · звʼязки «клітинка → наступна» гравця · номери/літери, виведені зі звʼязків.
- Час статичний; хід = створити або розірвати звʼязок. Пазл генерується (`random: setup`); старт/кінець або в кутах, або випадково (завжди показані).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка зі стрілкою | static | напрямок | наступник лежить на промені стрілки, будь-яка відстань |
| Остання клітинка (N) | sink | номер N | без стрілки, кінець шляху |
| Перша клітинка (1) | source | номер 1 | без попередника |
| Даний номер | mark | k | закріплений, змінити не можна |
| Звʼязок | mark | from → to | ставить гравець; один вихідний і один вхідний на клітинку |
| Ланцюг | zone | номери або літера | звʼязна послідовність; безіменний отримує літеру `a`, `a+1`, … |
| Точка «треба попередника» | mark | — | у куті клітинки, доки до неї не підвʼязано попередника |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_drag, a → b)` → ЯКЩО `custom: «b лежить на промені стрілки a»` (`+cond:on_ray`) and `legal(link)` → ТО `attach(a, b)` (b — наступник a).
- КОЛИ `input(right_drag, a → b)` → ЯКЩО `legal(link)` → ТО `attach(b, a)` (b — попередник a).
- КОЛИ `after(attach)` → ЯКЩО `custom: «одна з клітинок має номер k»` → ТО `set_value(other, k ± 1)` і далі по всьому ланцюгу.
- КОЛИ `after(attach)` → ЯКЩО `custom: «обидві клітинки без номерів»` → ТО `mark(chain, letter)` — `a` і `a+1`, наступний ланцюг — `b`, `b+1`; продовження ланцюга бере ту саму літеру.
- КОЛИ `after(attach)` → ТО `set_state(arrow, grey)` у джерела і `clear_state(dot, shown)` у приймача.
- КОЛИ `input(click, cell)` → ТО `custom: «підсвітити клітинки, з якими можна зʼєднати»`.
- КОЛИ `input(left_drag, cell → off_grid)` → ТО `detach(cell, neighbors)` — звʼязки клітинки розриваються.
- КОЛИ `input(right_drag, cell → off_grid)` → ТО `custom: «розірвати весь ланцюг клітинки»`.
- КОЛИ `constraint_broken(numbers)` → ЯКЩО `custom: «ланцюг зводить дві клітинки з несумісними номерами»` → ТО `block` (?).
- КОЛИ `all_constraints_met` → ТО `win` + `custom: «ефект перемоги, стиль у Preferences»`.
- Генерація: КОЛИ `level_start` → ЯКЩО `custom: «Force start/end to corners»` → ТО 1 — лівий верхній, N — правий нижній кут; інакше випадкові місця.
- Дедукція «єдиний кандидат»: якщо на промені стрілки лише одна клітинка без попередника — це наступник; симетрично: якщо на клітинку вказує лише одна стрілка — це попередник.
- Дедукція «номер на відстані»: між номерами k і k+m мусить вміститися ланцюг рівно з m кроків.
- Перемога: усі клітинки в одному ланцюгу 1…N, кожна стрілка вказує в бік наступника. Поразки й рахунку нема.

## Керування і ввід
- Ліва кнопка + drag від клітинки до наступника; права + drag — до попередника.
- Клік (лівий/правий) по клітинці — показ легальних цілей.
- Drag клітинки за межу поля: лівою — зняти її звʼязки, правою — розібрати весь ланцюг.
- Клавіатура: стрілки рухають курсор по клітинках і лініях; Enter — почати звʼязок, Enter над ціллю — завершити; Space — показати клітинки, що вказують на поточну (для звʼязку назад), Space ще раз — скасувати.
- Спільні дії колекції: undo/redo, нова гра, рестарт, solve.

## Вікна, меню, HUD
- `game-screen`: сітка зі стрілками (чорні → сірі після звʼязку), номери й літери ланцюгів, точки «треба попередника», лінії звʼязків, `legal-move-highlight` при кліку.
- Веб-версія (WASM): кнопки New game · Restart game · Undo move · Redo move · Solve game; меню Game: Enter game ID… · Enter random seed… · Download / Upload save file… · Preferences….
- Меню Type: пресети розміру; Custom… → `params-dialog` (Width, Height, Force start/end to corners).
- `settings-window` Preferences — стиль ефекту перемоги.
- `game-id-dialog` — game ID / random seed; `help-window` — мануал.

## Фічі поза полем
- Генератор з унікальним розвʼязком (?: як скрізь у колекції), розмір і кути старту/кінця в Custom.
- `undo` ∞ + `redo`, `restart-level`, Solve (`auto-solve`); `seed-display` / `seed-input` / `share-code`; збереження у файл.
- Janko: банк 310 паперових пазлів Pfeilpfad (`puzzle-bank`).

## Варіації й родичі
- У сімʼї: [Tatham collection](tatham-collection.md) (оболонка), [Fillomino](fillomino.md) і [Kakuro](kakuro.md) (числові пазли), [Masyu](masyu.md) (шлях через поле).
- Схожі за ідеєю: Hidato / Numbrix — шлях 1…N через сусідні клітинки без стрілок (?); Zipline — Janko називає схожим жанром (?).
- Поза сімʼєю: «кінь-тур» (гамільтонів шлях фігури, `chess-abstract`).
- **Осі варіацій**: напрямки стрілок (4 / 8) · відстань до наступника (будь-яка / сусідня) · кількість даних номерів · кути старту/кінця (фіксовані / випадкові).

## Цікавинки для курсу
- Обчислення легальних наступників: усі клітинки на промені стрілки без попередника — 🌱.
- Ланцюги як двозвʼязні списки з злиттям і перенумерацією (номер або літера + зсув) — 🥉.
- Тимчасові літерні мітки `a`, `a+1` для фрагментів без номера — 📎.
- Перевірка «один шлях 1…N, кожна стрілка в бік наступника» — 🌱.
- Генератор: випадковий гамільтонів шлях з напрямками + мінімізація даних номерів з перевіркою унікальності — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `legal-move-highlight` ↔ показ цілей при кліку · `path-drawing` ↔ drag-звʼязок · `keyboard-controls` · `unique-puzzle-generation`, `level-solver` · `field-size-picker`, `game-settings` · `seed-share`, `save-game`, `undo-redo` · `level-bank` (Janko).
- **Нема** → пропозиції карток:
  - `+arrow-successor-chain` «Шлях 1…N, де кожна клітинка-стрілка вказує на наступну» · game-logic/constraints · 📎 · слот {dirs: 4|8}.
  - `+chain-letter-labels` «Фрагменти ланцюга без номера отримують тимчасові літери a, a+1» · interface/input · 📎.
  - `+ray-successor-highlight` «Підсвітка всіх клітинок на промені, куди можна звʼязати» · interface/hud · 🌱 (уточнення `legal-move-highlight`).
  - `+solve-into-undo` — повтор з Tatham.

## Пропозиції до словників
- `+cond:on_ray(a, b, dir)` — B лежить на промені з A у напрямку dir, перешкоди не важливі (на відміну від `line_of_sight`).
- `+ui:chain-letter-label` — тимчасова літера ланцюга.
- `+ui:needs-predecessor-dot` — точка «до клітинки ще не підвʼязано попередника».
- `+window:params-dialog`, `+window:game-id-dialog` — повтори з Tatham collection.
- `+card:arrow-successor-chain`, `+card:chain-letter-labels` — див. мапу.

## Джерела
- ⭐ [Tatham: Signpost (мануал)](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/signpost.html) — правила, керування (drag до наступника/попередника, літери `a`/`a+1`, чорні/сірі стрілки, точки, drag за межу), клавіатура, Custom (Width, Height, Force start/end to corners), Preferences; «devised by Janko… 'Pfeilpfad'», додав James Harvey.
- [Tatham: Signpost (грати)](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/signpost.html) — WASM-версія, меню й коротка інструкція.
- [Janko: Pfeilpfad](https://www.janko.at/Raetsel/Pfeilpfad/index.htm) — правила DE/EN, 310 пазлів, «Signpost» як назва в Tatham; найраніша знайдена версія — Mikhael Khotiner (російськомовний сайт).
- YouTube: пошук «simon tatham signpost puzzle».

## Непевне
- (?) Походження: Tatham пише «devised by Janko», а Janko — що винахідник невідомий і найраніша версія від Mikhael Khotiner; рік не встановлено (`year: null`).
- (?) 8 напрямків стрілок (з діагоналями) — з памʼяті про вигляд гри, у мануалі не сказано.
- (?) Що відбувається при спробі зʼєднати несумісні номери (блок чи конфлікт) — не описано.
- (?) У Janko є й інший жанр «Signpost» (підрозділ Nanro) — це не та гра; не плутати.
- (?) Hidato / Numbrix / Zipline як родичі — з памʼяті / лише назва в Janko.
