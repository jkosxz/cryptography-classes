from googletrans import Translator
from caesar import cipher_caesar, decipher_caesar
from vigenere import generateKey, generateKey, originalText

import json
import random


def cipher_entry_caesar(filename_entry, filename_ciphered):
    """Takes list of entries to cipher; returns ciphered entries"""
    res = []
    json_file = json.load(open(filename_entry, 'r'))
    for entry in json_file['listOfEntries']:
        rng = random.randint(1, 26)
        res.append(cipher_caesar(entry, rng))

    return {'cypheredList': res}


def deciphering_caesar(ciphered_entries):
    """Takes list of ciphered entries and dumps into a file dictionary that contains ciphered text, deciphered text
    and shift number for Caesar method"""
    detector = Translator()
    decrypted_list = {'listOfDecryptedEntries': []}
    for entry in ciphered_entries['cypheredList']:
        shift = 0

        while True:
            entry_tested = decipher_caesar(entry, shift)

            ## if the Translator says that entered lang is English and is confident (1) then it is deciphered text
            if detector.detect(entry_tested).lang == 'en' and detector.detect(entry_tested).confidence == 1:
                decrypted_list['listOfDecryptedEntries'].append({'cipheredText': entry,
                                                                 'decipheredText': entry_tested,
                                                                 'numberOfShifts': shift})
                break
            else:
                pass
            shift += 1

    with open("files/result.json", "w") as outfile:
        outfile.write(json.dumps(decrypted_list, indent=1))


def main():
    ciphered_json = cipher_entry_caesar('files/entry.json', '')
    deciphering_caesar(ciphered_json)


if __name__ == '__main__':
    main()
