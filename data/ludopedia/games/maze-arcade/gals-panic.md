---
title: Gals Panic
slug: gals-panic
aka: [Gal's Panic, Gals Panic II, Gals Panic S]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: runtime
  goal: territory
year: 1990
platforms: [arcade, Sega Saturn, PlayStation]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Gals_Panic", best: true, note: "Qix-подібна: 80 % силуету, бос не дає залити свою область, символи-бонуси, сиквели й різниця між ними"}
  - {kind: other, url: "https://www.arcade-history.com/game/922/", note: "4-way джойстик + кнопка, шкала «персонаж ↔ монстр», рулетка між раундами"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=gals+panic+arcade+gameplay", note: "пошук; геймплей (контент для дорослих)"}
stage: v1
coverage: 60
mechanics: [move-4dir, touch-death, player-death, time-out, sequential-levels, item-pickup, temporary-modes, event-points, chase-player, random-walk, +region-fill, +territory-capture, +trail-vulnerable, +percent-goal, +border-crawler, +mask-percent-goal, +balance-gauge, +between-round-roulette, +picture-reveal]
proposes: ["+effect:leave_trail", "+card:mask-percent-goal", "+card:balance-gauge", "+card:between-round-roulette", "+card:picture-reveal", "+ui:balance-gauge", "+window:roulette-window", "+cond:in_mask"]
author: opus
date: 2026-11-09
---

# Gals Panic — Qix, де рахується не площа, а силует: відкривай фігуру, але стеж за шкалою, що тягне до «монстра»

## Суть
Гравець-маркер, як у Qix (див. `xonix`), відрізає частини поля лінією від межі; залита область відкриває прихований малюнок. Ціль раунду — не % усього поля, а **80 % силуету** — затемненої фігури на тлі. Шкала вгорі балансує між «персонажем» і «монстром»: що більше відкриваєш силуету за раз, то сильніше вона зсувається до монстра, а відкриття тла (не силуету) повертає її назад. Завершиш раунд, коли на картинці монстр, — раунд повториться.

> Аркада з еротичним контентом (картинки-нагорода); у файлі описано лише механіку.

## Поле і час
- Прямокутне поле-картинка: тло + силует (маска клітин, що рахуються до цілі); незахоплене приховане, захоплене — відкрите.
- Маркер ходить межами захопленої території і своєю незамкненою лінією, як у Qix.
- Real-time з таймером раунду; шкала дрейфує до «монстра» з часом.
- Пізні ігри (Gals Panic S) — прокрутка екрана: поле більше за екран; деякі — різати назовні від внутрішнього прямокутника (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Маркер | player | життя | рух 4 напрямки по межі; кнопкою — лінія в незахоплене |
| Лінія (слід) | hazard | власник | вразлива, доки не замкнена; замкнена — заливка |
| Силует | zone | % відкритого | рахується до цілі 80 % |
| Тло поза силуетом | zone | — | можна захоплювати; не рахується до цілі, але повертає шкалу |
| Бос раунду | boss | вид за раундом | рухається в незахопленому; область з ним не заливається |
| Павук (бос раунду 1) | boss | — | стріляє павутиною, що сповільнює маркер; породжує павучат |
| Вогняна куля (бос раунду 2) | boss | — | вибухає полумʼям, що вбиває того, хто ріже лінію |
| Дрібні вороги | enemy | — | заважають (поведінка не описана) |
| Символ-бонус | pickup | вид | корисний: «астероїдний дощ» знищує ворогів; шкідливий: перетворює картинку на жабу чи восьминога |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `cell(target, border)` → ТО `move(marker, dir)`.
- КОЛИ `input(dir + button)` → ЯКЩО `cell(target, hidden)` → ТО `move(marker, dir)`, `custom: «лінія тягнеться за маркером»` (`+effect:leave_trail`).
- КОЛИ `enter(marker, border)` з лінією → ТО `fill(region)` для області без боса, `reveal(region)`, `score(area)`.
- КОЛИ `contact(boss|enemy, line|marker)` → ТО `lives(-1)`, лінія зникає (?).
- КОЛИ `contact(flame, marker)` → ЯКЩО `custom: «маркер ріже лінію»` → ТО `lives(-1)`.
- КОЛИ `contact(web, marker)` → ТО `speed(marker, -k)`.
- КОЛИ `timer(every)` (павук) → ТО `spawn(spiderling)`.
- КОЛИ `fill(region)` → ЯКЩО `custom: «відкрито великий шматок силуету»` → ТО `custom: «шкала зсувається до монстра»`.
- КОЛИ `fill(region)` → ЯКЩО `not custom: «область у силуеті»` (`+cond:in_mask`) → ТО `custom: «шкала зсувається до персонажа»`.
- КОЛИ `tick` → ТО `custom: «шкала повільно дрейфує до монстра»`; КОЛИ `custom: «шкала нижче позначки»` → ТО `transform(picture, monster)`.
- КОЛИ `counter(mask_revealed%, >=, 80)` → ЯКЩО `not state(picture, monster)` → ТО `next_level`; інакше `restart` раунду.
- КОЛИ `contact(marker, bonus_symbol)` → ТО `custom: «ефект символу»`: знищити ворогів / перетворити картинку.
- КОЛИ `level_end` → ТО `choose(roulette)`, `custom: «нагорода або штраф на наступний раунд»`.
- КОЛИ `timer(round)` вичерпано → ТО `lives(-1)` (?).
- Тактика: замкнути боса в області без силуету — тоді 100 % силуету відкривається без захоплення всього тла.
- Перемога: 80 % силуету за кожною картинкою · Поразка: 0 життів · Рахунок: площа (?).

## Керування і ввід
- Gals Panic: 4-напрямний джойстик + одна кнопка (різати лінію), до двох гравців.
- Gals Panic II: 8-напрямний джойстик.

## Вікна, меню, HUD
- `attract-demo` / `splash-screen` → «Push Start».
- `game-screen`: поле з силуетом; HUD — `score`, `lives`, `+ui:balance-gauge` (шкала персонаж ↔ монстр зі стрілкою-позначкою), % силуету (`territory-percent`), `timer-countdown` (?).
- `+window:roulette-window` — рулетка між раундами (нагорода/штраф).
- `custom-window` — повна картинка після раунду; версія EXPRO-02 — екран «100 % clear».
- `game-over-continue` (?), `end-screen`.
- Переходи: splash → game-screen → (80 %) показ картинки → рулетка → наступний раунд; (монстр) → повтор раунду.

## Фічі поза полем
- `levels-sequential`: кілька персонажів по кілька раундів; після трьох виграних раундів з одним — фото-версія картинки.
- `operator-settings`: 12 DIP-перемикачів (зміст не описано).
- Gals Panic II — Quiz Mode (питання від персонажа), Card Dispenser (видача карток), шкала стала часовою (?).
- Silhouette Stories (PS, 1996) — без еротики, із сюжетним режимом; Gals Panic S — прокрутка й сильніші боси.

## Варіації й родичі
- Qix (1981) і Xonix — див. `xonix`: ціль — % усього поля, тут — % маски.
- Volfied — бос визначає «зовнішній» бік, підсилення (теж у `xonix`).
- Сиквели: II (1993), 3 (1995), 4 (1996), SS (Saturn), S (1997), S2, Panic Street (1999), S3 (2002).
- Сучасні мобільні «відкрий картинку» — та сама ідея без шкали.
- **Осі варіацій:**
  - ціль: % поля / % маски-силуету;
  - тиск: таймер / шкала-баланс / обидва;
  - що вирішує «зовнішній» бік заливки: області без ворогів / де бос;
  - між раундами: нічого / рулетка-модифікатор.

## Цікавинки для курсу
- Ціль за маскою: рахувати відкриті клітини лише в силуеті — 🌱: другий шар поля з булевою маскою.
- Шкала-баланс, яку штовхають два протилежні джерела (дорогий хід і «безпечний» хід) — 📎: ризик vs швидкість.
- Тактика «запри боса в тлі» — 🥉: гравцеві треба зрозуміти, що бос визначає заливку.
- Рулетка-модифікатор наступного раунду — 🌱.
- Боси раунду з різною атакою (павутина сповільнює, полумʼя на лінії) — 📎.

## Мапа на каталог
- Є: `move-4dir` · `touch-death` · `player-death` · `time-out` · `sequential-levels` · `item-pickup` + `temporary-modes` (символи) · `event-points` · `chase-player` / `random-walk` (боси, поведінка непевна).
- **Нема** → пропозиції карток:
  - `+region-fill`, `+territory-capture`, `+trail-vulnerable`, `+percent-goal`, `+border-crawler` (запропоновано в `xonix`).
  - `+mask-percent-goal` «Ціль — % маски, а не поля» · game-logic/win · 🌱 · слот {percent, mask}.
  - `+balance-gauge` «Шкала-баланс між двома станами» · game-logic/lose · 📎.
  - `+between-round-roulette` «Рулетка модифікаторів між раундами» · levels/progression · 🌱.
  - `+picture-reveal` «Захоплене відкриває картинку» · interface/render · 🌱 (уже пропонували в Tentai Show — підтверджую).

## Пропозиції до словників
- `+effect:leave_trail` — підтверджую (Qix, Xonix, Paper.io).
- `+cond:in_mask` — клітина/область належить масці-цілі (силует).
- `+ui:balance-gauge` — шкала зі стрілкою між двома полюсами і позначкою порогу.
- `+window:roulette-window` — рулетка нагород/штрафів між раундами.
- `+card:mask-percent-goal`, `+card:balance-gauge`, `+card:between-round-roulette`, `+card:picture-reveal`.

## Джерела
- ⭐ [Wikipedia: Gals Panic](https://en.wikipedia.org/wiki/Gals_Panic) — Kaneko 1990, 80 % силуету, бос не дає залити свою область (100 % силуету без усього тла), павук і вогняна куля, символи-бонуси (астероїди, жаба/восьминіг), сиквели.
- [Arcade History: Gals Panic](https://www.arcade-history.com/game/922/) — 4-way джойстик і кнопка, 2 гравці, шкала персонаж ↔ монстр (дрейф, відкриття силуету й тла), повтор раунду, рулетка, фото після трьох раундів, 12 DIP.
- YouTube: пошук «gals panic arcade gameplay».

## Непевне
- (?) Боси павук і вогняна куля — з опису серії; чи це саме оригінал 1990 — не певно.
- (?) Часова шкала: Wikipedia — з Gals Panic II, пошуковий сніпет — з серії S.
- (?) Поведінка дрібних ворогів, наявність Sparx-подібних, кількість життів, очки — не знайдено.
- (?) Що стається з лінією при смерті, чи є таймер в оригіналі (Arcade History каже «within the time limit»).
- (?) «Різати назовні від внутрішнього прямокутника» — сніпет без певної гри серії.
