import pandas as pd
pd.set_option('display.float_format', '{:,.2f}'.format)
pd.set_option('display.max_columns', 500)
from datetime import date
from dateutil.relativedelta import relativedelta




prop_price = 3.3e6
downpay = 201800+21000+1680+3.3e5
roi = 7.5
tenure = 300
annual_early_repay = 1e5
date_of_purchase = date(2019,2,2)
months_to_possession = 24
monthly_rent_earning = 12000
annual_maintenance = 30000
annual_prop_tax = 7000

limit_80c = 150000
self_pf_contri = 48600
int_rebate_limit = 200000

rd_rate = 0.075


roi = roi/1200
principal = prop_price -downpay
emi = principal * roi * (1+roi)**tenure / ((1+roi)**tenure - 1)
tax_rebate_princi_limit = (limit_80c - self_pf_contri)


dat = [{'date': date_of_purchase, 'pos': None, 'emi': None, 'interest_paid': None,
        'principle_repaid': None, 'Extra_repaid': downpay, 'prop_tax': None,
        'maintenance': None, 'rent': None, 'tax save on principal': None}]
int_accumulate = 0
for month in range(1,months_to_possession):
    date = date_of_purchase + relativedelta(months=month)
    interest = principal * roi
    int_accumulate += interest
    dat.append({'date': date, 'pos': principal, 'emi': interest,
                      'interest_paid': interest,
                      'principle_repaid': None,
                      'extra_repaid': None, 'prop_tax': None,
                      'maintenance': None, 'rent': None,
                      'tax save on principal': None,
                      "tax save on interest": None,
                      'unclaimed_int_amnt': int_accumulate,
                })
df = pd.DataFrame(dat)


date_of_possess = date + relativedelta(months=1)
months_in_fy = 4 - date_of_possess.month if date_of_possess.month < 4 \
    else 16 - date_of_possess.month

dat = []
for month in range(months_in_fy):
    date = date + relativedelta(months=1)
    interest = principal * roi
    emi = min(emi, principal + interest)
    princi_repay = emi - interest
    extra_repay = 0 if month < months_in_fy-1 else annual_early_repay
    principal = max(0, principal-princi_repay-extra_repay)
    rent = round(monthly_rent_earning*1.1**((month+1)//22)/100)*100
    property_tax = 0 if month < months_in_fy-1 else annual_prop_tax
    dat.append({
        'date': date, 'pos': principal, 'emi': emi,
        'interest_paid': interest, 'principle_repaid': princi_repay,
        'extra_repaid': extra_repay, 'prop_tax': property_tax,
        'maintenance': annual_maintenance / 12, 'rent': rent,
    })
df_fy1 = pd.DataFrame(dat)

total_principal_repaid = df_fy1.principle_repaid.sum() + df_fy1.extra_repaid.sum()
df_fy1['tax_save_princi'] = min(tax_rebate_princi_limit, total_principal_repaid) * .3 / df_fy1.shape[0]

loss_on_house = (df_fy1.interest_paid + df_fy1.maintenance +
                 df_fy1.prop_tax - df_fy1.rent).sum()
if loss_on_house > int_rebate_limit:
    int_accumulate += loss_on_house-int_rebate_limit
else:
    int_rebate_limit -= int_rebate_limit-loss_on_house
loss_on_house = int_rebate_limit
df_fy1['tax_save_interest'] = loss_on_house * .3 / df_fy1.shape[0]
df_fy1['unclaimed_int_amnt'] = int_accumulate
df2 = df.append(df_fy1)
while principal:
    for index in range(12):

loss_on_house = interest + annual_maintenance + property_tax - rent
max_int_rebate = int_rebate_limit / tax_months if month <= tax_months else int_rebate_limit / 12
if month < 96:
    if loss_on_house <= max_int_rebate:
        if int_accumulate:
            int_accumulate -= min(int_accumulate, max_int_rebate - loss_on_house)
            loss_on_house += min(int_accumulate, max_int_rebate - loss_on_house)
    else:
        int_accumulate += loss_on_house - max_int_rebate
        loss_on_house = max_int_rebate
else:
    loss_on_house = min(loss_on_house, max_int_rebate)
