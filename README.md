# RootsCTF — Civilization CTF Platform

A turnkey, production-ready [CTFd](https://ctfd.io/) instance pre-configured for the **RootsCTF: Civilization** competition.

---

## 🏛️ Features & Customizations Included

- **Civilization Theme (Charcoal & Emerald)**:
  - Sleek modern dark mode (`#14171E` canvas with `#1B202A` surfaces).
  - High-contrast, readable inputs, review/comment boxes, and modals.
  - Seamless header title without floating dark boxes.
  - Transparent, high-resolution Civilization logo neatly integrated into the navbar.
- **Calibrated Scoreboard Chart**:
  - Apache ECharts timeline graph with custom emerald theme palette.
  - **Toolbox Zoom & Restore**: Box-zoom into specific time intervals, step-back undo, and a dedicated **Reset Zoom** (`restore`) button.
  - Calibrated grid positioning (`top: 95px`, slider at `top: 38px`) so the zoom slider never collides with score lines or data points.
- **Pre-Configured Database (`ctfd.db`)**:
  - CTF name, user mode (`teams`), public scoreboard, and credentials already initialized.
  - Admin team & user: `Cosmos`.
  - Challenge review, scoring, and ratings system enabled.
- **Cryptography Challenge Suite (`Cryptography/`)**:
  - Full set of civilization-themed challenges with position-dependent ciphers, historical narratives, hints, flag keys (`Roots{...}`), and automated setup script (`setup_ctfd.py`).

---

## 🚀 Quick Start (Running the Exact Server)

### Prerequisites
- Python 3.9+ (Python 3.11 recommended)
- `pip` or [`uv`](https://docs.astral.sh/uv/)

### 1-Click Launch (Windows)
Double-click:
```bat
start.bat
```

### 1-Click Launch (Linux / macOS)
```bash
chmod +x start.sh
./start.sh
```

---

### Manual Setup & Run

1. **Install dependencies:**
   ```bash
   cd CTFd
   pip install -r requirements.txt
   ```
   *(Or using uv: `uv pip install -r requirements.txt`)*

2. **Start the server:**
   ```bash
   python serve.py --port 8000
   ```

3. **Open in your browser:**
   ```
   http://127.0.0.1:8000
   ```

---

## 🐳 Docker Deployment (Alternative)

To run with Docker:
```bash
cd CTFd
docker-compose up -d
```
Access at `http://localhost:8000`.

---

## 📁 Repository Structure

```
├── CTFd/
│   ├── CTFd/
│   │   ├── ctfd.db             # Pre-configured SQLite database (theme, users, scores, settings)
│   │   ├── uploads/             # Custom transparent logo and challenge file attachments
│   │   └── themes/core/         # Core theme templates & assets
│   ├── apply_theme.py           # Script to re-apply the Civilization theme to the database
│   ├── theme_header.html        # Raw theme CSS and ECharts calibration code
│   ├── live_scoreboard.html     # Dedicated standalone projector/stage live scoreboard
│   ├── serve.py                 # Development server entry point
│   ├── requirements.txt         # Python dependencies
│   └── docker-compose.yml       # Multi-container Docker configuration
├── Cryptography/
│   ├── challenges/              # Challenge YAMLs, ciphers, and solver scripts
│   ├── setup_ctfd.py            # Automated challenge deployment script via CTFd API
│   └── ctfd_challenges.csv      # Challenge backup matrix
├── start.bat                    # Windows 1-click server launcher
├── start.sh                     # Linux/macOS 1-click server launcher
└── README.md
```

---

## 🔑 Default Credentials
- **Admin User**: `Cosmos` (`dhyeymendpara72@gmail.com`)
- **Admin Team**: `Cosmos`
- **CTFd Port**: `8000`
