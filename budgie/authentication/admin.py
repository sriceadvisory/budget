from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.apps import apps
from django.utils.module_loading import import_module
from .models import User

admin.site.register(User)

# Ensure the token_blacklist app has a chance to register
try:
    import_module("rest_framework_simplejwt.token_blacklist.admin")
except Exception:
    pass

# Unregister token models from admin 
for model_name in ("OutstandingToken", "BlacklistedToken"):
    try:
        model = apps.get_model("token_blacklist", model_name)
        admin.site.unregister(model)
    except (LookupError, NotRegistered):
        pass