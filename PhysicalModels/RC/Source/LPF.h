/*
  ==============================================================================

    LPF.h
    Created: 9 Jun 2021 1:02:39pm
    Author:  fjpolo@gmail.com

    https://jatinchowdhury18.medium.com/bad-circuit-modelling-episode-1-component-tolerances-3ffdbe4e980c

  ==============================================================================
*/

#pragma once

/**
* \brief Includes
*/
#include "RCLPFCircuit.h"
#include "JuceHeader.h"
#include <cmath>
#include <complex>

/**
* \class RCLPFCircuit
*
* \brief
*/
class LPF {
public:
    LPF() : RCLPF()
    {}
    virtual ~LPF() {}
    virtual void setFreq(float freq) {
        RCLPF.setFreq(freq);
        if (freq != fc.getTargetValue()) {
            fc.setTargetValue(juce::jmin(freq, fs / 2.0f - 50.0f));
        }
    }
    void calcCoefs(float currFc)
    {
        float T = 1 / fs;
        a = exp( -T / (RCLPF.R1.getValue() * RCLPF.C1.getValue()) );
        b = 1 - a;
    }
    virtual void reset(float sampleRate)
    {
        fs = sampleRate;
        for (int n = 0; n < 2; ++n)
            z[n] = 0.0f;
        calcCoefs(fc.skip(smoothSteps));
    }
    virtual void processBlock(float* buffer, const int numSamples) {
        for (int n = 0; n < numSamples; ++n)
        {
            if (fc.isSmoothing() || Q.isSmoothing())
                calcCoefs(fc.getNextValue());
            buffer[n] = processSample(buffer[n]);
        }
    }
    float processSample(float x) {
        float y = z[1] + x * b;
        z[1] = x * a;
        return y;

    }
    virtual float getMagnitudeAtFreq(float freq) {
        std::complex <float> s(0, freq / fc.getTargetValue()); // s = j (w / w0)
        auto numerator = b;
        auto denominator = s - a * s;
        return abs(numerator / denominator);
    }
protected:
    juce::SmoothedValue<float, juce::ValueSmoothingTypes::Multiplicative> fc = 1000.0f;

private:
    RCLPFCircuit RCLPF;
    enum
    {
        smoothSteps = 200,
    };
    float fs = 44100.0f;
    float a;
    float b;
    float z[2]{1.0f, 0.0f};

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(LPF)
};