import webbrowser
import os
import json
import requests

# Read the token and playlist ID from the file
with open(r'G:\eMO\MoodTunes\new.txt', 'r') as f:
    data = json.load(f)
    token = data['token']
    playlist_id = data['playlist']

# Fetch playlist data
headers = {
    'Authorization': f'Bearer {token}'
}
response = requests.get(f'https://api.spotify.com/v1/playlists/{playlist_id}', headers=headers)
playlist_data = response.json()


def generate_tracks_html(tracks):
    html = ""
    for i, item in enumerate(tracks, 1):
        track = item['track']
        duration_ms = track['duration_ms']
        minutes, seconds = divmod(duration_ms // 1000, 60)
        html += f'''
        <li data-uri="{track['uri']}">
            <span class="track-number">{i}</span>
            <div class="track-info">
                <div class="track-title">{track['name']}</div>
                <div class="track-artist">{', '.join(artist['name'] for artist in track['artists'])}</div>
            </div>
            <span class="track-duration">{minutes}:{seconds:02d}</span>
        </li>
        '''
    return html
# Generate tracks HTML
tracks_html = generate_tracks_html(playlist_data['tracks']['items'])

# HTML content
html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>MoodTunes - Your Personalized Music Experience</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.7.2/font/bootstrap-icons.min.css" rel="stylesheet">
    <style>
        body {{
            background-color: #121212;
            color: #ffffff;
            font-family: 'Arial', sans-serif;
        }}
        .content-wrapper {{
            background-color: #181818;
            border-radius: 8px;
            padding: 2rem;
            margin-top: 2rem;
        }}
        .logo {{
            font-size: 2rem;
            font-weight: bold;
            color: #1DB954;
            margin-bottom: 1rem;
        }}
        #playlist-info {{
            display: flex;
            align-items: center;
            margin-bottom: 2rem;
        }}
        #playlist-info img {{
            width: 200px;
            height: 200px;
            object-fit: cover;
            margin-right: 2rem;
        }}
        #tracks-list {{
            list-style-type: none;
            padding: 0;
        }}
        #tracks-list li {{
            padding: 0.5rem 0;
            border-bottom: 1px solid #282828;
            display: flex;
            align-items: center;
        }}
        #tracks-list li:hover {{
            background-color: #282828;
        }}
        .track-number {{
            width: 30px;
            text-align: right;
            margin-right: 1rem;
            color: #b3b3b3;
        }}
        .track-info {{
            flex-grow: 1;
        }}
        .track-title {{
            font-weight: bold;
        }}
        .track-artist {{
            color: #b3b3b3;
        }}
        .track-duration {{
            color: #b3b3b3;
        }}
        #videoElement {{
            width: 320px;
            height: 240px;
            border-radius: 8px;
            margin-top: 20px;
            transform: scaleX(-1);
        }}
        #cursor {{
            position: fixed;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background-color: #1DB954;
            pointer-events: none;
            z-index: 10000;
            transform: translate(-50%, -50%);
        }}
        .container {{
    display: flex;
    justify-content: space-between;
}}

.content-wrapper {{
    display: flex;
    width: 100%;
}}

.left-section {{
    flex: 2;
    padding-right: 20px;
}}

.right-section {{
    flex: 1;
    padding-left: 20px;
}}

#playlist-info {{
    display: flex;
    align-items: center;
}}

#playlist-info img {{
    margin-right: 20px;
    max-width: 150px;
}}

#gestureDisplay {{
    font-weight: bold;
}}

#videoElement {{
    width: 100%;
    max-width: 300px;
    border: 2px solid #ddd;
    border-radius: 8px;
}}

    </style>
</head>
<body>
    <div id="cursor"></div>
<div class="container">
    <div class="content-wrapper">
        <div class="left-section">
            <h1 class="logo">MoodTunes</h1>
            <div id="playlist-info">
                <img src="{playlist_data['images'][0]['url']}" alt="Playlist Cover">
                <div>
                    <h2>{playlist_data['name']}</h2>
                    <p>{playlist_data['description']}</p>
                    <p>{len(playlist_data['tracks']['items'])} tracks</p>
                </div>
            </div>
            <ul id="tracks-list">
                {tracks_html}
            </ul>
            <div class="text-center mt-4">
                <button id="togglePlay" class="btn btn-success">Play/Pause</button>
                <button id="nextTrack" class="btn btn-primary">Next Track</button>
                <button id="previousTrack" class="btn btn-primary">Previous Track</button>
            </div>
        </div>
        <div class="right-section">
            <div class="text-center mt-4">
                <h3>Current Gesture: <span id="gestureDisplay">No gesture detected</span></h3>
                <video id="videoElement" autoplay></video>
            </div>
        </div>
    </div>
</div>


    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/control_utils/control_utils.js" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/drawing_utils/drawing_utils.js" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js" crossorigin="anonymous"></script>
    <script src="https://sdk.scdn.co/spotify-player.js"></script>
    <script>
    const videoElement = document.getElementById('videoElement');
    const gestureDisplay = document.getElementById('gestureDisplay');
    const cursor = document.getElementById('cursor');
    const togglePlayButton = document.getElementById('togglePlay');
    const nextTrackButton = document.getElementById('nextTrack');
    const previousTrackButton = document.getElementById('previousTrack');
    let lastGesture = '';
    let gestureStartTime = 0;

    const gestureDuration = 1000;
    let lastVolumeUpdateTime = 0;
    const volumeUpdateInterval = 200;
    const volumeChangeThreshold = 0.02;
    let lastClickTime = 0;
    const clickCooldown = 500;
    let player;
    

        const playlistData = {json.dumps(playlist_data)};
            async function fetchAndDisplayPlaylist(playlistId, token) {{
        try {{
            const response = await fetch(`https://api.spotify.com/v1/playlists/${{playlistId}}`, {{
                headers: {{
                    'Authorization': `Bearer ${token}`
                }}
            }});

            if (!response.ok) {{
                throw new Error(`HTTP error! status: ${{response.status}}`);
            }}

            const data = await response.json();
            const tracks = data.tracks.items;

            const playlistElement = document.getElementById('playlist');
            playlistElement.innerHTML = '<h2>' + data.name + '</h2>';
            
            const trackList = document.createElement('ul');
            tracks.forEach((item, index) => {{
                const track = item.track;
                const li = document.createElement('li');
                li.textContent = `${{index + 1}}. ${{track.name}} - ${{track.artists[0].name}}`;
                li.onclick = () => playTrack(index);
                trackList.appendChild(li);
            }});
            
            playlistElement.appendChild(trackList);
        }} catch (error) {{
            console.error('Error fetching playlist:', error);
        }}
    }}
        function playTrack(index) {{
        if (player) {{
            player.getCurrentState().then(state => {{
                if (state && state.track_window.current_track) {{
                    const currentIndex = state.track_window.previous_tracks.length;
                    const offset = index - currentIndex;
                    if (offset > 0) {{
                        player.nextTrack().then(() => {{
                            playTrack(index);
                        }});
                    }} else if (offset < 0) {{
                        player.previousTrack().then(() => {{
                            playTrack(index);
                        }});
                    }} else {{
                        player.togglePlay();
                    }}
                }} else {{
                    player.resume();
                }}
            }});
        }}
    }}
        window.onSpotifyWebPlaybackSDKReady = () => {{
            const token = '{token}';
            console.log('Token (first 10 chars):', token.substring(0, 10));
            
            player = new Spotify.Player({{
                name: 'MoodTunes Web Player',
                getOAuthToken: cb => {{ cb(token); }},
                volume: 0.5
            }});

            player.addListener('initialization_error', ({{ message }}) => {{ console.error('Failed to initialize', message); }});
            player.addListener('authentication_error', ({{ message }}) => {{ console.error('Failed to authenticate', message); }});
            player.addListener('account_error', ({{ message }}) => {{ console.error('Failed to validate Spotify account', message); }});
            player.addListener('playback_error', ({{ message }}) => {{ console.error('Failed to perform playback', message); }});

            player.addListener('ready', ({{ device_id }}) => {{
                console.log('Ready with Device ID', device_id);
                // Start playing the playlist
                fetch(`https://api.spotify.com/v1/me/player/play?device_id=${{device_id}}`, {{
                    method: 'PUT',
                    body: JSON.stringify({{ context_uri: `spotify:playlist:{playlist_id}` }}),
                    headers: {{
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${{token}}`
                    }}
                }});
            }});

            player.addListener('not_ready', ({{ device_id }}) => {{
                console.log('Device ID has gone offline', device_id);
            }});

            player.addListener('player_state_changed', state => {{
                if (state) {{
                    console.log('Currently playing:', state.track_window.current_track.name);
                    updateCurrentTrack(state.track_window.current_track);
                }}
            }});

            player.connect();
        }};

        function updateCurrentTrack(track) {{
            const trackElements = document.querySelectorAll('#tracks-list li');
            trackElements.forEach(el => el.classList.remove('text-success'));
            const currentTrackElement = document.querySelector(`#tracks-list li[data-uri="${{track.uri}}"]`);
            if (currentTrackElement) {{
                currentTrackElement.classList.add('text-success');
            }}
        }}

        function togglePlay() {{
            player.togglePlay().then(() => {{
                console.log('Toggled playback');
            }});
        }}

        function nextTrack() {{
            player.nextTrack().then(() => {{
                console.log('Skipped to next track');
            }});
        }}

        function previousTrack() {{
            player.previousTrack().then(() => {{
                console.log('Skipped to previous track');
            }});
        }}

            function onResults(results) {{
        if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {{
            const landmarks = results.multiHandLandmarks[0];
            const gesture = detectGesture(landmarks);
            gestureDisplay.textContent = gesture;

            const indexTip = landmarks[8];
            moveCursor(indexTip.x, indexTip.y);

            if (gesture === lastGesture) {{
                if (Date.now() - gestureStartTime >= gestureDuration) {{
                    handleGesture(gesture);
                }}
            }} else {{
                lastGesture = gesture;
                gestureStartTime = Date.now();
                initialThumbIndexDistance = null;
            }}
        }} else {{
            gestureDisplay.textContent = "No hand detected";
            lastGesture = '';
        }}
    }}

        const hands = new Hands({{locateFile: (file) => {{
            return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${{file}}`;
        }}}});
    hands.setOptions({{
        maxNumHands: 1,
        modelComplexity: 1,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5
    }});

    hands.onResults(onResults);

    const camera = new Camera(videoElement, {{
        onFrame: async () => {{
            await hands.send({{image: videoElement}});
        }},
        width: 320,
        height: 240
    }});

    camera.start();

    function detectGesture(landmarks) {{
        const thumbTip = landmarks[4];
        const indexTip = landmarks[8];
        const middleTip = landmarks[12];
        const ringTip = landmarks[16];
        const pinkyTip = landmarks[20];

        const palmBase = landmarks[0];

        // Calculate distances from each fingertip to the palm base
        const distances = [thumbTip, indexTip, middleTip, ringTip, pinkyTip].map(tip => 
            calculateDistance(tip, palmBase)
        );
        const closeThreshold = 0.1; 
        const allFingersClosed = distances.every(distance => distance < closeThreshold);
        if (thumbTip.y < indexTip.y && thumbTip.y < middleTip.y && thumbTip.y < ringTip.y && thumbTip.y < pinkyTip.y) {{
            return "Thumbs Up";
        }} else if (thumbTip.y > indexTip.y && thumbTip.y > middleTip.y && thumbTip.y > ringTip.y && thumbTip.y > pinkyTip.y) {{
            return "Thumbs Down";
        }} else if (indexTip.y < middleTip.y && middleTip.y < ringTip.y && ringTip.y < pinkyTip.y) {{
            return "Volume Up";
        }} else if (pinkyTip.y) {{
            return "Volume Down";
        }} else if (isPinchGesture(landmarks)) {{
            return "Pinch";
        }} else {{
            return "Moving";
        }}
    }}


    function isPinchGesture(landmarks) {{
        const thumbTip = landmarks[4];
        const indexTip = landmarks[8];
        
        // Calculate the distance between thumb tip and index tip
        const distance = Math.sqrt(
            Math.pow(thumbTip.x - indexTip.x, 2) +
            Math.pow(thumbTip.y - indexTip.y, 2) +
            Math.pow(thumbTip.z - indexTip.z, 2)
        );
        
        // You may need to adjust this threshold based on testing
        const pinchThreshold = 0.05;
        
        return distance < pinchThreshold;
    }}

    function moveCursor(x, y) {{
        const screenX = window.innerWidth * (1 - x);
        const screenY = window.innerHeight * y;

        cursor.style.left = `${{screenX}}px`;
        cursor.style.top = `${{screenY}}px`;
    }}

    function performClick() {{
        const currentTime = Date.now();
        if (currentTime - lastClickTime < clickCooldown) {{
            console.log('Click cooldown active');
            return;
        }}
        lastClickTime = currentTime;

        const cursorRect = cursor.getBoundingClientRect();
        const x = cursorRect.left + cursorRect.width / 2;
        const y = cursorRect.top + cursorRect.height / 2;

        const clickEvent = new MouseEvent('click', {{
            bubbles: true,
            cancelable: true,
            view: window,
            clientX: x,
            clientY: y
        }});
        document.elementFromPoint(x, y)?.dispatchEvent(clickEvent);

        console.log('Click performed at:', x, y);
    }}

    function handleGesture(gesture) {{
        switch(gesture) {{
            case "Thumbs Up":
                togglePlay();
                break;
            case "Thumbs Down":
                nextTrack();
                break;
            case "Volume Up":
                adjustVolume('up');
                break;
            case "Volume Down":
                adjustVolume('down')
                break;
            case "Pinch":
                performClick();
                break;
        }}
    }}
    // Helper function to calculate distance between two 3D points
    function calculateDistance(point1, point2) {{
        return Math.sqrt(
            Math.pow(point1.x - point2.x, 2) +
            Math.pow(point1.y - point2.y, 2) +
            Math.pow(point1.z - point2.z, 2)
        );
    }}
    function adjustVolume(direction) {{
        fetch('http://localhost:8000/volume', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json',
            }},
            body: JSON.stringify({{ direction: direction }}),
        }})
        .then(response => response.text())
        .then(data => {{
            console.log('Success:', data);
        }})
        .catch((error) => {{
            console.error('Error:', error);
        }});
    }}

    // Add event listeners to the buttons
    document.getElementById('togglePlay').addEventListener('click', togglePlay);
    document.getElementById('nextTrack').addEventListener('click', nextTrack);
    document.getElementById('previousTrack').addEventListener('click', previousTrack);

        togglePlayButton.addEventListener('click', togglePlay);
        nextTrackButton.addEventListener('click', nextTrack);
        previousTrackButton.addEventListener('click', previousTrack);
    </script>
</body>
</html>
'''


# Write to new.html
output_path = r"G:\eMO\MoodTunes\new.html"
with open(output_path, "w", encoding="utf-8") as fp:
    fp.write(html_content)

# Open the new HTML file in the default web browser
webbrowser.open('file://' + os.path.realpath(output_path))