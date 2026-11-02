---
title: Color Lines / Lines 98 (Лінії)
slug: lines-98
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: both
  goal: score
year: 1992
platforms: [MS-DOS, Windows 3.x, Windows 95/98, Mac, mobile, web, Linux (Five or More)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Color_Lines", best: true, note: "правила повністю: 9×9, 5 на старті, 3 нові, превʼю, 5+ у лінію, бонусний хід"}
  - {kind: wiki, url: "https://ru.wikipedia.org/wiki/Color_Lines", note: "деталі: шлях без діагоналей, лінія від нових куль без бонусного ходу, історія версій"}
  - {kind: wiki, url: "https://vi.wikipedia.org/wiki/Line_98", note: "Line 98 — в'єтнамська назва-ностальгія за Windows-версією"}
  - {kind: official, url: "https://help.gnome.org/users/five-or-more/stable/", note: "GNOME Five or More — відкритий клон, довідка"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=lines+98+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 80
mechanics: [cell-click, hover-highlight, chase-bfs, reachability-check, spawn-random-cell, no-moves-left, event-points, score-records, leaderboard, movement-animation, game-screen, end-screen, +path-move, +line-match-clear, +spawn-preview, +extra-move-on-clear]
proposes: ["+trigger:spawned", "+cond:path_exists", "+effect:path_move", "+effect:extra_move", "+ui:next-spawn-preview", "+ui:path-preview"]
author: opus
date: 2026-11-02
---

# Color Lines (Lines 98) — пересувай кулі вільним шляхом, щоб скласти 5 в ряд, поки поле не заповнилось

## Суть
На полі 9×9 лежать кольорові кулі; за хід гравець переносить одну кулю в будь-яку вільну клітину, до якої є шлях із вільних клітин (без діагоналей). Лінія з 5+ куль одного кольору (горизонталь, вертикаль, діагональ) зникає і дає ще один хід; якщо лінії нема — компʼютер ставить 3 нові кулі, кольори яких показано заздалегідь. Гра без гравітації й без таймера: «падіння» тут — постійний приплив нових куль, а суть — пошук шляху й планування ліній. Поразка — заповнене поле.

## Поле і час
- Квадратне поле 9×9, 7 кольорів; на старті 5 випадкових куль.
- Покрокова: хід = одне перенесення; між ходами — спавн 3 куль (якщо не було лінії).
- Шари: кулі на клітинах + превʼю наступних 3 кольорів (у HUD або, у частині версій, маленькими кулями прямо на клітинах, де вони виростуть (?)).
- Сусідство руху — 4 (шлях); сусідство лінії — 8 напрямків (4 осі).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Куля | tile | колір (7) | переноситься гравцем вільним шляхом; зникає в лінії 5+ свого кольору |
| Вибрана куля | tile (стан) | — | «підстрибує» (анімація), чекає клітину-ціль |
| Наступні кулі | spawner | 3 кольори | після ходу без лінії зʼявляються у випадкових вільних клітинах |
| Порожня клітина | — | — | ціль ходу, частина шляху |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click ball)` → ТО `set_state(ball, selected)` (повторний клік по іншій кулі — перевибір).
- КОЛИ `input(click empty cell)` → ЯКЩО `state(ball, selected) and custom: «path_exists — BFS по вільних клітинах, 4 напрямки»` → ТО `custom: «path_move — куля проходить шляхом клітина за клітиною»`; інакше `block` (нема шляху, хід не витрачено).
- КОЛИ `after(path_move)` → ЯКЩО `pattern(line(5+, same_color))` у будь-якому з 4 напрямків через перенесену кулю → ТО `clear(line)`, `score(f(n))`, `custom: «extra_move — нових куль цього ходу нема»`.
- КОЛИ `after(path_move)` → ЯКЩО `not pattern(line(5+))` → ТО `spawn_at(next_3, random_free_cells)`, `custom: «згенерувати нові 3 кольори превʼю»`.
- КОЛИ `spawned(ball)` → ЯКЩО `pattern(line(5+))` → ТО `clear(line)`, `score(f(n))`, але без додаткового ходу.
- Кілька ліній через одну кулю (хрест) зникають разом; довша лінія дає непропорційно більше очок.
- КОЛИ `custom: «after spawn»` → ЯКЩО `count(free_cells, ==, 0)` → ТО `game_over`; рахунок порівнюється з рекордом.
- Перемоги нема — рахунок до заповнення поля.

## Керування і ввід
- Лише миша: клік по кулі — вибір, клік по порожній клітині — хід. Кліку по клітині без шляху — нічого не відбувається.
- Нема undo в оригіналі; у частині клонів є undo на 1 хід і підсвітка шляху (?).

## Вікна, меню, HUD
- `game-screen`: поле 9×9; угорі `score`, `hi-score` (рекордсмен), превʼю 3 наступних кольорів (`custom: «next-spawn-preview»`), `timer-elapsed` у Windows-версіях (?).
- DOS Color Lines: фігури «короля» (рекорд) і «претендента» (поточний гравець), що росте з очками (?).
- `leaderboard` — таблиця рекордів з іменами після кінця гри; `end-screen` — «Game Over» + введення імені.
- Меню (Windows): Game (New, Hi-scores, Exit) · Options (показ наступних куль увімк/вимк, звук) (?).
- Переходи: game-screen → (поле повне) end-screen → leaderboard → нова гра.

## Фічі поза полем
- `leaderboard-local`; `custom: «toggle preview»` — сховати наступні кольори заради більших очок (у деяких версіях) (?).
- Windows 95 (1995): 256 кольорів, нові елементи, рівні складності (`difficulty-presets`).
- GNOME Five or More: розміри поля (`custom-difficulty`), фігури замість куль (`theme-select`), 3 або 7 стартових обʼєктів залежно від розміру.

## Варіації й родичі
- Color Lines (1992, Gamos, Олег Дьомін; художники Г. Денисов, І. Івкін) → Windows 95-порт (1995) → «Lines 98» — так її знають за Windows-збірками (особливо у Вʼєтнамі). Namco на її основі — Golly! Ghosts! Goal!; клони: Five or More (GNOME/KDE), Rainbow Lines, Park-o-Nora, Funny Balls (Cybiko).
- Родичі: Bejeweled (теж прибирання ліній, але обмін і гравітація), Tetris (тиск заповнення), гомоку (5 в ряд, 4 осі).
- **Осі варіацій**: поле (9×9 / інші розміри / гекс) · довжина лінії (5 / 4 / квадрат 2×2 / блок) · нових за хід (3 / залежить від рівня) · рух (шлях BFS / телепорт куди завгодно / лише сусідня) · превʼю (видно / приховано за бонус).

## Цікавинки для курсу
- Перевірка шляху BFS по вільних клітинах + покрокова анімація кулі шляхом — 🥉 (шлях, а не телепорт).
- Детектор ліній 5+ у 4 напрямках через одну кулю, з обʼєднанням хрестів — 📎.
- Спавн N куль у випадкові вільні клітини з превʼю кольорів наперед — 🌱.
- Правило «лінія → зайвий хід без спавну» vs «лінія від спавну → без бонусу» — 🌱.
- Простий AI-підказчик (жадібно оцінити ходи за довжиною лінії) — 🥉.

## Мапа на каталог
- Є: `cell-click` · `hover-highlight` · `chase-bfs` (той самий BFS, але для ходу кулі, не ворога) · `reachability-check` · `spawn-random-cell` · `no-moves-left` (поле повне) · `event-points` · `score-records` + `leaderboard` · `movement-animation` (куля котиться шляхом) · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+path-move` «Хід вільним шляхом» · entities/move · 🥉 · слот {adjacency: 4|8} — курсорний аналог `chase-bfs`.
  - `+line-match-clear` «Зникнення лінії з N однакових» · entities/legality · 📎 · слоти {n: 5, dirs: 4} (спільна з Dr. Mario).
  - `+spawn-preview` «Превʼю наступного спавну» · interface/hud · 🌱 · слот {count: 3, on_board: yes|no}.
  - `+extra-move-on-clear` «Бонусний хід за збіг» · game-logic/opponent · 🌱.

## Пропозиції до словників
- `+trigger:spawned` — ⏳ підтверджую (лінія від нових куль).
- `+cond:path_exists` — є шлях з вільних клітин між A і B (Lines, клік-рух Chip's Challenge).
- `+effect:path_move` — рух шляхом клітина за клітиною (відмінний від `move` і `teleport`); `+effect:extra_move` — ⏳ підтверджую.
- `+ui:next-spawn-preview` — кольори/місця наступного спавну (на відміну від `next-piece-preview` — не фігура гравця); `+ui:path-preview` — ⏳ підтверджую.

## Джерела
- ⭐ [Wikipedia: Color Lines](https://en.wikipedia.org/wiki/Color_Lines) — 9×9, 5 стартових, 3 нові з 7 кольорів, превʼю, 5+ у 4 напрямках, бонусний хід, кінець при заповненні.
- [Вікіпедія (ru): Color Lines](https://ru.wikipedia.org/wiki/Color_Lines) — шлях без діагоналей, лінія від нових куль без бонусного ходу, версії 1992/1995, Namco.
- [Wikipedia (vi): Line 98](https://vi.wikipedia.org/wiki/Line_98) — назва «Line 98», автори, роки.
- [GNOME Five or More](https://help.gnome.org/users/five-or-more/stable/) — відкритий клон, правила і зміна розміру поля.
- YouTube: пошук «lines 98 gameplay».

## Непевне
- (?) Формула очок (часто зустрічається 2·n або 10 + бонус за кулю понад 5) — у джерелах лише «довші лінії — значно більше».
- (?) Превʼю маленькими кулями на клітинах у Lines 98, таймер у Windows-версії, опція ховати превʼю — з памʼяті про клони.
- (?) «Король/претендент» у DOS-версії — з памʼяті.
- (?) Хто саме зробив збірку «Lines 98» — у джерелах лише як народна назва Windows-версії.
