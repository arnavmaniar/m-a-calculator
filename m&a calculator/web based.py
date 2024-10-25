from flask import Flask, render_template, request

app = Flask(__name__)

class BalanceSheetItem:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

class BalanceSheet:
    def __init__(self):
        self.assets = []
        self.liabilities = []
        self.equity = []
        self.goodwill = 0
        self.deferred_tax_assets = 0
        self.deferred_tax_liabilities = 0

    def add_asset(self, name, amount):
        self.assets.append(BalanceSheetItem(name, amount))

    def add_liability(self, name, amount):
        self.liabilities.append(BalanceSheetItem(name, amount))

    def add_equity(self, name, amount):
        self.equity.append(BalanceSheetItem(name, amount))

    def calculate_total(self, items):
        return sum(item.amount for item in items)

    def calculate_total_assets(self):
        return self.calculate_total(self.assets)

    def calculate_total_liabilities(self):
        return self.calculate_total(self.liabilities)

class MergersAndAcquisitions:
    def __init__(self, acquirer_balance_sheet, target_balance_sheet):
        self.acquirer_balance_sheet = acquirer_balance_sheet
        self.target_balance_sheet = target_balance_sheet

    def calculate_purchase_price(self, target_price_per_share, target_shares_outstanding, equity_consideration_percent,
                                 cash_consideration_percent):
        equity_consideration = (equity_consideration_percent / 100) * target_price_per_share * target_shares_outstanding
        cash_consideration = (cash_consideration_percent / 100) * target_price_per_share * target_shares_outstanding
        purchase_price = equity_consideration + cash_consideration
        return purchase_price

    def calculate_adjusted_book_value(self):
        adjusted_book_value_assets = self.target_balance_sheet.calculate_total_assets() - \
                                     self.target_balance_sheet.goodwill - \
                                     self.target_balance_sheet.deferred_tax_assets

        adjusted_book_value_liabilities = self.target_balance_sheet.calculate_total_liabilities() - \
                                          self.target_balance_sheet.deferred_tax_liabilities

        adjusted_book_value_net_assets = adjusted_book_value_assets - adjusted_book_value_liabilities

        return adjusted_book_value_assets, adjusted_book_value_liabilities, adjusted_book_value_net_assets

    def calculate_fair_value_of_target_assets(self, target_ppe_fair_value, target_intangible_assets_fair_value):
        fair_value_assets = target_ppe_fair_value + target_intangible_assets_fair_value
        return fair_value_assets

    def calculate_fair_value_of_target_liabilities(self, target_long_term_debt_fee, target_long_term_debt_amount):
        fair_value_liabilities = target_long_term_debt_fee + target_long_term_debt_amount
        return fair_value_liabilities

    def calculate_excess_purchase_price_over_fv_equity(self, purchase_price, fair_value_target_equity):
        excess_purchase_price = purchase_price - fair_value_target_equity
        return excess_purchase_price

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    acquirer_balance_sheet = BalanceSheet()
    target_balance_sheet = BalanceSheet()

    # Process form data for acquirer balance sheet
    acquirer_balance_sheet.add_asset("Cash", float(request.form.get("acquirer_cash", 0)))
    acquirer_balance_sheet.add_asset("A/R", float(request.form.get("acquirer_ar", 0)))
    # Add other assets, liabilities, equity similarly...

    # Process form data for target balance sheet
    target_balance_sheet.add_asset("Cash", float(request.form.get("target_cash", 0)))
    target_balance_sheet.add_asset("A/R", float(request.form.get("target_ar", 0)))
    # Add other assets, liabilities, equity similarly...

    # Process M&A related inputs
    target_price_per_share = float(request.form.get("target_price_per_share", 0))
    target_shares_outstanding = float(request.form.get("target_shares_outstanding", 0))
    equity_consideration_percent = float(request.form.get("equity_consideration_percent", 0))
    cash_consideration_percent = float(request.form.get("cash_consideration_percent", 0))
    target_ppe_fair_value = float(request.form.get("target_ppe_fair_value", 0))
    target_intangible_assets_fair_value = float(request.form.get("target_intangible_assets_fair_value", 0))
    target_long_term_debt_fee = float(request.form.get("target_long_term_debt_fee", 0))
    target_long_term_debt_amount = float(request.form.get("target_long_term_debt_amount", 0))

    ma_calc = MergersAndAcquisitions(acquirer_balance_sheet, target_balance_sheet)

    purchase_price = ma_calc.calculate_purchase_price(target_price_per_share, target_shares_outstanding,
                                                     equity_consideration_percent, cash_consideration_percent)

    adjusted_book_value_assets, adjusted_book_value_liabilities, adjusted_book_value_net_assets = \
        ma_calc.calculate_adjusted_book_value()

    fair_value_assets = ma_calc.calculate_fair_value_of_target_assets(target_ppe_fair_value,
                                                                      target_intangible_assets_fair_value)

    fair_value_liabilities = ma_calc.calculate_fair_value_of_target_liabilities(target_long_term_debt_fee,
                                                                                target_long_term_debt_amount)

    excess_purchase_price = ma_calc.calculate_excess_purchase_price_over_fv_equity(purchase_price,
                                                                                   adjusted_book_value_net_assets)

    return render_template('result.html', purchase_price=purchase_price,
                           adjusted_book_value_assets=adjusted_book_value_assets,
                           adjusted_book_value_liabilities=adjusted_book_value_liabilities,
                           adjusted_book_value_net_assets=adjusted_book_value_net_assets,
                           fair_value_assets=fair_value_assets,
                           fair_value_liabilities=fair_value_liabilities,
                           excess_purchase_price=excess_purchase_price)

if __name__ == "__main__":
    app.run(debug=True)
