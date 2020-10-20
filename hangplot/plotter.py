import sys
import time
import math

from config import Config

class Plotter: 
    def __init__(self, config):
        self.left=config.getLeftMotor()
        self.right=config.getRightMotor()
        self.pen=config.getPenMotor()
        self.degreesPerMilli=config.getDegreesPerMilli()
        self.width=config.getAnchorDistance()
        self.standardLength=config.getStandardLength()

    def read_file(self,filename):
        f=open(filename, 'r')
        content=f.read()
        f.close()
        return content.strip()

    def degrees(self,motor):
        return int(self.read_file(motor + '/position'))

    def to_wire_length(self,position):
        left=position[0] ** 2
        height=position[1] ** 2
        opposite=(self.width-position[0]) ** 2
        return (math.sqrt(left + height), math.sqrt(opposite + height))

    def write_file(self,filename, content):
        f=open(filename, 'w')
        f.write(content)
        f.close()

    def start_move(self,motor, target_position, speed):
        self.write_file(motor + '/position_sp', str(int(target_position)))
        self.write_file(motor + '/speed_sp', str(int(speed)))
        self.write_file(motor + '/command', 'run-to-rel-pos')

    def wait_for(self,motor):
        while self.read_file(motor + '/state') == 'running':
            print ('Waiting for ' + motor)
            time.sleep(1)

    def calculate_speed(self,desired_speed, speed):
        max_speed = max(abs(speed[0]), abs(speed[1]))
        scale = desired_speed / max_speed
        return (abs(speed[0] * scale), abs(speed[1] * scale))

    def move_to(self,target):
        current_wires=(self.standardLength + self.degrees(self.left)/self.degreesPerMilli,self.standardLength + self.degrees(self.right)/self.degreesPerMilli)
        print (self.left, self.right, target)
        print (current_wires)
        target_wires=self.to_wire_length(target)
        print (target_wires)
        adjust=(self.degreesPerMilli * (target_wires[0]-current_wires[0]),self.degreesPerMilli * (target_wires[1]-current_wires[1]))
        print (adjust)
        speed=self.calculate_speed(150, adjust)
        print (speed)
        self.start_move(self.left, adjust[0], speed[0])
        self.start_move(self.right, adjust[1], speed[1])
        self.wait_for(self.left)
        self.wait_for(self.right)

    def pen_mode(self,down):
        self.write_file(self.pen + '/speed_sp', '200')
        if down:
            self.write_file(self.pen + '/position_sp', '-150')
        else:
            self.write_file(self.pen + '/position_sp', '150')
        self.write_file(self.pen + '/command', 'run-to-rel-pos')
        self.wait_for(self.pen)
