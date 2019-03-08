#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 mohdanishaikh <mohdanishaikh@mohdanishaikh-Inspiron-7573>
#
# Distributed under terms of the MIT license.
import re
import glob
import os
import sys
import getopt

def preprocess_labeled_files(path):
    #files = glob.glob(path)
    #for name in files:
    words = []
    with open(path) as file:
        current_line = file.read()
        current_line = re.sub(r'([,.\"])', r' \1 ', current_line)
        words.extend(current_line.split())
    file.close()
    return words

def is_negative(word):
    ret_val = False
    ignore_punctuations = [",", ".", "\""]
    ignore_words = ["It", "We", "She", "He", "But", "These", "If", "All", "Its", "In", "And", "For", "This", "That", "Or", "On", 
                    "The", "I", "His", "Her", "At", "Then", "There", "Their", "Our", "As", "Was", "How", "What", "Any", "To", "Of",
                   "They", "Have", "Can", "Be", "A", "With", "You", "From", "By", "My", "I\'m", "I\'ll", "It\'s", "Before", "After", 
                    "I\'ve"]
    if not word:
        ret_val = True
    elif word[0].islower():
        ret_val = True
    elif re.search(r'\d', word):
        ret_val = True
    elif word in ignore_punctuations:
        ret_val = True
    elif word in ignore_words:
        ret_val = True
    elif word.isupper():
        ret_val = True
    elif word.count("\'") > 1:
        ret_val = True
    return ret_val

def clean_word(word):
    ends_apostrophe = False
    if word.endswith("\'s"):
        word = word.replace("\'s", "")
        ends_apostrophe = True
    elif word.endswith("s\'"):
        word = word.replace("s\'", "")
        ends_apostrophe = True
    word = re.sub(r'[^\w\s<>/]', '', word)
    return word, ends_apostrophe

def get_prefix(words, index, num_words):
    current_prefix = ""
    if index > 0:
        index = index - 1
        done = False
        num_prefixes = 0
        while not done:
            if words[index] == "," or words[index] == "\"":
                index = index - 1
            elif words[index] == ".":
                done = True
            else:
                current_prefix = words[index] + " " + current_prefix
                index = index - 1
                num_prefixes = num_prefixes + 1
            if num_prefixes == 2 or index < 0:
                done = True
    current_prefix = current_prefix.replace("<person>", "").replace("</person>", "")
    current_prefix = re.sub(r'[^\w\s]', '', current_prefix)
    if not current_prefix:
        current_prefix = "NA"
    return current_prefix.strip()

def get_suffix(words, index, num_words):
    current_suffix = ""
    if index < num_words - 1:
        index = index + 1
        done = False
        num_suffixes = 0
        while not done:
            if words[index] == "," or words[index] == "\"":
                index = index + 1
            elif words[index] == ".":
                done = True
            else:
                current_suffix = current_suffix + " " + words[index]
                index = index + 1
                num_suffixes = num_suffixes + 1
            if num_suffixes == 2 or index > num_words - 1:
                done = True
    current_suffix = current_suffix.replace("<person>", "").replace("</person>", "")
    current_suffix = re.sub(r'[^\w\s]', '', current_suffix)
    if not current_suffix:
        current_suffix = "NA"
    return current_suffix.strip()

def generate_candidates_labels(words, threshold):
    num_words = len(words)
    gen_threshold = threshold
    is_person = False
    candidates = []
    labels = []
    prefix = []
    suffix = []
    feature_ends_apostrophe = []
    for i in range(num_words):
        if i + threshold > num_words - 1:
            gen_threshold = num_words - i
        prune = False
        current_word, ends_apostrophe = clean_word(words[i])
        current_prefix = get_prefix(words, i, num_words)
        current_suffix = get_suffix(words, i, num_words)
        end_person = False
        not_title = True
        if current_word in ["Sir", "Mr", "Ms", "Dr", "Prof", "St"]:
            not_title = False
        if is_negative(current_word):
            prune = True
        else:
            if current_word.startswith("<person>") and current_word.endswith("</person>"):
                current_word = current_word.replace("<person>", "").replace("</person>", "")
                labels.append(1)
            elif current_word.startswith("<person>"):
                current_word = current_word.replace("<person>", "")
                is_person = True
                labels.append(1)
            elif current_word.endswith("</person>"):
                current_word = current_word.replace("</person>", "")
                is_person = False
                labels.append(1)
            elif not_title:
                if is_person:
                    labels.append(1)
                else:
                    labels.append(0)
            if not_title:
                candidates.append(current_word)
                if ends_apostrophe:
                    feature_ends_apostrophe.append(1)
                else:
                    feature_ends_apostrophe.append(0)
                prefix.append(current_prefix)
                suffix.append(current_suffix)
            
        j = 1
        if is_person:
            local_person = True
        while (j < gen_threshold) and (not prune):
            if is_negative(words[i + j]):
                prune = True
            else:
                current_suffix = get_suffix(words, i + j, num_words)
                current_local_word, ends_apostrophe = clean_word(words[i + j])
                current_word = current_word + " " + current_local_word
                if "<person>" in current_word and "</person>" in current_word:
                    current_word = current_word.replace("<person>", "").replace("</person>", "")
                elif "<person>" in current_word:
                    current_word = current_word.replace("<person>", "")
                elif "</person>" in current_word:
                    current_word = current_word.replace("</person>", "")
                    end_person = True
                if is_person and local_person:
                    labels.append(1)
                    if end_person:
                        local_person = False
                else:
                    labels.append(0)
                candidates.append(current_word)
                if ends_apostrophe:
                    feature_ends_apostrophe.append(1)
                else:
                    feature_ends_apostrophe.append(0)
                prefix.append(current_prefix)
                suffix.append(current_suffix)
                j = j + 1
    return candidates, labels, prefix, suffix, feature_ends_apostrophe

def write_data(path, content):
    f = open(path, "w")
    for line in content:
        f.write(str(line) + "\n")
    f.close()

def preprocess_driver(data_files, candidates_dir, labels_dir, features_dir):
    files = glob.glob(data_files)
    words = []
    for name in files:
        words = preprocess_labeled_files(name)  
        file_name = os.path.basename(name)
        candidates_file = candidates_dir + os.sep + file_name 
        prefix_file = candidates_dir + os.sep + file_name + ".pre"
        suffix_file = candidates_dir + os.sep + file_name + ".suf"
        labels_file = labels_dir + os.sep + file_name 
        feature_ends_apostrophe_file = features_dir + os.sep + file_name
        candidates, labels, prefix, suffix, feature_ends_apostrophe = generate_candidates_labels(words, 4)
        write_data(candidates_file, candidates)
        write_data(labels_file, labels)
        write_data(prefix_file, prefix)
        write_data(suffix_file, suffix)
        #write_data(feature_ends_apostrophe_file, feature_ends_apostrophe)

def usage(exit_code):
    print("You should just know!")
    sys.exit(exit_code)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:", ["help", "data="])
    except getopt.GetoptError as err:
        print(str(err))
        usage(2)
    data_dir = ""
    for o, a in opts:
        if o in ("-d", "--data"):
            data_dir = a
        elif o in ("-h", "--help"):
            usage(0)
        else:
            assert False, "unhandled option"
    if data_dir != "":
        project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        data_files = project_dir + os.sep + "data" + os.sep + data_dir  + os.sep + "*.txt"
        candidates_dir = project_dir + os.sep + "data" + os.sep + data_dir + os.sep + "candidates"
        if not os.path.exists(candidates_dir):
            os.makedirs(candidates_dir)
        labels_dir = project_dir + os.sep + "data" + os.sep + data_dir + os.sep +  "labels"
        if not os.path.exists(labels_dir):
            os.makedirs(labels_dir)
        features_dir = project_dir + os.sep + "data" + os.sep + "scratch"
        preprocess_driver(data_files, candidates_dir, labels_dir, features_dir)
    else:
        usage(2)

if __name__ == '__main__': 
    main()
