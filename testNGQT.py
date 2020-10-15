#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

from NodeGraphQt import (NodeGraph,
                         BaseNode,
                         BackdropNode,
                         setup_context_menu)
from NodeGraphQt import (PropertiesBinWidget,
                         NodeTreeWidget)

from PySide2 import QtCore,QtGui,QtWidgets

# import example nodes from the "example_nodes" package
#from NGQT.example_nodes import basic_nodes, widget_nodes

class JointNode(BaseNode):
    # set a unique node identifier.
    __identifier__ = 'Joint'

    # set the initial default node name.
    NODE_NAME = 'JointNode'

    def __init__(self):
        super(JointNode, self).__init__()
        self.set_color(25, 58, 51)
        self.get_widget('graph')

        # create input and output port.
        self.add_input('parent', color=(200, 10, 0))
        self.add_output('children')
        self.add_text_input(name='jointName',label='BoneName', text='joint')


def GenerateNodeFromCSV(csv, graph):
    kvlist = []
    nodes = []
    with open(csv, 'r', encoding='utf-8') as result:
        kv = result.readlines()
        for item in kv:
            k = item.split(',', 1)[0].replace(' ', '').replace('\n', '').replace('\t', '')
            v = item.split(',', 1)[1].replace(' ', '').replace('\n', '').replace('\t', '')
            if k!='' and v!='':
                kvlist.append((k, v))

    uuin = [i[0] for i in kvlist] + [i[1] for i in kvlist]
    uuin = list(set(uuin))
    uuin.sort()
    for i in uuin:
        node_t = graph.create_node('Joint.JointNode', name=i, selected=False, pos=[0, 0])
        node_t.set_property('jointName', i)

    for kv in kvlist:
        knode = graph.get_node_by_name(kv[0])
        vnode = graph.get_node_by_name(kv[1])
        if knode!=None and vnode!=None:
            vnode.set_output(0, knode.input(0))


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication([])

    # create node graph.
    graph = NodeGraph()


    # set up default menu and commands.
    setup_context_menu(graph)

    # widget used for the node graph.
    graph_widget = graph.widget
    graph_widget.resize(1100, 800)
    graph_widget.show()

    # show the properties bin when a node is "double clicked" in the graph.
    properties_bin = PropertiesBinWidget(node_graph=graph)
    properties_bin.setWindowFlags(QtCore.Qt.Tool)
    def show_prop_bin(node):
        if not properties_bin.isVisible():
            properties_bin.show()
    graph.node_double_clicked.connect(show_prop_bin)

    # show the nodes list when a node is "double clicked" in the graph.
    node_tree = NodeTreeWidget(node_graph=graph)
    def show_nodes_list(node):
        if not node_tree.isVisible():
            node_tree.update()
            node_tree.show()
    graph.node_double_clicked.connect(show_nodes_list)

    # create_jointnode function.
    def create_jointnode(graph):
        sp = graph.graph_rect()
        #p = [QtGui.QCursor.pos().x(), QtGui.QCursor.pos().y()]
        p = [sp[0] + sp[2]/2, sp[1]+sp[3]/2]
        new_node = graph.create_node('Joint.JointNode',
                                    name='joint',
                                    selected = False,
                                    pos=p)


    # get the main context menu.
    context_menu = graph.get_context_menu('graph')

    # add a menu called "Foo".
    #create_jointnode_menu = context_menu.add_menu('create joint')

    # add "Bar" command to the "Foo" menu.
    # we also assign a short cut key "Shift+t" for this example.
    context_menu.add_command('create joint', create_jointnode, "Ctrl+q")
    #qs = QtGui.QKeySequence(QtGui.Qt.CTRL + QtGui.Qt.LeftButton)
    #create_joint_node = context_menu.get_command('create joint')
    #create_joint_node.set_shortcut(qs)


    def generate_csv(graph):
        generatelist = []
        othernodes = graph.all_nodes()
        for i in othernodes:
            k = i.get_property('jointName')
            nodes = i.connected_input_nodes()
            values = list(nodes.values())
            if values[0].__len__() > 0:
                v = values[0][0].get_property('jointName')
                generatelist.append([k, v])

        file_path = QtWidgets.QFileDialog.getSaveFileName(filter='csv(*.csv);;All file(*.*)')
        file_path = file_path[0]
        #file_path = graph.save_dialog(ext='csv')
        fp = open(file_path, "w+")
        for i in generatelist:
            fp.write(i[0] + ',' + i[1] + '\n')
        fp.close()

    generate_menu = context_menu.add_menu('generate')
    generate_menu.add_command('Generate CSV', generate_csv)


    def generate_node_from_csv(graph):
        file_path = QtWidgets.QFileDialog.getOpenFileName(filter='csv(*.csv);;All file(*.*)')
        file_path = file_path[0]
        GenerateNodeFromCSV(file_path, graph)

    generate_menu.add_command('Generate Node From Csv', generate_node_from_csv)


    # registered nodes.
    reg_nodes = [
        #BackdropNode,
        JointNode,
        #basic_nodes.FooNode,
        #basic_nodes.BarNode,
        #widget_nodes.DropdownMenuNode,
        #widget_nodes.TextInputNode,
        #widget_nodes.CheckboxNode
    ]
    for n in reg_nodes:
        graph.register_node(n)

    sys.exit(app.exec_())
