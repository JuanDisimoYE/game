import math
import pygame
from char import timer
import os, pathlib
import copy
from vector import vector, add_vector, get_angle_of_vector
from coordinate_system import coordinate_system



class physical_object:
    def __init__(self, mask, mass, center_position: tuple[int,int] = (0, 0), speed:vector = (0,0), stiff:bool = True):
        self.mask = copy.deepcopy(mask)
        self.stiff = copy.deepcopy(stiff)
        self.mass = copy.deepcopy(mass)
        self.center_position = copy.deepcopy(center_position)
        self.previous_center_position = copy.deepcopy(center_position)
        self.default_position = self.__center_to_default(center_position)
        self.speed = copy.deepcopy(speed)

        self.collision_impulse = vector(0, 0)

    def __center_to_default(self, center_position:list) -> list:
        return [center_position[0] - self.mask.centroid()[0], center_position[1] - self.mask.centroid()[1]]
    
    def __default_to_center(self, default_position:list) -> list:
        return [default_position[0] + self.mask.centroid()[0], default_position[1] + self.mask.centroid()[1]]

    def set_center_position(self, center_position:list) -> None:
        self.center_position = center_position
        self.default_position = self.__center_to_default(center_position)

    def set_default_position(self, default_position:list) -> None:
        self.default_position = default_position
        self.center_position = self.__default_to_center(default_position)

    def set_mask(self, mask) -> None:
        self.mask = mask

    def get_center_position(self) -> list:
        return copy.deepcopy(self.center_position)
    
    def get_default_position(self) -> list:
        return copy.deepcopy(self.default_position)
    
    def __refresh_speed(self):
        self.speed.set_direction(get_angle_of_vector(self.previous_center_position, self.center_position))
    
    def get_speed(self):
        self.__refresh_speed()
        return copy.deepcopy(self.speed)
    
    def get_impulse(self):
        speed = self.get_speed()
        speed.set_length(speed.get_length()*self.get_mass())
        return speed
    
    def get_mass(self):
        return copy.deepcopy(self.mass)
    
    def get_default_position_difference(self, default_position:tuple):
        return (default_position[0] - self.get_default_position()[0], default_position[1] - self.get_default_position()[1])

        

class physical_system:
    def __init__(self, *list_of_physical_objects:physical_object):
        self.list_of_physical_objects = list(list_of_physical_objects)

    def add_physical_object(self, physical_object:physical_object):
        self.list_of_physical_objects.append(physical_object)

    def remove_physical_object(self, physical_object:physical_object):
        self.list_of_physical_objects.remove(physical_object)

    def physical_system_cyclic(self):
        for physical_object in self.list_of_physical_objects:
            self.__check_collisions_of_physical_object(physical_object)

        for physical_object in self.list_of_physical_objects:
            self.__run_physical_step(physical_object)

        return
    

    def __run_physical_step(self, physical_object:physical_object) -> None:
        resulting_impulse = add_vector(physical_object.get_impulse(), physical_object.collision_impulse)
        new_speed = resulting_impulse.get_length()/physical_object.get_mass()
        physical_object.speed.set_length(new_speed)
        physical_object.speed.set_direction(resulting_impulse.get_direction())




        return
    
    def __check_collisions_of_physical_object(self, physical_object:physical_object) -> None:
        if not physical_object.stiff:

            for collision_object in self.list_of_physical_objects:
                if collision_object == physical_object:
                    continue

                collision_center = self.__get_collision_center(physical_object, collision_object)
                if collision_center:
                    normal_angle = get_angle_of_vector(collision_center, physical_object.get_center_position())
                    if not collision_object.stiff:
                        normal_collision_impulse = collision_object.get_impulse() * math.cos(normal_angle - collision_object.get_speed().get_direction())
                        collision_impulse = vector(normal_angle, normal_collision_impulse)
                    else:
                        physical_impulse = physical_object.get_impulse()
                        normal_impulse = physical_impulse.get_length() * math.sin(math.pi - physical_impulse.get_direction())
                        collision_impulse = vector(normal_angle, 2*normal_impulse)

                    physical_object.collision_impulse = add_vector(physical_object.collision_impulse, collision_impulse)
            
        return
        
    def __get_collision_center(self, object:physical_object, collision_object:physical_object):
        collision_mask = object.mask.overlap_mask(collision_object.mask, object.get_default_position_difference(collision_object.get_default_position()))
        if collision_mask.count() > 0:
            center = collision_mask.centroid()
            world_c = [object.get_default_position()[0] + center[0], collision_object.get_default_position()[1] + center[1]]
        else:
            world_c = None
        return world_c
    
    def __get_difference(self, default_position:tuple):
        return (default_position[0] - self.get_default_position()[0], default_position[1] - self.get_default_position()[1])
    

def __calculate_speed(current_object_speed, object_mass, current_collusion_object_speed, collusion_object_mass):
    mass_ratio = collusion_object_mass/object_mass
    return (2*mass_ratio)*current_collusion_object_speed + (1 - mass_ratio)*current_object_speed



class circle:
    def __init__(self, path, x, y):
        self.image = pygame.image.load(path).convert()
        self.cs = coordinate_system(self.get_size())
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
        return self.extern_to_intern(self.get_mask().overlap(mask, self.__get_difference(default_position)))
    
    def get_overlap_center(self, mask, default_position):
        overlap_mask = self.get_mask().overlap_mask(mask, self.__get_difference(default_position))
        if overlap_mask.count() > 0:
            center = self.extern_to_intern(overlap_mask.centroid())
            print(f"{type(overlap_mask)}/{type(self.get_mask())}")
            world_c = [self.get_center()[0] + center[0] - 300, self.get_center()[1] + center[1] - 300]
        else:
            world_c = None
        return world_c
    
    def __get_difference(self, default_position:tuple):
        return (default_position[0] - self.get_default_position()[0], default_position[1] - self.get_default_position()[1])
    
    def set_center(self, center:tuple) -> None:
        self.prev_center   = copy.deepcopy(list(self.center_buffer))
        self.center_buffer = copy.deepcopy(list(self.center))
        self.center        = copy.deepcopy(list(center))

    def get_direction_angle(self) -> float:
        return get_angle_of_vector(self.prev_center, self.center)

    def get_center(self) -> tuple[int, int]:
        return copy.deepcopy(self.center)
    
    def get_prev_center(self) -> tuple[int, int]:
        return copy.deepcopy(self.prev_center)


    def get_default_position(self):
        return (self.center[0]-(self.image.get_size()[0]*0.5), self.center[1]-(self.image.get_size()[1]*0.5))


    
class draw_line:
    def __init__(self, screen, color:tuple[int,int,int], thigness:int):
        self.cs = coordinate_system(screen.get_size())
        self.screen = screen
        self.color = color
        self.thigness = thigness

    def __draw(self, point_1, point_2):
        pygame.draw.line(self.screen, self.color, self.cs.intern_to_extern(point_1), self.cs.intern_to_extern(point_2), self.thigness)
    
    def draw(self, point_1, point_2):
        self.__draw(point_1, point_2)

    def draw(self, origin, length, angle):
        point_2 = ( (origin[0]+length*math.sin(angle)), (origin[1]-length*math.cos(angle)) )
        self.__draw(origin, point_2)

    

def set_offset(overlap, offset):
    return (overlap[0]+offset[0], overlap[1]+offset[1])

def get_normal_angle(center:tuple, overlap:tuple):
    gegenkathete = center[0] - overlap[0]
    ankathete = overlap[1] - center[1]
    normal_angle = arctan(ankathete, gegenkathete)
    if overlap[1] < center[1]:
        normal_angle += math.pi

    return normal_angle

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

def main_physic_test():
    pygame.init()

    screen = pygame.display.set_mode((800, 800))

    frames_per_second = 60
    fps_timer = timer()
    running = True

    while running:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                running = False

        if fps_timer.is_timer_done():
            fps_timer.set_timer(1/frames_per_second)

            pygame.display.flip()





    pygame.quit()







    

def main_one_jumping_circle():
    pygame.init()

    screen_size = (800, 800)
    screen = pygame.display.set_mode(screen_size)
    cs = coordinate_system(screen_size)


    circle_big = circle(pathlib.Path(f"{os.getcwd()}/Images/physics/Physics_big_circle.png"), 300, 300)
    circle_small = circle(pathlib.Path(f"{os.getcwd()}/Images/physics/Physics_small_circle.png"), pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    pixel = pygame.Surface((5,5))
    pixel.fill((0,255,0))

    normal_line = draw_line(screen, (255,0,0), 3)
    incomming_line = draw_line(screen, (0,0,255), 3)

    fps_timer = timer()
    running = True

    overlap_ = False

    start_position = None
    speed = [0,0]

    pre_normal_angle = None
    pre_comming_in_angle = None
    pre_overlap_center = None

    frames_per_second = 60

    while running:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                running = False

        if fps_timer.is_timer_done():
            fps_timer.set_timer(1/frames_per_second)

            screen.fill((0,255,0))
            screen.blit(circle_big.get_image(), cs.intern_to_extern((0, 0)))

            if start_position == None:
                circle_small.set_center(cs.extern_to_intern(pygame.mouse.get_pos()))

                screen.blit(circle_small.get_image(), cs.intern_to_extern(circle_small.get_default_position()))

                if pygame.mouse.get_pressed()[0]:
                    start_position = cs.extern_to_intern(pygame.mouse.get_pos())
                    circle_small.set_center(cs.extern_to_intern(pygame.mouse.get_pos()))




            else:

                if pygame.mouse.get_pressed()[0]:
                    start_position = cs.extern_to_intern(pygame.mouse.get_pos())
                    circle_small.set_center(start_position)
                    # speed = [0,0]

                acceleration = 100
                dt = 1/frames_per_second

                    
                position = circle_small.get_center()
                speed[1] = speed[1] + acceleration*dt
                position[1] = position[1] + speed[1]*dt
                position[0] = position[0] + speed[0]*dt

                circle_small.set_center(position)

                overlap_center = circle_small.get_overlap_center(circle_big.get_mask(), circle_big.get_default_position())

                if overlap_center:
                    normal_angle = get_normal_angle(circle_small.get_center(), overlap_center)

                    speed_0 = get_speed(speed)
                    normal_vektor = get_normal_vektor(normal_angle, speed_0)

                    comming_in_angle = circle_small.get_direction_angle()
                    pre_normal_angle = normal_angle
                    pre_comming_in_angle = comming_in_angle
                    pre_overlap_center = overlap_center
                    if not is_direction_field_equal((normal_angle+math.pi), comming_in_angle):

                        angle_difference = normal_angle - comming_in_angle

                        outgoing_angle = normal_angle + angle_difference

                        speed[0] =   speed_0 * math.sin(outgoing_angle)
                        speed[1] = - speed_0 * math.cos(outgoing_angle)
                    else:
                        print(f"aa: {comming_in_angle*57.3}/{normal_angle*57.3}/{outgoing_angle*57.3}")
                        print(f"na: {normal_angle*57.3}")
                        print(f"df: {is_direction_field_equal((normal_angle+math.pi), comming_in_angle)}")
                        print(f"dp: {get_dot_product(speed, normal_vektor)}")

                


                screen.blit(circle_small.get_image(), cs.intern_to_extern(circle_small.get_default_position()))

                if pre_overlap_center:
                    normal_line.draw(pre_overlap_center, 50, pre_normal_angle)
                    incomming_line.draw(pre_overlap_center, 50, pre_comming_in_angle)

                if overlap_center: 
                    # screen.blit(overlap_surf, offset_)
                    screen.blit(pixel, cs.intern_to_extern(overlap_center))

            pygame.display.flip()





    pygame.quit()


def main():
    # main_physic_test()
    main_one_jumping_circle()


if __name__ == "__main__":
    main()