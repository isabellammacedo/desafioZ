from django.contrib import admin
from .models import Company, Document, Signers


admin.site.register(Company)
admin.site.register(Document)
admin.site.register(Signers)