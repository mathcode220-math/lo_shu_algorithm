"""
Lo Shu Balance Algorithm for Image Denoising
=============================================
Core implementation of the Lo Shu Balance Algorithm for image processing.
"""

import numpy as np
from typing import Tuple, Optional
from lo_shu_matrix import LoShuMatrix


class LoShuBalanceFilter:
    """
    Lo Shu Balance Algorithm for image denoising.
    
    This algorithm uses the unique properties of the Lo Shu Magic Square
    to achieve balanced noise reduction while preserving important details.
    
    Key Properties Used:
    1. Magic Constant (15): Ensures balanced distribution across dimensions
    2. Central Anchor (5): Provides stable reference point
    3. Diagonal Interference Cancellation: Opposite pairs sum to 10
    """
    
    def __init__(self, kernel_size: int = 3):
        """
        Initialize the Lo Shu Balance Filter.
        
        Args:
            kernel_size: Size of processing kernel (default 3x3)
        """
        if kernel_size != 3:
            raise ValueError("Lo Shu algorithm requires 3x3 kernel size")
        
        self.kernel_size = kernel_size
        self.lo_shu = LoShuMatrix()
        self.weights = self.lo_shu.get_weights_for_kernel()
    
    def _extract_patches(self, image: np.ndarray, patch_size: int) -> np.ndarray:
        """
        Extract overlapping patches from image.
        
        Args:
            image: Input image (2D array)
            patch_size: Size of patches to extract
            
        Returns:
            Array of shape (n_patches_h, n_patches_w, patch_size, patch_size)
        """
        h, w = image.shape
        patches_h = h - patch_size + 1
        patches_w = w - patch_size + 1
        
        patches = np.zeros((patches_h, patches_w, patch_size, patch_size), dtype=image.dtype)
        
        for i in range(patches_h):
            for j in range(patches_w):
                patches[i, j] = image[i:i+patch_size, j:j+patch_size]
        
        return patches
    
    def _apply_lo_shu_weighting(self, patch: np.ndarray) -> float:
        """
        Apply Lo Shu weighted averaging to a single patch.
        
        Uses Lo Shu values as weights for balanced averaging.
        
        Args:
            patch: 3x3 image patch
            
        Returns:
            Weighted average pixel value
        """
        # Apply Lo Shu weights
        weighted_sum = np.sum(patch.astype(np.float64) * self.weights)
        # Normalize by sum of weights (which is 1.0 already)
        return weighted_sum
    
    def _apply_bit_reversal(self, value: int, lo_shu_weight: int, bit_depth: int = 8) -> int:
        """
        Apply bit-reversal operation based on Lo Shu weight.
        
        Higher Lo Shu weights preserve more bits, lower weights apply more reversal.
        
        Args:
            value: Pixel value
            lo_shu_weight: Lo Shu weight (1-9)
            bit_depth: Bit depth of image
            
        Returns:
            Modified pixel value
        """
        if bit_depth == 8:
            max_val = 255
        else:
            max_val = (1 << bit_depth) - 1
        
        # Calculate bit preservation ratio based on Lo Shu weight
        # Higher weight = more bits preserved
        preservation_ratio = lo_shu_weight / 9.0
        
        # Apply weighted bit preservation
        preserved_bits = int(value * preservation_ratio)
        
        # Add dithering based on position
        dither_amount = int((1 - preservation_ratio) * (max_val * 0.1))
        if dither_amount > 0:
            preserved_bits += np.random.randint(-dither_amount, dither_amount + 1)
        
        return np.clip(preserved_bits, 0, max_val)
    
    def _distribute_quantization_error(self, image: np.ndarray, 
                                        error: np.ndarray,
                                        i: int, j: int) -> None:
        """
        Distribute quantization error using Lo Shu magic paths.
        
        Args:
            image: Image array (modified in place)
            error: Quantization error to distribute
            i, j: Position of the error source
        """
        h, w = image.shape
        
        # Distribute error to neighbors using Lo Shu weights
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if di == 0 and dj == 0:
                    continue
                
                ni, nj = i + di + 1, j + dj + 1
                
                if 0 <= ni < h and 0 <= nj < w:
                    # Get Lo Shu weight for this direction
                    lo_shu_weight = self.lo_shu.get_weight(di + 1, dj + 1)
                    # Normalize weight (exclude center)
                    normalized_weight = lo_shu_weight / (self.lo_shu.MAGIC_CONSTANT - self.lo_shu.CENTER_VALUE)
                    
                    # Distribute error proportionally
                    image[ni, nj] += error * normalized_weight * 0.5
    
    def apply(self, image: np.ndarray, preserve_edges: bool = True) -> np.ndarray:
        """
        Apply Lo Shu Balance Filter to an image.
        
        Args:
            image: Input image (2D grayscale or 3D RGB)
            preserve_edges: Whether to preserve edge details
            
        Returns:
            Filtered image
        """
        if image.ndim == 2:
            return self._apply_grayscale(image, preserve_edges)
        elif image.ndim == 3:
            # Process each channel separately
            result = np.zeros_like(image)
            for c in range(image.shape[2]):
                result[:, :, c] = self._apply_grayscale(image[:, :, c], preserve_edges)
            return result
        else:
            raise ValueError("Image must be 2D (grayscale) or 3D (RGB)")
    
    def _apply_grayscale(self, image: np.ndarray, preserve_edges: bool) -> np.ndarray:
        """
        Apply filter to grayscale image.
        
        Args:
            image: 2D grayscale image
            preserve_edges: Whether to preserve edge details
            
        Returns:
            Filtered image
        """
        h, w = image.shape
        result = np.zeros_like(image, dtype=np.float64)
        
        # Pad image to handle borders
        padded = np.pad(image.astype(np.float64), pad_width=1, mode='reflect')
        
        # Sliding window approach
        for i in range(h):
            for j in range(w):
                # Extract 3x3 patch centered at (i, j)
                patch = padded[i:i+3, j:j+3]
                
                # Apply Lo Shu weighted averaging
                result[i, j] = self._apply_lo_shu_weighting(patch)
        
        # Edge preservation enhancement
        if preserve_edges:
            result = self._enhance_edges(image.astype(np.float64), result)
        
        return np.clip(result, 0, 255).astype(image.dtype)
    
    def _enhance_edges(self, original: np.ndarray, filtered: np.ndarray) -> np.ndarray:
        """
        Enhance edges by blending original and filtered based on edge strength.
        
        Args:
            original: Original image
            filtered: Filtered image
            
        Returns:
            Edge-enhanced image
        """
        # Calculate gradient magnitude (simple Sobel approximation)
        grad_x = np.abs(np.diff(original, axis=1))
        grad_x = np.pad(grad_x, ((0, 0), (1, 0)), mode='reflect')
        
        grad_y = np.abs(np.diff(original, axis=0))
        grad_y = np.pad(grad_y, ((1, 0), (0, 0)), mode='reflect')
        
        gradient = grad_x + grad_y
        
        # Normalize gradient to 0-1 range
        grad_norm = gradient / (np.max(gradient) + 1e-10)
        
        # Blend: more original at edges, more filtered in smooth areas
        blend_factor = 0.7  # Base blending factor
        enhanced = filtered * (1 - grad_norm * blend_factor) + original * (grad_norm * blend_factor)
        
        return enhanced
    
    def apply_with_error_diffusion(self, image: np.ndarray) -> np.ndarray:
        """
        Apply Lo Shu filter with quantization error diffusion.
        
        This method distributes quantization error using Lo Shu magic paths,
        converting random noise into structured patterns less visible to human eye.
        
        Args:
            image: Input image
            
        Returns:
            Filtered image with error diffusion
        """
        result = image.astype(np.float64).copy()
        h, w = result.shape
        
        for i in range(h):
            for j in range(w):
                # Get original value
                original = result[i, j]
                
                # Extract patch if possible
                if i > 0 and i < h-1 and j > 0 and j < w-1:
                    patch = result[i-1:i+2, j-1:j+2]
                    filtered = self._apply_lo_shu_weighting(patch)
                else:
                    filtered = original
                
                # Calculate quantization error
                error = original - filtered
                
                # Apply filtered value
                result[i, j] = filtered
                
                # Distribute error to neighbors
                if i < h-2 and j < w-2:
                    self._distribute_quantization_error(result, error, i, j)
        
        return np.clip(result, 0, 255).astype(image.dtype)


def lo_shu_denoise(image: np.ndarray, method: str = 'standard') -> np.ndarray:
    """
    Convenience function for Lo Shu denoising.
    
    Args:
        image: Input image
        method: 'standard' or 'error_diffusion'
        
    Returns:
        Denoised image
    """
    filter_obj = LoShuBalanceFilter()
    
    if method == 'standard':
        return filter_obj.apply(image)
    elif method == 'error_diffusion':
        return filter_obj.apply_with_error_diffusion(image)
    else:
        raise ValueError(f"Unknown method: {method}")
