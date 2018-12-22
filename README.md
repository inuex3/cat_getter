# cat_getter
First. add permission.
in src
chmod +x cat_getter.py
Next, chenge video_stream_provider to your video in cat_getter.launch
<arg name="video_stream_provider" value="" />
Then 
roslaunch cat_getter cat_getter.launch
rosrun cat_getter cat_getter.py

you can see the image using image_view
rosrun image_view image_view image:=/neko
