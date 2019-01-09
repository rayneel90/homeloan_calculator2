from django.db import models

class Query(models):
    Price = models.IntegerField()
    ltv = models.FloatField()
    roi = models.FloatField()
    tenure = models.IntegerField()
    early_repay = models.IntegerField()
    rent_earning = models.IntegerField()
    maintenance = models.IntegerField()
    prop_tax = models.IntegerField()
    tax_80c = models.IntegerField()
    self_pf_contri = models.IntegerField()
    tax_rebate_int = models.IntegerField()
    rd_rate = models.FloatField()
