import requests
import json
from datetime import datetime

class FinancialModelingPrepAPI:
    def __init__(self, api_key="demo"):  # Use "demo" for testing, get free key from financialmodelingprep.com
        self.api_key = api_key
        self.base_url = "https://financialmodelingprep.com/api/v3"
        
        # Bank ticker symbols
        self.bank_tickers = {
            "JPMORGAN CHASE & CO": "JPM",
            "BANK OF AMERICA CORP": "BAC",
            "WELLS FARGO & COMPANY": "WFC", 
            "CITIGROUP INC": "C",
            "U.S. BANCORP": "USB",
            "PNC FINANCIAL SERVICES": "PNC",
            "TRUIST FINANCIAL CORP": "TFC",
            "CAPITAL ONE FINANCIAL": "COF",
            "REGIONS FINANCIAL CORP": "RF",
            "FIFTH THIRD BANCORP": "FITB"
        }
    
    def get_sec_filings(self, bank_name, year=None):
        """Get SEC filings for a bank"""
        ticker = self.bank_tickers.get(bank_name)
        if not ticker:
            return {"10-K": [], "10-Q": []}
            
        try:
            url = f"{self.base_url}/sec_filings/{ticker}?apikey={self.api_key}"
            response = requests.get(url)
            
            if response.status_code == 200:
                filings = response.json()
                
                filings_10k = []
                filings_10q = []
                
                for filing in filings:
                    filing_year = int(filing['fillingDate'].split('-')[0])
                    
                    if year is None or filing_year == year:
                        filing_data = {
                            'form': filing['type'],
                            'filing_date': filing['fillingDate'],
                            'url': filing['finalLink']
                        }
                        
                        if filing['type'] == '10-K':
                            filings_10k.append(filing_data)
                        elif filing['type'] == '10-Q':
                            filings_10q.append(filing_data)
                
                return {"10-K": filings_10k, "10-Q": filings_10q}
                
        except Exception as e:
            print(f"Error fetching FMP data: {e}")
            return {"10-K": [], "10-Q": []}
    
    def get_financial_statements(self, bank_name, year=None):
        """Get comprehensive financial statements"""
        ticker = self.bank_tickers.get(bank_name)
        if not ticker:
            return {}
            
        try:
            # Get income statement, balance sheet, cash flow
            statements = {}
            
            for statement_type in ['income-statement', 'balance-sheet-statement', 'cash-flow-statement']:
                url = f"{self.base_url}/{statement_type}/{ticker}?apikey={self.api_key}"
                if year:
                    url += f"&period=annual&limit=5"
                    
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    if year:
                        # Filter by year
                        filtered_data = [item for item in data if item.get('calendarYear') == str(year)]
                        statements[statement_type] = filtered_data
                    else:
                        statements[statement_type] = data[:3]  # Last 3 years
            
            return statements
            
        except Exception as e:
            print(f"Error fetching financial statements: {e}")
            return {}