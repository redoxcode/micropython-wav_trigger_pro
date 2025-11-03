## Description
This is a micropython library for the WAV Trigger Pro by robertsonics (also known as SparkFun Qwiic WAV Trigger Pro).
The WAV Trigger Pro is controlled using I2C (using the Qwiic style 4-pin JST connector).

This is a micropython port of the [arduino library](https://github.com/robertsonics/WAV_Trigger_Pro_Qwiic_Arduino_Library).

The WAV Trigger Pro is documented [here](https://www.robertsonics.com/wtpro-overview).

For your first tests you should use a freshly formated SD card and the example files provided [here](https://drive.google.com/file/d/17SlXueDCNjg29a56VSZPSQ7Gt-WlDesp/view?usp=drive_link).

All tracks should be named like this: 'XXXX_SomeName.wav' Where XXXX is the track number (has to be 4 digets with leading zeros (e.g. 0001, 0002, ...).

## API
### class wavTriggerPro(i2c,addr = WAV_TRIGGER_PRO_DEFAULT_ADDR)
- i2c: the machine.I2C instance to use
- addr: optional i2c address to use

```get_address()```
- Returns the i2c address of the WAV Trigger Pro.

```get_version()```
- Returns a bytes object with the firmware version of the WAV Trigger Pro.

```get_num_tracks()```
- Returns number of tracks found on the installed microSD card.

```track_play_poly(track, gainDb=0, bal=BALANCE_MID, attackMs=0, cents=0, flags=0)```
- This function starts track number t from the beginning, blending it with any other tracks that are currently playing, including potentially another copy of the same track.
- track: Track number to play
- gainDb: Target gain attenuation for the track, from 0 (full volume) to -80
- bal: Left/right balance for the track. 0 = full left, 64 = center, 127 = full right
- attackMs: Attack time in millisecondssecond
- cents: Pitch offset for the track instance, from -700 to +700. 100 cents is equal to one musical semi-tone.
- flags: Any combination of LOOP_FLAG | LOCK_FLAG | PITCH_BEND_FLAG
   - LOOP_FLAG: Track will loop over file length
   - LOCK_FLAG: Track will not yield to voice stealing algorithm
   - PITCH_BEND_FLAG: Track will follow MIDI PitchBend messages

```track_fade(track, gain, time)```
- this command initiates a hardware volume fade on all instances of the specified track number if it is currently playing. The track volume will transition smoothly from the current value to the target gain in the specified number of milliseconds. Use this command to smoothly change the volume of a playing track. To fade out and stop a track, use the trackStop() command below.
- track: Track number to fade
- gain: The target gain
- time: Time in milliseconds to perform the fade

```track_stop(track, releaseMs)```
- This command stops any instance of the specified track using the supplied release value in milliseconds. The track will fade and then stop.
- track: Track number to stop
- time: Time in milliseconds used for the fade out

```track_set_loop(track, loop)```
- Sets or resets the track loop flag.
- track: Track number
- loop: true or false

```track_set_lock(track, lock)```
- Sets or resets the track lock flag.
- track: Track number
- lock: true or false

```track_get_status(track)```
- returns 1 if one or more instances of the specified track are currently playing, otherwise returns 0.
- track: Track number

```stop_all()```
- This command stops all audio.

```get_num_active_voices()```
- This command returns the number of voices currently active.

```send_midi_msg(cmd, dat1, dat2)```
- This command sends a standard 3-byte MIDI message to the WAV Trigger Pro, just as if it had come from a MIDI Controller or Keyboard.
- cmd: Command byte
- dat1: First data byte
- dat2: Second data byte

```load_preset(preset)```
- This command tells the WAV Trigger Pro to load the specified preset from the microSD card.
- preset: Preset id to load

```set_output_gain(gainDb)```
- This sets the overall output gain of the WAV Trigger Pro's stereo audio output.
- gainDb: gain in dB, from 0 to -80dB.
