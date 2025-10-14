from django.db import models


class Board(models.Model):
    id = models.BigAutoField(primary_key=True)
    board_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'board'  # Custom table name
        managed = False  # Django won't manage this table
        verbose_name = 'Board'
        verbose_name_plural = 'Boards'
        ordering = ['board_name']

    def __str__(self):
        return self.board_name or f"Board {self.id}"