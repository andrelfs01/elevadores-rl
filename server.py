from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.UserParam import UserSettableParameter

from model import Modelo as modelo
from agents import ElevatorAgent, PassagerAgent, FloorAgent


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
        return "Passageiros atendidos: " + str(model.atendidos)

class TableData(VisualizationElement):
    '''
    Display a table agents there are.
    '''

    def __init__(self, model, list_agents_name, var_name):
        """ Create a new data renderer. """
        self.model = model
        self.list = list_agents_name
        self.var_name = var_name

    def render(self, model):
        text = ""
        for a in getattr(model, self.list):
            text = text + a.unique_id + ":" + str(getattr(a, self.var_name))
        return text

data_table = TableData(modelo,'floors', 'passageiros')
text_element = Contador()
canvas_element = CanvasGrid(elev_portrayal, 5, 31, 250, 900)
chart_element = ChartModule([{"Label": "Wolves", "Color": "#AA0000"},
                             {"Label": "Sheep", "Color": "#666666"}])

model_params = {                
                "elevators": 4,
                "floors": 16,
                "a": UserSettableParameter('slider', 'a', 0.01, 0.01, 2)}


server = ModularServer(modelo, [canvas_element, text_element, data_table], "ElevatorRL", model_params)
server.port = 8521
server.launch()