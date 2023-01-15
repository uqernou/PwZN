from bokeh.plotting import figure
from bokeh.layouts import layout
from bokeh.models import Slider, ColumnDataSource
from scipy.integrate import odeint
import numpy as np
from bokeh.io import output_notebook, curdoc

output_notebook()

#bokeh serve --show ./lab-09/main09.py - to run me
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

ft_0 = S_pop, I_pop, R_pop
solution = odeint(SIR_model_equation, ft_0, t, args=(N_pop, beta, gamma))
# create dict as basis for ColumnDataSource
sourceS = ColumnDataSource(data={'t': t, 'S': solution[:, 0]/N_pop})
sourceI = ColumnDataSource(data={'t': t, 'I': solution[:, 1]/N_pop})
sourceR = ColumnDataSource(data={'t': t, 'R': solution[:, 2]/N_pop})
# create a plot and renderer with ColumnDataSource data
fig = figure()
fig.line(x='t', y='S', source=sourceS, color='blue')
fig.line(x='t', y='I', source=sourceI, color='red')
fig.line(x='t', y='R', source=sourceR, color='green')

def update_beta(attr, old, new):
    solution = odeint(SIR_model_equation, ft_0, t, args=(N_pop, new, gamma))
    sourceS.data['S'] = solution[:, 0]/N_pop
    sourceI.data['I'] = solution[:, 1]/N_pop
    sourceR.data['R'] = solution[:, 2]/N_pop

def update_gamma(attr, old, new):
    solution = odeint(SIR_model_equation, ft_0, t, args=(N_pop, beta, new))
    sourceS.data['S'] = solution[:, 0]/N_pop
    sourceI.data['I'] = solution[:, 1]/N_pop
    sourceR.data['R'] = solution[:, 2]/N_pop


beta_slider = Slider(title="       β parameter:", start=0.0, end=1.0, step=0.01, value=beta)
gamma_slider = Slider(title="       γ parameter:", start=0.0, end=1.0, step=0.01, value=gamma)
beta_slider.on_change('value', update_beta)
gamma_slider.on_change('value', update_gamma)

layout = layout([beta_slider], [gamma_slider], [fig])
curdoc().add_root(layout)
