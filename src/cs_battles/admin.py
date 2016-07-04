from django.contrib import admin
from cs_battles import models
## Register your models here

# Register model for battle
admin.site.register(models.BattleResponse)
admin.site.register(models.Battle)

## Register filter
from cs_battles import filters

filters.filters()
