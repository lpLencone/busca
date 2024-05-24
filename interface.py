# Lucas Lençone Plaza
# Jefferson Eduardo Batista

import pygame
import sys
import busca
import acoes


class Grid:
    COLS = 14
    ROWS = 10
    CELL_SIZE = 40
    WIDTH = COLS * CELL_SIZE
    HEIGHT = ROWS * CELL_SIZE

    COLOR_BLOCK = (180, 100, 0)  # Dark orange
    COLOR_GRID = (180, 180, 180)  # Light grey
    COLOR_GOAL = (100, 255, 100)  # Light green
    COLOR_HOLE = (150, 0, 0)  # Dark red
    COLOR_ORANGE = (250, 130, 90)  # Light orange

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen, block, laranja_ativo):
        for j in range(self.COLS):
            for i in range(self.ROWS):
                color = self.COLOR_GRID
                if (i, j) in block:
                    color = self.COLOR_BLOCK
                elif (i, j) == (4, 7):
                    color = self.COLOR_GOAL
                elif j in acoes.buraco[i]:
                    color = self.COLOR_HOLE
                elif laranja_ativo and j in acoes.laranja[i]:
                    color = self.COLOR_ORANGE
                pygame.draw.rect(
                        screen, color,
                        (self.x + j * self.CELL_SIZE + 1, self.y + i * self.CELL_SIZE + 1,
                         self.CELL_SIZE - 1, self.CELL_SIZE - 1))


class TextBox:
    def __init__(self, x, y, w, h, text, text_size):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.text_size = text_size

    def draw(self, screen):
        text_surface = pygame.font.Font(None, self.text_size).render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        pygame.draw.rect(screen, (180, 180, 180), self.rect)
        screen.blit(text_surface, text_rect)


class Button:
    def __init__(self, x, y, w, h, text, text_size, action):
        self.rect = pygame.Rect(x, y, w, h)
        self.box = TextBox(x, y, w, h, text, text_size)
        self.action = action

    def draw(self, screen):
        self.box.draw(screen)


def position(w=0, h=0, /, set_x=None, set_y=None, add_x=None, add_y=None, use_last_x=False,
             use_last_y=False, getmax=False, *, _pos=[0, 0], _max=[0, 0], _last=[0, 0]):
    if set_x is not None:
        _pos[0] = set_x
    if set_y is not None:
        _pos[1] = set_y

    if use_last_x:
        _pos[0] = _last[0]
    if use_last_y:
        _pos[1] = _last[1]

    if add_x:
        _pos[0] += add_x
    if add_y:
        _pos[1] += add_y

    _pos[0] += w
    _pos[1] += h

    if _pos[0] > _max[0]:
        _max[0] = _pos[0]
    if _pos[1] > _max[1]:
        _max[1] = _pos[1]

    if getmax:
        return _max[:]

    _last[0] = _pos[0] - w
    _last[1] = _pos[1] - h

    return _last[0], _last[1], w, h


def main():
    global states, state_index, paused, widgets, problem
    pygame.init()

    screen_width, screen_height = position(getmax=True)
    screen = pygame.display.set_mode((screen_width, screen_height))
    paused = True

    clock = pygame.time.Clock()
    deltatime = 0

    while True:
        deltatime += clock.tick(60) / 1000
        if not paused and state_index + 1 < len(states) and deltatime > 0.1:
            state_index += 1
            deltatime = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for widget in widgets:
                    if isinstance(widget, Button) and widget.rect.collidepoint(event.pos):
                        widget.action(widget)

        screen.fill((0, 0, 0))
        grid.draw(screen, states[state_index], problem.usar_laranja)
        for widget in widgets:
            if isinstance(widget, TextBox):
                widget.text = f'Custo: {state_index}'
            widget.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    global states, state_index, paused, widgets, problem

    problem = busca.Bloxorz()
    heuristica = lambda t: busca.pitagoras(t.state, problem.goal[0])
    states = [problem.initial] + busca.best_first_graph_search(problem, heuristica).solution()
    state_index = 0
    paused = True

    def pause_action(button, value=None):
        global paused
        paused = not paused
        if value is not None:
            paused = value
        if paused:
            button.box.text = 'Play'
        else:
            button.box.text = 'Pause'

    def next_action(button, button_pause):
        global state_index
        if state_index + 1 < len(states):
            state_index += 1
        pause_action(button_pause, True)

    def previous_action(button, button_pause):
        global state_index
        if state_index > 0:
            state_index -= 1
        pause_action(button_pause, True)

    def algorithm_action(button, button_pause, value=None):
        global states, state_index

        button.box.text = 'A*' if button.box.text == 'Guloso' else 'Guloso'
        if value is not None:
            button.box.text = value

        if button.box.text == 'Guloso':
            states = [problem.initial] + \
                busca.best_first_graph_search(problem, heuristica).solution()
        else:
            states = [problem.initial] + \
                busca.astar_search(problem, heuristica).solution()

        state_index = 0
        pause_action(button_pause, True)

    def laranja_action(button, button_algorithm, button_pause):
        global problem
        if button.box.text == 'Laranja: ativo':
            button.box.text = 'Laranja: inativo'
            problem = busca.Bloxorz(False)
        else:
            button.box.text = 'Laranja: ativo'
            problem = busca.Bloxorz(True)
        algorithm_action(button_algorithm, button_pause, button_algorithm.box.text)

    def restaurar_action(button, button_algorithm, button_pause):
        algorithm_action(button_algorithm, button_pause, button_algorithm.box.text)

    grid_x, grid_y, _, _ = position(Grid.WIDTH, Grid.HEIGHT)
    grid = Grid(grid_x, grid_y)

    button_width = 200
    button_height = 45

    textbox_custo = TextBox(*position(button_width, button_height, set_y=0), 'Custo: 0', 32)
    button_pause = Button(*position(button_width, button_height, add_y=10, use_last_x=True),
                          'Play', 32, pause_action)
    button_next = Button(*position(button_width, button_height, add_y=10, use_last_x=True),
                         'Avançar', 32, lambda b: next_action(b, button_pause))
    button_previous = Button(*position(button_width, button_height, add_y=10, use_last_x=True),
                             'Voltar', 32, lambda b: previous_action(b, button_pause))
    button_algorithm = Button(*position(button_width, button_height, add_y=10, use_last_x=True),
                              'Guloso', 32, lambda b: algorithm_action(b, button_pause))
    button_laranja = Button(*position(button_width, button_height, add_y=10, use_last_x=True),
                            'Laranja: inativo', 32,
                            lambda b: laranja_action(b, button_algorithm, button_pause))
    button_restaurar = Button(*position(button_width, button_height, add_y=10, use_last_x=True),
                              'Restaurar', 32,
                              lambda b: restaurar_action(b, button_algorithm, button_pause))

    widgets = (button_algorithm, button_pause, button_next, button_previous,
               button_laranja, button_restaurar, textbox_custo)

    main()
