import time
from pynput.keyboard import Key, Listener
from pynput.mouse import Controller
from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel
import vgamepad as vg


class TreadmillController:
    """Handles the core treadmill logic - mouse to joystick conversion"""

    # Constants
    JOYSTICK_MIN = -32768
    JOYSTICK_MAX = 32767
    MOUSE_CENTER_X = 700
    MOUSE_CENTER_Y = 500

    def __init__(self):
        self.gamepad = vg.VX360Gamepad()
        self.mouse = Controller()
        self.sensitivity = 150
        self.poll_rate = 30
        self.quit_key = Key.ctrl_r
        self.enabled = False
        self.key_toggle = False

    def start(self):
        """Start the treadmill control loop"""
        self.enabled = True
        prev_mouse_y = 0

        while self.enabled and not self.key_toggle:
            # Calculate mouse delta from center
            current_mouse_y = (self.mouse.position[1] - self.MOUSE_CENTER_Y) * -self.sensitivity

            # Average with previous value for smoothing
            smoothed_y = (current_mouse_y + prev_mouse_y) / 2
            prev_mouse_y = current_mouse_y

            # Clamp to joystick range
            joystick_y = max(self.JOYSTICK_MIN, min(self.JOYSTICK_MAX, int(smoothed_y)))

            # Reset mouse to center
            self.mouse.position = (self.MOUSE_CENTER_X, self.MOUSE_CENTER_Y)

            print(f"Joystick y: {joystick_y}")

            # Update gamepad
            self.gamepad.left_joystick(x_value=0, y_value=joystick_y)
            self.gamepad.update()

            time.sleep(1 / self.poll_rate)

    def stop(self):
        """Stop the treadmill control loop"""
        self.enabled = False


class TreadmillThread(QThread):
    """Thread to run the treadmill control loop without blocking the UI"""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    def run(self):
        self.controller.start()


class MainWindow(QWidget):
    """Main GUI window for controlling the treadmill"""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.treadmill_thread = None
        self.setup_ui()

    def setup_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Maratron Kimoi")

        # Create widgets
        start_button = QPushButton("Start")
        start_button.clicked.connect(self.on_start)

        self.set_key_button = QPushButton("Set Stop Key")
        self.set_key_button.clicked.connect(self.on_set_key)

        poll_label = QLabel("Polling Rate (/sec):")
        sense_label = QLabel("Sensitivity:")

        self.key_label = QLabel(f"Stop Key: {self.controller.quit_key}")

        self.poll_rate_input = QLineEdit(str(self.controller.poll_rate))
        self.poll_rate_input.textChanged.connect(self.on_poll_rate_changed)

        self.sensitivity_input = QLineEdit(str(self.controller.sensitivity))
        self.sensitivity_input.textChanged.connect(self.on_sensitivity_changed)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(start_button)
        layout.addWidget(sense_label)
        layout.addWidget(self.sensitivity_input)
        layout.addWidget(poll_label)
        layout.addWidget(self.poll_rate_input)
        layout.addWidget(self.key_label)
        layout.addWidget(self.set_key_button)

        self.setLayout(layout)

    def on_poll_rate_changed(self, text):
        """Handle polling rate input changes"""
        if text:
            try:
                value = int(text)
                if value > 0:
                    self.controller.poll_rate = value
                    print(f"Poll rate: {value}")
            except ValueError:
                print(f"Invalid poll rate: {text}")

    def on_sensitivity_changed(self, text):
        """Handle sensitivity input changes"""
        if text:
            try:
                value = int(text)
                self.controller.sensitivity = value
                print(f"Sensitivity: {value}")
            except ValueError:
                print(f"Invalid sensitivity: {text}")

    def on_set_key(self):
        """Toggle key listening mode"""
        if not self.controller.key_toggle:
            self.key_label.setText("PRESS ANY KEY")
            self.set_key_button.setText("Confirm?")
            print("Listening for key...")
            self.controller.key_toggle = True
        else:
            self.key_label.setText(f"Stop Key: {self.controller.quit_key}")
            self.set_key_button.setText("Set Stop Key")
            print("Key confirmed")
            self.controller.key_toggle = False

    def on_start(self):
        """Start the treadmill control in a separate thread"""
        if self.treadmill_thread is None or not self.treadmill_thread.isRunning():
            self.treadmill_thread = TreadmillThread(self.controller)
            self.treadmill_thread.start()
            print("Treadmill started")


def on_key_press(key, controller):
    """Handle keyboard input for setting stop key and stopping"""
    if controller.key_toggle:
        print(f"Stop key will be: {key}")
        controller.quit_key = key
    elif key == controller.quit_key:
        controller.stop()
        print(f"Stopped with {controller.quit_key}")


def main():
    """Main entry point"""
    controller = TreadmillController()

    # Set up keyboard listener
    listener = Listener(on_press=lambda key: on_key_press(key, controller))
    listener.start()

    # Start GUI
    app = QApplication([])
    window = MainWindow(controller)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
