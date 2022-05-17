# Compatibility with Python 2.7.
from __future__ import print_function

import argparse
import os
import shutil
from subprocess import CalledProcessError
import zipfile
import time
import json
import io

import boto3
import botocore.exceptions

from converter import parse_vray_text
from renderer import sdk_render

preview_bucket = 'aws-vray-preview'
scenes_bucket = 'aws-vray-scenes'
creation_timeout = 30
rendering_tries = 6

class ActionType:
    RENDER = "RENDER"
    CONVERT = "CONVERT"
    DEFAULT = "DEFAULT"


def send_to_aws(config_asset, file, bucket, is_public):
    s3 = boto3.client('s3')
    temp_prefix = parse_vray_text.temp_prefix
    image_filename = os.path.join(config_asset['input_folder'], file)
    prefix = config_asset['input_folder'].split(temp_prefix)[-1] + "/" + file
    s3.upload_file(image_filename, bucket, prefix, ExtraArgs={'ACL': 'public-read'} if is_public else None)
    url = 'https://aws-vray-preview.s3-eu-west-1.amazonaws.com/' + prefix
    return url


def download_config(config, bucket):
    print("Trying to get a copy from AWS S3")
    file = 'config_asset.zip'
    temp_prefix = parse_vray_text.temp_prefix
    input_folder = parse_vray_text.generate_input_folder_path(config)
    os.makedirs(os.path.join(temp_prefix, input_folder), exist_ok=True)
    key = input_folder + "/" + file
    downloaded_path = os.path.join(temp_prefix, input_folder, file)
    return get_and_unzip_from_aws(key=key, downloaded_path=downloaded_path, bucket=bucket)


def get_and_unzip_from_aws(key, downloaded_path, bucket):
    s3 = boto3.client('s3')
    try:
        s3.download_file(bucket, key, downloaded_path)
        if downloaded_path.lower().endswith('.zip'):
            with zipfile.ZipFile(downloaded_path, 'r') as dzip:
                dzip.extractall(path=os.path.dirname(downloaded_path))
        return True
    except botocore.exceptions.ClientError as e:
        print('ERROR: {}.'.format(str(e)))
        print('key: {}'.format(key))
        print('downloaded_path: {}'.format(downloaded_path))
        print('bucket: {}'.format(bucket))
        return False
    except Exception as e:
        print('ERROR: {}.'.format(str(e)))
        return False


def get_template(config_asset, template='preview_2018'):
    input_folder = config_asset['input_folder']

    os.makedirs(os.path.join(input_folder, 'template'), exist_ok=True)

    if not os.path.exists(os.path.join(config_asset['input_folder'], 'template', 'props.json')):
        zipped_template = "{}.zip".format(template)
        get_and_unzip_from_aws(key=zipped_template, downloaded_path=os.path.join(input_folder, 'template', zipped_template), bucket='aws-vray-templates')
        os.remove(os.path.join(input_folder, 'template', zipped_template))


def convert_config(config, force_cache=False, aws_support=True):
# If we already have a copy of the asset
    config_asset = parse_vray_text.get_config_asset(config)
    if not config_asset or force_cache:
        if aws_support:
            # Try to get a copy in AWS S3
            zip_exists = download_config(config, scenes_bucket)
        else:
            zip_exists = False
        # We convert the scene from scratch
        if not zip_exists:
            print("Copy does not exist, creating new one")
            parse_vray_text.get_data_from_config(config)
            config_asset = parse_vray_text.create_asset_json_from_config(config)
            parse_vray_text.zip_config_asset_folder(config_asset)
            if aws_support:
                send_to_aws(config_asset, file='config_asset.zip', bucket=scenes_bucket, is_public=False)


def render_config(config, output, debug=False, force_cache=False):
    config_asset = parse_vray_text.get_config_asset(config)
    if config_asset:

        rotations = config['rotations'] if 'rotations' in config and config['rotations'] else None
        resolution = config['resolution'] if 'resolution' in config else None
        zoom = config['zoom'] if 'zoom' in config else None
        template = config['template'] if 'template' in config else 'preview_2018'
        region = config['region'] if 'region' in config else None
        input_folder = config_asset['input_folder']

        os.makedirs(os.path.join(input_folder, 'template'), exist_ok=True)

        if not os.path.exists(os.path.join(config_asset['input_folder'], 'template', 'props.json')):
            zipped_template = "{}.zip".format(template)
            get_and_unzip_from_aws(key=zipped_template, downloaded_path=os.path.join(input_folder, 'template', zipped_template), bucket='aws-vray-templates')
            os.remove(os.path.join(input_folder, 'template', zipped_template))

        if os.path.exists(os.path.join(input_folder, 'config_asset.zip')):
            os.remove(os.path.join(input_folder, 'config_asset.zip'))

        with io.open(os.path.join(config_asset['input_folder'], 'template', 'props.json'), 'r') as f:
            template_props = json.load(f)

        for rotation in rotations:
            print("Rendering model")
            if region and len(region) == 4:
                region_format = '.{}_{}-{}_{}'.format(region[0], region[1], region[2], region[3])
            else:
                region_format = ''
            prefix = 'output_{}_{}-{}_{}{}'.format(
                int(rotation[0]), int(rotation[1]),
                int(resolution[0]), int(resolution[1]),
                region_format
            )
            prefix_without_region = 'output_{}_{}-{}_{}'.format(
                int(rotation[0]), int(rotation[1]),
                int(resolution[0]), int(resolution[1])
            )

            vrscene_filename = os.path.join(config_asset['input_folder'], 'template', '{}.vrscene'.format(prefix))
            image_filename = os.path.join(config_asset['input_folder'], '{}.jpg'.format(prefix))

            nb_iter = 0
            while nb_iter <= creation_timeout:
                try:
                    efs_vrscene_path = os.path.join(
                        config_asset['input_folder'].replace(parse_vray_text.temp_prefix, '/mnt/vray/'),
                        template_props['name'], '{}.vrscene'.format(prefix_without_region)
                    )
                    if os.path.exists(efs_vrscene_path) and not force_cache:
                        shutil.copy(efs_vrscene_path, vrscene_filename)
                    else:
                        print("Creating vrscene file")
                        sdk_render.create_vrscene(config_asset, accessories, output_name=vrscene_filename, rotation=rotation, resolution=resolution, zoom=zoom, template_props=template_props)
                        os.makedirs(os.path.dirname(efs_vrscene_path), exist_ok=True)
                        if not (force_cache or debug):
                            shutil.copy(vrscene_filename, efs_vrscene_path)
                except RuntimeError as e:
                    if nb_iter == creation_timeout:
                        raise e
                    else:
                        time.sleep(1)
                        nb_iter = nb_iter + 1
                else:
                    nb_iter = creation_timeout + 1
            nb_iter = 0

            try:
                camera = template_props.get('camera_name', None)
                sdk_render.render_vrscene(vrscene_file=vrscene_filename, output_image=image_filename, camera=camera, debug=debug, region=region)
            except CalledProcessError as e:
                raise e
            else:
                if os.path.exists(image_filename):
                    output['path'] = image_filename

    else:
        raise Exception("Config asset does not exist. You need to convert your furniture it first")


def convert_batches(batches, force_cache=False, aws_support=True):
    for config in batches:
        convert_config(config, force_cache, aws_support)


def render_batches(batches, output, debug=False, force_cache=False):
    output['images'] = list()
    for config in batches:
        render_config(config, output, debug, force_cache)
        output['images'].append(output)


def launch(config, output=None, debug=False, local=False, action=ActionType.DEFAULT):
    force_cache = local
    aws_support = not local
    if debug:
        print("===== DEBUG MODE =====")
    if output is None:
        output = dict()

    if action in [ActionType.CONVERT, ActionType.DEFAULT]:
        convert_config(config, force_cache=force_cache, aws_support=aws_support)
    else:
        download_config(config, bucket=scenes_bucket)
    if action in [ActionType.RENDER, ActionType.DEFAULT]:
        render_config(config, output, debug, force_cache=force_cache)


def cli_run():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', help='Catalog ID')
    parser.add_argument('-ref', help='Reference of the furniture')
    parser.add_argument('-id', help='Configuration ID')
    parser.add_argument('-mail', help='Email for sending URLs')
    parser.add_argument('-rot', nargs='+', help='Rotations for rendering', type=float)
    parser.add_argument('-res', nargs='+', help='Resolution of the rendered image', type=int)
    parser.add_argument('-zoom', help='Zoom of the render view', type=float)
    parser.add_argument('-template', help='Template used for the rendering')
    parser.add_argument('-region', nargs='+', help="Region to render", type=int)
    parser.add_argument('-d', help='Debug mode', action="store_true")
    parser.add_argument('-l', help="Local mode", action="store_true")
    parser.add_argument('-a', help="Action")
    args = parser.parse_args()
    rotations_list = args.rot
    resolution = None if not args.res else (int(args.res[0]), int(args.res[0])) if len(args.res) == 1 else (int(args.res[0]), int(args.res[1]))
    zoom = None if not args.zoom else float(args.zoom)
    template = args.template if args.template else None
    region = args.region if args.region else None
    debug = args.d
    local = args.l
    action = args.a if args.a else ActionType.DEFAULT

    input_config = None

    if args.c:
        print("Catalog ID = {}".format(args.c))
    if args.ref:
        print("Reference = {}".format(args.ref))
    if args.id:
        print("Configuration ID = {}".format(args.id))
    if args.res:
        print("Resolution = {}".format(args.res))
    if args.rot:
        print("Rotations = {}".format(args.rot))
    if args.zoom:
        print("Zoom = {}".format(zoom))
    if args.template:
        print("Template = {}".format(args.template))
    if args.region:
        print("Region = {}".format(args.region))
    if args.a:
        print("Action = {}".format(args.a))
    if args.c and (args.ref or args.id):
        catalog_id = args.c
        if args.id:
            config_id = args.id
            reference = config_id.split('|')[0]
        if args.ref:
            reference = args.ref
            config_id = reference
        input_config = parse_vray_text.generate_config(
            catalog_id=catalog_id, reference=reference, config_id=config_id,
            rotations=rotations_list, resolution=resolution, zoom=zoom, template=template, region=region
        )


    if input_config:
        launch(input_config, debug=debug, local=local, action=action)

    else:
        print("You need to set at least one config")
        parser.print_help()


if __name__ == '__main__':
    cli_run()
