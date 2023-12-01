from datetime import datetime

def swing_condition():
    current_second = datetime.now().second
    return current_second % 5 == 0