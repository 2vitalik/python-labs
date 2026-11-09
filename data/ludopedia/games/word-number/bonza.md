---
title: Bonza Word Puzzle
slug: bonza
aka: [Bonza]
family: word-number
also: [board-digital]
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: partial
  random: none
  goal: state
year: 2014
platforms: [iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bonza_(video_game)", best: true, note: "суть: фрагменти кросворду, одна тематична підказка, Puzzle Creator (2016), MiniMega, App Store Best of 2014"}
  - {kind: other, url: "https://hardcoregamer.com/reviews/review-bonza-word-puzzle/78461/", note: "огляд: drag фрагментів, snap-звук, підказка за 50 монет, паки, ціни монет, нема збереження рівня"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=bonza+word+puzzle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [drag-drop-piece, stick-together, completion-detection, level-bank, level-select, level-unlock, shop-window, in-game-editor, level-exchange, sound-effects, music-toggle, game-screen, end-screen, event-effects, +crossword-fragments, +theme-clue, +hint-reveal-word, +meta-currency]
proposes: ["+cond:matches_solution", "+ui:theme-clue", "+ui:coin-counter", "+feature:hint-reveal-word", "+feature:puzzle-creator", "+card:crossword-fragments", "+card:meta-currency"]
author: opus
date: 2026-11-09
---

# Bonza Word Puzzle — кросворд розрізано на шматки; збери його назад, знаючи лише тему

## Суть
Гравець бачить розкидані по полю фрагменти кросворду — групи клітин з літерами (по 1–3 і більше клітин). Підказок до окремих слів нема: є одна тематична підказка на весь пазл («Things with buttons»). Треба перетягувати фрагменти так, щоб склалися всі слова теми, переплетені як у кросворді. Ядро — гібрид jigsaw і кросворду: шукаєш не форму шматка, а слово, яке він продовжує.

## Поле і час
- Поле — квадратна сітка-«стіл», на якій фрагменти лежать із привʼязкою до клітин (?).
- Фрагмент — поліоміно з літерою в кожній клітині; розмір і форма — з розрізу кросворду.
- Час статичний: таймера й рахунку нема (огляд Hardcore Gamer).
- Сесія — рівень (пазл) у паку; прогрес незакінченого рівня не зберігається (огляд).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фрагмент | object | клітини з літерами, форма | тягнеться цілком; повороту нема (?) |
| Злиплий блок | container | кілька фрагментів | після правильного зʼєднання рухається як одне ціле (?) |
| Клітина-літера | tile | символ | частина фрагмента; належить 1–2 словам розвʼязку |
| Тематична підказка | static | текст (слово / фраза / перша літера) | одна на пазл, над полем |
| Розвʼязок | static (прихований) | розміщення слів кросворду | порівнюється зі складеним |
| Монети | resource | кількість | заробляються за пазли або купуються; витрачаються на підказки |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag fragment)` → ТО `move(fragment, to)` (вільно по полю, з привʼязкою до сітки) (?).
- КОЛИ `adjacent(fragment, other)` → ЯКЩО `custom: «відносний зсув двох фрагментів = як у розвʼязку»` → ТО `attach(fragment, other)`, `sound(snap)` — фрагменти злипаються (?).
- КОЛИ `after(attach)` → ЯКЩО `custom: «склалося ціле слово теми»` → ТО `flash`, `sound(snap)` (огляд: «snap sound when you form a word»).
- КОЛИ `custom: «усі фрагменти в одному блоці за розвʼязком»` → ТО `win`, `currency(+n)`, `window(end-screen)`.
- КОЛИ `input(hint)` → ЯКЩО `has(player, coins ≥ 50)` → ТО `take(player, 50 coins)`, `custom: «одне слово розвʼязку складається на полі»`.
- КОЛИ `input(hint)` → ЯКЩО `not has(player, coins ≥ 50)` → ТО `window(shop-window)`.
- КОЛИ `level_end` → ТО `unlock(next_level)`.
- Перемога: кросворд зібрано повністю · Поразки нема · Рахунку нема; економіка — монети на підказки.

## Керування і ввід
- Тач: затиснути фрагмент і тягнути; відпустити — фрагмент лягає в клітини.
- Кнопка підказки (за монети); кнопки звуку й музики окремо.
- Клавіатури нема — літери вже на полі, змінюється лише розташування.

## Вікна, меню, HUD
- `game-screen`: тематична підказка (`theme-clue`), поле з фрагментами, кнопка підказки, `coin-counter`.
- `level-select`: паки (Starter — 10 легших пазлів; далі паки по 30+ рівнів, «all 30 packs» за оглядом) і рівні в паку.
- `shop-window`: монети за гроші (0.99 $ — 250, 1.99 $ — 550, 4.99 $ — 1500, 9.99 $ — 3250) + разові бонуси за лайк/фоловінг/лист другу (по 25).
- `end-screen`: зібраний кросворд, нагорода.
- `editor-window` (Puzzle Creator, 2016): задати слова й тему, гра ріже їх на фрагменти (?); поділитися з друзями (?).
- `settings-window`: звук, музика.
- Переходи: `main-menu` → `level-select` → `game-screen` → `end-screen` → наступний рівень.

## Фічі поза полем
- `puzzle-bank` паками з `level-unlock`.
- `hint` за внутрішню валюту (`meta-currency`): 50 монет — одне слово.
- `level-editor` (Puzzle Creator) + `level-sharing` (?).
- `sound-toggle`, `music-toggle` — окремо.
- `autosave` нема: закрив застосунок — рівень з початку (огляд).
- `daily-puzzle` (?): не підтверджено.

## Варіації й родичі
- Кросворд (сітка зі словами-перетинами) + jigsaw (фрагменти без форми-підказки).
- Родичі в корпусі: Scrabble (`scrabble.md`) — сітка перетинів слів; Waffle (`waffle.md`) — переставляння літер до правильних слів; NYT Connections (`nyt-connections.md`) — тематичні групи без підказок до кожного слова.
- **Осі варіацій:** розмір фрагмента (1 клітина = анаграма / великі шматки = jigsaw) · підказка (одна тема / по слову / перша літера) · поворот фрагментів (нема / є) · злипання (правильне / будь-яке).

## Цікавинки для курсу
- Drag фрагмента-поліоміно з привʼязкою до сітки — 📎: hit-test по клітинах, «примагнічування».
- Злипання правильних сусідів у блок (union-find за відносним зсувом від розвʼязку) — 🥉: перевірка «чи зсув двох фрагментів = зсув у розвʼязку».
- Різання кросворду на фрагменти для редактора (зв'язні шматки 1–4 клітини, щоб кожен шматок не видавав слово) — 🥈.
- Генератор тематичного кросворду з набору слів (розстановка перетинів) — 🥇: backtracking по перетинах.
- Підказка «одне слово» за валюту — 🌱.

## Мапа на каталог
- Є: `drag-drop-piece` ↔ перетягування фрагмента · `stick-together` ↔ правильні фрагменти злипаються й рухаються разом · `completion-detection` ↔ кросворд зібрано · `level-bank` / `level-select` / `level-unlock` ↔ паки · `shop-window` ↔ монети · `in-game-editor` / `level-exchange` ↔ Puzzle Creator · `sound-effects` / `music-toggle` ↔ snap-звук і перемикачі.
- **Нема** → пропозиції карток:
  - `+crossword-fragments` «Кросворд, розрізаний на фрагменти» · entities/legality · 🥉 · слоти {piece_size: int, rotate: bool}.
  - `+theme-clue` «Одна тематична підказка на рівень» · interface/hud · 🌱.
  - `+hint-reveal-word` «Підказка: відкрити одне слово розвʼязку» · game-logic/difficulty · 🌱 (родич `hint` у features).
  - `+meta-currency` «Валюта поза раундом на підказки/паки» · game-logic/economy · 📎 (на відміну від `round-currency`).

## Пропозиції до словників
- `+cond:matches_solution` — відносне положення двох елементів збігається з розвʼязком (Bonza, jigsaw-подібні).
- `+ui:theme-clue` — підказка-тема над полем.
- `+ui:coin-counter` — баланс внутрішньої валюти.
- `+feature:hint-reveal-word` — платна підказка «одне слово».
- `+feature:puzzle-creator` — редактор, де гравець задає слова, а гра будує пазл.
- `+card:crossword-fragments`, `+card:meta-currency` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Bonza (video game)](https://en.wikipedia.org/wiki/Bonza_(video_game)) — суть, тематична підказка, Puzzle Creator, MiniMega, 2014, 70 пазлів дешевше долара.
- [Hardcore Gamer: Review Bonza Word Puzzle](https://hardcoregamer.com/reviews/review-bonza-word-puzzle/78461/) — drag, snap, підказки й монети, паки, відсутність збереження.
- YouTube: пошук «bonza word puzzle gameplay».

## Непевне
- (?) Злипання правильно зʼєднаних фрагментів у блок — з памʼяті; огляд каже лише про snap-звук, коли склалося слово.
- (?) Повороту фрагментів нема — з памʼяті, джерела мовчать.
- (?) Як саме Puzzle Creator ріже кросворд і чи можна ділитися пазлами.
- (?) Щоденний пазл — не знайдено в джерелах.
- (?) Скільки монет дають за розвʼязаний пазл.
- Кількість паків: огляд пише «all 30 packs» — на момент огляду, згодом могло змінитися.
