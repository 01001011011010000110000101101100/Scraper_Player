# Desktop media player from Internet
---
## Overview:
#### Desktop application based on `PySide6` (Qt for Python) scrap media information and stream URL from URL link. Built-in media player (`VLC`) play the stream video in the application and scan the other media player in the user device and let the decide to the user to chose the favorite media player and save the watch information in local database (`SQLite`).
---
## Feature:
- ### Asynchronous & Performance:
  
    Uses `httpx` and its feature `AsyncClient` for data, images, and network requests are fetched and executed in the background without freezing the user interface (UI). In addition, integration between `Qt` and `asyncio` via `qasync`: this integration ensures a smooth interface while performing heavy software requests.

    Communications management and load control via Network Manager reuse the client `AsyncClient` rather than use a new client with every request. Moreover, Concurrency Limit: a maximum number of simultaneous requests has been set to avoid blocked from websites. Overtime, Rate Limit & Retry Handle: automatically handles retry errors upon receiving a `429` (Too Many Requests) response.
- ### Architecture & Scalability:

    Object-oriented design supported by Pattern Rules (`BaswParser`/Abstract Base Class), which means the possibility to add a new website easily by create a class inherits from `BaswParser` and to `WebsitesRegistry` regardless of the rest of rest of system.

  Rigorous data modeling uses `dataclasses` automated with `slots` to save memory and define a clear data structure (`IconModel`, `PageDetailsModel`, and `EpisodeModel`).
- ### Interface & User Experience (UI/UX):

    Modern interface with an elegant design (`PySide6` / `Qt6`): a lightweight and responsive graphical interface with options for browsing, searching, and displaying details in nested pages (`QStackedWidget`). In addition, Lazy/Async Image Loading: the cards are created first, then the posters and images are loaded accurately and discreetly to ensure a fast response to the interface.

    Operating external and built-in drivers: automatic recognition of video players installed in the operating system (such as `MPV`, `VLC`, `Celluloid`, `PotPlayer`, `IINA`).
- ### Robustness & Error Handling:

    Type Checking & Validation: checking transaction types such as `httpx.URL` and avoiding errors during operation. Moreover, Comprehensive Logging: logging details and operational exceptions in the app.log file facilitates problem tracking and resolution.
---
## Structure:
```plaintext
Scraper_Player/
├── docs/
│   ├── assets/
│   │   └── screen.png
│   └── ARCHITECTURE.md
│
├── graphic/
│   └── frontend.py
│
├── assets/
|   └── icons/
│       ├── home_btn_icon.svg
│       ├── menu_btn_icon.svg
│       └── search_btn_icon.svg
│
├── internet/
│   ├── internet_handle.py
│   ├── scraper.py
│   └── websites.py
│
├── regulator/
│   ├── config.py
│   └── models.py
│
├── user_interface_py/
│   ├── ui_card.py
│   └── ui_main.py
│
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── requirements.txt
├── app.log
└── app.py
```
---
## Prerequisites & Dependencies:
**Make sure you have Python 3.8+ installed. The project relies on the following major packages:**

* `pyside6`-the official Python module for the Qt 6 cross-platform application and UI framework.

* `httpx`-modern Python HTTP client library support asynchronous I/O requests. 

* `qasync`-Python library that allows you to use `asyncio` coroutines directly inside Qt-based desktop applications.

* `beautifulsoup4`-Python library to parser HTML and XML documents, primarily to extract data for web scraping.

* `lxml`-Python library to parser HTML and XML documents. However, in this project it used to parser HTML tree with Beautiful Soup due to its speed.

---
## Getting Started:
1. **Clone or Download the Repository:**
```bash
git clone "https://github.com/01001011011010000110000101101100/Scraper_Player"
cd "Scraper_Player"
```
2. **Create and activate virtual environment (Prefers):**
```bash
python -m venv .venv
source /.venv/bin/activate
```
3. **Install all packages from `requirements.txt` via `pip`:**
```bash
pip install -r "requirements.txt"
```
4. **Run the program:**
```bash
python app.py
```
---
## An overview of the graphical interface:
![Cannot found the image](/docs/assets/screen.png)