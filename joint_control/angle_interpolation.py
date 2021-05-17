'''In this exercise you need to implement an angle interploation function which makes NAO executes keyframe motion

* Tasks:
    1. complete the code in `AngleInterpolationAgent.angle_interpolation`,
       you are free to use splines interploation or Bezier interploation,
       but the keyframes provided are for Bezier curves, you can simply ignore some data for splines interploation,
       please refer data format below for details.
    2. try different keyframes from `keyframes` folder

* Keyframe data format:
    keyframe := (names, times, keys)
    names := [str, ...]  # list of joint names
    times := [[float, float, ...], [float, float, ...], ...]
    # times is a matrix of floats: Each line corresponding to a joint, and column element to a key.
    keys := [[float, [int, float, float], [int, float, float]], ...]
    # keys is a list of angles in radians or an array of arrays each containing [float angle, Handle1, Handle2],
    # where Handle is [int InterpolationType, float dTime, float dAngle] describing the handle offsets relative
    # to the angle and time of the point. The first Bezier param describes the handle that controls the curve
    # preceding the point, the second describes the curve following the point.
'''
import scipy.interpolate

from pid import PIDAgent
from keyframes import hello, wipe_forehead


class AngleInterpolationAgent(PIDAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(AngleInterpolationAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.keyframes = ([], [], [])
        # MY CODE HERE
        self._start_time = None
        self._prev_time = 0

    def think(self, perception):
        target_joints = self.angle_interpolation(self.keyframes, perception)
        self.target_joints.update(target_joints)
        return super(AngleInterpolationAgent, self).think(perception)

    def angle_interpolation(self, keyframes, perception):
        target_joints = {}
        # YOUR CODE HERE

        if not self._start_time:
            self._start_time = perception.time

        for i, joint_name in enumerate(keyframes[0]):
            times = keyframes[1][i]
            keys = keyframes[2][i]

            x = []
            x.extend(times)
            y = [key[0] for key in keys]

            k = len(x) - 1 if len(x) <= 3 else 3

            rel_time = perception.time - self._start_time

            if rel_time > times[-1]:
                continue

            tck = scipy.interpolate.splrep(x=x, y=y, k=k)
            r = scipy.interpolate.splev([rel_time + 0.025], tck)

            target_joints[joint_name] = r[0]

        return target_joints


if __name__ == '__main__':
    agent = AngleInterpolationAgent()
    agent.keyframes = hello()  # wipe_forehead(None)  # CHANGE DIFFERENT KEYFRAMES
    agent.run()
