# T271 · контракт фронту редактора гри

Робочий документ задачі: спільна частина ТЗ для тих, хто пише компоненти редактора `/my/game` і паспорта `/students/<нік>` паралельно. Рішення й вигляд — [T270](../../../games/.t/T270-P--game-desc-v3-design.md); тут — що вже є, як називається і хто що пише.

## Правила

- Vue 3 `<script setup>`, Bootstrap 5 лише CSS (без його JS), нових залежностей нема.
- Код лаконічний і очевидний; файл — одна відповідальність, орієнтир ≤ ~80 рядків, виріс — розбити. Код, імена, коментарі — англійською; тексти на екрані — українською, на «ти», без канцеляриту. Коментар — лише «чому», один рядок; шапка компонента — одним-двома рядками, що він таке.
- Мова дій T270 §1 — без винятків: додати — `btn btn-sm btn-add` з `<Icon name="plus" />` і словом; зберегти — `btn btn-sm btn-success` з `<Icon name="check" />` «Зберегти»; скасувати — `btn btn-sm btn-outline-secondary` «Скасувати»; прибрати рядок форми — `<button class="iact del"><Icon name="minus" /></button>`; видалити обʼєкт — `<DelButton what="…" @yes="…" />`; редагувати — `<button class="iact"><Icon name="pencil" /></button>`. Жодного `✕`, `💾`, `✏️`, `🗑️` як кнопок, жодного `btn-primary` / `btn-outline-primary`.
- Нічого не стрибає (T270 §2): що відкривається по кліку на рядок чи іконку — у `Pop`; форма редагування картки — на місці картки.
- Не чіпати: бекенд (`app/api`, `core/api`), `data/`, `.dev/`, git, чужі файли зі списку нижче. Не запускати дев-сервер, браузер, `npm install`, `vite build`.
- Перевірка свого: `node "/private/tmp/claude-505/-Users-v6u-Main-Dropbox-Dev-Dev-v4-Nure-python-labs/ce0b9770-b7a9-4bc9-b98f-eaa4cf0f5170/scratchpad/sfc-check.mjs" <свої .vue>` (розбір і компіляція кожного файла окремо; імпорти не перевіряє — шляхи й імена експортів звір очима з джерелами) і `node --check <свій .js>`.

## Що вже є (прочитай джерела перед вжитком)

Ядро `core/ui/` (імпорт через `@core/…`):
- `components/Icon.vue` — `<Icon name="…" />`: `plus minus done check x pencil trash move image down right left link note eye back table list search open unfold fold help`.
- `components/Pop.vue` — спливна панель: `<Pop v-model="open" width="22rem" block?>` зі слотом `#trigger="{ toggle, open }"` і вмістом у слоті за замовчуванням (`{ close }`).
- `components/DelButton.vue` — кошик з підтвердженням у панелі: `what` (кого, у знахідному: «сутність «Ворог»»), `note`, подія `yes`.
- `lightbox.js` — `showShot(list, i)`; сам `Lightbox` уже змонтований у `GameEditor`.
- `components/TagInput.vue`, `components/GrowArea.vue` — як були.
- `style.css` — класи `btn-add`, `iact` / `iact del` / `iact add`, `soft-input`, вигляд `<mark>`.
- `anchors.js` — `flash(id)` (через `jump`).

Сайт `app/vue/src/`:
- `ed.js` — `useEd()`: контекст редактора (поля — в шапці файла). Компоненти редактора беруть дані звідси, а не пропсами: `const ed = useEd()`; після запису — `ed.changed()`.
- `components/Picker.vue` + `pick.js` — список вибору з пошуком (T270 §5): `<Picker :items placeholder inline? autofocus? small? @pick>`, слот `#footer="{ q }"`.
- `items.js` — рядки для `Picker`: `cardItems(kinds, taken?, filter?)`, `cardItem(task, taken?)`, `windowTypeItems()`, `roleItems()`, `statItems(taken?)`, `wordItems(dic)`.
- `components/StableColumns.vue` — `<StableColumns :items v-slot="{ item }">`.
- `jump.js` — `jump(id)` (розкрити, прогорнути, спалахнути) і `target` (той, хто згортає вміст, стежить за ним і розкривається).
- `rules.js` — `clauses(rule, parts)`, `pieces`, `plain`, `sentence`, `specOf`, `groups`, `sidesFor`, `ruleGroup`, `RULE_GROUP_ORDER`, `mentions`.
- `components/RuleText.vue` (`rule`, `parts`), `components/Pieces.vue` (`list`) — речення для читання.
- `catalog.js` — `vocab` (форма — T270 §14.3), `tasks`, `taskIndex`, `kidsOf`, `zones`, `kindOf(task)`, `iconOf(part)`, `roleOf(key)`, `statOf(key)`, `aliasesOf(task)`, `zoneOf`, `subzoneTitle`, `COINS`, `paramsText`, `missingParams`, `CLAIM_STATUSES`, `PAIRS`.
- `api.js` — `postPart putPart deletePart uploadShot deleteShot postClaim putClaim deleteClaim judgeClaim postRule putRule deleteRule putMyGame postRef`.
- `components/CoinBadge.vue` (`coin`, `amount`), `components/Md.vue` (`text`) — як були.

Бекенд пишеться паралельно за T270 §14 — кодуй під контракт: `vocab.roles[key] = { label, icon, group, desc, slug, coin }`, `vocab.stats = [{ key, label, icon, unit, desc, slug, coin }]`, `vocab.field = [{ key, label, type, multi?, hint?, options: { value: { label, icon, desc, slug, coin } } }]`, `vocab.level`, `vocab.args`, `vocab.kinds`; заявка — `{ id, task, part, rule, auto, params, note, link, status, verdict }`; частина — `{ id, kind: field|entity|window|menu|level, title, icon, role, task, description, screenshots, window, items, props, stats, states }`.

## Ідентифікатори для переходів

Корінь картки частини — `id="p-<id частини>"`; рядок правила — `r-<id правила>`; рядок заявки — `c-<id заявки>`. Секції (`field`, `levels`, `entities`, `rules`, `windows`, `zone-<зона>`, `drafts`) ставить `GameEditor`.

## Простий режим

`ed.simple` — студент заповнює лише сутності (іконка, назва, тип, опис, скриншот) і вікна (назва, тип, опис, скриншот): решту в цих картках і формах сховати (T270 §12).

## Хто що пише

| хто | файли в `app/vue/src/components/` |
|---|---|
| оболонка (головна сесія) | `GameEditor.vue`, `AddBar.vue`, `Hints.vue`, `MyGameForm.vue`, сторінки, `ed.js`, `items.js`, `hints.js`, `myGame.js` |
| правила | `RulesBlock.vue`, `RuleRow.vue`, `RuleForm.vue`, `RulesMatrix.vue`, `PhasesStrip.vue`, `WordPick.vue`, `ArgFields.vue` |
| заявки й сутності | `ClaimRow.vue`, `ClaimPop.vue`, `MoveTo.vue`, `CardPicker.vue`, `ProposeCard.vue`, `SlotFields.vue`, `EntitiesBlock.vue`, `EntityCard.vue`, `EntityForm.vue`, `StatsEditor.vue`, `EmojiField.vue` |
| вікна | `WindowsBlock.vue`, `WindowCard.vue`, `WindowForm.vue`, `MenuItems.vue`, `MenuForm.vue`, `ShotStrip.vue`, `GameGraph.vue`, `../graphLayout.js` |
| поле, рівні, секції | `FieldCard.vue`, `FieldForm.vue`, `FieldProps.vue`, `OptionCards.vue`, `PropsList.vue`, `LevelsBlock.vue`, `LevelCard.vue`, `LevelForm.vue`, `ZoneSection.vue`, `ClaimsTable.vue` |

Старі `ClaimChip.vue`, `ClaimZones.vue` прибере оболонка наприкінці — не видаляй і не імпортуй їх.

## Інтерфейси між авторами (пиши під них, чужого не пиши)

- `<ClaimRow :claim where? />` — рядок заявки: монетка · назва · параметри · нотатка · 🔗 · статус; клік — панель з описом картки й діями; `where` — показати, до чого привʼязана (клік — перехід). Корінь — `id="c-<id>"`.
- `<CardPicker :kinds="['mechanic']" :anchor="{ part: id }" label="механіка" :suggest="fn?" :filter="fn?" />` — фіолетова кнопка «＋ label» → панель зі списком карток цих типів; сам створює заявку з привʼязкою `anchor` (`{ part }`, `{ rule }` або `{}`), питає обовʼязкові параметри, кличе `ed.changed()`. `suggest(task)` → `true` піднімає картку нагору під заголовок «підходять сюди».
- `<ProposeCard what="новий тип вікна" all-to="/tasks?…" @done />` — міні-форма «запропонувати нове» (T270 §10.2).
- `<SlotFields :specs :params />` — поля параметрів картки (як було).
- `<StatsEditor v-model free? />` — параметри сутності; `free` — без каталогу, лише свої рядки (параметри рівня).
- `<ShotStrip :part />` — скриншоти частини: мініатюри, перегляд, додати, прибрати.
- `<EntitiesBlock ref>`, `<RulesBlock ref>`, `<WindowsBlock ref>`, `<LevelsBlock ref>` — тіло секції; кожен `defineExpose({ add })`: відкрити форму нового (у правил — `add(prefill?)`, де `prefill = { when?, cond?, then?, card? }`; `card` — slug картки, яку привʼязати до правила після збереження).
- `<FieldCard />`, `<ZoneSection :zones="['game-logic']" title hint />`, `<ClaimsTable />` — без інших пропсів.
- `<FieldProps v-model :only="[ключі]?" />` — властивості поля для форми поля і для рівня.
