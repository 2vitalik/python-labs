---
title: Hungry Horace
slug: hungry-horace
aka: [Horacio Glotón, Horácio Glutão, Голодний Горацій]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: score
year: 1982
platforms: [ZX Spectrum, Timex TS2068, Commodore 64, Dragon 32/64, Windows, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hungry_Horace", best: true, note: "суть: парк, сторожі, дзвін як енерджайзер, платформи, редактор рівнів C64"}
  - {kind: other, url: "https://spectrumcomputing.co.uk/entry/2390/ZX-Spectrum/Hungry_Horace", note: "картка ZXDB: автор, видання, інструкції, мапа"}
  - {kind: other, url: "https://www.spectrumcomputing.co.uk/pub/sinclair/games-info/h/HungryHorace(HoracioGloton)(InvestronicaS.A.).txt", note: "інструкція іспанського видання: клавіші, 10/100 очок, 3 впіймання, секції з виходом"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=hungry+horace+zx+spectrum+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, move-by-input, impassable-cells, touch-death, chase-player, temporary-modes, event-points, reach-exit, sequential-levels, progress-acceleration, keyboard-controls, in-game-editor, player-death, +section-exit-no-clear, +alarm-panic, +thrown-out-of-park, +dropped-bonus-food]
proposes: ["+trigger:exit_section", "+effect:eject(a)", "+card:section-exit-no-clear"]
author: opus
date: 2026-11-09
---

# Hungry Horace — Pac-Man у парку: їж квіти, бий на сполох, щоб сторожі запанікували, і тікай у наступну секцію

## Суть
Горацій ходить доріжками, містками й тунелями парку й їсть усе на шляху; сторожі ловлять його й викидають з парку. Якщо він увімкне **сигналізацію (дзвін)**, сторожі панікують — тепер Горацій ловить і викидає їх. Головна відмінність від [Pac-Man](pac-man.md): рівень не треба зачищати — кожна секція парку має **вихід у наступну**, і йти можна будь-коли. Перша гра серії Horace від Psion для ZX Spectrum 16K.

## Поле і час
- Лабіринт-парк на клітинній сітці екрана; доріжки, містки, тунелі.
- Парк поділено на кілька секцій-екранів; у кожній — вихід у наступну; кожна наступна складніша.
- Real-time; сторожі рухаються самі.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Горацій | player | 3 впіймання | рух 4 напрямки клавішами |
| Квітка | pickup | 10 очок | зʼїдається при дотику |
| Сторож | enemy | — | ловить Горація і викидає з парку |
| Сигналізація (дзвін) | switch | кілька на парк | дотик → сторожі панікують |
| Сніданок сторожа (вишні, полуниці) | pickup | 100 очок | сторож іноді впускає, можна зʼїсти |
| Вихід секції | static | — | перехід у наступну секцію |
| Стіна, кущі | static | — | непрохідні |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(horace, dir)`; інакше `block`.
- КОЛИ `contact(horace, flower)` → ТО `disappear_b`, `score(10)`.
- КОЛИ `contact(horace, alarm)` → ТО `set_state(guard, panic, duration)` (як енерджайзер Pac-Man).
- КОЛИ `contact(guard, horace)` → ЯКЩО `not state(guard, panic)` → ТО `lives(-1)`, `custom: «Горація викидають з парку»` (`+effect:eject`).
- КОЛИ `contact(horace, guard)` → ЯКЩО `state(guard, panic)` → ТО `custom: «сторожа викидають з парку»` (`+effect:eject`), `score(n)` (?).
- КОЛИ `rng(p)` → ТО `spawn_at(breakfast, guard_cell)` (сторож впустив сніданок) (?).
- КОЛИ `contact(horace, breakfast)` → ТО `disappear_b`, `score(100)`.
- КОЛИ `reach(horace, exit)` → ТО `next_level` (наступна секція, складніша) — зʼїдати всі квіти й вмикати дзвін не обовʼязково.
- КОЛИ `counter(caught, ==, 3)` → ТО `game_over`.
- Перемога: нема — рекорд. Поразка: впійманий 3 рази. Рахунок: квітка 10, сніданок 100.

## Керування і ввід
- Q — вгору, Z — вниз, I — ліворуч, P — праворуч (іспанське видання).
- Ввід лише на рух; дій нема.

## Вікна, меню, HUD
- `game-screen` — секція парку, `score`, `lives` (?).
- `end-screen` — кінець гри.
- Переходи: старт → секція 1 → (вихід) секція 2 → … → (3 впіймання) кінець.

## Фічі поза полем
- `level-editor` — у версії C64 був редактор рівнів зі збереженням і обміном (за Wikipedia, без джерела); для Spectrum — фанатський редактор 2009 року і окремий «Levels Designer» (1984, у ZXDB як втрачений).
- Звук можна було підсилити через магнітофон, підʼєднаний до MIC.

## Варіації й родичі
- [Pac-Man](pac-man.md) — оригінал: зʼїсти всі точки, 4 енерджайзери по кутах, з'їдений привид-очі повертаються в будинок; тут — вихід у наступну секцію без зачистки, сигналізація на мапі, «викинутий» сторож.
- [Pac-Man: спін-офи](pac-man-spinoffs.md) — інші відходи від формули.
- Сиквели: Horace Goes Skiing (Frogger + лижі), Horace & the Spiders, Horace to the Rescue; Hungry Horace 2 (фанатський, 2010).
- **Осі варіацій:** мета рівня (зʼїсти все / дійти до виходу); енерджайзер (таблетка / кнопка-сигналізація на мапі); доля впійманого ворога (повернутись у будинок / викинутий з поля).

## Цікавинки для курсу
- Вихід, доступний одразу: гравець сам вирішує, скільки ризикувати заради очок — 🌱.
- Сигналізація як енерджайзер-перемикач на мапі — 🌱 (той самий `temporary-modes`, інше джерело).
- Ворог впускає бонус, який можна підібрати — 🌱.
- Секції парку як ланцюг екранів зі зростанням складності — 📎.

## Мапа на каталог
- Є: `move-4dir` · `move-by-input` · `impassable-cells` · `touch-death` · `chase-player` · `temporary-modes` · `event-points` · `reach-exit` · `sequential-levels` · `progress-acceleration` · `keyboard-controls` · `in-game-editor` (C64) · `player-death`.
- **Нема** → пропозиції карток:
  - `+section-exit-no-clear` «Вихід з рівня без вимоги зачистки» · levels/progression · 🌱.
  - `+alarm-panic` «Перемикач на мапі лякає ворогів» · entities/state · 🌱.
  - `+thrown-out-of-park` «Впійманого ворога прибирають з поля» · entities/combat · 🌱.
  - `+dropped-bonus-food` «Ворог випадково впускає бонус» · entities/spawn · 🌱.

## Пропозиції до словників
- `+trigger:exit_section` — аватар вийшов через вихід секції (близьке до Berzerk `+trigger:room_exit`; можна злити).
- `+effect:eject(a)` — прибрати сутність з поля «за межі» (не смерть: Горацій, сторож).
- `+card:section-exit-no-clear` — див. вище.

## Джерела
- ⭐ [Wikipedia: Hungry Horace](https://en.wikipedia.org/wiki/Hungry_Horace) — їжа в парку, сторожі, дзвін = енерджайзер, «простий клон Pac-Man», платформи, редактор рівнів C64.
- [ZXDB: Hungry Horace](https://spectrumcomputing.co.uk/entry/2390/ZX-Spectrum/Hungry_Horace) — Spectrum 16K, 1982, Sinclair Research, Pac-Man як натхнення, видання і локалізації, лінки на інструкції й мапу.
- [Інструкція Horacio Glotón (txt)](https://www.spectrumcomputing.co.uk/pub/sinclair/games-info/h/HungryHorace(HoracioGloton)(InvestronicaS.A.).txt) — клавіші QZIP, квітка 10, сніданок 100, 3 впіймання, кілька сигналізацій, секції з виходом, «не треба зʼїдати все».
- YouTube: пошук «hungry horace zx spectrum gameplay».

## Непевне
- (?) Кількість секцій парку і чи цикл повторюється (з памʼяті — 4 мапи).
- (?) Очки за викинутого сторожа; тривалість паніки; чи дзвін знову активний після використання.
- (?) Коли саме сторож впускає сніданок.
- (?) Чи є додаткові життя за очки.
- (?) Розкладка клавіш англійського видання (PDF-інструкція — скан, не прочитано).
