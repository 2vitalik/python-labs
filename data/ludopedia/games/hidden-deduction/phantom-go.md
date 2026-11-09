---
title: Phantom Go
slug: phantom-go
aka: [Kriegspiel Go, Phantom-Go]
family: hidden-deduction
also: [chess-abstract]
klass: figure
axes:
  field: square
  time: turn
  opponent: online
  info: hidden
  random: none
  goal: territory
year: 2005
platforms: [board (3 дошки + суддя), OpenSpiel (C++/Python), Computer Olympiad]
links:
  - {kind: other, url: "https://www.chessprogramming.org/Phantom_Go", best: true, note: "правила із суддею, оголошення взять, історія: Computer Olympiad 2007–2011, GoLois"}
  - {kind: other, url: "https://raw.githubusercontent.com/google-deepmind/open_spiel/master/docs/games.md", note: "OpenSpiel: «Go, except the opponent's stones are hidden», аналог Kriegspiel"}
  - {kind: other, url: "https://raw.githubusercontent.com/google-deepmind/open_spiel/master/open_spiel/games/phantom_go/phantom_go_board.cc", note: "реалізація: спостережний хід, розкриття каменя, синхронізація взять"}
  - {kind: other, url: "https://link.springer.com/chapter/10.1007/11922155_9", note: "Cazenave 2005, A Phantom Go Program"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Phantom+Go+hidden+stones", note: "пошук"}
stage: v1
coverage: 65
mechanics: [cell-click, turn-enforcement, pass-turn, repetition-draw, ai-opponent, online-multiplayer, game-screen, end-screen, +liberty-capture, +ko-rule, +suicide-rule, +pass-end, +area-scoring, +komi, +handicap-setup, +illegal-try-feedback, +referee-announcements, +observational-move, +public-stone-count, +belief-state-ai, +post-game-reveal]
proposes: ["+trigger:attempt", "+effect:announce", "+role:referee", "+cond:visible", "+ui:stone-counts", "+card:observational-move", "+card:public-stone-count"]
author: opus
date: 2026-11-09
---

# Phantom Go — го, де камені суперника невидимі: хід на чужий камінь відхиляють і показують його, а суддя оголошує взяття

## Суть
Го з прихованою інформацією, «Kriegspiel для го». Кожен бачить лише свої камені; повну дошку знає суддя (або сервер). Гравець вказує точку; якщо хід нелегальний, суддя просить іншу — і гравець дізнається, що там камінь. Про взяття суддя оголошує кількість знятих каменів, а власнику називає, які саме. Головне поле — тестовий полігон AI з неповною інформацією (Monte-Carlo, Computer Olympiad).

## Поле і час
- Дошка го; для Phantom Go стандарт — 9×9 (OpenSpiel: `board_size` 9, також 13 і 19).
- Три проєкції: дошка судді (повна) і дві дошки гравців (свої камені + розкриті чужі).
- Покроково; невдала спроба не передає хід. Обмеження довжини партії в OpenSpiel — `board_size² × 4` дій (спроби теж рахуються).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Свій камінь | piece | колір, група, дихання | як у го: ставиться, знімається, коли група без дихань |
| Камінь суперника | piece | прихований | видно, лише коли на нього «наткнувся» спробою ходу |
| Розкритий камінь | mark | — | позначка на своїй дошці після спостережного ходу |
| Точка ко | zone | 1 точка | хід туди відхиляють як спостережний |
| Суддя | neutral | повна дошка | перевіряє спроби, оголошує взяття |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, p)` → ЯКЩО `legal(«p вільна на справжній дошці, не ко, не самогубство»)` → ТО `place(player, stone)`, `end_turn`; інакше → ТО `reveal(p)` гравцю, `message(«Previous move was observational»)`, хід лишається в нього.
- КОЛИ `input(place, p)` → ЯКЩО `custom: «камінь займає останнє дихання групи суперника»` → ТО `custom: «зняти групу»`, `message(«N stones were captured»)` обом.
- КОЛИ `after(«взяття»)` → ТО `hide(«зняті камені»)` в обох проєкціях — власнику називають, які камені зняли (синхронізація дошок).
- КОЛИ `input(pass)` → ТО `pass_turn`, `message(«Previous move was valid and was a pass»)`.
- КОЛИ `custom: «два паси поспіль»` → ТО `game_over`, `custom: «площа за Тромпом–Тейлором + комі 7.5 білим»`.
- КОЛИ `repetition` → ТО `draw` (OpenSpiel трактує суперко як нічию).
- КОЛИ `counter(actions, >=, max_game_length)` → ТО `game_over`, підрахунок як звичайно.
- Публічно завжди: кількість каменів кожного кольору на дошці і чи був попередній хід дійсним.
- Перемога: більше очок площі (з комі) · Нічия: рівний рахунок або суперко.

## Керування і ввід
- Клік по точці = спроба ходу; кнопка «пас».
- Без судді-людини — сервер, що приховує чужі камені від клієнта.

## Вікна, меню, HUD
- `game-screen` (цифрова версія): своя дошка з розкритими чужими каменями, лічильники каменів обох сторін, рядок оголошень судді (`message-log`), `turn-indicator`.
- `end-screen`: рахунок і `post-game-reveal` — повна дошка після партії.
- `match-setup`: розмір дошки, комі, фора.

## Фічі поза полем
- Параметри OpenSpiel: `komi` (7.5), `board_size` (9), `handicap` (0; 2–9 каменів на фіксовані точки), `max_game_length`.
- Турніри програм: Computer Olympiad 2007 (Амстердам) — 2011 (Тілбург); програма GoLois (Cazenave).

## Варіації й родичі
- [go](../chess-abstract/go.md) — база; [dark-chess-kriegspiel](dark-chess-kriegspiel.md) — той самий прийом «спроба → ні» в шахах.
- OpenSpiel: Phantom Tic-Tac-Toe (приховані знаки суперника; версії classical — після невдалої спроби ходиш знову, abrupt — хід втрачено), Dark Hex (приховані камені Hex), [latent-tic-tac-toe](latent-tic-tac-toe.md) (хід показують із запізненням).
- **Осі варіацій**: що приховано «всі чужі камені / лише останній хід»; ціна спроби «безкоштовна / втрачений хід»; що оголошують «кількість / кількість + які»; ціль «територія / лінія / мат».

## Цікавинки для курсу
- Спостережний хід: відхилити спробу, розкрити камінь лише в проєкції гравця — 📎.
- Три проєкції стану (суддя + два гравці) і чесний клієнт — 🥉.
- Синхронізація після взяття: прибрати зняті камені з обох проєкцій — 📎.
- Підрахунок площі за Тромпом–Тейлором (flood fill по порожніх) — 🥉.
- AI з множиною можливих позицій (Monte-Carlo по сумісних дошках) — 👑.

## Мапа на каталог
- Є: `cell-click` · `turn-enforcement` · `pass-turn` · `repetition-draw` (суперко) · `ai-opponent` · `online-multiplayer` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+liberty-capture`, `+ko-rule`, `+suicide-rule`, `+pass-end`, `+area-scoring`, `+komi`, `+handicap-setup` — уже запропоновано в [go](../chess-abstract/go.md).
  - `+illegal-try-feedback`, `+referee-announcements`, `+post-game-reveal` — уже запропоновано в Kriegspiel; `+belief-state-ai` — у Geister.
  - `+observational-move` «Нелегальна спроба розкриває, що в точці, хід не втрачено» · entities/legality · 📎.
  - `+public-stone-count` «Публічні лічильники прихованих фігур» · interface/hud · 🌱.

## Пропозиції до словників
- `+trigger:attempt(move)` — спроба ходу, яку перевіряє суддя (вже пропонувався в Kriegspiel).
- `+effect:announce(text, to)` — оголошення судді; тут замінено наявним `message`.
- `+role:referee` — сутність, що знає повний стан.
- `+cond:visible(cell, side)` — точка видна стороні.
- `+ui:stone-counts` — лічильники каменів обох кольорів.

## Джерела
- ⭐ [Chessprogramming: Phantom Go](https://www.chessprogramming.org/Phantom_Go) — суддя з повною дошкою, «спроба → інша точка», оголошення кількості взятих і які саме; кінець після двох пасів; Computer Olympiad 2007–2011.
- [OpenSpiel games.md](https://raw.githubusercontent.com/google-deepmind/open_spiel/master/docs/games.md) — опис і посилання на Cazenave 2005; родичі Phantom TTT, Dark Hex, Latent TTT.
- [OpenSpiel phantom_go_board.cc](https://raw.githubusercontent.com/google-deepmind/open_spiel/master/open_spiel/games/phantom_go/phantom_go_board.cc) — розкриття точки при спробі, заборона самогубства, ко, оголошення «observational / valid / N stones were captured».
- [Cazenave 2005, A Phantom Go Program](https://link.springer.com/chapter/10.1007/11922155_9) — найраніше джерело (лише посилання, текст не читав).

## Непевне
- (?) Рік і автор правил: найраніше знайдене джерело — Cazenave 2005; людська гра, ймовірно, старша.
- (?) Чи людські правила теж розкривають камінь при невдалій спробі (chessprogramming цього не каже; OpenSpiel — так).
- (?) Підрахунок у людській грі — площа чи територія; комі 7.5 — значення OpenSpiel.
