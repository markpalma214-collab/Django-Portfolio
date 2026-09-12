# Django Portfolio — Osaka Night Theme

A single-page, four-section developer portfolio built with Django:

1. **Home** — profile photo, name, intro, about, social links (managed in admin)
2. **About** — skills, hobbies, personal info (managed in admin)
3. **Projects** — project grid, each card links to its GitHub repo (managed in admin)
4. **Reviews** — visitors sign in with Google to leave one review each, like/unlike other reviews, plus a social/contact section

All content on pages 1–3 and the socials on page 4 is editable from `/admin/` — you never need to touch the HTML to update your info.

---

## 1. Installation

```bash
python -m venv venv
```

Activate the virtual environment:

**Windows**
```bash
venv\Scripts\activate
```

**macOS / Linux**
```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 2. Create your `.env` file

Copy the example file:

```bash
cp .env.example .env      # macOS/Linux
copy .env.example .env    # Windows
```

Open `.env` and fill in:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

You can generate a `SECRET_KEY` with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

`.env` is listed in `.gitignore` and will never be committed.

---

## 3. Google Cloud OAuth setup

You need a Google OAuth Client ID/Secret so "Sign in with Google" actually works.

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or select an existing one).
3. Go to **APIs & Services → OAuth consent screen**.
   - Choose **External** (unless you have a Google Workspace org).
   - Fill in an app name, support email, and developer contact email.
   - Add the scopes `email` and `profile` (these are also requested automatically by allauth).
   - Add yourself as a test user if the app is still in "Testing" publishing status.
4. Go to **APIs & Services → Credentials → Create Credentials → OAuth client ID**.
   - Application type: **Web application**.
5. Under **Authorized redirect URIs**, add the callback URL that django-allauth generates for this project:

   ```
   http://127.0.0.1:8000/accounts/google/login/callback/
   ```

   (Add `http://localhost:8000/accounts/google/login/callback/` too, since some browsers treat `localhost` and `127.0.0.1` as different origins.)

6. Click **Create**. Google will show you a **Client ID** and **Client Secret**.
7. Copy both into your `.env` file:

   ```env
   GOOGLE_CLIENT_ID=xxxxxxxx.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=xxxxxxxx
   ```

No Google credentials are hardcoded anywhere in the codebase — `settings.py` reads them from environment variables via `os.getenv(...)`.

---

## 4. Django setup

Run migrations and create your admin account:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

**Important — configure the Site and Social App once, in the admin:**

1. Start the server (next step), then log in at `http://127.0.0.1:8000/admin/`.
2. Go to **Sites** and edit the one entry (id=1): set the domain to `127.0.0.1:8000` (or `localhost:8000`).
3. Go to **Social Applications → Add Social Application**:
   - Provider: **Google**
   - Name: anything, e.g. `Google`
   - Client id / Secret key: (these are already read from `.env` for the provider config, but allauth's admin-based flow also lets you register the same values here — enter the same Client ID/Secret from your `.env`)
   - Add your Site (`127.0.0.1:8000`) to **Chosen sites**
   - Save

Run the server:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`.

---

## 5. Managing your content

Log in to `/admin/` with your superuser account and manage:

- **Profile** — your name, tagline, profile picture, about text, GitHub/LinkedIn URLs
- **Skills** — one entry per skill
- **Hobbies** — one entry per hobby
- **Personal info** — free-form label/value pairs (e.g. "Location" → "Manila, PH")
- **Projects** — title, thumbnail, description, GitHub URL, technologies (comma-separated)
- **Social links** — GitHub, LinkedIn, Facebook, Instagram, Discord
- **Reviews** — moderate/delete reviews if needed

The homepage reads all of this from the database on every request, so changes in `/admin/` show up immediately — no HTML edits required.

---

## 6. How the pieces fit together

- **Authentication**: `django-allauth` handles the whole Google OAuth flow. The "Sign in with Google" buttons link to `{% provider_login_url 'google' %}`, which sends the visitor through Google, back to `/accounts/google/login/callback/`, and logs them in as a normal Django `User`.
- **One review per user**: enforced at the database level with `UniqueConstraint(fields=["user"], name="one_review_per_user")` on the `Review` model, and again at the view level (`submit_review` checks for an existing review before saving, and the template only shows the form when the user doesn't already have one).
- **Likes**: `Review.likes` is a `ManyToManyField` to the user model. The `toggle_like` view adds/removes the current user from that relation — a user can only be in the set once, so there's naturally only one like per review per user. This endpoint is a normal `@login_required` + CSRF-protected POST view; nothing is `@csrf_exempt`. The frontend JS reads the `csrftoken` cookie and sends it as an `X-CSRFToken` header.
- **Project links**: each `Project.github_url` is a plain `URLField` from the database, rendered directly (`<a href="{{ project.github_url }}">`) rather than through Django's internal `{% url %}` tag, since it points to an external site.

---

## 7. Troubleshooting common OAuth errors

**"redirect_uri_mismatch"**
The URI Google is redirecting to doesn't exactly match one of the URIs you added in Google Cloud Console. It must match character-for-character, including the trailing slash and protocol (`http` vs `https`). Double-check `http://127.0.0.1:8000/accounts/google/login/callback/`.

**"Error 400: invalid_client"**
Your `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` in `.env` don't match what's in Google Cloud Console, or the Social Application in `/admin/` has different values. Make sure both places match.

**"This app is blocked" / "Access blocked: this app's request is invalid"**
Your OAuth consent screen is still in Testing mode and your Google account isn't in the list of test users. Add your email under **OAuth consent screen → Test users**.

**Signing in works but no profile picture / name shows up**
Make sure your OAuth consent screen requests the `profile` and `email` scopes (allauth requests these by default via `SOCIALACCOUNT_PROVIDERS["google"]["SCOPE"]` in `settings.py`).

**"SocialApp matching query does not exist"**
You haven't created the **Social Application** entry in `/admin/` yet (step 4 above), or it isn't linked to the correct Site.

---

## 8. Project structure

```text
portfolio/
├── manage.py
├── portfolio/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── main/
│   ├── migrations/
│   ├── templates/main/
│   │   ├── base.html
│   │   └── index.html
│   ├── templatetags/
│   │   └── main_extras.py
│   ├── static/main/
│   │   ├── css/style.css
│   │   └── js/script.js
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── media/            (created at runtime for uploaded images)
├── static/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 9. Switching to PostgreSQL later

The models use plain Django fields with no SQLite-specific features, so migrating later is just:

1. `pip install psycopg2-binary` (or `psycopg`)
2. Update the `DATABASES` dict in `portfolio/settings.py` to point at Postgres (ideally read the connection info from more environment variables, the same way `SECRET_KEY` is read now).
3. Re-run `python manage.py migrate` against the new database.
