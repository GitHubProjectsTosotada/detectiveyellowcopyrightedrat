#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Detective Yellowcopyrightedrat - A Telegram bot to organize Pokémon GO raids
# Copyright (C) 2017 Jorge Suárez de Lis <hey@gentakojima.me>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from supportmethods import parse_profile_image
import re
import os

passed_tests = failed_tests = 0

# Load test files
for root, dirs, filenames in os.walk("testingimgs"):
    for f in filenames:
        m = re.match(r'(Rojo|Amarillo|Azul)_([0-9]{2})_([A-Za-z0-9]{3,15})_([A-Za-z]{3,12})_([A-Za-z0-9]{3,12})\.jpg', f)
        if m == None:
            print("[!] Ignoring file %s..." % f)
        else:
            print("[*] Testing file %s..." % f)

            expected_color = m.group(1)
            expected_level = m.group(2)
            expected_trainer_name = m.group(3)
            expected_pokemon = m.group(4)
            expected_pokemon_name = m.group(5)

            (trainer_name, level, chosen_color, chosen_pokemon, pokemon_name, chosen_profile) = parse_profile_image(os.path.join(root, f), expected_pokemon)

            try:
                assert chosen_color == expected_color
                passed_tests = passed_tests + 1
            except AssertionError as e:
                print(" [!] Incorrect team! '%s' vs. expected '%s'" % (chosen_color, expected_color))
                failed_tests = failed_tests + 1
            try:
                assert level == expected_level
                passed_tests = passed_tests + 1
            except AssertionError as e:
                print(" [!] Incorrect level! '%s' vs. expected '%s'" % (level, expected_level))
                failed_tests = failed_tests + 1
            try:
                assert trainer_name.lower() == expected_trainer_name.lower()
                passed_tests = passed_tests + 1
            except AssertionError as e:
                print(" [!] Incorrect trainer name! '%s' vs. expected '%s'" % (trainer_name, expected_trainer_name))
                failed_tests = failed_tests + 1
            try:
                assert chosen_pokemon == expected_pokemon
                passed_tests = passed_tests + 1
            except AssertionError as e:
                print(" [!] Incorrect Pokémon! '%s' vs. expected '%s'" % (chosen_pokemon, expected_pokemon))
                failed_tests = failed_tests + 1
            try:
                assert pokemon_name.lower() == expected_pokemon_name.lower()
                passed_tests = passed_tests + 1
            except AssertionError as e:
                print(" [!] Incorrect Pokémon name! '%s' vs. expected '%s'" % (pokemon_name, expected_pokemon_name))
                failed_tests = failed_tests + 1
            try:
                assert chosen_profile != None
                passed_tests = passed_tests + 1
            except AssertionError as e:
                print(" [!] Incorrect Profile model! No match at all!")
                failed_tests = failed_tests + 1

print("Passed tests: %s" % passed_tests)
print("Failed tests: %s" % failed_tests)
