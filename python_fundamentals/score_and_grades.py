#Assignment: Scores and Grades
import random
def generator ():
    for i in range (10):
        score = random.randint(60, 100)
        if score >= 60 and score <=69:
            print "score:", score, "your grade is D"
        if score >= 70 and score <=79:
            print "score:", score, "your grade is C"
        if score >= 80 and score <= 89:
            print "score:", score, "your grade is B"
        if score >= 90 and score <= 100:
            print "score:", score, "your grade is A"
        
generator()
