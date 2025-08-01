import re, sys
import numpy as np
import mpmath as mp
from tablegen import constants

from .base_handler import BASE2B


class BUCK_EXT(BASE2B):
    
    def __init__(self, args):
        super().__init__()

        self.TABLENAME = args.table_name
        self.PLOT = args.plot

        self.TWO_BODY = True
        spec_set = set()

        names = list()
        for pair in args.pairs:
            spec_lst = re.sub(r'\s+', '', pair).split("-")
            if len(spec_lst) != 2:
                print("\nERROR: Each pair should consist of exactly two atomic species.\n")
                sys.exit(1)
            names.append(pair)

        self.COEFFS = dict()


        print("Please provide extended Buckingham coefficients A, rho, C, and D for the following pairs:")

        visited = list()
        for pair_name in names:
            visited.append(pair_name)
            try:
                A = float(input(f"({pair_name}) A: "))
            except ValueError:
                print("Buckingham coefficients should be numbers")
                sys.exit()

            try:
                rho = float(input(f"({pair_name}) rho: "))
            except ValueError:
                print("Buckingham coefficients should be numbers")
                sys.exit()

            try:
                C = float(input(f"({pair_name}) C: "))
            except ValueError:
                print("Buckingham coefficients should be numbers")
                sys.exit()

            try:
                D = float(input(f"({pair_name}) D: "))
            except ValueError:
                print("Buckingham coefficients should be numbers")
                sys.exit()

            self.COEFFS[pair_name] = [A, rho, C, D]

        self.CUTOFF = mp.mpf(args.cutoff)
        self.DATAPOINTS = args.data_points


    def get_force(self, A, rho, C, D, r):
        A = mp.mpf(A)
        rho = mp.mpf(rho)
        C = mp.mpf(C)
        D = mp.mpf(D)
        r = mp.mpf(r)
        if (not A) and (not C) and (not rho):
            rho = mp.mpf(1)
        rp = r / (43 * rho)
        return float((A / rho) * mp.exp(-r / rho) - 6 * C * r**-7 * (1 - mp.exp(-rp**6)) + (6 * C / (43**6 * rho**6)) * r**-1 * mp.exp(-rp**6) + 12 * D * r**-13)


    def get_pot(self, A, rho, C, D, r):
        A = mp.mpf(A)
        rho = mp.mpf(rho)
        C = mp.mpf(C)
        D = mp.mpf(D)
        r = mp.mpf(r)
        if (not A) and (not C) and (not rho):
            rho = mp.mpf(1)
        rp = r / (43 * rho)
        return float(A * mp.exp(-r / rho) - (C / r**6) * (1 - mp.exp(-rp**6)) + D / r**12)


    def eval_force(self, pair_name, r):
        if pair_name in self.COEFFS.keys():
            return self.get_force(*self.COEFFS[pair_name], r)
        else:
            raise RuntimeError("ERROR: Inconsitent pair_name assignment!")

    def eval_pot(self, pair_name, r):
        if pair_name in self.COEFFS.keys():
            return self.get_pot(*self.COEFFS[pair_name], r)
        else:
            raise RuntimeError("ERROR: Inconsitent pair_name assignment!")

    def get_table_name(self):
        return self.TABLENAME

    def to_plot(self):
        return self.PLOT

    def get_cutoff(self):
        return float(self.CUTOFF)

    def get_datapoints(self):
        return self.DATAPOINTS

    def get_species(self):
        return self.SPECIES

    def get_pairs(self):
        return self.COEFFS.keys()
