---
title: Leap Year
slug: leap-year
aka: [Leap Year March]
family: thinky
also: [grid-platformer]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 2024
platforms: [PC, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Leap_Year_(video_game)", best: true, note: "суть: приховані рухи від старту, підказки в фоні, смерть від падіння з висоти стрибка; релізи, DLC"}
  - {kind: steam, url: "https://store.steampowered.com/app/2951770/Leap_Year/", note: "опис, 40+ кімнат, ~2 год, 12 досягнень"}
  - {kind: steam, url: "https://store.steampowered.com/app/3458170/Leap_Year_March/", note: "DLC «March»: 50+ кімнат, «a new way to die»"}
  - {kind: itch, url: "https://managore.itch.io/leap-year", note: "itch.io; замовлено Sokpop, патчі 1.0.2–1.0.7"}
  - {kind: other, url: "https://buried-treasure.org/2024/06/leap-year/", note: "рецензія: стрибок на 2 зрости, безпечне падіння на 1, сітка на тригері"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Leap+Year+Daniel+Linssen+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-by-input, gravity-fall, height-levels, environment-death, player-death, respawn, collect-all, item-pickup, keyboard-controls, +fall-height-death, +hidden-moveset, +knowledge-gate, +world-clues]
proposes: ["+trigger:landed", "+cond:fall_height", "+feature:grid-overlay", "+feature:knowledge-gate", "+card:fall-height-death", "+card:hidden-moveset", "+axis:progression"]
author: opus
date: 2026-11-09
---

# Leap Year — незграбний платформер, де стрибнути на місці смертельно, а всі рухи в тебе вже є, треба лише здогадатися

## Суть
Маленький герой шукає загублені дні лютого — сторінки календаря, розкидані по зшитому світу з 40+ кімнат. Він стрибає вдвічі вище свого зросту, але переживає падіння лише з власного зросту: звичайний стрибок на рівній підлозі вбиває. Нових умінь гра не дає: усі прийоми є від першої секунди, а відкриваються через спроби, смерті й підказки, вирізьблені у фоні. Це «метроїдбрейнія»: ключ до нових зон — знання, а не предмет.

## Поле і час
- Бічний вигляд, світ із блоків-клітин; утримання тригера накладає на екран сітку, щоб міряти висоти.
- Реал-тайм платформер з гравітацією; світ безперервний, кімнати сусідять.
- Висота — головна величина: різниця рівнів між точкою відриву / піку і точкою приземлення вирішує, живий герой чи ні.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | стрибок ≈ 2 блоки вгору, безпечне падіння ≈ 1 блок | ходить, стрибає; гине, якщо падав вище за безпечну висоту |
| Блок-земля | terrain | висота в клітинах | опора; сходинки скорочують падіння |
| Стеля | static | — | обриває стрибок, і пік стає нижчим — падіння безпечне |
| Сторінка календаря | pickup | день лютого | мета збирання; відкриває прогрес |
| Підказка у фоні | mark | малюнок / різьба | натяк на прихований прийом, сама нічого не робить |
| Друзі, що танцюють | neutral | — | NPC у світі (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ТО `move(hero, dir)`.
- КОЛИ `input(jump)` → ЯКЩО `supported(hero)` → ТО `custom: «стрибок до ~2 блоків угору»`.
- КОЛИ `custom: «під героєм порожньо»` → ТО `fall(hero)`.
- КОЛИ `custom: «герой приземлився»` → ЯКЩО `custom: «падав вище за безпечну висоту (~1 блок)»` → ТО `lose`, `respawn(hero, room_entry)` (?).
- КОЛИ `contact(hero, ceiling)` під час стрибка → ТО `custom: «пік стрибка обрізано — падіння коротшає»`.
- КОЛИ `custom: «приземлення на вищу сходинку»` → ТО `custom: «падіння рахується від піку до цієї сходинки»` — так виживають після стрибка.
- КОЛИ `contact(hero, page)` → ТО `pickup`, `counter(pages, +1)`.
- КОЛИ `counter(pages, =, all)` → ТО `win` (?).
- КОЛИ `custom: «гравець виконав прихований прийом»` → ТО `custom: «нова властивість висоти/руху, що відкриває шлях»` — суть прийомів у джерелах навмисно не розкрито.
- Перемога: зібрати всі сторінки місяця · Поразка: смерть від падіння (миттєвий повтор) · Рахунку нема.

## Керування і ввід
- Ходьба вліво/вправо, стрибок; тригер (на геймпаді) — накладка сітки.
- Інших дій на старті гравцеві не показують: решта — приховані комбінації того самого вводу (?).

## Вікна, меню, HUD
- `main-menu` (?): почати / продовжити.
- `game-screen`: кімната без HUD; накладка `grid-lines` на тригері.
- `custom-window` (календар, ?): зібрані дні місяця.
- Переходи: кімната → сусідня кімната виходом за край екрана.

## Фічі поза полем
- `grid-toggle` — сітка на утриманні тригера як інструмент вимірювання.
- `achievements`: 12 у Steam.
- DLC «Leap Year: March» (28.02.2025): новий місяць, 50+ кімнат, «новий спосіб померти».
- Прогрес — лише знання гравця: `knowledge-gate` замість `level-unlock`.

## Варіації й родичі
- Метроїдбрейнії: Void Stranger, Understand, Taiji (у сім'ї), Animal Well, Tunic, Outer Wilds; преса порівнює з Animal Well, Blue Prince, Lorelei and the Laser Eyes.
- Клітинні платформери: Lode Runner, Catrap, Toki Tori — `grid-platformer`.
- Осі варіацій: **падіння** — безпечне / шкода за висотою / смерть понад поріг; **уміння** — даються предметами (метроїдванія) / є від старту, приховані (метроїдбрейнія); **підказки** — текст / знаки у фоні / нема.

## Цікавинки для курсу
- Смерть від висоти падіння: пам'ятати висоту піку, рахувати різницю при приземленні — 🌱.
- Стеля й сходинки як інструменти скорочення падіння — 📎.
- Накладка сітки на утриманні кнопки — 🌱.
- Прихований прийом, що є з першого кадру й не оголошується, — 📎 у коді, 🥇 у дизайні.
- Зшитий світ кімнат з переходом за край екрана — 🥉.

## Мапа на каталог
- Є: `move-by-input` · `gravity-fall` · `height-levels` · `environment-death` · `player-death` · `respawn` · `collect-all` · `item-pickup` · `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+fall-height-death` «Смерть від висоти падіння» · entities/death · 🌱 · слоти {safe: n}.
  - `+hidden-moveset` «Приховані прийоми від старту» · entities/move · 📎.
  - `+knowledge-gate` «Прогрес відкриває знання, не предмет» · levels/progression · 🥉.
  - `+world-clues` «Підказки, намальовані у світі» · interface/graphics · 🌱.

## Пропозиції до словників
- `+trigger:landed` — сутність приземлилась після падіння; `+cond:fall_height` — висота падіння порівняно з N.
- `+feature:grid-overlay` — сітка поверх світу на утриманні кнопки (не перемикач `grid-toggle`); `+feature:knowledge-gate` — прогрес через знання гравця.
- `+card:fall-height-death`, `+card:hidden-moveset` — див. вище.
- `+axis:progression` = `knowledge` (нова вісь: чим відкривається світ — `items` / `knowledge` / `levels`).
- ⏳-слова, вжиті тут: `input`, `supported`, `move`, `fall`, `counter`, `respawn`, `terrain`, `neutral`, `mark`.

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Leap_Year_(video_game)) — приховані рухи від старту, підказки у фоні, падіння з висоти стрибка, GameMaker, Sokpop, релізи й DLC.
- [Steam](https://store.steampowered.com/app/2951770/Leap_Year/) і [DLC March](https://store.steampowered.com/app/3458170/Leap_Year_March/) — обсяг, досягнення, «a new way to die».
- [itch.io](https://managore.itch.io/leap-year) — опис, патчі.
- [Buried Treasure](https://buried-treasure.org/2024/06/leap-year/) — стрибок на 2 зрости / падіння на 1, сітка на тригері, жодних нових умінь.

## Непевне
- (?) Числа «стрибок ≈ 2, безпечно ≈ 1 блок» — із рецензій, словами «приблизно».
- (?) Суть прихованих прийомів — джерела не спойлять; правило про них — заглушка.
- (?) Що стається після смерті (повтор з входу в кімнату?) і чи є чекпойнти.
- (?) Дата: Steam 13.06.2024, Wikipedia 14.06.2024; Switch — 05.02.2026; DLC — 28.02.2025 (в одному джерелі — разом зі Switch).
- (?) Вікно календаря і головне меню — не бачив.
- Клас поля `square` — світ з блоків, але рух героя не клітинний; ближче до `grid-platformer`, у `thinky` — через ядро «відкрий правило».
