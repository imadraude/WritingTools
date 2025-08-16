import logging
import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtNetwork import QLocalServer, QLocalSocket

from WritingToolApp import WritingToolApp

# Set up logging to console
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    The main entry point of the application.
    """
    # Unique key for the application
    app_key = "WritingTools_App_Instance"

    # Check if another instance is running
    socket = QLocalSocket()
    socket.connectToServer(app_key)

    if socket.waitForConnected(500):
        # Another instance is running, so we exit
        logging.info("Another instance of Writing Tools is already running.")
        sys.exit(0)

    # Create a local server to prevent further instances
    local_server = QLocalServer()
    # Clean up the socket file if it exists
    QLocalServer.removeServer(app_key)
    local_server.listen(app_key)

    # Set the application name
    QCoreApplication.setApplicationName("WritingTools")

    app = WritingToolApp(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # Clean up the server when the application quits
    app.aboutToQuit.connect(local_server.close)

    sys.exit(app.exec())


if __name__ == '__main__':
    main()