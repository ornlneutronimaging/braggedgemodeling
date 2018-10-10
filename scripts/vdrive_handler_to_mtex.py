import argparse

from bem.texture.preparation.vdrive_handler import VDriveHandler
from bem.texture.preparation.vdrive_to_mtex import VDriveToMtex

parser = argparse.ArgumentParser(description='VDrive File Handler')
parser.add_argument('-i', '--input', help='VDrive file', type=str)
parser.add_argument('-io', '--intermediate_output', help='Intermediate Output File', type=str)
parser.add_argument('-o', '--output', help='Mtex Output File', type=str)

def vdrive_handler_to_mtex():

    args = parser.parse_args()

    o_vdrive = VDriveHandler(filename = args.input)
    o_vdrive.run()
    o_vdrive.export(filename = args.intermediate_output)

    o_handler = VDriveToMtex(filename = args.intermediate_output)
    o_handler.run()
    o_handler.export(filename = args.output)

if __name__ == "__main__":
    vdrive_handler_to_mtex()