---
title: Donsol
slug: donsol
aka: [Donsole]
family: roguelike
also: [board-digital]
klass: cursor
axes:
  field: 1d
  time: turn
  opponent: none
  info: hidden
  random: both
  goal: survive
year: 2015
platforms: [web (HTML5), desktop, mobile, Uxn/Varvara, NES, N64, GBA, NDS, 3DS, paper]
links:
  - {kind: itch, url: "https://hundredrabbits.itch.io/donsol", best: true, note: "Hundred Rabbits: повні правила на сторінці, керування, грати в браузері, ROM-и"}
  - {kind: wiki, url: "https://wiki.xxiivv.com/site/donsol", note: "XXIIVV: правила, втеча, автор John Eternal (Train Jam 2015), релізи"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=donsol+hundred+rabbits+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [hp-damage, inventory-limit, player-death, permadeath, keyboard-controls, cell-click, hover-highlight, restart-level, gui-render, +deck-dungeon, +room-from-deck, +escape-room, +degrading-shield, +potion-sickness]
proposes: ["+trigger:room_dealt", "+trigger:room_cleared", "+cond:last_kill(shield, op, v)", "+cond:skipped_last", "+cond:suit(card, s)", "+effect:deal(n)", "+effect:shuffle_back(cards)", "+effect:equip(card, slot)", "+role:card", "+ui:deck-counter", "+card:degrading-shield", "+card:potion-sickness"]
author: opus
date: 2026-11-09
---

# Donsol — данж зі звичайної колоди: кімната = 4 карти, щит тупішає з кожним блоком

## Суть
Колода з 54 карт (з джокерами) — це підземелля. Гравець тягне 4 карти — «кімнату» — і розігрує їх по одній: ♣♠ і джокери — монстри, ♦ — щити, ♥ — зілля. Головна механіка — **щит, що поглинає шкоду, але після першого блоку працює лише проти слабших монстрів**, і **зілля, що не діють підряд**. Можна раз утекти з кімнати (не двічі поспіль). Дуже близький родич Scoundrel (див. [card-dungeons](card-dungeons.md)), але з іншою математикою карт.

## Поле і час
- «Поле» — ряд із 4 відкритих карт кімнати + колода (закрита) + стан героя (HP, поточний щит). Сітки як такої нема: `field: 1d`.
- Хід = розіграти одну карту кімнати. Кімната закінчується, коли всі 4 карти «згорнуті», тоді тягнуться наступні 4.
- Випадковість — тасування на старті й повторне тасування після втечі (`random: both`); колода закрита — `info: hidden`.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | HP 21 (макс. 21), слот щита | не на полі — стан у панелі |
| Колода | supply | 54 карти | з неї тягнуться кімнати по 4 |
| Монстр ♣/♠ | enemy | 2–10 за номіналом; J 11, Q 13, K 15, A 17 | шкода = значення мінус щит (якщо щит діє) |
| Джокер | boss | 21 | монстр рівня «вбиває з повним HP без щита» |
| Щит ♦ | pickup | 2–10; фігури = 11 | поглинає шкоду; після блоку — лише проти монстрів, слабших за останнього заблокованого |
| Зілля ♥ | pickup | 2–10; фігури = 11 | +HP на значення, не вище 21; друге поспіль — не діє |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «кімната порожня»` → ТО `custom: «витягти 4 карти з колоди»`.
- КОЛИ `input(play monster)` → ЯКЩО `has(hero, shield)` і (`custom: «щит ще не блокував»` або `custom: «значення < останнього заблокованого»`) → ТО `damage(max(0, value − shield))`, `custom: «запамʼятати значення як останнє заблоковане»`.
- КОЛИ `input(play monster)` → ЯКЩО щит є, але `custom: «значення ≥ останнього заблокованого»` → ТО `custom: «щит ламається»`, `damage(value)` повністю.
- КОЛИ `input(play monster)` → ЯКЩО `not has(hero, shield)` → ТО `damage(value)`.
- КОЛИ `input(play shield)` → ТО `custom: «новий щит замінює старий, лічильник блоків скинуто»`.
- КОЛИ `input(play potion)` → ЯКЩО `not state(hero, sick)` → ТО `heal(hero, value)` (стеля 21), `set_state(hero, sick)`; інакше `disappear_b` без ефекту.
- КОЛИ `input(play monster|shield)` → ТО `clear_state(hero, sick)`.
- КОЛИ `input(escape)` → ЯКЩО `custom: «попередню кімнату не тікав»` або `count(monsters in room, ==, 0)` → ТО `custom: «решта карт повертається в колоду, колода тасується»`, нова кімната.
- КОЛИ `hp_zero(hero)` → ТО `lose`.
- КОЛИ `custom: «колоду вичерпано й остання карта розіграна»` → ТО `win`.
- Перемога: пройти всю колоду. Поразка: HP = 0. Рахунок: в оригінальних правилах не описано (?).

## Керування і ввід
- Itch-версія: стрілки — курсор по картах; `Ctrl`/`↑` — обрати (розіграти) карту; `Alt`/`↓` — утекти; `Shift` — рестарт.
- Мобільні й веб-версії — тап/клік по карті й кнопці втечі (?).

## Вікна, меню, HUD
- `game-screen`: 4 карти кімнати, `hp-bar` (HP/21), поточний щит з його останнім блоком, `deck-counter` (скільки лишилось), кнопка втечі (`custom-window`-кнопка), курсор.
- `difficulty-select` — на XXIIVV показано «Difficulty levels» (?) — зміст режимів не розкрито.
- `end-screen` — смерть або прохід колоди (?).
- Переходи: старт → `game-screen` → (HP 0 / колода порожня) → рестарт.

## Фічі поза полем
- `restart-level` (Shift) · кілька платформ із тими самими правилами (Uxn-ROM запускається будь-де).
- Паперова версія — просто колода карт (правила вміщуються на одну сторінку).

## Варіації й родичі
- [card-dungeons](card-dungeons.md) — Scoundrel (2011): 44 карти без червоних фігур, зброя ♦ «зношується» так само порогом, одне зілля на кімнату; Card Crawl, Dungelot, Mini Rogue.
- Різниця з Scoundrel: тут ♦ — **щит** (зменшує вхідну шкоду, ламається), фігури-монстри мають «роздуті» значення 11/13/15/17, джокери 21 = максимум HP; хворіють від зілль **поспіль** (а не «одне на кімнату»).
- Осі варіацій: **деградація захисту** (поріг останнього / злам на рівному / зношування лічильником) · **обмеження лікування** (одне на кімнату / не поспіль / стеля HP) · **втеча** (не поспіль / будь-коли без монстрів).

## Цікавинки для курсу
- Уся гра — консольний пасьянс на ≈120 рядків: колода, кімнати по 4, HP — 🌱.
- Щит з «монотонним» порогом (працює лише на спадаючих значеннях) — стан з памʼяттю останнього — 📎.
- Хвороба від зілль поспіль — прапорець, що знімається іншою дією — 🌱.
- Повернути карти в колоду й перетасувати після втечі — 🌱.
- Солвер/оцінка ймовірності пройти колоду методом Монте-Карло — 🥉.

## Мапа на каталог
- Є: `hp-damage` · `inventory-limit` (один слот щита) · `player-death` · `permadeath` · `keyboard-controls` · `cell-click`/`hover-highlight` (курсор по картах) · `restart-level` · `gui-render`.
- **Нема** → пропозиції карток:
  - `+deck-dungeon` «Данж = колода карт» · levels/generation · 🌱.
  - `+room-from-deck` «Кімната = N карт з колоди, розіграти всі» · levels/generation · 🌱 · слоти {n}.
  - `+escape-room` «Втеча з кімнати з обмеженням» · game-logic/difficulty · 🌱.
  - `+degrading-shield` «Щит лише проти слабших за останнього заблокованого» · entities/combat · 📎.
  - `+potion-sickness` «Лікування підряд не діє» · entities/state · 🌱.

## Пропозиції до словників
- `+trigger:room_dealt` (як у card-dungeons) — кімнату здано; `+trigger:room_cleared` — усі карти кімнати розіграні.
- `+cond:last_kill(shield, op, v)` — порівняння з останнім значенням, яке «зʼїв» предмет (тут — щит); `+cond:skipped_last` — у попередній кімнаті тікав; `+cond:suit(card, s)` — масть карти.
- `+effect:deal(n)` — здати N карт; `+effect:shuffle_back(cards)` — повернути в колоду й перетасувати; `+effect:equip(card, slot)` — покласти в слот.
- `+role:card` — карта як сутність поза полем.
- `+ui:deck-counter` — скільки карт лишилось.
- `+card:degrading-shield` · `+card:potion-sickness`.

## Джерела
- ⭐ [Donsol на itch.io (Hundred Rabbits)](https://hundredrabbits.itch.io/donsol) — правила мастей, значення фігур, втеча, клавіші, платформи.
- [XXIIVV: Donsol](https://wiki.xxiivv.com/site/donsol) — ті самі правила, HP 21, «гра скінчується, коли розіграно останню карту або HP = 0», автор John Eternal, Train Jam 2015.

## Непевне
- (?) Умова перемоги в джерелах прямо не названа («гра скінчується з останньою картою») — трактую як перемогу.
- (?) Режими складності: на XXIIVV є лише зображення «Difficulty levels» без тексту; в памʼяті — Easy/Normal/Expert зі зміною правил щита (?).
- (?) Чи кінець кімнати — після 4 розіграних карт, чи лишається одна, як у Scoundrel: джерело каже «room ends when all the cards are folded» → усі 4.
- (?) Рахунок/рекорд у цифрових версіях — не бачив.
