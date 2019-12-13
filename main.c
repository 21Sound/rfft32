#include <stdio.h>
#include <math.h>
#include "rfft32.h"

int main()
{
    printf("Hello World!\n");

    init_rfft32();

    FILE* rfftResultFile;
    FILE* irfftResultFile;

    complex32 spectrum32[NFFT/2+1];
    int32_t input32[NFFT];
    for (int i = 0; i < NFFT ; ++i) {
        input32[i] = (int32_t) (0x7FFFFFFF*sin(2.0*M_PI*1000*i/44100.0));
    }
    int32_t output32[NFFT];

    double absSpec[NFFT/2+1];
    double output[NFFT];

    // fft computation
    rfft32(input32, spectrum32);
    for (int i = 0; i < NFFT/2+1; ++i) {
        absSpec[i] = (double) spectrum32[i].re*spectrum32[i].re + (double) spectrum32[i].im*spectrum32[i].im;
        absSpec[i] = sqrt(absSpec[i]) / 0x7FFFFFFF;
    }
    rfftResultFile = fopen("rfftResult.raw", "wb+");
    fwrite(absSpec, sizeof(double), NFFT/2+1, rfftResultFile);
    fclose(rfftResultFile);

    // ifft computation
    irfft32(spectrum32, output32);
    for (int i = 0; i < NFFT; ++i) {
        output[i] = (double) output32[i];
        output[i] /= 0x7FFFFFFF;
    }
    irfftResultFile = fopen("irfftResult.raw", "wb+");
    fwrite(output, sizeof(double), NFFT, irfftResultFile);
    fclose(irfftResultFile);

    return 0;
}
