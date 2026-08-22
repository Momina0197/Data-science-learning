from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError

#Creating Database
engine = create_engine("sqlite:///tasks.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

#Define Models(User / Tasks)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer , primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    tasks = relationship('Task', back_populates='user', cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String)
    user_id =Column(Integer, ForeignKey("users.id"))
    user = relationship('User', back_populates='tasks')

Base.metadata.create_all(engine)

#Utitility Functions

def get_user_email(email):
    return session.query(User).filter_by(email=email).first()

def confirm_action(prompt):
    return input(f"{prompt} (yes/no): ").strip().lower() =='yes'

#CRUD Operations

def add_user():
    name , email = input("Enter User Name : "), input("Enter email: "),
    if get_user_email(email):
        print(f'User already exists: {email}')
        return
    
    try:
        session.add(User(name=name,email=email))
        session.commit()
        print(f'User {name} created!')
    except IntegrityError:
        session.rollback()
        print(f'Error')

def add_task():
    email = input("Enter the email of the user to add the task: ")
    user = get_user_email(email)
    if not user:
        print("No user found against that email")
        return

    title, description = input("Enter the Task Title: "), input("Enter the Task Description: ")
    session.add(Task(title=title, description=description, user=user))
    session.commit()
    print(f'{title} Added to the Database!')

def update_user():
    email= input("Enter the email of the user you want to update: ")
    user = get_user_email(email)
    if not user:
        print("No user found against that email")
        return

    user.name = input("Enter the new user name (or leave blank to keep the same) : ") or user.name
    user.email = input("Enter the new email (or leave blank to keep the same) : ") or user.email
    session.commit()
    print(f'User {user.name} has been update')

#Deleting

def delete_user():
    email = input("Enter the email of the user you want to delete: ")
    user = get_user_email(email)
    if not user:
        print("No user found against that email")
        return

    if confirm_action(f"Are you sure you want to delete the {user.name}? "):
        session.delete(user)
        session.commit()
        print("User has been deleted!")

def delete_task():
    email = input("Enter the email of the user whose task you want to delete: ")
    user = get_user_email(email)

    if not user:
        print("No user found against that email")
        return

    if not user.tasks:
        print("This user has no tasks.")
        return

    for task in user.tasks:
        print(f"TASK ID: {task.id}, TASK Title: {task.title}")

    task_id = input("Enter the id of the task you want to delete: ").strip()
    task = next((t for t in user.tasks if str(t.id) == task_id), None)

    if task is None:
        print("Invalid task ID for this user.")
        return

    if confirm_action(f"Are you sure you want to delete task {task.id}? "):
        session.delete(task)
        session.commit()
        print("Task has been deleted!")


# Main Operations

def main() -> None:
    actions ={
        "1":add_user,
        "2":add_task,
        "3":update_user,
        "4":delete_user,
        "5":delete_task,
    }

    while True:
        print("\nOptions:\n1. Add User\n2. Add Task\n3.Update User\n4. Delete User\n5. Delete Task\n6. Exit")
        choice = input("Enter an Option: ")
        if choice == "6":
            print("Adios!")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("That is not an option")

if __name__ == "__main__":
    main()

    