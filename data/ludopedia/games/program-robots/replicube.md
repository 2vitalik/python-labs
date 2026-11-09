---
title: Replicube
slug: replicube
aka: ["Picross 3D but with coding"]
family: program-robots
also: []
klass: puzzle
axes:
  field: 3d
  time: static
  opponent: none
  info: full
  random: none
  goal: state
year: 2025
platforms: [PC (Windows, macOS, Linux/SteamOS)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3401490/Replicube/", best: true, note: "опис: код на Lua відтворює воксельний обʼєкт, 2 лідерборди (розмір коду й ефективність), free edit, 2D-редактор, форум, експорт"}
  - {kind: official, url: "https://www.walaber.com/replicube", note: "сторінка розробника: «нема правильної відповіді — якщо код дає той самий обʼєкт, він правильний», експорт у MagicaVoxel"}
  - {kind: other, url: "https://www.walaber.com/replicube-press-kit", note: "прес-кіт: Lua, OS/2-подібний «віртуальний OS», дата 24.04.2025, ціна"}
  - {kind: other, url: "https://github.com/Kartones/replicube-game-solutions", note: "розвʼязки гравця з метриками Code size і Cycles/voxel у шапці кожного файла; coding.md — як рахуються інструкції"}
  - {kind: other, url: "https://blog.kartones.net/post/replicube-and-other-programming-videogames/", note: "огляд: підмножина Lua 5.3, булеві й бітові оператори, власні функції, print() для налагодження"}
  - {kind: other, url: "https://hn.svelte.dev/item/44535202", note: "обговорення HN: код з x, y, z, t, метрики «code size 118, 19.82 cycles per voxel»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Replicube+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [code-editor-window, help-window, puzzle-select, leaderboard, satisfy-constraints, completion-detection, user-procedures, level-exchange, tutorial-window, +real-language-code, +code-describes-field, +per-cell-function, +voxel-3d-target, +reference-replication, +palette-index-colors, +code-size-metric, +cycles-per-cell-metric, +percentile-leaderboard, +free-edit-sandbox, +code-generated-images, +community-forum-challenges, +os-desktop-ui, +optional-restriction-challenges]
proposes: ["+effect:eval_per_cell(code)", "+cond:matches_reference", "+feature:solution-metrics", "+window:metric-histograms", "+window:community-forum", "+window:image-code-editor", "+window:os-desktop", "+ui:code-metrics", "+feature:custom-wallpaper"]
author: opus
date: 2026-11-09
---

# Replicube — пишеш не програму для робота, а функцію від (x, y, z), що повертає колір кожного вокселя, і так відтворюєш 3D-обʼєкт

## Суть
Гра-іграшка Walaber (2025): дано еталонний воксельний обʼєкт, треба написати Lua-код, який його відтворить. Код не керує агентом і не має часу — він **описує поле**: для кожної клітини куба виконується той самий фрагмент з координатами `x, y, z`, і повернене число — номер кольору (0 / нічого = порожньо). Правильних відповідей безліч: зараховується будь-який код, що дає той самий обʼєкт, а змагання — у двох лідербордах: найкоротший код і найменше циклів на воксель. Девіз із прес-кіту — «Picross 3D, але з кодом».

## Поле і час
- Поле — невеликий воксельний куб (`field: 3d`) з координатами, центрованими в 0 (у розвʼязках є відʼємні `x, y, z`, напр. −3…3); точний розмір — у «Непевне».
- Шари: еталонний обʼєкт (ціль) + обʼєкт, згенерований кодом гравця.
- Часу нема (`time: static`): запуск = обчислити функцію для всіх вокселів, порівняти з еталоном. В анімованих задачах і 2D-редакторі є номер кадру `t` (?).
- Повна інформація, жодної випадковості: еталон видно цілком, перевірка детермінована.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Воксель | mark | (x, y, z), колір | отримує колір з результату коду; 0 / nil — порожній |
| Еталонний обʼєкт | zone | набір кольорових вокселів | ціль: згенероване має збігтися повністю |
| Код гравця | — (програма) | текст Lua, code size, cycles/voxel | виконується окремо для кожного вокселя з `x, y, z` |
| Колір палітри | — (значення) | номер (у розвʼязках 1…15) і константи `EMPTY`, `RED`, `GREEN`, `YELLOW`, `PURPLE`, `PEACH` | номер, який повертає код |
| Вбудовані функції | — | `abs`, `inrange`, математика Lua, `print` | доступні в коді; власні допоміжні функції дозволені |
| Лідерборд пазла | — | code size, cycles per voxel | дві окремі таблиці, часто суперечать одна одній |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(run)` → ТО `custom: «для кожного вокселя куба виконати код з x, y, z»`.
- КОЛИ `custom: «код повернув число c»` → ЯКЩО `custom: «c ≠ 0»` → ТО `paint(voxel, c)`; ЯКЩО `custom: «0, nil або нічого не повернуто»` → ТО `custom: «воксель порожній»` (неявне повернення = 0).
- КОЛИ `custom: «код повернув булеве»` → ТО `custom: «true зафарбовує вокселем (див. Непевне), false — порожньо»`.
- КОЛИ `custom: «помилка Lua під час виконання»` → ТО `crash`.
- КОЛИ `exec(print)` → ТО `message(value)` у консоль налагодження.
- КОЛИ `all_constraints_met` (усі воксели збіглися з еталоном) → ТО `win`, `custom: «записати code size і cycles/voxel у два лідерборди»`.
- КОЛИ `custom: «є розбіжність з еталоном»` → ТО `custom: «пазл не зараховано»` (як саме показується розбіжність — у «Непевне»).
- Code size: КОЛИ `custom: «оголошено змінну через local»` → ТО `counter(code_size, +1)`; кожна пара дужок → `counter(code_size, +1)`; ланцюг if-elseif на 1 інструкцію дешевший за два окремі if.
- Cycles: КОЛИ `custom: «змінну оголошено без local»` → ТО `counter(cycles, +k)` замість розміру; метрика — середня кількість циклів на воксель.
- КОЛИ `custom: «пазл має додаткове обмеження (напр. без жодного if)»` → ЯКЩО `custom: «код його порушує»` → ТО `custom: «челендж не зараховано»` (заплановано розробником (?)).
- Поразки нема; рахунок — лише метрики коду.

## Керування і ввід
- Текстовий редактор коду (Lua): пишеш тіло функції, запускаєш, дивишся результат поруч з еталоном.
- Обертання / масштаб 3D-переглядача обʼєкта (?).
- Free edit: той самий воксельний інструмент без еталона — для власних моделей.
- 2D-редактор: код генерує зображення й GIF-анімації.

## Вікна, меню, HUD
- `+window:os-desktop` — інтерфейс у стилі ранніх графічних ОС (OS/2): вікна-програми на робочому столі; фоном можна поставити власне 2D-творіння (`+feature:custom-wallpaper`).
- `puzzle-select` — набори пазлів (навчальні проєкти, вступні челенджі, тематичні набори (?)), позначки розвʼязаних.
- `code-editor` — редактор Lua з `+ui:code-metrics` (code size, cycles/voxel).
- `game-screen` — 3D-переглядач: еталон і згенерований обʼєкт.
- `help-window` — вбудована документація (скриншот «docs» на сайті розробника).
- `leaderboard` / `+window:metric-histograms` — дві таблиці на пазл; гравці орієнтуються на перцентилі (напр. «нижче 80-го перцентиля за розміром»).
- `+window:community-forum` — внутрішньоігровий форум: діляться творіннями й кидають виклик відтворити.
- `+window:image-code-editor` — 2D-редактор зображень/GIF кодом.
- Переходи: робочий стіл → набір пазлів → пазл (редактор + переглядач) → результат і лідерборди → наступний пазл; робочий стіл → free edit / 2D-редактор / форум.

## Фічі поза полем
- `mode-sandbox` — free edit без еталона.
- `export-import` — експорт 3D у формат MagicaVoxel (.vox), 2D — у PNG / GIF.
- `leaderboard-online` — два лідерборди на пазл; `+feature:solution-metrics` — розмір коду та ефективність як рахунок.
- `level-sharing` — форум з творіннями гравців як користувацькі пазли.
- Безкоштовне демо, Steam Cloud; ціна $9.99.

## Варіації й родичі
- Родичі в корпусі: `tis-100`, `exapunks`, `opus-magnum` (Zachlike-гістограми й метрики розвʼязку), `human-resource-machine` (розмір і швидкість програми як два рекорди), `befunge` і `markov-alg` (програма, що працює над полем, а не агентом).
- Межа сімʼї: агента нема — програма є «шейдером» поля; найближче до `pencil-logic` за метою (відтворити картинку, як Picross), але засоби — код.
- Осі варіацій: **що описує програма** (агента — Karel / поле поклітинно — Replicube / потік даних — TIS-100); **метрика** (розмір / цикли / площа); **еталон** (точний обʼєкт / вільна творчість).

## Цікавинки для курсу
- Поле як функція f(x, y, z) → колір: студент пише генератор рівня однією формулою — 📎.
- Перевірка збігу з еталоном поклітинно + звіт розбіжностей — 🌱.
- Метрики коду: підрахунок «інструкцій» (токенів) і середніх циклів на клітину — 🥈 (потрібен інтерпретатор / лічильник).
- Дві суперечливі метрики й гістограма-перцентиль гравців — 🥉.
- Пісочниця з експортом у відкритий формат (.vox / PNG) — 📎.
- Обмеження-челенджі («без if») як модифікатор пазла — 📎.

## Мапа на каталог
- Є: `code-editor-window` · `help-window` (документація) · `puzzle-select` · `leaderboard` · `satisfy-constraints` / `completion-detection` (збіг з еталоном) · `user-procedures` (власні функції Lua) · `level-exchange` (форум творінь) · `tutorial-window` (навчальні проєкти).
- **Нема** → пропозиції карток:
  - `+code-describes-field` «Програма описує поле, а не агента» · game-logic/program · 📎.
  - `+per-cell-function` «Та сама функція виконується для кожної клітини з координатами» · game-logic/program · 📎.
  - `+voxel-3d-target` «Ціль — 3D-воксельний обʼєкт» · interface/render · 🥈.
  - `+reference-replication` «Відтворити еталон точно» · game-logic/win · 🌱.
  - `+palette-index-colors` «Колір як індекс палітри, 0 = порожньо» · interface/render · 🌱.
  - `+code-size-metric` «Рахунок — розмір коду в інструкціях» · score · 🥉.
  - `+cycles-per-cell-metric` «Рахунок — середні цикли на клітину» · score · 🥈.
  - `+percentile-leaderboard` «Лідерборд як розподіл / перцентиль» · interface/menus · 🥉.
  - `+free-edit-sandbox` «Пісочниця без цілі тим самим інструментом» · levels/editor · 📎.
  - `+code-generated-images` «Код генерує 2D-зображення / GIF» · interface/render · 📎.
  - `+community-forum-challenges` «Гравці викладають творіння як виклики» · levels/editor · 🥈.
  - `+os-desktop-ui` «Інтерфейс як робочий стіл ОС з вікнами» · interface/menus · 🥉.
  - `+optional-restriction-challenges` «Додаткове обмеження на розвʼязок (без if)» · game-logic/constraints · 📎.

## Пропозиції до словників
- `+effect:eval_per_cell(code)` — виконати код для кожної клітини поля.
- `+cond:matches_reference` — поле збігається з еталоном.
- `+feature:solution-metrics` — метрики розвʼязку як рахунок (також TIS-100, Opus Magnum).
- `+window:metric-histograms` — гістограми / перцентилі метрик гравців.
- `+window:community-forum` — внутрішньоігровий форум творінь.
- `+window:image-code-editor` — редактор зображень кодом.
- `+window:os-desktop` — меню як робочий стіл з вікнами.
- `+ui:code-metrics` — панель розміру коду й циклів.
- `+feature:custom-wallpaper` — власне творіння як фон інтерфейсу.

## Джерела
- ⭐ [Steam: Replicube](https://store.steampowered.com/app/3401490/Replicube/) — опис, 2 лідерборди, free edit, 2D-редактор, форум, експорт, дата, платформи.
- [Walaber: Replicube](https://www.walaber.com/replicube) і [прес-кіт](https://www.walaber.com/replicube-press-kit) — Lua, «нема правильної відповіді», OS/2-подібний інтерфейс, MagicaVoxel.
- [GitHub: Kartones/replicube-game-solutions](https://github.com/Kartones/replicube-game-solutions) — реальні розвʼязки з метриками (напр. `return 7` — code size 2, 3.0 cycles/voxel; `if y > 0 then return 12 end return 8`); `coding.md` — правила підрахунку інструкцій.
- [Kartones: Replicube and other programming videogames](https://blog.kartones.net/post/replicube-and-other-programming-videogames/) — підмножина Lua 5.3, оператори, функції, `print()`.
- [HN: обговорення](https://hn.svelte.dev/item/44535202) — код з `x, y, z, t`, константи кольорів, значення метрик.
- YouTube: пошук «Replicube gameplay».

## Непевне
- (?) Розмір куба (у розвʼязках координати до ±3, згадано змінну `extent`) і кількість кольорів палітри (у розвʼязках номери 1…15) — точно не знайдено.
- (?) Розвʼязок `return -x == y` повертає булеве; як гра фарбує `true` (ймовірно, колір 1) — не підтверджено.
- (?) Змінна `t` (номер кадру) і анімовані пазли: є в коді з обговорення HN і в `coding.md` (`t`, `frames`), але чи це основна гра чи веб-челендж — не з'ясовано.
- (?) Чи підсвічує гра розбіжні воксели та як керується 3D-переглядач — не знайдено.
- (?) Назви наборів пазлів («tutorial projects», «intro challenges», «Alice creations») — з назв тек у репозиторії гравця.
- (?) Обмеження-челенджі («без жодного if») — у відповіді розробника як план; чи додано — не перевірено.
- (?) Мови: прес-кіт — лише англійська, Steam — англійська і ще 13.
