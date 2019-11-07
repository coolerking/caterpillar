# -*- coding: utf-8 -*-

def test_motor(use_debug=True):
    import pigpio
    pgio = pigpio.pi()

    import donkeycar as dk
    cfg = dk.load_config()
    V = dk.vehicle.Vehicle()

    class TestDriver:
        def __init__(self, debug=False):
            self.values = [
                [1, 0, 0.0], [1, 0, 0.1], [1, 0, 0.2], [1, 0, 0.3], [1, 0, 0.4], [1, 0, 0.5],
                [1, 0, 0.5], [1, 0, 0.4], [1, 0, 0.3], [1, 0, 0.2], [1, 0, 0.1], [1, 0, 0.0],
                [0, 1, 0.0], [0, 1, 0.1], [0, 1, 0.2], [0, 1, 0.3], [0, 1, 0.4], [0, 1, 0.5],
                [0, 1, 0.5], [0, 1, 0.4], [0, 1, 0.3], [0, 1, 0.2], [0, 1, 0.1], [0, 1, 0.0],
            ]
            self.debug = debug
            self.count = 0

        def run(self):
            vals = self.values[self.count]
            self.count = self.count + 1
            if self.count >= len(self.values):
                self.count = 0
            if self.debug:
                print('in1:{}, in2:{}, pwm:{}'.format(str(vals[0]), str(vals[1]), str(vals[2])))
            return vals[0], vals[1], vals[2], vals[0], vals[1], vals[2]
        
        def shutdown(self):
            self.count = 0
            self.debug = False

    V.add(TestDriver(debug=use_debug), outputs=[
        'left_motor_in1', 'left_motor_in2', 'left_motor_vref',
        'right_motor_in1', 'right_motor_in2', 'right_motor_vref'
    ])

    from parts import PIGPIO_OUT, PIGPIO_PWM

    # TB6612 STBY ピン初期化
    #stby = PIGPIO_OUT(pin=cfg.TB6612_STBY_GPIO, pgio=pgio, debug=use_debug)
    #stby.run(1)

    # 左モータ制御
    left_in1 = PIGPIO_OUT(pin=cfg.LEFT_MOTOR_IN1_GPIO, pgio=pgio, debug=use_debug)
    left_in2 = PIGPIO_OUT(pin=cfg.LEFT_MOTOR_IN2_GPIO, pgio=pgio, debug=use_debug)
    left_vref = PIGPIO_PWM(pin=cfg.LEFT_MOTOR_PWM_GPIO, pgio=pgio, freq=cfg.PWM_FREQ, range=cfg.PWM_RANGE, debug=use_debug)
    V.add(left_in1, inputs=['left_motor_in1'])
    V.add(left_in2, inputs=['left_motor_in2'])
    V.add(left_vref, inputs=['left_motor_vref'])  

    # 右モータ制御
    right_in1 = PIGPIO_OUT(pin=cfg.RIGHT_MOTOR_IN1_GPIO, pgio=pgio, debug=use_debug)
    right_in2 = PIGPIO_OUT(pin=cfg.RIGHT_MOTOR_IN2_GPIO, pgio=pgio, debug=use_debug)
    right_vref = PIGPIO_PWM(pin=cfg.RIGHT_MOTOR_PWM_GPIO, pgio=pgio, freq=cfg.PWM_FREQ, range=cfg.PWM_RANGE, debug=use_debug)
    V.add(right_in1, inputs=['right_motor_in1'])
    V.add(right_in2, inputs=['right_motor_in2'])
    V.add(right_vref, inputs=['right_motor_vref'])

    try:
        print('Start driving')
        #run the vehicle for 20 seconds
        V.start(rate_hz=cfg.DRIVE_LOOP_HZ, max_loop_count=cfg.MAX_LOOPS)
    except KeyboardInterrupt:
        print('Halt driving')
    finally:
        #if stby is not None:
        #    stby.run(0)
        #    if use_debug:
        #        print('Stop TB6612 STBY')
        if pgio is not None:
            pgio.stop()
            if use_debug:
                print('Stop pigpio controll')
        print('Stop driving')


def test_pad(use_debug=False):
    import donkeycar as dk
    cfg = dk.load_config()
    V = dk.vehicle.Vehicle()

    from parts import get_js_controller
        
    ctr = get_js_controller(cfg)
        
    V.add(ctr, 
          inputs=['cam/image_array'],
          outputs=['user/angle', 'user/throttle', 'user/mode', 'recording'],
          threaded=True)

    V.mem['pilot/angle'] = 0.0
    V.mem['pilot/throttle'] = 0.0


    class DriveMode:
        def run(self, mode, 
                    user_angle, user_throttle,
                    pilot_angle, pilot_throttle):
            if mode == 'user': 
                return user_angle, user_throttle
            
            elif mode == 'local_angle':
                return pilot_angle, user_throttle
            
            else: 
                return pilot_angle, pilot_throttle * cfg.AI_THROTTLE_MULT
        

    V.add(DriveMode(), 
        inputs=['user/mode', 'user/angle', 'user/throttle', 'pilot/angle', 'pilot/throttle'], 
        outputs=['angle', 'throttle'])
    
    class TestPad:
        def run(self, angle, throttle, mode, recording):
            print('an:{} th:{} mode:{}, rec:{}'.format(
                str(angle), str(throttle), str(mode), str(recording)
            ))
        def shutdown(self):
            pass
    V.add(TestPad(), inputs=['angle', 'throttle', 'user/mode', 'recording'])

    from parts import CaterpillerMotorDriver
    V.add(CaterpillerMotorDriver(
        left_balance=cfg.LEFT_PWM_BALANCE, 
        right_balance=cfg.RIGHT_PWM_BALANCE,
        debug=False),
        inputs=['throttle', 'angle'],
        outputs=['left_motor_vref', 'left_motor_in1', 'left_motor_in2', 'right_motor_vref', 'right_motor_in1', 'right_motor_in2'])

    class TestDriver:
        def run(self, left_in1, left_in2, left_pwm, right_in1, right_in2, right_pwm):
            print('lin1:{} lin2:{} lpwm:{} rin1:{} rin2:{} rpwm:{}'.format(
                str(left_in1), str(left_in2), str(left_pwm), str(right_in1), str(right_in2), str(right_pwm)
            ))
        def shutdown(self):
            pass
    V.add(TestDriver(), inputs=['left_motor_in1', 'left_motor_in2', 'left_motor_vref', 'right_motor_in1', 'right_motor_in2', 'right_motor_vref'])


    try:
        print('Start driving')
        #run the vehicle for 20 seconds
        V.start(rate_hz=cfg.DRIVE_LOOP_HZ, max_loop_count=cfg.MAX_LOOPS)
    except KeyboardInterrupt:
        print('Halt driving')
    finally:
        print('Stop driving')


if __name__ == '__main__':
    #test_motor(use_debug=True)
    test_pad(use_debug=True)