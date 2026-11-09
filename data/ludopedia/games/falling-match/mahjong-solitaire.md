---
title: Mahjong Solitaire (Shanghai, Маджонг-пасьянс)
slug: mahjong-solitaire
aka: [Shanghai, Mah-Jongg, Taipei, Mahjong Titans, KMahjongg, The Turtle, Shanghai Solitaire, Kyodai, «Маджонг»]
family: falling-match
also: []
klass: cursor
axes:
  field: layers
  time: turn
  opponent: none
  info: partial
  random: setup
  goal: state
year: 1981
platforms: [PLATO, PC, Mac, Amiga, Windows, Linux, web, mobile, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mahjong_solitaire", best: true, note: "правила, Turtle, 144 плитки, вільна плитка, складність (PSPACE/NP), варіанти, історія PLATO → Shanghai → Taipei → Mahjong Titans"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Shanghai_(video_game)", note: "Activision 1986: склад 144 плиток, квіти/сезони парують між собою, правило вільного ребра, сиквели"}
  - {kind: other, url: "https://docs.kde.org/stable_kf6/en/kmahjongg/kmahjongg/rules.html", note: "KMahjongg: правила, рекорд за часом, Hint знімає з рекордів"}
  - {kind: other, url: "https://docs.kde.org/stable_kf6/en/kmahjongg/kmahjongg/interface.html", note: "KMahjongg: меню — Numbered Game, Hint, Demo, Shuffle, Undo/Redo, Board Editor, пауза ховає плитки"}
  - {kind: other, url: "https://docs.kde.org/stable_kf6/en/kmahjongg/kmahjongg/configuration.html", note: "KMahjongg: блимання пар, тільки розвʼязні, показ знятих плиток"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=mahjong+solitaire+turtle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [cell-click, selection-highlight, hover-highlight, height-levels, undo-redo, restart-level, game-pause, time-out, time-bonus, score-records, leaderboard, no-moves-left, unsolvable-states, level-solver, seed-share, attract-demo, in-game-editor, editor-window, save-game, theme-select, game-screen, end-screen, settings-window, +pair-match-removal, +free-tile-rule, +reshuffle-remaining, +solvable-deal, +hint-pair, +pause-hides-field]
proposes: ["+cond:free_tile", "+effect:reshuffle", "+card:pair-match-removal", "+card:free-tile-rule", "+card:reshuffle-remaining", "+card:solvable-deal", "+card:hint-pair", "+card:pause-hides-field", "+ui:removed-tiles", "+feature:hint-disqualifies"]
author: opus
date: 2026-11-09
---

# Mahjong Solitaire — знімай пари однакових вільних плиток із багатошарової піраміди

## Суть
144 плитки маджонгу викладено лицем догори в багатошарову фігуру (класична — «черепаха», Turtle). Гравець знімає пари однакових плиток, але лише **вільних**: на плитці нічого не лежить і хоча б один бік (лівий або правий) відкритий. Мета — зняти всі; поразка — лишились плитки без жодної вільної пари. Ядро — вибір, яку з кількох однакових пар зняти, бо плитки під верхнім шаром не видно, а неправильний порядок замикає гру.

## Поле і час
- Поле — шари (`layers`): клітини півплиткової сітки на кількох висотах; плитка верхнього шару може перекривати дві-чотири нижні (зсув на пів плитки) (?).
- Turtle — «four-layer pattern» за Wikipedia + вершина й бічні «крила» (?); інші розкладки: ox, snake, dragon тощо, різної складності.
- Видимість: верхні плитки видно, нижні частково або зовсім сховані → `info: partial`.
- Покрокова, хід = знята пара; таймер лише для рекорду (KMahjongg, KShisen) або в режимі на час.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка масті (крапки, бамбук, ієрогліфи) | tile | масть, номер 1–9, 4 копії | парується лише з ідентичною |
| Вітер (4 види) | tile | 4 копії кожного | парується з ідентичною |
| Дракон (3 види) | tile | 4 копії кожного | парується з ідентичною |
| Квітка (4 види) | tile | по 1 копії | будь-яка квітка парується з будь-якою квіткою |
| Сезон (4 види) | tile | по 1 копії | будь-який сезон з будь-яким сезоном |
| Вільна плитка | tile (стан) | — | нічого зверху і вільний лівий або правий бік → можна вибрати |
| Вибрана плитка | tile (стан) | — | підсвічена, чекає пару |
| Розкладка | zone | 144 місця по шарах (Turtle) | задає, хто кого блокує; редагується редактором |
| Підказка | — (ui `hint-marker`) | — | блимає вільна пара |

Склад: 3 масті × 9 × 4 = 108 + вітри 16 + дракони 12 + квіти 4 + сезони 4 = 144.

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click tile)` → ЯКЩО `custom: «free_tile — на плитці нема плитки вищого шару і вільний лівий або правий бік»` → ТО `set_state(tile, selected)`; інакше `block`.
- КОЛИ `input(click tile2)` → ЯКЩО `state(tile1, selected) and custom: «free_tile(tile2)» and same(tile1, tile2, face)` → ТО `disappear(tile1)`, `disappear(tile2)`, `custom: «відкрити сусідів і плитки знизу»`.
- КОЛИ `input(click tile2)` → ЯКЩО `same(tile1, tile2, group)` і група — квіти або сезони → ТО те саме, що для ідентичних.
- КОЛИ `input(click tile2)` → ЯКЩО `not same(tile1, tile2, face)` → ТО `clear_state(tile1, selected)`, `set_state(tile2, selected)` (перевибір) (?).
- КОЛИ `all_gone(tile)` → ТО `win`; рекорд — за часом (KMahjongg).
- КОЛИ `no_moves(player)` → ТО `lose`; у частині версій замість цього `custom: «reshuffle — перемішати плитки, що лишились, по тих самих місцях»`.
- КОЛИ `input(shuffle)` → ТО `custom: «reshuffle»` (KMahjongg — у будь-який момент).
- КОЛИ `input(hint)` → ТО `custom: «блимнути вільною парою»`, `set_state(game, hinted)`; КОЛИ `win` → ЯКЩО `state(game, hinted)` → ТО рекорд не зараховується.
- КОЛИ `input(undo)` → ТО `undo(1)`; `redo` — повернути.
- КОЛИ `level_start` → ЯКЩО `mode(solvable_only)` → ТО `custom: «генерувати лише розвʼязну розкладку»` (майже всі сучасні версії).
- Режим на час: КОЛИ `timer(<=, 0)` → ТО `lose` (ліміт залежить від кількості плиток).
- Перемога: знято всі 144 · Поразка: нема вільної пари · Рахунок: час (або пари/набори в змагальних варіантах).
- Складність: максимізувати ймовірність розчищення — PSPACE-повно; з «підгляданням» під плитки — NP-повно; ≈3 % роздач Turtle нерозвʼязні навіть із підгляданням (10 млн симуляцій).

## Керування і ввід
- Миша / тач: клік по плитці — вибір, клік по другій — спроба пари; гра сама знімає пару.
- Клавіші KMahjongg: Ctrl+N нова, F5 рестарт, P пауза, H підказка, D демо, Ctrl+Z / Ctrl+Shift+Z undo/redo, G / F — обертання кута огляду.

## Вікна, меню, HUD
- `game-screen`: розкладка з тінями шарів; `selection-highlight`; `hint-marker`; `timer-elapsed`; `remaining-counter` плиток / доступних пар (?); `custom: «removed-tiles»` — знята стопка (опція KMahjongg).
- Меню Game: New · Load / Save · New Numbered Game… (`custom: «seed»`) · Restart · Pause (усі плитки ховаються) · Show High Scores (`leaderboard`, топ-10, імʼя) · Board Editor (`editor-window`) · Quit.
- Меню Move: Undo · Redo · Hint · Demo (`attract-demo`) · Shuffle.
- Меню View: Rotate View CW / CCW.
- `settings-window`: блимати парами вибраної плитки · тільки розвʼязні · показувати зняті плитки · розкладка (`level-select` розкладок) · набір плиток і фон (`theme-select`).
- `end-screen`: перемога (Shanghai — частина екрана «обсипається» і показує дракона, що кліпає оком) / нема ходів.
- Переходи: main → game-screen → (усе знято / нема пар) end-screen → leaderboard → нова роздача.

## Фічі поза полем
- `seed-input` (нумерована гра), `save-slots` (Load/Save), `level-editor` розкладок, вибір розкладок, `theme-select` плиток і фону.
- `hint` (знімає з рекордів), `undo` / `redo`, `restart-level`, `custom: «reshuffle»`, `auto-solve` як Demo.
- `pause` з приховуванням поля (щоб не планувати на паузі), `leaderboard-local` за часом.
- Змагальні варіанти: партнерська / дуельна гра з очками за пари й набори; двогравцевий режим у Clubhouse Games: 51 Worldwide Classics.

## Варіації й родичі
- Mah-Jongg (Brodie Lockard, PLATO, 1981) → Shanghai (Activision, 1986, ~10 млн копій) → Shanghai II: Dragon's Eye (1990) та інші сиквели → Taipei (Microsoft Entertainment Pack, 1990) → Mahjong Titans (Windows Vista/7), KMahjongg, нескінченні вебклони.
- Родичі: Shisen-Sho (одна площина, пара зʼєднується шляхом), Memory (пари, але приховані), Triple-tile «Tile Match» мобільні (3 однакові в лоток (?)).
- **Осі варіацій**: розкладка (Turtle / інші / 3D-куб) · правило вільної (лівий-або-правий бік / будь-який бік) · набір (маджонг / квіти / самоцвіти) · спецплитки-джокери · генерація (випадкова / гарантовано розвʼязна) · допомога (shuffle при глухому куті / hint / undo) · час (рекорд / ліміт).

## Цікавинки для курсу
- Перевірка «вільна плитка» в шарах з півклітинковим зсувом — 📎.
- Детектор «є вільна пара?» і підказка — 🌱; shuffle лишків по тих самих місцях — 🌱.
- Розкладка з текстового файла (шар, x, y) + редактор — 🥉.
- Генератор гарантовано розвʼязної роздачі (будувати зворотно: розставляти пари на місця, що були б вільними) — 🥇.
- Розвʼязувач з пошуком (DFS із відсіканням, порядок однакових пар) — 🥇.
- Пауза, що ховає поле, і «hint знімає з рекордів» — 🌱 (правило чесності як стан).

## Мапа на каталог
- Є: `cell-click` · `selection-highlight` · `hover-highlight` · `height-levels` (шари) · `undo-redo` · `restart-level` · `game-pause` · `time-out` (режим на час) · `time-bonus` / `score-records` / `leaderboard` (рекорд за часом) · `no-moves-left` · `unsolvable-states` · `level-solver` · `seed-share` (нумерована гра) · `attract-demo` (Demo) · `in-game-editor` + `editor-window` · `save-game` · `theme-select` · `game-screen` · `end-screen` · `settings-window`.
- **Нема** → пропозиції карток:
  - `+pair-match-removal` «Зняти пару однакових» · entities/interact · 🌱 · слот {match: identical|group}.
  - `+free-tile-rule` «Вільна плитка в шарах» · entities/legality · 📎 · слот {sides: left-or-right|any}.
  - `+reshuffle-remaining` «Перемішати лишки на тих самих місцях» · levels/generation · 🌱.
  - `+solvable-deal` «Гарантовано розвʼязна роздача» · levels/generation · 🥇.
  - `+hint-pair` «Підказати доступну пару» · interface/hud · 🌱.
  - `+pause-hides-field` «Пауза ховає поле» · game-logic/difficulty · 🌱.

## Пропозиції до словників
- `+cond:free_tile` — плитка вільна: нема плитки зверху і відкритий лівий або правий бік (Mahjong; не те саме, що `free(cell)` — порожня клітина).
- `+effect:reshuffle` — перемішати сутності, що лишились, по зайнятих місцях (Mahjong; уже просили Bejeweled, Candy Crush).
- `+ui:removed-tiles` — стопка знятих плиток (KMahjongg).
- `+feature:hint-disqualifies` — використання підказки чи undo знімає результат із рекордів (KMahjongg, KShisen).
- Вжито вже наявні `same(..., group)`, `all_gone`, `no_moves`, `mode`, `hint-marker`, `seed-input`, `attract-demo`.

## Джерела
- ⭐ [Wikipedia: Mahjong solitaire](https://en.wikipedia.org/wiki/Mahjong_solitaire) — 144 плитки, «four-layer pattern», вільна = можна зсунути вліво/вправо, перемога/поразка, shuffle, undo, складність, варіанти, історія.
- [Wikipedia: Shanghai (video game)](https://en.wikipedia.org/wiki/Shanghai_(video_game)) — склад набору, квіти/сезони парують між собою, «at least one free vertical edge», кінець без ходів, сиквели.
- [KMahjongg: Rules](https://docs.kde.org/stable_kf6/en/kmahjongg/kmahjongg/rules.html) — вільна плитка, рекорд за часом, Hint дискваліфікує.
- [KMahjongg: Interface](https://docs.kde.org/stable_kf6/en/kmahjongg/kmahjongg/interface.html) — повне меню.
- [KMahjongg: Configuration](https://docs.kde.org/stable_kf6/en/kmahjongg/kmahjongg/configuration.html) — блимання пар, розвʼязні роздачі, показ знятих.

## Непевне
- (?) Геометрія Turtle (кількість шарів з вершиною, «крила», півплитковий зсув) — Wikipedia каже лише «four-layer pattern».
- (?) Перевибір другою неоднаковою плиткою — поведінка різниться між версіями.
- (?) Лічильник доступних пар у HUD — є в багатьох клонах, у KDE-доках не згадано.
- (?) Режими Shanghai (Challenge Match, Tournament) — стаття про Shanghai їх не описує.
- (?) Мобільні «Tile Match» з лотком на 7 і трійками — з памʼяті, як родич.
