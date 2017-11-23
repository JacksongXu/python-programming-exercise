#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import os
import sys
import pickle
import re
from functools import wraps


class PersonInfor:
    """Person information,including name, email, phone number."""

    def __init__(self, name, email, phone_num):
        self.name = name
        self.email = email
        self.phone_num = phone_num

    def print_infor(self):
        print(self.name, ' ', self.email, ' ', self.phone_num)


def is_addrbook_opened(operation_fn):
    """Check whether the address book is opened or not."""
    @wraps(operation_fn)
    def wrap_fn(self_obj):
        if self_obj.opened:
            return operation_fn(self_obj)
        else:
            print("Invalid operation, due to the address book hasn't been opened!")
            return
    return wrap_fn


def is_addrbook_empty(operation_fn):
    """Check whether the address book is empty or not."""
    def wrap_fn(self_obj):
        if self_obj.dictdata:
            return operation_fn(self_obj)
        else:
            print("This is a empty address book!")
            return
    return wrap_fn


class AddressBook:
    """Operations for address book, including add, brows, search person information."""
    def __init__(self, book_file_path):
        self.file_path = book_file_path
        self.dictdata = {}
        self.opened = False

    def open(self):
        if self.opened:
            return

        if os.path.exists(self.file_path):  # check whether the specified address book file exist or not
            with open(self.file_path, 'rb') as f:
                self.dictdata = dict(pickle.load(f))
        else:
            createbook = input("Can't find the address book, create new one?(y/n) ")
            if re.match(r'[yY]', createbook):
                with open(self.file_path, 'wb') as f:
                    print("A new address book is created!")
            elif re.match(r'[nN]', createbook):
                sys.exit(0)
            else:
                print("Unknown command, exit!")
                sys.exit(1)

        self.opened = True

    @is_addrbook_opened
    def save(self):
        """Save the changed dict data to the disk."""
        with open(self.file_path, 'wb') as f:
            pickle.dump(self.dictdata, f)
        self.opened = False

    @is_addrbook_opened
    @is_addrbook_empty
    def browse(self):
        for key in self.dictdata.keys():
            self.dictdata[key].print_infor()

    @is_addrbook_opened
    def add(self):
        p_name = input("input name:")
        p_email = input("input email:")
        p_phonenum = input("input phone num:")
        p = PersonInfor(p_name, p_email, p_phonenum)
        self.dictdata[p.name] = p
        print("Added new person:")
        p.print_infor()

    @is_addrbook_opened
    @is_addrbook_empty
    def search(self):
        p_name = input("input the person's name you wanna search:")
        if p_name in self.dictdata.keys():
            self.dictdata[p_name].print_infor()
        else:
            print("Can't find the %s on the address book!" % p_name)

    @is_addrbook_opened
    @is_addrbook_empty
    def delete(self):
        p_name = input("input the person's name you wanna delete:")
        if p_name in self.dictdata.keys():
            self.dictdata.__delitem__(p_name)
            print("%s is deleted!" % p_name)
        else:
            print("Can't find the %s on the address book!" % p_name)


def main():
    addr_book_file = 'address_book.data'
    addr_book_file_path = os.path.join(os.getcwd(), addr_book_file)
    addr_book = AddressBook(addr_book_file_path)

    addr_book.open()
    addr_book_operation = True

    while addr_book_operation:
        operation = input("""Operation list:
        1. Browse address book
        2. Add person
        3. Delete person
        4. Search person
        5. Exit
        """)

        if operation == '1':
            addr_book.browse()
        elif operation == '2':
            addr_book.add()
        elif operation == '3':
            addr_book.delete()
        elif operation == '4':
            addr_book.search()
        elif operation == '5':
            addr_book_operation = False
        else:
            print("Unknown operation!\n")

    addr_book.save()
    sys.exit(0)


main()
