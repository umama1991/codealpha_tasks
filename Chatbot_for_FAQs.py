# Import required libraries
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download necessary NLTK data

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')


from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# Step 1: Define FAQ dataset
faqs = {
    "What is your return policy?": "You can return any item within 30 days of purchase.",
    "How do I track my order?": "You can track your order using the tracking link sent to your email.",
    "Do you offer international shipping?": "Yes, we ship to most countries worldwide.",
    "What payment methods do you accept?": "We accept credit/debit cards, PayPal, and bank transfers.",
    "How can I contact customer service?": "You can email us at support@example.com or call +1 234 567 890."
}

# Step 2: Preprocessing function
def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return ' '.join(tokens)

# Step 3: Prepare data
questions = list(faqs.keys())
preprocessed_questions = [preprocess(q) for q in questions]

# Step 4: Create TF-IDF vectors
vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(preprocessed_questions)

# Step 5: Chatbot response function
def chatbot_response(user_query):
    user_query = preprocess(user_query)
    user_vector = vectorizer.transform([user_query])
    similarities = cosine_similarity(user_vector, faq_vectors)
    best_match = similarities.argmax()
    score = similarities[0][best_match]

    if score < 0.3:
        return "I'm sorry, I couldn’t find a relevant answer."
    else:
        return faqs[questions[best_match]]

# Step 6: Chat loop
print("🤖 Chatbot: Hi! Ask me anything about our store (type 'quit' to exit).")
while True:
    user_input = input("You: ")
    if user_input.lower() in ['quit', 'exit']:
        print("🤖 Chatbot: Goodbye!")
        break
    response = chatbot_response(user_input)
    print("🤖 Chatbot:", response)
