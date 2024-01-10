import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as color
from scipy import constants, fft
#import time
import pandas as pd
import matplotlib.animation as animation
from tqdm import tqdm
import types



class w_packet:
    """
    Class representing a wave packet

    ...

    Attributes
    ----------
    freqs : array/list
        Frequencies contained in the packet.
    amplitudes : array/list
        Amplitudes associated to the frequencies.
    disp : list
        Function describing the dispersion relation and its optional arguments
        
    Methods
    -------
    display_components_df(**kwargs)
    generate_wave_x(x, t, **kwargs)
    generate_wave_t(t, x, **kwargs)
    wave(axis, **kwargs)
    animate(d, step, xx, **kwargs)
    power_spectrum(t, x)
    """
    def __init__(self, f, A, k, **kwargs):
        """
        Wave packet constructor.

        Parameters
        ----------
        f : array/list
            Frequencies of the packet.
        A : array/list
            Amplitudes associated to the frequencies.
        k : function
            Function desribing the dispersion relation of the package.
        **kwargs : float
            Optional arguments for the dispersion relation. Name them as they are named 
            in the definition of the function k.

        Returns
        -------
        None.
        """
        if len(f) != len(A):
            raise AttributeError("Make sure that the arrays of frequencies and amplitudes have the same sizes")
            return
        self.freqs = f 
        self.amplitudes = A 
        self.disp = [k] #dispersion relation of the packet
        for key, value in kwargs.items():
           self.disp.append(value) #optional arguments for the dispersion relation

    def display_components_df(self, **kwargs):
        """
        This method prints a dataframe displaying frequencies and amplitudes of the packet
        
        Parameters
        ----------
        **kwargs : 
            order: string
            - if order = 'freq' the df is shown in the order of increasing frequencies
            - if order = 'ampl' the df is shown in the order of decreasing amplitudes
            - default: 'freq'

        Returns
        -------
        None.
        """
        if len(self.freqs) == 0:
            raise AttributeError("Make sure that the arrays of the frequencies and the amplitudes are not empty")
            return
        indices = np.argsort(self.freqs)
        for key, value in kwargs.items():
            if key == 'order':
                if value == 'freq':
                    break
                elif value == 'ampl':
                    indices = np.argsort(self.amplitudes)[::-1]
                else:
                    raise AttributeError("{} is not a valid order".format(value))
                    return
        df = pd.DataFrame(columns = ['Frequencies (Hz)', 'Amplitudes (a.u.)'])
        df['Frequencies (Hz)'] = self.freqs[indices]
        df['Amplitudes (a.u.)'] =self.amplitudes[indices]
        print(df)
               
    def generate_wave_x(self, x, t, **kwargs):
        """
        This method calculates the sampled waveform of the packet along the x-axis by adding 
        up all the cosine functions with the frequencies and the aplitudes belonging to the 
        object. 

        Parameters
        ----------
        x : array
            Array containing the samples along the x-axis where the wave has to be
            calculated.
        t : float
            Fixed instant at which the wave has to be calculated.
        **kwargs : 
            progress: bool
            If progress = True, a progress bar from tqdm is shown while the wave is being calculated, otherwise it's not.
            Default: True

        Returns
        -------
        wf : array
            Array containing the calculated sampled wave packet.
        """
        if (len(self.freqs) == 0) or (len(self.amplitudes) == 0):
            raise AttributeError("Make sure you generated the frequencies and the amplitudes before generating the waveform")
            return 
        
        if ('progress' not in kwargs) or (kwargs['progress'] == True):
            print('Generating the wave...')
            interval = tqdm(range(0, len(self.freqs)))
        if 'progress' in kwargs:
            if kwargs['progress'] == False:
                interval = range(0, len(self.freqs))

        k = self.disp[0](self.freqs, *self.disp[1:])

        wf = np.zeros(len(x))
        
        for i in interval:
            wf = wf + self.amplitudes[i] * np.cos(k[i] * x - 2 *  np.pi * self.freqs[i] * t)
        return wf

        
    def generate_wave_t(self, t, x, **kwargs):
        """
        This method calculates the sampled waveform of the packet along the t-axis by adding 
        up all the cosine functions with the frequencies and the aplitudes belonging to the 
        object. 

        Parameters
        ----------
        t : array
            Array containing the samples along the t-axis where the wave has to be 
            calculated.
        x : float
            Fixed position at which the wave has to be calculated.
        **kwargs : 
            progress: bool
            If progress = True, a progress bar from tqdm is shown while the wave is being calculated, otherwise it's not.
            Default: True

        Returns
        -------
        wf : array
            Array containing the calculated sampled wave packet.
        """
        if (len(self.freqs) == 0) or (len(self.amplitudes) == 0):
            raise AttributeError("Make sure you generated the frequencies and the amplitudes before generating the wave")
            return 
        
        if ('progress' not in kwargs) or (kwargs['progress'] == True):
            print('Generating the wave...')
            interval = tqdm(range(0, len(self.freqs)))      
        if 'progress' in kwargs:
            if kwargs['progress'] == False:
                interval = range(0, len(self.freqs))
                
        k = self.disp[0](self.freqs, *self.disp[1:])
        
        
        wf = np.zeros(len(t))
        for i in interval:
            wf = wf + self.amplitudes[i] * np.cos(k[i] * x - 2 *  np.pi * self.freqs[i] * t)
        return wf
        
        
    def wave(self, axis, **kwargs):
        """
        This method calls the previous two methods to generate and plot the waveform along
        the specified axis. 

        Parameters
        ----------
        axis : string
            - if axis = 'x' the waveform is generated and plotted with respect to the x-axis
            - if axis = 't' the waveform is generated and plotted with respect to the t-axis
        **kwargs : 
            x: array (if axis = 'x'), float (if axis = 't')
                x samples (if axis = 'x'), fixed position (if axis = 't')
            t: array (if axis = 't'), float (if axis = 'x')
                t samples (if axis = 't'), fixed instant (if axis = 'x')
            ymax: float
                Absolute value of highest and lowest y shown in the plot. 
                Default: no ylim set
            color: string
                Color of the plot. Default: teal
        Returns
        -------
        y_plot : array
            Array containing the calculated sampled wave packet.

        """
        if axis == 'x': 
            if 'x' not in kwargs:
                raise AttributeError("Missing x axis")
                return
            if 't' not in kwargs:
                raise AttributeError("Missing instant t")
                return
            x_plot = kwargs['x']
            x_lab = 'x (m)'
            title = 'Wave packet at t = {} s'.format(kwargs['t'])
            y_plot = self.generate_wave_x(x_plot, kwargs['t'])
        elif axis == 't': 
            if 't' not in kwargs:
                raise AttributeError("Missing t axis")
                return
            if 'x' not in kwargs:
                raise AttributeError("Missing point x")
                return
            x_plot = kwargs['t']
            x_lab = 't (s)'
            title = 'Wave packet at x = {} m'.format(kwargs['x'])
            y_plot = self.generate_wave_t(x_plot, kwargs['x'])
        else:
            raise AttributeError("{} is not a valid axis".format(axis))
            return 
        plt.figure(figsize = (10,5))
        col = 'teal'
        if 'color' in kwargs:
            col = kwargs['color']
        plt.plot(x_plot, y_plot, color = col)
        plt.xlabel(x_lab)
        plt.ylabel('Amplitude (a.u.)')
        plt.title(title)
        if 'ylim' in kwargs:
            plt.ylim((-abs(kwargs['ylim']), abs(kwargs['ylim'])))
        plt.show()  
        return y_plot
        
        
    def animate(self, d, step, xx, **kwargs):
        """
        This method generates an animation of the time evolution of the packet

        Parameters
        ----------
        d : float
            Duration of the animation (last instant plotted).
        step : float
            Time interval between the instants of two consecutive frames.
        xx : array
            Array containing the samples along the x-axis where the animated wave has to be
            plotted.
        **kwargs : 
            save: bool
                If save = True, the animation is saved, otherwise it is not.
            pathname: string
                Pathname of the location where the animation has to be saved.

        Returns
        -------
        None.

        """
        if 'save' in kwargs:
            if (kwargs['save'] == True) and ('pathname' not in kwargs):
                raise AttributeError("Missing pathname")
                return
        num = int(d/step) + 1
        instants = np.linspace(0, d, num)
        fig, ax = plt.subplots(figsize = (10,5))
        ims = []
        yy = self.generate_wave_x(xx, 0, progress = False)
        im, = ax.plot(xx, yy, animated=True, color = 'teal')
        ims.append([im,])
        ymax = max(np.abs(yy))
        print("Generating the animation...")
        for tt in tqdm(instants[1:]):
            yy = self.generate_wave_x(xx, tt, progress = False)
            im, = ax.plot(xx, yy, animated=True, color = 'teal')
            ims.append([im,])


        ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                        repeat_delay=1000)

        if 'save' in kwargs:
            if (kwargs['save'] == True) and ('pathname' in kwargs):
                ani.save(kwargs['pathname'])

        ax.set_ylim((-abs(ymax), abs(ymax)))
        ax.set_ylabel('Amplitude (a.u.)')
        ax.set_xlabel('x (m)')
        plt.show()
        
    def power_spectrum(self, t, x, **kwargs):
        """
        This method uses scipy.fft methods rfft and rfftfreqs to calculate the DFT of the 
        packet with respect to the t-axis. It calculates the powers and, if requested,
        it plots the power spectrum.

        Parameters
        ----------
        t : array
            Time samples where the packet is calculated.
        x : float
            Fixed position where the packet is calculated.
        **kwargs : 
            plot: bool
                If plot = True, a plot of the power spectrum is generated.
                
        Returns
        -------
        fftfreqs : array
            Frequencies of the DFT of the packet.
        ffts : array
            Samples of the Fourier transform of the packet.
        powers : array
            Squared modules of the samples of the Fourier transform of the packet.
        """
        y = self.generate_wave_t(t, x, progress = False)
        ffts = fft.rfft(y, n = len(y))
        fftfreqs = fft.rfftfreq(len(t), d = t[1] - t[0])
        powers = np.absolute(ffts) ** 2
        if 'plot' in kwargs:
            if kwargs['plot'] == True:
                plt.figure(figsize = (10,5))
                plt.plot(fftfreqs, powers, color = 'crimson')
                plt.title('Power spectrum at x = {} m'.format(x))
                plt.xlabel('f (Hz)')
                plt.ylabel('Power (a.u.)')
                plt.xlim((0, 5))
                plt.show()
        return fftfreqs, ffts, powers



