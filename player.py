class Player:
    def __init__(self, name):
        self.name = name
        self.gpa = 3.00

        # Ensure GPA does not exceed 4.00
        self.gpa = min(self.gpa, 4.50)