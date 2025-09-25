import requests
import json
from datetime import datetime

class AlphaVantageAPI:
    def __init__(self, api_key="demo"):  # Get free key from alphavantage.co
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
        
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
    
    def get_earnings_reports(self, bank_name):
        """Get earnings reports (quarterly and annual)"""
        ticker = self.bank_tickers.get(bank_name)
        if not ticker:
            return {"annual": [], "quarterly": []}
            
        try:
            url = f"{self.base_url}?function=EARNINGS&symbol={ticker}&apikey={self.api_key}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "annual": data.get("annualEarnings", []),
                    "quarterly": data.get("quarterlyEarnings", [])
                }
                
        except Exception as e:
            print(f"Error fetching Alpha Vantage data: {e}")
            return {"annual": [], "quarterly": []}
    
    def get_company_overview(self, bank_name):
        """Get comprehensive company overview with financial metrics"""
        ticker = self.bank_tickers.get(bank_name)
        if not ticker:
            return {}
            
        try:
            url = f"{self.base_url}?function=OVERVIEW&symbol={ticker}&apikey={self.api_key}"
            response = requests.get(url)
            
            if response.status_code == 200:
                return response.json()
                
        except Exception as e:
            print(f"Error fetching company overview: {e}")
            return {}
    
    def get_financial_statements(self, bank_name, statement_type="INCOME_STATEMENT"):
        """Get financial statements (INCOME_STATEMENT, BALANCE_SHEET, CASH_FLOW)"""
        ticker = self.bank_tickers.get(bank_name)
        if not ticker:
            return {"annual": [], "quarterly": []}
            
        try:
            url = f"{self.base_url}?function={statement_type}&symbol={ticker}&apikey={self.api_key}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "annual": data.get("annualReports", []),
                    "quarterly": data.get("quarterlyReports", [])
                }
                
        except Exception as e:
            print(f"Error fetching {statement_type}: {e}")
            return {"annual": [], "quarterly": []}