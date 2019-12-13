#ifndef _RFFT32
#define _RFFT32

#include <stdint.h>

#define NFFT 4096

typedef struct {
    int32_t re,im;
} complex32;

void init_rfft32();
void rfft32(int32_t *input, complex32 *spectrum);
void irfft32(complex32 *spectrum, int32_t *output);

#endif
