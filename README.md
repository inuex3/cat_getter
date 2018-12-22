# cat_getter
First. add permission.
in src
chmod +x cat_getter.py
Then 
roslaunch cat_getter cat_getter.launch
rosrun cat_getter cat_getter.py

you can see the image using image_view
rosrun image_view image_view image:=/neko
