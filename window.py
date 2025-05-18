import game_component as gc

def custom_process_window():
    process_creator = gc.ProcessCreator()
    process_creator.run()

def process_window_with_difficulty(difficulty):
    process_creator = gc.ProcessClass()
    process_creator.set_difficulty(difficulty)
    process_creator.run()

def process_windows_with_custom(data):
    process_creator = gc.ProcessClass()
    process_creator.set_custom(True,data)
    process_creator.run()

def main_window():
    game = gc.SchedulingMaster()
    game.run()

if __name__ == "__main__":
    main_window()