---
title: MC Escher's Equestrian Armageddon
slug: mc-eschers-equestrian-armageddon
aka: []
family: thinky
also: [grid-platformer]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2013
platforms: [web]
links:
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=6851495", best: true, note: "грати в браузері: 4 рівні PuzzleScript"}
  - {kind: other, url: "https://api.github.com/gists/6851495", note: "вихідний код (gist, JSON, 2013-10-06): 4 стани героя, 8 правил сходинок, падіння, умова «No Horse»"}
  - {kind: other, url: "https://www.puzzlescript.net/Gallery/gifs/6851495.gif", note: "GIF з галереї: перший рівень"}
  - {kind: other, url: "https://raw.githubusercontent.com/increpare/PuzzleScript/master/src/games_dat.js", note: "дані галереї PuzzleScript: назва, автор Anna Clarke, лінк"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=MC+Escher%27s+Equestrian+Armageddon+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 85
mechanics: [move-4dir, move-by-input, keyboard-controls, gravity-fall, impassable-cells, destroy-all-enemies, undo-unlimited, restart-level, sequential-levels, save-progress, level-from-txt, +surface-gravity, +gravity-turn-stairs, +whip-adjacent-attack]
proposes: ["+card:gravity-turn-stairs", "+card:surface-gravity", "+card:whip-adjacent-attack", "+axis:gravity", "+window:title-screen"]
author: opus
date: 2026-11-19
---

# MC Escher's Equestrian Armageddon — герой ходить підлогою, стінами й стелею: сходинка в куті повертає його гравітацію на 90°, а мета — не лишити жодного коня

## Суть
Крихітна PuzzleScript-гра Anna Clarke (2013) на 4 рівні; назва — жарт про сходи Ешера й «кінський апокаліпсис». Герой має власну гравітацію в одному з чотирьох напрямків і падає туди до опори; сходинка в увігнутому куті переводить його з підлоги на стіну, зі стіни на стелю тощо.

Коні підкоряються звичайній гравітації вниз і самі не ходять. Клавіша дії поруч із конем перетворює його на калюжу крові; рівень пройдено, коли коней не лишилось.

## Поле і час
- Квадратна сітка в рамці стін, один екран на рівень; 4 рівні від 6×17 до ~20×43 клітин (з коду).
- Шари колізій: фон → кров → ціль → {герой у 4 станах, стіна, ящик, 4 види сходинок, кінь}; усе з останнього шару блокує одне одного.
- Покроково: хід = натискання. Будь-який рух запускає повторний прохід правил `again` (0.2 с), у якому герой і коні падають до опори; правило гравітації повторюється, доки є що зсунути, тож падіння завершується за один прохід.
- Гравітація — властивість сутності: у героя — стан ↓ / → / ← / ↑, у коней — завжди ↓. Опора — стіна, сходинка, кінь або сам герой.
- У легенді коду є ящик і ціль, але в рівнях вони не трапляються.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой (`Player1–4`) | player | гравітація ↓ / → / ← / ↑; спрайт повернутий ногами до своєї поверхні | крок у 4 напрямки екрана; падає в бік своєї гравітації до опори; дія — знищує коней поруч |
| Сходинка ↘ (`Steps1`) | static | кут «підлога + права стіна» | опора; перехід між підлогою і правою стіною |
| Сходинка ↙ (`Steps2`) | static | кут «підлога + ліва стіна» | опора; перехід між підлогою і лівою стіною |
| Сходинка ↗ (`Steps3`) | static | кут «права стіна + стеля» | опора; перехід між правою стіною і стелею |
| Сходинка ↖ (`Steps4`) | static | кут «ліва стіна + стеля» | опора; перехід між лівою стіною і стелею |
| Стіна | static | — | непрохідна, опора |
| Кінь | neutral | — | не ходить; падає вниз до опори; непрохідний і сам — опора; дія героя поруч → кров |
| Кров | mark | — | лишається на місці коня; прохідна, без поведінки |

## Правила (КОЛИ → ЯКЩО → ТО)
Рух і падіння:
- КОЛИ `input(dir)` → ЯКЩО `free(cell_ahead)` → ТО `move(hero, dir)`; інакше `block` (стіна, кінь, сходинка не «свого» напрямку).
- КОЛИ `after(move)` → ЯКЩО `free(cell_in_gravity_dir)` → ТО `fall(hero)` у бік власної гравітації, клітина за клітиною до опори.
- КОЛИ `after(move)` → ЯКЩО `free(cell_below)` → ТО `fall(horse)` — завжди вниз.

Сходинки (поворот гравітації на 90° і крок від кута вздовж нової поверхні):
- КОЛИ `input(dir)` → ЯКЩО `occupied(cell_ahead, steps)` and `custom: «сходинка — кут між поверхнею героя і сусідньою, герой іде в кут»` → ТО `set_state(hero, gravity_new)`, `move(hero, away_from_corner)`; в інших напрямках сходинка — `block`.

| Сходинка | Гравітація героя, куди йде | Нова гравітація, крок |
|---|---|---|
| ↘ `Steps1` | ↓, іде → | →, крок ↑ |
| ↘ `Steps1` | →, іде ↓ | ↓, крок ← |
| ↙ `Steps2` | ↓, іде ← | ←, крок ↑ |
| ↙ `Steps2` | ←, іде ↓ | ↓, крок → |
| ↗ `Steps3` | →, іде ↑ | ↑, крок ← |
| ↗ `Steps3` | ↑, іде → | →, крок ↓ |
| ↖ `Steps4` | ←, іде ↑ | ↑, крок → |
| ↖ `Steps4` | ↑, іде ← | ←, крок ↓ |

Дія і перемога:
- КОЛИ `input(action)` → ЯКЩО `occupied(neighbor4, horse)` → ТО `transform(horse, blood)` — усі коні в 4 сусідніх клітинах одразу.
- КОЛИ `all_gone(horse)` → ТО `win`, `next_level` (умова коду «No Horse»).
- Перемога: на рівні не лишилось коней · Поразки нема: герой не гине, глухий кут — undo / restart · Рахунку нема.

## Керування і ввід
- Стрілки — крок у напрямку **екрана**, а не відносно героя: на правій стіні вздовж неї ходять ↑ / ↓. Крок «від поверхні» підіймає на клітину, і герой одразу падає назад.
- X — дія: знищити коней поруч. Z — undo, R — рестарт (стандарт PuzzleScript).

## Вікна, меню, HUD
- `main-menu` — титульний екран PuzzleScript (`title-screen`): назва, «Anna Clarke», start / continue.
- `game-screen` — лише поле, HUD нема; стан гравітації видно зі спрайта героя.
- Переходи: титул → `game-screen` → (зник останній кінь) → наступний рівень → … → 4-й рівень.

## Фічі поза полем
- `levels-sequential` (4 рівні), `undo` ∞, `restart-level`, `continue` — стандарт PuzzleScript.
- Звуків нема (секція SOUNDS порожня); код відкритий у редакторі PuzzleScript.

## Варіації й родичі
- М. К. Ешер, «Відносність» (1953) — сходи, якими ходять у трьох гравітаціях; гра робить із цього правило: кут-сходинка перемикає «низ» героя.
- Родичі в корпусі: [Monument Valley](monument-valley.md) — неможлива геометрія Ешера й ходіння бічними гранями; [Kula World](../grid-platformer/kula-world.md) — гравітація повертається на 90° за **опуклим** ребром блока (тут — в **увігнутому** куті); [English Country Tune](english-country-tune.md) — своя гравітація в кожної кульки; [Sugar, Sugar](../dig-gravity/sugar-sugar.md) — перемикач гравітації для всього; [XOR](../dig-gravity/xor.md) — напрям падіння за типом обʼєкта; [Lime Rick](lime-rick.md) — інша PuzzleScript-гра з гравітацією героя.
- Осі варіацій: **чия гравітація** — уся сцена / кожна сутність своя (тут: герой ↔ коні) / за типом (XOR); **що її повертає** — перемикач (Sugar, Sugar) / увігнутий кут-сходинка (тут) / опуклий край (Kula World); **керування** — у координатах екрана (тут) / відносно героя.

## Цікавинки для курсу
- Гравітація як стан сутності (4 значення) і падіння в її бік до опори — 📎: `gravity-fall` з одним параметром напрямку.
- Сходинки як таблиця даних «стан × напрям × кут → новий стан + крок» (8 рядків) — 📎: гарна вправа на `interaction-table`.
- Дія «знищити всіх сусідів виду» і перемога «нікого не лишилось» — 🌱.
- Повторний прохід правил після ходу для падіння («хід → стабілізація») — 🌱.
- Розвʼязувач BFS: стан = позиція й гравітація героя + коні — 🥉 (після кожного кроку треба досимулювати падіння).

## Мапа на каталог
- Є: `move-4dir` · `move-by-input` · `keyboard-controls` ↔ стрілки; `gravity-fall` ↔ падіння героя й коней; `impassable-cells` ↔ стіни, сходинки, коні; `destroy-all-enemies` ↔ «No Horse»; `undo-unlimited` · `restart-level` · `sequential-levels` · `save-progress` · `level-from-txt` ↔ стандарт PuzzleScript.
- **Нема** → пропозиції карток:
  - `+gravity-turn-stairs` «Сходинка в куті повертає гравітацію героя на 90°» · entities/move · 📎 · слоти {corners: 4, transitions: 8}.
  - `+surface-gravity` (Monument Valley) — аватар ходить стінами й стелею; тут 4 дискретні поверхні.
  - `+whip-adjacent-attack` (Kroz) — тут без витрати: дія знищує коней у 4 сусідніх клітинах.

## Пропозиції до словників
- `+card:gravity-turn-stairs`, `+card:surface-gravity`, `+card:whip-adjacent-attack` — див. вище.
- `+axis:gravity` — значення `per-entity`: у кожної сутності свій напрям (герой — 4 стани, коні — завжди ↓).
- `+window:title-screen` — повтор (стандартний титул PuzzleScript).

## Джерела
- ⭐ [PuzzleScript: MC Escher's Equestrian Armageddon](https://www.puzzlescript.net/play.html?p=6851495) — гра в браузері, 4 рівні.
- [Вихідний код (gist через GitHub API)](https://api.github.com/gists/6851495) — обʼєкти й шари, 4 стани героя, 8 правил сходинок, падіння героя й коней, дія `[ Action Player | Horse ] -> [ Action Player | Blood ]`, умова `No Horse`; gist від 2013-10-06.
- [Дані галереї PuzzleScript](https://raw.githubusercontent.com/increpare/PuzzleScript/master/src/games_dat.js) — запис «MC Escher's Equestrian Armageddon · Anna Clarke» з цим лінком.
- [GIF з галереї](https://www.puzzlescript.net/Gallery/gifs/6851495.gif) — перший рівень: герой іде, падає в яму, підходить до коня.
- [Документація PuzzleScript: порядок виконання](https://www.puzzlescript.net/Documentation/executionorder.html) — правило виконується «as often as it can», пізні правила — після руху.
- YouTube: пошук «MC Escher's Equestrian Armageddon puzzlescript».

## Непевне
- (?) Останній рівень у коді має рядки різної довжини — як PuzzleScript його вирівнює, не перевірено.
- (?) Ящик і ціль у легенді — схоже, залишок шаблону; у рівнях їх нема.
- (?) Клавіші Z / R — стандарт PuzzleScript, у коді гри не задані.
- (?) Падіння за один прохід `again` виведено з документації; у грі не перевірено.
- (?) Відсилання до «Відносності» Ешера — тлумачення назви; автор цього не пояснює.
