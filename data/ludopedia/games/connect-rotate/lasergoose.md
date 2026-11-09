---
title: Lasergoose
slug: lasergoose
aka: [lasergoose]
family: connect-rotate
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: collect
year: 2025
platforms: [web]
links:
  - {kind: itch, url: "https://ravensisle.itch.io/lasergoose", best: true, note: "грати в браузері; керування, мета, коментарі гравців"}
  - {kind: other, url: "https://codeberg.org/maia/lasergoose", note: "код PuzzleScript (CC BY-NC 4.0): обʼєкти, правила, умова перемоги"}
  - {kind: other, url: "https://thinkygames.com/games/lasergoose/", note: "Thinky Games: single-screen beam reflection, день 19 Confounding Calendar 2025 (бачив у пошуку)"}
  - {kind: other, url: "https://confoundingcalendar.itch.io/", note: "Confounding Calendar — адвент-календар thinky-ігор"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=lasergoose+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [beam-tracing, mirror-reflect, move-4dir, keyboard-controls, swipe-gestures, collect-all, item-pickup, undo-unlimited, restart-level, movement-animation, sound-effects, facing-icon, game-screen, +move-to-beam-end, +flip-after-hit, +edge-walls, +beam-perch, +rotating-gate]
proposes: ["+trigger:beam_end", "+effect:flip_state", "+card:move-to-beam-end", "+card:flip-after-hit", "+card:edge-walls", "+card:beam-perch", "+card:rotating-gate"]
author: opus
date: 2026-11-09
---

# Lasergoose — гуска не ходить, а стріляє лазером і переноситься туди, де промінь уперся в стіну

## Суть
Одноекранний лабіринт-пазл на PuzzleScript: гуска має зібрати всі яйця. Ходити вона не вміє — стрілка випускає лазер, промінь летить, відбивається від дзеркал і впирається в стіну, а гуска опиняється в його кінцевій клітині. Частина дзеркал і поворотні ворота перемикаються від кожного проходу променя, тож лабіринт «зсувається» після кожного пострілу. Ядро — промінь як засіб пересування, а не як ціль.

## Поле і час
- Квадратна сітка, один екран-рівень (у коді — лабіринт на 13 рядків).
- Стіни — **ребра між клітинами**: блок `#` у коді на старті перетворюється на межі `WallN/S/W/E` сусідніх клітин і зникає.
- Хід = постріл; промінь анімований по клітині за тік реального часу (`realtime_interval 0.03`), але логіка покрокова.
- Інформація повна; випадковості в механіці нема (лише фаза блимання яєць).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гуска | player | напрям погляду W/E | не ходить; стріляє в 4 напрямки; переноситься в кінець променя |
| Промінь | projectile | напрям; голова | летить клітина за клітиною; зупиняється на стіні-ребрі; не зупиняється на яйцях |
| Стіна-ребро | static | бік клітини | блокує промінь і постріл у свій бік |
| Дзеркало `/` `\` | static | діагональ | відбиває промінь на 90° |
| Перемикне дзеркало Z/S | object | CW / CCW | відбиває як дзеркало; після пострілу, що його зачепив, перевертається на іншу діагональ |
| Поворотні ворота I / – | gate | стіни N-S або E-W | клітина-тунель зі стінами з двох боків; прохід променя повертає її на 90° |
| Жердинка (rest) | terrain | — | якщо промінь проходить через неї, гуска сідає тут, а не в кінці променя; погляд розвертається |
| Яйце | pickup | блимає жовте/біле | збирається, коли гуска опиняється в його клітині |
| Старт | static | блимає | позначка клітини; блимає на старті рівня й після гелкоту |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(arrow, dir)` → ЯКЩО `custom: «з цього боку клітини гуски нема стіни-ребра»` → ТО `custom: «випустити промінь у напрямку dir»`; інакше `block`.
- КОЛИ `tick` → ЯКЩО `custom: «перед головою променя нема стіни й гуски»` → ТО `move(beam, dir)`.
- КОЛИ `custom: «голова променя в клітині з дзеркалом»` → ТО `bounce(beam)` — поворот на 90° за діагоналлю.
- КОЛИ `custom: «промінь пройшов через перемикне дзеркало або ворота»` → ТО `set_state(piece, toggle)`.
- КОЛИ `blocked(beam)` (стіна-ребро попереду) → ТО `teleport(goose, beam_head)` (+trigger:beam_end).
- КОЛИ `custom: «промінь повернувся в клітину гуски»` → ТО `custom: «гуска лишається на місці»`; якщо нічого не перемкнулось — хід не записується в історію.
- КОЛИ `custom: «промінь пройшов клітину-жердинку»` → ТО `teleport(goose, rest)`, `face(goose, opposite)`.
- КОЛИ `custom: «постріл завершено»` → ЯКЩО `state(piece, toggle)` → ТО `custom: «дзеркало CW↔CCW, ворота N-S↔E-W»` (+effect:flip_state).
- КОЛИ `enter(goose, egg)` → ТО `disappear_b`, `sound(egg)`.
- КОЛИ `input(x)` → ТО `custom: «гелкіт: блимає позначка старту, на поле не впливає»`.
- КОЛИ `input(z)` → ТО `undo` · КОЛИ `input(r)` → ТО `restart`.
- КОЛИ `all_gone(egg)` → ТО `win`, `message(congratulations)`.
- Перемога: зібрано всі яйця · Поразка: нема · Рахунок: нема.

## Керування і ввід
- Стрілки або свайп — постріл у напрямку; гуска летить разом з наслідком пострілу.
- X або тап — гелкіт (без ефекту на поле); Z — undo; R — рестарт (на тачі — через меню PuzzleScript).
- Ввід приймається лише між пострілами (`throttle_movement`).

## Вікна, меню, HUD
- `game-screen`: лабіринт, гуска, яйця; лічильника яєць **нема** (гравці скаржились у коментарях).
- `custom-window`: текстові екрани PuzzleScript — вступ і привітання з перемогою.
- `pause-menu` (стандартне меню PuzzleScript на тачі): undo, рестарт.
- Титульного екрана нема (`notitle`).
- Переходи: вступ → game-screen → екран-привітання.

## Фічі поза полем
- `undo` без ліміту — автор спеціально взяв PuzzleScript Next заради коректного undo (неефективні постріли не записуються).
- `restart-level`.
- `touch-controls` (свайпи), `mouse-and-keyboard`.
- Звуки на постріл, приземлення, перемикання дзеркал, яйце, гелкіт.
- Сесія ~30 хв; один рівень.

## Варіації й родичі
- Промінь як транспорт — родич «телепорту по лінії» з роглайків і `teleport` взагалі; у корпусі промінь зазвичай мета: [deflektor](deflektor.md), [laser-tank](laser-tank.md), [chromatron](chromatron.md), [khet](khet.md).
- Перемикання дзеркал від променя — як у [spin-doctor](spin-doctor.md) (обертання від проїзду), а ворота-турнікети — як у [zenji](zenji.md) / [infinity-loop](infinity-loop.md) за ідеєю орієнтації.
- Ковзання до упору (сімʼя push-slide: Inertia, Ice) — найближчий родич руху: «лечу, доки не вперся», але з дзеркалами.
- Осі варіацій: **рух: крок / ковзання до стіни / політ по променю** · **дзеркала: фіксовані / перемикні від променя / обертні гравцем** · **стіни: клітини / ребра** · **зупинка: лише стіна / жердинка ловить раніше**.

## Цікавинки для курсу
- Рух «у кінець променя» з відбиттями — трасування до упору плюс перенос аватара — 🌱.
- Стіни на ребрах замість клітин (4 біти на клітину, перевірка з обох боків) — 📎.
- Перемикні дзеркала й ворота: стан змінюється **після** пострілу, промінь у тому ж пострілі ще бачить старий — 📎.
- Жердинка, що ловить гуску на шляху, — перша спеціальна клітина на трасі — 🌱.
- Undo, що пропускає «порожні» ходи (стан не змінився), — 📎.
- Перевірка, що рівень розвʼязний: BFS по станах (позиція × орієнтації перемикачів × зібрані яйця) — 🥈.

## Мапа на каталог
- Є: `beam-tracing` · `mirror-reflect` · `move-4dir` (4 напрямки пострілу) · `keyboard-controls` · `swipe-gestures` · `collect-all` · `item-pickup` · `undo-unlimited` · `restart-level` · `movement-animation` (анімація променя) · `sound-effects` · `facing-icon` (гуска дивиться W/E) · `game-screen`.
- **Нема** → пропозиції карток:
  - `+move-to-beam-end` «Аватар переноситься в кінець свого променя» · entities/move · 🌱.
  - `+flip-after-hit` «Обʼєкт перемикає орієнтацію після проходу променя» · entities/state · 📎.
  - `+edge-walls` «Стіни на ребрах між клітинами» · entities/legality · 📎.
  - `+beam-perch` «Клітина, що зупиняє рух по променю раніше» · entities/interact · 🌱 (родич `stop-cell`).
  - `+rotating-gate` «Ворота-тунель повертаються на 90° від проходу» · entities/state · 📎.

## Пропозиції до словників
- `+trigger:beam_end(beam)` — промінь досяг кінця траси (уперся в стіну).
- `+effect:flip_state(a)` — перемкнути бінарну орієнтацію (CW↔CCW, N-S↔E-W).

## Джерела
- ⭐ [itch.io: lasergoose](https://ravensisle.itch.io/lasergoose) — гра в браузері, керування (стрілки/свайп, X, Z, R), мета, PuzzleScript Next, коментарі.
- [Codeberg: maia/lasergoose](https://codeberg.org/maia/lasergoose) — повний код `lasergoose.puzzlescript`: обʼєкти, правила руху променя, перемикання, `no Egg`.
- [Thinky Games](https://thinkygames.com/games/lasergoose/) — класифікація «single-screen beam reflection», день 19 календаря (за результатами пошуку; сторінка віддає 403).
- [Confounding Calendar](https://confoundingcalendar.itch.io/) — контекст події.

## Непевне
- (?) Жердинка: правило в коді спрацьовує, коли будь-який сегмент променя на ній, — чи завжди перша на шляху, не перевіряв у грі.
- (?) «Справжній фінал» через гелкіт — лише натяк у коментарі (rot13); у прочитаних правилах гелкіт косметичний.
- (?) Як саме промінь поводиться при самоперетині (у коді два набори сегментів) — не розбирав.
- (?) Ворота «~» поза внутрішньою частиною лабіринту — призначення не зʼясоване.
