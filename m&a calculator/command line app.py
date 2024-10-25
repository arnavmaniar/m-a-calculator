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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    acquirer_balance_sheet = BalanceSheet()
    target_balance_sheet = BalanceSheet()

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
        # Calculate Adjusted Book Value of Target Assets
        adjusted_book_value_assets = self.target_balance_sheet.calculate_total_assets() - \
                                     self.target_balance_sheet.goodwill - \
                                     self.target_balance_sheet.deferred_tax_assets

        # Calculate Adjusted Book Value of Target Liabilities
        adjusted_book_value_liabilities = self.target_balance_sheet.calculate_total_liabilities() - \
                                          self.target_balance_sheet.deferred_tax_liabilities

        # Calculate Adjusted Book Value of Net Assets
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


def get_balance_sheet_data():
    balance_sheet = BalanceSheet()

    print("Enter assets (type 'done' to finish):")
    while True:
        asset_name = input("Asset name: ")
        if asset_name.lower() == 'done':
            break
        asset_amount = float(input("Amount: "))
        balance_sheet.add_asset(asset_name, asset_amount)

    print("Enter liabilities (type 'done' to finish):")
    while True:
        liability_name = input("Liability name: ")
        if liability_name.lower() == 'done':
            break
        liability_amount = float(input("Amount: "))
        balance_sheet.add_liability(liability_name, liability_amount)

    print("Enter equity (type 'done' to finish):")
    while True:
        equity_name = input("Equity name: ")
        if equity_name.lower() == 'done':
            break
        equity_amount = float(input("Amount: "))
        balance_sheet.add_equity(equity_name, equity_amount)

    return balance_sheet


def main():
    print("Enter Acquirer's Balance Sheet:")
    acquirer_balance_sheet = get_balance_sheet_data()

    print("\nEnter Target's Balance Sheet:")
    target_balance_sheet = get_balance_sheet_data()

    target_price_per_share = float(input("Enter Target Acquisition Price per Share (USD): "))
    target_shares_outstanding = float(input("Enter Target Shares Outstanding: "))
    equity_consideration_percent = float(input("Enter Equity Consideration (% of Purchase Price): "))
    cash_consideration_percent = float(input("Enter Cash Consideration (% of Purchase Price): "))
    target_ppe_fair_value = float(input("Enter Target's PP&E Fair Value: "))
    target_intangible_assets_fair_value = float(input("Enter Target's Intangible Assets Fair Value: "))
    target_long_term_debt_fee = float(input("Enter Target's Long-Term Debt Fee: "))
    target_long_term_debt_amount = float(input("Enter Target's Long-Term Debt Amount: "))

    ma_calc = MergersAndAcquisitions(acquirer_balance_sheet, target_balance_sheet)

    purchase_price = ma_calc.calculate_purchase_price(target_price_per_share, target_shares_outstanding,
                                                     equity_consideration_percent, cash_consideration_percent)
    print("\nPurchase Price:", purchase_price)

    adjusted_book_value_assets, adjusted_book_value_liabilities, adjusted_book_value_net_assets = \
        ma_calc.calculate_adjusted_book_value()
    print("Adjusted Book Value of Target Assets:", adjusted_book_value_assets)
    print("Adjusted Book Value of Target Liabilities:", adjusted_book_value_liabilities)
    print("Adjusted Book Value of Net Assets (Equity):", adjusted_book_value_net_assets)

    fair_value_assets = ma_calc.calculate_fair_value_of_target_assets(target_ppe_fair_value,
                                                                      target_intangible_assets_fair_value)
    print("Fair Value of Target Assets:", fair_value_assets)

    fair_value_liabilities = ma_calc.calculate_fair_value_of_target_liabilities(target_long_term_debt_fee,
                                                                                target_long_term_debt_amount)
    print("Fair Value of Target Liabilities:", fair_value_liabilities)

    excess_purchase_price = ma_calc.calculate_excess_purchase_price_over_fv_equity(purchase_price,
                                                                                   adjusted_book_value_net_assets)
    print("Excess of Purchase Price over FV of Target Equity (Goodwill):", excess_purchase_price)


if __name__ == "__main__":
    main()
