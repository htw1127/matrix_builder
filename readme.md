# Matrix Builder

### What is the Matrix Builder?
The importance of linear algebra and its representation in matrix form has been on a growing
trend for a long time. However, working with the matrix can be a difficult challenge; especially
working with many big matrices in a computer can be a quite tedious task. Therefore, through this project
we have sought to alleviate these burdensome problems with an intuitive solution.
Matrix builder is the GUI program which helps users to build any matrix using an interactive canvas based on 
the **tkinter** library. The program uses a basic drag-and-drop scheme to interact with the users. It supports various
ways to convert users' works in the program into useful formats which users can directly utilize. 


### Builder Layout
![](https://github.com/htw1127/matrix_builder/raw/main/images/builder_layout.png)
1. Menu Bar, which the user can saved/load or export the progress in different forms. 
2. Canvas, which the user can interact with.
3. Control Frame, which the user can use to configure various aspects of the matrix.
4. Group Manager, manages 'matrix group'; see below for detailed explanation.
5. Status Bar

## How to Start
#### From Command-line console
```commandline
build-matrix
```

#### From Python Context
```python
import builder as bd

# To Start the GUI
bd.main()
```
## How to Use (Example)
#### Delete, Create, and Rename Matrix
![](https://github.com/htw1127/matrix_builder/raw/main/images/delete_create_rename.gif)
- Use **RMB (Two-finger click in Mac)** on canvas to see drop down options.
- If a matrix is not given a name, its default name is "M + number of total matrix".
<br/>
<br/>
  
#### Zoom In/Out, and Translation
![](https://github.com/htw1127/matrix_builder/raw/main/images/zoom_in_out_translate.gif)

<br/>
<br/>

#### Resize Matrix
![](https://github.com/htw1127/matrix_builder/raw/main/images/resize.gif)
- Reset does the same thing as resize, but it does not save matrices.
<br/>
<br/>

#### Group Transpose
![](https://github.com/htw1127/matrix_builder/raw/main/images/group_transpose.gif)
-  Group cannot be moved once created, but it can be deleted.
-  Group List will not be saved after load or reset function.
<br/>
<br/>

#### Save and Load
![](https://github.com/htw1127/matrix_builder/raw/main/images/save_load.gif)
- ALL saved/exported files will be placed in the local copy of the builder package. 
<br/>
<br/>

#### Export
![](https://github.com/htw1127/matrix_builder/raw/main/images/export.gif)
- ALL saved/exported files will be placed in the local copy of the builder package. 
- **Sparse Python** and **Sparse C++** options are for matrices with few zeros.
<br/>
<br/>

### Helpful Key Bindings
- **Ctrl + v** : Copy and Paste the currently highlighted matrices
- **(Hold) Ctrl** : Enter Multiple Selection Mode. In this mode user can highlight multiple matrices
- **Ctrl + Mousewheel** : Zoom in and out of the canvas. The pivot point of zoom is where the point is
  currently located.
- **Shift + LMB Drag** : Can move the matrix inside the canvas
- **RMB** : Provides useful options depending on a selected entity in the canvas. 

<br/>
<br/>

Contributor: Taewoo Han\
Advisor: Dr. Forrest Laine\
This project started during UC Berkeley Spring 2020 as a research project. If there is any
issue or recommendation regarding the program, please email me at: *htw1127@gmail.com*