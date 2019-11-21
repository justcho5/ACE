import sys
from sys import getsizeof
sys.path.append("/Users/justina/Documents/EPFL/thesis/projects/hnsc/histoXai/tcav")
sys.path.append("/home/hjcho/projects/hnsc/histoXai/tcav")

import os
import numpy as np
import sklearn.metrics as metrics
import tcav.utils as utils
import tensorflow as tf

import ace_helpers
from ace import ConceptDiscovery
import argparse
from pympler import muppy, summary
import pandas as pd

from os import listdir
from os.path import isfile, join
import random


def sample(dir_list, num_random_images):
    tiles = []

    if len(tcga_dirs)>num_random_images:
        sample = random.sample(tcga_dirs, num_random_images)
        for dir in tcga_dirs:
            sample_dir = os.path.join(tiles_dir, dir)
            for root, _, files in os.walk(sample_dir):
                tiles.append(os.path.join(root,random.choice(files)))
                break
    else:
        sample = []
        sample.append(random.sample(tcga_dirs, r))
        for dir in tcga_dirs:
            sample_dir = os.path.join(tiles_dir, dir)
            for _,_,files in os.walk(sample_dir):
                samples = random.sample(files, q)
                for sample in samples:
                    tiles.append(os.path.join(root,sample))
                break
        for dir in sample:
            sample_dir = os.path.join(tiles_dir, dir)
            for _,_,files in os.walk(sample_dir):
                tiles.append(os.path.join(root,random.choice(files)))
                break
    return tiles

def copy_rand_images(tiles_dir, num_random_images, annota_path = None, category = None):

    if category:
        df = pd.read_csv("annota_path")
        df = df[df.HPV_status==category]
        lst = df.slide.values.tolist()
        return sample(lst, num_random_images)


    else:
        for root, dirs, files in os.walk(tiles_dir):
            tcga_dirs = [dir for dir in dirs if "TCGA" in dir]
            dic = {}
            q = num_random_images/len(tcga_dirs)
            r = num_random_images%len(tcga_dirs)
            break
        return sample(tcga_dirs, num_random_images)



def main():
    project_name = "hpv_224"
    tiles_dir = "/mnt/gpucluster/hnsc/slideflow_projects/hpv_224/tiles/"
    num_expts = 50
    num_random_images = 100
    project_dir = os.path.join("/home/hjcho/projects/hnsc/histoXai/", project_name)
    print(project_dir)
    samples_dir = os.path.join(project_dir,"samples") # csv files for sampling random images
    source_dir = os.path.join(project_dir, "source_dir")
    pos_dir = os.path.join(source_dir, "positive")
    neg_dir = os.path.join(source_dir, "negative")
    random_discovery = os.path.join(source_dir, "random_discovery")
    tf.gfile.MakeDirs(project_dir)
    tf.gfile.MakeDirs(samples_dir)
    tf.gfile.MakeDirs(source_dir)
    tf.gfile.MakeDirs(pos_dir)
    tf.gfile.MakeDirs(neg_dir)
    for i in range(num_expts+1):
        experiment_dir = os.path.join(source_dir, "random500_{}".format(i))
        tf.gfile.MakeDirs(experiment_dir)
        tiles = copy_rand_images(tiles_dir, num_random_images)
        for tile in tiles:
            tf.gfile.Copy(tile, experiment_dir)
        if i ==num_expts:
            tf.gfile.Rename(experiment_dir, random_discovery)
    for category in ["positive", "negative"]:
        tiles = copy_rand_images(tiles_dir, num_random_images, annota_path="/mnt/gpucluster/hnsc/slideflow_projects/hpv_224/tcga_hnsc_anns_n_slides.csv", category=category)
        if category == "positive":
            for tile in tiles:
                tf.gfile.Copy(tile, pos_dir)
        else:
            for tile in tiles:
                tf.gfile.Copy(tile,neg_dir)

    if __name__ == '__main__':
        main()
