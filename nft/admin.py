from django.contrib import admin
from .models import NftImage, Collection, NftPost

# Register your models here.
admin.site.register(Collection)
admin.site.register(NftPost)


@admin.register(NftImage)
class NftImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
