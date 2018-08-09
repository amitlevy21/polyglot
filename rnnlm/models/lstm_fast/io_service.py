import tensorflow as tf

from rnnlm.models.lstm_fast import reader
from rnnlm.models.lstm_fast import writer


def _words_to_ids(words, vocab):

    return [vocab[word] for word in words if word in vocab]


def raw_to_tf_records(raw_path, tf_record_path, vocab_path, seq_len):
    raw_file = tf.gfile.GFile(raw_path, "r")
    vocab_file = tf.gfile.GFile(vocab_path, "r")
    vocab = reader.build_vocab(vocab_file)
    packed_vocab = [vocab]

    gen_words = reader.gen_shifted_word(file_obj=raw_file, seq_len=seq_len)
    writer.write_tf_records(gen_words=gen_words,
                            destination_path=tf_record_path,
                            preprocessor_feature_fn=_words_to_ids,
                            preprocessor_feature_params=packed_vocab,
                            preprocessor_label_fn=_words_to_ids,
                            preprocessor_label_params=packed_vocab)


def load_tf_records(tf_record_path, batch_size, seq_len):
    return reader.read_tf_records(tf_record_path=tf_record_path, batch_size=batch_size, seq_len=seq_len)
