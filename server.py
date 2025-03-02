"""
Flask web server for the Emotion Detection application.

This application provides an API for analyzing emotions in text
using the Watson NLP Emotion Detection model. It accepts GET and POST
requests and returns emotion scores with the dominant emotion.
"""

from flask import Flask, render_template, jsonify, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detection")

@app.route('/')
def index():
    """Render the homepage."""
    return render_template("index.html")

@app.route('/emotionDetector', methods=['GET', 'POST'])
def detect_emotion():
    """
    API endpoint to analyze emotions in the given text.
    
    - Accepts both GET and POST requests.
    - Returns emotion scores and the dominant emotion.
    
    Returns:
        JSON response containing the emotion analysis or an error message.
    """

    text = ""

    if request.method == 'POST':
        data = request.json
        text = data.get("text", "")

    elif request.method == 'GET':
        text = request.args.get("textToAnalyze", "")

    print(f"DEBUG: Received text - {text}")  # Debugging print

    result = emotion_detector(text)

    # Handle case where no valid emotions were detected
    if result["dominant_emotion"] is None:
        return jsonify({"error": "Invalid text! Please try again!"}), 400

    response_text = (
        f"For the given statement, the system response is 'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, 'fear': {result['fear']}, "
        f"'joy': {result['joy']} and 'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )

    return response_text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
