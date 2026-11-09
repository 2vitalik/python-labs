---
title: SOKOBOT
slug: sokobot
aka: []
family: program-robots
also: [push-slide]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: collect
year: 2022
platforms: [PC (Windows)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1714050/", best: true, note: "опис, 6 скриншотів (панель команд з клавішами, рядки програм ботів, лічильники GOALS / COMMANDS / CYCLES, карта рівнів, лідерборди з гістограмами), трейлер"}
  - {kind: itch, url: "https://tayl1r.itch.io/sokobot", note: "itch-сторінка автора: Unity, Windows, демо; на itch нема лідербордів і гістограм (Steamworks)"}
  - {kind: other, url: "https://tayl1r.itch.io/sokobot/devlog/396382/jelly-update", note: "девлог Jelly Update: нова зона з желе, що склеює блоки"}
  - {kind: other, url: "https://gamebrain.co/game/sokobot", note: "опис «infinitely-looping assembly lines that combine shapes», відгуки про UI і жорсткі WASD"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=SOKOBOT+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [command-program, step-execution, cursor-place, move-4dir, stick-together, collect-quota, goal-counter, leaderboard, world-map, level-unlock, game-screen, settings-window, keyboard-controls, height-levels, +swarm-separate-programs, +looping-program, +grab-and-carry, +entity-rotate, +solution-metrics, +metric-histograms, +percentile-leaderboard, +gif-export, +solution-files, +step-run-speed, +command-repeat-count]
proposes: ["+effect:grab", "+effect:drop", "+effect:sleep(a)", "+effect:wake(a)", "+trigger:delivered(shape, target)", "+feature:solution-metrics", "+feature:gif-export", "+window:metric-histograms", "+ui:program-rows"]
author: opus
date: 2026-11-09
---

# SOKOBOT — розстав роботів, дай кожному рядок команд, і вони безкінечно збирають фігури з блоків

## Суть
Пазл-автоматизація Alexander Taylor (2022): гравець ставить на ізометричне поле маленьких роботів-SOKOBOT-ів і кожному пише **рядок простих команд** — крок, поворот, взяти/відпустити, спати, розбудити, чекати. Рядки крутяться по колу, тож боти разом утворюють **безкінечну складальну лінію**: беруть блоки з плит появи, складають з них фігуру й доставляють на ціль; рівень пройдено, коли зібрано 10 цілей. Боти «спілкуються» — один засинає й чекає, інший його будить. Розвʼязків безліч; змагання — у трьох метриках (кількість ботів, команд, циклів) з гістограмами друзів.

## Поле і час
- Квадратна сітка, показана ізометрично, з бортиком; є ями (чорні провали), підняті платформи (висота) і стіни-виступи.
- Плити: зелена — звідки зʼявляються блоки (?), червона/рожева — ціль з напівпрозорим «привидом» потрібної фігури; синя плита зі стрілками й кругла кнопка — призначення не встановлене (див. «Непевне»).
- Час `programmed`: цикл = кожен бот виконує одну команду свого рядка; рядок повторюється, доки не стоп. Лічильник CYCLES рахує цикли до виконання квоти.
- Повна інформація, випадковості нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| SOKOBOT | player | номер (BOT 00, 01…), колір, напрям, рядок команд | ставиться гравцем; виконує свій рядок по колу; несе блок / фігуру |
| Блок-куб (зелений «+», блакитний «◎», помаранчевий тощо) | object | колір / тип | бот бере й несе; блоки складаються у фігуру |
| Капсула / циліндр | object | орієнтація | частина фігури; бот обертає її разом із собою |
| Фігура (зібрана група блоків) | object | форма | має збігтися з привидом на цілі за формою й орієнтацією (?) |
| Желе (Jelly) | object | — | склеює блоки між собою (зона Jelly Update) |
| Плита появи | source | — | на ній зʼявляються нові блоки (?) |
| Плита-ціль з привидом фігури | sink | потрібна фігура | прийняту фігуру зараховує в GOALS (?) |
| Яма | hazard | — | провал у підлозі (?) |
| Платформа / підвищення | terrain | висота | інший рівень поля (у трейлері — рівні з білими платформами) |
| Стіна / бортик | static | — | непрохідна |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(add_sokobot, cell)` → ЯКЩО `free(cell)` → ТО `place(player, sokobot)`; Q / E під час перетягування → `rotate(sokobot, 90)`.
- КОЛИ `input(play)` → ТО `custom: «усі боти виконують по одній команді за цикл; дійшовши до кінця рядка, починають знову»`.
- КОЛИ `exec(move(dir))` → ЯКЩО `free(cell)` → ТО `move(sokobot, dir)` (W/A/S/D — абсолютні напрями сітки); інакше `custom: «помилка: ефект Error, бот / запуск зупиняється»` (?).
- КОЛИ `exec(rotate(cw|ccw))` → ЯКЩО `custom: «фігура в руках вміщується після повороту»` → ТО `rotate(sokobot, 90)` разом з фігурою; інакше `block` + коротка анімація невдалого повороту.
- КОЛИ `exec(grab)` → ЯКЩО `occupied(cell_front, block)` → ТО `custom: «бот бере блок / фігуру»`; повторна команда → `custom: «відпускає»` (?).
- КОЛИ `contact(block, block)` → ЯКЩО `custom: «між ними желе»` → ТО `attach(block, block)`.
- КОЛИ `exec(sleep)` → ТО `set_state(sokobot, asleep)` — бот стоїть на команді zZ, доки його не розбудять (?).
- КОЛИ `exec(awake)` → ТО `clear_state(other_bot, asleep)` — локально (сусідніх) або всіх (дві різні команди X / C) (?).
- КОЛИ `exec(wait, n)` → ТО `stun(sokobot, n)` — пропустити N циклів (?).
- КОЛИ `custom: «команда має число повторів N»` → ТО `custom: «виконати її N разів поспіль»` (?).
- КОЛИ `custom: «з плити появи забрали блок»` → ТО `spawn_at(block, source)` (?).
- КОЛИ `custom: «фігура збігається з привидом на цілі»` → ТО `counter(goals, +1)`, `disappear(shape)`.
- КОЛИ `counter(goals, >=, 10)` → ТО `win`, `window(end-screen)` з лідербордами й гістограмами.
- Рахунок: `counter(sokobots)`, `counter(commands)`, `counter(cycles)` — три незалежні метрики; поразки нема.

## Керування і ввід
- Мишею: перетягнути бота з картки ADD SOKOBOT на клітину; Q / E — поворот під час перетягування.
- Програма — **рядок клітинок-команд** під полем для кожного бота (≈36 слотів); команду ставлять з палітри або клавішами: Q ↺ · W ↑ · E ↻ · R (куб: взяти/відпустити) · A ← · S ↓ · D → · Z (zZ сон) · X / C (чашки: розбудити) · V (пунктирне коло: чекати).
- Під командою може стояти число (2, 4, 5, 9) — повтор або тривалість (?).
- Кнопки STOP · PLAY · STEP · SPEED (рівні 1…5; відтворення розвʼязку до ×25).
- Відгуки: розкладка WASD жорстко прошита (незручно на не-QWERTY), бракує drag-and-drop для команд.

## Вікна, меню, HUD
- `game-screen`: поле; QUIT і CONFIG угорі ліворуч; праворуч угорі — `goal-counter` GOALS n/10, COMMANDS, CYCLES; картка ADD SOKOBOT; STOP/PLAY/STEP/SPEED; `+ui:program-rows` — рядки BOT 00…BOT 08 з поточною командою, підсвіченою кольором бота (`instruction-highlight`); палітра команд з клавішами і «?».
- `world-map`: ізометрична мапа плиток-рівнів 0-0…2-4 і EX-0…EX-2 з мініатюрою фігури й галочкою; плитка «TO AREA 01» веде в іншу зону.
- Діалог рівня: файли розвʼязків FILE 00 / FILE 01 з метриками «боти / команди / цикли», дублювати, видалити, NEW FILE, BACK; три `leaderboard` (SOKOBOTS, COMMANDS, CYCLES) з рядками Top 1% / Top 10% і `+window:metric-histograms`.
- `end-screen` (після перемоги) — лідерборди й гістограми (з оновлення 2022-06).
- `settings-window` (CONFIG): гучність музики, master volume (?).
- Переходи: карта зон → діалог рівня (файл) → поле → перемога → діалог/карта.

## Фічі поза полем
- `+feature:solution-metrics` — три метрики, лідерборди друзів з гістограмами.
- `+feature:gif-export` — GIF-експортер для поширення розвʼязків.
- Кілька файлів розвʼязку на рівень (FILE 00, 01…) — `save-slots` для розвʼязків; слоти збереження профілю (додано після релізу).
- `world-map` з розгалуженою прогресією: «Stuck? Try another and come back later!»; EX-рівні; зона Jelly відкривається після двох EX-рівнів.
- `localization` — EN, JA, ZH (спрощ./трад.), KO; `achievements`, `cloud-save`; демо.
- Workshop / редактора рівнів нема (автор: «stretch goal»).

## Варіації й родичі
- Родичі в корпусі: `opus-magnum`, `spacechem`, `infinifactory` (циклічні програми + метрики + гістограми), `7-billion-humans`, `human-resource-machine`, `exapunks` (кілька виконавців), `cargo-bot`, `lightbot` (рядок команд), Sokoban-лінія з `push-slide` (переміщення блоків).
- Осі варіацій: **програма** (одна на всіх / окрема на кожного робота); **синхронізація** (жодної / сон-пробудження / семафори); **мета** (довезти один раз / квота з безкінечного циклу).

## Цікавинки для курсу
- Кілька роботів з окремими циклічними рядками команд, один такт на всіх — 🥉.
- Сон / пробудження як найпростіша синхронізація агентів — 🥈.
- Збирання фігури з блоків, поворот фігури з перевіркою колізій — 🥇.
- Плита появи + ціль з квотою = нескінченна складальна лінія — 📎.
- Три метрики розвʼязку і гістограма з перцентилями — 🥉.
- GIF-експорт запису розвʼязку — 📎.

## Мапа на каталог
- Є: `command-program` · `step-execution` · `cursor-place` · `move-4dir` · `stick-together` (желе) · `collect-quota` · `goal-counter` · `leaderboard` · `world-map` · `level-unlock` · `game-screen` · `settings-window` · `keyboard-controls` · `height-levels`.
- **Нема** → пропозиції карток:
  - `+swarm-separate-programs` «Кожен робот — свій рядок команд» · game-logic/program · 🥉.
  - `+looping-program` «Програма повторюється по колу до стопу» · game-logic/program · 🌱.
  - `+grab-and-carry` «Взяти / нести / відпустити обʼєкт» · entities/interact · 📎.
  - `+entity-rotate` «Поворот робота разом з вантажем, з перевіркою місця» · entities/move · 🥈.
  - `+solution-metrics`, `+metric-histograms`, `+percentile-leaderboard` — метрики, гістограми, Top 1 % / 10 %.
  - `+gif-export` «Запис розвʼязку в GIF» · interface/results · 📎.
  - `+solution-files` «Кілька збережених розвʼязків рівня» · game-logic/save · 🌱.
  - `+command-repeat-count` «Число повторів на команді» · game-logic/program · 🌱.
  - `+step-run-speed` — спільна для сімʼї.

## Пропозиції до словників
- `+effect:grab` / `+effect:drop` — взяти / відпустити обʼєкт (також у корпусі: Robozzle-подібні, Infinifactory).
- `+effect:sleep(a)` / `+effect:wake(a)` — синхронізація агентів сном і пробудженням.
- `+trigger:delivered(shape, target)` — фігуру доставлено на ціль (квота).
- `+feature:solution-metrics`, `+feature:gif-export`.
- `+window:metric-histograms` — гістограми метрик з позначкою свого результату.
- `+ui:program-rows` — рядки програм усіх агентів під полем.

## Джерела
- ⭐ [Steam: SOKOBOT](https://store.steampowered.com/app/1714050/) — опис і фічі (50+ рівнів, розгалужена прогресія, лідерборди й гістограми, GIF), скриншоти панелі команд і діалогу рівня; новини розробника (Jelly Update — 15 рівнів з желе; поворот з анімацією невдачі; Q/E під час перетягування; відтворення до ×25; «Local Awake VFX»; Top 1 % / Top 10 %).
- [itch.io: tayl1r/sokobot](https://tayl1r.itch.io/sokobot) — платформа, Unity, демо, без онлайн-фіч на itch.
- [Jelly Update (devlog)](https://tayl1r.itch.io/sokobot/devlog/396382/jelly-update) — зона з желе.
- [gamebrain: SOKOBOT](https://gamebrain.co/game/sokobot) — «infinitely-looping assembly lines that combine shapes», відгуки.
- YouTube: пошук «SOKOBOT gameplay».

## Непевне
- (?) Точний зміст команд R, Z, X, C, V — за іконками й новинами (куб, zZ, дві чашки кави, пунктирне коло; «Local Awake VFX»); офіційного списку не знайдено.
- (?) Що означають числа під командами (повтор / тривалість очікування).
- (?) Як саме зʼявляються нові блоки (плита появи) і як ціль перевіряє фігуру (форма, колір, орієнтація).
- (?) Що відбувається при зіткненні ботів, падінні в яму чи ході в стіну — є ефект «Error», але чи зупиняє він увесь запуск — не перевірено.
- (?) Призначення синьої плити зі стрілками та круглої кнопки на підлозі.
- (?) Дата: Steam і девлог — 04.03.2022; один агрегатор — 22.01.2022.
