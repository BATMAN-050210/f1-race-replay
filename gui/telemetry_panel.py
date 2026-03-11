import matplotlib
matplotlib.use('QtAgg')
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class TelemetryPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Setup Matplotlib Figure
        self.figure = Figure(facecolor='#1e1e1e')
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.layout.addWidget(self.canvas)
        
        # Subplots for Speed and Throttle
        self.ax_speed = self.figure.add_subplot(211)
        self.ax_throttle = self.figure.add_subplot(212, sharex=self.ax_speed)
        
        self.setup_plot_styles()

    def setup_plot_styles(self):
        for ax in [self.ax_speed, self.ax_throttle]:
            ax.set_facecolor('#1e1e1e')
            ax.tick_params(colors='white')
            for spine in ax.spines.values():
                spine.set_color('#333333')
                
        self.ax_speed.set_title("Speed (km/h)", color='white')
        self.ax_throttle.set_title("Throttle (%)", color='white')
        self.figure.tight_layout()

    def plot_telemetry(self, telemetry_data):
        self.ax_speed.clear()
        self.ax_throttle.clear()
        self.setup_plot_styles()

        if telemetry_data is not None and not telemetry_data.empty:
            time = telemetry_data['Time'].dt.total_seconds()
            self.ax_speed.plot(time, telemetry_data['Speed'], color='#00ffff')
            self.ax_throttle.plot(time, telemetry_data['Throttle'], color='#ff00ff')

        self.canvas.draw()