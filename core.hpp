// core.hpp
#ifndef CORE_HPP
#define CORE_HPP

#include <vector>
#include <cstddef>  // for size_t
#include <cstdint>  // for uint8_t
#include <array>
struct Core {
    std::size_t m;  // number of columns (width)
    std::size_t n;  // number of rows (height)
// Original image dimensions (set during imageProcessor)
    std::size_t origWidth;   // number of columns of the original image
    std::size_t origHeight;  // number of rows of the original image

    std::size_t canvasWidth; // height of the canvas in pixels
    std::size_t canvasHeight; // width of the canvas in pixels

    // 3D data: channels × n × m
    // flattened into a 1D vector. Each entry is one channel value (0-255).
    std::vector<uint8_t> matrix;
     // Constructor
     // Constructor
    Core(std::size_t width = 0, std::size_t height = 0)
      : m(width), n(height), origWidth(width), origHeight(height), matrix() {}

    // imageProcessor will allocate/populate matrix to size (3 * n * m) for 3 channels.
    void imageProcessor();
// 2. Nearest-Color Mapper: map each pixel’s color in matrix to nearest in palette
    void mapToNearestColor(const std::vector<std::array<uint8_t,3>>& palette);
// 3. Pixel Averaging Function — block reduction (2D → smaller 2D)
    Core reduceBlocks(std::size_t blockM, std::size_t blockN) const;
// 4. Matrix to Balls - Compute the require paintballs. Data contains: color, distance, yaw + pitch, for each paintball
    void matrixToBalls();
// 5. Wall — Matrix-Driven Balls: interpret the list of balls and paints it on the pygame canvas
    void displayWallSimulation(/*balls*/);
};

#endif // CORE_HPP
