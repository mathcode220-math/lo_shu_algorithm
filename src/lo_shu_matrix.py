"""
Lo Shu Magic Square Core Implementation
========================================
Implements the 3x3 Lo Shu Magic Square and its mathematical properties.
"""

import numpy as np
from typing import Tuple, List


class LoShuMatrix:
    """
    Represents the Lo Shu Magic Square (3x3) and its properties.
    
    The Lo Shu square is:
        8  1  6
        3  5  7
        4  9  2
    
    Properties:
    - Magic Constant: Sum of any row, column, or diagonal = 15
    - Central Anchor: 5 (median and center)
    - Diagonal Pairs: Opposite pairs sum to 10
    """
    
    # The canonical Lo Shu 3x3 magic square
    MATRIX = np.array([
        [8, 1, 6],
        [3, 5, 7],
        [4, 9, 2]
    ], dtype=np.int32)
    
    MAGIC_CONSTANT = 15
    CENTER_VALUE = 5
    DIAGONAL_SUM = 10
    
    def __init__(self):
        self._matrix = self.MATRIX.copy()
    
    @property
    def matrix(self) -> np.ndarray:
        """Returns the Lo Shu matrix."""
        return self._matrix
    
    @property
    def magic_constant(self) -> int:
        """Returns the magic constant (15)."""
        return self.MAGIC_CONSTANT
    
    @property
    def center_value(self) -> int:
        """Returns the center value (5)."""
        return self.CENTER_VALUE
    
    def get_weight(self, row: int, col: int) -> int:
        """Get the weight value at a specific position."""
        return self._matrix[row, col]
    
    def get_normalized_weight(self, row: int, col: int) -> float:
        """
        Get normalized weight (0.0 to 1.0) based on position.
        Normalized by dividing by 9 (max value in Lo Shu).
        """
        return self._matrix[row, col] / 9.0
    
    def get_diagonal_pair(self, row: int, col: int) -> Tuple[int, int]:
        """
        Get the diagonal pair values that sum to 10.
        Returns (center_value, opposite_value).
        """
        center = self.CENTER_VALUE
        value = self._matrix[row, col]
        opposite = self.DIAGONAL_SUM - value + center - center  # Simplified to 10 - value + adjustment
        return (value, 10 - value)
    
    def get_magic_paths(self) -> List[List[Tuple[int, int]]]:
        """
        Returns all magic paths (rows, columns, diagonals) as coordinate lists.
        """
        paths = []
        
        # Rows
        for i in range(3):
            paths.append([(i, j) for j in range(3)])
        
        # Columns
        for j in range(3):
            paths.append([(i, j) for i in range(3)])
        
        # Diagonals
        paths.append([(i, i) for i in range(3)])
        paths.append([(i, 2-i) for i in range(3)])
        
        return paths
    
    def verify_magic_constant(self) -> bool:
        """
        Verify that all rows, columns, and diagonals sum to the magic constant.
        """
        # Check rows
        for i in range(3):
            if np.sum(self._matrix[i, :]) != self.MAGIC_CONSTANT:
                return False
        
        # Check columns
        for j in range(3):
            if np.sum(self._matrix[:, j]) != self.MAGIC_CONSTANT:
                return False
        
        # Check diagonals
        if np.trace(self._matrix) != self.MAGIC_CONSTANT:
            return False
        if np.trace(np.fliplr(self._matrix)) != self.MAGIC_CONSTANT:
            return False
        
        return True
    
    def get_weights_for_kernel(self) -> np.ndarray:
        """
        Returns normalized weights suitable for convolution kernel.
        Weights sum to 1.0.
        """
        return self._matrix.astype(np.float64) / np.sum(self._matrix)
    
    def __str__(self) -> str:
        return str(self._matrix)
    
    def __repr__(self) -> str:
        return f"LoShuMatrix(MAGIC_CONSTANT={self.MAGIC_CONSTANT})"
