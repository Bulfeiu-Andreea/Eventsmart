from django.contrib import admin
from .models import Evenimente, Cheltuieli, Feedback, Mese, Participanti, Utilizatori

# Înregistrăm modelele în panoul de admin
admin.site.register(Evenimente)
admin.site.register(Cheltuieli)
admin.site.register(Feedback)
admin.site.register(Mese)
admin.site.register(Participanti)
admin.site.register(Utilizatori)
