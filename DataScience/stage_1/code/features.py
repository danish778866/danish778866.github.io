import csv
import os, sys, getopt
from nltk.corpus import wordnet
from gensim.models import KeyedVectors

def tag_word(w):
    pos_l = set()
    tags = [0,0,0,0,0]
    for tmp in wordnet.synsets(w):
        if tmp.name().split('.')[0] == w:
            pos_l.add(tmp.pos())
    for val in pos_l:
        if val  == 'n':
            tags[0]=1
        elif val  == 'v':
            tags[1]=1;
        elif val ==  'a':
            tags[2]=1
        elif val  ==  's':
            tags[3]=1
        elif val == 'r':
            tags[4]=1
        else:
            print(w, val)
    return tags

def word(w):
    if not wordnet.synsets(w):
        return False
    else:
        return True

def is_valid(path1):
    valid_cand = []
    with open(path1) as candidates:
        current_line = candidates.readline()
        if current_line:
            current_line = candidates.readline()
        while current_line:
            cand_words = current_line.split()
            v_c = False
            for w in cand_words:
                v_c = word(w) or v_c
            if v_c == True:
                valid_cand.append(1)
            else:
                valid_cand.append(0)
            current_line = candidates.readline()
    candidates.close()
    return valid_cand

def is_missing(path):
    is_missing = []
    with open(path) as list:
        current_line = list.readline()
        if current_line:
            current_line = list.readline()
        while current_line:
            if current_line == "NA":
                is_missing.append(1)
            else:
                is_missing.append(0)
            current_line = list.readline()
    return is_missing

def nvasr(path):
    tags = []
    with open(path) as list:
        current_line = list.readline()
        if current_line:
            current_line = list.readline()
        while current_line:
            #print(current_line)
            phrase = current_line.split()
            cur_tag =[0,0,0,0,0]
            for w in phrase:
                #print(w)
                this_tag = tag_word(w.lower())
                #print(this_tag)
                i=0
                while i<5:
                    if this_tag[i]==1:
                        cur_tag[i]=1
                    i=i+1
                #print(cur_tag)
            tags.append(cur_tag)
            current_line = list.readline()
    list.close()
    return tags

def has_apos(w):
    result = w.find("'")
    if result != -1:
        return 1
    else:
        return 0

def apos_cand(path):
    apos = []
    with open(path) as candidates:
        current_line = candidates.readline()
        if current_line:
            current_line = candidates.readline()
        while current_line:
            cand_words = current_line.split()
            a=False
            for w in cand_words:
                a = has_apos(w) or a
            if a == True:
                apos.append(1)
            else:
                apos.append(0)
            current_line = candidates.readline()
    candidates.close()
    return apos

def word2vec(path, model_path):
    model = KeyedVectors.load_word2vec_format(model_path, binary=True)
    vec = []
    #return vec
    with open(path) as list:
        num=0
        current_line = list.readline()
        if current_line:
            current_line = list.readline()
        while current_line:
            num=num+1
            #print(num)
            phrase = current_line.split()
            cur_tag = [0]*300
            j = 0
            for w in phrase:
                this_tag=[0]*300
                if w in model.vocab:
                    this_tag = model[w]
                i=0
                while i<len(this_tag):
                    cur_tag[i]=cur_tag[i]+this_tag[i]
                    i=i+1
                j=j+1
            i=0
            while i<len(cur_tag):
                cur_tag[i]=cur_tag[i]/j
                i=i+1
            vec.append(cur_tag)
            current_line = list.readline()
    list.close()
    return vec

def write_array(path, content, header):
    f = open(path, "w")
    f.write(str(header)+"\n")
    for line in content:
        f.write(','.join(str(var) for var in line) + "\n")
    f.close()

def write_data(path, content, header):
    f = open(path, "w")
    f.write(str(header)+"\n")
    for line in content:
        f.write(str(line) + "\n")
    f.close()

def usage(exit_code):
    print("You should just know!")
    sys.exit(exit_code)

def word2vec_header():
    a = "w2v"
    under = "_"
    comma = ","
    head = ""
    i = 0
    while i < 299:
        cnt = str(i)
        head = head + a + under + cnt + comma
        i = i + 1
    ctr = "299"
    head = head + a + under + ctr
    return head

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
        candidates_csv = project_dir + os.sep + "data" + os.sep + data_dir + os.sep + "candidates" + os.sep + "candidates.csv" 
        prefixes_csv = project_dir + os.sep + "data" + os.sep + data_dir + os.sep + "candidates" + os.sep + "prefixes.csv" 
        suffixes_csv = project_dir + os.sep + "data" + os.sep + data_dir + os.sep + "candidates" + os.sep + "suffixes.csv" 
        features_dir = project_dir + os.sep + "data" + os.sep + data_dir + os.sep + "features" + os.sep
        word2vec_model = project_dir + os.sep + "models" + os.sep + "third_party" + os.sep + "GoogleNews-vectors-negative300.bin"
        if not os.path.exists(features_dir):
            os.makedirs(features_dir)
        
        valid_cand  = is_valid(candidates_csv)
        valid_pre = is_valid(prefixes_csv)
        valid_suff = is_valid(suffixes_csv)
        is_missing_pre = is_missing(prefixes_csv)
        is_missing_suf = is_missing(suffixes_csv)
        nvasr_cand = nvasr(candidates_csv)
        nvasr_pre = nvasr(prefixes_csv)
        nvasr_suff = nvasr(suffixes_csv)
        apos = apos_cand(candidates_csv)
        feature_word2vec = word2vec(candidates_csv, word2vec_model)
        
        write_data(features_dir + "is_valid_cand.csv", valid_cand, "is_cand_valid")
        write_data(features_dir + "is_valid_pre.csv", valid_pre, "is_pre_valid")
        write_data(features_dir + "is_valid_suff.csv", valid_suff, "is_suff_valid")
        write_data(features_dir + "is_missing_pre.csv", is_missing_pre, "is_pre_missing")
        write_data(features_dir + "is_missing_suf.csv", is_missing_suf, "is_suff_missing")
        write_array(features_dir + "tags_cand.csv",nvasr_cand, "n_cand, v_cand,a_cand,s_cand,r_cand")
        write_array(features_dir + "tags_pre.csv",nvasr_pre, "n_pre, v_pre,a_pre,s_pre,r_pre")
        write_array(features_dir + "tags_suff.csv",nvasr_suff, "n_suff, v_suff,a_suff,s_suff,r_suff")
        write_data(features_dir + "has_apos_cand.csv", apos, "has_apos_any")
        write_array(features_dir + "word2vec.csv", feature_word2vec, word2vec_header())
    else:
        usage(2)

if __name__ == '__main__':
    main()
