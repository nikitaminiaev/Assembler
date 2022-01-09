from cred import *

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(ESSID, PASS)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

if __name__ == '__main__':
    import network
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    sta_if.active(True)
    ap_if.active(False)
    sta_if.connect(ESSID, PASS)
    print(sta_if.isconnected())
