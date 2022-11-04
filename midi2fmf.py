from mido import MidiFile
import sys
import math

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
OCTAVES = list(range(11))
NOTES_IN_OCTAVE = len(NOTES)


def number_to_note(number: int) -> tuple:
    return NOTES[number % NOTES_IN_OCTAVE], number // NOTES_IN_OCTAVE


def get_format(bmp):
    format = """Filetype: Flipper Music Format
Version: 0
BPM: """ + str(bmp) + """
Duration: 12
Octave: 5
Notes: """
    return format


def convert_file(file_name: str, output_file_name: str, bpm: int):
    mid = MidiFile(file_name, clip=True)
    notes = ""

    for msg in mid:
        msg_dict = msg.dict()

        if msg_dict["type"] == "set_tempo":
            bpm = math.floor(60000000 / msg_dict["tempo"])

        if msg_dict["type"] == "note_on":
            pause = str(round(3 / msg_dict["time"] if msg_dict["time"] else 1))
            notes = notes + pause + "P, "

        if msg_dict["type"] == "note_off":
            pause = str(round(3 / msg_dict["time"] if msg_dict["time"] else 1))
            note = number_to_note(msg_dict["note"])

            notes = notes + pause + note[0] + str(note[1]) + ", "

    notes = notes[:-2]

    with open(output_file_name, "w") as file:
        file.write(get_format(bpm) + notes)


def get_args_from_drag_drop(args):
    file_name = args[1]
    # remove windows full path
    file_name = file_name.split("\\")[-1]
    output_file_name = args[1].split(".")[0] + ".fmf"
    bpm = 130
    return file_name, output_file_name, bpm


def get_args_from_command_line():
    file_name = input("Enter file name: ")
    output_file_name = input("Enter output file name: ")
    bpm = int(input("Enter BPM: "))
    return file_name, output_file_name, bpm


def main():
    if len(sys.argv) > 1:
        file_name, output_file_name, bpm = get_args_from_drag_drop(sys.argv)
    else:
        file_name, output_file_name, bpm = get_args_from_command_line()

    convert_file(file_name, output_file_name, bpm)


main()
