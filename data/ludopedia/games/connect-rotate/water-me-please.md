---
title: Water Me Please!
slug: water-me-please
aka: [Water Me Please]
family: connect-rotate
also: [push-slide]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2016
platforms: [iOS, Android]
links:
  - {kind: other, url: "https://apps.apple.com/us/app/water-me-please/id920743929", best: true, note: "App Store: правило, 200+ пазлів, 3 зірки, підказки, історія версій"}
  - {kind: other, url: "https://play.google.com/store/apps/details?id=com.kiragames.waterme", note: "Google Play: 600+ пазлів, Relax/Challenge, Blueprint/Hammer/Frozen Clock"}
  - {kind: official, url: "https://www.kiragames.com/", note: "Kiragames — автори Unblock Me"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Water+Me+Please+kiragames+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 35
mechanics: [pipe-connectors, swipe-gestures, connectivity-check, completion-detection, sequential-levels, level-select, difficulty-levels, mode-select, tutorial-window, achievements-window, shop-window, +sliding-pipe-blocks, +flow-propagation, +hint-reveal, +helper-items, +stars-rating]
proposes: ["+effect:flow", "+feature:helper-items", "+card:sliding-pipe-blocks"]
author: opus
date: 2026-11-09
---

# Water Me Please! — посувай блоки з трубами, щоб вода з лійки дійшла до квітки

## Суть
Мобільний пазл Kiragames (автори Unblock Me): на полі блоки з шматками труб, лійка-джерело й квітка, яку треба полити. Гравець зсуває блоки вгору, вниз, ліворуч і праворуч, щоб зібрати безперервний шлях води. Це схрещення пазла-«пʼятнашок» з тісним полем і труб Pipe Mania: труби не обертаються, їх переставляють.

## Поле і час
- Квадратна сітка з блоками; вільних клітин мало, тож щоб поставити один блок, доводиться пересунути кілька інших (скарга гравця) (?) розмір поля.
- Покроково: хід — зсув блока; щойно шлях замкнувся, вода тече й рівень завершується автоматично.
- Світи й набори рівнів («Grassland», «set 2, level 17» у відгуках) (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Лійка | source | позиція, вихід | звідси тече вода |
| Квітка | sink | вхід | має отримати воду, «поки не зівʼяла» |
| Блок з трубою | conduit | форма труби (пряма, коліно, …) (?) | зсувається в 4 напрямки на вільне місце; труба рухається разом із блоком |
| Нерухомий блок / перешкода | static | — | (?) чи є такі |
| Вода | object | фронт | тече лише крізь стики, що збігаються |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(swipe, block, dir)` → ЯКЩО `free(cell_in_dir)` → ТО `move(block, dir)` (до упору чи на 1 — (?)), `counter(moves, +1)`; інакше `block`.
- КОЛИ `settled` → ЯКЩО `path_exists(can, flower)` → ТО `custom: «вода тече трубами»`, `win`.
- КОЛИ `level_end` → ТО `custom: «1–3 зірки за рівень»` (?) за кількістю ходів, `next_level`.
- КОЛИ `input(hint)` → ТО `custom: «підказка ходу»`.
- КОЛИ `input(blueprint)` → ТО `custom: «показати план шляху»` (?).
- КОЛИ `input(hammer)` → ТО `custom: «прибрати блок»` (?).
- КОЛИ `input(frozen_clock)` → ТО `timer(stop)` (?), у режимі Challenge.
- КОЛИ `counter(time_left, ==, 0)` → ЯКЩО `mode(challenge)` → ТО `lose` (?).
- Перемога: безперервний шлях від лійки до квітки. · Поразка: лише в Challenge (?). · Рахунок: 3 зірки на пазл.

## Керування і ввід
- Свайп або протягування блока пальцем у потрібний бік (iOS/Android; також Mac на M1 і visionOS).
- Кнопки помічників: підказка, Blueprint, Hammer, Frozen Clock — «обирай мудро».

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Relax · Challenge (з версії 1.2.1.0).
- `level-select`: набори й рівні зі зірками.
- `game-screen`: поле, лійка, квітка; кнопки помічників; таймер у Challenge (?).
- `end-screen`: зірки за рівень.
- `shop-window`: монети ($0.99–$9.99) і «прибрати рекламу» ($1.99).
- `tutorial-window`; `achievements-window` (Game Center); «мультяшні історії» (з 1.2.1.0).

## Фічі поза полем
- 200+ пазлів (iOS 2016) / 600+ (Google Play 2025); `stars-rating`, `levels-sequential`.
- `mode-zen` (Relax) і режим на час (Challenge); `difficulty-presets` (з 1.2.1.0).
- Нагороди за повернення в гру (з 1.2.1.0) (?) — щоденні.
- `hint` і помічники за монети; `achievements` Game Center.

## Варіації й родичі
- Родичі: Unblock Me (ті самі автори, ковзання блоків), Pipe Mania і Plumber (труби з поворотом), Roll the Ball (ковзні плитки з доріжкою).
- Осі варіацій: **як зʼєднують труби**: поворот плитки (Plumber) / зсув блоків (Water Me Please) / розстановка з черги (Pipe Mania) · **тиск часу**: нема (Relax) / таймер (Challenge).

## Цікавинки для курсу
- Ковзні блоки на тісному полі (як «пʼятнашки», але блоків багато) — 📎.
- Перевірка звʼязку джерело→приймач по стиках труб (BFS) — 📎 (картка `pipe-connectors`).
- Автозавершення рівня, щойно шлях замкнувся — 🌱.
- Помічники за валюту (план, молоток, заморожений годинник) — 🥉 (економіка + три різні дії).

## Мапа на каталог
- Є: `pipe-connectors` ↔ труби на блоках; `swipe-gestures`; `connectivity-check` ↔ лійка→квітка; `completion-detection`; `sequential-levels` + `level-select`; `difficulty-levels`; `mode-select` ↔ Relax/Challenge; `tutorial-window`, `achievements-window`, `shop-window`.
- **Нема** → пропозиції карток:
  - `+sliding-pipe-blocks` «Ковзні блоки з трубами» · entities/move · 📎.
  - `+flow-propagation` «Вода тече від джерела стиками» · entities/state · 📎 (є в сімʼї).
  - `+hint-reveal` · `+stars-rating` — уже пропоновані.
  - `+helper-items` «Помічники за валюту» · game-logic/economy · 🥉.

## Пропозиції до словників
- `+effect:flow` — вода/сигнал проходить звʼязаними трубами від джерела (тут — `custom`).
- `+feature:helper-items` — разові помічники за валюту (Blueprint, Hammer, Frozen Clock).
- `+card:sliding-pipe-blocks`.

## Джерела
- ⭐ [App Store](https://apps.apple.com/us/app/water-me-please/id920743929) — «рухай блоки ліворуч, праворуч, вгору, вниз, щоб зʼєднати потік води»; 200+ пазлів, 3 зірки, підказки, туторіали; версії 1.0.0 (8.03.2016) — 1.2.3 (4.11.2016), Relax/Challenge з 1.2.1.0.
- [Google Play](https://play.google.com/store/apps/details?id=com.kiragames.waterme) — лійка й квітка, «ковзання блоків у 4 напрямки», 600+ пазлів, Relax/Challenge, Blueprint / Hammer / Frozen Clock; відгуки про тісне поле й автозавершення.
- [Kiragames](https://www.kiragames.com/) — студія Unblock Me.
- YouTube: пошук «Water Me Please kiragames gameplay».

## Непевне
- (?) Блок сунеться на одну клітину чи до упору; розмір поля; чи є нерухомі блоки й порожні клітини.
- (?) Що саме роблять Blueprint, Hammer і Frozen Clock — назви з опису, дії — припущення.
- (?) За що дають зірки (кількість ходів?) і чи є таймер у Challenge.
- Рік у черзі «≤2016» — підтверджено: iOS 1.0.0 вийшла 8.03.2016.
