import requests
import json
import pandas as pd
from datetime import datetime
import time

class SECEdgarAPI:
    def __init__(self):
        self.base_url = "https://data.sec.gov/api/xbrl"
        self.headers = {
            'User-Agent': 'BankingAnalytics contact@example.com',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'data.sec.gov'
        }
        
        # Bank CIK numbers (Central Index Key)
        self.bank_ciks = {
            "JPMORGAN CHASE BANK": "0000019617",
            "BANK OF AMERICA": "0000070858", 
            "WELLS FARGO BANK": "0000072971",
            "CITIBANK": "0000831001",
            "U.S. BANK": "0000036104",
            "PNC BANK": "0000713676",
            "GOLDMAN SACHS BANK": "0000886982",
            "TRUIST BANK": "0000092230",
            "CAPITAL ONE": "0000927628",
            "TD BANK": "0000947263"
        }
    
    def get_bank_filings(self, bank_name, form_type="10-K", limit=5):
        """Get recent filings for a bank"""
        cik = self.bank_ciks.get(bank_name)
        if not cik:
            return []
            
        try:
            url = f"https://data.sec.gov/submissions/CIK{cik}.json"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                filings = data.get('filings', {}).get('recent', {})
                
                # Filter for specific form type
                forms = filings.get('form', [])
                dates = filings.get('filingDate', [])
                accessions = filings.get('accessionNumber', [])
                
                results = []
                for i, form in enumerate(forms):
                    if form == form_type and len(results) < limit:
                        results.append({
                            'form': form,
                            'filing_date': dates[i],
                            'accession': accessions[i],
                            'url': f"https://www.sec.gov/Archives/edgar/data/{cik.lstrip('0')}/{accessions[i].replace('-', '')}/{accessions[i]}-index.htm"
                        })
                
                return results
                
        except Exception as e:
            print(f"Error fetching filings: {e}")
            return []
    
    def get_financial_facts(self, bank_name):
        """Get financial facts for a bank"""
        cik = self.bank_ciks.get(bank_name)
        if not cik:
            return {}
            
        try:
            url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
                
        except Exception as e:
            print(f"Error fetching facts: {e}")
            return {}
    
    def extract_key_metrics(self, facts_data):
        """Extract key financial metrics from SEC data"""
        try:
            facts = facts_data.get('facts', {})
            us_gaap = facts.get('us-gaap', {})
            
            metrics = {}
            
            # Revenue
            if 'Revenues' in us_gaap:
                revenue_data = us_gaap['Revenues']['units']['USD']
                latest_revenue = revenue_data[-1] if revenue_data else None
                if latest_revenue:
                    metrics['Revenue'] = latest_revenue['val']
                    metrics['Revenue_Date'] = latest_revenue['end']
            
            # Net Income
            if 'NetIncomeLoss' in us_gaap:
                income_data = us_gaap['NetIncomeLoss']['units']['USD']
                latest_income = income_data[-1] if income_data else None
                if latest_income:
                    metrics['Net_Income'] = latest_income['val']
                    metrics['Net_Income_Date'] = latest_income['end']
            
            # Total Assets
            if 'Assets' in us_gaap:
                assets_data = us_gaap['Assets']['units']['USD']
                latest_assets = assets_data[-1] if assets_data else None
                if latest_assets:
                    metrics['Total_Assets'] = latest_assets['val']
                    metrics['Assets_Date'] = latest_assets['end']
            
            return metrics
            
        except Exception as e:
            print(f"Error extracting metrics: {e}")
            return {}