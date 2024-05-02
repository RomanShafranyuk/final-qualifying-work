import graphviz
import database

def get_graph(data):
    dot = graphviz.Graph(format="png")
    
    print(data)
    for i in range(len(data)):
        dot.node(str(data[i][0]))
        if data[i][1] != 0:
            dot.edge(str(data[i][0]), str(data[i][1]))
    dot.render(directory='.', view=True) 

# dot = graphviz.Graph(format="png")
# dot.node('A', 'King Arthur')  
# dot.node('B', 'Sir Bedevere the Wise')
# dot.node('L', 'Sir Lancelot the Brave')

# dot.edges(['AB', 'AL'])
# dot.edge('B', 'L', constraint='false')


# dot.render(directory='.', view=True) 
# get_graph(10)