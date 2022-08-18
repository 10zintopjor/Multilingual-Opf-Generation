from email.mime import base
from lib2to3.pytree import convert
from os import write
from requests import request
import requests
from openpecha.core.ids import get_base_id,get_initial_pecha_id
from datetime import datetime
from openpecha.core.layer import Layer, LayerEnum
from openpecha.core.pecha import OpenPechaFS 
from openpecha.core.metadata import InitialPechaMetadata,InitialCreationType
from bs4 import BeautifulSoup

from openpecha.core.annotation import AnnBase, Span
from uuid import uuid4
from pathlib import Path
from openpecha import github_utils,config
from zipfile import ZipFile
from pyewts import pyewts
import re
import logging

def create_opf(text,pecha_id):
    texts =text.splitlines()
    base_id = get_base_id()
    opf_path = f"{pecha_id}/{pecha_id}.opf"
    opf = OpenPechaFS(path =opf_path)
    bases = {f"{base_id}":text}
    layers = {f"{base_id}": {LayerEnum.segment: get_segment_layer(texts)}}
    meta = get_meta()
    opf.base = bases
    opf.save_base()
    opf.layers = layers
    opf.save_layers()
    opf._meta = meta
    opf.save_meta() 

    return base_id

def get_meta():
    instance_meta = InitialPechaMetadata(
            id=pecha_id,
            initial_creation_type=InitialCreationType.input,
            source_metadata={
                "title":"༄། །བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ་བཞུགས་སོ།",
                "language": "bo"
            })    
    return instance_meta        

def get_segment_layer(texts):
    segment_annotations = {}
    char_walker =0
    for base_text in texts:
        segment_annotation,char_walker = get_segment_annotation(char_walker,base_text)
        segment_annotations.update(segment_annotation)

    segment_layer = Layer(annotation_type= LayerEnum.segment,
    annotations=segment_annotations
    )        
    return segment_layer


def get_segment_annotation(char_walker,base_text):
    
    segment_annotation = {
        uuid4().hex:AnnBase(span=Span(start=char_walker, end=char_walker + len(base_text)))
    }

    return (segment_annotation,len(base_text)+1+char_walker)

def main():
    global pecha_id
    pecha_id = get_initial_pecha_id()
    text = Path("./tib_multilingual.txt").read_text()
    create_opf(text,pecha_id)

if __name__ == "__main__":
    main()

