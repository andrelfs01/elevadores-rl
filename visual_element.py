from mesa.visualization.ModularVisualization import VisualizationElement

class TableElement(VisualizationElement):
    dados = "<table id=data><tr><th>Table</th></tr></table>"
    js_code = "var TableModule = function() {\
        var tag = \"<table id=data><tr><th>Table</th></tr></table>\";\
        var text = $(tag)[0];\
        $(\"body\").append(text);\
        this.render = function(data) {\
            $(text).html(data);\
        };\
        this.reset = function() {\
            $(text).html(\"\");\
        };\
        };\
        elements.push(new TableModule());"

    def render(self, dados):
        """ Render all the text elements, in order. """
        #for element in dados:
        print(dados)
        self.dados = dados
        return str(self.dados)