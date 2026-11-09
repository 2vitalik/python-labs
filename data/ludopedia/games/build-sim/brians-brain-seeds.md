---
title: Brian's Brain і Seeds
slug: brians-brain-seeds
aka: [«Мозок Браяна», Seeds, B2/S]
family: build-sim
also: []
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: none
year: null
platforms: [web, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Brian%27s_Brain", best: true, note: "3 стани on/dying/off, народження при рівно 2 on-сусідах, кораблі, граблі, осцилятор періоду 3"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Seeds_(cellular_automaton)", note: "B2/S: кожна жива клітина вмирає щокроку; вибухове зростання; кораблі c/1"}
  - {kind: official, url: "https://golly.sourceforge.io/", note: "Golly — симулятор КА, сімейство Generations"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=brian%27s+brain+cellular+automaton", note: "пошук; рухомі структури"}
stage: v1
coverage: 80
mechanics: [cell-click, editor-palette, editor-draw-tools, editor-erase, in-game-editor, game-loop, game-pause, state-as-data, level-from-txt, import-open-formats, field-scaling, rule-variants, logic-render-split, unit-tests, +cellular-automaton-rule, +multi-state-cell, +rule-string, +step-run-speed, +pattern-library, +random-soup]
proposes: ["+ui:generation-counter", "+ui:rule-input", "+card:multi-state-cell", "+card:refractory-state", "+axis:states=n"]
author: opus
date: 2026-11-09
---

# Brian's Brain і Seeds — автомати Браяна Сільвермана: «народись при рівно 2 сусідах», і майже все, що живе, летить

## Суть
Два споріднені клітинні автомати Браяна Сільвермана (автора й [Wireworld](wireworld.md)). **Seeds** (B2/S): мертва клітина народжується, якщо в неї рівно 2 живі сусіди, а жива завжди вмирає наступного кроку — тому майже будь-який патерн вибухає хаосом на все поле. **Brian's Brain** додає третій стан «вмирає» (рефрактерний, як у нейрона після імпульсу): він блокує народження позаду і дає напрям руху, тож майже кожен патерн — космічний корабель. Гравець малює клітини і спостерігає; цілі немає.

## Поле і час
- Нескінченна (на практиці — велика або тор) квадратна сітка; сусідство Мура, 8 сусідів — як у [Life](game-of-life.md).
- Тік = покоління; синхронне оновлення з повного старого стану (подвійний буфер).
- Seeds — 2 стани (on/off); Brian's Brain — 3 стани (on / dying / off).
- «Швидкість світла» c = 1 клітина за тік; більшість кораблів обох автоматів летять із c/1.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вимкнена клітина (off) | tile | стан 0 | вмикається, якщо рівно 2 сусіди on |
| Увімкнена клітина (on, «firing») | tile | стан 1 | наступного тіку → dying (Brain) / off (Seeds) |
| Згасаюча клітина (dying, «refractory») | tile | стан 2, лише Brain | не рахується як on; у ній не можна народитись; наступного тіку → off |
| Космічний корабель | object | швидкість, період | емерджентний: рухається; у Seeds три поширені кораблі мають по 4 on-клітини |
| Граблі / паффер (rake, puffer) | spawner | — | рухаються й лишають слід / випускають інші кораблі |
| Осцилятор | object | період | повторюється на місці; у Brain є осцилятор періоду 3 (4 on + 4 dying) |
| Блок 2×2 on (Brain) | spawner | — | породжує ромб із 4 діагональних хвиль, що розлітаються з c |

## Правила (КОЛИ → ЯКЩО → ТО)
- Seeds: КОЛИ `tick` → ЯКЩО `state(x, off)` and `adjacent_count(x, on, =, 2)` → ТО `set_cell(x, on)`.
- Seeds: КОЛИ `tick` → ЯКЩО `state(x, on)` → ТО `set_cell(x, off)` (S порожнє — жодна клітина не виживає; «кожен патерн — фенікс»).
- Brain: КОЛИ `tick` → ЯКЩО `state(x, off)` and `adjacent_count(x, on, =, 2)` → ТО `set_cell(x, on)`.
- Brain: КОЛИ `tick` → ЯКЩО `state(x, on)` → ТО `set_cell(x, dying)`.
- Brain: КОЛИ `tick` → ЯКЩО `state(x, dying)` → ТО `set_cell(x, off)`; dying-сусіди в `adjacent_count` не рахуються.
- Обидва: усі переходи рахуються зі старого стану й застосовуються разом.
- Наслідок (Brain): dying-хвіст позаду on-клітин забороняє народження назад → патерн рухається в бік «голови» — та сама ідея, що хвіст електрона у Wireworld.
- КОЛИ `input(click, cell)` → ТО `set_cell(cell, selected_state)`; КОЛИ `input(random_fill)` → ТО `custom: «випадковий суп з щільністю p»`.
- Перемоги, поразки й рахунку нема.

## Керування і ввід
- Типовий симулятор (Golly й аналоги): палітра станів, клік/drag малює, гумка; Run/Pause, Step, швидкість; зум і пан.
- Вибір правила: рядок `B2/S` (Seeds) або правило сімейства Generations для Brain (?); випадкове заповнення.

## Вікна, меню, HUD
- `game-screen` (цифрова версія): поле, `element-picker` станів, Run/Pause, `step-button`, `speed-slider`, Clear, Random, `zoom-control`.
- HUD: `generation-counter`, кількість on-клітин (популяція).
- `custom-window` вибору правила/набору патернів; Import/Export RLE (`custom-window`).

## Фічі поза полем
- `step-mode`, `speed-control`, `pause`; `custom-rules` (той самий двіжок, інше правило); `export-import` патернів.
- Колекція патернів Seeds (Jason Summers; внески Stephen Wright, Noam Elkies, David Eppstein) — аналог `puzzle-bank` без прогресу.

## Варіації й родичі
- **Осі варіацій:** кількість станів (2 — Seeds/Life · 3 — Brain · 4 — Wireworld · N — Generations) · правило народження (рівно 2 / 3 / набір) · чи виживають on-клітини (S порожнє — «фенікс») · рефрактерний стан (так/ні) — саме він перетворює хаос Seeds на впорядковані потоки кораблів Brain.
- Родичі в корпусі: [game-of-life](game-of-life.md) (B3/S23; той самий підрахунок сусідів), [wireworld](wireworld.md) (той самий автор; хвіст = рефрактерний стан), [langtons-ant](langtons-ant.md), [cell-machine](cell-machine.md), [elementary-cellular-automata](elementary-cellular-automata.md) (1D-аналог, класи Вольфрама: Seeds — клас III).
- Поза корпусом: моделі збудливих середовищ (Greenberg–Hastings), Star Wars-правило з Generations (?).

## Цікавинки для курсу
- Seeds поверх готового Life-двіжка — 🌱 (змінити таблицю B/S).
- Brain: третій стан + «не рахується в сусідах» — 🌱 (масив int замість bool).
- Узагальнений двіжок Generations (N станів, рядок правила) — 📎.
- Детектор корабля: знайти патерн, що повторився зі зсувом (період, швидкість) — 🥉 (хеш нормалізованого стану).
- Пошук нових кораблів/осциляторів перебором малих стартів — 🥈.

## Мапа на каталог
- Є: `cell-click` · `editor-palette` / `editor-draw-tools` / `editor-erase` / `in-game-editor` · `game-loop` + `game-pause` · `state-as-data` · `level-from-txt` + `import-open-formats` (RLE) · `rule-variants` (B/S, Generations) · `field-scaling` · `logic-render-split` · `unit-tests`.
- **Нема** → пропозиції карток:
  - `+refractory-state` «Стан відпочинку після спрацювання: не рахується й блокує народження» · game-logic · 🌱 · слоти {duration}.
  - Перевикористано: `+cellular-automaton-rule`, `+multi-state-cell`, `+rule-string`, `+step-run-speed`, `+pattern-library`, `+random-soup`.

## Пропозиції до словників
- `+ui:generation-counter` — номер покоління (вже просили Life, Langton, Wireworld).
- `+ui:rule-input` — поле рядка правила.
- `+card:multi-state-cell` — див. Wireworld; тут 3 стани.
- `+card:refractory-state` — див. «Мапа на каталог».
- `+axis:states=n` — кількість станів клітини як вісь опису автоматів (2 / 3 / 4 / N).

## Джерела
- ⭐ [Wikipedia: Brian's Brain](https://en.wikipedia.org/wiki/Brian%27s_Brain) — правило, 3 стани, нейронна аналогія, кораблі й граблі, ромб із блоку 2×2, осцилятор періоду 3.
- [Wikipedia: Seeds](https://en.wikipedia.org/wiki/Seeds_(cellular_automaton)) — B2/S, «фенікс», клас III, кораблі c/1, колекція Summers, назва від Mirek Wójtowicz.
- [Golly](https://golly.sourceforge.io/) — симулятор.
- YouTube: пошук «brian's brain cellular automaton».

## Непевне
- (?) Рік створення обох правил — Wikipedia не дає; у черзі «1990-ті», тому `year: null`.
- (?) Нотація Generations для Brain (`/2/3` у MCell) — з памʼяті, у відкритих сторінках не бачив.
- (?) Поведінка на межі поля (тор чи обрізання) залежить від симулятора.
