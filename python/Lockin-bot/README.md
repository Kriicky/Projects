# Python Vision Focus Detector

A webcam-based focus detector that checks whether you're paying attention to your screen. If you look away or leave your desk for too long, it opens an alert page in your browser that plays an alarm and tells you to get back to work.

## Features

- Real-time face detection with OpenCV
- Estimates head orientation to decide if you're focused
- Alert page with an alarm sound when you lose focus
- Adjustable sensitivity and cooldown between alerts

## Requirements

- Python 3.8 or newer
- A webcam
- A modern web browser (for the alert page)
- Python packages listed in `requirements.txt` (OpenCV, Flask)

## Project Structure

```
python-vision/
├── main.py            # Webcam capture and focus detection
├── server.py          # Flask server that serves the alert page
├── templates/         # HTML for the alert page
├── requirements.txt   # Python dependencies
└── run.sh             # Convenience launcher (Linux/macOS)
```

## Installation

1. Get the code and move into the project folder:

   ```bash
   git clone <repository-url>
   cd python-vision
   ```

2. Create and activate a virtual environment:

   **Linux / macOS**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **Windows (PowerShell)**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

The detector needs the alert server running so it has a page to open.

**Option 1: launcher script (Linux/macOS)**

```bash
chmod +x run.sh   # first time only
./run.sh
```

**Option 2: run each part manually (any OS)**

In one terminal, start the alert server:

```bash
python server.py
```

In a second terminal (with the virtual environment activated), start the detector:

```bash
python main.py
```

Once running, the detector will:

1. Open your webcam
2. Detect your face and estimate whether you're looking at the screen
3. If you look away or leave for too long, open `http://127.0.0.1:5000/alert` in your default browser
4. The alert page plays an alarm and shows **"GET BACK TO WORK!"**

Press `q` in the camera window to quit.

## Configuration

Adjust these constants at the top of `main.py`:

| Setting           | Default                        | Description                                         |
|-------------------|--------------------------------|-----------------------------------------------------|
| `CAMERA_INDEX`    | `0`                            | Which webcam to use. Try `1`, `2`, … if you have more than one. |
| `ALERT_URL`       | `http://127.0.0.1:5000/alert`  | Page opened when you lose focus.                    |
| `ALERT_COOLDOWN`  | `30`                           | Minimum seconds between alerts.                     |
| `FOCUS_THRESHOLD` | `30`                           | Degrees of head turn allowed before an alert.       |

If you change the port in `server.py`, update `ALERT_URL` to match.

## How It Works

1. **Face detection:** OpenCV's Haar cascade classifier finds faces in each webcam frame.
2. **Focus estimation:** Head orientation is approximated from where your face sits relative to the center of the frame.
3. **Alert trigger:** If no face is found, or your head is turned past the threshold for too long, the alert page opens (no more than once per cooldown period).
4. **Alert page:** A small Flask server serves an HTML page that uses CSS animations and the Web Audio API to play the alarm.

## Troubleshooting

- **Camera won't open:** Close other apps using the webcam, or change `CAMERA_INDEX`. On macOS, allow camera access for your terminal in *System Settings → Privacy & Security → Camera*.
- **Alert page doesn't load:** Make sure `server.py` is running and that port 5000 isn't used by another program.
- **No sound:** Most browsers block audio until you've interacted with the page. Click the alert page once, or allow autoplay for `127.0.0.1`.

## Tips and Limitations

- Works best with good, even lighting.
- Sit within about 2–3 feet (60–90 cm) of the webcam.
- Multiple people or pets in frame can cause false positives.
- The orientation estimate is approximate; tune `FOCUS_THRESHOLD` to your setup.
