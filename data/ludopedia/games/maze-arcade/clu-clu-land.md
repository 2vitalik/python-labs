---
title: Clu Clu Land
slug: clu-clu-land
aka: [クルクルランド, Kuru Kuru Land, VS. Clu Clu Land, Welcome to New Clu Clu Land, Clu Clu Land D]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: hidden
  random: none
  goal: collect
year: 1984
platforms: [Famicom/NES, arcade (Nintendo VS. System), Famicom Disk System, e-Reader, GBA, Switch (NSO)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Clu_Clu_Land", best: true, note: "Turning Posts, злитки, що перевертаються, Unira, Black Hole, версії VS і Disk"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/クルクルランド", note: "найдетальніше: Rubber Trap, порядок кольорів стадій, тор на Purple/Yellow, бонус за 300, відмінності версій"}
  - {kind: official, url: "https://www.nintendo.com/jp/famicom/software/hvc-cl/index.html", note: "Nintendo (Famicom 40th): керування, правила, фігури злитків за кольором стадії"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Clu+Clu+Land+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-auto, wrap-edges, collect-all, touch-death, environment-death, player-death, time-out, time-bonus, event-points, projectile-shot, shoot-forward, temporary-modes, spawn-points, sequential-levels, difficulty-levels, game-screen, status-panel, remaining-counter, +grid-line-field, +post-swing-turn, +hidden-collectibles-reveal, +parity-reveal, +stun-push-kill, +rubber-trap, +shared-field-coop, +bonus-stage]
proposes: ["+effect:pivot(a, post)", "+effect:flip(a)", "+window:bonus-round", "+card:post-swing-turn", "+card:hidden-collectibles-reveal", "+card:parity-reveal", "+card:stun-push-kill", "+card:rubber-trap"]
author: opus
date: 2026-11-09
---

# Clu Clu Land — повертаєш лише хапаючись за стовпи: пропливи всі сховані злитки, оглушених їжаків дотискай до стіни

## Суть
Риба-куля Глуппі (Bubbles, Gloopy) безупинно пливе вперед по сітці стовпів і може змінити напрям лише двома способами: вхопитися рукою за стовп (Turning Post) і крутнутися навколо нього або відскочити від стіни. Під деякими відрізками між стовпами сховані золоті злитки: вони проявляються, коли Глуппі пропливає між стовпами в цьому місці; відкрити всі — пройти стадію. Злитки складаються в картинку, а колір рамки стадії підказує, яку саме. Морські їжаки Unira вбивають дотиком; їх оглушують хвилею і дотискають до зовнішньої стіни.

## Поле і час
- Поле — решітка стовпів; рух іде по відрізках між ними, злитки й пастки лежать на відрізках (поле-граф ліній, як в Amidar). Рамка стадії — стіна, від якої Глуппі відскакує.
- Стадії за кольором рамки в циклі: Pink (лише перша стадія) → Green → Sky → Purple → Yellow → знову Green. Sky — вузька складна стадія з чорною дірою в центрі; Purple — найбільша, ліво-право загорнуті (тор), 4 чорні діри; Yellow — теж тор, 4 центральні діри, найменше злитків.
- Real-time з таймером стадії; залишок часу і кількість злитків показано вгорі.
- Інформація прихована: де злитки, видно лише після проходу; підказка — колір рамки (набір фігур на колір).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Глуппі (1P червона, 2P зелена) | player | життя; стан «тримає стовп» | пливе вперед безупинно; хапає стовп і обертається; стріляє хвилею |
| Стовп (Turning Post) | static | вузол решітки | за нього можна вхопитися; поруч із Rubber Trap — непридатний |
| Схований злиток | pickup | місце на відрізку | проявляється, коли Глуппі пропливає між стовпами в цьому місці |
| Відкритий злиток | mark | лицем / тьмяним боком | на пізніх стадіях перевертається при кожному повторному проході |
| Rubber Trap | hazard | місце на відрізку | проявляється замість злитка, відкидає Глуппі назад; відрізок стає непрохідним |
| Unira | enemy | стан звичайний / оглушений | кидається на Глуппі, коли бачить; дотик — смерть |
| Оглушений Unira | object | жовтий, стиснутий, тимчасово | його можна виштовхати до зовнішньої стіни — тоді гине |
| Boss Unira | boss | лише VS-версія | новий ворог VS Clu Clu Land |
| Black Hole | hazard | 0–4 на стадії | падіння — смерть; звідси виходять Unira; над нею безпечно, тримаючись за стовп |
| Хвиля (електрична / звукова) | projectile | — | летить уперед, оглушує Unira |
| Зовнішня стіна | static | колір = підказка картинки | Глуппі відскакує; оглушений Unira об неї розбивається |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `not state(gloopy, gripping)` → ТО `move(gloopy, facing)`.
- КОЛИ `blocked(gloopy)` → ТО `bounce(gloopy)` (відскок від стіни — другий спосіб розвернутися).
- КОЛИ `input(dir)` → ЯКЩО `custom: «у напрямку dir поруч робочий стовп»` → ТО `set_state(gloopy, gripping)`, `custom: «обертатися навколо стовпа, доки кнопку тримають»`.
- КОЛИ `custom: «кнопку напрямку відпущено»` → ЯКЩО `state(gloopy, gripping)` → ТО `clear_state(gloopy, gripping)`, `move(gloopy, facing)` — вилітає туди, куди дивився в мить відпускання.
- КОЛИ `enter(gloopy, hidden_spot)` → ЯКЩО `custom: «тут схований злиток»` → ТО `reveal(spot)`, `counter(gold_left, -1)`.
- КОЛИ `enter(gloopy, hidden_spot)` → ЯКЩО `custom: «тут Rubber Trap»` → ТО `reveal(spot)`, `bounce(gloopy)`, `set_cell(spot, wall)`, `custom: «стовпи обабіч більше не хапаються»`.
- КОЛИ `enter(gloopy, ingot)` → ЯКЩО `custom: «стадія з перевертанням»` (касета — з 22-ї; VS і Disk Beginner — з 23-ї; Disk Expert — з першої) → ТО `custom: «перевернути злиток лицем ↔ тьмяним боком»`, `counter(gold_left, ±1)` — кожен відрізок треба пройти непарну кількість разів.
- КОЛИ `input(fire)` → ТО `spawn(wave)` у напрямку `facing`.
- КОЛИ `contact(wave, unira)` → ТО `set_state(unira, stunned)`, `transform(unira, stunned_unira)` (стискається й жовтіє).
- КОЛИ `contact(gloopy, unira)` → ЯКЩО `state(unira, stunned)` → ТО `push(unira)`; інакше `lose` (−1 життя).
- КОЛИ `contact(stunned_unira, outer_wall)` → ТО `disappear_a`, `score(n)`.
- КОЛИ `state_off(unira, stunned)` → ТО `custom: «знову звичайний Unira»`.
- КОЛИ `level_start` → ЯКЩО `count(black_hole, >, 0)` → ТО `spawn_at(unira, black_hole)`; стадія без центральної діри (Pink у Disk) — без Unira.
- КОЛИ `enter(gloopy, black_hole)` → ЯКЩО `not state(gloopy, gripping)` → ТО `lose`.
- КОЛИ `edge(gloopy)` → ЯКЩО `custom: «стадія Purple або Yellow»` → ТО `wrap(gloopy)` (ліво ↔ право).
- КОЛИ `counter(gold_left, ==, 0)` → ТО `win` стадії, `custom: «екран блимає»`, `next_level`.
- КОЛИ `counter(time_left, ==, 0)` → ТО `lose` (−1 життя).
- КОЛИ `level_end` → ЯКЩО `mode(1P)` and `custom: «пройдено менш ніж за 300 відліків»` → ТО `score(bonus)`.
- КОЛИ `level_end` → ЯКЩО `mode(2P)` → ТО `score(bonus)` тому, хто відкрив більше злитків.
- КОЛИ `level_start` → ТО `set_state(gloopy, idle_invincible)` (касета, Disk): Глуппі стоїть і невразливий до першого вводу або кінця часу; VS і Disk — `idle(n)` → `move(gloopy, facing)` (примусовий старт).
- КОЛИ `level_end` → ЯКЩО `custom: «пройдено Yellow»` (VS/Disk Beginner — ще й після 2-ї стадії) → ТО `window(bonus-round)`: зібрати якомога більше злитків за час; повний збір — `score(3000)` (касетний баг дає 30).
- Перемога: нема (нескінченний цикл стадій). · Поразка: життя вичерпано → `game_over`; у 2P гравці мають окремі життя, той, хто лишився, грає далі сам. · Рахунок: злитки, розбиті Unira, бонус за швидкість, бонус-стадія.

## Керування і ввід
- D-pad — висунути руку в напрямку; утримання тримає стовп і крутить Глуппі навколо нього, відпускання — вилітає в поточному напрямку. Без стовпа хрестовина не повертає.
- A/B — хвиля вперед (оглушити Unira).
- 1–2 гравці одночасно на одному полі; у VS-аркаді оператор вирішує, чи 2P коштує 1 монету (стандарт — 2).

## Вікна, меню, HUD
- `splash-screen` — титул; вибір 1P / 2P (`mode-select`).
- `difficulty-select` — Disk-версія: BEGINNER / EXPERT.
- `game-screen` — стадія в кольоровій рамці; HUD угорі: `timer-countdown`, `remaining-counter` (злитків лишилось), `score`, `lives` (?).
- `custom-window` бонус-стадії (`+window:bonus-round`) — збір злитків на час, підсумок.
- `end-screen` — game over.
- Переходи: титул → game-screen → (злитки всі) блимання → наступна стадія → (після Yellow) бонус-стадія → … → (життя 0) game over → титул.

## Фічі поза полем
- `levels-sequential` циклом кольорів: касета — 4 розкладки на цикл, VS — 8; розкладки повторюються кожні 4 цикли.
- `difficulty-presets` (Disk: Beginner/Expert — з якої стадії починається перевертання).
- `operator-settings` (VS-аркада: ціна 2P).
- `mode-coop` — одночасна гра вдвох; суперництво за бонус; напарник може визволити Глуппі з глухої пастки двох сусідніх Rubber Trap (касетний баг-розклад).
- Нема збережень, паролів, паузи-меню (?).

## Варіації й родичі
- VS. Clu Clu Land (1984, аркада): удвічі більше розкладок, Boss Unira, частина пасток замінена злитками. Welcome to New Clu Clu Land (FDS, 1992) — порт VS з вибором складності; в Animal Crossing — «Clu Clu Land D». Порти: Sharp Zaurus, e-Reader, GBA (Famicom Mini), NSO.
- Родичі: Amidar (рух ребрами решітки, фарбування граней), Pac-Man (зібрати все, ворог з центру), Pengo і Heiankyo Alien (оглушити, а потім добити), Lady Bug і Drelbs (решітка зі станом).
- Осі варіацій:
  - **як аватар повертає**: будь-де (Pac-Man) / лише хапаючись за стовп або відскоком (Clu Clu Land) / лише на розвилках (Amidar);
  - **ціль збору**: видима (крапки) / схована під ребром (Clu Clu) / схована з парністю (перевертання);
  - **як убити ворога**: не можна / оглушити й виштовхати в стіну (Clu Clu) / оглушити й закопати (Heiankyo) / розчавити блоком (Pengo).

## Цікавинки для курсу
- Поворот лише навколо стовпа: стан «тримаю», кутова швидкість, напрям вильоту = поточний `facing` у мить відпускання — 🥉 (рух не по клітинах, а по ребрах з обертанням).
- Сховані злитки на ребрах + картинка з них + колір рамки як підказка — 📎.
- Перевертання на кожному проході (парність) — 🌱 логіка, 📎 з візуалізацією «скільки разів пройдено».
- Оглушити хвилею → штовхати → розбити об стіну: ланцюг станів ворога — 📎.
- Rubber Trap змінює топологію (ребро закрите, сусідні стовпи мертві); дві сусідні пастки дають глухий кут — 🥉 з перевіркою досяжності решти злитків.
- Тор лише на частині стадій (Purple/Yellow) — 🌱.

## Мапа на каталог
- Є: `move-auto` ↔ Глуппі пливе сам; `wrap-edges` ↔ Purple/Yellow; `collect-all` ↔ усі злитки; `touch-death` ↔ Unira; `environment-death` ↔ Black Hole; `player-death` · `time-out` ↔ таймер; `time-bonus` ↔ бонус за 300; `event-points`; `projectile-shot` + `shoot-forward` ↔ хвиля; `temporary-modes` ↔ оглушення; `spawn-points` ↔ Unira з дір; `sequential-levels` ↔ цикл кольорів; `difficulty-levels` ↔ Beginner/Expert; `game-screen` · `status-panel` · `remaining-counter`.
- **Нема** → пропозиції карток:
  - `+grid-line-field` (Amidar) — рух по ребрах решітки стовпів.
  - `+post-swing-turn` «Поворот лише хапаючись за стовп» · entities/move · 🥉 · слот {release: facing}.
  - `+hidden-collectibles-reveal` «Сховані на шляху предмети проявляються проходом» · entities/interact · 📎 · слот {hint: shape}.
  - `+parity-reveal` «Предмет перевертається при кожному проході» · entities/state · 🌱.
  - `+stun-push-kill` «Оглушити й дотиснути до стіни» · entities/combat · 📎.
  - `+rubber-trap` «Схована пастка закриває ребро й сусідні опори» · entities/legality · 📎.
  - `+shared-field-coop` — 2P одночасно на одному полі з окремими життями.
  - `+bonus-stage` «Бонус-стадія на час між циклами» · game-logic/score · 🌱.

## Пропозиції до словників
- `+effect:pivot(a, post)` — обертатися навколо опори, доки тримається ввід (уже пропонувалось у корпусі — підтверджую).
- `+effect:flip(a)` — перевернути двостановий предмет (відкритий ↔ тьмяний злиток).
- `+window:bonus-round` — окремий бонус-екран між стадіями (Amidar, Clu Clu Land, Devil World, Drelbs).
- `+card:post-swing-turn`, `+card:hidden-collectibles-reveal`, `+card:parity-reveal`, `+card:stun-push-kill`, `+card:rubber-trap` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Clu Clu Land](https://en.wikipedia.org/wiki/Clu_Clu_Land) — Turning Posts як єдиний спосіб повороту, злитки, перевертання на пізніх рівнях, Unira і хвиля, Black Hole, таймер, VS/Disk-версії, порти.
- [Wikipedia JA: クルクルランド](https://ja.wikipedia.org/wiki/クルクルランド) — Rubber Trap, відскок від стіни, з якої стадії перевертання, бонус менш ніж за 300, бонус-стадія 3000/30, порядок кольорів і тор, idle-невразливість, 2P-правила, розкладки 4/8.
- [Nintendo: Famicom 40th — クルクルランド](https://www.nintendo.com/jp/famicom/software/hvc-cl/index.html) — офіційне керування (тримати/відпустити), A/B — хвиля, оглушений жовтий Unira до зовнішньої стіни, бонус після жовтої стадії, фігури злитків за кольором.
- YouTube: пошук «Clu Clu Land gameplay».

## Непевне
- (?) Точні очки за злиток, за розбитого Unira і бонус за швидкість; стартова кількість життів і тривалість таймера — не знайдено.
- (?) Як саме поводиться Unira (кидається «на очах» — по лінії? випадково?) і чи є випадковість у грі; `random: none` — припущення.
- (?) Поведінка Boss Unira у VS-версії.
- (?) Режими Game A / Game B на касеті — не підтверджено; рецензія CONTINUE описує A/B як «праву руку», хрестовину як «ліву» — розходиться з офіційним «A/B — хвиля».
- (?) Чи можна в 2P штовхати чи оглушувати напарника.
