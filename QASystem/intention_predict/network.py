# -*- coding: utf-8 -*-
"""
Created on Thu May 30 20:44:42 2019

@author: cm
"""

import os
import tensorflow as tf
import QASystem.intention_predict.modeling as modeling
from QASystem.intention_predict.hyperparameters import Hyperparamters as hp


num_labels = hp.num_labels
bert_config_file = os.path.join(hp.bert_path,'albert_config.json')
bert_config = modeling.AlbertConfig.from_json_file(bert_config_file)



class Albert(object):
    def __init__(self,is_training):
        # Training or not
        self.is_training = is_training    
        
        # Placeholder       
        self.input_ids = tf.placeholder(tf.int32, shape=[None, hp.sequence_length], name='input_ids')
        self.input_masks = tf.placeholder(tf.int32, shape=[None,  hp.sequence_length], name='input_masks')
        self.segment_ids = tf.placeholder(tf.int32, shape=[None,  hp.sequence_length], name='segment_ids')
        self.label_ids = tf.placeholder(tf.float32, shape=[None,hp.num_labels], name='label_ids')
               
        # Load BERT model
        self.model = modeling.AlbertModel(
                                    config=bert_config,
                                    is_training=self.is_training,
                                    input_ids=self.input_ids,
                                    input_mask=self.input_masks,
                                    token_type_ids=self.segment_ids,
                                    use_one_hot_embeddings=False)

        # Get the feature vector by BERT
        output_layer = self.model.get_pooled_output()      
         
        # Hidden size 
        hidden_size = output_layer.shape[-1].value                            

        with tf.name_scope("Full-connection"):  
            output_weights = tf.get_variable(
                  "output_weights", [num_labels, hidden_size],
                  initializer=tf.truncated_normal_initializer(stddev=0.02))            
            output_bias = tf.get_variable(
                  "output_bias", [num_labels], initializer=tf.zeros_initializer())   
            logits = tf.nn.bias_add(tf.matmul(output_layer, output_weights, transpose_b=True), output_bias)            
            # Prediction sigmoid(Multi-label)
            self.probabilities = tf.nn.sigmoid(logits)
 

        with tf.variable_scope("Prediction"):             
            # Prediction               
            zero = tf.zeros_like(self.probabilities)
            one = tf.ones_like(self.probabilities)
            self.predictions = tf.where(self.probabilities < 0.5, x=zero, y=one)
            



