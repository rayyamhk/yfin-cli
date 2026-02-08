import yfinance as yf
from rich.console import Console

console = Console()

if __name__ == "__main__":
    industry = yf.Industry("agricultural-inputs")
    console.print(industry.top_companies)
    console.print(type(industry.top_companies))
