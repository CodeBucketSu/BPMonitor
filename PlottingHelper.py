'''This modele inherits from guiqwt.plot.PlotManager 
to imlement the plotting work.
'''

from guiqwt.plot import PlotManager, CurvePlot
from guiqwt.builder import make


colors = ['red', 'blue', 'green']

class PlottingHelper(object):
	'''This is the class implementing the plotting work.'''
	def __init__(self, parent, signal_names, sample_rate):
		'''Do the initialization work.
		A PlottingHelper object helps plotting a group of signals all of which 
		has the same number of points to plot at one time.
		signal_names: 
			a dictionary {'list_name':['list of signal names']}
		sample_rate:
			the sample_rate of the signals
		'''

		self.sample_rate = sample_rate
		self.signal_names = signal_names
		self.curve_items = {}
		self.curve_plots = {}
		self.plot_manager = PlotManager(parent)

		for list_name, sig_name_list in self.signal_names.items():
			# One CurvePlot object for every sig_name_list
			curve_plot = CurvePlot()
			curve_plot.axisScaleDraw(CurvePlot.Y_LEFT).setMinimumExtent(10)
			self.curve_plots[list_name] = curve_plot
			curve_plot.plot_id = id(curve_plot)
			for i, sig_name in enumerate(sig_name_list):
				# One CurveItem object for every signal_name 
				print sig_name, colors[i]
				self.curve_items[sig_name] = make.curve([0], [0], \
					color=colors[i], title=sig_name)
				curve_plot.add_item(self.curve_items[sig_name])

			# add the curve_plot object to plot_manager
			self.plot_manager.add_plot(curve_plot) 

		# register and activate the tools 
		self.plot_manager.register_standard_tools()
		self.plot_manager.get_default_tool().activate()
		self.plot_manager.synchronize_axis(CurvePlot.X_BOTTOM, \
									self.plot_manager.plots.keys())

	def update_curves(self, time, signals, interval_in_second):	
		'''update the curves everytime the signals change
		time:
			the time sequence, which is also the x_axis data
		signal:
			a dictionary of signals to plot, the keys of which is recorded
			in self.signal_names.
			and in fact these are the y_axis data
		'''
		xmax = time[-1]
		xmin = max(xmax - interval_in_second, 0)
		xdata = time
		for list_name, sig_name_list in self.signal_names.items():
			# 
			for i, sig_name in enumerate(sig_name_list):
				# 
				ydata = signals[sig_name]
				idxmn = int(xmin*self.sample_rate)
				idxmx = int(xmax*self.sample_rate)
				self.curve_items[sig_name].set_data(xdata[idxmn:idxmx], \
													ydata[idxmn:idxmx])

			self.curve_plots[list_name].do_autoscale()












