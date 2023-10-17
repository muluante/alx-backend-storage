#!/usr/bin/env python3
""" A py script that provides stats about Nginx logs stored in MongoDB """
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    all_docs = nginx_collection.count_documents({})
    get_m = nginx_collection.count_documents({"method": "GET"})
    post_m = nginx_collection.count_documents({"method": "POST"})
    put_m = nginx_collection.count_documents({"method": "PUT"})
    patch_m = nginx_collection.count_documents({"method": "PATCH"})
    delete_m = nginx_collection.count_documents({"method": "DELETE"})
    get_path = nginx_collection.count_documents(
            {"method": "GET", "path": "/status"})

    print(f"{all_docs} logs")
    print("Methods:")
    print(f"\tmethod GET: {get_m}")
    print(f"\tmethod POST: {post_m}")
    print(f"\tmethod PUT: {put_m}")
    print(f"\tmethod PATCH: {patch_m}")
    print(f"\tmethod DELETE: {delete_m}")
    print(f"{get_path} status check")
