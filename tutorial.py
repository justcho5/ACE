```
python3 ace_run.py --num_parallel_runs 0 --target_class zebra --source_dir SOURCE_DIR --working_dir SAVE_DIR --model_to_run GoogleNet --model_path ./tensorflow_inception_graph.pb --labels_path ./imagenet_labels.txt --bottlenecks mixed4c --num_random_exp 40 --max_imgs 50 --min_imgs 30
```
import os
num_parallel_runs = 0
target_class = "positive"
source_dir = "/mnt/gpucluster/hnsc/data/hnsc_slides/tiles/all/hpv_positive/source_dir"
proj_dir = "/mnt/gpucluster/hnsc/histoXai/ace_projects/ace_test_hpv/"
working_dir = os.path.join(proj_dir, "save_dir")
model_to_run = "Xception"
model_path = os.path.join(proj_dir, frozen_model.pb)
labels_path = os.path.join(proj_dir, labels.txt)
bottlenecks = "add_11/add"
num_random_exp = 20
max_imgs = 50
min_imgs = 30



import pandas as pd

df = pd.read_csv("/Users/justina/Documents/EPFL/thesis/project/hnsc/sara/tcga_hnsc_anns_n_slides.csv")
df
df[df.HPV_status == 'positive'][['slide']].to_csv("positive_slides.csv", header=False, index=False)
