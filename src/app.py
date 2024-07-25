from flask import Flask, request


app = Flask(__name__)

@app.route('/test', methods=['POST'])
def webhook():
    json_data = request.get_json()
    print(json_data)

    return ''

if __name__ == '__main__':
    app.run(port=3444, debug=True)