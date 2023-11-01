import random
import csv
from functools import reduce
import numpy as np

class Course:
    def __init__(self, name, credits, period, duration, prerequisites):
        self.name = name
        self.credits = credits
        self.period = period
        self.duration = duration
        self.prerequisites = prerequisites

def generate_curriculum(courses):
    courses.sort(key=lambda c: c.period)
    curriculum = []
    credits_completed = [0] * 8
    prerequisites_completed = [False] * len(courses)

    for i, course in enumerate(courses):
        prerequisites_satisfied = all(prerequisites_completed[p] for p in course.prerequisites)
        period_credits_remaining = 60 - credits_completed[course.period - 1]
        period_duration_remaining = 40 - sum(c.duration for c in curriculum)
        period_time_remaining = min(period_credits_remaining, period_duration_remaining)
        course_fits_in_period = course.duration <= period_time_remaining

        if prerequisites_satisfied and course_fits_in_period:
            curriculum.append(course)
            credits_completed[course.period - 1] += course.credits
            prerequisites_completed[i] = True

    return curriculum

def calculate_fitness(solution):
    curriculum = generate_curriculum(solution)
    return -len(curriculum)

def blue_whale_algorithm(courses, population_size=30, max_iterations=100):
    def crossover(parent1, parent2):
        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2

    def mutate(solution):
        index1, index2 = random.sample(range(len(solution)), 2)
        solution[index1], solution[index2] = solution[index2], solution[index1]
        return solution

    def generate_initial_population(courses, population_size):
        population = []
        for _ in range(population_size):
            new_individual = courses.copy()
            random.shuffle(new_individual)
            population.append(new_individual)
        return population

    population = generate_initial_population(courses, population_size)
    best_solution = min(population, key=calculate_fitness)
    best_fitness = calculate_fitness(best_solution)

    for iteration in range(max_iterations):
        for i in range(0, population_size, 2):
            parent1, parent2 = random.sample(population, 2)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)

            population.extend([child1, child2])

        population = sorted(population, key=calculate_fitness)[:population_size]
        current_best_solution = min(population, key=calculate_fitness)
        current_best_fitness = calculate_fitness(current_best_solution)

        if current_best_fitness < best_fitness:
            best_solution = current_best_solution
            best_fitness = current_best_fitness

    return generate_curriculum(best_solution)

def read_courses_from_csv(filename):
    courses = []

    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            name = row[0].strip()
            credits = int(row[1].strip())
            period = int(row[2].strip())
            duration = int(row[3].strip())

            prerequisites = [int(x.strip()) for x in row[4].split()] if row[4].strip() else []

            courses.append(Course(name, credits, period, duration, prerequisites))

    return courses

filename = input("Enter the name of the CSV file containing course information: ")
courses = read_courses_from_csv(filename)

population_size = 30
max_iterations = 100

curriculum = blue_whale_algorithm(courses, population_size, max_iterations)

print("Curriculum:")
for course in curriculum:
    print(f"{course.name} ({course.credits} credits, period {course.period}, {course.duration} hours/week)")