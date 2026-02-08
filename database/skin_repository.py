# -*- coding: utf-8 -*-

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)


def fetch_all_hashes():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT image_hash FROM skins")
            return [row[0] for row in cur.fetchall()]


def insert_skin(
    user_id: str,
    character_name: str,
    raca: str,
    image_url: str,
    image_hash: str,
    created_by: int
):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO skins
                (user_id, character_name, raca, imagem_url, image_hash, created_by)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                user_id,
                character_name,
                raca,
                image_url,
                image_hash,
                created_by
            ))
            conn.commit()
