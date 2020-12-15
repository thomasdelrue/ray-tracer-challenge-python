from tuples import Point, Vector


class Projectile:
    def __init__(self, position: Point, velocity: Vector):
        self.position = position
        self.velocity = velocity


class Environment:
    def __init__(self, gravity: Vector, wind: Vector):
        self.gravity = gravity
        self.wind = wind


def tick(env: Environment, proj: Projectile):
    position = proj.position + proj.velocity
    velocity = proj.velocity + env.gravity + env.wind
    return Projectile(position, velocity)


if __name__ == '__main__':
    proj = Projectile(Point(0, 1, 0), Vector(1, 100, 0).normalize())
    env = Environment(Vector(0, -0.1, 0), Vector(-0.01, 0, 0))

    i = 0
    while proj.position.y > 0:
        i += 1
        proj = tick(env, proj)
        print(f'tick {i}: projectile at {proj.position}')
