# Emergency QR

A simple Django project that generates emergency-information QR codes for users, saves the QR image, and emails the QR to the user after registration. Scan the QR code to view the person's emergency details (name, age, blood group, address, emergency contact, medical conditions).

## Features

- Register a user with emergency contact information via a simple form
- Automatically generate a QR code that links to a public emergency details page
- Save generated QR images to `media/qr_codes/`
- Email the QR code image to the registered user

## Tech stack

- Python 3.x
- Django 5.1.6
- qrcode (library) + pillow for image handling

Dependencies are listed in `requirement.txt`.

## Quick start (local development)

1. Clone the repo and change directory

	```bash
	git clone <repo-url>
	cd emergency_qr
	```

2. Create a virtual environment and activate it

	```bash
	python3 -m venv .venv
	source .venv/bin/activate
	```

3. Install dependencies

	```bash
	pip install -r requirement.txt
	```

4. Set environment variables (use a `.env` file or export in your shell). At minimum provide:

	- SECRET_KEY — Django secret key
	- EMAIL_HOST_USER — SMTP username (used to send QR emails)
	- EMAIL_HOST_PASSWORD — SMTP password (app password when using Gmail)

	Example `.env` (not checked into source control):

	```env
	SECRET_KEY=your_secret_key_here
	EMAIL_HOST_USER=your-email@example.com
	EMAIL_HOST_PASSWORD=your-email-password-or-app-password
	```

5. Run migrations and start the development server

	```bash
	python manage.py migrate
	python manage.py runserver
	```

6. Open http://127.0.0.1:8000/ (or `/register/`) to register a user and generate a QR code.

Notes:
- The app stores generated QR images under `media/qr_codes/`.
- Email sending is configured in `settings.py` via SMTP (Gmail settings are included). For Gmail, use an app password or configure the account to allow SMTP access.

## Routes

- `/` or `/register/` — register form to create emergency info and generate QR
- `/emergency/<uuid:user_id>/` — public page that shows emergency details for the given UUID (this is the URL encoded into the QR)

## Project structure (key files)

- `emergency_info/models.py` — `EmergencyInfo` model, QR generation and email sending are implemented here
- `emergency_info/views.py` — registration view and emergency detail view
- `emergency_info/urls.py` — app routes
- `emergency_info/templates/` — `register.html` and `emergency_info.html`
- `emergency_qr/settings.py` — Django settings (EMAIL_BACKEND, MEDIA settings, installed apps)

## Deployment notes

- A `vercel.json` file is present in the repository; deploying a Django app to Vercel requires configuring a WSGI/ASGI adapter or using serverless approach. Alternatively, consider deploying to platforms that natively support Django apps (Heroku, Railway, Render, etc.).
- Remember to set `DEBUG=False` and configure `ALLOWED_HOSTS` and secure environment variables in production.

## Tests

There are no automated tests included yet. Adding basic tests for model creation and the views would be recommended as a next step.

## Security & privacy

- Do not commit `.env` or any secrets to source control. Use environment variables in CI/CD or your hosting provider's secrets manager.
- Be mindful that the emergency details page is public to anyone with the QR link; consider adding access controls or expiring links if privacy is required.

## Next steps / suggestions

- Add unit tests for model save logic (QR generation) and views
- Add an admin or user dashboard for managing entries and re-sending QR emails
- Add rate-limiting and validation for registration form

## License & contact

This repository does not include a license file. Add a LICENSE if you intend to make this project public.

For questions or contributions, open an issue or pull request in the repository.

