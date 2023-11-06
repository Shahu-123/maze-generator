import game
import login
import home
import welcome


play = welcome.show_welcome_page()
if play:
    login.init_db()
username = login.login_register_page()
active = True
while username and active:
    user_choice = home.home()
    active = game.game(user_choice, username)