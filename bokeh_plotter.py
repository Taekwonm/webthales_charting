class BokehPlotter:
    def __init__(self, state_names, title=None):
        self.state_names = state_names
        state_count = len(state_names)
        self.columns = 5
        self.rows = int(numpy.ceil(state_count / float(self.columns)))

        # fill grid by filling each "row" with <self.columns> number of plots
        self.grid_plot = [[] for n in range(self.rows)]

        if title:
            # no built-in bokeh functionality for a gridplot title
            self.title = title

    def PlotBatch(self, trajectories):
        plots = []
        colors = Viridis256 + Plasma256

        for analyte in self.state_names:
            times = []
            analyte_data = []
            for traj in trajectories:
                p_time, p_data = traj.times, traj.GetAnalyteRow(analyte)
                times.append(p_time)
                analyte_data.append(p_data)

            p1 = figure(width=250, plot_height=250,
                        title=analyte, tools='pan,wheel_zoom,hover,reset')

            p1.multi_line(times, analyte_data,
                          line_color=colors[:len(times)])

            plots.append(p1)

        cols = self.columns
        self.grid_plot = [
            [plots[r * cols + c] for c in range(cols)
             if (r * cols + c < len(plots))]
            for r in range(self.rows)]

    def SaveFullPlot(self, outfile):
        p = gridplot(self.grid_plot)
        output_file(outfile)
        save(p)

    def SaveIndividualPlots(self, outdir):
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        for row in self.grid_plot:
            for plot in row:
                output_file(outdir + plot.title.text)
                save(plot)
        '''
        if len(self.grid_plot) <= 5:
            p = gridplot(self.grid_plot)
            output_file(outfile)
            save(p)     
        else:
            grid_plots = [self.grid_plot[n:m]
                          for n in range(0, len(self.grid_plot) - 4, 5)
                          for m in range(5, len(self.grid_plot) + 1, 5)
                          if (m - n == 5)]
            for i in range(len(grid_plots)):
                p = gridplot(grid_plots[i])
                output_file(outfile + '_plot' + str(i) + '.html')
                save(p)        
        '''
