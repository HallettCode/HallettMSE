import random
import pygame, pygame.gfxdraw
import winsound

class Chip8:
    def __init__(self):
        self.memory = [0]*4096
        self.fontset = [0xF0, 0x90, 0x90, 0x90, 0xF0, 0x20, 0x60, 0x20, 0x20, 0x70, 0xF0, 0x10, 0xF0, 0x80, 0xF0, 0xF0, 0x10, 0xF0, 0x10, 0xF0, 0x90, 0x90, 0xF0, 0x10, 0x10, 0xF0, 0x80, 0xF0, 0x10, 0xF0, 0xF0, 0x80, 0xF0, 0x90, 0xF0, 0xF0, 0x10, 0x20, 0x40, 0x40, 0xF0, 0x90, 0xF0, 0x90, 0xF0, 0xF0, 0x90, 0xF0, 0x10, 0xF0, 0xF0, 0x90, 0xF0, 0x90, 0x90, 0xE0, 0x90, 0xE0, 0x90, 0xE0, 0xF0, 0x80, 0x80, 0x80, 0xF0, 0xE0, 0x90, 0x90, 0x90, 0xE0, 0xF0, 0x80, 0xF0, 0x80, 0xF0, 0xF0, 0x80, 0xF0, 0x80, 0x80]
        self.rom = []
        self.V = [0]*16
        self.stack = [0]*16
        self.delay_timer = 0
        self.sound_timer = 0
        self.display = [[0 for x in range(0,32)] for y in range(0,64)]
        self.keys = [0]*16
        self.bindings = [pygame.K_x, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_z, pygame.K_c, pygame.K_4, pygame.K_r, pygame.K_f, pygame.K_v]
        
        self.pc = 0x200
        self.sp = 0
        self.I = 0
        self.redraw = True
        self.interrupt = False

        pygame.display.init()
        self.surface = pygame.Surface((64, 32))
        self.screen = pygame.display.set_mode((640, 360), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Chip8 Emulator")

        for i in range(0, len(self.fontset)):
            self.memory[i] = self.fontset[i]

        self.transfer_rom_to_mem("pong.rom")
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
        print(format(opcode, '#04X'))
        self.NNN = opcode & 0x0FFF
        self.NN = opcode & 0x00FF
        self.X = (opcode & 0x0F00) >> 8
        self.Y = (opcode & 0x00F0) >> 4
        self.N = opcode & 0x000F
        self.ID = opcode & 0xF000

        if self.ID == 0x0000:
            if self.NN == 0x00E0:
                self.display = [[0 for x in range(32)] for y in range(64)]
                self.pc += 2
            elif self.NN == 0x00EE:
                self.sp -= 1
                self.pc = self.stack[self.sp]
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
                self.V[0xF] = self.V[self.Y] & 0x1
                self.V[self.Y] >>= 1
                self.V[self.X] = self.V[self.Y]
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
                self.V[0xF] = (self.V[self.Y] & 0x80) >> 7
                self.V[self.Y] <<= 1
                if self.V[self.Y] >= 256:
                    self.V[self.Y] -= 256
                self.V[self.X] = self.V[self.Y]
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
            ##print("Drawing at ({},{}) sprite starting at {}".format(self.V[self.X], self.V[self.Y], format(self.I,'04X')))
            pixel = 0
            self.V[0xF] = 0
            for yline in range(0,self.N):
                pixel = self.memory[self.I + yline]
                for xline in range(0,8):
                    if pixel & 0x80 != 0:
                        self.V[0xF] = self.set_pixel(self.V[self.X]+xline,self.V[self.Y]+yline) == 1
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
            elif self.NN == 0x0033:
                self.memory[self.I] = self.V[self.X] // 100
                self.memory[self.I + 1] = self.V[self.X] // 10 % 10
                self.memory[self.I + 2] = self.V[self.X] % 100 % 10
                self.pc += 2
            elif self.NN == 0x0055:
                for i in range(0, self.X + 1):
                    self.memory[self.I + i] = self.V[i]
                self.I += 3
                self.pc += 2
            elif self.NN == 0x0065:
                for i in range(0, self.X + 1):
                    self.V[i] = self.memory[self.I + i]
                self.I += 3
                self.pc += 2

    def draw_screen(self):
        for x in range(0,64):
            for y in range(0,32):
                if self.display[x][y] == 1:
                    pygame.gfxdraw.pixel(self.surface, x, y, (255, 255, 255, 255))
                else:
                    pygame.gfxdraw.pixel(self.surface, x, y, (0, 0, 0, 255))
        pygame.transform.scale(self.surface, (self.screen.get_width(), self.screen.get_height()), self.screen)
        pygame.display.flip()

    def set_pixel(self, x, y):
        if x > 63:
            x -= 64
        if x < 0:
            x += 64
        if y > 31:
            y -= 32
        if y < 0:
            y += 32
        old = self.display[x][y]
        self.display[x][y] ^= 1
        return (old == 1) and self.display[x][y] == 0

    def main_loop(self):
        done = False
        while done == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
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
            #self.clock.tick(120)
            
        pygame.quit()

c = Chip8()
