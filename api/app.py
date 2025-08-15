from flask import Flask

# Create application instance
app = Flask(__name__)

@app.route('/')
def home():
    return {"message": "Flask on Vercel!"}

# Required for both local and Vercel
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
else:
    # For Vercel
    application = app