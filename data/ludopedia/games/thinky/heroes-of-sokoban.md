---
title: Heroes of Sokoban
slug: heroes-of-sokoban
aka: [Heroes of Sokoban I]
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
year: 2013
platforms: [web]
links:
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=6860122", best: true, note: "грати в браузері; 22 рівні з навчальними підписами"}
  - {kind: other, url: "https://api.github.com/gists/6860122", note: "вихідний код PuzzleScript (gist): OBJECTS, 22 правила, WINCONDITIONS, рівні"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Heroes+of+Sokoban+puzzlescript", note: "пошук; проходження"}
stage: v1
coverage: 75
mechanics: [move-4dir, move-by-input, push-object, pull-object, party-switch, swap-on-contact, teleport, button-toggle, key-and-door, impassable-cells, all-on-targets, undo-unlimited, restart-level, sequential-levels, keyboard-controls, sound-effects, +hold-all-switches, +chain-push, +line-of-sight-swap, +heroes-as-objects]
proposes: ["+card:line-of-sight-swap", "+card:heroes-as-objects", "+card:chain-push", "+effect:cast_ray", "+window:title-screen", "+window:message-screen"]
author: opus
date: 2026-11-09
---

# Heroes of Sokoban — три герої з різними дієсловами (штовхати, тягти, мінятися) і одна мета: усі на виходах

## Суть
Sokoban з партією: Воїн штовхає, Злодій тягне, Чарівник міняється місцями з першим блоком на лінії руху. Активний один; кнопка дії передає керування наступному. Неактивні герої — такі самі обʼєкти, як ящики: їх можна штовхати, тягти й ними мінятися («Heroes can move each other»). Мета — поставити кожного героя на окрему ціль, використовуючи кольорові кнопки й двері.

## Поле і час
- Квадратна сітка, один екран на рівень; 22 рівні в коді, перші вісім з підписом-навчанням.
- Шари колізій (з коду): фон → службовий `Temp` → ціль / кнопка / відчинені двері / `ShadowDoor` → тверді (стіна, зачинені двері, герої, ящики).
- Покроково: тік = ввід гравця; `key_repeat_interval 0.25` — утримання клавіші повторює крок.
- Промінь Чарівника (`Temp`) — службовий обʼєкт, пробігає порожні клітини за один хід і зникає в `late`; гравець бачить лише результат.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Воїн (`Fighter`, червоний) | player | активний / `SFighter` неактивний | крок 4 напрямки; штовхає ящик або неактивного героя, разом з усім ланцюгом за ним |
| Злодій (`Thief`, зелений) | player | активний / `SThief` | крок 4 напрямки; тягне ящик/героя, що стоїть позаду; штовхати не вміє |
| Чарівник (`Wizard`, синій) | player | активний / `SWizard` | хід = промінь уперед по порожніх клітинах; перший ящик/герой на шляху — обмін місцями; стіна — звичайний крок |
| Неактивний герой (`SPlayer`) | object | — | стоїть; для інших героїв — `Moveable`, як ящик; тисне на кнопку |
| Ящик (`Crate`) | object | — | штовхає Воїн, тягне Злодій, обмінюється Чарівник; тисне на кнопку |
| Стіна (`Wall`) | static | — | непрохідна; зупиняє промінь Чарівника |
| Жовта / фіолетова кнопка (`YellowSwitch`, `PurpleSwitch`) | switch | колір | натиснута, поки на ній ящик або будь-який герой |
| Жовті / фіолетові двері (`YellowDoor`, `PurpleDoor`) | gate | колір; зачинені / відчинені | відчинені, лише поки натиснуті **всі** кнопки свого кольору; зачинені — як стіна (`Static`) |
| Ціль (`Goal`) | static | — | клітина, на якій має стояти герой |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell_ahead)` → ТО `move(active, dir)`.
- КОЛИ `contact(fighter, moveable)` → ТО `push`; КОЛИ `custom: «рухомий Moveable впирається в інший Moveable»` → ЯКЩО `custom: «на полі є Воїн»` → ТО `push` — ланцюг будь-якої довжини; упор у стіну → `block` усього ланцюга.
- КОЛИ `input(dir)` → ЯКЩО `turn_of(thief)` and `occupied(cell_behind, moveable)` → ТО `move(thief, dir)`, `pull(moveable)`.
- КОЛИ `contact(thief, moveable)` → ТО `block` (Злодій не штовхає).
- КОЛИ `input(dir)` → ЯКЩО `turn_of(wizard)` → ТО `custom: «промінь Temp летить у напрямку руху крізь клітини без Moveable і без Static»`.
- КОЛИ `custom: «промінь упирається в Moveable»` → ТО `swap(wizard, moveable)`, `sound(teleport)`.
- КОЛИ `custom: «промінь упирається в Static (стіна, зачинені двері)»` → ТО `move(wizard, dir)` — звичайний крок, який блокується, якщо стіна поруч.
- КОЛИ `after(move)` → ТО `custom: «Temp прибирається (late)»`.
- КОЛИ `input(action)` → ТО `set_state(active, inactive)`, `custom: «керування переходить до наступного героя в циклі Воїн → Злодій → Чарівник → Воїн, відсутніх пропускає»`, `sound(switch)`.
- КОЛИ `custom: «кінець ходу (late)»` → ЯКЩО `custom: «на кожній кнопці кольору X стоїть ящик або герой»` → ТО `set_state(doors_X, open)`, `sound(open)`.
- КОЛИ `custom: «кінець ходу (late)»` → ЯКЩО `custom: «хоч одна кнопка кольору X порожня»` → ТО `set_state(doors_X, closed)`, `sound(close)`.
- КОЛИ `all_on(hero, goal)` → ЯКЩО `custom: «кожна ціль зайнята героєм»` → ТО `win`, `next_level` (умови коду: «All Hero on Goal» і «All Goal on Hero»).
- Перемога: усі герої (і активний, і неактивні) на цілях · Поразки нема — глухий кут знімає `undo` / `restart` · Рахунку нема.

## Керування і ввід
- Стрілки / WASD — крок активного героя (для Чарівника — «постріл» обміном у цьому напрямку).
- `X` / пробіл (action у PuzzleScript) — передати керування наступному героєві.
- `Z` — undo, `R` — рестарт, `Esc` — меню (стандарт PuzzleScript).

## Вікна, меню, HUD
- `title-screen` (custom, стандарт PuzzleScript): назва, автор Jonah Ostroff, start / continue.
- `game-screen`: лише поле; активного героя видно за спрайтом (неактивні — `S*`-версії), HUD нема.
- `message-screen` (custom): підписи-навчання між рівнями («Walk to the exit.», «Red warrior pushes blocks.», «Hold down switches to open doors.», «Press multiple switches at once.», «Green thief pulls blocks.», «Blue wizard teleports to blocks.», «Press action to switch heroes.», «Heroes can move each other.»), фінал «Thanks for playing!».
- Переходи: title → рівні підряд з повідомленнями → фінал → title.

## Фічі поза полем
- `undo` ∞, `restart-level` — стандарт рушія.
- `levels-sequential`: 22 рівні, без вибору; `continue` на титулі (?).
- `tutorial` — вбудований підписами: кожен новий герой чи елемент вводиться окремим рівнем.
- Відкритий код (`mod-support` через «hack» у редакторі PuzzleScript).

## Варіації й родичі
- Родичі в корпусі: [Kwirk](../push-slide/kwirk.md) (кілька аватарів, Select), [Sokoban](../push-slide/sokoban.md), [Baba Is You](baba-is-you.md) (PUSH / PULL / SWAP як властивості), [Mirror Isles](mirror-isles.md) (обмін з образом), [Snakebird](snakebird.md) (кілька аватарів, що штовхають одне одного).
- Наступники того ж автора — Heroes of Sokoban II / III (?).
- Осі варіацій: **дієслово героя** — штовхати (ланцюгом) / тягти / мінятися на відстані; **неактивний герой** — перешкода (Kwirk) / рухомий обʼєкт (тут); **двері** — від однієї кнопки / від усіх кнопок кольору (тут); **обмін** — з будь-яким обʼєктом на лінії / лише з сусіднім (Baba SWAP).

## Цікавинки для курсу
- Три герої з різними функціями руху за спільним інтерфейсом «хід = дієслово(напрям)» — 🥉 (поліморфізм на сітці, ідеальне завдання на класи).
- Обмін Чарівника з першим блоком на лінії: трасування променя по клітинах до першої перешкоди, далі розгалуження «рухоме / тверде» — 📎.
- Ланцюгове штовхання будь-якої довжини лише для Воїна — 📎.
- Неактивні герої як ящики: одна сутність змінює роль `player` ↔ `object` за станом — 🥉.
- Двері, відчинені лише поки натиснуті всі кнопки кольору (перерахунок щоходу в `late`) — 📎.
- Розвʼязувач BFS по станах (позиції 3 героїв + ящиків + активний) — 🥇.

## Мапа на каталог
- Є: `move-4dir` · `move-by-input` · `push-object` (Воїн) · `pull-object` (Злодій) · `party-switch` (action) · `swap-on-contact` і `teleport` — найближче до обміну Чарівника · `button-toggle` + `key-and-door` (кольорові кнопки й двері) · `impassable-cells` · `all-on-targets` · `undo-unlimited` · `restart-level` · `sequential-levels` · `keyboard-controls` · `sound-effects`.
- **Нема** → пропозиції карток:
  - `+line-of-sight-swap` «Обмін місцями з першим обʼєктом на лінії» · entities/interact · 📎 · слоти {targets: moveable, on_wall: step|block}.
  - `+heroes-as-objects` «Неактивний аватар — рухомий обʼєкт для інших» · entities/state · 🥉 — дитина `party-switch`.
  - `+chain-push` «Штовхання ланцюга з кількох обʼєктів» · entities/legality · 📎 · слот {max_len} — дитина `push-object`.
  - `+hold-all-switches` (повтор корпусу) — двері відчинені, поки натиснуті всі кнопки кольору.

## Пропозиції до словників
- `+effect:cast_ray` — пустити службовий промінь до першої перешкоди й повернути, у що він уперся (Чарівник; Mirror Isles має схоже).
- `+card:line-of-sight-swap`, `+card:heroes-as-objects`, `+card:chain-push` — див. вище.
- `+window:title-screen`, `+window:message-screen` — повтор пропозицій Mirror Isles (стандартні екрани PuzzleScript).
- ⏳-слова, вжиті тут: `input`, `free`, `occupied`, `turn_of`, `move`, `pull`, `swap`, `set_state`, `sound`, `after`, `all_on`, `next_level`, ролі `switch`, `gate`.

## Джерела
- ⭐ [Heroes of Sokoban на puzzlescript.net](https://www.puzzlescript.net/play.html?p=6860122) — гра в браузері.
- [Gist з кодом через GitHub API](https://api.github.com/gists/6860122) — метадані (автор Jonah Ostroff, створено 2013-10-06), обʼєкти, шари, усі 22 правила, умови перемоги, 22 рівні й тексти повідомлень.
- YouTube: пошук «Heroes of Sokoban puzzlescript».

## Непевне
- (?) Що стається, коли двері зачиняються на герої чи ящику, що стоїть у прорізі: правило `late` пише `YellowDoor` у клітину, а двері й герої в одному шарі колізій — можливо, обʼєкт зникає; у грі не перевірено.
- (?) Чи Воїн штовхає ланцюг, у якому є неактивний Чарівник/Злодій, — за кодом так (обидва `Moveable`).
- (?) Сиквели Heroes of Sokoban II / III — з памʼяті; сайт автора jonahostroff.com не відповідає.
- (?) Черга дала рік 2014 — gist створено 2013-10-06.
- (?) Призначення клавіш action/undo — стандарт PuzzleScript, у коді гри не задано.
