class ALU:
    def __init__(self):
        self.left_input = None
        self.right_input = None
        self.result = None

    def add(self):
        return self.left_input + self.right_input

    def sub(self):
        return self.left_input - self.right_input

    def mul(self):
        return self.left_input * self.right_input

    def div(self):
        return self.left_input // self.right_input

    def mod(self):
        return self.left_input % self.right_input

    def inc(self):
        return self.left_input + 1

    def dec(self):
        return self.left_input - 1

class Datapath:
    def __init__(self):
        self.alu = ALU()
        self.gen_regs = [0 for _ in range(8)]

    def latch_general_regs(self, signal):
        pass
        # ТУТ БУДЕТ ОГРОМНЫЙ МАТЧ КЕЙС С ОБРАБОТКОЙ !!!ВСЕХ!!! СИГНАЛОВ
