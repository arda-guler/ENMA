# PROGRAM: RAO-STYLE THRUST OPTIMIZED BELL NOZZLE DESIGNER
# FOR LIQUID PROPELLANT ROCKET ENGINES
#
# Author: H. A. Güler (arda-guler @ Github)

import matplotlib.pyplot as plt
import math
import csv

def get_parabola_point(Nx, Ny, Qx, Qy, Ex, Ey, t):
    x = ((1-t)**2) * Nx + 2*(1-t)*t*Qx + (t**2) * Ex
    y = ((1-t)**2) * Ny + 2*(1-t)*t*Qy + (t**2) * Ey

    return x, y

def compute(D_throat, D_exit, length_percent=80, theta_n=None, theta_e=None):

    xs = []
    ys = []

    if length_percent < 60:
        length_percent = 60
        print("Nozzle length was set below 60%. Automatically setting to 60%...")
    
    R_throat = D_throat * 0.5
    R_exit = D_exit * 0.5
    expansion_ratio = (R_exit**2) / (R_throat**2)

    # theta_n not given, get it from Rao's graph
    if not theta_n:
        if length_percent <= 70:
            if expansion_ratio < 10:
                theta_n = 30
            else:
                theta_n = 35

        elif length_percent <= 85:
            if expansion_ratio < 30:
                theta_n = 25
            else:
                theta_n = 30

        else:
            if expansion_ratio <= 15:
                theta_n = 20
            else:
                theta_n = 25

    # theta_e not given, get it from Rao's graph
    if not theta_e:
        if length_percent <= 70:
            if expansion_ratio < 15:
                theta_e = 20
            else:
                theta_e = 15

        elif length_percent <= 85:
            if expansion_ratio < 10:
                theta_e = 15
            elif expansion_ratio < 40:
                theta_e = 10
            else:
                theta_e = 5

        else:
            if expansion_ratio < 6:
                theta_e = 10
            else:
                theta_e = 5

    # compute where the parabola starts
    print("Parabola start angle:", theta_n)
    print("Parabola end angle:", theta_e)
    x_throat = 0
    x_parabola = 0.382*R_throat*math.sin(math.radians(theta_n))
    x_exit = (length_percent/100) * (((expansion_ratio**0.5) - 1) * R_throat)/math.tan(math.radians(15))

    Nx = x_parabola
    Ny = R_throat + (R_throat * 0.382) - (((R_throat * 0.382)**2) - (x_parabola**2))**(0.5)

    Ex = x_exit
    Ey = R_exit

    m1 = math.tan(math.radians(theta_n))
    m2 = math.tan(math.radians(theta_e))
    C1 = Ny - m1*Nx
    C2 = Ey - m2*Ex

    Qx = (C2-C1)/(m1-m2)
    Qy = (m1*C2 - m2*C1)/(m1-m2)

    x = -R_throat * 1.5 / 2
    throat_dx = (x_parabola - x)/100

    # throat downstream and upstream arcs
    while x < x_parabola:
        if x < 0:
            R_arc = R_throat * 1.5
        else:
            R_arc = R_throat * 0.382

        xs.append(x)
        ys.append(R_throat + R_arc - ((R_arc**2) - (x**2))**(0.5))

        x += throat_dx

    # parabola
    t = 0
    dt = 0.05

    while t <= 1:
        x, y = get_parabola_point(Nx, Ny, Qx, Qy, Ex, Ey, t)
        xs.append(x)
        ys.append(y)
        t += dt

    return xs, ys

xs, ys = compute(120, 300, 80)
fig, axs = plt.subplots(1,1)
axs.plot(xs, ys)
axs.axis('equal')
plt.xlabel("Axial / X")
plt.ylabel("Radial / Y")
plt.show()

rows = []
for i in range(len(xs)):
    rows.append([xs[i], ys[i]])

outfile = open("latest.csv", "w")
csvwriter = csv.writer(outfile)
for r in rows:
    csvwriter.writerow(r)

outfile.close()
