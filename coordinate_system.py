from test_functions import get_line

class coordinate_system:
    def __init__(self, size:tuple[int,int]):
        "size is the size of the display"
        self.size = size

    def extern_to_intern(self, extern:tuple ) -> list:
        return [extern[0], self.size[1] - extern[1]]
        
    def intern_to_extern(self, intern:tuple) -> list:
        return [intern[0], self.size[1] - intern[1]]
    





if __name__ == "__main__":
    test = coordinate_system((800,800))

    if test.extern_to_intern((500,10)) != [500, 790]: print(f"error in line {get_line()}")

    print("coordinate_system test done")