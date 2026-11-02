---
title: LOK Digital
slug: lok-digital
family: thinky
also: [word-number, pencil-logic]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: state
year: 2024
platforms: [PC, Mac, Linux, iOS, Android, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/LOK_Digital", best: true, note: "суть: слова чорнять клітини, LOK = 3+1, TLAK = 4+2, X як вільна літера, підказки, daily; історія книжки"}
  - {kind: official, url: "https://lok-digital.com/", note: "офіційний сайт, лінки на всі магазини і пресkit"}
  - {kind: other, url: "https://lok-digital.com/presskit", note: "пресkit: 15 світів, 150+ пазлів, daily з лідербордом"}
  - {kind: steam, url: "https://store.steampowered.com/app/2207440/LOK_Digital/", note: "демо, 14 мов"}
  - {kind: play, url: "https://draknek.itch.io/lok-digital", note: "itch.io: доступність (colorblind, high-contrast, one-button), редактор на PC"}
  - {kind: other, url: "https://www.letibus.com/lok", note: "паперова книжка LOK Блажа Урбана Грацара — першоджерело"}
  - {kind: other, url: "https://www.pocketgamer.com/lok-digital/review/", note: "огляд: як складати слова, TA і TLAK, книжка слів у рівні"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=LOK+Digital+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [cell-click, hover-highlight, satisfy-constraints, completion-detection, markup-validity, sequential-levels, level-unlock, level-select, daily-puzzle, leaderboard, in-game-editor, help-window, settings-window, save-progress, +undo-redo, +world-map, +word-as-command, +word-path-select, +letter-wildcard, +rule-teaching-by-example, +post-word-action, +color-by-letter-flood, +hint-solution-steps]
proposes: ["+trigger:input", "+trigger:word_spelled", "+cond:in_dictionary", "+cond:free_path", "+effect:mark", "+effect:choose", "+effect:set_cell", "+role:mark", "+role:word", "+window:map-window", "+window:codex-window", "+window:daily-window", "+ui:word-book", "+feature:undo", "+feature:daily-puzzle", "+feature:world-map", "+axis:rules"]
author: opus
date: 2026-11-02
---

# LOK Digital — знайди слово мови LOK на сітці літер, і воно зробить свою магію: зачорнить ще клітини

## Суть
Поле — сітка літер (іноді порожніх клітин і дірок). Гравець виділяє в ній **слова вигаданої мови LOK** — літери поспіль по прямій; виділені клітини чорніють. Кожне слово, крім того, має **власну дію-заклинання**: LOK дозволяє зачорнити ще одну будь-яку клітину, TLAK — дві сусідні, TA — усі клітини з тією самою літерою тощо. Мета — зачорнити **всі** клітини; правила слів гра **не пояснює текстом**, а показує прикладами-рівнями. Ядро — «мова як механіка»: словник = набір правил-ефектів, а пошук слів (word search) став пазлом на порядок застосування.

## Поле і час
- Квадратна сітка, невелика (типово ~4×4…8×8 (?)); клітина = літера мови LOK, порожня (без літери) або «дірка» (немає клітини).
- Чорна клітина «виходить із сітки»: її вже не можна використати як літеру, але слова **читаються крізь** чорні клітини й дірки (сусідні літери слова можуть бути розділені ними).
- Часу нема: статичний пазл, хід = одне складене слово плюс, можливо, вибір цілі для його ефекту.
- Один екран, камера нерухома; рівні згруповано у 15 світів, кожен вводить нове слово чи взаємодію.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина-літера | tile | літера (L, O, K, T, A, B, E…) | біла → чорна, коли увійшла у слово або в ефект слова |
| Порожня клітина | tile | без літери | не дає складати слова крізь себе як літеру; чорніє лише від ефектів (?) |
| Дірка / «повітря» | static | — | клітини нема; слово читається крізь неї (air gap) |
| Чорна клітина | mark | — | використана; пропускається при читанні; на ній живуть істоти LOK (косметика) |
| Слово LOK | word | 3 літери | склав → чорніють 3 клітини + гравець обирає **1 будь-яку** клітину й чорнить її |
| Слово TLAK | word | 4 літери | склав → 4 клітини + **2 сусідні** клітини на вибір |
| Слово TA | word | 2 літери | склав → обрати клітину; чорніють **усі** клітини з тією ж літерою (або всі порожні, якщо обрано порожню) |
| Слово BE | word | 2 літери | склав → вписати будь-яку літеру в порожню клітину (?) |
| Слово LOLO | word | 4 літери | склав → чорніє лінія клітин по діагоналі (?) |
| Літера X | tile | — | «вільна»: можна вставляти між літерами будь-якого слова як заповнювач/поворот (?) |
| Істоти LOK | — | — | косметичні; заселяють чорні клітини, світ «росте» з прогресом |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(select_path)` → ЯКЩО `cond: in_dictionary(word)` і `custom: «літери йдуть по прямій ортогонально; між ними — лише чорні клітини, дірки або X»` → ТО `mark(cells, black)` для літер слова; інакше `custom: «виділення не приймається»`.
- КОЛИ `word_spelled(LOK)` → ТО `choose(any_white_cell)`, `mark(cell, black)`.
- КОЛИ `word_spelled(TLAK)` → ТО `choose(two_adjacent_white_cells)`, `mark(cells, black)`.
- КОЛИ `word_spelled(TA)` → ТО `choose(cell)`, `mark(all_cells_with_same_letter(cell), black)` (порожня клітина → усі порожні).
- КОЛИ `word_spelled(BE)` → ТО `choose(empty_cell)`, `set_cell(cell, letter)` (?).
- КОЛИ `word_spelled(LOLO)` → ТО `custom: «зачорнити діагональну лінію»` (?).
- КОЛИ `contact(path, X)` → ТО `custom: «X пропускається як заповнювач, слово читається далі»` — X можна використати вільно між літерами інших слів.
- КОЛИ `all_constraints_met` (`count(white_cells, ==, 0)`) → ТО `win`, `unlock(next)`.
- КОЛИ `custom: «білих клітин лишилось, а жодне слово не складається»` → глухий кут: undo/restart (поразки як події нема).
- Ефект слова вибирає ціль гравець → порядок слів і вибір «зайвих» клітин — уся складність: зачорниш не ту клітину — розірвеш інше слово.
- Нові слова гра лише **показує**: перший рівень світу розвʼязується лише тим словом, і гравець виводить правило з того, що сталося (`custom: «правило вчиться прикладом»`).
- Перемога: усі клітини чорні · Поразка: нема · Рахунок: нема (у daily — лідерборд за часом/ходами (?)).

## Керування і ввід
- Миша/тач: провести (drag) або клікати літери слова по черзі; підсвітка виділеного шляху; відпустив — слово перевіряється.
- Після слова з ефектом — режим вибору цілі: клік по клітині (або двох, TLAK).
- Undo кроку, рестарт рівня, підказка (показує наступне слово послідовності).
- One-button-режим доступності (itch.io): ввід однією кнопкою з авто-скануванням (?).
- Геймпад на Switch (курсор по клітинах) (?).

## Вікна, меню, HUD
- `splash-screen` — лого Draknek & Friends.
- `main-menu` — Play (кампанія) · Daily · Settings · Credits.
- `map-window` — світ-мапа зі світами-островами; рівні як вузли; світ відкривається після N пройдених рівнів попереднього; зайві «challenge»-рівні необовʼязкові.
- `game-screen` — сітка літер; HUD: `word-book` (книжечка відкритих слів із прикладами їх дії), `undo-button`, `restart-button`, `hint-button`.
- `hints-window` — підказка: послідовність слів, що розвʼязує рівень (по одному кроку).
- `daily-window` — процедурний пазл дня + `leaderboard` друзів/світу.
- `settings-window` — звук/музика, мова (14), темна тема, колорблайнд-палітра, високий контраст, one-button.
- `editor-window` — редактор рівнів (лише PC, за словами розробника на itch.io).
- Переходи: main-menu → map-window → (рівень) game-screen → (win) map-window; main-menu → daily-window → game-screen.

## Фічі поза полем
- `world-map` + `level-unlock` з порогом пройдених рівнів (кампанія 150+ рівнів, 15 світів).
- `undo`, `restart-level`, `hint` (покроковий «show-solution»).
- `daily-puzzle` з процедурною генерацією + `leaderboard-online` (на itch.io — без лідерборду).
- `codex`-подібна книжка слів: відкриті слова з ілюстраціями дії — словник як частина інтерфейсу.
- `level-editor` (PC), `autosave`/`cloud-save` (Steam Cloud), `achievements`.
- Доступність: `colorblind-palette`, `high-contrast`, `one-hand-mode`/one-button, `tutorial` інтерактивний без тексту, `localization` 14 мов.

## Варіації й родичі
- Паперовий оригінал **LOK** (книжка Блажа Урбана Грацара, 120+ пазлів, сухостирана плівка) — ті самі правила без undo і підказок; ідея — від Increpare (word search мовою токі-пона).
- Родичі: word search (класика), Boggle (шлях літер), Baba Is You (слова як правила), Tametsi/ Hexcells — «правило з прикладу».
- **Осі варіацій:** форма слова — пряма / зі зламом через X / вільний шлях (Boggle); ефект слова — лише чорнить себе / + довільна клітина / + клас клітин (TA) / + змінює літери (BE); хто обирає ціль ефекту — гравець / фіксовано правилом; мова — справжня (word search) / вигадана з малим словником.

## Цікавинки для курсу
- Слово як команда: словник `{слово: ефект}` + перевірка шляху на сітці — 🥉 (дані + валідатор шляху).
- Читання «крізь» чорні клітини й дірки (сусідство в стиснутому ряду) — 📎.
- Ефекти з вибором цілі (режим «обери клітину» після ходу) — 🥉: двофазний хід у UI.
- TA: масове зачорнення за класом літери — 🌱.
- Розвʼязувач рівня перебором послідовностей слів і виборів — 🥇 (дерево станів, відсікання).
- Генератор daily-рівнів з гарантованим розвʼязком — 👑 (`unique-puzzle-generation`).

## Мапа на каталог
- Є: `cell-click` + `hover-highlight` ↔ виділення літер; `satisfy-constraints` + `completion-detection` ↔ усі чорні; `markup-validity` ↔ перевірка слова; `sequential-levels` + `level-unlock` + `level-select` ↔ світи; `daily-puzzle` + `leaderboard` ↔ daily; `in-game-editor` ↔ редактор PC; `help-window` ↔ книжка слів; `settings-window`; `save-progress`.
- **Нема** → пропозиції карток:
  - `+undo-redo` «Undo ходів у грі» · game-logic/flow · 📎 — як у Baba Is You.
  - `+world-map` «Мапа світу з вузлами-рівнями» · levels/progression · 🥉 — як у Baba Is You.
  - `+word-as-command` «Слово-команда з ефектом» · game-logic/rules · 🥉 · слот {effects: list}.
  - `+word-path-select` «Виділення слова шляхом по сітці» · interface/input · 📎 · слот {shape: straight|bend|free}.
  - `+letter-wildcard` «Вільна літера-заповнювач (X)» · game-logic/rules · 🌱.
  - `+post-word-action` «Хід із вибором цілі після дії» · interface/input · 🥉 — двофазний хід.
  - `+color-by-letter-flood` «Ефект на всі клітини класу» · entities/interact · 🌱 — TA.
  - `+rule-teaching-by-example` «Навчання правилу без тексту» · support/docs · 🥉 — перший рівень світу як приклад.
  - `+hint-solution-steps` «Підказка — наступний крок розвʼязку» · levels/solvability · 🥈 (потребує розвʼязувача).

## Пропозиції до словників
- `+trigger:input` — виділення шляху; `+trigger:word_spelled(word)` — складено слово зі словника (подія, на яку чіпляється ефект).
- `+cond:in_dictionary` — шлях утворює слово словника (🔥 ×4 уже); `+cond:free_path` — між літерами лише чорні/дірки/X.
- `+effect:mark` (зачорнити), `+effect:choose` (гравець обирає ціль ефекту), `+effect:set_cell` (BE вписує літеру).
- `+role:mark` (чорна клітина), `+role:word` — слово як сутність-правило (тут не лежить на полі, а «шукається» в ньому — інший варіант, ніж у Baba).
- `+window:map-window`, `+window:codex-window` (книжка слів), `+window:daily-window`.
- `+ui:word-book` — довідник відкритих слів із анімацією ефекту, доступний з рівня.
- `+feature:undo`, `+feature:daily-puzzle`, `+feature:world-map`.
- `+axis:rules` — тут нове значення `discovered`: правила фіксовані, але приховані, гравець виводить їх з прикладів (Baba — `mutable`).

## Джерела
- ⭐ [Wikipedia: LOK Digital](https://en.wikipedia.org/wiki/LOK_Digital) — LOK = 3+1, TLAK = 4+2, TA/LOLO з умовами, X вільна, підказки, daily, історія книжки.
- [Офіційний сайт](https://lok-digital.com/) і [пресkit](https://lok-digital.com/presskit) — 15 світів, 150+ пазлів, daily з лідербордами.
- [Steam](https://store.steampowered.com/app/2207440/LOK_Digital/) — опис, мови, демо.
- [itch.io](https://draknek.itch.io/lok-digital) — доступність, темна тема, редактор на PC.
- [Pocket Gamer review](https://www.pocketgamer.com/lok-digital/review/) — складання слів (ортогонально, крізь чорні), TA, TLAK, книжка слів.
- [Книжка LOK](https://www.letibus.com/lok) — паперовий першоджерело.
- YouTube: [пошук «LOK Digital gameplay»](https://www.youtube.com/results?search_query=LOK+Digital+gameplay).

## Непевне
- (?) BE (вписати літеру в порожню клітину) і LOLO (діагональна лінія) — з короткого пошукового резюме оглядів, не з першоджерела; точні умови LOLO не перевірені.
- (?) Роль X: «вільна між літерами» (Wikipedia) vs «дозволяє змінити напрям слова» (огляд) — можливо, обидва.
- (?) Порожні клітини: чи можна читати слово крізь них, чи лише крізь дірки й чорні.
- (?) Повний список слів (у грі їх більше: 15 світів) — гра свідомо не публікує правила; описано лише підтверджені.
- (?) Метрика лідерборду daily (час чи кількість undo/підказок), one-button-режим і керування геймпадом — не перевірено.
- (?) Розміри сіток — з памʼяті скриншотів.
