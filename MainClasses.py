from BaseClasses import EntryBase, BookBase


class PhoneEntry(EntryBase):
    """This class holds entries of people with a name and a phone number"""
    attributes = ('name', 'phone')

class PhoneEntryExt(PhoneEntry):
    """This class holds entries of people with a name, phone number and email address"""
    attributes = ('email',)

class PhoneEntryExt2(PhoneEntryExt):
    """This class holds entries of people with a name, phone number and email address and a age"""
    attributes = ('age',)




class PhoneBook(BookBase):
    """This class is a Phone book that holds entries with a name and a phone number."""
    ENTRY_TYPE = PhoneEntry
    
    
class PhoneBookExt(BookBase):
    """This class is a Phone book that holds entries with a name, phone number and email address."""
    ENTRY_TYPE = PhoneEntryExt


class PhoneBookExt2(BookBase):
    """This class is a Phone book that holds entries with a name, phone number, email address and age."""
    ENTRY_TYPE = PhoneEntryExt2




if __name__ == '__main__':
    book = PhoneBookExt2()
    book.add_contact('ana', 1234, 'ana@mail.com', 24)
    book.add_contact('ana', 2345, 'ana2@email.com', 19)
    book.add_contact('bob', 1234, 'bob@email.org', 21)
    book.add_contact(name='carl', phone=9876, email='carl@carl.carl', age=23)

    print(book)
    print(book.search(name='ana'))
    print(book.search(name='ana', phone=1234))
