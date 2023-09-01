clear all, close all, clc

num = [0 0 2 11];
dem = [1 0 -4 19];

ft = tf(num,dem);
ft
[A, B, C, D] = tf2ss(ft)

