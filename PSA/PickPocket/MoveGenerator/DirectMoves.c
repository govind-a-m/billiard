#include <stdio.h>
#include <math.h>
#include "DirectMoves.h"

struct Point Pockets[6] = {
                    {P1_0,P1_1},
                    {P2_0,P2_1},
                    {P1_0,-1*P1_1},
                    {-1*P1_0,-1*P1_1},
                    {-1*P2_0,P2_1},
                    {-1*P1_0,P1_1}
                  };

struct Vector iVec = {1,0};

void CalcShotAngle(struct Move* move)
{ double dist_trgt_cue = 0;
  double shifted_ghost_x = 0;
  double shifted_ghost_y = 0;
  
  dist_trgt_cue = distance(move->target.position,move->cue.position);
  move->ghostball.x = move->target.position.x+BallDiameter*(move->target.position.x-move->pocket.x)/dist_trgt_cue;
  move->ghostball.x = move->target.position.y+BallDiameter*(move->target.position.y-move->pocket.y)/dist_trgt_cue;
  move->aiming_vec.from.x = move->cue.position.x;
  move->aiming_vec.from.y = move->cue.position.y;
  move->aiming_vec.to.x = move->ghostball.x;
  move->aiming_vec.to.y = move->ghostball.y;
  move->target_vec.to.x = move->pocket.x;
  move->target_vec.to.y = move->pocket.y;
  move->target_vec.from.x = move->ghostball.x;
  move->target_vec.from.y = move->ghostball.y;
  ComputeSegmentVec(&(move->target_vec));
  ComputeSegmentVec(&(move->aiming_vec));
  move->shotangle = AngleBtwVectors(&(move->target_vec.vec),&(move->aiming_vec.vec));
  shifted_ghost_x = move->ghostball.x-move->cue.position.x;
  shifted_ghost_y = move->ghostball.y-move->cue.position.y;
  move->aiming_vec_ag = atan(shifted_ghost_y/shifted_ghost_x);
  if(shifted_ghost_x>0)
  {
    move->aiming_vec_ag = M_PI+move->aiming_vec_ag;
  }
}

void CheckValidity(struct Move* move,struct Ball* ball)
{ struct Ball b;
  double min_dst_to_aiming_line;
  double min_dst_to_target_line;

  move->valid = 0;
  if(move->shotangle>MIN_AngleOfStrike)
  {
    for(int i=0;i<6;i++)
    { 
      b = *(ball+i);
      if(b.valid)
      {
        min_dst_to_aiming_line = PerpSegment(move->aiming_vec,b.position);
        min_dst_to_target_line = PerpSegment(move->target_vec,b.position);
        if((min_dst_to_aiming_line<BallDiameter)||(min_dst_to_target_line<BallDiameter))
        {
          move->valid = i;
        }
      }
    }
  }
  else
  {
    move->valid = 2;
  }
}

void CalcMinVelocity_reqd(struct Move* move)
{
  move->target_vel = CONST_P1*move->target_vec.length+CONST_P2;
  move->impact_vel = 2*move->target_vel*cos(move->shotangle);
  move->v = move->impact_vel+(CONST_P1*move->aiming_vec.length+CONST_P2);
}



void ComputeSegmentVec(struct Segment* seg)
{ 
  seg->vec.x = seg->to.x-seg->from.x;
  seg->vec.y = seg->to.y-seg->from.y;
  seg->length = VectorLength(*(seg->vec));
}


double AngleBtwVectors(struct Vector vec1,struct Vector vec2)
{
  return acos(VectorDot(vec1,vec2)/(VectorLength(vec1)*VectorLength(vec2)));
}


double VectorLength(struct Vector vec)
{
  return sqrt(pow(vec.x,2),pow(vec.y,2));
}

double distance(struct Point p1,struct Point p2)
{
  return sqrt(pow(p1.x-p2.x,2),pow(p1.y-p2.y,2));
}

double VectorDot(struct Vector vec1,struct Vector vec2)
{
  return vec1.x*vec2.x+vec1.y*vec2.y;
}

double PerpSegment(struct Segment seg,struct Point p)
{ double a,b,c,h;

  a = distance(seg.from,p);
  b = seg.length;
  c = distance(seg.to,p);
  h = 0.5*sqrt((a + b + c)*(-a + b + c)*(a - b + c)*(a + b - c))/b;//herons formula
  if((h<=a) && (h<=b))
  {
    return h;
  }
  return 99999;
}