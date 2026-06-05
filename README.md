# Ingredient Intelligence: Sephora Product & Review Analytics

An interactive Streamlit dashboard analyzing Sephora product ingredients, surfactant trends, brand formulation profiles, pricing patterns, and customer review language.

## Project Overview

This project applies data science and chemical-industry context to a public Sephora product and review dataset. Instead of treating beauty products as generic retail items, the analysis focuses on surfactants and ingredient positioning: how premium personal care brands appear to be shifting away from traditional sulfates toward milder or greener cleansing systems.

The app is designed as a portfolio project for data science, data analytics, and business analytics roles, especially in CPG, personal care, specialty chemicals, and supply chain-adjacent industries.

## Business Questions

- Which surfactants appear most frequently across Sephora products?
- How does surfactant usage vary by product category?
- What does each brand's formulation profile look like?
- Do products using mild or green surfactants differ in price or rating?
- What themes appear in customer review text for selected products?

## Features

- **Surfactant Frequency Analysis**  
  Tracks traditional sulfate surfactants and mild/green alternatives across the product catalog.

- **Category Filtering**  
  Allows users to filter product categories and compare formulation patterns across segments.

- **Brand Explorer**  
  Searchable brand selector showing surfactant profile, average product rating, average price, and top-rated products.

- **Review Intelligence**  
  Lightweight NLP-style text mining on customer review text, including theme counts, frequent terms, positive review examples, and critical review examples.

- **Price vs. Formulation**  
  Interactive Plotly scatter plot connecting price, rating, and surfactant type.

- **Portfolio UI**  
  Custom Streamlit styling with a polished editorial dashboard layout.

## Dataset

Source: Public Sephora product and skincare review dataset from Kaggle.

Main files used:

- `product_info.csv`
- `reviews_0-250.csv`
- `reviews_250-500.csv`
- `reviews_500-750.csv`
- `reviews_750-1250.csv`
- `reviews_1250-end.csv`

The product catalog includes product names, brands, ingredients, prices, ratings, categories, and product-level review counts. The review files include customer review text, ratings, recommendation flags, and product IDs.

Note: Some brands appear in the product catalog but do not have matching detailed review-text rows in the review files. In those cases, the app still shows product-level catalog metrics, but Review Intelligence displays a data coverage message.

## Methods Used

- Data cleaning and joining with `pandas`
- Ingredient keyword detection for surfactant classification
- Category and brand-level aggregation
- Interactive charting with `Plotly`
- Lightweight review text mining using Python regex and word counts
- Streamlit app development and custom CSS styling

## Surfactants Tracked

Traditional surfactants:

- Sodium Lauryl Sulfate
- Sodium Laureth Sulfate
- Ammonium Lauryl Sulfate
- Ammonium Laureth Sulfate
- SLS / SLES mentions

Mild / green surfactants:

- Cocamidopropyl Betaine
- Coco-Glucoside
- Decyl Glucoside
- Sodium Cocoyl Isethionate
- Lauryl Glucoside
- Disodium Laureth Sulfosuccinate

## How To Run Locally

1. Clone or download this project folder.
2. Place the Sephora CSV files in the same folder as `app.py`.
3. Install dependencies:

```bash
pip3 install -r requirements.txt
```

4. Start the Streamlit app:

```bash
streamlit run app.py
```

5. Open the local URL shown by Streamlit, usually:

```text
http://localhost:8501
```

## Key Takeaways

- Mild surfactants appear more frequently than traditional sulfate systems across the Sephora catalog.
- Cocamidopropyl betaine is the dominant detected surfactant, consistent with premium personal care positioning around mildness and foam quality.
- Brand-level views help connect formulation strategy with price and customer ratings.
- Review text adds qualitative context by surfacing customer concerns around hydration, irritation, scent, texture, cleansing power, and value.

## Portfolio Framing

This project demonstrates the ability to combine:

- data science workflows,
- domain-specific chemical industry knowledge,
- product and customer analytics,
- interactive dashboard development,
- and business interpretation.

It is intended to show more than generic dashboarding: the analytical framing is specific to personal care formulation and specialty chemical trends.

## Future Improvements

- Add historical product trend data if available.
- Expand ingredient detection beyond surfactants to preservatives, actives, oils, fragrance allergens, and claims.
- Add clustering or topic modeling for review themes.
- Deploy with a proper data-hosting strategy for large review CSV files.
