import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QVBoxLayout

class F1TrackRenderer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Setup PyQtGraph Plot
        self.plot_widget = pg.PlotWidget(background='#000000')
        self.plot_widget.hideAxis('left')
        self.plot_widget.hideAxis('bottom')
        self.layout.addWidget(self.plot_widget)
        
        # Data placeholders
        self.track_curve = self.plot_widget.plot([], [], pen=pg.mkPen('gray', width=4))
        self.car_scatter = pg.ScatterPlotItem(size=12, brush=pg.mkBrush('red'))
        self.plot_widget.addItem(self.car_scatter)
        self.text_items = {} # To hold driver names

    def setup_track(self, track_x, track_y):
        """Draws the track line."""
        self.track_curve.setData(track_x, track_y)
        
    def update_car_positions(self, car_data):
        """Updates car dots and labels. car_data is a dict: {'VER': (x, y)}"""
        spots = []
        
        # Clear old text labels
        for text_item in self.text_items.values():
            self.plot_widget.removeItem(text_item)
        self.text_items.clear()

        # Draw new dots and text
        for abbr, (x, y) in car_data.items():
            spots.append({'pos': (x, y), 'data': 1})
            
            text = pg.TextItem(text=abbr, color='white', anchor=(0, 1))
            text.setPos(x, y)
            self.plot_widget.addItem(text)
            self.text_items[abbr] = text
            
        self.car_scatter.setData(spots)