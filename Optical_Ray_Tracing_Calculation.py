# This code allows you to input various lens properties to calculate the 
# effective focal length of a lens system in a liquid
# n = refractive index
# r = radius of curvature (front = closer to the incoming light, back = closer 
# to the sensor)
# t = thickness (0 if thin lens)
# all measurements are in mm

import math

# focal length of single lens
def single_focal_len(n, r_front, r_back, t):
    global focal
    focal = ((n - 1)*(1/r_front - 1/r_back + t*(n - 1)/
                          (n*r_front*r_back)))**(-1)
    
# location of principal planes
def prin_planes(focal, n, t, r_front, r_back):
    global h1
    global h2
    h1 = -focal*(n-1)*t/(r_back*n) # measured from first vertex
    h2 = -focal*(n-1)*t/(r_front*n) # measured from second vertex

# focal length of the system
def system_focal_len(focal_first, focal_second, dist):
    global sys_focal
    sys_focal = ((1/focal_first) + (1/focal_second) - dist/ 
                 (focal_first*focal_second))**(-1)

# Lens and liquid properties
# Add, subtract, or edit properties as needed

# first lens
n1 = 1.728
r_front1 = 41.01
r_back1 = 4.35
t1 = 1.03

# second lens
n2 = 1.67
r_front2 = 4.35
r_back2 = -6.98
t2 = 3.06

# third lens
n3 = 1.673
r_front3 = 6.18
r_back3 = -6.18
t3 = 2.5

# first liquid
nliq = 1.333
r_frontl1 = float("inf")
r_backl1 = r_front1
tliq1 = 3.0

# second liquid
r_frontl2 = r_back2
r_backl2 = r_front3
tliq2 = 0.5

# third liquid
r_frontl3 = r_back3
r_backl3 = r_frontl1
tliq3 = 5.0


# lens property listed in order from view port to sensor
# edit this section to match the order of your personal configuration 

n_list = [nliq,n1,n2,nliq,n3,nliq]
    
r_front_list = [r_frontl1,r_front1,r_front2,r_frontl2,r_front3,r_frontl3]

r_back_list = [r_backl1,r_back1,r_back2,r_backl2,r_back3,r_backl3]

t_list = [tliq1,t1,t2,tliq2,t3,tliq3]


# focal length of each lens
focal_len_list = []

for (a,b,c,d) in zip(n_list,r_front_list,r_back_list,t_list):
    single_focal_len(a,b,c,d)
    focal_len_list.append(focal)


# principal plane of each lens, 1 refers to the plane closer to the 
# light, 2 is closer to the sensor
prin_planes_1_list = []
prin_planes_2_list = []

for (a,b,c,d,e) in zip(focal_len_list,n_list,t_list,r_front_list,r_back_list):
    prin_planes(a,b,c,d,e)
    prin_planes_1_list.append(h1)
    prin_planes_2_list.append(h2)

# distance between the principal planes
len_prin_planes_2 = len(prin_planes_2_list) - 1
del prin_planes_1_list[0]
del prin_planes_2_list[len_prin_planes_2]
diff_prin_planes = []

for (a,b) in zip(prin_planes_2_list,prin_planes_1_list):
    diff_prin_planes.append(b-a)

# focal length of the system
focal_first_list = [focal_len_list[0]]
del focal_len_list[0]

for (a,b,c) in zip(focal_first_list,focal_len_list, diff_prin_planes):
   system_focal_len(a,b,c)
   focal_first_list.append(sys_focal)


# effective focal length
len_focal_first_list = len(focal_first_list)-2
EFL = focal_first_list[len_focal_first_list]
print('EFL =', round(EFL,2), 'mm')


# angular horizontal field of view
h = 3.68  # horizontal dimension of the sensor
FOV = 2*math.atan(h/(2*EFL))
FOV_deg = math.degrees(FOV)
print('FOV =', round(FOV_deg, 2), 'deg')


# f-stop
diameter = 4.5
f_stop = EFL/diameter
print('F-stop =',round(f_stop,2))

