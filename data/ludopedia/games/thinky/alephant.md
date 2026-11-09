---
title: Alephant
slug: alephant
aka: []
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2023
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1823730/Alephant/", best: true, note: "опис ідеї (алеф + нікуд = звук), 3 кліпи механіки, відгуки"}
  - {kind: itch, url: "https://le-slo.itch.io/alephant", note: "GameMaker, клавіатура + Xbox-контролер; devlog 1.0.1"}
  - {kind: other, url: "https://steamcommunity.com/app/1823730/discussions/0/4629232886909852428/", note: "автор пояснює мету рівня і «побіління» пар"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=2960869232", note: "гайд-розвʼязки: структура розділів і назви рівнів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Alephant+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 35
mechanics: [move-4dir, move-by-input, keyboard-controls, controls-remap, push-object, stick-together, teleport, level-select, world-map, sound-effects, background-music, tutorial-window, achievements-window, +sound-trigger-tile, +pair-under-letter, +progress-recolor, +charges-per-item, +sequence-reproduce, +wordless-teaching]
proposes: ["+cond:below", "+cond:sequence_match", "+card:sound-trigger-tile", "+card:sequence-reproduce"]
author: opus
date: 2026-11-09
---

# Alephant — безмовна гра про мову: присунь огласовку під алеф, і він заговорить звуком, що діє на поле

## Суть
Sokoban-подібна головоломка Lucas Le Slo. Слоненя ходить по сітці з літерами **алеф** (א) і медальйонами **нікуда** — івритських огласовок камац, сеґол і хірік. Сам алеф «німий». Нікуд, поставлений під алеф, зʼєднується з ним, і пара отримує звук. Наступ на пару «вимовляє» звук, а кожен звук має власний ефект на полі: телепорт, дію на обертові символи тощо. Правила гра не пояснює словами: кожен світ приносить новий символ, і гравець сам розгадує, що той робить. Окремі рівні-«розмови» з волами вимагають відтворити почуту послідовність звуків.

## Поле і час
- Квадратна сітка-«рамка» неправильної форми; на полі клітини, алефи, медальйони нікуда. Вид згори.
- Покроково: хід = крок слоненяти; звук і його наслідки — у тому самому ході.
- Розділи: Aleph (латинські літери A–N), Kamatz (грецькі α–π), Segol (фінікійські), Hiriq (арабські), The Ox (івритські). У кожному близько 14–18 рівнів, загалом «80-odd». Рівні названо літерами алфавіту розділу.
- Прогрес між рівнями йде справа наліво, як письмо семітських мов (відгук).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Слоненя | player | — | рух 4 напрямки; штовхає символи; наступ на пару — «вимовити» звук |
| Алеф (א) | object | вільний / зʼєднаний; колір | вільний — стилізований «німий» гліф; зʼєднаний із нікудом — звичайна літера кольору пари |
| Камац (ָ) | object | колір | медальйон, що штовхається; під алефом утворює пару; звук пари рухає інші фігури на відстані (?) |
| Сеґол (ֶ) | object | напрям (вгору, діагональ…) | пара дає «варп» — переносить слоненя (?) у бік, куди дивиться сеґол; може повертатися |
| Хірік (ִ) | object | заряди | пара діє на інший символ, кожна дія витрачає заряд (?) |
| Пара алеф+нікуд | object | озвучена / ні | перший наступ → звук і пара біліє (мітка прогресу) |
| Вол | neutral | — | співрозмовник у рівнях-«розмовах»: каже послідовність звуків |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(elephant, dir)`.
- КОЛИ `contact(elephant, niqqud)` → ЯКЩО `free(cell_behind)` → ТО `push(niqqud)`; інакше `block`.
- КОЛИ `adjacent(niqqud, aleph)` → ЯКЩО `custom: «нікуд стоїть прямо під алефом»` (`+cond:below`) → ТО `attach(niqqud, aleph)`, `transform(aleph, voiced_aleph)`, `custom: «алеф бере колір нікуда»`.
- КОЛИ `enter(elephant, pair)` → ЯКЩО `first_time` → ТО `sound(vowel)`, `set_state(pair, white)`, `custom: «ефект звуку цього нікуда»`.
- КОЛИ `enter(elephant, pair)` → ЯКЩО `not first_time` і `custom: «звук нічого не змінить»` → ТО `custom: «тиша — звуку нема»`; звук лунає, лише коли щось зміниться.
- КОЛИ `custom: «звучить сеґол»` → ТО `teleport(elephant, …)` у бік сеґола до першої перешкоди (?).
- КОЛИ `custom: «звучить хірік»` → ЯКЩО `counter(hiriq_charges, >, 0)` → ТО `custom: «дія на сусідній символ»`, `counter(hiriq_charges, -1)` (?).
- КОЛИ `custom: «звук зачіпає обертовий символ»` → ТО `rotate(symbol, ±90|45)` (?).
- КОЛИ `custom: «кожен алеф зʼєднаний з нікудом і озвучений»` → ТО `win` (мету сформулював автор у Steam-обговоренні).
- КОЛИ `custom: «рівень-розмова: послідовність звуків збіглася з реплікою з «!»-бульбашки»` (`+cond:sequence_match`) → ТО `win`.
- Поразки й рахунку нема; глухий кут — рестарт або undo (?).

## Керування і ввід
- Клавіатура (WASD за замовчуванням) або Xbox-контролер; у меню є переназначення клавіш (автор у Steam-обговоренні).
- Окремої дії «сказати» нема: звук вимовляється наступом на пару.
- Катсцени «!» пропускаються утриманням будь-якої клавіші.

## Вікна, меню, HUD
- `game-screen`: поле в рамці, фон кольору розділу, у кутку — літера-назва рівня; HUD нема.
- `world-map` / `level-select`: хаб розділу, рівні рядами; щоб іти далі, досить пройти найлегший ряд.
- `dialogue-window`: розмова слоненяти з волом; репліка — бульбашка з алефом і нікудом.
- `custom-window` «!» — катсцена-розмова, яку можна пропустити утриманням клавіші.
- `settings-window`: переназначення клавіш; `achievements-window` (Steam).

## Фічі поза полем
- `levels-sequential` у межах ряду, `level-unlock` наступного розділу після найлегшого ряду; решта рівнів — опційні.
- `achievements`, `cloud-save` (Steam), `remap-controls`, `gamepad-support`, `localization` (EN, ES).
- Підказок у грі нема; гравці користуються гайдом-розвʼязками.

## Варіації й родичі
- Ранні безкоштовні сокобани Le Slo (Flockoban, Metamor[ρ]hosis на le-slo.itch.io) — найближчі «кузени» за відгуком.
- `games/thinky/all-the-gold-in-fort-locks.md` — пізніша спільна робота Le Slo (дизайн пазлів).
- `games/thinky/sokobond.md` — злипання символів у пару за правилом сусідства; тут пара утворюється лише вертикально.
- `games/thinky/baba-is-you.md` — правила як обʼєкти; тут правило дає звук пари, а не текст.
- **Осі варіацій:** що активує обʼєкт — дотик / пара / наступ на пару; навчання — текстом / безмовно (тут); мета — цілі під ящиками / озвучити все / відтворити послідовність.

## Цікавинки для курсу
- Зʼєднання «нікуд під алефом» як правило сусідства з напрямком — 📎.
- Клітина-тригер: перший наступ запускає ефект і перефарбовує пару в «готово» — 🌱.
- Звук лише тоді, коли він щось змінить (перевірка наслідку перед ефектом) — 🥉.
- Рівень-«розмова»: порівняти зіграну послідовність звуків з еталоном (Simon) — 📎.
- Хаб із рядами рівнів, де для просування досить найлегшого ряду — 🌱.

## Мапа на каталог
- Є: `move-4dir`, `move-by-input`, `keyboard-controls`, `controls-remap`; `push-object` ↔ медальйони нікуда; `stick-together` ↔ пара алеф+нікуд; `teleport` ↔ «варп» сеґола (?); `level-select`, `world-map` ↔ хаб; `sound-effects`, `background-music`; `tutorial-window` ↔ безмовні вступні рівні; `achievements-window`.
- **Нема** → пропозиції карток:
  - `+sound-trigger-tile` «Наступ на обʼєкт запускає ефект-звук» · entities/interact · 📎.
  - `+pair-under-letter` «Обʼєкт під обʼєктом утворює пару» · entities/interact · 📎.
  - `+progress-recolor` «Виконана частина цілі змінює колір» · interface/hud · 🌱.
  - `+charges-per-item` «Предмет із кількома зарядами» · entities/state · 🌱.
  - `+sequence-reproduce` «Відтворити почуту послідовність» · game-logic/win · 📎.
  - `+wordless-teaching` «Безмовне навчання рівнями» · support/docs · 🌱.

## Пропозиції до словників
- `+cond:below(a, b)` — A стоїть прямо під B (огласовка під літерою; опора знизу — окреме `supported`).
- `+cond:sequence_match(seq)` — зіграна послідовність дій або звуків збігається з еталоном (Alephant, Simon).
- `+card:sound-trigger-tile`, `+card:sequence-reproduce` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Alephant](https://store.steampowered.com/app/1823730/Alephant/) — «Aleph… combined with the niqqud… make a sound», «word-less game about language», реліз 1.03.2023; 3 кліпи (штовхання камаца під алеф, зміна кольору, розмова з волом); відгуки: камац/сеґол/хірік, воли, справа наліво, «telepathically control puzzle pieces», найлегший ряд.
- [Steam-обговорення: Significance of turning white](https://steamcommunity.com/app/1823730/discussions/0/4629232886909852428/) — автор: «connect every aleph to a niqqud and then step on every connected aleph».
- Steam-обговорення (π, Kaf, The Ox) — підказки автора: звук лише коли щось зміниться; «warp» від сеґола; «up-facing / diagonal segol»; «last hiriq charge»; рівні-розмови «!».
- [Гайд «Alephant Solutions»](https://steamcommunity.com/sharedfiles/filedetails/?id=2960869232) — розділи Aleph, Kamatz, Segol, Hiriq, The Ox і назви рівнів.
- [itch.io: Alephant](https://le-slo.itch.io/alephant) — GameMaker, контролер, devlog 1.0.1 («Segol Conversation Cutscene»).

## Непевне
- (?) Точні ефекти звуків: «варп» сеґола, витрата зарядів хіріка, «телепатичне» керування в камаці, обертання символів — відновлено з підказок у обговореннях і з кліпів, не з правил.
- (?) Чи штовхаються самі алефи, чи переміщуються лише звуками (гравець пише «put an aleph in the upper corridor»).
- (?) Чи є undo/рестарт і як влаштовано «розмову»: чи треба наступати на пари в потрібному порядку.
- (?) Зʼєднання саме «під» алефом — з кліпів і з того, як пишуть нікуд; в описі гри не сказано.
