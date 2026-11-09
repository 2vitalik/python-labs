---
title: Block Dude
slug: block-dude
aka: [Blockdude, Block-Man (DOS-попередник)]
family: grid-platformer
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2000
platforms: [TI-83, TI-89, TI-Nspire, Playdate, PC, web]
links:
  - {kind: itch, url: "https://joyrider3774.itch.io/blockdude-playdate", best: true, note: "сучасний порт: правила, керування, 25 рівнів Block-Man, редактор, автосейв; грати в браузері"}
  - {kind: other, url: "https://www.ticalc.org/archives/files/fileinfo/93/9343.html", note: "оригінал Brandon Sterner, TI-83 (Ion), 22.01.2000; відгук про паролі з 3 символів"}
  - {kind: other, url: "https://github.com/mitch3b/BlockDude", note: "порт: «бере й кладе один блок, лізе на один блок»"}
  - {kind: other, url: "https://gist.github.com/straker/df855f22e57576c80d6126aa5609654e", note: "мінімальна реалізація JS: умови взяти/покласти, підйом, падіння"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Block+Dude+TI-83+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [move-by-input, gravity-fall, impassable-cells, reach-exit, sequential-levels, level-password, level-select, in-game-editor, save-autosave, player-camera, keyboard-controls, +carry-one-block, +step-climb-1, +place-block]
proposes: ["+effect:climb", "+card:carry-one-block", "+card:step-climb-1"]
author: opus
date: 2026-11-09
---

# Block Dude — чоловічок носить на голові один блок і будує сходинки висотою 1 до дверей

## Суть
Калькуляторна класика TI-83: вид збоку, цегляні стіни, вільні блоки й двері. Герой ходить ліворуч-праворуч, **вилазить лише на перешкоду висотою 1** і **несе над головою не більше одного блока**, який може покласти перед собою. Рівень — у тому, щоб зі скупого набору блоків скласти сходи до дверей, часто розбираючи й переносячи вже збудоване. Покроковий пазл без ворогів і без часу.

## Поле і час
- Сітка клітин, вид збоку; рівень ширший за екран калькулятора — камера йде за героєм (?).
- Гравітація: герой і покладений блок падають до першої опори; падіння безпечне.
- Тік = одне натискання; світ стоїть, доки гравець не діє.
- Клітина: порожньо / стіна-цегла / блок / двері.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Block Dude | player | напрям погляду; несе 0/1 блок | крок ліво/право; підйом на 1; бере/кладе блок перед собою |
| Стіна (цегла) | static | — | непрохідна, нерухома; на неї лізуть і кладуть блоки |
| Блок | object | лежить / несеться | береться, якщо зверху порожньо; несеться над головою; кладеться перед собою й падає |
| Двері | static | — | вхід = рівень пройдено |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `not facing(dude, dir)` → ТО `face(dude, dir)`; інакше ЯКЩО `free(next)` → ТО `move(dude, dir)`, `fall(dude)`.
- КОЛИ `input(up)` → ЯКЩО `not free(front)` і `free(above_front)` і `free(above_dude)` → ТО `custom: «вилізти на клітину над перешкодою»` — лише на висоту 1.
- КОЛИ `input(down)` → ЯКЩО `not has(dude, block)` і `occupied(front, block)` і `free(above_front)` → ТО `pickup`, `custom: «блок над головою»`.
- КОЛИ `input(down)` → ЯКЩО `has(dude, block)` і `free(front)` → ТО `place(block, front)`, `fall(block)`.
- КОЛИ `input(down)` → ЯКЩО `has(dude, block)` і `not free(front)` і `free(above_front)` → ТО `place(block, above_front)` — на перешкоду попереду.
- КОЛИ `custom: «блок над головою впирається у стелю»` → ТО `block` — з блоком не пройти під низькою стелею (?).
- КОЛИ `enter(dude, door)` → ТО `win`, `next_level`, `message(password)`.
- Перемога: дійти до дверей. Поразки нема — глухий кут лікується перезапуском рівня (?). Рахунку нема.

## Керування і ввід
- TI-83: ←/→ — поворот і крок, ↑ — вилізти, ↓ — взяти/покласти блок (рецензент скаржився, що підйом окремою клавішею незручний).
- Порт Playdate/PC: підйом автоматичний при русі в перешкоду висотою 1; X / A — взяти або покласти.
- Ввід покроковий: одна клавіша — одна дія.

## Вікна, меню, HUD
- `splash-screen` / `main-menu`: Грати, Пароль (?).
- `level-password` — вхід на рівень за паролем із 3 символів.
- `game-screen`: поле + номер рівня.
- `end-screen` рівня — показ пароля наступного.
- Порт Playdate: `level-select`, `editor-window` (пакети рівнів), `settings-window` (скіни, інверсія, розмір тексту), режим «freeview» — огляд рівня.
- Переходи: меню → рівень → (двері) пароль → наступний рівень.

## Фічі поза полем
- `levels-sequential` + `level-password` (TI-83) — повернутись до будь-якого пройденого рівня.
- Порти: `level-select`, `autosave`, `level-editor` з обміном пакетами (zip), `theme-select` (5 скінів).
- `restart-level` (?) — у порту з gist нема; в оригіналі — ймовірно.
- Undo нема в жодному відкритому джерелі.

## Варіації й родичі
- Block-Man (Soleau Software, DOS) — та сама ідея; автор порту пише, що невідомо, хто був першим.
- Порти й фан-сиквели: TI-89, Nspire, Block Dude: The Sands of Time (xLIB), Playdate, microStudio, Vircon32.
- Родичі: Catrap, Boxboy (власні блоки), Fire 'n Ice (сходинка 1 без стрибка), Toki Tori.
- Осі: **скільки блоків несеш** (1 / стек); **підйом** (клавіша / автоматично); **куди кладеш** (попереду з падінням / на перешкоду).

## Цікавинки для курсу
- Носіння одного блока над головою — стан аватара `carrying` + колізія блока зі стелею — 🌱.
- Підйом на 1 як єдиний «стрибок» — 🌱.
- Покласти блок перед собою з падінням до опори або на перешкоду — 📎.
- Паролі з 3 символів як збереження прогресу — 🌱.
- Солвер BFS по станам (позиція, погляд, блоки) — 🥇.

## Мапа на каталог
- Є: `move-by-input` · `gravity-fall` · `impassable-cells` · `reach-exit` · `sequential-levels` · `level-password` · `level-select` · `in-game-editor` · `save-autosave` (порт) · `player-camera` · `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+carry-one-block` «Нести один блок над головою і класти перед собою» · entities/interact · 📎.
  - `+step-climb-1` «Підйом на перешкоду висотою 1» · entities/move · 🌱 (також Fire 'n Ice).
  - `+place-block` — як у Toki Tori.

## Пропозиції до словників
- `+effect:climb(a, dir)` — піднятися на клітину над перешкодою (Block Dude, Fire 'n Ice; відмінне від `move` і від драбини).
- `+card:carry-one-block`, `+card:step-climb-1` — див. вище.

## Джерела
- ⭐ [itch.io: Blockdude (Playdate + PC)](https://joyrider3774.itch.io/blockdude-playdate) — правила, керування, 25 рівнів (21 з Block-Man), редактор, автосейв, кредити Sterner і Soleau.
- [ticalc.org: Block Dude (TI-83)](https://www.ticalc.org/archives/files/fileinfo/93/9343.html) — автор, дата 22.01.2000, Ion; відгук: паролі, «поклади блок, щоб узяти інший».
- [GitHub: mitch3b/BlockDude](https://github.com/mitch3b/BlockDude) — опис здібностей героя.
- [Gist: straker Block Dude](https://gist.github.com/straker/df855f22e57576c80d6126aa5609654e) — код правил: взяти лише блок без нічого зверху, покласти з падінням чи на перешкоду.
- YouTube: пошук «Block Dude TI-83 gameplay».

## Непевне
- (?) Рік: 2000 — дата завантаження на ticalc.org; можливі ранніші BASIC-версії ~1999.
- (?) Кількість рівнів оригіналу TI-83 (за памʼяттю ~11) не підтверджено.
- (?) Чи блокує стеля рух із блоком і підйом із блоком; чи можна взяти блок, коли над головою стіна.
- (?) Перезапуск рівня і камера-скрол в оригіналі.
