---
title: Gridwordy
slug: gridwordy
aka: []
family: word-number
also: [falling-match]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: score
year: 2020
platforms: [iOS, iPadOS, macOS]
links:
  - {kind: other, url: "https://apps.apple.com/mx/app/gridwordy/id1506039949", best: true, note: "App Store: шлях по 8 сусідах, літери зникають, верхні падають, згори нові; свайп ряду/стовпця зсуває літери; режими часу й розміри сітки; Game Center"}
  - {kind: official, url: "https://myappstudios.com/ios-games/gridwordy/", note: "сторінка розробника (Vaibhav Electronics / myappstudios): той самий опис, нагорода «Wordly Wise» за найдовше слово"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=gridwordy+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [word-validation, path-drawing, gravity-fall, spawn-random-cell, row-conveyor, swipe-gestures, time-out, event-points, score-records, leaderboard, field-size-picker, mode-select, theme-select, game-screen, end-screen, +path-trace-word, +word-clear-refill, +row-col-shift-letters, +longest-word-award]
proposes: ["+effect:refill_from_top", "+ui:longest-word"]
author: opus
date: 2026-11-09
---

# Gridwordy — Boggle, де складене слово зникає: літери згори падають у дірки, а ряд чи стовпець можна прокрутити свайпом

## Суть
Повна сітка перемішаних літер. Гравець веде шлях по сусідніх клітинах (горизонталь, вертикаль, діагональ) і складає слово; його літери зникають, верхні падають униз, а згори входять нові, тож сітка завжди повна. Якщо слів не видно — свайп по ряду чи стовпцю зсуває його літери і відкриває нові шляхи. Ціль — очки за час і «найдовше слово» (нагорода «Wordly Wise»). Від Boggle (`boggle.md`) відрізняє змінне поле, від SpellTower (`spelltower.md`) — нескінченне поповнення і зсув рядів.

## Поле і час
- Квадратна сітка, повністю заповнена; кілька розмірів на вибір (які — не сказано).
- Поле змінюється після кожного слова (зникнення → падіння → поповнення) і після свайпу (циклічний зсув ряду/стовпця (?)).
- Час — «кілька режимів часу» (?): імовірно відлік раунду або без таймера.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Літера | tile | символ | вибирається в шлях; зникає у слові; падає, якщо під нею порожньо |
| Нова літера | tile | випадкова (?) | входить згори в порожні клітини |
| Ряд / стовпець | zone | — | свайп зсуває всі літери лінії |
| Шлях | mark | послідовність сусідніх клітин | підсвічується, поки ведеш |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag path)` → ЯКЩО `custom: «наступна клітина — один з 8 сусідів попередньої, без повтору»` → ТО `custom: «літера додається до слова»`; інакше `block`.
- КОЛИ `input(release)` → ЯКЩО `in_dictionary(word)` → ТО `clear(path cells)`, `score(n)` (?).
- КОЛИ `input(release)` → ЯКЩО `not in_dictionary(word)` → ТО `custom: «шлях скидається»`.
- КОЛИ `after(clear)` → ТО `fall(letters above)`.
- КОЛИ `after(fall)` → ТО `spawn_at(letter, top)` — сітка знову повна.
- КОЛИ `input(swipe row|col)` → ТО `shift(row|col, dir)`.
- КОЛИ `counter(word length, >, best)` → ТО `custom: «нове найдовше слово — претендент на Wordly Wise»`.
- КОЛИ `counter(time_left, ==, 0)` (у режимі на час (?)) → ТО `window(end-screen)`.
- Перемога: нема стану перемоги; мета — рекорд очок / найдовше слово · Поразка: кінець часу (?) · Рахунок: формула не описана (?).

## Керування і ввід
- Тач: провести пальцем по сусідніх літерах, відпустити — подати слово.
- Свайп уздовж ряду або стовпця (поза шляхом) — зсунути лінію. Як гра розрізняє свайп-зсув і шлях — не описано (?).

## Вікна, меню, HUD
- `game-screen`: сітка, `word-preview` (поточне слово), `score`, `timer-countdown` (?), `longest-word`.
- `mode-select`: режим часу і розмір сітки.
- `settings-window`: колір тла.
- `leaderboard` / `achievements-window`: Game Center.
- `end-screen`: результат раунду (?).

## Фічі поза полем
- `theme-select` (колір тла), `leaderboard-online` і `achievements` через Game Center, статистика гравця (версія 10.0), оновлення словника в патчах.
- Лише англійська; безкоштовна з рекламою.

## Варіації й родичі
- Boggle (`boggle.md`) — шлях по 8 сусідах, поле статичне, таймер.
- SpellTower (`spelltower.md`), Bookworm (`bookworm.md`) — слово зникає, решта падає; Wordament (`wordament.md`), Squaredle (`squaredle.md`) — без гравітації.
- Sixteen / пʼятнашки-зсуви — зсув ряду як окремий хід (див. `shift` у словнику).
- **Осі варіацій:** поповнення (нема / згори випадково / з черги) · зсув рядів (нема / свайп) · час (раунд / без) · мета (очки / найдовше слово / очистити поле).

## Цікавинки для курсу
- Видалення шляху + гравітація по стовпцях + поповнення згори — 🌱.
- Циклічний зсув ряду/стовпця свайпом — 🌱.
- Розрізнення жестів «шлях» і «свайп-зсув» на тач-екрані — 📎.
- Генератор поповнення з частотами літер, щоб на полі завжди було хоч одне слово (перевірка солвером) — 🥈.

## Мапа на каталог
- Є: `word-validation` · `path-drawing` ↔ шлях по сусідах · `gravity-fall` · `spawn-random-cell` ↔ нові літери згори · `row-conveyor` ↔ зсув ряду · `swipe-gestures` · `time-out` · `event-points` · `score-records` · `leaderboard` · `field-size-picker` · `mode-select` · `theme-select` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+path-trace-word` — див. `boggle.md`, `nyt-connections.md`.
  - `+word-clear-refill` «Слово зникає, поле падає й поповнюється» · entities/move · 🌱.
  - `+row-col-shift-letters` «Свайп зсуває ряд/стовпець літер» · interface/input · 🌱.
  - `+longest-word-award` «Окрема нагорода за найдовше слово» · game-logic/score · 🌱.

## Пропозиції до словників
- `+effect:refill_from_top` — порожні клітини після падіння заповнюються новими згори (Gridwordy, match-3, Bookworm).
- `+ui:longest-word` — найдовше слово сесії/рекорд.

## Джерела
- ⭐ [App Store: Gridwordy](https://apps.apple.com/mx/app/gridwordy/id1506039949) — правила шляху, зникнення й падіння, поповнення, свайп ряду/стовпця, режими часу і розміри, Game Center, історія версій (© 2020, Vaibhav Electronics).
- [myappstudios: Gridwordy](https://myappstudios.com/ios-games/gridwordy/) — опис розробника, «Wordly Wise».
- YouTube: пошук «gridwordy gameplay».

## Непевне
- (?) Формула очок, мінімальна довжина слова, назви й тривалість режимів часу, розміри сітки — жодне джерело не дало.
- (?) Зсув ряду — циклічний чи з виштовхуванням літери за край; чи коштує він щось (час, очки).
- (?) Чи є кінець гри без таймера (нема слів) і чи гарантує генератор наявність слова.
- (?) Рік — 2020 з копірайту; найраніша видима версія в історії — 2023.
- Гра маленька і погано задокументована; файл короткий свідомо.
</content>
</invoke>
