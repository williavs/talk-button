from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QWidget,
    QPushButton, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QTimer, QUrl, QSize
from PyQt6.QtGui import QFont, QDesktopServices, QPixmap, QPainter, QPainterPath
from pathlib import Path

class AnimatedLabel(QLabel):
    def __init__(self, text, delay=0, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("color: white; margin-top: 10px;")
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setWordWrap(True)
        
        # Initial state
        self.setGraphicsEffect(None)
        self.hide()
        
        # Animate after delay
        QTimer.singleShot(delay, self.animate_in)
        
    def animate_in(self):
        self.show()
        # Start from left
        self.move(self.x() - 50, self.y())
        self.setStyleSheet("color: rgba(255, 255, 255, 0);")
        
        # Position animation
        self.pos_anim = QPropertyAnimation(self, b"pos")
        self.pos_anim.setDuration(800)
        self.pos_anim.setStartValue(QPoint(self.x(), self.y()))
        self.pos_anim.setEndValue(QPoint(self.x() + 50, self.y()))
        self.pos_anim.setEasingCurve(QEasingCurve.Type.OutQuart)
        
        # Opacity animation through stylesheet
        self.style_anim = QPropertyAnimation(self, b"styleSheet")
        self.style_anim.setDuration(800)
        self.style_anim.setStartValue("color: rgba(255, 255, 255, 0);")
        self.style_anim.setEndValue("color: rgba(255, 255, 255, 1);")
        self.style_anim.setEasingCurve(QEasingCurve.Type.OutQuart)
        
        self.pos_anim.start()
        self.style_anim.start()

class CircularImageLabel(QLabel):
    def __init__(self, image_path, size=200, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self.setScaledContents(True)
        
        # Load and process the image
        pixmap = QPixmap(str(image_path))
        if not pixmap.isNull():
            # Create circular mask
            target = QPixmap(size, size)
            target.fill(Qt.GlobalColor.transparent)
            
            painter = QPainter(target)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            
            # Create circular path
            path = QPainterPath()
            path.addEllipse(0, 0, size, size)
            painter.setClipPath(path)
            
            # Scale and draw the image
            scaled_pixmap = pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
            
            # Center the image
            x = (size - scaled_pixmap.width()) // 2
            y = (size - scaled_pixmap.height()) // 2
            painter.drawPixmap(x, y, scaled_pixmap)
            painter.end()
            
            self.setPixmap(target)
        
        # Add glow effect
        self.setStyleSheet("""
            QLabel {
                background: transparent;
                border-radius: 100px;
                border: 2px solid rgba(74, 144, 226, 0.3);
            }
        """)
        
        # Initial state
        self.setGraphicsEffect(None)
        self.hide()
        
    def animate_in(self):
        self.show()
        # Scale animation
        self.scale_anim = QPropertyAnimation(self, b"geometry")
        self.scale_anim.setDuration(1000)
        current_geo = self.geometry()
        center = current_geo.center()
        start_geo = QPoint(center.x() - 0, center.y() - 0)
        self.scale_anim.setStartValue(self.geometry())
        self.scale_anim.setEndValue(current_geo)
        self.scale_anim.setEasingCurve(QEasingCurve.Type.OutBack)
        self.scale_anim.start()

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setFixedSize(600, 700)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the dialog UI."""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #2b2b2b;
            }
            QScrollBar:vertical {
                border: none;
                background: #2b2b2b;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.1);
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        # Content widget
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(10)
        
        # Profile Image
        image_path = Path(__file__).parent.parent.parent.parent / "public" / "profile.jpeg"
        profile_image = CircularImageLabel(image_path, size=200)
        content_layout.addWidget(profile_image, alignment=Qt.AlignmentFlag.AlignCenter)
        QTimer.singleShot(100, profile_image.animate_in)
        
        # Header
        title = AnimatedLabel("Willy V3", delay=400)
        title.setFont(QFont('Inter', 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(title)
        
        subtitle = AnimatedLabel("AI Engineer & Product Manager", delay=600)
        subtitle.setFont(QFont('Inter', 16))
        subtitle.setStyleSheet("color: #4a90e2;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(subtitle)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background: rgba(255, 255, 255, 0.1); margin: 20px 0;")
        content_layout.addWidget(separator)
        
        # About Me
        about_title = AnimatedLabel("About Me", delay=800)
        about_title.setFont(QFont('Inter', 18, QFont.Weight.Bold))
        content_layout.addWidget(about_title)
        
        about_text = AnimatedLabel(
            "Based in Brooklyn, I'm a multifaceted technologist combining AI engineering "
            "with product management. By day, I serve as a Product Manager at Justworks, "
            "where I help shape the future of HR and payroll solutions. By night, I'm "
            "building V3Consult (v3-ai.com), where I develop innovative AI applications "
            "and provide consulting services.\n\n"
            "When I'm not coding or strategizing product development, you'll find me in "
            "Brooklyn with my two dogs, Christopher and Andrew, and my partner. I'm "
            "passionate about leveraging AI to create practical solutions that make a "
            "real difference in how people work and interact with technology.",
            delay=1000
        )
        content_layout.addWidget(about_text)
        
        # Projects
        projects_title = AnimatedLabel("Projects", delay=1200)
        projects_title.setFont(QFont('Inter', 18, QFont.Weight.Bold))
        content_layout.addWidget(projects_title)
        
        projects = [
            ("V3 AI", "AI consulting and application development"),
            ("Living Letter", "A community platform fostering hope and connection, providing support and resources for suicide prevention"),
            ("Curated by Sonia", "Sustainable fashion curation service helping clients build eco-conscious wardrobes")
        ]
        
        for i, (name, desc) in enumerate(projects):
            project = AnimatedLabel(f"<b>{name}</b><br>{desc}", delay=1400 + i*200)
            content_layout.addWidget(project)
        
        # Contact
        contact_title = AnimatedLabel("Get in Touch", delay=2000)
        contact_title.setFont(QFont('Inter', 18, QFont.Weight.Bold))
        content_layout.addWidget(contact_title)
        
        contact_text = AnimatedLabel(
            "Whether you're interested in AI consulting, product development, or just "
            "want to connect, I'm always open to new opportunities and conversations.",
            delay=2200
        )
        content_layout.addWidget(contact_text)
        
        # Links
        links = [
            ("Email", "willy@v3-ai.com"),
            ("GitHub", "github.com/williavs"),
            ("LinkedIn", "linkedin.com/in/willyv3"),
            ("Website", "v3-ai.com")
        ]
        
        for i, (platform, link) in enumerate(links):
            link_label = AnimatedLabel(f"<b>{platform}:</b> <a href='{link}' style='color: #4a90e2; text-decoration: none;'>{link}</a>", delay=2400 + i*200)
            link_label.setOpenExternalLinks(True)
            content_layout.addWidget(link_label)
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        # Dialog styling
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
            }
        """) 