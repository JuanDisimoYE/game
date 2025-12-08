import math
import pygame
from char import timer


class circle:
    def __init__(self, path, x, y):
        self.image = pygame.image.load(path).convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.center = [x, y]

    def get_size(self) -> tuple[int, int]:
        return self.image.get_size()
    
    def get_image(self):
        return self.image
    
    def get_mask(self):
        return pygame.mask.from_surface(self.image)
    
    def is_overlap(self, mask, default_position):
        return self.get_mask().overlap(mask, self.__get_difference(default_position))
    
    def __get_difference(self, default_position:tuple):
        return (self.get_default_position()[0]-default_position[0], self.get_default_position()[1]-default_position[1])
    
    def set_center(self, center:tuple) -> None:
        self.center = [center[0], center[1]]

    def get_center(self) -> tuple[int, int]:
        return self.center


    def get_default_position(self):
        return (self.center[0]-(self.image.get_size()[0]*0.5), self.center[1]-(self.image.get_size()[1]*0.5))
    





def main():
    pygame.init()

    screen = pygame.display.set_mode((600, 600))

    circle_big = circle("C:/Users/julia/OneDrive/Desktop/VS Code/game/Images/physics/Physics_big_circle.png", 300, 300)
    circle_small = circle("C:/Users/julia/OneDrive/Desktop/VS Code/game/Images/physics/Physics_small_circle.png", pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    pixel = pygame.Surface((10,10))
    pixel.fill((255,0,0))

    fps_timer = timer()
    running = True

    print(circle_small.get_size())
    overlap_ = False

    start_position = None
    speed = 0

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
                    print(f"overlap: {overlap_} -> {overlap}")
                    print(f"get_pos: {pygame.mouse.get_pos()}")
                    print(f"center: {circle_small.center}")
                    print(f"default: {circle_small.get_default_position()}")
                    overlap_ = overlap

                if pygame.mouse.get_pressed()[0]:
                    start_position = pygame.mouse.get_pos()
                    circle_small.set_center(pygame.mouse.get_pos())

            else:
                acceleration = 80
                dt = 1/60

                position = circle_small.get_center()
                speed += acceleration*dt
                position[1] += speed*dt

                circle_small.set_center(position)

                if circle_small.is_overlap(circle_big.get_mask(), circle_big.get_default_position()) and (speed > 0):
                    speed = -speed


                screen.blit(circle_small.get_image(), circle_small.get_default_position())


            # if overlap:
            #     screen.blit(pixel, overlap)
            # else:
            #     screen.blit(pixel, (0,0))

            pygame.display.flip()





    pygame.quit()


if __name__ == "__main__":
    main()