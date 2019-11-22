# FrontEnd Senders
class MovePlayerEvent:

    def __init__(self, key):
        if key == "Up":
            self.factor = 1
        else:
            self.factor = - 1


class RotatePlayerEvent:

    def __init__(self, key):
        if key == "Right":
            self.rotation = 10
        else:
            self.rotation = - 10
