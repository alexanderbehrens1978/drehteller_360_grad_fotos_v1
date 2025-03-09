import os
import subprocess
import time
import re
from app.services.config_manager import config_manager

def take_photo(filename=None):
    """
    Nimmt ein Foto auf
    """
    # Wenn Simulator-Modus aktiv ist
    if config_manager.get('simulator.enabled', True):
        print("Simulator: Foto aufnehmen")
        # Hier würde der Simulator-Code stehen
        return "simulation.jpg"
        
    try:
        # Pfad für das Speichern von Fotos
        photo_dir = 'static/photos'
        os.makedirs(photo_dir, exist_ok=True)
        
        # Falls kein Dateiname angegeben wurde, einen generieren
        if not filename:
            filename = f"photo_{int(time.time())}.jpg"
        
        # Kamera-Einstellungen aus Konfiguration holen
        camera_type = config_manager.get('camera.type', 'webcam')
        camera_device = config_manager.get('camera.device_path', '/dev/video0')
        
        # Vollständiger Ausgabepfad
        output_path = os.path.join(photo_dir, filename)
        
        # Je nach Kameratyp unterschiedliche Aufnahmemethode
        if camera_type == 'gphoto2':
            # DSLR mit gphoto2 - mit verbesserter Fehlerbehandlung
            print(f"Versuche, Foto mit gphoto2 aufzunehmen: {output_path}")
            
            # gphoto2 Kommando mit geeigneten Parametern
            cmd = [
                'gphoto2',
                '--force-overwrite',  # Bestehende Dateien überschreiben
                '--set-config', 'capturetarget=1',  # Auf Speicherkarte speichern
                '--capture-image-and-download',
                '--filename', output_path
            ]
            
            # Ausführen mit Timeout
            try:
                result = subprocess.run(cmd, timeout=30, 
                                      stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE, 
                                      text=True)
                
                print(f"gphoto2 Ausgabe: {result.stdout}")
                if result.stderr:
                    print(f"gphoto2 Fehler: {result.stderr}")
                
                # Prüfen ob Datei tatsächlich erstellt wurde
                if not os.path.exists(output_path):
                    # Falls die Datei nicht da ist, prüfe ob wir ein "location"
                    # in der Ausgabe haben
                    if "Saving file as" in result.stdout:
                        # Extrahiere den tatsächlichen Dateinamen
                        match = re.search(r"Saving file as (.*)", result.stdout)
                        if match:
                            actual_file = match.group(1).strip()
                            if os.path.exists(actual_file):
                                # Datei umbenennen
                                import shutil
                                shutil.move(actual_file, output_path)
                                print(f"Datei umbenannt: {actual_file} -> {output_path}")
                    else:
                        # Wenn kein spezieller Fall, Fehler werfen
                        raise Exception(f"gphoto2 hat keine Datei erzeugt: {output_path}")
                    
                print(f"Foto erfolgreich aufgenommen: {output_path}")
            except subprocess.TimeoutExpired:
                print("Timeout bei gphoto2 - Kamera reagiert nicht")
                
                # Versuche, alle gphoto2-Prozesse zu beenden
                try:
                    subprocess.run(['pkill', '-f', 'gphoto2'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
                except:
                    pass
                    
                raise Exception("Timeout beim Fotografieren")
              else:
            # Webcam mit OpenCV
            print(f"Versuche, Foto mit OpenCV aufzunehmen: {camera_device}")
            try:
                import cv2
                cap = cv2.VideoCapture(camera_device)
                
                # Auflösung einstellen
                width = config_manager.get('camera.resolution.width', 1280)
                height = config_manager.get('camera.resolution.height', 720)
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                
                # Foto aufnehmen
                ret, frame = cap.read()
                if not ret:
                    raise Exception(f"Fehler beim Auslesen der Kamera: {camera_device}")
                    
                # Foto speichern
                cv2.imwrite(output_path, frame)
                cap.release()
            except ImportError:
                print("OpenCV nicht installiert, verwende fswebcam als Fallback")
                
                # Fallback zu fswebcam, wenn OpenCV nicht verfügbar ist
                try:
                    subprocess.run([
                        'fswebcam',
                        '--no-banner',
                        '--resolution', f"{width}x{height}",
                        '-d', camera_device,
                        output_path
                    ], check=True)
                except subprocess.CalledProcessError as e:
                    raise Exception(f"Fehler bei fswebcam: {e}")
            
        print(f"Foto aufgenommen und gespeichert als: {filename}")
        return filename
    except Exception as e:
        print(f"Fehler beim Aufnehmen des Fotos: {e}")
        import traceback
        traceback.print_exc()
        return None
else:
            # Webcam mit OpenCV
            print(f"Versuche, Foto mit OpenCV aufzunehmen: {camera_device}")
            try:
                import cv2
                cap = cv2.VideoCapture(camera_device)
                
                # Auflösung einstellen
                width = config_manager.get('camera.resolution.width', 1280)
                height = config_manager.get('camera.resolution.height', 720)
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                
                # Foto aufnehmen
                ret, frame = cap.read()
                if not ret:
                    raise Exception(f"Fehler beim Auslesen der Kamera: {camera_device}")
                    
                # Foto speichern
                cv2.imwrite(output_path, frame)
                cap.release()
            except ImportError:
                print("OpenCV nicht installiert, verwende fswebcam als Fallback")
                
                # Fallback zu fswebcam, wenn OpenCV nicht verfügbar ist
                try:
                    subprocess.run([
                        'fswebcam',
                        '--no-banner',
                        '--resolution', f"{width}x{height}",
                        '-d', camera_device,
                        output_path
                    ], check=True)
                except subprocess.CalledProcessError as e:
                    raise Exception(f"Fehler bei fswebcam: {e}")
            
        print(f"Foto aufgenommen und gespeichert als: {filename}")
        return filename
    except Exception as e:
        print(f"Fehler beim Aufnehmen des Fotos: {e}")
        import traceback
        traceback.print_exc()
        return None
