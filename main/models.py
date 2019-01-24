from django.db import models

class Query(models.Model):
    prop_price = models.IntegerField("Asset Price", )
    downpay = models.IntegerField("Downpayment")
    roi = models.FloatField("Rate of Interest")
    tenure = models.IntegerField("Tenure")
    annual_early_repay = models.IntegerField("Annual Early Repay")
    date_of_purchase = models.DateField("Date of Purchase")
    months_to_possession = models.IntegerField("Months to possess")
    monthly_rent_earning = models.IntegerField()
    annual_maintenance = models.IntegerField()
    annual_prop_tax = models.IntegerField()
    limit_80c = models.IntegerField()
    self_pf_contri = models.IntegerField()
    int_rebate_limit = models.IntegerField()
    rd_rate = models.FloatField()
