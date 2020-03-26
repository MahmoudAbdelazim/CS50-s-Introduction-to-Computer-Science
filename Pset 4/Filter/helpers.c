#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int blue, green, red;
    for (int i = 0; i < width; i++) {
        for (int j = 0; j < height; j++) {
            blue = image[j][i].rgbtBlue;
            green = image[j][i].rgbtGreen;
            red = image[j][i].rgbtRed;
            int avg = round((blue + green + red) / 3.0);
            image[j][i].rgbtBlue = avg;
            image[j][i].rgbtGreen = avg;
            image[j][i].rgbtRed = avg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);
            if (sepiaRed > 255) {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255) {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255) {
                sepiaBlue = 255;
            }
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++) {
        for (int j = 0, k = width - 1; j < k; j++, k--) {
            int redj, redk, greenj, greenk, bluej, bluek;
            redj = image[i][j].rgbtRed;
            greenj = image[i][j].rgbtGreen;
            bluej = image[i][j].rgbtBlue;
            redk = image[i][k].rgbtRed;
            greenk = image[i][k].rgbtGreen;
            bluek = image[i][k].rgbtBlue;
            image[i][j].rgbtRed = redk;
            image[i][j].rgbtGreen = greenk;
            image[i][j].rgbtBlue = bluek;
            image[i][k].rgbtRed = redj;
            image[i][k].rgbtGreen = greenj;
            image[i][k].rgbtBlue = bluej;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE newImage[height][width];
    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {

            int red = 0, green = 0, blue = 0, pixelCnt = 0;

            for (int x = i - 1; x < (i+2); x++) {
                for (int y = j - 1; y < (j+2); y++) {

                    if (x >= 0 && y >= 0) {
                        pixelCnt++;
                        red += image[x][y].rgbtRed;
                        green += image[x][y].rgbtGreen;
                        blue += image[x][y].rgbtBlue;
                    }
                }
            }
            int redAvg = round((double)red / pixelCnt);
            int greenAvg = round((double)green / pixelCnt);
            int blueAvg = round((double)blue / pixelCnt);
            newImage[i][j].rgbtRed = redAvg;
            newImage[i][j].rgbtGreen = greenAvg;
            newImage[i][j].rgbtBlue = blueAvg;
        }
    }
    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            image[i][j] = newImage[i][j];
        }
    }
    return;
}
