import os
import sys
from PyQt5.QtWidgets import QApplication
from core.application_initializer import initialize_application

def main():
    # Detecta o sistema operacional e configura o backend gráfico
    if sys.platform.startswith("linux"):
        desktop_session = os.environ.get("XDG_SESSION_TYPE", "").lower()

        if desktop_session == "wayland":
            print("Wayland detectado. Configurando para Wayland...")
            os.environ["QT_QPA_PLATFORM"] = "xcb" # Força o uso do X11 pode alterar para "wayland" se necessário
            
        else:
            print("X11 detectado ou sessão desconhecida. Configurando para X11...")
            os.environ["QT_QPA_PLATFORM"] = "xcb"

    elif sys.platform == "win32":
        print("Windows detectado. Nenhuma configuração adicional necessária.")

    elif sys.platform == "darwin":
        print("macOS detectado. Nenhuma configuração adicional necessária.")

    # Inicializa o aplicativo PyQt5
    app = QApplication(sys.argv)
    screens_controller = initialize_application()
    screens_controller.set_screen("login")
    screens_controller.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()