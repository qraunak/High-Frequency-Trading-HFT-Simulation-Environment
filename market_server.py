import asyncio
import json
import random
import logging
from typing import Dict, List

class MarketServer:
    def __init__(self, host: str = 'localhost', port: int = 8888):
        self.host = host
        self.port = port
        self.clients: Dict[asyncio.StreamWriter, str] = {}
        self.market_data: Dict[str, Dict] = {}
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """Set up logging for the market server."""
        logger = logging.getLogger('MarketServer')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def generate_market_data(self):
        """Simulate dynamic market data generation."""
        symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
        for symbol in symbols:
            # Simulate price movements with some randomness
            last_price = self.market_data.get(symbol, {}).get('price', random.uniform(50, 500))
            price_change = random.normalvariate(0, last_price * 0.001)
            new_price = last_price + price_change

            self.market_data[symbol] = {
                'symbol': symbol,
                'price': round(new_price, 2),
                'volume': random.randint(1000, 100000),
                'timestamp': asyncio.get_event_loop().time()
            }

    async def broadcast_market_data(self):
        """Broadcast market data to all connected clients."""
        while True:
            self.generate_market_data()
            market_update = json.dumps(self.market_data)
            
            # Broadcast to all connected clients
            for writer in list(self.clients.keys()):
                try:
                    writer.write(market_update.encode() + b'\n')
                    await writer.drain()
                except Exception as e:
                    self.logger.error(f"Error broadcasting to client: {e}")
                    await self.remove_client(writer)
            
            # Wait for a short interval before next update
            await asyncio.sleep(0.1)

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle incoming client connections."""
        # Identify client
        peername = writer.get_extra_info('peername')
        self.logger.info(f'New connection from {peername}')
        
        # Register client
        self.clients[writer] = str(peername)

        try:
            while True:
                # Read client messages (optional for future extensions)
                data = await reader.readline()
                if not data:
                    break
                
                # Process incoming trade requests or other messages
                message = data.decode().strip()
                self.logger.info(f'Received message from {peername}: {message}')

        except asyncio.CancelledError:
            pass
        except Exception as e:
            self.logger.error(f'Error handling client {peername}: {e}')
        finally:
            await self.remove_client(writer)

    async def remove_client(self, writer: asyncio.StreamWriter):
        """Remove a client from the connected clients."""
        if writer in self.clients:
            peername = writer.get_extra_info('peername')
            self.logger.info(f'Connection closed for {peername}')
            del self.clients[writer]
            writer.close()
            await writer.wait_closed()

    async def start_server(self):
        """Start the market server."""
        server = await asyncio.start_server(
            self.handle_client, self.host, self.port)
        
        addr = server.sockets[0].getsockname()
        self.logger.info(f'Serving on {addr}')

        # Start broadcasting market data
        broadcast_task = asyncio.create_task(self.broadcast_market_data())

        async with server:
            await server.serve_forever()

def main():
    """Main entry point for the market server."""
    server = MarketServer()
    
    try:
        asyncio.run(server.start_server())
    except KeyboardInterrupt:
        print("\nMarket server shutting down...")

if __name__ == '__main__':
    main()