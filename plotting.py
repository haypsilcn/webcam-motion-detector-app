 from bokeh.plotting import figure, show, output_file
 from bokeh.models import HoverTool, ColumnDataSource
 from motion_detector import data_frame

 data_frame["start_string"] = data_frame["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
 data_frame["end_string"] = data_frame["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

 column_source = ColumnDataSource(data_frame)

 graph = figure(x_axis_type = "datetime", height = 100, width = 500, responsive = True, title = "Motion Graph")
 graph.yaxis.minor_tick_line_color = None
 graph.ygrid[0].ticker.desired_num_ticks = 1

 hover = HoverTool(tooltips = [("Start", "@start_string"), ("End", "@end_string")])
 graph.add_tools(hover)

 q = graph.quad(left = data_frame["Start"], right = data_frame["End"],
                bottom = 0, top = 1, color = "blue",
                source = column_source)

 output_file("Graph.html")
 show(graph)