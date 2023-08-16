import asyncio
import boto3
import csv
import datetime
import json
import logging
import moto
import os
import requests
from landsatxplore.api import API
from landsatxplore.earthexplorer import EarthExplorer
from botocore.exceptions import ClientError


env_var = os.environ

api = API(env_var.get("LC8_USERNAME", ""), env_var.get("LC8_PASSWORD", ""))
earth_api_url = env_var.get("NASA_EARTH_API_URL", "https://api.nasa.gov/planetary/earth/imagery")
earth_api_key = env_var.get("NASA_EARTH_API_KEY", "")
storage_folder = "./lt_json_files/"
bucket_name = env_var.get("BUCKET_NAME", "")


@moto.mock_s3
async def save_data(field_id, date, image_data):
    s3_conn = boto3.client("s3", region_name="us-east-1")
    try:
        response = s3_conn.upload_file(image_data, bucket_name, f"{field_id}/{date}/_imagery.png")
        return response
    except ClientError as e:
        logging.error(e)
        return False


async def get_timely_data(start_date, end_date):
    __start = datetime.datetime.now()
    response = api.search(
        dataset='landsat_ot_c2_l2',
        start_date=start_date,
        end_date=end_date,
        max_cloud_cover=10
    )
    print(f"{len(response)} scenes found.")

    if len(response) > 0:
        ee = EarthExplorer(env_var.get("LC8_EE_USERNAME", ""), env_var.get("LC8_EE_PASSWORD", ""))
        # Process the result
        for scene in response:
            # print(scene['acquisition_date'].strftime('%Y-%m-%d'))
            # Write scene footprints to disk
            # Code Template for downloading polygon data to local folder:
            # fname = f"{scene['landsat_product_id']}.geojson"
            # with open(storage_folder + fname, "w") as f:
            #    json.dump(scene['spatial_coverage'].__geo_interface__, f)
            # Code to use scenes to download imagery data using EE API
            await save_data(scene["field_id"], start_date, open(ee.download(scene["field_id"], "./data"), "r"))

        ee.logout()

        __end = datetime.datetime.now()
        print("Time: ", __end - __start)

    return response


async def get_earth_api_images(field_id, date, lat, long, dim):
    response = requests.get(
        url=earth_api_url,
        params={
            "lat": lat,
            "lon": long,
            "dim": dim,
            "date": date,
            "api_key": earth_api_key,
        }
    )
    print(response.url)
    print(response.status_code)
    if len(response.content) > 0:
        for key, value in response:
            with open(f"image-{date}.png", "wb") as f:
                f.write(requests.get(value).content)
                await save_data(field_id, date, os.path.basename(f.name))
        return "Connection to S3 successful..."

    return "There was an error"

with open("places.csv", "r") as f:
    csv_read = csv.reader(f, delimiter=',')
    for row in csv_read:
        # Code for explicit new API usage
        asyncio.run(get_timely_data("2000-01-01", "2000-01-01"))
        # Template for NASA API
        # asyncio.run(get_earth_api_images(row[0], row[1], row[2], row[3], row[4]))
