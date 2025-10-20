/*
 * Author: Matteo Valente
 * Date:   October 5th, 2025
 * File:   Part1.c
 * Description:
 *     gcc Part1.c -o Part1 -lm
 *     ./Part1
 *     Generate 1000 exponential random variable samples from your equation
 *     Given a exponential distribution with uniform U(0,1)
 *     What is the mean and variance of the 1000 random variables you generated? 
 *     Do they agree with the expected value and the variance of an exponential random variable
 *     Equation ---> x = -ln(u) / lambda
 */

#include <stdio.h>  // Printf()
#include <stdlib.h> // Rand()
#include <math.h>   // Log()
#include <time.h>   // Srand()

int main(void){
    
    // Initialize values
    int N = 1000;
    double lambda = 75.0;
    double samples[N];
    double sum = 0.0, sample_mean = 0.0, sample_variance = 0.0;
    double expected_mean = 1.0 / lambda;
    double expected_variance = 1.0 / pow(lambda, 2);

    // Seed random number generator according to outline
    srand((unsigned)time(0));

    // Generate samples. Since rand 32,767 and we want 0 to 1, divide by max
    // Extend our range a bit here so we avoid ln(0)
    for(int i = 0; i < N; i++){
        double U = ((double)rand() + 1.0) / ((double)RAND_MAX + 2.0);
        samples[i] = -log(1-U) / lambda;
        sum += samples[i];
    }

    // Calculate Mean
    sample_mean = sum / N;

    // Calculate Variance
    for(int i = 0; i < N; i++){
        sample_variance += pow(samples[i] - sample_mean, 2);
    }
    sample_variance /= (N - 1);

    // Print out simulation results
    printf("Lambda = %.2f\n", lambda);
    printf("Number of Samples = %d\n", N);
    printf("Sample Mean = %.6f\n", sample_mean);
    printf("Sample Variance = %.6f\n", sample_variance);
    printf("Expected Mean = %.6f\n", expected_mean);
    printf("Expected Variance = %.6f\n", expected_variance);

    return 0;
}