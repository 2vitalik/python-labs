---
title: Scrabble (цифрові версії; Words With Friends)
slug: scrabble
family: word-number
also: [board-digital]
klass: cursor
axes:
  field: square
  time: turn
  opponent: online
  info: hidden
  random: runtime
  goal: score
year: 1948
platforms: [board, PC, web, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Scrabble", best: true, note: "повні правила: премії, бінго, обмін, челендж, кінець гри, розподіл плиток"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Words_with_Friends", note: "цифровий еталон: 104 плитки, бінго 35, інший розклад премій, power-ups, асинхронні партії"}
  - {kind: other, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=scrabble", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=how+to+play+scrabble+rules", note: "пошук; правила"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=words+with+friends+gameplay", note: "пошук; цифровий інтерфейс"}
stage: v1
coverage: 65
mechanics: [hot-seat, turn-enforcement, move-timer, ai-opponent, ai-greedy, drag-drop-piece, event-points, score-records, profile-stats, leaderboard, end-screen, game-screen, save-game, +word-validation, +premium-squares, +tile-rack, +tile-bag-draw, +line-placement, +cross-word-scoring, +bingo-bonus, +blank-tile, +tile-exchange, +word-challenge, +endgame-rack-penalty, +move-generator]
proposes: ["+trigger:input", "+trigger:turn_end", "+cond:in_dictionary", "+cond:legal", "+effect:score", "+effect:give", "+effect:take", "+effect:pass_turn", "+effect:end_turn", "+role:tile", "+role:zone", "+ui:tile-rack", "+ui:score-preview", "+ui:tiles-left", "+ui:shuffle-button", "+ui:recall-button", "+window:tile-bag-window", "+window:game-list", "+window:word-lookup", "+feature:async-multiplayer", "+feature:word-strength", "+feature:post-game-analysis", "+axis:session"]
author: opus
date: 2026-11-02
---

# Scrabble — виклади слово з руки на 15×15 так, щоб перехрестити чужі й зібрати премії

## Суть
Гравці по черзі викладають на спільне поле 15×15 слова з 7 плиток своєї «руки», підʼєднуючи їх до вже викладених, як у кросворді. Очки — сума вартостей літер усіх утворених слів з урахуванням премійних клітин (×2/×3 літери чи слова); використати всі 7 плиток — бонус. Рука поповнюється з мішка наосліп, тож гра — суміш словникового знання, геометрії поля й керування рукою. Цифрові версії (Words With Friends, офіційні Scrabble-застосунки) додають автоматичну перевірку слів, асинхронні партії, AI і підказки.

## Поле і час
- Поле 15×15 = 225 клітин; центр H8 — зірка (старт). Шари: премія клітини (постійна) + плитка (кладеться назавжди).
- Премії (класичний Scrabble): 24 DL (×2 літера), 12 TL (×3 літера), 17 DW (×2 слово, разом з центром), 8 TW (×3 слово); розклад симетричний. У Words With Friends — інший розклад (TW не в кутах, TL і TW можна зачепити одним словом).
- Хід = одна дія гравця (викласти / обміняти / пасувати). Онлайн — асинхронно: хід може тривати години, одночасно десятки партій (WWF: до 40).
- Прихована інформація: рука суперника й порядок плиток у мішку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка-літера | tile | літера, вартість 1–10 | лежить у мішку → руці → на полі; на полі незмінна |
| Бланк | tile | вартість 0, літера призначається при викладанні | діє як будь-яка літера; призначена літера фіксована до кінця гри |
| Мішок | container | 100 плиток (Scrabble EN) / 104 (WWF) | видає випадкові плитки; кількість лишених видно |
| Рука (rack) | container | ≤ 7 плиток | поповнюється до 7 після ходу, доки є в мішку |
| Клітина DL / TL | zone | ×2 / ×3 до літери | діє лише на плитку, викладену цим ходом |
| Клітина DW / TW | zone | ×2 / ×3 до слова | множить усе слово, включно зі старими плитками; лише цим ходом |
| Центральна зірка | zone | DW у Scrabble | перше слово мусить її покрити |
| Гравець | player | рахунок, рука | 2–4 сторони, хід по черзі |

Розподіл EN (Scrabble): A9 B2 C2 D4 E12 F2 G3 H2 I9 J1 K1 L4 M2 N6 O8 P2 Q1 R6 S4 T6 U4 V2 W2 X1 Y2 Z1 + 2 бланки; вартості: 1 — A E I L N O R S T U · 2 — D G · 3 — B C M P · 4 — F H V W Y · 5 — K · 8 — J X · 10 — Q Z (?).

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «кожен тягне 1 плитку; найближча до A ходить першою (бланк найкращий)»`, `give(each, 7 tiles)`.
- КОЛИ `input(play)` → ЯКЩО перший хід → ТО вимога: ≥ 2 плитки й одна з них на центрі H8.
- КОЛИ `input(play)` → ЯКЩО `legal(move)` → ТО `score(sum(words))`, `give(player, draw(min(7−rack, bag)))`, `end_turn`; інакше `block` + `message`.
- `legal(move)`: усі нові плитки в одному рядку або стовпці; між ними немає порожніх клітин (проміжки заповнені старими плитками); хоча б одна нова плитка сусідить з наявною (крім першого ходу); діагоналей нема.
- Усі слова, утворені ходом (головне + кожне перпендикулярне, що зачепило нову плитку), мусять бути `in_dictionary`. У цифрових версіях невалідний хід просто не приймається; у настільній — через челендж.
- Рахунок слова: сума вартостей літер, де нові плитки на DL/TL множаться; потім слово множиться на всі DW/TW під новими плитками (два DW = ×4, два TW = ×9). Премія під старою плиткою вже «витрачена».
- КОЛИ `count(tiles_played, ==, 7)` → ТО `score(+50)` — бінго (WWF: +35).
- Бланк: КОЛИ `input(place blank)` → ТО `choose(letter)`; вартість 0, але премія слова діє.
- КОЛИ `input(exchange k)` → ЯКЩО `count(bag, >=, 7)` → ТО `take(player, k)`, `give(player, k new)`, `score(0)`, `end_turn`.
- КОЛИ `input(pass)` → ТО `score(0)`, `pass_turn`.
- Челендж (настільна/клубна): КОЛИ `input(challenge)` → ЯКЩО хоч одне слово невалідне → ТО `custom: «плитки повертаються в руку, 0 очок»`; інакше челенджер втрачає хід (double) / нічого (free) / −5 очок (WESPA).
- КОЛИ `count(rack, ==, 0) and count(bag, ==, 0)` → ТО `game_over`: кожен віднімає суму своїх плиток у руці; той, хто вийшов, додає суму чужих.
- КОЛИ шість поспіль безочкових ходів → ТО `game_over` (за рішенням гравця).
- Цифрове: КОЛИ `timer(turn_time, ==, 0)` (асинхронний ліміт, напр. дні) → ТО `custom: «автоматична поразка / резиґнація»` (?).
- Перемога: більше очок після фінального перерахунку · Поразка: менше / резиґнація / тайм-аут · Нічия: у турнірах — по ½.

## Керування і ввід
- Drag-n-drop плитки з руки на клітину; або тап по плитці, потім по клітині; плитку на полі (цього ходу) можна стягнути назад.
- Кнопки: Play/Submit, Shuffle (перемішати руку), Recall (повернути всі плитки цього ходу в руку), Swap/Exchange (вибір плиток для обміну), Pass, Resign.
- Бланк: після викладання — вікно вибору літери.
- Під час розкладання — `score-preview` біля останньої плитки (скільки очок дасть хід), підсвітка валідності (?).
- Черга ходів жорстка: поле заблоковане, коли хід суперника.

## Вікна, меню, HUD
- `game-screen`: поле 15×15 з підписаними преміями (DL/TL/DW/TW), `tile-rack` з 7 плитками й вартостями, рахунки обох гравців, `turn-indicator`, `tiles-left` (у мішку), остання гра суперника підсвічена, кнопки Play/Shuffle/Recall/Swap/Pass.
- `game-list` (WWF): список активних партій «твій хід / їхній хід», запрошення, завершені.
- `tile-bag-window`: які плитки ще не вийшли (мішок + рука суперника) — класичний «трекінг плиток» вбудовано.
- `word-lookup`: значення зіграного слова зі словника (тап по слову).
- `log-window` / `move-list`: історія ходів з очками.
- `confirm-dialog`: резиґнація, обмін.
- `end-screen`: фінальні рахунки, бонус/штраф за руку, найкраще слово, кнопка Rematch; `post-game-analysis` (WWF/офіційні застосунки: найкращий можливий хід кожного разу) (?).
- `lobby-window`: пошук суперника (друг за ніком, випадковий Smart Match, спільнота).
- `chat-box` у партії (WWF).
- `stats-window` / `profile-window`: партій, перемог, середній бал за хід, найкраще слово.
- Переходи: `game-list` → `game-screen` партії; кінець партії → `end-screen` → Rematch → новий `game-screen`.

## Фічі поза полем
- `async-multiplayer`: хід надсилається, суперник отримує push; кілька партій паралельно.
- `ai-opponent-levels`: соло проти бота (простий бот — жадібний за очками).
- `hint` / power-ups (WWF): Word Radar (підсвічує клітини, де можна скласти слово), Swap+ (обмін без втрати ходу), Hindsight (найкращий хід суперника після факту), Word Clue; «Word Strength» — сила твого ходу відносно найкращого можливого.
- `stats`, `leaderboard-online`, рейтинги (офіційні застосунки).
- Вибір словника (NWL/TWL, Collins у офіційних; ENABLE+ у WWF) — `custom-rules`.
- `turn-timer` у швидких режимах (?), `local-multiplayer` пасом-і-грай.

## Варіації й родичі
- Words With Friends: 104 плитки, бінго 35, інші вартості й розклад премій; Scrabble GO, NYT Crossplay (2025–2026).
- Upwords — плитки кладуться поверх інших (висота до 5); Mathable — те саме з арифметикою; Bananagrams — без поля, кожен свій кросворд, на швидкість; Boggle — без розміщення, пошук шляхів.
- Скрабл-варіанти: Super Scrabble (21×21, ×4 клітини), Duplicate Scrabble (усі грають ту саму руку, рахується найкращий хід), Clabbers (слово — будь-яка анаграма).
- **Осі варіацій:** топологія (плоско / стос у висоту) · розподіл плиток і вартості · бінго-бонус · перевірка слова (челендж / автомат) · що спільне (одне поле / свої поля) · доступ до руки (прихована / спільна в Duplicate).

## Цікавинки для курсу
- Легальність викладання (одна лінія, без дірок, звʼязність, перший хід через центр) — 🥈.
- Підрахунок очок усіх утворених слів з преміями, що діють лише на нові плитки — 🥈 (пошук перпендикулярних слів від кожної нової плитки).
- Мішок і рука: тягнення до 7, обмін лише за ≥ 7 у мішку, кінцевий перерахунок рук — 📎.
- Бланк із призначеною літерою й нульовою вартістю — 📎.
- Перевірка слів за словником-файлом (set / trie) — 🌱.
- AI, що генерує всі легальні ходи (anchor squares + cross-checks, trie/DAWG/GADDAG) і бере максимум — 🥇; оцінка «залишку руки» — 👑.
- «Word Radar» — підсвітка клітин, де існує хоч один легальний хід — 🥇 (той самий генератор).

## Мапа на каталог
- Є: `hot-seat` ↔ пас-і-грай · `turn-enforcement` · `move-timer` ↔ таймери ходу/шаховий годинник у турнірах · `ai-opponent` / `ai-greedy` ↔ бот за очками · `drag-drop-piece` ↔ плитки з руки · `cell-click` · `event-points` ↔ вартості літер · `score-records` · `profile-stats` · `leaderboard` · `save-game` ↔ асинхронні партії живуть між сесіями · `completion-detection` ↔ кінець гри (мішок і рука порожні) · `end-screen` · `game-screen` · `help-window` · `settings-window`.
- **Нема** → пропозиції карток:
  - `+word-validation` — див. wordle.md.
  - `+premium-squares` «Премійні клітини ×2/×3 літери/слова» · game-logic/score · 📎 · слоти {layout: file}.
  - `+tile-rack` «Рука з N плиток» · entities/state · 📎 · слоти {size: 7}.
  - `+tile-bag-draw` «Мішок і тягнення наосліп» · entities/spawn · 🌱 · слоти {distribution: table}.
  - `+line-placement` «Викладання в одну лінію зі звʼязністю» · entities/legality · 🥈.
  - `+cross-word-scoring` «Рахунок усіх утворених слів» · game-logic/score · 🥈.
  - `+bingo-bonus` «Бонус за всю руку» · game-logic/score · 🌱 · слоти {bonus: 50|35}.
  - `+blank-tile` «Джокер-плитка з призначеною літерою» · entities/state · 📎.
  - `+tile-exchange` «Обмін плиток замість ходу» · game-logic/opponent · 🌱.
  - `+word-challenge` «Челендж слова суперника» · game-logic/opponent · 📎 · слоти {penalty: double|free|points}.
  - `+endgame-rack-penalty` «Штраф за плитки в руці на кінець» · game-logic/score · 🌱.
  - `+move-generator` «Генератор усіх легальних ходів (AI, підказки)» · game-logic/opponent · 🥇.

## Пропозиції до словників
- `+trigger:input` (play / exchange / pass / challenge), `+trigger:turn_end`.
- `+cond:in_dictionary`, `+cond:legal` — легальність викладання.
- `+effect:give` / `+effect:take` — тягнення з мішка й обмін; `+effect:pass_turn`, `+effect:end_turn`.
- `+role:tile`, `+role:zone` (премійна клітина).
- `+ui:tile-rack` — рука плиток; `+ui:score-preview` — живе превʼю очок ходу; `+ui:tiles-left` — лічильник мішка; `+ui:shuffle-button`, `+ui:recall-button`.
- `+window:tile-bag-window` — невийдені плитки; `+window:game-list` — список паралельних асинхронних партій; `+window:word-lookup` — значення слова.
- `+feature:async-multiplayer` — хід надсилається, партія живе днями; `+feature:word-strength` — оцінка ходу відносно найкращого; `+feature:post-game-analysis`.
- `+axis:session` — `match`, але асинхронний (днями).

## Джерела
- ⭐ [Wikipedia: Scrabble](https://en.wikipedia.org/wiki/Scrabble) — правила: поле, премії (24/12/17/8), 100 плиток, викладання, рахунок, бінго 50, обмін, челендж, кінець гри, словники NWL/Collins, історія (Butts, Brunot).
- [Wikipedia: Words With Friends](https://en.wikipedia.org/wiki/Words_with_Friends) — відмінності: 104 плитки, бінго 35, розклад премій, ENABLE-словник, power-ups, Word Strength, до 40 партій.
- [BGG: пошук Scrabble](https://boardgamegeek.com/geeksearch.php?action=search&q=scrabble) — варіанти й обговорення.
- YouTube: пошуки «how to play scrabble rules», «words with friends gameplay».

## Непевне
- (?) Розподіл і вартості плиток EN — з памʼяті (вікі підтверджує лише 100 плиток, 1–10 очок, 2 бланки).
- (?) Точний розклад премій WWF і вартості його плиток — не виписано; вікі каже лише «інший розклад» і «деякі вартості інші».
- (?) Тайм-аут асинхронної партії, швидкі режими з таймером, пост-аналіз партії — з памʼяті про застосунки, не перевірено.
- (?) Підсвітка валідності слова під час розкладання — є в частині застосунків, не в усіх.
