import yfinance as yf
from rich.console import Console

console = Console()

if __name__ == "__main__":
    sector = yf.Sector("basic-materials")
    console.print(sector.name)
    console.print(type(sector.name))