# -*- coding: utf-8 -*-
import time

class RGB_LED:
    ''' 
    Toggle a GPIO pin on at max_duty pwm if condition is true, off if condition is false.
    Good for LED pwm modulated
    '''
    def __init__(self, pin_r, pin_g, pin_b, pgio=None, invert_flag=False):
        import pigpio
        pgio = pgio or pigpio.pi()
        from parts import PIGPIO_PWM
        self.pwm_r = PIGPIO_PWM(pin_r, pgio=pgio)
        self.pwm_g = PIGPIO_PWM(pin_g, pgio=pgio)
        self.pwm_b = PIGPIO_PWM(pin_b, pgio=pgio)

        self.invert = invert_flag
        print('setting up gpio in board mode')

        self.pwm_r.run(0)
        self.pwm_g.run(0)
        self.pwm_b.run(0)
        self.zero = 0
        if( self.invert ):
            self.zero = 100

        self.rgb = (50, self.zero, self.zero)

        self.blink_changed = 0
        self.on = False

    def toggle(self, condition):
        if condition:
            r, g, b = self.rgb
            self.set_rgb_duty(r, g, b)
            self.on = True
        else:
            self.set_rgb_duty(self.zero, self.zero, self.zero)
            self.on = False

    def blink(self, rate):
        if time.time() - self.blink_changed > rate:
            self.toggle(not self.on)
            self.blink_changed = time.time()

    def run(self, blink_rate):
        if blink_rate == 0:
            self.toggle(False)
        elif blink_rate > 0:
            self.blink(blink_rate)
        else:
            self.toggle(True)

    def set_rgb(self, r, g, b):
        r = r if not self.invert else 100-r
        g = g if not self.invert else 100-g
        b = b if not self.invert else 100-b
        self.rgb = (r, g, b)
        self.set_rgb_duty(r, g, b)

    def set_rgb_duty(self, r, g, b):
        self.pwm_r.run(r)
        self.pwm_g.run(g)
        self.pwm_b.run(b)

    def shutdown(self):
        self.toggle(False)
        self.pwm_r = None
        self.pwm_g = None
        self.pwm_b = None