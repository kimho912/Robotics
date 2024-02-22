#include <stdio.h>
#include <math.h>

int UTA_ID = 1001967176;

double PD_control(theta, theta_dot, theta_ref, theta_dot_ref)
double theta, theta_dot, theta_ref, theta_dot_ref;
{
    double mg = 0.0;
    double torque = 0.0;
    double I, G, B = 0.0;
    double b = 0.0;
    
// Gravity equation
    // torque = 1;
    // When torque = 1, theta = -0.678716 & theta_dot = 0
    // 1 = mg*sin(M_PI_2 - 0.678716)
    mg = 1 / sin(M_PI_2 - 0.678716);

    G = mg*sin(M_PI_2 - theta);
    // Torque without gravity
    torque = G;
    
// Viscous friction equation
    // Find a constant velocity = 0.1587931719
    torque = G + 40;
    b = 40 /251.9;
    
    B = b * theta_dot;
    // Torque without the viscous friction plus Gravity
    torque = B + G;
    
// Inertia equation
    // Getting theta_dot_dot
    // in case c = 10
        // torque = B + G + 10;
        // theta_dot_dot = (448.546098-448.099975)/(1/500) = 223.0615
        // I1 = 10/223.0615 = 0.04483068571;
    // in case c = 5
        // theta_dot_dot = 169.312152-169.097124/(1/500)= 107.514
        // I2 = 5/107.514 = 0.04650557137;
    //average = 0.04483068571 + 0.04650557137 / 2
    
    I = 0.04566812854;
    
    // overroll torque
    torque = I + B + G;
    
    printf("theta: %f, theta_dot: %f\n",theta,theta_dot);
    
    return(torque);
}
