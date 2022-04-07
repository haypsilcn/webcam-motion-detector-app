from motion_detector import data_frame
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

column_source = ColumnDataSource(data_frame)

graph = figure(x_axis_type="datetime", height=100, width=500, sizing_mode="scale_both", title="Motion Graph")
graph.yaxis.minor_tick_line_color = None
graph.yaxis.ticker.desired_num_ticks = 1

hover = HoverTool(
    tooltips=[("Start", "@Start{%Y-%m-%d %H:%M:%S}"), ("End", "@End{%Y-%m-%d %H:%M:%S}")],
    formatters={"@Start": "datetime", "@End": "datetime"})
graph.add_tools(hover)

q = graph.quad(left="Start", right="End",
               bottom=0, top=1, color="blue",
               source=column_source)

output_file("graph.html")
show(graph)
