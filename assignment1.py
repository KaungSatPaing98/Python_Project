""" Travel Tracker Assignment 1

Created by Kaung Sat Paing, 21 April 2023
URL - https://github.com/JCUS-CP1404/cp1404--travel-tracker---assignment-1-KaungSatPaing98

"""

import random
from operator import itemgetter

FILENAME = "places.csv"
MENU = """Menu:
L - List places
R - Recommend random place
A - Add new place
M - Mark a place as visited
Q - Quit"""


def main():
    """Allow users to track places they want to travel and already travel."""
    print("Travel Tracker 1.0 - by Kaung Sat Paing")
    places_file = open(FILENAME)
    places = read_data(places_file)
    visited_places = list_visited_places(places)
    unvisited_places = list_unvisited_places(places)
    print("{} places loaded from {}".format(len(places), FILENAME))
    print(MENU)

    choice = input(">>> ").lower()
    while choice != 'q':

        if choice == 'l':
            list_places(places, visited_places, unvisited_places)
        elif choice == 'r':
            random_places(places)
        elif choice == 'a':
            add_place(places, unvisited_places)
        elif choice == 'm':
            mark_places(places, visited_places, unvisited_places)
        else:
            print("Invalid menu choice")

        print(MENU)
        choice = input(">>> ").lower()

    places_file.close()
    print(f"{len(places)} places saved to {FILENAME}")
    print("Have a nice day :)")
    save_to_file(places)


def read_data(file):
    """Read the data form places.csv file."""
    places = []
    for each_line in file:
        each_line = each_line.strip()  # remove unnecessary white spaces
        places_details = each_line.split(",")  # split and put into the list
        places.append(places_details)
    return places


def sort_places(unvisited_places, visited_places):
    """ Sorted places for unvisited and visited places"""
    for unvisited_place in unvisited_places:
        unvisited_place[2] = int(unvisited_place[2])
    unvisited_places.sort(key=itemgetter(2))
    for visited_place in visited_places:
        visited_place[2] = int(visited_place[2])
    visited_places.sort(key=itemgetter(2))


def list_visited_places(places):
    """ List places for visited places"""
    visited_places = []
    for visited_place in places:
        if visited_place[3] == "v":
            visited_places.append(visited_place)
    return visited_places


def list_unvisited_places(places):
    """ List places for unvisited places"""
    unvisited_places = []
    for unvisited_place in places:
        if unvisited_place[3] == "n":
            unvisited_places.append(unvisited_place)
    return unvisited_places


def list_places(places, visited_places, unvisited_places):
    """ Display formatted list of places details."""
    sort_places(unvisited_places, visited_places)

    count = 1
    for place in unvisited_places:  # looping for unvisited places
        if place[3] == 'n':
            print("{}{}. {:8} in {:11} {:>2}".format("*", count, place[0], place[1], place[2]))
            count += 1

    for place in visited_places:  # looping for visited places
        if place[3] == 'v':
            print(" {}. {:8} in {:11} {:>2}".format(count, place[0], place[1], place[2]))
            count += 1

    if len(places) == len(visited_places):  # when the unvisited places is not have / displaying the No places to visit
        print(f"{len(places)} places. No places left to visit. Why not add a new place?")
    else:
        print("{} places. You still want to visit {} places.".format(len(places),
                                                                     (len(places) - len(visited_places))))


def random_places(places):
    """ Random places for unvisited places """
    unvisited_places = [place for place in places if place[3] == "n"]
    if unvisited_places:
        place = random.choice(unvisited_places)
        print("Not sure where to visit next?")
        print(f"How about... {place[0]} in {place[1]}?")
    else:
        print("No places left to visit!")


def mark_places(places, visited_places, unvisited_places):
    if len(places) == len(visited_places):  # check the all places are visited
        print("No places to visited")
    else:
        list_places(places, visited_places, unvisited_places)
        print("Enter the number of a place to mark as visited")

        valid_place_num = False
        while not valid_place_num:  # error checking for mark places number input
            try:
                choice = int(input(">>> "))
                if choice > 0 and places[choice - 1]:
                    if choice <= len(unvisited_places):  # check for number input
                        marked_place = unvisited_places[choice - 1]
                        print("{} in {} visited".format(marked_place[0], marked_place[1]))
                        marked_place[3] = "v"
                        visited_places.append(marked_place)
                        del unvisited_places[choice - 1]
                    else:
                        marked_place = visited_places[choice - len(unvisited_places) - 1]
                        print(f"You have already visited {marked_place[0]}")
                    valid_place_num = True
                    return choice - 1
                else:
                    print("Number must be > 0")
            except IndexError:
                print("Invalid place number")
            except ValueError:
                print("Invalid input; enter a valid number")


def add_place(places, unvisited_places):
    """ Add new places to CSV file"""
    while True:
        name = input("Name: ")
        if name:
            break
        else:
            print("Input cannot be blank")
    while True:
        country = input("Country: ")
        if country:
            break
        else:
            print("Input cannot be blank")
    while True:
        try:
            priority = int(input("Priority: "))
            break
        except ValueError:
            print("Priority must be an integer")
    new_places = [name, country, priority, "n"]
    print("{} in {} (priority {}) added to Travel Tracker".format(name, country, priority))
    places.append(new_places)
    unvisited_places.append(new_places)
    save_to_file(places)


def save_to_file(places):
    """Save the updated places lists to the file. """
    out_file = open(FILENAME, "w")
    for each_places in places:
        for i, places_detail in enumerate(each_places):
            if i == len(each_places) - 1:
                print(places_detail, file=out_file)
            else:
                print(places_detail, file=out_file, end=",")
    out_file.close()


main()

