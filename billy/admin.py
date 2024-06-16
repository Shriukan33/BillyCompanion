from django.contrib import admin
from .models import Stat, BillyClass, Item, Billy, BillyStat, Adventure, ItemEffect


class StatAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]


class BillyClassAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]


class ItemEffectInline(admin.TabularInline):
    model = ItemEffect
    extra = 0


class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "type"]
    inlines = [ItemEffectInline]
    list_filter = ["books", "type"]


class ItemEffectAdmin(admin.ModelAdmin):
    list_display = ["item", "stat", "value", "description"]


class BillyStatInline(admin.TabularInline):
    model = BillyStat
    extra = 0


class BillyAdmin(admin.ModelAdmin):
    list_display = ["name", "billy_class"]
    inlines = [BillyStatInline]


class AdventureAdmin(admin.ModelAdmin):
    list_display = ["book", "billy"]


admin.site.register(Stat, StatAdmin)
admin.site.register(BillyClass, BillyClassAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Billy, BillyAdmin)
admin.site.register(Adventure, AdventureAdmin)
admin.site.register(ItemEffect, ItemEffectAdmin)
