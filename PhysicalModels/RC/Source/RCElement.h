/*
  ==============================================================================

    Element.h
    Created: 9 Jun 2021 12:04:52pm
    Author:  fjpolo@gmail.com

    https://jatinchowdhury18.medium.com/bad-circuit-modelling-episode-1-component-tolerances-3ffdbe4e980c

  ==============================================================================
*/

#pragma once

#include "JuceHeader.h"
#include <random>
#include <chrono> 

/**
* \enum Tolerance
*
* \brief
*/
enum class Tolerance
{
    Ideal,
    PointOne,
    PointFive,
    One,
    Five,
    Ten,
    Twenty,
};

/**
* \class MyRandomGenerator
*
* \brief
*/
class MyRandomGenerator : public std::default_random_engine
{
public:
    MyRandomGenerator()
    {
        seed(std::chrono::system_clock::now().time_since_epoch().count());
    }
};

/**
* \class RCElement
*
* \brief
*/
class RCElement
{
public:
    RCElement(float value) :
        idealValue (value),
        distribution (0.0f, 5.0f),
        pointOneFactor (getFactor (0.0f, 0.001f)),
        pointFiveFactor (getFactor (0.001f, 0.005f)),
        oneFactor (getFactor (0.005f, 0.01f)),
        fiveFactor (getFactor (0.01f, 0.05f)),
        tenFactor(getFactor(0.05f, 0.1f)),
        twentyFactor(getFactor(0.05f, 0.2f))
    {
    
    }

    void setValue (float newValue) { 
        idealValue = newValue; 
    }
    void setTolerance (Tolerance newTol) { 
        tol = newTol; 
    }

    float getValue()
    {
        /*Switch tolerance*/
        switch (tol) {
            case Tolerance::Ideal:
            {
                return idealValue;
            }
            case Tolerance::PointOne:
            {
                return idealValue * (1.0f + pointOneFactor);
            }
            case Tolerance::PointFive:
            {
                return idealValue * (1.0f + pointFiveFactor);
            }
            case Tolerance::One:
            {
                return idealValue * (1.0f + oneFactor);
            }
            case Tolerance::Five:
            {
                return idealValue * (1.0f + fiveFactor);
            }
            case Tolerance::Ten:
            {
                return idealValue * (1.0f + tenFactor);
            }
            case Tolerance::Twenty:
            {
                return idealValue * (1.0f + twentyFactor);
            }
            default:
            {
                return idealValue;
            }
        }

        return idealValue;
    }

    float getFactor (float tol_low, float tol_high)
    {
        float return_val = 10000000.0f;
        while (abs(return_val) > tol_high || abs(return_val) < tol_low)
            return_val = distribution (generator);
        return return_val;
    }

    static juce::StringArray getChoices()
    {
        return juce::StringArray ({ "Ideal", "0.1%", "0.5%", "1%", "5%", "10%" });
    }

private:
    float idealValue;

    MyRandomGenerator generator;
    std::normal_distribution<float> distribution;

    const float pointOneFactor;
    const float pointFiveFactor;
    const float oneFactor;
    const float fiveFactor;
    const float tenFactor;
    const float twentyFactor;

    Tolerance tol = Tolerance::Ideal;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (Element)
};

