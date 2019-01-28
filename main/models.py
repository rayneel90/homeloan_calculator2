from django.db import models

class Query(models.Model):
    prop_price = models.IntegerField("Asset Price",blank=True, null=True)
    other_cost = models.IntegerField("All other Costs", blank = True, null = True)
    ltv = models.FloatField("Bank Contribution",blank=True, null=True)
    roi = models.FloatField("Rate of Interest",blank=True, null=True)
    tenure = models.IntegerField("Tenure",blank=True, null=True)
    annual_early_repay = models.IntegerField("Annual Early Repay",blank=True, null=True)
    date_of_purchase = models.DateField("Date of Purchase",blank=True, null=True)
    months_to_possession = models.IntegerField("Months to possess",blank=True, null=True)
    monthly_rent_earning = models.IntegerField("Monthly Rent",blank=True, null=True)
    annual_maintenance = models.IntegerField("Annual Maintenance",blank=True, null=True)
    annual_prop_tax = models.IntegerField("Property Tax",blank=True, null=True)
    limit_80c = models.IntegerField("80c Limit",blank=True, null=True)
    self_pf_contri = models.IntegerField("Self Contribution of PF",blank=True, null=True)
    int_rebate_limit = models.IntegerField("LOH Rebate",blank=True, null=True)
    rd_rate = models.FloatField("FD interest rate",blank=True, null=True)

