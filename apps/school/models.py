from django.db import models

class School(models.Model):
    id = models.BigAutoField(primary_key=True)
    madrasha_id = models.CharField(max_length=100, null=True, blank=True)
    mtype = models.IntegerField(null=True, blank=True)
    elhaqno = models.CharField(max_length=100, null=True, blank=True)
    stage = models.IntegerField(null=True, blank=True)
    stageserial = models.IntegerField(null=True, blank=True)
    mnname = models.CharField(max_length=100, null=True, blank=True)
    ara_mname = models.CharField(max_length=100, null=True, blank=True)
    mname = models.CharField(max_length=100, null=True, blank=True)
    did = models.BigIntegerField(null=True, blank=True)
    des_id = models.BigIntegerField(null=True, blank=True)
    tid = models.BigIntegerField(null=True, blank=True)
    village = models.CharField(max_length=100, null=True, blank=True)
    post = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    enabledisable = models.SmallIntegerField(null=True, blank=True)
    year = models.SmallIntegerField(null=True, blank=True)
    mmlabel = models.CharField(max_length=100, null=True, blank=True)
    editdate = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    school_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'schools'  # Custom table name
        managed = False  # Django won't manage this table
        indexes = [
            models.Index(fields=['elhaqno', 'mobile'], name='idx_schools_elhaqno_mobile'),  # Priority index for search
            models.Index(fields=['elhaqno'], name='idx_schools_elhaqno'),  # Single field index for elhaqno
            models.Index(fields=['mobile'], name='idx_schools_mobile'),  # Single field index for mobile
            models.Index(fields=['madrasha_id', 'did', 'des_id', 'tid'], name='idx_schools_madrasha_related'),  # Related fields index
        ]

    def __str__(self):
        return self.mname
