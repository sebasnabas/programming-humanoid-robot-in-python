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

    def think(self, perception):
        target_joints = self.angle_interpolation(self.keyframes, perception)
        self.target_joints.update(target_joints)
        return super(AngleInterpolationAgent, self).think(perception)

    def angle_interpolation(self, keyframes, perception):
        target_joints = {}
        # YOUR CODE HERE
        for i, joint_name in enumerate(keyframes[0]):
            times = keyframes[1][i]
            keys = keyframes[2][i]

            if len(times) < 1 or joint_name not in perception.joint.keys():
                continue

            angle = keys[0][0]
            if joint_name in perception.joint.keys() and abs(angle - perception.joint[joint_name]) < 0.00001:
                times.pop(0)
                angle = keys.pop(0)[0]

            time = times[0]
            p0_angle = perception.joint[joint_name]
            p1_angle = keys[0][1][-1]
            p2_angle = angle
            p3_angle = keys[0][-1][-1]

            t = perception.time / (perception.time + time)

            bezier_interpolation = \
                (1 - 3)**3 * p0_angle \
                    + 3*(1 - t)**2 * t * p1_angle \
                        + 3*(1 - t) * t**2 * p2_angle \
                            + t**3 * p3_angle
            target_joints[joint_name] = bezier_interpolation

        return target_joints


if __name__ == '__main__':
    agent = AngleInterpolationAgent()
    agent.keyframes = wipe_forehead(None)  # CHANGE DIFFERENT KEYFRAMES
    agent.run()
