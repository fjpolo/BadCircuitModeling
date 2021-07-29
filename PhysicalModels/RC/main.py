#
# Imports
#
from scipy import signal
from matplotlib import pyplot as plt
from matplotlib import style
from scipy import signal
import numpy as np
import math


#
# Private functions
#

# Plot PlotFreqResponse
def PlotFreqResponse(x, title):
    #
    # Plot fequency response
    #
    # fig = plt.figure()
    [freq, response] = signal.freqz(x)
    fig, pltArr = plt.subplots(2, sharex=True) 
    fig.suptitle(title)
    #Magnitude
    pltArr[0].plot((freq/math.pi), 20 * np.log10(np.abs(response)+1e-6))
    pltArr[0].set_title("Magnitude of Frequency Response")
    pltArr[0].set_xlabel('Normalized Frequency (xPi [rad/sample])')
    pltArr[0].set_ylabel("Magnitude [dB]")
    # Phase
    angles = np.unwrap(np.angle(response))
    pltArr[1].plot((freq/math.pi), angles)
    pltArr[1].set_title("Phase of Frequency Response")
    pltArr[1].set_xlabel('Normalized Frequency (xPi [rad/sample])')
    pltArr[1].set_ylabel("Angle [xPi [rad/sample]]")


#
#
# Main
#
#
if __name__ == "__main__":

    # https://www.dsprelated.com/showcode/199.php
    # https://www.beis.de/Elektronik/Filter/AnaDigFilt/1stOrderDigFilt.html

    # # # f = logspace(-1,5,500)
    # # # RC = 1/(2*pi*100)
    # # # w,Hs = signal.freqs([1/RC],[1,1/RC],2*pi*f)
    # # # a = exp(-1/(RC*2e5))
    # # # w,Hz = signal.freqz([1-a],[1, -a],2*pi*f/2e5)
    # # # semilogx(f,20*log10(abs(Hs)))
    # # # semilogx(f,20*log10(abs(Hz)))
    # # # axis([1e-1,1e5,-60,5])

    # # #
    # # # RLC LPF
    # # #
    # # fs = 44100  # sampling frequency
    # # fc = 5000  # corner frequency of the lowpass

    # # # coefficients of analog lowpass filter
    # # Qinf = 0.8
    # # sinf = 2*np.pi*fc
    # # C = 1e-6
    # # L = 1/(sinf**2*C)
    # # R = sinf*L/Qinf

    # # B = [0, 0, 1]
    # # A = [L*C, R*C, 1]

    # # # cofficients of digital filter
    # # T = 1/fs
    # # b = [T**2, 2*T**2, T**2]
    # # a = [(4*L*C+2*T*R*C+T**2), (-8*L*C+2*T**2), (4*L*C-2*T*R*C+T**2)]

    # # # compute frequency responses
    # # Om, Hd = signal.freqz(b, a, worN=1024)
    # # tmp, H = signal.freqs(B, A, worN=fs*Om)

    # # # plot results
    # # f = Om*fs/(2*np.pi)
    # # plt.figure(figsize=(10, 4))
    # # plt.semilogx(f, 20*np.log10(np.abs(H)),
    # #             label=r'$|H(j \omega)|$ of analog filter')
    # # plt.semilogx(f, 20*np.log10(np.abs(Hd)),
    # #             label=r'$|H_d(e^{j \Omega})|$ of digital filter')
    # # plt.xlabel(r'$f$ in Hz')
    # # plt.ylabel(r'dB')
    # # plt.axis([100, fs/2, -70, 3])
    # # plt.legend()
    # # plt.grid()

    # # # Show plots
    # # plt.show()




    #
    # 1st order RC LPF
    #
    fs = 192000
    fc = 200
    R1 = 1000
    f = np.logspace(-1,5,500)
    print(f"fs: {fs}[sps]")
    print(f"fc: {fc}[sps]")
    
    # C1
    C1 = 1 / (2 * math.pi * R1 * fc)
    print(f"R1: {R1}[R]")
    print(f"C1: {C1}[F]")

    # RC
    RC = R1 * C1
    print(f"RC: {RC}[R.F]")

    # T 
    T = 1/fs
    Tao = T/2 * math.pi

    

    # SImple
    G = 1
    b_simple = [1, 0]
    a_simple = [1, 0]
    b_simple[0] = G / (Tao*fs)
    b_simple[1] = 0
    a_simple[0] = 1
    a_simple[1] = b_simple[0] - 1

    # Bilinear
    w = 1/RC
    # Prewarped coefficient for Bilinear transform
    A = 1 / (math.tan((w*T) / 2))
    # LPF
    b_bilinear = [1, 0]
    a_bilinear = [1, 0]
    b_bilinear[0] = 1 / (1+A)
    b_bilinear[1] = b_bilinear[0]
    a_bilinear[1] = (1-A) / (1+A)



    # S domain
    w,Hs = signal.freqs([1/RC],[1,1/RC],2*math.pi*f)
    # print(f"Hs: {Hs}")

    # Z domain
    freq, Hz_simple = signal.freqz(b_simple, a_simple, 2*math.pi*f/fs)
    freq, Hz_bilinear = signal.freqz(b_bilinear, a_bilinear, 2*math.pi*f/fs)
    # print(f"Hz: {Hz_simple}")

    # Plot
    plt.figure()
    plt.semilogx(f,20*np.log10(abs(Hs)), label='S')
    plt.semilogx(f,20*np.log10(abs(Hz_simple)), label='Z simple')
    plt.semilogx(f,20*np.log10(abs(Hz_bilinear)), label='Z bilinear')
    plt.axis([1e-1,1e5,-60,5])
    plt.xlabel('Frequency[Hz]')
    plt.ylabel('Frequncy Response - Magnitude[dB]')
    plt.title('Frequency Response')
    plt.legend()

    #
    # with tolerances
    #
    

    plt.show()
