import pygame
import keyboard
from pygame.time import Clock
from char import Character, timer
import os, pathlib

def is_right():
    return keyboard.is_pressed('d')

def is_left():
    return keyboard.is_pressed('a')

def get_list_of_paths_of_directory(directory_path:pathlib.WindowsPath) -> list:
    list_of_elements = os.listdir(directory_path)
    for index in range(len(list_of_elements)):
        list_of_elements[index] = pathlib.Path(directory_path, list_of_elements[index])
    return list_of_elements

def main():

    pygame.init()
    clock = pygame.time.Clock()

    time = 0.1
    rotation = 0

    screen = pygame.display.set_mode((640, 640))

    # circle_img = pygame.image.load("circle.png").convert()
    # circle_settings = circle_img.get_rect(x,30)

    running = True
    # x = 0

    standing_directory = pathlib.Path("C:/Users/julia/OneDrive/Desktop/VS Code/game/Images/standing/")
    jump_directory = pathlib.Path("C:/Users/julia/OneDrive/Desktop/VS Code/game/Images/jump/")
    walk_directory = pathlib.Path("C:/Users/julia/OneDrive/Desktop/VS Code/game/Images/walk/")

    list_of_paths_to_standing_images = get_list_of_paths_of_directory(standing_directory)
    list_of_paths_to_jump_images = get_list_of_paths_of_directory(jump_directory)
    list_of_paths_to_walk_images = get_list_of_paths_of_directory(walk_directory)

    main_character = Character(list_of_paths_to_standing_images,
                               list_of_paths_to_jump_images,
                               list_of_paths_to_walk_images,
                               320, 320)
    
    platform = pygame.image.load("C:/Users/julia/OneDrive/Desktop/VS Code/game/Images/Platform.png").convert()
    platform.set_colorkey((255,255,255))
    
    fps_timer = timer()
    fps_counter_timer = timer()
    calls_per_second = 0

    while running:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                running = False

        if fps_timer.is_timer_done():
            fps_timer.set_timer(1/60)
            calls_per_second += 1

            screen.fill((0,255,0))

            # pos = pygame.mouse.get_pos()
            screen.blit(platform, (180, 375))
            screen.blit(main_character.get_character(is_right(), is_left(), 1), main_character.get_position())

            pygame.display.flip()



            if fps_counter_timer.is_timer_done():
                fps_counter_timer.set_timer(1)
                print(calls_per_second)
                calls_per_second = 0
        # time = clock.tick(60) / 1000



    pygame.quit()


if __name__ == "__main__":
    main()