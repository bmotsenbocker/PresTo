# This code allows you to input various lens properties to calculate the 
# effective focal length of a lens system
# n = refractive index
# r = radius of curvature (front = closer to the incoming light, back = closer 
# to the sensor)
# t = thickness (0 if thin lens)
# all measurements are in mm

import math

# focal length of single lens
def single_focal_len(n, r_front, r_back, t):
    global focal
    focal = ((n-1)*(1/r_front - 1/r_back + t*(n - 1)/
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


# properties of the first lens
n1 = 1.673
r_front1 = 3.5
r_back1 = -3.5
t1 = 2.3

# second lens
n2 = 1.673
r_front2 = 3.71
r_back2 = -5.60
t2 = 5.0

# first liquid
nliq = 1.333
r_frontl1 = float('inf')
r_backl1 = r_front1
tliq1 = 1.0

# second liquid
r_frontl2 = r_back1
r_backl2 = r_front1
tliq2 = 1.0

# third liquid
r_frontl3 = r_back1
r_backl3 = 1000000
tliq3 = 2.0

# fourth liquid
r_frontl4 = r_back2
r_backl4 = r_frontl1
tliq4 = 3.0


# lens property listed in order from port to sensor
n_list = [nliq,n1,nliq,n1,nliq]
    
r_front_list = [r_frontl1,r_front1,r_frontl2,r_front1,
                r_frontl3]

r_back_list = [r_backl1,r_back1,r_backl2,r_back1,r_backl3]

t_list = [tliq1,t1,tliq2,t1,tliq3]


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


# angular field of view
h = 3.68  # horizontal dimension of the sensor
FOV = 2*math.atan(h/(2*EFL))
FOV_deg = math.degrees(FOV)
print('FOV =', round(FOV_deg, 2), 'deg')


# image circle diameter
ICD = 2 * EFL * math.tan(FOV/2)
print('ICD =', round(ICD, 2), 'mm')

# f-stop
diameter = 3.0 
f_stop = EFL/diameter
print('F-stop =',round(f_stop,2))