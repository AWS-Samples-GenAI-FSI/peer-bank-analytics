# 🏦 Banking Peer Analytics

AI-powered banking analytics platform that provides real-time peer comparison and financial analysis using FDIC data and Amazon Bedrock's Claude AI.

## 🚀 Features

### 📊 **Real-Time Data Integration**
- **FDIC API Integration**: Live data from 10 major US banks
- **Historical Analysis**: Quarterly data from 2023-2024
- **6 Key Banking Metrics**: ROA, ROE, NIM, Tier 1 Capital, LDR, CRE Concentration

### 🤖 **AI-Powered Analysis**
- **Claude AI Integration**: Intelligent financial analysis and insights
- **Peer Comparison**: Automated performance benchmarking
- **Trend Analysis**: Quarterly performance tracking

### 📈 **Interactive Visualizations**
- **Line Charts**: Trend analysis over time
- **Bar Charts**: Comparative performance metrics
- **Heatmaps**: Performance correlation analysis
- **Real-time Updates**: Dynamic chart generation

## 🏛️ **Supported Banks**

1. JPMorgan Chase Bank (Base Bank)
2. Bank of America
3. Wells Fargo Bank
4. Citibank
5. U.S. Bank
6. PNC Bank
7. Goldman Sachs Bank
8. Truist Bank
9. Capital One
10. TD Bank

## 📋 **Banking Metrics**

| Metric | Description |
|--------|-------------|
| **ROA** | Return on Assets - Net income as % of average assets |
| **ROE** | Return on Equity - Net income as % of average equity |
| **NIM** | Net Interest Margin - Interest spread as % of assets |
| **Tier 1 Capital** | Core capital as % of risk-weighted assets |
| **LDR** | Loan-to-Deposit Ratio - Loans as % of deposits |
| **CRE Concentration** | Commercial real estate loans as % of total capital |

## 🛠️ **Installation**

### Prerequisites
- Python 3.8+
- AWS Account with Bedrock access
- Streamlit

### Setup
```bash
# Clone the repository
git clone https://github.com/AWS-Samples-GenAI-FSI/peer-bank-analytics.git
cd peer-bank-analytics

# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials
aws configure

# Run the application
streamlit run 1_🏠_Home.py
```

## 🔧 **Configuration**

### AWS Bedrock Setup
Ensure you have access to:
- `anthropic.claude-3-haiku-20240307-v1:0`

### Environment Variables
```bash
export AWS_DEFAULT_REGION=us-east-1
export AWS_PROFILE=your-profile
```

## 📱 **Usage**

### 1. **Home Page**
- Overview of BankIQ+ capabilities
- Navigation to analysis tools

### 2. **Peer Bank Analytics**
- Select metrics for analysis
- Choose peer banks for comparison
- View interactive charts and AI insights
- Download analysis data

### 3. **Financial Reports Analyzer**
- Select banks for detailed analysis
- AI-powered report analysis using Claude
- View simulated 10-K/10-Q report insights

## 🏗️ **Architecture**

```
├── 1_🏠_Home.py              # Main application entry
├── pages/
│   ├── 1_Peer_bank_analytics.py    # FDIC data analysis
│   └── 2_Financial_Reports_Analyzer.py  # Report analysis
├── src/
│   ├── bedrock/
│   │   └── bedrock_helper.py        # Claude AI integration
│   └── utils/
│       └── ui_helpers.py            # UI components
├── data/                            # Sample data files
├── images/                          # UI assets
└── requirements.txt                 # Dependencies
```

## 🔄 **Data Flow**

1. **FDIC API** → Real banking data retrieval
2. **Data Processing** → Quarterly metrics calculation
3. **Claude AI** → Intelligent analysis generation
4. **Plotly Charts** → Interactive visualizations
5. **Streamlit UI** → User interface rendering

## 📊 **API Integration**

### FDIC APIs Used
- **Institutions API**: Bank information and identifiers
- **Financials API**: Historical quarterly financial data

### Data Caching
- **1-hour cache** for FDIC API responses
- **Session state** for user selections
- **Automatic refresh** for real-time updates

## 🎯 **Key Benefits**

- **Real-time Analysis**: Live FDIC data integration
- **AI Insights**: Claude-powered financial analysis
- **Interactive UI**: Dynamic charts and comparisons
- **Regulatory Compliance**: Official FDIC data sources
- **Scalable Architecture**: Cloud-native design

## 🔒 **Security & Compliance**

- AWS IAM integration for secure access
- FDIC official data sources
- No sensitive data storage
- Secure API communications

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 **Support**

For questions and support:
- Create an issue in this repository
- Contact the AWS Samples team

## 🏷️ **Tags**

`banking` `fintech` `aws` `bedrock` `claude` `fdic` `analytics` `streamlit` `python` `ai` `genai`

---

**Powered by Amazon Bedrock - BankIQ+**