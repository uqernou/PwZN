import sympy as sym
import numpy as np
import matplotlib.pyplot as plt


def printFunction(expr):
    sym.pprint(expr)


fig, ((ax, ax0), (ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(4, 2, figsize=(40, 30), sharex=True, sharey=True)
x = np.linspace(0, 4, 1000)

sym.init_printing(use_latex='mathjax')
x0, v0, w, w0, A, beta, t = sym.symbols('x_0 v_0 omega omega_0 A beta t', real=True)
x1, x2, x3, x4 = sym.symbols('x_1 x_2 x_3 x_4', cls=sym.Function)

# Simple harmonic oscillator
simple = sym.Eq(x1(t).diff(t, 2) + w ** 2 * x1(t), 0)
simpleSolve = sym.dsolve(simple,
                         x1(t),
                         ics={x1(0): x0, x1(t).diff(t).subs(t, 0): v0}  # warunki początkowe
                         )
pythonFunction = sym.lambdify(t, simpleSolve.rhs.subs({x0: 2, v0: 2, w: 2}))

ax.plot(x, pythonFunction(x), color="red", linewidth=4)
ax.set_xlabel("time", size=15)
ax.set_ylabel("$x_1(t)$", size=15)
ax.set_title("Simple harmonic oscillator $x_1(t)$, $\omega=2$, $v_0=2$, $x_0=2$", size=25)
ax.grid(color='grey', linestyle='-', linewidth=0.9)

for i in range(2, 6):
    pythonFunction = sym.lambdify(t, simpleSolve.rhs.subs({x0: 2, v0: 2, w: i}))
    val = pythonFunction(x)
    ax0.plot(x, pythonFunction(x), linewidth=4, label=("$\omega=$" + str(i)))
ax0.set_xlabel("time", size=15)
ax0.set_ylabel("$x_1(t)$", size=15)
ax0.set_title("Simple harmonic oscillator $x_1(t)$, $v_0=2$, $x_0=2$", size=25)
ax0.grid(color='grey', linestyle='-', linewidth=0.9)
ax0.legend()

print("Equation of simple harmonic oscillator: ")
printFunction(simple)
# print("Solve: ")
# printFunction(simpleSolve)

# Damped harmonic oscillator
damped = sym.Eq(x2(t).diff(t, 2) + w ** 2 * x2(t) + 2 * beta * x2(t).diff(t), 0)
dampedSolve = sym.dsolve(damped,
                         x2(t),
                         ics={x2(0): x0, x2(t).diff(t).subs(t, 0): v0}  # warunki początkowe
                         )

print("Equation of damped harmonic oscillator: ")
printFunction(damped)
# print("Solve: ")
# printFunction(dampedSolve)
for i in range(2, 6):
    pythonFunction = sym.lambdify(t, dampedSolve.rhs.subs({x0: 2, v0: 2, w: 6, beta: i}))
    ax1.plot(x, pythonFunction(x).real, linewidth=4, label=("$\\beta=$" + str(i)))
    pythonFunction = sym.lambdify(t, dampedSolve.rhs.subs({x0: 2, v0: 2, w: i, beta: 1}))
    ax2.plot(x, pythonFunction(x).real, linewidth=4, label=("$\omega=$" + str(i)))

ax1.set_xlabel("time", size=15)
ax2.set_xlabel("time", size=15)
ax1.set_ylabel("$x_2(t)$", size=15)
ax2.set_ylabel("$x_2(t)$", size=15)
ax1.set_title("Damped harmonic oscillator $x_2(t)$, $\omega=6$, $v_0=2$, $x_0=2$", size=25)
ax2.set_title("Damped harmonic oscillator $x_2(t)$, $v_0=2$, $x_0=2$, $\\beta=2$ ", size=25)
ax1.grid(color='grey', linestyle='-', linewidth=0.9)
ax2.grid(color='grey', linestyle='-', linewidth=0.9)
ax1.legend()
ax2.legend()

# Driven harmonic oscillators
driven = sym.Eq(x3(t).diff(t, 2) + w ** 2 * x3(t), A * sym.cos(w0*t))
drivenSolve = sym.dsolve(driven,
                         x3(t),
                         ics={x3(0): x0, x3(t).diff(t).subs(t, 0): v0}  # warunki początkowe
                         )

print("Equation of driven harmonic oscillator: ")
printFunction(driven)
# print("Solve: ")
# printFunction(drivenSolve)
for i in range(1, 6):
    pythonFunction = sym.lambdify(t, drivenSolve.rhs.subs({x0: 2, v0: -2, w: 6, A: 10, w0: i}))
    ax3.plot(x, pythonFunction(x).real, linewidth=4, label=("$\omega_0=$" + str(i)))
    pythonFunction = sym.lambdify(t, drivenSolve.rhs.subs({x0: 2, v0: -2, w: 6, A: 3*i, w0: 3}))
    ax4.plot(x, pythonFunction(x).real, linewidth=4, label=("$A=$" + str(2*i)))

ax3.set_xlabel("time", size=15)
ax4.set_xlabel("time", size=15)
ax3.set_ylabel("$x_3(t)$", size=15)
ax4.set_ylabel("$x_3(t)$", size=15)
ax3.set_title("Driven harmonic oscillator $x_3(t)$, $\omega=6$, $v_0=-2$, $x_0=2$, A=10", size=25)
ax4.set_title("Driven harmonic oscillator $x_3(t)$, $\omega=6$, $v_0=-2$, $x_0=2$, $\omega_0=3$", size=25)
ax3.grid(color='grey', linestyle='-', linewidth=0.9)
ax4.grid(color='grey', linestyle='-', linewidth=0.9)
ax3.legend()
ax4.legend()

# Damped & driven harmonic oscillators
dampedDriven = sym.Eq(x4(t).diff(t, 2) + w ** 2 * x4(t) + 2 * beta * x4(t).diff(t), A * sym.cos(w0*t))
dampedDrivenSolve = sym.dsolve(dampedDriven,
                         x4(t),
                         ics={x4(0): x0, x4(t).diff(t).subs(t, 0): v0}  # warunki początkowe
                         )

print("Equation of damped & driven harmonic oscillator: ")
printFunction(dampedDriven)
# print("Solve: ")
# printFunction(dampedDrivenSolve)
for i in range(2, 6):
    pythonFunction = sym.lambdify(t, dampedDrivenSolve.rhs.subs({x0: 2, v0: -2, w: 6, beta: 1, A: 2, w0: i}))
    ax5.plot(x, pythonFunction(x).real, linewidth=4, label=("$\omega_0=$" + str(i)))
    pythonFunction = sym.lambdify(t, dampedDrivenSolve.rhs.subs({x0: 2, v0: -2, w: 6, beta: 1, A: 2*i, w0: 6}))
    ax6.plot(x, pythonFunction(x).real, linewidth=4, label=("$A=$" + str(2*i)))

ax5.set_xlabel("time", size=15)
ax6.set_xlabel("time", size=15)
ax5.set_ylabel("$x_3(t)$", size=15)
ax6.set_ylabel("$x_3(t)$", size=15)
ax5.set_title("Damped & driven harmonic oscillator $x_4(t)$, $\omega=6$, $v_0=-2$, $x_0=2$, $\\beta=1$, A=2", size=25)
ax6.set_title("Damped & driven harmonic oscillator $x_4(t)$, $\omega=6$, $v_0=-2$, $x_0=2$, $\\beta=1$, $\omega_0=6$", size=25)
ax5.grid(color='grey', linestyle='-', linewidth=0.9)
ax6.grid(color='grey', linestyle='-', linewidth=0.9)
ax5.legend()
ax6.legend()

plt.show()
