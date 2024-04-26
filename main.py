from predictor.arima import Arima
from utils.read_line import read_line_chart
from bokeh.plotting import figure, show, output_file
import numpy as np

class TrendsPredictor:
    def __init__(self, image_path):
        self.image_path = image_path
        self._read_line()
        self._fit_model()
    
    def _read_line(self):
        self.sequence = read_line_chart(self.image_path)
        return self.sequence
    
    def _fit_model(self):
        self.model = Arima(
            data = self.sequence,
            p = 1,
            d = 1,
            q = 1
        )

    def forecast(self, steps=10):
        forecasts = self.model.forecast(steps)
        
        output_file("renders/forecast.html")
        p = figure(title="Time Series Forecast", x_axis_label="Time", y_axis_label="Value")
        
        p.line(list(range(len(self.sequence))), self.sequence, line_color="blue", legend_label="Original Data")
        
        forecast_x = list(np.arange(len(self.sequence), len(self.sequence) + len(forecasts)))
        p.line(forecast_x, forecasts, line_color="red", legend_label="Forecasted Data")
        
        show(p)
        
        return forecasts


x = TrendsPredictor('images/eras.png')
print(x.sequence)
print(x.forecast(10))