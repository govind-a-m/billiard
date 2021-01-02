#include <math.h>

#ifndef M_PI 
#define M_PI acos(-1.0)
#endif
// Ball parameters
#define BallRadius 0.5
#define BallDiameter 1.00

// Table measurements
#define half_width_inner 8.875
#define half_width_outer 9.85
#define half_length_inner 18.775
#define half_length_outer 19.7
#define half_mid_width (half_width_inner+half_width_outer)/2
#define P1_0 (half_width_inner+half_width_outer)/2
#define P1_1 (half_length_inner+half_length_outer)/2
#define P2_0 half_mid_width
#define P2_1 0

#define MIN_AngleOfStrike ((86*M_PI)/180)
#define CONST_P1 1.602
#define CONST_P2 20.49

struct Point
{
  double x;
  double y;
};

enum ballname
{
  CueBall=0,
  Ball1,
  Ball2,
  Ball3,
  Ball4,
  Ball5,
  Ball6,

};

struct Vector
{
  double x;
  double y;
};

struct  Ball
{
  int ballidx;
  struct Point position;
};

struct Segment
{
  struct Point from;
  struct Point to;
  struct Vector vec;
  double length;
};

struct Move
{
  struct Ball cue;
  struct Point pocket;
  struct Ball target;
  struct Point ghostball;
  struct Segment target_vec;
  struct Segment aiming_vec;
  double shotangle;
  unsigned long valid;
  double target_vel;
  double v;
  double impact_vel;
  double aiming_vec_ag;
  double min_dst_to_aiming_line;
  double min_dst_to_target_line;
};

void CalcShotAngle(struct Move* move);
void CheckValidity(struct Move* move,struct Ball* ball,int nof_balls);
void CalcMinVelocity_reqd(struct Move* move);
void ComputeSegmentVec(struct Segment* seg);
double AngleBtwVectors(struct Vector vec1,struct Vector vec2);
double VectorLength(struct Vector vec);
double distance(struct Point p1,struct Point p2);
double VectorDot(struct Vector vec1,struct Vector vec2);
double PerpSegment(struct Segment seg,struct Point p);
void ProcessMove(struct Move* move_ptr,struct Ball* ball_ptr,int nof_balls);

