# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Cheltuieli(models.Model):
    id_cheltuiala = models.AutoField(primary_key=True)
    id_eveniment = models.ForeignKey('Evenimente', models.DB_CASCADE, db_column='id_eveniment')
    descriere = models.CharField(max_length=255)
    suma = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'cheltuieli'


class Evenimente(models.Model):
    id_eveniment = models.AutoField(primary_key=True)
    titlu = models.CharField(max_length=150)
    data = models.DateTimeField()
    buget = models.DecimalField(max_digits=10, decimal_places=2)
    capacitate = models.IntegerField()
    pret_baza_bilet = models.DecimalField(max_digits=10, decimal_places=2)
    cost_variabil_om = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.titlu
    class Meta:
        managed = False
        db_table = 'evenimente'


class Feedback(models.Model):
    id_feedback = models.AutoField(primary_key=True)
    id_eveniment = models.ForeignKey(Evenimente, models.DB_CASCADE, db_column='id_eveniment')
    mesaj = models.TextField()
    scor_sentiment = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feedback'


class Mese(models.Model):
    id_masa = models.AutoField(primary_key=True)
    id_eveniment = models.ForeignKey(Evenimente, models.DB_CASCADE, db_column='id_eveniment')
    nume_masa = models.CharField(max_length=100)
    capacitate_maxima = models.IntegerField()

    def __str__(self):
            return self.nume_masa
    class Meta:
        managed = False
        db_table = 'mese'


class Participanti(models.Model):
    id_participant = models.AutoField(primary_key=True)
    id_eveniment = models.ForeignKey(Evenimente, models.DB_CASCADE, db_column='id_eveniment')
    id_masa = models.ForeignKey(Mese, models.DB_SET_NULL, db_column='id_masa', blank=True, null=True)
    nume = models.CharField(max_length=150)
    email = models.CharField(max_length=100, blank=True, null=True)
    status_rsvp = models.CharField(max_length=50)
    cod_qr = models.CharField(max_length=255, blank=True, null=True)
    bilet_platit = models.IntegerField()

    def __str__(self):
        return self.nume
    
    class Meta:
        managed = False
        db_table = 'participanti'


class Utilizatori(models.Model):
    id_utilizator = models.AutoField(primary_key=True)
    nume_utilizator = models.CharField(unique=True, max_length=50)
    parola = models.CharField(max_length=255)
    nume_complet = models.CharField(max_length=100)
    rol = models.CharField(max_length=50)

    def __str__(self):
            return self.nume_complet
    class Meta:
        managed = False
        db_table = 'utilizatori'
