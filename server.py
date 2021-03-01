from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from model import Modelo as modelo
from agents import ElevatorAgent, PassagerAgent

def elev_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is PassagerAgent:
        portrayal["Shape"] = "resources/passager.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is ElevatorAgent:
        portrayal["Shape"] = "resources/elevator.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text"] = '1'
        portrayal["text_color"] = "White"


    return portrayal

class ElevatorRL(TextElement):
    '''
    Display a text count of how many under observation agents there are.
    '''

    def __init__(self):
        pass

    def render(self, model):
        return "Observed agents: " + str(model.atendidos)


text_element = ElevatorRL()
canvas_element = CanvasGrid(elev_portrayal, 5, 16, 350, 600)
chart_element = ChartModule([{"Label": "Wolves", "Color": "#AA0000"},
                             {"Label": "Sheep", "Color": "#666666"}])

model_params = {                
                "elevators": 4,
                "floors": 16,
                "a": UserSettableParameter('slider', 'a', 0.01, 0.01, 2)}

server = ModularServer(modelo, [canvas_element, text_element], "ElevatorRL", model_params)
server.port = 8521
server.launch()