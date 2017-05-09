from django.db import models

# Create your models here.

class Schema(models.Model):

    schema_name = models.CharField(max_length=250)

class Table(models.Model):
    
    schema = models.ForeignKey('Schema', on_delete=models.CASCADE)
    table_name = models.CharField(max_length=250)

class TableField(models.Model):

    table = models.ForeignKey('Table', on_delete=models.CASCADE)
    field_name = models.CharField(max_length=250)
    allow_null = models.BooleanField(default=False)
    inner_type = models.CharField(max_length=250, default="")

class ForeignKey(models.Model):

    constraint_name = models.CharField(max_length=250)
    on_table = models.ForeignKey('Table', on_delete=models.CASCADE, related_name='on_table')
    to_table = models.ForeignKey('Table', on_delete=models.CASCADE, related_name='to_name')