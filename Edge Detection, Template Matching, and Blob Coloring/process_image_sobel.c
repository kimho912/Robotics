#include <stdio.h>
#include <math.h>
#include <X11/Xlib.h>

#define DIM 512

/******************************************************************/
/* This structure contains the coordinates of a box drawn with    */
/* the left mouse button on the image window.                     */
/* roi.x , roi.y  - left upper corner's coordinates               */
/* roi.width , roi.height - width and height of the box           */
/******************************************************************/
extern XRectangle roi;

unsigned char convolution(unsigned char image[DIM][DIM],int template[3][3],int row,int col);
/******************************************************************/
/* Main processing routine. This is called upon pressing the      */
/* Process button of the interface.                               */
/* image  - the original greyscale image                          */
/* size   - the actual size of the image                          */
/* proc_image - the image representation resulting from the       */
/*              processing. This will be displayed upon return    */
/*              from this function.                               */
/******************************************************************/
void process_image(image, size, proc_img)
unsigned char image[DIM][DIM];
int size[2];
unsigned char proc_img[DIM][DIM];
{
    // Sobel templates
    // Please uncomment the desired template as a parameter in the convolution function
    // int sobelVertical[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    // int sobelHorizontal[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};
    // int sobelMajDiag[3][3] = {{0, -1, -2}, {1, 0, -1}, {2, 1, 0}};
    int sobelMinDiag[3][3] = {{-2, -1, 0}, {-1, 0, 1}, {0, 1, 2}};

    for (int x = 0; x < size[0] - 2; x++)
    {
        for (int y = 0; y < size[1] - 2; y++)
        {
            proc_img[x][y] = convolution(image,sobelMinDiag,x,y); // switch the second parameter, if needed.
        }
    }
}
unsigned char convolution(unsigned char image[DIM][DIM],int template[3][3],int row,int col)
{
    int sum = 0;
    for (int i = 0; i < 3; i++) 
    {
        for (int j = 0; j < 3; j++) 
        {
            sum += (int)image[row + i][col + j] * template[i][j];
        }
    }
    // check if sum is out of range [0:255]
    if (sum < 0) 
    {
        sum = 0;
    }
    else if (sum > 255)
    {
        sum = 255;
    }
    return (unsigned char)sum;
}