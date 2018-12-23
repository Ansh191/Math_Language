import cProfile
pr = cProfile.Profile()
pr.enable()
from main import main

main("sqrt[5]")
pr.disable()
pr.dump_stats('profile.profile')