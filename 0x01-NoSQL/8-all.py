#!/usr/bin/env python3
"""MongoDB"""
from pymongo import MongoClient


def list_all(mongo_collection):
    """List all documents in a MongoDB collection."""
    documents = mongo_collection.find()
    return list(documents) if documents else []
