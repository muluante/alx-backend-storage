#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""
import redis
import requests


def get_page(url: str) -> str:
    """obtains the HTML content of a URL and returns it"""
    redis_client = redis.Redis()
    count_key = f"count:{url}"

    if redis_client.exists(count_key):
        redis_client.incr(count_key)
        return redis_client.get(url).decode()

    response = requests.get(url)
    html_content = response.text

    redis_client.set(url, html_content, ex=10)

    redis_client.set(count_key, 1)

    return html_content
