
import random
import os

class Task:

    def __init__(self, task_string, task_id):
        """
        This is the constructor for the Task class.
        Parameters:
        task_string (str): Task string
        task_id (str): Task id
        """
        self.task_string = task_string
        self.task_id = task_id
        self.completed = 'I'
        self.next_task = None

class ToDoListProcessor:

    def __init__(self):
        """
        This is the constructor for the ToDoListProcessor class.
        """
        self.head = None
        self.tail = None
        self.task_count = 0

    def initiateToDoList(self, read_input_file):
        """
        This method reads the input file and processes the commands.
        Parameters:
        read_input_file (str): Input file name
        """
        try:
            with open(read_input_file, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    task_string = line.strip().split(':')
                    command = task_string[0].strip()
                    task = task_string[1].strip()
                    if(command == "Add a Task"):
                        task_id = self.addTask(task)
                        output = f"ADDED:{task_id}-{task}"
                        self.write_to_file(output)
                    elif(command == "Remove Task"):
                        if len(task) == 6 and task[0:2] == "TA" and task[2:].isdigit():
                            task_id,task_string = self.removeTask(task_number=task)
                        else:
                            task_id,task_string = self.removeTask(task_string=task)
                        output = f"REMOVED:{task_id}-{task_string}"
                        self.write_to_file(output)
                    elif(command == "Search Task"):
                        search_results = self.searchTask(task)
                        if len(search_results) :
                            output= '{}{}\n{}\n{}'.format(f"SEARCHED:{task}\n",
                                                              '-'*30,
                                                              '\n'.join([f'{id}-{name}' for id, name in search_results]),
                                                              '-'*30)
                        self.write_to_file(output)
                    elif(command == "Mark Complete"):
                        task_id = self.completeTask(task_string=task)
                        output = f"COMPLETED:{task_id}-{task}"
                        self.write_to_file(output)
                    elif(command == "Mark InComplete"):
                        self.incompleteTask(task_string=task)
                        output = f"UNCOMPLETED:{task_id}-{task}"
                        self.write_to_file(output)
                    elif(command == "Task Status"):
                        output = f"TASK STATUS:\nTask-Number Task-String Task-Status \n'-'*30\n "
                        tasks_status = self.statusTask()
                        if len(tasks_status):
                            output = '{}{}\n{}\n{}'.format(f"TASK-STATUS:\nTask-Number Task-String Task-Status \n",
                                                              '-'*30,
                                                              '\n'.join([f'{id}-{name}-{status}' for id, name, status in tasks_status]),
                                                              '-'*30)
                            self.write_to_file(output)
                    else:
                        print("Invalid input")
                        return

                    self.display_tasks(self.head)
        except FileNotFoundError:
            print("File not found")
            raise FileNotFoundError
        except Exception as e:
            print(f"Following exception occured while processing the command \"{line}\" : " + str(e))
            raise e

    #TODO added only for testing. to be deleted before submission
    def display_tasks(self, head):
        """
        This method displays the tasks in the to-do list.
        Parameters:
        head (Task): Head of the linked list
        """
        current = head
        tasks = []
        while current:
            tasks.append(current.task_id)
            current = current.next_task
        print(tasks)

    def write_to_file(self, output):
        """
        This method writes the output to the output file.
        Parameters:
        output (str): Output string
        """
        with open('outputPS03.txt', 'a') as output_file:
            output_file.write(output + "\n")

    def addTask(self, task_string=""):
        """
        This method adds a task to the to-do list.
        Parameters:
        task_string (str): Task string
        """
        print(f"Adding following task: {task_string}")
        try:
            task_number = self.generate_task_number()
            new_task = Task(task_string, task_number)
            self.task_count += 1
            if self.head is None:
                self.head = new_task
                self.tail = self.head
            else:
                self.tail.next_task= new_task
                self.tail = new_task
            return new_task.task_id
        except Exception as e:
            print(f"Exception while adding the task {task_string} " + str(e))
            raise e

    def removeTask(self, task_string="", task_number=""):
        """
        This method removes a task from the to-do list.
        Parameters:
        task_string (str): Task string
        task_number (str): Task number
        """
        print(f"Removing following task: {task_string} {task_number}")
        try:
            isFound = False
            task_identifier = ""
            if task_number != "":
                task_identifier = task_number
            else:
                task_identifier = task_string
            current = self.head
            previous = None
            while current is not None:
                if str(current.task_id) == task_identifier or current.task_string.lower() == task_identifier.lower():
                    isFound = True
                    task_number = current.task_id
                    task_string = current.task_string
                    if previous is None:
                        self.head = current.next_task
                        if not self.head:
                            self.tail = None
                    else:
                        previous.next_task = current.next_task
                        if current == self.tail:
                            self.tail = previous

                    self.task_count -= 1
                previous = current
                current = current.next_task
            if not isFound:
                raise Exception(f"Task {task_string} {task_number} is not found to be removed!")
            return task_number,task_string
        except Exception as e:
            print("Exception while removing the task {task_string} {task_number}" + str(e))
            raise e


    def searchTask(self, search_string=""):
        print(f"Searching following task: {search_string}")
        try:
            if (search_string == ""):
                print("Empty search keyword was passed")
                return
            isFound = False
            search_results = []
            current = self.head
            while current is not None:
                if str(current.task_id) == search_string or search_string.lower() in current.task_string.lower():
                    isFound = True
                    search_results.append((current.task_id, current.task_string))
                current = current.next_task
            if not isFound:
                raise Exception(f"Task with keyword {search_string} is not found!")
            return search_results
        except Exception as e:
            print(f"Exception while searching for {search_string}" + str(e))
            raise e    

    def completeTask(self, task_string="", task_number=""):
        print(f"Completing following task: {task_string} {task_number}")
        try:
          isFound = False
          if task_number != "":
            task_identifier = task_number
          else:
            task_identifier = task_string
          current = self.head
          while current is not None:
            if str(current.task_id) == task_identifier or current.task_string.lower() == task_identifier.lower():
              current.completed = 'C'
              isFound = True
              task_number = current.task_id
              break
            current = current.next_task
          if not isFound:
            raise Exception(f"Task {task_string} {task_number} is not found to be updated!")
          return task_number
        except Exception as e:
            print("Exception while completing the task {task_string} {task_number}" + str(e))
            raise e

    def incompleteTask(self, task_string="", task_number=""):
        print(f"Incompleting following task: {task_string} {task_number}")
        try:
          isFound = False
          if task_number != "":
            task_identifier = task_number
          else:
            task_identifier = task_string
          current = self.head
          while current is not None:
            if str(current.task_id) == task_identifier or current.task_string.lower() == task_identifier.lower():
              current.completed = False
              isFound = True
              #print(current.task_id," ",current.task_string," ",current.completed)
              break
            else: current = current.next_task
          if not isFound:
            raise Exception(f"Task {task_string} {task_number} is not found to be updated!")
        except Exception as e:
            print("Exception while updating the task {task_string} {task_number}" + str(e))
            raise e


    def statusTask(self):
        print("Status of the tasks:")
        task_status = []
        try:
          current = self.head
          output = ""
          while current is not None:
            task_status.append((current.task_id, current.task_string, current.completed))
            current = current.next_task  
          print(task_status)
          return task_status
        except Exception as e:
            print("Exception while updating the task {task_string} {task_number}" + str(e))
            raise e


    def generate_task_number(self):
        random_number = random.randint(0, 9999)
        formatted_number = f"TA{random_number:04d}"
        return "TA1234"
        # return formatted_number


if __name__ == "__main__":
    input_file = "inputPS03.txt"
    output_file = "outputPS03.txt"
    to_do_processor = ToDoListProcessor()
    if os.path.exists(output_file):
        os.remove(output_file)
    to_do_processor.initiateToDoList(input_file)
