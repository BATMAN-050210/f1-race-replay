import numpy as np

class ReplayEngine:
    def __init__(self):
        self.telemetry_data = {}
        self.min_time = 0
        self.max_time = 0
        self.current_time = 0

    def load_data(self, data_loader):
        """Pre-loads all driver telemetry into memory for blazing fast playback."""
        self.telemetry_data = {}
        drivers = data_loader.get_all_drivers()
        all_times = []
        
        for driver in drivers:
            abbr = driver['Abbreviation']
            tel = data_loader.get_driver_telemetry(abbr)
            if tel is not None and not tel.empty:
                # Convert timestamps to plain seconds
                time_sec = tel['Time'].dt.total_seconds().values
                x = tel['X'].values
                y = tel['Y'].values
                self.telemetry_data[abbr] = {'time': time_sec, 'x': x, 'y': y}
                
                all_times.append(time_sec[0])
                all_times.append(time_sec[-1])
        
        if all_times:
            self.min_time = min(all_times)
            self.max_time = max(all_times)
            self.current_time = self.min_time

    def get_positions_at_time(self, time_sec):
        """Instantly finds where every car was at a specific second in the race."""
        positions = {}
        for abbr, data in self.telemetry_data.items():
            times = data['time']
            # Find the exact index for the current time
            idx = np.searchsorted(times, time_sec)
            
            # Keep cars on track if time goes out of bounds
            if idx >= len(times): idx = len(times) - 1
            if idx < 0: idx = 0
                
            positions[abbr] = (data['x'][idx], data['y'][idx])
        return positions