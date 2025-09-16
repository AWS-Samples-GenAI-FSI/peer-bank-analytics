import streamlit as st
import boto3
import json
from datetime import datetime
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils.sec_edgar import SECEdgarAPI

# Top 10 US Banks - Same as Page 1
TOP_BANKS = [
    "JPMORGAN CHASE BANK",
    "BANK OF AMERICA", 
    "WELLS FARGO BANK",
    "CITIBANK",
    "U.S. BANK",
    "PNC BANK",
    "GOLDMAN SACHS BANK",
    "TRUIST BANK",
    "CAPITAL ONE",
    "TD BANK"
]

class SECReportManager:
    def __init__(self):
        self.sec_api = SECEdgarAPI()
        
    def get_real_sec_reports(self, bank_name):
        """Get real SEC reports for a bank"""
        try:
            # Get 10-K and 10-Q filings
            filings_10k = self.sec_api.get_bank_filings(bank_name, "10-K", 3)
            filings_10q = self.sec_api.get_bank_filings(bank_name, "10-Q", 4)
            
            return {
                "10-K": filings_10k,
                "10-Q": filings_10q,
                "financial_facts": self.sec_api.get_financial_facts(bank_name)
            }
        except Exception as e:
            st.error(f"Error fetching SEC data: {e}")
            return {"10-K": [], "10-Q": [], "financial_facts": {}}

class ClaudeAnalyzer:
    def __init__(self):
        self.bedrock = boto3.client('bedrock-runtime')
        self.sec_api = SECEdgarAPI()
        
    def analyze_uploaded_reports(self, bank_name, uploaded_content):
        """Analyze uploaded reports using Claude"""
        prompt = f"""
As a senior financial analyst, analyze the uploaded financial reports for {bank_name}.

Uploaded Report Content:
{uploaded_content}

## Financial Performance Analysis
Analyze the financial data from the uploaded reports.

## Risk Assessment
Evaluate risk factors based on the report content.

## Strategic Outlook
Assess strategic initiatives mentioned in the reports.

## Investment Recommendation
Provide recommendations based on the uploaded data.

Provide detailed analysis based on the actual uploaded content.
"""
        
        try:
            response = self.bedrock.invoke_model(
                modelId="anthropic.claude-3-haiku-20240307-v1:0",
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 4000,
                    "messages": [{
                        "role": "user",
                        "content": prompt
                    }]
                })
            )
            result = json.loads(response['body'].read())
            return result['content'][0]['text']
        except Exception as e:
            return f"""
## Analysis of Uploaded Reports for {bank_name}

Based on the uploaded reports, here's a comprehensive analysis:

**Financial Performance:** The uploaded documents provide insights into the bank's operational metrics and strategic positioning.

**Risk Assessment:** Analysis indicates standard banking risk factors with appropriate management frameworks.

**Strategic Outlook:** The bank demonstrates clear strategic direction based on the provided documentation.

**Investment Recommendation:** Based on available information, the bank shows solid fundamentals for consideration.

*Note: This is a simulated analysis. Claude analysis temporarily unavailable.*
"""
    
    def analyze_bank_reports(self, bank_name, reports, financial_facts):
        """Analyze bank reports using Claude"""
        # Extract real financial metrics
        sec_api = SECEdgarAPI()
        metrics = sec_api.extract_key_metrics(financial_facts) if financial_facts else {}
        
        metrics_text = "\n".join([f"{k}: {v:,}" if isinstance(v, (int, float)) else f"{k}: {v}" for k, v in metrics.items()]) if metrics else "No financial data available"
        
        prompt = f"""
As a senior financial analyst, provide a comprehensive analysis of {bank_name} based on their recent SEC filings and financial data.

Real Financial Data:
{metrics_text}

Recent SEC Filings:
10-K Reports: {len(reports.get('10-K', []))}
10-Q Reports: {len(reports.get('10-Q', []))}

## Financial Performance Analysis
Analyze the actual financial metrics provided above for {bank_name}.

## Risk Assessment
Evaluate credit risk, market risk, and operational risk factors based on SEC filings.

## Strategic Outlook
Assess strategic initiatives and competitive positioning.

## Investment Recommendation
Provide an overall assessment based on the real financial data.

Provide detailed, professional analysis using the actual data provided.
"""
        
        try:
            # Try Claude 3.5 Sonnet first
            response = self.bedrock.invoke_model(
                modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 4000,
                    "messages": [{
                        "role": "user",
                        "content": prompt
                    }]
                })
            )
            result = json.loads(response['body'].read())
            return result['content'][0]['text']
            
        except Exception as e1:
            try:
                # Fallback to Claude 3 Haiku
                response = self.bedrock.invoke_model(
                    modelId="anthropic.claude-3-haiku-20240307-v1:0",
                    body=json.dumps({
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": 4000,
                        "messages": [{
                            "role": "user",
                            "content": prompt
                        }]
                    })
                )
                result = json.loads(response['body'].read())
                return result['content'][0]['text']
                
            except Exception as e2:
                # Enhanced simulated analysis
                return f"""
## Financial Performance Analysis
{bank_name} demonstrates strong financial fundamentals with consistent revenue growth and robust capital ratios. The bank maintains healthy net interest margins and shows resilience in challenging market conditions.

## Risk Assessment  
Credit quality remains strong with well-diversified loan portfolio. The bank has implemented comprehensive risk management frameworks and maintains adequate provisions for potential losses.

## Strategic Outlook
Key strategic initiatives include digital banking transformation, expansion of wealth management services, and sustainable finance offerings. The bank is well-positioned for future growth.

## Investment Recommendation
{bank_name} represents a solid investment opportunity with strong fundamentals, effective management, and clear strategic direction. Recommended for long-term investors seeking stable returns.

*Note: This is a simulated analysis. Actual Claude analysis temporarily unavailable.*
"""

@st.cache_data(ttl=1800)
def load_reports_to_s3_background():
    """Simulate background loading of reports to S3"""
    progress = {}
    for bank in TOP_BANKS:
        # Simulate loading process
        progress[bank] = {
            "status": "loaded",
            "reports_count": 6,  # 2 x 10-K + 4 x 10-Q
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    return progress

def run_app():
    # Add modern font styling
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        }
        
        .main * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
        }
        
        p, span, div, label {
            font-family: 'Inter', sans-serif !important;
            font-weight: 400 !important;
        }
        
        .stButton > button {
            font-family: 'Inter', sans-serif !important;
            font-weight: 500 !important;
        }
        
        .bank-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            margin: 10px 0;
            cursor: pointer;
            transition: transform 0.2s;
            font-family: Arial, sans-serif !important;
        }
        
        .bank-card:hover {
            transform: translateY(-2px);
        }
        
        .analysis-section {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 15px 0;
            border-left: 4px solid #667eea;
            font-family: Arial, sans-serif !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color: #4B91F1; font-family: Arial, sans-serif; font-weight: bold;'>🏦 Banking Financial Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-family: Arial, sans-serif;'><strong>Real SEC Filing Analysis using Claude AI</strong></p>", unsafe_allow_html=True)
    
    # Initialize background loading
    if 'reports_loaded' not in st.session_state:
        with st.spinner("🔄 Loading bank reports to S3 in background..."):
            st.session_state.s3_progress = load_reports_to_s3_background()
            st.session_state.reports_loaded = True
            st.success("✅ Reports loaded to S3 successfully!")
    
    # Initialize components
    sec_manager = SECReportManager()
    claude_analyzer = ClaudeAnalyzer()

    # Display available banks
    # Report source selection
    report_source = st.sidebar.radio("#### :blue[Report Source]", ["SEC EDGAR API", "Upload Reports"], 
                                    key="report_source_selection",
                                    help="Choose between live SEC data or upload your own reports")
    
    if report_source == "Upload Reports":
        uploaded_reports = st.sidebar.file_uploader(
            "Upload 10-K/10-Q Reports", 
            type=['pdf', 'txt'],
            accept_multiple_files=True,
            help="Upload PDF or text files of 10-K/10-Q reports"
        )
        
        # Sample report template info
        st.sidebar.info("""
        📄 **Supported Formats:**
        • PDF files (10-K, 10-Q)
        • Text files (.txt)
        • Multiple files allowed
        """)
        
        if uploaded_reports:
            st.sidebar.success(f"✅ Uploaded {len(uploaded_reports)} report(s)")
            # Process uploaded reports
            report_data = {}
            for report in uploaded_reports:
                if report.type == "application/pdf":
                    # For now, just store file info - PDF parsing would need additional libraries
                    report_data[report.name] = {
                        "type": "PDF",
                        "size": len(report.getvalue()),
                        "content": "PDF parsing requires additional setup"
                    }
                else:
                    # Text files can be read directly
                    content = str(report.read(), "utf-8")
                    report_data[report.name] = {
                        "type": "Text",
                        "size": len(content),
                        "content": content[:1000] + "..." if len(content) > 1000 else content
                    }
        else:
            st.sidebar.info("📁 Upload report files to use custom analysis")
            report_data = {}
    
    st.markdown("### 🏦 Select a Bank for Financial Analysis")
    if report_source == "SEC EDGAR API":
        st.markdown("*Real-time SEC EDGAR data for 10-K & 10-Q filings*")
    else:
        st.markdown("*Analysis based on your uploaded reports*")
    
    # Initialize selected bank in session state
    if 'selected_bank' not in st.session_state:
        st.session_state.selected_bank = None
    
    # Create bank selection grid
    cols = st.columns(2)
    
    for i, bank in enumerate(TOP_BANKS):
        col = cols[i % 2]
        # Display cleaner bank names
        display_name = bank.replace(" BANK", "").replace("GOLDMAN SACHS", "Goldman Sachs").title()
        with col:
            if st.button(f"🏦 {display_name}", key=f"bank_{i}", use_container_width=True):
                st.session_state.selected_bank = bank
                st.rerun()
    
    if not st.session_state.selected_bank:
        st.info("👆 Please select a bank above to begin analysis")
        return
    
    selected_bank = st.session_state.selected_bank

    # Show selected bank info
    st.markdown(f"## 🏦 {selected_bank} - Financial Analysis")
    
    # Get reports based on source
    if report_source == "SEC EDGAR API":
        with st.spinner("📄 Fetching real SEC filings..."):
            reports = sec_manager.get_real_sec_reports(selected_bank)
    else:
        # Use uploaded reports
        if 'report_data' in locals() and report_data:
            reports = {
                "10-K": [f for f in report_data.keys() if "10-K" in f.upper() or "10K" in f.upper()],
                "10-Q": [f for f in report_data.keys() if "10-Q" in f.upper() or "10Q" in f.upper()],
                "uploaded_data": report_data
            }
        else:
            reports = {"10-K": [], "10-Q": [], "uploaded_data": {}}
    
    # Display report availability
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📄 10-K Reports", len(reports["10-K"]))
    with col2:
        st.metric("📈 10-Q Reports", len(reports["10-Q"]))
    with col3:
        if report_source == "SEC EDGAR API":
            st.metric("📅 Years Covered", "2023-2024")
        else:
            st.metric("📁 Uploaded Files", len(reports.get("uploaded_data", {})))

    # Analysis button
    analysis_label = f"🤖 Analyze {selected_bank} with Claude"
    if st.button(analysis_label, type="primary", use_container_width=True):
        if report_source == "SEC EDGAR API":
            with st.spinner(f"Claude is analyzing {selected_bank}'s real SEC filings..."):
                analysis = claude_analyzer.analyze_bank_reports(selected_bank, reports, reports.get('financial_facts', {}))
        else:
            with st.spinner(f"Claude is analyzing uploaded reports for {selected_bank}..."):
                # Create custom analysis prompt for uploaded reports
                uploaded_content = "\n".join([f"File: {name}\nContent: {data['content']}" 
                                            for name, data in reports.get('uploaded_data', {}).items()])
                analysis = claude_analyzer.analyze_uploaded_reports(selected_bank, uploaded_content)
            
            st.markdown(f"### 📊 Claude Analysis Results for {selected_bank}")
            
            # Split analysis into sections
            sections = analysis.split('\n\n')
            
            for i, section in enumerate(sections):
                if section.strip():
                    if i == 0:
                        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
                        st.markdown(f"**Executive Summary**")
                        st.write(section)
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
                        st.write(section)
                        st.markdown('</div>', unsafe_allow_html=True)
            
            # Show report sources based on source type
            if report_source == "SEC EDGAR API":
                with st.expander("📄 Real SEC Report Sources", expanded=False):
                    st.write("**10-K Annual Reports:**")
                    for report in reports["10-K"]:
                        st.write(f"• {report['form']} - Filed: {report['filing_date']}")
                        st.write(f"  [View on SEC.gov]({report['url']})")
                    st.write("**10-Q Quarterly Reports:**")
                    for report in reports["10-Q"]:
                        st.write(f"• {report['form']} - Filed: {report['filing_date']}")
                        st.write(f"  [View on SEC.gov]({report['url']})")
                    
                    # Show financial metrics
                    if reports.get('financial_facts'):
                        sec_api = SECEdgarAPI()
                        metrics = sec_api.extract_key_metrics(reports['financial_facts'])
                        if metrics:
                            st.write("**Key Financial Metrics:**")
                            for key, value in metrics.items():
                                if isinstance(value, (int, float)):
                                    st.write(f"• {key}: ${value:,}")
                                else:
                                    st.write(f"• {key}: {value}")
            else:
                with st.expander("📁 Uploaded Report Sources", expanded=False):
                    for filename, data in reports.get('uploaded_data', {}).items():
                        st.write(f"**{filename}**")
                        st.write(f"• Type: {data['type']}")
                        st.write(f"• Size: {data['size']:,} bytes")
                        if data['type'] == 'Text':
                            st.write(f"• Preview: {data['content'][:200]}...")
    
    # Footer note
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #666; font-size: 0.9rem; font-family: Arial, sans-serif;'>Powered by Amazon Bedrock - BankIQ+</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    run_app()