from permuted_tree import merkelize, mk_branch, verify_branch, blake, mk_multi_branch, verify_multi_branch
from poly_utils import PrimeField
import time
from fft import fft
from fri import prove_low_degree, verify_low_degree_proof
from utils import get_power_cycle, get_pseudorandom_indices, is_a_power_of_2

"""
All calculations are done modulo ; Vitalik used this prime field modulus
because it is the largest prime below 2^256 whose multiplicative group contains
an order 2^32 subgroup (that is, there's a number g such that successive powers
of g modulo this prime loop around back to 1 after exactly 32^32 cycles), and
which is of the form 6k+5. The first property is necessary to make sure that
the efficient versions of the FFT and FRI algorithms can work, and the second
ensures that the MIMC actually can be computed "backwards". We dont need the
backwards computation but keep that modulus anyway.
"""

modulus = 2**256 - 2**32 * 351 + 1
f = PrimeField(modulus)

# This is the higher power root of unity to calculate the intermediate
# evaluations of the polynomials i.e. not exactly on the computation trace
# Where evaluations are zero for some polys and lead to problems with
# evaluation
# Root of unity such that x^(precision)=1
precision = (7 + 1) * 8
G2 = f.exp(7, (modulus-1)//precision)

skips = precision // (7 + 1)
G1 = f.exp(G2, skips)

# Powers of the higher order root of unity
xs = get_power_cycle(G2, modulus)


array = [0, 1, 2]
# print(array[1:])
# print(array[:1])


def degreedtatest_old(x, y):
    for i in range(1, len(x)):
        if i == len(x) - 1:
            return 999
        poly = f.lagrange_interp([xi for xi in x[:i+1]],
                                 [yi for yi in y[:i+1]])
        eval = f.eval_poly_at(poly, x[i+1])
        evalinside = f.eval_poly_at(poly, x[2])

        if eval == y[i+1]:
            return i

def degreedtatest(x, y, exclude_multiples_of):
    # returns degree of a dataset point has degree zero
    print("x :", x)
    print("y :", y)

    for i in range(1, len(x)):
        if i == len(x) - 1:
            return 999
        print("index:", i)

        x_points = [xi for xi in x[:i+1]]
        y_points = [yi for yi in y[:i+1]]

        if exclude_multiples_of:
            pts = [x for x in range(len(x_points)) if x % exclude_multiples_of]
            print("excluded multiples of ", exclude_multiples_of)
        else:
            pts = range(len(x_points))

        x_points = [x_points[i] for i in pts]
        y_points = [y_points[i] for i in pts]
        print("interpolating xs: ", x_points)
        print("interpolating ys: ", y_points)
        poly = f.lagrange_interp([xi for xi in x_points],
                                 [yi for yi in y_points])
        print("poly", poly)
        eval = f.eval_poly_at(poly, x[i+1])
        print("evaluation at the next point x =", x[i+1], "f(x)", eval, "=?", y[i+1])
        # evalinside = f.eval_poly_at(poly, x[2])
        # print("evalinside: ", evalinside)
        if eval == y[i+1]:
            return len(x_points) - 1


x = [xs[0], xs[1], xs[2], xs[3], xs[4], xs[5]]
y = [f.eval_poly_at([1, 1, 1, 1, 1], xi) for xi in x]


print("degree: ", degreedtatest(x, y, 5))
