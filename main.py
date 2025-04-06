from kivy.app import App
from controllers.screens_controller import ScreensController

class GurgelParkApp(App):
    def build(self):
        self.controller = ScreensController()
        return self.controller.get_root_widget()


if __name__ == '__main__':
    GurgelParkApp().run()