# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'card.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QScrollArea, QSizePolicy,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget)

class Ui_anime_card_widget(object):
    def setupUi(self, anime_card_widget):
        if not anime_card_widget.objectName():
            anime_card_widget.setObjectName(u"anime_card_widget")
        anime_card_widget.resize(856, 732)
        anime_card_widget.setStyleSheet(u"background-color: #60060614;\n"
"color: #ffffff;\n"
"border-radius: 16px;\n"
"border: 1px solid #374151;")
        self.verticalLayout_2 = QVBoxLayout(anime_card_widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.card_stacked = QStackedWidget(anime_card_widget)
        self.card_stacked.setObjectName(u"card_stacked")
        self.card_page = QWidget()
        self.card_page.setObjectName(u"card_page")
        self.verticalLayout_3 = QVBoxLayout(self.card_page)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scrollArea = QScrollArea(self.card_page)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        # self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollWidget = QWidget()
        self.scrollWidget.setObjectName(u"scrollWidget")
        self.scrollWidget.setGeometry(QRect(0, 0, 802, 801))
        self.verticalLayout_4 = QVBoxLayout(self.scrollWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.details_layout = QVBoxLayout()
        self.details_layout.setObjectName(u"details_layout")
        self.icon_label = QLabel(self.scrollWidget)
        self.icon_label.setObjectName(u"icon_label")
        self.icon_label.setMinimumSize(QSize(400, 566))
        self.icon_label.setMaximumSize(QSize(400, 566))

        self.details_layout.addWidget(self.icon_label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.title_label = QLabel(self.scrollWidget)
        self.title_label.setObjectName(u"title_label")

        self.details_layout.addWidget(self.title_label)

        self.status_label = QLabel(self.scrollWidget)
        self.status_label.setObjectName(u"status_label")

        self.details_layout.addWidget(self.status_label)
        self.status_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.episodesContainer = QWidget(self.scrollWidget)
        self.episodesContainer.setObjectName(u"episodesContainer")
        self.verticalLayout_6 = QVBoxLayout(self.episodesContainer)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.episodes_layout = QVBoxLayout()
        self.episodes_layout.setObjectName(u"episodes_layout")

        self.verticalLayout_6.addLayout(self.episodes_layout)


        self.details_layout.addWidget(self.episodesContainer)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.details_layout.addItem(self.verticalSpacer)


        self.verticalLayout_4.addLayout(self.details_layout)

        self.scrollArea.setWidget(self.scrollWidget)

        self.verticalLayout_3.addWidget(self.scrollArea)

        self.card_stacked.addWidget(self.card_page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.card_stacked.addWidget(self.page_2)

        self.verticalLayout_2.addWidget(self.card_stacked)


        self.retranslateUi(anime_card_widget)

        QMetaObject.connectSlotsByName(anime_card_widget)
    # setupUi

    def retranslateUi(self, anime_card_widget):
        anime_card_widget.setWindowTitle(QCoreApplication.translate("anime_card_widget", u"Form", None))
        self.icon_label.setText("")
        self.title_label.setText("")
    # retranslateUi

