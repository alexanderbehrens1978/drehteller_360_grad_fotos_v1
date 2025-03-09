# Datei: app/utils/templates.py
# Modul mit Templates für HTML, CSS und JavaScript

import json

def get_index_html_template(config):
    """Liefert das HTML-Template für den 360°-Viewer"""
    return f'''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config['project_name']} - 360° Ansicht</title>
    <link rel="stylesheet" href="css/viewer.css">
</head>
<body>
    <div class="viewer-container">
        <div class="viewer-header">
            <h1>{config['project_name']}</h1>
            <p>{config['session_name']}</p>
        </div>
        
        <div class="viewer-content">
            <div id="viewer360" class="viewer-360">
                <img id="currentImage" src="images/frame_000.jpg" alt="360° Ansicht">
                <div class="viewer-controls">
                    <button id="playPauseBtn" class="control-btn">Pause</button>
                    <input type="range" id="rotationSlider" min="0" max="{len(config['images']) - 1}" value="0" class="slider">
                </div>
            </div>
        </div>
        
        <div class="viewer-footer">
            <p>Erstellt mit 360° Drehteller Fotografie-System</p>
        </div>
    </div>
    
    <script src="js/viewer.js"></script>
</body>
</html>'''

def get_viewer_js_template(config):
    """Liefert das JavaScript-Template für den 360°-Viewer"""
    js_template = '''// 360° Viewer JavaScript

// Konfiguration
const viewerConfig = CONFIG_JSON;

// Elemente
const currentImage = document.getElementById('currentImage');
const rotationSlider = document.getElementById('rotationSlider');
const playPauseBtn = document.getElementById('playPauseBtn');

// Variablen
let currentFrame = 0;
let isPlaying = true;
let animationId = null;
let lastDragX = 0;
let isDragging = false;
let autoRotationSpeed = 0.2; // Frames pro Animation

// Bild laden
function loadFrame(frameIndex) {
    currentFrame = frameIndex;
    rotationSlider.value = frameIndex;
    currentImage.src = viewerConfig.images[frameIndex].path;
}

// Animation starten/stoppen
function togglePlayPause() {
    isPlaying = !isPlaying;
    playPauseBtn.textContent = isPlaying ? 'Pause' : 'Play';
    
    if (isPlaying) {
        startAnimation();
    } else {
        stopAnimation();
    }
}

// Animation starten
function startAnimation() {
    if (animationId) return;
    
    function animate() {
        currentFrame = (currentFrame + autoRotationSpeed) % viewerConfig.total_frames;
        loadFrame(Math.floor(currentFrame));
        animationId = requestAnimationFrame(animate);
    }
    
    animationId = requestAnimationFrame(animate);
}

// Animation stoppen
function stopAnimation() {
    if (animationId) {
        cancelAnimationFrame(animationId);
        animationId = null;
    }
}

// Event-Listener
playPauseBtn.addEventListener('click', togglePlayPause);

rotationSlider.addEventListener('input', function() {
    stopAnimation();
    isPlaying = false;
    playPauseBtn.textContent = 'Play';
    loadFrame(parseInt(this.value));
});

// Touch/Maus-Steuerung
const viewer = document.getElementById('viewer360');

viewer.addEventListener('mousedown', handleDragStart);
viewer.addEventListener('touchstart', handleDragStart);

window.addEventListener('mousemove', handleDragMove);
window.addEventListener('touchmove', handleDragMove);

window.addEventListener('mouseup', handleDragEnd);
window.addEventListener('touchend', handleDragEnd);

function handleDragStart(event) {
    event.preventDefault();
    stopAnimation();
    isPlaying = false;
    playPauseBtn.textContent = 'Play';
    isDragging = true;
    lastDragX = event.clientX || event.touches[0].clientX;
}

function handleDragMove(event) {
    if (!isDragging) return;
    event.preventDefault();
    
    const clientX = event.clientX || event.touches[0].clientX;
    const deltaX = clientX - lastDragX;
    lastDragX = clientX;
    
    // Berechne die Anzahl der zu verschiebenden Frames
    const framesToMove = -Math.sign(deltaX) * Math.ceil(Math.abs(deltaX) / 10);
    const newFrame = Math.floor((currentFrame + framesToMove + viewerConfig.total_frames) % viewerConfig.total_frames);
    
    loadFrame(newFrame);
}

function handleDragEnd() {
    if (!isDragging) return;
    isDragging = false;
    
    // Automatische Rotation nach Mausinteraktion fortsetzen
    if (!isPlaying) {
        isPlaying = true;
        playPauseBtn.textContent = 'Pause';
        startAnimation();
    }
}

// Initialisierung
document.addEventListener('DOMContentLoaded', function() {
    loadFrame(0);
    startAnimation();
});'''

    # Konfiguration als JSON einfügen
    return js_template.replace('CONFIG_JSON', json.dumps(config, indent=4))

def get_viewer_css_template():
    """Liefert das CSS-Template für den 360°-Viewer"""
    return '''/* 360° Viewer CSS */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    background-color: #f5f5f5;
    color: #333;
}

.viewer-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.viewer-header {
    text-align: center;
    margin-bottom: 20px;
}

.viewer-header h1 {
    font-size: 24px;
    margin-bottom: 5px;
}

.viewer-content {
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}

.viewer-360 {
    position: relative;
    width: 100%;
    min-height: 300px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    user-select: none;
}

.viewer-360 img {
    max-width: 100%;
    max-height: 80vh;
    display: block;
    cursor: grab;
}

.viewer-360 img:active {
    cursor: grabbing;
}

.viewer-controls {
    width: 100%;
    padding: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
    background-color: rgba(0, 0, 0, 0.05);
}

.control-btn {
    padding: 8px 16px;
    background-color: #4682B4;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.2s;
}

.control-btn:hover {
    background-color: #3A6D96;
}

.slider {
    flex-grow: 1;
    max-width: 500px;
    height: 6px;
    appearance: none;
    background-color: #ddd;
    border-radius: 3px;
    outline: none;
}

.slider::-webkit-slider-thumb {
    appearance: none;
    width: 16px;
    height: 16px;
    background-color: #4682B4;
    border-radius: 50%;
    cursor: pointer;
}

.slider::-moz-range-thumb {
    width: 16px;
    height: 16px;
    background-color: #4682B4;
    border-radius: 50%;
    cursor: pointer;
    border: none;
}

.viewer-footer {
    text-align: center;
    margin-top: 20px;
    font-size: 14px;
    color: #777;
}

/* Responsive Design */
@media (max-width: 768px) {
    .viewer-container {
        padding: 10px;
    }
    
    .viewer-header h1 {
        font-size: 20px;
    }
    
    .control-btn {
        padding: 6px 12px;
        font-size: 12px;
    }
}
