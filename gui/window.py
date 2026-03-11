from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                               QPushButton, QComboBox, QLabel, QListWidget)
from PySide6.QtCore import Qt, QTimer
from gui.telemetry_panel import TelemetryPanel
from data.loader import F1DataLoader
from replay.renderer import F1TrackRenderer
from replay.engine import ReplayEngine

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("F1 Race Replay Analysis")
        self.resize(1280, 720)
        self.setStyleSheet("background-color: #121212; color: #ffffff;")
        
        self.data_loader = F1DataLoader()
        self.replay_engine = ReplayEngine()
        
        # --- NEW: Playback Timer ---
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.playback_speed = 15.0 # 15x speed so the cars don't crawl!
        # ---------------------------

        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # LEFT PANEL
        left_panel = QVBoxLayout()
        self.year_combo = QComboBox()
        self.year_combo.addItems(["2023", "2024"])
        self.gp_combo = QComboBox()
        self.gp_combo.addItems(["Bahrain", "Monaco", "Silverstone", "Monza"])
        
        self.load_btn = QPushButton("Load Race Data")
        self.load_btn.setStyleSheet("background-color: #e10600; font-weight: bold; padding: 10px;")
        self.load_btn.clicked.connect(self.load_race_data)

        self.driver_list = QListWidget()
        self.driver_list.itemClicked.connect(self.driver_selected)

        left_panel.addWidget(QLabel("Season:"))
        left_panel.addWidget(self.year_combo)
        left_panel.addWidget(QLabel("Grand Prix:"))
        left_panel.addWidget(self.gp_combo)
        left_panel.addWidget(self.load_btn)
        left_panel.addWidget(QLabel("Drivers:"))
        left_panel.addWidget(self.driver_list)
        
        # CENTER PANEL
        center_panel = QVBoxLayout()
        self.track_renderer = F1TrackRenderer()
        
        playback_layout = QHBoxLayout()
        self.play_btn = QPushButton("▶ Play")
        self.pause_btn = QPushButton("⏸ Pause")
        
        # --- NEW: Connect Buttons to Functions ---
        self.play_btn.clicked.connect(self.play_race)
        self.pause_btn.clicked.connect(self.pause_race)
        # -----------------------------------------

        playback_layout.addWidget(self.play_btn)
        playback_layout.addWidget(self.pause_btn)

        center_panel.addWidget(self.track_renderer, stretch=1)
        center_panel.addLayout(playback_layout)

        # RIGHT PANEL
        right_panel = QVBoxLayout()
        self.telemetry_panel = TelemetryPanel()
        right_panel.addWidget(self.telemetry_panel)

        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(center_panel, 3)
        main_layout.addLayout(right_panel, 2)

    def load_race_data(self):
        year = int(self.year_combo.currentText())
        gp = self.gp_combo.currentText()
        self.load_btn.setText("Loading... (Please Wait)")
        self.load_btn.setEnabled(False)
        QApplication.processEvents() # Unfreezes the UI while loading
        
        # 1. Load Data
        self.data_loader.load_session(year, gp)
        drivers = self.data_loader.get_all_drivers()
        
        self.driver_list.clear()
        for driver in drivers:
            self.driver_list.addItem(f"{driver['Abbreviation']} - {driver['LastName']}")
            
        # 2. Draw Track
        track_x, track_y = self.data_loader.get_track_coordinates()
        self.track_renderer.setup_track(track_x, track_y)
        
        # 3. Load Engine & Draw Initial Grid
        self.replay_engine.load_data(self.data_loader)
        initial_positions = self.replay_engine.get_positions_at_time(self.replay_engine.min_time)
        self.track_renderer.update_car_positions(initial_positions)
            
        self.load_btn.setText("Load Race Data")
        self.load_btn.setEnabled(True)

    def driver_selected(self, item):
        abbr = item.text().split(" - ")[0]
        telemetry = self.data_loader.get_driver_telemetry(abbr)
        self.telemetry_panel.plot_telemetry(telemetry)

    # --- NEW: PLAYBACK FUNCTIONS ---
    def play_race(self):
        if self.replay_engine.telemetry_data:
            self.timer.start(50) # Update every 50ms (20 FPS)

    def pause_race(self):
        self.timer.stop()

    def update_frame(self):
        # Advance the clock (0.05 seconds * 15x speed)
        self.replay_engine.current_time += (0.05 * self.playback_speed)
        
        # Stop if race is over
        if self.replay_engine.current_time > self.replay_engine.max_time:
            self.pause_race()
            return

        # Update graphic
        positions = self.replay_engine.get_positions_at_time(self.replay_engine.current_time)
        self.track_renderer.update_car_positions(positions)