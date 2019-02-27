# IDEA (Text Data Visualizer)

![django-version-2.1.2](https://img.shields.io/badge/django-v2.1.2-brightgreen.svg)
![python-version-3.6.7](https://img.shields.io/badge/python-3.6.7-blue.svg)
![GitHub](https://img.shields.io/github/license/DevBruce/IDEA.svg)  
![GitHub release](https://img.shields.io/github/release/DevBruce/IDEA.svg)
![GitHub Release Date](https://img.shields.io/github/release-date/DevBruce/IDEA.svg)

## Intro & Purpose

It is hard for non-developer to visualize data.  
But if you use IDEA, you can **visualize data easily.**

> Please feel free to provide feedback If `Project: IDEA` have any problems

<br><br>

## Requirements

If you want to test `Project: IDEA` locally on your environment,  
The followings are required.  

- [mecab-ko](https://bitbucket.org/eunjeon/mecab-ko)

- [mecab-ko-dic](https://bitbucket.org/eunjeon/mecab-ko-dic)

<br>

### Python Packages

```bash
$ pip install -r requirements.txt
```

<br>

### Secret Data

1. Make `.secrets` directory at `ROOT_DIR`

2. Make `base.json` at `/.secrets`

<br>

Form of `base.json`

```json
{
  "SECRET_KEY": "<SECRET_KEY>"
}
```

Input your Django SECRET\_KEY at `<SECRET_KEY>`.  

<br>

### matplotlibrc

You have to set backend parameter in your `matplotlibrc`.  

Normally, it is located at `~/.matplotlib`.  

Open `matplotlibrc` file and set backend parameter like below.

```
backend : Agg
```

<br>

### Set Environment Variable

There are three separate settings.py. It is recommended that you use files for local.(`local.py`)  
Set the environment variable through the code below and run the server.  

```bash
$ export DJANGO_SETTINGS_MODULE=config.settings.local
```

<br><br>

## Three Types Of Visualization

- Semantic Network Analysis (Interactive) (with [ECharts](http://echarts.baidu.com/) - [Les Miserables](http://www.echartsjs.com/examples/editor.html?c=graph))

- Word Cloud

<br><br>

## How To Use

If you have some data which you want to visualize,  
just put it in IDEA.  
Then click Visualization button!

<br><br>

## History

[![GitHub release](https://img.shields.io/github/release/DevBruce/IDEA.svg)](https://github.com/DevBruce/IDEA/releases)
[![GitHub Release Date](https://img.shields.io/github/release-date/DevBruce/IDEA.svg)](https://github.com/DevBruce/IDEA/releases)

See [HISTORY.md](https://github.com/DevBruce/IDEA/blob/master/HISTORY.md)

<br><br>

## Preview

- **Home** / **Config Page**

<br>

<div align="center">
<a href="https://github.com/DevBruce/IDEA/blob/master/preview/home.png">
<img src="https://github.com/DevBruce/IDEA/blob/master/preview/home.png" width="400">
</a>
<a href="https://github.com/DevBruce/IDEA/blob/master/preview/config_page.png">
<img src="https://github.com/DevBruce/IDEA/blob/master/preview/config_page.png" width="400">
</a>
</div>

<br><br>

- **Semantic Network Analysis (Interactive)** / **Word Cloud (Simple Image)**

<br>

<div align="center">
<a href="https://github.com/DevBruce/IDEA/blob/master/preview/sna_interactive.png">
<img src="https://github.com/DevBruce/IDEA/blob/master/preview/sna_interactive.png" width="400">
</a>
<a href="https://github.com/DevBruce/IDEA/blob/master/preview/wc.png">
<img src="https://github.com/DevBruce/IDEA/blob/master/preview/wc.png" width="400">
</a>
</div>

<br><br>

## Copyright

Copyright © 2018 by DevBruce \<<Bruce93k@gmail.com>\>  
Licensed under the GNU General Public License v3.0  

<br><br>

## Reference

See [NOTICE/README.md](https://github.com/DevBruce/IDEA/blob/master/NOTICE/README.md)
