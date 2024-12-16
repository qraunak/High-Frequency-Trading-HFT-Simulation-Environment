import os
from dataclasses import dataclass, field

@dataclass
class MarketConfig:
    """Configuration for the HFT market simulation."""
    
    # Server configuration
    SERVER_HOST: str = 'localhost'
    SERVER_PORT: int = 8888
    
    # Trading bot configuration
    NUM_TRADING_BOTS: int = 5
    
    # Logging configuration
    LOG_LEVEL: str = 'INFO'
    LOG_DIR: str = os.path.join(os.path.dirname(__file__), 'logs')
    
    # Market simulation parameters
    SYMBOLS: list = field(default_factory=lambda: ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA'])
    
    # Trading strategy parameters
    MAX_TRADE_QUANTITY: int = 100
    MIN_TRADE_QUANTITY: int = 10
    
    def __post_init__(self):
        """Ensure log directory exists."""
        os.makedirs(self.LOG_DIR, exist_ok=True)

# Create a singleton configuration instance
config = MarketConfig()