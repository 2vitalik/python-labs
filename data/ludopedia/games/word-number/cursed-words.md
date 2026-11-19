---
title: Cursed Words
slug: cursed-words
aka: ["Cursed Words: The Word Game That Isn't"]
family: word-number
also: [roguelike]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: runtime
  goal: score
year: 2026
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3856460/", best: true, note: "опис і трейлер: «Starts as Boggle, ends as Schrödinger»; 5 етапів по 2 зустрічі й босу; персонаж, стікери, штампи, розхідні плитки; 300 предметів, 11 персонажів, 20 босів, 26 викликів"}
  - {kind: fandom, url: "https://cursedwords.wiki.gg/", note: "wiki.gg: плитки, прокляття, предмети, боси, квести, корони, піни"}
  - {kind: other, url: "https://cursedwords.wiki.gg/wiki/Curses", note: "прокляті плитки: ?, числа й дроби, шахові фігури, карти, валюти, «хиткі» літери; шанси генерації"}
  - {kind: other, url: "https://cursedwords.wiki.gg/wiki/Tiles", note: "кольори плиток і їхні ефекти"}
  - {kind: other, url: "https://cursedwords.wiki.gg/wiki/Daily", note: "Cursedle — щоденний Wordle на сітці 6×6 з відгуком «поруч»"}
  - {kind: other, url: "https://rogueliker.com/cursed-words-roguelike-puzzle-game/", note: "огляд: сітка 5×5, слово з повʼязаних плиток, раунд із пʼяти сіток, магазин, боси"}
  - {kind: steam, url: "https://store.steampowered.com/app/4264890/", note: "безкоштовне демо (27.01.2026), прогрес переходить у повну гру"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Cursed+Words+Buried+Things+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [word-validation, path-drawing, round-currency, shop-between-levels, shop-buyback, run-relics, in-round-upgrades, sequential-levels, difficulty-levels, daily-puzzle, piece-move-patterns, piece-capture, en-passant, wrap-edges, weighted-spawn, achievements-window, character-select, shop-window, game-screen, end-screen, language-picker, +path-trace-word, +letter-value-scoring, +target-score-rounds, +boss-fight, +wildcard-tile, +poker-hand-eval, +shop-reroll, +ascension-levels, +meta-unlocks, +special-letter-tiles, +letter-feedback, +chess-move-path, +positional-wildcard, +scatter-tiles, +effect-order-slots, +adjacency-feedback, +unused-turns-payout, +challenge-runs]
proposes: ["+cond:chess_move", "+cond:word_position", "+cond:poker_hand", "+effect:scatter", "+effect:reroll", "+ui:target-score", "+feature:challenge-quests", "+feature:ascension-levels", "+feature:dictionary-language", "+axis:rules"]
author: opus
date: 2026-11-19
---

# Cursed Words — Boggle-роглайк: тягни слова по сітці 5×5, набирай ціль зустрічі, а предмети й боси перетворюють літери на числа, шахові фігури й карти

## Суть
Роглайк-забіг на ядрі Boggle: на сітці 5×5 плиток-літер гравець веде слово через повʼязані плитки, очки слова — вартості плиток (як у Scrabble) з додатками й множниками. За кілька сіток треба набрати ціль зустрічі; виграш дає гроші, між зустрічами — магазин стікерів, штампів і розхідних плиток.

Головна незвичність — «прокляття»: з ходом забігу на сітці зʼявляються плитки-числа (джокер лише на N-й позиції слова), шахові фігури (наступну літеру визначає хід фігури), карти (покерні комбінації всередині слова), валюти й «?». Слоган Steam — «Starts as Boggle, ends as Schrödinger».

Забіг — 5 етапів по 2 зустрічі й босу; бос змінює правила зустрічі (сітка 4×4, мінімальна довжина слова, Q на полі, крадіжка грошей). Поруч живе щоденний режим Cursedle — Wordle на сітці 6×6.

## Поле і час
- Сітка 5×5 плиток; бос Bat зменшує її до 4×4…3×3 (проклятий — до 3×2), Cursedle — 6×6. Плитка = літера (або прокляття) + необовʼязковий колір.
- Зустріч = кілька сіток (за оглядом Rogueliker — пʼять); бос Badger і Red-корона забирають по сітці. Кожна сітка генерується наново: літери за частотами мови, потім пін, предмети й бос «розкидають» (scatter) особливі плитки.
- Хід = скласти й подати слово (?). Часу нема (Steam: «Playable without Timed Input», «Save Anytime»).
- Предмет Hungry Snake зшиває сітку по горизонталі: шлях, суміжність для очок і шахові фігури переходять через край.
- Забіг: етапи 1–5 → перемога; пʼять проклятих босів за забіг відкривають 6-й етап з боєм проти Michael.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка-літера | tile | BASE SCORE як у Scrabble (A 1 … J/X 8, Q/Z 10) | крок шляху слова; генерується за частотами мови й корони |
| Сітка | zone | 5×5 (Bat — менша, Cursedle — 6×6) | нова на кожну сітку зустрічі; з Hungry Snake — зшита по горизонталі |
| RED / BLUE | tile | +1 BASE SCORE | колір, на який реагують предмети |
| PURPLE | tile | +2 BASE SCORE | рахується і RED, і BLUE |
| SHINY | tile | BASE SCORE = 50 | змінами бази не зачіпається |
| VOID | tile | відʼємна BASE SCORE | бонуси до бази віднімаються; застосовується останнім |
| WHITE | tile | — | «travel to anywhere»: дозволяє несуміжний хід шляху |
| GOLD | tile | BASE SCORE = поточні $ | — |
| PINK | tile | $1 | відкладає $1; на першій зустрічі наступного етапу повертає подвоєним |
| GREEN | tile | 10 % | 10 % очок поданого слова додає до кожного наступного слова зустрічі |
| CACTUS | tile | +1 BASE на початку кожної сітки | колір не перекривається scatter-ом; розхідною плиткою не замінюється |
| GLITCH | tile | — | стає випадковою проклятою плиткою; у пул кольорів — останнім |
| Безбарвна плитка | tile | — | не колір для предметів (Yeti Crab знебарвлює кольорові) |
| «?» (blank) | tile | BASE 0 | будь-яка літера на будь-якій позиції |
| Число / дріб | tile | 1–8; дроби (½…⅒) | будь-яка літера, але лише на позиції N; TILE SCORE = N, дріб — чисельник + знаменник |
| Шахова фігура | piece | p 1 · h/b 3 · r 5 · q 9 · k 15; чорна / біла | будь-яка літера; наступну плитку слова задає хід фігури; хід на фігуру іншого кольору — «взяття» |
| Карта | tile | масть ♣♦♥♠ (база не змінюється); джокер — 0 | плитки слова складають покерні комбінації незалежно від позицій |
| Валюта | tile | BASE 0 | конкретна літера (€ = E, $ = S, ¥ = Y…), не голосна й не приголосна; +$1 за подання |
| «Хитка» літера | tile | — | предмет дає їй ще одне прочитання: Q як QU, Z як S, 1/5/10 як I/V/X |
| Плитка-предмет | pickup | BASE 0 | дає ефект предмета, коли входить у слово |
| Розхідна плитка | supply | колір / тип | купується в магазині, кладеться на сітку замість плитки |
| Стікер | supply | до 5; рівень 1–3, foil — до 5 | правило або бонус очок; діє зліва направо, порядок можна міняти будь-коли |
| Штамп | supply | до 5; без апгрейдів | як стікер, діє після стікерів |
| Пін | supply | 1, свій у персонажа | діє першим; після етапу апгрейд лівої чи правої половини |
| Персонаж | player | 11; свій пін | визначає старт забігу (Rodman — RED і BLUE на кожну сітку, Sam Gambit — пішак і +8 за взяття) |
| Бос | boss | 15 звичайних + 5 прихованих; проклята версія з Purple-корони | модифікатор правил зустрічі, що посилюється з етапом |
| Гроші $ | resource | — | за виграні зустрічі й невикористані сітки; витрачаються в магазині |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(grid)` → ТО `spawn_at(tile, all cells)` — літери за частотами мови; потім `set_state(rng tiles, colour|curse)` від піна, предметів і боса (Rodman: 1 RED + 1 BLUE; Head In The Clouds: 2 WHITE).
- КОЛИ `input(drag tile)` → ЯКЩО `custom: «плитка суміжна з останньою плиткою слова»` → ТО `mark(tile, selected)`; інакше `block` (діагоналі й повтор плитки — (?)).
- КОЛИ `input(drag tile)` → ЯКЩО `state(last tile, WHITE)` → ТО `custom: «наступна плитка — будь-яка клітина (несуміжний хід)»`.
- КОЛИ `input(drag tile)` → ЯКЩО `occupied(last tile, chess piece)` and `not custom: «клітина досяжна ходом фігури»` → ТО `block`; k — на 1, q/r/b — лініями, h — буквою «Г» з перескоком, p — уперед (з домашнього ряду на 2), бʼє навскіс, en passant; рокіровки нема.
- КОЛИ `input(drag tile)` → ЯКЩО `custom: «шлях фігури проходить крізь фігуру свого кольору»` → ТО `block`; на фігуру іншого кольору — ТО `custom: «взяття»` (Sam Gambit: `score(+8)`).
- КОЛИ `edge(path)` → ЯКЩО `has(player, Hungry Snake)` → ТО `wrap(path)` — лише по горизонталі.
- КОЛИ `input(submit)` → ЯКЩО `in_dictionary(word)` and `custom: «обмеження боса й квесту виконано»` → ТО `score(WORD SCORE)`, `counter(grids, -1)`; під джокери гра сама підбирає справжнє слово (показ — опція з v4.5).
- КОЛИ `input(submit)` → ЯКЩО `occupied(word, number N)` and `custom: «N ≠ позиція плитки в слові»` → ТО `block`; дріб стоїть на позиції чисельника або знаменника.
- КОЛИ `input(submit)` → ЯКЩО `occupied(word, currency)` → ТО `currency(+1)` за кожну (₭ і ₩ генеруються, але не подаються без «хиткого» ефекту).
- КОЛИ `input(submit)` → ЯКЩО `custom: «карти слова складають комбінацію: N однакових, дві пари, фул-хаус, флеш (5), стрит (5)»` → ТО `custom: «спрацьовують предмети на комбінацію»` (Peacock — ×WORD SCORE за флеш; Martini — флеш і стрит з 3 карт).
- Підрахунок: `custom: «WORD SCORE = Σ TILE SCORE (BASE SCORE + бонуси) + додатки WORD SCORE, далі множники ×WORD SCORE»`; черга — пін → стікери зліва направо → штампи зліва направо → ефекти боса.
- КОЛИ `phase_start(grid)` → ЯКЩО `state(tile, CACTUS)` → ТО `set_value(tile, base + 1)`.
- КОЛИ `input(submit)` → ЯКЩО `state(tile, PINK)` → ТО `custom: «відкласти $1 до першої зустрічі наступного етапу, там повернути ×2»`.
- КОЛИ `input(submit)` → ЯКЩО `state(tile, GREEN)` → ТО `custom: «+10 % цього WORD SCORE до кожного наступного слова зустрічі»`.
- КОЛИ `spawned(GLITCH)` → ТО `transform(GLITCH, random cursed tile)`.
- КОЛИ `counter(score, >=, target)` → ТО `custom: «зустріч виграно»`, `currency(+нагорода + за кожну невикористану сітку)`, `window(shop-window)`.
- КОЛИ `counter(grids, ==, 0)` → ЯКЩО `counter(score, <, target)` → ТО `lose` (кінець забігу (?)).
- КОЛИ `input(buy)` → ЯКЩО `counter($, >=, price)` → ТО `currency(-price)`, `give(player, item)`; перший предмет кожного магазину безкоштовний (до Yellow-корони).
- КОЛИ `input(sell)` → ТО `take(player, item)`, `currency(+n)`.
- КОЛИ `input(reroll)` → ТО `currency(-cost)`, `custom: «оновити вітрину»`.
- КОЛИ `input(use consumable)` → ЯКЩО `not state(target tile, CACTUS)` → ТО `place(player, consumable)` замість плитки сітки.
- КОЛИ `level_start` → ЯКЩО `state(encounter, boss)` → ТО ефект боса (етап 1, звичайний / проклятий):
  - Bat — `custom: «сітка 4×4 / 4×3»`; Badger — `counter(grids, -1 / -2)`; Cobra — `custom: «слова від 4 / 5 плиток»` (до 7 / 8); Wolf — `custom: «слова до 5 / 4 плиток»`.
  - Axolotl — `set_state(rng ×3 / ×5, Q)` на кожну сітку; Mole — 3 / 5 VOID; Bison — числа 7–9 / 7–11; Robo-Eel — `disappear(2 / 3 tiles)`; Yeti Crab — `transform(2 / 3 coloured tiles, colourless)`.
  - Salamander — `custom: «−1 / −2 TILE SCORE кожній плитці»`; Toothed Whale — `custom: «ціль ×1.25 / ×1.35»`; Fox — `currency(-2 / -3)` за слово; Robo-Monkey — кожна сітка `score(−$ / −2×$)`.
  - Capybara (з етапу 2) — після кожного слова `custom: «перемішати порядок стікерів (проклятий — і штампів)»`; Hyena (з етапу 2) — `custom: «примусово продати предмет на старті зустрічі»`.
- КОЛИ `level_end` → ЯКЩО `state(encounter, boss)` → ТО `choose(left | right half of pin)` (з ID Card — обидві), `next_level`.
- КОЛИ `level_end` → ЯКЩО `level(==, 5)` and `state(encounter, boss)` → ТО `win`; ЯКЩО `counter(cursed bosses, ==, 5)` → ТО `custom: «етап 6 — бій з Michael»`.
- Cursedle: КОЛИ `input(submit)` → ТО `feedback(guess)` по плитках: сіра — не в слові й не поруч · червона — не в слові, але суміжна з плиткою слова · жовта — у слові не на місці · зелена — на місці; збіг за плиткою, не за літерою.
- Cursedle: КОЛИ `counter(tries, ==, 5)` → ТО `game_over` до наступної дати; очки вимкнено, сітка засіяна датою.
- Перемога: перемогти боса етапу 5 · Поразка: сітки скінчились без цілі (?) · Рахунок: WORD SCORE за слово, ціль на кожну зустріч; у статистиці — найдовше й найдорожче слово забігу.

## Керування і ввід
- Миша або тач: провести слово по плитках і подати (Steam: «Mouse Only Option», «Touch Only Option»); чи є введення з клавіатури — (?).
- Перетягування стікерів і штампів у слотах — порядок застосування можна міняти будь-коли, і перед поданням.
- Магазин: купити, продати, reroll вітрини; розхідну плитку — накласти на клітину сітки.
- Після етапу — вибір половини піна; у Cursedle — 5 подань.

## Вікна, меню, HUD
- `main-menu`: забіг, квести; у дні Cursedle ніс Michael фіолетовий — клік → `daily-window`.
- `character-select`: 11 персонажів (відкриваються коронами й досягненнями); вибір корони — (?).
- `game-screen`: сітка, поточне слово й очки, `target-score`, `remaining-counter` (сітки зустрічі), `coins` ($), `equipment-slots` (пін, 5 стікерів, 5 штампів), підказки-описи предметів (`tooltip`) (?).
- `shop-window`: стікери, штампи, розхідні плитки, foil-предмети (після першого стікера 3-го рівня), reroll, продаж.
- `upgrade-window`: апгрейд лівої чи правої половини піна після етапу.
- `achievements-window` (досягнення Steam відкривають предмети) (?); `settings-window`: гучність, доступність — вимкнути «Reroll reminder pulse».
- `end-screen`: підсумок забігу — найдовше й найдорожче слово.
- Переходи: main-menu → character-select → game-screen (зустріч) → shop-window → … → бос → upgrade-window → наступний етап → end-screen.

## Фічі поза полем
- `difficulty-presets` — 7 накопичувальних корон: Purple (проклятий один з двох босів етапу) → Yellow (без безкоштовного предмета, reroll +$1) → Orange (рідкісні літери −1/−2 BASE) → Pink (2 замкнені слоти штампів) → Green (менше голосних) → Blue (2 замкнені слоти стікерів) → Red (−1 сітка на зустріч).
- `custom-rules` — 26 квестів-викликів із власними правилами й закріпленим набором предметів (відкриваються перемогою з Sam Gambit): Knight Time «усе ходить конем», Red Letter Day — без голосних, Bullseye — ціль треба влучити точно, Two Wrongs — відʼємні цілі, On Cooldown — без літер попереднього слова.
- `unlockables` / `achievements` — корони з кожним персонажем відкривають предмети; персонажі — за коронами (Nat-H4 — 3 Purple-корони).
- `mode-daily` — Cursedle (після перемоги над Michael кожним персонажем; без retry з v4.9); `mode-speedrun` — відкриває квест We're Finally Landing («побити 15 хвилин»).
- `dictionary-language` — сітки-пазли англійською, іспанською, німецькою, французькою (оновлення 12.03.2026); інтерфейс — лише англійська.
- `cloud-save`, `continue` (Save Anytime), `touch-controls`, `mouse-and-keyboard`; DLC «The Madness of Michael» (листопад 2026) — 5 квестів і секретний режим з налаштовуваними викликами.

## Варіації й родичі
- Boggle ([boggle.md](boggle.md)) — ядро «слово з сусідніх плиток»; Squaredle ([squaredle.md](squaredle.md)); Wordle ([wordle.md](wordle.md)) — основа Cursedle.
- Balatro-подібні забіги: Wordatro ([wordatro.md](wordatro.md)), Passant (`chess-abstract/passant.md`) — шахи як Balatro; Bookworm ([bookworm.md](bookworm.md)) — вартість слова як сила; Pile-Up Poker ([pile-up-poker.md](pile-up-poker.md)) — покерні комбінації на сітці.
- **Осі варіацій:** «куди далі шлях слова» (сусід / будь-куди через WHITE / хід фігури / конем для всіх у Knight Time / через край у Hungry Snake) · джокери (повні «?» / позиційні числа / валюти-літери / «хиткі» прочитання) · де живуть модифікатори (слоти предметів / плитки на полі / бос) · обмеження на слово (мін./макс. довжина, без кольорових, без голосних).

## Цікавинки для курсу
- «Куди можна далі» як поліморфна функція типу плитки: сусід / будь-куди / хід шахової фігури / тор — 🥉.
- Перевірка слова з джокерами «?» і позиційними числами, коли гра сама підбирає справжнє слово (шаблон по trie) — 🥈.
- Конвеєр підрахунку «пін → стікери → штампи → бос» зі слотами, порядок яких змінює результат (Chain of Responsibility) — 📎.
- Покерні комбінації серед плиток слова, позиції не важливі, карти можна ділити між комбінаціями — 📎.
- Cursedle: відгук Wordle на 2D-сітці з кольором «поруч із розвʼязком» — 🥉.
- Боси як плагіни правил з параметром етапу (розмір сітки, довжина слова, scatter) — 🥉 за систему, кожен бос 🌱.
- Генерація сітки за частотами літер + scatter особливих плиток зі шансами (1 % джокер, 9 % масть; предмети 1 / 9 / 90 %) — 📎.

## Мапа на каталог
- Є: `word-validation` ↔ словник 4 мов · `path-drawing` ↔ шлях слова мишею · `round-currency` ↔ $ · `shop-between-levels` + `shop-window` ↔ магазин після зустрічі · `shop-buyback` ↔ продаж предметів · `run-relics` ↔ стікери, штампи, пін · `in-round-upgrades` ↔ рівні стікерів · `sequential-levels` ↔ 5 етапів · `difficulty-levels` ↔ корони · `daily-puzzle` ↔ Cursedle · `piece-move-patterns` + `piece-capture` + `en-passant` ↔ шахові прокляття · `wrap-edges` ↔ Hungry Snake · `weighted-spawn` ↔ частоти літер і рідкості предметів · `character-select` · `achievements-window` · `game-screen` · `end-screen` · `language-picker`.
- **Нема** → пропозиції карток:
  - `+path-trace-word`, `+letter-value-scoring`, `+target-score-rounds`, `+boss-fight`, `+wildcard-tile`, `+poker-hand-eval`, `+shop-reroll`, `+ascension-levels`, `+meta-unlocks`, `+special-letter-tiles`, `+letter-feedback` — уже пропоновані корпусом (Boggle, Wordatro, Balatro-подібні).
  - `+chess-move-path` «Наступна клітина шляху — ходом шахової фігури» · game-logic/constraints · 🥉 · слоти {pieces: p,h,b,r,q,k; take: on}.
  - `+positional-wildcard` «Джокер лише на N-й позиції слова» · game-logic/constraints · 🌱 · слот {range: 1–8, fractions: on}.
  - `+scatter-tiles` «Розкидати особливі плитки на нову сітку» · levels/generation · 🌱 · слоти {kind, count}.
  - `+effect-order-slots` «Слоти модифікаторів: порядок = черга застосування» · game-logic/score · 📎 · слот {slots: 5}.
  - `+adjacency-feedback` «Відгук "не в розвʼязку, але поруч"» · game-logic/constraints · 📎.
  - `+unused-turns-payout` «Невикористані спроби → гроші» · game-logic/economy · 🌱.
  - `+challenge-runs` «Забіг-виклик з модифікатором правил і заданим набором» · game-logic/difficulty · 📎.

## Пропозиції до словників
- `+cond:chess_move` — клітина досяжна ходом фігури з попередньої плитки (Cursed Words; Knight Time — для всіх плиток).
- `+cond:word_position` — плитка стоїть на N-й позиції слова (числа-прокляття).
- `+cond:poker_hand` — плитки складають покерну комбінацію (Cursed Words, Balatro-подібні).
- `+effect:scatter` — надати N випадковим плиткам нової сітки колір чи прокляття.
- `+effect:reroll` — оновити вітрину за плату (як у Wordatro).
- `+ui:target-score` — ціль зустрічі поруч із рахунком.
- `+feature:challenge-quests` — квести-виклики з модифікатором правил і закріпленим набором предметів.
- `+feature:ascension-levels` — накопичувальні щаблі складності, що відкриваються перемогами (корони).
- `+feature:dictionary-language` — мова словника як параметр правил.
- `+axis:rules` — `unlocked`: правила гри змінюються впродовж забігу (літери стають числами, фігурами, картами).

## Джерела
- ⭐ [Steam: Cursed Words](https://store.steampowered.com/app/3856460/) — опис, трейлер, структура забігу, кількість предметів, персонажів, босів і викликів; Buried Things / Forklift Interactive, 02.04.2026.
- [Cursed Words Wiki](https://cursedwords.wiki.gg/) — сторінки Tiles, Curses, Chess, Letters, Stickers, Stamps, Items, Bosses (кожен бос окремо), Crowns, Quests, Daily, List of pins, Hungry Snake, Footprints, Head In The Clouds, Honeypot, Ruler, Knight Time.
- [Rogueliker: огляд](https://rogueliker.com/cursed-words-roguelike-puzzle-game/) — сітка 5×5, повʼязані плитки, вартості як у Scrabble, раунд із пʼяти сіток, магазин, 5 слотів стікерів і штампів.
- Steam News (`ISteamNews/GetNewsForApp`, appid 3856460) — патчі v3.15–v4.12: словники ES/DE/FR, показ «справжніх» слів, Down Under ×−3, Cursedle без retry, DLC «The Madness of Michael».
- [Steam: демо](https://store.steampowered.com/app/4264890/) — 27.01.2026, 8 персонажів і 16 босів у демо-описі.
- YouTube: пошук «Cursed Words Buried Things gameplay».

## Непевне
- (?) Суміжність шляху: 8 сусідів, як у Boggle, чи 4 — джерела кажуть лише «link these tiles»; чи можна двічі взяти плитку в одному слові.
- (?) Одне слово на сітку і пʼять сіток на зустріч — з огляду Rogueliker і непрямо з вікі («You get 1 fewer grid»), прямо не сказано.
- (?) Чи кінчається забіг, якщо ціль не набрано, — не перевірено; так у Balatro.
- (?) Точна формула WORD SCORE (порядок додатків і множників) і що буває з невалідним словом.
- (?) WHITE «travel to anywhere» — стрибок із білої плитки чи на неї.
- (?) Вибір корони перед забігом — окремим вікном чи в меню персонажа; чи досягнення показані в грі, а не лише в Steam.
- (?) Purple-корона: «один з двох босів етапу проклятий» — чи гравець обирає боса з двох, а Steam каже про одного боса на етап.
- (?) Тег Steam «Moddable» — підтримки модів у джерелах не бачив; «фінальна сітка-пазл» з патчу v4.9 — не зʼясовано, що це.
