/* One-level Haar DWT on even-length float buffer. Teaching only. Not optimized. */
#include <stdio.h>
#include <stdlib.h>

void haar_forward(const float *x, int n, float *approx, float *detail) {
    int i, m = n / 2;
    const float s = 0.7071067811865476f;
    for (i = 0; i < m; i++) {
        approx[i] = s * (x[2 * i] + x[2 * i + 1]);
        detail[i] = s * (x[2 * i] - x[2 * i + 1]);
    }
}

int main(void) {
    float x[8] = {1, 2, 3, 4, 4, 3, 2, 1};
    float a[4], d[4];
    int i;
    haar_forward(x, 8, a, d);
    printf("approx:");
    for (i = 0; i < 4; i++) printf(" %f", a[i]);
    printf("\ndetail:");
    for (i = 0; i < 4; i++) printf(" %f", d[i]);
    printf("\n/* not hardware tested */\n");
    return 0;
}
