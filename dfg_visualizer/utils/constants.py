GRAPH_VIZ_RANKDIR = "rankdir = {}\n"
GRAPH_VIZ_START_NODE = 'start[shape="circle" fontsize="20" margin="0.05" label="&#9650;" style="filled" fillcolor="green"]\n'
GRAPH_VIZ_END_NODE = 'complete[shape="circle" fontsize="30" margin="0" label="&#9632;" style="filled" fillcolor="red"]\n'
GRAPH_VIZ_NODE = '{}[shape="none" fontsize="18" label=<\n{}>]\n'
GRAPH_VIZ_NODE_DATA = '<table cellpadding="3" cellborder="1" cellspacing="0" border="0" style="rounded">\n{}</table>\n'
GRAPH_VIZ_NODE_DATA_ROW = (
    '\t<tr><td bgcolor="{}"><font face="arial" color="white">{}</font></td></tr>\n'
)
GRAPH_VIZ_LINK = '{}->{}[penwidth="{}" fontsize="16" label=<\n{}>]\n'
GRAPH_VIZ_LINK_DATA = '<table cellpadding="0" cellborder="0" cellspacing="0" border="0" style="rounded">\n{}</table>\n'
GRAPH_VIZ_LINK_DATA_ROW = (
    '\t<tr><td bgcolor="snow"><font face="arial" color="{}">{}</font></td></tr>\n'
)

GRAPH_VIZ_START_END_LINK = '{}->{}[penwidth="{}" color="gray75" fontsize="16" style="dashed" arrowhead="none" label=<\n<table cellpadding="0" cellborder="0" cellspacing="0" border="0">\n\t<tr><td bgcolor="white"><font face="arial" color="{}">{}</font></td></tr>\n</table>>]\n'
