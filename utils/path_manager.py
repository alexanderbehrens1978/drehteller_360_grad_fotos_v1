# Datei: utils/path_manager.py
# Modul für das Pfad- und Dateimanagement

import os
import logging
from pathlib import Path

class PathManager:
    """Klasse zur Verwaltung von Pfaden und Verzeichnissen"""
    
    def __init__(self, base_dir=None):
        """Initialisiert den PathManager"""
        self.logger = logging.getLogger(__name__)
        
        # Wenn kein Basisverzeichnis angegeben wurde, verwenden wir das Home-Verzeichnis
        if base_dir is None:
            self.base_dir = os.path.join(os.path.expanduser('~'), 'Drehteller-Projekte')
        else:
            self.base_dir = base_dir
        
        # Pfade für die verschiedenen Verzeichnisse
        self.projects_dir = os.path.join(self.base_dir, 'projects')
        self.exports_dir = os.path.join(self.base_dir, 'exports')
        self.temp_dir = os.path.join(self.base_dir, 'temp')
        self.cache_dir = os.path.join(self.base_dir, 'cache')
    
    def ensure_directories(self):
        """Stellt sicher, dass alle benötigten Verzeichnisse existieren"""
        directories = [
            self.base_dir,
            self.projects_dir,
            self.exports_dir,
            self.temp_dir,
            self.cache_dir
        ]
        
        for directory in directories:
            try:
                os.makedirs(directory, exist_ok=True)
                self.logger.debug(f"Verzeichnis erstellt/gefunden: {directory}")
            except Exception as e:
                self.logger.error(f"Fehler beim Erstellen des Verzeichnisses {directory}: {str(e)}")
    
    def get_project_path(self, project_id):
        """Gibt den Pfad zu einem Projekt zurück"""
        return os.path.join(self.projects_dir, project_id)
    
    def get_project_sessions_path(self, project_id):
        """Gibt den Pfad zu den Sessions eines Projekts zurück"""
        return os.path.join(self.get_project_path(project_id), 'sessions')
    
    def get_session_path(self, project_id, session_id):
        """Gibt den Pfad zu einer Session zurück"""
        return os.path.join(self.get_project_sessions_path(project_id), session_id)
    
    def get_photo_path(self, project_id, session_id, angle):
        """Gibt den Pfad zu einem Foto zurück"""
        session_path = self.get_session_path(project_id, session_id)
        return os.path.join(session_path, f"angle_{angle:03d}.jpg")
    
    def get_export_path(self, project_id, export_name=None):
        """Gibt den Pfad für einen Export zurück"""
        if export_name is None:
            export_name = f"export_{project_id}"
        
        return os.path.join(self.exports_dir, export_name)
    
    def get_temp_path(self, filename=None):
        """Gibt einen temporären Pfad zurück"""
        if filename is None:
            # Verwende die aktuelle Zeit als Dateinamen
            import time
            filename = f"temp_{int(time.time())}"
        
        return os.path.join(self.temp_dir, filename)
    
    def ensure_project_directories(self, project_id):
        """Stellt sicher, dass die Projektverzeichnisse existieren"""
        project_path = self.get_project_path(project_id)
        sessions_path = self.get_project_sessions_path(project_id)
        
        try:
            os.makedirs(project_path, exist_ok=True)
            os.makedirs(sessions_path, exist_ok=True)
            return True
        except Exception as e:
            self.logger.error(f"Fehler beim Erstellen der Projektverzeichnisse für {project_id}: {str(e)}")
            return False
    
    def ensure_session_directory(self, project_id, session_id):
        """Stellt sicher, dass das Session-Verzeichnis existiert"""
        session_path = self.get_session_path(project_id, session_id)
        
        try:
            os.makedirs(session_path, exist_ok=True)
            return True
        except Exception as e:
            self.logger.error(f"Fehler beim Erstellen des Session-Verzeichnisses {session_id}: {str(e)}")
            return False
    
    def clear_temp_directory(self):
        """Löscht alle Dateien im temporären Verzeichnis"""
        try:
            for filename in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, filename)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            return True
        except Exception as e:
            self.logger.error(f"Fehler beim Löschen des temporären Verzeichnisses: {str(e)}")
            return False
