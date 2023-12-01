from flask import Flask, request, jsonify
from logger import set_logger
app_logger = set_logger(logger_name="MyApp")
last_result = None
app = Flask(__name__)

@app.route('/reverse')
def reverse():
    app_logger.info("inside reverse function")
    global last_result
    app_logger.info(f"last saved result is {last_result}")
    input_string = request.args.get('in','')
    app_logger.info(f"reversing the string {input_string}")
    if input_string == '':
        app_logger.error(f"Error : Received an empty string")
        app_logger.info("exiting reverse function with 400 status code")
        return jsonify({'error': "BadInput: Empty string"}), 400
    last_result = ' '.join(reversed(input_string.split()))
    app_logger.info(f"result of reversing is {last_result}")
    app_logger.info("exiting reverse function successfully")
    return jsonify({'result': last_result})

@app.route('/restore')
def restore():
    app_logger.info("inside restore function")
    global last_result
    app_logger.info(f"last saved result is {last_result}")
    if last_result is None:
        app_logger.info("exiting reverse function with 400 status code")
        return jsonify({'error': "No successful Invocation of reverse api has been recorded"}), 400
    app_logger.info("exiting reverse function successfully")
    return jsonify({'result': last_result})

@app.route('/status', methods=['GET'])
def status():
    app_logger.info("inside status function")
    return jsonify({'status': 'Service is up'})

if __name__ == '__main__':
    # port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(host='0.0.0.0', port=5000)

