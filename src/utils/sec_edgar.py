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
        
        # Top 10 banks matching your TOP_BANKS list
        self.bank_ciks = {
            "JPMORGAN CHASE & CO": "0000019617",
            "BANK OF AMERICA CORP": "0000070858", 
            "WELLS FARGO & COMPANY": "0000072971",
            "CITIGROUP INC": "0000831001",
            "U.S. BANCORP": "0000036104",
            "PNC FINANCIAL SERVICES": "0000713676",
            "TRUIST FINANCIAL CORP": "0001534701",
            "CAPITAL ONE FINANCIAL": "0000927628",
            "REGIONS FINANCIAL CORP": "0001281761",
            "FIFTH THIRD BANCORP": "0000035527"
        }
    
    def get_bank_filings(self, bank_name, form_type="10-K", limit=100, year=None):
        """Get filings for a bank with optional year filter"""
        cik = self.bank_ciks.get(bank_name)
        if not cik:
            return []
            
        try:
            # Get both recent and historical filings
            url = f"https://data.sec.gov/submissions/CIK{cik}.json"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code != 200:
                return []
                
            data = response.json()
            all_results = []
            
            # Process recent filings
            recent = data.get('filings', {}).get('recent', {})
            all_results.extend(self._process_filings(recent, cik, form_type, year))
            
            # Process historical filings if available
            files = data.get('filings', {}).get('files', [])
            for file_info in files:
                if len(all_results) >= limit:
                    break
                    
                # Fetch historical filing data
                hist_url = f"https://data.sec.gov/submissions/{file_info['name']}"
                hist_response = requests.get(hist_url, headers=self.headers)
                if hist_response.status_code == 200:
                    hist_data = hist_response.json()
                    all_results.extend(self._process_filings(hist_data, cik, form_type, year))
                    time.sleep(0.1)  # Rate limiting
            
            return all_results[:limit]
                
        except Exception as e:
            print(f"Error fetching filings for {bank_name}: {e}")
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
    
    def _process_filings(self, filings_data, cik, form_type, year):
        """Process filing data and filter by form type and year"""
        forms = filings_data.get('form', [])
        dates = filings_data.get('filingDate', [])
        accessions = filings_data.get('accessionNumber', [])
        
        results = []
        for i, form in enumerate(forms):
            if form == form_type:
                filing_date = dates[i]
                filing_year = int(filing_date.split('-')[0])
                
                # Apply year filter if specified
                if year is None or filing_year == year:
                    results.append({
                        'form': form,
                        'filing_date': filing_date,
                        'accession': accessions[i],
                        'url': f"https://www.sec.gov/Archives/edgar/data/{cik.lstrip('0')}/{accessions[i].replace('-', '')}/{accessions[i]}-index.htm"
                    })
        
        return results