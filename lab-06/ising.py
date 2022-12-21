import argparse
import numpy
import random
import utils as utils
from numba import jit
import numpy as np
from alive_progress import alive_bar
import time


def main():
    parser = argparse.ArgumentParser(description="Argument parser")
    parser.add_argument("-m", "--M", help="Mesh size", type=int, required=True, default=25)
    parser.add_argument("-j", "--J", help="J value", type=float, required=True, default=1.0)
    parser.add_argument("-beta", "--Beta", help="Beta param value", type=float, required=True, default=0.25)
    parser.add_argument("-b", "--B", help="B field value", type=float, required=True, default=0.0)
    parser.add_argument("-s", "--S", help='Steps of simulation', type=int, required=True, default=100)
    parser.add_argument("-g", "--G", help="Spin density", type=float, required=True, default=0.5)
    parser.add_argument("-i", "--I", help="File name with image", type=str, required=False, default="none")
    parser.add_argument("-a", "--A", help='File name with animation', type=str, required=False, default="none")
    parser.add_argument("-magnetization", "--Magnetization", help='File name with magnetization', type=str,
                        required=False, default="none")
    argument = parser.parse_args()
    n = argument.M
    J = argument.J
    beta = argument.Beta
    B = argument.B
    steps = argument.S
    rho = argument.G
    image_name = argument.I
    animation_name = argument.A
    magnetization_name = argument.Magnetization
    imgs = []
    magnetization = np.empty(steps)

    with alive_bar(steps, force_tty=True) as bar:
        start = time.time_ns()
        for _ in Simulation(n, rho, J, B, steps, beta, magnetization, imgs, image_name):
            bar()
        stop = time.time_ns()
        print(stop-start)
        # Time 31,681 s
        if animation_name != 'none':
            utils.save_gif(animation_name, imgs)
        if magnetization_name != 'none':
            utils.save_text_file(magnetization_name, magnetization)

def Simulation(n, rho, J, B, steps, beta, magnetization, imgs, image_name):
    mesh = numpy.ones((n, n))
    init(n, rho, J, B, steps, beta, magnetization, mesh)
    for step in range(0, steps):
        simulation_step(n, rho, J, B, steps, beta, magnetization, mesh)
        utils.draw_mesh(mesh, utils.create_file_name(image_name, step), n, imgs)
    yield

@jit(nopython=True)
def init(n, rho, J, B, steps, beta, magnetization, mesh):
    H = 0.0
    M = 0.0
    for i in range(len(mesh)):
        for j in range(len(mesh[i])):
            if random.uniform(0, 1) >= rho:
                mesh[i][j] = -1

    for i in range(len(mesh)):
        for j in range(len(mesh[i])):
            spin_i = mesh[i][j]
            H = H - J * get_energy_neighbors(spin_i, mesh, i, j, n) - B * spin_i

@jit(nopython=True)
def simulation_step(n, rho, J, B, steps, beta, magnetization, mesh):
    counter = 0
    while counter < n ** 2:
        i_rand = random.randint(0, n - 1)
        j_rand = random.randint(0, n - 1)
        spin_i = mesh[i_rand][j_rand]
        spin_rand = -1 * spin_i
        E0 = - J * utils.get_energy_neighbors(spin_i, mesh, i_rand, j_rand,
                                              n) - B * np.sum(mesh)
        E1 = - J * utils.get_energy_neighbors(spin_rand, mesh, i_rand, j_rand,
                                              n) - B * np.sum(mesh)
        dE = E1 - E0
        if dE < 0.0:
            mesh[i_rand][j_rand] = spin_rand
        elif random.uniform(0, 1) < numpy.exp(-beta * dE):
            mesh[i_rand][j_rand] = spin_rand
        counter = counter + 1
    M = (1.0 / n ** 2) * np.sum(mesh)
    np.append(magnetization, M)


@jit(nopython=True)
def get_energy_neighbors(spin, arr, xi, yi, arr_len):
    max_xi = xi
    max_yi = yi
    if xi - 1 == arr_len:
        max_xi = 0
    if yi - 1 == arr_len:
        max_yi = 0
    return (spin * arr[xi - 1][yi] +
            spin * arr[xi][max_yi] +
            spin * arr[max_xi][yi] +
            spin * arr[xi][yi - 1])

main()