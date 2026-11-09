---
title: Jeson Mor (Девʼять коней)
slug: jeson-mor
aka: [Jesön Mor, Есөн морь, Nine Horses, Девʼять коней, Девять коней]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 1974
platforms: [board, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Jeson_Mor", best: true, note: "правила, центр e5 «зайняти й вийти», взяти всіх, стратегія центру, позиція-цугцванг"}
  - {kind: wiki, url: "https://ru.wikipedia.org/wiki/Девять_коней", note: "те саме RU: дошка 9×9, коні на перших рядах, вихід з центру; повна інформація, без випадковості"}
  - {kind: other, url: "https://gambiter.com/chess/variants/Jeson_mor.html", note: "«просто зайняти e5 замало — конь мусить потім вийти»; коня на e5 можна взяти; варіант 8×8 ліній"}
  - {kind: other, url: "https://www.deskovehry.info/pravidla/jesonmor.htm", note: "чеські правила: «kámen ходить як šachový kůň», зайняти e5 і покинути"}
  - {kind: other, url: "https://ludii.games/details.php?keyword=Jeson%20Mor", note: "Ludii: правила за Popova 1974 — перемога вже за хід у центр; .lud-опис гри"}
  - {kind: bgg, url: "https://www.boardgamegeek.com/boardgame/37917", note: "BGG (лінк зі статті Вікіпедії, не відкривав)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=jeson+mor+nine+horses", note: "пошук; партії"}
stage: v1
coverage: 75
mechanics: [piece-move-patterns, piece-capture, legal-move-highlight, destroy-all-enemies, hot-seat, ai-opponent, cell-click, drag-drop-piece, game-screen, end-screen, help-window, +occupy-and-leave-win]
proposes: ["+cond:attackers_count", "+ui:attack-count-overlay", "+card:occupy-and-leave-win"]
author: opus
date: 2026-11-09
---

# Jeson Mor — монгольські «девʼять коней»: лише шахові коні на 9×9, виграє той, хто зайде в центр і вийде з нього

## Суть
Традиційна монгольська гра двох гравців, яку вважають шаховим варіантом: у кожного девʼять шахових коней на першому ряду дошки 9×9. Коні ходять і бʼють як у шахах; виграє той, хто першим поставить коня на центральну клітину e5 **і наступним ходом виведе його звідти** — просто зайняти центр замало, бо коня на e5 можна взяти. Інша перемога — взяти всіх коней суперника. Уся стратегія — рахунок, скільки коней кожної сторони «дивиться» на e5.

## Поле і час
- Дошка 9×9 (вертикалі a–i, горизонталі 1–9), центр — e5. Альтернатива: дошка 8×8 ліній, фігури — на 81 перетині (як 9×9 клітин).
- Розстановка: білі коні на a1–i1, чорні — на a9–i9 (діаграма RU-вікі).
- Хід = один хід одного коня; хто ходить першим — домовляються гравці.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кінь | piece | 9 на сторону | хід шахового коня (1+2), стрибає через будь-що; бʼє ворожого коня заміщенням |
| Кінь у центрі | piece | стан `on_center` | якщо наступним ходом вийде з e5 — перемога; поки стоїть — його можна взяти |
| Центральна клітина e5 | zone | 1 клітина | ціль: зайти й вийти |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move(knight, to))` → ЯКЩО `turn_of(side)` and `custom: «to — хід шахового коня»` and `not occupied(to, own_knight)` → ТО `move(knight, to)`, `end_turn`; інакше `block`.
- КОЛИ `contact(knight, enemy_knight)` → ТО `disappear_b` — взяття заміщенням, як у шахах.
- КОЛИ `enter(knight, center)` → ТО `set_state(knight, on_center)` — зокрема, коли кінь бʼє іншого коня на e5.
- КОЛИ `contact(enemy_knight, knight)` → ЯКЩО `state(knight, on_center)` → ТО `disappear_b` — центрового можна взяти, тоді в центрі вже кінь суперника.
- КОЛИ `leave(knight, center)` → ЯКЩО `state(knight, on_center)` → ТО `win`.
- КОЛИ `all_gone(enemy_knight)` → ТО `win`.
- Набір Ludii (Popova 1974): КОЛИ `enter(knight, center)` → ТО `win` — без вимоги вийти.
- Стратегія (EN-вікі): займати e5, лише коли на нього нападає **строго більше** своїх коней, ніж ворожих; якщо в суперника більше — доводити своїх нападників до рівності.
- Цугцванг (EN-вікі): чорні d7, f7, c6, g6 і білі c4, g4, d3, f3 — по 4 нападники на e5. Той, хто ходить, програє: зайде в центр — серія розмінів закінчиться конем суперника на e5; відведе коня — суперник матиме перевагу й зайде сам.
- Перемога: зайти в e5 і вийти · взяти всіх коней · Нічия: джерела не описують.

## Керування і ввід
- Фізична дошка: пересунути коня.
- Цифрова версія (Ludii): клік по коню й по цілі; підсвітка 2–8 клітин ходу коня.

## Вікна, меню, HUD
(цифрова версія)
- `game-screen`: дошка 9×9 з виділеним центром, `legal-move-highlight`, `turn-indicator`, `captured-pieces`; кандидат `attack-count-overlay` — скільки коней кожної сторони бʼє e5.
- `help-window` — правила; `end-screen` — «вийшов з центру» або «взято всіх».
- Переходи: main-menu → game-screen → end-screen.

## Фічі поза полем
- `hotseat`; Ludii — загальна система ігор, де Jeson Mor є як опис `.lud` (AI-агенти Ludii для цієї гри не перевіряв (?)).
- `rules-page` — у Ludii посилання на джерело правил (Popova 1974).
- Збереження, рейтинги, онлайн — не знайдено.

## Варіації й родичі
- [chess.md](chess.md) — хід коня; [n-queens-knights-tour.md](../pencil-logic/n-queens-knights-tour.md) — хід коня як головоломка.
- [lichess-variants.md](lichess-variants.md): King of the Hill — перемога входом короля в центр d4/d5/e4/e5; тут ціль та сама за суттю, але треба ще й вийти.
- [hexapawn.md](hexapawn.md) — ще одна мініатюрна гра з одним типом фігур і простою ціллю.
- **Осі варіацій**:
  - **Ціль у центрі**: зайти (Ludii, King of the Hill) · зайти й вийти (Jeson Mor за Вікіпедією) · утримати N ходів.
  - **Склад армій**: усі типи шахових фігур · один тип (лише коні).
  - **Дошка**: 9×9 клітин · 8×8 ліній з фігурами на перетинах (той самий граф).

## Цікавинки для курсу
- Генератор ходів коня на 9×9 і взяття — 🌱.
- Перемога «зайти й вийти»: стан на фігурі + тригер виходу — 🌱.
- Підрахунок нападників на e5 і симуляція серії розмінів як оцінка позиції — 🥉.
- AI minimax з оцінкою центру й розпізнаванням цугцвангу — 🥇.
- Режим «правила Ludii / правила Вікіпедії» як перемикач умови перемоги — 📎.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ лише кінь · `piece-capture` · `legal-move-highlight` · `destroy-all-enemies` ↔ взяти всіх коней · `hot-seat` · `ai-opponent` (?) · `cell-click` · `drag-drop-piece` · `game-screen` · `end-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+occupy-and-leave-win` «Перемога — зайти фігурою на клітину-ціль і наступним ходом вийти» · game-logic/win · 🌱 · слоти {cell: center, must_leave: bool}.

## Пропозиції до словників
- `+cond:attackers_count(cell, side, op, n)` — скільки фігур сторони атакує клітину (стратегія центру Jeson Mor, оцінка для AI; родич `adjacent_count`).
- `+ui:attack-count-overlay` — число нападників кожної сторони на ключовій клітині.
- `+card:occupy-and-leave-win` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Jeson Mor](https://en.wikipedia.org/wiki/Jeson_Mor) — дошка, розстановка, хід і взяття, «зайти в e5 і вийти», взяти всіх, альтернатива 8×8 ліній, стратегія і позиція-цугцванг; Pritchard 1994/2007.
- [Wikipedia RU: Девять коней](https://ru.wikipedia.org/wiki/Девять_коней) — правила, діаграма розстановки, монгольська назва.
- [Gambiter: Jeson Mor](https://gambiter.com/chess/variants/Jeson_mor.html) — «merely occupying e5 is not enough», коня на e5 можна взяти, взяти всіх.
- [deskovehry.info](https://www.deskovehry.info/pravidla/jesonmor.htm) — чеські правила: фішки ходять як шаховий кінь, зайняти e5 і покинути.
- [Ludii: Jeson Mor](https://ludii.games/details.php?keyword=Jeson%20Mor) — правила за A. Popova (1974, Études mongoles): перемога ходом у центр; категорії race/reach.
- The World of Abstract Games (homepages.di.fc.ul.pt/~jpn/gv/jesonmor.htm) — не відкрилась (помилка сертифіката); BGG — лінк зі статті, не відкривав.
- YouTube: пошук «jeson mor nine horses».

## Непевне
- (?) Головна розбіжність: Вікіпедія, Gambiter і deskovehry — «зайти й вийти», Ludii (Popova 1974) — «зайти»; у шапці й правилах — перший варіант.
- (?) Чи рахується вихід з e5 зі взяттям і чи мусить вихід бути саме наступним ходом (RU-вікі: «на наступному ходу», EN — «on a later turn») — не уточнено.
- (?) Нічиїх (повторення, пат) джерела не описують — для цифрової версії треба вирішити самим.
- (?) Рік у шапці — найраніше бачене джерело (Popova 1974); гра традиційна, старша.
- (?) Хто ходить першим — «за домовленістю»; стандартного правила нема.
