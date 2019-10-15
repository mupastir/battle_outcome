import random


class BaseUnit:

    def __init__(self, recharge):
        self.health = 100
        self.recharge = recharge


class Soldier(BaseUnit):

    def __init__(self, recharge):
        super(Soldier, self).__init__(recharge)
        self.experience = 0

    def up_experience(self, func):
        def decorated(*args):
            func(*args)
            self.experience += 1
            return

        return decorated

    def attack(self):
        return 0.5 * (1 + self.health / 100) * random.randint(
            50 + self.experience, 100) / 100

    def damage(self):
        return 0.05 + self.experience / 100


class Vehicle(BaseUnit):

    def __init__(self, recharge, *operators):
        super(Vehicle, self).__init__(recharge)
        self.operators = operators
