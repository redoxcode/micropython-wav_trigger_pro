#WAV Trigger Pro I2C library
#This is a micropython port of
#https://github.com/robertsonics/WAV_Trigger_Pro_Qwiic_Arduino_Library

import machine
import time

class wavTriggerPro:
    WAV_TRIGGER_PRO_DEFAULT_ADDR = 0x13

    CMD_GET_VERSION=1
    CMD_GET_NUM_TRACKS=2
    CMD_TRACK_PLAY_POLY=3
    CMD_GET_TRACK_STATUS=4
    CMD_GET_NUM_ACTIVE_VOICES=5
    CMD_TRACK_SET_LOOP=6
    CMD_TRACK_SET_LOCK=7
    CMD_STOP_ALL= 8
    CMD_TRACK_STOP=9
    CMD_TRACK_FADE=10
    CMD_MIDI_MSG=11
    CMD_LOAD_PRESET=12
    CMD_SET_OUTPUT_GAIN=13


    LOOP_FLAG=0x01
    LOCK_FLAG=0x02
    PITCH_BEND_FLAG=0x04
    BALANCE_MID=64

    RESPONSE_DELAY = 0.002
    
    def __init__(self,i2c,addr = WAV_TRIGGER_PRO_DEFAULT_ADDR):
        self.i2c = i2c
        self.addr = addr

    def get_address(self):
        return self.addr;

    def get_version(self):
        self.i2c.writeto(self.addr, bytes([self.CMD_GET_VERSION]))
        return self.i2c.readfrom(self.addr,12)

    def get_num_tracks(self):
        self.i2c.writeto(self.addr, bytes([self.CMD_GET_NUM_TRACKS]))
        rxbuf = self.i2c.readfrom(self.addr,2)
        numTracks = rxbuf[1];
        numTracks = (numTracks << 8) + rxbuf[0];
        return int(numTracks)

    def play_track_poly(self,track, gainDb=0, bal=BALANCE_MID, attackMs=0, cents=0, flags=0):
        txbuf = bytearray(12)
        txbuf[0] = self.CMD_TRACK_PLAY_POLY
        txbuf[1] = track
        txbuf[2] = (track >> 8)
        txbuf[3] = gainDb
        txbuf[4] = (gainDb >> 8)
        txbuf[5] = bal
        txbuf[6] = attackMs
        txbuf[7] = attackMs >> 8
        txbuf[8] = cents
        txbuf[9] = cents >> 8
        txbuf[10] = flags
        self.i2c.writeto(self.addr, txbuf)

    def track_fade(self,track, gainDb=0, timeMs=500):
        txbuf = bytearray(8)
        txbuf[0] = self.CMD_TRACK_FADE
        txbuf[1] = track
        txbuf[2] = (track >> 8)
        txbuf[3] = gainDb
        txbuf[4] = (tmp16 >> 8)
        txbuf[5] = timeMs
        txbuf[6] = (timeMs >> 8)
        self.i2c.writeto(self.addr, txbuf)


    def track_set_loop(self,track, loop=True):
        txbuf = bytearray(6)
        txbuf[0] = self.CMD_TRACK_SET_LOOP
        txbuf[1] = track
        txbuf[2] = (track >> 8)
        txbuf[3] = 1 if loop else 0
        self.i2c.writeto(self.addr, txbuf)

    def track_set_lock(self,track, lock=True):
        txbuf = bytearray(6)
        txbuf[0] = self.CMD_TRACK_SET_LOCK
        txbuf[1] = track
        txbuf[2] = (track >> 8)
        txbuf[3] = 1 if lock else 0
        self.i2c.writeto(self.addr, txbuf)

    def track_stop(self,track, releaseMs=0):
        txbuf = bytearray(6)
        txbuf[0] = self.CMD_TRACK_STOP
        txbuf[1] = track
        txbuf[2] = (track >> 8)
        txbuf[3] = releaseMs
        txbuf[4] = (releaseMs >> 8)
        self.i2c.writeto(self.addr, txbuf)
        
    def get_num_active_voices(self):
        txbuf = bytearray(2)
        txbuf[0] = self.CMD_GET_NUM_ACTIVE_VOICES
        self.i2c.writeto(self.addr, txbuf)
        time.sleep(self.RESPONSE_DELAY)
        rxbuf = self.i2c.readfrom(self.addr,1)
        numVoices = rxbuf[0];
        return int(numVoices)

    def track_get_status(self,track):
        txbuf = bytearray(4)
        txbuf[0] = self.CMD_GET_TRACK_STATUS
        txbuf[1] = track
        txbuf[2] = (track >> 8)
        self.i2c.writeto(self.addr, txbuf)
        time.sleep(self.RESPONSE_DELAY)
        rxbuf = self.i2c.readfrom(self.addr,1)
        trackStat = rxbuf[0]
        return int(trackStat)

    def stop_all(self):
        txbuf = bytearray(2)
        txbuf[0] = self.CMD_STOP_ALL
        self.i2c.writeto(self.addr, txbuf)

    def send_midi_msg(self,cmd, dat1, dat2):
        txbuf = bytearray(6)
        txbuf[0] = self.CMD_MIDI_MSG
        txbuf[1] = cmd
        txbuf[2] = dat1 & 0x7f
        txbuf[3] = dat2 & 0x7f
        self.i2c.writeto(self.addr, txbuf)
        
    def load_preset(self,preset):
        txbuf = bytearray(4)
        txbuf[0] = self.CMD_LOAD_PRESET
        txbuf[1] = preset
        txbuf[2] = (preset >> 8)
        self.i2c.writeto(self.addr, txbuf)

    def set_output_gain(self,gainDb=0):
        txbuf = bytearray(4)
        txbuf[0] = self.CMD_SET_OUTPUT_GAIN
        txbuf[1] = gainDb
        txbuf[2] = (gainDb >> 8)
        self.i2c.writeto(self.addr, txbuf)
