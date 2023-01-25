from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.UserParam import UserSettableParameter

from model_full_state import Modelo as modelo
from agents_full_state import ElevatorAgent, PassagerAgent, FloorAgent

# Green
RICH_COLOR = "#46FF33"
# Red
POOR_COLOR = "#FF3C33"
# Blue
MID_COLOR = "#3349FF"

def elev_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is PassagerAgent:
        portrayal["Shape"] = "resources/passager.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    if type(agent) is FloorAgent:
        portrayal["Shape"] = "resources/floor.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 3
        portrayal["text"] = str(agent.number) 

    elif type(agent) is ElevatorAgent:
        portrayal["Shape"] = "resources/elevator.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text"] = agent.state
        portrayal["text_color"] = "White"


    return portrayal

class Contador(TextElement):
    '''
    Display a text count of how many under observation agents there are.
    '''

    def __init__(self):
        pass

    def render(self, model):
        return "Passageiros atendidos: " + str(len(model.attended))

class VisualizadorElevador(TextElement):
    def __init__(self, numero):
        self.numero = numero

    def render(self, model):
        elevador = model.elevators[self.numero]
        return f"Elevador {self.numero}:  {str(len(elevador.passageiros))}"

text_element = Contador()
elevator1_element = VisualizadorElevador(0)
elevator2_element = VisualizadorElevador(1)
elevator3_element = VisualizadorElevador(2)
elevator4_element = VisualizadorElevador(3)
canvas_element = CanvasGrid(elev_portrayal, 5, 16, 200, 800)
#canvas_element = CanvasGrid(elev_portrayal, 5, 8, 400, 800)

# model_params = {                
#                 "elevators": 4,
#                 "floors": 16,
#                 "a": UserSettableParameter('slider', 'a', 0.01, 0.01, 2)}

model_params = {                
                "elevators": 4,
                "floors": 16,
                "passager_flow" :  UserSettableParameter('choice', 'Passager flow', value='up', choices=['up', 'dp', 'du']),
                #"controller" : 'baseline',
                "controller" : UserSettableParameter('choice', 'Controller', value='baseline', choices=['baseline', 'dist', 'ga', 'pessimistic','discriminant function']),
                "alpha" : UserSettableParameter('number', 'alpha (for GA only [1-9999])', value=0,description='(for GA only [1-9999])'),
                "beta" : UserSettableParameter('number', 'beta (for GA only [1-9999])', value=0,description='(for GA only [1-9999])'),
                "theta" : UserSettableParameter('number', 'theta  (for GA only [1-9999])', value=0,description='(for GA only [1-9999])'),
                "output_file" : True,
                "a": 0}

# map data to chart in the ChartModule
passagers_chart = ChartModule(
    [
        {"Label": "Attended", "Color": RICH_COLOR},
        {"Label": "Floors", "Color": POOR_COLOR},
        {"Label": "Cars", "Color": MID_COLOR},
    ]
)

# map data to chart in the ChartModule
times_chart = ChartModule(
    [
        {"Label": "WaitingTime", "Color": RICH_COLOR},
        {"Label": "JourneyTime", "Color": POOR_COLOR},
        {"Label": "TotalTime", "Color": MID_COLOR},
    ]
)

# map data to chart in the ChartModule
time_floor_chart = ChartModule(
    [
        {"Label": "WaitingFloor", "Color": RICH_COLOR}
    ]
)

# map data to chart in the ChartModule
mean_crowding_chart = ChartModule(
    [
        {"Label": "Crowding", "Color": RICH_COLOR}
    ]
)


server = ModularServer(modelo, [canvas_element, elevator1_element,elevator2_element,elevator3_element,elevator4_element, passagers_chart, times_chart, time_floor_chart, mean_crowding_chart, text_element], "ElevatorRL", model_params)
server.port = 8521
server.launch()
