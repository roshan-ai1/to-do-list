import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('todo.db')
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    try:
        sql_create_todo_table = """ CREATE TABLE IF NOT EXISTS todo (
                                        id integer PRIMARY KEY,
                                        task text NOT NULL,
                                        status text NOT NULL
                                    ); """
        c = conn.cursor()
        c.execute(sql_create_todo_table)
    except Error as e:
        print(e)

def add_task(conn, task):
    sql = ''' INSERT INTO todo (task, status)
              VALUES(?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, (task, "Pending"))
    conn.commit()
    return cur.lastrowid

def view_tasks(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM todo")
    rows = cur.fetchall()
    for row in rows:
        print(f"ID: {row[0]} | Task: {row[1]} | Status: {row[2]}")

def update_task(conn, task_id, status):
    sql = ''' UPDATE todo
              SET status = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (status, task_id))
    conn.commit()

def delete_task(conn, task_id):
    sql = 'DELETE FROM todo WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (task_id,))
    conn.commit()

def main():
    conn = create_connection()
    if conn is not None:
        create_table(conn)
    else:
        print("Error! Cannot create the database connection.")

    while True:
        print("\nTo-Do List Application")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task Status")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            task = input("Enter the task: ")
            add_task(conn, task)
            print("Task added successfully!")
        elif choice == '2':
            view_tasks(conn)
        elif choice == '3':
            task_id = int(input("Enter the task ID to update: "))
            status = input("Enter the new status (Pending/Completed): ")
            update_task(conn, task_id, status)
            print("Task updated successfully!")
        elif choice == '4':
            task_id = int(input("Enter the task ID to delete: "))
            delete_task(conn, task_id)
            print("Task deleted successfully!")
        elif choice == '5':
            if conn:
                conn.close()
            print("Exiting the application.")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == '__main__':
    main()
