import ccxt
import time

# Set up your API keys
api_key = '8vKnN2BRIcs1zuFdb8YwqxtZkyZ+VT/aGXN6iIaqhaD2tbspR2BOWo0F'
secret_key = 'AIxD+pIfqOw23VLVXfHs4XbAIdLW0RjY9wmKVaV0am9X4gg+l47lXSdE+PPVZLKh06Z+0Iz+ToTRPO1DrAjYag=='

# Initialize the exchange object
exchange = ccxt.kraken({
    'apiKey': api_key,
    'secret': secret_key,
})

# Define your trading strategy
def execute_trade(symbol, quantity, side, price=None):
    # Placeholder for trade execution logic
    if side == 'buy':
        print(f"Executing {side} order for {quantity} {symbol} at price {price}")
        # Implement the logic to place a buy order on the exchange (use the appropriate CCXT method)
        # Example: exchange.create_market_buy_order(symbol, quantity)

# Example buy logic with dynamic trading pair selection
def should_place_buy_order():
    # Fetch the account balance
    account_balance = exchange.fetch_balance()

    # Find a trading pair with sufficient balances in both base and quote currencies
    for symbol, balance_info in account_balance['total'].items():
        if '/' not in symbol:
            continue  # Skip symbols that do not contain '/'

        base_currency, quote_currency = symbol.split('/')
        
        if base_currency != 'USD' and quote_currency != 'USD' and balance_info > 0:
            return symbol, balance_info

    return None, 0  # Return None if no suitable trading pair is found


def main():
    profit_threshold = 25
    loss_percent_threshold = 4.9
    safety_margin = 10

    while True:
        symbol, base_currency_balance = should_place_buy_order()

        if symbol and base_currency_balance > 0:
            ticker = exchange.fetch_ticker(symbol)
            current_price = ticker['last']
            open_orders = exchange.fetch_open_orders(symbol)

            # Example: Place a market buy order
            execute_trade(symbol, base_currency_balance, 'buy', current_price)

            # Example: Sell if down by 2 percent
            if open_orders and open_orders[0]['side'] == 'buy':
                bought_price = open_orders[0]['price']
                percent_loss = ((current_price - bought_price) / bought_price) * 100

                if percent_loss >= loss_percent_threshold:
                    # Execute sell order
                    execute_trade(symbol, open_orders[0]['quantity'], 'sell')

            # Example: Sell if profit exceeds $50
            if open_orders and open_orders[0]['side'] == 'buy':
                bought_price = open_orders[0]['price']
                profit = current_price - bought_price

                if profit >= profit_threshold:
                    # Execute sell order
                    execute_trade(symbol, open_orders[0]['quantity'], 'sell')

        time.sleep(60)  # Sleep for 1 minute

if __name__ == "__main__":
    main()
