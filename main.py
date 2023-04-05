from flask import Flask, render_template, jsonify, request
from utils.wgcf import get_wgcf
from utils.verify_recaptcha import submit
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["1 per minute"],
    storage_uri="memory://",
)

@app.route('/')
@limiter.limit("120 per minute")
def index():
  return render_template('index.html')


@app.route('/api', methods=['POST'])
@limiter.limit("1 per minute")
def api():
  try:
    recaptcha_key = "6LeMdl0lAAAAAH0pJfh16KYFKi_cFMgFCQM0cGMg" # Your recaptcha key
    json = request.get_json()
    method = json['method']
    extra = json['extra']
    recaptcha = json["recaptcha_code"]
    remoteip = request.remote_addr
    if submit(recaptcha_key, recaptcha, remoteip)[0] == False:
      return jsonify({"error": "Recaptcha failed", "success": False})
    else:
      result = get_wgcf(method, extra)
  except Exception as e:
    return jsonify({"error": str(e), "success": False})
  return jsonify({"result": result, "success": True})
    


if __name__ == '__main__':
  app.run()