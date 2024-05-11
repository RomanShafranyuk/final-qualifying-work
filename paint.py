import graphviz

def get_graph(data: list):
    """
    Отрисовывает блокчейн цепь по данным из data.


            Параметры:
                    data (list) : номера узлов и указатели на узел-родителя
            

    """
    dot = graphviz.Graph(format="png")
    for i in range(len(data)):
        dot.node(str(data[i][0]))
        if data[i][1] != 0:
            dot.edge(str(data[i][0]), str(data[i][1]))
    dot.render(directory='.', view=True) 

