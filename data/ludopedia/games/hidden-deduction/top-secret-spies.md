---
title: Top Secret Spies (Heimlich & Co.)
slug: top-secret-spies
aka: [Heimlich & Co., Under Cover, Detective & Co.]
family: hidden-deduction
also: [board-digital]
klass: figure
axes:
  field: 1d
  time: turn
  opponent: hotseat
  info: hidden
  random: both
  goal: race
year: 1984
platforms: [board (Edition Perlhuhn 1984, Ravensburger 1986, Amigo 2001, Rio Grande)]
links:
  - {kind: other, url: "https://kramer-spiele.hier-im-netz.de/spielregeln/TopSecretSpies_Heimlich_US_.pdf", best: true, note: "правила Rio Grande/Amigo (EN, PDF): базова гра, варіант Top Secret з 26 картами, варіант «Secret Dossier»"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Top_Secret_Spies", note: "Kramer, Spiel des Jahres 1986, перший трек очок довкола поля"}
  - {kind: wiki, url: "https://de.wikipedia.org/wiki/Heimlich_%26_Co.", note: "видання, 2–7 гравців, руїна −3, «Kramerleiste», Top-Secret-Karten Amigo"}
  - {kind: other, url: "https://www.spiel-des-jahres.de/spiele/heimlich-co", note: "12 будівель (10 будинків, руїна, церква), трек 41 поле, сейф у будинку 7"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Heimlich+%26+Co+board+game", note: "пошук; правила"}
stage: v1
coverage: 70
mechanics: [hot-seat, turn-enforcement, wrap-edges, event-points, rule-variants, pass-device, match-setup, game-screen, end-screen, help-window, +roll-and-move, +split-move-points, +move-any-piece, +hidden-identity, +unowned-colors, +moving-scoring-site, +score-track-around-board, +negative-space, +reaction-card-window, +deck-draw, +hand-limit, +identity-guess-bonus, +belief-set-tracking]
proposes: ["+effect:roll_dice", "+effect:draw_card", "+trigger:scoring", "+ui:score-track", "+ui:deduction-sheet", "+window:dossier-window", "+card:move-any-piece", "+card:moving-scoring-site", "+card:identity-guess-bonus"]
author: opus
date: 2026-11-09
---

# Top Secret Spies (Heimlich & Co.) — усі рухають усіх агентів по колу будинків, а чий колір твій — таємниця до кінця

## Суть
Сім агентів-фігур стоять на кільці з 12 будівель; кожен гравець таємно знає лише свій колір, решта кольорів можуть бути «вільними» — без власника. На хід гравець кидає кубик і ділить очки руху між **будь-якими** агентами, а коли хтось заходить у будинок із сейфом, усі агенти отримують очки за номер свого будинку. Щоб тебе не «викрили» й не загнали в руїни, треба допомагати чужим і блефувати. У варіанті «Досьє» наприкінці ще й вгадують, хто є хто.

## Поле і час
- Кільце з 12 будівель за годинниковою: церква (0) → будинки 1–10 → руїни (−3) → церква; рух лише за годинниковою, 1 очко = 1 будівля.
- Кілька агентів у будівлі — можна; сейф стоїть в одній будівлі.
- Трек очок довкола поля (41 поле, старт = фініш) — по маркеру на колір.
- Хід: кидок → рух → (варіант: фаза Top Secret) → підрахунок, якщо є → кубик лівому сусіду.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Агент ×5–7 | piece | колір | рухає будь-хто; очки за номер будинку при підрахунку |
| Карта агента | mark | колір, закрита | визначає власника кольору; нероздані — «вільні агенти» під полем |
| Церква | static | 0 | старт агентів; при підрахунку 0 очок |
| Будинок 1–10 | static | номер = очки | при підрахунку агент отримує номер будинку |
| Руїни | hazard | −3 | при підрахунку −3 (не нижче старту) |
| Сейф | object | будівля | перехід агента в його будівлю = підрахунок; після — переставляється |
| Маркер очок | mark | колір | крокує треком; першим за фініш — кінець гри |
| Кубик | object | грані «1-3», 2, 3, 4, 5, 6 | «1-3» — на вибір 1, 2 або 3 |
| Карта Top Secret ×26 | pickup | 14 видів дій | лише у варіанті; рука ≤ 4 |

## Правила (КОЛИ → ЯКЩО → ТО)
- Старт: КОЛИ `game_start` → ТО `custom: «агенти в церкві, маркери на старті, сейф у будинку 7; кожному таємно карта кольору; решта — вільні агенти, закрито під полем»`; агентів: 2 гравці — 5, 3 — 6, 4+ — 7.
- КОЛИ `turn_start(player)` → ТО `custom: «кидок кубика»` (`+effect:roll_dice`); 2–6 — стільки очок; «1-3» — `choose(1 | 2 | 3)`.
- КОЛИ `input(move, agent, k)` → ТО `move(agent, cw)` k разів; очки можна ділити між будь-якими агентами, рухати хоча б одного, витратити всі, не зберігаючи.
- КОЛИ `enter(agent, safe_building)` → ТО `custom: «підрахунок»` (`+trigger:scoring`); прохід крізь будинок із сейфом не рахується.
- Підрахунок: для кожного агента `counter(score[color], +building_number)`.
- Підрахунок у руїнах: КОЛИ `custom: «підрахунок»` → ЯКЩО `cell(agent, ruins)` → ТО `counter(score[color], -3)` (не нижче старту); у церкві — 0.
- КОЛИ `after(scoring)` → ТО `custom: «активний гравець ставить сейф у будь-яку будівлю (і руїни, і церкву)»`; постановка сейфа на агентів підрахунку не дає.
- КОЛИ `turn_end(player)` → ТО `end_turn` (кубик лівому сусіду).
- КОЛИ `counter(score, >=, finish)` → ТО `custom: «доіграти хід; відкрити всі карти, і вільні теж»`, `game_over`; виграє власник найдальшого маркера; ЯКЩО `custom: «найдальший — вільний агент»` → ТО `custom: «переграти»`.
- Варіант Top Secret: на старті кожен тягне 2 карти (`+effect:draw_card`), рука ≤ 4; ЯКЩО `count(hand, ==, 4)` → п'яту не тягнуть.
- КОЛИ `enter(agent, ruins)` → ЯКЩО `turn_of(player)` → ТО `custom: «тягнути 1 карту на кожен випадок, не на агента»`; КОЛИ `custom: «випало «1-3» і гравець не рухає нікого»` → ТО `custom: «тягнути 1 карту»`.
- КОЛИ `after(move)` → ТО `custom: «фаза Top Secret: охочі грають карти за годинниковою від активного, доки всі підряд не спасують»`; підрахунок — лише якщо після фази агент досі в будинку з сейфом.
- Карти: `move(agent, back 1–2)` · `move(agent, ±1)` · два агенти −1 · два агенти +1 · агент у будинку з сейфом ±1 · `custom: «сейф у будь-яку будівлю»` · `teleport(agent, ruins)` · `teleport(all, church)` · `swap(agent_a, agent_b)` · `teleport(agent, other_agent)` · 1–2 агенти з руїн у церкву · агент +1…3 · два маркери +3 (не далі поля 40) · `teleport(agent, safe)` · `custom: «подивитись карту вільного агента — грати двома, наприкінці лишити кращого»` (не з 7 гравцями).
- Варіант «Досьє»: КОЛИ `counter(first_marker, >=, 29)` → ТО `custom: «кожен таємно записує, хто грає яким кольором (або «вільний»)»`; КОЛИ `game_over` → ТО `counter(score[own], +5)` за кожне вгадане.
- Перемога: маркер свого кольору першим за фінішем (або найдальший) · Поразка: — · Рахунок: позиція маркера; у «Досьє» + 5 за вгадані кольори.

## Керування і ввід
- Кидок кубика; розподіл очок кроками по агентах (хто куди, скільки).
- Ведення таємних нотаток-досьє: хто кого рухав у руїни, хто не скористався підрахунком.
- Таємна карта кольору — лише перегляд власником; розмова й блеф — частина гри.

## Вікна, меню, HUD
- `match-setup` (цифрова версія): 2–7 гравців, варіанти Top Secret і «Досьє».
- `game-screen` (цифрова версія): кільце 12 будівель з номерами, агенти, сейф; `+ui:score-track` довкола поля; результат кубика; рука карт Top Secret.
- `pass-device` (цифрова версія): показ таємної карти кольору й руки.
- `+window:dossier-window` (цифрова версія): `+ui:deduction-sheet` «колір → гравець / вільний» з нотатками.
- `end-screen` (цифрова версія): відкриті кольори, бонуси досьє, переможець.
- `help-window` (цифрова версія): список 14 карт.

## Фічі поза полем
- `custom-rules`: базова гра · Top Secret (карти й нове правило кубика) · «Досьє» (поєднується з обома).
- Кількість агентів залежить від кількості гравців; із 7 гравцями вільних агентів нема.

## Варіації й родичі
- Видання: Edition Perlhuhn (1984), Ravensburger (1986), Amigo (2001, нове оформлення й 26 карт Top Secret), Rio Grande (Top Secret Spies); Under Cover — назва в огляді Games Magazine.
- Родичі: [inkognito.md](inkognito.md) (прихована особа й напарник), [mr-jack.md](mr-jack.md) (особа серед спільних фігур), [geistertreppe.md](geistertreppe.md) (чия фігура — таємниця), [stratego.md](stratego.md).
- **Осі варіацій**:
  - фігури: свої / спільні — рухає будь-хто (тут);
  - власник кольору: відомий / таємний із «вільними» без власника (тут);
  - очки: за власну дію / усім одразу за положення (тут);
  - дедукція: лише блеф (базова) / вгадування з бонусом (Досьє).

## Цікавинки для курсу
- Кільцевий трек і розподіл очок руху між багатьма фігурами — 🌱.
- Підрахунок «усім за положення» при вході в будинок сейфа + переставляння сейфа — 🌱.
- Фаза реакцій: карти по колу, доки всі не спасують, і скасування підрахунку — 📎.
- Таємні кольори з «вільними» агентами + бонус за вгадування — 📎.
- AI, що оцінює ймовірність «хто який колір» за історією ходів — 🥇.

## Мапа на каталог
- Є: `hot-seat` / `turn-enforcement` · `wrap-edges` ↔ кільце будівель · `event-points` ↔ номер будинку · `rule-variants` ↔ Top Secret і Досьє · `pass-device` · `match-setup` · `game-screen` / `end-screen` / `help-window`.
- **Нема** → пропозиції карток:
  - `+move-any-piece` «Будь-хто рухає будь-яку фігуру» · game-logic/opponent · 🌱.
  - `+moving-scoring-site` «Точка підрахунку, яку переставляє гравець» · game-logic/score · 🌱.
  - `+identity-guess-bonus` «Наприкінці вгадати чужі ролі за бонус» · game-logic/score · 🌱.
  - `+reaction-card-window` «Фаза реакцій: карти по колу до загального пасу» · game-logic/opponent · 📎.
  - Також: `+roll-and-move`, `+split-move-points`, `+hidden-identity`, `+unowned-colors`, `+score-track-around-board`, `+negative-space`, `+deck-draw`, `+hand-limit`, `+belief-set-tracking`.

## Пропозиції до словників
- `+effect:roll_dice` — кидок кубика з особливою гранню («1-3» на вибір).
- `+effect:draw_card` — тягнути карту в руку.
- `+trigger:scoring` — настала ситуація підрахунку (агент увійшов у будинок сейфа після фази реакцій).
- `+ui:score-track` — трек очок довкола поля, маркер на колір.
- `+ui:deduction-sheet` — таблиця «колір → гравець» для нотаток.
- `+window:dossier-window` — таємне досьє, що фіксується в певний момент.
- `+card:move-any-piece`, `+card:moving-scoring-site`, `+card:identity-guess-bonus`.

## Джерела
- ⭐ [Правила Top Secret Spies (Rio Grande/Amigo, PDF)](https://kramer-spiele.hier-im-netz.de/spielregeln/TopSecretSpies_Heimlich_US_.pdf) — склад, сетап, кубик «1-3», рух за годинниковою, підрахунок і сейф, кінець гри, варіант Top Secret (усі 14 карт), варіант «Досьє» (поле 29, +5).
- [Wikipedia: Top Secret Spies](https://en.wikipedia.org/wiki/Top_Secret_Spies) — Kramer, Ravensburger, SdJ 1986, трек очок довкола поля, «Under Cover» / «Detective & Co.».
- [Wikipedia DE: Heimlich & Co.](https://de.wikipedia.org/wiki/Heimlich_%26_Co.) — видання 1984/1986/2001, 2–7 гравців, руїна −3, Kramerleiste, нагороди.
- [Spiel des Jahres: Heimlich & Co.](https://www.spiel-des-jahres.de/spiele/heimlich-co) — 12 будівель, трек 41 поле, сейф у будинку 7, «Profi»-варіант з вгадуванням.

## Непевне
- (?) Фінішне поле: трек 41 поле (spiel-des-jahres.de), карта Top Secret згадує «поле 40»; EN-Wikipedia подає «129+ / 142+» очок — можливо, інше видання (кілька кіл).
- (?) Перехід руїни → церква на кільці виведено з прикладу правил (агент з 10 «вперед» потрапляє в руїни), прямо не сказано.
- (?) Правила видань 1984/1986 (без карт) можуть відрізнятися деталями кубика; описано видання Amigo/Rio Grande 2001.
