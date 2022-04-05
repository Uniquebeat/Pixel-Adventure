from csv import reader
from os import walk
import pygame


def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        layout = reader(map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path):
    surface_list = []
    for _, __, img_files in walk(path):
        for img in img_files:
            full_path = path + '/' + img
            surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(surface)
    return surface_list
