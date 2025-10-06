/*
 * Author: Matteo Valente
 * Date:   October 5th, 2025
 * File:   Part2.c
 * Description:
 *     gcc Part2.c -o Part2 -lm
 *     ./Part2
 *     Run the experiment for T seconds, take the result, run the experiment again for 2T seconds and see if the expected values of the output variables change
 *     Arrival -> Generate a random variable that represents the arrival times of packets to a queue (Exponential distribution)
 *     Calculate the departure time of a packet based on the state of the queue
 *     Generate a set of random observation times according to the packet arrival distribution with rate at least 3 times the rate of the packet arrival
 *     Eecording the following: the time-average of the number of packets in the queue, E[N], the proportion of time the server is idle (i.e., the system is empty) 
 *     -> PIDLE and in the case of a finite queue, the probability PLOSS that a packet will be dropped (due to the buffer being full when it arrives)
 *     You need to have three counters: Na = number of packet arrivals, Nd = number of packets departures, and No = number of observations
 *     Put all the events in a list and sort them
 *     Equation ---> x = -ln(u) / lambda
 */

// Queue Implementation -> https://heycoach.in/blog/dynamic-queue-implementation-in-c/

#include <stdio.h>  // Printf()
#include <stdlib.h> // Rand()
#include <math.h>   // Log()
#include <time.h>   // Srand()

#define ARRIVAL 0
#define OBSERVER 1
#define DEPARTURE 2

typedef struct Event {
    int type;
    double time;
    struct Event* next;
} Event;

typedef struct Packet{
    double arrival_time;
    double service_time;
} Packet;

typedef struct Node{
    Packet packet;
    struct Node* next;
} Node;

typedef struct Queue{
    Node* front;
    Node* rear;
} Queue;

Queue* createQueue(){
    Queue* q = (Queue*)malloc(sizeof(Queue));
    q -> front = NULL;
    q -> rear = NULL;
    return q;
}

void enQueue(Queue* q, Packet packet){
    Node* newNode = (Node*)malloc(sizeof(Node));
    if (!newNode){
        printf("Memory Allocation Failed!\n");
        return;
    }
    newNode -> packet = packet;
    newNode -> next = NULL;

    if (q -> rear == NULL){
        q -> front = newNode;
        q -> rear = newNode;
    } else{
        q -> rear -> next = newNode;
        q -> rear = newNode;
    }
}

Packet deQueue(Queue* q){
    if (q -> front == NULL){
        printf("Queue Empty!\n");
        Packet empty = {0.0, 0.0};
        return empty;
    }

    Node* temp = q -> front;
    Packet packet = temp -> packet;
    q -> front = q -> front->next;

    if (q -> front == NULL){
        q -> rear = NULL;
    }

    free(temp);
    return packet;
}

int isEmpty(Queue* q){
    return q -> front == NULL;
}

void freeQueue(Queue* q){
    while (!isEmpty(q)){
        deQueue(q);
    }
    free(q);
}

double random_variable_generator(double rate) {
    double U = ((double)rand() + 1.0) / ((double)RAND_MAX + 2.0);
    return -log(U) / rate;
}

int main(void){
    
    srand((unsigned)time(0));

    // Dummy lamda and mu for now
    double lambda = 2.0;    
    double mu = 1.0;
    double simulation_time = 1000;
    
    return 0;
}