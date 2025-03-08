#!/usr/bin/env python3
# Datei: app.py
# Hauptanwendungsmodul für die 360° Drehteller Anwendung

import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from config.settings import Settings
from controllers.arduino_controller import ArduinoController
from controllers.camera_controller import CameraController
from controllers.turntable_controller import TurntableController
from models.project import Project, ProjectManager
from utils.arduino_finder import ArduinoFinder
from utils.camera_finder import CameraFinder
from utils.path_manager import PathManager

# Flask-App initialisieren
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Pfadmanager initialisieren
path_manager = PathManager()
path_manager.ensure_directories()

# Einstellungen laden
settings = Settings()

# Controller initialisieren
arduino_finder = ArduinoFinder()
camera_finder = CameraFinder()
arduino_controller = None
camera_controller = None
turntable_controller = None

# Projektverwaltung initialisieren
project_manager = ProjectManager(path_manager.projects_dir)

@app.route('/')
def index():
    """Hauptseite der Anwendung"""
    projects = project_manager.get_all_projects()
    return render_template('index.html', projects=projects)

@app.route('/project/new', methods=['GET', 'POST'])
def new_project():
    """Neues Projekt erstellen"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        angle_step = int(request.form.get('angle_step', 5))
        
        project = Project(name=name, description=description, angle_step=angle_step)
        project_manager.save_project(project)
        
        return redirect(url_for('index'))
    return render_template('project.html', mode='new')

@app.route('/project/<project_id>')
def view_project(project_id):
    """Ein vorhandenes Projekt anzeigen"""
    project = project_manager.get_project(project_id)
    if not project:
        return redirect(url_for('index'))
    return render_template('project.html', mode='view', project=project)

@app.route('/project/<project_id>/edit', methods=['GET', 'POST'])
def edit_project(project_id):
    """Ein vorhandenes Projekt bearbeiten"""
    project = project_manager.get_project(project_id)
    if not project:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        project.name = request.form.get('name')
        project.description = request.form.get('description')
        project.angle_step = int(request.form.get('angle_step', 5))
        project_manager.save_project(project)
        return redirect(url_for('view_project', project_id=project_id))
    
    return render_template('project.html', mode='edit', project=project)

@app.route('/project/<project_id>/delete')
def delete_project(project_id):
    """Ein Projekt löschen"""
    project_manager.delete_project(project_id)
    return redirect(url_for('index'))

@app.route('/project/<project_id>/capture', methods=['GET', 'POST'])
def capture_session(project_id):
    """Eine neue Aufnahmesession für ein Projekt starten"""
    global arduino_controller, camera_controller, turntable_controller
    
    project = project_manager.get_project(project_id)
    if not project:
        return redirect(url_for('index'))
    
    if not arduino_controller:
        arduino_controller = ArduinoController(settings.arduino_port, settings.arduino_baudrate)
    
    if not camera_controller:
        camera_controller = CameraController(settings.camera_type, settings.camera_device)
    
    if not turntable_controller:
        turntable_controller = TurntableController(arduino_controller, project.angle_step)
    
    if request.method == 'POST':
        # Session starten und Fotos machen
        if turntable_controller.start_session(project, camera_controller):
            return redirect(url_for('view_project', project_id=project_id))
        else:
            error = "Fehler beim Starten der Aufnahmesession"
            return render_template('capture.html', project=project, error=error)
    
    return render_template('capture.html', project=project)

@app.route('/settings', methods=['GET', 'POST'])
def app_settings():
    """Anwendungseinstellungen verwalten"""
    if request.method == 'POST':
        # Arduino-Einstellungen
        settings.arduino_port = request.form.get('arduino_port')
        settings.arduino_baudrate = int(request.form.get('arduino_baudrate', 9600))
        
        # Kamera-Einstellungen
        settings.camera_type = request.form.get('camera_type')
        settings.camera_device = request.form.get('camera_device')
        settings.camera_resolution = request.form.get('camera_resolution')
        
        # Einstellungen speichern
        settings.save()
        
        return redirect(url_for('index'))
    
    # Arduino-Ports finden
    arduino_ports = arduino_finder.find_arduino_ports()
    
    # Kameras finden
    cameras = camera_finder.find_cameras()
    gphoto_cameras = camera_finder.find_gphoto_cameras()
    
    return render_template('settings.html', 
                          settings=settings,
                          arduino_ports=arduino_ports,
                          cameras=cameras,
                          gphoto_cameras=gphoto_cameras)

@app.route('/viewer/<project_id>/<session_id>')
def view_360(project_id, session_id):
    """360°-Viewer für eine Fotosession anzeigen"""
    project = project_manager.get_project(project_id)
    if not project:
        return redirect(url_for('index'))
    
    session = project.get_session(session_id)
    if not session:
        return redirect(url_for('view_project', project_id=project_id))
    
    return render_template('viewer.html', project=project, session=session)

@app.route('/api/project/<project_id>/sessions')
def api_project_sessions(project_id):
    """API-Endpunkt zum Abrufen der Sessions eines Projekts"""
    project = project_manager.get_project(project_id)
    if not project:
        return jsonify({'error': 'Projekt nicht gefunden'}), 404
    
    sessions = [session.to_dict() for session in project.sessions]
    return jsonify(sessions)

@app.route('/api/turntable/move', methods=['POST'])
def api_move_turntable():
    """API-Endpunkt zum Bewegen des Drehtellers"""
    global arduino_controller, turntable_controller
    
    if not arduino_controller:
        arduino_controller = ArduinoController(settings.arduino_port, settings.arduino_baudrate)
    
    if not turntable_controller:
        turntable_controller = TurntableController(arduino_controller, 5)
    
    degrees = int(request.form.get('degrees', 5))
    success = turntable_controller.move_degrees(degrees)
    
    return jsonify({'success': success})

@app.route('/api/camera/capture', methods=['POST'])
def api_capture_photo():
    """API-Endpunkt zum Aufnehmen eines Fotos"""
    global camera_controller
    
    if not camera_controller:
        camera_controller = CameraController(settings.camera_type, settings.camera_device)
    
    project_id = request.form.get('project_id')
    session_id = request.form.get('session_id')
    angle = int(request.form.get('angle', 0))
    
    photo_path = path_manager.get_photo_path(project_id, session_id, angle)
    success = camera_controller.capture_photo(photo_path)
    
    return jsonify({'success': success, 'path': photo_path if success else None})

@app.route('/viewer/<project_id>/<session_id>')
def view_360(project_id, session_id):
    """360°-Viewer für eine Fotosession anzeigen"""
    project = project_manager.get_project(project_id)
    if not project:
        return redirect(url_for('index'))
    
    session = project.get_session(session_id)
    if not session:
        return redirect(url_for('view_project', project_id=project_id))
    
    return render_template('viewer.html', project=project, session=session)

@app.route('/logs')
def view_logs():
    """Anzeige der Anwendungslogs"""
    log_file = os.path.join(os.path.dirname(__file__), 'app.log')
    logs = []
    
    try:
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = f.readlines()
                logs.reverse()  # Neueste Logs zuerst
        else:
            logs = ["Keine Logdatei gefunden."]
    except Exception as e:
        logs = [f"Fehler beim Lesen der Logdatei: {str(e)}"]
    
    return render_template('logs.html', logs=logs)

@app.route('/logs')
def view_logs():
    """Anzeige der Anwendungslogs"""
    log_file = os.path.join(os.path.dirname(__file__), 'app.log')
    logs = []
    
    try:
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = f.readlines()
                logs.reverse()  # Neueste Logs zuerst
        else:
            logs = ["Keine Logdatei gefunden."]
    except Exception as e:
        logs = [f"Fehler beim Lesen der Logdatei: {str(e)}"]
    
    return render_template('logs.html', logs=logs)

if __name__ == '__main__':
    # Beim Start der Anwendung die Controller initialisieren
    try:
        arduino_controller = ArduinoController(settings.arduino_port, settings.arduino_baudrate)
        camera_controller = CameraController(settings.camera_type, settings.camera_device)
        turntable_controller = TurntableController(arduino_controller, 5)
    except Exception as e:
        print(f"Warnung: Controller konnten nicht initialisiert werden: {e}")
        print("Die Anwendung wird trotzdem gestartet. Bitte überprüfen Sie die Einstellungen.")
    
    # Webserver starten
    app.run(host='0.0.0.0', port=5000, debug=True)
