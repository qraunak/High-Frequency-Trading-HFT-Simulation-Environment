import asyncio
import multiprocessing
import signal
import sys
from market_server import MarketServer
from trading_bot import TradingBot
from config import config

def run_market_server():
    """Run the market server in a separate process."""
    server = MarketServer(
        host=config.SERVER_HOST, 
        port=config.SERVER_PORT
    )
    
    try:
        asyncio.run(server.start_server())
    except KeyboardInterrupt:
        print("\nMarket server shutting down...")

def run_trading_bots():
    """Run trading bots in a separate process."""
    bots = [
        TradingBot(
            bot_id=f'Bot_{i+1}', 
            server_host=config.SERVER_HOST, 
            server_port=config.SERVER_PORT
        ) for i in range(config.NUM_TRADING_BOTS)
    ]

    async def run_bots():
        """Run all bots concurrently."""
        await asyncio.gather(
            *[bot.connect_to_market() for bot in bots]
        )

    try:
        asyncio.run(run_bots())
    except KeyboardInterrupt:
        print("\nTrading bots shutting down...")

def main():
    """
    Main entry point for the HFT simulation.
    Runs market server and trading bots in separate processes.
    """
    # Set up signal handling for graceful shutdown
    def signal_handler(sig, frame):
        print("\nInterrupt received. Shutting down simulation...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # Create processes for market server and trading bots
    market_server_process = multiprocessing.Process(
        target=run_market_server, 
        name='MarketServerProcess'
    )
    trading_bots_process = multiprocessing.Process(
        target=run_trading_bots, 
        name='TradingBotsProcess'
    )

    # Start processes
    market_server_process.start()
    trading_bots_process.start()

    # Wait for processes to complete
    market_server_process.join()
    trading_bots_process.join()

if __name__ == '__main__':
    # Ensure multiprocessing works correctly on different platforms
    multiprocessing.set_start_method('spawn')
    main()