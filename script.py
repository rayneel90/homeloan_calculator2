import pandas as pd

################################################################################
#                                  Inputs                                      #
################################################################################

price = 3.5e6
ltv = .8
roi = 0.0785 / 12
tenure = 300
early_repay = 1e5


rent_earning = 12000
maintenance = 30000
prop_tax = 7000

tax_80c = 150000
self_pf_contri = 48600
tax_rebate_int = 200000

rd_rate = 0.075

################################################################################
#                                     EMI                                      #
################################################################################

principal = price * ltv
downpay = price - principal
emi = principal * roi * (1+roi)**tenure / ((1+roi)**tenure - 1)

################################################################################
#                                    POS                                       #
################################################################################
dat = []
month = 0
while principal:
    month += 1
    interest = principal * roi
    emi = min(emi, principal + interest)
    princi_repay = emi - interest
    extra_repay = 0 if month%12 else early_repay
    principal = max(0, principal-princi_repay-extra_repay)
    dat.append({'month': month, 'pos': principal, 'emi': emi, 'interest_paid': interest,
                'principle_repaid': princi_repay, 'Extra_repaid': extra_repay})
dat = pd.DataFrame(dat)