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
import argparse
import pandas as pd

from os import listdir
from os.path import isfile, join
import random


def sample(tiles_nolabel_dir, dir_list, num_random_images, q, r):
    tiles = []

    if len(dir_list)>num_random_images:
        sample = random.sample(dir_list, num_random_images)
        for dir in sample:
            sample_dir = os.path.join(tiles_nolabel_dir, dir)
            for root, _, files in os.walk(sample_dir):
                tiles.append(os.path.join(root,random.choice(files)))
                break
    else:
        sample = random.sample(dir_list, r)
        print(sample)
        print(r)
        for dir in dir_list:
            sample_dir = os.path.join(tiles_nolabel_dir, dir)
            for root,_,files in os.walk(sample_dir):
                samples = random.sample(files, q)
                for samp in samples:
                    tiles.append(os.path.join(root,samp))
                break
        for dir in sample:
            sample_dir = os.path.join(tiles_nolabel_dir, dir)
            print("sample", sample_dir)
            for root,_,files in os.walk(sample_dir):
                print(files)
                print(root)
                tiles.append(os.path.join(root,random.choice(files)))
                break
    return tiles

def copy_rand_images(tiles_nolabel_dir, num_random_images, annota_path = None, category = None):

    if category:
        df = pd.read_csv(annota_path)
        df = df[df.HPV_status==category]
    
        lst = df.slide.values.tolist()
        print(len(lst))
        print(len(set(lst)))
        q=int(num_random_images/len(lst))
        r=num_random_images%len(lst)
        return sample(tiles_nolabel_dir,lst, num_random_images,q,r)


    else:
        for root, dirs, files in os.walk(tiles_nolabel_dir):
            tcga_dirs = [dir for dir in dirs if "TCGA" in dir]
            print(len(tcga_dirs))
            print(len(set(tcga_dirs)))
            dic = {}
            q = int(num_random_images/len(tcga_dirs))
            r = num_random_images%len(tcga_dirs)
            break
        return sample(tiles_nolabel_dir,tcga_dirs, num_random_images, q,r)



def main():
    project_name = "hpv_224"
    tiles_dir = "/mnt/gpucluster/hnsc/slideflow_projects/hpv_224/tiles/"
    tiles_nolabel_dir = os.path.join(tiles_dir, "no_label")
    num_expts = 50
    num_random_images = 100
    project_dir = os.path.join(tiles_dir, project_name)
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
        tiles = copy_rand_images(tiles_nolabel_dir, num_random_images)
        for tile in tiles:
            file = tile.split("/")[-1]
            try:
                tf.gfile.Copy(tile, os.path.join(experiment_dir,file))
            except:
                print(tile)
                print(os.path.join(experiment_dir,file))
        if i ==num_expts:
            tf.gfile.Rename(experiment_dir, random_discovery)
    for category in ["positive", "negative"]:
        tiles = copy_rand_images(tiles_nolabel_dir, num_random_images, annota_path="/mnt/gpucluster/hnsc/slideflow_projects/hpv_224/tcga_hnsc_anns_n_slides.csv", category=category)
        if category == "positive":
            for tile in tiles:
                file = tile.split("/")[-1]
                tf.gfile.Copy(tile, os.path.join(pos_dir, file))
        else:
            for tile in tiles:
                file = tile.split("/")[-1]
                tf.gfile.Copy(tile,os.path.join(neg_dir, file))

if __name__ == '__main__':
    main()
