""" Build index from directory listing

make_index.py </path/to/directory> [--header <header text>]
"""

INDEX_TEMPLATE = r"""
<html>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <link rel="stylesheet" href="../../css/show_page.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <body>
    <nav class="navbar navbar-inverse">
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>                        
          </button>
          <a class="navbar-brand" href="#">Team SDS</a>
        </div>
        <div class="collapse navbar-collapse" id="myNavbar">
          <ul class="nav navbar-nav">
            <li class="active"><a href="https://danish778866.github.io/DataScience">About</a></li>
            <li><a href="https://danish778866.github.io/DataScience/stage_1.html">Stage 1</a></li>
            <li><a href="https://danish778866.github.io/DataScience/stage_2.html">Stage 2</a></li>
            <li><a href="https://danish778866.github.io/DataScience/stage_3.html">Stage 3</a></li>
            <li><a href="https://danish778866.github.io/DataScience/stage_4.html">Stage 4</a></li>
          </ul>
          <ul class="nav navbar-nav navbar-right">
            <li><a href="https://github.com/danish778866/CS839_Project" class="fa fa-github"></a></li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="container">
        <div class="row">
             <div class="item col-sm-12">
                <div class="itemhead">
                    <h4>${header}</h4>
                </div>
                <div class="itemcontent">

<ol>
% for name in names:
    <li><a href="${name}">${name}</a></li>
% endfor
</ol>
</div>
             </div>
        </div>
    </div>
<script>
$( document ).ready(function() {
    $('a').each(function(){
        if ($(this).prop('href') == window.location.href) {
            $(this).parents('li').addClass('active');
	} else {
            $(this).parents('li').removeClass('active');
	}
    });
});
</script>
  </body>
</html>
"""

EXCLUDED = ['index.html']

import os
import argparse

# May need to do "pip install mako"
from mako.template import Template


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("--header")
    args = parser.parse_args()
    fnames = [fname for fname in sorted(os.listdir(args.directory))
              if fname not in EXCLUDED]
    header = (args.header if args.header else os.path.basename(args.directory))
    print(Template(INDEX_TEMPLATE).render(names=fnames, header=header))


if __name__ == '__main__':
    main()

