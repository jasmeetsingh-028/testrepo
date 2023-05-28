import discord
import random
import json
import torch
from model import NeuralNet
from utils_nltk import bag_of_words, tokenize



# Create a Discord client instance
intents = discord.Intents.default()
intents.members = True  # Needed to receive member events (e.g. on_member_join)
client = discord.Client(intents=intents)


# Load your NLP model using PyTorch

# Define an event listener to handle incoming messages
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print('Message received: {0.content}'.format(message))
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    with open('intents.json', 'r') as f:
        intnts = json.load(f)

    FILE = 'data.pth'

    data = torch.load(FILE)

    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]

    all_words = data["all_words"]
    tags = data["tags"]
    model_state = data["model_state"]

    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()
    
    # Preprocess the message text for input to the model
    sentence = str(message.content)

    print(f'user: {sentence}')
    print(type(sentence), len(sentence))

    sentence = tokenize(sentence)
    x = bag_of_words(sentence,all_words)
    x = x.reshape(1, x.shape[0])  #model expects in this format
    x = torch.from_numpy(x)  #converting it into torch tensor as model expects this and bow gives numpy array as output

    output = model(x.to(device))
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    print( "PROCESSED!" ,prob)

    if prob.item()> 0.70:

                for intent in intnts["intents"]:
                    if tag == intent["tag"]:
                        response_text = random.choice(intent['responses'])

    else:
         
         response_text = 'i did not understand the Master Scarn!'
        
    print(f'response: {response_text}')

    # Send the response back to the Discord channel
    await message.channel.send(response_text)

# Run the client and connect to the Discord API
client.run('MTA4MDA2NjkxMzA2Mjg5MTU1MQ.GWFXkY.QyA9waTc5fr4f3aZLu4lBIqX0-vOPUe9GPVq8A')
