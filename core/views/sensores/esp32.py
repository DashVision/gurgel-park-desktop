import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal
import serial

class SerialReader(QThread):
    status_received = pyqtSignal(str)

    def __init__(self, port, baud=9600):
        super().__init__()
        self.port = port
        self.baud = baud
        self._running = True

    def run(self):
        try:
            ser = serial.Serial(self.port, self.baud, timeout=1)
        except serial.SerialException as e:
            print(f"Não foi possível abrir {self.port}: {e}")
            return
        while self._running:
            raw = ser.readline()
            line = raw.decode('utf-8', errors='ignore').strip()
            if line:
                self.status_received.emit(line)
        ser.close()

    def stop(self):
        self._running = False
        self.wait()

class ParkingApp(QWidget):
    def __init__(self, port="COM3"):
        super().__init__()
        self.setWindowTitle("Monitor de Vaga")
        self.label = QLabel("Conectando...", self)
        self.button = QPushButton("Iniciar", self)
        self.button.clicked.connect(self.start_monitor)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.port = port
        self.reader = None

    def start_monitor(self):
        if self.reader and self.reader.isRunning():
            self.reader.stop()
        self.reader = SerialReader(self.port)
        self.reader.status_received.connect(self.update_status)
        self.reader.start()
        self.label.setText("⏳ Monitorando...")

    def update_status(self, status):
        self.label.setText("🚗 Vaga Ocupada" if status=="OCUPADO" else "✅ Vaga Livre")

    def closeEvent(self, event):
        if self.reader and self.reader.isRunning():
            self.reader.stop()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ParkingApp(port="COM3")  # porta do ESP32
    window.show()
    sys.exit(app.exec_())
