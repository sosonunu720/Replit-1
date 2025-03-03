import os
import logging
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

# Configure Gemini API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_response(prompt):
    try:
        # Use the gemini-1.5-flash model directly
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate response
        response = model.generate_content(prompt)
        return True, response.text
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return False, str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.json.get('prompt', '')
    if not prompt:
        return jsonify({'success': False, 'message': 'No prompt provided'})

    success, response = get_gemini_response(prompt)
    return jsonify({
        'success': success,
        'message': response
    })

@app.route('/model-info')
def model_info():
    try:
        available_models = []
        for model in genai.list_models():
            model_info = {
                'name': model.name,
                'display_name': model.display_name,
                'supported_methods': model.supported_generation_methods
            }
            available_models.append(model_info)
        
        return jsonify({
            'success': True,
            'models': available_models
        })
    except Exception as e:
        logger.error(f"Error listing models: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
