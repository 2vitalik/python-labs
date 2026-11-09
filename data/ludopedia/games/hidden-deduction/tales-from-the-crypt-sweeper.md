---
title: Tales from the Crypt Sweeper
slug: tales-from-the-crypt-sweeper
aka: [Crypt Sweeper, cryptsweeper]
family: hidden-deduction
also: []
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: hidden
  random: setup
  goal: state
year: 2017
platforms: [web (itch.io, HTML5 Unity WebGL)]
links:
  - {kind: itch, url: "https://laundrybear.itch.io/tales-from-the-crypt-sweeper", best: true, note: "грати в браузері; опис правил (ЛКМ — копати, ПКМ — прапорець, символи перемішуються щогри), знімки поля 20×20, коментарі про перший клік"}
  - {kind: other, url: "https://itch.io/jam/tojam-12", note: "джем TOJam 12 «What TWELVEs below!», 93 роботи; гра в списку як «A cryptographic minesweeper-like»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tales+from+the+Crypt+Sweeper+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [cell-click, neighbor-count-clue, flood-reveal, completion-detection, face-button, game-screen, +symbol-cipher-clue]
proposes: ["+effect:shuffle", "+card:symbol-cipher-clue"]
author: opus
date: 2026-11-09
---

# Tales from the Crypt Sweeper — сапер, де числа замінені символами, а ключ шифру щогри новий

## Суть
Класичний [minesweeper](minesweeper.md) на кладовищі: копаєш склепи, обминаючи могили з привидами. Відкрита клітина показує не цифру, а **символ** (півмісяць, тризуб тощо), що означає кількість привидів поруч. Відповідність «символ → число» перемішується в кожній новій грі, тож перші ходи — це злам шифру: який символ стоїть біля одного привида, а який біля трьох. Джемова гра Laundry Bear Games (TOJam 12).

## Поле і час
- Квадратна сітка; на знімках — 20×20 клітин у рамці, над полем — портрет-індикатор стану, під полем — легенда керування.
- Час не тисне: таймера на знімках нема, хід = один клік (`time: static`).
- Шари: закрита плита · відкрита клітина з символом або порожня · прапорець · привид (видно лише після поразки).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Закрита плита (склеп) | tile | закрита / відкрита | ЛКМ відкриває; ПКМ ставить прапорець |
| Могила з привидом | hazard | — | відкрити = поразка; після поразки показуються всі |
| Символ-підказка | mark | символ ← перестановка чисел 1–8 | кількість привидів серед 8 сусідів, записана поточним шифром |
| Порожня клітина (0) | mark | — | без символу; запускає каскад відкриття сусідів |
| Прапорець (квітка) | mark | — | позначка гравця «тут могила» |
| Портрет | static | обличчя / череп | показує стан гри; після поразки — череп |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «розкласти привидів по могилах»`, `custom: «перемішати набір символів: кожному числу 1–8 — випадковий символ»` (`+effect:shuffle`).
- КОЛИ `input(dig, cell)` → ЯКЩО `not occupied(cell, grave)` → ТО `reveal(cell)`, `set_value(cell, symbol[adjacent_count(cell, grave)])`.
- КОЛИ `after(reveal)` → ЯКЩО `adjacent_count(cell, grave, ==, 0)` → ТО `reveal(neighbors8)` — каскад, доки трапляються нулі.
- КОЛИ `input(dig, cell)` → ЯКЩО `occupied(cell, grave)` → ТО `reveal(all graves)`, `transform(portrait, skull)`, `lose`.
- Перший клік не захищений: ЯКЩО `first_time` і `occupied(cell, grave)` → ТО так само `lose` (гравці в коментарях скаржаться, автор лишив класичне правило).
- КОЛИ `input(flag, cell)` → ЯКЩО `custom: «клітина закрита»` → ТО `mark(cell, flag)`; повторний ПКМ → `unmark(cell)` (?).
- КОЛИ `counter(closed_safe, ==, 0)` → ТО `win`.
- Перемога: відкрито всі клітини без могил · Поразка: відкрито могилу · Рахунку нема.
- Гравцеві «правило» шифру — `custom: «у всіх клітинах однаковий символ = однакове число»` — гра його не перевіряє, ним користується лише голова гравця.

## Керування і ввід
- ЛКМ — копати (відкрити клітину), ПКМ — поставити прапорець; підказка про це завжди внизу екрана.
- Інших дій на знімках і в описі нема; клік по портрету як рестарт — (?).

## Вікна, меню, HUD
- `game-screen`: поле 20×20, портрет над полем (`face-button`-подібний), `legend` під полем («LEFT CLICK: DIG» / «RIGHT CLICK: FLAG»).
- Лічильника мін і таймера не видно; окремого меню, налаштувань і `end-screen` на знімках нема — поразка показується на самому полі (усі привиди + череп).
- Переходи: `game-screen` → поразка/перемога на тому ж екрані → нова гра (як саме — (?)).

## Фічі поза полем
—

## Варіації й родичі
- База — [minesweeper](minesweeper.md); інші переписані підказки — [cavern-sweeper](cavern-sweeper.md) (різні види монстрів), [omegasweeper](omegasweeper.md) (сума з антимінами), [14-minesweeper-variants](14-minesweeper-variants.md) (правила підказок змінюються); підказку голосом — [blind-sweeper](blind-sweeper.md).
- Злам коду як окрема гра — [mastermind](mastermind.md), [jotto](jotto.md); тут код — лише шар поверх сапера.
- **Осі варіацій «подача підказки»:** цифри / кольори / фіксовані символи / символи з новим ключем щогри (ця гра) / звук; «нуль» зашифрований чи ні (тут — порожня клітина, тож каскад працює як у базі).

## Цікавинки для курсу
- Шифр підказок: масив `glyphs`, `random.shuffle` на старті, рендер `glyphs[n]` замість `str(n)` — 🌱.
- Каскад нулів, коли «нуль» не зашифровано, а решта — так — 📎 (класичний flood fill + розділення логіки й рендера).
- Режим-перемикач «цифри / шифр» на тому самому двіжку — 🌱 (картка `logic-render-split` у дії).
- Помічник-розшифровувач: гравець підписує символ своїм числом, гра підставляє позначку у всі такі клітини — 📎.
- Розвʼязувач, що одночасно шукає і перестановку символів, і розкладку мін (CSP з невідомим ключем) — 🥇.

## Мапа на каталог
- Є: `cell-click` ↔ копати; `neighbor-count-clue` ↔ символ = число привидів поруч; `flood-reveal` ↔ порожні клітини розкриваються хвилею; `completion-detection` ↔ перемога; `face-button` ↔ портрет над полем (рестарт — (?)); `game-screen`.
- **Нема** → пропозиції карток:
  - `+symbol-cipher-clue` «Числа-підказки записані символами з випадковим ключем на гру» · game-logic/constraints · 🌱 · слоти {zero_encoded: bool, reshuffle: per-game|per-level}.

## Пропозиції до словників
- `+effect:shuffle` — перемішати набір (тут — відповідність символів числам; уже пропонувався в корпусі для колод і плиток).
- `+card:symbol-cipher-clue` — див. вище.

## Джерела
- ⭐ [itch.io: Tales from the Crypt Sweeper](https://laundrybear.itch.io/tales-from-the-crypt-sweeper) — опис: копати склепи, символи замість чисел, рандом щогри, ЛКМ/ПКМ; два знімки (поле 20×20, легенда, поразка з усіма привидами й черепом); коментарі: перший клік не безпечний, вгадування трапляється; Unity, TOJam 12.
- [itch.io: TOJam 12](https://itch.io/jam/tojam-12) — сторінка джему й опис гри в списку робіт.
- Збірка гри (Unity WebGL, `global-metadata.dat` у `cryptsweeper.data.unityweb`) — імена класів/полів: `Element` (mine, flagged, revealed, zeroTexture, emptyTextures, minePercentage), `Grid` (uncoverMines, adjacentMines, FFuncover, isFinished, GameOverButton), `Utilities.Shuffle`.
- YouTube: пошук «Tales from the Crypt Sweeper gameplay».

## Непевне
- (?) Рік: на сторінці дати нема; 2017 — за TOJam 12 і чергою.
- (?) Скільки привидів на полі: імʼя поля `minePercentage` у коді натякає, що кожна клітина стає могилою з певною ймовірністю (як у відомому Unity-туторіалі сапера), тобто кількість мін щоразу різна; число не бачив.
- (?) Скільки різних символів (на знімках — 4: півмісяць, тризуб, ♃-подібний, підкова) і чи схожі між собою деякі з них (питання гравця в коментарях без відповіді).
- (?) Чи можна копати клітину під прапорцем; чи ПКМ знімає прапорець; чи клік по портрету починає нову гру (кнопка `GameOverButton` у коді є).
- (?) Чи гра показує екран перемоги.
