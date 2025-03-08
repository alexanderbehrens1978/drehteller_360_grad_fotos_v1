# Datei: controllers/turntable_controller.py
# Modul zur Steuerung des Drehtellers

import time
import logging
import math
from pathlib import Path
from models.photo_session import PhotoSession

class TurntableController:
    """Klasse zur Steuerung des Drehtellers mit dem Arduino"""
    
    # Konstanten für den Drehteller (0,8° pro Umdrehung bei diesem Motor)
    MOTOR_DEGREE_PER_SECOND = 0.8 / 5.0  # 0,8° in 5 Sekunden (basierend auf den Angaben)
