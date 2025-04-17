# test_env.py (save in project root)
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ChatApp.settings")

import django
django.setup()

print("✅ Django loaded properly with settings.")
