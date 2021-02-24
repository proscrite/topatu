import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import peakutils
import re

from copy import deepcopy
from scipy.optimize import curve_fit

class Filter:
    def __init__(self, path: str = None, name: str = None,
                 wl: np.array = None, transm: np.array = None, refl: np.array = None,
                 df: pd.DataFrame = None):
        self.path = path
        self.name = name
        self.wl = wl
        self.transm = transm
        self.refl = refl
        self.df = df

    def read_txt(self):
        self.name = os.path.splitext(os.path.split(self.path)[1])[0]
        self.df = pd.read_csv(self.path, sep='\t', skiprows=None, decimal='.', names=['Wavelength', 'Transmission'])
        self.df.set_index('Wavelength', inplace=True)


    def read_excel(self):
        self.name = os.path.splitext(os.path.split(self.path)[1])[0]
        skip = 0

        if 'DM' in self.name: skip = 1           # First row is 'Unpolarized Performance of x nm Dichroic Mirror'
        self.df = pd.read_excel(self.path, skiprows=skip)

        for i,c in enumerate(self.df.columns.values):
            if 'Wavelength' in c:
                self.df.rename({c: 'Wavelength'}, axis=1, inplace=True)  # In some files it appears as 'Wavelength (cm)' in others without blankspace
            if 'Transmission' in c:
                self.df.rename({c: 'Transmission'}, axis=1, inplace=True)  # In some files it appears as 'Wavelength (cm)' in others without blankspace
            if 'Reflectance' in c:
                self.df.rename({c: 'Reflectance'}, axis=1, inplace=True)  # In some files it appears as 'Wavelength (cm)' in others without blankspace


        self.df.set_index('Wavelength', inplace=True)
        self.df['Transmission'] /= 100
        try:
            self.df['Reflectance'] /= 100
            self.df.drop(columns=['Unnamed: 0', 'Unnamed: 1'], inplace = True)
        except KeyError:
            pass

    def plot(self):
        plt.plot(self.df['Transmission'], label='Transmission')
        try:
            plt.plot(self.df['Reflectance'], label='Reflectance')
        except KeyError:
            pass
        plt.gca().set(xlabel = 'Wavelength [nm]', ylabel = 'Transm/Reflectance', title=self.name);
        plt.legend()

    def multiply(self, other):
        """Multiply transmission and reflection by another values of other filter by matching wavelengths
           Other will only multiply in transmission"""
        inters = self.df.index.intersection(other.df.index) # Find intersection of indices
        prodDf = pd.DataFrame()
        prodDf['Transmission'] = self.df.loc[inters]['Transmission'].multiply(other.df.loc[inters]['Transmission'])
        try:
            prodDf['Reflectance'] = self.df.loc[inters]['Reflectance'].multiply(other.df.loc[inters]['Transmission'])
        except KeyError:
            pass
        return prodDf
