import math
from physics import get_normal_angle


r_center = 100
r_overlap = 120

phi = 0.0

while phi < (math.pi*2):
    center = (math.cos(phi)*r_center, math.sin(phi)*r_center)
    overlap = (math.cos(phi)*r_overlap, math.sin(phi)*r_overlap)

    print(get_normal_angle(center, overlap)*57.3)

    phi += 0.1