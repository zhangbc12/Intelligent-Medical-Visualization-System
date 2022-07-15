import os
pwd = os.path.dirname(os.path.abspath(__file__))
from QASystem.intention_predict.utils import load_vocabulary


class Hyperparamters:
    # Train parameters
    num_train_epochs = 40
    print_step = 20
    batch_size = 32           
    summary_step = 20
    num_saved_per_epoch = 1
    max_to_keep = 100
    logdir = 'logdir/model_01'
    file_save_model = 'model/model_01'

    # Predict model file
    file_model = 'model/saved_01'
    
    # Train/Test data 
    data_dir = os.path.join(pwd,'data')
    train_data = 'train_medical.csv'
    test_data = 'test_onehot.csv'
    
    # Load vocabulcary dict
    dict_id2label,dict_label2id = load_vocabulary(os.path.join(pwd,'data','labels.txt'))
    label_vocabulary = list(dict_id2label.values())
    
    # Optimization parameters
    warmup_proportion = 0.1    
    use_tpu = None
    do_lower_case = True    
    learning_rate = 5e-5     
    
    # TextCNN parameters
    num_filters = 128    
    filter_sizes = [2,3,4,5,6,7]
    embedding_size = 384
    keep_prob = 0.5
    
    # Sequence and Label
    sequence_length = 60
    num_labels = len(list(dict_id2label))    
 
    # ALBERT
    model = 'albert_small_zh_google'
    bert_path = os.path.join(pwd,model)
    vocab_file = os.path.join(pwd,model,'vocab_chinese.txt')
    init_checkpoint = os.path.join(pwd,model,'albert_model.ckpt')
    saved_model_path = os.path.join(pwd,'model')    