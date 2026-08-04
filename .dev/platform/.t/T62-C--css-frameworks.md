# T62 · Bootstrap 5 vs Tailwind: порівняння з прикладами

`2026-08-04` · 🔆 clarification

Контекст:
- запит Vitalik у [T60](T60-Q--profile-questions.md) Q1: порівняти за функціоналом/можливостями/критеріями, показати типовий код обох, порадити, що зручніше;
- вибір — [T63](T63-Q--css-framework-choice.md); v1 профілю тим часом іде на Bootstrap (статус-кво) — [T61](../../.rounds/.t/T61-R--profile-decisions.md).

## Суть різниці одним абзацом

Bootstrap — бібліотека **готових компонентів** (картка, навбар, таблиця, алерт, модалка): пишеш `class="card"` — і воно вже виглядає охайно, дизайн придуманий за тебе. Tailwind — **конструктор з утиліт** (`px-4`, `rounded-lg`, `bg-blue-600`): готових компонентів нема взагалі, кожен елемент збираєш сам з атомарних класів — повний контроль, але кожен відступ і колір — твоє рішення.

## Той самий блок «GitHub» обома

Bootstrap:

```html
<div class="card mb-3">
  <div class="card-header">GitHub</div>
  <div class="card-body">
    <label class="form-label">Посилання на репозиторій</label>
    <input class="form-control" placeholder="https://github.com/...">
    <div class="form-text">Приватний, єдиний на всі лаби.</div>
    <button class="btn btn-primary mt-3">Зберегти</button>
  </div>
</div>
```

Tailwind:

```html
<div class="mb-4 rounded-xl border border-gray-200 bg-white shadow-sm">
  <div class="border-b border-gray-200 px-4 py-2 font-medium">GitHub</div>
  <div class="p-4">
    <label class="mb-1 block text-sm font-medium text-gray-700">Посилання на репозиторій</label>
    <input class="w-full rounded-lg border border-gray-300 px-3 py-2
                  focus:border-blue-500 focus:ring-2 focus:ring-blue-200 focus:outline-none"
           placeholder="https://github.com/...">
    <p class="mt-1 text-sm text-gray-500">Приватний, єдиний на всі лаби.</p>
    <button class="mt-3 rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">Зберегти</button>
  </div>
</div>
```

Перший — коротший і «сам знає», як виглядати; другий — багатослівніший, але кожен піксель під контролем (і рамку, і фокус-кільце, і ховер ти обрав сам).

## Порівняння за критеріями

- **Швидкість для CRUD/адмінок:** Bootstrap виграє — форми, таблиці, бейджі, алерти готові; Tailwind вимагає або писати кожен елемент, або тягнути компонентний шар поверх (daisyUI, Flowbite).
- **Вигляд з коробки:** Bootstrap — «стандартно, але охайно» (твій запит дослівно); Tailwind з коробки — взагалі ніяк, скидає всі стилі до нуля.
- **Унікальність дизайну:** Tailwind виграє — свій вигляд без боротьби з чужими стилями; Bootstrap-сайти впізнавані, глибока кастомізація — через SCSS-змінні, марудно.
- **Читабельність шаблонів:** Bootstrap — семантичні класи (`btn-primary`); Tailwind — довгі рядки утиліт, у Vue це лікується винесенням у компоненти (наш `ProfileForm.vue` і так компонент — терпимо).
- **JS-віджети:** у Bootstrap в комплекті (модалки, дропдауни, колапси); Tailwind — тільки CSS, інтерактив пишеш сам чи береш headless-бібліотеку.
- **Сучасна екосистема:** тренд на боці Tailwind (нові UI-бібліотеки виходять під нього); Bootstrap стабільний, але «вчорашній».
- **Розмір бандла:** Tailwind генерує лише використані класи (менший CSS); Bootstrap тягне все (~230 КБ CSS, з gzip ~30 — на практиці байдуже).

## Чому в іншому проєкті я радив Tailwind, а тут — ні

Tailwind сильний там, де потрібен **свій** дизайн (лендинг, продукт з обличчям) або де вже стоїть компонентна бібліотека під нього. Тут — внутрішня система на форми й таблиці, мета «мінімум коду, стандартно але симпатично», і Bootstrap уже працює в репо. Для python-labs зручнішим буде **Bootstrap**: менше рішень на кожен елемент, менше рядків у шаблонах, нуль міграції. Це не «навічно»: якщо колись захочеться унікального вигляду — переїзд сторінок такого розміру дешевий.

## Твої думки та питання

> 
