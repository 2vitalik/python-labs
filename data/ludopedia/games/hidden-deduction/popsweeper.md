---
title: Popsweeper
slug: popsweeper
aka: []
family: hidden-deduction
also: []
klass: cursor
axes:
  field: graph
  time: realtime
  opponent: none
  info: hidden
  random: setup
  goal: state
year: 2026
platforms: [web (itch.io, HTML5), Android (Google Play)]
links:
  - {kind: itch, url: "https://mightysebas.itch.io/popsweeper", best: true, note: "грати в браузері; «How to play», 8 зон, сили, Ice Field; опубліковано 06.11.2026"}
  - {kind: official, url: "https://mightysebas.com/popsweeper", note: "сторінка автора: що роблять сили Wind / Shake / Rift / Lantern; походження з Global Game Jam 2025"}
  - {kind: other, url: "https://play.google.com/store/apps/details?id=com.mightysebas.popsweeper", note: "Google Play: ті самі рівні, гра офлайн"}
  - {kind: itch, url: "https://relibrana.itch.io/lullapop", note: "Lullapop (GGJ 2025, серед авторів MightySebas): бульбашковий сапер без фізики, ймовірний предок"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Popsweeper+bubble+minesweeper+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [cell-click, neighbor-count-clue, mines-after-first-click, gravity-fall, completion-detection, no-guess-generation, tutorial-window, save-progress, language-picker, game-screen, end-screen, +contact-graph-neighbors, +physics-reshuffle, +limited-powers, +no-powers-challenge, +zone-mechanic-per-world, +star-rating, +daily-gift, +missions]
proposes: ["+cond:touching", "+effect:impulse", "+feature:no-powers-level", "+feature:daily-gift", "+feature:missions", "+card:contact-graph-neighbors", "+card:physics-reshuffle", "+card:limited-powers", "+card:no-powers-challenge", "+card:zone-mechanic-per-world"]
author: opus
date: 2026-11-09
---

# Popsweeper — сапер із бульбашок у банці: сусіди — ті, хто торкається, а фізика після кожного попу перетасовує сусідство

## Суть
Поле — купа бульбашок у скляній банці, а не сітка. Лопнута бульбашка показує, скільки бомб серед бульбашок, **яких вона торкається**. Бульбашки — фізичні тіла: купа осідає під час гри, і хто кого торкається, змінюється. Тому дедукція йде по графу дотиків, який перебудовується після ходів. Межова гра сімʼї без сітки; сітковий шар — режим Ice Field (класичний сапер на кубиках льоду).

## Поле і час
- Банка з бульбашками різного розміру; суміжність = граф фізичних контактів (`field: graph`), позиції вільні.
- Фізика працює безперервно: купа осідає (`gravity-fall`), сили й особливі бульбашки зсувають її. Таймера й тиску часу джерела не згадують.
- Хід = поп або прапорець; після нього купа осідає, і граф дотиків рахується заново.
- **Ice Field**: третій світ без фізики й без сил — 30 полів із кубиків льоду на сітці, жодне не потребує вгадування.
- Портретна й альбомна орієнтація.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Бульбашка | tile | розмір, тип, прихована бомба/ні | фізичне тіло; поп відкриває число дотичних бомб |
| Бомба | hazard | прихована в бульбашці | позначається прапорцем; поп бомби — ймовірно поразка (?) |
| Лопнута бульбашка | mark | число | кількість бомб серед дотичних бульбашок |
| Прапорець | mark | — | «тут бомба»; ставиться утриманням або ПКМ |
| Банка | static | форма | стінки, в яких осідає купа |
| Особливі бульбашки зон | tile | вітер, лід, магніти, чорнило, слиз, поплавці, гігантські | кожна зона додає одну; що саме роблять, джерела не описують (?) |
| Pip / Puck | neutral | — | гід: короткі уроки про кожну нову бульбашку; Puck звільняється після 10-го поля Ice Field |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(pop, b)` → ЯКЩО `first_time` → ТО `custom: «у b бомби бути не може — перший поп завжди безпечний»`.
- КОЛИ `input(pop, b)` → ЯКЩО `not state(b, bomb)` → ТО `set_state(b, popped)`, `set_value(b, «кількість бомб серед бульбашок, яких b торкається»)`.
- КОЛИ `settled` → ТО `custom: «перерахувати дотики; числа на полі відповідають новому графу»` (?).
- КОЛИ `input(hold | right_click, b)` → ТО `mark(b, flag)`.
- КОЛИ `input(pop, b)` → ЯКЩО `state(b, bomb)` → ТО `lose` (?) (у Lullapop поп міни закінчує гру).
- КОЛИ `all_gone(safe_bubble)` → ЯКЩО `custom: «кожна бомба під прапорцем»` → ТО `win`, `window(end-screen)` з 1–3 зірками.
- КОЛИ `input(power, wind, b)` → ТО `custom: «вітер підкидає купу вгору від бульбашки b»`.
- КОЛИ `input(power, shake)` → ТО `custom: «струс усієї банки»`.
- КОЛИ `input(power, rift)` → ТО `teleport(bubbles, «згори банки»)` — бульбашки падають назад зверху.
- КОЛИ `input(power, lantern)` → ТО `reveal(«одна бомба»)`.
- КОЛИ `level_start` → ЯКЩО `mode(no_powers)` → ТО `custom: «сили недоступні»`.
- Ice Field: КОЛИ `input(pop, c)` → ТО як у класичному сапері ([minesweeper](minesweeper.md)), без фізики.
- Перемога: прапорці на всіх бомбах і лопнуті всі інші бульбашки · Поразка: поп бомби (?) · Рахунок: зірки за рівень, критерії не описані (?).

## Керування і ввід
- Тап / клік — лопнути бульбашку; утримання / ПКМ — прапорець.
- Сили — окремими кнопками (`ability-buttons`) (?).
- Тач і миша, обидві орієнтації екрана.

## Вікна, меню, HUD
- `game-screen`: банка з купою, прапорці, кнопки сил (?).
- `end-screen`: «банку очищено» з трьома зірками (скриншот).
- `tutorial-window`: уроки Pip перед першим рівнем із новою бульбашкою.
- Вибір зон і рівнів (8 зон по рівнях, Ice Field, нескінченні банки) — окремий екран (?).
- Магазин або вибір косметики (бульбашки, банка, вбрання гіда, ефект попу) (?).

## Фічі поза полем
- 120 рівнів у 8 зонах; кожна зона додає новий тип бульбашки.
- Режими: кампанія, Ice Field (30 полів), endless jars.
- Рівні «без сил» — виклик (`no-powers-level`).
- `unlockables` — косметика; щоденний подарунок, місії, сезонні події (перша — Pumpkin Hollow).
- Прогрес у браузері або на телефоні, офлайн; 10 мов.

## Варіації й родичі
- [minesweeper](minesweeper.md) — сітка 8-сусідства; [globesweeper](globesweeper.md) і [non-euclidean-minesweeper](non-euclidean-minesweeper.md) — нестандартна, але **незмінна** суміжність.
- Lullapop (GGJ 2025, та сама команда) — бульбашкова тема без фізики.
- **Осі варіацій**: суміжність «сітка / граф / граф дотиків, що змінюється»; що рухає поле «нічого / гравітація / сили гравця»; сили «нема / обмежені / заборонені в рівні».

## Цікавинки для курсу
- Граф дотиків із фізики: пара кіл торкається, якщо відстань ≤ r1 + r2 + ε — 📎.
- Перерахунок чисел після осідання і питання «чи лишилась дедукція чесною» — 🥈.
- Простий двіжок осідання кіл у банці (гравітація + розштовхування) — 🥉.
- Сили як обмежені дії: Lantern = `reveal` однієї бомби, Rift = переставити згори — 🌱.
- Генерація рівня без вгадування на змінному графі — 👑 (дослідницьке: граф після ходу наперед невідомий).

## Мапа на каталог
- Є: `cell-click` · `neighbor-count-clue` (сусіди = дотики) · `mines-after-first-click` · `gravity-fall` · `completion-detection` · `no-guess-generation` (Ice Field) · `tutorial-window` · `save-progress` · `language-picker` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+contact-graph-neighbors` «Сусіди = тіла, що торкаються» · game-logic/constraints · 📎.
  - `+physics-reshuffle` «Поле осідає й міняє суміжність після ходу» · entities/move · 🥈.
  - `+limited-powers` «Обмежені сили-підказки на рівень» · game-logic/difficulty · 🌱.
  - `+no-powers-challenge` «Рівень із забороною підказок» · game-logic/difficulty · 🌱.
  - `+zone-mechanic-per-world` «Кожен світ вводить один новий тип сутності» · levels/progression · 🌱.

## Пропозиції до словників
- `+cond:touching(a, b)` — тіла торкаються (суміжність без сітки).
- `+effect:impulse(area, dir)` — фізичний поштовх групи тіл (вітер, струс).
- `+feature:no-powers-level` · `+feature:daily-gift` · `+feature:missions`.
- Вжито наявні: `settled`, `set_value`, `teleport`, `ability-buttons`, `unlockables`.

## Джерела
- ⭐ [itch.io: Popsweeper](https://mightysebas.itch.io/popsweeper) — опис і «How to play»: дотики, перший поп безпечний, прапорці, 8 зон, Ice Field, сили, косметика; дата публікації.
- [mightysebas.com/popsweeper](https://mightysebas.com/popsweeper) — що роблять Wind, Shake, Rift, Lantern; GGJ 2025; Android і браузер.
- [Google Play](https://play.google.com/store/apps/details?id=com.mightysebas.popsweeper) — той самий опис, офлайн.
- [itch.io: Lullapop](https://relibrana.itch.io/lullapop) — GGJ 2025, команда з MightySebas: поп міни будить кошеня й закінчує гру; ПКМ двічі — «?».

## Непевне
- (?) Що стається при попі бомби в Popsweeper — опис мовчить; поразка взята з Lullapop.
- (?) Чи лопнута бульбашка зникає з купи (тоді купа осідає) чи лишається з числом; чи числа оновлюються після осідання.
- (?) Що роблять бульбашки зон (вітер, лід, магніти, чорнило, слиз, поплавці, гігантські) — названі, не описані.
- (?) Критерії зірок, кількість сил на рівень, правила endless jars.
- (?) Чи Lullapop — саме та джем-гра, з якої «перебудовано» Popsweeper: автор збігається, назва не підтверджена.
