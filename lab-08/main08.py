import random
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

N_pop = 10000
S_pop, I_pop, R_pop = 9999, 1, 0
gamma, beta = 0.1, 0.3
t = np.linspace(0, 1000, 1000)


def SIR_model_equation(ft, t, N, beta, gamma):
    S, I, R = ft
    dS_dt = -beta * S * I / N
    dI_dt = beta * S * I / N - gamma * I
    dR_dt = gamma * I
    return dS_dt, dI_dt, dR_dt


fig, ((ax, ax0), (ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(4, 2, figsize=(20, 15), sharex=True, sharey=True)
ax_arr = [ax, ax0, ax1, ax2, ax3, ax4, ax5, ax6]
for axes in ax_arr:
    ft_0 = S_pop, I_pop, R_pop
    beta_rand = random.random()
    gamma_rand = random.uniform(0, .4)
    solution = odeint(SIR_model_equation, ft_0, t, args=(N_pop, beta_rand, gamma_rand))
    S = solution[:, 0]/N_pop
    I = solution[:, 1]/N_pop
    R = solution[:, 2]/N_pop
    axes.plot(t, S, 'b', alpha=0.5, lw=2, label='Susceptible')
    axes.plot(t, I, 'r', alpha=0.5, lw=2, label='Infected')
    axes.plot(t, R, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
    axes.set_xlabel('Time /days')
    axes.set_ylabel('Population')
    axes.set_title('SIR model $\\beta=$' + str(round(beta_rand, 2)) + ', $\gamma=$' + str(round(gamma_rand, 2)))
    axes.yaxis.set_tick_params(length=0)
    axes.xaxis.set_tick_params(length=0)
    axes.grid(b=True, which='major', c='w', lw=2, ls='-')
    axes.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    axes.legend()

plt.show()