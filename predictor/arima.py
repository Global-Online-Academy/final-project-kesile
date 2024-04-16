import numpy as np

class Arima:
    def __init__(self, data, p, d, q):
        self.data = data
        self.p = p
        self.d = d
        self.q = q
        self.coefficients = None
        self.prepare_data()
        self.fit()

    def prepare_data(self):
        diff_data = self.data.copy()
        for _ in range(self.d):
            diff_data = np.diff(diff_data)
        self.diff_data = diff_data[self.d:]

    def fit(self):
        X = []
        for i in range(self.p, len(self.diff_data)):
            x_row = [self.diff_data[i - j] for j in range(1, self.p + 1)]
            x_row += [-self.diff_data[i - j] for j in range(1, self.q + 1)]
            X.append(x_row)
        X = np.array(X)

        y = self.diff_data[self.p:]

        coefficients = np.linalg.lstsq(X, y, rcond=None)[0]
        self.coefficients = coefficients

    def forecast(self, steps):
        predictions = []
        last_data = self.data[-self.p:]
        for _ in range(steps):
            ar_terms = [last_data[j] for j in range(self.p)]
            ma_terms = predictions[-self.q:] if len(predictions) >= self.q else [0] * self.q
            predicted = sum(self.coefficients[:self.p] * ar_terms) + sum(self.coefficients[self.p:] * ma_terms)
            predictions.append(round(predicted))
            last_data = np.append(last_data[1:], predicted)
        
        if self.data[-1] != predictions[0]:
            adjustment = self.data[-1] - predictions[0]
            predictions = [prediction + adjustment for prediction in predictions]

        return predictions
