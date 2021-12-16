#pragma once
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif
size_t read_s16_1(const char *filename, int16_t **args);
size_t read_s16_2(const char *filename, int16_t **args);
size_t read_s16_3(const char *filename, int16_t **args);
int write_s16(const char *filename, int16_t *results, size_t noutput);

size_t read_u32_1(const char *filename, uint32_t **args);
size_t read_u32_2(const char *filename, uint32_t **args);
size_t read_u32_3(const char *filename, uint32_t **args);
size_t read_u32_4(const char *filename, uint32_t **args);

#define read_b32_1(x, y) read_u32_1(x, y)
#define read_b32_2(x, y) read_u32_2(x, y)
#define read_b32_3(x, y) read_u32_3(x, y)
#define read_b32_4(x, y) read_u32_4(x, y)
int write_u32(const char *filename, uint32_t *output, size_t noutput);
#define write_b32(x, y, z) write_u32(x, y, z)

size_t read_s16_1(const char *filename, int16_t **args);
size_t read_s16_2(const char *filename, int16_t **args);
size_t read_s16_3(const char *filename, int16_t **args);
int write_s16(const char *filename, int16_t *output, size_t noutput);

size_t read_u16_1(const char *filename, uint16_t **args);
size_t read_u16_2(const char *filename, uint16_t **args);
size_t read_u16_3(const char *filename, uint16_t **args);

#define read_b16_1(x, y) read_u16_1(x, y)
#define read_b16_2(x, y) read_u16_2(x, y)
#define read_b16_3(x, y) read_u16_3(x, y)
#define read_b16_4(x, y) read_u16_4(x, y)
int write_u16(const char *filename, uint16_t *output, size_t noutput);
#define write_b16(x, y, z) write_u16(x, y, z)

size_t read_s32_1(const char *filename, int32_t **args);
size_t read_s32_2(const char *filename, int32_t **args);
size_t read_s32_3(const char *filename, int32_t **args);
int write_s32(const char *filename, int32_t *output, size_t noutput);

size_t read_u32_1(const char *filename, uint32_t **args);
size_t read_u32_2(const char *filename, uint32_t **args);
size_t read_u32_3(const char *filename, uint32_t **args);
int write_u32(const char *filename, uint32_t *output, size_t noutput);
#define write_pred(x, y, z) write_u32(x, y, z)

size_t read_s64_1(const char *filename, int64_t **args);
size_t read_s64_2(const char *filename, int64_t **args);
size_t read_s64_3(const char *filename, int64_t **args);
int write_s64(const char *filename, int64_t *output, size_t noutput);


size_t read_u64_1(const char *filename, uint64_t **args);
size_t read_u64_2(const char *filename, uint64_t **args);
size_t read_u64_3(const char *filename, uint64_t **args);
size_t read_u64_4(const char *filename, uint64_t **args);

#define read_b64_1(x, y) read_u64_1(x, y)
#define read_b64_2(x, y) read_u64_2(x, y)
#define read_b64_3(x, y) read_u64_3(x, y)
#define read_b64_4(x, y) read_u64_4(x, y)
int write_u64(const char *filename, uint64_t *output, size_t noutput);
#define write_b64(x, y, z) write_u64(x, y, z)

size_t read_f32_1(const char *filename, float **args);
size_t read_f32_2(const char *filename, float **args);
size_t read_f32_3(const char *filename, float **args);
int write_f32(const char *filename, float *output, size_t noutput);

size_t read_f64_1(const char *filename, double **args);
size_t read_f64_2(const char *filename, double **args);
size_t read_f64_3(const char *filename, double **args);
int write_f64(const char *filename, double *output, size_t noutput);

int read_custom(const char *filename, void **args, size_t sz_arg, int (*reader)(const char *,
																				void *,
																				size_t));

int write_custom(const char *filename, void *output, size_t noutput,
				 int (*writer)(char *, size_t, void *, size_t));

int write_custom_inout(const char *filename, void *output, size_t noutput,
                       void *args,
                       int (*writer)(char *, size_t, void *, void *, size_t));

int normsort_cmp16(const void *a, const void *b);
int normsort_cmp32(const void *a, const void *b);
int normsort_cmp64(const void *a, const void *b);

#ifdef __cplusplus
}
#endif
