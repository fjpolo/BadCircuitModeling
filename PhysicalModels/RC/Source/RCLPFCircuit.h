/*
  ==============================================================================

    RCLPFCircuit.h
    Created: 9 Jun 2021 12:17:25pm
    Author:  fjpolo@gmail.com

    https://jatinchowdhury18.medium.com/bad-circuit-modelling-episode-1-component-tolerances-3ffdbe4e980c

  ==============================================================================
*/

#pragma once

/**
* \brief Includes
*/
#include "RCElement.h"

/**
* \class RCLPFCircuit
*
* \brief
*/
class RCLPFCircuit
{
public:
    RCElement R1;
    RCElement C1;
    RCLPFCircuit() :
        R1(1000.0f),           // Fixed
        C1((float)3.3e-8)      // 
    {}

    void setTolerance(int tol)
    {
        Tolerance tolerance = static_cast<Tolerance> (tol);
        R1.setTolerance(tolerance);
        C1.setTolerance(tolerance);
    }

    void setFreq(float freq)
    {
        /*Set C1*/
        auto wc = juce::MathConstants<float>::twoPi * freq;
        C1.setValue((float)(1.0f / ( R1.getValue() * wc)));
    }

    float getActualFreq()
    {
        /**
        *   wc = 1/RC ^ wp = 2*pi*fc -> fc = 1/2*pi*RC
        */
        return (float)(1/ juce::MathConstants<float>::twoPi * R1.getValue() * C1.getValue());
    }


private:

    /**/
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(LPFCircuit)
};