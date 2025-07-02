import pandas as pd

# Define customer reviews
reviews_data = [
    # Positive reviews
    {"Review": "Absolutely love this product! Exceeded my expectations and arrived quickly.", "Sentiment": "Positive"},
    {"Review": "Great quality and excellent customer service. Will definitely buy again!", "Sentiment": "Positive"},
    {"Review": "Five stars! Works perfectly and the packaging was very thoughtful.", "Sentiment": "Positive"},

    # Neutral reviews
    {"Review": "The product is okay. It works but nothing special.", "Sentiment": "Neutral"},
    {"Review": "Delivery took a bit longer than expected, but the item is fine.", "Sentiment": "Neutral"},
    {"Review": "Average experience. Not bad, but not outstanding either.", "Sentiment": "Neutral"},

    # Negative reviews
    {"Review": "Very disappointed. The item didn’t work as described.", "Sentiment": "Negative"},
    {"Review": "Customer support was unhelpful and slow to respond.", "Sentiment": "Negative"},
    {"Review": "The product arrived damaged and I had to return it.", "Sentiment": "Negative"},
]

# Create DataFrame
df_reviews = pd.DataFrame(reviews_data)

# Save to CSV
df_reviews.to_csv("customer_reviews.csv", index=False)

# Save to TXT (tab-separated format)
df_reviews.to_csv("customer_reviews.txt", sep='\t', index=False)
