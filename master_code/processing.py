from module_imports import *

def initialize_model():
    '''
    Loads the model 'CryptoBert' from HuggingFace and returns it.
    '''
    MODEL_bert = f"ElKulako/cryptobert"
    tokenizer_bert = AutoTokenizer.from_pretrained(MODEL_bert)
    tokenizer_bert.model_max_length = 512
    #solve the error: RuntimeError: The expanded size of the tensor (562) must match the existing size (514) at non-singleton dimension
    config_bert = AutoConfig.from_pretrained(MODEL_bert)
    model_bert = AutoModelForSequenceClassification.from_pretrained(MODEL_bert)
    model_bert.config.max_position_embeddings = 512
    return model_bert


def scores_bert(sample_text):
    '''
    Runs a string through the model to analyse sentiment.
    '''
    MODEL_bert = f"ElKulako/cryptobert"
    tokenizer_bert = AutoTokenizer.from_pretrained(MODEL_bert)
    encoded_input_bert = tokenizer_bert(sample_text, return_tensors='pt')
    output_bert = model_bert(**encoded_input_bert)
    scores_bert = output_bert[0][0].detach().numpy()
    scores_bert = softmax(scores_bert) #1st score is negative, 2nd score is netural, 3rd score is positive
    return scores_bert
