import json
import requests
import numpy as np
import tensorflow_datasets as tfds

import tensorflow as tf

breeds = ['affenpinscher', 'afghan_hound', 'african_hunting_dog', 'airedale',
          'american_staffordshire_terrier', 'appenzeller',
          'australian_terrier', 'basenji', 'basset', 'beagle',
          'bedlington_terrier', 'bernese_mountain_dog',
          'black-and-tan_coonhound', 'blenheim_spaniel', 'bloodhound',
          'bluetick', 'border_collie', 'border_terrier', 'borzoi',
          'boston_bull', 'bouvier_des_flandres', 'boxer',
          'brabancon_griffon', 'briard', 'brittany_spaniel', 'bull_mastiff',
          'cairn', 'cardigan', 'chesapeake_bay_retriever', 'chihuahua',
          'chow', 'clumber', 'cocker_spaniel', 'collie',
          'curly-coated_retriever', 'dandie_dinmont', 'dhole', 'dingo',
          'doberman', 'english_foxhound', 'english_setter',
          'english_springer', 'entlebucher', 'eskimo_dog',
          'flat-coated_retriever', 'french_bulldog', 'german_shepherd',
          'german_short-haired_pointer', 'giant_schnauzer',
          'golden_retriever', 'gordon_setter', 'great_dane',
          'great_pyrenees', 'greater_swiss_mountain_dog', 'groenendael',
          'ibizan_hound', 'irish_setter', 'irish_terrier',
          'irish_water_spaniel', 'irish_wolfhound', 'italian_greyhound',
          'japanese_spaniel', 'keeshond', 'kelpie', 'kerry_blue_terrier',
          'komondor', 'kuvasz', 'labrador_retriever', 'lakeland_terrier',
          'leonberg', 'lhasa', 'malamute', 'malinois', 'maltese_dog',
          'mexican_hairless', 'miniature_pinscher', 'miniature_poodle',
          'miniature_schnauzer', 'newfoundland', 'norfolk_terrier',
          'norwegian_elkhound', 'norwich_terrier', 'old_english_sheepdog',
          'otterhound', 'papillon', 'pekinese', 'pembroke', 'pomeranian',
          'pug', 'redbone', 'rhodesian_ridgeback', 'rottweiler',
          'saint_bernard', 'saluki', 'samoyed', 'schipperke',
          'scotch_terrier', 'scottish_deerhound', 'sealyham_terrier',
          'shetland_sheepdog', 'shih-tzu', 'siberian_husky', 'silky_terrier',
          'soft-coated_wheaten_terrier', 'staffordshire_bullterrier',
          'standard_poodle', 'standard_schnauzer', 'sussex_spaniel',
          'tibetan_mastiff', 'tibetan_terrier', 'toy_poodle', 'toy_terrier',
          'vizsla', 'walker_hound', 'weimaraner', 'welsh_springer_spaniel',
          'west_highland_white_terrier', 'whippet',
          'wire-haired_fox_terrier', 'yorkshire_terrier']


# get the image & process that
def get_image(image):
    tensor = tf.io.decode_jpeg(image, channels=3)
    color_channel = tf.image.convert_image_dtype(tensor, tf.float32)
    resize = tf.image.resize(color_channel, (224, 224))

    return resize


# create batch data from the input
def create_batch(data):
    dataset = tf.data.Dataset.from_tensors(tf.constant(data))
    data_batch = dataset.map(get_image).batch(1)

    # convert batch data to numpy array
    convert_to_numpy = tfds.as_numpy(data_batch)
    for i in convert_to_numpy:
        return tf.constant(i)


# send input data to the model and get model predictions
def make_predictions(batch_data):
    headers = {"content-type": "application/json"}
    url = 'https://agile-escarpment-25393.herokuapp.com'
    full_url = f"{url}/v1/models/full-data-resnet50v2/versions/1:predict"

    # turn input data to json object
    data = json.dumps({"signature_name": "serving_default",
                       "instances": create_batch(batch_data).numpy().tolist()})

    # get response form the model
    response = requests.post(full_url, data=data, headers=headers)
    predictions = json.loads(response.text)['predictions']

    return get_breed(predictions[0])


# convert model predictions into label & get the prediction score
def get_breed(prediction):
    max_index = breeds[np.argmax(prediction)]
    score = np.max(prediction)

    return max_index, score
