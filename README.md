# HallettMSE
Version 0.1

## Info

### HallettMSE?
HallettMSE is a multi-system emulator built in Python 3.6 using Pygame. It is currently Windows only.

### Emulator Support
HallettMSE currently only supports CHIP-8, but more will be coming in the future

### Does HallettMSE come with ROMs?
All ROMs bundled with HallettMSE are in the public domain and available freely on the web with permission from the author(s). I do not encourage illegal copying of ROMs.

### How to use HallettMSE
The CHIP-8 Emulator is automatically set to run pong on startup. You can run HallettMSE either from the .bat file, or through the IDLE.
To change the ROM, open the source code and change the name of the ROM in `self.rom_name = "pong.rom"` on line 31.

### Emulator versions
- CHIP-8 - Version 0.1

## System Requirements
HallettMSE requires a Windows PC that can run Python 3.6, with Pygame installed.
Please note that the sound for the CHIP-8 emulator is generated using Winsound, which is windows only.
Support for Linux is coming soon

## Changelog

### Version 0.1
- Initial Release
- CHIP-8 Support
- Bundled with sample ROMs

## Todo
- UI for emulator selection
- Expand on CHIP-8 Compatibility list
- **_SCHIP_**
- Linux support for CHIP-8 and SCHIP
- Clean up the directory
- Options