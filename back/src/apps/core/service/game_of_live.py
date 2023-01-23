import hashlib
import random

from django.db.models import Max, F, Count, Q

from src.apps.core.exceptions import NonAliveCellsException, NoChangeStateException, ExistingStateException
from src.apps.core.models import Cell


class GameOfLife:
    MIN_PERCENT_START_ALIVE = 30
    MAX_PERCENT_START_ALIVE = 50

    def __init__(self, world):
        self.world = world

    def get_current_state(self):
        vals = list(self.world.world_cells.order_by('cell__x', 'cell__y').values_list('alive', flat=True))
        value_for_state = "".join([str(int(v)) for v in vals])
        return hashlib.sha256(str(value_for_state).encode()).hexdigest()

    def init_world(self):
        cells = []
        for x in range(self.world.width):
            for y in range(self.world.height):
                cells.append(Cell(x=x, y=y))

        existing_cells = Cell.objects.filter(x__in=[cell.x for cell in cells], y__in=[cell.y for cell in cells])
        existing_coords = {(cell.x, cell.y) for cell in existing_cells}
        cells = [cell for cell in cells if (cell.x, cell.y) not in existing_coords]

        Cell.objects.bulk_create(cells)
        self.world.cells.set(existing_cells)
        self.world.cells.add(*cells)

        cell_count = self.world.cells.count()

        num_alive = random.randint(cell_count * self.MIN_PERCENT_START_ALIVE // 100,
                                   cell_count * self.MAX_PERCENT_START_ALIVE // 100)
        cell_ids = self.world.cells.values_list('id', flat=True)

        random_world_cells = random.sample(list(cell_ids), num_alive)
        self.world.world_cells.filter(cell__in=random_world_cells).update(alive=True)

        self.world.states.create(
            generation_num=0,
            state_hash=self.get_current_state(),
        )

    def next_generation(self):
        with_alive_count = self.world.world_cells.annotate(alive_count=Count('world__cells__id', filter=Q(
            world__cells__x__in=[F('cell__x') - 1, F('cell__x'), F('cell__x') + 1]) & Q(
            world__cells__y__in=[F('cell__y') - 1, F('cell__y'), F('cell__y') + 1]) & Q(
            world__world_cells__alive=True) & ~Q(world__cells__id=F('cell_id')), distinct=True), )

        to_die = list(with_alive_count.filter(Q(alive=False) | ~Q(alive_count__in=[2, 3])).values_list('id', flat=True))
        to_alive = list(with_alive_count.filter(Q(alive=False) & Q(alive_count=3)).values_list('id', flat=True))

        self.world.world_cells.filter(id__in=to_alive).update(alive=True)
        self.world.world_cells.filter(id__in=to_die).update(alive=False)

        current_state = self.get_current_state()

        if self.world.world_cells.filter(alive=True).count() == 0:
            raise NonAliveCellsException()

        if not to_die and not to_alive:
            raise NoChangeStateException()

        if self.world.states.filter(state_hash=current_state):
            raise ExistingStateException()

        max_gen_num = self.world.states.aggregate(Max('generation_num')).get('generation_num__max')
        self.world.states.create(
            generation_num=max_gen_num + 1,
            state_hash=current_state
        )
        return self.world
