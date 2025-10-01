from django.db import models
from apps.admin.CentralExam.models import ExamSetup

class RegistrationOverview(models.Model):
    exam_setup = models.ForeignKey(
        ExamSetup,
        on_delete=models.CASCADE,
        db_column='exam_setup_id',
        related_name='registration_overviews'
    )
    marhala = models.ForeignKey(
        'subject.Marhala',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='marhala_id',
        related_name='registration_overviews'
    )
    reg_date_from = models.DateField()
    reg_date_to = models.DateField()
    reg_regular_fee = models.DecimalField(max_digits=10, decimal_places=2)
    reg_irregular_jemni = models.DecimalField(max_digits=10, decimal_places=2)
    reg_irregular_manonnoyon = models.DecimalField(max_digits=10, decimal_places=2)
    reg_irregular_others = models.DecimalField(max_digits=10, decimal_places=2)
    late_date_from = models.DateField()
    late_date_to = models.DateField()
    late_regular_fee = models.DecimalField(max_digits=10, decimal_places=2)
    late_irregular_jemni = models.DecimalField(max_digits=10, decimal_places=2)
    late_irregular_manonnoyon = models.DecimalField(max_digits=10, decimal_places=2)
    late_irregular_others = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'exam_fees'
        managed = False

    def __str__(self):
        return f"{self.exam_setup.exam_name} Overview"
