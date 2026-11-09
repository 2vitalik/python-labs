---
title: Latent Tic-Tac-Toe
slug: latent-tic-tac-toe
aka: [LTTT, Latent TTT]
family: hidden-deduction
also: [chess-abstract]
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: none
  goal: state
year: 2009
platforms: [OpenSpiel (C++/Python)]
links:
  - {kind: other, url: "https://raw.githubusercontent.com/google-deepmind/open_spiel/master/docs/games.md", best: true, note: "OpenSpiel: «moves are not disclosed until after the opponent's next move», хід втрачено, якщо невалідний"}
  - {kind: other, url: "https://raw.githubusercontent.com/google-deepmind/open_spiel/master/open_spiel/games/latent_ttt/latent_ttt.cc", note: "реалізація: справжня дошка + два погляди, відкладене розкриття, втрачений хід"}
  - {kind: other, url: "https://mlanctot.info/files/papers/nips09mccfr.pdf", note: "Lanctot et al. 2009 (MCCFR): визначення гри і розмір дерева"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=latent+tic+tac+toe", note: "пошук"}
stage: v1
coverage: 70
mechanics: [cell-click, turn-enforcement, pass-device, ai-opponent, game-screen, end-screen, +line-win, +delayed-reveal, +lost-move-on-collision, +belief-state-ai, +post-game-reveal]
proposes: ["+effect:reveal_delayed", "+ui:pending-move", "+card:delayed-reveal", "+card:lost-move-on-collision"]
author: opus
date: 2026-11-09
---

# Latent Tic-Tac-Toe — хрестики-нулики, де хід суперника видно лише після твого наступного ходу, а хід у зайняту клітину пропадає

## Суть
Дослідницька гра з неповною інформацією (Lanctot et al., 2009, тестова гра для MCCFR). Правила хрестиків-нуликів, але хід суперника тобі **не показують**, доки ти не зробиш свій наступний. Якщо ти вибрав клітину, яку суперник уже зайняв, твій хід втрачено — зате тепер ти знаєш, що там. Мала гра з великим деревом: 70,4 млн історій, близько 16 млн інформаційних множин.

## Поле і час
- Дошка 3×3; справжня дошка + погляд кожного гравця (свої знаки й розкриті чужі).
- Покроково, по черзі; знання про хід суперника запізнюється на один твій хід.
- Найдовша історія — 18 дій (Lanctot 2009, табл. 1).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Хрестик / нулик | piece | сторона | ставиться на справжню дошку, якщо клітина вільна |
| Відкладений хід суперника | mark | клітина | невидимий тобі, доки ти не походиш |
| Розкритий знак суперника | mark | — | зʼявляється у твоєму погляді після твого ходу або після «зіткнення» |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, c)` → ЯКЩО `free(c)` на справжній дошці → ТО `place(player, mark)`, `end_turn`.
- КОЛИ `input(place, c)` → ЯКЩО `occupied(c, opponent_mark)` → ТО `custom: «хід втрачено»`, `reveal(c)` цьому гравцю, `end_turn`.
- КОЛИ `turn_end(player)` → ТО `reveal(«клітина останнього ходу суперника»)` у погляді гравця — розкриття на один хід пізніше.
- КОЛИ `input(place, c)` → ЯКЩО `legal(«c порожня у власному погляді»)` → ТО спроба дозволена; зайняте у твоєму погляді вибрати не можна.
- КОЛИ `pattern(line(3))` → ТО `win`.
- КОЛИ `custom: «справжня дошка заповнена без лінії»` → ТО `draw`.
- Перемога: три в ряд на справжній дошці · Нічия: дошку заповнено · Рахунок: виграш / нічия / програш (нульова сума).

## Керування і ввід
- Клік по клітині свого погляду; зайняті у погляді клітини недоступні.
- Для двох людей потрібна завіса `pass-device` або сервер.

## Вікна, меню, HUD
- `game-screen` (цифрова версія): твій погляд на дошку, позначка «суперник уже походив» без місця (`pending-move`), `turn-indicator`.
- `end-screen` + `post-game-reveal`: справжня дошка після кінця.

## Фічі поза полем
- В OpenSpiel параметрів нема; є undo для пошуку (відкат справжньої дошки й обох поглядів).

## Варіації й родичі
- [line-games](../chess-abstract/line-games.md) — звичайні хрестики-нулики.
- Phantom Tic-Tac-Toe (OpenSpiel) — знаки суперника приховані **завжди**, повну дошку знає лише суддя; невдала спроба в класичній версії дає ходити знову, в «abrupt» — хід втрачено; [phantom-go](phantom-go.md) — той самий прийом у го; [dark-chess-kriegspiel](dark-chess-kriegspiel.md).
- **Осі варіацій**: що приховано «весь суперник / лише останній хід»; ціна зіткнення «хід втрачено / ходиш ще раз»; затримка розкриття «0 / 1 хід / до кінця».

## Цікавинки для курсу
- Справжня дошка + два погляди з затримкою розкриття — 📎.
- Зіткнення в зайнятій клітині: втрачений хід і розкриття — 🌱.
- Порахувати розмір дерева гри й інформаційних множин — 🥈.
- AI на CFR / Monte-Carlo для гри з неповною інформацією — 👑.

## Мапа на каталог
- Є: `cell-click` · `turn-enforcement` · `pass-device` · `ai-opponent` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+line-win` — уже запропоновано в [line-games](../chess-abstract/line-games.md); `+belief-state-ai` — у Geister; `+post-game-reveal` — у Kriegspiel.
  - `+delayed-reveal` «Хід суперника видно лише після свого наступного» · game-logic/opponent · 📎.
  - `+lost-move-on-collision` «Хід у приховано зайняту клітину пропадає» · entities/legality · 🌱.

## Пропозиції до словників
- `+effect:reveal_delayed(cell, n)` — розкрити клітину через N ходів.
- `+ui:pending-move` — знак «суперник походив», без місця.

## Джерела
- ⭐ [OpenSpiel games.md](https://raw.githubusercontent.com/google-deepmind/open_spiel/master/docs/games.md) — опис гри й посилання на Lanctot et al. 2009; поруч Phantom TTT, Phantom Go, Dark Hex.
- [OpenSpiel latent_ttt.cc](https://raw.githubusercontent.com/google-deepmind/open_spiel/master/open_spiel/games/latent_ttt/latent_ttt.cc) — справжня дошка і два погляди, розкриття відкладеного ходу при власному ході, зайнята клітина = втрачений хід, легальні ходи — порожні у власному погляді.
- [OpenSpiel phantom_ttt.h](https://raw.githubusercontent.com/google-deepmind/open_spiel/master/open_spiel/games/phantom_ttt/phantom_ttt.h) — родич: суддя, версії classical / abrupt.
- [Lanctot et al. 2009, Monte Carlo Sampling for Regret Minimization](https://mlanctot.info/files/papers/nips09mccfr.pdf) — «moves are not disclosed until after the opponent's next move, and lost if invalid at the time they are revealed»; |H| = 70,4 млн, |I| ≈ 16 млн, довжина 18.

## Непевне
- (?) Статті й OpenSpiel формулюють втрату по-різному: стаття — «невалідний на момент розкриття», OpenSpiel — клітина вже зайнята на справжній дошці в момент ходу; тут описано за OpenSpiel.
- (?) Перевірку лінії й нічиї OpenSpiel бере зі звичайних хрестиків-нуликів; файл цього не показує.
