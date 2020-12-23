from tkinter import Text, constants as c

SENSOR_NAME = {
    'SERVO_X': 'servo_x',
    'SERVO_Y': 'servo_y',
    'SERVO_Z': 'servo_z',
    'HALL': 'hall',
}


class Dto:

    def __init__(self, sensor_name: str = '', frame=None, side=c.TOP):
        self.sensor_name = sensor_name
        self.var = {
            'sensor': sensor_name,
            'data': '0',
        }
        # self.text = Text(frame, width=25, height=4, bg='darkgreen', fg='white', wrap=c.WORD)
        # self.text.pack(side=side)   # для дебага

    def on_scale(self, val):
        self.var['data'] = str(int((val)))
        # self.text.insert(1.0, str(self.var))
