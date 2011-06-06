#!/usr/bin/env python3
# tectonicus_cli.py
# Restores the old cli options that were removed in tectonius 2.00.
# We generate the xml on runtime and *maybe* cache it for later use.
# Also, we'll keep the default options of the older, sub-2.00 tectonicus.

import argparse
import xml.etree.ElementTree as etree

parser = argparse.ArgumentParser(
    description='''Command-line interface to the Tectoniucs map renderer.''',
    argument_default=''
    )

parser.add_argument(
    '--alphaBits',
    type=int,
    default=8,
    help='''alphaBits specifies how many bits are assigned to designate the alpha on the tiles of the map. It is recommended to use 0 (off) or 8 (full). However, Tectonicus passes the value directly to your graphics card, so you can theoretically pass any value your graphics card supports.'''
    )

parser.add_argument(
    '--bedsInitiallyVisible',
    type=bool,
    default=True,
    help='''Specifies whether or not bed markers are initially visible.'''
    )

parser.add_argument(
    '--cacheDir',
    type=str,
    help='''Specifies the directory to be used for caching. Caching is enabled by default, and the default directory location is a subdirectory within the output directory.'''
    )

parser.add_argument(
    '--cameraAngle',
    type=int,
    default=45,
    help='''This changes the orientation of north. The default setting of 45 produces an oblique view with north at the upper left of the map. 0 will give you north at the top; 90 will give you east at the top; and so on. As you increase this number imagine the map's cardinal directions rotating in a counter-clockwise direction.'''
    )

parser.add_argument(
    '--closestZoomSize',
    type=int,
    default=12,
    help='''Sets the closest zoom size. When zoomed-in all the way this value determines the area that will be visible in one of the rendered picture files. Increase [x] to "widen" the camera lens of this closest view.'''
    )

parser.add_argument(
    '--colorDepth',
    type=int,
    default=16,
    help='''Color Depth, like alpha bits, specifies how many bits are assigned to the colors in the tiles of the map. It is also passed directly to you graphics card, so you can pass any supported value. However, 24 ("millions of colors" or "truecolor"), or 16 ("thousands of colors"), is recommended.'''
    )

parser.add_argument(
    '--dimension',
    type=str,
    default='terra',
    choices=['terra', 'nether'],
    help='''Use along with --renderStyle=nether to render ther nether.'''
    )

parser.add_argument(
    '--eraseOutputDir',
    type=bool,
    default=False,
    help='''Specify 'True' to erase the entire output directory and render from scratch.'''
    )

parser.add_argument(
    '--imageCompressionLevel',
    type=int,
    default=0.95,
    help='''For jpeg renders only, specify a number between 1.0 and 0.1 to change the compression level. Defaults to 0.95.'''
    )

parser.add_argument(
    '--imageFormat',
    type=str,
    default='png',
    choices=['jpg', 'gif', 'png'],
    help='''Specifies the type of image to output to.'''
    )

parser.add_argument(
    '--lighting',
    type=str,
    default='day',
    choices=['none', 'night', 'day'],
    help='''Choose the lighting style to render with.'''
    )

parser.add_argument(
    '--logFile',
    type=str,
    default='TectonicusLog.txt',
    help='The file name to use for the log file.'
    )

parser.add_argument(
    '--minecraftJar',
    type=str,
    help='''The path to your client minecraft jar.'''
    )

parser.add_argument(
    '--maxTiles',
    type=int,
    default=-1,
    help='''This specialized argument is used only for troubleshooting. For example --maxTiles=100 will create a kind of "preview" map render consisting of only 100 base tiles (i.e. not the entire map).'''
    )

parser.add_argument(
    '--mode',
    type=str,
    default='cmd',
    choices=['cmd', 'gui', 'players'],
    help='''Selects the mode in which Tectonicus runs. --mode=players will not render a map but update the player locations.'''
    )

parser.add_argument(
    '--numDownsampleThreads',
    type=int,
    default=1,
    help='''Set to the number of cores you want to use for distributing the downsampling computing.'''
    )

parser.add_argument(
    '--numSamples',
    type=int,
    default=4,
    choices=list(range(5)),
    help='''Specifies the number of samples for antialiasing. Defaults to 4 (high quality). Setting ==numSamples=0 can sometimes eliminate problems with graphics cards that do not support anti-aliasing.'''
    )

parser.add_argument(
    '--numZoomLevels',
    type=int,
    default=8,
    help='''This defines how many zoom levels the resulting map will have.'''
    )

parser.add_argument(
    '--outputDir',
    type=str,
    help='''This specifies the directory you want the rendered map files to placed in.'''
    )

parser.add_argument(
    '--outputHtmlName',
    type=str,
    default='map.html',
    help='''Use this to change the name of the html file tectonicus outputs.'''
    )

parser.add_argument(
    '--playerFilterFile',
    type=str,
    help='''Specifies the whitelist or blacklist file for use with the --players argument.'''
    )

parser.add_argument(
    '--players',
    type=str,
    default='all',
    choices=['none', 'ops', 'blacklist', 'whitelist', 'all'],
    help='''Sets Tectonicus to render none, all, ops, or omit or include from a blacklist or a whitelist.'''
    )

parser.add_argument(
    '--playersInitiallyVisible',
    type=bool,
    default=True,
    help='''Determines if the players will be visible on initial loading of the map.'''
    )

parser.add_argument(
    '--portals',
    type=str,
    default='all',
    choices=['none', 'all'],
    help='''Determines if the portals will be visible on the map.'''
    )

parser.add_argument(
    '--portalsInitiallyVisible',
    type=bool,
    default=True,
    help='''Determines if the portals will be visible on initial loading of the map.'''
    )

parser.add_argument(
    '--renderStyle',
    type=str,
    default='regular',
    choices=['cave', 'nether', 'regular'],
    help='''Specifies the map type to render. Caves only, the nether (requires setting: --dimension=nether) or the regular world map.'''
    )

parser.add_argument(
    '--showSpawn',
    type=bool,
    default=True,
    help='''Specifies whether or not to show an icon for the spawn position.'''
    )

parser.add_argument(
    '--signs',
    type=str,
    default='special',
    choices=['none', 'all', 'special'],
    help='''Signs that use special characters !, -, = or ~ will be visible on the map as location markers. The text on these signs must begin and end with any of the listed special characters. For example a sign reading "-- Lookout point --" will appear as a location marker at all zoom levels. When clicked, the marker will pop up a tooltip bubble showing the full text of the sign. Setting --signs=all will make all signs into map markers regardless of the writing on the signs. Empty signs are always skipped since they are used for aesthetic purposes.'''
    )

parser.add_argument(
    '--signsInitiallyVisible',
    type=bool,
    default=True,
    help='''Determines if the signs will be visible on initial loading of the map.'''
    )

parser.add_argument(
    '--singlePlayerName',
    type=str,
    help='''Name to use when rendering single player world.'''
    )

parser.add_argument(
    '--spawnInitiallyVisible',
    type=bool,
    default=True,
    help='''etermines if the spawn point will be visible on initial loading of the map.'''
    )

parser.add_argument(
    '--texturePack',
    type=str,
    help='''Specify the location of a custom texturepack to use. Uses the standard textures located in minecraft.jar by default.'''
    )

parser.add_argument(
    '--tileSize',
    type=int,
    default=512,
    help='''Specifies the size of the output image tiles, in pixels. Minimum: 64 Maximum: 1024'''
    )

parser.add_argument(
    '--useBiomeColors',
    type=bool,
    default=False,
    help='''Set to use biome colours for grass and leaves. Use True or False.'''
    )

parser.add_argument(
    '--useCache',
    type=bool,
    default=True,
    help='''Enable or disable the use of the cache to speed up repeated map rendering.'''
    )

parser.add_argument(
    '--verbose',
    type=bool,
    default=False,
    help='''Set to True to print additional debug output during render.'''
    )

parser.add_argument(
    '--worldDir',
    type=str,
    help='''Path to your minecraft world directory.'''
    )

args = vars(parser.parse_args())

tectonicus = etree.Element('tectonicus', version='2')

etree.SubElement(tectonicus, 'config',
    mode=args['mode'],
    outputDir=args['outputDir'],
    outputHtmlName=args['outputHtmlName'],
    minecraftJar=args['minecraftJar'],
    texturePack=args['texturePack'],
    numZoomLevels=str(args['numZoomLevels']),
    singlePlayerName=args['singlePlayerName'],
    spawnInitiallyVisible=str(args['spawnInitiallyVisible']).lower(),
    playersInitiallyVisible=str(args['playersInitiallyVisible']).lower(),
    bedsInitiallyVisible=str(args['bedsInitiallyVisible']).lower(),
    signsInitiallyVisible=str(args['signsInitiallyVisible']).lower(),
    portalsInitiallyVisible=str(args['portalsInitiallyVisible']).lower(),
    numDownsampleThreads=str(args['numDownsampleThreads']),
    eraseOutputDir=str(args['eraseOutputDir']).lower(),
    useCache=str(args['useCache']).lower(),
    logFile=args['logFile']
    )

etree.SubElement(tectonicus, 'rasterizer',
    type='lwjgl',
    colorDepth=str(args['colorDepth']),
    alphaBits=str(args['alphaBits']),
    numSamples=str(args['numSamples']),
    tileSize=str(args['tileSize'])
    )

print(etree.tostring(tectonicus))