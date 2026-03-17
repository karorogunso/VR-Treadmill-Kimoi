# VR-Treadmill Kimoi Version

A Python-based VR treadmill application that converts mouse movement into virtual Xbox 360 controller joystick input. Perfect for VR treadmill setups where you want to control in-game movement using physical motion.

## Features

- Real-time mouse position tracking converted to joystick input
- GUI interface to adjust sensitivity and polling rate
- Customizable stop key binding
- Virtual Xbox 360 controller emulation via ViGEmBus

## Requirements

### System Requirements
- **Operating System**: Windows 10/11 (64-bit)
- **Python**: Python 3.8 or higher (only needed if running from source)
- **VR Setup**: Any VR treadmill or setup that uses mouse input

### Required Software
1. **ViGEmBus Driver** (REQUIRED for gamepad emulation)
   - Download from: https://github.com/nefarius/ViGEmBus/releases
   - Install the latest release before running the application

### Python Dependencies (if running from source)
```bash
pip install pynput
pip install vgamepad
pip install PyQt6
```
Or install all at once:
```bash
pip install -r requirements.txt
```

## Installation

### Option 1: Using Pre-built Executable (Recommended)
1. Install the [ViGEmBus driver](https://github.com/nefarius/ViGEmBus/releases)
2. Download `Maratron.exe` from the releases
3. Run `Maratron.exe` - no Python installation needed!

### Option 2: Running from Source
1. Install Python 3.8 or higher
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Or install individually:
   ```bash
   pip install pynput vgamepad PyQt6
   ```
3. Install the [ViGEmBus driver](https://github.com/nefarius/ViGEmBus/releases)
4. Run the script:
   ```bash
   python treadmill.py
   ```

### Option 3: Building Your Own Executable
**Note: Requires Windows OS to build the .exe file**

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Build the executable:
   ```bash
   python -m PyInstaller Maratron.spec --clean
   ```
3. Find your executable in the `dist` folder

## How to Use

### Basic Usage
1. **Launch the application** (either `Maratron.exe` or `python treadmill.py`)
2. **Configure settings** (optional):
   - **Sensitivity**: How responsive the joystick is to mouse movement (default: 150)
   - **Polling Rate**: How many times per second the mouse is checked (default: 30/sec)
   - **Stop Key**: Key to stop the joystick input (default: Right Ctrl)
3. **Click "Start"** to begin converting mouse movement to joystick input
4. **Move your mouse** - the vertical position controls the joystick Y-axis
5. **Press the Stop Key** (Right Ctrl by default) to stop

### Changing the Stop Key
1. Click **"Set Stop Key"** button
2. The label will change to **"PRESS ANY KEY"**
3. Press the key you want to use as the stop key
4. Click **"Confirm?"** to save the new key

### Steam Input Setup
To bind the virtual gamepad in Steam:
1. Open `treadmill.py` in a text editor
2. Comment out line 98: `mouse.position = (700, 500)`
   - Add `#` at the beginning: `# mouse.position = (700, 500)`
3. Run the script and configure Steam Input to recognize the virtual controller
4. Once configured, uncomment the line (remove the `#`) and restart the script

### Adjusting Mouse Reset Position
If the mouse cursor appears off-screen during use:
1. Open `treadmill.py` in a text editor
2. Find line 98: `mouse.position = (700, 500)`
3. Adjust the coordinates to match your screen center
   - Example for 1920x1080: `mouse.position = (960, 540)`

## Configuration

### Default Settings (can be changed in the GUI):
- **Sensitivity**: 150
- **Polling Rate**: 30 times per second
- **Stop Key**: Right Ctrl

### Permanent Configuration (edit `treadmill.py`):
Lines 14-16 contain the default values:
```python
sensitivity = 150    # How sensitive the joystick will be
pollRate = 30        # How many times per second the mouse will be checked
quitKey = Key.ctrl_r # Which key will stop the program
```

## Troubleshooting

### "Could not find module 'ViGEmClient.dll'" error
- **Solution**: Install the [ViGEmBus driver](https://github.com/nefarius/ViGEmBus/releases)

### PyInstaller not recognized in PowerShell
- **Solution**: Use `python -m PyInstaller` instead of just `pyinstaller`

### Mouse cursor is off-screen
- **Solution**: Edit line 98 in `treadmill.py` to adjust the reset position

### Antivirus blocks the .exe file (False Positive)
- **Why**: PyInstaller executables are commonly flagged as false positives (especially Trojan:Win32/Wacatac.B!ml) because:
  - They self-extract to temp directories at runtime
  - They bundle Python + libraries in a way that looks like malware packers
  - The .exe is unsigned
- **Solution**:
  1. Add an exclusion in Windows Defender: `Settings > Virus & threat protection > Exclusions`
  2. Verify safety: Upload to VirusTotal.com (most scanners will show clean)
  3. Build from source yourself using the instructions above
  4. Submit false positive report to Microsoft: https://www.microsoft.com/wdsi/filesubmission

### Controller not detected in games
- **Solution**:
  1. Ensure ViGEmBus driver is installed
  2. Check if the virtual controller appears in "Devices and Printers" when the app is running
  3. Some games may need Steam Input configured

## Plan
- Refactor Code
- Create Better GUI
- Using an OpenXR library from https://github.com/KhronosGroup/OpenXR-SDK to directly control the game.
- Remove ViGEmBus driver in future release
- Support for horizontal (X-axis) movement
- Multiple controller profiles

## License

This project uses the ViGEmBus driver for virtual gamepad emulation.
