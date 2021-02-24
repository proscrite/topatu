import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from lmfit import Parameters, minimize, report_fit

import numpy as np
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

def bound_roi(im : np.ndarray, mx = tuple, size : int = 200):
    """im : image in grayscale
       mx : tuple with the argmax of the im matrix
       size : 1/2*max size of the roi
       if size > mx: take bound to be 0 or im.shape[]"""
    bounds_roi = []
    for m in mx:
        if 0 < m - size:
            bounds_roi.append(m - size)
        else: bounds_roi.append(0)
        if m + size < im.shape[0]:
            bounds_roi.append(m + size)
        else: bounds_roi.append(im.shape[0])
    return bounds_roi

def guess_centroid(im : np.ndarray):
    return np.unravel_index(im.argmax(), im.shape)

def select_roi(im : np.ndarray, bounds : list) -> np.ndarray:
    return im[bounds[0] : bounds[1], bounds[2] : bounds[3]]

def plot_fit_result(im : np.ndarray, p0 : list, ax = None):
    """Plot gaussian center (p0[1], p0[2]) as a cross
    and a circle of radius p0[3]"""
    if ax == None : ax = plt.gca()
    pl = ax.imshow(im)#, cmap=plt.get_cmap('gray'))
    cross = ax.scatter(x=p0[1], y=p0[2], marker='x',
     color='r', label = '(%.1f, %.1f)' %(p0[1], p0[2]))

    circle = plt.Circle((p0[1], p0[2]), radius=p0[3], color='r', lw=1, fill=False,
     label = '$(\sigma_x, \sigma_y) = $ (%.1f, %.1f)' %(p0[3], p0[4]))
    ax.add_artist(circle)
    ax.legend([cross], ['(%.1f, %.1f)' %(p0[1], p0[2])])

def fitGauss2d(im : np.ndarray, p0 : list, mode: str = 'waist'):
    """Fit to 2D gaussian.
        mode: str = ['waist', 'ind']
            'waist': single sigma for r -> 2*r^2/w^2
            'ind': independent sigma for x/y -> 2*[ (x/sig_x)**2 + (y/sig_y)**2]
        p0: initial guess of parameters:
            [I0, x0, y0, w] for 'waist' mode
            [I0, x0, y0, sigma_x, sigma_y] for 'ind' mode
    """

    x = np.arange(0, im.shape[1], 1)
    y = np.arange(0, im.shape[0], 1)

    xx, yy = np.meshgrid(x , y)

    def gaussian2D(x, y, cen_x, cen_y, sig_x, sig_y, offset):
        """Gaussian beam intensity, 2 sigma parametrization"""
        return np.exp(-2.0*(((cen_x-x)/sig_x)**2 + ((cen_y-y)/sig_y)**2)) + offset

    def gaussian2DWaist(x, y, cen_x, cen_y, w, offset):
        """Gaussian beam intensity, waist parametrization"""
        return np.exp(-2.0*((cen_x-x)**2 + (cen_y-y)**2)/w**2) + offset

    def residuals(p, x, y, z, mode: str = mode):
        height = p["height"].value
        cen_x = p["centroid_x"].value
        cen_y = p["centroid_y"].value
        if mode == 'ind':
            sigma_x = p["sigma_x"].value
            sigma_y = p["sigma_y"].value
        elif mode == 'waist':
            w = p["waist"].value
        offset = p["background"].value
        return (z - height*gaussian2D(x,y,
                                      cen_x, cen_y, sigma_x, sigma_y, offset)) if mode == 'ind'  else (z - height*gaussian2DWaist(x,y,
                                                                                                                cen_x, cen_y, w, offset))
    initial = Parameters()
    initial.add("height",value=p0[0])
    initial.add("centroid_x",value=p0[1])
    initial.add("centroid_y",value=p0[2])
    if mode == 'ind':
        initial.add("sigma_x",value=p0[3])
        initial.add("sigma_y",value=p0[4])
    elif mode == 'waist':
        initial.add("waist",value=(p0[3] + p0[4])/2)
    else:
        print('Select one of the available modes: "waist" or "ind" ')
        return 0

    initial.add("background",value=0)

    fit = minimize(residuals, initial, args=(xx, yy, im, mode))#, method='cg')
    return fit

def make_params(fit):
    par = []
    for k in fit.params.keys():
        par.append(fit.params[k].value)
        print("{} = {}".format(k, fit.params[k].value))
    return par

def fitGausRowCol(im : np.ndarray, mx : tuple, flag_p : bool = False):
    """Fit a gaussian on the (row, column) of im specified by mx
    Can be used to guess sigma_x and sigma_y"""
    def gauss(x, *p):
        A, mu, sigma, B = p
        return A *  np.exp(-( x-mu )**2 / (2.*sigma**2)) + B
    from peakutils import baseline
    bl = np.average(baseline(imroi[mxroi[0], :]))
    from scipy.optimize import curve_fit
    yrow = im[mx[0], :]
    xrow = range(len(yrow))
    prow0 = [yrow.max(), np.argmax(yrow), 10, bl]
    fitrow, _ = curve_fit(gauss, xrow, yrow, p0 = prow0)

    ycol = im.T[mx[1], :]
    xcol = range(len(ycol))
    pcol0 = [ycol.max(), np.argmax(ycol), 10, bl]
    fitcol, _ = curve_fit(gauss, xcol, ycol, p0=pcol0)
    if flag_p: plotProfiles(yrow, ycol, fitrow, fitcol)
    return fitcol, fitrow

def plotProfiles(yrow, ycol, fitr, fitc):
    fig, ax = plt.subplots(1, 2, figsize=(16,8))
    ax[0].plot(ycol)
    xpl = range(len(ycol))
    ax[0].plot(gauss(xpl, *fitc), label = '$\sigma = $ %.1f' %fitc[2])
    ax[0].set_title("X profile")
    ax[0].legend(fontsize=12)

    ax[1].plot(yrow)
    xpl2 = range(len(yrow))
    ax[1].plot(gauss(xpl2, *fitr), label = '$\sigma = $ %.1f' %fitr[2])
    ax[1].set_title("Y profile")
    ax[1].legend(fontsize=12)

def zoom_out(pars : list, bounds : list):
    """Shift fit centroid back by the bounds offset to recover position in original image"""
    newc = [p + s for p, s in zip(pars[1:3], bounds[2::-2])]
    from copy import deepcopy
    newp = deepcopy(pars)
    newp[1:3] = newc
    return newp

def fit2dGauss(im : np.ndarray, DEBUG : bool = False, flag_p : bool = True) :
    """Fit 2d gaussian to an RGB image, perform ROI selection, parameter setting
    DEBUG flag shows whole process, flag_p shows final result"""
#     img = rgb2gray(im)
    mx = guess_centroid(im)
    bounds = bound_roi(im, mx, 500)
    imroi = select_roi(im, bounds)

    mxroi = guess_centroid(imroi)
    flp = False
    if DEBUG:
        flp = True
        pl = plt.imshow(imroi)#, cmap=plt.get_cmap('gray'))
        plt.scatter(mx[1] - bounds[2], mx[0] - bounds[0], marker='x', color='r')

    # Guess sigmas

    fitr, fitc = fitGausRowCol(imroi, mxroi, flag_p=flp)
    sigma_x = fitc[2]
    sigma_y = fitr[2]

    p0 = [imroi.max(), mxroi[1], mxroi[0], sigma_x, sigma_y]
    if DEBUG:
        plot_fit_result(imroi, p0)
        plt.title('Initial parameter guess')

    # Fit to 2dGaussian

    fit = fitGauss2d(imroi, p0 = p0)

    pars = make_params(fit)
    if DEBUG:
        plot_fit_result(imroi, pars)
        plt.title('Fit result')

    #  Zoom out of ROI

    newp = zoom_out(pars, bounds)
    if flag_p:
        plot_fit_result(im, newp)
        plt.title('Fit result zoomed out')
    return newp
