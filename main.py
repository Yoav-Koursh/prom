import copy
from itertools import zip_longest

import cv2
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

import calc_point
import detect_type
import distancefromline
import find_speed
import image_cut
import moving_avg
import turn_vectors
import video_to_vector
import math
import matplotlib.pyplot as plt
desired_fps = 15
sec_start = 42 # when to start video
num_secs = 0.5 # number of seconds of the video the program will use

basic_expected_error = 1000
if __name__ == '__main__':
    speeds=[]
    camera_locations = [np.array([0,-3.4,0]),np.array([-5.6,0 ,0]),np.array([0,2.1,0])]
    n_pixels1, n_pixels2, n_pixels3 = 0 , 0 , 0
    video = cv2.VideoCapture('dronefootage2.mp4') #video file name
    locations = []
    fps_jump = 10 #basic FPS jump
    frames_counter = 0
    video.set(cv2.CAP_PROP_POS_FRAMES, 30 * sec_start)
    prev_frames, video = image_cut.image_cut(video, fps_jump)
    frames_counter += fps_jump
    object1locs=[]
    object2locs=[]
    object3locs=[]
    direction_vecs_history=[]
    while frames_counter<(num_secs * 30) :
        if frames_counter % 10 ==0:
            print('.' ,end='')
        frames, video = image_cut.image_cut(video, fps_jump)
        if frames is None:
            break
        direction_vectors=[]
        new_direction_vec, n_pixels1, object1loc = video_to_vector.image_to_vector(frames[0], prev_frames[0],1)
        direction_vectors.append(new_direction_vec)#, video_to_vector.predicted_pixel(predicted_location, camera_angles[2]), expected_error))
        new_direction_vec, n_pixels2, object2loc = video_to_vector.image_to_vector(frames[1], prev_frames[1],3)
        new_direction_vec = (turn_vectors.turn_vector(new_direction_vec, -0.0872665))
        direction_vectors.append(new_direction_vec)#, video_to_vector.predicted_pixel(predicted_location, camera_angles[3]), expected_error))
        new_direction_vec, n_pixels3, object3loc = video_to_vector.image_to_vector(frames[2], prev_frames[2],0)
        direction_vectors.append(new_direction_vec)#, video_to_vector.predicted_pixel(predicted_location, camera_angles[0]), expected_error))
        new_loc =calc_point.find_closest(camera_locations,direction_vectors )
        check=False
        for i in range(len(direction_vectors)):
            if distancefromline.distance_from_line(camera_locations[i], direction_vectors[i], new_loc)>3:
                check= True
        if new_loc is not None and not check:# and new_loc[0][2]<0:
            locations.append(new_loc[0]*np.array([-1,1,-1]))
            # if direction_vectors[0] is not None and direction_vectors[1] is not None and direction_vectors[2] is not None:
            #     direction_vecs_history.append(direction_vectors)

            if len(locations)>1:
                xy_speed = find_speed.find_xy_speed(locations[-1], locations[-2], 30/fps_jump)
                speeds.append(find_speed.find_speed(locations[-1], locations[-2], 30/fps_jump))
                object_pixel_num = max(n_pixels1, n_pixels2, n_pixels3)
                object_pixel_radius = object_pixel_num/(2*3.14)
                object_radius = (object_pixel_radius/ 1920)* new_loc[0][2] * math.tan(1.9)
                print(f'r {object_radius}, xy {xy_speed}')
                fps_jump = abs(int(object_radius * 30 // xy_speed)) + 1
                # print(f'num frames left{video_length - frame_counter}')

        frames_counter += fps_jump
        prev_frames = frames

    x_data = [object1locs[i][1] for i in range(len(object1locs))]
    y_data = [object1locs[i][0] for i in range(len(object1locs))]
    plt.plot(x_data,y_data,'o',label= '1')
    x_data = [object2locs[i][1] for i in range(len(object2locs))]
    y_data = [object2locs[i][0] for i in range(len(object2locs))]
    plt.plot(x_data,y_data,'o', label = '2')
    x_data = [object3locs[i][1] for i in range(len(object2locs))]
    y_data = [object3locs[i][0] for i in range(len(object2locs))]
    plt.plot(x_data,y_data,'o', label ="3")
    plt.legend()
    plt.show()

    locations = np.array(locations)
    x_locations = [locations[i][1] for i in range (len(locations))]
    y_locations = [-locations[i][0] for i in range (len(locations))]
    z_locations = [locations[i][2] for i in range (len(locations))]
    print('real deal')
    print([(float(x_locations[i]), float(y_locations[i]), float(z_locations[i])) for i in range(len(locations))])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(f' object is {detect_type.detect(speeds, locations)}')
    # print([[f'({camera_locations[i][0]},{camera_locations[i][1]},{camera_locations[i][2]}) + t*({direction_vecs_history[j][i]})' for i in range(2)]for j in range(len(direction_vecs_history))])
    # long_ass_String = '['
    # for i in range(len(direction_vecs_history)):
    #     long_ass_String += f', (-3.4,0,0)+ t* (-{direction_vecs_history[i][0][1]}, -{direction_vecs_history[i][0][0]} ,{direction_vecs_history[i][0][2]})'
    # print(long_ass_String+']')
    #
    # long_ass_String = '['
    # for i in range(len(direction_vecs_history)):
    #     long_ass_String += f', (0,-5.6,0)+ t* (-{direction_vecs_history[i][1][1]}, -{direction_vecs_history[i][1][0]} ,{direction_vecs_history[i][1][2]})'
    # print(long_ass_String+']')
    #
    # long_ass_String = '['
    # for i in range(len(direction_vecs_history)):
    #     long_ass_String += f', (2.1,0,0) +t* (-{direction_vecs_history[i][2][1]}, -{direction_vecs_history[i][2][0]} ,{direction_vecs_history[i][2][2]})'
    # print(long_ass_String+']')

    # plt.plot(x_locations, y_locations, 'o')
    # plt.show()
    # plt.plot (z_locations, 'o')
    # plt.show()
    cv2.waitKey(0)
    cv2.destroyAllWindows()






