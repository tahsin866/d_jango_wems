from django.db import models


class Division(models.Model):
    """Division model - বিভাগ"""
    id = models.BigAutoField(primary_key=True)
    dname = models.CharField(max_length=255, verbose_name="বিভাগের নাম")
    division = models.CharField(max_length=255, verbose_name="বিভাগ")
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name="ব্যবহারকারী নাম")

    class Meta:
        db_table = 'division'
        managed = False
        verbose_name = 'বিভাগ'
        verbose_name_plural = 'বিভাগসমূহ'
        ordering = ['division']

    def __str__(self):
        return self.dname or self.division


class District(models.Model):
    """District model - জেলা"""
    id = models.BigAutoField(primary_key=True)
    dname = models.CharField(max_length=255, verbose_name="জেলার নাম")
    district = models.CharField(max_length=255, verbose_name="জেলা")
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name="ব্যবহারকারী নাম")
    # Foreign key relationship with Division
    division_ref = models.ForeignKey(
        Division,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='desid',
        verbose_name="বিভাগ"
    )

    class Meta:
        db_table = 'district'
        managed = False
        verbose_name = 'জেলা'
        verbose_name_plural = 'জেলাসমূহ'
        ordering = ['district']

    def __str__(self):
        return self.dname or self.district


class Thana(models.Model):
    """Thana model - থানা"""
    id = models.BigAutoField(primary_key=True)
    dname = models.CharField(max_length=255, verbose_name="থানার নাম")
    thana = models.CharField(max_length=255, verbose_name="থানা")
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name="ব্যবহারকারী নাম")
    thana_id = models.BigIntegerField(verbose_name="থানা ID")
    # Foreign key relationship with District
    district_ref = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='des_id',
        verbose_name="জেলা"
    )

    class Meta:
        db_table = 'thana'
        managed = False
        verbose_name = 'থানা'
        verbose_name_plural = 'থানাসমূহ'
        ordering = ['thana']

    def __str__(self):
        return self.dname or self.thana