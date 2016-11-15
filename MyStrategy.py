from model.ActionType import ActionType
from model.Game import Game
from model.Move import Move
from model.Wizard import Wizard
from model.World import World


class MyStrategy:

    first_run = True
    ally_wizards = list()
    enemy_wizards = list()

    def move(self, me: Wizard, world: World, game: Game, move: Move):

        self.find_nearby_units(me, world)
        move.speed = game.wizard_forward_speed
        move.strafe_speed = game.wizard_strafe_speed
        move.turn = me.get_angle_to_unit(self.ally_wizards[0])
        if me.get_distance_to_unit(self.ally_wizards[0]) < game.magic_missile_radius:
            move.action = ActionType.MAGIC_MISSILE

    def find_nearby_units(self, me: Wizard, world: World):

        temp_ally_wizards = list()
        temp_enemy_wizards = list()

        for wizard in world.wizards:
            if wizard.faction == me.faction and wizard is not me:
                temp_ally_wizards.append(wizard)
            elif wizard is not me:
                # why does this not find anything?!
                temp_enemy_wizards.append(wizard)
        self.ally_wizards = sorted(temp_ally_wizards, key=lambda w: w.get_distance_to_unit(me))
        self.enemy_wizards = sorted(temp_enemy_wizards, key=lambda w: w.get_distance_to_unit(me))
        print(temp_ally_wizards)
        print(temp_enemy_wizards)
