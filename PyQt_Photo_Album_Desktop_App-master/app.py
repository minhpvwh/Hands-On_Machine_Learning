import sys
from os import listdir
from os.path import isfile, join
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon

DEFAULT_IMAGE_ALBUM_DIRECTORY = './my-album/'

## Check that a file name has a valid image extension for QPixmap
def filename_has_image_extension(filename):
    valid_img_extensions = \
        ['bmp', 'gif', 'jpg', 'jpeg', 'png', 'pbm', 'pgm', 'ppm', 'xbm', 'xpm', 'arw', 'jfif']
    filename = filename.lower()
    extension = filename[-3:]
    four_char = filename[-4:] ## exclusively for jpeg
    if extension in valid_img_extensions or four_char in valid_img_extensions:
        return True
    else:
        return False


## Widget for the single image that is currently on display
class DisplayImage(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.parent = parent
        self.pixmap = QPixmap()
        self.label = QLabel(self)
        self.assigned_img_full_path = ''

    def update_display_image(self, path_to_image=''):
        self.assigned_img_full_path = path_to_image

        ## render the display image when a thumbnail is selected
        self.on_main_window_resize()

    def on_main_window_resize(self, event=None):
        main_window_size = self.parent.size()
        main_window_height = main_window_size.height()
        main_window_width = main_window_size.width()

        display_image_max_height = main_window_height - 50
        display_image_max_width = main_window_width - 200

        self.pixmap = QPixmap(self.assigned_img_full_path)
        self.pixmap = self.pixmap.scaled(QSize(display_image_max_width, display_image_max_height), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.label.setPixmap(self.pixmap)


## Widget for selecting an image in the directory to display
## Makes a vertical scrollable widget with selectable image thumbnails
class ImageFileSelector(QWidget):
    def __init__(self, parent=None, album_path='', display_image=None):
        QWidget.__init__(self, parent=parent)
        self.display_image = display_image
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setVerticalSpacing(30)

        ## Get all the image files in the directory
        files = [f for f in listdir(album_path) if isfile(join(album_path, f))]
        row_in_grid_layout = col_in_grid_layout = 0
        first_img_file_path = ''

        ## Render a thumbnail in the widget for every image in the directory
        for file_name in files:
            if filename_has_image_extension(file_name) is False: continue

            img_label = QLabel()
            img_label01 = QLabel()
            img_label02 = QLabel()
            img_label03 = QLabel()
            img_label04 = QLabel()

            text_label = QLabel()
            text_label01 = QLabel()
            text_label02 = QLabel()
            text_label03 = QLabel()
            text_label04 = QLabel()

            img_label.setAlignment(Qt.AlignCenter)
            img_label01.setAlignment(Qt.AlignCenter)
            img_label02.setAlignment(Qt.AlignCenter)
            img_label03.setAlignment(Qt.AlignCenter)
            img_label04.setAlignment(Qt.AlignCenter)

            text_label.setAlignment(Qt.AlignCenter)
            text_label01.setAlignment(Qt.AlignCenter)
            text_label02.setAlignment(Qt.AlignCenter)
            text_label03.setAlignment(Qt.AlignCenter)
            text_label04.setAlignment(Qt.AlignCenter)

            file_path = album_path + file_name
            pixmap = QPixmap(file_path)
            pixmap = pixmap.scaled(QSize(100, 100), Qt.KeepAspectRatio, Qt.SmoothTransformation)

            img_label.setPixmap(pixmap)
            img_label01.setPixmap(pixmap)
            img_label02.setPixmap(pixmap)
            img_label03.setPixmap(pixmap)
            img_label04.setPixmap(pixmap)

            text_label.setText(file_name)
            text_label01.setText(file_name)
            text_label02.setText(file_name)
            text_label03.setText(file_name)
            text_label04.setText(file_name)

            img_label.mousePressEvent = lambda e, index=row_in_grid_layout, file_path=file_path: self.on_thumbnail_click(e, index, file_path)
            text_label.mousePressEvent = img_label.mousePressEvent

            thumbnail = QBoxLayout(QBoxLayout.TopToBottom)
            thumbnail.addWidget(img_label)
            thumbnail.addWidget(text_label)
            thumbnail01 = QBoxLayout(QBoxLayout.TopToBottom)
            thumbnail01.addWidget(img_label01)
            thumbnail01.addWidget(text_label01)
            thumbnail02 = QBoxLayout(QBoxLayout.TopToBottom)
            thumbnail02.addWidget(img_label02)
            thumbnail02.addWidget(text_label02)
            thumbnail03 = QBoxLayout(QBoxLayout.TopToBottom)
            thumbnail03.addWidget(img_label03)
            thumbnail03.addWidget(text_label03)
            thumbnail04 = QBoxLayout(QBoxLayout.TopToBottom)
            thumbnail04.addWidget(img_label04)
            thumbnail04.addWidget(text_label04)

            self.grid_layout.addLayout(thumbnail, row_in_grid_layout, 0, Qt.AlignCenter)
            self.grid_layout.addLayout(thumbnail01, row_in_grid_layout, 1, Qt.AlignCenter)
            self.grid_layout.addLayout(thumbnail02, row_in_grid_layout, 2, Qt.AlignCenter)
            self.grid_layout.addLayout(thumbnail03, row_in_grid_layout, 3, Qt.AlignCenter)
            self.grid_layout.addLayout(thumbnail04, row_in_grid_layout, 4, Qt.AlignCenter)

            if row_in_grid_layout == 0: first_img_file_path = file_path
            row_in_grid_layout += 1

        ## Automatically select the first file in the list during init
        self.on_thumbnail_click(None, 0, first_img_file_path)

    def on_thumbnail_click(self, event, index, img_file_path):
        ## Deselect all thumbnails in the image selector
        print(len(self.grid_layout))
        for text_label_index in range(9):
            text_label = self.grid_layout.itemAtPosition(text_label_index, 0).itemAt(1).widget()
            text_label.setStyleSheet("background-color:none;")

        ## Select the single clicked thumbnail
        text_label_of_thumbnail = self.grid_layout.itemAtPosition(index, 0).itemAt(1).widget()
        text_label_of_thumbnail.setStyleSheet("background-color:blue;")

        ## Update the display's image
        self.display_image.update_display_image(img_file_path)


class App(QWidget):
    def __init__(self):
        super().__init__()
        ## Set main window attributes
        self.title = 'Photo Album Viewer'
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 600
        self.resizeEvent = lambda e : self.on_main_window_resize(e)

        ## Make 2 widgets, one to select an image and one to display an image
        self.display_image = DisplayImage(self)
        self.image_file_selector = ImageFileSelector(album_path=DEFAULT_IMAGE_ALBUM_DIRECTORY, display_image=self.display_image)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedWidth(600)
        nav = scroll
        nav.setWidget(self.image_file_selector)

        ## Add the 2 widgets to the main window layout
        layout = QGridLayout(self)
        layout.addWidget(nav, 0, 0, Qt.AlignLeft)
        layout.addWidget(self.display_image.label, 0, 1, Qt.AlignRight)
        bu = QPushButton("Browse File", self)
        # bu.setIcon(QIcon("../default.png"))
        # bu.setIconSize(QSize(100, 100))
        bu.setMinimumHeight(50)
        # a = QLabel(self,'m')
        # thumbnail = QBoxLayout(self)
        # thumbnail.addWidget(bu)
        # thumbnail.addWidget(a)
        # layout.addWidget(q, 0, 2)
        layout.addWidget(bu, 0, 2)


        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(1800, 600)
        self.show()

    ## Set the display image size based on the new window size
    def on_main_window_resize(self, event):
        self.display_image.on_main_window_resize(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
