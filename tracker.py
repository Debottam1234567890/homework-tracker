import csv
import pygame
from datetime import datetime

# Initialize Pygame
pygame.init()

# Constants for the window size and colors
WIDTH, HEIGHT = 1000, 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
GREEN = (34, 139, 34)
RED = (220, 20, 60)
GRAY = (200, 200, 200)
BG_COLOR = (245, 245, 250)

FONT = pygame.font.SysFont('arial', 20)
BIG_FONT = pygame.font.SysFont('arial', 28, bold=True)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Homework Tracker")

# Function to read tasks from CSV
def read_tasks_from_csv(file_path="hw.csv"):
    tasks = []
    try:
        with open(file_path, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tasks.append(row)
    except FileNotFoundError:
        print("hw.csv not found.")
    return tasks

# Function to display the header on the GUI
def draw_header():
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 60))
    title = BIG_FONT.render("📚 Homework Tracker Dashboard", True, WHITE)
    screen.blit(title, (20, 15))

# Function to display individual tasks in the GUI
def draw_task_card(task, x, y, w, h):
    # Determine color by priority
    priority_colors = {
        "Critical": RED,
        "This Week": (255, 165, 0),
        "Long-term": GREEN,
        "Extra Credit": (148, 0, 211),
        "Fun Project": (30, 144, 255),
    }
    color = priority_colors.get(task['priority'], GRAY)
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=12)
    pygame.draw.rect(screen, BLACK, (x, y, w, h), 2, border_radius=12)

    margin = 10
    lines = [
        f"Subject: {task['subject']}",
        f"Description: {task['description']}",
        f"Due Date: {task['due date']}",
        f"Priority: {task['priority']}",
        f"Logged: {task['date_of_log']}"
    ]
    for i, line in enumerate(lines):
        text = FONT.render(line, True, WHITE)
        screen.blit(text, (x + margin, y + margin + i * 25))

# Function to draw all tasks in the GUI
def draw_tasks(tasks):
    start_y = 80
    card_width, card_height = WIDTH - 80, 140
    spacing = 160
    for i, task in enumerate(tasks):
        y = start_y + i * spacing
        draw_task_card(task, 40, y, card_width, card_height)

# Function to add a new task to CSV (terminal input)
def add_task_to_csv(subject, description, due_date, priority, date_of_log, file_path="hw.csv"):
    with open(file_path, mode="a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([subject, description, due_date, priority, date_of_log])

# Function to display existing tasks in the terminal
def display_tasks(tasks):
    if not tasks:
        print("\nNo tasks available.\n")
    else:
        print("\nExisting Homework Tasks:")
        for idx, task in enumerate(tasks, start=1):
            print(f"{idx}. Subject: {task['subject']}, Description: {task['description']}, Due Date: {task['due date']}, Priority: {task['priority']}, Logged: {task['date_of_log']}")

# Main function to handle input and task management
def main():
    while True:
        print("\nWelcome to the Homework Tracker!")
        print("1. View Homework Tasks (GUI)")
        print("2. Add New Task (Terminal)")
        print("3. Exit")

        choice = input("Please select an option (1/2/3): ").strip()

        if choice == '1':
            tasks = read_tasks_from_csv()
            # Running GUI to display tasks
            clock = pygame.time.Clock()
            running = True
            while running:
                screen.fill(BG_COLOR)
                draw_header()
                draw_tasks(tasks)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                pygame.display.flip()
                clock.tick(60)

            pygame.quit()

        elif choice == '2':
            subject = input("Enter the subject: ")
            description = input("Enter the description: ")
            due_date = input("Enter the due date (YYYY-MM-DD): ")
            priority = input("Enter the priority (Critical, This Week, Long-term, Extra Credit, Fun Project): ")
            date_of_log = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            add_task_to_csv(subject, description, due_date, priority, date_of_log)
            print("\nTask added successfully!")

        elif choice == '3':
            print("Exiting Homework Tracker. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
