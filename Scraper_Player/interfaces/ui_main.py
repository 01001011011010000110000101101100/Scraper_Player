# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QStackedWidget, QStatusBar,
    QVBoxLayout, QWidget)

import os
ICON_DIR = os.path.dirname(os.path.abspath("__main__"))
def put_path(file_name: str) -> str:
    assest_dir = os.path.join(ICON_DIR, "assets")
    icon_dir = os.path.join(assest_dir, "icons")
    print(os.path.join(icon_dir, file_name))
    print(type(os.path.join(icon_dir, file_name)))

    return os.path.join(icon_dir, file_name)

class Ui_MzAnime(object):
    def setupUi(self, MzAnime):
        if not MzAnime.objectName():
            MzAnime.setObjectName(u"MzAnime")
        MzAnime.setWindowModality(Qt.WindowModality.ApplicationModal)
        MzAnime.resize(798, 688)
        MzAnime.setMaximumSize(QSize(1920, 1080))
        MzAnime.setStyleSheet(u"background-color: #060614;\n"
"color: #ffffff;\n"
"border-radius: 16px;\n"
"border: 1px solid #374151;\n"
"\n"
"\n"
"QPushButton {\n"
"    border-radius: 16px; /* \u062d\u0648\u0627\u0641 \u062f\u0627\u0626\u0631\u064a\u0629 \u0623\u0646\u064a\u0642\u0629 */\n"
"	border: 1px solid #374151;\n"
"	padding: 8px 16px; /* \u0644\u0625\u0639\u0637\u0627\u0621 \u0645\u0633\u0627\u062d\u0629 \u062f\u0627\u062e\u0644\u064a\u0629 \u062c\u0645\u064a\u0644\u0629 */\n"
"}\n"
"\n"
"")
        MzAnime.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QWidget(MzAnime)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMaximumSize(QSize(1920, 1080))
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.full_stacked = QStackedWidget(self.centralwidget)
        self.full_stacked.setObjectName(u"full_stacked")
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.verticalLayout_5 = QVBoxLayout(self.page_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.upper_widget = QWidget(self.page_3)
        self.upper_widget.setObjectName(u"upper_widget")
        self.horizontalLayout = QHBoxLayout(self.upper_widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.upper_layout = QHBoxLayout()
        self.upper_layout.setObjectName(u"upper_layout")
        self.menu_btn = QPushButton(self.upper_widget)
        self.menu_btn.setObjectName(u"menu_btn")
        self.menu_btn.setStyleSheet(u"background-color: rgb(119, 118, 123);")
        icon = QIcon()
        icon.addFile(put_path(u"menu_btn_icon.svg"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu_btn.setIcon(icon)
        self.menu_btn.setIconSize(QSize(45, 45))

        self.upper_layout.addWidget(self.menu_btn)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.upper_layout.addItem(self.horizontalSpacer_2)

        self.home_btn = QPushButton(self.upper_widget)
        self.home_btn.setObjectName(u"home_btn")
        self.home_btn.setMinimumSize(QSize(55, 55))
        self.home_btn.setStyleSheet(u"background-color: rgb(119, 118, 123);")
        icon1 = QIcon()
        icon1.addFile(put_path(u"home_btn_icon.svg"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.home_btn.setIcon(icon1)
        self.home_btn.setIconSize(QSize(45, 45))

        self.upper_layout.addWidget(self.home_btn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.upper_layout.addItem(self.horizontalSpacer)

        self.search_filed = QLineEdit(self.upper_widget)
        self.search_filed.setObjectName(u"search_filed")
        self.search_filed.setMinimumSize(QSize(0, 20))

        self.upper_layout.addWidget(self.search_filed)

        self.search_btn = QPushButton(self.upper_widget)
        self.search_btn.setObjectName(u"search_btn")
        self.search_btn.setMinimumSize(QSize(40, 40))
        self.search_btn.setStyleSheet(u"background-color: rgb(119, 118, 123);")
        icon2 = QIcon()
        icon2.addFile(put_path(u"search_btn_icon.svg"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.search_btn.setIcon(icon2)
        self.search_btn.setIconSize(QSize(30, 30))

        self.upper_layout.addWidget(self.search_btn)


        self.horizontalLayout.addLayout(self.upper_layout)


        self.verticalLayout_5.addWidget(self.upper_widget)

        self.lower_stacked = QStackedWidget(self.page_3)
        self.lower_stacked.setObjectName(u"lower_stacked")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_4 = QVBoxLayout(self.page)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.lower_QVlayout = QVBoxLayout()
        self.lower_QVlayout.setObjectName(u"lower_QVlayout")
        self.lowerArea = QScrollArea(self.page)
        self.lowerArea.setObjectName(u"lowerArea")
        self.lowerArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 734, 493))
        self.lower_layout = QGridLayout(self.scrollAreaWidgetContents)
        self.lower_layout.setObjectName(u"lower_layout")
        self.lowerArea.setWidget(self.scrollAreaWidgetContents)

        self.lower_QVlayout.addWidget(self.lowerArea)


        self.verticalLayout_4.addLayout(self.lower_QVlayout)

        self.lower_stacked.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.lower_stacked.addWidget(self.page_2)

        self.verticalLayout_5.addWidget(self.lower_stacked)

        self.full_stacked.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.full_stacked.addWidget(self.page_4)

        self.verticalLayout.addWidget(self.full_stacked)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        MzAnime.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MzAnime)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 798, 26))
        MzAnime.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MzAnime)
        self.statusbar.setObjectName(u"statusbar")
        MzAnime.setStatusBar(self.statusbar)

        self.retranslateUi(MzAnime)

        QMetaObject.connectSlotsByName(MzAnime)
    # setupUi

    def retranslateUi(self, MzAnime):
        MzAnime.setWindowTitle(QCoreApplication.translate("MzAnime", u"MainWindow", None))
        self.home_btn.setText("")
        self.search_btn.setText("")
    # retranslateUi

