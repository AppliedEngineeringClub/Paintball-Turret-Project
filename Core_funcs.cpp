#include "core.hpp"        // for Core definition
#include <iostream>         // for std::cout, std::cerr
#include <stdexcept>        // for std::runtime_error
#include <cstdlib>          // for std::system
#include <fstream>          // for std::ifstream, std::ofstream
#include <cstddef>          // for std::size_t
#include <cstdint>          // for uint8_t
#include <string>           // for std::string
#include <limits>           // for std::numeric_limits
#include <array>            // for std::array
#include <vector>           // for std::vector

namespace {
// Very small helper to extract an integer after a given JSON key in a tiny file.
// This is not a general JSON parser; it just finds e.g. "width": 123.
bool extractIntFromJson(const std::string& path, const std::string& key, long& out) {
    std::ifstream in(path);
    if (!in) return false;
    std::string s((std::istreambuf_iterator<char>(in)), std::istreambuf_iterator<char>());
    auto pos = s.find('"' + key + '"');
    if (pos == std::string::npos) return false;
    pos = s.find(':', pos);
    if (pos == std::string::npos) return false;
    // Move past ':' and whitespace
    ++pos;
    while (pos < s.size() && (s[pos] == ' ' || s[pos] == '\t')) ++pos;
    // Read number
    bool neg = false;
    if (pos < s.size() && s[pos] == '-') { neg = true; ++pos; }
    long val = 0; bool any = false;
    while (pos < s.size() && std::isdigit(static_cast<unsigned char>(s[pos]))) {
        any = true;
        val = val * 10 + (s[pos] - '0');
        ++pos;
    }
    if (!any) return false;
    out = neg ? -val : val;
    return true;
}
}

void Core::imageProcessor() {
    const int CHANNELS = 3;  // R, G, B

    // Try to generate outputs with Python helper (non-fatal if missing Pillow).
    // Preferred: get_matrix_data.py writes image/out/pythonoutput.bin and meta.json
    // Fallbacks handled below.
    (void)std::system("python3 python/get_matrix_data.py > /dev/null 2>&1");

    // First attempt: read width/height from image/out/meta.json (written by get_matrix_data.py)
    long w = -1, h = -1;
    if (!extractIntFromJson("image/out/meta.json", "width", w) ||
        !extractIntFromJson("image/out/meta.json", "height", h)) {
        // Second attempt: use legacy get_dimensions.py which writes pythonoutput.txt
        if (std::system("python3 python/get_dimensions.py > /dev/null 2>&1") == 0) {
            std::ifstream din("pythonoutput.txt");
            if (din) {
                din >> w >> h;
            }
        }
    }

    if (w <= 0 || h <= 0) {
        // Final fallback: pick a tiny default so the program can run
        w = 8; h = 8;
        std::cerr << "Warning: could not determine image dimensions; using "
                  << w << "x" << h << " fallback.\n";
    }

    origWidth  = static_cast<std::size_t>(w);
    origHeight = static_cast<std::size_t>(h);
    m = origWidth;
    n = origHeight;

    matrix.clear();
    matrix.resize(static_cast<std::size_t>(CHANNELS) * origHeight * origWidth);

    // Try to read raw RGB bytes. Preferred path written by get_matrix_data.py
    auto read_bin = [&](const std::string& path) -> bool {
        std::ifstream in(path, std::ios::binary);
        if (!in) return false;
        in.read(reinterpret_cast<char*>(matrix.data()),
                static_cast<std::streamsize>(matrix.size() * sizeof(uint8_t)));
        return static_cast<std::size_t>(in.gcount()) == matrix.size() * sizeof(uint8_t);
    };

    bool ok = read_bin("image/out/pythonoutput.bin");
    if (!ok) {
        ok = read_bin("pythonoutput.bin");
    }
    if (!ok) {
        // If still not available, fill with a simple gradient so downstream logic can proceed.
        for (std::size_t y = 0; y < origHeight; ++y) {
            for (std::size_t x = 0; x < origWidth; ++x) {
                std::size_t idx = (y * origWidth + x) * CHANNELS;
                matrix[idx + 0] = static_cast<uint8_t>((x * 255) / (origWidth  ? origWidth - 1  : 1));
                matrix[idx + 1] = static_cast<uint8_t>((y * 255) / (origHeight ? origHeight - 1 : 1));
                matrix[idx + 2] = 0;
            }
        }
        std::cerr << "Warning: no binary pixel data found; generated a test gradient instead.\n";
    }

    // Debug: Either print first few values or entire matrix if requested
    {
        const char* env = std::getenv("PRINT_FULL_MATRIX");
        bool print_full = (env && *env);
        if (!print_full) {
            std::size_t maxToPrint = std::min<std::size_t>(matrix.size(), 10);
            std::cout << "Debug: first " << maxToPrint << " values of matrix: ";
            for (std::size_t i = 0; i < maxToPrint; ++i) {
                std::cout << static_cast<int>(matrix[i]) << ' ';
            }
            std::cout << "\n";
        } else {
            std::cout << "Debug: printing full matrix (" << origHeight << "x" << origWidth
                      << "x" << CHANNELS << ") as rows of (r,g,b) values\n";
            for (std::size_t y = 0; y < origHeight; ++y) {
                for (std::size_t x = 0; x < origWidth; ++x) {
                    std::size_t idx = (y * origWidth + x) * CHANNELS;
                    int r = static_cast<int>(matrix[idx + 0]);
                    int g = static_cast<int>(matrix[idx + 1]);
                    int b = static_cast<int>(matrix[idx + 2]);
                    std::cout << '(' << r << ',' << g << ',' << b << ')';
                    if (x + 1 < origWidth) std::cout << ' ';
                }
                std::cout << '\n';
            }
        }
    }

    std::cout << "Core::imageProcessor(): matrix ready ("
              << CHANNELS << " × " << origHeight << " × " << origWidth << ")\n";
}

// mapToNearestColor: replace each pixel with the nearest color from the palette (by RGB distance)
void Core::mapToNearestColor(const std::vector<std::array<uint8_t,3>>& palette) {
    if (palette.empty() || matrix.empty()) {
        return;
    }

    const std::size_t CHANNELS = 3; // expecting RGB
    if (matrix.size() % CHANNELS != 0) {
        // malformed matrix; do nothing
        return;
    }

    const std::size_t pixelCount = matrix.size() / CHANNELS;

    for (std::size_t i = 0; i < pixelCount; ++i) {
        const std::size_t idx = i * CHANNELS;
        const int r = static_cast<int>(matrix[idx + 0]);
        const int g = static_cast<int>(matrix[idx + 1]);
        const int b = static_cast<int>(matrix[idx + 2]);

        std::uint32_t bestDist = std::numeric_limits<std::uint32_t>::max();
        std::size_t bestIdx = 0;

        for (std::size_t p = 0; p < palette.size(); ++p) {
            const int pr = static_cast<int>(palette[p][0]);
            const int pg = static_cast<int>(palette[p][1]);
            const int pb = static_cast<int>(palette[p][2]);

            const int dr = r - pr;
            const int dg = g - pg;
            const int db = b - pb;

            const std::uint32_t dist = static_cast<std::uint32_t>(dr * dr + dg * dg + db * db);
            if (dist < bestDist) {
                bestDist = dist;
                bestIdx = p;
            }
        }

        matrix[idx + 0] = palette[bestIdx][0];
        matrix[idx + 1] = palette[bestIdx][1];
        matrix[idx + 2] = palette[bestIdx][2];
    }
}

// reduceBlocks implementation stub
Core Core::reduceBlocks(std::size_t /*blockM*/, std::size_t /*blockN*/) const {
    // TODO: implement block reduction logic
    return Core(0, 0);
}
    // TODO: implement matrix-to-balls logic 

// matrixToBalls implementation stub
void Core::matrixToBalls() {
   // this will be mono lithic and prob use bash for the linux comands 
   // tranlate to comands for the moters

    // use pgio pins 
    // methid one is gen a script and send it all at one time 
    // methid 2 live input 
    // methid 3 
    // check for limits and not over doing it on speed and angle lim 
    // moter one gpio 12 is x and gpio 13 is y 
    
}

void Core::displayWallSimulation(){
    // input form maxrix 
// (void)std::system("python3 python/DisplayWallSimulattion.py > /dev/null 2>&1");
}
