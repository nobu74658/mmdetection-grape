# Copyright 2016 Bhautik J Joshi
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from .AbstractProjection import AbstractProjection
from mpmath import mp

class SideBySideFisheyeProjection(AbstractProjection):
  def __init__(self):
    AbstractProjection.__init__(self)

  def set_angular_resolution(self):
    mp.dps = 50
    self.angular_resolution = mp.pi/self.imsize[1]

  def _pixel_value(self, angle, rotate=0):
    theta = angle[0]
    phi = angle[1]
    if theta is None or phi is None:
      return (0,0,0)
    
    if theta + rotate > mp.pi:
      return (0,0,0)
    
    # z is elevation in this case
    sphere_pnt = self.point_on_sphere(theta, phi, rotate=rotate)

    u = 0.5+(sphere_pnt[0]*-0.5)
    
    if theta >=0:
      u = u*0.5 + 0.5
    else:
      u = (1.0-u)*0.5

    #sphere_pnt.z: -1..1 -> v: 0..1
    v = 0.5+(sphere_pnt[2]*0.5)

    return self.get_pixel_from_uv(u,v, self.image)

  @staticmethod
  def angular_position(texcoord):
    up = texcoord[0]
    v = texcoord[1]
    # correct for hemisphere
    if up>=0.5:
      u = 2.0*(up-0.5)
    else:
      u = 2.0*up

    # ignore points outside of circles
    if ((u-0.5)*(u-0.5) + (v-0.5)*(v-0.5))>0.25:
      return None, None

    # v: 0..1-> vp: -1..1
    mp.dps = 50
    phi = mp.asin(2.0*(v-0.5))

    # u = mp.cos(phi)*mp.cos(theta)
    # u: 0..1 -> upp: -1..1
    u = 1.0-u

    #丸め誤差でtheta が計算出来なくなるので，その場合の対応
    a = 2.0*(u-0.5) / mp.cos(phi) 
    if (a < -1):
      a = -1.0
    elif( 1 < a ):
      a = 1.0
    
    theta = mp.acos( a )
    #theta = mp.acos( 2.0*(u-0.5) / mp.cos(phi) )

    # if up<0.5:
    #    theta = theta-mp.pi

    # up = texcoord[0]
    # v = texcoord[1]
    # # correct for hemisphere
    # if up>=0.5:
    #   u = 2.0*(up-0.5)
    # else:
    #   u = 2.0*up

    # # ignore points outside of circles
    # if ((u-0.5)*(u-0.5) + (v-0.5)*(v-0.5))>0.25:
    #   return None, None

    # # v: 0..1-> vp: -1..1
    # mp.dps = 100
    # phi = mp.asin(2.0*(v-0.5))

    # # u = math.cos(phi)*math.cos(theta)
    # # u: 0..1 -> upp: -1..1
    # u = 1.0-u
    # theta = mp.acos( 2.0*(u-0.5) / mp.cos(phi) )

    # if up<0.5:
    #    theta = theta-mp.pi

    return (theta,phi)
