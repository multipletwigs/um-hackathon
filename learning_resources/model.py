import torch
class RegressionModel(torch.nn.Module):
    def __init__(self, input_dim, output_dim):
        super(RegressionModel, self).__init__()

        # Define a simple layer.
        # Equation of layer is y = Wx + b
        self.linear = torch.nn.Linear(input_dim, output_dim)

    def forward(self, x):

        # Simple linear regression.
        y_pred = self.linear(x)
        return y_pred

    def train(self, training_data, attributes, num_epochs, learning_rate):
        # Define the loss and optimizer.
        criterion = torch.nn.MSELoss()

        # Define the optimizer needed. There's SGD, Adam, etc.
        # self.parameters() returns all trainable parameters of the model.
        optimizer = torch.optim.RMSprop(self.parameters(), lr=learning_rate)

        inputs = torch.from_numpy(training_data[attributes].values).float()
        labels = torch.from_numpy(training_data["median_house_value"].values).float()
        
        # Train the model with early stopping.
        for epoch in range(num_epochs):

            # Reset the gradients to zero before starting to do backpropragation.
            optimizer.zero_grad()

            # Forward pass.
            y_pred = self.forward(inputs)

            # Compute the loss.
            loss = criterion(y_pred, labels)

            # Backward pass.
            loss.backward()
            optimizer.step()

            # Print the loss every 10 epochs.
            if (epoch + 1) % 10 == 0:
                print("Epoch: {}/{}, Loss: {}".format(epoch + 1, num_epochs, loss.item()))