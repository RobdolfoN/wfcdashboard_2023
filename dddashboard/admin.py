from django.contrib import admin

# Register your models here.

from .models import *
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Count
from django.contrib.admin.filters import DateFieldListFilter

# admin.site.register(Customer)
admin.site.register(Dashboard_user)
# admin.site.register(CompanyData)
admin.site.register(CompanyName)
# admin.site.register(Tag)
# admin.site.register(Order)

class YearCreatedFilter(admin.SimpleListFilter):
    title = 'year created'  # or use _('year created') for translation
    parameter_name = 'year_created'

    def lookups(self, request, model_admin):
        # Return a list of tuples. Each tuple is a pair of (value, verbose name)
        return [(str(year), str(year)) for year in range(2015, 2031)]

    def queryset(self, request, queryset):
        if self.value():
            # Filter the queryset based on the selected year
            return queryset.filter(year_created__year=self.value())


class CompanyDataAdmin(admin.ModelAdmin):
    list_filter = (YearCreatedFilter,)  # Use the custom filter

# Re-register CompanyData with the custom admin class
admin.site.register(CompanyData, CompanyDataAdmin)