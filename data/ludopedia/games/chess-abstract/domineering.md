---
title: Domineering
slug: domineering
aka: [Stop-Gate, Crosscram]
family: chess-abstract
also: [board-digital]
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 1973
platforms: [paper, web, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Domineering", best: true, note: "правила, значення малих областей у теорії ігор (−1, ±1), хто виграє на квадратах 1×1…11×11, хто й коли розвʼязав 8×8–11×11"}
  - {kind: wiki, url: "https://fr.wikipedia.org/wiki/Domineering", note: "автор (Göran Andersson, 1973), Гарднер 1974, звʼязок із Cram"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Cram_(game)", note: "безсторонній родич: обидві орієнтації, стратегія симетрії, misère, Grundy-значення"}
  - {kind: play, url: "https://ludii.games/details.php?keyword=Domineering", note: "Ludii: формалізовані правила, інші назви Stop Gate / Crosscram"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=domineering+game+combinatorial+game+theory", note: "пошук; лекції про гру"}
stage: v1
coverage: 75
mechanics: [polyomino-placement, cursor-place, no-moves-left, hot-seat, turn-enforcement, ai-opponent, ai-greedy, ai-minimax, level-solver, cell-click, hover-highlight, last-move-highlight, field-size-picker, game-screen, main-menu, end-screen, help-window, settings-window, undo-step, state-as-data, unit-tests, +place-stone, +last-move-wins, +asymmetric-sides, +board-layouts, +partisan-orientation, +game-sum-decomposition]
proposes: ["+axis:impartiality", "+ui:moves-left-per-side", "+feature:region-analysis", "+card:partisan-orientation", "+card:game-sum-decomposition"]
author: opus
date: 2026-11-09
---

# Domineering — кладеш доміно лише своєю орієнтацією: один вертикально, другий горизонтально; хто не може покласти — програв

## Суть
Паперова гра двох на клітчастому полі будь-якої форми. По черзі кожен кладе доміно на дві сусідні вільні клітини: **Left (V) — лише вертикально, Right (H) — лише горизонтально**. Хто на своєму ході не має куди покласти доміно, програє (нормальна гра). Ядро — ніхто не ходить фігурою, обидва лише зменшують простір; поле швидко розпадається на незалежні області, і гра стає «сумою ігор» — тому Domineering є хрестоматійним прикладом комбінаторної теорії ігор.

## Поле і час
- Будь-яка множина клітин клітчастого паперу: квадрат 6×6, прямокутник, довільне поліоміно. Стандарту розміру нема; турнір MSRI грали на 8×8.
- Один шар: клітина вільна / накрита. Доміно, раз покладене, лишається назавжди; взяття нема.
- Покроково, двоє, повна інформація, без випадковості. Хід = одне доміно. Пасу нема.
- Хто ходить першим — домовленість (у прикладі Wikipedia на 5×5 першим ходить H і програє на 13-му ході).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина поля | static | вільна / накрита | частина маски поля; накрита доміно назавжди |
| Доміно Left | piece | 1×2, орієнтація лише вертикальна | кладеться на 2 вертикально сусідні вільні клітини |
| Доміно Right | piece | 2×1, орієнтація лише горизонтальна | кладеться на 2 горизонтально сусідні вільні клітини |
| Гравець | player | сторона Left (V) / Right (H) | на своєму ході мусить покласти доміно |
| Область | zone | звʼязна компонента вільних клітин | після розпаду поля — окрема «гра», незалежна від інших (стратегічне поняття) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «усі клітини маски вільні; сторони домовились, хто V, хто H і хто першим»`.
- КОЛИ `turn_start(side)` → ЯКЩО `no_moves(side)` → ТО `lose` (для `side`; суперник виграє).
- КОЛИ `input(place, cells)` → ЯКЩО `turn_of(Left)` і `fits(domino_vertical, cells)` → ТО `place(Left, domino)`, `end_turn`.
- КОЛИ `input(place, cells)` → ЯКЩО `turn_of(Right)` і `fits(domino_horizontal, cells)` → ТО `place(Right, domino)`, `end_turn`.
- КОЛИ `input(place, cells)` → ЯКЩО `not fits(own_orientation, cells)` (зайнято, поза маскою або чужа орієнтація) → ТО `block`.
- КОЛИ `after(place)` → ТО `custom: «вільні клітини, яких не торкається жодне можливе доміно сторони, для неї мертві»` — ізольована клітина не дає ходу нікому.
- КОЛИ `after(place)` → ЯКЩО `not connected(free_cells)` → ТО `custom: «позиція = сума незалежних областей»` (аналіз; на правила не впливає).
- Перемога: суперник не може покласти доміно своєї орієнтації · Поразка: ти не можеш · Нічиєї нема: гра скінченна (клітин меншає), повторень нема. Рахунок: партія 1 / 0.

## Керування і ввід
- Папір: олівцем обводиш дві клітини або малюєш риску через них.
- (цифрова версія) Наведення на клітину показує тінь доміно своєї орієнтації (`ghost-piece`): для V — клітина + нижня/верхня сусідня, для H — ліва/права; клік — покласти. Для однозначності — точка кліку = верхня/ліва клітина доміно.
- Альтернатива: drag між двома сусідніми клітинами; чужа орієнтація просто не підсвічується.

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Проти AI · Двоє за одним пристроєм · Правила → `help-window` · Налаштування.
- `match-setup` / `settings-window`: розмір прямокутника або форма поля (маска), хто V / H, хто першим, рівень AI, варіант Cram.
- `game-screen`: сітка; доміно у кольорах сторін; `ghost-piece` під курсором; `turn-indicator`; лічильник можливих ходів кожної сторони (`moves-left-per-side`); `last-move-highlight`; `undo-button` проти AI.
- `end-screen`: «V не має ходу — H переміг», кількість ходів; Реванш.
- Переходи: main-menu → match-setup → game-screen → end-screen → game-screen / main-menu.

## Фічі поза полем
- `custom-difficulty` — розмір/форма поля; `custom-rules` — Cram (будь-яка орієнтація), misère.
- `ai-opponent-levels`: випадковий → жадібний (максимізуй різницю «мої можливі ходи − його») → alpha-beta з розкладом на області.
- `undo` проти AI; `hotseat`; аналіз позиції — значення кожної області (`region-analysis`, режим навчання CGT).

## Варіації й родичі
- **Cram** — безсторонній варіант: обидва гравці кладуть доміно будь-якої орієнтації; розбирається теоремою Шпрага — Гранді. На полі парне×парне виграє другий дзеркаленням через центр, на парне×непарне — перший (перше доміно в центр, далі дзеркало). Misère-Cram — хто не може піти, той виграв. Інші назви Cram: plugg, dots-and-pairs.
- **Форма поля** — прямокутники m×n (значення зібрані на сайті Nathan Bullock), довільні поліоміно; гра на будь-якій мапі клітин.
- Розвʼязані квадрати: перший гравець виграє на 2×2, 3×3, 4×4, 6×6, 7×7, 8×8, 9×9, 10×10, 11×11; другий — на 1×1 і 5×5. 8×8 розвʼязали Breuker, Uiterwijk, van den Herik (2000), 9×9 — невдовзі після них, 10×10 — Nathan Bullock (2002), 11×11 — Jos Uiterwijk (2016).
- Значення малих областей: 1×2 (два в ряд, горизонтально) = {|0} = −1 — запасний хід для Right; 2×2 = {1|−1} = ±1 — «гаряча» гра, кожен хоче сходити туди першим; 2×3 — дробове значення (дріб і температура — у джерелі).
- Родичі: [amazons](amazons.md) (теж «хто не може піти — програв», поле розпадається на області), [dots-and-boxes](dots-and-boxes.md) (класика CGT), [hex](hex.md) (лише постановка), [konane](konane.md); Blokus і pentomino-гра в `board-digital` (викладання поліоміно).
- **Осі варіацій**: орієнтація (своя для кожного — Domineering / будь-яка — Cram) · мета (нормальна / misère) · фігура (доміно / інші поліоміно (?)) · поле (прямокутник / маска).

## Цікавинки для курсу
- Поле-маска + перевірка «дві сусідні вільні клітини в моїй орієнтації» + генерація всіх ходів сторони — 🌱.
- Кінець гри як `no_moves(side)` на старті ходу, а не окрема умова перемоги — 🌱.
- Жадібний AI «максимізуй (мої ходи − його ходи)», з урахуванням «безпечних» ходів, які суперник не може зіпсувати — 📎.
- Alpha-beta на 6×6–8×8 з транспозиційною таблицею — 🥈.
- Розклад позиції на звʼязні області (flood fill) і сума ігор: значення −1, ±1, дроби; показ «хто виграє в кожній області» — 🥇.
- Повний розвʼязувач квадратних полів на рівні 8×8+ (дослідницькі програми 2000–2016) — 👑.
- Перемикач Domineering ↔ Cram і стратегія дзеркала як перевірка AI — 📎.

## Мапа на каталог
- Є: `polyomino-placement` ↔ доміно як поліоміно з 2 клітин · `cursor-place` ↔ поставити на вільні клітини · `no-moves-left` ↔ хто не може піти — програв · `hot-seat`, `turn-enforcement` · `ai-opponent`, `ai-greedy`, `ai-minimax`, `level-solver` ↔ розвʼязування позицій · `cell-click`, `hover-highlight` ↔ тінь доміно · `last-move-highlight` · `field-size-picker` · вікна `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window` · `undo-step`, `state-as-data`, `unit-tests`.
- Наявні пропозиції корпусу: `+place-stone` (хід — постановка), `+last-move-wins` (нормальна гра), `+asymmetric-sides` (у сторін різні ходи), `+board-layouts` (форма поля; див. [ataxx](ataxx.md)).
- **Нема** → пропозиції карток:
  - `+partisan-orientation` «Кожна сторона кладе фігуру лише своєю орієнтацією» · entities/legality · 🌱 · слоти {left: vertical, right: horizontal, any: bool (Cram)}.
  - `+game-sum-decomposition` «Розклад позиції на незалежні області (сума ігор)» · game-logic/analysis · 🥇 — також Amazons, Go-ендшпілі, Dots and Boxes.

## Пропозиції до словників
- `+axis:impartiality` — `impartial` (у сторін ті самі ходи: Cram, Nim) · `partisan` (різні ходи: Domineering, шахи) · `shared-moves` (ходи однакові, різна мета: Phutball).
- `+ui:moves-left-per-side` — лічильник легальних ходів кожної сторони (оцінка позиції, наочно для новачка).
- `+feature:region-analysis` — режим аналізу: показ значення/переможця кожної незалежної області.
- `+card:partisan-orientation`, `+card:game-sum-decomposition` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Domineering](https://en.wikipedia.org/wiki/Domineering) — правила, інші назви (Stop-Gate, Crosscram), значення малих областей ({|0} = −1, {1|−1} = ±1), таблиця переможців квадратних полів, історія розвʼязання 8×8 (2000), 10×10 (2002), 11×11 (2016), турнір MSRI 8×8.
- [Wikipedia FR: Domineering](https://fr.wikipedia.org/wiki/Domineering) — автор Göran Andersson, 1973; Мартін Гарднер — 1974; Cram як варіант без чергування орієнтацій.
- [Wikipedia: Cram](https://en.wikipedia.org/wiki/Cram_(game)) — безсторонній варіант, стратегії симетрії, misère, Grundy-значення 2×n, Gardner, Scientific American, 1974.
- [Ludii: Domineering](https://ludii.games/details.php?keyword=Domineering) — формалізовані правила (V/H, «хто не може піти — програв»), назви Stop Gate / Crosscram.
- YouTube: пошук «domineering game combinatorial game theory».

## Непевне
- (?) Рік: французька Wikipedia — 1973 (Andersson), англійська року не дає; у шапці 1973.
- (?) Хто ходить першим за «канонічними» правилами — джерела не фіксують; у таблиці розвʼязаних полів «перший гравець» трактую як «той, хто ходить першим, за будь-якої орієнтації» (для квадратів симетрично).
- (?) Варіанти з триміно/іншими поліоміно — не бачив у джерелах, лише як вісь варіацій.
- (?) Точне значення 2×3 у статті відображено криво ({2|−1/2}, середнє 3/4, температура 1¼ — перевірити за Winning Ways).
- (?) Усталеної UA-назви не знайшов.
