---
title: A Good Snowman Is Hard to Build
slug: a-good-snowman-is-hard-to-build
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2015
platforms: [PC, iOS, Android, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/A_Good_Snowman_Is_Hard_to_Build", best: true, note: "правила: три кулі спадного розміру, ріст на снігу, кімнати живоплоту, undo по ходу і reset кімнати"}
  - {kind: official, url: "https://agoodsnowman.com/", note: "офіційний сайт: автори, платформи, «pay what the temperature is» на itch.io"}
  - {kind: steam, url: "https://store.steampowered.com/app/316610/A_Good_Snowman_Is_Hard_To_Build/", note: "сторінка Steam"}
  - {kind: other, url: "https://www.pcgamer.com/uk/a-good-snowman-is-hard-to-build-trailer-introduces-the-charming-chilly-puzzler", note: "новина з трейлером"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=a+good+snowman+is+hard+to+build+gameplay", note: "пошук; геймплей"}
  - {kind: play, url: "https://www.puzzlescript.net/", note: "PuzzleScript — рушій, у якому зроблено прототип (2014); сам прототип не знайдено"}
stage: v1
coverage: 75
mechanics: [move-4dir, keyboard-controls, swipe-gestures, push-object, floor-types, cell-transform, impassable-cells, sequential-levels, level-unlock, save-progress, movement-animation, background-music, +undo-redo, +grow-on-terrain, +stack-by-size, +terrain-consumed, +world-map]
proposes: ["+trigger:input", "+cond:same", "+cond:compare", "+cond:cell", "+effect:grow", "+effect:set_cell", "+effect:attach", "+effect:move", "+role:terrain", "+window:map-window", "+feature:undo", "+feature:world-map", "+axis:undo"]
author: opus
date: 2026-11-02
---

# A Good Snowman Is Hard to Build — котити сніжки, що ростуть на снігу, і складати сніговиків

## Суть
Чорний монстрик у саду-лабіринті з живоплоту ліпить сніговиків: треба поставити три кулі — велику, середню, малу — одна на одну. Куля, прокочена по снігу, **росте на один розмір і з'їдає сніг** під собою, лишаючи траву; по траві котиться без змін. Монстр лише штовхає, по одній кулі; тож ресурс (сніг) витрачається незворотно, і порядок прокочування вирішує все. Кімнати саду — окремі пазли; збудовані в кімнаті сніговики відкривають сусідні.

## Поле і час
- Квадратна сітка, вигляд зверху; сад — неперервний світ із кімнат, розділених живоплотом; камера показує поточну кімнату/область.
- Клітина має шар підлоги (сніг / трава) і шар обʼєкта (куля, стос куль, монстр, живопліт, дерево/лавка).
- Покроково: хід = крок монстра (з можливим поштовхом).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Монстр | player | — | крок у 4 напрямки; штовхає одну кулю; на кулі не стає |
| Мала куля | object | розмір 1 | котиться на 1; на снігу → середня |
| Середня куля | object | розмір 2 | котиться на 1; на снігу → велика |
| Велика куля | object | розмір 3 | котиться на 1; на снігу не росте, але сніг з'їдає (?) |
| Стос (2 кулі) | object | низ > верх | низ не рухається; поштовх скочує верхню кулю (?) |
| Сніговик | static | 3 кулі 3>2>1 | готовий, отримує обличчя, більше не рухається (?) |
| Сніг | terrain | — | куля на ньому росте; сніг → трава |
| Трава | terrain | — | куля котиться без змін |
| Живопліт / дерева / лавки | static | — | непрохідні для монстра й куль |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(target)` → ТО `move(monster, dir)`.
- КОЛИ `contact(monster, ball)` → ЯКЩО `free(cell_behind)` → ТО `push`; ЯКЩО `occupied(cell_behind, ball)` і розмір там більший → ТО `attach(ball, on_top)` (поставити зверху); інакше `block`.
- Ланцюгом кулі не штовхаються: куля перед кулею = `block` (якщо не стос).
- КОЛИ `enter(ball, snow)` → ЯКЩО `custom: «розмір < 3»` → ТО `grow(ball, 1)`; у всіх випадках `set_cell(grass)`.
- КОЛИ `enter(ball, grass)` → ТО нічого.
- КОЛИ `contact(monster, stack)` → ТО `custom: «верхня куля скочується в наступну клітину за тими ж правилами (на вільне, на сніг з ростом або на більшу кулю)»` (?).
- КОЛИ `custom: «стос: велика + середня + мала»` → ТО `transform(snowman)`, `counter(snowmen_left, -1)`.
- КОЛИ `counter(snowmen_left, ==, 0)` у кімнаті → ТО `unlock(adjacent_rooms)`.
- Поразки нема: кулю, що виросла не туди, або витрачений сніг повертає лише undo/reset кімнати. Рахунку нема.

## Керування і ввід
- Стрілки/WASD — крок; Z — undo на один хід; R — reset кімнати.
- Мобільні: свайп у напрямку, кнопки undo/reset на екрані.
- Геймпад на Switch.

## Вікна, меню, HUD
- `splash-screen` / `main-menu` — продовжити, налаштування (?).
- `map-window` — не окреме вікно: сад-лабіринт сам є хабом, монстр ходить між кімнатами; на вході в кімнату вона стає пазлом.
- `game-screen` — поле кімнати; HUD мінімальний: кнопки undo/reset (мобільні), без лічильників.
- `settings-window` — звук/музика (?).
- `end-screen` — сніговики оживають/фінальна сцена після всіх кімнат (?).
- Переходи: main-menu → сад → (кімната) пазл → (усі сніговики) сусідні кімнати відкриті.

## Фічі поза полем
- `undo` (по одному ходу) + `restart-level` (reset кімнати); `autosave`.
- `world-map` у вигляді ходильного саду + `level-unlock` сусідніх кімнат.
- `achievements` (Steam); `music-toggle`/гучність (?). Підказок і редактора нема (?).

## Варіації й родичі
- Прототип у PuzzleScript (2014); автор пазлів Alan Hazelden (також Sokobond, A Monster's Expedition, Cosmic Express).
- Родичі: Sokoban (лише штовхання), Stephen's Sausage Roll (стан обʼєкта міняється поштовхом), Katamari (ріст від прокочування — у real-time 3D).
- **Осі варіацій:** ріст — немає / від терену / від інших обʼєктів; ресурс — нескінченний / витрачається клітиною; стекування — немає / за розміром / за кольором.

## Цікавинки для курсу
- Ріст обʼєкта від типу клітини + витрата терену (сніг → трава) — 🥉: дві взаємодії в одному поштовху.
- Стекування за правилом «менше на більше» з перевіркою готового сніговика — 🥉.
- Скочування верхньої кулі зі стосу — 📎.
- Кімнати-пазли всередині ходильного хабу з відкриттям сусідів — 🥉.
- Розвʼязувач кімнати (BFS по станам: позиції й розміри куль + маска снігу) — 🥇; маска снігу робить простір станів показово великим.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` + `swipe-gestures` ↔ ввід; `push-object` ↔ кулі; `floor-types` ↔ сніг/трава; `cell-transform` ↔ сніг → трава (тут змінюється і клітина, і обʼєкт); `impassable-cells` ↔ живопліт; `sequential-levels` + `level-unlock` + `save-progress` ↔ сад; `movement-animation` ↔ перекочування; `background-music` ↔ саундтрек Priscilla Snow.
- **Нема** → пропозиції карток:
  - `+undo-redo` «Undo ходів у грі» · game-logic/flow · 📎.
  - `+grow-on-terrain` «Обʼєкт росте, проходячи терен» · entities/state · 📎 · слот {max_size: 3}.
  - `+stack-by-size` «Стекування менше на більше» · entities/legality · 🥉.
  - `+terrain-consumed` «Терен витрачається при використанні» · entities/interact · 📎 — дитина `cell-transform`.
  - `+world-map` «Ходильний хаб із кімнатами-рівнями» · levels/progression · 🥉.

## Пропозиції до словників
- `+trigger:input`.
- `+cond:same(a, b, size)` / порівняння розмірів — потрібне `+cond:compare(a, b, prop, op)` для «більший за» (стекування); `+cond:cell` — тип клітини під кулею.
- `+effect:grow`, `+effect:set_cell`, `+effect:attach` (поставити на стос), `+effect:move` — кандидати, тут основні.
- `+role:terrain` — сніг і трава.
- `+window:map-window` — хаб як ходильний світ; `+feature:undo`, `+feature:world-map`.
- `+axis:undo` — `unlimited` по одному ходу + reset кімнати.

## Джерела
- ⭐ [Wikipedia: A Good Snowman Is Hard to Build](https://en.wikipedia.org/wiki/A_Good_Snowman_Is_Hard_to_Build) — три кулі спадного розміру, ріст на снігу, кімнати відкривають сусідні, undo/reset, PuzzleScript-прототип.
- [Офіційний сайт](https://agoodsnowman.com/) — автори, платформи.
- [Steam](https://store.steampowered.com/app/316610/A_Good_Snowman_Is_Hard_To_Build/).
- [PC Gamer: трейлер](https://www.pcgamer.com/uk/a-good-snowman-is-hard-to-build-trailer-introduces-the-charming-chilly-puzzler).
- YouTube: [пошук «a good snowman is hard to build gameplay»](https://www.youtube.com/results?search_query=a+good+snowman+is+hard+to+build+gameplay).

## Непевне
- (?) Велика куля на снігу з'їдає сніг — з огляду («найбільшою кулею розчищають шлях»), але не з правил гри.
- (?) Як саме рухається стос при поштовху (скочується верхня куля) і чи можна розібрати готового сніговика.
- (?) Post-game: після всіх сніговиків є друга частина/«сон» з іншими правилами — не перевірено.
- (?) Кількість сніговиків/кімнат, меню й налаштування — з памʼяті або не знайдено.
- (?) PuzzleScript-прототип 2014 року онлайн не знайдено; дано лінк на сам рушій.
