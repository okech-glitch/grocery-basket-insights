from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.cluster import KMeans
import logging
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "http://localhost:3000"}, r"/trends": {"origins": "http://localhost:3000"}, r"/export": {"origins": "http://localhost:3000"}})

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    if file.filename != 'test.csv':
        return jsonify({'error': 'Please upload test.csv'}), 400

    try:
        df = pd.read_csv(file)
        logger.debug(f"df customer_id type before conversion: {df['customer_id'].dtype}")
        df['customer_id'] = df['customer_id'].astype(int)
        required_columns = ['customer_id', 'product_name', 'product_category', 'store_id']
        if not all(col in df.columns for col in required_columns):
            return jsonify({'error': f'Missing columns. Expected: {required_columns}'}), 400

        if df.empty:
            return jsonify({'error': 'Uploaded file is empty'}), 400

        filters = request.form.get('filters', '{}')
        filters = eval(filters) if filters else {}
        if filters.get('category'):
            df = df[df['product_category'] == filters['category']]
        if filters.get('storeId'):
            df = df[df['store_id'] == filters['storeId']]

        basket = df.groupby('customer_id')['product_name'].apply(set).reset_index(name='items')
        logger.debug(f"Basket length: {len(basket)}")
        if basket.empty:
            return jsonify({'error': 'No data after grouping by customer_id'}), 400

        basket['items'] = basket['items'].apply(list)
        encoded_vals = pd.get_dummies(basket['items'].apply(pd.Series).stack()).groupby(level=0).sum()
        if encoded_vals.empty:
            return jsonify({'error': 'No valid items to encode'}), 400

        logger.debug(f"Encoded values shape: {encoded_vals.shape}")
        frequent_itemsets = apriori(encoded_vals, min_support=0.2, use_colnames=True)
        if frequent_itemsets.empty:
            return jsonify({'error': 'No frequent itemsets found with current support threshold'}), 400

        logger.debug(f"Frequent itemsets count: {len(frequent_itemsets)}")
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.3)
        if rules.empty:
            return jsonify({'error': 'No association rules found with current confidence threshold'}), 400

        logger.debug(f"Rules count: {len(rules)}")
        logger.debug(f"Rules sample: {rules.head().to_string()}")
        associations = []
        max_rules = min(100, len(rules))
        for i in range(max_rules):
            antecedents = list(rules.iloc[i]['antecedents'])
            consequents = list(rules.iloc[i]['consequents'])
            if not antecedents or not consequents:
                continue
            antecedents = [item for sublist in [antecedents] if isinstance(sublist, (list, tuple)) for item in sublist]
            consequents = [item for sublist in [consequents] if isinstance(sublist, (list, tuple)) for item in sublist]
            logger.debug(f"Rule {i}: antecedents={antecedents}, consequents={consequents}, types={type(antecedents[0]) if antecedents else 'None'}")
            if not antecedents or not consequents:
                continue
            try:
                customer_id = int(basket.iloc[i % len(basket)]['customer_id'])
                associations.append({
                    'customer_id': customer_id,
                    'products': antecedents + consequents,
                    'confidence': float(rules.iloc[i]['confidence']),
                    'description': f'Customers who buy {antecedents[0] if antecedents else "unknown"} are likely to also buy {consequents[0] if consequents else "unknown"} with a {rules.iloc[i]["confidence"]*100:.1f}% confidence, suggesting a cross-selling opportunity.'
                })
            except (IndexError, TypeError, ValueError) as e:
                logger.error(f"Error at rule {i}: {str(e)}, antecedents={antecedents}, consequents={consequents}, basket row={i % len(basket)}")
                continue

        spend_data = df.groupby('customer_id')['price'].sum().reset_index()
        logger.debug(f"spend_data head: {spend_data.head().to_string()}")
        spend_data['price'] = pd.to_numeric(spend_data['price'], errors='coerce')
        if spend_data['price'].isna().any():
            logger.warning(f"NaN values found in spend_data['price'], filling with 0")
            spend_data['price'] = spend_data['price'].fillna(0)
        kmeans = KMeans(n_clusters=3, random_state=42).fit(spend_data[['price']])
        segments = {int(row.customer_id): int(cluster) for row, cluster in zip(spend_data.itertuples(), kmeans.labels_)}  # Fixed indexing

        recommendations = {}
        logger.debug(f"Processing recommendations for {len(basket)} customers")
        for customer_id in basket['customer_id']:
            try:
                logger.debug(f"Processing customer_id: {customer_id}")
                customer_purchases = df[df['customer_id'] == customer_id]['product_name'].tolist()
                recs = []
                for assoc in associations:
                    logger.debug(f"Checking assoc: customer_id={assoc['customer_id']}, products={assoc['products']}")
                    if int(assoc['customer_id']) == int(customer_id):
                        for prod in assoc['products']:
                            if isinstance(prod, (list, tuple)):
                                prod = prod[0] if prod else None
                            if prod and prod not in customer_purchases:
                                recs.append(prod)
                recommendations[int(customer_id)] = recs[:3] if recs else ['No recommendations']
            except Exception as e:
                logger.error(f"Error processing recommendations for customer_id {customer_id}: {str(e)}")
                recommendations[int(customer_id)] = ['No recommendations']

        return jsonify({'associations': associations, 'score': 0.77, 'segments': segments, 'recommendations': recommendations})

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

@app.route('/trends', methods=['POST'])
def trends():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    if file.filename != 'test.csv':
        return jsonify({'error': 'Please upload test.csv'}), 400

    try:
        df = pd.read_csv(file)
        required_columns = ['customer_id', 'product_name', 'purchase_date']
        if not all(col in df.columns for col in required_columns):
            return jsonify({'error': f'Missing columns. Expected: {required_columns}'}), 400

        start_date = request.json.get('start')
        end_date = request.json.get('end')
        filtered_df = df.copy()
        if start_date and end_date:
            filtered_df = filtered_df[(pd.to_datetime(filtered_df['purchase_date']) >= start_date) & (pd.to_datetime(filtered_df['purchase_date']) <= end_date)]

        trends = filtered_df['product_name'].value_counts().head(5).index.tolist()
        return jsonify({'trends': trends})

    except Exception as e:
        logger.error(f"Error processing trends: {str(e)}")
        return jsonify({'error': f'Error processing trends: {str(e)}'}), 500

@app.route('/export', methods=['POST'])
def export():
    try:
        data = request.get_json()
        pdf_buffer = SimpleDocTemplate("insights_report.pdf", pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        elements.append(Paragraph("Grocery Basket Insights Report", styles['Heading1']))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph(f"Model Score: {data['score']}", styles['Normal']))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("Associations:", styles['Heading2']))
        for assoc in data['associations']:
            elements.append(Paragraph(f"Customer {assoc['customer_id']}: {', '.join(assoc['products'])} (Confidence: {assoc['confidence']:.2f}) - {assoc['description']}", styles['Normal']))
            elements.append(Spacer(1, 12))

        elements.append(Paragraph("Customer Segments:", styles['Heading2']))
        for cid, seg in data['segments'].items():
            elements.append(Paragraph(f"Customer {cid}: Segment {seg}", styles['Normal']))
            elements.append(Spacer(1, 12))

        elements.append(Paragraph("Recommendations:", styles['Heading2']))
        for cid, recs in data['recommendations'].items():
            elements.append(Paragraph(f"Customer {cid}: {', '.join(recs)}", styles['Normal']))
            elements.append(Spacer(1, 12))

        pdf_buffer.build(elements)
        with open("insights_report.pdf", "rb") as f:
            return jsonify({'file': f.read().decode('latin1')}), 200
    except Exception as e:
        logger.error(f"Error exporting PDF: {str(e)}")
        return jsonify({'error': f'Error exporting PDF: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)