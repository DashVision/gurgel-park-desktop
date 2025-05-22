import os
import sys

def configure_os():
    """Configura o backend gráfico de acordo com o sistema operacional"""
    if sys.platform.startswith("linux"):
        desktop_session = os.environ.get("XDG_SESSION_TYPE", "").lower()

        if desktop_session == "wayland":
            print("Wayland detectado. Configurando para Wayland...")
            os.environ["QT_QPA_PLATFORM"] = "xcb"

        else:
            print("X11 detectado ou sessão desconhecida. Configurando para X11...")
            os.environ["QT_QPA_PLATFORM"] = "xcb"

    elif sys.platform == "win32":
        print("Windows detectado. Nenhuma configuração adicional necessária.")

    elif sys.platform == "darwin":
        print("macOS detectado. Nenhuma configuração adicional necessária.")