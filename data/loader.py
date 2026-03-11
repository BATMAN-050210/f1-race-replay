import fastf1
import os

class F1DataLoader:
    def __init__(self, cache_dir="f1_cache"):
        self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        fastf1.Cache.enable_cache(self.cache_dir)
        self.session = None

    def load_session(self, year, grand_prix, session_type="R"):
        """Loads the session data."""
        print(f"Loading {year} {grand_prix} - {session_type}...")
        self.session = fastf1.get_session(year, grand_prix, session_type)
        self.session.load()
        return self.session

    def get_driver_telemetry(self, driver_identifier):
        """Returns telemetry for a specific driver."""
        if not self.session:
            return None
        laps = self.session.laps.pick_driver(driver_identifier)
        telemetry = laps.get_telemetry()
        return telemetry

    def get_all_drivers(self):
        """Returns a list of drivers in the session."""
        if not self.session:
            return []
        # session.drivers returns a list of driver numbers
        return [self.session.get_driver(d) for d in self.session.drivers]   
    def get_track_coordinates(self):
        """Gets X, Y coordinates to draw the track using the fastest lap."""
        if not self.session:
            return [], []
        # We use the fastest lap of the session to trace the track shape
        fastest_lap = self.session.laps.pick_fastest()
        telemetry = fastest_lap.get_telemetry()
        return telemetry['X'].tolist(), telemetry['Y'].tolist()

    def get_initial_car_positions(self):
        """Gets the very first X, Y position for each driver to place them on the grid."""
        positions = {}
        if not self.session:
            return positions
        for driver in self.get_all_drivers():
            abbr = driver['Abbreviation']
            telemetry = self.get_driver_telemetry(abbr)
            if telemetry is not None and not telemetry.empty:
                # Grab the first row of telemetry for their starting X/Y
                first_row = telemetry.iloc[0]
                positions[abbr] = (first_row['X'], first_row['Y'])
        return positions