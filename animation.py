class CastAnim:
    DURATION = 0.55

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.t = 0.0
        self.done = False

    def update(self, dt):
        self.t += dt / self.DURATION
        if self.t >= 1.0:
            self.t = 1.0
            self.done = True

    def pos(self):
        s = self.t
        x = self.start[0] + (self.end[0] - self.start[0]) * s
        arc_h = -120 * s * (1 - s) * 4
        y = self.start[1] + (self.end[1] - self.start[1]) * s + arc_h
        return (x, y)
