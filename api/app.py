from flask import Flask, request, jsonify
import spacy

# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome to the SpaCy NLP Flask API!"


@app.route('/analyze', methods=['POST'])
def analyze_text():
    # Get the text from the request
    data = request.json
    text = data.get('text', '')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Process the text using SpaCy
    doc = nlp(text)

    # Extract tokens, entities, and more
    tokens = [token.text for token in doc]
    entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
    noun_chunks = [chunk.text for chunk in doc.noun_chunks]

    return jsonify({
        "tokens": tokens,
        "entities": entities,
        "noun_chunks": noun_chunks
    })


@app.route('/similarity', methods=['POST'])
def sentence_similarity():
    data = request.json
    sentence1 = data.get('sentence1', '')
    sentence2 = data.get('sentence2', '')

    if not sentence1 or not sentence2:
        return jsonify({"error": "Both sentences are required"}), 400

    # Create SpaCy Doc objects for both sentences
    doc1 = nlp(sentence1)
    doc2 = nlp(sentence2)

    # Calculate similarity
    similarity = doc1.similarity(doc2)

    return jsonify({"similarity": similarity})


if __name__ == '__main__':
    app.run(debug=True)
