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
sec_start = 28 # when to start video
num_secs = 15 # number of seconds of the video the program will use

camera_angles = np.array([(1.1781, 2.0944), (0.7875, 1.4), (0.7242, 1.3676), (0.93265875, 1.65806), (0.488, 0.6342)])


if __name__ == '__main__':
    speeds=[]

    camera_locations = [np.array([0,-3.4,0]),np.array([-5.6,0 ,0]),np.array([0,2.1,0])]

    n_pixels1, n_pixels2, n_pixels3 = 0 , 0 , 0

    video = cv2.VideoCapture('dronefootage2.mp4') #video file name
    video.set(cv2.CAP_PROP_POS_FRAMES, 38 * sec_start)
    fps_jump = 2 #basic FPS jump
    frames_counter = 0

    locations = []

    prev_frames, video = image_cut.image_cut(video, fps_jump)
    frames_counter += fps_jump

    object1locs=[]
    object2locs=[]
    object3locs=[]
    direction_vecs_history=[]
    my_tast_D = []
    while frames_counter < (num_secs * 30) :
        frames, video = image_cut.image_cut(video, fps_jump)

        if frames is None:
            break

        direction_vectors=[]

        new_direction_vec, n_pixels1, object1loc = video_to_vector.image_to_vector(frames[0], prev_frames[0],0)
        direction_vectors.append(new_direction_vec)#, video_to_vector.predicted_pixel(predicted_location, camera_angles[2]), expected_error))
        object1locs.append(object1loc)

        new_direction_vec, n_pixels2, object2loc = video_to_vector.image_to_vector(frames[1], prev_frames[1],1)
        # new_direction_vec = (turn_vectors.turn_vector(new_direction_vec, -0.0872665))
        direction_vectors.append(new_direction_vec)#, video_to_vector.predicted_pixel(predicted_location, camera_angles[3]), expected_error))
        object2locs.append(object2loc)

        new_direction_vec, n_pixels3, object3loc = video_to_vector.image_to_vector(frames[2], prev_frames[2],2)
        direction_vectors.append(new_direction_vec)#, video_to_vector.predicted_pixel(predicted_location, camera_angles[0]), expected_error))
        object3locs.append(object3loc)

        if frames_counter == 3:
            my_tast_D.append(direction_vectors)

        new_loc =calc_point.find_closest(camera_locations, direction_vectors)

        check=False
        for i in range(len(direction_vectors)):
            if distancefromline.distance_from_line(camera_locations[i], direction_vectors[i], new_loc)>3:
                check= True


        if new_loc is not None and not check:# and new_loc[0][2]<0:
            if direction_vectors[0] is not None and direction_vectors[1] is not None and direction_vectors[2] is not None:
                locations.append(new_loc[0] * np.array([-1, 1, -1]))
                direction_vecs_history.append(direction_vectors)


            if len(locations)>1:
                xy_speed = find_speed.find_xy_speed(locations[-1], locations[-2], 30/fps_jump)
                speeds.append(find_speed.find_speed(locations[-1], locations[-2], 30/fps_jump))
                object_pixel_num = max(n_pixels1, n_pixels2, n_pixels3)
                object_pixel_radius = object_pixel_num/(2*3.14)
                object_radius = (object_pixel_radius/ 1920)* new_loc[2] * math.tan(1.9)
                # print(f'r {object_radius}, xy {xy_speed}')
                fps_jump = abs(int(object_radius * 30 // xy_speed)) + 1
                # print(f'num frames left{video_length - frame_counter}')

        frames_counter += fps_jump
        prev_frames = frames
    print(len(direction_vecs_history))
    print(len(locations))
    #print(f' frame 6 {direction_vecs_history[4]}')
    x_data_1 = [object1locs[i][1] for i in range(len(object1locs))]
    y_data_1 = [object1locs[i][0] for i in range(len(object1locs))]
    plt.plot(x_data_1,y_data_1,'o',label= '1')

    x_data_2 = [object2locs[i][1] for i in range(len(object2locs))]
    y_data_2 = [object2locs[i][0] for i in range(len(object2locs))]
    plt.plot(x_data_2,y_data_2,'o', label = '2')


    x_data_3 = [object3locs[i][1] for i in range(len(object2locs))]
    y_data_3 = [object3locs[i][0] for i in range(len(object2locs))]
    plt.plot(x_data_3,y_data_3,'o', label ="3")


    plt.legend()
    plt.show()


    """best_vecs = np.array([[1,0,0],[0,1,0]])
    best_res = math.inf

    print("starting the big boy")
    for a in np.linspace(-0.99,0.99,6):
        print("a = " + str(a))
        for b in np.linspace(-0.99, 0.99, 6):
            print("b = " + str(b))
            for c in np.linspace(-0.99, 0.99, 6):
                print("c = " + str(c))
                cam_1_y_v = (a * b * c + np.sqrt(a ** 2 * b ** 2 * c ** 2 - (a ** 2) * (1 - a ** 2 - b **2 - c ** 2 - b ** 2 * c ** 2))) / (a ** 2 - 1)
                cam_1_z_u = np.sqrt(1 - a ** 2 - b **2)
                cam_1_z_v = np.sqrt(1 - a ** 2 - cam_1_y_v **2)

                u_hat_1 = np.array([[a, b, cam_1_z_u]])
                v_hat_1 = np.array([[c, cam_1_y_v, cam_1_z_v]])
                origin_1 = np.cross(u_hat_1, v_hat_1)
                for d in np.linspace(-0.99, 0.99, 6):
                    for e in np.linspace(-0.99, 0.99, 6):
                        for f in np.linspace(-0.99, 0.99, 6):
                            cam_2_y_v = (d * e * f + np.sqrt(d ** 2 * e ** 2 * f ** 2 - (d ** 2) * (
                                        1 - d ** 2 - e ** 2 - f ** 2 - e ** 2 * f ** 2))) / (d ** 2 - 1)
                            cam_2_z_u = np.sqrt(1 - d ** 2 - e ** 2)
                            cam_2_z_v = np.sqrt(1 - d ** 2 - cam_2_y_v ** 2)

                            u_hat_2 = np.array([[d, e, cam_2_z_u]])
                            v_hat_2 = np.array([[f, cam_2_y_v, cam_2_z_v]])
                            origin_2 = np.cross(u_hat_2, v_hat_2)
                            for g in np.linspace(-0.99, 0.99, 6):
                                for h in np.linspace(-0.99, 0.99, 6):
                                    for i in np.linspace(-0.99, 0.99, 6):
                                        cam_3_y_v = (g * i * c + np.sqrt(g ** 2 * i ** 2 * c ** 2 - (g ** 2) * (
                                                1 - g ** 2 - i ** 2 - c ** 2 - i ** 2 * c ** 2))) / (g ** 2 - 1)
                                        cam_3_z_u = np.sqrt(1 - g ** 2 - i ** 2)
                                        cam_3_z_v = np.sqrt(1 - g ** 2 - cam_3_y_v ** 2)

                                        u_hat_3 = np.array([[g, h, cam_3_z_u]])
                                        v_hat_3 = np.array([[i, cam_3_y_v, cam_3_z_v]])

                                        origin_3 = np.cross(u_hat_3, v_hat_3)

                                        real_x_1 = (x_data_1[4] - 1920 / 2) / (1920 / 2) * np.tan(camera_angles[1][1] / 2)
                                        real_y_1 = (y_data_1[4] - 1080 / 2) / (1080 / 2) * np.tan(camera_angles[1][0] / 2)
                                        x_vec_1 = u_hat_1 * real_x_1
                                        y_vec_1 = v_hat_1 * real_y_1
                                        D_1 = x_vec_1 + y_vec_1 + origin_1


                                        real_x_2 = (x_data_2[4] - 1920 / 2) / (1920 / 2) * np.tan(camera_angles[3][1] / 2)
                                        real_y_2 = (y_data_2[4] - 1080 / 2) / (1080 / 2) * np.tan(camera_angles[3][0] / 2)
                                        x_vec_2 = u_hat_2 * real_x_2
                                        y_vec_2 = v_hat_2 * real_y_2
                                        D_2 = x_vec_2 + y_vec_2 + origin_2


                                        real_x_3 = (x_data_3[4] - 1920 / 2) / (1920 / 2) * np.tan(camera_angles[0][1] / 2)
                                        real_y_3 = (y_data_3[4] - 1080 / 2) / (1080 / 2) * np.tan(camera_angles[0][0] / 2)
                                        x_vec_3 = u_hat_3 * real_x_3
                                        y_vec_3 = v_hat_3 * real_y_3
                                        D_3 = x_vec_3 + y_vec_3 + origin_3


                                        curr_res = calc_point.compute_projected_distance_sum(np.array([D_1,D_2,D_3]), camera_locations, calc_point.find_closest(np.array([D_1,D_2,D_3]), camera_locations))

                                        if curr_res < best_res:
                                            best_res = curr_res
                                            best_vecs = np.array([[u_hat_1, v_hat_1], [u_hat_2, v_hat_2], [u_hat_3, v_hat_3]])


    print(f'best vecs{best_vecs}')"""
    locations = np.array(locations)
    x_locations = [locations[i][1] for i in range (len(locations))]
    y_locations = [-locations[i][0] for i in range (len(locations))]
    z_locations = [locations[i][2] for i in range (len(locations))]
    print('real deal')
    print([(float(x_locations[i]), float(y_locations[i]), float(z_locations[i])) for i in range(len(locations))])
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






