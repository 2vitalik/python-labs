---
title: Tricky Tangled Train Tracks
slug: tricky-tangled-train-tracks
aka: []
family: connect-rotate
also: [thinky]
klass: avatar
axes:
  field: free
  time: turn
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2025
platforms: [web]
links:
  - {kind: itch, url: "https://managore.itch.io/tricky-tangled-train-tracks", best: true, note: "грати в браузері; у коментарях: 14 станцій, undo утриманням ↓, петля до старту"}
  - {kind: other, url: "https://confoundingcalendar.itch.io/", note: "Confounding Calendar 2025, тиждень 2: «Lay tracks to connect all the stations on the island»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tricky+Tangled+Train+Tracks", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [keyboard-controls, undo-unlimited, single-loop-check, satisfy-constraints, completion-detection, goal-counter, impassable-cells, +turtle-track, +turning-radius, +station-pass, +track-overlap-check]
proposes: ["+effect:lay_track", "+cond:no_overlap", "+card:turtle-track", "+card:turning-radius"]
author: opus
date: 2026-11-09
---

# Tricky Tangled Train Tracks — одна колія з широким радіусом повороту має пройти всі 14 станцій острова й замкнутись у петлю

## Суть
Мініатюра Daniel Linssen для адвент-календаря Confounding Calendar 2025. Гравець кладе одну колію шматок за шматком від стартової точки: прямо, дуга ліворуч або дуга праворуч. Мета — провести колію через усі 14 станцій острова й повернутись на старт, замкнувши петлю. Складність — у великому **радіусі повороту**: розвернутись тісно не можна, тож петлю доводиться планувати наперед.

## Поле і час
- Острів із водою (озера) і 14 станціями; колія складається з фіксованих шматків, тому положення й напрям голови дискретні — це «черепашача графіка», а не клітинна сітка (`field: free`) (?).
- Покроково (`turn`): один шматок за натискання; світ без вводу не змінюється.
- Межа сімʼї: ближній сітковий родич — Cosmic Express чи Railbound (колія по клітинах); тут шматок колії — дуга з власною геометрією.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Голова колії (потяг) | player | позиція, напрям (стрілка спереду) | наступний шматок кладеться від голови |
| Шматок колії | conduit | вид: прямий / дуга вліво / дуга вправо | має маску зіткнення; накладання — недійсне розміщення |
| Станція | sink | стан: не зʼєднана / зʼєднана / недійсна; знак «!» | зараховується, коли колія правильно проходить крізь неї |
| Вода (озеро) | static | — | колію сюди не покласти (?) |
| Старт | static | — | кінцева точка петлі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(up)` → ЯКЩО `custom: «прямий шматок не перекриває колію чи воду»` → ТО `place(player, straight)`, `move(head, forward)`; інакше `block`, `sound(invalid)`.
- КОЛИ `input(left|right)` → ЯКЩО `custom: «дуга не перекриває колію чи воду»` → ТО `place(player, arc)`, `face(head, left|right)` — поворот лише дугою фіксованого радіуса.
- КОЛИ `input(down)` → ТО `undo(1)`; утримання ↓ — швидкий undo підряд.
- КОЛИ `enter(track, station)` → ЯКЩО `custom: «колія проходить станцію правильно»` → ТО `set_state(station, connected)`, `counter(stations, +1)`; інакше `set_state(station, invalid)` (?).
- КОЛИ `reach(head, start)` → ЯКЩО `counter(stations, ==, 14)` → ТО `win` (петля замкнена).
- Перемога: одна замкнена петля через усі 14 станцій. · Поразки нема — лише undo. · Рахунок: зʼєднано N/14.

## Керування і ввід
- Стрілки: ↑ — прямо, ← / → — дуга вліво/вправо, ↓ — скасувати (утримання — швидко). Підтримується тач.
- Окремої кнопки рестарту автор не згадує; undo її замінює.

## Вікна, меню, HUD
- `game-screen`: острів, колія, `remaining-counter` станцій (гравці пишуть «12/14»), підказка керування (спрайт клавіш), «!» над п'ятьма першими станціями.
- Інших вікон не видно: гра — один рівень у браузерному вікні itch.io.

## Фічі поза полем
- `undo` без ліміту (утримання ↓). Збережень, рівнів і налаштувань нема (?).

## Варіації й родичі
- Родичі: Cosmic Express і Railbound (колія по клітинах з обмеженнями), Trainyard (вільне малювання колій), класичні пазли на одну петлю (Masyu, Slitherlink).
- Осі варіацій: **як задано поворот**: клітина-кут (Railbound) / дуга фіксованого радіуса (TTTT) · **чи дозволено перетин**: ні / так (?) · **станції**: усі в довільному порядку / за номерами.

## Цікавинки для курсу
- Колія як «черепашача графіка»: голова з напрямом, шматок прямо або дуга — 📎.
- Перевірка накладання шматків колії через маски зіткнення — 🥉 (геометрія дуг, не клітин).
- Замкненість петлі й лічильник зʼєднаних станцій — 🌱.
- Розвʼязувач перебором послідовностей «прямо/вліво/вправо» з відсіканням — 🥇 (гравці кажуть, що без плану це «перебір усіх поворотів»).

## Мапа на каталог
- Є: `keyboard-controls` ↔ стрілки; `undo-unlimited` ↔ ↓; `single-loop-check` ↔ замкнена петля; `satisfy-constraints` + `completion-detection`; `goal-counter` ↔ N/14; `impassable-cells` ↔ вода (?).
- **Нема** → пропозиції карток:
  - `+turtle-track` «Колія шматками від голови: прямо / дуга» · entities/move · 📎.
  - `+turning-radius` «Мінімальний радіус повороту» · entities/legality · 🥉.
  - `+station-pass` «Станція зараховується проїздом» · game-logic/win · 🌱.
  - `+track-overlap-check` «Колія не накладається на себе» · entities/legality · 🥉.

## Пропозиції до словників
- `+effect:lay_track` — покласти наступний шматок колії від голови (тут — `place` + `move`/`face`).
- `+cond:no_overlap` — новий шматок не перекриває наявні й перешкоди.
- `+card:turtle-track`, `+card:turning-radius`.

## Джерела
- ⭐ [itch.io](https://managore.itch.io/tricky-tangled-train-tracks) — гра в браузері; коментарі: «1/14 станцій», «turning circle», автор: «утримуй ↓ для швидкого undo»; підказки гравців: перемога — повернутись на старт і замкнути петлю, «!» над першими пʼятьма станціями.
- [Confounding Calendar](https://confoundingcalendar.itch.io/) — 2025, тиждень 2: «Lay tracks to connect all the stations on the island».
- Ресурси HTML5-збірки (GameMaker): шматки колії вгору/вліво/вправо з масками зіткнення, станції (valid / invalid / warning), озеро, стрілка спереду, звуки «недійсне розміщення», «зʼєднано станцію», «undo станції».
- YouTube: пошук «Tricky Tangled Train Tracks».

## Непевне
- (?) Чи може колія перетинати сама себе: маски зіткнення кажуть «ні», але гравець згадує форму «вісімки».
- (?) Що робить станцію «недійсною»: напрям проїзду, кут входу чи проїзд повз.
- (?) Що означає «!» над станціями — підказка порядку перших пʼяти чи попередження.
- (?) Чи колію можна класти на воду; скільки напрямів має голова колії.
