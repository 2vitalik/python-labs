---
title: "Puzzmo: Bongo"
slug: bongo
aka: [Bongo]
family: word-number
also: []
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: partial
  random: none
  goal: score
year: 2024
platforms: [web (Puzzmo), iOS (застосунок Puzzmo, 2025)]
links:
  - {kind: other, url: "https://seths.blog/2024/11/bongo-is-here/", best: true, note: "правила від автора (Seth Godin): лоток зі стопками літер, слова 3–5 літер, 2x/3x, бланк-зірочка, бонус-змійка згори вниз, бонус за поширені слова"}
  - {kind: other, url: "https://seths.blog/2024/11/game-design-and-strategy-bongo-part-3/", note: "дизайн: вартості плиток щодня інші, «нема правильної відповіді — є краща», rowScore/totalScore у share-лінку"}
  - {kind: other, url: "https://seths.blog/2024/11/bongo-4-thinking-about-power-users-skive/", note: "«проблема Scrabble» і бонус за поширені слова (ідея Zach Gage)"}
  - {kind: other, url: "https://playlin-site-production.pages.dev/game/bongo/", note: "гайд: 25 плиток + джокер, лише рядки, неонова бонус-лінія, Bongo Champion"}
  - {kind: other, url: "https://www.cindyderosier.com/2025/01/bongo-at-puzzmocom.html", note: "блог гравчині: 25 літер із 5 прихованих тематичних слів, тематичне слово стає фіолетовим"}
  - {kind: other, url: "https://apps.apple.com/us/app/-/id6714482734", note: "застосунок Puzzmo для iOS; про Bongo — один рядок, правил нема"}
  - {kind: play, url: "https://www.puzzmo.com/play/bongo", note: "грати (боту недоступно)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=puzzmo+bongo+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [daily-puzzle, word-validation, drag-drop-piece, pocket, event-points, leaderboard, share-result, game-screen, end-screen, help-window, save-progress, +letter-value-scoring, +premium-squares, +blank-tile, +row-only-words, +bonus-path-word, +common-word-bonus, +daily-letter-values, +hidden-theme-words, +partial-pool-use, +daily-champion]
proposes: ["+cond:length", "+cond:common_word", "+ui:row-score", "+ui:tile-value", "+ui:bonus-path-overlay", "+feature:daily-champion", "+feature:curator-note", "+card:row-only-words", "+card:bonus-path-word", "+card:common-word-bonus"]
author: opus
date: 2026-11-09
---

# Puzzmo: Bongo — сольний «Scrabble» 5×5: розклади літери з лотка в п'ять рядків-слів, рахуються лише рядки й одна бонус-змійка

## Суть
Щодня гравець отримує лоток літерних плиток (стопки однакових літер), бланк і порожню сітку 5×5 з клітинами 2x/3x. Треба скласти по слову в кожному ряду (3–5 літер) так, щоб сума вартостей літер з множниками була найбільшою; стовпці не перевіряються. Окремо підсвічена «змійка» клітин згори вниз — бонус-слово, а поширені слова отримують бонус замість рідкісних (антидот до «проблеми Scrabble»). Правильної відповіді нема — лише краща дошка; рахунок іде в денний лідерборд.

## Поле і час
- Сітка 5×5; кожен ряд — окреме слово зліва направо, 3–5 літер.
- Шари: клітина (звичайна / 2x / 3x, частина клітин належить бонус-змійці) + плитка-літера з вартістю.
- Поза полем: лоток зі стопками літер (25 літер, взятих із 5 прихованих тематичних слів) і бланк; усі не обовʼязково використати.
- Час: статичний пазл, без таймера (гайд — «2–5 хвилин»). Розкладка множників, вартості літер і змійка щодня інші.
- Масштаб очок: приклад зі share-лінків — CRUX у ряду 406, WEEKS у ряду 4 — 468, загальний рахунок 931–1074.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка-літера | tile | літера, вартість (щодня інша) | з лотка на клітину; переставляється; повертається в лоток (?) |
| Бланк (пастельна зірочка) | tile | вартість (?) | стає будь-якою літерою на вибір гравця |
| Лоток | zone | стопки однакових літер | джерело плиток; залишок не обовʼязковий |
| Клітина | terrain | звичайна | приймає одну плитку |
| Клітина 2x / 3x | terrain | множник ×2 / ×3 | множить вартість літери, що на ній лежить |
| Ряд | zone | 5 клітин | дає одне слово 3–5 літер; має власний rowScore |
| Бонус-змійка | zone | клітини різних рядів, читання згори вниз | якщо її літери складають слово — бонус |
| Тематичне слово | mark | 5 прихованих слів дня | ряд із таким словом фарбується фіолетовим |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «видати лоток: 25 літер із 5 тематичних слів + бланк; показати вартості й розкладку 2x/3x дня»`.
- КОЛИ `input(drag tile, cell)` → ЯКЩО `free(cell)` → ТО `place(player, tile)`; інакше `custom: «плитки міняються місцями або хід не приймається»` (?).
- КОЛИ `input(drag tile, tray)` → ТО `custom: «плитка повертається в лоток»` (?).
- КОЛИ `input(place blank)` → ТО `choose(літера A–Z)`, `set_value(blank, літера)`.
- КОЛИ `input(place)` → ЯКЩО `custom: «літери ряду утворюють суцільне слово з 3–5 літер»` і `in_dictionary(word)` → ТО `score(Σ вартість_літери × множник_клітини)` для ряду.
- КОЛИ `enter(tile, cell_2x|cell_3x)` → ТО `multiplier(2|3)` для вартості цієї літери.
- КОЛИ `input(place)` → ЯКЩО `custom: «слово є в частотному списку поширених»` → ТО `score(+бонус за поширене слово)` (розмір — у «Непевне»).
- КОЛИ `input(place)` → ЯКЩО `custom: «літери клітин змійки згори вниз — слово»` і `in_dictionary(word)` → ТО `score(+бонус-слово)`.
- КОЛИ `input(place)` → ЯКЩО `custom: «слово ряду — одне з 5 прихованих тематичних»` → ТО `paint(row, purple)`.
- Стовпці: `custom: «вертикальні послідовності не перевіряються й не рахуються»` — головна відмінність від Scrabble і Waffle.
- Лоток: `custom: «невикористані літери не штрафуються»` (?).
- КОЛИ `input(submit)` → ТО `window(end-screen)`, `custom: «рахунок у світовий денний лідерборд»`.
- КОЛИ `input(submit)` → ЯКЩО `custom: «рахунок вищий за попередній власний»` → ТО `custom: «кращу дошку можна подавати ще раз»` (?).
- КОЛИ `level_end` (кінець дня) → ЯКЩО `custom: «найвищий рахунок, поданий першим»` → ТО `custom: «звання Bongo Champion»`.
- КОЛИ `input(share)` → ТО `custom: «найкраще слово з очками ряду й загальним рахунком — у буфер обміну»`.
- Перемога: нема — краща дошка · Поразка: нема · Рахунок: Σ рядів (вартості × множники + бонус поширеного слова) + бонус-змійка.

## Керування і ввід
- Drag-and-drop плитки з лотка на клітину й між клітинами (миша/тач).
- Бланк: після розміщення — вибір літери.
- Кнопки: подати дошку, SHARE (копіює найкраще слово).

## Вікна, меню, HUD
- `game-screen`: сітка 5×5 з мітками 2x/3x і підсвіченою змійкою (`bonus-path-overlay`), лоток зі стопками (`pocket`), вартість на кожній плитці (`tile-value`), очки біля кожного ряду (`row-score`), `score` загальний.
- `end-screen`: рахунок, місце в лідерборді, записка куратора дня (тема й автор) (`curator-note`).
- `leaderboard`: світовий денний (платформа Puzzmo, також групи друзів (?)).
- `help-window`: правила (типово для Puzzmo (?)).
- Переходи: сторінка дня Puzzmo → `game-screen` → submit → `end-screen` → назад до дошки покращувати.

## Фічі поза полем
- `daily-puzzle`: новий набір щодня, кураторський — теми підбирають друзі Puzzmo, спільнота й гості; будь-хто може надіслати 8 тематичних слів, з яких беруть 5.
- `daily-champion`: звання за перший найвищий рахунок дня.
- `share-result`: найкраще слово з очками для соцмереж.
- Платформа Puzzmo: `leaderboard-online`, `streaks`, `stats`, збереження між пристроями (див. [pile-up-poker.md](pile-up-poker.md)).

## Варіації й родичі
- [scrabble.md](scrabble.md) — вартості літер, премійні клітини, бланк; Bongo прибирає суперника, мішок і перетини слів.
- [waffle.md](waffle.md), [knotwords.md](knotwords.md) — сітки слів, де рахуються обидва напрямки; тут — лише рядки.
- [pile-up-poker.md](pile-up-poker.md) — сусід по Puzzmo: ряди сітки як окремі «руки» з очками.
- [alphabear.md](alphabear.md), [wordatro.md](wordatro.md) — сума вартостей літер з множниками.
- [spelltower.md](spelltower.md) — ще одна гра Zach Gage на Puzzmo.
- **Осі варіацій:** що рахується (рядки / рядки + стовпці / + бонус-лінія) · джерело літер (фіксований лоток / мішок / рука) · бонус слова (рідкісність — Scrabble / поширеність — Bongo / тема) · обовʼязковість (усі літери / частина).

## Цікавинки для курсу
- Підрахунок ряду: суцільне слово + словник + множники клітин — 🌱.
- Бонус-змійка: друге «читання» тих самих клітин іншим шляхом — 📎 (одна плитка працює у двох словах).
- Частотний словник як джерело бонусу («поширене слово») замість вартості рідкісних літер — 📎.
- Розв'язувач «найкраща дошка»: перебір слів з лотка під 5 рядків з обмеженням на спільні літери + змійка — 🥇 (рюкзак/пакування зі словником).
- Щоденний набір з п'яти прихованих тематичних слів і підсвітка, коли гравець їх знайшов — 🌱.

## Мапа на каталог
- Є: `daily-puzzle` · `word-validation` · `drag-drop-piece` ↔ розстановка плиток · `pocket` ↔ лоток · `event-points` ↔ вартості літер · `leaderboard` · `share-result` · `save-progress` · `game-screen` · `end-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+letter-value-scoring`, `+premium-squares`, `+blank-tile` — див. [scrabble.md](scrabble.md).
  - `+row-only-words` «Слова лише в рядках, стовпці вільні» · game-logic/constraints · 🌱.
  - `+bonus-path-word` «Підсвічений шлях клітин дає друге слово-бонус» · game-logic/score · 📎 · слоти {path: cells}.
  - `+common-word-bonus` «Бонус за поширене слово (частотний список)» · game-logic/score · 📎 · слоти {freq_list}.
  - `+daily-letter-values` «Вартості літер і розкладка множників щодня інші» · levels/bank · 🌱.
  - `+hidden-theme-words` «Приховані тематичні слова підсвічуються, коли їх складено» · game-logic/score · 🌱.
  - `+partial-pool-use` «Не обовʼязково використати всі літери» · game-logic/constraints · 🌱.
  - `+daily-champion` «Звання за перший найвищий рахунок дня» · interface/results · 🌱.

## Пропозиції до словників
- `+cond:length` — довжина слова ≥ N (уже пропонована spelltower.md).
- `+cond:common_word` — слово є в частотному списку поширених.
- `+ui:row-score` — очки ряду біля рядка; `+ui:tile-value` — вартість на плитці; `+ui:bonus-path-overlay` — підсвічений шлях бонус-слова.
- `+feature:daily-champion` — звання дня; `+feature:curator-note` — записка автора дня після завершення.
- `+card:row-only-words`, `+card:bonus-path-word`, `+card:common-word-bonus`.

## Джерела
- ⭐ [Seth Godin: Bongo is here](https://seths.blog/2024/11/bongo-is-here/) — правила словами автора: лоток, 3–5 літер, 2x/3x, бланк, змійка згори вниз, бонус поширених слів.
- [Seth Godin: Bongo part 3](https://seths.blog/2024/11/game-design-and-strategy-bongo-part-3/) — щоденні вартості, бланк і бонус-слово множать варіанти, приклад rowScore/totalScore.
- [Seth Godin: Bongo 4](https://seths.blog/2024/11/bongo-4-thinking-about-power-users-skive/) — чому бонус за поширені слова.
- [Playlin: Bongo](https://playlin-site-production.pages.dev/game/bongo/) — 25 плиток + джокер, лише рядки, неонова лінія, Bongo Champion.
- [Cindy deRosier: Bongo at Puzzmo](https://www.cindyderosier.com/2025/01/bongo-at-puzzmocom.html) — 25 літер із 5 тематичних слів, фіолетові тематичні, подача 8 слів спільнотою.
- [App Store: Puzzmo](https://apps.apple.com/us/app/-/id6714482734) — застосунок платформи (2025), правил Bongo нема.

## Непевне
- (?) Розмір бонусу за поширене слово і за бонус-змійку, вартість бланка — у джерелах нема.
- (?) Довжина й форма змійки: автор — «вертикальна сіра змійка згори вниз», гайд — «неонова лінія»; скільки клітин — не сказано.
- (?) Чи рахується ряд, де літери не утворюють суцільного слова, і чи можна лишати клітини порожніми (слова 3–4 літер у ряду з 5 клітин).
- (?) Чи множник 2x/3x — лише на літеру (так у автора) чи бувають множники слова.
- (?) Скільки разів можна подавати дошку і чи зараховується найкраща спроба.
- (?) Перетягування на зайняту клітину (обмін чи відмова), повернення плитки в лоток.
- Рік: черга подає «?» — гра вийшла 2024-11-20 (пост «Bongo is here»); ⭐-лінк черги (App Store) правил не містить.
