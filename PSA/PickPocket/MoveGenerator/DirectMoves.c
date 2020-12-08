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

void CalcShotAngle(struct Move* move)
{ double dist_trgt_cue = 0;
  dist_trgt_cue = distance(move->target,move->cue);
  move->ghostball.x = move->target.position.x+BallDiameter*(move->target.position.x-move->pocket.x)/dist_trgt_cue;
  move->ghostball.x = move->target.position.y+BallDiameter*(move->target.position.y-move->pocket.y)/dist_trgt_cue;
  move->aiming_vec.from.x = move->cue.position.x;
  move->aiming_vec.from.y = move->cue.postion.y;
  move->aiming_vec.to.x = move->ghostball.x;
  move->aiming_vec.to.y = move->ghostball.y;
  move->target_vec.from.x = move->pocket.x;
  move->target_vec.from.y = move->pocket.y;
  move->target_vec.to.x = move->ghostball.x;
  move->target_vec.to.y = move->ghostball.y;

}

double distance(struct Point p1,struct Point p2)
{
  return sqrt(pow(p1.x-p2.x,2),pow(p1.y-p2.y,2));
}

double angle_between(struct Segment s1,struct Segment s2)
{
  


}
