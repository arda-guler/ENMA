import matplotlib.pyplot as plt
import datetime
import os
import csv

def plot_all(xs, ys, mach_data=None):
    # PLOT CONTOUR & MACH NUMBER
    plotnum = 0
    
    _, ax = plt.subplots()
    plotnum += 1
    plt.figure(plotnum)

    ax.plot(xs, ys)
    ax.set_xlabel("Axial, X (mm)")
    ax.set_ylabel("Radial, Y (mm)")
    ax.set_aspect('equal')

    if mach_data:
        Mxs = mach_data[0] + mach_data[2]
        Mys = mach_data[1] + mach_data[3]
        
        ax2 = ax.twinx()
        ax2.set_aspect('auto')
        ax2.yaxis.set_label_position("left")
        ax2.yaxis.tick_left()
        ax2.plot(Mxs, Mys)
        ax2.set_ylabel("Mach Number")

    plt.grid()

    if mach_data:
        plt.title("Nozzle Contour & Mach Profile")
    else:
        plt.title("Nozzle Contour")

    # EXPORT
    folder_name = "nozzle_design_" + datetime.datetime.now().strftime("%y%m%d%H%M%S")
    print("Exporting data to folder: " + folder_name)

    try:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
    except:
        print("ERROR: Could not create folder. Try saving figures by hand.")
        plt.show()
        return

    try:
        rows = []
        for i in range(len(xs)):
            rows.append([xs[i], ys[i]])

        outfile = open(folder_name + "/contour.csv", "w")
        csvwriter = csv.writer(outfile)
        for r in rows:
            csvwriter.writerow(r)

        outfile.close()
    except:
        print("WARNING: Could not export contour data file.")

    try:
        for i in range(1, plotnum + 1):
            new_fig = plt.figure(i)
            save_str = folder_name + "/figure_" + str(i) + ".png"
            new_fig.savefig(save_str)
    except:
        print("ERROR: Could not save some or all of the figures. Try saving figures by hand.")
        plt.show()
        return

    print("Figures exported successfully!")

    # show figure(s)
##    for i in range(1, plotnum + 1):
##        new_fig = plt.figure(i)
##        new_fig.show()
##        input("Press Enter to continue...")
    
    print("Clearing figures from memory...")
    for i in range(1, plotnum + 1):
        new_fig = plt.figure(i)
        new_fig.clear()
        plt.close()

    print("Analysis done!")
