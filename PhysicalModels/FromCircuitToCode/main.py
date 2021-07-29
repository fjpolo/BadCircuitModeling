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
# Constants
#
NUM_POINTS = 100


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
class DiodeClipper:
    """Models a diode clipper"""
    def __init__(self, _is1, _is2, _vt1, _vt2, _gr1):
        self.is1 = _is1
        self.is2 = _is2
        self.vt1 = _vt1
        self.vt2 = _vt2
        self.gr1 = _gr1
    def ticker(self, input):
        """Calculates V2 vor a given input"""
        v1 = input
        v2 = 0

        for it in range(500):
            vd1 = (0 - v2)
            ed1 = math.exp(vd1 / self.vt1)
            id1 = self.is1 * ed1  - self.is1
            gd1 = self.is1 * ed1 / self.vt1
            id1eq = id1 - (gd1 * vd1)


            vd2 = (v2 - 0)
            ed2 = math.exp(vd2 / self.vt2)
            id2 = self.is2 * ed2 - self.is2
            gd2 = self.is2 * ed2 / self.vt2
            id2eq = id2 - (gd2 * vd2)

            v2 = (id1eq - id2eq + self.gr1 * v1) / (gd1 + gd2 + self.gr1)
        return v2

# 
class RC_LPF:
    """Models a 1 pole LP linear filter"""
    def __init__(self, _r1, _m, _c1, _sr):
        self.gr1 = (1/_r1)
        self.m = _m
        self.minv = 1/_m
        self.sr = _sr
        self.gc1 = _c1 * self.sr * self.minv
        self.ic1eq = 0
        self.v2 = 0
    
    def ticker(self, v1):
        """Calculates v2 vor a given input v1.-"""

        v2 = (self.gr1*v1 + self.ic1eq) / (self.gr1 + self.gc1)
        self.ic1eq += self.minv * (self.gc1 * v2 - self.ic1eq)
        return v2

# 
class RC_HPF:
    """Models a 1 pole HP linear filter"""
    def __init__(self, _r1, _m, _c1, _sr):
        self.gr1 = (1/_r1)
        self.m = _m
        self.minv = 1/_m
        self.sr = _sr
        self.gc1 = _c1 * self.sr * self.minv
        self.ic1eq = 0
        self.v2 = 0
    
    def ticker(self, v1):
        """Calculates v2 vor a given input v1.-"""

        v2 = (self.gc1*v1 + self.ic1eq) / (self.gc1 - self.gr1)
        self.ic1eq += self.minv * (self.gc1 * (-v2) - self.ic1eq)
        return v2

#
class RC_HPF_LPF:
    """Models a 1 pole HPF 1 pole LPF linear"""
    def __init__(self, _gr1, _gr2, _m, _gc1, _gc2, _ic1eq, _ic2eq, _sr):
        self.gr1 = _gr1
        self.gr2 = _gr2
        self.m = _m
        self.minv = 1/_m
        self.sr = _sr
        self.gc1 = _gc1 * self.sr * self.minv
        self.gc2 = _gc2 * self.sr * self.minv
        self.ic1eq = _ic1eq
        self.ic2eq = _ic2eq
        self.v3 = 0
        self.v2 = 0

    def ticker(self, input):
        """Calculates V2 vor a given input"""
        v1 = input
        v3 = (self.gc1 * self.ic2eq + self.gr1 * (self.ic1eq + self.ic2eq + self.gc1 * v1) ) / (self.gr1 * (self.gc2 + self.gr2) + self.gc1 * (self.gc2 + self.gr1 + self.gr2) ) 
        v2 = (self.gr1 * v1 + self.gc1 * v3 - self.ic1eq ) / (self.gc1 + self.gr1)
      
        self.ic1eq += self.minv * (self.gc1 * (v3 - v2) - self.ic1eq)
        self.ic2eq += self.minv * (self.gc2 * (v3 - 0) - self.ic2eq)

        return v3

#
class FullDiodeClipper:
    """Models a 1 pole HPF 1 pole LPF linear + Diode clipper"""
    def __init__(self, _gr1, _gr2, _m, _sr, _gc1, _gc2, _is1, _is2, _vt1, _vt2):
        self.gr1 = _gr1
        self.gr2 = _gr2
        self.m = _m
        self.minv = 1/self.m
        self.sr = _sr
        self.gc1 = _gc1 * self.sr * self.minv
        self.gc2 = _gc2 * self.sr * self.minv
        self.is1 = _is1
        self.is2 = _is2
        self.vt1 = _vt1
        self.vt2 = _vt2
        self.ic1eq = 0
        self.ic2eq = 0

    def ticker(self, input):
        """Calculates Vo vor a given Vi"""
        v1 = input
        v2 = 0
        v3 = 0
        
        for it in range(20):
            # Diode 1
            vd1 = (0 - v3)
            ed1 = math.exp(vd1 / self.vt1)
            id1 = self.is1 * ed1  - self.is1
            gd1 = self.is1 * ed1 / self.vt1
            id1eq = id1 - (gd1 * vd1)
            # Diode 2
            vd2 = (v3 - 0)
            ed2 = math.exp(vd2 / self.vt2)
            id2 = self.is2 * ed2 - self.is2
            gd2 = self.is2 * ed2 / self.vt2
            id2eq = id2 - (gd2 * vd2)

            # Filter
            A = (self.ic1eq + self.ic2eq + id1eq - id2eq)
            B = self.gc1
            C = self.gc1 + self.gc2 + gd1 - gd2 + self.gr2
            v3 = ( B * v2 - A ) / C
            v2 = (self.gr1 * v1 + self.gc1 * v3 - self.ic1eq) / (self.gr1 + self.gc1)

        self.ic1eq += self.minv * (self.gc1 * (v3 - v2) - self.ic1eq)
        self.ic2eq += self.minv * (self.gc2 * (v3 - 0) - self.ic2eq)

        return v3


#
#
# Main
#
#
if __name__ == "__main__":

    #
    # Diode clipper
    #
    myDiodeClipper = DiodeClipper(_is1=1e-15, _is2=1e-15, _vt1=26e-3, _vt2=26e-3, _gr1=(1.0/(2.2e3)))
    vi = np.linspace(-10, 10, NUM_POINTS)
    vo = []
    for it in range(NUM_POINTS):
        vo_temp = myDiodeClipper.ticker(input=vi[it])
        vo.append(vo_temp)
    plt.figure()
    plt.title("Waveshaper: Diode Clipper")
    plt.plot(vi, vo)
    plt.xlabel("Vi[V]")
    plt.ylabel("Vo[V]")

    # Sawtooth
    t = np.linspace(0, 1, NUM_POINTS)
    sawtooth = 3.3 * signal.sawtooth(2 * np.pi * 5 * t)
    vo = []
    for it in range(NUM_POINTS):
        vo_temp = myDiodeClipper.ticker(input=sawtooth[it])
        vo.append(vo_temp)
    plt.figure()
    plt.plot(t, sawtooth)    
    plt.plot(t, vo)

    # #
    # # Filter part - LPF
    # #
    # LPfilter = RC_LPF( _r1=(220e3), _m=(1/2.0), _c1=(3.3e-8), _sr=500)
    # vo = []
    # for it in range(NUM_POINTS):
    #     vo_temp = LPfilter.ticker(v1=sawtooth[it])
    #     vo.append(vo_temp)
    # plt.figure()
    # plt.plot(t, sawtooth)    
    # plt.plot(t, vo)

    # #
    # # Filter part - HPF
    # #
    # HPfilter = RC_HPF( _r1=(1e3), _m=(1/2.0), _c1=(3.3e-8), _sr=500)
    # vo = []
    # for it in range(NUM_POINTS):
    #     vo_temp = HPfilter.ticker(v1=sawtooth[it])
    #     vo.append(vo_temp)
    # plt.figure()
    # plt.plot(t, sawtooth)    
    # plt.plot(t, vo)

    #
    # Filter part
    #
    filter = RC_HPF_LPF( _gr1=(1/4.7e3), _gr2=(1/6.8e3), _m=(1/2.0), _gc1=(0.47e-6), _gc2=(0.1e-6), _ic1eq=0, _ic2eq=0, _sr=5000)
    vo = []
    for it in range(NUM_POINTS):
        vo_temp = filter.ticker(input=sawtooth[it])
        vo.append(vo_temp)
    plt.figure()
    plt.plot(t, sawtooth)    
    plt.plot(t, vo)


    #
    # Full Circuit
    #

    # Input
    sawtooth1 = 10 * signal.sawtooth(2 * np.pi * 5 * t)
    sawtooth2 = 5 * signal.sawtooth(2 * np.pi * 5 * t)
    sawtooth3 = 3.3 * signal.sawtooth(2 * np.pi * 5 * t)
    sawtooth4 = 2 * signal.sawtooth(2 * np.pi * 5 * t)
    sawtooth5 = 1 * signal.sawtooth(2 * np.pi * 5 * t)
    sawtooth6 = 0.7 * signal.sawtooth(2 * np.pi * 5 * t)

    # Filter objects
    filter1 = RC_HPF_LPF( _gr1=(1/4.7e3), _gr2=(1/6.8e3), _m=(1/2.0), _gc1=(0.47e-6), _gc2=(0.1e-6), _ic1eq=0, _ic2eq=0, _sr=5000)
    filter2 = RC_HPF_LPF( _gr1=(1/4.7e3), _gr2=(1/6.8e3), _m=(1/2.0), _gc1=(0.47e-6), _gc2=(0.1e-6), _ic1eq=0, _ic2eq=0, _sr=5000)
    filter3 = RC_HPF_LPF( _gr1=(1/4.7e3), _gr2=(1/6.8e3), _m=(1/2.0), _gc1=(0.47e-6), _gc2=(0.1e-6), _ic1eq=0, _ic2eq=0, _sr=5000)
    filter4 = RC_HPF_LPF( _gr1=(1/4.7e3), _gr2=(1/6.8e3), _m=(1/2.0), _gc1=(0.47e-6), _gc2=(0.1e-6), _ic1eq=0, _ic2eq=0, _sr=5000)
    filter5 = RC_HPF_LPF( _gr1=(1/4.7e3), _gr2=(1/6.8e3), _m=(1/2.0), _gc1=(0.47e-6), _gc2=(0.1e-6), _ic1eq=0, _ic2eq=0, _sr=5000)
    filter6 = RC_HPF_LPF( _gr1=(1/4.7e3), _gr2=(1/6.8e3), _m=(1/2.0), _gc1=(0.47e-6), _gc2=(0.1e-6), _ic1eq=0, _ic2eq=0, _sr=5000)
    
    # Vo
    vo1 = []
    vo2 = []
    vo3 = []
    vo4 = []
    vo5 = []
    vo6 = []
    
    # Output
    for it in range(NUM_POINTS):
        vo_temp = filter1.ticker(input=sawtooth1[it])
        vo_temp = myDiodeClipper.ticker(input=vo_temp)
        vo1.append(vo_temp)
        vo_temp = filter2.ticker(input=sawtooth2[it])
        vo_temp = myDiodeClipper.ticker(input=vo_temp)
        vo2.append(vo_temp)
        vo_temp = filter3.ticker(input=sawtooth3[it])
        vo_temp = myDiodeClipper.ticker(input=vo_temp)
        vo3.append(vo_temp)
        vo_temp = filter4.ticker(input=sawtooth4[it])
        vo_temp = myDiodeClipper.ticker(input=vo_temp)
        vo4.append(vo_temp)
        vo_temp = filter5.ticker(input=sawtooth5[it])
        vo_temp = myDiodeClipper.ticker(input=vo_temp)
        vo5.append(vo_temp)
        vo_temp = filter6.ticker(input=sawtooth6[it])
        vo_temp = myDiodeClipper.ticker(input=vo_temp)
        vo6.append(vo_temp)


    # Plot
    plt.figure()
    plt.plot(t, sawtooth)    
    plt.plot(t, vo1, label="Vi=10[V]")
    plt.plot(t, vo2, label="Vi=5[V]")
    plt.plot(t, vo3, label="Vi=3.3[V]")
    plt.plot(t, vo4, label="Vi=2[V]")
    plt.plot(t, vo5, label="Vi=1[V]")
    plt.plot(t, vo6, label="Vi=0.7[V]")
    plt.legend()

    # #
    # # Full Circuit
    # #
    # circuit = FullDiodeClipper(
    #     _gr1=(1.0/(2.2e3)), 
    #     _gr2=(1.0/(6.8e3)), 
    #     _m=(1/2.0), 
    #     _sr=(5000), 
    #     _gc1=(0.47e-6), 
    #     _gc2=(0.01e-6), 
    #     _is1=(1e-15), 
    #     _is2=(1e-15), 
    #     _vt1=(26e-3), 
    #     _vt2=(26e-3)
    #     ) 

    # vi = np.linspace(-5, 5, NUM_POINTS)
    # vo = []
    # for it in range(NUM_POINTS):
    #     vo_temp = circuit.ticker(input=vi[it])
    #     vo.append(vo_temp)
    # plt.figure()
    # plt.title("Waveshaper: LPF + HPF + Diode Clipper")
    # plt.plot(vi, vo)
    # plt.xlabel("Vi[V]")
    # plt.ylabel("Vo[V]")

    # t = np.linspace(0, 1, NUM_POINTS)
    # sawtooth = 3.3 * signal.sawtooth(2 * np.pi * 5 * t)  
    # vo = []
    # for it in range(NUM_POINTS):
    #     vo_temp = circuit.ticker(input=sawtooth[it])
    #     vo.append(vo_temp)
    # plt.figure()
    # plt.plot(t, sawtooth)    
    # plt.plot(t, vo)


    # Show plot
    plt.show()
