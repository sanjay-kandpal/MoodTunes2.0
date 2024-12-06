from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import platform
import ctypes

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes and origins

def change_volume_windows(direction):
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    
    # Initialize COM library
    ctypes.windll.ole32.CoInitialize(None)
    
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    current_volume = volume.GetMasterVolumeLevelScalar()
    
    if direction == 'up':
        new_volume = min(1.0, current_volume + 0.1)
    else:
        new_volume = max(0.0, current_volume - 0.1)
    
    volume.SetMasterVolumeLevelScalar(new_volume, None)
    
    # Uninitialize COM library
    ctypes.windll.ole32.CoUninitialize()

def change_volume_linux(direction):
    if direction == 'up':
        os.system("amixer -q sset Master 10%+")
    else:
        os.system("amixer -q sset Master 10%-")

@app.route('/volume', methods=['POST', 'OPTIONS'])
def change_volume():
    if request.method == 'OPTIONS':
        # Handling preflight request
        return jsonify({}), 200
    
    direction = request.json.get('direction')
    
    try:
        if platform.system() == 'Windows':
            change_volume_windows(direction)
        elif platform.system() == 'Linux':
            change_volume_linux(direction)
        else:
            return jsonify({"error": "Unsupported operating system"}), 400
        
        return jsonify({"message": "Volume adjusted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)