  # def on_motion(self, event):
    #     if self.press is None:
    #         return
    #     if event.inaxes == self.ax:
    #         prev_data, xpress, ypress = self.press
    #         dx = event.xdata - xpress
    #         dy = event.ydata - ypress
    #         self.x , self.y = (prev_data[0] + dx, prev_data[1] + dy)

    #         self.point.set_data(self.x , self.y)
    #         self.point.figure.canvas.draw()
    #         # self.print_position((self.x , self.y))
    #         if self.conj != None:
    #             self.conj.x, self.conj.y = self.x, -self.y
    #             self.conj.point.set_data(self.conj.x, self.conj.y)
    #             self.conj.point.figure.canvas.draw()
