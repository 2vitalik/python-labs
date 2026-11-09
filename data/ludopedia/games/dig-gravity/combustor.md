---
title: Combustor
slug: combustor
aka: []
family: dig-gravity
also: [build-sim]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: none
year: 2026
platforms: [PC (Windows)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/5047230/Combustor/", best: true, note: "опис: клітина тримає всі гази + T, p; займання від 700 K при 300 K довкола; полумʼя гасне у відкритому повітрі; режими Species/Pressure/Temperature/Velocity/Reactions; графіки метрик"}
  - {kind: steam, url: "https://store.steampowered.com/app/5348040", note: "демо (окремий app); у пошуковому сніпеті — реакції й Chem Codex"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Combustor+gas+simulator", note: "пошук; геймплей"}
stage: v1
coverage: 35
mechanics: [in-game-editor, editor-palette, +gas-diffusion, +pressure-field, +temperature-field, +heat-diffusion, +view-modes, +reaction-table, +ignition-threshold, +feed-rate-source, +metric-charts]
proposes: ["+cond:temp", "+cond:pressure", "+effect:ignite", "+effect:react", "+effect:diffuse", "+role:material", "+role:field", "+ui:view-mode-toggle", "+ui:metric-chart", "+card:ignition-threshold", "+card:feed-rate-source", "+card:metric-charts"]
author: opus
date: 2026-11-09
---

# Combustor — малюй стіни, змішуй гази, давай іскру: клітинна газодинаміка з порогом займання

## Суть
Двовимірний симулятор газів: гравець малює конструкцію (стіни), напускає гази, підпалює іскрою й дивиться, як вона працює — від стабільного пальника до реактивного двигуна чи вибуху. На відміну від falling-sand ігор (Noita, The Powder Toy), клітина тут не «одна частинка», а **суміш усіх газів** із температурою, тиском і швидкістю. Головна механіка — займання: паливо поруч з окисником саме не горить; потрібне джерело запалювання і суміш, достатньо щільна, щоб утримати тепло. Мета задана слоганом: «збудуй найкращий реактивний двигун, розвʼяжи пазли або просто все підірви».

## Поле і час
- Квадратна сітка клітин (Euler-сітка, а не частинки); у кожній клітині — частки кожного газу, температура, тиск, швидкість (і «інші властивості»).
- Real-time симуляція; довкілля — повітря 300 K.
- Шари відображення одного стану: Species, Pressure, Temperature, Velocity, Reactions.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина газу | field | частки газів, T, p, v | обмінюється газом, теплом, імпульсом із сусідами |
| Стіна | static | — | малюється; непроникна для газу; замикає полумʼя |
| Паливо | material | частка в клітині | горить з окисником при T ≥ 700 K |
| Окисник | material | частка в клітині | потрібен для горіння |
| Продукти горіння | material | — | утворюються реакцією (?) |
| Іскра | source | — | джерело запалювання: локально нагріває суміш |
| Подача газу | source | швидкість подачі (feed rate) | безперервно напускає газ (?) |
| Повітря довкілля | field | 300 K | тло, куди втрачається тепло |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(paint, wall)` → ТО `set_cell(cell, wall)`.
- КОЛИ `input(paint, gas)` → ТО `custom: «додати газ у клітини під пензлем»`.
- КОЛИ `input(spark, cell)` → ТО `custom: «нагріти клітини іскрою»`.
- КОЛИ `tick` → ТО `custom: «гази дифундують і переносяться полем швидкостей; тиск вирівнюється»`.
- КОЛИ `tick` → ТО `custom: «теплообмін між сусідніми клітинами й довкіллям 300 K»` (?).
- КОЛИ `tick` → ЯКЩО `custom: «у клітині є паливо й окисник»` і `custom: «T ≥ 700 K»` → ТО `custom: «реакція: паливо + окисник → продукти + тепло»`.
- КОЛИ `tick` → ЯКЩО `custom: «паливо й окисник поруч, але T < 700 K»` → ТО нічого — `custom: «самозаймання нема»`.
- КОЛИ `tick` → ЯКЩО `custom: «тепловтрати більші за тепло реакції (тонкий струмінь у відкритому повітрі)»` → ТО `custom: «T падає нижче порогу — полумʼя гасне»`.
- КОЛИ `tick` → ЯКЩО `custom: «полумʼя замкнене стінами або подача більша»` → ТО `custom: «полумʼя самопідтримується й гріється»`.
- КОЛИ `timer(every)` → ТО `spawn_at(gas, feed)` — подача газу з заданою швидкістю (?).
- КОЛИ `input(view, x)` → ТО `custom: «перемкнути шар відображення: Species / Pressure / Temperature / Velocity / Reactions»`.
- Перемога: у пісочниці нема; пазли й «двигун» — (?) · Поразка: — · Рахунок: метрики конструкції на графіках (тяга?) (?).

## Керування і ввід
- Мишею малюєш стіни й гази, ставиш іскру (`control: click-cell`/пензель); перемикач шару відображення; панель графіків.
- Конкретні клавіші — (?).

## Вікна, меню, HUD
- `game-screen`: полотно симуляції + палітра (стіна, гази, іскра) + `view-mode-toggle` (5 шарів) + `metric-chart` (графіки метрик).
- `codex-window` — Chem Codex з умовами реакцій (?) (лише пошуковий сніпет).
- `puzzle-select` — пазли (?); `main-menu`, `settings-window` — (?).

## Фічі поза полем
- `mode-sandbox` (малюй і дивись) + пазли (?) + «двигун» як інженерна ціль (?).
- `achievements` — Steam; аналітика конструкції — графіки метрик для доведення дизайну.

## Варіації й родичі
- У сімʼї: [the-powder-toy](the-powder-toy.md) (частинки + поля тиску й температури), [noita](noita.md), [sandboxels](sandboxels.md), [sandspiel](sandspiel.md) — усі на моделі «одна частинка на клітину», від якої Combustor свідомо відмовляється.
- Поза сімʼєю: [oxygen-not-included-cells](../build-sim/oxygen-not-included-cells.md) — один газ на клітину з масою й температурою.
- **Осі варіацій** клітинної фізики: клітина = частинка (falling sand) / клітина = маса одного газу (ONI) / клітина = суміш усіх газів + T, p, v (Combustor); займання — від сусіда-вогню (TPT) / за порогом температури суміші (Combustor).

## Цікавинки для курсу
- Клітина як вектор концентрацій + дифузія між сусідами — 🥈.
- Поріг займання + баланс «тепло реакції проти тепловтрат»: полумʼя живе лише в замкненому обʼємі або при сильній подачі — 🥇.
- Поле тиску й швидкостей (адвекція газу) — 👑 (по суті CFD на сітці).
- Перемикач шарів відображення одного стану (вид / тиск / температура / швидкість / реакції) — 📎.
- Графіки метрик конструкції в реальному часі — 🥉.

## Мапа на каталог
- Є: `in-game-editor` ↔ малювання конструкції · `editor-palette` ↔ стіна / газ / іскра.
- Повтори з корпусу: `+gas-diffusion` · `+pressure-field` · `+temperature-field` · `+heat-diffusion` (?) · `+view-modes` · `+reaction-table` (?).
- **Нема** → пропозиції карток:
  - `+ignition-threshold` «Займання від порогу температури суміші» · entities/state · 🥈 · слоти {t_ignite: 700, needs: [fuel, oxidizer]}.
  - `+feed-rate-source` «Джерело з регульованою швидкістю подачі» · entities/spawn · 📎 · слот {rate}.
  - `+metric-charts` «Живі графіки метрик симуляції» · interface/hud · 🥉.

## Пропозиції до словників
- `+cond:temp` і `+cond:pressure` — порівняння температури / тиску клітини з порогом (повтор TPT).
- `+effect:ignite` — підпал (повтор Noita); `+effect:react` — реакція в клітині: реагенти → продукти + тепло; `+effect:diffuse` — обмін із сусідами (повтор TPT).
- `+role:material` — речовина в клітині (повтор TPT/Noita); `+role:field` — поле стану на сітці (повтор TPT).
- `+ui:view-mode-toggle` — перемикач шару відображення; `+ui:metric-chart` — живий графік метрики.
- `+card:ignition-threshold`, `+card:feed-rate-source`, `+card:metric-charts` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Combustor](https://store.steampowered.com/app/5047230/Combustor/) — увесь опис механіки: не falling sand; клітина з усіма газами, T, p; стіни, суміш, іскра; 700 K / 300 K; тонкий струмінь гасне, стіни або подача рятують; 5 режимів відображення; графіки; Szymon Aniola, 10.11.2026.
- [Steam: демо (app 5348040)](https://store.steampowered.com/app/5348040) — окремий app демо.
- YouTube: пошук «Combustor gas simulator».

## Непевне
- (?) Пошуковий сніпет сторінки демо називає реакції Combustion, Aether Condensation, Shock Detonation, Rift Cascade, Vitrium Cracking і внутрішній довідник Chem Codex; на фетчі сторінки цього не видно.
- (?) Які саме гази, чи є впускні й випускні отвори (подача газу виведена з фрази «raise the feed rate»), чи теплообмін моделюється окремо.
- (?) Структура пазлів і як міряється «двигун» (тяга? ККД?) — не описано.
- (?) Дата: Steam — 10.11.2026; пошуковий сніпет — жовтень 2026.
