# T275 · контракт виконавців (фронт і бек)

Робочий документ задачі: спільна частина ТЗ для тих, хто пише паралельно. Рішення й вигляд — [T274](../../../games/.t/T274-P--game-desc-v4-design.md) (розділи §1–§11); мова інтерфейсу — [T270](../../../games/.t/T270-P--game-desc-v3-design.md) §1–§5; що вже є в редакторі — [контракт T271](../T271--game-desc-v3/front-contract.md) (перелік цеглинок чинний).

## Правила

- Vue 3 `<script setup>`, Bootstrap 5 лише CSS, нових залежностей нема. Бек — FastAPI + Beanie, як поруч.
- Код лаконічний і очевидний, «ніби писав сам Vitalik»: мінімум шарів і магії; файл — одна відповідальність, орієнтир ≤ ~80 рядків, виріс — розбити. Код, імена, коментарі — англійською; тексти на екрані — українською, на «ти», без канцеляриту. Коментар — лише «чому», один рядок; шапка компонента — одним-двома рядками, що він таке. Перед здачею перечитай свої коментарі й прибери зайві.
- Мова дій T270 §1 — без винятків: додати — `btn btn-sm btn-add` з `<Icon name="plus" />` і словом; зберегти — `btn btn-sm btn-success` з `<Icon name="check" />` «Зберегти»; скасувати — `btn btn-sm btn-outline-secondary` «Скасувати»; прибрати рядок форми — `<button class="iact del"><Icon name="minus" /></button>`; видалити обʼєкт — `<DelButton what="…" @yes="…" />`; редагувати — `<button class="iact"><Icon name="pencil" /></button>`. Жодного `✕`, `💾`, `✏️`, `🗑️` як кнопок, жодного `btn-primary` / `btn-outline-primary` у редакторі, каталозі й знахідках. Перемикач вигляду — `btn-group btn-group-sm` з `btn-outline-secondary` і `active`.
- Нічого не стрибає (T270 §2): що відкривається по кліку на рядок чи іконку — у `Pop`; форма редагування — на місці картки.
- На екрані «категорія / підкатегорія» (не «зона / підзона»); у коді — `zone` / `subzone`.
- Обидві теми (світла й темна: кольори через змінні Bootstrap і `color-mix`, без голих `#fff` / `#000` для тексту й тла) і ширина 390 px (нічого не вилазить убік).
- Не чіпати: чужі файли з таблиці нижче, `data/`, `.dev/` (крім свого звіту, якщо просять), git. Не запускати дев-сервер, браузер, `npm install`, `vite build` (дев-сервери вже крутяться на 8030 / 5030 і самі підхоплюють файли — не зупиняй їх).
- Перевірка свого: `node "/private/tmp/claude-505/-Users-v6u-Main-Dropbox-Dev-Dev-v4-Nure-python-labs/f2a89dd8-1d36-494d-b42d-a5c6e2e63d87/scratchpad/sfc-check.mjs" <свої .vue>` (розбір і компіляція кожного файла окремо; імпортів не перевіряє — шляхи й імена експортів звір очима з джерелами) і `node --check <свій .js>`.
- У відповіді: що зроблено (файли), що свідомо не зроблено й чому, де сумнів, що варто перевірити в браузері. До 30 рядків.

## Нове спільне (вже написано, читай джерела)

- `app/vue/src/fold.js` — памʼять згортання: `isFolded(key)`, `toggleFold(key)`, `setFold(key, on)`, `foldAll(keys, on)`; ключі — `ed:<секція>`, `game:<блок>`.
- `app/vue/src/sandbox.js` — `sandbox` (ref: slug основи, поки пісочниця ввімкнена), `setSandbox(slug | '')` — вмикає заголовок `X-Sandbox` на всіх запитах (`@core/http.js: extra`).
- `app/vue/src/api.js` — `getSandbox(slug)`, `resetSandbox(slug)`, `judgeRef(id, { status, reply })`; `postRef` / `putRef` приймають ще `kind`, `zone`, `subzone`, `task`.
- `@core/local.js` — `load(key)`, `save(key, value)` (localStorage, що може бути відсутнім).
- `@core/components/TagInput.vue` — тег додає Enter, **кома** або вихід з поля; напис за замовчуванням — «через кому».

## Хто що пише

| хто | файли |
|---|---|
| **бек** | `app/api/routes/sandbox.py` (новий), `routes/my_game.py`, `my_parts.py`, `my_claims.py`, `my_rules.py`, `my_shots.py`, `my_template.py`, `routes/refs.py`, `models/ref.py`, `bot/game_alerts.py`, `main.py`, `tests/smoke_*.py` |
| **каталог** `/tasks` | `components/MasonryGroups.vue` → новий `TaskGroups.vue` (старий видалити), `TaskCatalog.vue`, `ZoneNav.vue`, `TaskCard.vue`, `TaskBody.vue`, `TaskAdd.vue` (+ свої нові поруч), `TaskFilters.vue`, `TaskNames.vue`, `TaskWhere.vue`, `TaskEdit.vue`, `taskMeta.js`, `pages/TasksPage.vue` |
| **правила** | `components/RulesBlock.vue`, нові `RulesControls.vue`, `RulesTime.vue` (+ спільне своє), `PhasesStrip.vue` |
| **знахідки** | `pages/RefsPage.vue`, `components/RefCard.vue`, нові `IdeaForm.vue`, `RefFilters.vue` (+ свої), `ProposeCard.vue`, `AskTeacher.vue` |
| **схема** | `graphLayout.js`, `graphTree.js`, `components/GameGraph.vue`, `GraphPanel.vue`, новий `GraphOutline.vue` |
| **оболонка** | `components/GameEditor.vue`, `SectionHead.vue`, новий `DraftStrip.vue`, `EntityCard.vue` і `WindowCard.vue` (лише позначка «ще не описано»), `hints.js`, `pages/GamePage.vue`, нові `GameMoments.vue` + `moments.js`, `MyGameForm.vue`, `pages/MyGamePage.vue`, `ShotStrip.vue` (лише пісочниця), `router.js`, `EntityForm.vue` і `FieldProps.vue` (лише напис поля тегів) |

## Інтерфейси між авторами (пиши під них, чужого не пиши)

- `<IdeaForm :kind? :zone? :subzone? :task? compact? @done @cancel />` (знахідки) — форма запису знахідки чи ідеї: що передано пропсом — те підставлено й не питається (показується рядком «про що»); `compact` — для панелі `Pop` (без вибору категорії, якщо вона передана); сама шле `postRef`, на успіху показує «Надіслано ✓» і за мить кличе `done`. **Каталог** ставить її в `Pop` шапки підкатегорії (`kind="idea"`, `zone`, `subzone`) і внизу розгорнутої картки (`kind="fix"`, `task`, `zone`, `subzone`).
- `ed.sandbox` (оболонка, булеве в контексті редактора) — редактор працює в пісочниці: `ShotStrip` не показує «додати скриншот».
- Секції редактора мають id `field`, `levels`, `entities`, `rules`, `windows`, `zone-<категорія>` (як було); заявка без місця більше не живе в секції `drafts` — вона в смужці своєї секції (оболонка), рядок заявки — той самий `ClaimRow` (`id="c-<id>"`).
- Форма частини для запису (`postPart` / `putPart`) — як її приймає `app/api/routes/my_parts.py` (`PartIn`); відповідь гри — `app/api/passport.py`.
- Бек пишеться паралельно за T274 §11 — фронт кодує під контракт.
