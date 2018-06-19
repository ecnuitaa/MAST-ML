import os
from os.path import join # because it's used so much
from time import gmtime, strftime

import glob
from dominate import document
from dominate.tags import *

# Goal for this thing:
"""
MAST-ML massively machine ml Turing complete
Datetime

if errors___presetn_:
    errorwarings.txt

Best:
Model params
Title
[plot]

Worst:
model params
Title
[plot]

Title
[plot]

Title
[plot]

final_data.csv
statiscics.csv
info.txt
debug.txt
"""

def is_train_image(path):
    basename = os.path.basename(f)
    return basename.split('.') == 'png' and 'train_' in basename

def is_test_image(path):
    basename = os.path.basename(f)
    return basename.split('.') == 'png' and 'test_' in basename

def show_data(split_dir):

    # collect test image, train image, and other file links
    links = list()
    for root, _, files in os.walk(split_dir):
        for f in files:
            if is_train_image(f):
                train_image = join(root, f)
            elif is_test_image(f):
                test_image = join(root, f)
            else:
                links.append(join(root, f))

    # loop seperately so we can control order
    h2('Train')
    image(train_image)
    h2('Test')
    image(test_image)
    for l in links:
        link(l)

def make_html(outdir):
    for root, dirs, files in os.walk(outdir):
        for d in dirs:
            if 'split_' in os.path.basename(d):
                show_data(join(root, d))

def make_html_2000(save_dir, images: list, starting_data_csv, computed_csvs: list, conf, statistics,
        error_log, debug_log, best=None, median=None, worst=None):
    """ Makes saves html to file with all of the stuff you give it. 
    all arguments refer to the file paths to the things, not the things themselves. """

    # TODO everyhting should be flat files in same dir as index.html
    images = [os.path.basename(path) for path in images]
    statistics = os.path.basename(statistics)

    # check if error_log has an substantial content
    if os.path.exists(error_log):
        with open(error_log) as f:
            errors_present = len(f.read()) > 4

    with document(title='MASTML') as doc:

        # title and date
        h1('MAterial Science Tools - Machine Learning')
        h4(strftime("%Y-%m-%d %H:%M:%S", gmtime()))

        # link to error log
        if errors_present:
            p('You have errors! check ', link(error_log))

        link(statistics)

        # best worst and median images
        for name, path in (('best', best), ('median', median), ('worst', worst)):
            if path:
                h2(name)
                h3(path)
                div(img(src=best), _class='photo')

        # all plots
        h2('Plots')

        for path in images:
            h3(path)
            div(img(src=path), _class='photo')

        # links to csv's
        for path in computed_csvs:
            link(path)

        # link to conf file and starting data
        link(conf)
        link(starting_data_csv)
        link(debug_log)


    with open(join(save_dir, 'index.html'), 'w') as f:
        f.write(doc.render())


def link(href):
    """ Makes it slightly shorter to link files with their names"""
    return p(a(href, href=href))

def image(src):
    div(img(src=src), _class='photo')