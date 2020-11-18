# Program for Employee directory using data structure

class emp_directory:
    def __init__(self):
        self.manager = {
            'SOFTWARE': [],
            'HR': [],
            'SECURITY': []
        }
        self.senior = {
            'SOFTWARE': [],
            'HR': [],
            'SECURITY': []
        }
        self.junior = {
            'SOFTWARE': [],
            'HR': [],
            'SECURITY': []
        }
        self.trainee = {
            'SOFTWARE': [],
            'HR': [],
            'SECURITY': []
        }

    def create_manager(self, name, pos, dept):
        """ function to create employee manager."""
        self.manager[dept.upper()].append(
            {
                'name': name,
                'pos': pos,
                'dept': dept,
                'senior': [],
                'junior': [],
                'trainee': []
            }
        )

    def create_senior(self, name, pos, dept):
        """ function to create employee senior."""
        self.senior[dept.upper()].append(
            {
                'name': name,
                'pos': pos,
                'dept': dept,
                'manager': self.manager[dept.upper()][0]['name'],
                'junior': [],
                'trainee': []
            }
        )
        self.manager[dept.upper()][0]['senior'].append(
            {
                'name': name,
                'pos': pos,
                'dept': dept
            }
        )

    def create_junior(self, name, pos, dept):
        """ functions to create employee junior."""
        self.junior[dept.upper()].append(
            {
                'name': name,
                'pos': pos,
                'dept': dept,
                'manager': self.manager[dept.upper()][0]['name'],
                'senior': self.senior[dept.upper()][0]['name'],
                'trainee': []
            }
        )
        self.manager[dept.upper()][0]['junior'].append(
            {
                'name': name,
                'pos': pos,
                'dept': dept
            }
        )
        self.senior[dept.upper()][0]['junior'].append(
            {
                'name': name,
                'pos': pos,
                'dept': dept
            }
        )

    def create_trainee(self, name, pos, dept):
        """ function to create employee trainee."""
        self.trainee[dept.upper()].append(
            {
                'name': name,
                'pos': pos,
                'dept': dept,
                'manager': self.manager[dept.upper()][0]['name'],
                'senior': self.senior[dept.upper()][0]['name'],
                'junior': self.junior[dept.upper()][0]['name'],
            }
        )
        self.manager[dept.upper()][0]['trainee'].append(
            {
                'name': name,
                'pos': pos,
                'dept': dept
            }
        )
        self.senior[dept.upper()][0]['trainee'].append(
            {
                'name': name,
                'pos': pos,
                'dept': dept
            }
        )
        self.junior[dept.upper()][0]['trainee'].append(
            {
                'name': name,
                'pos': pos,
                'dept': dept
            }
        )

    def create_emp(self, name, pos, dept):
        """function to create employee based on postion."""
        if pos.upper() == 'MANAGER':
            self.create_manager(name, pos, dept)
        elif pos.upper() == 'SENIOR':
            self.create_senior(name, pos, dept)
        elif pos.upper() == 'JUNIOR':
            self.create_junior(name, pos, dept)
        else:
            self.create_trainee(name, pos, dept)


# python main method
if __name__ == '__main__':
    # create an instance of class emp_directory
    emp = emp_directory()
    # - dept wise manager.
    emp.create_emp('M1', 'manager', 'software')
    emp.create_emp('H1', 'manager', 'hr')
    emp.create_emp('S1', 'manager', 'security')
    # - dept wise senior.
    emp.create_emp('SS1', 'senior', 'software')
    emp.create_emp('SH1', 'senior', 'hr')
    emp.create_emp('SS1', 'senior', 'security')
    # - dept wise junior.
    emp.create_emp('JS1', 'junior', 'software')
    emp.create_emp('JS2', 'junior', 'software')
    emp.create_emp('JH1', 'junior', 'hr')
    emp.create_emp('JS1', 'junior', 'security')
    emp.create_emp('JS1', 'junior', 'security')
    # - dept wise trainee.
    emp.create_emp('TS1', 'trainee', 'software')
    emp.create_emp('TS2', 'trainee', 'software')
    emp.create_emp('TS3', 'trainee', 'software')
    emp.create_emp('TH1', 'trainee', 'hr')
    emp.create_emp('TS1', 'trainee', 'security')
    emp.create_emp('TS2', 'trainee', 'security')
    print('*****************************************************************')
    print('*****************************************************************')
    # print('LIST OF MANAGER:')
    # print(emp.manager)
    # print('LIST OF SENIOR:')
    # print(emp.senior)
    # print('LIST OF JUNIOR:')
    # print(emp.junior)
    # print('LIST OF TRAINEE:')
    # print(emp.trainee)
    print("Employee Directory:")
    print("Number of Managers: %d" % (
        len(emp.manager['SOFTWARE']) +
        len(emp.manager['HR']) +
        len(emp.manager['SECURITY'])
        )
    )
    print("Number of Senior: %d" % (
        len(emp.manager['SOFTWARE'][0]['senior']) +
        len(emp.manager['HR'][0]['senior']) +
        len(emp.manager['SECURITY'][0]['senior'])
        )
    )
    print("Number of Junior: %d" % (
        len(emp.manager['SOFTWARE'][0]['junior']) +
        len(emp.manager['HR'][0]['junior']) +
        len(emp.manager['SECURITY'][0]['junior'])
        )
    )
    print("Number of Traine: %d" % (
        len(emp.manager['SOFTWARE'][0]['trainee']) +
        len(emp.manager['HR'][0]['trainee']) +
        len(emp.manager['SECURITY'][0]['trainee'])
        )
    )
