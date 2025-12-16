import math
import pygame
from char import timer
import os, pathlib


class circle:
    def __init__(self, path, x, y):
        self.image = pygame.image.load(path).convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.center = [x, y]
        self.prev_center = [x, y]

    def get_size(self) -> tuple[int, int]:
        return self.image.get_size()
    
    def get_image(self):
        return self.image
    
    def get_mask(self):
        return pygame.mask.from_surface(self.image)
    
    def is_overlap(self, mask, default_position):
        return self.get_mask().overlap(mask, self.__get_difference(default_position))
    
    def __get_difference(self, default_position:tuple):
        return (default_position[0] - self.get_default_position()[0], default_position[1] - self.get_default_position()[1])
    
    def set_center(self, center:tuple) -> None:
        self.prev_center = self.center
        self.center = [center[0], center[1]]

    def get_direction_angle(self) -> int:
        return arctan(self.center[0]-self.prev_center[0], self.center[1]-self.prev_center[1])

    def get_center(self) -> tuple[int, int]:
        return self.center
    
    def get_prev_center(self) -> tuple[int, int]:
        return self.prev_center


    def get_default_position(self):
        return (self.center[0]-(self.image.get_size()[0]*0.5), self.center[1]-(self.image.get_size()[1]*0.5))
    


def set_offset(overlap, offset):
    return (overlap[0]+offset[0], overlap[1]+offset[1])

def get_normal_angle(center:tuple[int, int], overlap:tuple[int, int]) -> int:
    gegenkathete = overlap[0] - center[0]
    ankathete = center[1] - overlap[1]
    
    return arctan(ankathete, gegenkathete)

def arctan(ankathete:int, gegenkathete:int) -> int:
    if ankathete == 0:
        angle = math.pi/2
    else:
        angle = math.atan(gegenkathete / ankathete)
    return angle

def get_speed(speed:list[int,int]):
    return math.sqrt( (speed[0]*speed[0]) + (speed[1]*speed[1]) )


def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 800))

    circle_big = circle(pathlib.Path(f"{os.getcwd()}/Images/physics/Physics_big_circle.png"), 300, 300)
    circle_small = circle(pathlib.Path(f"{os.getcwd()}/Images/physics/Physics_small_circle.png"), pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    pixel = pygame.Surface((10,10))
    pixel.fill((255,0,0))

    fps_timer = timer()
    running = True

    print(circle_small.get_size())
    overlap_ = False

    start_position = None
    speed = [0,0]
    tmp_cooldown = False

    _overlap = None

    while running:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                running = False

        if fps_timer.is_timer_done():
            fps_timer.set_timer(1/60)

            screen.fill((0,255,0))
            screen.blit(circle_big.get_image(), (0, 0))

            if start_position == None:
                circle_small.set_center(pygame.mouse.get_pos())

                screen.blit(circle_small.get_image(), circle_small.get_default_position())

                overlap = circle_small.is_overlap(circle_big.get_mask(), circle_big.get_default_position())

                if overlap_ != overlap:
                    overlap_ = overlap

                if pygame.mouse.get_pressed()[0]:
                    start_position = pygame.mouse.get_pos()
                    circle_small.set_center(pygame.mouse.get_pos())

            else:

                if pygame.mouse.get_pressed()[0]:
                    start_position = pygame.mouse.get_pos()
                    circle_small.set_center(pygame.mouse.get_pos())

                acceleration = 10
                dt = 1/60

                position = circle_small.get_center()
                speed[1] += acceleration*dt
                position[1] += speed[1]*dt
                position[0] += speed[0]

                print(f"{speed[0]}/{speed[1]}")

                circle_small.set_center(position)

                overlap = circle_small.is_overlap(circle_big.get_mask(), circle_big.get_default_position())
                if overlap and not tmp_cooldown:
                    # print(overlap)
                    _overlap = set_offset(overlap, circle_small.get_default_position())
                    normal_angle = get_normal_angle(circle_small.get_center(), _overlap)
                    # an = circle_small.get_prev_center()[0] - circle_small.get_center()[0]
                    # gegen = circle_small.get_center()[1] - circle_small.get_prev_center()[1]
                    # normal_angle = arctan(an, gegen)

                    comming_in_angle = circle_small.get_direction_angle()

                    angle_difference = comming_in_angle - normal_angle

                    outgoing_angle = comming_in_angle - 2*angle_difference

                    speed_0 = get_speed(speed)
                    print(f"Vx, Vy, V: {speed[0]}, {speed[1]} {speed_0}")
                    speed[0] = - speed_0 * math.cos(outgoing_angle)
                    speed[1] = - speed_0 * math.sin(outgoing_angle)

                    tmp_cooldown = True
                    
                    # print(normal_angle *57.3)
                    print(f"comming[normal]going: {comming_in_angle*57.3}[{normal_angle*57.3}]{outgoing_angle*57.3}")
                else:
                    tmp_cooldown = False
                


                screen.blit(circle_small.get_image(), circle_small.get_default_position())
                if _overlap:
                    screen.blit(pixel, _overlap)

            pygame.display.flip()





    pygame.quit()


if __name__ == "__main__":
    main()