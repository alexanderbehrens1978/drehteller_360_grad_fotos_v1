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
        self.template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates', 'viewer')
    
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
        try:
            # Verzeichnisse erstellen
            js_dir = os.path.join(export_path, "js")
            css_dir = os.path.join(export_path, "css")
            os.makedirs(js_dir, exist_ok=True)
            os.makedirs(css_dir, exist_ok=True)
            
            # HTML-Template aus Datei laden
            html_template_path = os.path.join(self.template_dir, 'index.html')
            
            # Wenn Template nicht existiert, Fallback zum integrierten Template
            if not os.path.exists(html_template_path):
                self.logger.warning(f"HTML-Template nicht gefunden: {html_template_path}, verwende Fallback")
                return self._create_viewer_html_fallback(export_path, config)
            
            # Dateien aus den Templates erstellen
            with open(html_template_path, 'r') as f:
                html_content = f.read()
            
            # Platzhalter ersetzen
            html_content = html_content.replace('{{PROJECT_NAME}}', config['project_name'])
            html_content = html_content.replace('{{SESSION_NAME}}', config['session_name'])
            html_content = html_content.replace('{{MAX_FRAMES}}', str(len(config['images']) - 1))
            
            # Speichern
            with open(os.path.join(export_path, "index.html"), 'w') as f:
                f.write(html_content)
            
            # JavaScript aus Datei laden
            js_template_path = os.path.join(self.template_dir, 'viewer.js')
            if os.path.exists(js_template_path):
                with open(js_template_path, 'r') as f:
                    js_content = f.read()
                
                # Konfiguration einfügen
                js_content = js_content.replace('{{CONFIG}}', json.dumps(config, indent=4))
                
                # Speichern
                with open(os.path.join(js_dir, "viewer.js"), 'w') as f:
                    f.write(js_content)
            else:
                self.logger.warning(f"JS-Template nicht gefunden: {js_template_path}")
            
            # CSS aus Datei laden
            css_template_path = os.path.join(self.template_dir, 'viewer.css')
            if os.path.exists(css_template_path):
                shutil.copy2(css_template_path, os.path.join(css_dir, "viewer.css"))
            else:
                self.logger.warning(f"CSS-Template nicht gefunden: {css_template_path}")
                
            return True
            
        except Exception as e:
            self.logger.error(f"Fehler beim Erstellen des Viewers: {str(e)}")
            # Fallback
            return self._create_viewer_html_fallback(export_path, config)
    
    def _create_viewer_html_fallback(self, export_path, config):
        """Fallback-Methode, wenn externe Templates nicht verfügbar sind"""
        try:
            # Index.html
            from .templates import get_index_html_template
            index_html = get_index_html_template(config)
            index_path = os.path.join(export_path, "index.html")
            
            # JavaScript
            from .templates import get_viewer_js_template
            js_content = get_viewer_js_template(config)
            js_dir = os.path.join(export_path, "js")
            os.makedirs(js_dir, exist_ok=True)
            js_path = os.path.join(js_dir, "viewer.js")
            
            # CSS
            from .templates import get_viewer_css_template
            css_content = get_viewer_css_template()
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
                
            return True
            
        except Exception as e:
            self.logger.error(f"Fehler bei Fallback-Methode: {str(e)}")
            return False
