#include <stdio.h>
#include <math.h>
#include <X11/Xlib.h>

#define DIM 512

extern XRectangle roi;

float convolution(unsigned char image[DIM][DIM], float template[roi.width][roi.height], int row, int col, float template_mean, float template_stddev);
void normalize(float data[roi.width][roi.height], float mean, float stddev);
void get_mean_stddev(float data[roi.width][roi.height], float *mean, float *stddev);

void process_image(unsigned char image[DIM][DIM], int size[2], unsigned char proc_img[DIM][DIM])
{
    // selected templates
    float template[roi.width][roi.height];
    float template_mean, template_stddev;
    
    // extracting template from image
    for (int x = 0; x < roi.width; x++)
    {
        for (int y = 0; y < roi.height; y++)
        {
            template[x][y] = (float)image[roi.x + x][roi.y + y];
        }
    }

    get_mean_stddev(template, &template_mean, &template_stddev);
    normalize(template, template_mean, template_stddev);

    for (int x = 0; x < size[0]-roi.width; x++)
    {
        for (int y = 0; y < size[1]-roi.height; y++)
        {
            float conv_result = convolution(image, template, x, y, template_mean, template_stddev);
            // Normalize the result of the convolution to be between 0 and 255
            proc_img[x + roi.width / 2][y + roi.height / 2] = (unsigned char)(conv_result * 255.0f);
        }
    }
}

float convolution(unsigned char image[DIM][DIM], float template[roi.width][roi.height], int row, int col, float template_mean, float template_stddev)
{
    float sum = 0.0;
    float n = roi.height * roi.width;
    float subimage_mean, subimage_stddev;
    float subimage[roi.width][roi.height];
    
    // Extract subimage and calculate its mean and standard deviation
    for (int x = 0; x < roi.width-1; x++)
    {
        for (int y = 0; y < roi.height-1; y++)
        {
            subimage[x][y] = (float)image[row+x][col+y];
        }
    }
    get_mean_stddev(subimage, &subimage_mean, &subimage_stddev);
    normalize(subimage, subimage_mean, subimage_stddev);
    
    // Perform normalized cross-correlation
    for (int i = 0; i < roi.width; i++)
    {
        for (int j = 0; j < roi.height; j++)
        {
            sum += subimage[i][j] * (template[i][j] - template_mean) / template_stddev;
        }
    }
    
    sum = fmax(0.0, fmin(sum / n, 1.0)) * 255.0;

    return sum;
}

void normalize(float data[roi.width][roi.height], float mean, float stddev)
{
    // Normalize each pixel value using the mean and standard deviation
    for (int i = 0; i < roi.width; i++)
    {
        for (int j = 0; j < roi.height; j++)
        {
            data[i][j] = (data[i][j] - mean) / stddev;
        }
    }
}
void get_mean_stddev(float data[roi.width][roi.height], float *mean, float *stddev)
{
    *mean = 0.0;
    *stddev = 0.0;

    // Compute mean
    for (int i = 0; i < roi.width; i++)
    {
        for (int j = 0; j < roi.height; j++)
        {
            *mean += data[i][j];
        }
    }

    *mean /= (roi.width * roi.height);

    // Compute standard deviation
    for (int i = 0; i < roi.width; i++)
    {
        for (int j = 0; j < roi.height; j++)
        {
            *stddev += pow(data[i][j] - *mean, 2);
        }
    }

    *stddev /= (roi.width * roi.height);
    *stddev = sqrt(*stddev);
}
