---
title: Catrap (Pitman)
slug: catrap
family: grid-platformer
also: [push-slide, dig-gravity]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: collect
year: 1985
platforms: [Sharp MZ-700 (1985), Game Boy (1990), i-mode (2004–2007), 3DS Virtual Console (2011)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Catrap", best: true, note: "версії, 100 раундів, відкат кнопкою A, редактор, історія Pitman/Power Paws"}
  - {kind: other, url: "https://ja.wikipedia.org/wiki/PITMAN", note: "JP-стаття: камені, копання ґрунту, «перемогти всіх ворогів», раунди 1–99 у довільному порядку"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=catrap+game+boy+gameplay", note: "пошук; геймплей GB"}
stage: v1
coverage: 70
mechanics: [move-4dir, gravity-fall, push-object, impassable-cells, destroy-all-enemies, touch-death, level-select, in-game-editor, editor-palette, editor-erase, editor-playtest, game-screen, main-menu, sound-effects, +ladder-climb, +rewind, +party-switch, +destructible-blocks, +undo-redo, +stack-climb, +move-counter-scrub]
proposes: ["+trigger:input", "+effect:fall", "+effect:undo", "+role:terrain", "+feature:rewind", "+axis:undo", "+axis:actors", "+ui:move-counter", "+ui:character-indicator", "+window:editor-window", "+card:move-counter-scrub"]
author: opus
date: 2026-11-02
---

# Catrap — двоє котів-копачів з гравітацією і першим «відмотуванням» ходів на консолі

## Суть
Бічна кімната-пазл: кіт (у частині раундів — двоє котів, між якими перемикаєшся) штовхає камені, копає ґрунт, лазить драбинами й має «вибити» всіх монстрів і привидів, просто зайшовши в них. Стрибати не можна, а все незакріплене — коти, камені, монстри — падає під дією гравітації, тож кожен крок незворотно змінює рельєф. Головна знахідка: кнопка відкату ходів назад аж до початку раунду — одна з найраніших реалізацій «rewind» у пазлі, через що гра вважається попередницею Braid-подібного відкату (Destructoid: «працює як UNDO, а не подорож у часі»).

## Поле і час
- Один екран-кімната, бічний вид, квадратна сітка (GB — приблизно 10×8 клітин (?)); камери нема, усе видно.
- Час — покроковий: кожне натискання = один крок кота, після нього домальовується падіння; вороги нерухомі (?), тож тиску часу нема.
- Шари: стіни/цегла (статичні), ґрунт (руйнівний), драбини (прохідний шар поверх порожнечі), рухомі обʼєкти (коти, камені, монстри).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кіт (Pit Boy / Pit Girl) | player | 1–2 на раунд | ходить ліво/право, лізе драбиною, падає без опори; стрибати не вміє |
| Камінь (boulder) | object | — | штовхається на 1 клітину вбік, якщо за ним вільно; падає без опори; є опорою для кота |
| Ґрунт (soil) | object | — | кіт заходить у нього → клітина зникає (копання) |
| Стіна / цегла | static | — | непрохідна, опора |
| Драбина | terrain | — | дозволяє рух угору/вниз; на ній кіт не падає |
| Монстр | enemy | — | нерухомий (?); падає без опори (?); кіт заходить у нього → монстр вибитий з екрана |
| Привид | enemy | — | як монстр; чи падає — (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `free(next)` → ТО `move(cat, dir)`.
- КОЛИ `input(left|right)` → ЯКЩО `occupied(next, boulder)` і `free(cell_behind)` → ТО `push`, `move(cat, dir)`; інакше `block`.
- КОЛИ `input(left|right)` → ЯКЩО `occupied(next, soil)` → ТО `disappear_b` (копання), кіт лишається чи заходить — (?).
- КОЛИ `contact(cat, monster|ghost)` → ТО `disappear_b`, `counter(enemies_left, -1)`.
- КОЛИ `input(up|down)` → ЯКЩО `cell(here|target, ladder)` → ТО `move(cat, dir)`; інакше `block`.
- КОЛИ `after(move)` → ЯКЩО `not supported(a)` і `not cell(a, ladder)` → ТО `fall(a)` для кота, каменя, монстра (порядок падіння — знизу вгору (?)).
- КОЛИ `fall(boulder)` → ЯКЩО внизу кіт → ТО `custom: «камінь лягає на кота / кіт гине»` (?).
- КОЛИ `input(switch)` → ТО `custom: «керування переходить до іншого кота»`.
- КОЛИ `input(rewind)` → ТО `custom: «стан повертається на 1 крок назад; утримання — безперервно до початку раунду»`.
- КОЛИ `all_gone(enemy)` → ТО `win`, `next_level` (раунд зараховано).
- Поразка: формально нема — застряг → відкат або рестарт раунду. Рахунок: нема, лише позначка «пройдено».

## Керування і ввід
- Хрестовина — крок; A — відкат ходу (за Wikipedia); утримання — швидкий відкат; перемотка вперед — (?).
- Select/B — перемкнути кота (?).
- Start — меню раунду / вибір раунду.

## Вікна, меню, HUD
- `splash-screen` → `main-menu`: Play · Edit (редактор) (?).
- `level-select` — номер раунду 1–99, будь-який порядок; сотий відкривається після всіх (JP wiki).
- `game-screen` — кімната + смуга внизу: номер раунду, `custom: «лічильник кроків для відкату»` (?), індикатор активного кота (?).
- `editor-window` — та сама кімната з курсором і палітрою елементів (?).
- Переходи: main-menu → level-select → game-screen → (усі вороги вибиті) → level-select/наступний раунд; main-menu → editor-window → game-screen (тест).

## Фічі поза полем
- `rewind` / `undo` (∞ кроків до старту раунду) — ключова фіча; рестарт фактично не потрібен.
- `level-select` з відкриттям 100-го раунду після всіх 99; збереження прогресу на GB — (?) (картридж без батареї?).
- `level-editor` — «гравці можуть створювати свої лабіринти» (Wikipedia); чи зберігаються після вимкнення — (?).
- Нема таймера, очок, життів.

## Варіації й родичі
- MZ-700 (1985, type-in BASIC у Oh!MZ) → Game Boy (1990, ASK Kodansha / Asmik) → i-mode Pitmania 1/2/Infinite → 3DS VC (2011); у GB раунд 77 викладений літерами M і Z на честь оригіналу.
- Родичі: Lode Runner (бічна сітка, драбини, копання), Boulder Dash (камені й ґрунт), Kwirk і Solomon's Key (бічні пазл-кімнати), Toki Tori і Braid (rewind).
- Осі: **відкат** (нема / рестарт / undo N / rewind ∞); **кількість аватарів** (1 / 2 з перемиканням / кооп); **хто підлягає гравітації** (лише гравець / обʼєкти / вороги теж).

## Цікавинки для курсу
- Rewind як стек повних станів поля з безперервним відкатом і лічильником — 🥈 (state-as-data + історія).
- Гравітація для всіх рухомих сутностей після кожного кроку з правильним порядком падіння — 🥉.
- Перемикання між двома котами, які можуть ставати опорою один одному — 🥉.
- Ворог-«ціль», що не рухається, але падає: ворог як обʼєкт пазла, а не загроза — 📎.
- Редактор кімнат 10×8 з тестом — 🥈 (як у картки `in-game-editor`).

## Мапа на каталог
- Є: `move-4dir` (ліво/право + драбина) · `gravity-fall` · `push-object` · `impassable-cells` · `destroy-all-enemies` · `touch-death` (?) · `level-select` · `in-game-editor` + `editor-palette` + `editor-erase` + `editor-playtest` · `game-screen` · `main-menu`.
- **Нема** → пропозиції карток:
  - `+ladder-climb` «Драбини» · entities/move · 📎 (спільна з Lode Runner, Toki Tori).
  - `+rewind` «Безперервний відкат часу» · game-logic/save · 🥈 (як у Toki Tori).
  - `+undo-redo` «Undo/redo ходів» · game-logic/flow · 🥉.
  - `+party-switch` «Кілька аватарів з перемиканням» · entities/move · 🥉.
  - `+destructible-blocks` «Руйновані блоки» · entities/interact · 🌱 — ґрунт зникає при вході.
  - `+stack-climb` «Підйом на інші фігури» · entities/state · 🥉 — кіт стоїть на камені/іншому коті.
  - `+move-counter-scrub` «Лічильник кроків як шкала перемотки» · interface/hud · 📎 — номер кроку видно, відкат крутить його назад.

## Пропозиції до словників
- `+trigger:input` — натискання гравця (крок, відкат, перемикання).
- `+effect:fall` — падіння до опори після кроку; `+effect:undo` — повернути попередній стан.
- `+role:terrain` — драбина: на ній стоять/лізуть, не падають.
- `+feature:rewind` — безперервний відкат (Catrap прямо названий у `features.md`).
- `+axis:undo` = `rewind`; `+axis:actors` = `party` (2 коти).
- `+ui:move-counter` (лічильник кроків для відкату), `+ui:character-indicator` (хто зараз активний).
- `+window:editor-window` — редактор кімнат.
- `+card:move-counter-scrub` — див. вище.

## Джерела
- ⭐ [Wikipedia: Catrap](https://en.wikipedia.org/wiki/Catrap) — 100 раундів, відкат кнопкою A, редактор, MZ-700/GB/i-mode/3DS, назви Pitman і Power Paws.
- [ja.wikipedia: PITMAN](https://ja.wikipedia.org/wiki/PITMAN) — штовхання каменів, копання ґрунту, мета «перемогти всіх ворогів», раунди 1–99 у будь-якому порядку, 100-й в кінці.
- YouTube: пошук «catrap game boy gameplay».

## Непевне
- (?) Перемикання котів: Wikipedia лише каже «двоє котів», яка кнопка і чи в усіх раундах — не перевірено.
- (?) Чи можна перемотати вперед після відкату (VCR-подібно), чи лише назад; чи показується лічильник кроків.
- (?) Чи падають монстри/привиди і чи вбиває камінь кота; чи рухаються вороги взагалі.
- (?) Розмір кімнати на GB; збереження прогресу й саморобних рівнів без батареї.
- WebSearch вичерпано, StrategyWiki (403) і HG101 (на обслуговуванні) недоступні — частина правил з памʼяті.
