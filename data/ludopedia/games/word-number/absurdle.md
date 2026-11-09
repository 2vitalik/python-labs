---
title: Absurdle
slug: absurdle
aka: [Адверсарний Wordle]
family: word-number
also: [hidden-deduction]
klass: puzzle
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: none
  goal: state
year: 2022
platforms: [web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Absurdle", best: true, note: "суть адверсарного алгоритму, нескінченні спроби, Hatetris як предок"}
  - {kind: official, url: "https://qntm.org/absurdle", note: "сторінка автора (qntm); fetch-ем віддає 403"}
  - {kind: other, url: "https://www.wlrn.org/2022-01-23/youve-heard-of-wordle-now-get-ready-for-sweardle-and-absurdle", note: "стаття 2022: автор, «менше 4 спроб не виграти»"}
  - {kind: other, url: "https://nerdschalk.com/absurdle-game-like-wordle-what-is-it-where-and-how-to-play-rules-explained/", note: "режими Hard / Challenge / Timed / Expanded, кнопка випадкової спроби"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=absurdle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [keyboard-controls, cell-click, completion-detection, word-validation, ai-opponent, game-screen, help-window, settings-window, mode-select, end-screen, share-result, time-out, +letter-feedback, +adversarial-answer, +hard-mode, +keyboard-state, +candidate-buckets, +target-forcing-mode, +expanded-dictionary]
proposes: ["+cond:consistent_with_hints", "+effect:prune_candidates", "+ui:on-screen-keyboard", "+ui:random-guess-button", "+feature:hard-mode", "+feature:mode-challenge", "+feature:expanded-dictionary"]
author: opus
date: 2026-11-09
---

# Absurdle — Wordle, де слово не загадане: гра після кожної спроби обирає найгіршу для тебе відповідь

## Суть
Інтерфейс як у Wordle: вводиш 5-літерне слово, отримуєш кольори. Але секретного слова нема — гра тримає множину всіх слів, сумісних з усіма відповідями, і після кожної спроби обирає той колірний патерн, що лишає найбільше кандидатів. Виграєш, коли зведеш множину до одного слова і введеш його. Ідея перенесена з Hatetris того ж автора (qntm): супротивник — не випадковість, а алгоритм, що мінімізує твою інформацію.

## Поле і час
- Поле — рядки по 5 клітин, як у Wordle, але рядків не 6: кількість спроб не обмежена, поле росте вниз.
- Під полем — екранна клавіатура зі станами літер.
- Хід = одна підтверджена спроба; часу нема (крім режиму Timed). Нема щоденної задачі: гра детермінована, однакова для всіх, доки однакові спроби (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Множина кандидатів | zone (прихована) | список слів-відповідей (~2 000+) | після спроби звужується до одного «відра» патерну |
| Відро (bucket) | zone (прихована) | патерн кольорів, слова з цим патерном | тимчасове: усі відра будуються заново на кожну спробу |
| Рядок спроби | zone | 5 клітин | заморожується після підтвердження |
| Плитка-літера | tile | літера, стан empty/typed/green/yellow/grey | колір — за обраним відром, не за «справжнім» словом |
| Клавіша клавіатури | tile (UI) | найкращий відомий стан | фарбується, як у Wordle |
| Словник допустимих спроб | static | ширший за список відповідей | спроба поза ним відхиляється |
| Цільове слово (Challenge) | static | 1 слово, видно гравцеві | лише в Challenge mode: його треба змусити стати відповіддю |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(letter)` → ЯКЩО `count(typed, <, 5)` → ТО `custom: «літера в наступну клітину активного рядка»`.
- КОЛИ `input(enter)` → ЯКЩО `not in_dictionary(guess)` → ТО `message("not a word")`; спроба не рахується (?).
- КОЛИ `input(enter)` → ЯКЩО `mode(hard) and not consistent_with_hints(guess)` → ТО `custom: «спроба відхилена: треба вжити всі літери з позитивним відгуком»`.
- КОЛИ `input(enter)` → ЯКЩО слово валідне → ТО `custom: «розбити кандидатів на відра за патерном, який дала б кожна можлива відповідь»`.
- КОЛИ `after(розбиття)` → ТО `prune_candidates(largest bucket)` — лишити найбільше відро (найменше інформації гравцеві).
- КОЛИ `after(prune_candidates)` → ТО `feedback(guess)`, `paint(tiles, pattern відра)`, `paint(keys, max(state))`.
- Сірі літери прибирають усі слова, де є ця літера: тому ранні спроби майже завжди «всі сірі».
- КОЛИ `pattern(row all green)` → ТО `win`, `window(end-screen)` з кількістю спроб.
- КОЛИ `input(random guess)` → ТО `custom: «вписати в рядок випадкове допустиме слово»`.
- Challenge mode: КОЛИ `win` → ЯКЩО `not same(answer, target)` → ТО `custom: «виклик провалено — треба було загнати гру саме в це слово»` (?).
- Timed mode: КОЛИ `counter(time_left, ==, 0)` → ТО `lose` (60 секунд за джерелом).
- Перемога: множина = 1 слово і воно введене · Поразка: нема (крім Timed і Challenge) · Рахунок: кількість спроб, менше — краще.

## Керування і ввід
- Фізична клавіатура або екранна: літери, Backspace, Enter.
- Кнопка випадкової спроби в правому нижньому куті клавіатури.
- Курсора по клітинах нема; ввід — у наступну вільну клітину.

## Вікна, меню, HUD
- `game-screen`: поле спроб (росте), `on-screen-keyboard` зі станами, `random-guess-button`.
- `help-window`: пояснення «Absurdle — це Wordle, що змінює відповідь» (?).
- `settings-window` / `mode-select`: Hard mode, Challenge mode, Timed, Expanded word list (?): точний вигляд меню не бачив.
- `end-screen`: виграш за N спроб, кнопка поширення (?).
- Переходи: старт → `game-screen` → перемога → `end-screen` → нова гра.

## Фічі поза полем
- `hard-mode` — як у Wordle: наступні спроби мусять містити всі літери з позитивним відгуком.
- `mode-challenge` — дано цільове слово; треба вести спроби так, щоб адверсарій сам опинився на ньому.
- `mode-time-attack` (Timed) — 60 секунд на виклик.
- `expanded-dictionary` — список відповідей розширено рідкісними словами (AAHED, XYLYL).
- `share-result` (?), `undo`/`hint` — нема.

## Варіації й родичі
- Предок ідеї: Hatetris (qntm) — Tetris, що завжди дає найгіршу фігуру.
- Wordle (`wordle.md`) — той самий фідбек, але слово фіксоване; Absurdle — це Wordle з minimax-супротивником.
- Mastermind з адверсарним кодувальником («cheating Mastermind»), Kaboom (`hidden-deduction/kaboom.md`) — міни, що «переміщуються» проти гравця, коли ти вгадуєш.
- Quordle / Nerdle (`nerdle.md`) — інші осі тієї ж оболонки.
- **Осі варіацій:** вибір відра (найбільше / найменш інформативне за ентропією / випадкове велике) · тай-брейк (?) · ліміт спроб (нема / таймер) · ціль (будь-яке слово / заданий таргет) · обмеження спроб (вільно / hard mode).

## Цікавинки для курсу
- Розбиття множини кандидатів на ≤243 відра за патерном і вибір найбільшого — 🥈: чистий алгоритм над словником, а гра виглядає «як Wordle».
- Обчислення патерну з дублікатами (два проходи) як ключ для групування — 🥉 (повторне використання з Wordle).
- Challenge mode: шукати послідовність спроб, що змушує адверсарія лишити саме таргет, — 👑: гра-проти-алгоритму, пошук у дереві відповідей.
- Hard mode як валідатор проти історії відгуків — 📎.
- Таймер 60 с і кнопка випадкової спроби — 🌱.
- Розвʼязувач «мінімум спроб проти адверсарія» (minimax по дереву відер) — 🥇.

## Мапа на каталог
- Є: `keyboard-controls` · `cell-click` ↔ екранна клавіатура · `completion-detection` ↔ 5 зелених · `word-validation` ↔ спроба мусить бути словом · `ai-opponent` ↔ адверсарій · `time-out` ↔ Timed · `share-result` (?) · `game-screen` · `help-window` · `settings-window` · `mode-select` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+letter-feedback`, `+keyboard-state`, `+hard-mode`, `+adversarial-answer` — див. `wordle.md`.
  - `+candidate-buckets` «Групування кандидатів за патерном відгуку» · game-logic/opponent · 🥈 · слоти {pick: largest|max-entropy}.
  - `+target-forcing-mode` «Загнати адверсарія в задану відповідь» · game-logic/win · 🥇.
  - `+expanded-dictionary` «Перемикач розширеного словника відповідей» · game-logic/difficulty · 🌱.

## Пропозиції до словників
- `+cond:consistent_with_hints` — спроба не суперечить відкритим підказкам (hard mode; Wordle, Absurdle, Nerdle).
- `+effect:prune_candidates` — звузити приховану множину станів до обраної підмножини (Absurdle, адверсарний Kaboom).
- `+ui:on-screen-keyboard` — екранна клавіатура зі станами літер.
- `+ui:random-guess-button` — вписати випадкову допустиму спробу.
- `+feature:hard-mode` — опційне посилення правил спроби.
- `+feature:mode-challenge` — режим з заданою ціллю, яку треба нав'язати системі.
- `+feature:expanded-dictionary` — розширений словник як налаштування складності.

## Джерела
- ⭐ [Wikipedia: Absurdle](https://en.wikipedia.org/wiki/Absurdle) — адверсарна суть, нескінченні спроби, Hatetris.
- [WLRN, 2022](https://www.wlrn.org/2022-01-23/youve-heard-of-wordle-now-get-ready-for-sweardle-and-absurdle) — автор Sam Hughes (qntm), «менше ніж за 4 спроби не виграти» (слова автора).
- [Nerdschalk: правила Absurdle](https://nerdschalk.com/absurdle-game-like-wordle-what-is-it-where-and-how-to-play-rules-explained/) — найбільше відро, режими Hard / Challenge / Timed / Expanded, кнопка випадкової спроби.
- [qntm.org/absurdle](https://qntm.org/absurdle) — офіційна сторінка (не відкрилась: 403).
- YouTube: пошук «absurdle gameplay».

## Непевне
- (?) Тай-брейк між однаково великими відрами — офіційне пояснення qntm не вдалося відкрити (403).
- (?) Розмір списку відповідей «2 000+» — з вторинного джерела; точні списки не бачив.
- (?) Чи можна виграти за 2 спроби: WLRN цитує автора «не менше 4», Nerdschalk — «2 не виключено»; можливо, змінилось між версіями.
- (?) Деталі Challenge mode (що буде, якщо адверсарій лишив інше слово) і вигляд меню режимів — не бачив сам.
- (?) Наявність share-кнопки, поведінка на неіснуючому слові — з памʼяті.
