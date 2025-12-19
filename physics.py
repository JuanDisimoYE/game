import math
import pygame
from char import timer
import os, pathlib
import copy


class circle:
    def __init__(self, path, x, y):
        self.image = pygame.image.load(path).convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.center = [x, y]
        self.center_buffer = [x, y]
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
        self.prev_center   = copy.deepcopy(list(self.center_buffer))
        self.center_buffer = copy.deepcopy(list(self.center))
        self.center        = copy.deepcopy(list(center))

    def get_direction_angle(self) -> float:
        ankathete = self.center[1] - self.prev_center[1]
        gegenkathete = self.prev_center[0] - self.center[0]
        return arctan(ankathete, gegenkathete)

    def get_center(self) -> tuple[int, int]:
        return copy.deepcopy(self.center)
    
    def get_prev_center(self) -> tuple[int, int]:
        return copy.deepcopy(self.prev_center)


    def get_default_position(self):
        return (self.center[0]-(self.image.get_size()[0]*0.5), self.center[1]-(self.image.get_size()[1]*0.5))
    


def set_offset(overlap, offset):
    return (overlap[0]+offset[0], overlap[1]+offset[1])

def get_normal_angle(center:tuple, overlap:tuple):
    gegenkathete = center[0] - overlap[0]
    ankathete = overlap[1] - center[1]
    return arctan(ankathete, gegenkathete)

def get_normal_vektor(angle:float, length) -> list:
    return [length*math.sin(angle), length*math.sin(angle)]

def arctan(ankathete, gegenkathete):
    if ankathete == 0:
        angle = math.pi/2
    else:
        angle = math.atan(gegenkathete / ankathete)
    return angle


def get_speed(speed:list[int,int]):
    return math.sqrt( (speed[0]*speed[0]) + (speed[1]*speed[1]) )

def get_distance(point_1:list[int,int], point_2:list[int,int]):
    return math.sqrt( ( (point_1[0]-point_2[0])**2 ) + (point_1[1]-point_2[1])**2 )

def get_dot_product(vektor_1:list[int,int], vektor_2:list[int,int]) -> float:
    return (vektor_1[0]*vektor_2[0]) + (vektor_1[1]*vektor_2[1])

def is_direction_field_equal(angle_1, angle_2) -> bool:
    if (angle_2 < (angle_1+math.pi/2)) and (angle_2 > (angle_1-math.pi/2)):
        same_direction_field = True
    else:
        same_direction_field = False
    return same_direction_field



def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 800))

    circle_big = circle(pathlib.Path(f"{os.getcwd()}/Images/physics/Physics_big_circle.png"), 300, 300)
    circle_small = circle(pathlib.Path(f"{os.getcwd()}/Images/physics/Physics_small_circle.png"), pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    pixel = pygame.Surface((5,5))
    pixel.fill((0,255,0))

    fps_timer = timer()
    running = True

    print(circle_small.get_size())
    overlap_ = False
    prev = 0

    start_position = None
    speed = [0,0]

    _overlap = None

    frames_per_second = 60

    world_c = [0,0]

    _overlap_surf = None
    _offset_ = None
    _pixel = None
    _world_c = None

    pi = 3.141

    while running:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                running = False

        if fps_timer.is_timer_done():
            fps_timer.set_timer(1/frames_per_second)

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
                    speed = [0,0]

                acceleration = 100
                dt = 1/frames_per_second

                    
                position = circle_small.get_center()
                speed[1] = speed[1] + acceleration*dt
                position[1] = position[1] + speed[1]*dt
                position[0] = position[0] + speed[0]*dt

                circle_small.set_center(position)

                overlap = circle_small.is_overlap(circle_big.get_mask(), circle_big.get_default_position())

                if overlap:
                    offset = (-circle_small.get_center()[0]+300, -circle_small.get_center()[1]+300)
                    offset_= ( circle_small.get_center()[0]-300,  circle_small.get_center()[1]-300)
                    overlap_mask = circle_small.get_mask().overlap_mask(circle_big.get_mask(), offset)
                    if overlap_mask.count() > 0:
                        center = overlap_mask.centroid()   # Schwerpunkt in lokalen Koordinaten der overlap_mask
                        world_c[0] = circle_small.get_center()[0] + center[0] - 300                 # in Welt-/Screen-Koordinaten umrechnen
                        world_c[1] = circle_small.get_center()[1] + center[1] - 300
                        overlap_surf = overlap_mask.to_surface(setcolor=(255, 0, 0, 255), unsetcolor=(0, 0, 0, 0))
                        # screen.blit(overlap_surf, offset_)

                    _overlap = set_offset(overlap, circle_small.get_default_position())
                    normal_angle = get_normal_angle(circle_small.get_center(), world_c)
                    print(f"na: {normal_angle*57.3}")
                    print(f"{_overlap}/{world_c}")

                    # normal_angle = math.atan((circle_small.get_center()[0]-_overlap[0])/(_overlap[1]-circle_small.get_center()[1]))# + (math.pi()/2)
                    speed_0 = get_speed(speed)
                    normal_vektor = get_normal_vektor(normal_angle, speed_0)
                    print(f"dp: {get_dot_product(speed, normal_vektor)}")

                    comming_in_angle = circle_small.get_direction_angle()
                    print(f"df: {is_direction_field_equal((normal_angle+math.pi), comming_in_angle)}")
                    if not is_direction_field_equal((normal_angle+math.pi), comming_in_angle):

                        angle_difference = normal_angle - comming_in_angle

                        outgoing_angle = normal_angle + angle_difference

                        print(f"{comming_in_angle*57.3}/{normal_angle*57.3}/{outgoing_angle*57.3}")
                        
                        speed[0] =   speed_0 * math.sin(outgoing_angle)
                        speed[1] = - speed_0 * math.cos(outgoing_angle)
                


                screen.blit(circle_small.get_image(), circle_small.get_default_position())

                # if _overlap and not _overlap_surf: 
                #     _overlap_surf = overlap_surf
                #     _offset_ = offset_
                #     _pixel = pixel
                #     _world_c = world_c

                if _overlap: 
                    screen.blit(overlap_surf, offset_)
                    screen.blit(pixel, world_c)

            pygame.display.flip()





    pygame.quit()


if __name__ == "__main__":
    main()