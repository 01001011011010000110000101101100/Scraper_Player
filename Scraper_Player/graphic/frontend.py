"""
    The file that responsible for GUI interface and connect logic with the application's attributes.
"""

import os, sys, asyncio, logging, sqlite3
from typing import List, Callable, Any

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QMainWindow,
    QLabel, QPushButton, QHBoxLayout, QMessageBox,
    QDialog, QButtonGroup, QRadioButton, QBoxLayout, QLayout,
    QGridLayout, QSizePolicy
)
from PySide6.QtGui import QPixmap, QDesktopServices
from PySide6.QtCore import QTimer, Qt, QSize, QUrl, QSettings
from httpx import URL
from qasync import asyncSlot
import subprocess
import shutil

from interfaces.ui_main import Ui_MzAnime
from interfaces.ui_card import Ui_anime_card_widget
import internet.scraper as scraper
from internet.internet_handle import NetworkManager
from regulator.models import IconModel, PageDetailsModel, EpisodeModel
from database.handle_database import DatabaseManager

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow) : 
    def __init__(self) : 
        super().__init__()
        
        self.ui = Ui_MzAnime()
        self.ui.setupUi(self)
        self.setWindowTitle("App")

        self.full_stacked = self.ui.full_stacked
        self.upper_layout = self.ui.upper_layout

        self.lower_stacked = self.ui.lower_stacked
        self.lower_layout = self.ui.lower_layout

        self.home_btn = self.ui.home_btn
        self.home_btn.clicked.connect(self.go_home)

        self.search_btn = self.ui.search_btn
        self.search_filed = self.ui.search_filed

        self.search_filed.setPlaceholderText("Search..")
        self.search_btn.clicked.connect(self.searching)

        self.menu_btn = self.ui.menu_btn
        self.available_players = self.detect_installed_players()

        self._is_player_open = False
        DatabaseManager.init_database()

        QTimer.singleShot(20, self.load_main_page)

    # ----------------------------------
    #   1. Main Asynchronous Functions 
    # ----------------------------------

    @asyncSlot()
    async def load_main_page(self) -> None :
        """
        Load the cards in the main data when the app in lunched
        or the home button is clicked (As a refresh button) 
        """  

        self.grid_clear()
        self.lower_stacked.setCurrentIndex(0)

        cards_list = await scraper.fetch_main_icons()

        if not cards_list : 
            self.grid_clear()
            QMessageBox.warning(self, 'Warning', "Has a problem with load data pleas try later")
            return

        row = 0; col = 0; max_col = 4

        for card in cards_list :

            card_widget = await self.create_card(card)
            self.lower_layout.addWidget(card_widget, row, col)

            col += 1
            if col >= max_col :
                row += 1; col = 0


    @asyncSlot()
    async def display_page(self, page_url: URL) -> None :
        """ 
        Display card page when clicked in main page
        it takes the url from the url in the create_card.
        The URL has defined in a lambda function when the card created
        """

        self.validity_buttons(self.lower_layout, False)
        self.grid_clear()
        details: PageDetailsModel = await scraper.fetch_card_data(page_url) # Scrap data from the internet

        # The container widget has the page index for lower_stacked
        card_page_widget = QWidget()
        if not details:
            QMessageBox.warning(card_page_widget, "Warning", "Cannot found data!. Please try later")
            return # Checks if the data exists or not

        # Download the ui widget and initialize
        ui_page = Ui_anime_card_widget()
        ui_page.setupUi(card_page_widget)

        # Connect extracted data with the designed widget
        ui_page.title_label.setText(f'<h1>{details.title}</h1>'); ui_page.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        continuity = details.continuity
        description = details.description
        categories = ", ".join(details.categories)

        text_label = f"""
        الحالة :   {continuity}\n
        التصنيف : {categories}\n
        الوصف :  {description}\n
        """
        ui_page.status_label.setText(text_label)
        ui_page.status_label.setWordWrap(True)
        ui_page.status_label.adjustSize()

        ico_url = details.icon_url
        await self.set_icon(ico_url, ui_page.icon_label)

        epi_list : List[EpisodeModel] = details.episodes_urls
        for epi_obj in reversed(epi_list):

            # Create the episodes widget and the layout 
            epi_widget = QWidget()
            layout = QHBoxLayout(epi_widget)

            # Define the label and button data
            epi_count = QLabel(f"الحلقة رقم : {epi_obj.number}"); epi_count.setAlignment(Qt.AlignmentFlag.AlignRight)
            mark_btn = QPushButton("شوهد")
            mark_btn.clicked.connect(lambda checked, epi_num=epi_obj.number, mv_name=details.title: DatabaseManager.watched_epi(mv_name, epi_num))
            watch_btn = QPushButton("مشاهدة")
            watch_btn.clicked.connect(lambda checked, source_url=epi_obj.source_url, btn=watch_btn: self.open_player(source_url, btn))
            watch_btn.setMinimumHeight(30)

            # Set the data in the layout 
            layout.addWidget(epi_count)
            # layout.addWidget(mark_btn)
            layout.addWidget(watch_btn)
            ui_page.episodes_layout.addWidget(epi_widget)

        while self.lower_stacked.count() > 1:
            old_widget = self.lower_stacked.widget(1)
            self.lower_stacked.removeWidget(old_widget)
            old_widget.deleteLater()

        self.lower_stacked.addWidget(card_page_widget)
        self.lower_stacked.setCurrentWidget(card_page_widget)


    @asyncSlot()
    async def open_player(self, source_url: URL, w_btn: QPushButton = None) -> None :
        """
        Open the stream URL in a Player. Takes the layout to enable th buttons if disabled.
        If the function got non layout instance will nothing going to happen.
        """

        if self._is_player_open : return None


        if not isinstance(source_url, URL) :
            logger.error("Have given non URL instance to open the media player")
            raise ValueError(f"Except httpx.URL instance. Got {type(source_url).__name__}")

        if not isinstance(w_btn, QPushButton) and not isinstance(w_btn, None):
            logger.error(f"except QPushButton or nothing but got {type(w_btn).__name__}")
            raise ValueError(f"Except 'QPushButton' instance or nothing. Got {type(w_btn).__name__}")

        self._is_player_open = True
        w_btn.setDisabled(True)

        card_data = await scraper.fetch_card_data(source_url)
        source = card_data.source_url
        stream_url = await scraper.fetch_stream_url(source)

        watch_dialog = self.PlayerDialog(stream_url=stream_url, parent=self)
        watch_dialog.exec()

        self._is_player_open = False
        w_btn.setEnabled(True)


    @asyncSlot()
    async def searching(self) -> None : 

        sub = self.search_filed.text().strip()
        self.search_filed.clear()
        if not sub :
            return

        self.validity_buttons(self.upper_layout, False)

        self.grid_clear()
        self.lower_stacked.setCurrentIndex(0)

        cards_list : List[IconModel] = await scraper.search(sub)

        if not cards_list : 
            QMessageBox.warning(self, "Search Failed", f"Cannot found result for {sub}")
            return

        row = 0; col = 0; max_col = 4

        for card in cards_list :
            card_widget = await self.create_card(card)
            self.lower_layout.addWidget(card_widget, row, col)

            col += 1
            if col >= max_col :
                row += 1; col = 0
        self.validity_buttons(self.upper_layout, True)

    # ----------------------------------
    #   2. Sub-Asynchronous Functions
    # ----------------------------------

    async def create_card(self, card_data : IconModel) -> QWidget :  
        """
        Create a widget to display it in the lower layout.
        The widget has the icon and title of the anime.
        The icon is a button has the page URL.
        Thus, when the button is clicked it goes to load the page and display it in lower stacked
        """

        card = QWidget()
        card.setMaximumSize(220, 400)
        card.setStyleSheet("""
            QWidget {
                background-color: #1a1a2e;
                border-radius: 10px;
                border: 1px solid #16213e;
            }
        """)

        layout = QVBoxLayout(card)

        img_btn = QPushButton("Loading")
        img_btn.setFixedSize(200, 280)
        img_btn.clicked.connect(lambda checked, page_url=card_data.page_url: self.display_page(page_url))

        title_label = QLabel(card_data.title)
        title_label.setWordWrap(True)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(img_btn)
        layout.addWidget(title_label)

        icon_url : URL | None = card_data.icon_url
        if icon_url :
            asyncio.create_task(self.set_icon(icon_url, img_btn))

        return card


    async def set_icon(self, icon_url: URL, place_holder: QLabel | QPushButton) -> None:
        """ 
        The function take the URL of a web icon and the icon container to load the icon from the internat and place it in the container
        """

        try:
            resp = await scraper.send_request(url=icon_url)
            logger.debug(f"Sended a request to get picture to {icon_url} the response is : {resp.status_code} the content is : {resp.content}")
            if resp.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(resp.content)

                if isinstance(place_holder, QLabel) :
                    place_holder.clear()
                    place_holder.setPixmap(pixmap)
                    place_holder.setMinimumSize(400, 566)
            
                else:
                    place_holder.setText("")
                    place_holder.setIcon(pixmap)
                    place_holder.setIconSize(QSize(200, 366))
                    
        except Exception:
            place_holder.setText("Icon")


    # ----------------------------------
    #   3. Sub-Synchronous Functions
    # ----------------------------------

    def go_home(self) -> None :
        """
        Set index 0 in lower_layout to return to the main page
        """
        self.validity_buttons(self.upper_layout, False)
        self.lower_stacked.setCurrentIndex(0)
        self.load_main_page()
        self.validity_buttons(self.upper_layout, True)
        self.validity_buttons(self.lower_layout, True)


    def grid_clear(self) -> None :
        """ 
        Clear the lower layout from cards to append a new data without conflict 
        """

        if self.lower_layout :
            while self.lower_layout.count() :
                child = self.lower_layout.takeAt(0)
                if child.widget() :
                    child.widget().deleteLater()
            self.lower_layout.update()


    def detect_installed_players(self) -> list:
            
                available_players = []
        
                candidates = [
                    ("VLC (System)", ["vlc"]),
                    ("VLC (Flatpak)", ["flatpak", "run", "org.videolan.VLC"]),
                    ("VLC (Snap)", ["snap", "run", "vlc"]),
                    ("MPV Player", ["mpv"]),
                    ("MPV (Flatpak)", ["flatpak", "run", "io.mpv.Mpv"]),
                    ("Celluloid", ["celluloid"]),
                    ("PotPlayer", ["potplayer"]),
                    ("IINA", ["iina"]),
                ]
        
                for name, cmd in candidates:
                    if shutil.which(cmd[0]):
                        if len(cmd) > 1:
                            try:
                                check = subprocess.run(cmd + ["--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                                if check.returncode == 0:
                                    available_players.append((name, cmd))
                            except Exception:
                                continue
                        else:
                            available_players.append((name, cmd))
        
                return available_players


    def validity_buttons(self, layout: QVBoxLayout | QHBoxLayout | QGridLayout, enable : bool) :
        """ Enable or disable buttons in the given layout. True means enable and False means disable the buttons. """

        if not isinstance(layout, QLayout) and not isinstance(layout, QBoxLayout):
            logger.error("Get non layout instance to disable or enable the layout buttons")
            raise ValueError(f"Except 'QVBoxLayout', 'QHBoxLayout', or 'QGridLayout' instance. Got {type(layout).__name__}")

        if not isinstance(enable, bool) :
            logger.error("Non bool instance has given")
            raise ValueError(f"Except bool instance. Got {type(layout).__name__}")

        buttons = layout.findChildren(QPushButton)
        for btn in buttons: 
            btn.setEnabled(enable)


    def closeEvent(self, event):
        asyncio.create_task(NetworkManager.close())
        DatabaseManager.close_database()
        event.accept()

    # ----------------------------------
    #   4. Sub-Class Widgets
    # ----------------------------------

    class PlayerDialog(QDialog) :
        def __init__(self, stream_url : URL, parent: QMainWindow | QWidget =None) :
            super().__init__(parent)

            self.setWindowTitle("Chose Player")
            self.resize(380, 250)
            # self.setStyleSheet("""
            #     background-color: #060614;\n"
            #     "color: #ffffff;\n"
            #     "border-radius: 16px;\n"
            #     "border: 1px solid #374151;
            # """)

            layout = QVBoxLayout()

            self.btn_group = QButtonGroup(self)
            self.players_list = parent.available_players
            self.stream_url = str(stream_url)
        
            rb_default = QRadioButton("Default App")
            self.btn_group.addButton(rb_default, 99) 
            rb_default.setChecked(True)
            layout.addWidget(rb_default)

            for idx, (name, cmd) in enumerate(self.players_list):
                rb = QRadioButton(name)
                self.btn_group.addButton(rb, idx)
                layout.addWidget(rb)

            self.btn_play = QPushButton("Start")
            self.btn_play.setStyleSheet("padding: 8px; font-weight: bold;")
            self.btn_play.clicked.connect(self.play_stream)
            layout.addWidget(self.btn_play)

            self.setLayout(layout)


        def play_stream(self) -> None:
            """ 
            Open the selected player by Terminal order
            """
            selected_id = self.btn_group.checkedId()

            # Chose default player
            if selected_id == 99:
                success = QDesktopServices.openUrl(QUrl(self.stream_url))
                if not success:
                    QMessageBox.warning(self, "Warning", "Cannot open the default OS player.")

            # Chose selected player
            elif selected_id >= 0:
                _, cmd = self.players_list[selected_id]
                full_command = cmd + [self.stream_url]
                try:
                    subprocess.Popen(full_command)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Cannot open the selected player:\n{e}")