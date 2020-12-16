from typing import Optional


class Intersection:
    def __init__(self, t: float, _object: object):
        self.t = t
        self.object = _object

    def __repr__(self):
        return f'Intersection(t={self.t}, object={self.object})'


class Intersections:
    def __init__(self, *intersections):
        self.intersections = sorted(intersections, key=lambda intersection: intersection.t)

    @property
    def count(self):
        return len(self.intersections)

    def __getitem__(self, item):
        return self.intersections[item]

    def hit(self) -> Optional[Intersection]:
        for intersect in self.intersections:
            # return the first non-negative t intersection from the ordered list
            if intersect.t >= 0:
                return intersect
