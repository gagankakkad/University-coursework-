
import pygame # type: ignore
import random
import math
import pandas as pd


pygame.init()# Initialize Pygame

WIDTH = 800# Set up the screen
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))# pygame.org setting up main window for testing
pygame.display.set_caption("Click on targets from centre")


clock = pygame.time.Clock()# Set up the clock

TARGET_RADIUS = 26# Set up the targets
target1_pos = (WIDTH//2, TARGET_RADIUS)# Targers set in star position
target2_pos = (700, HEIGHT-TARGET_RADIUS )
target3_pos = (TARGET_RADIUS, HEIGHT//2)
target4_pos = (WIDTH-TARGET_RADIUS, HEIGHT//2)
target5_pos = (200, HEIGHT-TARGET_RADIUS)
targets = [target1_pos, target2_pos, target3_pos, target4_pos, target5_pos]# List of targets


font = pygame.font.SysFont(None, 25)#Set up the font


clicked_targets = [False] * len(targets)# Coubting how many targets clicked
start_time = 0
end_time = 0
overshoots = [0] * len(targets)
distances = [0] * len(targets)
accuracies = [0] * len(targets)


running = True # Set up the game loop
while running:
    
    for event in pygame.event.get():# Start events 
        if event.type == pygame.QUIT:
            running = False # If game no longer running
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(targets)):
                if not clicked_targets[i] and math.sqrt((event.pos[0]-targets[i][0])**2 + (event.pos[1]-targets[i][1])**2) < TARGET_RADIUS:# If not clicked and distance < radius
                    clicked_targets[i] = True
                    overshoots[i] = abs(event.pos[0]-targets[i][0])# Calculate overshoot from x coordinate 
                    distances[i] = math.sqrt((event.pos[0]-targets[i][0])**2 + (event.pos[1]-targets[i][1])**2)# Formula for distance from w3resources
                    accuracies[i] = 1 - distances[i]/TARGET_RADIUS # Closest to centre of target
                    if i == 0:
                        start_time = pygame.time.get_ticks()#start timer pygame.org
                    elif all(clicked_targets): # If all targets clicked stop clock
                        end_time = pygame.time.get_ticks() #pygame.org

    
    screen.fill((255, 255, 255))# Clear the screen

    
    for i in range(len(targets)): # Draw the targets
        pygame.draw.circle(screen, (255-i*50, 0, i*50), targets[i], TARGET_RADIUS)
        target_text = font.render(str(i+1), True, (0, 0, 0))
        screen.blit(target_text, (targets[i][0]-7, targets[i][1]-12))

    # Draw the cursor
    cursor_pos = pygame.mouse.get_pos() # Tracking mouse position
    #pygame.draw.circle(screen, (0, 0, 255), cursor_pos, 5)

    
    midpoint_x = sum([target[0] for target in targets])//len(targets)# Calculate the optimal path between the targets
    midpoint_y = sum([target[1] for target in targets])//len(targets)
    optimal_path_pos = (midpoint_x, midpoint_y)
    for target in targets:
        pygame.draw.line(screen, (0, 0, 0), target, optimal_path_pos, 2)

   
    def display_statistics():
        
    
        overall_accuracy = sum(accuracies)/len(targets)# Calculate overall accuracy

    
        time_taken_text = font.render(f"Time taken: {(end_time-start_time)/1000:.2f} seconds", True, (0, 0, 0))# Display time taken
        screen.blit(time_taken_text, (10, 10))

    
        overall_accuracy_text = font.render(f"Overall accuracy: {overall_accuracy:.2%}", True, (0, 0, 0)) # Display overall accuracy
        screen.blit(overall_accuracy_text, (10, 40))

    
        for i in range(len(targets)):# Display individual accuracies
            accuracy_text = font.render(f"Accuracy {i+1}: {accuracies[i]:.2%}", True, (0, 0, 0))
            screen.blit(accuracy_text, (10, 70+i*30))

    
        for i in range(len(targets)):# Display overshoots
            overshoot_text = font.render(f"Overshoot {i+1}: {overshoots[i]/TARGET_RADIUS:.2%}", True, (0, 0, 0))
            screen.blit(overshoot_text, (250, 70+i*30))

    
        for i in range(len(targets)):
            distance_text = font.render(f"Distance {i+1}: {distances[i]:.2f}", True, (0, 0, 0))# Display distances
            screen.blit(distance_text, (450, 70+i*30))

        data = {'Target': range(1, len(targets)+1),
                'Accuracy': accuracies,
                'Overshoot': overshoots,
                'Distance': distances}
        df = pd.DataFrame(data)

    
        df.to_csv('stats.csv', index=False)# Write data to a .csv file
    
    if all(clicked_targets): # Display stats once all targets clicked
        screen.fill((255, 255, 255))# Clear screen
        display_statistics() # Display all the stats 

    pygame.display.update()

    
        

   
    clock.tick(60)# pygame.org


pygame.quit()# Quit Pygame