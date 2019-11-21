# -*- coding: utf-8 -*-

def test_pad():
    import donkeycar as dk
    cfg = dk.load_config()
    V = dk.vehicle.Vehicle()

    import numpy as np

    V.mem['cam/image_array'] = np.zeros((120, 160, 3))

    from parts.controller import PS3JoystickController
    ctr = PS3JoystickController(
        throttle_dir=cfg.JOYSTICK_THROTTLE_DIR,
        throttle_scale=cfg.JOYSTICK_MAX_THROTTLE,
        steering_scale=cfg.JOYSTICK_STEERING_SCALE,
        auto_record_on_throttle=cfg.AUTO_RECORD_ON_THROTTLE
    )
    V.add(ctr, 
          inputs=['cam/image_array'],
          outputs=['user/angle', 'user/throttle', 'user/mode', 'recording'],
          threaded=True)

    class PrintUser:
        def run(self, a, t, u, r):
            print('a:{} t:{}, u:{}, r:{}'.format(
                str(a), str(t), str(u), str(r)
            ))
    prt = PrintUser()
    V.add(prt, inputs=[
        'user/angle', 'user/throttle', 'user/mode', 'recording'
    ])

    try:
        print('Start driving')
        V.start(rate_hz=cfg.DRIVE_LOOP_HZ, max_loop_count=cfg.MAX_LOOPS)
    except KeyboardInterrupt:
        print('Halt driving')
    finally:
        print('Stop driving')


if __name__ == '__main__':
    test_pad()