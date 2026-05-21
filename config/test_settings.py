import re

from django.db.models.signals import class_prepared


def _remove_schema_prefix(sender, **_kwargs):
    db_table = sender._meta.db_table
    if not db_table or '"' not in db_table or "." not in db_table:
        return
    m = re.match(r'^"(\w+)"\."(\w+)"$', db_table)
    if m:
        sender._meta.db_table = m.group(2)
        return
    m = re.match(r'^(\w+)"\."(\w+)$', db_table)
    if m:
        sender._meta.db_table = m.group(2)


class_prepared.connect(_remove_schema_prefix)

from config.settings import *  # noqa: F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

SECRET_KEY = "django-insecure-test-key-not-used-in-production-abcdef1234567890xyz"

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
