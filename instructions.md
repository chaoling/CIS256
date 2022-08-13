# Instructions  

#### Suppose the file studentdata.txt contains information on grades students earned on various assignments. Each line has the last name of a student (which you can assume is one word) and the numeric grade that the student received. All grades are out of 100 points. Students can appear multiple times in the file. 

Here’s a sample file: 

```Arnold 90 Brown 84 Arnold 80 Cocher 77 Cocher 100 ```

Write a function that reads the data from the file into a dictionary. 
Then continue prompting the user for names of students. 

For each student, it should print the average of that student’s grades. 
Stop prompting when the user enters the name of a student not in the dictionary. 

### Sample runs:
```
Enter name: Arnold 
The average for Arnold is: 85.0 
Enter name: Brown 
The average for Brown is: 84.0 
Enter name: Cocher 
The average for Cocher is: 88.5 
Enter name: Doherty 
Goodbye! 
```
