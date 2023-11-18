import game
import login
import settings
import welcome
import home
import scores

class WindowController:
    def __init__(self):
        self.username = None
        self.settings = None
        self.leaderboard_level = None
        self.windows = {
            'welcome': welcome.show_welcome_page,
            'login': login.login_register_page,
            'home': home.home,
            'local_scores': lambda: scores.show_local_scores(self.username, self.leaderboard_level),
            'global_scores': lambda: scores.show_global_scores(self.leaderboard_level),
            'settings': settings.home,
            'game': lambda: game.game(self.settings, self.username)
        }

    def show_window(self, name):
        if name == "welcome":
            self.windows[name]()
            return self.show_window('login')

        elif name == "login":
            self.username = self.windows[name]()
            return self.show_window('home')

        elif name == "settings":
            self.settings = self.windows[name]()
            return self.show_window("game")

        elif name == "home":
            choice = self.windows[name]()
            if "setup" in choice:
                return self.show_window('settings')
            elif "local" in choice:
                self.leaderboard_level = choice[5:]
                return self.show_window('local_scores')
            elif "global" in choice:
                self.leaderboard_level = choice[6:]
                return self.show_window('global_scores')
            elif "log out" in choice:
                self.username = None
                self.settings = None
                return self.show_window('login')
        elif name == "local_scores":
            self.windows[name]()
            return self.show_window('home')
        elif name == "global_scores":
            self.windows[name]()
            return self.show_window('home')
        elif name == "game":
            return_home = self.windows[name]()
            if return_home:
                return self.show_window('home')
            else:
                return self.show_window('welcome')
        else:
            return self.windows[name]()


x = WindowController()
x.show_window('welcome')