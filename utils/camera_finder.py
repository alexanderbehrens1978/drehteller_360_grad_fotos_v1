# Datei: utils/camera_finder.py
# Modul zur Erkennung von Kameras (Webcams und gphoto2-Kameras)

import os
import logging
import subprocess
import re
import platform
import json

class CameraFinder:
    """Klasse zur Erkennung von Kameras (Webcams und gphoto2-Kameras)"""
    
    def __init__(self):
        """Initialisiert den Kamera-Finder"""
        self.logger = logging.getLogger(__name__)
        self.gphoto2_available = self._check_gphoto2()
    
    def _check_gphoto2(self):
        """Prüft, ob gphoto2 installiert ist"""
        try:
            result = subprocess.run(['which', 'gphoto2'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
            return result.returncode == 0
        except Exception:
            return False
    
    def find_cameras(self):
        """Findet alle angeschlossenen Webcams"""
        cameras = []
        
        try:
            if platform.system() == 'Linux':
                cameras = self._find_linux_webcams()
            elif platform.system() == 'Windows':
                cameras = self._find_windows_webcams()
            elif platform.system() == 'Darwin':  # macOS
                cameras = self._find_macos_webcams()
            else:
                self.logger.warning("Nicht unterstütztes Betriebssystem für Webcam-Erkennung")
        except Exception as e:
            self.logger.error(f"Fehler bei der Webcam-Suche: {str(e)}")
        
        return cameras
    
    def _find_linux_webcams(self):
        """Findet Webcams unter Linux mit v4l2-ctl"""
        cameras = []
        
        try:
            # Prüfen, ob v4l-utils installiert ist
            check_cmd = ['which', 'v4l2-ctl']
            check_result = subprocess.run(check_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            if check_result.returncode != 0:
                self.logger.warning("v4l2-ctl nicht gefunden, verwende Fallback-Methode")
                return self._find_linux_webcams_fallback()
            
            # Geräteliste mit v4l2-ctl abfragen
            cmd = ['v4l2-ctl', '--list-devices']
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            if result.returncode != 0:
                self.logger.error(f"Fehler bei v4l2-ctl: {result.stderr}")
                return self._find_linux_webcams_fallback()
            
            # Ausgabe parsen
            current_device = None
            for line in result.stdout.splitlines():
                line = line.strip()
                
                if line and not line.startswith('/dev/'):
                    # Zeile enth
