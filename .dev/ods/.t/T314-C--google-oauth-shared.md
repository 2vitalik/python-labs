# T314 · Google OAuth: один проєкт на всі сайти

`2026-11-16` · 🔆 clarification

Контекст:
- рішення Vitalik у чаті 2026-11-17: один Google Cloud проєкт (номер `616100985001` — з `client_id` python і в проді, і в деві; назва `nure-labs` з [T43](../../platform/.t/T43-C--gcp-oauth-setup.md) була лише прикладом — не покладатися) на python, ods і майбутній oop; назва на екрані входу — спільна, нейтральна; клієнт — свій на кожен сайт (як [T181](T181-Q--ods-deploy-choices.md) Q3 a);
- уточнює крок 0.2 [T252](T252-C--ods-deploy-checklist.md): той самий проєкт, але спершу — назва.

## Що видно зараз (перевірено 2026-11-17)

- Вхід на python.labs.in.ua → Google пише «Перейти в додаток **Python Labs**»; контакт розробника на екрані — пошта підтримки з Branding.
- Назву й логотип Google бере з **проєкту** (Branding), не з клієнта — тому всі клієнти проєкту показують одне імʼя.
- Ключі на сайт — пара `GOOGLE_CLIENT_ID` + `GOOGLE_CLIENT_SECRET` з клієнта; адреса повернення в клієнті має збігатися до символу.

## Кроки в консолі (≈10 хв)

Посилання — з номером проєкту, відкривають одразу потрібний.

1. **Назва** — [Branding](https://console.cloud.google.com/auth/branding?project=616100985001): App name → нейтральна (напр. «Лабораторні ХНУРЕ» або «labs.in.ua»); логотип, якщо є з python, — прибрати; Home page / Privacy policy, якщо вказують на python, — лишити (той самий домен) або очистити; Authorized domains — `labs.in.ua` (є чи додати). Save.
   - Застереження Google: назву й логотип на екрані входу показує лише перевірений бренд; без перевірки — домен. Якщо після Save на сторінці зʼявиться «Verify branding» чи статус «потребує перевірки» — не тиснути, а сказати мені: перевірка хоче домашню сторінку з тією самою назвою й політику приватності, і це окреме рішення.
2. **Аудиторія** — [Audience](https://console.cloud.google.com/auth/audience?project=616100985001): лише глянути. Виявилось **Internal** (проєкт належить організації nure.ua): входять лише акаунти @nure.ua, «Testing / In production» і перевірки бренду для Internal немає — назва показується одразу. Нічого не міняти; зовнішня пошта (gmail) не ввійде навіть з `ADMIN_EMAILS`.
3. **Клієнт ODS** — [Clients](https://console.cloud.google.com/auth/clients?project=616100985001) → Create client ([одразу форма](https://console.cloud.google.com/auth/clients/create?project=616100985001)) → Web application → назва `ods-labs prod` → Authorized redirect URIs: `https://ods.labs.in.ua/api/auth/callback` (без слеша в кінці; JavaScript origins — порожньо) → Create.
   - **Secret Google показує один раз**, у момент створення: одразу — в 1Password `ods-labs Google OAuth (prod)` (ID і secret). Загубився — не відновити, лише новий секрет у тому ж клієнті.
4. Необовʼязково: клієнт python перейменувати на `python-labs prod` — для порядку, на вхід не впливає.
5. Дев-клієнт `nure-labs-web` не чіпати: ods локально входить через `FAKE_USER_EMAIL`.
6. OOP згодом — лише крок 3 зі своєю адресою `https://<домен oop>/api/auth/callback`.

## Що міняється поза консоллю

- Python: нічого — ключі й `.env` на сервері ті самі.
- ODS: ID і secret — у `vv env edit ods-labs` за [T252](T252-C--ods-deploy-checklist.md) (ID у редакторі, secret — прихованим вводом).
- Код: нічого.

## Перевірка

- 2026-11-17: кроки 1–3 Vitalik зробив; сторінка входу python одразу показує «Перейти в додаток (nure).labs.in.ua» — назву ще можуть змінити на «NURE Labs» (рада в чаті: дужки студенту незрозумілі). Клієнт `ods-labs prod` створено.

Після Save у Branding — відкрити вхід на python.labs.in.ua: має бути нова назва (кілька хвилин на оновлення допустимо). Перевірити можу й я: адреса `/api/auth/login` → сторінка Google → назва додатка в ній.

## Твої думки та питання

> 
