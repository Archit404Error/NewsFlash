import numpy as np

import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import tensorflow_hub as hub
from math import floor

model = tf.keras.models.load_model('dem_or_rep.h5')

def similarity_matrix(merge_list):
    g = tf.Graph()
    with g.as_default():
      text_input = tf.placeholder(dtype=tf.string, shape=[None])
      embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder-large/3")
      embedded_text = embed(text_input)
      init_op = tf.group([tf.global_variables_initializer(), tf.tables_initializer()])
    g.finalize()

    session = tf.Session(graph=g)
    session.run(init_op)

    #initialize embeddings array:
    emb_all = np.zeros([len(merge_list),512])
    #Outer for loop:
    for i in range(0,len(merge_list)):
        #Here is where we run the previously started session, so it is important to run previous step succesfully:
        i_emb = session.run(embedded_text, feed_dict={text_input: [merge_list[i]]})
        emb_all[i,:] = i_emb
    return emb_all

def political_bias(inp):
    emb_all = similarity_matrix(inp)
    prob = model.predict(emb_all)
    classifications = []
    for pair in prob:
        pair_prob = pair[0]

        if floor(pair_prob * 100) <= 82:
            classifications.append('democratic')
        else:
            classifications.append('republican')
    return classifications
