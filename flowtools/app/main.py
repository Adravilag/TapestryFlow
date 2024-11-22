from ttkbootstrap import Window
from app.views.dashboard import DashboardView
from app.logger_config import logger

def main():
    logger.info("Iniciando TapestryFlow...")
    root = Window(themename="darkly")
    DashboardView(root)
    root.mainloop()

if __name__ == "__main__":
    main()
