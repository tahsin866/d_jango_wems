from django.db import models

class Division(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')  # Division ID
    division = models.CharField(max_length=100, db_column='division')  # division name column
    username = models.CharField(max_length=100, null=True, blank=True)
    entdate = models.DateTimeField(null=True, blank=True)
    entyear = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'division'
        managed = False

class District(models.Model):
    desid = models.AutoField(primary_key=True, db_column='desid')  # District ID
    division = models.ForeignKey(Division, on_delete=models.CASCADE, db_column='did', to_field='id', related_name='districts')
    distserialno = models.IntegerField(null=True, blank=True)
    desname = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100)
    username = models.CharField(max_length=100, null=True, blank=True)
    entdate = models.DateTimeField(null=True, blank=True)
    entyear = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'district'
        managed = False

class Thana(models.Model):
    thana_id = models.AutoField(primary_key=True, db_column='thana_id')  # Thana ID
    district = models.ForeignKey(District, on_delete=models.CASCADE, db_column='des_id', to_field='desid', related_name='thanas')
    thana_name = models.CharField(max_length=100, null=True, blank=True)
    thana = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100, null=True, blank=True)
    ent_date = models.CharField(max_length=100, null=True, blank=True)
    ent_year = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'thana'
        managed = False