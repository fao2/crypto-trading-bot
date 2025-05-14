import json
import time
from datetime import datetime
import requests
from transformers import pipeline
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TradingAssistant:
    def __init__(self):
        self.language = os.getenv('LANGUAGE', 'en')
        self.user_data = self._load_user_data()
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        
    def _load_user_data(self):
        try:
            with open('config.json') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'alerts': [],
                'preferences': {
                    'risk_tolerance': 'medium',
                    'fav_coins': ['bitcoin', 'ethereum']
                }
            }

    def get_market_data(self, coin_id='bitcoin'):
        """Fetch real-time market data from CoinGecko API"""
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        try:
            response = requests.get(url)
            data = response.json()['market_data']
            return {
                'current_price': data['current_price']['usd'],
                'price_change_24h': data['price_change_percentage_24h'],
                'high_24h': data['high_24h']['usd'],
                'low_24h': data['low_24h']['usd']
            }
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def set_price_alert(self, coin, target_price, alert_type):
        """Set new price alert"""
        self.user_data['alerts'].append({
            'coin': coin,
            'target': target_price,
            'type': alert_type,
            'created': datetime.now().isoformat()
        })
        self._save_data()

    def _save_data(self):
        with open('config.json', 'w') as f:
            json.dump(self.user_data, f, indent=2)

    def check_alerts(self):
        """Check all active alerts"""
        triggered = []
        for alert in self.user_data['alerts']:
            data = self.get_market_data(alert['coin'])
            if not data:
                continue
                
            if alert['type'] == 'above' and data['current_price'] > alert['target']:
                triggered.append(alert)
            elif alert['type'] == 'below' and data['current_price'] < alert['target']:
                triggered.append(alert)
        return triggered

    def get_psychological_tip(self):
        tips = {
            'en': [
                "💰 Don't chase losses - stick to your strategy",
                "🧘 Trade the chart, not your emotions",
                "⚖️ Always use proper risk management"
            ],
            'id': [
                "💰 Jangan kejar kerugian - patuhi strategi",
                "🧘 Tradinglah berdasarkan chart, bukan emosi",
                "⚖️ Selalu gunakan manajemen risiko yang tepat"
            ]
        }
        return tips[self.language][datetime.now().second % 3]

# Main Execution
if __name__ == "__main__":
    bot = TradingAssistant()
    
    while True:
        print("\n" + "="*30)
        print("CRYPTO TRADING ASSISTANT")
        print("="*30)
        print("1. Market Data")
        print("2. Set Price Alert")
        print("3. Check Alerts")
        print("4. Get Trading Tip")
        print("5. Exit")
        
        choice = input("Select option: ")
        
        if choice == '1':
            coin = input("Coin ID (e.g bitcoin): ")
            data = bot.get_market_data(coin)
            print(f"\nCurrent Price: ${data['current_price']:,.2f}")
            print(f"24h Change: {data['price_change_24h']:.2f}%")
            print(f"24h Range: ${data['low_24h']:,.2f} - ${data['high_24h']:,.2f}")
        
        elif choice == '2':
            coin = input("Coin ID: ")
            price = float(input("Target price: "))
            alert_type = input("Alert when price is (above/below): ")
            bot.set_price_alert(coin, price, alert_type)
            print("✅ Alert set successfully!")
        
        elif choice == '3':
            alerts = bot.check_alerts()
            if alerts:
                print("\n🚨 TRIGGERED ALERTS:")
                for alert in alerts:
                    print(f"{alert['coin'].upper()} is now {alert['type']} ${alert['target']}")
            else:
                print("No alerts triggered")
        
        elif choice == '4':
            print("\n" + bot.get_psychological_tip())
        
        elif choice == '5':
            print("Goodbye! Happy trading!")
            break
        
        time.sleep(1)
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

COINGECKO_API_KEY = os.getenv('COINGECKO_API_KEY', '')

def get_market_data(self, coin_id='bitcoin'):
    """Enhanced with API Key"""
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    headers = {}
    
    if COINGECKO_API_KEY:
        headers = {'x-cg-demo-api-key': COINGECKO_API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise error for bad status
        data = response.json()
        return {
            'current_price': data['market_data']['current_price']['usd'],
            'price_change_24h': data['market_data']['price_change_percentage_24h'],
            'high_24h': data['market_data']['high_24h']['usd'],
            'low_24h': data['market_data']['low_24h']['usd'],
            'last_updated': data['last_updated']
        }
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None
