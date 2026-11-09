---
title: Sudoku Mansion
slug: sudoku-mansion
aka: [Судоку-маєток]
family: pencil-logic
also: [thinky]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: hidden
  random: none
  goal: constraints
year: 2026
platforms: [PC, Steam Deck]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/5005590/Sudoku_Mansion/", best: true, note: "опис: кімнати-варіанти, класи (German Whisperer → Region Sum Ambassador), боси, таємні кімнати, доступність"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=5005590&count=25&maxlength=6000", note: "патчноути 1.0.1–1.4.1 (JSON): туман, перекриття кімнат, ліхтарі, боси з фазами, undo 1000"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Sudoku+Mansion+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [markup-validity, completion-detection, satisfy-constraints, conflict-highlight, pencil-marks, cell-click, keyboard-controls, multi-select, undo-redo, save-multi-slot, save-autosave, tutorial-window, help-window, settings-window, controls-remap, achievements-window, field-scaling, +fog-reveal, +overlapping-grids, +ruleset-swap, +rule-discovery, +boss-puzzle, +multi-phase-boss, +line-constraints, +killer-cage, +dot-constraints, +mistake-check, +brute-force-limit, +guiding-marker, +player-notes, +rules-panel]
proposes: ["+cond:class(c)", "+effect:switch_ruleset", "+ui:class-pill", "+ui:guiding-marker", "+ui:rules-panel", "+feature:brute-force-limit", "+feature:rewind-to-mistake", "+feature:player-notes", "+feature:demo-save-transfer", "+axis:rules", "+card:ruleset-swap", "+card:multi-phase-boss", "+card:mistake-check"]
author: opus
date: 2026-11-09
---

# Sudoku Mansion — маєток із кімнат-судоку, де «клас» перечитує ту саму кімнату за іншим правилом

## Суть
Сюжетна пазл-пригода від сетера Nurator (Vault Door Studios, серпень 2026): гравець ходить нелінійним маєтком, кожна кімната — ручний варіант судоку, що вводить одне нове поняття. Головна ідея — **класи**: розблокований клас змінює правила вже знайомої кімнати при тій самій розмітці (кімнату, пройдену як German Whisperer, можна пройти вдруге як Region Sum Ambassador). Кімнати перекриваються, частина поля під туманом; є таємні кімнати, сховища, пастки й боси з кількома фазами. Понад 50 пазлів.

## Поле і час
- Одна велика мапа маєтку з кімнат-сіток різного розміру (є 8×8 і 9×9 — патч 1.2.0 позначає «9 у сітці 8×8» як конфлікт); кімнати **перекриваються**, олівці синхронізуються в спільних клітинках; між кімнатами — проміжки (клавіатурний курсор їх перестрибує, до 3 клітинок).
- Шари клітинки: туман · цифра або літера · олівці (кути/центр) · колір · елементи правил (лінії, клітки, крапки, стрілки).
- Зовнішні кімнати (outside rooms), тематичні зони зі своїми правилами: Chapel, Library, Armory, Dining Room, Planetarium, House of Chance, Untamed Cave, Fractured Constellations, Threefold Vault (боси/кімнати з патчів).
- Час статичний; хід = цифра/позначка; без таймінгу («Playable without Timed Input»).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | цифра 1…N або літера · олівці · колір | приймає значення; може належати двом кімнатам |
| Кімната | zone | розмір N×N; набір правил; клас | рядки/стовпці/регіони без повторів + правила варіанту |
| Перекриття кімнат | zone | спільні клітинки | значення має задовольнити обидві кімнати; олівці синхронні |
| Клас (German Whisperer, Region Sum Ambassador …) | switch | набір правил | перечитує ті самі елементи кімнати за іншим правилом |
| Туман | hazard | закриті клітинки | ховає частину кімнати; знімається по ходу (у фазі 2 боса — більше) |
| Лінія (whisper / region sum / modular) | mark | шлях клітинок | обмеження залежить від активного класу |
| Killer-клітка · Kropki-крапка · Hitpoint Arrow · Quadruple · Antiknight | mark | тип і число | стандартні модулі варіантного судоку |
| Бос | boss | кілька фаз, кнопки перемикання | окремий пазл; після розвʼязку значок → золотий лавровий вінок |
| Ліхтар (lamp charges) | resource | заряди | обмежує перебір цифр (anti brute force) (?) |
| Таємна кімната / сховище / пастка / trapdoor | container | — | контент поза основним шляхом; винагорода за повернення |
| Направляючий маркер | static | — | вказує на наступне вартісне перекриття |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(digit d)` → ЯКЩО `not unique(row|col|box)` у кімнаті (у перекритті — в обох) → ТО `constraint_broken(sudoku)`.
- КОЛИ `input(digit d)` → ЯКЩО `custom: «d > N кімнати»` → ТО `constraint_broken(range)` (1.2.0).
- КОЛИ `input(digit d)` → ЯКЩО `mode(antiknight)` and `custom: «та сама цифра на ход коня»` → ТО `constraint_broken(antiknight)` (1.1.0).
- КОЛИ `input(choose class c)` → ТО `custom: «правила кімнати = правила класу; розмітка та сама»` (див. пропозицію effect:switch_ruleset).
- German Whisperer: КОЛИ `input(digit)` на лінії → ЯКЩО `custom: «активний клас — Whisperer»` and `custom: «сусіди різняться < 5»` → ТО `constraint_broken(whisper)`.
- Region Sum Ambassador: КОЛИ `input(digit)` на лінії → ЯКЩО `custom: «активний клас — Region Sum»` and `custom: «суми відрізків лінії в різних регіонах не рівні»` → ТО `constraint_broken(region_sum)`.
- Killer: КОЛИ `input(digit)` у клітці → ЯКЩО `not sum(cage, n)` or `not unique(cage)` → ТО `constraint_broken(killer)`.
- КОЛИ `custom: «прогрес у маєтку»` → ТО `unlock(class)` (?) — як саме відкриваються класи, джерело не каже.
- КОЛИ `custom: «кімната розвʼязана / фаза боса»` → ТО `reveal(fogged_cells)`; у класовій кімнаті reset знову відкриває туман правильно (1.1.0).
- КОЛИ `input(check)` → ТО `custom: «показати помилки; видалити хибні цифри лише після підтвердження»` (1.0.1).
- КОЛИ `input(digit d)` → ЯКЩО `custom: «d поза розвʼязком»` → ТО `counter(lamp_charges, -1)` (?) — механіку ліхтарів «проти брутфорсу» описано лише в патчах.
- КОЛИ `custom: «для кімнати бракує правила/класу»` → ТО `message(missing_rule_warning)` (1.4.0).
- КОЛИ `all_constraints_met` (бос) → ТО `custom: «значок боса → золотий вінок»`, `unlock(next_area)` (?).
- КОЛИ `input(undo)` → ТО `undo(1)` лише для цифр (не для опцій і нотаток), до 1000 кроків, історія — у збереженні; «rewind» — назад до моменту перед останньою помилкою.
- Перемога: розвʼязати кімнати, боси й таємниці маєтку (сюжетний фінал + епілоги). Поразки нема; рахунок — % проходження в слоті збереження.

## Керування і ввід
- Повністю мишею, повністю клавіатурою (переназначувані гарячі клавіші), контролером (Steam Input, трекпад, діагональний рух, малювання ліній з відкатом) або лише тачем.
- Клік/drag — вибір клітинок; long press — вибрати всі такі ж цифри/олівці; Delete/Backspace — стерти; Shift/Ctrl+Delete — стерти відповідні олівці; `/` — перемкнути цифри ↔ літери; Alt+літера — ввести літеру; M — звук.
- Опції вводу: ліва кнопка-скрол вибирає клітинки; фіксовані позиції кутових цифр; вимкнути «неможливі цифри»; Reset View — повернути камеру мапи.

## Вікна, меню, HUD
- `main-menu` (?) → `save-slots` — кілька слотів з % проходження (100 % — окремий текст).
- `game-screen`: мапа маєтку, `fog-overlay`, ліва колонка правил (`+ui:rules-panel`, «лише релевантні правила» за замовчуванням), `+ui:class-pill` — значок активного класу, вкладки lore/rules, вкладка нотаток гравця, `+ui:guiding-marker`, `pencil-marks`, `conflict-highlight`, кнопки фаз боса.
- Попап правила з кнопкою help і прикладами-картинками → `hints-window` (клік по правилу відкриває підказки; підказки для всіх складних пазлів і для розблокування боса).
- `tutorial-window` — навчальні попапи (окремо для Steam Deck і ПК, можна сховати).
- `settings-window`: розмір тексту, кольорові теми, колірна сліпота, вигляд елементів, контраст, гучність, перемикач попапів правил, опції вводу.
- `end-screen` / `dialogue-window` — сюжетні тексти й епілоги (Trapdoor 1); `achievements-window` (Steam).
- Переходи: слот → мапа → кімната/бос (без окремих екранів — усе на одній мапі (?)).

## Фічі поза полем
- `save-slots` + `autosave` («Save Anytime») + `cloud-save`; `+feature:demo-save-transfer` — прогрес демо переходить у повну гру.
- `undo` (до 1000, у збереженні) + `+feature:rewind-to-mistake`; `auto-check` (conflict checker, antiknight-конфлікти, «9 у 8×8»), `+mistake-check` з підтвердженням.
- `hint` — підказки по правилах і пазлах; `onboarding-hints` — направляючий маркер; попередження про відсутнє правило.
- `+feature:brute-force-limit` — заряди ліхтаря проти перебору.
- `+feature:player-notes` — вкладка вільних нотаток гравця.
- Доступність: `font-scale`, `colorblind-palette`, `high-contrast`, `remap-controls`, `gamepad-support`, `touch-controls`, `one-hand-mode` (лише миша / лише клавіатура).
- `achievements`; Steam Deck Verified.

## Варіації й родичі
- [sudokuvania](sudokuvania.md) — безкоштовний попередник жанру в SudokuPad: туман, «вивчені» правила, бос-пазли на гаттай-мапі; Mansion додає класи й сюжет.
- [sudoku-variants](sudoku-variants.md), [sudoku-line-dot-variants](sudoku-line-dot-variants.md) — модулі (Whispers, Region Sum, Killer, Kropki, Arrow, Antiknight), з яких зібрано кімнати.
- Cracking the Cryptic: Fog of War — туман у комерційному застосунку (див. sudoku-variants).
- Осі варіацій: **правила кімнати** (фіксовані / відкриваються / обираються класом) · **звʼязок кімнат** (окремі рівні / перекриття зі спільними клітинками) · **захист від перебору** (нема / ліхтарі / ліміт помилок).

## Цікавинки для курсу
- Клас = набір правил над тією самою розміткою; перемикач перечитує лінії по-іншому — 🥈 (правила як дані, валідатор за активним набором).
- Перекриття кімнат зі синхронними олівцями — 🥉.
- Undo з історією в збереженні + rewind до останньої помилки — 🥈 (потрібен розвʼязок і стек станів).
- Заряди проти брутфорсу — 📎 (лічильник, що карає за цифри поза розвʼязком).
- Бос із фазами й кнопками перемикання фаз — 🥉.
- Попередження «бракує правила» і направляючий маркер — 📎 (аналіз, що гравцеві доступно).

## Мапа на каталог
- Є: `markup-validity` · `completion-detection` · `satisfy-constraints` · `conflict-highlight` · `pencil-marks` · `cell-click` · `keyboard-controls` · `multi-select` (long press) · `undo-redo` · `save-multi-slot` · `save-autosave` · `tutorial-window` · `help-window` · `settings-window` · `controls-remap` · `achievements-window` · `field-scaling` (мапа, Reset View).
- **Нема** → пропозиції карток:
  - `+ruleset-swap` «Той самий рівень за іншим набором правил» · game-logic/constraints · 🥈 · слот {sets: list}.
  - `+multi-phase-boss` «Бос-пазл із фазами» · levels/progression · 🥉.
  - `+mistake-check` «Перевірка помилок проти розвʼязку з підтвердженням» · game-logic/constraints · 📎.
  - `+brute-force-limit` «Обмеження перебору (заряди)» · game-logic/difficulty · 📎.
  - `+guiding-marker` «Маркер наступного кроку» · interface/hud · 🌱.
  - `+player-notes` «Нотатки гравця» · interface/input · 🌱.
  - `+fog-reveal` · `+overlapping-grids` · `+rule-discovery` · `+boss-puzzle` · `+rules-panel` · `+line-constraints` · `+killer-cage` · `+dot-constraints` — як у sudokuvania / sudoku-variants.

## Пропозиції до словників
- `+cond:class(c)` — активний клас (набір правил) гравця.
- `+effect:switch_ruleset` — змінити набір правил кімнати без зміни розмітки.
- `+ui:class-pill` — значок активного класу; `+ui:guiding-marker` — стрілка до наступного вартісного місця; `+ui:rules-panel` — повтор.
- `+feature:brute-force-limit` · `+feature:rewind-to-mistake` · `+feature:player-notes` · `+feature:demo-save-transfer`.
- `+axis:rules` — значення `switchable`: гравець сам обирає чинний набір правил (класи).
- `+card:ruleset-swap` · `+card:multi-phase-boss` · `+card:mistake-check` — див. мапу.

## Джерела
- ⭐ [Steam: Sudoku Mansion](https://store.steampowered.com/app/5005590/Sudoku_Mansion/) — опис, класи, список фіч, доступність, дата 19.08.2026, Vault Door Studios.
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=5005590&count=25&maxlength=6000) — 21 патчноут: перекриття кімнат, туман, ліхтарі, боси з фазами, undo, гарячі клавіші, Steam Deck.
- YouTube: [пошук](https://www.youtube.com/results?search_query=Sudoku+Mansion+gameplay).

## Непевне
- (?) Повний список класів і їхніх правил — на Steam названо лише German Whisperer і Region Sum Ambassador.
- (?) Як відкриваються класи й двері між кімнатами, що саме знімає туман — описів не знайшов.
- (?) Ліхтарі: «charges against brute forcing», «lost for digits outside the solution» — точна механіка невідома.
- (?) Правило Region Sum Line тут дано за стандартом CtC (суми відрізків у регіонах рівні); у грі його переформульовували (1.2.3).
- (?) Чи є окреме головне меню й екрани кімнат, чи все на одній мапі.
