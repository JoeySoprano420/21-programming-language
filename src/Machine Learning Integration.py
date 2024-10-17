from sklearn.ensemble import RandomForestClassifier
import numpy as np

class BlackjackML:
    def __init__(self):
        # Pre-trained model with dummy data (for illustration)
        self.model = RandomForestClassifier()

        # Dummy training data (feature: var values, target: 0/1 decisions)
        self.X_train = np.array([[10, 5], [12, 7], [8, 3], [15, 10], [5, 2]])
        self.y_train = np.array([1, 0, 1, 0, 1])  # Binary outcome: 1 for proceed, 0 for stop
        
        self.model.fit(self.X_train, self.y_train)

    def predict_action(self, var_values):
        var_values = np.array(var_values).reshape(1, -1)
        prediction = self.model.predict(var_values)
        return "Proceed" if prediction[0] == 1 else "Stop"

# Example Usage
ml_handler = BlackjackML()
action = ml_handler.predict_action([12, 7])  # Predict based on variable values
print(f"Suggested Action: {action}")
