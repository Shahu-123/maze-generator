import game
import login
import settings
import welcome
import home

class WindowController:
    def __init__(self):
        self.username = None
        self.settings = None
        self.windows = {
            'welcome': welcome.show_welcome_page,
            'login': login.login_register_page,
            'home': home.home,
            'settings': settings.home,
            'game': lambda: game.game(self.settings, self.username)
        }

    def show_window(self, name):
        if name == "login":
            self.username = self.windows[name]()
            return self.show_window('home')

        elif name == "welcome":
            self.windows[name]()
            return self.show_window('login')

        elif name == "settings":
            self.settings = self.windows[name]()
            return self.show_window("game")

        elif name == "home":
            choice = self.windows[name]()
            if choice == "setup":
                return self.show_window('settings')
            elif choice == "local":
                pass
            elif choice == "global":
                pass
            elif choice == "log out":
                self.username = None
                self.settings = None
                return self.show_window('login')

        elif name == "game":
            return_home = self.windows[name]()
            if return_home:
                return self.show_window('home')
            else:
                return self.show_window('welcome')
        else:
            return self.windows[name]()


x = WindowController()
x.show_window('login')