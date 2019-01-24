import pandas as pd
pd.set_option('display.float_format', '{:,.2f}'.format)
pd.set_option('display.max_columns', 500)
from datetime import date
from dateutil.relativedelta import relativedelta

################################################################################
#                                  Inputs                                      #
################################################################################

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



################################################################################
#                                     EMI                                      #
################################################################################


# def calculation(price=3.5e6, downpay = 3e6, roi =0,tenure = 300,\
#                 early_repay = 1e5, time_to_possession = 24, rent_earning = 12000,
#                 maintenance = 30000,
#                 prop_tax = 7000,self_pf_contri = 48600,
#                 tax_rebate_int = 200000,rd_rate = 0.075, **kwargs):

roi = roi/1200
principal = prop_price -downpay
emi = principal * roi * (1+roi)**tenure / ((1+roi)**tenure - 1)
tax_princi = (limit_80c - self_pf_contri)/12

month_of_possession = date_of_purchase + relativedelta(months=months_to_possession)

tax_months = 4 - month_of_possession.month if month_of_possession.month < 4 \
    else 16 - month_of_possession.month

################################################################################
#                                    POS                                       #
################################################################################
premi_dat = [{'month': 0, 'pos': None, 'emi': None, 'interest_paid': None,
         'principle_repaid': None,
         'Extra_repaid': downpay, 'prop_tax': None,
         'maintenance': None, 'rent': None, 'tax save on principal': None}]
int_accumulate = 0
fy = date_of_purchase.year if date_of_purchase.month < 4 else date_of_purchase.year + 1
fm = (date_of_purchase.month + 9) % 12  # convert julian month to fiscal month
fm = fm if fm else 12  # replace month 0 with month 12

for index in range(1, months_to_possession):
    date = date_of_purchase + relativedelta(months=index)
    interest = principal * roi
    int_accumulate += interest
    premi_dat.append({'month': 0, 'pos': principal, 'emi': interest,
                      'interest_paid': interest,
                      'principle_repaid': None,
                      'Extra_repaid': None, 'prop_tax': None,
                      'maintenance': None, 'rent': None,
                      'tax save on principal': None,
                      "tax save on interest": None,
                      'unclaimed_int_amnt': int_accumulate,
                      })
premi_dat = pd.DataFrame(premi_dat)


month = 1
dat = []

while principal:
    interest = principal * roi
    emi = min(emi, principal + interest)
    princi_repay = emi - interest
    extra_repay = 0 if month % 12 else annual_early_repay
    principal = max(0, principal-princi_repay-extra_repay)
    rent = round(monthly_rent_earning*(1.1)**(max(0, month-months_to_possession)//24)/100)*100
    property_tax = 0 if month % 12 else annual_prop_tax
    tax_save_princi = min(tax_princi,princi_repay+extra_repay)*.3
    loss_on_house = interest + annual_maintenance + property_tax - rent
    max_int_rebate = int_rebate_limit / tax_months if month <= tax_months else int_rebate_limit/12
    if month < 96:
            if loss_on_house <= max_int_rebate:
                if int_accumulate :
                    int_accumulate -= min(int_accumulate, max_int_rebate - loss_on_house)
                    loss_on_house += min(int_accumulate, max_int_rebate - loss_on_house)
            else:
                int_accumulate += loss_on_house - max_int_rebate
                loss_on_house = max_int_rebate
    else:
        loss_on_house = min(loss_on_house, max_int_rebate)
    dat.append({
        'month': month+ months_to_possession, 'pos': principal, 'emi': emi,
        'interest_paid': interest, 'principle_repaid': princi_repay,
        'Extra_repaid': extra_repay, 'prop_tax': property_tax,
        'maintenance': annual_maintenance / 12, 'rent': rent,
        'tax save on principal': tax_save_princi,
        "tax save on interest": loss_on_house * .3,
        'unclaimed_int_amnt': int_accumulate
    })
    month += 1
dat = pd.DataFrame(dat)
dat = premi_dat.append(dat)
dat = dat[['month', 'pos', 'emi', 'interest_paid', 'principle_repaid',
           'Extra_repaid', 'prop_tax', 'rent', 'maintenance',
           'tax save on principal', "tax save on interest", 'unclaimed_int_amnt']]
dat = dat.to_csv('temp.csv')
