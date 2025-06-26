import random

def classify_waste_image(image):
    # Fake prediction for now
    labels = ['Plastic', 'Organic', 'Metal', 'Paper']
    label = random.choice(labels)
    confidence = random.uniform(70, 99)
    return label, confidence
