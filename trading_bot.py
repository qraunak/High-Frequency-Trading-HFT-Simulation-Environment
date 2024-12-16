import asyncio
import json
import logging
import random
from typing import Dict, Any

class TradingBot:
    def __init__(self, 
                 bot_id: str, 
                 server_host: str = 'localhost', 
                 server_port: int = 8888):
        self.bot_id = bot_id
        self.server_host = server_host
        self.server_port = server_port
        self.market_data: Dict[str, Any] = {}
        self.positions: Dict[str, Dict[str, Any]] = {}
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """Set up logging for the trading bot."""
        logger = logging.getLogger(f'TradingBot_{self.bot_id}')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def get_trading_strategy(self, symbol: str) -> str:
        """
        Implement a simple trading strategy.
        Returns 'BUY', 'SELL', or 'HOLD' based on market conditions.
        """
        if symbol not in self.market_data:
            return 'HOLD'

        price = self.market_data[symbol]['price']
        
        # Simple mean reversion strategy
        if symbol not in self.positions:
            self.positions[symbol] = {
                'avg_price': 0,
                'quantity': 0
            }

        current_position = self.positions[symbol]

        # Random trading for simulation
        decision = random.choices(
            ['BUY', 'SELL', 'HOLD'], 
            weights=[0.4, 0.4, 0.2]
        )[0]

        # More sophisticated strategy could be implemented here
        if decision == 'BUY':
            trade_quantity = random.randint(10, 100)
            self.logger.info(
                f'BOT {self.bot_id} - STRATEGY: Buying {trade_quantity} of {symbol} at ${price}'
            )
            current_position['quantity'] += trade_quantity
            current_position['avg_price'] = (
                (current_position['avg_price'] * 
                 (current_position['quantity'] - trade_quantity) + 
                 price * trade_quantity) / current_position['quantity']
            )
            return 'BUY'

        elif decision == 'SELL':
            # Only sell if we have a position
            if current_position['quantity'] > 0:
                sell_quantity = min(
                    current_position['quantity'], 
                    random.randint(10, current_position['quantity'])
                )
                self.logger.info(
                    f'BOT {self.bot_id} - STRATEGY: Selling {sell_quantity} of {symbol} at ${price}'
                )
                current_position['quantity'] -= sell_quantity
                return 'SELL'

        return 'HOLD'

    async def process_market_data(self, market_data: Dict[str, Any]):
        """Process incoming market data and make trading decisions."""
        self.market_data = market_data

        # Make trading decisions for each symbol
        for symbol in market_data.keys():
            self.get_trading_strategy(symbol)

    async def connect_to_market(self):
        """Connect to the market server and start trading."""
        try:
            reader, writer = await asyncio.open_connection(
                self.server_host, self.server_port
            )
            self.logger.info(f'BOT {self.bot_id} connected to market server')

            try:
                while True:
                    # Read market data
                    data = await reader.readline()
                    if not data:
                        break

                    # Parse market data
                    try:
                        market_data = json.loads(data.decode())
                        await self.process_market_data(market_data)
                    except json.JSONDecodeError:
                        self.logger.error('Invalid market data received')

            except asyncio.CancelledError:
                pass
            except Exception as e:
                self.logger.error(f'Error in market data processing: {e}')
            finally:
                writer.close()
                await writer.wait_closed()

        except ConnectionRefusedError:
            self.logger.error(
                f'BOT {self.bot_id} could not connect to market server'
            )
        except Exception as e:
            self.logger.error(f'Unexpected error: {e}')

def main():
    """Create multiple trading bots."""
    bot_count = 5
    bots = [TradingBot(f'Bot_{i+1}') for i in range(bot_count)]

    async def run_bots():
        """Run all bots concurrently."""
        await asyncio.gather(
            *[bot.connect_to_market() for bot in bots]
        )

    try:
        asyncio.run(run_bots())
    except KeyboardInterrupt:
        print("\nTrading simulation shutting down...")

if __name__ == '__main__':
    main()