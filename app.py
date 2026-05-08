from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# ========== إعدادات OTMAN ==========
DEVELOPER = "@otman_v2"
API_NAME = "OTMAN JWT GENERATOR API"
VERSION = "1.0"

# حسابك الضيف فقط
GUEST_UID = "4683806909"
GUEST_PASSWORD = "7380D7DE7CC34F23AE7A3EB0DAA83E5941E56473F9FD1E8B8EFDD1EB5649DE63"

# ========== نقاط النهاية ==========

@app.route('/')
def home():
    return jsonify({
        "name": API_NAME,
        "version": VERSION,
        "developer": DEVELOPER,
        "account_used": GUEST_UID,
        "endpoints": {
            "/get": "الحصول على JWT (استخدم ?uid= و &password=)",
            "/health": "فحص حالة API"
        }
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "api": API_NAME,
        "developer": DEVELOPER,
        "account_used": GUEST_UID
    })

@app.route('/get')
def get_jwt():
    # جلب المعاملات من الرابط
    uid = request.args.get('uid')
    password = request.args.get('password')
    
    # استخدام حسابك إذا لم يتم إرسال أي معاملات
    if not uid:
        uid = GUEST_UID
        password = GUEST_PASSWORD
    
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;US;)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    }
    
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    
    try:
        response = requests.post(url, headers=headers, data=data, timeout=15)
        result = response.json()
        
        if response.status_code == 200 and "access_token" in result:
            return jsonify({
                "success": True,
                "developer": DEVELOPER,
                "uid": uid,
                "access_token": result.get("access_token"),
                "open_id": result.get("open_id"),
                "message": "تم جلب JWT بنجاح"
            })
        else:
            return jsonify({
                "success": False,
                "developer": DEVELOPER,
                "error": "فشل في الحصول على التوكن",
                "details": result
            }), 400
            
    except Exception as e:
        return jsonify({
            "success": False,
            "developer": DEVELOPER,
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
