---
title: Cryptic crossword (Криптичний кросворд)
slug: cryptic-crossword
aka: [Cryptic, British crossword, Криптичний кросворд, Cryptic puzzle]
family: word-number
also: [pencil-logic]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: hidden
  random: none
  goal: constraints
year: 1925
platforms: [paper, web, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Cryptic_crossword", best: true, note: "сітки (15×15, половина клітин checked, barred), будова підказки, enumeration, усі типи підказок з індикаторами і прикладами, Ximenes/Libertarian, Torquemada, історія"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Crossword", note: "загальні правила сіток: across/down, нумерація, американська проти британської"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=how+to+solve+cryptic+crossword", note: "пошук; розвʼязування (напр. Cracking the Cryptic)"}
stage: v1
coverage: 50
mechanics: [cell-click, keyboard-controls, selection-highlight, word-validation, completion-detection, satisfy-constraints, conflict-highlight, daily-puzzle, level-bank, save-progress, difficulty-levels, game-screen, help-window, puzzle-select, +across-down-entry, +enumeration, +clue-list, +definition-plus-wordplay, +anagram-clue, +hidden-word-clue, +container-clue, +reversal-clue, +homophone-clue, +double-definition, +charade-clue, +deletion-clue, +letter-selection-clue, +checked-unchecked-cells, +barred-grid, +reveal-letter, +check-entry, +anagram-helper]
proposes: ["+cond:fits_enumeration", "+cond:crossings_agree", "+effect:reveal_letter", "+ui:clue-list", "+ui:current-clue-bar", "+ui:enumeration", "+feature:check-entry", "+feature:anagram-helper", "+feature:prize-puzzle"]
author: opus
date: 2026-11-09
---

# Cryptic crossword — кросворд, де кожна підказка — загадка з двох частин: означення відповіді + словесна гра (анаграма, приховане слово, вставка, реверс…)

## Суть
Сітка британського типу з чорними клітинами, де лише близько половини клітин перетинаються двома словами. Кожна підказка містить означення (синонім відповіді на початку або в кінці) і «subsidiary indication» — інструкцію словесної гри, з якої відповідь збирається з частин. Поверхове прочитання підказки — навмисна обманка; слова-індикатори («shredded», «hides», «returned», «we hear») підказують тип операції. Довжина відповіді дана в дужках: «(8)», «(7,9)». Паперова класика; описую як цифрову версію з позначкою «(цифрова версія)», а типи підказок — як правила гри.

## Поле і час
- Типово 15×15 з поворотною симетрією 180°; The Times Quick Cryptic — 13×13, jumbo — 23×23.
- **Checked / unchecked клітини:** у британській сітці лише ~половина клітин перевіряється перетином; The Times вимагає, щоб перетиналось ≥ половини літер кожного слова.
- Advanced-варіант — barred grid ~12×12: без чорних клітин, межі слів — товсті риски; перетинається ≥ ¾ літер.
- Шари: клітина (біла / чорна), номер у першій клітині слова, вписана літера; поза полем — списки Across і Down з enumeration.
- Часу нема; у змаганнях і застосунках — секундомір.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Біла клітина | tile | літера / порожньо; checked чи unchecked | приймає одну літеру; checked — спільна для Across і Down |
| Чорна клітина | static | — | розділяє слова |
| Риска (barred grid) | static | межа між клітинами | закінчує слово замість чорної клітини |
| Номер | mark | 1…N | у першій клітині слова; спільний для Across/Down, якщо обидва стартують тут |
| Слово-відповідь | zone | номер, напрямок, enumeration (наприклад 7,9) | ланцюг клітин; збігається з відповіддю |
| Підказка | static | текст: означення + wordplay + звʼязка | лежить у списку Across/Down |
| Означення | mark | частина підказки | синонім відповіді тієї ж частини мови, часу, числа |
| Індикатор | mark | слово-маркер типу | вказує операцію: анаграма, вставка, реверс… |
| Фодер (fodder) | mark | літери / слова підказки | сировина для операції |

## Правила (КОЛИ → ЯКЩО → ТО)
Вписування (цифрова версія):
- КОЛИ `input(type letter)` → ЯКЩО `free(cell)` or `custom: «перезапис літери»` → ТО `set_value(cell, letter)`, `custom: «курсор на наступну клітину слова»`.
- КОЛИ `input(click cell)` → ЯКЩО `state(cell, selected)` → ТО `custom: «перемкнути напрямок Across ↔ Down»`.
- КОЛИ `custom: «слово заповнене»` → ЯКЩО `custom: «довжина й пробіли збігаються з enumeration»` and `custom: «перетини узгоджені з сусідніми словами»` → ТО `custom: «слово кандидат»`.
- КОЛИ `all_constraints_met` → ЯКЩО `custom: «усі літери = розвʼязку автора»` → ТО `win`, `window(end-screen)`.

Будова підказки (кожна правильна підказка):
- КОЛИ `custom: «підказка»` → ТО `custom: «відповідь = означення (на початку або в кінці) і водночас = результат wordplay; звʼязки from / gives / could be між ними»`.
- Ximenean-принцип: точне означення + чесна інструкція + нічого зайвого; Libertarian-видання (The Guardian) дозволяють вільніший синтаксис.

Типи підказок як правила (індикатор → операція):
- Анаграма: КОЛИ `custom: «індикатор shredded / dancing»` → ТО `custom: «відповідь = перестановка літер фодера»`. «Chaperone shredded corset (6)» → ESCORT.
- Шарада: КОЛИ `custom: «частини поспіль»` → ТО `custom: «відповідь = склейка частин»`. «Outlaw leader managing money (7)» → BAN + KING.
- Вставка / контейнер: КОЛИ `custom: «індикатор about / inside / around»` → ТО `custom: «одна частина всередині іншої»`. «Utter nothing when there's wickedness about (5)» → VOICE.
- Видалення: КОЛИ `custom: «beheaded / endlessly / heartlessly»` → ТО `custom: «прибрати першу / останню / середню літеру»`. «Beheaded celebrity is sailor (3)» → TAR.
- Подвійне означення: КОЛИ `custom: «два означення без wordplay»` → ТО `custom: «відповідь підходить до обох»`. «Not seeing window covering (5)» → BLIND.
- Приховане слово: КОЛИ `custom: «індикатор hides / in / some»` → ТО `custom: «відповідь — підрядок тексту підказки через межі слів»`. «Found ermine, deer hides damaged (10)» → UNDERMINED.
- Перші / останні / непарні літери: КОЛИ `custom: «initially / ends / odd»` → ТО `custom: «вибрати відповідні літери слів»`. «Initially amiable person eats primate (3)» → APE.
- Гомофон: КОЛИ `custom: «we hear / reportedly / on the radio»` → ТО `custom: «відповідь звучить як фодер»`. «We hear twins shave (4)» → PARE.
- Реверс: КОЛИ `custom: «returned; у Down — rising»` → ТО `custom: «фодер задом наперед»`. «Returned beer fit for a king (5)» → REGAL.
- Криптичне означення: КОЛИ `custom: «уся підказка — означення-обманка, часто з ?»` → ТО `custom: «відповідь за переносним змістом»`. «Flower of London? (6)» → THAMES.
- Спунеризм: КОЛИ `custom: «Spooner's»` → ТО `custom: «обміняти початкові звуки двох слів»`.
- Паліндром, letter bank, reverse anagram — рідкісні типи з окремими індикаторами.
- &lit: КОЛИ `custom: «уся підказка = і означення, і wordplay»` → ТО `custom: «обидва читання дають ту саму відповідь»`. «Spoil vote! (4)» → VETO.
- Скорочення: КОЛИ `custom: «circa, why, you, римські числа»` → ТО `custom: «C, Y, U, XI як готові шматки»`.
- Комбінація: КОЛИ `custom: «кілька індикаторів»` → ТО `custom: «операції в порядку синтаксису»` (реверс + вставка: HONORABLE).

Цифрові допомоги (?):
- КОЛИ `input(check)` → ТО `custom: «позначити хибні літери слова / сітки»`.
- КОЛИ `input(reveal)` → ТО `reveal(letter | word | grid)`.
- Перемога: уся сітка = розвʼязок · Поразки нема · Рахунок: час (змагання, онлайн-рейтинги (?)); у призових пазлах газет — перший правильний розвʼязок, витягнутий з надісланих.

## Керування і ввід
- Папір: вписати ручкою; пробіли у відповіді — з enumeration.
- (цифрова версія) клік по клітині або підказці → виділено слово; набір з клавіатури, Backspace — назад; Tab — до наступної підказки (?); повторний клік — зміна напрямку.
- Розвʼязування: вгадати, де означення, знайти індикатор, застосувати операцію до фодера, перевірити перетинами.

## Вікна, меню, HUD
- (цифрова версія) `game-screen`: сітка, `selection-highlight` поточного слова, `current-clue-bar`, `clue-list` (Across / Down, розвʼязані сірим), `enumeration`, кнопки `check-button` (літера / слово / сітка) і reveal, `timer-elapsed` (?).
- (цифрова версія) `confirm-dialog`: «Reveal all?», «Clear all?».
- (цифрова версія) `puzzle-select` / архів пазлів за датою і сетером; `help-window` — довідник типів підказок.
- (цифрова версія) `end-screen`: «розвʼязано», час.
- (цифрова версія) друк сітки — як у `codeword.md`.

## Фічі поза полем
- `daily-puzzle` (щоденні газетні), `puzzle-bank` (архів), `auto-check` / `check-entry`, `show-solution`, `save-progress` між сесіями.
- `anagram-helper` (?): розкладка літер фодера по колу або перемішування — у частині онлайн-розвʼязувачів.
- `prize-puzzle`: призовий пазл з надсиланням розвʼязку (Private Eye — £150 першому правильному витягнутому).
- Змагання клю-райтингу: Azed — щомісячний конкурс на найкращу підказку.
- Сетер під псевдонімом (Torquemada, Ximenes, Azed, Araucaria) — підпис як «рівень складності» видання.

## Варіації й родичі
- Класичний (американський) кросворд — кожна клітина checked, підказки-означення, без wordplay (черга `word-number`, ще не описаний).
- Barred / advanced cryptic (Azed, Listener, Mephisto) — без чорних клітин, рідкісні слова, без enumeration.
- Variety / themed cryptic — відповіді треба змінити перед вписуванням (додати, прибрати літеру, анаграмувати), іноді складаючи приховане повідомлення; «ніни» — сховані в сітці слова; панграми.
- Quick cryptic (The Times, 13×13) — легший вхід.
- Codeword (`codeword.md`) і Arrowword (`arrowword.md`) — інші гілки «вписати в сітку»; Bonza (`bonza.md`), Knotwords (`knotwords.md`) — сітка без підказок.
- **Осі варіацій:** сітка (чорні клітини / риски) · частка checked (½ / ¾ / усі) · підказки (означення / означення + wordplay / нема) · enumeration (є / нема) · тема (нема / відповіді змінюються перед вписуванням) · стиль (Ximenean / Libertarian).

## Цікавинки для курсу
- Модель сітки: номери з білих клітин, слова Across/Down, checked/unchecked — 🌱.
- Ввід зі зміною напрямку, автокурсор, підсвітка поточної підказки — 📎.
- Check / reveal по літері, слову, сітці — 🌱.
- Перевірка симетрії 180° і правила «≥ ½ літер checked» для генератора сіток — 📎.
- Помічник розвʼязування: за enumeration і вписаними літерами знайти кандидатів у словнику (шаблон «?A?E??») — 🥉.
- Валідатор типів підказки: перевірити, що відповідь — анаграма фодера / підрядок тексту / реверс — 🥉.
- Автогенерація криптичних підказок за типами — 👑 (семантика означень і правдоподібна поверхня).

## Мапа на каталог
- Є: `cell-click` · `keyboard-controls` · `selection-highlight` ↔ поточне слово · `word-validation` ↔ відповідь = розвʼязку · `completion-detection` · `satisfy-constraints` ↔ перетини й enumeration · `conflict-highlight` ↔ check · `daily-puzzle` · `level-bank` ↔ архів · `save-progress` · `difficulty-levels` ↔ quick / standard / advanced · `game-screen` · `help-window` · `puzzle-select`.
- **Нема** → пропозиції карток:
  - `+across-down-entry` «Ввід по словах Across/Down з перемиканням» · interface/input · 📎.
  - `+enumeration` «Довжина й будова відповіді (7,9) у підказці» · game-logic/constraints · 🌱.
  - `+clue-list` «Списки підказок з позначкою розвʼязаних» · interface/hud · 🌱.
  - `+definition-plus-wordplay` «Підказка = означення + інструкція» · game-logic/constraints · 🥈.
  - `+anagram-clue` · `+hidden-word-clue` · `+container-clue` · `+reversal-clue` · `+homophone-clue` · `+double-definition` · `+charade-clue` · `+deletion-clue` · `+letter-selection-clue` — типи словесної гри як окремі перевірки · game-logic/constraints · 🌱–🥉 кожна.
  - `+checked-unchecked-cells` «Частина клітин без перетину» · levels/format · 🌱.
  - `+barred-grid` «Межі слів рисками замість чорних клітин» · levels/format · 📎.
  - `+reveal-letter` (є в `codeword.md`) · `+check-entry` «Перевірити літеру/слово/сітку» · game-logic/constraints · 🌱.
  - `+anagram-helper` «Перемішувач літер фодера» · interface/input · 🌱.

## Пропозиції до словників
- `+cond:fits_enumeration` — вписане відповідає довжині й розбиттю (7,9) (кросворди всіх видів).
- `+cond:crossings_agree` — літери слова узгоджені з перпендикулярними словами.
- `+effect:reveal_letter` — показати правильну літеру клітини (Codeword, Cryptic, цифрові кросворди).
- `+ui:clue-list` — списки Across/Down (є також пропозиція з TypeShift).
- `+ui:current-clue-bar` — поточна підказка над/під сіткою.
- `+ui:enumeration` — довжина відповіді біля підказки.
- `+feature:check-entry` — перевірка літери/слова/сітки за розвʼязком.
- `+feature:anagram-helper` — допоміжне перемішування літер.
- `+feature:prize-puzzle` — пазл з надсиланням розвʼязку і розіграшем.

## Джерела
- ⭐ [Wikipedia: Cryptic crossword](https://en.wikipedia.org/wiki/Cryptic_crossword) — сітки (15×15, симетрія, ½ checked, правило The Times, barred ~12×12, ¾ checked, 13×13 / 23×23), будова підказки, enumeration, 15+ типів з індикаторами й прикладами, Ximenean/Libertarian, Torquemada (1925–1939), Afrit 1946, Ximenes 1966, конкурси Azed і Private Eye, ніни, панграми.
- [Wikipedia: Crossword](https://en.wikipedia.org/wiki/Crossword) — загальні конвенції сіток (across/down, нумерація, американські правила).
- YouTube: пошук «how to solve cryptic crossword».

## Непевне
- (?) Рік 1925: Torquemada почав у The Saturday Westminster 1925, «часто вважається винахідником»; точної дати першого криптичного кросворду стаття не дає (перший газетний кросворд у Британії — Sunday Express, 2.11.1924).
- (?) Цифрові допомоги (check / reveal / anagram helper / таймер / клавіатурні скорочення) — з загального знання сайтів газет; сторінку The Guardian відкрити не вдалося.
- (?) Онлайн-рейтинги часу — не перевірено; Times Crossword Championship у статті не згадано.
- Друга частина статті Wikipedia (після 100 тис. символів) не читалась — можуть бути ще варіанти.
</content>
</invoke>
