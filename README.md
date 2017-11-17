# HallettMSE
Version 0.2a

## Info

### HallettMSE?
HallettMSE is a multi-system emulator built in Python 3.6 using Pygame. It is currently Windows only.

### Emulator Support
HallettMSE currently only supports CHIP-8 and SCHIP, but more will be coming in the future

### Does HallettMSE come with ROMs?
All ROMs bundled with HallettMSE are in the public domain and available freely on the web with permission from the author(s). I do not encourage illegal copying of ROMs.

### How to use HallettMSE
The CHIP-8 Emulator is automatically set to run pong on startup. You can run HallettMSE either from the .bat file, or through the IDLE.
To change the ROM, open the source code and change the name of the ROM from the line `self.rom_name = "roms\\CHIP-8\\pong.rom"`

## System Requirements
HallettMSE requires a Windows PC that can run Python 3.6, with Pygame installed.
Please note that the sound for the CHIP-8 and SCHIP emulator is generated using Winsound, which is windows only.
Support for Linux is coming soon

## Changelog

### Version 0.1
- Initial Release
- CHIP-8 Support
- Bundled with sample ROMs

### Version 0.2
- SCHIP support - added compatibility list, 4 games
- Cleaner directory
- New experimental rendering system - expect much higher performance on low-end systems
- Bugfixes

## Todo
- UI for emulator selection
- Expand on CHIP-8 Compatibility list
- Linux support for CHIP-8 and SCHIP
- Options
