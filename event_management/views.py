from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Evenimente, Cheltuieli, Participanti

@login_required
def dashboard_organizator(request):
    eveniment = Evenimente.objects.first()
    
    cheltuieli_totale = 0
    if eveniment:
        cheltuieli_lista = Cheltuieli.objects.filter(id_eveniment=eveniment.id)
        cheltuieli_totale = sum(float(c.suma) for c in cheltuieli_lista if c.suma)

    pret_bilet = getattr(eveniment, 'pret_baza_bilet', 50) if eveniment else 50
    cost_variabil = getattr(eveniment, 'cost_variabil_persoana', 15) if eveniment else 15
    costuri_fixe = cheltuieli_totale

    break_even_bilete = 0
    if (pret_bilet - cost_variabil) > 0:
        break_even_bilete = costuri_fixe / (pret_bilet - cost_variabil)

    etichete, venituri, cheltuieli_grafic = genereaza_date_grafic_economic(eveniment)

    context = {
        'eveniment': eveniment,
        'cheltuieli_totale': cheltuieli_totale,
        'break_even_bilete': round(break_even_bilete),
        'grafic_etichete': etichete,
        'grafic_venituri': venituri,
        'grafic_cheltuieli': cheltuieli_grafic,
    }

    return render(request, 'dashboard.html', context)

def calculeaza_pret_dinamic(eveniment, numar_participanti):
    capacitate = getattr(eveniment, 'capacitate', 100)
    pret_baza = getattr(eveniment, 'pret_baza_bilet', 50)
    
    bilete_ramase = capacitate - numar_participanti
    procent_ramas = (bilete_ramase / capacitate) * 100
    
    pret_final = pret_baza
    if procent_ramas <= 10:
        pret_final = pret_baza * 1.25
    elif procent_ramas <= 30:
        pret_final = pret_baza * 1.10
        
    return round(pret_final, 2)

from .models import Mese

def atribuie_participant_la_masa(id_masa, id_participant):
    masa = Mese.objects.filter(id=id_masa).first()
    if not masa:
        return "Masa nu există."
    
    capacitate_maxima = getattr(masa, 'capacitate', 8)
    participanti_actuali = Participanti.objects.filter(id_masa=id_masa).count()
    
    if participanti_actuali >= capacitate_maxima:
        return "Masa este plină!"
    
    participant = Participanti.objects.filter(id=id_participant).first()
    if participant:
        participant.id_masa = id_masa
        participant.save()
        return "Participant atribuit cu succes la masă."
    
    return "Participantul nu există."

def genereaza_date_grafic_economic(eveniment):
    if not eveniment:
        return [], [], []
    
    capacitate = getattr(eveniment, 'capacitate', 100)
    pret_bilet = getattr(eveniment, 'pret_baza_bilet', 50)
    cost_variabil = getattr(eveniment, 'cost_variabil_persoana', 15)
    
    cheltuieli_lista = Cheltuieli.objects.filter(id_eveniment=eveniment.id)
    costuri_fixe = sum(float(c.suma) for c in cheltuieli_lista if c.suma)
    
    etichete_bilete = []
    venituri_totale = []
    cheltuieli_totale_grafic = []
    
    pas = max(1, capacitate // 10)
    for x in range(0, capacitate + 1, pas):
        etichete_bilete.append(x)
        venituri_totale.append(x * pret_bilet)
        cheltuieli_totale_grafic.append(costuri_fixe + (x * cost_variabil))
        
    return etichete_bilete, venituri_totale, cheltuieli_totale_grafic