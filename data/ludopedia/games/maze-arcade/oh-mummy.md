---
title: Oh Mummy
slug: oh-mummy
aka: [Oh Mummy!]
family: maze-arcade
also: []
klass: avatar
axes:
  field: graph
  time: realtime
  opponent: ai
  info: hidden
  random: setup
  goal: collect
year: 1983
platforms: [ZX Spectrum, Camputers Lynx, Amstrad CPC (1984), MSX, Tatung Einstein, C64]
links:
  - {kind: play, url: "https://c64.krissz.hu/oh-mummy/play-online", best: true, note: "інструкція C64-версії: 20 блоків, 10 скарбів / 6 порожніх / по одному мумія, вартовий, ключ, сувій; 5 членів команди; 5 рівнів skill і speed; грати в браузері"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Oh_Mummy", note: "сліди, обведення блоку відкриває вміст, ключ + гробниця для виходу, сувій, відкрита мумія йде на наступний рівень, гра по черзі"}
  - {kind: other, url: "https://everygamegoing.com/larticle/gameplay-amstrad-oh-mummy/5765", note: "Personal Computer News (1984): 5 рядів по 4 блоки, вміст, життя або очки між пірамідами, опції"}
  - {kind: other, url: "https://www.everygamegoing.com/larticle/Oh-Mummy-000/25780", note: "Amstrad Action: 5 рівнів у піраміді, сувій проти одного вартового, план пірамід не змінюється"}
  - {kind: other, url: "https://www.worldofspectrum.org/pub/sinclair/games-info/o/OhMummy.txt", note: "інструкція ZX: клавіші A/Z/K/L, перевизначення, джойстик"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Oh+Mummy+Amstrad+gameplay", note: "пошук; геймплей Amstrad"}
stage: v1
coverage: 65
mechanics: [move-4dir, visited-trail, item-pickup, key-and-door, reach-exit, chase-player, touch-death, player-death, temporary-modes, event-points, sequential-levels, progress-acceleration, difficulty-levels, game-settings, hot-seat, keyboard-controls, controls-remap, background-music, sound-effects, status-panel, game-screen, +line-paint-box-fill, +box-surround-reveal, +hidden-content-mix, +release-on-reveal, +one-hit-shield, +enemy-carry-over, +set-completion-reward]
proposes: ["+card:box-surround-reveal", "+card:hidden-content-mix", "+card:release-on-reveal", "+card:one-hit-shield", "+card:enemy-carry-over", "+card:set-completion-reward"]
author: opus
date: 2026-11-09
---

# Oh Mummy — обійди блок гробниці слідами, і він покаже, що в ньому: скарб, ключ, сувій чи мумію

## Суть
Археолог ходить коридорами між 20 блоками гробниці й лишає сліди. Блок, обійдений слідами з усіх чотирьох боків, відкривається: там скарб, порожнеча, королівська мумія, ключ, сувій або вартовий-мумія, що одразу виходить на полювання. Вихід відкривається, коли знайдено ключ і королівську мумію, тож гравець вирішує, скільки ще блоків ризикнути обійти заради скарбів. Ядро — Amidar-обведення, де нагорода прихована, а частина «нагород» — вороги.

## Поле і час
- Поле — регулярна гратка: 5 рядів по 4 блоки (20 блоків), між ними коридори; гравець і мумії ходять лише коридорами — фактично граф ребер навколо прямокутників.
- Блок відкривається, коли пройдено всі чотири його сторони «від кута до кута»; спільна сторона рахується для обох сусідніх блоків (?).
- Real-time, один нерухомий екран. Піраміда = 5 рівнів з тим самим планом; кожен наступний трохи складніший, нова піраміда — вартові уважніші.
- Вміст блоків на рівні (C64): 10 скарбів, 6 порожніх і по одному: королівська мумія, вартовий, ключ, сувій.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Археолог (команда) | player | 5 членів команди (C64) | рух 4 напрямки коридорами, лишає сліди |
| Слід | mark | — | позначає пройдений відрізок коридору |
| Блок гробниці | container | вміст прихований | відкривається, коли всі 4 сторони в слідах |
| Скарб (скриня) | pickup | 10 на рівень | очки при відкритті |
| Порожній блок | — | 6 на рівень | нічого не дає |
| Королівська мумія (саркофаг) | pickup | 1 на рівень | очки; разом із ключем відкриває вихід |
| Ключ | pickup | 1 на рівень | разом із королівською мумією відкриває вихід |
| Сувій | pickup | 1 на рівень, діє лише на цьому рівні | захищає від одного вартового, знищуючи його |
| Вартовий у блоці | enemy | 1 на рівень | спить у блоці; відкриття випускає його в погоню |
| Вартовий-мисливець | enemy | 1 з початку рівня | ходить коридорами за гравцем; розум задає skill і піраміда |
| Вихід | gate | — | пропускає на наступний рівень після ключа й мумії |
| Коридори й стіни блоків | static | 4 × 5 блоків | рух лише коридорами |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell_ahead)` → ТО `move(player, dir)`, `mark(cell, footprint)`.
- КОЛИ `pattern(region_closed)` (усі 4 сторони блоку в слідах) → ТО `reveal(block)`.
- КОЛИ `pattern(region_closed)` → ЯКЩО `occupied(block, treasure)` → ТО `score(+treasure)`.
- КОЛИ `pattern(region_closed)` → ЯКЩО `occupied(block, royal_mummy)` → ТО `score(+royal)`, `counter(royal_found, +1)`.
- КОЛИ `pattern(region_closed)` → ЯКЩО `occupied(block, key)` → ТО `give(player, key)`.
- КОЛИ `pattern(region_closed)` → ЯКЩО `occupied(block, scroll)` → ТО `set_state(player, scroll_shield)` до кінця рівня.
- КОЛИ `pattern(region_closed)` → ЯКЩО `occupied(block, guardian)` → ТО `spawn(guardian)`, `custom: «випущений вартовий одразу полює»`.
- КОЛИ `level_start` → ТО `spawn(guardian)` — один вартовий полює від початку, другий схований у блоці.
- КОЛИ `tick` → ТО `custom: «вартовий іде коридором до гравця; на низькому skill — часто блукає й кружляє в кутах»`.
- КОЛИ `contact(guardian, player)` → ЯКЩО `state(player, scroll_shield)` → ТО `disappear(guardian)`, `clear_state(player, scroll_shield)`.
- КОЛИ `contact(guardian, player)` → ЯКЩО `not state(player, scroll_shield)` → ТО `lives(-1)`, `disappear(guardian)`.
- КОЛИ `contact(player, exit)` → ЯКЩО `has(player, key) and counter(royal_found, ==, 1)` → ТО `next_level`; інакше `block` (?).
- КОЛИ `level_end` → ЯКЩО `count(guardian, >, 0)` → ТО `custom: «живі вартові переходять на наступний рівень»`.
- КОЛИ `level_end` → ЯКЩО `counter(level_in_pyramid, ==, 5)` → ТО `lives(+1)` або `score(bonus)`, `custom: «нова піраміда: вартові не переходять, але уважніші»`.
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over`.
- Перемога: фіналу нема — піраміди йдуть одна за одною з тим самим планом. Поразка: уся команда спіймана. Рахунок: скарби й королівські мумії, бонус за піраміду.

## Керування і ввід
- ZX Spectrum: A — вгору, Z — вниз, K — ліворуч, L — праворуч; клавіші перевизначаються, можна джойстик.
- Amstrad/C64: джойстик або клавіатура.
- Дія лише одна — рух; сувій спрацьовує сам при зустрічі з вартовим.
- Два гравці — по черзі, рівень кожному (Wikipedia: «обмежений» мультиплеєр).

## Вікна, меню, HUD
- `settings-window` перед грою: швидкість (5 рівнів, «від помірної до вбивчої»), skill (5 рівнів: наскільки розумні вартові на старті), музика, звукові ефекти (C64; PCN називає ті самі опції для Amstrad).
- `game-screen`: 20 блоків, сліди, відкриті вміст і вартові; `score`, `lives` (команда), номер рівня/піраміди (?).
- `end-screen` — кінець гри (?).
- Переходи: налаштування → game-screen → (вихід) наступний рівень → (5-й рівень) нова піраміда з нагородою; (команда вичерпана) → end-screen.

## Фічі поза полем
- `difficulty-presets`: два незалежні повзунки — швидкість і «злість» мумій (по 5 рівнів).
- `levels-sequential`: піраміди по 5 рівнів; між пірамідами — додатковий член команди або бонус-очки.
- `music-toggle`, `sound-toggle`; музика — «The Streets of Cairo».
- `hotseat` для двох по черзі; збережень і рекордів у джерелах нема.

## Варіації й родичі
- `amidar` — та сама гратка й обведення прямокутника, але там блок просто заливається; Oh Mummy додає прихований вміст. Також `pepper-ii`, `make-trax`.
- Oh Mummy 2021 (Fitosoft, ZX Spectrum) — сучасний ремейк; є мобільні версії (?).
- Родичі за прихованим вмістом: Minesweeper (`hidden-deduction`) — відкриття клітини може бути пасткою.
- **Осі варіацій:** що дає обведений блок (заливка / прихований вміст / ворог) · умова виходу (усе / ключ + ціль / квота) · вороги між рівнями (скидаються / переходять / переходять у межах піраміди) · захист (нема / одноразовий щит / тимчасова сила).

## Цікавинки для курсу
- Обведення блоку: перевірка «усі 4 ребра навколо прямокутника відвідані» — 🌱, гарна вправа на граф ребер.
- Фіксований склад вмісту (10/6/4), перемішаний по блоках на старті рівня — 🌱, класичний shuffle.
- Вартовий, що спить у блоці й прокидається від відкриття — 📎: подія відкриття породжує ворога.
- Сувій-щит на один удар, що діє лише в межах рівня — 🌱.
- Вартові переходять на наступний рівень, але не між пірамідами — 📎: стан, що живе між рівнями.
- «Злість» мумій 1–5 як параметр погоні (частка кроків до гравця проти випадкових) — 🥉 (наша інтерпретація налаштування).

## Мапа на каталог
- Є: `move-4dir` · `visited-trail` (сліди) · `item-pickup` · `key-and-door` (ключ відмикає вихід) · `reach-exit` · `chase-player` · `touch-death` + `player-death` (команда) · `temporary-modes` (сувій-щит) · `event-points` · `sequential-levels` + `progress-acceleration` · `difficulty-levels` + `game-settings` · `hot-seat` · `keyboard-controls` + `controls-remap` · `background-music` + `sound-effects` · `status-panel` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+line-paint-box-fill` (є в Amidar) — тут обведення не заливає, а відкриває.
  - `+box-surround-reveal` «Обвести блок — відкрити вміст» · entities/interact · 🌱 · слот {content: table}.
  - `+hidden-content-mix` «Фіксований набір вмісту, розкиданий по блоках» · levels/generation · 🌱 · слот {mix: {treasure: 10, empty: 6, …}}.
  - `+release-on-reveal` «Відкриття випускає ворога» · entities/spawn · 📎.
  - `+one-hit-shield` «Щит на один удар, знищує нападника» · entities/state · 🌱 · слот {scope: level}.
  - `+enemy-carry-over` «Вороги переходять на наступний рівень» · levels/progression · 📎 · слот {reset_every: 5}.
  - `+set-completion-reward` «Нагорода за серію рівнів: життя або очки» · game-logic/score · 🌱.

## Пропозиції до словників
- `+card:box-surround-reveal`, `+card:hidden-content-mix`, `+card:release-on-reveal`, `+card:one-hit-shield`, `+card:enemy-carry-over`, `+card:set-completion-reward` — див. «Мапу на каталог».
- Нових слів правил не треба: обведення лягає на `pattern(region_closed)`, вміст — на `occupied` + `reveal`.

## Джерела
- ⭐ [C64 Online: Oh Mummy](https://c64.krissz.hu/oh-mummy/play-online) — повна інструкція C64-версії (склад вмісту, вартові, сувій, команда з 5, skill/speed), емулятор у браузері.
- [Wikipedia: Oh Mummy](https://en.wikipedia.org/wiki/Oh_Mummy) — платформи, Gem Software / Amsoft, сліди, ключ і гробниця, мумія йде за гравцем на наступний рівень, гра по черзі.
- [Personal Computer News](https://everygamegoing.com/larticle/gameplay-amstrad-oh-mummy/5765) — «п'ять рядів по чотири блоки», вміст, нагорода між пірамідами, опції.
- [Amstrad Action](https://www.everygamegoing.com/larticle/Oh-Mummy-000/25780) — 5 рівнів у піраміді, сувій проти одного вартового.
- [World of Spectrum: інструкція](https://www.worldofspectrum.org/pub/sinclair/games-info/o/OhMummy.txt) — клавіші A/Z/K/L, перевизначення.
- YouTube: пошук «Oh Mummy Amstrad gameplay».

## Непевне
- (?) Чи розкладка вмісту випадкова на кожному рівні (`random: setup`) — джерела кажуть лише про склад.
- (?) Сувій: PCN — «захищає від однієї атаки»; Wikipedia — «дозволяє вбити одну мумію»; C64 — «знищує одного вартового на цьому рівні». Записано як щит, що знищує нападника.
- (?) Чи гине вартовий, коли ловить гравця без сувою (C64: «гине член команди й мумія»), — в інших версіях не перевірено.
- (?) Де вихід на полі й чи він блокує до ключа й мумії, чи просто не діє.
- (?) Чи зараховується спільна сторона двох блоків обом; чи стирають вартові сліди.
- (?) Значення очок, кількість життів у ZX/Amstrad, склад HUD — у відкритих джерелах нема.
