---
title: Corrypt
slug: corrypt
aka: [Corrypt (Michael Brough)]
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
year: 2012
platforms: [Windows, Mac, iOS]
links:
  - {kind: itch, url: "https://smestorp.itch.io/corrypt", best: true, note: "завантажити (Windows / Mac, «назви свою ціну»); правил на сторінці нема — найшвидше зрозуміти, зігравши"}
  - {kind: other, url: "https://gamedeveloper.com/design/road-to-the-igf-michael-brough-s-i-corrypt-i-", note: "інтервʼю (IGF 2014): «Sokoban-esque puzzle game with a twist», магія руйнує світ, звʼязок клітин між кімнатами, кнопки й двері"}
  - {kind: other, url: "https://homeoftheunderdogs.net/game.php?id=5358", note: "огляд: ящики липнуть — тягнуться за героєм цілим рядом; «речовина», кожне наступне застосування дорожче"}
  - {kind: other, url: "https://game-solver.com/corrypt/", note: "відгуки: магія «freezes the tile in place, for every area»; глючні клітини переносять предмети між екранами; друга половина — відкритий світ"}
  - {kind: other, url: "https://www.freeindiegam.es/?p=4721", note: "ПК-реліз 19.12.2012; коментарі: Z — ціль стрілками — Z; ліміт застосувань магії; undo по кімнатах"}
  - {kind: other, url: "https://apps.apple.com/gb/app/corrypt/id588935336", note: "iOS від 12.01.2013; нотатки версій: повільніші скелети, нагадування про undo"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Michael_Brough_(game_designer)", note: "ігри автора: Corrypt — 2012; фіналіст IGF Nuovo 2014"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Corrypt+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [move-4dir, keyboard-controls, push-object, pull-object, button-toggle, undo-redo, item-pickup, +forced-pull, +flip-screen-rooms, +global-tile-freeze, +spell-charges, +quest-giver, +per-room-undo]
proposes: ["+effect:freeze_tile_global", "+cond:tile_frozen", "+feature:per-room-undo", "+axis:rules", "+card:global-tile-freeze", "+card:forced-pull"]
author: opus
date: 2026-11-19
---

# Corrypt — Sokoban з липкими ящиками, де магія заморожує клітину відразу в усіх кімнатах світу

## Суть
Покрокова кімнатна головоломка Michael Brough (2012): герой ходить світом екранів-кімнат, штовхає й тягне ящики, тисне кнопки, що відчиняють двері, і розвʼязує проблеми дивних мешканців (грибного народу). Ящики «липкі»: щойно відходиш від ящика поруч, він їде слідом, а за ним — увесь ряд. Головний поворот — обмежена магія, що **заморожує клітину на її місці в усіх кімнатах одразу**, — і світ починає ламатися: «глючні» клітини переносять предмети з екрана на екран, а гра, за словами автора, стає про те, як «making a right mess of the world so that a number can go up».

## Поле і час
- Квадратна сітка; кожна кімната — один екран («small one-screen gridded play pens», HOTU); кімнати сусідять краями, проходи — на краях («edge openings from adjacent rooms»).
- Ключова топологія: позиція (x, y) однакова в усіх кімнатах; зачарована клітина стає спільною для них (?) — звідси «звʼязок далеких клітин» (ідея, за автором, виросла з телепорта й багу, що зʼєднував далекі клітини).
- Покроково: хід — крок героя. Нотатки версії згадують «slower skeletons», тож скелети, імовірно, рухаються самі (?).
- Undo — у межах кімнати («room-by-room undos»); у відгуках — «not as forgiving» як у сучасних пазлах.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | — | крок у 4 напрямки; штовхає ящик; відходячи від ящика, тягне його (і ряд за ним) |
| Ящик | object | — | штовхається; липне до героя — їде слідом, коли той відходить |
| Кнопка | switch | → двері | відчиняє двері («buttons that open doors»); утримувати чи досить натиснути — (?) |
| Двері | gate | відчинено / зачинено | відчиняються кнопкою |
| Стіна | static | — | непрохідна |
| Вода | terrain | — | є в грі (автор шкодує, що анімував її); дія — (?) |
| Драбина | static | — | її можна знищити (коментар на freeindiegam.es); сенс — (?) |
| Грибний народ | neutral | — | мешканці зі своїми проблемами, яким допомагаєш |
| Скелети | enemy | швидкість | рухаються (нотатки версії); поведінка — (?) |
| Магія | resource | лічильник застосувань | збирається й витрачається; перше застосування «will clear an impasse», кожне наступне дорожче (HOTU: «mark-up») (?) |
| Зачарована клітина | zone | позиція (x, y) | заморожена на місці «for every area»; переносить предмети між екранами |
| Жетони рахунку | pickup | — | «score tokens» — число, що росте в другій половині (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
Sokoban з липкими ящиками:
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`.
- КОЛИ `contact(player, crate)` → ЯКЩО `free(cell_behind_crate)` → ТО `push`, `move(player, dir)`; інакше `block`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(cell_behind_player, crate)` and `free(next_cell)` → ТО `move(player, dir)`, `pull(crate)` — і весь ряд ящиків позаду (HOTU: «whenever you try and move away from any adjacent crate, it happily follows you»).
- КОЛИ `enter(crate, button)` → ТО `set_state(door, open)`.
- КОЛИ `leave(crate, button)` → ТО `clear_state(door, open)` (?).
- КОЛИ `reach(player, room_edge)` → ЯКЩО `custom: «на краю прохід»` → ТО `custom: «перехід у сусідню кімнату»`.

Магія:
- КОЛИ `contact(player, magic)` → ТО `pickup(player, magic)`, `counter(magic, +1)` (?).
- КОЛИ `input(cast)` → ЯКЩО `counter(magic, >, 0)` → ТО `custom: «вибрати клітину стрілками й підтвердити тією самою клавішею»`, `counter(magic, -1)`.
- КОЛИ `custom: «магію накладено на клітину (x, y)»` → ТО `custom: «вміст клітини заморожено на її місці в усіх кімнатах світу»`.
- КОЛИ `custom: «предмет потрапив на зачаровану клітину»` → ТО `custom: «предмет зʼявляється на тій самій позиції в іншій кімнаті»` (?).
- КОЛИ `input(undo)` → ТО `undo` — лише в межах поточної кімнати (?).
- Перемога: перша половина — розвʼязати проблеми мешканців; друга — відкритий світ і число, що має рости (?). · Поразка: нема, але магію можна «permanently screw up» і застрягти (коментар на freeindiegam.es). · Рахунок: жетони (?).

## Керування і ввід
- Стрілки — крок із поштовхом чи тягненням (?).
- Магія: Z → стрілками вибрати ціль → Z ще раз (коментар на freeindiegam.es).
- Undo — клавіша (?), діє в межах кімнати; iOS — тач (?).

## Вікна, меню, HUD
- `game-screen`: кімната-екран у «glitchy» піксельній графіці; HUD — лічильник магії чи жетонів (?).
- `map-window` (?): коментарі згадують «map squares» — клітинки мапи кімнат.
- `dialogue-window`: репліки мешканців («funny dialog» у відгуку App Store).
- Кімната «Error» (відгук про виліт гри саме там) — частина зламаного світу (?).
- Переходи: кімната → (прохід на краю) сусідня кімната.

## Фічі поза полем
- `undo` по кімнатах; у iOS-версії 3 додано нагадування про undo.
- `autosave` (?): коментатор цитує збережений стан з «one magic-use remaining».
- Автор зробив власний тач-редактор рівнів, спрайтів і музики на iPad; гравцеві він, судячи з джерел, не доступний (?).
- IGF 2014 — фіналіст Nuovo Award.

## Варіації й родичі
- Автор у корпусі: `games/roguelike/868-hack.md` (там Corrypt серед його ігор; також Zaga-33, Imbroglio, Cinco Paus).
- Батько — `games/push-slide/sokoban.md`; тягнення — `games/thinky/increpare-micro-puzzles.md` (Pushy-V Pully-H), `games/grid-platformer/pushmo.md`; правила як матеріал, який ламає гравець, — `games/thinky/baba-is-you.md`.
- Світ кімнат-екранів — `+flip-screen-rooms` (Jet Set Willy, Knight Lore у корпусі).
- **Осі варіацій:** тягнення — нема / за бажанням / примусове (Corrypt) / рядом; магія — локальна / глобальна на всі кімнати (Corrypt); межа між кімнатами — незалежні карти / спільні клітини.

## Цікавинки для курсу
- Примусове тягнення ряду ящиків, коли відходиш, — 📎.
- Світ кімнат-екранів з переходом через край — 📎.
- Глобальне замороження клітини: одна позиція (x, y) спільна для всіх кімнат (шар-перекриття над картами кімнат) — 🥈.
- Предмет на спільній клітині «переходить» між кімнатами — 🥉.
- Обмежений ресурс магії, що дорожчає з кожним застосуванням, — 🌱.
- Undo в межах кімнати (стек на кімнату, скидання при виході) — 📎.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ стрілки й Z; `push-object` ↔ ящики; `pull-object` ↔ липке тягнення; `button-toggle` ↔ кнопки й двері; `undo-redo` ↔ undo по кімнатах; `item-pickup` ↔ магія, жетони.
- **Нема** → пропозиції карток:
  - `+global-tile-freeze` «Заморозити клітину в усіх кімнатах» · entities/state · 🥈.
  - `+forced-pull` «Примусове тягнення: обʼєкт поруч їде слідом, коли відходиш» · entities/move · 📎 · слот {chain: bool}.
  - `+flip-screen-rooms` (уже в корпусі) — світ екранів.
  - `+spell-charges` (уже в корпусі: Rift Wizard) — обмежені застосування магії.
  - `+quest-giver` (уже в корпусі) — мешканці з проблемами.
  - `+per-room-undo` «Undo в межах кімнати» · game-logic/history · 🌱.

## Пропозиції до словників
- `+effect:freeze_tile_global(cell)` — зафіксувати вміст клітини на її позиції в усіх кімнатах чи рівнях.
- `+cond:tile_frozen(cell)` — клітина зачарована (спільна для всіх кімнат).
- `+feature:per-room-undo` — undo, що діє лише в поточній кімнаті.
- `+axis:rules` — значення `breakable`: гравець ламає світ гри як механіку (поруч із `unlocked`).
- `+card:global-tile-freeze`, `+card:forced-pull` — механік нема в каталозі.

## Джерела
- ⭐ [itch.io: Corrypt](https://smestorp.itch.io/corrypt) — завантаження Windows / Mac, «назви свою ціну», iOS-значок; опису правил нема.
- [Game Developer: Road to the IGF](https://gamedeveloper.com/design/road-to-the-igf-michael-brough-s-i-corrypt-i-) — «Sokoban-esque puzzle game with a twist», руйнівна магія, звʼязок клітин між кімнатами, кнопки й двері, тач-редактор на iPad, IGF Nuovo 2014.
- [Home of the Underdogs](https://homeoftheunderdogs.net/game.php?id=5358) — липкі ящики й ряд, що їде слідом; однокімнатні «play pens»; «речовина» з дорожчанням.
- [Game-Solver: Corrypt](https://game-solver.com/corrypt/) — відгуки: «freezes the tile in place, for every area», «glitched tiles that transport items from screen to screen», «drag the blocks as well as push them», відкритий світ у другій половині.
- [FreeIndieGam.es](https://www.freeindiegam.es/?p=4721) — дата ПК-релізу, коментарі про Z-стрілки-Z, ліміт магії, undo по кімнатах, знищені драбини.
- [App Store](https://apps.apple.com/gb/app/corrypt/id588935336) — опис, iOS від 12.01.2013, нотатки версій.
- [Wikipedia: Michael Brough](https://en.wikipedia.org/wiki/Michael_Brough_(game_designer)) — рік 2012 і номінація.
- YouTube: [пошук «Corrypt gameplay»](https://www.youtube.com/results?search_query=Corrypt+gameplay).

## Непевне
- (?) Точна модель магії: заморожена клітина незмінна чи спільна для всіх кімнат (обидва формулювання — з відгуків та інтервʼю); скільки застосувань і як вони поповнюються.
- (?) «There's a mark-up for each subsequent injection» (HOTU) — чи це зростання ціни магії.
- (?) Друга половина гри («topsy turvy», відкритий світ, жетони й число) — лише з відгуків.
- (?) Скелети, вода, драбини, «magic doors», «daughter» («a neat rule-change» у коментарі) — назви з відгуків і коментарів, механіка невідома.
- (?) Чи штовхаються ряди ящиків ланцюгом і чи можна відійти від ящика, не тягнучи його.
- (?) Рік: у черзі 2013 (iOS-реліз 12.01.2013), але ПК-версія вийшла 19.12.2012, Wikipedia — 2012.
