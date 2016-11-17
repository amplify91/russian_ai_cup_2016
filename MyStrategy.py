from model.ActionType import ActionType
from model.Game import Game
from model.Move import Move
from model.Wizard import Wizard
from model.World import World
# from keras.models import Sequential
# from keras.layers import Dense
import numpy


class MyStrategy:

    # model = Sequential()
    # model.add(Dense(42))

    first_run = True
    ally_wizards = list()
    enemy_wizards = list()
    enemy_minions = list()

    def move(self, me: Wizard, world: World, game: Game, move: Move):

        self.find_nearby_units(me, world, game)

        if len(self.enemy_wizards) > 0:
            if me.get_distance_to_unit(self.enemy_wizards[0]) < game.magic_missile_radius:
                if me.life > me.max_life/2:
                    self.attack(me, game, move)
                else:
                    self.retreat(me, game, move)
            else:
                self.engage(me, game, move)
        elif len(self.enemy_minions) > 0:
            self.farm(me, game, move)
        else:
            self.follow(me, game, move)

    def find_nearby_units(self, me: Wizard, world: World, game: Game):

        # tl;dr Parse the state of all Units in the World
        # Populate structures representing each unit in the world to be used in different behaviors

        temp_ally_wizards = list()
        temp_enemy_wizards = list()
        temp_enemy_minions = list()

        for wizard in world.wizards:
            if wizard.faction == me.faction:
                # "is not me" does not work as expected
                temp_ally_wizards.append(wizard)
            elif wizard:
                temp_enemy_wizards.append(wizard)
        self.ally_wizards = sorted(temp_ally_wizards, key=lambda w: me.get_distance_to_unit(w))
        self.enemy_wizards = sorted(temp_enemy_wizards, key=lambda w: me.get_distance_to_unit(w))
        for minion in world.minions:
            if minion.faction is not me.faction and me.get_distance_to_unit(minion) < game.magic_missile_radius:
                temp_enemy_minions.append(minion)
        self.enemy_minions = sorted(temp_enemy_minions, key=lambda m: me.get_distance_to_unit(m))

    def retreat(self, me: Wizard, game: Game, move: Move):
        # pretty sure this works! Starts to break if no targets are nearby to run from
        threat_level_normalizer = 15
        threat_vector = [0, 0]
        for wizard in self.enemy_wizards:
            threat_level_coefficient = (wizard.level + threat_level_normalizer) / (me.level + threat_level_normalizer)
            threat_factor = threat_level_coefficient / (me.get_distance_to_unit(wizard) + 1) * wizard.cast_range
            angle = me.get_angle_to_unit(wizard)
            threat_vector[0] += threat_factor * numpy.cos(angle)
            threat_vector[1] += threat_factor * numpy.sin(angle)
        turn = numpy.deg2rad(numpy.arctan(threat_vector[1]/threat_vector[0]))
        # print(turn, threat_vector, threat_factor)
        move.turn = turn
        move.speed = game.wizard_forward_speed
        print("Move to retreat!")

    def follow(self, me: Wizard, game: Game, move: Move):
        if me.get_distance_to_unit(self.ally_wizards[1]) > me.radius *3:
            move.turn = me.get_angle_to_unit(self.ally_wizards[1])
            move.speed = game.wizard_forward_speed
            # print("Move to follow.")

    def attack(self, me: Wizard, game: Game, move: Move):
        if len(self.enemy_wizards) > 0 and me.get_distance_to_unit(self.enemy_wizards[0]) < game.magic_missile_radius:
            move.turn = me.get_angle_to_unit(self.enemy_wizards[0])
            if me.get_distance_to_unit(self.enemy_wizards[0]) > game.magic_missile_radius * 0.8:
                move.speed = game.wizard_forward_speed
                print("Move to attack.")
            move.action = ActionType.MAGIC_MISSILE
            print("Attack.")

    def farm(self, me: Wizard, game: Game, move: Move):
        if len(self.enemy_minions) > 0 and me.get_distance_to_unit(self.enemy_minions[0]) < game.magic_missile_radius:
            move.turn = me.get_angle_to_unit(self.enemy_minions[0])
            if me.get_distance_to_unit(self.enemy_minions[0]) > game.magic_missile_radius * 0.7:
                move.speed = game.wizard_forward_speed
                print("Move to farm.")
            move.action = ActionType.MAGIC_MISSILE
            print("Farm.")

    def engage(self, me: Wizard, game: Game, move: Move):
        if len(self.enemy_wizards) > 0 and me.get_distance_to_unit(self.enemy_wizards[0]) > game.magic_missile_radius:
            move.turn = me.get_angle_to_unit(self.enemy_wizards[0])
            move.speed = game.wizard_forward_speed
            print("Engage.")
