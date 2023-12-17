import tensorflow as tf

# Load the Keras model
model = tf.keras.models.load_model('models/gen_model_50.h5')

# Export the model to SavedModel format
tf.saved_model.save(model, 'models/gen_model_50')
