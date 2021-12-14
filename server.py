import torch
import torchvision.models as models
import torch.nn as nn
from torchvision import datasets, transforms as T
import torchvision
# from IPython.display import Image, display
from PIL import Image
from flask import Flask, json, request


# Recurrent neural network (many-to-one)
class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(RNN, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        # Set initial hidden and cell states
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)

        # Forward propagate LSTM
        out, _ = self.lstm(x, (h0, c0))  # out: tensor of shape (batch_size, seq_length, hidden_size)

        # Decode the hidden state of the last time step
        out = self.fc(out[:, -1, :])
        return out

def preprocess(image):
    image = T.ToTensor()(image)
#     image = image.unsqueeze(0)
    return image

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

model = RNN(28, 128, 2, 10)
model.load_state_dict(torch.load('model.ckpt', map_location=device))
model.to(device)
model.eval()


api = Flask(__name__)

@api.route('/inference', methods=['POST'])
def get_result():
    res = {}
    file = request.files['image']
    if not file:
        res['status'] = 'missing image'
    else:
        res['status'] = 'success'
        image = Image.open(file.stream)
        inputs = preprocess(image).to(device)
        print(inputs.shape)
        outputs = model(inputs[:1])
        _, predicted = torch.max(outputs.data, 1)
        res['ret'] = int(predicted)

    return json.dumps(res)

api.run(host='0.0.0.0')