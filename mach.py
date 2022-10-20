import math
pi = math.pi
uni_gas_const = uni_gas_const = 8.314472 # m2 kg s-2 K-1 mol-1

pseudo_infinity = 10e6

# this function calculates the distribution of the combustion gas flow mach number
# across the engine
# see https://www.grc.nasa.gov/WWW/k-12/airplane/nozzled.html for more
# also especially see https://www.grc.nasa.gov/WWW/K-12/airplane/astar.html
# (the R here isn't the universal constant)
def calc_mach_num(xs, ys, gamma):
    global uni_gas_const, pi

    subsonic_M = []
    subsonic_x = []

    throat_y = min(xs)

    # subsonic region
    for i in range(len(xs)):
        
        x = xs[i]
        y = ys[i]

        if y == throat_y:
            # we have come to the throat, where the Mach number should be 1
            # therefore, the computations need to switch to supersonic mode

            # record where we left off so the supersonic function will take over
            # from there
            last_i = i
            break

        A_star = pi * throat_y**2
        A = pi * y**2
        A_ratio = A/A_star

        # - - - - - - BEGIN QUOTE - - - - - -
        gp1 = gamma + 1
        gm1 = gamma - 1

        arat = A_ratio
        aro = 2
        macho = 0.30

        fac1 = gp1/(2*gm1)
        machn = macho + 0.05

        infinity_fuse = 0
        while abs(A_ratio - aro) > 0.0001:
            fac = 1 + 0.5 * gm1 * machn**2
            arn = 1/(machn * fac**(-fac1) * (gp1/2)**fac1)
            deriv = (arn-aro)/(machn-macho)
            aro = arn
            macho = machn
            machn = macho + (arat - aro)/deriv

        # - - - - - - END QUOTE - - - - - -

            infinity_fuse += 1

            if infinity_fuse > pseudo_infinity:
                print("Mach number calculator might have entered an infinite loop, because it hasn't converged for", pseudo_infinity, "iterations. (A)bort or (C)ontinue for another", pseudo_infinity, "iterations?")
                fuse_replacement = input(" > ")
                if fuse_replacement.lower() == "c":
                    infinity_fuse = 0
                elif fuse_replacement.lower() == "a":
                    print("Analysis aborted.")
                    input("Press Enter to quit...")
                    quit()
                else:
                    print("Invalid choice!")

        # required failsafe
        if macho >= 1 or macho < 0.2:
            macho = 0
            
        subsonic_M.append(macho)
        subsonic_x.append(x)

    # calculate for supersonic region
    # density is variable
    # m_dot is const
    supersonic_M = []
    supersonic_x = []

    for i in range(last_i, len(xs)):
        
        x = xs[i]
        y = ys[i]
        
        A_star = pi * throat_y**2
        A = pi * y**2
        A_ratio = A/A_star

        # - - - - - - BEGIN QUOTE - - - - - -
        gp1 = gamma + 1
        gm1 = gamma - 1

        arat = A_ratio
        aro = 2
        macho = 2.2

        fac1 = gp1/(2*gm1)
        machn = macho + 0.05

        infinity_fuse = 0
        while abs(A_ratio - aro) > 0.0001:
            fac = 1 + 0.5 * gm1 * machn**2
            arn = 1/(machn * fac**(-fac1) * (gp1/2)**fac1)
            deriv = (arn-aro)/(machn-macho)
            aro = arn
            macho = machn
            machn = macho + (arat - aro)/deriv
        # - - - - - - END QUOTE - - - - - -

            infinity_fuse += 1

            if infinity_fuse > pseudo_infinity:
                print("Mach number calculator might have entered an infinite loop, because it hasn't converged for", pseudo_infinity, "iterations. (A)bort or (C)ontinue for another", pseudo_infinity, "iterations?")
                fuse_replacement = input(" > ")
                if fuse_replacement.lower() == "c":
                    infinity_fuse = 0
                elif fuse_replacement.lower() == "a":
                    print("Analysis aborted.")
                    input("Press Enter to quit...")
                    quit()
                else:
                    print("Invalid choice!")
        
        supersonic_M.append(macho)
        supersonic_x.append(x)

    return subsonic_x, subsonic_M, supersonic_x, supersonic_M

