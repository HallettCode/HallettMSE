# HallettMSE
Version 0.1

## Info

### HallettMSE?
HallettMSE is a multi-system emulator built in Python 3.6 using Numpy. It is currently Windows only.

### Emulator Support
HallettMSE currently only supports CHIP-8, but more will be coming in the future

### Does HallettMSE come with ROMs?
All ROMs bundled with HallettMSE are in the public domain and available freely on the web with permission from the author(s). I do not encourage illegal copying of ROMs.

### How to use HallettMSE
The CHIP-8 Emulator is automatically set to run pong on startup. You can run HallettMSE either from the .bat file, or through the IDLE.
To change the ROM, open the source code and change the name of the ROM in `self.transfer_rom_to_mem("pong.rom")` on line 31.

### Emulator versions
- CHIP-8 - Version 0.1b

### CHIP-8 Controls
For input, the CHIP-8 uses a 16 button hexadecimal keypad with the following keys: 

1 2 3 C  
4 5 6 D  
7 8 9 E  
A 0 B F  

The keyboard mappings are as follows:

1 2 3 4  
Q W E R  
A S D F  
Z X C V  

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
- Add an FPS cap to the main loop for CHIP-8
- **_SCHIP_**
- Linux support for CHIP-8 and SCHIP
- Clean up the directory
- Options
