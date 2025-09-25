import streamlit as st
import boto3
import json
from datetime import datetime
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils.sec_edgar import SECEdgarAPI

# Check if user is authenticated - auto redirect to home
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.switch_page("1_🏠_Home.py")



# Top 10 US Banks with reliable SEC filings
TOP_BANKS = [
    "JPMORGAN CHASE & CO",
    "BANK OF AMERICA CORP",
    "WELLS FARGO & COMPANY",
    "CITIGROUP INC",
    "U.S. BANCORP",
    "PNC FINANCIAL SERVICES",
    "TRUIST FINANCIAL CORP",
    "CAPITAL ONE FINANCIAL",
    "REGIONS FINANCIAL CORP",
    "FIFTH THIRD BANCORP"
]

class SECReportManager:
    def __init__(self):
        self.sec_api = SECEdgarAPI()
        
    def get_real_sec_reports(self, bank_name, year=None):
        """Get real SEC reports for a bank with optional year filter"""
        try:
            # Get more filings with year filter - 4 10-Qs per year
            filings_10k = self.sec_api.get_bank_filings(bank_name, "10-K", 5, year)
            filings_10q = self.sec_api.get_bank_filings(bank_name, "10-Q", 50, year)
            
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
            response = self.bedrock.converse_stream(
                modelId="anthropic.claude-3-haiku-20240307-v1:0",
                messages=[{
                    "role": "user",
                    "content": [{"text": prompt}]
                }],
                inferenceConfig={"maxTokens": 4000}
            )
            
            full_text = ""
            placeholder = st.empty()
            
            for event in response['stream']:
                if 'contentBlockDelta' in event:
                    delta = event['contentBlockDelta']['delta']
                    if 'text' in delta:
                        full_text += delta['text']
                        placeholder.markdown(full_text)
            
            return full_text
        except Exception as e:
            st.error(f"❌ **Amazon Bedrock Error:** Unable to access Claude AI models. Please check your AWS credentials and Bedrock permissions. Error: {str(e)}")
            st.stop()
    
    def analyze_bank_reports(self, bank_name, reports, financial_facts):
        """Analyze bank reports using Claude - handles both API and uploaded data"""
        
        # Check if this is uploaded data or API data
        if 'uploaded_data' in reports and reports['uploaded_data']:
            # Handle uploaded files
            uploaded_content = "\n\n".join([f"=== FILE: {name} ===\nType: {data['type']}\nSize: {data['size']} bytes\n\nContent:\n{data['content']}" 
                                        for name, data in reports['uploaded_data'].items()])
            
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
        else:
            # Handle API data (original logic)
            sec_api = SECEdgarAPI()
            metrics = sec_api.extract_key_metrics(financial_facts) if financial_facts else {}
            
            metrics_text = "\n".join([f"{k}: {v:,}" if isinstance(v, (int, float)) else f"{k}: {v}" for k, v in metrics.items()]) if metrics else "No financial data available"
            
            # Get detailed filing information
            filing_details = ""
            if reports.get('10-K'):
                filing_details += "\n10-K Annual Reports:\n"
                for filing in reports['10-K'][:3]:
                    filing_details += f"- {filing.get('form', 'N/A')} filed {filing.get('filing_date', 'N/A')}\n"
            
            if reports.get('10-Q'):
                filing_details += "\n10-Q Quarterly Reports:\n"
                for filing in reports['10-Q'][:4]:
                    filing_details += f"- {filing.get('form', 'N/A')} filed {filing.get('filing_date', 'N/A')}\n"
            
            prompt = f"""
As a senior financial analyst with 15+ years of banking experience, provide a comprehensive analysis of {bank_name}.

## FINANCIAL DATA AVAILABLE:
{metrics_text}

## SEC FILINGS ANALYZED:
{filing_details}

Total Filings: {len(reports.get('10-K', []))} 10-K reports, {len(reports.get('10-Q', []))} 10-Q reports

## REQUIRED ANALYSIS (minimum 1000 words):

### 1. FINANCIAL PERFORMANCE ANALYSIS
- Analyze revenue trends, profitability metrics, and efficiency ratios
- Compare performance to industry benchmarks
- Identify key financial strengths and weaknesses

### 2. COMPREHENSIVE RISK ASSESSMENT
- **Credit Risk**: Loan portfolio quality, charge-offs, allowances
- **Market Risk**: Interest rate sensitivity, trading activities
- **Operational Risk**: Technology, compliance, regulatory issues
- **Liquidity Risk**: Funding sources, deposit stability

### 3. STRATEGIC BUSINESS ANALYSIS
- Core business segments and revenue diversification
- Digital transformation initiatives
- Market expansion strategies
- Competitive positioning vs peers

### 4. INVESTMENT RECOMMENDATION
- Target price and rating (Buy/Hold/Sell)
- Key catalysts and risk factors
- 12-month outlook and scenarios

Provide specific numbers, dates, and detailed analysis. Use professional banking terminology.
"""
        
        try:
            # Try Claude 3.5 Sonnet with streaming
            response = self.bedrock.converse_stream(
                modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
                messages=[{
                    "role": "user",
                    "content": [{"text": prompt}]
                }],
                inferenceConfig={"maxTokens": 4000}
            )
            
            # Stream the response
            full_text = ""
            placeholder = st.empty()
            
            for event in response['stream']:
                if 'contentBlockDelta' in event:
                    delta = event['contentBlockDelta']['delta']
                    if 'text' in delta:
                        full_text += delta['text']
                        placeholder.markdown(full_text)
            
            return full_text
            
        except Exception as e1:
            try:
                # Fallback to Claude 3 Haiku with streaming
                response = self.bedrock.converse_stream(
                    modelId="anthropic.claude-3-haiku-20240307-v1:0",
                    messages=[{
                        "role": "user",
                        "content": [{"text": prompt}]
                    }],
                    inferenceConfig={"maxTokens": 4000}
                )
                
                full_text = ""
                placeholder = st.empty()
                
                for event in response['stream']:
                    if 'contentBlockDelta' in event:
                        delta = event['contentBlockDelta']['delta']
                        if 'text' in delta:
                            full_text += delta['text']
                            placeholder.markdown(full_text)
                
                return full_text
                
            except Exception as e2:
                st.error(f"❌ **Amazon Bedrock Error:** Unable to access Claude AI models. Please check your AWS credentials and Bedrock permissions. Error: {str(e2)}")
                st.stop()

# Removed simulated S3 loading function - now using real SEC API

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
        
        
        /* Hide Streamlit's problematic elements */
        .stDeployButton {
            display: none !important;
        }
        
        [data-testid="stToolbar"] {
            display: none !important;
        }
        
        .stActionButton {
            display: none !important;
        }
        
        /* Hide any element containing the problematic text */
        [title*="keyword_double_arrow_right"] {
            display: none !important;
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
            font-family: 'Inter', sans-serif !important;
        }
        
        /* Style login input boxes */
        .stTextInput > div > div > input {
            border: 2px solid #e0e0e0 !important;
            border-radius: 8px !important;
            padding: 12px !important;
            font-family: 'Inter', sans-serif !important;
            background-color: #ffffff !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #2C5F41 !important;
            box-shadow: 0 0 0 2px rgba(44, 95, 65, 0.2) !important;
        }
        
        /* Make page and content full width */
        .main .block-container {
            max-width: 100% !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            width: 100% !important;
        }
        
        .stApp > div:first-child {
            max-width: 100% !important;
        }
        
        /* Make text content use full width */
        .analysis-section {
            width: 100% !important;
            max-width: 100% !important;
        }
        
        [data-testid="stMarkdownContainer"] {
            width: 100% !important;
            max-width: 100% !important;
        }
        
        [data-testid="stExpander"] {
            width: 100% !important;
            max-width: 100% !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color: #2C5F41; font-family: Arial, sans-serif; font-weight: bold;'>🏦 Banking Financial Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-family: Arial, sans-serif;'><strong>Real SEC Filing Analysis using Claude AI</strong></p>", unsafe_allow_html=True)
    
    # Initialize session state
    if 'reports_loaded' not in st.session_state:
        st.session_state.reports_loaded = True
    
    # Initialize components
    sec_manager = SECReportManager()
    claude_analyzer = ClaudeAnalyzer()

    # Display available banks
    # Report source selection
    report_source = st.sidebar.radio("#### :green[Report Source]", ["SEC EDGAR API", "Upload Reports"], 
                                    key="report_source_selection",
                                    help="Choose between live SEC data or upload your own reports")
    
    # Year selection for SEC EDGAR API
    if report_source == "SEC EDGAR API":
        selected_year = st.sidebar.selectbox(
            "#### :green[Select Year]",
            [2024, 2023, 2022, 2021, 2020],
            index=0,
            key="year_selection",
            help="Select the year for SEC filings"
        )
    else:
        selected_year = None
    
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
        • PDF files (10-K, 10-Q) - Auto text extraction
        • Text files (.txt)
        • Multiple files allowed
        
        📦 **Requirements:**
        • For PDF support: `pip install PyPDF2`
        • Max 5000 chars per file for analysis
        """)
        
        if uploaded_reports:
            st.sidebar.success(f"✅ Uploaded {len(uploaded_reports)} report(s)")
            # Process uploaded reports
            report_data = {}
            for report in uploaded_reports:
                if report.type == "application/pdf":
                    try:
                        # Try to extract text from PDF
                        import PyPDF2
                        pdf_reader = PyPDF2.PdfReader(report)
                        text_content = ""
                        for page in pdf_reader.pages:
                            text_content += page.extract_text() + "\n"
                        
                        # Clean and limit content for analysis
                        # Remove extra whitespace and fix formatting
                        cleaned_content = ' '.join(text_content.split())
                        content = cleaned_content[:5000] + "..." if len(cleaned_content) > 5000 else cleaned_content
                        
                        report_data[report.name] = {
                            "type": "PDF",
                            "size": len(report.getvalue()),
                            "content": content if content.strip() else f"PDF file {report.name} - Unable to extract text content."
                        }
                    except ImportError:
                        st.sidebar.error("❌ PyPDF2 not installed. Install with: pip install PyPDF2")
                        report_data[report.name] = {
                            "type": "PDF", 
                            "size": len(report.getvalue()),
                            "content": f"PDF file {report.name} - PyPDF2 library required for PDF text extraction."
                        }
                    except Exception as e:
                        st.sidebar.warning(f"⚠️ Could not extract text from {report.name}: {str(e)}")
                        report_data[report.name] = {
                            "type": "PDF",
                            "size": len(report.getvalue()), 
                            "content": f"PDF file {report.name} - Text extraction failed: {str(e)}."
                        }
                else:
                    # Text files can be read directly
                    try:
                        raw_content = str(report.read(), "utf-8")
                        # Clean content to avoid formatting issues
                        cleaned_content = ' '.join(raw_content.split())
                        content = cleaned_content[:5000] + "..." if len(cleaned_content) > 5000 else cleaned_content
                        
                        report_data[report.name] = {
                            "type": "Text",
                            "size": len(raw_content),
                            "content": content
                        }
                    except Exception as e:
                        st.sidebar.error(f"❌ Error reading {report.name}: {str(e)}")
                        report_data[report.name] = {
                            "type": "Text",
                            "size": 0,
                            "content": f"Error reading file: {str(e)}"
                        }
        else:

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
    
    # Auto-detect bank from uploaded document content if using Upload Reports
    if report_source == "Upload Reports" and 'report_data' in locals() and report_data:
        # Extract bank name from document content (first 1000 characters)
        detected_bank = "Unknown Bank"
        
        for filename, data in report_data.items():
            content = data['content'][:1000].upper()  # Check first 1000 chars
            
            # Look for bank names in document content
            if "WEBSTER BANK" in content or "WEBSTER FINANCIAL" in content:
                detected_bank = "Webster Bank"
                break
            elif "JPMORGAN CHASE" in content or "JP MORGAN" in content:
                detected_bank = "JPMorgan Chase"
                break
            elif "BANK OF AMERICA" in content or "BOFA" in content:
                detected_bank = "Bank of America"
                break
            elif "WELLS FARGO" in content:
                detected_bank = "Wells Fargo"
                break
            elif "GOLDMAN SACHS" in content:
                detected_bank = "Goldman Sachs"
                break
            elif "CITIGROUP" in content or "CITIBANK" in content:
                detected_bank = "Citibank"
                break
            elif "U.S. BANK" in content or "US BANK" in content:
                detected_bank = "U.S. Bank"
                break
            elif "PNC BANK" in content or "PNC FINANCIAL" in content:
                detected_bank = "PNC Bank"
                break
            elif "TRUIST" in content or "BB&T" in content:
                detected_bank = "Truist Bank"
                break
            elif "CAPITAL ONE" in content:
                detected_bank = "Capital One"
                break
            elif "TD BANK" in content:
                detected_bank = "TD Bank"
                break
            elif "NELNET" in content:
                detected_bank = "Nelnet"
                break
        
        # If no specific bank found, try to extract any company name from content
        if detected_bank == "Unknown Bank":
            import re
            # Look for common patterns like "COMPANY NAME" or "Company, Inc."
            patterns = [
                r'([A-Z][A-Z\s&]+(?:BANK|FINANCIAL|CORP|CORPORATION|INC|COMPANY))',
                r'([A-Z][A-Za-z\s&]+(?:Bank|Financial|Corp|Corporation|Inc|Company))',
                r'([A-Z][A-Z\s]+)(?=\s+(?:ANNUAL|QUARTERLY|REPORT|10-K|10-Q))'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content[:2000])
                if matches:
                    # Take the first reasonable match
                    candidate = matches[0].strip()
                    if len(candidate) > 3 and len(candidate) < 50:
                        detected_bank = candidate.title()
                        break
        
        selected_bank = detected_bank
        st.info(f"🎯 Auto-detected bank: **{selected_bank}** from document content")
    else:
        if not st.session_state.selected_bank:
            st.info("👆 Please select a bank above to begin analysis")
            return
        selected_bank = st.session_state.selected_bank

    # Show selected bank info
    st.markdown(f"## 🏦 {selected_bank} - Financial Analysis")
    
    # Get reports based on source
    if report_source == "SEC EDGAR API":
        with st.spinner(f"📄 Fetching {selected_year} SEC filings..."):
            reports = sec_manager.get_real_sec_reports(selected_bank, selected_year)
            

            
            # Filter reports by selected year
            if selected_year:
                filtered_10k = [r for r in reports.get('10-K', []) if r.get('filing_date', '').startswith(str(selected_year))]
                filtered_10q = [r for r in reports.get('10-Q', []) if r.get('filing_date', '').startswith(str(selected_year))]
                reports['10-K'] = filtered_10k
                reports['10-Q'] = filtered_10q
                
                # Debug info
                if not filtered_10k and not filtered_10q:
                    st.info(f"No SEC filings found for {selected_bank} in {selected_year}. Try a different year.")
    else:
        # Use uploaded reports
        if 'report_data' in locals() and report_data:
            # Better detection for 10-K/10-Q in filenames and content
            reports_10k = []
            reports_10q = []
            
            for filename, data in report_data.items():
                filename_upper = filename.upper()
                content_upper = data['content'][:500].upper()  # Check first 500 chars
                
                # Check filename and content for 10-K indicators
                if ("10-K" in filename_upper or "10K" in filename_upper or 
                    "ANNUAL" in filename_upper or "YEAR" in filename_upper or
                    "10-K" in content_upper or "ANNUAL REPORT" in content_upper):
                    reports_10k.append(filename)
                # Check for 10-Q indicators
                elif ("10-Q" in filename_upper or "10Q" in filename_upper or 
                      "QUARTER" in filename_upper or "Q1" in filename_upper or "Q2" in filename_upper or
                      "Q3" in filename_upper or "Q4" in filename_upper or
                      "10-Q" in content_upper or "QUARTERLY REPORT" in content_upper):
                    reports_10q.append(filename)
                else:
                    # Default to 10-K for annual reports
                    reports_10k.append(filename)
            
            reports = {
                "10-K": reports_10k,
                "10-Q": reports_10q,
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
            st.metric("📅 Year Selected", str(selected_year))
        else:
            st.metric("📁 Uploaded Files", len(reports.get("uploaded_data", {})))

    # Analysis button
    analysis_label = f"🤖 Analyze {selected_bank} with Amazon Bedrock"
    if st.button(analysis_label, type="primary", use_container_width=True):
        with st.spinner(f"Amazon Bedrock is analyzing {selected_bank}'s financial reports..."):
            # Use same analysis method for both API and uploaded data
            analysis = claude_analyzer.analyze_bank_reports(selected_bank, reports, reports.get('financial_facts', {}))
            if analysis is None:
                return  # Stop execution if Claude failed
        
        st.markdown(f"### 📊 Amazon Bedrock Analysis Results for {selected_bank}")
        
        # Add PDF download button
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib.units import inch
            import io
            
            def create_pdf_report(bank_name, analysis_text, reports_data, report_source):
                buffer = io.BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=letter)
                styles = getSampleStyleSheet()
                story = []
                
                # Title
                title = Paragraph(f"Financial Analysis Report - {bank_name}", styles['Title'])
                story.append(title)
                story.append(Spacer(1, 0.2*inch))
                
                # Date
                date = Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y')}", styles['Normal'])
                story.append(date)
                story.append(Spacer(1, 0.3*inch))
                
                # Analysis content
                for section in analysis_text.split('\n\n'):
                    if section.strip():
                        para = Paragraph(section.replace('\n', '<br/>'), styles['Normal'])
                        story.append(para)
                        story.append(Spacer(1, 0.2*inch))
                
                # Add sources section
                story.append(Spacer(1, 0.5*inch))
                sources_title = Paragraph("Report Sources", styles['Heading2'])
                story.append(sources_title)
                story.append(Spacer(1, 0.2*inch))
                
                if report_source == "SEC EDGAR API":
                    # Add SEC report sources
                    if reports_data.get('10-K'):
                        story.append(Paragraph("10-K Annual Reports:", styles['Heading3']))
                        for report in reports_data['10-K']:
                            source_text = f"• {report['form']} - Filed: {report['filing_date']}<br/>  URL: {report['url']}"
                            story.append(Paragraph(source_text, styles['Normal']))
                        story.append(Spacer(1, 0.1*inch))
                    
                    if reports_data.get('10-Q'):
                        story.append(Paragraph("10-Q Quarterly Reports:", styles['Heading3']))
                        for report in reports_data['10-Q']:
                            source_text = f"• {report['form']} - Filed: {report['filing_date']}<br/>  URL: {report['url']}"
                            story.append(Paragraph(source_text, styles['Normal']))
                        story.append(Spacer(1, 0.1*inch))
                else:
                    # Add uploaded report sources
                    story.append(Paragraph("Uploaded Report Sources:", styles['Heading3']))
                    for filename, data in reports_data.get('uploaded_data', {}).items():
                        source_text = f"• {filename}<br/>  Type: {data['type']}<br/>  Size: {data['size']:,} bytes"
                        story.append(Paragraph(source_text, styles['Normal']))
                        story.append(Spacer(1, 0.1*inch))
                
                doc.build(story)
                buffer.seek(0)
                return buffer
            
            pdf_buffer = create_pdf_report(selected_bank, analysis, reports, report_source)
            st.download_button(
                label="📄 Download Analysis as PDF",
                data=pdf_buffer.getvalue(),
                file_name=f"{selected_bank}_Analysis_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                type="secondary"
            )
        except ImportError:
            st.info("💡 Install reportlab to enable PDF download: `pip install reportlab`")
        
        # Analysis already displayed via streaming - no need to display again
        
        # Show report sources based on source type - minimal spacing
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div style="margin-top: 100px; padding-top: 50px;">', unsafe_allow_html=True)
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
                    elif data['type'] == 'PDF':
                        st.write(f"• Content extracted: {len(data['content'])} characters")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer note
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #666; font-size: 0.9rem; font-family: Arial, sans-serif;'>Powered by Amazon Bedrock - BankIQ+</p>", unsafe_allow_html=True)



if __name__ == "__main__":
    run_app()