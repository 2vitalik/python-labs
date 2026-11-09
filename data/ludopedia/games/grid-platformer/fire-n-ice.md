---
title: Fire 'n Ice
slug: fire-n-ice
aka: [Solomon's Key 2, "ソロモンの鍵2 クールミン島救出作戦", Soromon no Kagi 2]
family: grid-platformer
also: [push-slide]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 1992
platforms: [NES/Famicom, Nintendo Switch Online]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Solomon%27s_Key_2", best: true, note: "правила льоду: де створюється, ковзання, примерзання, гасіння, глеки, труби, підйом на 1; 100 етапів, паролі, редактор"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ソロモンの鍵_(ゲーム)", note: "JA: розділ про сиквел — лід замість блоків, менше екшену; дати"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Fire+n+Ice+NES+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-by-input, gravity-fall, inertia-slide, push-object, impassable-cells, cell-transform, destroy-all-enemies, sequential-levels, level-password, save-progress, in-game-editor, cheat-codes, game-screen, +create-destroy-block, +ice-sticks-to-wall, +extinguish-by-block, +step-climb-1, +burning-jar, +pipe-travel]
proposes: ["+card:ice-sticks-to-wall", "+card:extinguish-by-block", "+card:step-climb-1", "+card:pipe-travel", "+trigger:landed"]
author: opus
date: 2026-11-09
---

# Fire 'n Ice — маг без стрибка творить лід навскіс униз і гасить ним усі вогні етапу

## Суть
Сиквел-приквел Solomon's Key, де екшн замінено пазлом. Dana не стрибає: ходить, зіходить з уступів і вилазить лише на сходинку висотою 1. Єдина магія — **створити або прибрати крижаний блок у клітині навскіс униз ліворуч чи праворуч**. Лід штовхають — він **ковзає до упору або падає**; поставлений збоку від стіни, труби, глека чи іншого льоду — **примерзає** і висить. Етап пройдено, коли всі вогні загашено льодом, що в'їхав у них або впав згори.

## Поле і час
- Одноекранний етап-сітка, вигляд збоку, гравітація для Dana і вільного льоду.
- Real-time, але без таймера: час не тисне, гра — чистий пазл (?).
- Клітина: порожньо / камінь (стіна) / лід (вільний чи примерзлий) / вогонь / глек (холодний чи палаючий) / труба.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Dana | player | — | хід ліво/право; вилазить на блок висотою 1, якщо над ним порожньо; зіходить з уступу й падає |
| Камінь / стіна | static | — | непрохідний, нерухомий |
| Крижаний блок | object | вільний / примерзлий | створюється й прибирається магією; штовхнутий ковзає до упору; без опори падає |
| Вогонь (полумʼя) | enemy | — | гасне від льоду, що вʼїхав у нього або впав згори; усі загашені — перемога |
| Глек | terrain | холодний / палає | по холодному ходять; від дотику вогню спалахує; на палаючому стояти не можна, лід над ним тане |
| Труба | terrain | — | Dana пересувається крізь трубу; до труби лід примерзає |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(dana, dir)`; без опори — `fall(dana)`.
- КОЛИ `input(dir)` → ЯКЩО `not free(next)` і `free(above_next)` і `custom: «перешкода висотою 1»` → ТО `move(dana, up+dir)` — сходинка.
- КОЛИ `input(magic)` → ЯКЩО `free(diag_down_front)` → ТО `spawn_at(ice, diag_down_front)`; ЯКЩО `occupied(diag_down_front, ice)` → ТО `disappear_b`.
- КОЛИ `contact(dana, ice)` → ЯКЩО `not state(ice, frozen)` і `free(cell_behind)` → ТО `push(ice)`, `slide(ice, dir)`.
- КОЛИ `after(slide)` → ЯКЩО `free(below)` → ТО `fall(ice)`.
- КОЛИ `custom: «лід створено/зупинено збоку від стіни, труби, глека чи льоду»` → ТО `attach(ice, neighbor)`, `set_state(ice, frozen)` — висить без опори.
- КОЛИ `contact(ice, fire)` → ТО `disappear_both` — лід вʼїхав у вогонь або впав на нього згори (?: чи зникає лід).
- КОЛИ `contact(fire, jar)` → ТО `set_state(jar, burning)`.
- КОЛИ `enter(ice, cell)` → ЯКЩО `custom: «клітина над палаючим глеком»` → ТО `disappear_a`; Dana на палаючому глеку стояти не може.
- КОЛИ `enter(dana, pipe)` → ТО `custom: «пройти крізь трубу до іншого кінця»`.
- КОЛИ `all_gone(fire)` → ТО `win`, `next_level`.
- Перемога гри: 10 світів × 10 етапів і перемога над Druidle; далі — чит-код на звук-тест і 50 бонус-етапів. Поразка: глухий кут → перезапуск етапу (?). Рахунку нема (?).

## Керування і ввід
- Хрестовина ліво/право — хід (і поворот); підйом на сходинку — тим самим рухом.
- Кнопка магії — створити/прибрати лід навскіс униз у бік погляду.
- Штовхання — просто йти в лід.
- Меню паузи з перезапуском етапу (?).

## Вікна, меню, HUD
- `splash-screen` / `main-menu`: гра, продовжити (пароль), редактор (?).
- `game-screen`: етап + номер світу/етапу.
- `level-password` — у західних версіях вхід за паролем.
- `editor-window` — редактор етапів (зберігання лише в японській версії).
- `end-screen` етапу → наступний; фінал після Druidle.
- Переходи: меню → етап → (усі вогні) наступний етап → (кінець світу) наступний світ.

## Фічі поза полем
- `levels-sequential`: 10 світів по 10 етапів + 50 бонусних.
- Збереження: японська версія — батарейка (`autosave`), західна — паролі.
- `level-editor`: свої етапи; зберігаються лише в JP-версії.
- Чит-код після проходження (звук-тест, бонус-етапи).

## Варіації й родичі
- Solomon's Key (1986) — та сама ідея «створи/прибери блок», але з екшеном, стрибками, ключем і дверима.
- Kickle Cubicle — лід як снаряд і заморожування ворогів; Pengo, Pushover — ковзання й ланцюги.
- Осі: **де твориться блок** (попереду / навскіс униз / будь-де); **чим блок зупиняється** (стіна / падіння / примерзання до сусіда); **як гаситься ціль** (вʼїхати / впасти згори / обидва).

## Цікавинки для курсу
- Лід, що ковзає до упору й падає, коли під ним порожньо: `slide` + `fall` по черзі — 📎.
- Примерзання до сусіда: блок без опори не падає, якщо збоку стіна/лід — 🥉 (опора не лише знизу).
- Сходинка висотою 1 замість стрибка — 🌱.
- Глек, що спалахує від вогню й топить лід над собою, — ланцюг станів — 📎.
- Редактор етапів + паролі — 🥉.

## Мапа на каталог
- Є: `move-by-input` · `gravity-fall` · `inertia-slide` · `push-object` · `impassable-cells` · `cell-transform` (глек → палаючий) · `destroy-all-enemies` (вогні) · `sequential-levels` · `level-password` · `save-progress` · `in-game-editor` · `cheat-codes` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+ice-sticks-to-wall` «Блок примерзає до бічного сусіда й не падає» · entities/move · 🥉.
  - `+extinguish-by-block` «Блок гасить ціль ударом збоку чи згори» · entities/interact · 🌱.
  - `+step-climb-1` «Підйом на перешкоду висотою 1 без стрибка» · entities/move · 🌱 (Fire 'n Ice, Block Dude).
  - `+pipe-travel` «Прохід крізь трубу» · entities/move · 🌱.
  - `+create-destroy-block` — як у Solomon's Key, ціль — навскіс униз.

## Пропозиції до словників
- `+card:ice-sticks-to-wall`, `+card:extinguish-by-block`, `+card:step-climb-1`, `+card:pipe-travel` — див. вище.
- `+trigger:landed(a, floors)` — лід, що впав на вогонь (спільне з Space Panic, Prince of Persia).

## Джерела
- ⭐ [Wikipedia: Solomon's Key 2](https://en.wikipedia.org/wiki/Solomon%27s_Key_2) — магія навскіс униз, ковзання, примерзання до стіни/труби/глека/льоду, гасіння, глеки, труби, підйом на 1 блок; 10×10 етапів + 50 бонусних, батарейка/паролі, редактор.
- [Wikipedia JA: ソロモンの鍵 (ゲーム)](https://ja.wikipedia.org/wiki/ソロモンの鍵_(ゲーム)) — сиквел: лід замість блоків, менше екшену, задуманий як окрема гра.
- YouTube: пошук «Fire n Ice NES gameplay».

## Непевне
- (?) Чи зникає сам лід, коли гасить вогонь, і чи вбиває Dana дотик до вогню.
- (?) Чи можна штовхнути примерзлий лід і чи примерзає блок, що доковзав до стіни.
- (?) Рухомі вогні в пізніх світах, вороги-привиди — не підтверджено; таймера й очок, імовірно, нема.
- (?) Перезапуск етапу, карта світу, структура меню — з памʼяті, джерело не відкрилось (StrategyWiki, Giant Bomb — 403).
