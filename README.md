![Yeentooth Loco](https://github.com/tunggsten/Yeentooth-Engine/blob/main/logo.png?raw=true)
# Yeentooth Engine - A simple 3D game engine made for my A-Level Computer Science coursework.

### This is a simple game engine made with Python, Tkinter and Pygame. This is meant for demonstration rather than actual use (since I'm sure most people don't want their game to run sequentially on one cpu core), but if I make it faster in the future then maybe I'll use it for something.

![A rotating rainbow cube in a grey room, rendered with Yeentooth](https://github.com/tunggsten/Yeentooth-Engine/blob/main/graphics.gif)

## **Features:**

 * Intuitive Object System

In Yeentooth, everything is built up of Abstracts. 
Abstracts are points in 3D space, which have a set of axes their children lie and move on. Scenes in games are heirachies of abstracts, which will be able to be saved and loaded into other scenes as Hyperstracts (.hstrct) files

You can use abstract parenting to create movement systems quickly and easily, and you have fine control over both local and global coordinates.

 * Bespoke rendering engine

Yeentooth uses custom implementations of common graphical and mathematical functions, from matrix multiplication to triangle filling, ultimately built on top of Pygame. This makes it easier to modify and expand apon depending on your needs.

## **Planned features**
