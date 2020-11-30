"""The following functions handle filenames and extract characteristics of the measurements:
 exposure time and excitation power"""
def extract_p_texp(f):
    texp = re.search('_\d+ms_', f).group(0).replace('ms', '').replace('_', '')

    try:
        pi = re.search('_\d+p\d+mW_', f).group(0).replace('mW', '').replace('_', '').replace('p', '.')
    except AttributeError:
        pi = re.search('_\d+mW_', f).group(0).replace('mW', '').replace('_', '')
    return texp, pi

def extract_pstr(f):
    try:
        pi = re.search('_\d+p\d+mW_', f).group(0)
    except AttributeError:
        pi = re.search('_\d+mW_', f).group(0)
    return pi

"""These functions classify a list of files by the properties extracted above"""

def get_pi_texps(files: list)->(list,list):
    """Extract unique (not repeated) incident P and exposure times from filenames
    input:
        files: list with the names of files to look into
    output:
        pi_list: list with unique incident powers (in mW)
        texps: list with unique exposure times"""
    texp0, pi0 = extract_p_texp(files[0])

    texps = [float(texp0)]
    pi_list = [float(pi0)]

    for i,f in enumerate(files):

        texp, pi = extract_p_texp(f)

        if float(pi) != pi_list[-1]:
            pi_list.append(float(pi))
            texps.append(float(texp))
    return pi_list, texps

def get_pi_str(files:list)-> list:
    """Get incident powers as list of strings (ex '_197p3mW_')"""
    pi0 = extract_pstr(filesFBIBa[0])

    pi_str = [pi0]

    for i,f in enumerate(filesFBIBa):

        pi = extract_pstr(f)

        if pi != pi_str[-1]:
            pi_str.append(pi)
    return pi_str

def avg_imgs_by_pi(files: list, pi_str: list)->list:
    """Average images in files (list) classified by identical incident power from pi_str"""

    im0 = plt.imread(files[0]).astype(int)
    im_pwr = []
    texps = []
    pi_list = []

    for pi in pi_str:
        n_im = 0
        im_p = np.zeros_like(im0)
        for f in files:
            if pi in f:
                im_p += plt.imread(f).astype(int)
                n_im += 1
        im_pwr.append(im_p/n_im)
    return im_pwr

"""The following functions deal with masks"""

def guess_centroid(im : np.ndarray):
    return np.unravel_index(im.argmax(), im.shape)

def create_circular_mask(h, w, center=None, radius=None):

    if center is None: # use the middle of the image
        center = (int(w/2), int(h/2))
    if radius is None: # use the smallest distance between the center and image walls

        radius = min(center[0], center[1], w-center[0], h-center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    mask = dist_from_center <= radius
    return mask

def mask_image(im: np.array, mask: np.array) -> np.array:
    masked = im.copy()
    masked[~mask] = 0
    return masked

def circular_roi(im: np.array, radius: int = 120)-> np.array:
    """Create a circular mask around the intensity maximum of im with specified radius
    and return the masked image"""
    mx = guess_centroid(im)
    mask = create_circular_mask(im.shape[0], im.shape[1], center=(mx[1], mx[0]), radius=radius)
    return mask_image(im, mask)
