import random
import pygame, pygame.gfxdraw
import winsound

class Chip8:
    def __init__(self):
        self.memory = [0]*4096
        self.fontset = [0xF0, 0x90, 0x90, 0x90, 0xF0, 0x20, 0x60, 0x20, 0x20, 0x70, 0xF0, 0x10, 0xF0, 0x80, 0xF0, 0xF0, 0x10, 0xF0, 0x10, 0xF0, 0x90, 0x90, 0xF0, 0x10, 0x10, 0xF0, 0x80, 0xF0, 0x10, 0xF0, 0xF0, 0x80, 0xF0, 0x90, 0xF0, 0xF0, 0x10, 0x20, 0x40, 0x40, 0xF0, 0x90, 0xF0, 0x90, 0xF0, 0xF0, 0x90, 0xF0, 0x10, 0xF0, 0xF0, 0x90, 0xF0, 0x90, 0x90, 0xE0, 0x90, 0xE0, 0x90, 0xE0, 0xF0, 0x80, 0x80, 0x80, 0xF0, 0xE0, 0x90, 0x90, 0x90, 0xE0, 0xF0, 0x80, 0xF0, 0x80, 0xF0, 0xF0, 0x80, 0xF0, 0x80, 0x80]
        self.super_fontset = [0xff, 0xff, 0xc3, 0xc3, 0xc3, 0xc3, 0xc3, 0xc3, 0xff, 0xff, 0x18, 0x78, 0x78, 0x18, 0x18, 0x18, 0x18, 0x18, 0xff, 0xff, 0xff, 0xff, 0x03, 0x03, 0xff, 0xff, 0xc0, 0xc0, 0xff, 0xff, 0xff, 0xff, 0x03, 0x03, 0xff, 0xff, 0x03, 0x03, 0xff, 0xff, 0xc3, 0xc3, 0xc3, 0xc3, 0xff, 0xff, 0x03, 0x03, 0x03, 0x03, 0xff, 0xff, 0xc0, 0xc0, 0xff, 0xff, 0x03, 0x03, 0xff, 0xff, 0xff, 0xff, 0xc0, 0xc0, 0xff, 0xff, 0xc3, 0xc3, 0xff, 0xff, 0xff, 0xff, 0x03, 0x03, 0x06, 0x0c, 0x18, 0x18, 0x18, 0x18, 0xff, 0xff, 0xc3, 0xc3, 0xff, 0xff, 0xc3, 0xc3, 0xff, 0xff, 0xff, 0xff, 0xc3, 0xc3, 0xff, 0xff, 0x03, 0x03, 0xff, 0xff, 0x7e, 0xff, 0xc3, 0xc3, 0xc3, 0xff, 0xff, 0xc3, 0xc3, 0xc3, 0xfc, 0xfc, 0xc3, 0xc3, 0xfc, 0xfc, 0xc3, 0xc3, 0xfc, 0xfc, 0x3c, 0xff, 0xc3, 0xc0, 0xc0, 0xc0, 0xc0, 0xc3, 0xff, 0x3c, 0xfc, 0xfe, 0xc3, 0xc3, 0xc3, 0xc3, 0xc3, 0xc3, 0xfe, 0xfc, 0xff, 0xff, 0xc0, 0xc0, 0xff, 0xff, 0xc0, 0xc0, 0xff, 0xff, 0xff, 0xff, 0xc0, 0xc0, 0xff, 0xff, 0xc0, 0xc0, 0xc0, 0xc0]
        self.rom = []
        self.V = [0]*16
        self.rpl = [0]*8
        self.stack = [0]*16
        self.delay_timer = 0
        self.sound_timer = 0
        self.display = [[0 for x in range(0,32)] for y in range(0,64)]
        self.keys = [0]*16
        self.bindings = [pygame.K_x, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_z, pygame.K_c, pygame.K_4, pygame.K_r, pygame.K_f, pygame.K_v]
        
        self.pc = 0x200
        self.sp = 0
        self.I = 0

        self.mode = 0

        pygame.display.init()
        self.surface = pygame.Surface((64, 32))
        self.super_surface = pygame.Surface((128,64))
        self.screen = pygame.display.set_mode((640, 360), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Chip8 Emulator")

        self.surfarray = pygame.surfarray.pixels2d(self.surface)
        '''self.surfarray[3][3] = 0xFF0000
        pygame.surfarray.blit_array(self.surface, self.surfarray)
        pygame.transform.scale(self.surface, (self.screen.get_width(), self.screen.get_height()), self.screen)
        pygame.display.flip()
        '''

        for i in range(0, len(self.fontset)):
            self.memory[i] = self.fontset[i]
        for i in range(0, len(self.super_fontset)):
            self.memory[0x50 + i] = self.super_fontset[i]

        self.rom_name = "roms/CHIP-8/pong.rom"
        self.transfer_rom_to_mem(self.rom_name)
        self.main_loop()
    
    def transfer_rom_to_mem(self, rom_name):
        with open(rom_name, 'rb') as f:
            self.rom = list(f.read())
            f.close()
        for i in range(0, len(self.rom)):
            self.memory[0x200 + i] = self.rom[i]

    def update_keys(self):
        for i in range(0, len(self.keys)):
            if pygame.key.get_pressed()[self.bindings[i]]:
                self.keys[i] = 1
            else:
                self.keys[i] = 0

    def interpret_opcode(self, opcode):
        self.NNN = opcode & 0x0FFF
        self.NN = opcode & 0x00FF
        self.X = (opcode & 0x0F00) >> 8
        self.Y = (opcode & 0x00F0) >> 4
        self.N = opcode & 0x000F
        self.ID = opcode & 0xF000
        ##print(format(self.pc, '#04x'), format(opcode, '#05x'))
        ##print(self.V, format(self.I,'#04x'))

        if self.ID == 0x0000:
            if self.Y == 0x000C: ## Scroll display N lines down
                for yline in range(63,self.N-1,-1):
                    for xline in range(0,128):
                        self.display[xline][yline] = self.display[xline][yline-self.N]
                for yline in range(0,self.N):
                    for xline in range(0,128):
                        self.display[xline][yline] = 0
                self.pc += 2
            elif self.NN == 0x00E0:
                if self.mode == 0:
                    self.surfarray.fill(0)
                else:
                    self.display = [[0 for x in range(64)] for y in range(128)]
                self.pc += 2
            elif self.NN == 0x00EE:
                self.sp -= 1
                self.pc = self.stack[self.sp]
            elif self.NN == 0x00FB: ## Scroll display 4 pixels right
                for yline in range(0,64):
                    for xline in range(127,3,-1):
                        self.display[xline][yline] = self.display[xline-4][yline]
                    self.display[0][yline] = 0
                    self.display[1][yline] = 0
                    self.display[2][yline] = 0
                    self.display[3][yline] = 0
                self.pc += 2
            elif self.NN == 0x00FC: ## Scroll display 4 pixels left
                for yline in range(0,64):
                    for xline in range(0,124):
                        self.display[xline][yline] = self.display[xline + 4][yline]
                    self.display[124][yline] = 0
                    self.display[125][yline] = 0
                    self.display[126][yline] = 0
                    self.display[127][yline] = 0
                self.pc += 2
            elif self.NN == 0x00FD:
                self.done = True
            elif self.NN == 0x00FE:
                self.mode = 0
                self.pc += 2
            elif self.NN == 0x00FF:
                self.mode = 1
                self.display = [[0 for x in range(64)] for y in range(128)]
                self.pc += 2
        elif self.ID == 0x1000:
            self.pc = self.NNN
        elif self.ID == 0x2000:
            self.stack[self.sp] = self.pc + 2
            self.sp += 1
            self.pc = self.NNN
        elif self.ID == 0x3000:
            if self.V[self.X] == self.NN:
                self.pc += 4
            else:
                self.pc += 2
        elif self.ID == 0x4000:
            if self.V[self.X] != self.NN:
                self.pc += 4
            else:
                self.pc += 2
        elif self.ID == 0x5000:
            if self.V[self.X] == self.V[self.Y]:
                self.pc += 4
            else:
                self.pc += 2
        elif self.ID == 0x6000:
            self.V[self.X] = self.NN
            self.pc += 2
        elif self.ID == 0x7000:
            self.V[self.X] += self.NN
            if self.V[self.X] >= 256:
                self.V[self.X] -= 256
            self.pc += 2
        elif self.ID == 0x8000:
            if self.N == 0x0000:
                self.V[self.X] = self.V[self.Y]
                self.pc += 2
            elif self.N == 0x0001:
                self.V[self.X] |= self.V[self.Y]
                self.pc += 2
            elif self.N == 0x0002:
                self.V[self.X] &= self.V[self.Y]
                self.pc += 2
            elif self.N == 0x0003:
                self.V[self.X] ^= self.V[self.Y]
                self.pc += 2
            elif self.N == 0x0004:
                self.V[self.X] += self.V[self.Y]
                if self.V[self.X] >= 256:
                    self.V[self.X] -= 256
                    self.V[0xF] = 1
                else:
                    self.V[0xF] = 0
                self.pc += 2
            elif self.N == 0x0005:
                self.V[self.X] -= self.V[self.Y]
                if self.V[self.X] < 0:
                    self.V[self.X] += 256
                    self.V[0xF] = 0
                else:
                    self.V[0xF] = 1
                self.pc += 2
            elif self.N == 0x0006:
                self.V[0xF] = self.V[self.X] & 0x1
                self.V[self.X] >>= 1
                self.pc += 2
            elif self.N == 0x0007:
                self.V[self.X] = self.V[self.Y] - self.V[self.X]
                if self.V[self.X] < 0:
                    self.V[self.X] += 256
                    self.V[0xF] = 0
                else:
                    self.V[0xF] = 1
                self.pc += 2
            elif self.N == 0x000E:
                self.V[0xF] = (self.V[self.X] & 0x80) >> 7
                self.V[self.X] <<= 1
                if self.V[self.X] >= 256:
                    self.V[self.X] -= 256
                self.pc += 2
        elif self.ID == 0x9000:
            if self.V[self.X] != self.V[self.Y]:
                self.pc += 4
            else:
                self.pc += 2
        elif self.ID == 0xA000:
            self.I = self.NNN
            self.pc += 2
        elif self.ID == 0xB000:
            self.pc = self.NNN + self.V[0x0]
        elif self.ID == 0xC000:
            self.V[self.X] = random.randrange(0,255) & self.NN
            self.pc += 2
        elif self.ID == 0xD000:
            pixel = 0
            self.V[0xF] = 0
            if self.N == 0 and self.mode == 1: 
                for yline in range(0,8):
                    pixel = self.memory[self.I + (yline * 2)] << 8 | self.memory[self.I + ((yline * 2) + 1)]
                    for xline in range(0,16):
                        if pixel & 0x8000 != 0:
                            if self.set_pixel(self.V[self.X]+xline,self.V[self.Y]+yline) == 1:
                                    self.V[0xF] = 1
                        pixel <<= 1
            else:
                pixel = 0
                self.V[0xF] = 0
                for yline in range(0,self.N):
                    pixel = self.memory[self.I + yline]
                    for xline in range(0,8):
                        if pixel & 0x80 != 0:
                            if self.rom_name == 'roms/CHIP-8/blitz.rom':
                                self.V[0xF] = self.set_pixel(self.V[self.X]+xline,self.V[self.Y]+yline)
                            else:
                                if self.set_pixel(self.V[self.X]+xline,self.V[self.Y]+yline) == 1:
                                    self.V[0xF] = 1
                        pixel <<= 1
            self.pc += 2
        elif self.ID == 0xE000:
            if self.NN == 0x009E:
                if self.keys[self.V[self.X]] == 1:
                    self.pc += 4
                else:
                    self.pc += 2
            elif self.NN == 0x00A1:
                if self.keys[self.V[self.X]] != 1:
                    self.pc += 4
                else:
                    self.pc += 2
        elif self.ID == 0xF000:
            if self.NN == 0x0007:
                self.V[self.X] = self.delay_timer
                self.pc += 2
            elif self.NN == 0x000A:
                for i in range(0, len(self.keys)):
                    if self.keys[i] == 1:
                        self.V[self.X] = i
                        self.pc += 2
            elif self.NN == 0x0015:
                self.delay_timer = self.V[self.X]
                self.pc += 2
            elif self.NN == 0x0018:
                self.sound_timer = self.V[self.X]
                self.pc += 2
            elif self.NN == 0x001E:
                self.I += self.V[self.X]
                if self.I >= 4096:
                    self.I -= 4096
                self.pc += 2
            elif self.NN == 0x0029:
                self.I = self.V[self.X] * 5
                self.pc += 2
            elif self.NN == 0x0030:
                if self.mode == 1:
                    self.I = (self.V[self.X] * 10) + 0x50
                self.pc += 2
            elif self.NN == 0x0033:
                self.memory[self.I] = self.V[self.X] // 100
                self.memory[self.I + 1] = self.V[self.X] // 10 % 10
                self.memory[self.I + 2] = self.V[self.X] % 100 % 10
                self.pc += 2
            elif self.NN == 0x0055:
                for i in range(0, self.X + 1):
                    self.memory[self.I + i] = self.V[i]
                self.I += self.X
                self.pc += 2
            elif self.NN == 0x0065:
                for i in range(0, self.X + 1):
                    self.V[i] = self.memory[self.I + i]
                self.I += self.X
                self.pc += 2
            elif self.NN == 0x0075:
                print("75")
                for i in range(0, self.X + 1):
                    self.rpl[i] = self.V[i]
                self.pc += 2
            elif self.NN == 0x0085:
                print("85")
                for i in range(0, self.X + 1):
                    self.V[i] = self.rpl[i]
                self.pc += 2
        

    def draw_screen(self):
        if self.mode == 0:
            pygame.surfarray.blit_array(self.surface, self.surfarray)
            pygame.transform.scale(self.surface, (self.screen.get_width(), self.screen.get_height()), self.screen)
        else:
            for x in range(0,128):
                for y in range(0,64):
                    if self.display[x][y] == 1:
                        pygame.gfxdraw.pixel(self.super_surface, x, y, (255, 255, 255, 255))
                    else:
                        pygame.gfxdraw.pixel(self.super_surface, x, y, (0, 0, 0, 255))
            pygame.transform.scale(self.super_surface, (self.screen.get_width(), self.screen.get_height()), self.screen)
        pygame.display.flip()

    def set_pixel(self, x, y):

        if self.mode == 1:
            old = self.display[x][y]
            self.display[x][y] ^= 1
            if (old == 1) and self.display[x][y] == 0:
                return 1
            else:
                return 0
        else:
            if x > 63:
                x -= 64
            if x < 0:
                x += 64
            if y > 31:
                y -= 32
            if y < 0:
                y += 32
            old = self.surfarray[x][y]
            self.surfarray[x][y] ^= 0xFFFFFF
            if (old == 0xFFFFFF) and self.surfarray[x][y] == 0x000000:
                return 1
            else:
                return 0

    def main_loop(self):
        self.done = False
        while self.done == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    self.update_keys()
                if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN:
                    None

            self.interpret_opcode((self.memory[self.pc] << 8) | self.memory[self.pc+1])
            if self.delay_timer > 0:
                self.delay_timer -= 1
            if self.sound_timer > 0:
                winsound.Beep(400,100)
                self.sound_timer = 0

            self.draw_screen()
            if self.rom_name == "roms/CHIP-8/rand.rom":
                self.clock.tick(30)
            else:
                self.clock.tick(120)
        pygame.quit()

c = Chip8()
