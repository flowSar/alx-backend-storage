#!/usr/bin/env python3
"""MongoDB"""
from pymongo import MongoClient


def update_topics(mongo_collection, name, topics):
    """Updates the topics of a school document based on the name."""
    mongo_collection.update_one({"name": name}, {"$set": {"topics": topics}})
