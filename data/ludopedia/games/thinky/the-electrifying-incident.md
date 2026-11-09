---
title: "The Electrifying Incident: A Monster Mini-Expedition"
slug: the-electrifying-incident
aka: [The Electrifying Incident, A Monster Mini-Expedition]
family: thinky
also: [push-slide, connect-rotate]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2025
platforms: [PC, Mac]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3352300/The_Electrifying_Incident_A_Monster_MiniExpedition/", best: true, note: "опис: клешня-маніпулятор, електричні пастки, замкнені двері; 30–90 хв"}
  - {kind: other, url: "https://steamcommunity.com/app/3352300/reviews/?browsefilter=toprated&l=english", note: "відгуки гравців: вал клешні гнеться на кутах, ящик на плиті замикає коло, метал проводить струм, постгейм з реактором"}
  - {kind: other, url: "https://ladiesgamers.com/the-electrifying-incident-a-monster-mini-expedition-review/", note: "огляд: клешня огинає перешкоди, електрифіковані щілини, undo/reset, звʼязані кімнати"}
  - {kind: other, url: "https://godotengine.org/showcase/the-electrifying-incident-a-monster-miniexpedition/", note: "Godot Showcase: рушій, платформи, Steam і itch.io"}
  - {kind: other, url: "https://playtester.io/the-electrifying-incident-a-monster-mini-expedition", note: "підписи скріншотів: електрифіковані плитки, важіль"}
  - {kind: official, url: "https://www.draknek.org/games/", note: "список ігор Draknek & Friends"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=The+Electrifying+Incident+Monster+Mini-Expedition+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, pull-object, button-toggle, key-and-door, touch-death, environment-death, impassable-cells, undo-step, restart-level, keyboard-controls, +gamepad-controls, +grabber-arm-reach, +bendable-arm, +circuit-door, +conductive-tool, +interconnected-rooms]
proposes: ["+effect:grab", "+cond:powered", "+trigger:circuit_closed", "+cond:conductive", "+card:grabber-arm-reach", "+card:bendable-arm", "+card:circuit-door", "+card:conductive-tool", "+card:interconnected-rooms"]
author: opus
date: 2026-11-09
---

# The Electrifying Incident — монстр не штовхає, а тягає ящики гнучкою металевою клешнею крізь електричну лабораторію

## Суть
Мініпродовження [A Monster's Expedition](a-monsters-expedition.md) від Draknek & Friends: той самий монстр, але замість островів і колод — реактор інопланетної станції. Новина одна й центральна: ящики не штовхають тілом, а **хапають здалеку** механічною клешнею, чий вал гнеться на кутах і огинає стовпи. Друга вісь — **електрика**: ящик на плиті замикає коло й відчиняє двері, а живий струм у ящиках і плитках убиває, причому металева клешня його проводить. Пише лише нове відносно Expedition — правила колод/плотів тут не діють.

## Поле і час
- Квадратна сітка кімнат-пазлів станції; кімнати зʼєднані між собою, ящики часто переносять з однієї в іншу. Мапи нема (гравці скаржаться).
- Шари клітини: підлога (звичайна / живий контур / щілина під струмом) + обʼєкт (ящик, стовп, двері, плита, важіль).
- Покроково, тік = ввід; анімація монстра «похитується» при поворотах, тому огляд пише «не строго сітка» (?).
- Сюжетний «таймер» розплавлення реактора — лише антураж, реального відліку не описано.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Монстр | player | — | крок 4 напрямки; гине від дотику до струму |
| Клешня-маніпулятор | object | вал з вигинами | видовжується від монстра до ящика й тримає його; вал згинається на кутах і тримає форму, огинаючи стовпи (?) |
| Ящик | object | звичайний | його хапають, тягнуть і переносять клешнею; на плиті замикає коло |
| Електрифікований ящик | hazard | під струмом | дотик тілом — смерть; схопити клешнею — струм іде металом до монстра |
| Плита контакту | switch | — | ящик на ній замикає коло → струм іде до дверей |
| Двері | gate | закриті / відчинені | відчиняються, коли їхнє коло під струмом |
| Живий контур (плитки) | hazard | під струмом, коли коло замкнене (?) | пройти ним — смерть |
| Щілина під струмом | hazard | частково електрифікована | ящик через неї переносять клешнею |
| Стовп / лампа | static | — | об нього огинається вал клешні — так будують кутові траєкторії |
| Важіль | switch | — | перемикає щось у кімнаті (?) |
| Реактор | static | фінал | постгейм: перезапустити безпечно, замкнувши коло з одним ящиком |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell_ahead)` → ТО `move(monster, dir)`; інакше `block`.
- КОЛИ `input(grab)` → ЯКЩО `line_of_sight(monster, box)` → ТО `custom: «клешня видовжується до ящика й хапає його»` (кілька клітин відстані).
- КОЛИ `input(dir)` → ЯКЩО `has(monster, held_box)` → ТО `pull(box)` / `custom: «ящик рухається разом з клешнею; на куті вал згинається й тримає форму»`.
- КОЛИ `contact(arm, pillar)` → ТО `custom: «вал огинає стовп — далі ящик іде вже під кутом»`.
- КОЛИ `contact(box, plate)` → ТО `set_state(door, open)`, `custom: «коло замкнене, струм іде до дверей»`.
- КОЛИ `leave(box, plate)` → ТО `clear_state(door, open)` (?).
- КОЛИ `contact(monster, electric_box)` → ТО `lose`, `custom: «монстра вдаряє струмом»`.
- КОЛИ `input(grab)` → ЯКЩО `state(box, electrified)` → ТО `lose` — метал клешні проводить струм.
- КОЛИ `enter(monster, live_circuit)` → ТО `lose`.
- КОЛИ `input(lever)` → ТО `custom: «перемкнути стан пристрою кімнати»` (?).
- КОЛИ `input(undo)` → ТО `undo(1)`; КОЛИ `input(reset)` → ТО `restart` поточного пазла.
- КОЛИ `reach(monster, reactor_room)` → ТО `win` сюжету; постгейм: КОЛИ `custom: «коло реактора замкнене одним ящиком»` → ТО `custom: «безпечний перезапуск, фінальне досягнення»`.
- Перемога: дійти до реактора; мета-ціль — безпечно його перезапустити. Поразка: удар струмом (знімається undo/reset). Рахунку нема.

## Керування і ввід
- Стік/стрілки — рух; кнопка — схопити/відпустити ящик клешнею (одна кнопка).
- Undo (крок пазла назад) і Reset (з початку пазла) — з екранними підказками; повна підтримка геймпада й Steam Deck.

## Вікна, меню, HUD
- `main-menu` → `game-screen` (кімната, підказки кнопок undo/reset як `undo-button`, `restart-button`); `pause-menu` з налаштуваннями (`settings-window`) (?).
- `map-window` — **нема** (критика гравців).
- `end-screen` — титри після реактора; досягнення Steam (`achievements-window` платформи).

## Фічі поза полем
- `undo` (покроковий, гравці називають його «дивним»), `restart-level` для кімнати.
- Звʼязані кімнати замість списку рівнів; ящики переносяться між пазлами — можна потрапити в нерозвʼязний стан, не помітивши.
- `achievements` — фінальне досягнення за безпечний перезапуск реактора працює як мета-пазл.
- `gamepad-support`, Steam Deck.

## Варіації й родичі
- Пряма гілка: [a-monsters-expedition](a-monsters-expedition.md) (той самий монстр, колоди й плоти), [a-good-snowman-is-hard-to-build](a-good-snowman-is-hard-to-build.md); родичі за «інструментом-продовжувачем»: Hook (лінії-гаки), Pushmo/Stretchmo (тягнення), [linelith](linelith.md) (маршрут лінією).
- Електрика як двері: Portal-подібні плити + двері, Chip's Challenge (кнопки й двері), Sokoban-пазли з «плитою під ящиком».
- **Осі варіацій**: як гравець рухає ящик — тілом (штовх) / тягне за собою / дистанційно хапає; інструмент — прямий / гнучкий з вигинами на кутах; що дає ящик на плиті — двері / струм у контур / шкода гравцю.

## Цікавинки для курсу
- Клешня, що хапає ящик на відстані по прямій лінії — 📎 (line_of_sight + привʼязка).
- Гнучкий вал із вигинами: траєкторія ящика як ламана навколо стовпів, яка тримає форму — 🥈 (геометрія ланцюга точок вигину).
- Ящик на плиті замикає електричне коло → двері — 🥉 (граф контура, flood fill струму).
- Провідний інструмент: схопити ящик під струмом = смерть — 📎 (умова на матеріал).
- Звʼязані кімнати з перенесенням ящиків між пазлами — 🥉 (спільний стан світу, ризик нерозвʼязності).

## Мапа на каталог
- Є: `move-4dir` · `pull-object` (тягнення клешнею) · `button-toggle` (плита → двері) · `key-and-door` · `touch-death` (струм) · `environment-death` (живі плитки) · `impassable-cells` · `undo-step` · `restart-level` · `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+grabber-arm-reach` «Хапання обʼєкта на відстані» · entities/interact · 📎.
  - `+bendable-arm` «Гнучкий інструмент з вигинами на кутах» · entities/move · 🥈.
  - `+circuit-door` «Ящик на плиті замикає коло, струм відчиняє двері» · entities/interact · 🥉.
  - `+conductive-tool` «Інструмент проводить шкоду (струм) до гравця» · entities/death · 📎.
  - `+interconnected-rooms` «Кімнати-пазли з переносом обʼєктів між ними» · levels/progression · 🥉.

## Пропозиції до словників
- `+effect:grab` — схопити обʼєкт на відстані й тримати (є як кандидат з Cargo-Bot ×3 — тут клешня).
- `+cond:powered` — клітина/обʼєкт під струмом (кандидат з Galaxy Trucker, Duskers).
- `+cond:conductive` — обʼєкт/інструмент проводить струм (кандидат з Caves of Qud).
- `+trigger:circuit_closed` — коло замкнулось (кандидат з Hook; тут — ящиком на плиті).
- Карткові пропозиції — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam](https://store.steampowered.com/app/3352300/The_Electrifying_Incident_A_Monster_MiniExpedition/) — опис: клешня «lift and move boxes from afar», електричні пастки, замкнені двері, 15.04.2025, Windows/macOS.
- [Відгуки Steam](https://steamcommunity.com/app/3352300/reviews/?browsefilter=toprated&l=english) — хапання за кілька клітин, вигин вала на краях, плита замикає коло, метал проводить струм, нема мапи, постгейм з одним ящиком біля реактора.
- [LadiesGamers](https://ladiesgamers.com/the-electrifying-incident-a-monster-mini-expedition-review/) — вал огинає перешкоди (лампу), «zipper»-перенос через щілину, undo/reset, звʼязані кімнати.
- [Godot Showcase](https://godotengine.org/showcase/the-electrifying-incident-a-monster-miniexpedition/) · [playtester.io](https://playtester.io/the-electrifying-incident-a-monster-mini-expedition) — платформи, підписи скріншотів (важіль, живі плитки).

## Непевне
- (?) Точна механіка клешні: максимальна дальність, чи тягне ящик лише до себе, чи може штовхати ним від себе, як саме фіксуються вигини.
- (?) Чи живі плитки під струмом завжди чи лише коли коло замкнене; що робить важіль.
- (?) Чи двері зачиняються, коли ящик знято з плити.
- (?) Сітка: огляд LadiesGamers каже «не строго сітка», інші описують Sokoban-кімнати — ймовірно, логіка клітинна, а рух лише анімований.
- (?) Кількість пазлів не опубліковано; час — 30–90 хв (Steam), ~1 год (LadiesGamers), до 2 год (Digital Chumps за пошуковим переказом).
- Thinky Games і Digital Chumps віддали 403 — їхні описи (плити від блоків, удар струмом крізь клешню) відомі лише з переказу пошуку.
