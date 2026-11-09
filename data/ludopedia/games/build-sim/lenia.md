---
title: Lenia
slug: lenia
aka: [Ленія, continuous Game of Life, неперервне «Життя»]
family: build-sim
also: []
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: setup
  goal: none
year: 2018
platforms: [web, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Lenia", best: true, note: "формули: ядро, функція росту, крок, Life як окремий випадок"}
  - {kind: official, url: "https://chakazul.github.io/lenia.html", note: "сторінка автора: таймлайн, Orbium, 3D/4D, багатоканальна версія, статті"}
  - {kind: play, url: "https://chakazul.github.io/Lenia/JavaScript/Lenia.html", note: "грати в браузері: JS-версія v1.3 з бібліотекою форм і графіками"}
  - {kind: play, url: "https://chakazul.github.io/Lenia/WebGL/", note: "WebGL-демо"}
  - {kind: other, url: "https://github.com/Chakazul/Lenia", note: "код: Python, R, Jupyter, Matlab, JavaScript"}
  - {kind: other, url: "https://colab.research.google.com/github/OpenLenia/Lenia-Tutorial/blob/main/Tutorial_From_Conway_to_Lenia.ipynb", note: "туторіал «From Conway to Lenia» (Colab)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=lenia+cellular+automata", note: "пошук; відео істот"}
stage: v1
coverage: 55
mechanics: [cell-click, game-loop, game-pause, state-as-data, rule-variants, field-scaling, field-size-picker, wrap-edges, gui-render, logic-render-split, theme-select, +cellular-automaton-rule, +continuous-cell-state, +convolution-kernel, +growth-function, +step-run-speed, +pattern-library, +random-soup, +fft-convolution, +pattern-stats, +gif-export]
proposes: ["+cond:kernel_sum", "+effect:add_value", "+ui:kernel-graph", "+ui:growth-graph", "+ui:param-slider", "+ui:stats-plot", "+window:species-library", "+feature:gif-export", "+axis:states=continuous", "+axis:neighbourhood=kernel", "+card:convolution-kernel", "+card:continuous-cell-state"]
author: opus
date: 2026-11-09
---

# Lenia — «Життя» з неперервними станами: клітина — число 0…1, сусідство — кільце-ядро радіуса R, а з нього повзають «організми»

## Суть
Узагальнення клітинних автоматів (Bert Wang-Chak Chan): замість двох станів — значення в [0,1], замість 8 сусідів — зважена сума по кругу радіуса R (ядро-кільце), замість таблиці B/S — гладка функція росту G з параметрами μ, σ. Крок — додати `Δt·G(K∗A)` і обрізати до [0,1]. Гравець, як і в Life, не грає, а ставить початковий стан (форму з бібліотеки або випадкову «суп»), крутить параметри й дивиться, що виживе. Ядро для курсу — **межа клітинності**: поле досі сітка, але правило вже «фізика» (згортка), і Life (`game-of-life.md`) — лише точка в просторі параметрів.

## Поле і час
- Квадратна ґратка (у JS-версії — розмір поля в клітинах і пікселях на клітину). Межі — тор (згортка через FFT природно циклічна) (?).
- Стан клітини — дійсне число; дискретна версія має `P` рівнів з кроком `1/P` (P = 4 → {0, .25, .5, .75, 1}).
- Сусідство — куля радіуса `R` (евклідова норма, може включати центр); `R` — «кількість клітин на радіус ядра», тож та сама істота існує в різних роздільностях.
- Тік — `Δt = 1/T`; `T` — кроків на одиницю часу. Усі клітини оновлюються синхронно з повного старого стану.
- Розширення автора: 3D/4D (2019-12), N-вимірне (2020-01), кілька ядер (2020-01, самовідтворення), кілька каналів (2020-02, агрегати).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина | tile | значення A ∈ [0,1] | щотіку отримує `Δt·G(U)` і обрізається до [0,1] |
| Ядро K | static | R, ранг B, піки β, форма ядра KC | нормоване (сума 1) кільце/кільця ваг; дає потенціал `U = K∗A` |
| Функція росту G | static | μ, σ, форма (експонента, поліном, прямокутник) | однопікова: G(U) ∈ [-1,1], +1 при U = μ, падає з відстанню |
| Порожнеча | terrain | A = 0 | нульові клітини навколо істоти; ростуть, лише якщо U поряд потрапляє у вікно μ±σ |
| Організм (Orbium, Scutium, Gyropteron…) | object | вид, швидкість, період | емерджентна стійка пляма; рухається, обертається, самовідновлюється |
| «Суп» | spawner | щільність, область | випадкові значення в області — генератор кандидатів |

Організми — не сутності двіжка, а стійкі патерни, як глайдери в Life; автор описує 400+ «видів» і таксономію (ряди Orbiformes, Scutiformes, Pterifera, Heliciformes…).

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `custom: «U(x) = Σ K(n)·A(x+n) по кулі радіуса R; K = KS(‖n‖)/|KS| (сума ваг 1, отже U ∈ [0,1])»`.
- КОЛИ `tick` → ТО `custom: «G = G(U; μ, σ) ∈ [-1,1]»` → ТО `set_value(cell, clip(A + Δt·G, 0, 1))`; усі клітини — одночасно по старому стану.
- КОЛИ `tick` → ЯКЩО `custom: «|U − μ| малий (U у вікні росту)»` → ТО `custom: «A росте до 1»`; інакше `custom: «A згасає до 0»`.
- Ядро-оболонка: `custom: «KS(r; β) = β[⌊B·r⌋] · KC(B·r mod 1)»`; KC(0) = KC(1) = 0, зазвичай KC(½) = 1 — кільця з піками β.
- Форми KC: експонента `exp(α − α/(4r(1−r)))`, α = 4 · поліном `(4r(1−r))^α` · прямокутник `1[¼,¾]`.
- Форми G: експонента `2·exp(−(u−μ)²/(2σ²)) − 1` · поліном · прямокутник `2·1[μ±σ](u) − 1`.
- Life як окремий випадок: `R = T = P = 1`, `KC(r) = 1[¼,¾](r) + ½·1[0,¼)(r)` (центр важить половину), G — прямокутник з μ = 0.35, σ = 0.07.
- КОЛИ `input(load-species)` → ТО `place(cursor, organism)` з його параметрами (R, T, μ, σ, β).
- КОЛИ `input(randomize)` → ТО `custom: «заповнити область випадковими значеннями (суп)»`.
- КОЛИ `input(param-change)` → ТО `custom: «нове правило діє з наступного тіку; істота або пристосовується, або розпадається/вибухає»`.
- КОЛИ `custom: «маса m = ΣA → 0»` → ТО `custom: «істота вимерла»`; КОЛИ `custom: «маса заповнила поле»` → `custom: «вибух»` — неформальні «поразки».
- Перемога: — (іграшка, `goal: none`). Неформальна мета — знайти стійкий «вид» (самоорганізація, рух, самовідновлення, симетрія).

## Керування і ввід
- Старт/стоп симуляції, крок на 1 тік, рестарт клітин.
- Повзунки й поля параметрів: μ, σ, R, T, β₁…β₄, α, η; вибір форм ядра (Gaussian bump, polynomial, trapezoidal, step для SmoothLife, high step для Life) і росту (Gaussian, polynomial, trapezoidal, step).
- Поле: додати випадкові клітини, перемістити/повернути, змінити розмір; копіювати/вставити стан.
- Бібліотека форм: завантажити істоту (з її параметрами), автоцентрування на ній.
- Режими кольору й шари перегляду (стан, приріст, сума сусідів, ядро).

## Вікна, меню, HUD
- `game-screen`: поле f(x) + додаткові вікна: Δ-вид `G(K∗A)`, вид суми сусідів `K∗A`, вид ядра k(u).
- `custom-window` «Параметри»: повзунки, вибір функцій, Run / Preset / Field / Space / Pixel / Soliton.
- `+window:species-library`: список форм/видів з назвами (Orbium unicaudatus, Scutium solidus…).
- `stats-window`: статистика реального часу — маса m, ріст g, обʼєм, щільність, кутова швидкість, моменти Hu/Flusser; детектор періоду («Calc stats»); 3D-графіки.
- `help-window`: вкладка «How to use», вкладка деталей обчислень.
- HUD: `+ui:kernel-graph` (k(r) від r), `+ui:growth-graph` (G(n)), лічильник часу t і Δt, fps.
- Переходи: параметр → поле одразу; бібліотека → поле з новою істотою і параметрами.

## Фічі поза полем
- `custom-rules` — увесь простір параметрів ядра й росту (і перемикач на SmoothLife / Game of Life).
- `step-mode`, `speed-control` (fps), `pause`.
- `+feature:gif-export` — запис GIF; копіювання/вставка стану як тексту (формат на вибір).
- `theme-select` — колірні схеми.
- Код на 5 мовах + Colab-туторіал; варіанти 3D/4D/ND, багатоядерна й багатоканальна (у Python-версії).
- Нема рахунку, рівнів, збережень прогресу.

## Варіації й родичі
- Життя Конвея (`game-of-life.md`) — окремий випадок; Brian's Brain/Seeds (`brians-brain-seeds.md`) — інша дискретна гілка (кілька станів); елементарні 1D (`elementary-cellular-automata.md`).
- SmoothLife (Rafler) — попередник із гладким кільцевим сусідством; Larger than Life — дискретний великий радіус.
- Рідини ONI (`oxygen-not-included-cells.md`), Terraria (`terraria-liquids.md`) — теж неперервне значення в клітині, але з законом збереження маси; у Lenia маса не зберігається.
- Осі варіацій: **стан** (2 / N / неперервний) · **сусідство** (Мур-8 / радіус r / зважене ядро) · **правило** (таблиця B/S / гладка G) · **вимір** (2D / 3D / ND) · **канали** (1 / кілька взаємодіючих полів) · **крок** (дискретний / Δt → 0, диф. рівняння).
- Ігрові нащадки: Particle Life та «artificial life» пісочниці (?), Flow Lenia (маса зберігається) (?).

## Цікавинки для курсу
- Крок Lenia наївною згорткою радіуса R на numpy — 📎 (подвійний цикл → векторизація; пастка — оновлення на місці).
- Той самий крок через FFT (згортка = множення спектрів, тор безкоштовно) — 🥉 (і заміри: наївна O(N·R²) проти O(N log N)).
- «Life як точка Lenia»: параметри R=T=P=1 + прямокутна G відтворюють B3/S23 — 🥉 (тест рівності двох двіжків — чудова задача на тести).
- Бібліотека істот у JSON/RLE-подібному форматі з параметрами — 📎.
- Статистика патерна: маса, центр мас, швидкість, детектор періоду — 🥈.
- Пошук нових видів: перебір μ/σ + фільтр «вижило, рухається, не вибухнуло» — 🥇 (еволюційний пошук, як у EvoJAX-ноутбуці).
- Багатоканальна Lenia (кілька полів впливають одне на одне) — 👑.

## Мапа на каталог
- Є: `cell-click` (клік по полю) · `game-loop` + `game-pause` · `state-as-data` (поле = масив float) · `rule-variants` (форми ядра і росту, перемикач Life/SmoothLife) · `field-scaling` + `field-size-picker` · `wrap-edges` (тор) · `gui-render` + `logic-render-split` (кілька видів одного стану) · `theme-select`.
- **Нема** → пропозиції карток:
  - `+continuous-cell-state` «Неперервний стан клітини» · game-logic · 📎 · слот {levels P} — float 0..1 замість bool, clip.
  - `+convolution-kernel` «Сусідство-ядро» · game-logic · 🥉 · слоти {R, peaks β, core} — зважена сума по кругу замість лічби 8 сусідів.
  - `+growth-function` «Функція росту» · game-logic · 📎 · слоти {μ, σ, shape} — гладка заміна таблиці B/S.
  - `+fft-convolution` «Згортка через FFT» · code/perf · 🥈.
  - `+pattern-stats` «Статистика патерна» · interface/hud · 🥈 — маса, швидкість, період.
  - `+gif-export` «Експорт GIF» · support · 🥉.
  - `+cellular-automaton-rule`, `+step-run-speed`, `+pattern-library`, `+random-soup` — вже запропоновані в `game-of-life.md` / `brians-brain-seeds.md`.

## Пропозиції до словників
- `+cond:kernel_sum` — зважена сума по ядру в межах вікна (узагальнення `adjacent_count` для Lenia, SmoothLife, тепла в ONI).
- `+effect:add_value` — додати до значення клітини з обрізанням (`A += Δt·G`, clip); `set_value` не передає «приріст».
- `+ui:kernel-graph`, `+ui:growth-graph` — графіки функцій правила поруч із полем.
- `+ui:param-slider` — повзунок параметра правила в реальному часі.
- `+ui:stats-plot` — живий графік статистик патерна.
- `+window:species-library` — бібліотека форм із параметрами правила (на відміну від `pattern-library` Life, де правило одне).
- `+feature:gif-export` — запис анімації.
- `+axis:states=continuous` — до запропонованої `states=n` (Brian's Brain).
- `+axis:neighbourhood=kernel` — вісь сусідства: moore8 / vn4 / radius-r / kernel.
- `+card:convolution-kernel`, `+card:continuous-cell-state` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Lenia](https://en.wikipedia.org/wiki/Lenia) — повні формули (U = K∗A, KS, KC, G), Life як окремий випадок (μ = 0.35, σ = 0.07), 400+ видів, нагороди 2018–2019.
- [Сторінка автора](https://chakazul.github.io/lenia.html) — таймлайн (Orbium 2015-04-15; 3D/4D, ND, multi-kernel, multi-channel 2019–2020), лінки на код і демо.
- [JS-версія](https://chakazul.github.io/Lenia/JavaScript/Lenia.html) — інтерфейс: види поля, параметри μ/σ/R/T/β, форми функцій, статистика, бібліотека форм.
- [GitHub Chakazul/Lenia](https://github.com/Chakazul/Lenia) — код (не відкривав, лінк зі сторінки автора); основна стаття — arXiv:1812.05433 (Complex Systems, 2019).

## Непевне
- (?) Тор як межа поля — випливає з FFT-реалізації, у джерелах прямо не сказано.
- (?) Параметри Orbium (R = 13, μ = 0.15, σ = 0.015 — з памʼяті) — у файл не вписано.
- (?) Підписи кнопок JS-версії частково стерті у витязі; клавіатурні скорочення не встановлено.
- (?) SmoothLife як попередник і Flow Lenia / Particle Life як нащадки — з власних знань; сторінки не відкривав.
