#!/usr/bin/env python3
# coding=utf-8
"""
Retrieve data from netCDF4 files and store it into objects
"""
from collections import namedtuple
from datetime import datetime

__author__ = 'Lorenzo'

from src.xco2 import Xco2

OCOpoint = namedtuple(
    'OCOpoint',
    ['timestamp', 'xco2', 'latitude', 'longitude']
)


def createOCOpoint(**data):
    """Take numpy data for each point and create a namedtuple"""
    # #todo: take a look to Python ctypes library
    # from ctypes import *
    # class Point(Structure):
    #     _fields_ = [
    #         ("latitude", c_float),
    #         ("longitude", c_float),
    #         ('xco2', c_float),
    #         ('timestamp', c_wchar_p)  # Py type: str or None
    #     ]
    #

    return OCOpoint(
        latitude=data['latitude'],
        longitude=data['longitude'],
        timestamp=datetime(*map(int, data['date'])),
        xco2=float(data['xco2'])
    )


def create_generator_from_dataset(ds, rng=None):
    """
    Each file contains 30000+ relevations, loop over them and create a generator.

    :param nc4.Dataset ds:
    :param int rng:
    :return:
    """
    rng = len(ds['latitude']) if not rng else rng
    return (
        createOCOpoint(**{
            'latitude': round(ds['latitude'][i], 6),
            'longitude': round(ds['longitude'][i], 6),
            'xco2': ds['xco2'][i],
            'date': ds['date'][i],
        }) for i in range(rng))


def bulk_dump(session, objs_generator):
    """
    Dump in the database big amounts of objects from a generator.

    :param Session session:
    :param iter objs_generator:
    """
    while True:
        try:
            obj = next(objs_generator)
            new = Xco2(
                xco2=obj.xco2,
                timestamp=obj.timestamp,
                coordinates=Xco2.shape_geography(
                    obj.latitude,  obj.longitude),
                pixels=Xco2.shape_geometry(
                    obj.latitude, obj.longitude)
            )
            session.add(new)
            session.commit()
        except StopIteration:
            return
        except Exception as e:
            raise e

def return_hdf_groups(ds):
    """
    Return HDF% groups in the dataset
    :param nc4.Dataset ds:
    :return: tuple of strings
    """
    def walk_tree(top):
        values = top.groups.values()
        yield values
        for value in top.groups.values():
            for children in walk_tree(value):
                yield children

    # print('GROUPS \n')
    groups = []
    for children in walk_tree(ds):
        for child in children:
            groups.append(child)
    return tuple(groups)


def return_data_format(ds):
    """
    Return format of the netCDF
    :param nc4.Dataset ds:
    :return: str
    """
    return ds.data_model


def return_dimensions(ds):
    """
    Return HDF5 dimensions in the dataset
    :param nc4.Dataset ds:
    :return: OrderedDict
    """
    # print('DIMENSIONS \n')
    return ds.dimensions


def return_variables(ds):
    """
    Return HDF5 variables in the dataset
    :param nc4.Dataset ds:
    :return: OrderedDict
    """
    return ds.variables


def return_attributes(ds):
    """
    Return HDF5 attributes in the dataset
    :param nc4.Dataset ds:
    :return: tuple
    """
    return tuple(
        [
            (name, getattr(ds, name))
            for name in ds.ncattrs()
        ]
    )


def return_variable_doc(ds, var):
    """
    Return documentation for a variable
    :param Dataset ds
    :param str var:
    :return: str
    """
    return ds[var].__dict__




