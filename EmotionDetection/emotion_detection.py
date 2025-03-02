import requests
import json

def emotion_detector(text_to_analyse):
    """Function to detect emotion from the given text using Watson NLP."""
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text_to_analyse } }

    if not text_to_analyse.strip():  # Check for empty input
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None
        }

    response = requests.post(url, headers=headers, json=input_json)
    
    if response.status_code == 400:  # Handle bad request response
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None
        }

    if response.status_code == 200:
        response_json = response.json()
        
        emotions_list = response_json.get("emotionPredictions", [])
        if not emotions_list:
            return {
                "anger": None,
                "disgust": None,
                "fear": None,
                "joy": None,
                "sadness": None,
                "dominant_emotion": None
            }

        emotions = emotions_list[0].get("emotion", {})

        emotion_scores = {
            "anger": emotions.get("anger", None),
            "disgust": emotions.get("disgust", None),
            "fear": emotions.get("fear", None),
            "joy": emotions.get("joy", None),
            "sadness": emotions.get("sadness", None),
        }

        # Determine dominant emotion (only if at least one emotion is not None)
        dominant_emotion = max(emotion_scores, key=emotion_scores.get) if any(emotion_scores.values()) else None

        emotion_scores["dominant_emotion"] = dominant_emotion

        return emotion_scores

    return {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None
    }
