---
title: Bananagrams
slug: bananagrams
aka: [Банананграми, Bananagrams Duel, Double Bananagrams]
family: word-number
also: [board-digital]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: hotseat
  info: hidden
  random: runtime
  goal: race
year: 2006
platforms: [board, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bananagrams", best: true, note: "144 плитки, Split/Peel/Dump/Bananas, розподіл літер, варіанти, історія, онлайн-версія 2008–2012"}
  - {kind: other, url: "https://www.asmodee.co.uk/blogs/news/bananagrams-rules", note: "правила дистриб'ютора: 21/15/11 плиток, Rotten Banana, варіанти Smoothie, Café, Solitaire, кооператив"}
  - {kind: official, url: "https://bananagrams.com/blog/how-to-play-bananagrams-remotely-over-a-video-call", note: "офіційний блог: гра по відеозвʼязку, кожен з власною купою"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=bananagrams+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 60
mechanics: [simultaneous-versus, word-validation, connectivity-check, infinite-field, completion-detection, drag-drop-piece, rule-variants, hot-seat, online-multiplayer, time-bonus, score-records, game-screen, end-screen, help-window, +tile-bag-draw, +tile-exchange, +peel-all-draw, +personal-grid, +grid-rebuild, +word-challenge, +disqualify-return]
proposes: ["+effect:exchange", "+effect:all_draw", "+cond:in_pool", "+ui:bunch-counter", "+feature:mode-solitaire", "+card:peel-all-draw", "+card:personal-grid"]
author: opus
date: 2026-11-09
---

# Bananagrams — кожен на швидкість будує свій кросворд з руки; хто вичерпав руку — усі тягнуть ще по плитці

## Суть
Без дошки й черги: усі гравці одночасно складають із власних плиток власну звʼязну сітку слів, як у кросворді. Коли хтось використав усі плитки, він кричить «Peel!» — і **кожен** тягне ще одну, тож лідер прискорює всіх. Сітку можна будь-коли розбирати й перебудовувати. Ядро — real-time гонка з персональним полем і спільною купою; «Бананас» перемагає той, хто першим закінчить, коли купа вичерпана.

## Поле і час
- Поле кожного гравця — необмежена квадратна сітка на столі (`infinite-field`); слова лише зліва направо або зверху вниз, без діагоналей.
- Спільний ресурс — купа (Bunch) 144 плиток догори дном.
- Час реальний, ходів нема; події (Peel, Dump) відбуваються будь-коли.
- Прихована інформація: плитки в купі; чужі сітки видно, але на гру це не впливає.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка-літера | tile | літера; без вартості | купа → рука → сітка; у сітці можна переставляти |
| Купа (Bunch) | container | 144 плитки | видає плитки наосліп; кінець гри, коли плиток менше, ніж гравців |
| Рука гравця | container | старт 21 / 15 / 11 | невикладені плитки |
| Сітка гравця | zone | без меж | має бути звʼязним кросвордом зі словникових слів |
| Гравець | player | рука, сітка | грає одночасно з усіма |
| Банан-чохол | container | — | лише зберігання (у варіанті Café — замість купи) |

Розподіл літер: J K Q X Z ×2 · B C F H M P V W Y ×3 · G ×4 · L ×5 · D S U ×6 · N ×8 · R T ×9 · O ×11 · I ×12 · A ×13 · E ×18.

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ЯКЩО `count(players, <=, 4)` → ТО `give(each, 21 tiles)`; 5–6 → 15; 7–8 → 11.
- КОЛИ `input(«Split!»)` → ТО `reveal(hands)`, `custom: «усі одночасно починають будувати»`.
- КОЛИ `input(place)` → ТО `place(player, tile)` у свою сітку; КОЛИ `input(move tile)` → ТО `custom: «перестановка/розбір сітки дозволені будь-коли»`.
- КОЛИ `input(«Peel!»)` → ЯКЩО `counter(hand, ==, 0)` and `custom: «у купі ≥ гравців плиток»` → ТО `custom: «кожен гравець, включно з тим, хто крикнув, бере 1 плитку»`.
- КОЛИ `input(«Dump!»)` → ТО `custom: «повернути 1 плитку в купу, взяти 3»` — без ліміту, на інших не впливає.
- КОЛИ `input(«Bananas!»)` → ЯКЩО `counter(hand, ==, 0)` and `custom: «у купі менше плиток, ніж гравців»` → ТО `custom: «гра зупиняється, перевірка сітки»`.
- КОЛИ `custom: «перевірка сітки»` → ЯКЩО `in_dictionary(all words)` and `connected(grid)` → ТО `win` — «Top Banana».
- КОЛИ `custom: «перевірка сітки»` → ЯКЩО `not in_dictionary(word)` → ТО `custom: «Rotten Banana: гравця знято, його плитки в купу»`, гра триває для решти.
- Заборонені: помилки, абревіатури, власні назви, неприйняті слова — оскаржують інші гравці.
- Перемога: першим вичерпати руку при порожній купі з валідною сіткою · Поразка: інші гравці / дискваліфікація · Рахунку нема.

## Керування і ввід
- Настільна: руками кладеш, зсуваєш, розбираєш плитки; голосові команди «Split», «Peel», «Dump», «Bananas» — це і є ввід.
- Онлайн-версія (Large Animal Games + Majesco, 2008–2012): drag плиток на свою сітку, кнопки Peel/Dump (?).

## Вікна, меню, HUD
- (цифрова версія) `game-screen`: своя нескінченна сітка з прокруткою, рука, `bunch-counter` (скільки лишилось у купі), кнопки Peel / Dump, сповіщення про чужі Peel (`toast`).
- (цифрова версія) `end-screen`: переможець, сітки гравців, оскаржені слова.
- (цифрова версія) `mode-select`: live-гра · виклики · соло («Banana Café» — побити свій час).
- (цифрова версія) `help-window` — правила й команди.
- Переходи: `main-menu` → `mode-select` → `game-screen` → `Bananas!` → `end-screen`.

## Фічі поза полем
- `mode-solitaire` — соло на час або на мінімум слів · `mode-coop` — плитки відкриті, одна спільна сітка.
- `custom-rules`: Smoothie (усі 144 плитки роздано, без Peel/Dump; тай-брейк — найдовше слово), Café (плитки в чохлі, Dump є, Peel нема).
- Видання: My First Bananagrams, Duel (двоє), Double (подвійний набір), WildTiles (джокери), мовні версії.
- Онлайн (2008–2012): «Banana Chip» кредити; open-source солвер Bananagram Solve.

## Варіації й родичі
- Scrabble (`scrabble.md`), Upwords (`upwords.md`) — спільна дошка й черга; тут — персональні сітки й одночасність.
- Boggle (`boggle.md`) — теж real-time «усі одночасно», але поле спільне і незмінне.
- Bonza (`bonza.md`) — збирання кросворду з фрагментів.
- **Осі варіацій:** роздача (порційно з Peel / уся одразу) · обмін (Dump 1→3 / нема) · сітка (особиста / спільна кооп) · кінець (купа < гравців / усі роздано) · перевірка (оскарження / автоматична).

## Цікавинки для курсу
- Перевірка сітки: знайти всі горизонтальні й вертикальні послідовності ≥2 і перевірити словником + звʼязність (BFS) — 📎.
- Real-time подія «Peel» для всіх клієнтів одночасно (сервер, гонка подій) — 🥈.
- Нескінченна сітка як `dict[(x, y)] -> letter` з прокруткою — 🌱.
- Солвер: розкласти руку в одну звʼязну сітку (backtracking, евристики) — 🥇.
- Dump 1→3 і умова кінця «у купі менше, ніж гравців» — 🌱.

## Мапа на каталог
- Є: `simultaneous-versus` ↔ усі грають одночасно · `word-validation` · `connectivity-check` ↔ звʼязна сітка · `infinite-field` ↔ сітка без меж · `completion-detection` ↔ Bananas · `drag-drop-piece` · `rule-variants` ↔ Smoothie, Café · `hot-seat` (спільний стіл) · `online-multiplayer` ↔ 2008–2012 · `time-bonus` / `score-records` ↔ соло на час · `game-screen` · `end-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+tile-bag-draw`, `+tile-exchange`, `+word-challenge` — див. `scrabble.md`.
  - `+peel-all-draw` «Лідер вичерпав руку — усі тягнуть» · game-logic/opponent · 📎.
  - `+personal-grid` «Кожен будує своє поле з особистої руки» · levels/generation · 📎.
  - `+grid-rebuild` «Розібрати й перебудувати вже викладене» · interface/input · 🌱.
  - `+disqualify-return` «Дискваліфікований повертає ресурси в загальний пул» · game-logic/lose · 🌱.

## Пропозиції до словників
- `+effect:exchange` — віддати k одиниць у пул і взяти n (Dump 1→3; обмін у Scrabble/Upwords).
- `+effect:all_draw` — кожен гравець отримує з пулу (Peel).
- `+cond:in_pool` — у спільному пулі ≥ N одиниць (кінець Bananagrams).
- `+ui:bunch-counter` — скільки лишилось у спільній купі.
- `+feature:mode-solitaire` — соло без суперників (на час / мінімум слів).
- `+card:peel-all-draw`, `+card:personal-grid` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Bananagrams](https://en.wikipedia.org/wiki/Bananagrams) — 144 плитки, команди, розподіл літер, варіанти, автори Abraham і Rena Nathanson, London Toy Fair 2006, онлайн-версія.
- [Asmodee UK: Bananagrams rules](https://www.asmodee.co.uk/blogs/news/bananagrams-rules) — 21/15/11, напрями слів, Rotten Banana, Smoothie, Café, Solitaire/кооп.
- [Bananagrams: play remotely](https://bananagrams.com/blog/how-to-play-bananagrams-remotely-over-a-video-call) — офіційний варіант з власною купою і 21 плиткою кожному.
- YouTube: пошук «bananagrams how to play».

## Непевне
- (?) Rotten Banana: у різних джерелах — дискваліфікація з поверненням плиток, у деяких правилах — гравець просто продовжує з плитками; узяв версію Asmodee.
- (?) Peel можна кликати лише з валідною сіткою — одні джерела вимагають, інші ні.
- (?) Інтерфейс онлайн-версії 2008–2012 (кнопки, режими) — не бачив; вікна узагальнено.
- (?) Чи дозволено Dump, коли в купі менше 3 плиток — у джерелах нема.
