# 🏎️💨 F1 Race Replay & Telemetry Visualizer

A custom-built Python desktop application that allows you to load real-world Formula 1 race data, visualize the cars racing around the track in real-time, and analyze live driver telemetry (speed and throttle).

## ✨ Features
* **Live Track Visualization:** Watch the cars actually race around the circuit using `pyqtgraph`.
* **Real-World Data:** Connects directly to the official F1 timing servers using `fastf1` to pull accurate race data.
* **Telemetry Dashboard:** Click on any driver to see their live speed and throttle graphs update as they drive.
* **Custom Engine:** Built from scratch using Python, `PySide6`, `pandas`, and `numpy` for blazing fast data processing.

## 🚀 How to Run It (For my friends)
If you want to play around with this on your own PC, here is how you do it:

1. Click the green **"<> Code"** button at the top of this page and click **"Download ZIP"**.
2. Extract the folder to your computer and open it in VS Code.
3. Open a terminal in VS Code and install the heavy-lifting libraries by running:
   ```bash
   pip install -r requirements.txt
