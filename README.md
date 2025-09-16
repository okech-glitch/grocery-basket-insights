# 🛒 Grocery Basket Insights: AI-Powered Cross-Selling Analytics

![Grocery Basket Insights](https://img.shields.io/badge/Grocery--Basket--Insights-blue?style=for-the-badge&logo=shopping-cart&logoColor=white)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-black.svg)](https://flask.palletsprojects.com)
[![mlxtend](https://img.shields.io/badge/mlxtend-0.23+-green.svg)](https://rasbt.github.io/mlxtend/)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3+-cyan.svg)](https://tailwindcss.com)
[![Chart.js](https://img.shields.io/badge/Chart.js-4+-orange.svg)](https://www.chartjs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Boosting retail sales with AI-driven insights to identify product bundles and enhance cross-selling opportunities.**

---

## 🎯 Project Overview

Grocery Basket Insights is a demo application developed for the 2025 Hackathon, designed to analyze customer transaction data and predict product bundles for effective cross-selling. Using association rule mining (via mlxtend), it processes shopping data to recommend product combinations, helping retailers optimize sales strategies and improve customer experiences.

### 🌍 Problem Statement

- **Sales Opportunities**: Missed chances to upsell related products due to lack of insights.
- **Customer Behavior**: Limited understanding of buying patterns across 3,331 customers.
- **Data Utilization**: Untapped potential in transaction data for targeted marketing.
- **Efficiency**: Manual analysis of 39,324 association rules is time-consuming.

### 🚀 Solution

- **AI-Powered Recommendations**: Identifies top product associations with confidence scores.
- **Interactive Interface**: User-friendly frontend with visualizations and filters.
- **Data Export**: Downloadable CSV for easy sharing with sales teams.
- **Customization**: Filters by customer ID and confidence levels for tailored insights.

---

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Flask Backend │    │   Data Analysis │
│   (React)       │◄──►│   (Python)      │◄──►│   (mlxtend)     │
│                 │    │                 │    │                 │
│ • Top 10 List   │    │ • /predict      │    │ • Transaction   │
│ • Chart         │    │ • Data Upload   │    │ • Association   │
│ • Download      │    │ • Error Handling│    │ • Confidence    │
│ • Filters       │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 🌟 Current Features

### 🎯 Core Functionality

- **Association Rule Mining**: Generates 39,324 rules from 3,331 customer transactions.
- **Top 10 Associations**: Displays the most confident product bundles.
- **Real-Time Insights**: Sub-second processing for uploaded data.
- **User-Friendly Design**: Responsive interface with dark/light mode toggle.

### 📊 Data Visualization

- **Confidence Chart**: Bar chart showing association confidence levels.
- **Model Score**: Displays overall model performance (e.g., 0.77).
- **Dynamic Filters**: Adjust by customer ID and minimum confidence.

### 🗺️ Data Coverage

- **Customer Base**: Analyzes data from 3,331 unique customers.
- **Product Range**: Supports multiple product categories from transactions.
- **Exportable Results**: Full dataset available as CSV.

### 🔧 Technical Features

- **Flask Backend**: Python-based API for data processing.
- **React Frontend**: Modern JavaScript framework with Tailwind CSS.
- **mlxtend Library**: Powers association rule mining.
- **Chart.js**: Enables interactive confidence visualizations.

---

## 🚀 Proposed Features (Roadmap)

### 📱 Enhanced User Experience

- **Multi-Format Export**: Add Excel and PDF export options.
- **Offline Mode**: Cache results for offline access.
- **User Roles**: Basic login for sales/marketing teams.
- **Notifications**: Alerts for high-confidence opportunities.

### 📊 Advanced Analytics

- **Sorting Options**: Sort by confidence or customer frequency.
- **Pagination**: Navigate large association lists.
- **Trend Analysis**: Track changes in buying patterns over time.
- **Segmentation**: Group customers by behavior.

### 🤖 AI Enhancements

- **Predictive Modeling**: Forecast future buying trends.
- **Personalization**: Tailor recommendations per customer.
- **Real-Time Updates**: Periodic data refresh from backend.
- **Natural Language**: Simple query interface for non-tech users.

### 🌍 Expanded Applications

- **Multi-Retailer Support**: Adapt for different store chains.
- **Category Insights**: Deep dive into specific product categories.
- **Seasonal Campaigns**: Highlight seasonal product bundles.
- **Integration**: Connect with existing POS systems.

---

## 🧮 How Associations Are Calculated

The tool uses association rule mining to identify product relationships based on transaction data. Here’s the simplified process:

### **1. Input Features (From test.csv)**

- **Customer ID**: Unique identifier for each shopper.
- **Products**: List of items purchased in a transaction.
- **Store ID**: Location of purchase (optional).
- **Price**: Transaction value (optional for weighting).

### **2. Association Rule Mining**

- **Algorithm**: Apriori (via mlxtend).
- **Training Data**: Transaction data from test.csv.
- **Metrics**:
  - **Support**: Frequency of itemsets (e.g., 5% of transactions).
  - **Confidence**: Likelihood of buying B given A (e.g., 75%).
  - **Lift**: Strength of rule (e.g., 1.2 means 20% stronger than random).

### **3. Rule Selection Formula**

```
Confidence = (Number of Transactions with A and B) / (Number of Transactions with A)
Top 10 = Sort by Confidence and Select Highest
```

### **4. Interpretation**

| Confidence Range | Strength     | Action                               |
|------------------|-------------|--------------------------------------|
| 80-100%          | Very Strong | Promote heavily (e.g., bundles)      |
| 60-79%           | Moderate    | Suggest at checkout                  |
| 40-59%           | Weak        | Monitor and test marketing           |
| 0-39%            | Very Weak   | Avoid promotion                      |

### **5. Feature Importance**

- **Transaction Frequency (40%)**: How often products appear together.
- **Customer Diversity (30%)**: Spread across different shoppers.
- **Price Correlation (20%)**: Related to purchase value.
- **Store Variation (10%)**: Differences by location.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 14+
- Git

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/grocery-basket-insights.git
   cd grocery-basket-insights
   ```

2. **Backend Setup (Python/Flask)**

   ```bash
   # Create virtual environment
   python -m venv .venv
   .venv\Scripts\activate  # On Windows

   # Install Python dependencies
   pip install -r requirements.txt
   ```

3. **Frontend Setup (React)**

   ```bash
   cd web_app/frontend
   # Install Node.js dependencies
   npm install
   ```

4. **Start the Backend**

   ```bash
   cd ..\backend
   python app.py
   # Backend will run on http://localhost:5000
   ```

5. **Start the Frontend**

   ```bash
   cd ..\frontend
   npm start
   # Frontend will run on http://localhost:3000
   ```

---

## 🏗️ Project Structure

```
grocery-basket-insights/
├── 📁 web_app/
│   ├── 📁 backend/             # Flask backend application
│   │   ├── app.py             # Main Flask app
│   │   ├── data_processor.py  # Data processing logic
│   │   └── requirements.txt   # Python dependencies
│   ├── 📁 frontend/            # React frontend application
│   │   ├── src/               # Source files
│   │   │   ├── App.js         # Main component
│   │   │   ├── index.css      # Styles
│   │   │   └── index.js       # Entry point
│   │   ├── public/            # Static assets
│   │   │   └── data/          # test.csv location
│   │   └── package.json       # Node.js dependencies
├── 📁 README.md                # This file
└── 📁 LICENSE                  # License file
```

---

## 🔧 Backend API Endpoints

### Core Endpoints

- `GET /health` - System health check
- `POST /predict` - Process uploaded transaction data
- `GET /status` - Backend status and model info

### Example API Usage

```bash
# Upload transaction data
curl -X POST "http://localhost:5000/predict" \
  -F "file=@test.csv"

# Response
{
  "associations": [
    {"customer_id": 1, "products": ["bread", "butter"], "confidence": 0.85}
  ],
  "score": 0.77
}
```

---

## 🎨 Frontend Features

### Dashboard Components

- **Top 10 Associations**: List of high-confidence product bundles.
- **Confidence Chart**: Bar chart for visual analysis.
- **Download Button**: Export all associations as CSV.
- **Filter Inputs**: Adjust by customer ID and confidence.
- **Theme Toggle**: Switch between dark and light modes.

### Technology Stack

- **Framework**: React 18 with JavaScript
- **Styling**: Tailwind CSS 3
- **Charts**: Chart.js 4
- **Forms**: Built-in React state management

---

## 🧪 Testing

### Backend Testing

```bash
# Run tests (if implemented)
python -m pytest
```

### Frontend Testing

```bash
cd web_app/frontend
# Run tests
npm test
```

---

## 🚀 Deployment

### Backend Deployment

```bash
# Using Python
python app.py

# Using Docker (optional setup)
docker build -t grocery-basket-insights-backend .
docker run -p 5000:5000 grocery-basket-insights-backend
```

### Frontend Deployment

```bash
cd web_app/frontend
# Build for production
npm run build

# Start production server
npm start

# Deploy to Vercel
vercel --prod
```

---

## 📊 Model Performance

- **Rules Generated**: 39,324 from 3,331 customers.
- **Algorithm**: Apriori (mlxtend).
- **Confidence Range**: 0-1 (e.g., 0.85 = 85% likelihood).
- **Processing Time**: <1 second for uploads.
- **Score**: 0.77 (model reliability metric).

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use consistent React practices
- Write tests for new features
- Update documentation for changes
- Use conventional commit messages

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Open-source community for mlxtend, Flask, and React.
- Retail data providers for transaction insights.

---

## 📞 Support

- **Documentation**: Local Docs
- **Issues**: GitHub Issues
- **Email**: okechobonyo@gmail.com

---

**Built with ❤️ for smarter retail solutions**

---

## 🔄 Recent Updates

- **v1.2.0**: Added dark/light mode and CSV download
- **v1.1.0**: Enhanced association rule mining with filters
- **v1.0.0**: Initial release with core functionality
