---
title: Knotwords
slug: knotwords
family: word-number
also: [pencil-logic]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2022
platforms: [iOS, Android, Windows, macOS]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1963900/Knotwords/", best: true, note: "опис правил одним реченням, трейлер, дата 28.04.2022, автори"}
  - {kind: play, url: "https://play.google.com/store/apps/details?id=com.noodlecake.knotwords", note: "Android-версія (видавець Noodlecake)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Zach_Gage", note: "автор; Knotwords у списку робіт (2022)"}
  - {kind: other, url: "https://en.wikipedia.org/wiki/Canadian_Game_Awards", note: "Knotwords (Gage & Schlesinger) у категорії Best Mobile/Casual Game"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=knotwords+zach+gage+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [cell-click, keyboard-controls, satisfy-constraints, markup-validity, completion-detection, daily-puzzle, level-bank, profile-stats, end-screen, game-screen, help-window, settings-window, save-progress, +word-validation, +region-letter-pool, +crossword-runs, +hint-meter, +streak-stats, +share-result]
proposes: ["+trigger:input", "+trigger:all_constraints_met", "+cond:in_dictionary", "+cond:in_pool", "+effect:mark", "+effect:unmark", "+role:mark", "+role:zone", "+ui:region-letter-pool", "+ui:conflict-highlight", "+window:puzzle-select", "+window:daily-window", "+feature:hint", "+feature:puzzle-bank", "+axis:session"]
author: opus
date: 2026-11-02
---

# Knotwords — кросворд без підказок: кожен регіон дає рівно свої літери, кожен ряд і стовпець мусить бути словом

## Суть
Поле — фігурна кросвордна сітка, розбита товстими межами на регіони; у кожному регіоні написано мультимножину літер, яку треба розкласти саме в його клітини. Мета — щоб кожен горизонтальний і вертикальний відрізок з ≥2 літер став дійсним словом. Визначень-підказок нема: замість «що за слово» гравець думає «які літери куди», тож це судоку-логіка з алфавітом замість цифр (Steam: «minimal and elegant logic puzzle — with words»). Автор наголошує, що пазл «стає легшим, що далі просуваєшся» — кожне вписане слово звужує сусідів.

## Поле і час
- Квадратна сітка довільної форми (не обовʼязково прямокутник): є «порожнеча» поза полем і чорні клітини-розриви (?), тож слова мають різну довжину.
- Шари: клітини + регіони (`zone`) з пулом літер + літери, вписані гравцем.
- Час статичний; на екрані — лише секундомір (?). Розмір пазлів від маленьких 4×4-подібних до більших (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина | mark | літера або порожньо | гравець вписує/стирає літеру з пулу свого регіону |
| Регіон (knot) | zone | множина клітин, пул літер (мультимножина), \|пул\| = \|клітини\| | дає лише свої літери; пул показує, які ще не використані |
| Відрізок-слово (run) | static | горизонтальний/вертикальний, довжина ≥ 2 | заповнений → перевірка за словником |
| Межа поля / розрив | static | — | обриває відрізок |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(select cell)` → ТО `custom: «клавіатура показує лише літери пулу регіону цієї клітини»`.
- КОЛИ `input(letter)` → ЯКЩО `in_pool(region, letter)` → ТО `mark(cell, letter)`, `custom: «літера в пулі позначається використаною»`; інакше `block`.
- КОЛИ `input(erase)` → ТО `unmark(cell)`, літера повертається в пул.
- КОЛИ `pattern(run_full)` → ЯКЩО `not in_dictionary(run)` → ТО `custom: «відрізок підсвічено як недійсне слово»` (`conflict-highlight`) (?).
- КОЛИ `custom: «усі клітини заповнені»` → ЯКЩО `all_constraints_met` (кожен run — слово, кожен пул вичерпано) → ТО `win`, `window(end-screen)`.
- Пул регіону рівно відповідає його клітинам: використати іншу літеру чи залишити клітину порожньою неможливо — це й є головне обмеження поряд зі словником.
- Однорядкові «слова» з 1 літери не перевіряються (?).
- Розвʼязок задуманий єдиним; перевірка ведеться за правилами (будь-яке дійсне заповнення зараховується) (?).
- Перемога: усі відрізки — слова · Поразки нема · Рахунок: час / використані підказки (?).

## Керування і ввід
- Тап по клітині → вибір; літера — з екранної «клавіатури» пулу регіону або фізичної клавіатури на ПК (?).
- Повторний тап / перетягування літери між клітинами регіону — перестановка (?).
- Режим «олівця» нема — неоднозначність тримають у голові (?).

## Вікна, меню, HUD
- `game-screen`: сітка з товстими межами регіонів, пули літер у кутах регіонів (`region-letter-pool`), підсвітка недійсних слів, кнопка підказки (?).
- `daily-window` / `puzzle-select`: щоденні пазли і місячна «книжка» пазлів (?).
- `end-screen`: розвʼязана сітка, час, серія (?).
- `settings-window`: перевірка слів увімк/вимк, тема (?).
- `help-window`/`tutorial-window`: інтерактивне навчання на перших пазлах (?).
- Переходи: головна → daily / книжка → `game-screen` → `end-screen`.

## Фічі поза полем
- `daily-puzzle`: щоденні пазли (безкоштовно) (?).
- `puzzle-bank`: щомісячна книжка пазлів за підпискою / покупкою (?).
- `hint`: кілька видів підказок — від «показати недійсні слова» до «відкрити літеру» (?).
- `stats`/`streaks`, `achievements` (Steam Achievements), `cloud-save` (Steam Cloud).

## Варіації й родичі
- Кросворд (сітка слів без підказок), Scrabble (мультимножина літер), судоку/Kakuro (регіони з фіксованим набором), «кросворд-скелет» (fill-in, word-fit) — найближчий паперовий родич: там дано список слів, тут — літери регіонів.
- Інші ігри Gage/Schlesinger: SpellTower, Typeshift (колонки-барабани з літерами), Good Sudoku.
- **Осі варіацій:** що дано (список слів / пул літер регіону / нічого, лише форма) · межі регіонів (1 клітина = звичайний кросворд з даними літерами / ряд / довільна форма) · перевірка (миттєва / лише в кінці) · словник (загальний / тематичний).

## Цікавинки для курсу
- Валідатор: витягнути всі горизонтальні й вертикальні відрізки ≥2 з сітки довільної форми й перевірити словником — 🌱.
- Пул літер регіону як мультимножина (`Counter`) з поверненням при стиранні — 🌱.
- Розвʼязувач: backtracking по регіонах із відсіченням префіксів за trie («цей недописаний run — ще префікс якогось слова?») — 🥇.
- Генератор пазла з єдиним розвʼязком (заповнити сітку словами, поділити на регіони, перевірити унікальність солвером) — 👑.
- Підказки рівнями (показати конфлікт → показати клітину) — 📎.

## Мапа на каталог
- Є: `cell-click` · `keyboard-controls` ↔ вписування літер · `satisfy-constraints` ↔ усі run-и — слова · `markup-validity` ↔ підсвітка недійсних · `completion-detection` · `daily-puzzle` · `level-bank` ↔ книжки пазлів · `profile-stats` · `save-progress` · `end-screen` · `game-screen` · `help-window` · `settings-window`.
- **Нема** → пропозиції карток:
  - `+word-validation` — див. wordle.md.
  - `+region-letter-pool` «Регіон з пулом літер/цифр, які треба розкласти» · game-logic/constraints · 📎 · слоти {pool: multiset}.
  - `+crossword-runs` «Усі горизонтальні й вертикальні відрізки мусять бути словами» · game-logic/constraints · 🥉 · слоти {min_len: 2}.
  - `+hint-meter` — див. nyt-connections.md (тут — рівні підказок).
  - `+streak-stats`, `+share-result` — див. wordle.md.

## Пропозиції до словників
- `+trigger:input`; `+trigger:all_constraints_met` (⏳) — фінальна перевірка.
- `+cond:in_dictionary`; `+cond:in_pool` — літера ще є в пулі регіону.
- `+effect:mark` / `+effect:unmark` (⏳).
- `+role:mark` (⏳) — літера в клітині; `+role:zone` (⏳) — регіон з пулом.
- `+ui:region-letter-pool` — набір літер у куті регіону, використані тьмяніють; `+ui:conflict-highlight` (⏳).
- `+window:puzzle-select` (⏳), `+window:daily-window` (⏳).
- `+feature:hint`, `+feature:puzzle-bank` (⏳).
- `+axis:session` — `daily` + `level`.

## Джерела
- ⭐ [Steam: Knotwords](https://store.steampowered.com/app/1963900/Knotwords/) — правила одним реченням, трейлер, дата, Zach Gage і Jack Schlesinger, досягнення, Steam Cloud.
- [Google Play: Knotwords](https://play.google.com/store/apps/details?id=com.noodlecake.knotwords) — Android (Noodlecake).
- [Wikipedia: Zach Gage](https://en.wikipedia.org/wiki/Zach_Gage) — автор, список робіт (Knotwords 2022, SpellTower, Puzzmo).
- [Wikipedia: Canadian Game Awards](https://en.wikipedia.org/wiki/Canadian_Game_Awards) — Knotwords у категорії Best Mobile/Casual Game.
- YouTube: пошук «knotwords zach gage gameplay».

## Непевне
- Окремої статті Wikipedia нема; офіційний сайт knotwords.com не резолвився, Thinky Games віддав 403, WebSearch вичерпано — правила понад «arrange the letters in each section so every word is valid, across and down» записані з памʼяті.
- (?) Види підказок, «книжка пазлів» щомісяця, модель монетизації, наявність секундоміра.
- (?) Підсвітка недійсних слів — автоматична чи вмикається в налаштуваннях.
- (?) Чорні клітини всередині поля vs. лише фігурний контур; чи гарантована єдиність розвʼязку.
- (?) Перемога в Canadian Game Awards чи лише номінація — сніпет показує назву в категорії.
