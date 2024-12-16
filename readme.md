# High-Frequency Trading (HFT) Simulation Environment

## Project Overview

This High-Frequency Trading (HFT) Simulation is a sophisticated Python-based distributed system that models a realistic trading environment. The project demonstrates key concepts of networked trading systems, including:

- Asynchronous market data streaming
- Concurrent trading bot execution
- Real-time market simulation
- Network communication using TCP/IP

## System Architecture

### Components

1. **Market Server (`market_server.py`):**
   - Simulates a live market environment
   - Generates dynamic market data for multiple stocks
   - Broadcasts real-time market updates to connected trading bots
   - Supports multiple concurrent client connections

2. **Trading Bots (`trading_bot.py`):**
   - Autonomously connect to the market server
   - Implement basic trading strategies
   - Make buy/sell/hold decisions based on market data
   - Maintain individual trading positions
   - Log trading activities

3. **Configuration (`config.py`):**
   - Centralizes system-wide configuration parameters
   - Defines market symbols, trading parameters, and server settings
   - Provides easy customization of simulation environment

4. **Simulation Runner (`run_hft_simulation.py`):**
   - Manages multiprocessing of market server and trading bots
   - Provides graceful startup and shutdown mechanisms

## Key Features

- **Asynchronous Communication:** Utilizes `asyncio` for non-blocking I/O operations
- **Realistic Market Simulation:** Generates semi-random price movements
- **Multiprocessing Support:** Runs market server and trading bots in separate processes
- **Configurable Parameters:** Easy to adjust trading and market simulation settings
- **Comprehensive Logging:** Detailed logging of market events and trading decisions

## Prerequisites

- Python 3.8+
- Recommended: Virtual environment

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Simulation

```bash
python run_hft_simulation.py
```

## Customization

Modify `config.py` to adjust:
- Number of trading bots
- Market symbols
- Server host and port
- Trading strategy parameters

## Simulation Workflow

1. Market Server starts and begins generating market data
2. Trading Bots connect to the server
3. Bots receive real-time market updates
4. Bots make trading decisions based on predefined strategies
5. Trading activities are logged in real-time




