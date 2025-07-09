"""
Servicio de programación de tareas para respaldos.
"""

import threading
import time
import schedule
from typing import Callable, Optional
from config.settings import MESSAGES


class SchedulerService:
    """Servicio para programar y ejecutar tareas de respaldo."""
    
    def __init__(self, log_callback: Callable[[str], None]):
        self.log_callback = log_callback
        self.running = False
        self.thread: Optional[threading.Thread] = None
    
    def schedule_daily_backup(self, time_str: str, backup_function: Callable) -> None:
        """Programa un respaldo diario a una hora específica."""
        schedule.every().day.at(time_str).do(backup_function)
        self.log_callback(MESSAGES['daily_scheduled'].format(time_str))
    
    def schedule_interval_backup(self, interval_hours: int, backup_function: Callable) -> None:
        """Programa un respaldo cada cierto número de horas."""
        schedule.every(interval_hours).hours.do(backup_function)
        self.log_callback(MESSAGES['interval_scheduled'].format(interval_hours))
    
    def start(self) -> None:
        """Inicia el programador de tareas."""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.thread.start()
        self.log_callback(MESSAGES['scheduler_started'])
    
    def stop(self) -> None:
        """Detiene el programador de tareas."""
        if not self.running:
            return
        
        self.running = False
        schedule.clear()
        self.log_callback(MESSAGES['scheduler_stopped'])
    
    def _scheduler_loop(self) -> None:
        """Bucle principal del programador."""
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def clear_schedule(self) -> None:
        """Limpia todas las tareas programadas."""
        schedule.clear()
    
    @property
    def is_running(self) -> bool:
        """Indica si el programador está ejecutándose."""
        return self.running
