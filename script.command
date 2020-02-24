#!/bin/bash
cd ~
[ ! -d "play" ] && mkdir -p "play"
cd play
[ ! -d "options-python" ] && git clone https://github.com/danmaxdanilov/options-python.git
cd options-python
git fetch origin
git reset --hard origin/master

## copy chromedriver
cp -rf chromedriver /usr/local/bin/chromedriver

## run main app
cd ~/play/options-python
chmod +x simpletest.py
export PYTHON_UTILS="~/play/options-python"
export PATH="$PYTHON_UTILS:$PATH"
python3 simpletest.py

## copy files
cd ~
[ ! -d "Desktop/Опционы" ] && mkdir -p "Desktop/Опционы"
option_dir=$(date +'%d-%m-%Y')
[ ! -d "Desktop/Опционы/${option_dir}" ] && mkdir -p "Desktop/Опционы/${option_dir}"
output_dir=$(~/Desktop/Опционы/${option_dir})
echo $output_dir
cd ~/play/options-python
cp -v *.png ~/Desktop/Опционы/$option_dir
#find ./ -name '*.png' -exec cp -prfv '{}' '${output_dir}' ';'
