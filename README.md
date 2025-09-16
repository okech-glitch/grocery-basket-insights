# Grocery Basket Insights Challenge

## Overview
The Grocery Basket Insights Challenge is a demo application developed for the 2025 Hackathon, utilizing AI to analyze customer transaction data and predict product bundles for cross-selling opportunities. This project features a Flask backend for processing data with association rule mining (using `mlxtend`) and a React frontend for interactive visualization and user interaction. Key enhancements include displaying the top 10 associations, a downloadable CSV for all data, and a toggleable dark/light mode.

## Features
- **Association Rule Mining**: Identifies frequent itemsets and generates association rules with confidence scores.
- **Top 10 Associations**: Displays the top 10 customer-product associations on the frontend.
- **CSV Download**: Enables downloading all association data as a CSV file.
- **Interactive Chart**: Visualizes confidence levels with a bar chart.
- **Dark/Light Mode**: User-selectable theme for enhanced accessibility.
- **Filtering**: Filter associations by customer ID and minimum confidence.
- **Model Score**: Shows a performance score (e.g., 0.77).

## Prerequisites
- **Python 3.8+**
- **Node.js 14+**
- **Git** (for version control)

## Dependencies
### Backend
- `flask`
- `pandas`
- `mlxtend`
- `scikit-learn`
- `reportlab`
- `flask-cors`

### Frontend
- `react`
- `react-scripts`
- `react-chartjs-2`
- `chart.js`
- `tailwindcss` (for styling)

## Installation

### Clone the Repository
```bash
git clone https://github.com/yourusername/grocery-basket-insights.git
cd grocery-basket-insights
Backend Setup

Navigate to the backend directory:
bashcd web_app/backend

Install dependencies:
bashpip install -r requirements.txt

If requirements.txt is missing, generate it with:
bashpip freeze > requirements.txt



Run the Flask server:
bashpython app.py

Confirm it runs on http://localhost:5000.



Frontend Setup

Navigate to the frontend directory:
bashcd web_app/frontend

Install dependencies:
bashnpm install

Start the development server:
bashnpm start

Access the app at http://localhost:3000.



Data

Place test.csv in web_app/frontend/public/data/ for the frontend download link.
Ensure test.csv includes columns: customer_id, product_name, product_category, store_id, and price.

Usage

Start the backend and frontend servers as outlined above.
Open http://localhost:3000 in your browser.
Upload test.csv via the file input.
Explore the top 10 associations, apply filters (customer ID, confidence), and download the full dataset.
Toggle between dark and light modes using the provided button.

Configuration

Proxy: Verify package.json in the frontend contains "proxy": "http://localhost:5000" for API requests.
Tailwind CSS: Ensure index.css includes @tailwind base; @tailwind components; @tailwind utilities;.
Port: If port 5000 is occupied, modify app.py (e.g., app.run(debug=True, port=5001)) and update the proxy accordingly.

Troubleshooting

Proxy Error (ECONNRESET): Ensure the backend is running on localhost:5000. Check firewall settings or try a different port.
HTTP 500 Error: Review backend logs for Error processing file: details and share for further diagnosis.
Missing Styles: Confirm Tailwind is configured in tailwind.config.js with content: ["./src/**/*.{js,jsx,ts,tsx}"].
Data Not Loading: Check console logs (F12 > Console) for Response data: and ensure test.csv is correctly formatted.

Future Enhancements

Sorting: Add sorting options for confidence or customer ID.
Pagination: Implement pagination for large association lists.
Excel Export: Include Excel export functionality.
Real-Time Updates: Add periodic backend polling.
User Authentication: Integrate basic login for demo users.

Contributing

Fork the repository.
Create a feature branch (git checkout -b feature-name).
Commit changes (git commit -m "Add feature-name").
Push to the branch (git push origin feature-name).
Open a Pull Request.

Credits

Developed by Christopher Okech

License
This project is licensed under the MIT License.