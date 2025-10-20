from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Main menu page with Game of Life background animation"""
    return render_template('index.html')

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Print some debug info
    print("=== Amides WebApp Menu Server ===")
    print(f"Templates directory: {os.path.abspath('templates')}")
    print(f"Index file exists: {os.path.exists('templates/index.html')}")
    print("==================================")
    
    app.run(debug=True, host='0.0.0.0', port=8000)

