# Cervical Cancer Detection

# by Harshit Patel

Cervical Cancer Detection was one of the most deadlies cancer. Technologies like PAP smear test, etc. have helped reduced the mortatlity rate drastically. But in rural areas it is very hard to get the medical expertise of expert pathologists who can classify cervical cells as either malignant or benign. 

In our project, I designed the Machine Learning Model and Software for detecting cervical cancer from cell images collected from pap smear test. For this we used the benchmark Harlev Dataset (https://mde-lab.aegean.gr/downloads). The data set had 917 images, which I splitted into a training/cv/test set of 60%/20%/20% and trained the model on Training set. I thresholded images using Intersecting Cortical Model (ICM) Algorithm and extracted thirteen features from all images. We used those features to train the model. The final test f1 score was 90.65% using Random Forest Classifier.

Finally, I used Python's PyQt5 library to design a GUI for the software.
