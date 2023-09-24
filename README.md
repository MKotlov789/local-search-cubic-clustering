#  local Search Algorithm for Cubic Clustering

 This repository contains classes and code related to the cubic partition problem, a fundamental task in subspace clustering. Subspace clustering is a technique used to estimate the number and normal vectors of planes from a set of noisy point samples in 3D space.
This repository presents the implementation of the educational project "A local Search Algorithm for Cubic Clustering" provided by the Machine Learning for Computer Vision
Chair at the Institute of Artificial Intelligence of the Faculty of Computer Science of TU Dresden.


## Table of Contents

- [Overview](#overview)
- [Classes](#classes)
- [Usage](#usage)
- [References](#references)

## Overview

The cubic partition problem plays a crucial role in various applications, such as estimating planes from a set of noisy point samples in 3D space. Given a set of points, the goal is to partition them into subsets that belong to the same plane or distinct planes. This partitioning is essential for identifying the number of planes and their respective normal vectors.

To address this problem, the Subspace Clustering Application provides classes and algorithms that analyze triples of points to determine their assignment to planes. By fitting planes through the origin and evaluating the cost of grouping three points based on their distances from that plane, this application tackles the cubic partition problem.

## Classes

### `GreedyMovingKl`

The `GreedyMovingKl` class extends `_BaseGreedyClustering` and implements a greedy clustering algorithm designed for the cubic partition problem. It performs iterative clustering based on minimizing the objective function, aiming to find an optimal clustering solution. It provides methods for moving points between clusters, calculating objective function changes.


### `InstanceOfProblem`

The `InstanceOfProblem` class represents an instance of the cubic partition problem. It defines the problem's parameters, including the set of points, their distances from planes, normal vectors of planes.

## Usage

You can utilize the classes provided in this repository to perform subspace clustering for problems like the cubic partition problem. The classes offer algorithms and utilities for clustering noisy point samples into meaningful subsets, enabling you to estimate the number and normal vectors of planes.

You can run a main.py that demonstrates the application of the algorithm to a instance of the problem with 2 planes and 16 points

## References
 
1. [https://mlcv.inf.tu-dresden.de/index.html](https://mlcv.inf.tu-dresden.de/index.html): Machine Learning for Computer Vision
Chair at the Institute of Artificial Intelligence of the Faculty of Computer Science of TU Dresden.

2. [Kernighan, B. W., & Lin, S. (1970)](https://ieeexplore.ieee.org/document/6771083) - An efficient heuristic procedure for partitioning graphs.

3. [Beier, T., Kroeger, T., Kappes, J. H., Kothe, U., & Hamprecht, F. A. (2014)](https://ieeexplore.ieee.org/document/6909789) - Cut, glue & cut: A fast, approximate solver for multicut partitioning.

4. [Bagon, S., & Galun, M. (2011)](https://arxiv.org/abs/1104.3719) - Optimizing large-scale correlation clustering.

5. [Branch, M. A., Coleman, T. F., & Li, Y. (1999)](https://epubs.siam.org/doi/abs/10.1137/S1064827593255720) - A subspace, interior, and conjugate gradient method for large-scale bound-constrained minimization problems.

6. [Zhao, L., Nagamochi, H., & Ibaraki, T. (2005)](https://link.springer.com/article/10.1007/s10107-005-0589-0) - Greedy splitting algorithms for approximating multiway partition problems.

Feel free to explore the code and adapt it to your specific subspace clustering needs. If you have any questions or need assistance, please don't hesitate to reach out to the repository's contributors.

**Note**: This repository is intended for educational and research purposes in the field of subspace clustering.
