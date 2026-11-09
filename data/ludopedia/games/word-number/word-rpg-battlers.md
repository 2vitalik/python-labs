---
title: Letter Quest і Spellspire — словесні RPG-бої
slug: word-rpg-battlers
aka: [Letter Quest, "Letter Quest: Grimm's Journey", "Letter Quest: Grimm's Journey Remastered", Spellspire]
family: word-number
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 2014
platforms: [Windows, macOS, Linux, PS4, Xbox One, Switch]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/328730/", best: true, note: "Letter Quest: Grimm's Journey — плитки ворогів (poison, plague, stone, whirlwind, duplicator, spike, flipped), кристали, зброя, книги, зілля, 40 етапів × 4 способи"}
  - {kind: steam, url: "https://store.steampowered.com/app/373970/Letter_Quest_Grimms_Journey_Remastered/", note: "Remastered (05.08.2015): Endless mode зі своїм лоадаутом, ввід з клавіатури, тултіпи, 70 квестів"}
  - {kind: other, url: "https://pixelpoppers.com/review/letter-quest-grimms-journey/", note: "огляд: пул 15 літер, шкода з довжини й рідкості, апгрейди за самоцвіти, челенджі рівнів, порівняння з Bookworm Adventures"}
  - {kind: official, url: "https://www.letterquestgame.com/", note: "Letter Quest: список поганих плиток, scythes, книги, crystal stars"}
  - {kind: steam, url: "https://store.steampowered.com/app/626580/", note: "Spellspire (10tons, 23.05.2017): слово з сітки = заклинання з палички, вежа, екіпірування, зілля й сувої"}
  - {kind: other, url: "https://www.thexboxhub.com/spellspire-review/", note: "Spellspire: 10 випадкових літер на етап, слова ≥3, таймінги атак кожного монстра, стихії, 100 поверхів, бос кожні 10, challenge star"}
  - {kind: other, url: "https://sirusgaming.com/2017/11/14/spellspire-review-a-wizards-spells", note: "Spellspire: магазин між рівнями, monsterpedia, підказка за 1 золото, видалення літери з хвостом при тапі"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=letter+quest+grimm%27s+journey+gameplay", note: "пошук; геймплей Letter Quest"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=spellspire+gameplay", note: "пошук; геймплей Spellspire"}
stage: v1
coverage: 60
mechanics: [cell-click, keyboard-controls, controls-remap, word-validation, hp-damage, status-effects, inventory-items, shop-between-levels, shop-catalog, shop-window, sequential-levels, level-unlock, world-map, codex-window, achievements-window, leaderboard, save-progress, mode-select, game-screen, end-screen, settings-window, popup-text, event-effects, +word-as-attack, +letter-weight-damage, +status-tile, +equip-loadout, +stage-challenges, +elemental-weakness, +attack-timer-bar, +longest-word-hint, +endless-custom-loadout, +timed-shop-chest]
proposes: ["+cond:word_weight", "+cond:weak_to", "+ui:attack-timer-bar", "+ui:enemy-preview", "+window:challenge-select", "+feature:stage-challenges", "+feature:timed-chest", "+card:stage-challenges"]
author: opus
date: 2026-11-09
---

# Letter Quest і Spellspire — дві гілки схеми Bookworm Adventures: покроковий бій з прокачкою і real-time бій з однаковими літерами на весь етап

## Суть
Обидві гри — наступники [bookworm-adventures.md](bookworm-adventures.md): слово з літер сітки = удар по монстру, що довше й рідкісніше слово, то сильніший. Різниця з BWA мала, тож вони описані одним файлом як дві точки на осях варіацій. **Letter Quest: Grimm's Journey** (Bacon Bandit Games, 2014) тримає покроковість і пул із 15 літер, але додає ширший набір «поганих» плиток від ворогів, магазин апгрейдів за самоцвіти, зброю й книги та 4 способи пройти кожен етап. **Spellspire** (10tons, 2017) робить бій real-time: 10 випадкових літер на етап, кожен монстр б'є за своїм таймінгом, а стихії й екіпірування (паличка, капелюх, мантія) вирішують більше, ніж словник.

## Поле і час
- Letter Quest: пул 15 плиток-літер; використані замінюються «напіввипадково» (сусідство не потрібне, як у BWA). Покроково: слово гравця → дія ворога.
- Spellspire: 10 випадкових літер на етап; програв — новий набір. Літери, найімовірніше, не витрачаються в межах етапу (?). Час real-time: кожен монстр має власний інтервал атаки, гравець складає слова, скільки встигне.
- Обидві: над сіткою — бойова сцена з HP героя й ворога; етапи послідовні на мапі (LQ) або на поверхах вежі (Spellspire: 100 поверхів, далі підземелля).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Grimm / Rose (LQ) | player | HP, зброя, книги, апгрейди | слово = атака; HP 0 → етап заново |
| Чарівник (Spellspire) | player | HP, паличка, капелюх, мантія | слово = заклинання з палички |
| Плитка-літера | tile | літера, вага | у слові → шкода; LQ: замінюється новою |
| Кристальна плитка (LQ) | tile | бонус | у слові дає особливий бонус |
| Poison / Spike (LQ) | hazard | стан плитки від ворога | у слові шкодить герою (?) — точно який з них що робить, у «Непевне» |
| Plague / Stone / Whirlwind / Duplicator / Flipped / Broken (LQ) | tile | стан плитки від ворога | ускладнюють слово; ефекти — у «Непевне» |
| Ворог (LQ) | enemy | HP, здібності | після слова: шкода, крадіжка HP, самолікування, критичний удар, псування плиток |
| Монстр (Spellspire) | enemy | HP, таймінг атаки, шкода, стихія | б'є за своїм таймером; вразливий / стійкий до вогню, отрути |
| Бос | boss | HP, сильніші атаки | LQ — у кінці зон; Spellspire — кожен 10-й поверх, б'є «з одного удару» |
| Зброя: коса (LQ) | pickup | рівень апгрейда | кілька видів, прокачуються |
| Книга (LQ) | pickup | рівень | унікальний пасивний бонус, обирається й прокачується |
| Паличка (Spellspire) | pickup | стихія | додає підпал, отруту, вампіризм або заморозку |
| Капелюх / мантія (Spellspire) | pickup | ефект | бонус шкоди за слова з голосної на початку, повільніші атаки ворогів, захист від отрути |
| Зілля здоровʼя | pickup | — | лікує героя; у Spellspire іноді падає з ворогів |
| Сувій / word-search (Spellspire) | pickup | — | підсвічує найсильніші / найдовше слово етапу |
| Самоцвіти / золото | resource | — | валюта апгрейдів (LQ — самоцвіти, Spellspire — монети) |

## Правила (КОЛИ → ЯКЩО → ТО)
Спільне (як у BWA):
- КОЛИ `input(click tile | type letter)` → ТО `custom: «літера додається до слова; сусідство не перевіряється»`.
- КОЛИ `input(cast)` → ЯКЩО `in_dictionary(word)` → ТО `damage(enemy, custom: «з довжини слова і рідкості літер»)`; інакше `block`.
- КОЛИ `hp_zero(enemy)` → ТО `currency(+n)`, `custom: «наступний ворог етапу»`.
- КОЛИ `hp_zero(player)` → ТО `lose`, `restart`.
- КОЛИ `level_end` → ТО `currency(+n)`, `unlock(next stage)`.

Letter Quest:
- КОЛИ `after(cast)` → ТО `clear(word tiles)`, `spawn_at(tile, cleared cells)` — «напіввипадково».
- КОЛИ `input(cast)` → ЯКЩО `has(word, crystal tile)` → ТО `custom: «бонус кристала»`.
- КОЛИ `turn_end(player)` → ТО одна дія ворога: `damage(player, n)` · `heal(enemy, n)` · `custom: «краде HP»` · `custom: «критичний удар»` · `set_state(tile, poison|plague|stone|whirlwind|duplicator|spike|flipped|broken)`.
- КОЛИ `input(cast)` → ЯКЩО `has(word, spoiled tile)` → ТО `damage(player, n)` (огляд: «плитки, що шкодять при вживанні»).
- КОЛИ `input(use potion)` → ЯКЩО `has(player, potion)` → ТО `take(player, potion)`, `heal(player, n)`.
- КОЛИ `input(cast)` → ЯКЩО `has(player, weapon | book)` → ТО `custom: «модифікатор шкоди/ефекту зброї або книги»`.
- КОЛИ `level_start` → ЯКЩО `mode(challenge)` → ТО `custom: «обмеження етапу: на швидкість / з голосних лише E / рівно 4 літери»`.
- КОЛИ `level_end` → ЯКЩО `mode(challenge)` і `custom: «обмеження дотримано»` → ТО `currency(+n)`, `give(player, star)`.
- КОЛИ `input(buy upgrade)` → ЯКЩО `counter(gems, >=, price)` → ТО `currency(-price)`, `custom: «апгрейд героя / зброї / книги»`.
- Endless (Remastered): КОЛИ `hp_zero(enemy)` → ЯКЩО `mode(endless)` → ТО `custom: «новий ворог без кінця; рахунок — скільки протримався»`.

Spellspire:
- КОЛИ `level_start` → ТО `custom: «10 випадкових літер на етап»`, `window(game-screen)`.
- КОЛИ `input(cast)` → ЯКЩО `in_dictionary(word)` і `custom: «≥ 3 літер»` → ТО `damage(enemy, custom: «росте з довжиною; 8–10 літер — найсильніші»)`.
- КОЛИ `input(cast)` → ЯКЩО `has(player, wand fire|poison|frost|drain)` → ТО `set_state(enemy, burning|poisoned|frozen)` або `heal(player, n)` (вампіризм).
- КОЛИ `input(cast)` → ЯКЩО `state(enemy, fire_resistant)` → ТО `custom: «вогонь слабший, потрібна отрута»`.
- КОЛИ `input(cast)` → ЯКЩО `has(player, robe|hat vowel bonus)` і `custom: «слово з голосної»` → ТО `multiplier(×k)`.
- КОЛИ `timer(per monster)` → ТО `damage(player, n)`; ЯКЩО `has(player, slow-enemy gear)` → ТО `custom: «інтервал довший»`.
- КОЛИ `hp_zero(player)` → ТО `restart`, `custom: «новий набір літер»`.
- КОЛИ `level_end` → ЯКЩО `mode(challenge)` і `custom: «жодного удару по героєві»` → ТО `give(player, challenge star)`, `currency(+n)`.
- КОЛИ `input(use scroll)` → ТО `reveal(custom: «найсильніші слова етапу»)`.
- КОЛИ `level_start` → ЯКЩО `custom: «поверх кратний 10»` → ТО `spawn_at(boss, arena)`.
- Перемога: LQ — пройти 40 етапів (і зірки челенджів) · Spellspire — вершина вежі (100 поверхів), далі підземелля · Поразка: HP 0 → етап заново · Рахунок: Endless (LQ), лідерборди.

## Керування і ввід
- LQ: мишка/тач по плитках або клавіатура — друк літер, Backspace стирає останню; хоткеї перепризначаються.
- Spellspire: тач по літерах або кнопки геймпада; тап по літері в слові прибирає її і всі після неї; на геймпаді вибір і стирання незручні (огляд).
- Між етапами — магазин і екіпірування; Spellspire показує монстрів етапу ще до входу.

## Вікна, меню, HUD
- `game-screen`: сітка/набір літер, поточне слово, кнопка атаки, HP героя й ворога (`hp-bar`), `popup-text` шкоди, полиця зілля; Spellspire — таймінги атак ворогів (`attack-timer-bar`) (?), тултіпи (LQ Remastered).
- `map-window` (LQ): мапа етапів з п'ятьма зонами; Spellspire — поверхи вежі.
- `challenge-select`: 4 способи пройти етап (LQ) / одноразовий челендж поверху (Spellspire).
- `shop-window`: апгрейди, зброя, книги, зілля (LQ); палички, капелюхи, мантії, сувої, скриня з оновленням раз на 8 год (Spellspire).
- `codex-window`: monsterpedia (Spellspire, купується в магазині).
- `mode-select` (LQ Remastered): Endless — вибір фону, музики, героя, зброї й набору плиток.
- `achievements-window`, `leaderboard` (Steam), `settings-window` (хоткеї, роздільність).
- Переходи: мапа/вежа → `enemy-preview` (Spellspire) → бій → `end-screen` (нагорода, зірка челенджу) → магазин → далі.

## Фічі поза полем
- `meta-progression`: апгрейди героя, зброї, книг (LQ); екіпірування з вільною заміною (Spellspire).
- `stage-challenges`: повтор етапу з обмеженням за нагороду; зірки челенджів відкривають товари в магазині (Spellspire).
- `mode-endless` з власним лоадаутом (LQ Remastered).
- `hint`: підказка за 1 золото, сувій найсильніших слів (Spellspire).
- `achievements` (LQ — 52, Remastered — 60), 70 квестів, `remap-controls`, `cloud-save`.
- `timed-chest`: скриня магазину, що оновлюється раз на 8 год (Spellspire).

## Варіації й родичі
- [bookworm-adventures.md](bookworm-adventures.md) — спільний предок схеми; [bookworm.md](bookworm.md) — шлях по сусідах і гравітація.
- [wordatro.md](wordatro.md) — слово як рука в роглайті; [alphabear.md](alphabear.md) — плитки з лічильником; Puzzle Quest — та сама «пазл = удар» у match-3.
- **Осі варіацій:** час (покроково / таймер атаки кожного ворога) · літери (витрачаються й поповнюються / сталий набір на етап) · що вирішує шкоду (довжина / рідкість / стихія й вразливість) · погані плитки (немає / кілька станів / ціла таксономія) · прогресія (скарби на главу / магазин апгрейдів / екіпірування в слотах) · повтор етапу (нема / челенджі з обмеженнями / нескінченний режим).

## Цікавинки для курсу
- Шкода з довжини слова (поріг ≥3, бонус 8–10) і таблиця ваги літер — 🌱.
- Стани плиток від ворога (отрута, камінь, перевернута, дублікатор) з власною поведінкою в слові — 🥉.
- Real-time таймер атаки для кожного монстра поверх «друку слів» — 📎.
- Стихії: паличка-ефект × вразливість/стійкість монстра — 📎.
- Челенджі етапу як модифікатори правил (лише голосна E, рівно 4 літери, на час) — 📎 (один валідатор зі слотами).
- Підказка «найсильніше слово з 10 літер»: перебір словника за мультимножиною літер — 🥉.
- Магазин з таймерною скринею (оновлення раз на 8 год) — 🌱.

## Мапа на каталог
- Є: `cell-click` / `keyboard-controls` / `controls-remap` ↔ ввід слова · `word-validation` · `hp-damage` · `status-effects` ↔ підпал, отрута, заморозка · `inventory-items` ↔ зілля, сувої · `shop-between-levels` / `shop-catalog` / `shop-window` · `sequential-levels` / `level-unlock` / `world-map` · `codex-window` ↔ monsterpedia · `achievements-window` · `leaderboard` · `save-progress` · `mode-select` ↔ Endless · `game-screen` · `end-screen` · `settings-window` · `popup-text` · `event-effects`.
- **Нема** → пропозиції карток:
  - `+word-as-attack`, `+letter-weight-damage`, `+status-tile`, `+equip-loadout`, `+attack-timer-bar` — як у bookworm-adventures.md (друга-третя гра).
  - `+stage-challenges` «Повтор рівня з обмеженням правил за нагороду» · levels/progression · 📎 · слоти {constraint, reward}.
  - `+elemental-weakness` «Стихія атаки × вразливість/стійкість ворога» · entities/combat · 📎 · слоти {elements, table}.
  - `+longest-word-hint` «Підказка: найсильніше слово з наявних літер» · game-logic/difficulty · 🥉.
  - `+endless-custom-loadout` «Нескінченний режим з вибором героя, зброї, плиток» · game-logic/modes · 🌱.
  - `+timed-shop-chest` «Скриня магазину з оновленням за реальним часом» · game-logic/economy · 🌱 · слоти {period: 8h}.

## Пропозиції до словників
- `+cond:word_weight` — вага слова (довжина × рідкість) проти порогу (друга гра після BWA).
- `+cond:weak_to` — ворог вразливий / стійкий до стихії атаки (Spellspire).
- `+ui:attack-timer-bar` — шкала до удару ворога (друга гра після BWA Arena).
- `+ui:enemy-preview` — список монстрів етапу до входу (Spellspire).
- `+window:challenge-select` — вибір способу/обмеження для повтору етапу.
- `+feature:stage-challenges` — повтор рівня з обмеженнями за зірки й валюту.
- `+feature:timed-chest` — оновлення магазину за реальним часом.
- `+card:stage-challenges` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Letter Quest: Grimm's Journey](https://store.steampowered.com/app/328730/) — повний перелік поганих плиток, кристали, зброя, книги, зілля, 40 етапів × 4, 30+ монстрів, 70 квестів, словник 190 000+.
- [Steam: Letter Quest Remastered](https://store.steampowered.com/app/373970/Letter_Quest_Grimms_Journey_Remastered/) — Endless mode, клавіатура й Backspace, тач, тултіпи.
- [Pixelpoppers: Letter Quest](https://pixelpoppers.com/review/letter-quest-grimms-journey/) — пул 15 літер, челенджі етапу (швидко, лише E, рівно 4 літери), порівняння з BWA.
- [letterquestgame.com](https://www.letterquestgame.com/) — scythes, книги, crystal stars, broken-плитка.
- [Steam: Spellspire](https://store.steampowered.com/app/626580/) — слово = заклинання, вежа, екіпірування, зілля й сувої, дата.
- [TheXboxHub: Spellspire](https://www.thexboxhub.com/spellspire-review/) — 10 літер, слова ≥3, таймінги монстрів, стихії, ефекти шмоток, скриня 8 год, 100 поверхів, бос кожні 10, challenge star.
- [Sirus Gaming: Spellspire](https://sirusgaming.com/2017/11/14/spellspire-review-a-wizards-spells) — магазин, monsterpedia, підказка за 1 золото, тап-видалення хвоста слова.
- YouTube: пошуки «letter quest grimm's journey gameplay», «spellspire gameplay».

## Непевне
- (?) Ефекти поганих плиток LQ поодинці: за назвами — spike/poison шкодять при вживанні, stone блокує, flipped ховає літеру, duplicator/plague поширюються; джерела дають лише назви.
- (?) «Помʼякшений таймер» LQ з рядка черги — у джерелах не знайшов; режим «на швидкість» є лише як челендж етапу.
- (?) Spellspire: чи сталі 10 літер упродовж етапу (схоже, так), розкладка сітки, чи є пауза між хвилями.
- (?) Spellspire на мобільних платформах — не перевірено.
- (?) Розмір поля LQ (15 літер — так, розкладка 5×3 (?)), формула шкоди обох ігор.
