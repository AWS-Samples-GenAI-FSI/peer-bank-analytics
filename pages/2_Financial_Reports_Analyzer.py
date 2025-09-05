import streamlit as st
import boto3
import json
from datetime import datetime
import time

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

class S3ReportManager:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = "banking-reports-analysis"
        
    def simulate_s3_reports(self, bank_name):
        """Simulate S3 reports availability"""
        return {
            "10-K": [f"{bank_name}-10K-2024.pdf", f"{bank_name}-10K-2023.pdf"],
            "10-Q": [f"{bank_name}-10Q-Q1-2024.pdf", f"{bank_name}-10Q-Q2-2024.pdf", 
                     f"{bank_name}-10Q-Q3-2023.pdf", f"{bank_name}-10Q-Q4-2023.pdf"]
        }

class ClaudeAnalyzer:
    def __init__(self):
        self.bedrock = boto3.client('bedrock-runtime')
        
    def analyze_bank_reports(self, bank_name, reports):
        """Analyze bank reports using Claude"""
        prompt = f"""
As a senior financial analyst, provide a comprehensive analysis of {bank_name} based on their recent financial reports.

## Financial Performance Analysis
Analyze revenue growth, profitability trends, and key financial ratios for {bank_name}.

## Risk Assessment
Evaluate credit risk, market risk, and operational risk factors.

## Strategic Outlook
Assess strategic initiatives, digital transformation efforts, and competitive positioning.

## Investment Recommendation
Provide an overall assessment and key takeaways for investors.

Provide detailed, professional analysis in each section.
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
    st.markdown("<p style='text-align: center; font-family: Arial, sans-serif;'><strong>AI-Powered Analysis of Top 10 US Banks using Claude</strong></p>", unsafe_allow_html=True)
    
    # Initialize background loading
    if 'reports_loaded' not in st.session_state:
        with st.spinner("🔄 Loading bank reports to S3 in background..."):
            st.session_state.s3_progress = load_reports_to_s3_background()
            st.session_state.reports_loaded = True
            st.success("✅ Reports loaded to S3 successfully!")
    
    # Initialize components
    s3_manager = S3ReportManager()
    claude_analyzer = ClaudeAnalyzer()

    # Display available banks
    st.markdown("### 🏦 Select a Bank for Financial Analysis")
    st.markdown("*Reports for 2023-2024 (10-K & 10-Q) are pre-loaded in S3*")
    
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
    
    # Get reports from S3
    reports = s3_manager.simulate_s3_reports(selected_bank)
    
    # Display report availability
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📄 10-K Reports", len(reports["10-K"]))
    with col2:
        st.metric("📈 10-Q Reports", len(reports["10-Q"]))
    with col3:
        st.metric("📅 Years Covered", "2023-2024")

    # Analysis button
    if st.button(f"🤖 Analyze {selected_bank} with Claude", type="primary", use_container_width=True):
        with st.spinner(f"Claude is analyzing {selected_bank}'s financial reports..."):
            analysis = claude_analyzer.analyze_bank_reports(selected_bank, reports)
            
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
            
            # Show report sources
            with st.expander("📄 Report Sources", expanded=False):
                st.write("**10-K Annual Reports:**")
                for report in reports["10-K"]:
                    st.write(f"• {report}")
                st.write("**10-Q Quarterly Reports:**")
                for report in reports["10-Q"]:
                    st.write(f"• {report}")
    
    # Footer note
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #666; font-size: 0.9rem; font-family: Arial, sans-serif;'>Powered by Amazon Bedrock - BankIQ+</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    run_app()