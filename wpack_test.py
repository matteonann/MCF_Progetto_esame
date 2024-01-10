import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as color
from scipy import constants, fft
#import time
import pandas as pd
import matplotlib.animation as animation
from tqdm import tqdm
import types
import argparse




# Frequency distributions


def dist_f_1(N):
    """
    Inverse cumulative function for the probability distribution of frequencies 
    p(f) = f/3 for f in [0, 2], 2/3(3-f) for f in (2, 3] 

    Parameters
    ----------
    N : int
        Number of frequencies to be generated.

    Returns
    -------
    inv_c_func : array
        Generated frequencies.

    """
    y = np.random.random(N)
    mask1 = (y >= 0) & (y <= 2/3)
    mask2 = (y > 2/3) & (y <= 1)
    inv_c_func = np.zeros(N)
    inv_c_func[mask1] = np.sqrt(6 * y[mask1])
    inv_c_func[mask2] = 3 - np.sqrt(3 * (1 - y[mask2]))
    return inv_c_func

def dist_f_2(N):
    """
    Inverse cumulative function for the probability distribution of frequencies 
    p(f) = f for f in [0, 3]

    Parameters
    ----------
    N : int
        Number of frequencies to be generated.

    Returns
    -------
    inv_c_func : array
        Generated frequencies.

    """
    y = np.random.random(N)
    inv_c_func = 3 * np.sqrt(y)
    return inv_c_func

# Amplitude distributions

def dist_A_1(N, f, a):
    """
    Inverse cumulative function for the probability distribution of amplitudes 
    p_f(A) = A for A in [0, a*sqrt(f)]

    Parameters
    ----------
    N : int
        Number of amplitudes to be generated.
    f : float/array
        Frequency/(frequencies) corresponding to the amplitudes to be generated.
    a : float
        Parameter of the distribution.

    Returns
    -------
    inv_c_func : array
        Generated amplitudes.

    """
    y = np.random.random(N)
    inv_c_func = a * np.sqrt(f * y)
    return inv_c_func


def dist_A_2(N, f):
    """
    Inverse cumulative function for the probability distribution of amplitudes 
    p_f(A) = (1+f)^3 A^2 for A in [0, 1/(1+f)]

    Parameters
    ----------
    N : int
        Number of amplitudes to be generated.
    f : float/array
        Frequency/(frequencies) corresponding to the amplitudes to be generated.

    Returns
    -------
    inv_c_func : array
        Generated amplitudes.

    """
    y = np.random.random(N)
    inv_c_func = (y ** (1/3)) / (1+f)
    return inv_c_func


# Dispersion relations 

def disp_1(f, c):
    """
    This function calculates the wave number k starting from the frequency f according to
    the dispersion relation w = sqrt(ck)

    Parameters
    ----------
    f : float/array
        Frequency.
    c : float
        Parameter of the dispersion relation.

    Returns
    -------
    k : float/array
        Wave number, k = (2 pi f)^2/c.

    """
    omega = 2 * np.pi * f
    k = (omega ** 2) /c
    return k

def disp_2(f, c):
    """
    This function calculates the wave number k starting from the frequency f according to
    the dispersion relation w = sqrt(ck^2)

    Parameters
    ----------
    f : float/array
        Frequency.
    c : float
        Parameter of the dispersion relation.

    Returns
    -------
    k : float/array
        Wave number, k = (2 pi f)/sqrt(c).

    """
    omega = 2 * np.pi * f
    k = omega / np.sqrt(c)
    return k

def disp_3(f, c):
    """
    This function calculates the wave number k starting from the frequency f according to
    the dispersion relation w = sqrt(ck^3)

    Parameters
    ----------
    f : float/array
        Frequency.
    c : float
        Parameter of the dispersion relation.

    Returns
    -------
    k : float/array
        Wave number, k = (2 pi f)^(2/3) / c^(1/3).

    """
    omega = 2 * np.pi * f
    k = (omega ** (2/3)) / (c ** (1/3))
    return k

def disp_4(f, b, c):
    """
    This function calculates the wave number k starting from the frequency f according to
    the dispersion relation w = sqrt(b+ck^2)

    Parameters
    ----------
    f : float/array
        Frequency.
    c : float
        Parameter of the dispersion relation.
    b : float
        Parameter of the dispersion relation.

    Returns
    -------
    k : float/array
        Wave number, k = sqrt((2 pi f)^2 - b) / c).

    """
    omega = 2 * np.pi * f
    k = np.sqrt((abs(omega ** 2 - b)) / (c))
    return k
#---------------------------------------


from wpack import w_packet


def parse_arguments():
    parser = argparse.ArgumentParser(
    description="Choosing freq/ampl distributions and dispersion relations",
    formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-fd', '--freq_dist', action='store', type=int, default=1, help=(
    "Frequency distribution. Choose from the following:\n"
    "1) p(f) = f/3 for f in [0, 2], 2/3(3-f) for f in (2, 3] (default)\n"
    "2) p(f) = 2/9 f for f in [0, 3]\n"
    ))
    parser.add_argument('-ad', '--ampl_dist', action='store', type=int,  default=1, help=(
    "Amplityde distribution. Choose from the following:\n"
    "1) p_f(A) = A for A in [0, a*sqrt(f)] (default)\n"
    "2) p_f(A) = (1+f)^3 A^2 for A in [0, 1/(1+f)]"))
    parser.add_argument('-dr', '--disp_rel', action='store', type=int,  default=2, help=(
    "Dispersion relation. Choose from the following:\n"
    "1) w = sqrt(ck)\n"
    "2) w = sqrt(ck^2) (default)\n"
    "3) w = sqrt(ck^3)\n"
    "4) w = sqrt(b+ck^2)"))
    return  parser.parse_args()






args = parse_arguments()
args = np.array([arg for arg in args.__dict__.values()])


# Generating the frequencies 
n_comp = input('How many frequencies and amplitudes do you want to generate? ')

if args[0] == 1:
    freq = dist_f_1(int(n_comp))
    x_freq_dist = np.arange(0, 3, 0.1)
    mask_xf_1 = x_freq_dist <= 2
    mask_xf_2 = x_freq_dist > 2
    freq_dist = np.zeros(len(x_freq_dist))
    freq_dist[mask_xf_1] = x_freq_dist[mask_xf_1]/3
    freq_dist[mask_xf_2] = 2/3 * (3 - x_freq_dist[mask_xf_2])
    
elif args[0] == 2:
    freq = dist_f_2(int(n_comp))
    func = dist_f_1
    x_freq_dist = np.arange(0, 3, 0.1)
    freq_dist = 2/9 * x_freq_dist

f_hist = input('Do you want to see the frequencies distribution histogram? [y/n] ')
if (f_hist != 'y') and (f_hist != 'n'):
    raise ValueError("'{}' is not a valid answer".format(f_hist))
if f_hist == 'y':
    bins = input('Please insert the number of bins you want to display: ')
    plt.figure(figsize = (10,5))
    plt.hist(freq, bins = int(bins), color = 'crimson', density = True, label = 'f dist.')
    plt.plot(x_freq_dist, freq_dist, color = 'teal', label = 'f. prob. dist.')
    plt.xlabel('f (Hz)')
    plt.ylabel('p(f)')
    plt.title('Frequencies distribution histogram (normalized)')
    plt.legend()
    plt.show()
    
# Generating the amplitudes
if args[1] == 1:
    ampl = dist_A_1(int(n_comp), freq, 1)

elif args[1] == 2:
    ampl = dist_A_2(int(n_comp), freq)

A_hist = input('Do you want to see the amplitudes distribution histogram? [y/n] ')
if (A_hist != 'y') and (A_hist != 'n'):
    raise ValueError("'{}' is not a valid answer".format(A_hist), density = True)
if A_hist == 'y':
    bins = input('Please insert the number of bins you want to display: ')
    plt.figure(figsize = (10,5))
    plt.hist(ampl, bins = int(bins), color = 'crimson')
    plt.xlabel('A (a. u.)')
    plt.ylabel('N. occurrencies')
    plt.title('Amplitudes distribution histogram')
    plt.show()


f_hist_w = input('Do you want to see the weighed frequencies distribution histogram? [y/n] ')
if (f_hist_w != 'y') and (f_hist_w != 'n'):
    raise ValueError("'{}' is not a valid answer".format(f_hist_w))
if f_hist_w == 'y':
    bins = input('Please insert the number of bins you want to display: ')
    plt.figure(figsize = (10,5))
    plt.hist(freq, bins = int(bins), weights = ampl, color = 'crimson')
    plt.xlabel('f (Hz)')
    plt.ylabel('N. occurrencies')
    plt.title('Frequencies distribution histogram')
    plt.show()
    


# Creating the packet


if args[2] == 1:
    packet = w_packet(freq, ampl, disp_1, c = 9e16)
    x_0 = np.arange(-1.5, 1.5, 0.005)*1e16
    x_evo = np.arange(-0.5, 2, 0.005)*1e17 #per durata animazione = 20 s
    #x_f = 1000000000
    #x_f = 10000000000000
    x_f = 1e16
    
elif args[2] == 2:
    packet = w_packet(freq, ampl, disp_2, c = 9e16)
    x_0 = np.arange(-1, 1, 0.005)*1e9
    x_evo = np.arange(-1, 7, 0.005)*1e9 #per durata animazione = 20 s
    x_f = 1e9

elif args[2] == 3:
    packet = w_packet(freq, ampl, disp_3, c = 9e16)
    x_0 = np.arange(-7, 7, 0.005)*1e6
    x_evo = np.arange(-3, 38, 0.005)*1e6 #per durata animazione = 20 s
    x_f = 1e6
    
elif args[2] == 4:
    packet = w_packet(freq, ampl, disp_4, b = -1000, c = 9e16)
    x_0 = np.arange(-2, 2, 0.005)*1e9
    x_evo = np.arange(-2, 40, 0.005)*1e9 #per durata animazione = 20 s
    x_f = 1e9
    

t = np.arange(-5, 5, 1/60)


    
    
# Plotting the packet along x-axis at t=0


packet.wave(axis = 'x', x = x_0, t=0)


# Displaying the components

comp = input('Do you want to print a dataframe of the freq. and amplitudes of the package? [y/n] ')
if (comp != 'y') and (comp != 'n'):
    raise ValueError("'{}' is not a valid answer".format(comp))
elif comp == 'y':
    order_df = input('Do you want them to be printed in the order of increasing frequencies [1] or decreasing amplitudes [2]? ')
    if (order_df != '1') and (order_df != '2'):
        raise ValueError("'{}' is not a valid answer".format(order_df))
    elif order_df == '1':
        order = 'freq'
    else:
        order = 'ampl'
    packet.display_components_df(order = order)
    
# Animating the time evolution of the packet

anim = input('Do you want to see the animation of the time evolution of the packet? [y/n] ')

if (anim != 'y') and (anim != 'n'):
    raise ValueError("'{}' is not a valid answer".format(anim))
elif anim == 'y':
    sv = False
    path = ''
    save = input('Do you want to save the animation? [y/n] ')
    if (save != 'y') and (save != 'n'):
        raise ValueError("'{}' is not a valid answer".format(save))
    elif save == 'y':
        sv = True
        path = input('Insert the pathname of the file you want to save. Please include the file name and the extension (.gif): ')

    packet.animate(20, 0.1, x_evo, save = sv, pathname = path)


# Plotting the Fourier power spectrum


spectrum = input('Do you want to see the Fourier power spectrum of the packet at x=0? [y/n] ')
if (spectrum != 'y') and (spectrum != 'n'):
    raise ValueError("'{}' is not a valid answer".format(spectrum))
elif spectrum == 'y':
    packet.wave(axis = 't', t = t, x=0)
    fftfreqs_0, ffts_0, powers_0 = packet.power_spectrum(t, 0, plot = True)
    
    #Plotting the real part 
    
    plt.figure(figsize = (10,5))
    plt.plot(fftfreqs_0, 2*abs(ffts_0.real)/len(t), color = 'crimson', label = 'Real part spectrum')
    plt.title('Real part spectrum at x = {} m'.format(0))
    plt.hist(freq, bins = 30, weights = ampl, color = 'teal', label = 'f dist. weighed hist.')
    plt.xlabel('f (Hz)')
    plt.ylabel('Real part (a.u.)')
    plt.xlim((0, 3))
    plt.legend()
    plt.show()



spectrum_x = input('Do you want to see the Fourier power spectrum of the packet at another position? [y/n] ')
if (spectrum_x != 'y') and (spectrum_x != 'n'):
    raise ValueError("'{}' is not a valid answer".format(spectrum_x))
elif spectrum_x == 'y':
    packet.wave(axis = 't', t = t, x=x_f)
    fftfreqs_x, ffts_x, powers_x = packet.power_spectrum(t, x_f, plot = True)
    
    
  
    comparison = input('Do you want to compare the power spectra at the two positions? [y/n] ')
    if (comparison != 'y') and (comparison != 'n'):
        raise ValueError("'{}' is not a valid answer".format(comparison))
    elif comparison == 'y':
    
        t = np.arange(-5, 15, 1/60) 
    
        fftfreqs_0, ffts_0, powers_0 = packet.power_spectrum(t, 0, plot = False)
        fftfreqs_x, ffts_x, powers_x = packet.power_spectrum(t, x_f, plot = False)
    
    
        plt.figure(figsize = (10,5))
        plt.plot(fftfreqs_0, powers_0, color = 'crimson', label = 'Power spectrum at x = 0 m', alpha = 0.5)
        plt.plot(fftfreqs_x, powers_x, color = 'teal', label = 'Power spectrum at x = {} m'.format(x_f), alpha = 0.5)
        plt.title('Comparison of the 2 power spectra')
        plt.xlabel('f (Hz)')
        plt.ylabel('Power (a.u.)')
        plt.xlim((0, 3))
        plt.legend()
        plt.show()
    

    








