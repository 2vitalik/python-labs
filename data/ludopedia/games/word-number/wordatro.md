---
title: Wordatro!
slug: wordatro
aka: [Wordatro]
family: word-number
also: [roguelike]
klass: cursor
axes:
  field: 1d
  time: turn
  opponent: none
  info: partial
  random: runtime
  goal: score
year: 2025
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3140120/Wordatro", best: true, note: "опис: пул літер з вартостями, 10 рівнів з ціллю, reroll, 50+ бонусів, Daily, 7 мов словника"}
  - {kind: other, url: "https://www.fixgamingchannel.com/wordatro-review-a-roguelite-word-game/", note: "огляд: energy-спроби, reroll, бонуси між раундами, особливі літери (жирні/курсив/підкреслені)"}
  - {kind: other, url: "https://themagicrain.com/?p=54200", note: "огляд: поля нема, 10 рівнів, складності Easy–Pro, Twitch-інтеграція"}
  - {kind: other, url: "https://web.phenixxgaming.com/2025/02/28/wordatro-pc-preview", note: "превʼю демо: довжина слова ↑ множник, приклади бонусів"}
  - {kind: other, url: "https://vaporlens.app/app/3140120/wordatro", note: "зведення відгуків: режими, проблеми словника й UI"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=wordatro+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [word-validation, event-points, move-limit, run-relics, sequential-levels, daily-puzzle, seed-share, leaderboard, difficulty-levels, achievements-window, difficulty-select, mode-select, game-screen, end-screen, main-menu, settings-window, language-picker, +letter-value-scoring, +length-multiplier, +hand-reroll, +target-score-rounds, +special-letter-tiles, +bonus-draft, +stream-chat-vote]
proposes: ["+effect:reroll", "+ui:reroll-counter", "+ui:target-score", "+ui:letter-hand", "+feature:dictionary-language", "+feature:stream-integration"]
author: opus
date: 2026-11-09
---

# Wordatro! — Balatro зі словами: склади слово з руки літер, набери ціль раунду, між раундами бери бонуси

## Суть
Роглайт-забіг з 10 рівнів. На кожному — цільовий рахунок і обмежена кількість спроб («energy»): з пулу літер складаєш слово, воно дає очки за вартість літер і множник, який росте з довжиною. Погану руку можна перекинути (reroll), але перекидання теж лічені. Після рівня обираєш один з кількох бонусів (50+ у грі), що змінюють підрахунок до кінця забігу — «джокери» Balatro у словесній грі. Поля-сітки нема: «поле» — рядок руки літер, як підставка Scrabble.

## Поле і час
- Рука — ряд плиток-літер (1d); «мішок» літер прихований, звідки добирається рука (?).
- Хід = зіграти одне слово (−1 energy) або перекинути руку (−1 reroll). Часу нема.
- Забіг = 10 рівнів зі зростанням цілі; демо мало до 7 рівнів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка-літера | tile | літера, базова вартість (рідкісні дорожчі) | вибирається в слово; після зіграння замінюється з мішка (?) |
| Особлива літера | tile | формат: жирна / курсив / підкреслена | додає цінність слову (тип бонусу — за форматом) (?) |
| Рука | zone | N літер (?) | ряд, з якого складають слово; reroll міняє весь або частину |
| Мішок літер | supply | прихований склад | джерело добору; гравцеві не показаний |
| Бонус | pickup | один з 50+, напр. «+ Vowel», «Alone», «Stock Exchange» | пасивний модифікатор очок/множника до кінця забігу |
| Ціль рівня | static | рахунок, напр. 240 на 3-му раунді | досяг — рівень пройдено |
| Energy | resource | спроби на рівень | −1 за кожне зігране слово |
| Reroll | resource | лічені | −1 за перекидання |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click letter)` → ТО `custom: «літера переходить з руки в слово, що складається»`.
- КОЛИ `input(play word)` → ЯКЩО `not in_dictionary(word, language)` → ТО `message`, `block`; energy не витрачається (?).
- КОЛИ `input(play word)` → ЯКЩО `in_dictionary(word)` → ТО `score(sum(letter values) × mult)`, `counter(energy, −1)`.
- Множник росте з кожною літерою довжини слова; бонуси додають до вартостей і множника.
- КОЛИ `input(reroll)` → ЯКЩО `count(rerolls, >, 0)` → ТО `reroll(hand)`, `counter(rerolls, −1)`.
- КОЛИ `counter(score, >=, target)` → ТО `choose(bonuses)`, `next_level`.
- КОЛИ `counter(energy, ==, 0)` → ЯКЩО `count(score, <, target)` → ТО `lose` (у Classic — мінус життя (?)).
- КОЛИ `counter(level, ==, 10)` і ціль набрана → ТО `win`, `window(end-screen)`.
- Приклади бонусів з превʼю: «перекинь лише одну літеру — її вартість зростає»; «множник +x після кожного ходу».
- Перемога: пройти 10 рівнів · Поразка: energy скінчилась без цілі · Рахунок: сума очок, Daily — у глобальному лідерборді.

## Керування і ввід
- Мишка/тап: клік по літерах руки (порядок кліків = порядок у слові), кнопки «зіграти» і «reroll»; перестановка руки (?).
- На Steam Deck — тач або стилус (кнопки дрібні, за відгуками).

## Вікна, меню, HUD
- `game-screen`: `letter-hand`, поточне слово, `target-score`, `score`, `energy-bar` (energy), `reroll-counter`, `level-number`, іконки обраних бонусів.
- `upgrade-window`: вибір бонусу з випадкової пропозиції після рівня (є reroll пропозиції (?)).
- `main-menu` → `mode-select` (Classic · Daily Challenge · seeded run) → `difficulty-select` (Tutorial (?) · Easy · Medium · Hard · Pro).
- `achievements-window`: 50 викликів-досягнень.
- `leaderboard` (Daily), `settings-window` (мова словника й інтерфейсу).
- `end-screen`: результат забігу.

## Фічі поза полем
- `mode-daily` з `leaderboard-online`; `seed-input` (seeded run); `difficulty-presets` (Easy–Pro).
- `dictionary-language` — 7 мов словника (EN, FR, ES, DE, IT, PT-BR, NL): мова змінює правила валідації, а не лише інтерфейс.
- `stream-integration` — Twitch-чат пропонує слова опитуванням.
- `achievements` (50 викликів). `meta-progression` і `unlockables` — нема (скарга відгуків).

## Варіації й родичі
- Balatro (покерні руки → слова), Bookworm (`bookworm.md`, бойова вартість слова), Scrabble (`scrabble.md`, вартості літер), Luck be a Landlord (`build-sim/luck-be-a-landlord.md`, роглайт з азартного ядра).
- Інші «Balatro-словесні» 2025: Beyond Words (MindFuel Games), Word Play (?).
- **Осі варіацій:** поле (рука без сітки / сітка Boggle) · ресурс спроб (energy / руки й скиди Balatro) · модифікатори (пасивні бонуси / особливі плитки / обидва) · словник (одна мова / кілька) · мета-прогресія (нема / розблокування).

## Цікавинки для курсу
- Підрахунок слова «вартості × множник довжини» + конвеєр бонусів-модифікаторів — 📎: шаблон Strategy/Decorator для правил очок.
- Цикл раунду з energy/reroll і ціллю, що зростає — 🌱.
- Драфт бонусу з випадкової трійки між рівнями — 📎.
- Мішок літер з частотами і перевірка «рука взагалі дає хоч одне слово» — 🥈 (відгуки скаржаться на руки з самих голосних).
- Словник кількома мовами з завантаженням списку — 🥉.

## Мапа на каталог
- Є: `word-validation` · `event-points` ↔ вартості літер · `move-limit` ↔ energy · `run-relics` ↔ бонуси до кінця забігу · `sequential-levels` ↔ 10 рівнів · `daily-puzzle` · `seed-share` ↔ seeded run · `leaderboard` · `difficulty-levels` · `difficulty-select` · `mode-select` · `achievements-window` · `language-picker` · `game-screen` · `end-screen` · `main-menu` · `settings-window`.
- **Нема** → пропозиції карток:
  - `+letter-value-scoring` «Очки слова = сума вартостей літер» · game-logic/score · 🌱 (Scrabble, Bookworm).
  - `+length-multiplier` «Множник за довжину слова» · game-logic/score · 🌱.
  - `+hand-reroll` «Перекинути руку за лічений ресурс» · game-logic/economy · 🌱.
  - `+target-score-rounds` «Раунд: набрати ціль за N ходів» · game-logic/win · 🌱.
  - `+special-letter-tiles` «Плитки з модифікатором (формат літери)» · entities/state · 📎.
  - `+bonus-draft` «Вибір 1 з N бонусів між рівнями» · game-logic/economy · 📎.
  - `+stream-chat-vote` «Глядачі пропонують хід опитуванням» · interface/input · 🥈.

## Пропозиції до словників
- `+effect:reroll` — замінити руку/пропозицію новою випадковою (Wordatro, Balatro, роглайт-магазини).
- `+ui:reroll-counter` — скільки перекидань лишилось.
- `+ui:target-score` — ціль рівня поруч із поточним рахунком.
- `+ui:letter-hand` — рука плиток-літер поза полем.
- `+feature:dictionary-language` — мова словника як параметр правил.
- `+feature:stream-integration` — Twitch-чат впливає на гру.

## Джерела
- ⭐ [Steam: Wordatro!](https://store.steampowered.com/app/3140120/Wordatro) — опис, 10 рівнів, reroll, 50+ бонусів, 50 викликів, Daily, 7 мов, розробник Le Poulet, 23.06.2025.
- [Fix Gaming Channel: огляд](https://www.fixgamingchannel.com/wordatro-review-a-roguelite-word-game/) — energy, reroll, «multis», цілі 146/240, бонуси «+ Vowel», «Alone», «Stock Exchange», формати літер.
- [The Magic Rain: огляд](https://themagicrain.com/?p=54200) — без поля, 10 рівнів, Easy/Medium/Hard/Pro, Twitch-опитування.
- [Phenixx Gaming: превʼю](https://web.phenixxgaming.com/2025/02/28/wordatro-pc-preview) — множник з довжиною, приклади бонусів, демо до 7 рівнів.
- [Vaporlens: зведення відгуків](https://vaporlens.app/app/3140120/wordatro) — режими (Classic з життями, Daily, seeded), проблеми словника, UI.
- YouTube: пошук «wordatro gameplay».

## Непевне
- (?) Розмір руки, склад мішка, чи добирається рука після слова — жодне джерело не дало.
- (?) Точна формула очок і що дають формати літер (жирна/курсив/підкреслена).
- (?) Чи витрачається energy на невалідне слово; чи є reroll пропозиції бонусів.
- (?) Classic «з життями» — лише з агрегатора відгуків; Tutorial як рівень складності — так само.
- Гра без сітки (рука = 1d): описано як межовий випадок сімʼї; файл короткий через брак первинних джерел.
