from django.contrib import admin
from .models import QueryRecord, SentimentRecord

#@admin.site.register(QueryRecord)
#class QueryAdmin(admin.ModelAdmin):
#    list_display = ('query', 'last_updated')

#@admin.site.register(SentimentRecord)
#class SentimentAdmin(admin.ModelAdmin):
#    list_display = ('query', 'date', 'score')

admin.site.register(QueryRecord)
admin.site.register(SentimentRecord)
