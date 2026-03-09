"""
Benchmark Algorithms for Comparison
====================================
Implements standard image processing filters for comparison with Lo Shu algorithm.
"""

import numpy as np
from scipy import ndimage
from typing import Optional


class BenchmarkFilters:
    """
    Collection of benchmark filters for comparison.
    """
    
    @staticmethod
    def mean_filter(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
        """
        Apply mean (average) filter.
        
        Args:
            image: Input image
            kernel_size: Size of averaging kernel
            
        Returns:
            Filtered image
        """
        if image.ndim == 2:
            return ndimage.uniform_filter(image.astype(float), size=kernel_size)
        elif image.ndim == 3:
            result = np.zeros_like(image, dtype=float)
            for c in range(image.shape[2]):
                result[:, :, c] = ndimage.uniform_filter(image[:, :, c].astype(float), size=kernel_size)
            return result
        else:
            raise ValueError("Image must be 2D or 3D")
    
    @staticmethod
    def gaussian_filter(image: np.ndarray, kernel_size: int = 3, sigma: Optional[float] = None) -> np.ndarray:
        """
        Apply Gaussian filter.
        
        Args:
            image: Input image
            kernel_size: Size of Gaussian kernel
            sigma: Standard deviation of Gaussian (default: kernel_size/6)
            
        Returns:
            Filtered image
        """
        if sigma is None:
            sigma = kernel_size / 6.0
        
        if image.ndim == 2:
            return ndimage.gaussian_filter(image.astype(float), sigma=sigma)
        elif image.ndim == 3:
            result = np.zeros_like(image, dtype=float)
            for c in range(image.shape[2]):
                result[:, :, c] = ndimage.gaussian_filter(image[:, :, c].astype(float), sigma=sigma)
            return result
        else:
            raise ValueError("Image must be 2D or 3D")
    
    @staticmethod
    def median_filter(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
        """
        Apply median filter.
        
        Args:
            image: Input image
            kernel_size: Size of median filter kernel
            
        Returns:
            Filtered image
        """
        if image.ndim == 2:
            return ndimage.median_filter(image, size=kernel_size)
        elif image.ndim == 3:
            result = np.zeros_like(image)
            for c in range(image.shape[2]):
                result[:, :, c] = ndimage.median_filter(image[:, :, c], size=kernel_size)
            return result
        else:
            raise ValueError("Image must be 2D or 3D")
    
    @staticmethod
    def bilateral_filter(image: np.ndarray, diameter: int = 9, sigma_color: float = 75, 
                         sigma_space: float = 75) -> np.ndarray:
        """
        Apply bilateral filter (edge-preserving smoothing).
        
        Note: This is a simplified implementation. For production use,
        consider using OpenCV's cv2.bilateralFilter.
        
        Args:
            image: Input image
            diameter: Diameter of each pixel neighborhood
            sigma_color: Filter sigma in the color space
            sigma_space: Filter sigma in the coordinate space
            
        Returns:
            Filtered image
        """
        # Simplified bilateral filter approximation
        if image.ndim == 3:
            image_gray = np.mean(image, axis=2)
        else:
            image_gray = image
        
        # Gaussian smoothing
        smoothed = ndimage.gaussian_filter(image_gray.astype(float), sigma=sigma_space/3)
        
        # Edge-aware blending
        gradient = np.abs(ndimage.laplace(image_gray.astype(float)))
        edge_mask = gradient / (np.max(gradient) + 1e-10)
        
        # Blend based on edge strength
        result = smoothed * (1 - edge_mask * 0.5) + image_gray.astype(float) * (edge_mask * 0.5)
        
        if image.ndim == 3:
            result_3d = np.zeros_like(image, dtype=float)
            for c in range(image.shape[2]):
                result_3d[:, :, c] = result
            return result_3d
        
        return result
    
    @staticmethod
    def bayer_dither(image: np.ndarray, bits: int = 4) -> np.ndarray:
        """
        Apply Bayer dithering matrix for color reduction.
        
        Args:
            image: Input image
            bits: Number of bits for color reduction
            
        Returns:
            Dithered image
        """
        # 4x4 Bayer matrix
        bayer_matrix = np.array([
            [0, 8, 2, 10],
            [12, 4, 14, 6],
            [3, 11, 1, 9],
            [15, 7, 13, 5]
        ]) / 16.0
        
        if image.ndim == 3:
            result = np.zeros_like(image)
            for c in range(image.shape[2]):
                result[:, :, c] = BayerFilters._apply_dither(image[:, :, c], bayer_matrix, bits)
            return result
        else:
            return BayerFilters._apply_dither(image, bayer_matrix, bits)
    
    @staticmethod
    def _apply_dither(channel: np.ndarray, bayer_matrix: np.ndarray, bits: int) -> np.ndarray:
        """Apply dithering to a single channel."""
        h, w = channel.shape
        levels = 2 ** bits
        
        # Tile Bayer matrix
        tiled_bayer = np.tile(bayer_matrix, (h // 4 + 1, w // 4 + 1))[:h, :w]
        
        # Apply dithering
        dithered = channel.astype(float) + tiled_bayer * (256 / levels)
        dithered = (dithered / 256) * levels
        dithered = np.floor(dithered) * (256 / levels)
        
        return np.clip(dithered, 0, 255)


class BayerFilters:
    """
    Bayer matrix operations for color filter array processing.
    """
    
    # Standard Bayer pattern
    BAYER_PATTERN = np.array([
        ['R', 'G'],
        ['G', 'B']
    ])
    
    @staticmethod
    def get_bayer_mask(image: np.ndarray, color: str = 'R') -> np.ndarray:
        """
        Get mask for specific color channel in Bayer pattern.
        
        Args:
            image: Input image
            color: Color channel ('R', 'G', or 'B')
            
        Returns:
            Boolean mask
        """
        h, w = image.shape[:2]
        mask = np.zeros((h, w), dtype=bool)
        
        if color == 'R':
            mask[::2, ::2] = True
        elif color == 'B':
            mask[1::2, 1::2] = True
        elif color == 'G':
            mask[::2, 1::2] = True
            mask[1::2, ::2] = True
        
        return mask
    
    @staticmethod
    def demosaic_bayer(bayer_image: np.ndarray) -> np.ndarray:
        """
        Simple bilinear demosaicing of Bayer pattern image.
        
        Args:
            bayer_image: Raw Bayer pattern image
            
        Returns:
            Demosaiced RGB image
        """
        h, w = bayer_image.shape
        rgb = np.zeros((h, w, 3), dtype=float)
        
        # Red channel
        rgb[::2, ::2, 0] = bayer_image[::2, ::2]
        rgb[::2, 1::2, 0] = (bayer_image[::2, ::2] + bayer_image[::2, 2::2]) / 2
        rgb[1::2, ::2, 0] = (bayer_image[::2, ::2] + bayer_image[2::2, ::2]) / 2
        rgb[1::2, 1::2, 0] = (bayer_image[::2, ::2] + bayer_image[::2, 2::2] + 
                              bayer_image[2::2, ::2] + bayer_image[2::2, 2::2]) / 4
        
        # Blue channel
        rgb[1::2, 1::2, 2] = bayer_image[1::2, 1::2]
        rgb[1::2, ::2, 2] = (bayer_image[1::2, 1::2] + bayer_image[1::2, 3::2]) / 2
        rgb[::2, 1::2, 2] = (bayer_image[1::2, 1::2] + bayer_image[3::2, 1::2]) / 2
        rgb[::2, ::2, 2] = (bayer_image[1::2, 1::2] + bayer_image[1::2, 3::2] + 
                           bayer_image[3::2, 1::2] + bayer_image[3::2, 3::2]) / 4
        
        # Green channel
        rgb[::2, 1::2, 1] = bayer_image[::2, 1::2]
        rgb[1::2, ::2, 1] = bayer_image[1::2, ::2]
        rgb[::2, ::2, 1] = (bayer_image[::2, 1::2] + bayer_image[::2, 3::2] + 
                           bayer_image[2::2, 1::2] + bayer_image[2::2, 3::2]) / 4
        rgb[1::2, 1::2, 1] = (bayer_image[1::2, ::2] + bayer_image[1::2, 2::2] + 
                             bayer_image[3::2, ::2] + bayer_image[3::2, 2::2]) / 4
        
        # Handle boundaries
        rgb = np.clip(rgb, 0, 255)
        
        return rgb
