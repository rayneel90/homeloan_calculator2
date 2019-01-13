from django.db import models

class Query(models.Model):
    price = models.IntegerField("Asset Price", )
    downpay = models.IntegerField("Downpayment")
    roi = models.FloatField("Rate of Interest")
    tenure = models.IntegerField("Tenure")
    early_repay = models.IntegerField("Annual Early Repay")
    # rent_earning = models.IntegerField()
    # maintenance = models.IntegerField()
    # prop_tax = models.IntegerField()
    # tax_80c = models.IntegerField()
    # self_pf_contri = models.IntegerField()
    # tax_rebate_int = models.IntegerField()
    # rd_rate = models.FloatField()
