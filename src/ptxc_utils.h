#pragma once
#include <math.h>
#include <fenv.h>

#ifdef USE_PTXM
#include <ptxm/models.h> /* ptxs models.h for PTX math instructions */
#endif

#ifndef PYCPARSER /* pycparser doesn't handle _Generic */
#define FTZ(X) _Generic((X), \
						float: FTZf,			\
						double: FTZd)(X)

#define SAT(X) _Generic((X), \
						float: SATf,			\
						double: SATd)(X)

#define FMA(X, Y, Z) _Generic((X),				\
							  float: fmaf,		\
							  double: fma)(X, Y, Z)

#define SQRT(X) _Generic((X),				\
						 float: sqrtf,		\
						 double: sqrt)(X)

#define SINE(X) _Generic((X),				\
						 float: sinf,		\
						 double: sin)(X)

#define COSINE(X) _Generic((X),				\
						 float: cosf,		\
						 double: cos)(X)

#define LOG2(X) _Generic((X),				\
						 float: log2f,		\
						 double: log2)(X)

#define EXP2(X) _Generic((X),           \
                         float: exp2,   \
                         double: exp2)(X)

#define COPYSIGN(X, Y) _Generic((X),                    \
                                float: copysignf,       \
                                double: copysign)(X, Y)

#define extract_24(X) _Generic((X),								\
							   uint32_t: extract_24_unsigned,	\
							   int32_t: extract_24_signed)(X)

#define MAXVALUE(x) _Generic((x), \
							 int16_t: INT16_MAX,	\
							 uint16_t: UINT16_MAX,	\
							 int32_t: INT32_MAX,	\
							 uint32_t: UINT32_MAX,	\
							 int64_t: INT64_MAX,	\
							 uint64_t: UINT64_MAX)

#define ABSOLUTE(x) _Generic((x), \
							 int16_t: abs,	\
							 int32_t: abs,	\
							 int64_t: labs)(x)

#define INTWIDTH(x) _Generic((x), \
							 int16_t: 16,	\
							 uint16_t: 16,	\
							 int32_t: 32,	\
							 uint32_t: 32,	\
							 int64_t: 64,	\
							 uint64_t: 64)


#endif

#ifdef USE_PTXM

#define ptxm_rcp ptxm_rcp_sm5x
#define ptxm_sqrt ptxm_sqrt_sm5x
#define ptxm_sin ptxm_sin_sm5x
#define ptxm_cos ptxm_cos_sm5x
#define ptxm_lg2 ptxm_lg2_sm5x
#define ptxm_ex2 ptxm_ex2_sm5x
#define ptxm_rsqrt ptxm_rsqrt_sm5x

#undef RCP
#undef SQRT
#undef SINE
#undef COSINE
#undef LOG2
#undef EXP2

#ifndef PYCPARSER
#define RCP(X) _Generic((X),                    \
                        float: ptxm_rcp,        \
                        double: RCP_DOUBLE)(X)

#define RSQRT(X) _Generic((X),                      \
                          float: ptxm_rsqrt,        \
                          double: RSQRT_DOUBLE)(X)

#define SQRT(X) _Generic((X),				\
						 float: ptxm_sqrt,  \
						 double: sqrt)(X)

#define SINE(X) _Generic((X),				\
						 float: ptxm_sin,   \
						 double: sin)(X)

#define COSINE(X) _Generic((X),				\
                           float: ptxm_cos, \
                           double: cos)(X)

#define LOG2(X) _Generic((X),				\
						 float: ptxm_lg2,   \
						 double: log2)(X)

#define EXP2(X) _Generic((X),				\
                         float: ptxm_ex2,   \
                         double: exp2)(X)

#endif
static inline double RCP_DOUBLE(double X) { return 1.0/X; }
static inline double RSQRT_DOUBLE(double X) {return RCP_DOUBLE(SQRT(X)); }

#else
#define RCP(X) (1.0 / (X))
#define RSQRT(X) RCP(SQRT(X))
#endif

typedef uint16_t bitstring16_t;
typedef uint32_t bitstring32_t;
typedef uint64_t bitstring64_t;
typedef uint32_t BIT_T;

static inline float FTZf(float x) {
  if(fpclassify(x) == FP_SUBNORMAL) {
	return copysignf(0.0, x);
  }

  return x;
}

static inline double FTZd(double x) {
  if(fpclassify(x) == FP_SUBNORMAL) {
	return copysign(0.0, x);
  }

  return x;
}

static inline uint32_t extract_24_unsigned(uint32_t x) {
  return x & 0xffffff;
}

static inline uint32_t extract_24_signed(int32_t x) {
  uint32_t xx = x;
  xx = x & 0xffffff;
  if(xx & 0x800000) xx |= 0xff000000;

  return xx;
}

#include "ptxc_utils_template.h"

int32_t ADD_SATURATE_s32(int32_t x, int32_t y) {
  /* see Dietz et al., ICSE 2012 */

  if(x > 0 && y > 0 && x > INT32_MAX - y)
	return INT32_MAX;

  if(x < 0 && y < 0 && x < INT32_MIN - y)
	return INT32_MIN;

  return x + y;
}

int32_t SUB_SATURATE_s32(int32_t x, int32_t y) {
  /* 0 - +ve will never cause underflow */
  if(x < 0 && y > 0 && x < INT32_MIN + y) {
	return INT32_MIN;
  }

  /* 0 - -ve can cause overflow */
  if(x >= 0 && y < 0 && x > INT32_MAX + y) {
	return INT32_MAX;
  }

  // both same sign or no overflow detected
  return x - y;
}

static inline uint8_t ReadByte(uint8_t control, uint64_t value, uint8_t pos) {
  uint8_t byte = 0;
  byte = (value >> ((control & 0x7) * 8)) & 0xff;
  if(control & 0x8) {
	if(byte & 0x80)
	  return 0xff;
	else
	  return 0x0;
  } else {
	return byte;
  }
}

static inline float DIV_FULL(float dividend, float divisor) {
  // this is not a correct implementation...
  return dividend / divisor;
}

static inline float DIV_APPROX(float dividend, float divisor) {
  int special_case = 0;

  // based on a liberal reading of __fdividef in the CUDA Math API, as
  // well as actual outputs.

  if(!(isinf(divisor) || isnan(divisor))) {
    special_case = (0x1.0p126 < fabsf(divisor) && fabsf(divisor) < 0x1.0p128);
  }

  if(special_case && !isnan(dividend))
    return isinf(dividend) ? NAN : 0.0;

  // this is not a correct implementation...
  return dividend / divisor;
}

static inline float fminf_ptx(float a, float b) {
  float res;
  res = fminf(a, b);

  // ptx requires +0.0 > -0.0
  if((res == 0.0) && (a == b)) {
    if(signbit(a))
      return a;
    else
      return b;
  }

  return res;
}

static inline float fmaxf_ptx(float a, float b) {
  float res;
  res = fmaxf(a, b);

  // ptx requires +0.0 > -0.0
  if((res == 0.0) && (a == b)) {
    if(signbit(a))
      return b;
    else
      return a;
  }

  return res;
}

static inline double fmin_ptx(double a, double b) {
  double res;
  res = fmin(a, b);

  // ptx requires +0.0 > -0.0
  if((res == 0.0) && (a == b)) {
    if(signbit(a))
      return a;
    else
      return b;
  }

  return res;
}

static inline double fmax_ptx(double a, double b) {
  double res;
  res = fmax(a, b);

  // ptx requires +0.0 > -0.0
  if((res == 0.0) && (a == b)) {
    if(signbit(a))
      return b;
    else
      return a;
  }

  return res;
}
