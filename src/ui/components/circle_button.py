from PyQt6.QtWidgets import QPushButton, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

class CircleButton(QPushButton):
    def __init__(self, size, parent=None):
        super().__init__(parent)
        self.setFixedSize(QSize(size, size))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Setup layout for text
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # State text label
        self.state_text = QLabel("Ready")
        self.state_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont('Inter', 14)
        font.setWeight(QFont.Weight.Medium)
        self.state_text.setFont(font)
        layout.addWidget(self.state_text)
        
        # Style states
        self.idle_style = """
            QPushButton {
                background-color: rgba(74, 144, 226, 0.1);
                border: 2px solid rgba(74, 144, 226, 0.7);
                border-radius: %dpx;
            }
            QPushButton:hover {
                background-color: rgba(74, 144, 226, 0.15);
            }
        """ % (size // 2)
        
        self.recording_style = """
            QPushButton {
                background-color: rgba(255, 0, 0, 0.1);
                border: 2px solid rgba(255, 0, 0, 0.7);
                border-radius: %dpx;
            }
        """ % (size // 2)
        
        self.processing_style = """
            QPushButton {
                background-color: rgba(255, 215, 0, 0.1);
                border: 2px solid rgba(255, 215, 0, 0.7);
                border-radius: %dpx;
            }
        """ % (size // 2)
        
        self.api_missing_style = """
            QPushButton {
                background-color: rgba(74, 144, 226, 0.05);
                border: 2px dashed rgba(74, 144, 226, 0.5);
                border-radius: %dpx;
            }
            QPushButton:hover {
                background-color: rgba(74, 144, 226, 0.1);
            }
        """ % (size // 2)
        
        # Initial state
        self.setStyleSheet(self.idle_style)
        
    def update_state(self, state: str):
        """Update the button state text."""
        state_text_map = {
            "ready": "Ready",
            "recording": "Recording...",
            "processing": "Processing...",
            "api_missing": "Set API key"
        }
        self.state_text.setText(state_text_map.get(state, state))
        
    def mousePressEvent(self, event):
        """Let parent window handle all mouse events."""
        event.ignore()
        
    def mouseMoveEvent(self, event):
        """Let parent window handle all mouse events."""
        event.ignore()
        
    def mouseReleaseEvent(self, event):
        """Let parent window handle all mouse events."""
        event.ignore()