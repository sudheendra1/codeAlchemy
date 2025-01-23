from flask import Flask, jsonify
import traceback

app = Flask(__name__)

@app.route('/')
def home():
    try:
        # Intentional error: undefined variable 'message'
        return jsonify(message)
    except Exception as e:
        # Print the stack trace when an error occurs
        print(f"Error: {e}")
        traceback.print_exc()
        return jsonify({"error": "An error occurred", "message": str(e)}), 500

@app.route('/error')
def error():
    try:
        # Another intentional error: division by zero
        result = 10 / 0
        return jsonify(result)
    except Exception as e:
        # Print the stack trace when an error occurs
        print(f"Error: {e}")
        traceback.print_exc()
        return jsonify({"error": "An error occurred", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
