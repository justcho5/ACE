import sys
sys.path.append("/home/hjcho/projects/hnsc/histoXai/tcav")
import tensorflow as tf
from tensorflow.python.framework import graph_io
from tensorflow.keras.applications.inception_v3 import InceptionV3

from tensorflow.python.platform import gfile
import tcav.utils as utils
import tensorflow as tf

def make_logfile(graph_path, logdir):
    sess = utils.create_session()
    with sess.graph.as_default():
        input_graph_def = tf.GraphDef()
        with tf.gfile.FastGFile(graph_path, 'rb') as f:
            input_graph_def.ParseFromString(f.read())
            tf.import_graph_def(input_graph_def)
        LOGDIR=logdir
        train_writer = tf.summary.FileWriter(LOGDIR)
        train_writer.add_graph(sess.graph)

def freeze_graph(graph, session, output, model_folder, model_filename):
    with graph.as_default():
        graphdef_inf = tf.graph_util.remove_training_nodes(graph.as_graph_def())
        graphdef_frozen = tf.graph_util.convert_variables_to_constants(session, graphdef_inf, output)
        graph_io.write_graph(graphdef_frozen, model_folder, model_filename, as_text=False)

def convert_to_pb(h5_model_path, model_folder, pb_filename):
    tf.keras.backend.set_learning_phase(0)
    keras_model_path = h5_model_path

    base_model = tf.keras.models.load_model(keras_model_path, compile=False)
    base_model.compile(loss='sparse_categorical_crossentropy',
                    optimizer=tf.keras.optimizers.Adam())
    session = tf.keras.backend.get_session()

    INPUT_NODE = base_model.inputs[0].op.name
    OUTPUT_NODE = base_model.outputs[0].op.name
    freeze_graph(session.graph, session, [out.op.name for out in base_model.outputs], model_folder, pb_filename)

def main():
    h5_file = "/mnt/gpucluster/hnsc/slideflow_projects/hpv_224/models/HPV_status-hpv_224-kfold3/trained_model.h5"
    model_folder = "/mnt/gpucluster/hnsc/slideflow_projects/hpv_224/models/HPV_status-hpv_224-kfold3/"
    pb_filename = "hpv224_xception.pb"
    convert_to_pb(h5_file, model_folder, pb_filename)

if __name__ == '__main__':
    main()
