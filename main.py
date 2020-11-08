from arcBot import ArcBot


USERNAME = "XXXXXX"
PASSWORD = "******"


mybot = ArcBot(USERNAME, PASSWORD)
mybot.login_kerebos()
mybot.obtain_available_arc_sessions()
mybot.book_times()