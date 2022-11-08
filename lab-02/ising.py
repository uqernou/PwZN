import argparse
import numpy
import random
import utils as utils
from alive_progress import alive_bar


class IsingMC:
    def __init__(self):
        self.extract_params()
        self.init_variables()
        self.run_script()

    def extract_params(self):
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
        self.n = argument.M
        self.J = argument.J
        self.beta = argument.Beta
        self.B = argument.B
        self.steps = argument.S
        self.rho = argument.G
        self.image_name = argument.I
        self.animation_name = argument.A
        self.magnetization_name = argument.Magnetization

    def init_variables(self):
        self.imgs = []
        self.magnetization = []
        self.mesh = numpy.ones((self.n, self.n))
        self.H = 0.0
        self.M = 0.0
        self.shuffle_mesh()
        self.calculate_hamiltonian()

    def shuffle_mesh(self):
        for i in range(len(self.mesh)):
            for j in range(len(self.mesh[i])):
                if random.uniform(0, 1) >= self.rho:
                    self.mesh[i][j] = -1

    def calculate_hamiltonian(self):
        for i in range(len(self.mesh)):
            for j in range(len(self.mesh[i])):
                spin_i = self.mesh[i][j]
                self.H = self.H - self.J * utils.get_energy_neighbors(spin_i, self.mesh, i, j, self.n) - self.B * spin_i

    def calculate_magnetization(self):
        self.M = (1.0 / self.n ** 2) * utils.sum_spin(self.mesh)
        self.magnetization.append(self.M)

    def simulation(self):
        for step in range(0, self.steps):
            self.simulation_step()
            utils.draw_mesh(self.mesh, utils.create_file_name(self.image_name, step), self.n, self.imgs)
            yield

    def simulation_step(self):
        counter = 0
        while counter < self.n ** 2:
            i_rand = random.randint(0, self.n - 1)
            j_rand = random.randint(0, self.n - 1)
            spin_i = self.mesh[i_rand][j_rand]
            spin_rand = -1 * spin_i
            E0 = - self.J * utils.get_energy_neighbors(spin_i, self.mesh, i_rand, j_rand,
                                                           self.n) - self.B * utils.sum_spin(self.mesh)
            E1 = - self.J * utils.get_energy_neighbors(spin_rand, self.mesh, i_rand, j_rand,
                                                           self.n) - self.B * utils.sum_spin(self.mesh)
            dE = E1 - E0
            if dE < 0.0:
                self.mesh[i_rand][j_rand] = spin_rand
            elif utils.check_probability(self.beta, dE) == 1:
                self.mesh[i_rand][j_rand] = spin_rand
            counter = counter + 1
        self.calculate_magnetization()

    def run_script(self):
        with alive_bar(self.steps, force_tty=True) as bar:
            for _ in self.simulation():
                bar()
            if self.animation_name != 'none':
                utils.save_gif(self.animation_name, self.imgs)
            if self.magnetization_name != 'none':
                utils.save_text_file(self.magnetization_name, self.magnetization)
