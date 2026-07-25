# T43 · Покрокова інструкція: Google OAuth-клієнт

`2026-07-25` · 🔆 clarification

Контекст:
- [T40](T40-Q--auth-mvp-questions.md) Q6: GCP-акаунта нема, потрібна інструкція; секрети не проходять через чат/репо.

## Кроки (≈10 хвилин, білінг не потрібен)

1. **Консоль:** зайди на console.cloud.google.com з **2vitalik@gmail.com** (раджу особистий акаунт, не @nure.ua — університетські Workspace нерідко забороняють створювати GCP-проєкти). Прийми умови.
2. **Проєкт:** селектор проєктів угорі → New Project → назва, напр. `nure-labs` → Create; переконайся, що новий проєкт вибрано.
3. **Consent screen:** меню ☰ → APIs & Services → OAuth consent screen (у новій консолі розділ зветься «Google Auth Platform»). Тип аудиторії — **External**; App name — напр. «NURE Labs»; support/contact email — твій. Додаткові скоупи не додавати (базові openid/email/profile і так є).
4. **Тест-користувачі:** розділ Audience → Test users → додай свою @nure.ua-пошту. Поки апка в режимі Testing, входити можуть лише перелічені акаунти.
5. **OAuth-клієнт:** APIs & Services → Credentials → Create Credentials → **OAuth client ID** → Application type: **Web application**, назва `nure-labs-web`. Authorized redirect URIs — додай два:
   - `http://localhost:8000/api/auth/callback`
   - `http://localhost:5173/api/auth/callback`
   (бекенд напряму і через Vite-proxy у деві; порти узгоджені з планом [T44](T44--auth-mvp/plan.md) — міняються лише разом.) JavaScript origins лишай порожніми — flow серверний.
6. **Секрети:** після Create зʼявляться Client ID і Client secret → внеси їх у `app/backend/.env` (файл-шаблон `.env.example` буде в репо; сам `.env` — git-ignored). У чат не вставляй.
7. **На потім (деплой):** додати `https://<домен>/api/auth/callback` у redirect URIs і натиснути **Publish app** — зніме ліміт 100 тест-користувачів; для базових скоупів верифікація Google не потрібна.

## Твої думки та питання

> 
