from flask import Flask
from flask_cors import CORS
from config import is_production
from routes.health_routes import health_bp



def create_app():
    """
    Application factory pattern to create and configure the Flask app.
    """
    
    # Create application instance
    app = Flask(__name__)
    
    # Configure Flask for better performance with large responses
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for development
    
    # Enable CORS for all routes
    CORS(app, expose_headers=['Content-Disposition'])
    
    # Register blueprints
    app.register_blueprint(health_bp, url_prefix='/api/v1')
    
    return app


# Create the Flask app instance
app = create_app()


# @app.route('/')
# def home():
#     return {"message": "Flask on Vercel!"}

# Required for both local and Vercel
if __name__ == '__main__':
    debug_mode = True if not is_production else False
    app.run(debug=debug_mode, threaded=True, host='0.0.0.0', port=5328)