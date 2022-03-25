from random import randrange
import random


###############
# BOARD CLASS #
###############
class Board:
    # Constructor method
    def __init__(self):
        # Build blank board for this Object instance
        self.board = [[" ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "]]
        self.chromosome = []  # Blank chromosome
        self.fitness = None  # Create fitness variable
        self.generate_chromosome()  # Generate chromosome list

    # Set chromosome method - used to replace a board's chromosome with a newly spliced one
    def set_chromosome(self, chromosome):
        self.chromosome = chromosome
        self.determine_fitness()
        self.update_board()

    # Generate chromosome method - used to generate a list of 8 random integers from 0-7
    def generate_chromosome(self):
        for x in range(8):
            self.chromosome.append(randrange(8))
        self.determine_fitness()
        self.update_board()

    # Determine fitness function - used to calculate the total attacks on a board, which is the fitness of a board
    def determine_fitness(self):
        totalAttacks = 0
        occurenceDict = {}
        clonedList = self.chromosome.copy()
        for item in clonedList:
            if item in occurenceDict:
                occurenceDict[item] += 1
            else:
                occurenceDict[item] = 1

        for key in occurenceDict:
            if occurenceDict[key] != 1:
                totalAttacks += self.attack_counter(occurenceDict[key])

        occurenceDictDiagP = {}
        occurenceDictDiaN = {}

        for x in range(8):
            item = clonedList[x] - x
            if item in occurenceDictDiagP:
                occurenceDictDiagP[item] += 1
            else:
                occurenceDictDiagP[item] = 1

        for key in occurenceDictDiagP:
            if occurenceDictDiagP[key] != 1:
                totalAttacks += self.attack_counter(occurenceDictDiagP[key])

        for x in range(8):
            item = clonedList[x] + x
            if item in occurenceDictDiaN:
                occurenceDictDiaN[item] += 1
            else:
                occurenceDictDiaN[item] = 1

        for key in occurenceDictDiaN:
            if occurenceDictDiaN[key] != 1:
                totalAttacks += self.attack_counter(occurenceDictDiaN[key])

        self.fitness = totalAttacks

    # Update board method - used to update string representation of the current board
    def update_board(self):
        self.board = [[" ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "]]
        for x in range(8):
            row = self.chromosome[x]
            col = x
            self.board[row][col] = "X"

    # Attack counter method - used to count the number of attacks given the number of occurrences in a line
    def attack_counter(self, num):
        sum = 0
        for x in range(num):
            sum += x
        return sum

    # String representation for Board Object ( used in print() )
    def __str__(self):
        # Building board information string
        boardString = "============================================================\n"
        boardString += "### BOARD INFORMATION ###\n"
        boardString += "Fitness level: " + str(self.fitness) + "\n"
        boardString += "Chromosome: " + str(self.chromosome) + "\n\n"

        # Building board string
        boardString += "-------------------------------------------------\n"
        for row in range(8):
            for col in self.board[row]:
                boardString += "|  "
                boardString += str(col)
                boardString += "  "
            boardString += "|\n"
            boardString += "-------------------------------------------------\n"
        boardString += "============================================================\n"

        return boardString


# Find fittest board method - used to find the fittest board in a population and print/return it
def find_fittest_board(pop):
    fittestBoard = None
    lowestFitnessScore = 999
    for b in pop:
        if b.fitness < lowestFitnessScore:
            lowestFitnessScore = b.fitness
            fittestBoard = b

    print("- GENERATION " + str(generation) + " -")
    # print(fittestBoard)
    return lowestFitnessScore


# Select parents method - used to randomly select 2 parents for reproduction
def select_parents(parentPop):
    parentsList = []  # Create list to hold selected parents
    parentPop.sort(key=lambda y: y.fitness)  # Sort parent population so fittest parents are at start

    # Randomly select 2 parents
    for parent in range(2):
        randomDouble = random.random()  # Randomly choose double between 0 and 1
        randomIndex = int(POPULATION_SIZE * (randomDouble ** 5))  # Using exp curve we can choose fitter parents
        parentsList.append(parentPop[randomIndex])

    return parentsList


# Mutate method - used to mutate
def mutate(chromosome):
    randPercentage = randrange(100) + 1
    if randPercentage <= MUTATION_CHANCE:
        randomIndex = randrange(8)
        randomInt = randrange(8)
        chromosome[randomIndex] = randomInt
    return chromosome


def reproduce(parentsList):
    childrenList = []
    crossoverPoint = randrange(8)

    parent1_chromosome = parentsList[0].chromosome.copy()
    parent2_chromosome = parentsList[1].chromosome.copy()

    child1_chromosome = parent1_chromosome[:crossoverPoint] + parent2_chromosome[crossoverPoint:]
    child2_chromosome = parent2_chromosome[:crossoverPoint] + parent1_chromosome[crossoverPoint:]

    child1_chromosome = mutate(child1_chromosome)
    child2_chromosome = mutate(child2_chromosome)

    child1 = Board()
    child2 = Board()
    child1.set_chromosome(child1_chromosome)
    child2.set_chromosome(child2_chromosome)

    childrenList.append(child1)
    childrenList.append(child2)

    return childrenList


################
# MAIN PROGRAM #
################
if __name__ == '__main__':
    POPULATION_SIZE = 150  # Population size constant
    MUTATION_CHANCE = 30
    solution_set = []
    while len(solution_set) < 92:
        print("Solution set (" + str(len(solution_set)) + "): " + str(solution_set))
        population = []  # List to hold all boards for current generation
        generation = 1
        lowestFitness = 999

        # Populating first generation
        for x in range(POPULATION_SIZE):
            board = Board()
            population.append(board)

        # Loop to find generation with fitness = 0 (stop looping if generations exceed 5000)
        while lowestFitness > 0 and generation < 5000:
            lowestFitness = find_fittest_board(population)  # Update the lowestFitness variable and print the best board
            generation += 1  # Increment generation counter
            parentPopulation = population.copy()  # Current generation becomes new parent population

            # Iterate over population by steps of two. Select two random parents and replace them with offspring
            for x in range(0, POPULATION_SIZE, 2):
                parents = select_parents(parentPopulation)  # Choose two random parents
                children = reproduce(parents)  # Using above parents, create offspring
                population[x] = children[0]
                population[x + 1] = children[1]

        for board in population:
            if board.fitness == 0:
                if board.chromosome not in solution_set:
                    print(board)
                    solution_set.append(board.chromosome)

    print("Solution set (" + str(len(solution_set)) + "): " + str(solution_set))