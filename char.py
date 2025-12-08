import pygame
import keyboard
from pygame.time import Clock
import pathlib
import time


class timer:
    def __init__(self):
        self.timestamp_s = time.time()

    def set_timer(self, time_s):
        self.timestamp_s = time.time() + time_s

    def get_remaining_time_s(self):
        difference_s = self.timestamp_s - time.time()
        if difference_s < 0:
            difference_s = 0   
        return difference_s
    
    def is_timer_done(self):
        if self.get_remaining_time_s() == 0:
            return True
        else:
            return False
    

class Character:
    def __init__(self, list_of_paths_to_standing_images:list, list_of_paths_to_jumping_images:list, list_of_paths_to_walking_images:list, position_x:int, position_y:int):
        cleared_standing_path_list = self.__delete_unvalid_paths_from_path_list(list_of_paths_to_standing_images)
        self.list_of_standing_images = self.__get_image_list_of_path_list(cleared_standing_path_list)

        cleared_jumping_path_list = self.__delete_unvalid_paths_from_path_list(list_of_paths_to_jumping_images)
        self.list_of_jumping_images = self.__get_image_list_of_path_list(cleared_jumping_path_list)

        cleared_walking_path_list = self.__delete_unvalid_paths_from_path_list(list_of_paths_to_walking_images)
        self.list_of_walking_images = self.__get_image_list_of_path_list(cleared_walking_path_list)

        self.current_walk_picture = 0
        self.current_standing_image = 0
        self.picture_change_distance_px = 7
        self.walked_distance = 0

        self.position_x = position_x
        self.position_y = position_y

        self.time_between_steps_s = 0.1
        self.timer = timer()


    def __delete_unvalid_paths_from_path_list(self, path_list:list) -> list:
        for path in path_list:
            if not pathlib.Path(path).exists():
                print(f"__delete_unvalid_paths_from_path_list: deleted {path}")
                path_list.remove(path)
        return path_list


    def __get_image_list_of_path_list(self, path_list:list) -> list:
        image_list = list()
        for path in path_list:
            image = pygame.image.load(path).convert()
            image.set_colorkey((255,255,255))
            image_list.append(image)
        return image_list
    

    def __get_next_walking_image(self) -> int:
        next_index = self.current_walk_picture + 1
        if next_index >= len(self.list_of_walking_images):
            next_index = 0
        return next_index
    

    def __get_previous_walking_image(self) -> int:
        previous_index = self.current_walk_picture - 1
        if previous_index < 0:
            previous_index = len(self.list_of_walking_images) - 1
        return previous_index
    
    def __get_next_standing_image(self) -> int:
        next_index = self.current_standing_image + 1
        if next_index >= len(self.list_of_standing_images):
            next_index = 0
        return next_index


    def get_character(self, go_right:bool, go_left:bool, distance:int):
        if self.__is_walking(go_right, go_left, distance):
            if go_right:
                self.walked_distance += distance
            else:
                self.walked_distance -= distance

            if self.walked_distance >= 7:
                self.walked_distance -= 7
                self.position_x += 7
                self.current_walk_picture = self.__get_next_walking_image()
            elif self.walked_distance <= -7:
                self.walked_distance += 7
                self.position_x -= 7
                self.current_walk_picture = self.__get_previous_walking_image()

            return self.list_of_walking_images[self.current_walk_picture]

        elif self.__is_standing(go_right, go_left, distance):
            if self.timer.is_timer_done():
                self.timer.set_timer(0.2)
                self.current_standing_image = self.__get_next_standing_image()

            return self.list_of_standing_images[self.current_standing_image]
        

    def __is_walking(self, go_right:bool, go_left:bool, distance:int) -> bool:
        if (go_left ^ go_right) and (distance != 0):
            is_walking = True
        else:
            is_walking = False
        return is_walking    

    def __is_standing(self, go_right:bool, go_left:bool, distance:int) -> bool:
        return not self.__is_walking(go_right, go_left, distance)


    def get_position(self):
        return self.position_x, self.position_y
    