#pragma once
#include <stdint.h>
#include "128types.h"

inline static uint32_t MULWIDE_u16_u32(uint16_t x, uint16_t y)
{
  uint32_t d;
  d = ((uint32_t) x) * ((uint32_t) y);
  return d;
}


inline static uint64_t MULWIDE_u32_u64(uint32_t x, uint32_t y)
{
  uint64_t d;
  d = ((uint64_t) x) * ((uint64_t) y);
  return d;
}


inline static my_uint128_t MULWIDE_u64_u128(uint64_t x, uint64_t y)
{
  my_uint128_t d;
  d = ((my_uint128_t) x) * ((my_uint128_t) y);
  return d;
}


inline static int32_t MULWIDE_s16_s32(int16_t x, int16_t y)
{
  int32_t d;
  d = ((int32_t) x) * ((int32_t) y);
  return d;
}


inline static int64_t MULWIDE_s32_s64(int32_t x, int32_t y)
{
  int64_t d;
  d = ((int64_t) x) * ((int64_t) y);
  return d;
}


inline static my_int128_t MULWIDE_s64_s128(int64_t x, int64_t y)
{
  my_int128_t d;
  d = ((my_int128_t) x) * ((my_int128_t) y);
  return d;
}


inline static uint64_t MUL24_u32_u64(uint32_t x, uint32_t y)
{
  uint64_t d;
  uint32_t xx;
  uint32_t yy;
  xx = extract_24(x);
  yy = extract_24(y);
  x = xx;
  y = yy;
  d = ((uint64_t) x) * ((uint64_t) y);
  return d;
}


inline static int64_t MUL24_s32_s64(int32_t x, int32_t y)
{
  int64_t d;
  uint32_t xx;
  uint32_t yy;
  xx = extract_24(x);
  yy = extract_24(y);
  x = xx;
  y = yy;
  d = ((int64_t) x) * ((int64_t) y);
  return d;
}


inline static float SAT_f32(float x)
{
  if (isnan(x))
    return 0.0;

  if (x <= 0.0)
    return 0.0;
  else
    if (x > 1.0)
    return 1.0;
  else
    return x;


}


inline static double SAT_f64(double x)
{
  if (isnan(x))
    return 0.0;

  if (x <= 0.0)
    return 0.0;
  else
    if (x > 1.0)
    return 1.0;
  else
    return x;


}


inline static int16_t MAX_s16(int16_t x, int16_t y)
{
  if (x < y)
    return y;
  else
    return x;

}


inline static int32_t MAX_s32(int32_t x, int32_t y)
{
  if (x < y)
    return y;
  else
    return x;

}


inline static int64_t MAX_s64(int64_t x, int64_t y)
{
  if (x < y)
    return y;
  else
    return x;

}


inline static uint16_t MAX_u16(uint16_t x, uint16_t y)
{
  if (x < y)
    return y;
  else
    return x;

}


inline static uint32_t MAX_u32(uint32_t x, uint32_t y)
{
  if (x < y)
    return y;
  else
    return x;

}


inline static uint64_t MAX_u64(uint64_t x, uint64_t y)
{
  if (x < y)
    return y;
  else
    return x;

}


inline static float MIN_f32(float x, float y)
{
  if (x < y)
    return x;
  else
    return y;

}


inline static double MIN_f64(double x, double y)
{
  if (x < y)
    return x;
  else
    return y;

}


inline static int16_t MIN_s16(int16_t x, int16_t y)
{
  if (x < y)
    return x;
  else
    return y;

}


inline static int32_t MIN_s32(int32_t x, int32_t y)
{
  if (x < y)
    return x;
  else
    return y;

}


inline static int64_t MIN_s64(int64_t x, int64_t y)
{
  if (x < y)
    return x;
  else
    return y;

}


inline static uint16_t MIN_u16(uint16_t x, uint16_t y)
{
  if (x < y)
    return x;
  else
    return y;

}


inline static uint32_t MIN_u32(uint32_t x, uint32_t y)
{
  if (x < y)
    return x;
  else
    return y;

}


inline static uint64_t MIN_u64(uint64_t x, uint64_t y)
{
  if (x < y)
    return x;
  else
    return y;

}


inline static float ADD_ROUND_f32(float x, float y, int mode)
{
  float t;
  fesetround(mode);
  t = x + y;
  fesetround(FE_TONEAREST);
  return t;
}


inline static double ADD_ROUND_f64(double x, double y, int mode)
{
  double t;
  fesetround(mode);
  t = x + y;
  fesetround(FE_TONEAREST);
  return t;
}


inline static float SUB_ROUND_f32(float x, float y, int mode)
{
  float t;
  fesetround(mode);
  t = x - y;
  fesetround(FE_TONEAREST);
  return t;
}


inline static double SUB_ROUND_f64(double x, double y, int mode)
{
  double t;
  fesetround(mode);
  t = x - y;
  fesetround(FE_TONEAREST);
  return t;
}


inline static float MUL_ROUND_f32(float x, float y, int mode)
{
  float t;
  fesetround(mode);
  t = x * y;
  fesetround(FE_TONEAREST);
  return t;
}


inline static double MUL_ROUND_f64(double x, double y, int mode)
{
  double t;
  fesetround(mode);
  t = x * y;
  fesetround(FE_TONEAREST);
  return t;
}


inline static float DIV_ROUND_f32(float x, float y, int mode)
{
  float t;
  fesetround(mode);
  t = x / y;
  fesetround(FE_TONEAREST);
  return t;
}


inline static double DIV_ROUND_f64(double x, double y, int mode)
{
  double t;
  fesetround(mode);
  t = x / y;
  fesetround(FE_TONEAREST);
  return t;
}


inline static float FMA_ROUND_f32(float x, float y, float z, int mode)
{
  float t;
  fesetround(mode);
  t = FMA(x, y, z);
  fesetround(FE_TONEAREST);
  return t;
}


inline static double FMA_ROUND_f64(double x, double y, double z, int mode)
{
  double t;
  fesetround(mode);
  t = FMA(x, y, z);
  fesetround(FE_TONEAREST);
  return t;
}


inline static float RCP_ROUND_f32(float x, int mode)
{
  float t;
  fesetround(mode);
  t = 1.0 / x;
  fesetround(FE_TONEAREST);
  return t;
}


inline static double RCP_ROUND_f64(double x, int mode)
{
  double t;
  fesetround(mode);
  t = 1.0 / x;
  fesetround(FE_TONEAREST);
  return t;
}


inline static float SQRT_ROUND_f32(float x, int mode)
{
  float t;
  fesetround(mode);
  t = SQRT(x);
  fesetround(FE_TONEAREST);
  return t;
}


inline static double SQRT_ROUND_f64(double x, int mode)
{
  double t;
  fesetround(mode);
  t = SQRT(x);
  fesetround(FE_TONEAREST);
  return t;
}


inline static void extractAndZeroExt_4_u32(uint32_t src, uint32_t *dst)
{
  for (int i = 0; i < 4; i++)
  {
    dst[i] = (uint32_t) ((uint8_t) (src & 0xff));
    src >>= 8;
  }

}


inline static void extractAndZeroExt_4_s32(uint32_t src, int32_t *dst)
{
  for (int i = 0; i < 4; i++)
  {
    dst[i] = (int32_t) ((uint8_t) (src & 0xff));
    src >>= 8;
  }

}


inline static void extractAndZeroExt_2_u32(uint32_t src, uint32_t *dst)
{
  for (int i = 0; i < 2; i++)
  {
    dst[i] = (uint32_t) ((uint16_t) (src & 0xffff));
    src >>= 16;
  }

}


inline static void extractAndZeroExt_2_s32(uint32_t src, int32_t *dst)
{
  for (int i = 0; i < 2; i++)
  {
    dst[i] = (int32_t) ((uint16_t) (src & 0xffff));
    src >>= 16;
  }

}


inline static void extractAndSignExt_4_u32(uint32_t src, uint32_t *dst)
{
  for (int i = 0; i < 4; i++)
  {
    dst[i] = (uint32_t) ((int8_t) (src & 0xff));
    src >>= 8;
  }

}


inline static void extractAndSignExt_4_s32(uint32_t src, int32_t *dst)
{
  for (int i = 0; i < 4; i++)
  {
    dst[i] = (int32_t) ((int8_t) (src & 0xff));
    src >>= 8;
  }

}


inline static void extractAndSignExt_2_u32(uint32_t src, uint32_t *dst)
{
  for (int i = 0; i < 2; i++)
  {
    dst[i] = (uint32_t) ((int16_t) (src & 0xffff));
    src >>= 16;
  }

}


inline static void extractAndSignExt_2_s32(uint32_t src, int32_t *dst)
{
  for (int i = 0; i < 2; i++)
  {
    dst[i] = (int32_t) ((int16_t) (src & 0xffff));
    src >>= 16;
  }

}


inline static uint16_t ADD_CARRY_u16(uint16_t a, uint16_t b, uint16_t cf, int *outcf)
{
  uint16_t ua;
  uint16_t ub;
  uint16_t ures;
  uint16_t umax;
  int f;
  ua = (uint16_t) a;
  ub = (uint16_t) b;
  umax = MAXVALUE(umax);
  ures = (ua + ub) + ((uint16_t) cf);
  *outcf = (ua > (umax - ub)) || ((cf == 1) && ((ua + ub) == umax));
  return (uint16_t) ures;
}


inline static int16_t ADD_CARRY_s16(int16_t a, int16_t b, int16_t cf, int *outcf)
{
  uint16_t ua;
  uint16_t ub;
  uint16_t ures;
  uint16_t umax;
  int f;
  ua = (uint16_t) a;
  ub = (uint16_t) b;
  umax = MAXVALUE(umax);
  ures = (ua + ub) + ((uint16_t) cf);
  *outcf = (ua > (umax - ub)) || ((cf == 1) && ((ua + ub) == umax));
  return (int16_t) ures;
}


inline static uint32_t ADD_CARRY_u32(uint32_t a, uint32_t b, uint32_t cf, int *outcf)
{
  uint32_t ua;
  uint32_t ub;
  uint32_t ures;
  uint32_t umax;
  int f;
  ua = (uint32_t) a;
  ub = (uint32_t) b;
  umax = MAXVALUE(umax);
  ures = (ua + ub) + ((uint32_t) cf);
  *outcf = (ua > (umax - ub)) || ((cf == 1) && ((ua + ub) == umax));
  return (uint32_t) ures;
}


inline static int32_t ADD_CARRY_s32(int32_t a, int32_t b, int32_t cf, int *outcf)
{
  uint32_t ua;
  uint32_t ub;
  uint32_t ures;
  uint32_t umax;
  int f;
  ua = (uint32_t) a;
  ub = (uint32_t) b;
  umax = MAXVALUE(umax);
  ures = (ua + ub) + ((uint32_t) cf);
  *outcf = (ua > (umax - ub)) || ((cf == 1) && ((ua + ub) == umax));
  return (int32_t) ures;
}


inline static uint64_t ADD_CARRY_u64(uint64_t a, uint64_t b, uint64_t cf, int *outcf)
{
  uint64_t ua;
  uint64_t ub;
  uint64_t ures;
  uint64_t umax;
  int f;
  ua = (uint64_t) a;
  ub = (uint64_t) b;
  umax = MAXVALUE(umax);
  ures = (ua + ub) + ((uint64_t) cf);
  *outcf = (ua > (umax - ub)) || ((cf == 1) && ((ua + ub) == umax));
  return (uint64_t) ures;
}


inline static int64_t ADD_CARRY_s64(int64_t a, int64_t b, int64_t cf, int *outcf)
{
  uint64_t ua;
  uint64_t ub;
  uint64_t ures;
  uint64_t umax;
  int f;
  ua = (uint64_t) a;
  ub = (uint64_t) b;
  umax = MAXVALUE(umax);
  ures = (ua + ub) + ((uint64_t) cf);
  *outcf = (ua > (umax - ub)) || ((cf == 1) && ((ua + ub) == umax));
  return (int64_t) ures;
}


inline static uint16_t SUB_CARRY_u16(uint16_t a, uint16_t b, uint16_t cf, int *outcf)
{
  uint16_t ua;
  uint16_t ub;
  uint16_t ures;
  int f;
  ua = (uint16_t) a;
  ub = (uint16_t) b;
  ures = ua - (ub + ((uint16_t) cf));
  *outcf = (ub > ua) || ((cf == 1) && (ua == ub));
  return (uint16_t) ures;
}


inline static int16_t SUB_CARRY_s16(int16_t a, int16_t b, int16_t cf, int *outcf)
{
  uint16_t ua;
  uint16_t ub;
  uint16_t ures;
  int f;
  ua = (uint16_t) a;
  ub = (uint16_t) b;
  ures = ua - (ub + ((uint16_t) cf));
  *outcf = (ub > ua) || ((cf == 1) && (ua == ub));
  return (int16_t) ures;
}


inline static uint32_t SUB_CARRY_u32(uint32_t a, uint32_t b, uint32_t cf, int *outcf)
{
  uint32_t ua;
  uint32_t ub;
  uint32_t ures;
  int f;
  ua = (uint32_t) a;
  ub = (uint32_t) b;
  ures = ua - (ub + ((uint32_t) cf));
  *outcf = (ub > ua) || ((cf == 1) && (ua == ub));
  return (uint32_t) ures;
}


inline static int32_t SUB_CARRY_s32(int32_t a, int32_t b, int32_t cf, int *outcf)
{
  uint32_t ua;
  uint32_t ub;
  uint32_t ures;
  int f;
  ua = (uint32_t) a;
  ub = (uint32_t) b;
  ures = ua - (ub + ((uint32_t) cf));
  *outcf = (ub > ua) || ((cf == 1) && (ua == ub));
  return (int32_t) ures;
}


inline static uint64_t SUB_CARRY_u64(uint64_t a, uint64_t b, uint64_t cf, int *outcf)
{
  uint64_t ua;
  uint64_t ub;
  uint64_t ures;
  int f;
  ua = (uint64_t) a;
  ub = (uint64_t) b;
  ures = ua - (ub + ((uint64_t) cf));
  *outcf = (ub > ua) || ((cf == 1) && (ua == ub));
  return (uint64_t) ures;
}


inline static int64_t SUB_CARRY_s64(int64_t a, int64_t b, int64_t cf, int *outcf)
{
  uint64_t ua;
  uint64_t ub;
  uint64_t ures;
  int f;
  ua = (uint64_t) a;
  ub = (uint64_t) b;
  ures = ua - (ub + ((uint64_t) cf));
  *outcf = (ub > ua) || ((cf == 1) && (ua == ub));
  return (int64_t) ures;
}


inline static int16_t MACHINE_SPECIFIC_execute_rem_divide_by_neg_s16(int16_t a, int16_t b)
{
  return a % ABSOLUTE(b);
}


inline static int32_t MACHINE_SPECIFIC_execute_rem_divide_by_neg_s32(int32_t a, int32_t b)
{
  return a % ABSOLUTE(b);
}


inline static int64_t MACHINE_SPECIFIC_execute_rem_divide_by_neg_s64(int64_t a, int64_t b)
{
  return a % ABSOLUTE(b);
}


inline static uint16_t SHL_u16(uint16_t a, uint32_t b)
{
  if (b >= INTWIDTH(a))
  {
    b = INTWIDTH(a);
    a <<= b - 1;
    return a << 1;
  }
  else
  {
    return a << b;
  }

}


inline static uint32_t SHL_u32(uint32_t a, uint32_t b)
{
  if (b >= INTWIDTH(a))
  {
    b = INTWIDTH(a);
    a <<= b - 1;
    return a << 1;
  }
  else
  {
    return a << b;
  }

}


inline static uint64_t SHL_u64(uint64_t a, uint32_t b)
{
  if (b >= INTWIDTH(a))
  {
    b = INTWIDTH(a);
    a <<= b - 1;
    return a << 1;
  }
  else
  {
    return a << b;
  }

}


inline static int16_t SHR_s16(int16_t a, uint32_t b)
{
  if (b >= INTWIDTH(a))
  {
    b = INTWIDTH(a);
    a >>= b - 1;
    return a >> 1;
  }
  else
  {
    return a >> b;
  }

}


inline static int32_t SHR_s32(int32_t a, uint32_t b)
{
  if (b >= INTWIDTH(a))
  {
    b = INTWIDTH(a);
    a >>= b - 1;
    return a >> 1;
  }
  else
  {
    return a >> b;
  }

}


inline static int64_t SHR_s64(int64_t a, uint32_t b)
{
  if (b >= INTWIDTH(a))
  {
    b = INTWIDTH(a);
    a >>= b - 1;
    return a >> 1;
  }
  else
  {
    return a >> b;
  }

}


inline static uint16_t SHR_u16(uint16_t a, uint32_t b)
{
  if (b >= INTWIDTH(a))
  {
    b = INTWIDTH(a);
    a >>= b - 1;
    return a >> 1;
  }
  else
  {
    return a >> b;
  }

}


inline static uint32_t SHR_u32(uint32_t a, uint32_t b)
{
  if (b >= INTWIDTH(a))
  {
    b = INTWIDTH(a);
    a >>= b - 1;
    return a >> 1;
  }
  else
  {
    return a >> b;
  }

}


inline static uint64_t SHR_u64(uint64_t a, uint32_t b)
{
  if (b >= INTWIDTH(a))
  {
    b = INTWIDTH(a);
    a >>= b - 1;
    return a >> 1;
  }
  else
  {
    return a >> b;
  }

}


#if __STDC_VERSION__ >= 201101L
#define MULWIDE(X, Y) _Generic(X, \
                               uint16_t: MULWIDE_u16_u32, \
                               uint32_t: MULWIDE_u32_u64, \
                               uint64_t: MULWIDE_u64_u128, \
                               int16_t: MULWIDE_s16_s32, \
                               int32_t: MULWIDE_s32_s64, \
                               int64_t: MULWIDE_s64_s128)(X, Y)

#define MUL24(X, Y) _Generic(X, \
                             uint32_t: MUL24_u32_u64, \
                             int32_t: MUL24_s32_s64)(X, Y)

#define SATURATE(X) _Generic(X, \
                             float: SAT_f32, \
                             double: SAT_f64)(X)

#define MAX(X, Y) _Generic(X, \
                           int16_t: MAX_s16, \
                           int32_t: MAX_s32, \
                           int64_t: MAX_s64, \
                           uint16_t: MAX_u16, \
                           uint32_t: MAX_u32, \
                           uint64_t: MAX_u64)(X, Y)

#define MIN(X, Y) _Generic(X, \
                           float: MIN_f32, \
                           double: MIN_f64, \
                           int16_t: MIN_s16, \
                           int32_t: MIN_s32, \
                           int64_t: MIN_s64, \
                           uint16_t: MIN_u16, \
                           uint32_t: MIN_u32, \
                           uint64_t: MIN_u64)(X, Y)

#define ADD_ROUND(X, Y, M) _Generic(X, \
                                    float: ADD_ROUND_f32, \
                                    double: ADD_ROUND_f64)(X, Y, M)

#define SUB_ROUND(X, Y, M) _Generic(X, \
                                    float: SUB_ROUND_f32, \
                                    double: SUB_ROUND_f64)(X, Y, M)

#define MUL_ROUND(X, Y, M) _Generic(X, \
                                    float: MUL_ROUND_f32, \
                                    double: MUL_ROUND_f64)(X, Y, M)

#define DIV_ROUND(X, Y, M) _Generic(X, \
                                    float: DIV_ROUND_f32, \
                                    double: DIV_ROUND_f64)(X, Y, M)

#define FMA_ROUND(X, Y, Z, M) _Generic(X, \
                                       float: FMA_ROUND_f32, \
                                       double: FMA_ROUND_f64)(X, Y, Z, M)

#define RCP_ROUND(X, M) _Generic(X, \
                                 float: RCP_ROUND_f32, \
                                 double: RCP_ROUND_f64)(X, M)

#define SQRT_ROUND(X, M) _Generic(X, \
                                  float: SQRT_ROUND_f32, \
                                  double: SQRT_ROUND_f64)(X, M)

#define extractAndZeroExt_4(X, Y) _Generic(Y, \
                                           uint32_t*: extractAndZeroExt_4_u32, \
                                           int32_t*: extractAndZeroExt_4_s32)(X, Y)

#define extractAndZeroExt_2(X, Y) _Generic(Y, \
                                           uint32_t*: extractAndZeroExt_2_u32, \
                                           int32_t*: extractAndZeroExt_2_s32)(X, Y)

#define extractAndSignExt_4(X, Y) _Generic(Y, \
                                           uint32_t*: extractAndSignExt_4_u32, \
                                           int32_t*: extractAndSignExt_4_s32)(X, Y)

#define extractAndSignExt_2(X, Y) _Generic(Y, \
                                           uint32_t*: extractAndSignExt_2_u32, \
                                           int32_t*: extractAndSignExt_2_s32)(X, Y)

#define ADD_CARRY(W, X, Y, Z) _Generic(W, \
                                       uint16_t: ADD_CARRY_u16, \
                                       int16_t: ADD_CARRY_s16, \
                                       uint32_t: ADD_CARRY_u32, \
                                       int32_t: ADD_CARRY_s32, \
                                       uint64_t: ADD_CARRY_u64, \
                                       int64_t: ADD_CARRY_s64)(W, X, Y, Z)

#define SUB_CARRY(W, X, Y, Z) _Generic(W, \
                                       uint16_t: SUB_CARRY_u16, \
                                       int16_t: SUB_CARRY_s16, \
                                       uint32_t: SUB_CARRY_u32, \
                                       int32_t: SUB_CARRY_s32, \
                                       uint64_t: SUB_CARRY_u64, \
                                       int64_t: SUB_CARRY_s64)(W, X, Y, Z)

#define MACHINE_SPECIFIC_execute_rem_divide_by_neg(X, Y) _Generic(X, \
                                                                  int16_t: MACHINE_SPECIFIC_execute_rem_divide_by_neg_s16, \
                                                                  int32_t: MACHINE_SPECIFIC_execute_rem_divide_by_neg_s32, \
                                                                  int64_t: MACHINE_SPECIFIC_execute_rem_divide_by_neg_s64)(X, Y)

#define SHL(X, Y) _Generic(X, \
                           uint16_t: SHL_u16, \
                           uint32_t: SHL_u32, \
                           uint64_t: SHL_u64)(X, Y)

#define SHR(X, Y) _Generic(X, \
                           int16_t: SHR_s16, \
                           int32_t: SHR_s32, \
                           int64_t: SHR_s64, \
                           uint16_t: SHR_u16, \
                           uint32_t: SHR_u32, \
                           uint64_t: SHR_u64)(X, Y)

#endif