import copy
import inspect

class EntryBase:
    """This serves as the base class for entries.
    It includes pretty printing and limitations to possible attributes.
    When inheriting, simply include in 'attributes' the variables that you want to add to this class (not in parent classes already)"""
    _can_set_any_attr = True
    attributes = ()
    
    @classmethod
    def _get_parent_hierarchy_with_attributes(cls):
        base_classes = [base for base in inspect.getmro(cls) if (hasattr(base, 'attributes'))]
        return base_classes[::-1]
    
    @classmethod
    def _get_all_attributes(cls):
        base_classes = cls._get_parent_hierarchy_with_attributes()
        # Using tuples and summing in this order, allows us to keep the proper attribute order from Base -> Parent -> Child
        return sum((base.attributes for base in base_classes), start=())
        
    
    def __new__(cls, *args, **kwargs):
        """Update attributes to include from parent classes"""
        instance = super().__new__(cls)
        instance.attributes = cls._get_all_attributes()
        instance._can_set_any_attr = False
        return instance
    
    
    def __init__(self, *args, **kwargs):
        """Create instance with the proper attributes automatically. Basically just imitates __init__ but with automatic variables"""
        if len(args) > len(self.attributes):
            raise TypeError(f"Received too many (non-positional) arguments")
        
        # Create mapping of {args: attributes}
        dict_args = dict(zip(self.attributes, args))
        
        # Raise error if repeated assignments to attributes
        if (common_args := (dict_args.keys() & kwargs)):   #  python 3.8 syntax only!
            raise TypeError(f"{self.__class__.__name__}'s init got multiple values for argument(s): {common_args}")
        
        kwargs.update(dict_args)  # Merge the two dictionaries
        
        if (set(self.attributes) != kwargs.keys()):  # Invalid args
            # Check for missing arguments:
            if (missing_args := (set(self.attributes) - kwargs.keys())):    #  python 3.8 syntax only!
                raise TypeError(f"{self.__class__.__name__}'s init is missing the following argument(s): {missing_args}")

            # Check of extra arguments:
            if (unexpected_args := (kwargs.keys() - self.attributes)):  #  python 3.8 syntax only!
                raise TypeError(f"{self.__class__.__name__}'s init received unexpected argument(s): {unexpected_args}")
                
            raise TypeError("Unexpected Error")
        
        
        else:  # Correct args, so add them
            self.__dict__.update(kwargs)
    
    
        
    def __setattr__(self, name, value):
        """Limit settting attributes to those selected"""
        # This can still be broken by using __dict__. Couldn't find a way to lock that without the usage of __slots__, or replacing __dict__ with my own class
        if self._can_set_any_attr or name in self.attributes:
            super().__setattr__(name, value)
        else:
            raise AttributeError(f"Unable to set '{name}' for class {self.__class__.__name__}")
            
    def __getitem__(self, key):
        """Allow getting attributes using a index like notation."""
        if key in self.attributes:
            return self.__getattribute__(key)
        else:
            raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{key}'")
    
    def __str__(self):
        return '\n'.join(f'{attr}: {self[attr]}' for attr in self.attributes)
        
    def __repr__(self):
        return f'{self.__class__.__name__}({", ".join(f"{attr}={self[attr]}" for attr in self.attributes)})'
    

class BookBase:
    """This serves as the base class for the book entries that we have.
    This already includes most necessary functions and tools, like indexing, searching, adding, printing and copying.
    When inheriting from it to create phone books, change the 'ENTRY_TYPE' variable to the entry class desired."""
    ENTRY_TYPE = EntryBase
    attributes = None # this will be filled later with ENTRY_TYPE._get_all_attributes()
    
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.attributes = cls.ENTRY_TYPE._get_all_attributes()
        return instance
    
    def __init__(self):
        self.entries = []
        
    def add_contact(self, *args, **kwargs):
        """Add a contact to the book. The args/kwargs required are defined by the ENTRY_TYPE."""
        self.entries.append(self.ENTRY_TYPE(*args, **kwargs))
                
        
    def find(self, **kwargs):
        """Find all the entries to match the given (keyword) arguments. Returns a list of matches (or an empty list if no matches were found)"""
        matches = []
        for entry in self.entries:
            found = True
            for (kw, value) in kwargs.items():
                if entry[kw] != value:  # if kw in self.attributes and entry[kw] != kwargs[kw]:  -> use this if we want to ignore kwords that don't exist
                    found = False
                    break
                    
            if found:
                matches.append(entry)
        return matches
    
            
    def create_copy(self):
        """Returns a copy of this book with deepcopies for all the entries."""
        return copy.deepcopy(self)  # needs to be deepcopy in order to also copy the inner entries
    
    
    def print_book(self):
        """Prints a representation of the book."""
        print(self)
        
        
    def __getitem__(self, key):
        """Allow to search by index."""
        return self.entries[key]
    
    
    def __repr__(self):
        if self.entries:
            return f"{self.__class__.__name__} ({len(self.entries)} entries of type '{self.ENTRY_TYPE.__name__}' with attributes {self.attributes})"
        else:
            return f'{self.__class__.__name__} (Empty)'
    
    
    def __str__(self):
        if self.entries:
            s = ''
            ix_length = len(str(len(self.entries)))  # for better float/string formatting and divider size
            for ix, entry in enumerate(self.entries, start=1):
                s += f'--- Entry #{ix:0{ix_length}} ---\n{entry}\n\n'
            s += '-' * (15 + ix_length)
        else:
            s = "Your book has no entries yet"
        return s
    
    
    ### A few aliases to make it easier
    new_contact = create_contact = add_contact
    search = find
    print = print_book
    get_copy = create_copy

