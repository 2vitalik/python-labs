---
title: A=B
slug: a-equals-b
aka: [A = B, "A=B (Artless Games)"]
family: program-robots
also: [word-number]
klass: cursor
axes:
  field: 1d
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2022
platforms: [PC (Windows, Steam)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1720850/", best: true, note: "Artless Games, 29.03.2022; єдина інструкція A=B; мінімум рядків; редактор рівнів, Workshop, мінігра"}
  - {kind: wiki, url: "https://esolangs.org/wiki/A%3DB", note: "специфікація мови: порядок правил, перше входження, ключові слова (return)/(start)/(end)/(once) зі світами"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=3441284586", note: "гайд найкоротших розвʼязків: усі глави й рівні, ліміти 255 символів і 100000, рекорди рядків"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=2967327695", note: "трюки: керівні символи, сортування, унарна арифметика, рівні без ключових слів"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=2791056593", note: "правила вбудованої мінігри Pangu Project (кубики, колонія на Марсі)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=A%3DB+game+artless+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [command-program, sequential-levels, in-game-editor, level-exchange, +string-rewrite-rule, +io-test-streams, +solution-metrics, +workshop-sharing, +keyword-unlock-by-chapter, +anchored-rewrite, +halt-with-output, +once-rule, +step-and-length-limits, +bonus-minigame]
proposes: ["+effect:rewrite(a, b)", "+effect:halt", "+cond:anchored(a, start|end)", "+feature:keyword-unlock", "+ui:line-counter", "+card:string-rewrite-rule", "+card:anchored-rewrite", "+card:keyword-unlock-by-chapter", "+card:halt-with-output"]
author: opus
date: 2026-11-09
---

# A=B — мова з однією інструкцією «замінити A на B»: гравець пише впорядковані правила підстановки, які перетворюють вхідний рядок на потрібний вихід

## Суть
Зачлайк-головоломка від Artless Games: кожен рівень — задача над рядком (усі літери у верхній регістр, відсортувати, перевірити паліндром, помножити два двійкові числа), а програма — список рядків `A=B`. Інтерпретатор щокроку бере перше зверху правило, ліва частина якого входить у рядок, і замінює перше входження; коли жодне не підходить — рядок і є відповіддю. Це нормальний алгоритм Маркова з кількома ключовими словами, які відкриваються по главах. Виклик — розвʼязати однією мінімальною кількістю рядків.

## Поле і час
- «Поле» — один рядок ASCII-символів (1D); на рівні кілька тест-кейсів «вхід → очікуваний вихід».
- Тік = одна підстановка; після неї пошук знову з першого правила (`time: programmed`).
- Ліміти: довжина рядка 255 символів, ліміт часу 100000 (кроків (?)); розвʼязки «unbounded-input» мусять працювати й поза ними.
- Коментарі `#` і порожні рядки — не рахуються як рядки коду.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Робочий рядок | object | ≤ 255 ASCII-символів | на старті = вхід тест-кейсу; змінюється підстановками |
| Правило `A=B` | mark | ліва A, права B (будь-яка, B може бути порожня) | замінює перше входження A на B |
| `A=(return)B` | mark | B — відповідь | спрацювало → програма зупиняється, вихід = B (світ 2) |
| `(start)A=B` / `(end)A=B` | mark | якір | A шукається лише на початку / в кінці рядка (світ 3) |
| `A=(start)B` / `A=(end)B` | mark | — | A видаляється, B дописується на початок / в кінець рядка (світ 3) |
| `(once)A=B` | mark | — | правило спрацьовує щонайбільше раз за запуск (світ 4) |
| Керівний символ | object | символ, якого нема у вході й виході | «маркер», що ходить рядком і стирається наприкінці (прийом гравців) |
| Тест-кейс | zone | вхід, очікуваний вихід | програма має пройти всі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(run)` → ТО `custom: «робочий рядок = вхід тест-кейсу; лічильник кроків = 0»`.
- КОЛИ `tick` → ЯКЩО `custom: «знайдено перше зверху правило, чия A входить у рядок (з урахуванням якорів і once)»` → ТО `custom: «перше (найлівіше) входження A замінюється на B»`, `counter(steps, +1)`.
- КОЛИ `exec(rule)` → ЯКЩО `custom: «правило (start)A=B»` and `custom: «A — префікс рядка»` → ТО `custom: «префікс A → B»`; `(end)` — так само для суфікса.
- КОЛИ `exec(rule)` → ЯКЩО `custom: «права частина (start)B / (end)B»` → ТО `custom: «A вирізається, B вставляється на початок / в кінець»` — так символи «їздять» рядком.
- КОЛИ `exec(rule)` → ЯКЩО `custom: «правило (once)»` and `not first_time` → ТО `block` — правило пропускається.
- КОЛИ `exec(rule)` → ЯКЩО `custom: «права частина (return)B»` → ТО `custom: «вихід = B»`, `custom: «зупинка програми»`.
- КОЛИ `program_end` → ТО `custom: «вихід = поточний рядок»` — жодне правило не застосовне.
- КОЛИ `program_end` → ЯКЩО `same(output, expected, text)` → ТО `custom: «наступний тест-кейс»`; інакше `message(«хибний вихід»)` (?).
- КОЛИ `all_constraints_met` → ТО `win`, `custom: «записати кількість рядків»`.
- КОЛИ `counter(length, >, 255)` → ТО `crash`.
- КОЛИ `counter(steps, >, 100000)` → ТО `crash` — нескінченний цикл (як у truth-machine `1=11`).
- Перемога: усі тест-кейси дали очікуваний вихід · Поразка: нема — правиш програму · Рахунок: кількість рядків коду (рекорди виду «1/1», виклик «найменше рядків»).

## Керування і ввід
- Текстовий редактор програми: один рядок = одне правило; ключові слова пишуться в дужках прямо в тексті.
- Запуск на тест-кейсах; покрокове виконання й показ проміжних рядків — (?).
- Вхід — лише ASCII, крім коментарів.

## Вікна, меню, HUD
- `chapter-select`: глави 1–6 і Workshop-набори (напр. «Kazuei's Problems», k-1…k-12).
- `game-screen` + `code-editor`: умова задачі, приклади вхід/вихід, редактор правил, лічильник рядків (?).
- `custom-window` — вбудована мінігра Pangu Project.
- `end-screen`: рівень розвʼязано, кількість рядків (?).
- `achievements-window` — через Steam (18 досягнень).

## Фічі поза полем
- Глави: 1 «A=B» (6 рівнів), 2 «Keyword» (9, відкриває `(return)`), 3 «Start and End» (7), 4 «Once Upon A Time» (16), 5 «Math» (6: Count, A+1, A+B, A−B, A*B, A/B), 6 «Aftermath» (3, рівні без ключових слів).
- `level-editor` і Steam Workshop: гравці публікують власні задачі.
- Steam Cloud, 18 досягнень (серед них «Best the professor» (?)), мови EN / 简体 / 繁體 / 日本語.
- Мінігра **Pangu Project**: соло-гра з кубиками про колонію на Марсі — 10 раундів, 4 кубики на раунд, креслення й модифікатори M.O.D.; мета — збудувати 3 проєкти.

## Варіації й родичі
- [markov-alg](markov-alg.md) — інша гра (Fewjix, 2019): правила `"A" to "B"` лежать прямо на 2D-полі й переписують себе; A=B — «чистий» 1D-варіант без аватара.
- Мова-основа — нормальні алгоритми Маркова, есолангова «///» (теж лише заміна); родичі за жанром — [human-resource-machine](human-resource-machine.md), [tis-100](tis-100.md), [stack-machines](stack-machines.md).
- Від тих самих авторів — Understand (за Esolang wiki).
- **Осі варіацій:** якорі (нема / start-end) · вихід (весь рядок / `return`) · одноразові правила (`once`) · одновимірний рядок / 2D-поле символів · оцінка (рядки / кроки).

## Цікавинки для курсу
- Інтерпретатор A=B: перше застосовне правило, перше входження, повтор з початку — 🌱.
- Ключові слова `(start)/(end)` з обох боків і `(once)/(return)` — 📎.
- Тест-раннер: усі кейси, ліміти довжини й кроків, діагностика першої розбіжності — 📎.
- Детектор зациклення замість голого ліміту кроків (повтор стану рядка) — 🥉.
- Пошук найкоротшої програми перебором для простих рівнів — 🥇.
- Редактор рівнів: задача = генератор тест-кейсів + еталонний розвʼязок — 🥉.

## Мапа на каталог
- Є: `command-program` (список правил виконується після запуску) · `sequential-levels` (лінійні глави) · `in-game-editor` (редактор рівнів) · `level-exchange` (Workshop).
- **Нема** → пропозиції карток:
  - `+string-rewrite-rule` — підтвердження (Markov Alg).
  - `+anchored-rewrite` «Правило діє лише на початку/кінці рядка або переносить туди результат» · game-logic/program · 📎.
  - `+halt-with-output` «Правило зупиняє програму й задає відповідь» · game-logic/program · 🌱.
  - `+once-rule` «Правило спрацьовує раз за запуск» · game-logic/program · 🌱.
  - `+keyword-unlock-by-chapter` «Нові конструкції мови відкриваються главами» · levels/progression · 🌱.
  - `+step-and-length-limits` «Ліміти кроків і довжини стану як аварія програми» · game-logic/program · 🌱.
  - `+bonus-minigame` «Вбудована окрема гра» · interface/menus · 🥉.
  - `+io-test-streams`, `+solution-metrics`, `+workshop-sharing` — підтвердження.

## Пропозиції до словників
- `+effect:rewrite(a, b)` — замінити входження A на B (підтвердження з Markov Alg).
- `+effect:halt` — програма зупиняється з результатом (підтвердження з Turing Complete).
- `+cond:anchored(a, start|end)` — входження на початку / в кінці рядка.
- `+feature:keyword-unlock` — нові слова мови відкриваються прогресом.
- `+ui:line-counter` — лічильник рядків програми як оцінка.
- `+card:string-rewrite-rule`, `+card:anchored-rewrite`, `+card:keyword-unlock-by-chapter`, `+card:halt-with-output` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: A=B](https://store.steampowered.com/app/1720850/) — Artless Games, 29.03.2022 (ранній доступ з 15.11.2021); «only one instruction: A=B»; мінімум рядків; редактор рівнів, Workshop, 18 досягнень, мінігра.
- [Esolang wiki: A=B](https://esolangs.org/wiki/A%3DB) — перше застосовне правило, перше входження, зупинка без застосовних правил; таблиця ключових слів зі світами; коментарі `#`; Turing-повнота.
- [Гайд найкоротших розвʼязків](https://steamcommunity.com/sharedfiles/filedetails/?id=3441284586) — повний список глав і рівнів, ліміти 255 і 100000, оцінка рядками.
- [Tricks and Hints](https://steamcommunity.com/sharedfiles/filedetails/?id=2967327695) — керівні символи, переміщення на початок/кінець, унарна арифметика, глава 6 без ключових слів.
- [Pangu Project (JA)](https://steamcommunity.com/sharedfiles/filedetails/?id=2791056593) — правила мінігри (сторінку гайда знято, вміст із кешу).

## Непевне
- (?) Тест-кейси фіксовані чи генеруються випадково (`random: none` — припущення).
- (?) Ліміт 100000 — кроків підстановки чи інша одиниця «часу».
- (?) Як збігається порожня ліва частина (`=(return)Hello, world!`, `(once)=hello`) — найімовірніше на початку рядка.
- (?) Чи можна поєднувати ключові слова в одному рядку; чи `(return)`/`(once)` бувають з іншого боку.
- (?) Інтерфейс: покроковий режим, підсвітка правила, вигляд екрана результату — описів не знайдено.
- (?) Умова досягнення «Best the professor» — ймовірно, перемогти еталон «професора» за кількістю рядків.
