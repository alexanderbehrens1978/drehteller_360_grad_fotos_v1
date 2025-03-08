// 360° Viewer JavaScript

// Konfiguration
const viewerConfig = {{CONFIG}};

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
