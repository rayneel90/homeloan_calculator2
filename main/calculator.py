import pandas as pd
pd.set_option('display.float_format', '{:,.2f}'.format)
pd.set_option('display.max_columns', 500)
from datetime import date
from dateutil.relativedelta import relativedelta

################################################################################
#                                   Inputs                                     #
################################################################################
#
prop_price = 3.3e6
downpay = 201800+1680+3.3e5
roi = 7.9
tenure = 180
annual_early_repay = 1e5
date_of_purchase = date(2019,2,5)
months_to_possession = 24
monthly_rent_earning = 12000
annual_maintenance = 30000
annual_prop_tax = 7000
premi = False
limit_80c = 150000
self_pf_contri = 48600
int_rebate_limit = 200000

rd_rate = 7.5


################################################################################
#                              EMI Computation                                 #
################################################################################

def calculation(prop_price = 3.3e6 , other_cost = 201800+1680+3.3e5, ltv = 80, roi = 7.9, tenure = 180, annual_early_repay = 1e5,
                date_of_purchase=date(2019, 2, 5), months_to_possession = 24, monthly_rent_earning = 12000 ,
                annual_maintenance=30000, annual_prop_tax = 7000 , limit_80c = 150000 , self_pf_contri = 48600,
                int_rebate_limit=200000, rd_rate = 7.5, premi=False, **kwargs):
    roi /= 1200
    ltv /= 100
    principal = prop_price * (ltv)
    EMI = principal * roi * (1+roi)**tenure / ((1+roi)**tenure - 1)
    tax_rebate_princi_limit = (limit_80c - self_pf_contri)
    rd_rate /= 100


    dat = [{'date': date_of_purchase, 'pos': principal, 'emi': 0, 'interest_paid': 0,
            'principle_repaid': 0, 'extra_repaid': other_cost + principal * (1-ltv), 'prop_tax': 0,
            'maintenance': 0, 'rent': 0, 'tax_save_princi': 0, 'tax_save_interest': 0}]
    int_accumulate = 0
    for month in range(1,months_to_possession):
        date = date_of_purchase + relativedelta(months=month)
        if premi:
            interest = principal * roi
            emi = interest
            princi_repay = 0
            princi_tax = 0
        else:
            interest = principal * roi
            emi = min(EMI, principal + interest)
            princi_repay = emi - interest
            princi_tax = min(tax_rebate_princi_limit/12,princi_repay) * .3
            principal -= princi_repay
        int_accumulate += interest
        dat.append({'date': date, 'pos': principal, 'emi': emi,
                          'interest_paid': interest,
                          'principle_repaid': princi_repay,
                          'extra_repaid': 0, 'prop_tax': 0,
                          'maintenance': 0, 'rent': 0,
                          'tax_save_princi': princi_tax,
                          "tax_save_interest": 0,
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
        rent = round(monthly_rent_earning*1.1**((month+1)//22)/100)*100
        property_tax = 0 if month < months_in_fy-1 else annual_prop_tax
        principal = max(0, principal - princi_repay - extra_repay)
        dat.append({
            'date': date, 'pos': principal, 'emi': emi,
            'interest_paid': interest, 'principle_repaid': princi_repay,
            'extra_repaid': extra_repay, 'prop_tax': property_tax,
            'maintenance': annual_maintenance / 12, 'rent': rent,
        })
    df_fy1 = pd.DataFrame(dat)

    total_principal_repaid = df_fy1.principle_repaid.sum() + df_fy1.extra_repaid.sum()
    df_fy1['tax_save_princi'] = min(tax_rebate_princi_limit/12, total_principal_repaid/df_fy1.shape[0]) * .3

    loss_on_house = (df_fy1.interest_paid + df_fy1.maintenance +
                     df_fy1.prop_tax - df_fy1.rent).sum()
    if loss_on_house > int_rebate_limit:
        int_accumulate += loss_on_house - int_rebate_limit
        loss_on_house = int_rebate_limit
    else:
        int_accumulate -= min(int_accumulate, int_rebate_limit - loss_on_house)
        loss_on_house += min(int_accumulate, int_rebate_limit - loss_on_house)
    loss_on_house = int_rebate_limit
    df_fy1['tax_save_interest'] = loss_on_house * .3 / df_fy1.shape[0]
    df_fy1['unclaimed_int_amnt'] = int_accumulate
    df = df.append(df_fy1)
    fy = 1
    while principal:
        fy += 1
        dat = []
        for index in range(12):
            month +=1
            date = date + relativedelta(months=1)
            interest = principal * roi
            emi = min(emi, principal + interest)
            princi_repay = emi - interest
            extra_repay = 0 if index < 11 else annual_early_repay
            rent = round(monthly_rent_earning * 1.1 ** (month  // 22) / 100) * 100
            property_tax = 0 if index < 11 else annual_prop_tax
            principal = max(0, principal - princi_repay - extra_repay)
            dat.append({
                'date': date, 'pos': principal, 'emi': emi,
                'interest_paid': interest, 'principle_repaid': princi_repay,
                'extra_repaid': extra_repay, 'prop_tax': property_tax,
                'maintenance': annual_maintenance / 12, 'rent': rent,
            })
            if not principal:
                break
        df_fy = pd.DataFrame(dat)
        total_principal_repaid = df_fy.principle_repaid.sum() + df_fy.extra_repaid.sum()
        df_fy['tax_save_princi'] = min(tax_rebate_princi_limit, total_principal_repaid) * .3 / df_fy.shape[0]
        loss_on_house = (df_fy.interest_paid + df_fy.maintenance +
                         df_fy.prop_tax - df_fy.rent).sum()
        if fy <= 8 and int_accumulate:
            if loss_on_house > int_rebate_limit:
                int_accumulate += loss_on_house - int_rebate_limit
                loss_on_house = int_rebate_limit
            else:
                int_accumulate -= min(int_accumulate, int_rebate_limit - loss_on_house)
                loss_on_house += min(int_accumulate, int_rebate_limit - loss_on_house)
        df_fy['tax_save_interest'] = loss_on_house * .3 / df_fy.shape[0]
        df_fy['unclaimed_int_amnt'] = int_accumulate
        df = df.append(df_fy)

    df = df[['date', 'pos', 'emi', 'interest_paid', 'principle_repaid', 'extra_repaid',  'maintenance', 'prop_tax',
         'rent', 'tax_save_princi', 'tax_save_interest',
       'unclaimed_int_amnt']]

    df['net_outflow'] = df.emi + df.extra_repaid + df.maintenance + df.prop_tax - \
                        (df.rent + df.tax_save_princi + df.tax_save_interest)

    enddt = df.date.tolist()[-1]
    df['time_adj_contribution'] = df.apply(lambda x: x['net_outflow']*(1+rd_rate/4)**(
                    ((enddt.year - x['date'].year)*12+(enddt.month - x['date'].month))/3), axis=1)
    templist=[]
    for i in range(1,df.shape[0]+1):
        temp_df = df.iloc[:i,:]
        enddt = temp_df.date.tolist()[-1]
        templist.append(temp_df.apply(lambda x: x['net_outflow'] * (1 + rd_rate / 4) ** (
                ((enddt.year - x['date'].year) * 12 + (enddt.month - x['date'].month)) / 3), axis=1).sum() + temp_df.pos.tolist()[-1])
    df['future_value'] = templist
    return df
