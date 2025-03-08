# Datei: utils/image_processor.py
# Modul für die Bildverarbeitung

import os
import logging
import shutil
import json
from pathlib import Path

class ImageProcessor:
    """Klasse zur Verarbeitung von Bildern für die 360°-Anzeige"""
    
    def __init__(self, path_manager):
        """Initialisiert den ImageProcessor"""
        self.logger = logging.getLogger(__name__)
        self.path_manager = path_manager
    
    def prepare_360_viewer(self, project, session):
        """Bereitet die Bilder für die 360°-Anzeige vor"""
        try:
            # Exportverzeichnis erstellen
            export_name = f"{project.id}_{session.id}_360"
            export_path = self.path_manager.get_export_path(project.id, export_name)
            os.makedirs(export_path, exist_ok=True)
            
            # Unterverzeichnis für Bilder
            images_dir = os.path.join(export_path, "images")
            os.makedirs(images_dir, exist_ok=True)
            
            # Konfigurationsdatei erstellen
            config = {
                'project_name': project.name,
                'session_name': session.name,
                'angle_step': session.angle_step,
                'total_frames': len(session.photos),
                'images': []
            }
            
            # Bilder kopieren und Konfiguration aktualisieren
            for angle, photo_path in sorted(session.photos.items()):
                # Zieldateiname
                target_filename = f"frame_{int(angle):03d}.jpg"
                target_path = os.path.join(images_dir, target_filename)
                
                # Bild kopieren
                shutil.copy2(photo_path, target_path)
                
                # Zur Konfiguration hinzufügen
                config['images'].append({
                    'angle': angle,
                    'path': f"images/{target_filename}"
                })
            
            # Konfigurationsdatei speichern
            config_path = os.path.join(export_path, "config.json")
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
            
            # HTML-Viewer kopieren
            self._create_viewer_html(export_path, config)
            
            self.logger.info(f"360°-Viewer erfolgreich erstellt: {export_path}")
            return export_path
        
        except Exception as e:
            self.logger.error(f"Fehler bei der Vorbereitung des 360°-Viewers: {str(e)}")
            return None
    
    def _create_viewer_html(self, export_path, config):
        """Erstellt die HTML-Dateien für den 360°-Viewer"""
        # index.html
        index_html = self._get_index_html_template(config)
        index_path = os.path.join(export_path, "index.html")
        
        # JavaScript
        js_content = self._get_viewer_js_template(config)
        js_dir = os.path.join(export_path, "js")
        os.makedirs(js_dir, exist_ok=True)
        js_path = os.path.join(js_dir, "viewer.js")
        
        # CSS
        css_content = self._get_viewer_css_template()
        css_dir = os.path.join(export_path, "css")
        os.makedirs(css_dir, exist_ok=True)
        css_path = os.path.join(css_dir, "viewer.css")
        
        # Dateien schreiben
        with open(index_path, 'w') as f:
            f.write(index_html)
        
        with open(js_path, 'w') as f:
            f.write(js_content)
        
        with open(css_path, 'w') as f:
            f.write(css_content)
    
    def _get_index_html_template(self, config):
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
    
    def _get_viewer_js_template(self, config):
        """Liefert das JavaScript-Template für den 360°-Viewer"""
        return f'''// 360° Viewer JavaScript

// Konfiguration
const viewerConfig = {JSON_CONFIG};

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
});
'''.replace('{JSON_CONFIG}', json.dumps(config, indent=4))
    
    def _get_viewer_css_template(self):
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
